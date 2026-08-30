import copy
import hashlib
import importlib.util
import inspect
import shutil
import tempfile
import unittest
import uuid
from datetime import datetime, timezone
from pathlib import Path

from scripts.quality_control_report import publish_quality_control_report
from scripts.validate_folder_invocation import validate_installed_skill_invocation


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "skills" / "section-1983-drafting"
SCRIPT = PACKAGE / "scripts" / "judge_overlay_receipt.py"
ANTI_GAMING_CHECKS = (
    "assignment-manipulation",
    "preference-exploitation",
    "desired-outcome-tailoring",
    "adverse-authority-concealment",
    "record-distortion",
    "court-personalization",
    "outcome-or-behavior-prediction",
    "unsupported-judge-conclusion",
)
FIXED_TIME = datetime(2026, 8, 22, 8, 30, 0, tzinfo=timezone.utc)
FIXED_RUN = "11111111-1111-4111-8111-111111111111"


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def packet(artifact_bytes=b"Frozen filing bytes."):
    return {
        "schema_version": "1.0",
        "audited_version_id": "VERSION-21",
        "scope": "Apply the validated assigned-judge overlay to the frozen filing.",
        "approved_source_ids": ["CORPUS-SOURCE-1", "COURT-SOURCE-1"],
        "artifacts": [
            {
                "relative_path": "filing.md",
                "sha256": sha256_bytes(artifact_bytes),
            }
        ],
        "overlay": {
            "skill_id": "drafting-for-judge-example",
            "version": "v3",
            "sha256": "a" * 64,
            "checked_on": "2026-08-22",
            "validation_status": "passed",
        },
        "corpus": {
            "corpus_id": "CORPUS-EXAMPLE-1",
            "version": "v2",
            "sha256": "b" * 64,
            "checked_on": "2026-08-22",
            "validation_status": "passed",
        },
        "court_conduct_inputs": [
            {
                "source_id": "COURT-SOURCE-1",
                "checked_on": "2026-08-22",
                "validation_status": "passed",
            }
        ],
        "transfer_cards": [
            {
                "card_id": "CARD-EXAMPLE-1",
                "validation_status": "passed",
                "used": False,
            }
        ],
        "prohibited_inference_checks": [
            {"check_id": check_id, "passed": True}
            for check_id in ANTI_GAMING_CHECKS
        ],
        "requested_result": {
            "status": "completed",
            "drafting_changes": [],
            "no_change_reason": "No qualifying support permits a judge-specific proposition.",
            "failure_class": None,
        },
    }


