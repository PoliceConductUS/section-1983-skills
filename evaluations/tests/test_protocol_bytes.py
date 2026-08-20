import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

from evaluations.judgment import (
    STREAM_LIMIT,
    TRUNCATION_MARKER,
    CandidateProtocolError,
    JudgmentProtocolError,
    run_candidate,
    run_judgments,
)


REPOSITORY = Path(__file__).resolve().parents[2]


def evaluation_fixture():
    return {
        "id": "protocol-fixture",
        "prompt": "Review the bounded synthetic record.",
        "sources": [{"id": "SRC-1", "content": "Synthetic source."}],
        "source_ids": ["SRC-1"],
        "candidate": "# Result\n\n[cite:SRC-1]\n",
        "deterministic": {
            "required_fields": [],
            "ordered_headings": ["Result"],
            "banned_terms": [],
            "banned_patterns": [],
            "required_citations": ["SRC-1"],
        },
        "rubric": [
            {
                "id": "bounded-source",
                "description": "Uses only the supplied synthetic source.",
            }
        ],
    }


def write_script(directory, name, body):
    path = Path(directory) / name
    path.write_text(textwrap.dedent(body))
    return path


def write_cli_inputs(directory):
    root = Path(directory)
    fixture_directory = root / "corpus" / "protocol-fixture"
    fixture_directory.mkdir(parents=True)
    (fixture_directory / "prompt.md").write_text("Review the synthetic record.\n")
    (fixture_directory / "source.md").write_text("Synthetic source.\n")
    (fixture_directory / "sources.json").write_text(
        json.dumps([{"id": "SRC-1", "path": "source.md"}])
    )
    (fixture_directory / "passing.md").write_text("# Result\n\n[cite:SRC-1]\n")
    (fixture_directory / "regression.md").write_text("# Result\n")
    manifest = {
        "id": "protocol-fixture",
        "synthetic": True,
        "target_skill": "filing-ci",
        "prompt": "prompt.md",
        "sources": "sources.json",
        "passing_candidate": "passing.md",
        "regressions": [
            {
                "id": "missing-citation",
                "candidate": "regression.md",
                "expected_findings": ["citation-missing"],
            }
        ],
        "deterministic": {
            "required_fields": [],
            "ordered_headings": ["Result"],
            "banned_terms": [],
            "banned_patterns": [],
            "required_citations": ["SRC-1"],
        },
        "rubric": [
            {
                "id": "bounded-source",
                "description": "Uses only the supplied synthetic source.",
            }
        ],
    }
    (fixture_directory / "fixture.json").write_text(json.dumps(manifest))
    baseline = root / "baseline.json"
    baseline.write_text(
        json.dumps(
            {
                "fixtures": {
                    "protocol-fixture": {
                        "minimum_deterministic_pass_count": 1,
                        "minimum_judgment_pass_rates": {},
                    }
                }
            }
        )
    )
    return root / "corpus", baseline


def run_cli(directory, candidate_command=None, judgment_command=None):
    root = Path(directory)
    corpus, baseline = write_cli_inputs(root)
    json_report = root / "report.json"
    markdown_report = root / "report.md"
    command = [
        sys.executable,
        "-m",
        "evaluations.cli",
        "--corpus",
        str(corpus),
        "--baseline",
        str(baseline),
        "--json-output",
        str(json_report),
        "--markdown-output",
        str(markdown_report),
    ]
    if candidate_command is not None:
        command.extend(["--candidate-command-json", json.dumps(candidate_command)])
    if judgment_command is not None:
        command.extend(["--judgment-command-json", json.dumps(judgment_command)])
    completed = subprocess.run(
        command,
        cwd=REPOSITORY,
        text=True,
        capture_output=True,
        check=False,
    )
    return completed, json_report, markdown_report


