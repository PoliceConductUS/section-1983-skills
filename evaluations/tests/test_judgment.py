import json
import math
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from evaluations.judgment import (
    CandidateProtocolError,
    JudgmentProtocolError,
    aggregate_judgments,
    run_candidate,
    run_judgments,
)


FIXTURE = {
    "id": "judgment-fixture",
    "prompt": "Review the synthetic candidate.",
    "sources": [{"id": "SRC-1", "content": "Synthetic source."}],
    "candidate": "Synthetic candidate [cite:SRC-1].",
    "rubric": [
        {"id": "source-boundary", "description": "Uses bounded sources only."},
        {"id": "no-silent-edit", "description": "Does not edit the draft."},
    ],
}


FAKE_JUDGE = """import json
import os
import sys
import time

request = json.load(sys.stdin)
mode = sys.argv[1]
if mode == "timeout":
    time.sleep(3)
criteria = [item["id"] for item in request["rubric"]]
if mode == "missing":
    criteria = criteria[:-1]
elif mode == "duplicate":
    criteria.append(criteria[0])
elif mode == "unknown":
    criteria.append("unknown-criterion")
details = {
    "cwd": os.getcwd(),
    "entries": os.listdir(),
    "request": request,
}
fixture_id = request["fixture_id"]
run_id = request["run_id"]
if mode == "wrong-fixture":
    fixture_id = "other-fixture"
elif mode == "wrong-run":
    run_id = "other-run"
response = {
    "fixture_id": fixture_id,
    "run_id": run_id,
    "decisions": [
        {
            "criterion_id": criterion,
            "passed": True,
            "reason": json.dumps(details, sort_keys=True),
        }
        for criterion in criteria
    ],
}
if mode == "missing-reason":
    response["decisions"][0].pop("reason")
elif mode == "empty-reason":
    response["decisions"][0]["reason"] = ""
elif mode == "non-boolean":
    response["decisions"][0]["passed"] = "true"
json.dump(response, sys.stdout)
"""


FAKE_CANDIDATE = """import json
import os
import sys
import time

request = json.load(sys.stdin)
if sys.argv[1] == "timeout":
    time.sleep(3)
environment_keys = (
    "PREFIX_CONVERSATION_SUFFIX",
    "SESSION_TOKEN_EXTRA",
    "AGENT_THREAD_CONTEXT",
    "MiXeD_SeSsIoN_Key",
    "PWD",
    "OLDPWD",
    "EVALUATION_API_KEY",
)
details = {
    "cwd": os.getcwd(),
    "entries": os.listdir(),
    "request": request,
    "environment": {
        key: os.environ[key]
        for key in environment_keys
        if key in os.environ
    },
}
response = {"output": json.dumps(details, sort_keys=True)}
if sys.argv[1] == "missing-output":
    response = {"result": "wrong-field"}
json.dump(response, sys.stdout)
"""