def load_module(path=SCRIPT, name=None):
    specification = importlib.util.spec_from_file_location(
        name or f"judge_overlay_receipt_{uuid.uuid4().hex}",
        path,
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def tree_bytes(root):
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


class JudgeOverlayReceiptRuntimeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module() if SCRIPT.is_file() else None

    def api(self, name):
        self.assertIsNotNone(self.module, f"missing public receipt module: {SCRIPT}")
        self.assertTrue(hasattr(self.module, name), f"missing public API: {name}")
        return getattr(self.module, name)

    def make_roles(self, directory, artifact_bytes=b"Frozen filing bytes."):
        root = Path(directory) / "invocation"
        filing = root / "filing"
        judge_corpus = root / "judge-corpus"
        court_conduct = root / "court-conduct"
        output = root / "output"
        for path in (filing, judge_corpus, court_conduct, output):
            path.mkdir(parents=True, exist_ok=True)
        (filing / "filing.md").write_bytes(artifact_bytes)
        (judge_corpus / "corpus.json").write_text('{"validated":true}\n')
        (court_conduct / "conduct.json").write_text('{"approved":true}\n')
        return filing, judge_corpus, court_conduct, output

    def execute(self, value, filing, judge_corpus, court_conduct, **overrides):
        arguments = {
            "filing_root": filing,
            "judge_corpus_root": judge_corpus,
            "court_conduct_root": court_conduct,
            "filing_target": "filing.md",
            "now": FIXED_TIME,
            "run_id": FIXED_RUN,
        }
        arguments.update(overrides)
        return self.api("execute_receipt")(value, **arguments)

    def invocation(self, filing, judge_corpus, court_conduct, output):
        installed = output.parent / "installed-static-judge-overlay"
        references = installed / "references"
        references.mkdir(parents=True)
        (references / "folder-contract.json").write_text(
            """{
  "version": 1,
  "skill": "drafting-for-judge-example",
  "input_roles": ["filing", "judge-corpus", "court-conduct"],
  "target": {"policy": "required", "roles": ["filing"]},
  "internet": "disabled",
  "output": {"mode": "append-immutable"}
}
"""
        )
        return validate_installed_skill_invocation(
            {
                "version": 1,
                "skill": "drafting-for-judge-example",
                "inputs": [
                    {"role": "filing", "root": str(filing)},
                    {"role": "judge-corpus", "root": str(judge_corpus)},
                    {"role": "court-conduct", "root": str(court_conduct)},
                ],
                "output": {"root": str(output)},
                "target": {"role": "filing", "path": "filing.md"},
                "runtime": {"max_seconds": 60, "max_input_bytes": 1_048_576},
                "internet": "disabled",
                "isolation": {
                    "inputs": "read-only",
                    "output": "read-write",
                    "undeclared": "none",
                },
            },
            installed,
        )

    def test_complete_packet_validates_without_mutation(self):
        value = packet()
        before = copy.deepcopy(value)
        validated = self.api("validate_packet")(value)
        self.assertEqual(validated, before)
        self.assertEqual(value, before)

    def test_folder_api_replaces_project_version_and_output_authority(self):
        parameters = set(inspect.signature(self.api("execute_receipt")).parameters)
        required = {
            "filing_root",
            "judge_corpus_root",
            "court_conduct_root",
            "filing_target",
        }
        forbidden = {
            "project_boundary",
            "version_folder",
            "output_root",
            "output_path",
            "audits",
        }
        self.assertEqual(
            {"missing": set(), "forbidden": set()},
            {"missing": required - parameters, "forbidden": forbidden & parameters},
        )

    def test_completed_no_change_returns_deterministic_host_publishable_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            filing, corpus, conduct, output = self.make_roles(directory)
            before = {
                "filing": tree_bytes(filing),
                "judge-corpus": tree_bytes(corpus),
                "court-conduct": tree_bytes(conduct),
            }
            first = self.execute(packet(), filing, corpus, conduct)
            second = self.execute(packet(), filing, corpus, conduct)
            self.assertEqual(first, second)
            self.assertEqual(first["outcome"], "no-judge-specific-drafting-change")
            self.assertIsNone(first["failure_class"])
            self.assertNotIn("artifact_path", first)
            self.assertIsInstance(first["report_bytes"], bytes)
            report = first["report_bytes"].decode("utf-8")
            self.assertIn("no judge-specific drafting change", report)
            self.assertIn("No qualifying support permits a judge-specific proposition.", report)
            self.assertIn("filing.md", report)
            self.assertNotIn(str(filing), report)
            self.assertEqual(list(output.iterdir()), [])
            self.assertEqual(
                {
                    "filing": tree_bytes(filing),
                    "judge-corpus": tree_bytes(corpus),
                    "court-conduct": tree_bytes(conduct),
                },
                before,
            )

            invocation = self.invocation(filing, corpus, conduct, output)
            receipt = publish_quality_control_report(
                invocation,
                skill_version="v3",
                quality_control_kind="judge-overlay-execution",
                run_id=FIXED_RUN,
                run_at=FIXED_TIME,
                scope=packet()["scope"],
                result=first["outcome"],
                approved_source_identities=packet()["approved_source_ids"],
                failed_findings=[],
                passing_but_suboptimal_recommendations=[],
                body=first["report_bytes"].decode("utf-8"),
            )
            self.assertEqual(receipt["status"], "success")
            self.assertEqual(receipt["internet"], {"policy": "disabled", "used": False})
            self.assertEqual(
                receipt["artifacts"][0]["path"],
                "quality-control-reports/judge-overlay-execution-20260822T083000Z-11111111-1111-4111-8111-111111111111.md",
            )

    def test_supported_change_records_only_used_neutral_cards(self):
        value = packet()
        value["transfer_cards"][0]["used"] = True
        value["requested_result"] = {
            "status": "completed",
            "drafting_changes": [
                {
                    "change_id": "CHANGE-1",
                    "description": "Organize the neutral rule before the supported facts.",
                    "transfer_card_ids": ["CARD-EXAMPLE-1"],
                }
            ],
            "no_change_reason": None,
            "failure_class": None,
        }
        with tempfile.TemporaryDirectory() as directory:
            filing, corpus, conduct, _ = self.make_roles(directory)
            result = self.execute(value, filing, corpus, conduct)
        self.assertEqual(result["outcome"], "judge-specific-drafting-change")
        report = result["report_bytes"].decode("utf-8")
        self.assertIn("CHANGE-1", report)
        self.assertIn("CARD-EXAMPLE-1", report)
        self.assertNotIn("no judge-specific drafting change", report)

    def test_nonpassing_inputs_return_stable_failed_closed_receipts(self):
        mutations = (
            ("overlay-missing", ("overlay", "validation_status"), "missing"),
            ("overlay-stale", ("overlay", "validation_status"), "stale"),
            ("overlay-invalid", ("overlay", "validation_status"), "failed"),
            ("overlay-unavailable", ("overlay", "validation_status"), "unavailable"),
            ("corpus-invalid", ("corpus", "validation_status"), "failed"),
            (
                "court-conduct-input-stale",
                ("court_conduct_inputs", 0, "validation_status"),
                "stale",
            ),
            (
                "transfer-card-invalid",
                ("transfer_cards", 0, "validation_status"),
                "failed",
            ),
        )
        for expected_class, path, status in mutations:
            with self.subTest(failure_class=expected_class):
                value = packet()
                target = value
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = status
                with tempfile.TemporaryDirectory() as directory:
                    filing, corpus, conduct, _ = self.make_roles(directory)
                    result = self.execute(value, filing, corpus, conduct)
                self.assertEqual(result["outcome"], "failed-closed")
                self.assertEqual(result["failure_class"], expected_class)
                report = result["report_bytes"].decode("utf-8")
                self.assertIn(expected_class, report)
                self.assertNotIn("## Drafting Changes\n\n- ", report)

    def test_anti_gaming_checks_are_exactly_once_and_true(self):
        cases = {}
        missing = packet()
        missing["prohibited_inference_checks"].pop()
        cases["missing"] = missing
        failed = packet()
        failed["prohibited_inference_checks"][0]["passed"] = False
        cases["failed"] = failed
        duplicate = packet()
        duplicate["prohibited_inference_checks"].append(
            copy.deepcopy(duplicate["prohibited_inference_checks"][0])
        )
        cases["duplicate"] = duplicate
        unknown = packet()
        unknown["prohibited_inference_checks"][0]["check_id"] = "personality-optimization"
        cases["unknown"] = unknown
        for label, value in cases.items():
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                filing, corpus, conduct, _ = self.make_roles(directory)
                result = self.execute(value, filing, corpus, conduct)
                self.assertEqual(result["outcome"], "failed-closed")
                self.assertEqual(result["failure_class"], "prohibited-inference-check-failed")

    def test_unsupported_change_and_fingerprint_mismatch_fail_closed(self):
        unsupported = packet()
        unsupported["requested_result"] = {
            "status": "completed",
            "drafting_changes": [
                {
                    "change_id": "CHANGE-1",
                    "description": "Use an unsupported judge conclusion.",
                    "transfer_card_ids": ["CARD-UNKNOWN"],
                }
            ],
            "no_change_reason": None,
            "failure_class": None,
        }
        mismatched = packet()
        mismatched["artifacts"][0]["sha256"] = "f" * 64
        for value, expected in (
            (unsupported, "drafting-change-unsupported"),
            (mismatched, "artifact-fingerprint-mismatch"),
        ):
            with self.subTest(failure_class=expected), tempfile.TemporaryDirectory() as directory:
                filing, corpus, conduct, _ = self.make_roles(directory)
                before = tree_bytes(filing)
                result = self.execute(value, filing, corpus, conduct)
                self.assertEqual(result["outcome"], "failed-closed")
                self.assertEqual(result["failure_class"], expected)
                self.assertEqual(tree_bytes(filing), before)

    def test_roots_targets_and_packet_artifacts_are_canonical_and_confined(self):
        receipt_error = self.api("ReceiptError")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            filing, corpus, conduct, output = self.make_roles(directory)
            outside = root / "outside.md"
            outside.write_bytes(b"Frozen filing bytes.")
            (filing / "linked.md").symlink_to(outside)
            file_root = root / "not-a-root.txt"
            file_root.write_text("not a directory")
            for overrides in (
                {"judge_corpus_root": root / "missing"},
                {"court_conduct_root": file_root},
            ):
                with self.subTest(overrides=overrides), self.assertRaises(receipt_error):
                    self.execute(packet(), filing, corpus, conduct, **overrides)
            for target in (
                None,
                "",
                "/filing.md",
                "../filing.md",
                "./filing.md",
                "folder//filing.md",
                "filing.md/",
                "bad\x00name",
                "linked.md",
                "missing.md",
            ):
                with self.subTest(target=target), self.assertRaises(receipt_error):
                    self.execute(packet(), filing, corpus, conduct, filing_target=target)
            for relative_path in (
                str((filing / "filing.md").resolve()),
                "../filing.md",
                "./filing.md",
                "folder//filing.md",
                "filing.md/",
                "bad\x00name",
                "audits/prior.md",
                "linked.md",
            ):
                value = packet()
                value["artifacts"][0]["relative_path"] = relative_path
                with self.subTest(relative_path=relative_path), self.assertRaises(receipt_error):
                    self.execute(value, filing, corpus, conduct)
            self.assertEqual(list(output.iterdir()), [])

    def test_processor_runs_from_isolated_package_without_root_imports(self):
        with tempfile.TemporaryDirectory() as directory:
            isolated = Path(directory) / "section-1983-drafting"
            shutil.copytree(PACKAGE, isolated)
            isolated_script = isolated / "scripts" / "judge_overlay_receipt.py"
            source = isolated_script.read_text()
            self.assertNotRegex(source, r"(?m)^\s*(?:from|import)\s+scripts(?:\.|\s)")
            module = load_module(isolated_script, "isolated_judge_overlay_receipt")
            filing, corpus, conduct, _ = self.make_roles(directory)
            result = module.execute_receipt(
                packet(),
                filing_root=filing,
                judge_corpus_root=corpus,
                court_conduct_root=conduct,
                filing_target="filing.md",
                now=FIXED_TIME,
                run_id=FIXED_RUN,
            )
        self.assertIsInstance(result["report_bytes"], bytes)

    def test_cli_exposes_only_declared_folder_authority(self):
        parser = self.api("_parser")()
        options = {
            option
            for action in parser._actions
            for option in action.option_strings
        }
        required = {
            "--filing-root",
            "--judge-corpus-root",
            "--court-conduct-root",
            "--filing-target",
        }
        forbidden = {
            "--project-boundary",
            "--version-folder",
            "--output-root",
            "--output-path",
            "--audits",
        }
        self.assertEqual(
            {"missing": set(), "forbidden": set()},
            {"missing": required - options, "forbidden": forbidden & options},
        )


if __name__ == "__main__":
    unittest.main()
