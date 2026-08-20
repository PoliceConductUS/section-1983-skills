import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from evaluations.reporting import (
    compare_baseline,
    render_json,
    render_markdown,
    report_exit_status,
)


def evaluation_result():
    return {
        "fixtures": [
            {
                "fixture_id": "fixture-one",
                "deterministic": {
                    "passed": True,
                    "pass_count": 1,
                    "findings": [],
                },
                "judgment": {
                    "available": True,
                    "criteria": {
                        "source-boundary": {
                            "passes": 2,
                            "run_count": 3,
                            "pass_rate": 2 / 3,
                            "variance": 2 / 9,
                            "unstable": True,
                            "decisions": [],
                        }
                    },
                },
            }
        ],
        "regressions": [],
    }


def write_command_fixture(corpus):
    fixture = corpus / "fixture-one"
    fixture.mkdir(parents=True)
    (fixture / "prompt.md").write_text("Synthetic prompt.\n")
    (fixture / "source.md").write_text("Synthetic source.\n")
    (fixture / "sources.json").write_text(
        json.dumps([{"id": "SRC-1", "path": "source.md"}])
    )
    (fixture / "passing.md").write_text("# Result\n\n[SRC-1]\n")
    (fixture / "regression.md").write_text("")
    manifest = {
        "id": "fixture-one",
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
            {"id": "source-boundary", "description": "Uses bounded sources."}
        ],
    }
    (fixture / "fixture.json").write_text(json.dumps(manifest))
    return fixture


class BaselineComparisonTest(unittest.TestCase):

    def test_reports_deterministic_and_judgment_regressions_without_editing_baseline(self):
        current = evaluation_result()
        baseline = {
            "fixtures": {
                "fixture-one": {
                    "minimum_deterministic_pass_count": 2,
                    "minimum_judgment_pass_rates": {"source-boundary": 0.75},
                }
            }
        }
        original = json.dumps(baseline, sort_keys=True)

        findings = compare_baseline(current, baseline)

        self.assertEqual(
            {finding["id"] for finding in findings},
            {"baseline-deterministic-regression", "baseline-judgment-regression"},
        )
        self.assertEqual(
            {
                (
                    finding["fixture_id"],
                    finding["metric"],
                    finding["minimum"],
                    finding["current"],
                )
                for finding in findings
            },
            {
                ("fixture-one", "deterministic_pass_count", 2, 1),
                ("fixture-one", "source-boundary.pass_rate", 0.75, 2 / 3),
            },
        )
        self.assertEqual(json.dumps(baseline, sort_keys=True), original)


class ReportRenderingTest(unittest.TestCase):

    def test_json_and_markdown_render_the_same_fixture_and_regression_state(self):
        report = evaluation_result()
        report["regressions"] = [
            {
                "id": "baseline-judgment-regression",
                "fixture_id": "fixture-one",
                "metric": "source-boundary.pass_rate",
                "minimum": 0.75,
                "current": 2 / 3,
            }
        ]

        json_report = json.loads(render_json(report))
        markdown_report = render_markdown(report)

        self.assertEqual(json_report, report)
        self.assertIn("fixture-one", markdown_report)
        self.assertIn("source-boundary", markdown_report)
        self.assertIn("0.666", markdown_report)
        self.assertIn("0.222", markdown_report)
        self.assertIn("unstable", markdown_report.lower())
        self.assertIn("baseline-judgment-regression", markdown_report)

    def test_report_exit_status_is_nonzero_for_a_regression(self):
        passing = evaluation_result()
        failing = evaluation_result()
        failing["regressions"] = [
            {"id": "baseline-deterministic-regression", "fixture_id": "fixture-one"}
        ]

        self.assertEqual(report_exit_status(passing), 0)
        self.assertNotEqual(report_exit_status(failing), 0)

    def test_markdown_never_labels_unavailable_judgment_as_passed(self):
        report = evaluation_result()
        report["fixtures"][0]["judgment"] = {
            "available": False,
            "reason": "Judgment command unavailable.",
            "runs": [],
        }

        markdown = render_markdown(report).lower()

        self.assertIn("judgment", markdown)
        self.assertIn("unavailable", markdown)
        self.assertNotIn("judgment passed", markdown)
        self.assertNotIn("judgment: passed", markdown)
        self.assertNotIn("| judgment | passed |", markdown)