class CandidateRunnerTest(unittest.TestCase):

    def write_fake_candidate(self, directory):
        candidate = Path(directory) / "fake_candidate.py"
        candidate.write_text(FAKE_CANDIDATE)
        return candidate

    def test_public_runners_apply_default_timeout_to_short_commands(self):
        with tempfile.TemporaryDirectory() as root:
            candidate = self.write_fake_candidate(root)
            judge = Path(root) / "fake_judge.py"
            judge.write_text(FAKE_JUDGE)

            candidate_result = run_candidate(
                FIXTURE,
                [sys.executable, str(candidate), "valid"],
                run_id="candidate-default-timeout",
            )
            judgment_result = run_judgments(
                FIXTURE,
                [sys.executable, str(judge), "valid"],
                repetitions=3,
            )

        self.assertIn("output", candidate_result)
        self.assertTrue(judgment_result["available"])
        self.assertEqual(len(judgment_result["runs"]), 3)

    def test_each_candidate_invocation_uses_a_new_process_and_empty_working_directory(self):
        with tempfile.TemporaryDirectory() as root:
            candidate = self.write_fake_candidate(root)
            command = [sys.executable, str(candidate), "valid"]

            first = run_candidate(
                FIXTURE, command, run_id="candidate-1", timeout_seconds=2
            )
            second = run_candidate(
                FIXTURE, command, run_id="candidate-2", timeout_seconds=2
            )

        details = [json.loads(first["output"]), json.loads(second["output"])]
        self.assertEqual(len({item["cwd"] for item in details}), 2)
        self.assertTrue(all(item["entries"] == [] for item in details))
        requests = [item["request"] for item in details]
        self.assertEqual(
            {request["run_id"] for request in requests},
            {"candidate-1", "candidate-2"},
        )
        for request in requests:
            self.assertEqual(request["fixture_id"], FIXTURE["id"])
            self.assertEqual(request["prompt"], FIXTURE["prompt"])
            self.assertEqual(request["sources"], FIXTURE["sources"])
            self.assertTrue(
                {"fixture_id", "prompt", "run_id", "sources"}.issubset(request)
            )
            self.assertTrue(
                {"conversation_id", "provider_session_id", "session_id"}.isdisjoint(
                    request
                )
            )

    def test_rejects_candidate_response_without_output(self):
        with tempfile.TemporaryDirectory() as root:
            candidate = self.write_fake_candidate(root)

            with self.assertRaises(CandidateProtocolError):
                run_candidate(
                    FIXTURE,
                    [sys.executable, str(candidate), "missing-output"],
                    run_id="candidate-1",
                    timeout_seconds=2,
                )

    def test_child_environment_removes_context_keys_and_working_directory_state(self):
        seeded_environment = {
            "PREFIX_CONVERSATION_SUFFIX": "synthetic-context",
            "SESSION_TOKEN_EXTRA": "synthetic-session",
            "AGENT_THREAD_CONTEXT": "synthetic-thread",
            "MiXeD_SeSsIoN_Key": "synthetic-mixed",
            "PWD": "/synthetic/pwd",
            "OLDPWD": "/synthetic/oldpwd",
            "EVALUATION_API_KEY": "synthetic-allowed-credential",
        }
        with tempfile.TemporaryDirectory() as root:
            candidate = self.write_fake_candidate(root)
            with mock.patch.dict(os.environ, seeded_environment, clear=False):
                result = run_candidate(
                    FIXTURE,
                    [sys.executable, str(candidate), "valid"],
                    run_id="candidate-environment",
                    timeout_seconds=2,
                )

        environment = json.loads(result["output"])["environment"]
        self.assertEqual(
            environment,
            {"EVALUATION_API_KEY": "synthetic-allowed-credential"},
        )

    def test_candidate_rejects_invalid_timeout_before_command_execution(self):
        for timeout_seconds in (
            0,
            -1,
            True,
            False,
            math.nan,
            math.inf,
            -math.inf,
        ):
            with self.subTest(timeout=timeout_seconds), tempfile.TemporaryDirectory() as root:
                root_path = Path(root)
                sentinel = root_path / "executed"
                command = root_path / "sentinel.py"
                command.write_text(
                    "from pathlib import Path\n"
                    "import sys\n"
                    "Path(sys.argv[1]).write_text('executed')\n"
                )

                with self.assertRaises(ValueError):
                    run_candidate(
                        FIXTURE,
                        [sys.executable, str(command), str(sentinel)],
                        run_id="candidate-timeout-validation",
                        timeout_seconds=timeout_seconds,
                    )

                self.assertFalse(sentinel.exists())

    def test_candidate_timeout_is_bounded_and_uses_stable_protocol_error(self):
        with tempfile.TemporaryDirectory() as root:
            candidate = self.write_fake_candidate(root)
            started = time.monotonic()

            with self.assertRaisesRegex(CandidateProtocolError, "timeout"):
                run_candidate(
                    FIXTURE,
                    [sys.executable, str(candidate), "timeout"],
                    run_id="candidate-timeout",
                    timeout_seconds=0.05,
                )

            self.assertLess(time.monotonic() - started, 1)


