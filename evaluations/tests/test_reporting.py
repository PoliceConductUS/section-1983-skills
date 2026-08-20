import json
import re
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

from evaluations.cli import build_parser
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
    (fixture / "passing.md").write_text("# Result\n\n[cite:SRC-1]\n")
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


def file_tree_snapshot(directory):
    root = Path(directory)
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def path_snapshot(path):
    target = Path(path)
    if target.is_symlink():
        resolved = target.resolve(strict=False)
        resolved_bytes = resolved.read_bytes() if resolved.is_file() else None
        return ("symlink", target.readlink().as_posix(), resolved_bytes)
    if not target.exists():
        return ("absent",)
    if target.is_file():
        return ("file", target.read_bytes())
    return ("directory", file_tree_snapshot(target))


def string_values(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [text for item in value.values() for text in string_values(item)]
    if isinstance(value, list):
        return [text for item in value for text in string_values(item)]
    return []


def captured_stream_values(value):
    streams = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key.casefold() in {"stdout", "stderr"} and isinstance(item, str):
                streams.append(item)
            streams.extend(captured_stream_values(item))
    elif isinstance(value, list):
        for item in value:
            streams.extend(captured_stream_values(item))
    return streams


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

    def test_unavailable_judgment_with_baseline_minimum_has_no_fabricated_rate(self):
        current = evaluation_result()
        current["fixtures"][0]["judgment"] = {
            "available": False,
            "reason": "Judgment command unavailable.",
            "runs": [],
        }
        baseline = {
            "fixtures": {
                "fixture-one": {
                    "minimum_deterministic_pass_count": 1,
                    "minimum_judgment_pass_rates": {"source-boundary": 0.75},
                }
            }
        }

        findings = compare_baseline(current, baseline)

        self.assertEqual(len(findings), 1)
        finding = findings[0]
        self.assertEqual(finding["id"], "baseline-judgment-unavailable")
        self.assertEqual(finding["fixture_id"], "fixture-one")
        self.assertEqual(finding["metric"], "source-boundary.pass_rate")
        self.assertEqual(finding["minimum"], 0.75)
        self.assertNotIn("current", finding)
        current["regressions"] = findings
        self.assertNotEqual(report_exit_status(current), 0)
        self.assertIn("baseline-judgment-unavailable", render_json(current))
        markdown = render_markdown(current)
        self.assertIn("baseline-judgment-unavailable", markdown)
        self.assertIn("unavailable", markdown.lower())
        self.assertIn("minimum 0.75", markdown.lower())
        self.assertNotIn("current 0", markdown.lower())


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

    def test_cli_default_timeout_is_sixty_seconds(self):
        arguments = build_parser().parse_args(
            [
                "--corpus",
                "synthetic-corpus",
                "--baseline",
                "synthetic-baseline.json",
                "--json-output",
                "synthetic-result.json",
                "--markdown-output",
                "synthetic-result.md",
            ]
        )

        self.assertEqual(arguments.command_timeout_seconds, 60)

    def run_evaluation(
        self,
        root,
        fixture_changes=None,
        baseline_changes=None,
        candidate_command=None,
        judgment_command=None,
        json_output=None,
        markdown_output=None,
        timeout_seconds=None,
        source_manifest_changes=None,
        before_command=None,
        baseline_replacement=None,
    ):
        corpus = Path(root) / "corpus"
        fixture = write_command_fixture(corpus)
        if source_manifest_changes:
            source_manifest_path = fixture / "sources.json"
            sources = json.loads(source_manifest_path.read_text())
            source_manifest_changes(sources)
            source_manifest_path.write_text(json.dumps(sources))
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
        if baseline_replacement:
            baseline = baseline_replacement(baseline)
        if baseline_changes:
            baseline_changes(baseline)
        baseline_path = Path(root) / "baseline.json"
        baseline_path.write_text(json.dumps(baseline))
        json_output = Path(json_output) if json_output else Path(root) / "result.json"
        markdown_output = (
            Path(markdown_output) if markdown_output else Path(root) / "result.md"
        )
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
        if timeout_seconds is not None:
            command.append(f"--command-timeout-seconds={timeout_seconds}")
        if before_command:
            before_command(
                {
                    "baseline": baseline_path,
                    "corpus": corpus,
                    "fixture": fixture,
                    "json_output": json_output,
                    "markdown_output": markdown_output,
                }
            )
        completed = subprocess.run(command, text=True, capture_output=True)
        return completed, json_output, markdown_output

    def test_command_rejects_output_paths_that_alias_inputs_or_each_other(self):
        cases = (
            "json-is-baseline",
            "markdown-is-baseline",
            "outputs-equal",
            "json-inside-corpus",
            "markdown-inside-corpus",
            "json-is-candidate",
            "json-symlink-to-baseline",
            "markdown-symlink-to-baseline",
            "outputs-symlink-to-same-file",
        )

        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as root:
                root_path = Path(root)
                baseline_path = root_path / "baseline.json"
                json_output = root_path / "result.json"
                markdown_output = root_path / "result.md"
                shared_output = None
                corpus_before = None
                configured_outputs_before = None
                ordinary_outputs_before = None
                if case == "json-is-baseline":
                    json_output = baseline_path
                elif case == "markdown-is-baseline":
                    markdown_output = baseline_path
                elif case == "outputs-equal":
                    json_output = markdown_output = root_path / "same-output"
                elif case == "json-inside-corpus":
                    json_output = root_path / "corpus" / "result.json"
                elif case == "markdown-inside-corpus":
                    markdown_output = root_path / "corpus" / "result.md"
                elif case == "json-is-candidate":
                    json_output = (
                        root_path / "corpus" / "fixture-one" / "passing.md"
                    )
                elif case == "json-symlink-to-baseline":
                    json_output.symlink_to(baseline_path)
                elif case == "markdown-symlink-to-baseline":
                    markdown_output.symlink_to(baseline_path)
                elif case == "outputs-symlink-to-same-file":
                    shared_output = root_path / "shared-output"
                    shared_output.write_text("shared sentinel")
                    json_output.symlink_to(shared_output)
                    markdown_output.symlink_to(shared_output)
                sentinel_command = root_path / "sentinel_command.py"
                sentinel_command.write_text(
                    "from pathlib import Path\n"
                    "import sys\n"
                    "Path(sys.argv[1]).write_text('executed')\n"
                )
                candidate_sentinel = root_path / "candidate-executed"
                judge_sentinel = root_path / "judge-executed"

                def snapshot_corpus(layout):
                    nonlocal corpus_before, configured_outputs_before, ordinary_outputs_before
                    corpus_before = file_tree_snapshot(layout["corpus"])
                    configured_outputs_before = (
                        path_snapshot(layout["json_output"]),
                        path_snapshot(layout["markdown_output"]),
                    )
                    ordinary_outputs_before = (
                        path_snapshot(root_path / "result.json"),
                        path_snapshot(root_path / "result.md"),
                    )

                completed, _, _ = self.run_evaluation(
                    root,
                    json_output=json_output,
                    markdown_output=markdown_output,
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
                    timeout_seconds=2,
                    before_command=snapshot_corpus,
                )

                self.assertNotEqual(completed.returncode, 0)
                self.assertNotIn("Traceback", completed.stderr)
                self.assertIn("configuration", completed.stderr.lower())
                self.assertLessEqual(len(completed.stderr.encode()), 4096)
                self.assertFalse(candidate_sentinel.exists())
                self.assertFalse(judge_sentinel.exists())
                self.assertEqual(
                    file_tree_snapshot(root_path / "corpus"), corpus_before
                )
                self.assertEqual(
                    (
                        path_snapshot(json_output),
                        path_snapshot(markdown_output),
                    ),
                    configured_outputs_before,
                )
                self.assertEqual(
                    (
                        path_snapshot(root_path / "result.json"),
                        path_snapshot(root_path / "result.md"),
                    ),
                    ordinary_outputs_before,
                )
                self.assertEqual(
                    baseline_path.read_text(),
                    json.dumps(
                        {
                            "fixtures": {
                                "fixture-one": {
                                    "minimum_deterministic_pass_count": 1,
                                    "minimum_judgment_pass_rates": {},
                                }
                            }
                        }
                    ),
                )
                if shared_output:
                    self.assertEqual(shared_output.read_text(), "shared sentinel")

    def test_output_preflight_preserves_existing_destination_in_both_orders(self):
        for invalid_format in ("json", "markdown"):
            with self.subTest(
                invalid_format=invalid_format
            ), tempfile.TemporaryDirectory() as root:
                root_path = Path(root)
                json_output = root_path / "result.json"
                markdown_output = root_path / "result.md"
                valid_output = markdown_output if invalid_format == "json" else json_output
                invalid_output = json_output if invalid_format == "json" else markdown_output
                valid_output.write_text("existing output sentinel")
                invalid_output.mkdir()
                outputs_before = (
                    path_snapshot(json_output),
                    path_snapshot(markdown_output),
                )

                completed, _, _ = self.run_evaluation(
                    root,
                    json_output=json_output,
                    markdown_output=markdown_output,
                    timeout_seconds=2,
                )

                self.assertNotEqual(completed.returncode, 0)
                self.assertNotIn("Traceback", completed.stderr)
                self.assertIn("configuration", completed.stderr.lower())
                self.assertLessEqual(len(completed.stderr.encode()), 4096)
                self.assertEqual(
                    (path_snapshot(json_output), path_snapshot(markdown_output)),
                    outputs_before,
                )

    def test_command_accepts_expected_findings_as_a_subset_and_writes_both_reports(self):
        with tempfile.TemporaryDirectory() as root:
            completed, json_output, markdown_output = self.run_evaluation(
                root, timeout_seconds=2
            )

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

    def test_command_reports_unavailable_judgment_against_baseline_minimum(self):
        def require_judgment_baseline(baseline):
            baseline["fixtures"]["fixture-one"][
                "minimum_judgment_pass_rates"
            ] = {"source-boundary": 0.75}

        with tempfile.TemporaryDirectory() as root:
            completed, json_output, markdown_output = self.run_evaluation(
                root, baseline_changes=require_judgment_baseline
            )

            self.assertNotEqual(completed.returncode, 0)
            result = json.loads(json_output.read_text())
            finding = next(
                item
                for item in result["regressions"]
                if item["id"] == "baseline-judgment-unavailable"
            )
            self.assertNotIn("current", finding)
            markdown = markdown_output.read_text()
            self.assertIn("baseline-judgment-unavailable", markdown)
            self.assertIn("unavailable", markdown.lower())
            self.assertIn("minimum 0.75", markdown.lower())
            self.assertNotIn("current 0", markdown.lower())

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

    def test_every_malformed_loader_contract_prevents_agent_execution(self):
        def contract_value(field, value):
            def change(manifest):
                manifest["deterministic"][field] = value

            return change

        def rubric_value(value):
            def change(manifest):
                manifest["rubric"] = value

            return change

        def manifest_value(field, value):
            def change(manifest):
                manifest[field] = value

            return change

        cases = (
            ("invalid-regex", contract_value("banned_patterns", [{"id": "bad", "pattern": "["}])),
            ("required-field-non-string", contract_value("required_fields", [7])),
            ("required-field-empty", contract_value("required_fields", [""])),
            ("heading-non-string", contract_value("ordered_headings", [7])),
            ("heading-empty", contract_value("ordered_headings", [""])),
            ("term-missing-id", contract_value("banned_terms", [{"term": "term"}])),
            ("term-empty-id", contract_value("banned_terms", [{"id": "", "term": "term"}])),
            ("term-missing-value", contract_value("banned_terms", [{"id": "term"}])),
            ("term-non-string", contract_value("banned_terms", [{"id": "term", "term": 7}])),
            ("term-empty", contract_value("banned_terms", [{"id": "term", "term": ""}])),
            ("pattern-missing-id", contract_value("banned_patterns", [{"pattern": "pattern"}])),
            ("pattern-empty-id", contract_value("banned_patterns", [{"id": "", "pattern": "pattern"}])),
            ("pattern-missing-value", contract_value("banned_patterns", [{"id": "pattern"}])),
            ("pattern-non-string", contract_value("banned_patterns", [{"id": "pattern", "pattern": 7}])),
            ("pattern-empty", contract_value("banned_patterns", [{"id": "pattern", "pattern": ""}])),
            ("citations-not-list", contract_value("required_citations", "SRC-1")),
            ("citation-non-string", contract_value("required_citations", [7])),
            ("citation-empty", contract_value("required_citations", [""])),
            ("rubric-id-missing", rubric_value([{"description": "Bounded."}])),
            ("rubric-id-empty", rubric_value([{"id": "", "description": "Bounded."}])),
            ("rubric-id-non-string", rubric_value([{"id": 7, "description": "Bounded."}])),
            ("rubric-description-missing", rubric_value([{"id": "bounded"}])),
            ("rubric-description-empty", rubric_value([{"id": "bounded", "description": ""}])),
            ("rubric-description-non-string", rubric_value([{"id": "bounded", "description": 7}])),
            ("fixture-id-empty", manifest_value("id", "")),
            ("target-skill-empty", manifest_value("target_skill", "")),
            (
                "regression-id-empty",
                lambda manifest: manifest["regressions"][0].update({"id": ""}),
            ),
            (
                "expected-findings-empty",
                lambda manifest: manifest["regressions"][0].update(
                    {"expected_findings": []}
                ),
            ),
            ("rubric-empty", rubric_value([])),
            (
                "required-fields-duplicate",
                contract_value(
                    "required_fields", ["analysis.result", "analysis.result"]
                ),
            ),
            (
                "headings-duplicate",
                contract_value("ordered_headings", ["Result", "Result"]),
            ),
            (
                "citations-duplicate",
                contract_value("required_citations", ["SRC-1", "SRC-1"]),
            ),
            (
                "expected-findings-duplicate",
                lambda manifest: manifest["regressions"][0].update(
                    {
                        "expected_findings": [
                            "citation-missing",
                            "citation-missing",
                        ]
                    }
                ),
            ),
        )

        for label, fixture_changes in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as root:
                root_path = Path(root)
                sentinel_command = root_path / "sentinel_command.py"
                sentinel_command.write_text(
                    "from pathlib import Path\n"
                    "import sys\n"
                    "Path(sys.argv[1]).write_text('executed')\n"
                )
                candidate_sentinel = root_path / "candidate-executed"
                judge_sentinel = root_path / "judge-executed"

                completed, _, _ = self.run_evaluation(
                    root,
                    fixture_changes=fixture_changes,
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

    def test_empty_source_identifier_prevents_agent_execution(self):
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

            def empty_source_identifier(sources):
                sources[0]["id"] = ""

            completed, _, _ = self.run_evaluation(
                root,
                source_manifest_changes=empty_source_identifier,
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
                timeout_seconds=2,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(candidate_sentinel.exists())
            self.assertFalse(judge_sentinel.exists())

    def test_malformed_baseline_prevents_agents_and_preserves_all_inputs_and_outputs(self):
        def replace_root(value):
            return lambda baseline: value

        def change_fixtures(value):
            def change(baseline):
                baseline["fixtures"] = value
                return baseline

            return change

        def change_fixture_minimums(value):
            def change(baseline):
                baseline["fixtures"]["fixture-one"] = value
                return baseline

            return change

        def change_deterministic_minimum(value):
            def change(baseline):
                baseline["fixtures"]["fixture-one"][
                    "minimum_deterministic_pass_count"
                ] = value
                return baseline

            return change

        def change_judgment_minimums(value):
            def change(baseline):
                baseline["fixtures"]["fixture-one"][
                    "minimum_judgment_pass_rates"
                ] = value
                return baseline

            return change

        cases = (
            ("root-array", replace_root([])),
            ("fixtures-array", change_fixtures([])),
            ("fixture-minimum-number", change_fixture_minimums(7)),
            ("deterministic-bool", change_deterministic_minimum(True)),
            ("deterministic-negative", change_deterministic_minimum(-1)),
            ("deterministic-float", change_deterministic_minimum(1.5)),
            ("deterministic-string", change_deterministic_minimum("1")),
            ("judgment-map-array", change_judgment_minimums([])),
            (
                "judgment-rate-bool",
                change_judgment_minimums({"source-boundary": True}),
            ),
            (
                "judgment-rate-string",
                change_judgment_minimums({"source-boundary": "0.5"}),
            ),
            (
                "judgment-rate-nan",
                change_judgment_minimums({"source-boundary": float("nan")}),
            ),
            (
                "judgment-rate-positive-infinity",
                change_judgment_minimums({"source-boundary": float("inf")}),
            ),
            (
                "judgment-rate-negative-infinity",
                change_judgment_minimums({"source-boundary": float("-inf")}),
            ),
            (
                "judgment-rate-negative",
                change_judgment_minimums({"source-boundary": -0.1}),
            ),
            (
                "judgment-rate-over-one",
                change_judgment_minimums({"source-boundary": 1.1}),
            ),
            (
                "unknown-fixture",
                change_fixtures(
                    {
                        "unknown-fixture": {
                            "minimum_deterministic_pass_count": 1,
                            "minimum_judgment_pass_rates": {},
                        }
                    }
                ),
            ),
            (
                "unknown-rubric",
                change_judgment_minimums({"unknown-rubric": 0.5}),
            ),
        )

        for label, baseline_replacement in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as root:
                root_path = Path(root)
                sentinel_command = root_path / "sentinel_command.py"
                sentinel_command.write_text(
                    "from pathlib import Path\n"
                    "import sys\n"
                    "Path(sys.argv[1]).write_text('executed')\n"
                )
                candidate_sentinel = root_path / "candidate-executed"
                judge_sentinel = root_path / "judge-executed"
                before = None

                def snapshot_layout(layout):
                    nonlocal before
                    before = {
                        "baseline": layout["baseline"].read_bytes(),
                        "corpus": file_tree_snapshot(layout["corpus"]),
                        "json": path_snapshot(layout["json_output"]),
                        "markdown": path_snapshot(layout["markdown_output"]),
                    }

                completed, json_output, markdown_output = self.run_evaluation(
                    root,
                    baseline_replacement=baseline_replacement,
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
                    timeout_seconds=2,
                    before_command=snapshot_layout,
                )

                self.assertNotEqual(completed.returncode, 0)
                self.assertNotIn("Traceback", completed.stderr)
                self.assertIn("configuration", completed.stderr.lower())
                self.assertLessEqual(len(completed.stderr.encode()), 4096)
                self.assertFalse(candidate_sentinel.exists())
                self.assertFalse(judge_sentinel.exists())
                self.assertEqual(
                    {
                        "baseline": (root_path / "baseline.json").read_bytes(),
                        "corpus": file_tree_snapshot(root_path / "corpus"),
                        "json": path_snapshot(json_output),
                        "markdown": path_snapshot(markdown_output),
                    },
                    before,
                )

    def test_cli_rejects_nonpositive_timeout_before_agent_execution(self):
        for timeout_seconds in (0, -1):
            with self.subTest(timeout=timeout_seconds), tempfile.TemporaryDirectory() as root:
                root_path = Path(root)
                sentinel_command = root_path / "sentinel_command.py"
                sentinel_command.write_text(
                    "from pathlib import Path\n"
                    "import sys\n"
                    "Path(sys.argv[1]).write_text('executed')\n"
                )
                candidate_sentinel = root_path / "candidate-executed"
                judge_sentinel = root_path / "judge-executed"

                completed, _, _ = self.run_evaluation(
                    root,
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
                    timeout_seconds=timeout_seconds,
                )

                self.assertNotEqual(completed.returncode, 0)
                self.assertFalse(candidate_sentinel.exists())
                self.assertFalse(judge_sentinel.exists())

    def test_cli_rejects_nonfinite_timeout_before_agents_or_output(self):
        for timeout_seconds in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(timeout=timeout_seconds), tempfile.TemporaryDirectory() as root:
                root_path = Path(root)
                sentinel_command = root_path / "sentinel_command.py"
                sentinel_command.write_text(
                    "from pathlib import Path\n"
                    "import sys\n"
                    "Path(sys.argv[1]).write_text('executed')\n"
                )
                candidate_sentinel = root_path / "candidate-executed"
                judge_sentinel = root_path / "judge-executed"
                before = None

                def snapshot_layout(layout):
                    nonlocal before
                    before = {
                        "baseline": layout["baseline"].read_bytes(),
                        "corpus": file_tree_snapshot(layout["corpus"]),
                        "json": path_snapshot(layout["json_output"]),
                        "markdown": path_snapshot(layout["markdown_output"]),
                    }

                completed, json_output, markdown_output = self.run_evaluation(
                    root,
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
                    timeout_seconds=timeout_seconds,
                    before_command=snapshot_layout,
                )

                self.assertNotEqual(completed.returncode, 0)
                self.assertNotIn("Traceback", completed.stderr)
                self.assertIn("configuration", completed.stderr.lower())
                self.assertLessEqual(len(completed.stderr.encode()), 4096)
                self.assertFalse(candidate_sentinel.exists())
                self.assertFalse(judge_sentinel.exists())
                self.assertEqual(
                    {
                        "baseline": (root_path / "baseline.json").read_bytes(),
                        "corpus": file_tree_snapshot(root_path / "corpus"),
                        "json": path_snapshot(json_output),
                        "markdown": path_snapshot(markdown_output),
                    },
                    before,
                )

    def test_agent_failures_produce_bounded_stable_json_and_markdown_reports(self):
        cases = (
            ("candidate", "timeout", "candidate-command-timeout"),
            ("candidate", "nonzero", "candidate-command-nonzero"),
            ("candidate", "malformed", "candidate-response-malformed-json"),
            ("candidate", "incomplete", "candidate-response-incomplete"),
            ("judgment", "timeout", "judgment-command-timeout"),
            ("judgment", "nonzero", "judgment-command-nonzero"),
            ("judgment", "malformed", "judgment-response-malformed-json"),
            ("judgment", "incomplete", "judgment-response-incomplete"),
        )

        for agent, mode, finding_id in cases:
            with self.subTest(agent=agent, mode=mode), tempfile.TemporaryDirectory() as root:
                root_path = Path(root)
                fake_agent = root_path / "fake_agent.py"
                fake_agent.write_text(
                    "import json\n"
                    "import sys\n"
                    "import time\n"
                    "request = json.load(sys.stdin)\n"
                    "agent = sys.argv[1]\n"
                    "mode = sys.argv[2]\n"
                    "if mode == 'timeout':\n"
                    "    time.sleep(3)\n"
                    "if mode == 'nonzero':\n"
                    "    raise SystemExit(7)\n"
                    "if mode == 'malformed':\n"
                    "    sys.stdout.write('not json')\n"
                    "elif mode == 'incomplete':\n"
                    "    json.dump({'result': 'incomplete'}, sys.stdout)\n"
                    "elif agent == 'candidate':\n"
                    "    json.dump({'output': '# Result\\n\\n[cite:SRC-1]'}, sys.stdout)\n"
                    "else:\n"
                    "    json.dump({'fixture_id': request['fixture_id'], 'run_id': request['run_id'], 'decisions': []}, sys.stdout)\n"
                )
                command = [sys.executable, str(fake_agent), agent, mode]
                candidate_command = command if agent == "candidate" else None
                judgment_command = command if agent == "judgment" else None
                started = time.monotonic()

                completed, json_output, markdown_output = self.run_evaluation(
                    root,
                    candidate_command=candidate_command,
                    judgment_command=judgment_command,
                    timeout_seconds=0.05,
                )

                self.assertLess(time.monotonic() - started, 1)
                self.assertNotEqual(completed.returncode, 0)
                self.assertNotIn("Traceback", completed.stderr)
                result = json.loads(json_output.read_text())
                self.assertIn(
                    finding_id,
                    {finding["id"] for finding in result["regressions"]},
                )
                markdown = markdown_output.read_text()
                self.assertIn(finding_id, markdown)
                self.assertLessEqual(len(json_output.read_bytes()), 65536)
                self.assertLessEqual(len(markdown_output.read_bytes()), 65536)
                self.assertLessEqual(len(completed.stderr.encode()), 65536)
                for stream in captured_stream_values(result):
                    self.assertLessEqual(len(stream), 8192)
                for text in string_values(result) + [markdown, completed.stderr]:
                    for match in re.finditer(r"(.)\1+", text, re.DOTALL):
                        self.assertLessEqual(len(match.group(0)), 8192)
                if agent == "judgment":
                    judgment = result["fixtures"][0]["judgment"]
                    self.assertFalse(judgment["available"])
                    self.assertNotIn("passed", judgment)
                    self.assertNotIn("criteria", judgment)

    def test_missing_candidate_executable_reports_unavailable_and_skips_judge(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            judge_sentinel = root_path / "judge-executed"
            judge_command = root_path / "judge.py"
            judge_command.write_text(
                "from pathlib import Path\n"
                "import sys\n"
                "Path(sys.argv[1]).write_text('executed')\n"
            )

            completed, json_output, markdown_output = self.run_evaluation(
                root,
                candidate_command=["missing-candidate-executable-issue-6"],
                judgment_command=[
                    sys.executable,
                    str(judge_command),
                    str(judge_sentinel),
                ],
                timeout_seconds=2,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertNotIn("Traceback", completed.stderr)
            self.assertFalse(judge_sentinel.exists())
            result = json.loads(json_output.read_text())
            self.assertIn(
                "candidate-command-unavailable",
                {finding["id"] for finding in result["regressions"]},
            )
            markdown = markdown_output.read_text()
            self.assertIn("candidate-command-unavailable", markdown)
            self.assertIn("unavailable", markdown.lower())

    def test_missing_judgment_executable_is_explicitly_unavailable_and_never_passed(self):
        with tempfile.TemporaryDirectory() as root:
            completed, json_output, markdown_output = self.run_evaluation(
                root,
                judgment_command=["missing-judgment-executable-issue-6"],
                timeout_seconds=2,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(json_output.read_text())
            judgment = result["fixtures"][0]["judgment"]
            self.assertFalse(judgment["available"])
            self.assertEqual(judgment["id"], "judgment-command-unavailable")
            self.assertIn("unavailable", judgment["reason"].lower())
            self.assertNotIn("passed", judgment)
            self.assertNotIn("criteria", judgment)
            markdown = markdown_output.read_text()
            self.assertIn("judgment-command-unavailable", json_output.read_text())
            self.assertIn("judgment-command-unavailable", markdown)
            judgment_lines = [
                line.casefold()
                for line in markdown.splitlines()
                if "judgment" in line.casefold()
            ]
            self.assertTrue(judgment_lines)
            self.assertTrue(any("unavailable" in line for line in judgment_lines))
            for line in judgment_lines:
                self.assertNotRegex(line, r"\bpass(?:ed)?\b")

    def test_large_agent_output_is_truncated_in_bounded_reports(self):
        for agent in ("candidate", "judgment"):
            with self.subTest(agent=agent), tempfile.TemporaryDirectory() as root:
                root_path = Path(root)
                noisy_agent = root_path / "noisy_agent.py"
                noisy_agent.write_text(
                    "import json\n"
                    "import sys\n"
                    "json.load(sys.stdin)\n"
                    "sys.stdout.write('x' * 200000)\n"
                    "sys.stderr.write('y' * 200000)\n"
                    "raise SystemExit(7)\n"
                )
                command = [sys.executable, str(noisy_agent)]

                completed, json_output, markdown_output = self.run_evaluation(
                    root,
                    candidate_command=command if agent == "candidate" else None,
                    judgment_command=command if agent == "judgment" else None,
                    timeout_seconds=2,
                )

                self.assertNotEqual(completed.returncode, 0)
                self.assertNotIn("Traceback", completed.stderr)
                self.assertLessEqual(len(completed.stderr.encode()), 65536)
                self.assertLessEqual(len(json_output.read_bytes()), 65536)
                self.assertLessEqual(len(markdown_output.read_bytes()), 65536)
                json_report = json_output.read_text()
                markdown_report = markdown_output.read_text()
                self.assertIn("[truncated]", json_report)
                self.assertIn("[truncated]", markdown_report)
                report_value = json.loads(json_report)
                for stream in captured_stream_values(report_value):
                    self.assertLessEqual(len(stream), 8192)
                for text in string_values(report_value) + [
                    markdown_report,
                    completed.stderr,
                ]:
                    repeated_spans = [
                        match.group(0)
                        for match in re.finditer(r"(.)\1+", text, re.DOTALL)
                    ]
                    if repeated_spans:
                        self.assertLessEqual(
                            max(len(span) for span in repeated_spans),
                            8192,
                        )

    def test_empty_or_unmanifested_corpus_prevents_agent_execution(self):
        for child_without_manifest in (False, True):
            with self.subTest(
                child_without_manifest=child_without_manifest
            ), tempfile.TemporaryDirectory() as root:
                root_path = Path(root)
                corpus = root_path / "corpus"
                corpus.mkdir()
                if child_without_manifest:
                    (corpus / "missing-manifest").mkdir()
                baseline = root_path / "baseline.json"
                baseline.write_text(json.dumps({"fixtures": {}}))
                sentinel_command = root_path / "sentinel_command.py"
                sentinel_command.write_text(
                    "from pathlib import Path\n"
                    "import sys\n"
                    "Path(sys.argv[1]).write_text('executed')\n"
                )
                candidate_sentinel = root_path / "candidate-executed"
                judge_sentinel = root_path / "judge-executed"
                command = [
                    sys.executable,
                    "-m",
                    "evaluations.cli",
                    "--corpus",
                    str(corpus),
                    "--baseline",
                    str(baseline),
                    "--json-output",
                    str(root_path / "result.json"),
                    "--markdown-output",
                    str(root_path / "result.md"),
                    "--candidate-command-json",
                    json.dumps(
                        [
                            sys.executable,
                            str(sentinel_command),
                            str(candidate_sentinel),
                        ]
                    ),
                    "--judgment-command-json",
                    json.dumps(
                        [
                            sys.executable,
                            str(sentinel_command),
                            str(judge_sentinel),
                        ]
                    ),
                    "--command-timeout-seconds",
                    "2",
                ]

                completed = subprocess.run(command, text=True, capture_output=True)

                self.assertNotEqual(completed.returncode, 0)
                self.assertFalse(candidate_sentinel.exists())
                self.assertFalse(judge_sentinel.exists())

    def test_out_of_root_fixture_symlink_is_rejected_before_agents_or_output(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            corpus = root_path / "corpus"
            corpus.mkdir()
            external_fixture = write_command_fixture(root_path / "external")
            linked_fixture = corpus / "linked-fixture"
            linked_fixture.symlink_to(external_fixture, target_is_directory=True)
            baseline = root_path / "baseline.json"
            baseline.write_text(
                json.dumps(
                    {
                        "fixtures": {
                            "fixture-one": {
                                "minimum_deterministic_pass_count": 1,
                                "minimum_judgment_pass_rates": {},
                            }
                        }
                    }
                )
            )
            json_output = linked_fixture / "passing.md"
            markdown_output = root_path / "result.md"
            sentinel_command = root_path / "sentinel_command.py"
            sentinel_command.write_text(
                "from pathlib import Path\n"
                "import sys\n"
                "Path(sys.argv[1]).write_text('executed')\n"
            )
            candidate_sentinel = root_path / "candidate-executed"
            judge_sentinel = root_path / "judge-executed"
            external_before = file_tree_snapshot(external_fixture)
            baseline_before = baseline.read_bytes()
            outputs_before = (
                path_snapshot(json_output),
                path_snapshot(markdown_output),
            )
            command = [
                sys.executable,
                "-m",
                "evaluations.cli",
                "--corpus",
                str(corpus),
                "--baseline",
                str(baseline),
                "--json-output",
                str(json_output),
                "--markdown-output",
                str(markdown_output),
                "--candidate-command-json",
                json.dumps(
                    [
                        sys.executable,
                        str(sentinel_command),
                        str(candidate_sentinel),
                    ]
                ),
                "--judgment-command-json",
                json.dumps(
                    [
                        sys.executable,
                        str(sentinel_command),
                        str(judge_sentinel),
                    ]
                ),
                "--command-timeout-seconds",
                "2",
            ]

            completed = subprocess.run(command, text=True, capture_output=True)

            self.assertNotEqual(completed.returncode, 0)
            self.assertNotIn("Traceback", completed.stderr)
            self.assertIn("configuration", completed.stderr.lower())
            self.assertLessEqual(len(completed.stderr.encode()), 4096)
            self.assertFalse(candidate_sentinel.exists())
            self.assertFalse(judge_sentinel.exists())
            self.assertEqual(file_tree_snapshot(external_fixture), external_before)
            self.assertEqual(baseline.read_bytes(), baseline_before)
            self.assertEqual(
                (path_snapshot(json_output), path_snapshot(markdown_output)),
                outputs_before,
            )


if __name__ == "__main__":
    unittest.main()