class ProtocolBoundaryTest(unittest.TestCase):

    def assert_bounded_replacement_text(self, value):
        self.assertIn("\ufffd", value)
        self.assertLessEqual(len(value), STREAM_LIMIT)
        self.assertTrue(value.endswith(TRUNCATION_MARKER))

    def assert_cli_failure_report(
        self,
        completed,
        json_report,
        markdown_report,
        finding_id,
    ):
        self.assertNotEqual(completed.returncode, 0)
        self.assertTrue(json_report.is_file(), completed.stderr)
        self.assertTrue(markdown_report.is_file(), completed.stderr)
        report = json.loads(json_report.read_text())
        findings = [
            finding
            for finding in report["regressions"]
            if finding["id"] == finding_id
        ]
        self.assertEqual(len(findings), 1)
        self.assertIn(finding_id, markdown_report.read_text())
        return findings[0]

    def test_unhashable_judgment_criterion_is_stable_protocol_failure(self):
        fixture = evaluation_fixture()
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(
                directory,
                "unhashable_criterion.py",
                """
                import json
                import sys

                request = json.load(sys.stdin)
                criterion = json.loads(sys.argv[1])
                response = {
                    "fixture_id": request["fixture_id"],
                    "run_id": request["run_id"],
                    "decisions": [
                        {
                            "criterion_id": criterion,
                            "passed": True,
                            "reason": "Synthetic reason.",
                        }
                    ],
                    "padding": "x" * 9000,
                }
                print(json.dumps(response))
                """,
            )
            for criterion in (["bounded-source"], {"id": "bounded-source"}):
                with self.subTest(criterion=criterion):
                    with self.assertRaises(JudgmentProtocolError) as captured:
                        run_judgments(
                            fixture,
                            [sys.executable, str(script), json.dumps(criterion)],
                            3,
                        )

                    self.assertEqual(
                        captured.exception.finding_id,
                        "judgment-response-incomplete",
                    )
                    self.assertLessEqual(len(captured.exception.stdout), STREAM_LIMIT)

    def test_unhashable_judgment_criterion_produces_bounded_cli_report(self):
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(
                directory,
                "unhashable_criterion_cli.py",
                """
                import json
                import sys

                request = json.load(sys.stdin)
                criterion = json.loads(sys.argv[1])
                print(json.dumps({
                    "fixture_id": request["fixture_id"],
                    "run_id": request["run_id"],
                    "decisions": [{
                        "criterion_id": criterion,
                        "passed": True,
                        "reason": "Synthetic reason.",
                    }],
                    "padding": "x" * 9000,
                }))
                """,
            )
            for index, criterion in enumerate(
                (["bounded-source"], {"id": "bounded-source"})
            ):
                with self.subTest(criterion=criterion):
                    run_directory = Path(directory) / f"run-{index}"
                    run_directory.mkdir()
                    completed, json_report, markdown_report = run_cli(
                        run_directory,
                        judgment_command=[
                            sys.executable,
                            str(script),
                            json.dumps(criterion),
                        ],
                    )
                    finding = self.assert_cli_failure_report(
                        completed,
                        json_report,
                        markdown_report,
                        "judgment-response-incomplete",
                    )
                    self.assertLessEqual(len(finding["stdout"]), STREAM_LIMIT)
                    self.assertTrue(finding["stdout"].endswith(TRUNCATION_MARKER))

    def test_invalid_utf8_stdout_is_stable_malformed_response(self):
        fixture = evaluation_fixture()
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(
                directory,
                "invalid_stdout.py",
                """
                import sys

                sys.stdin.buffer.read()
                sys.stdout.buffer.write(b"\\xff" + b"x" * 9000)
                """,
            )
            cases = (
                (
                    "candidate",
                    CandidateProtocolError,
                    "candidate-response-malformed-json",
                    lambda: run_candidate(
                        fixture,
                        [sys.executable, str(script)],
                        "candidate-run",
                    ),
                ),
                (
                    "judgment",
                    JudgmentProtocolError,
                    "judgment-response-malformed-json",
                    lambda: run_judgments(
                        fixture,
                        [sys.executable, str(script)],
                        3,
                    ),
                ),
            )
            for label, error_type, finding_id, invoke in cases:
                with self.subTest(agent=label):
                    with self.assertRaises(error_type) as captured:
                        invoke()

                    self.assertEqual(captured.exception.finding_id, finding_id)
                    self.assert_bounded_replacement_text(captured.exception.stdout)

    def test_invalid_utf8_stdout_produces_stable_cli_reports(self):
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(
                directory,
                "invalid_stdout_cli.py",
                """
                import sys

                sys.stdin.buffer.read()
                sys.stdout.buffer.write(b"\\xff" + b"x" * 9000)
                """,
            )
            cases = (
                ("candidate", "candidate-response-malformed-json"),
                ("judgment", "judgment-response-malformed-json"),
            )
            for index, (agent, finding_id) in enumerate(cases):
                with self.subTest(agent=agent):
                    run_directory = Path(directory) / f"run-{index}"
                    run_directory.mkdir()
                    arguments = {f"{agent}_command": [sys.executable, str(script)]}
                    completed, json_report, markdown_report = run_cli(
                        run_directory,
                        **arguments,
                    )
                    finding = self.assert_cli_failure_report(
                        completed,
                        json_report,
                        markdown_report,
                        finding_id,
                    )
                    self.assert_bounded_replacement_text(finding["stdout"])

    def test_invalid_utf8_stderr_with_valid_json_is_bounded_protocol_failure(self):
        fixture = evaluation_fixture()
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(
                directory,
                "invalid_stderr.py",
                """
                import json
                import sys

                sys.stdin.buffer.read()
                sys.stdout.write(json.dumps({"output": "Synthetic output."}))
                sys.stdout.flush()
                sys.stderr.buffer.write(b"\\xff" + b"e" * 9000)
                raise SystemExit(7)
                """,
            )
            cases = (
                (
                    "candidate",
                    CandidateProtocolError,
                    "candidate-command-nonzero",
                    lambda: run_candidate(
                        fixture,
                        [sys.executable, str(script)],
                        "candidate-run",
                    ),
                ),
                (
                    "judgment",
                    JudgmentProtocolError,
                    "judgment-command-nonzero",
                    lambda: run_judgments(
                        fixture,
                        [sys.executable, str(script)],
                        3,
                    ),
                ),
            )
            for label, error_type, finding_id, invoke in cases:
                with self.subTest(agent=label):
                    with self.assertRaises(error_type) as captured:
                        invoke()

                    self.assertEqual(captured.exception.finding_id, finding_id)
                    self.assert_bounded_replacement_text(captured.exception.stderr)

    def test_invalid_utf8_stderr_is_bounded_in_cli_reports(self):
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(
                directory,
                "invalid_stderr_cli.py",
                """
                import json
                import sys

                sys.stdin.buffer.read()
                sys.stdout.write(json.dumps({"output": "Synthetic output."}))
                sys.stdout.flush()
                sys.stderr.buffer.write(b"\\xff" + b"e" * 9000)
                raise SystemExit(7)
                """,
            )
            cases = (
                ("candidate", "candidate-command-nonzero"),
                ("judgment", "judgment-command-nonzero"),
            )
            for index, (agent, finding_id) in enumerate(cases):
                with self.subTest(agent=agent):
                    run_directory = Path(directory) / f"run-{index}"
                    run_directory.mkdir()
                    arguments = {f"{agent}_command": [sys.executable, str(script)]}
                    completed, json_report, markdown_report = run_cli(
                        run_directory,
                        **arguments,
                    )
                    finding = self.assert_cli_failure_report(
                        completed,
                        json_report,
                        markdown_report,
                        finding_id,
                    )
                    self.assert_bounded_replacement_text(finding["stderr"])


if __name__ == "__main__":
    unittest.main()