class JudgmentRunnerTest(unittest.TestCase):

    def write_fake_judge(self, directory):
        judge = Path(directory) / "fake_judge.py"
        judge.write_text(FAKE_JUDGE)
        return judge

    def test_every_repetition_uses_a_new_process_and_empty_working_directory(self):
        with tempfile.TemporaryDirectory() as root:
            judge = self.write_fake_judge(root)

            result = run_judgments(
                FIXTURE,
                [sys.executable, str(judge), "valid"],
                repetitions=3,
                timeout_seconds=2,
            )

        self.assertTrue(result["available"])
        self.assertEqual(len(result["runs"]), 3)
        details = [
            json.loads(run["decisions"][0]["reason"]) for run in result["runs"]
        ]
        self.assertEqual(len({item["cwd"] for item in details}), 3)
        self.assertTrue(all(item["entries"] == [] for item in details))
        requests = [item["request"] for item in details]
        self.assertEqual(len({request["run_id"] for request in requests}), 3)
        for request in requests:
            self.assertEqual(request["fixture_id"], FIXTURE["id"])
            self.assertEqual(request["prompt"], FIXTURE["prompt"])
            self.assertEqual(request["sources"], FIXTURE["sources"])
            self.assertEqual(request["candidate"], FIXTURE["candidate"])
            self.assertEqual(request["rubric"], FIXTURE["rubric"])
            self.assertTrue(
                {
                    "candidate",
                    "fixture_id",
                    "prompt",
                    "rubric",
                    "run_id",
                    "sources",
                }.issubset(request)
            )
            self.assertTrue(
                {"conversation_id", "provider_session_id", "session_id"}.isdisjoint(
                    request
                )
            )

    def test_rejects_missing_duplicate_and_unknown_rubric_decisions(self):
        with tempfile.TemporaryDirectory() as root:
            judge = self.write_fake_judge(root)

            for mode in ("missing", "duplicate", "unknown"):
                with self.subTest(mode=mode), self.assertRaises(
                    JudgmentProtocolError
                ):
                    run_judgments(
                        FIXTURE,
                        [sys.executable, str(judge), mode],
                        repetitions=3,
                        timeout_seconds=2,
                    )

    def test_rejects_invalid_fixture_run_reason_and_passed_protocol_values(self):
        modes = (
            "wrong-fixture",
            "wrong-run",
            "missing-reason",
            "empty-reason",
            "non-boolean",
        )

        with tempfile.TemporaryDirectory() as root:
            judge = self.write_fake_judge(root)

            for mode in modes:
                with self.subTest(mode=mode), self.assertRaises(
                    JudgmentProtocolError
                ):
                    run_judgments(
                        FIXTURE,
                        [sys.executable, str(judge), mode],
                        repetitions=3,
                        timeout_seconds=2,
                    )

    def test_requires_at_least_three_repetitions(self):
        with self.assertRaisesRegex(ValueError, "at least three"):
            run_judgments(
                FIXTURE,
                [sys.executable, "unused.py"],
                repetitions=2,
                timeout_seconds=2,
            )

    def test_judgment_rejects_invalid_timeout_before_command_execution(self):
        for timeout_seconds in (
            0,
            -1,
            True,
            False,
            math.nan,
            math.inf,
            -math.inf,
        ):
            with self.subTest(timeout=timeout_seconds), tempfile.TemporaryDirectory() as root:
                root_path = Path(root)
                sentinel = root_path / "executed"
                command = root_path / "sentinel.py"
                command.write_text(
                    "from pathlib import Path\n"
                    "import sys\n"
                    "Path(sys.argv[1]).write_text('executed')\n"
                )

                with self.assertRaises(ValueError):
                    run_judgments(
                        FIXTURE,
                        [sys.executable, str(command), str(sentinel)],
                        repetitions=3,
                        timeout_seconds=timeout_seconds,
                    )

                self.assertFalse(sentinel.exists())

    def test_judgment_timeout_is_bounded_and_uses_stable_protocol_error(self):
        with tempfile.TemporaryDirectory() as root:
            judge = self.write_fake_judge(root)
            started = time.monotonic()

            with self.assertRaisesRegex(JudgmentProtocolError, "timeout"):
                run_judgments(
                    FIXTURE,
                    [sys.executable, str(judge), "timeout"],
                    repetitions=3,
                    timeout_seconds=0.05,
                )

            self.assertLess(time.monotonic() - started, 1)

    def test_marks_unconfigured_or_unexecutable_judgment_unavailable(self):
        cases = (None, ["command-that-does-not-exist-issue-6"])

        for command in cases:
            with self.subTest(command=command):
                result = run_judgments(
                    FIXTURE, command, repetitions=3, timeout_seconds=2
                )

                self.assertFalse(result["available"])
                self.assertEqual(result["runs"], [])
                self.assertIn("unavailable", result["reason"].lower())
                self.assertNotIn("passed", result)
                self.assertNotIn("criteria", result)


class JudgmentAggregationTest(unittest.TestCase):

    def test_reports_pass_rate_variance_instability_and_raw_reasons(self):
        runs = []
        outcomes = (True, True, False)
        for index, passed in enumerate(outcomes, start=1):
            runs.append(
                {
                    "fixture_id": "judgment-fixture",
                    "run_id": f"run-{index}",
                    "decisions": [
                        {
                            "criterion_id": "source-boundary",
                            "passed": passed,
                            "reason": f"reason-{index}",
                        }
                    ],
                }
            )

        aggregate = aggregate_judgments(
            "judgment-fixture",
            [{"id": "source-boundary", "description": "Uses bounded sources."}],
            runs,
        )

        criterion = aggregate["criteria"]["source-boundary"]
        self.assertEqual(criterion["passes"], 2)
        self.assertEqual(criterion["run_count"], 3)
        self.assertAlmostEqual(criterion["pass_rate"], 2 / 3)
        self.assertAlmostEqual(criterion["variance"], 2 / 9)
        self.assertTrue(criterion["unstable"])
        self.assertEqual(
            criterion["decisions"],
            [
                {"run_id": "run-1", "passed": True, "reason": "reason-1"},
                {"run_id": "run-2", "passed": True, "reason": "reason-2"},
                {"run_id": "run-3", "passed": False, "reason": "reason-3"},
            ],
        )


if __name__ == "__main__":
    unittest.main()
