import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    ROOT
    / "skills"
    / "section-1983-drafting"
    / "scripts"
    / "judge_overlay_receipt.py"
)
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


class JudgeOverlayReceiptRuntimeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = None
        if SCRIPT.is_file():
            spec = importlib.util.spec_from_file_location("judge_overlay_receipt", SCRIPT)
            cls.module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.module)

    def api(self, name):
        self.assertIsNotNone(self.module, f"missing public receipt module: {SCRIPT}")
        self.assertTrue(hasattr(self.module, name), f"missing public API: {name}")
        return getattr(self.module, name)

    def make_version(self, directory, artifact_bytes=b"Frozen filing bytes."):
        project = Path(directory, "project")
        version = project / "versions" / "v21"
        version.mkdir(parents=True)
        artifact = version / "filing.md"
        artifact.write_bytes(artifact_bytes)
        companion = version / "source-map.json"
        companion.write_text('{"frozen":true}')
        return project, version, artifact

    def execute(self, project, version, value):
        return self.api("execute_receipt")(
            value,
            project_boundary=project,
            version_folder=version,
            now=FIXED_TIME,
            run_id=FIXED_RUN,
        )

    def test_complete_packet_validates_without_mutation(self):
        value = packet()
        before = copy.deepcopy(value)

        validated = self.api("validate_packet")(value)

        self.assertEqual(validated, before)
        self.assertEqual(value, before)

    def test_completed_no_change_writes_one_immutable_version_local_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            project, version, artifact = self.make_version(directory)
            before = {
                path: path.read_bytes()
                for path in version.rglob("*")
                if path.is_file()
            }

            result = self.execute(project, version, packet())

            expected = (
                version
                / "audits"
                / "judge-overlay-execution-20260822T083000Z-11111111-1111-4111-8111-111111111111.md"
            )
            self.assertEqual(result["outcome"], "no-judge-specific-drafting-change")
            self.assertIsNone(result["failure_class"])
            self.assertEqual(Path(result["report_path"]).resolve(), expected.resolve())
            report = expected.read_text()
            self.assertIn("no judge-specific drafting change", report)
            self.assertIn("No qualifying support permits a judge-specific proposition.", report)
            self.assertIn("drafting-for-judge-example", report)
            self.assertIn("CORPUS-EXAMPLE-1", report)
            self.assertIn("COURT-SOURCE-1", report)
            self.assertIn("CARD-EXAMPLE-1", report)
            self.assertIn(sha256_bytes(artifact.read_bytes()), report)
            self.assertNotRegex(report, r"(?im)^result:\s*pass(?:ed)?\s*$")
            for path, content in before.items():
                self.assertEqual(path.read_bytes(), content)
            self.assertEqual(
                sorted(
                    path.relative_to(version).as_posix()
                    for path in version.rglob("*")
                    if path.is_file() and path not in before
                ),
                [expected.relative_to(version).as_posix()],
            )

    def test_supported_change_requires_and_records_used_neutral_card(self):
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
            project, version, _ = self.make_version(directory)

            result = self.execute(project, version, value)

            self.assertEqual(result["outcome"], "judge-specific-drafting-change")
            report = Path(result["report_path"]).read_text()
            self.assertIn("CHANGE-1", report)
            self.assertIn("CARD-EXAMPLE-1", report)
            self.assertNotIn("no judge-specific drafting change", report)

    def test_nonpassing_required_inputs_write_stable_failed_closed_receipts(self):
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
                    project, version, _ = self.make_version(directory)
                    result = self.execute(project, version, value)

                    self.assertEqual(result["outcome"], "failed-closed")
                    self.assertEqual(result["failure_class"], expected_class)
                    report = Path(result["report_path"]).read_text()
                    self.assertIn("failed-closed", report)
                    self.assertIn(expected_class, report)
                    self.assertNotRegex(report, r"(?im)^result:\s*pass(?:ed)?\s*$")
                    self.assertNotIn("## Drafting Changes\n\n- ", report)

    def test_every_anti_gaming_check_is_exactly_once_and_true(self):
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
            with self.subTest(case=label):
                with tempfile.TemporaryDirectory() as directory:
                    project, version, _ = self.make_version(directory)
                    result = self.execute(project, version, value)

                    self.assertEqual(result["outcome"], "failed-closed")
                    self.assertEqual(
                        result["failure_class"], "prohibited-inference-check-failed"
                    )

    def test_unsupported_change_fails_closed(self):
        value = packet()
        value["requested_result"] = {
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
        with tempfile.TemporaryDirectory() as directory:
            project, version, _ = self.make_version(directory)

            result = self.execute(project, version, value)

            self.assertEqual(result["outcome"], "failed-closed")
            self.assertEqual(result["failure_class"], "drafting-change-unsupported")

    def test_artifact_fingerprint_mismatch_fails_closed_without_editing_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            project, version, artifact = self.make_version(directory)
            value = packet()
            value["artifacts"][0]["sha256"] = "f" * 64
            original = artifact.read_bytes()

            result = self.execute(project, version, value)

            self.assertEqual(result["outcome"], "failed-closed")
            self.assertEqual(result["failure_class"], "artifact-fingerprint-mismatch")
            self.assertEqual(artifact.read_bytes(), original)
            report = Path(result["report_path"]).read_text()
            self.assertIn("Expected SHA-256", report)
            self.assertIn("Actual SHA-256", report)

    def test_invalid_version_or_artifact_path_writes_no_report(self):
        receipt_error = self.api("ReceiptError")
        with tempfile.TemporaryDirectory() as directory:
            project, version, _ = self.make_version(directory)
            outside = Path(directory, "outside", "v1")
            outside.mkdir(parents=True)
            outside.joinpath("filing.md").write_bytes(b"Frozen filing bytes.")
            path_cases = (
                ("outside-version", outside, packet()),
                (
                    "absolute-artifact",
                    version,
                    {
                        **packet(),
                        "artifacts": [
                            {
                                "relative_path": str(version / "filing.md"),
                                "sha256": sha256_bytes(b"Frozen filing bytes."),
                            }
                        ],
                    },
                ),
                (
                    "traversal-artifact",
                    version,
                    {
                        **packet(),
                        "artifacts": [
                            {
                                "relative_path": "../filing.md",
                                "sha256": sha256_bytes(b"Frozen filing bytes."),
                            }
                        ],
                    },
                ),
                (
                    "audits-artifact",
                    version,
                    {
                        **packet(),
                        "artifacts": [
                            {
                                "relative_path": "audits/prior.md",
                                "sha256": sha256_bytes(b"prior"),
                            }
                        ],
                    },
                ),
            )
            for label, selected_version, value in path_cases:
                with self.subTest(case=label):
                    with self.assertRaises(receipt_error):
                        self.execute(project, selected_version, value)
            self.assertFalse((version / "audits").exists())
            self.assertFalse((outside / "audits").exists())

    @unittest.skipIf(os.name == "nt", "symlink confinement is POSIX-specific")
    def test_audits_symlink_escape_and_collision_preserve_existing_bytes(self):
        receipt_error = self.api("ReceiptError")
        with tempfile.TemporaryDirectory() as directory:
            project, version, _ = self.make_version(directory)
            outside = Path(directory, "outside-audits")
            outside.mkdir()
            (version / "audits").symlink_to(outside, target_is_directory=True)

            with self.assertRaises(receipt_error):
                self.execute(project, version, packet())

            self.assertEqual(list(outside.iterdir()), [])

        with tempfile.TemporaryDirectory() as directory:
            project, version, _ = self.make_version(directory)
            audits = version / "audits"
            audits.mkdir()
            collision = (
                audits
                / "judge-overlay-execution-20260822T083000Z-11111111-1111-4111-8111-111111111111.md"
            )
            collision.write_text("immutable prior receipt")

            with self.assertRaises(receipt_error):
                self.execute(project, version, packet())

            self.assertEqual(collision.read_text(), "immutable prior receipt")

    def test_no_invocation_writes_no_receipt_but_cli_invocation_does(self):
        with tempfile.TemporaryDirectory() as directory:
            project, version, _ = self.make_version(directory)
            self.assertFalse((version / "audits").exists())

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--project-boundary",
                    str(project),
                    "--version-folder",
                    str(version),
                ],
                input=json.dumps(packet()),
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            response = json.loads(result.stdout)
            self.assertEqual(
                response["outcome"], "no-judge-specific-drafting-change"
            )
            self.assertTrue(Path(response["report_path"]).is_file())


if __name__ == "__main__":
    unittest.main()