class EvaluationCommandTest(unittest.TestCase):

    def run_evaluation(
        self,
        root,
        fixture_changes=None,
        baseline_changes=None,
        candidate_command=None,
        judgment_command=None,
    ):
        corpus = Path(root) / "corpus"
        fixture = write_command_fixture(corpus)
        if fixture_changes:
            manifest_path = fixture / "fixture.json"
            manifest = json.loads(manifest_path.read_text())
            fixture_changes(manifest)
            manifest_path.write_text(json.dumps(manifest))
        baseline = {
            "fixtures": {
                "fixture-one": {
                    "minimum_deterministic_pass_count": 1,
                    "minimum_judgment_pass_rates": {},
                }
            }
        }
        if baseline_changes:
            baseline_changes(baseline)
        baseline_path = Path(root) / "baseline.json"
        baseline_path.write_text(json.dumps(baseline))
        json_output = Path(root) / "result.json"
        markdown_output = Path(root) / "result.md"
        command = [
            sys.executable,
            "-m",
            "evaluations.cli",
            "--corpus",
            str(corpus),
            "--baseline",
            str(baseline_path),
            "--json-output",
            str(json_output),
            "--markdown-output",
            str(markdown_output),
        ]
        if candidate_command:
            command.extend(
                ["--candidate-command-json", json.dumps(candidate_command)]
            )
        if judgment_command:
            command.extend(
                ["--judgment-command-json", json.dumps(judgment_command)]
            )
        completed = subprocess.run(command, text=True, capture_output=True)
        return completed, json_output, markdown_output

    def test_command_accepts_expected_findings_as_a_subset_and_writes_both_reports(self):
        with tempfile.TemporaryDirectory() as root:
            completed, json_output, markdown_output = self.run_evaluation(root)

            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(json_output.read_text())
            markdown = markdown_output.read_text()

        fixture = result["fixtures"][0]
        permanent = fixture["permanent_regressions"][0]
        self.assertEqual(permanent["id"], "missing-citation")
        self.assertTrue(
            {"citation-missing"}.issubset(permanent["observed_findings"])
        )
        self.assertIn("heading-missing", permanent["observed_findings"])
        self.assertTrue(permanent["expectation_met"])
        judgment = fixture["judgment"]
        self.assertFalse(judgment["available"])
        self.assertNotIn("passed", judgment)
        self.assertNotIn("criteria", judgment)
        self.assertIn("judgment", markdown.lower())
        self.assertIn("unavailable", markdown.lower())
        self.assertIn("missing-citation", markdown)
        judgment_status_lines = [
            line.casefold()
            for line in markdown.splitlines()
            if "judgment" in line.casefold()
        ]
        self.assertTrue(judgment_status_lines)
        for line in judgment_status_lines:
            self.assertNotRegex(line, r"\bpass(?:ed)?\b")

    def test_command_returns_nonzero_for_permanent_or_baseline_regression(self):
        def mismatch_expected_findings(manifest):
            manifest["regressions"][0]["expected_findings"] = ["banned-pattern"]

        def raise_baseline(baseline):
            baseline["fixtures"]["fixture-one"][
                "minimum_deterministic_pass_count"
            ] = 2

        cases = (
            (mismatch_expected_findings, None),
            (None, raise_baseline),
        )

        for fixture_changes, baseline_changes in cases:
            with self.subTest(
                fixture_regression=fixture_changes is not None
            ), tempfile.TemporaryDirectory() as root:
                completed, json_output, markdown_output = self.run_evaluation(
                    root,
                    fixture_changes=fixture_changes,
                    baseline_changes=baseline_changes,
                )

                self.assertNotEqual(completed.returncode, 0)
                result = json.loads(json_output.read_text())
                self.assertTrue(result["regressions"])
                self.assertTrue(markdown_output.read_text())

    def test_command_returns_nonzero_for_deterministic_candidate_failure(self):
        def select_failing_candidate(manifest):
            manifest["passing_candidate"] = "regression.md"

        with tempfile.TemporaryDirectory() as root:
            completed, json_output, markdown_output = self.run_evaluation(
                root, fixture_changes=select_failing_candidate
            )

            self.assertNotEqual(completed.returncode, 0)
            result = json.loads(json_output.read_text())
            self.assertIn(
                "deterministic-candidate-failure",
                {finding["id"] for finding in result["regressions"]},
            )
            self.assertIn("deterministic", markdown_output.read_text().lower())

    def test_invalid_corpus_prevents_configured_candidate_and_judge_execution(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            sentinel_command = root_path / "sentinel_command.py"
            sentinel_command.write_text(
                "from pathlib import Path\n"
                "import sys\n"
                "Path(sys.argv[1]).write_text('executed')\n"
            )
            candidate_sentinel = root_path / "candidate-executed"
            judge_sentinel = root_path / "judge-executed"

            def remove_synthetic(manifest):
                manifest.pop("synthetic")

            completed, _, _ = self.run_evaluation(
                root,
                fixture_changes=remove_synthetic,
                candidate_command=[
                    sys.executable,
                    str(sentinel_command),
                    str(candidate_sentinel),
                ],
                judgment_command=[
                    sys.executable,
                    str(sentinel_command),
                    str(judge_sentinel),
                ],
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(candidate_sentinel.exists())
            self.assertFalse(judge_sentinel.exists())


if __name__ == "__main__":
    unittest.main()
