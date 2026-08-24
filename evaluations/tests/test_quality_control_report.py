import hashlib
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scripts.quality_control_report import (
    QualityControlReportError,
    build_quality_control_report_plan,
    publish_quality_control_report,
)
from scripts.skill_output_writer import OutputError
from scripts.validate_folder_invocation import build_input_manifest, validate_invocation


METADATA_FENCE = b"```quality-control-report+json\n"


def sha256(contents):
    return hashlib.sha256(contents).hexdigest()


class QualityControlReportTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.filing_root = self.root / "filing"
        self.authorities_root = self.root / "authorities"
        self.prior_reports_root = self.root / "prior-reports"
        self.output_root = self.root / "output"
        for path in (
            self.filing_root,
            self.authorities_root,
            self.prior_reports_root,
            self.output_root,
        ):
            path.mkdir()
        (self.filing_root / "draft.md").write_bytes(b"# Draft\n\nReviewed text.\n")
        (self.authorities_root / "case.txt").write_bytes(b"Synthetic authority.\n")
        report_folder = self.prior_reports_root / "quality-control-reports"
        report_folder.mkdir()
        (report_folder / "older-audit.md").write_bytes(b"prior report\n")
        (report_folder / "sibling-audit.md").write_bytes(b"sibling report\n")

    def tearDown(self):
        self.temporary_directory.cleanup()

    def invocation(self, *, target_role="filing", target_path="draft.md"):
        return validate_invocation(
            {
                "version": 1,
                "skill": "synthetic-quality-control",
                "inputs": [
                    {"role": "filing", "root": str(self.filing_root)},
                    {"role": "authorities", "root": str(self.authorities_root)},
                    {"role": "prior-reports", "root": str(self.prior_reports_root)},
                ],
                "output": {"root": str(self.output_root)},
                "target": {"role": target_role, "path": target_path},
                "runtime": {"max_seconds": 60, "max_input_bytes": 1_048_576},
                "internet": "disabled",
                "isolation": {
                    "inputs": "read-only",
                    "output": "read-write",
                    "undeclared": "none",
                },
            }
        )

    def report_arguments(self):
        return {
            "skill_version": "2.4.0",
            "quality_control_kind": "authority-audit",
            "run_id": "qc-run-7f3a",
            "run_at": datetime(2026, 8, 24, 16, 17, 18, 123456, timezone.utc),
            "scope": "Citations and quoted language in the selected filing.",
            "result": "pass",
            "failed_findings": [],
            "passing_but_suboptimal_recommendations": [
                {"id": "QC-ADVISORY-1", "recommendation": "Prefer a tighter pinpoint."}
            ],
            "body": "# Authority audit\n\nNo failed findings.\n",
        }

    def metadata(self, contents):
        self.assertTrue(contents.startswith(METADATA_FENCE))
        metadata_bytes, body = contents[len(METADATA_FENCE) :].split(b"\n```\n\n", 1)
        return json.loads(metadata_bytes), body

    def tree_hashes(self, root):
        return {
            path.relative_to(root).as_posix(): sha256(path.read_bytes())
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    def test_plan_records_complete_metadata_and_one_canonical_unique_path(self):
        invocation = self.invocation()

        plan = build_quality_control_report_plan(invocation, **self.report_arguments())
        metadata, body = self.metadata(plan.contents)

        self.assertEqual(
            plan.relative_path,
            "quality-control-reports/authority-audit-20260824T161718123456Z-qc-run-7f3a.md",
        )
        self.assertEqual(
            metadata,
            {
                "failed_findings": [],
                "input_manifest": {
                    "inputs": [
                        {
                            "files": [
                                {
                                    "path": "draft.md",
                                    "sha256": sha256(b"# Draft\n\nReviewed text.\n"),
                                    "size": 24,
                                }
                            ],
                            "role": "filing",
                        },
                        {
                            "files": [
                                {
                                    "path": "case.txt",
                                    "sha256": sha256(b"Synthetic authority.\n"),
                                    "size": 21,
                                }
                            ],
                            "role": "authorities",
                        },
                        {"files": [], "role": "prior-reports"},
                    ]
                },
                "passing_but_suboptimal_recommendations": [
                    {
                        "id": "QC-ADVISORY-1",
                        "recommendation": "Prefer a tighter pinpoint.",
                    }
                ],
                "quality_control_kind": "authority-audit",
                "result": "pass",
                "run_at": "2026-08-24T16:17:18.123456Z",
                "run_id": "qc-run-7f3a",
                "run_manifest": {
                    "path": ".skill-runs/qc-run-7f3a/manifest.json",
                    "run_id": "qc-run-7f3a",
                },
                "schema_version": 1,
                "scope": "Citations and quoted language in the selected filing.",
                "skill": "synthetic-quality-control",
                "skill_version": "2.4.0",
                "target": {
                    "path": "draft.md",
                    "role": "filing",
                    "sha256": sha256(b"# Draft\n\nReviewed text.\n"),
                    "size": 24,
                },
            },
        )
        self.assertEqual(body, b"# Authority audit\n\nNo failed findings.\n")
        self.assertEqual(plan.input_manifest, metadata["input_manifest"])

        later = self.report_arguments()
        later["run_id"] = "qc-run-8b4c"
        self.assertNotEqual(
            plan.relative_path,
            build_quality_control_report_plan(invocation, **later).relative_path,
        )

    def test_prior_reports_are_excluded_unless_one_is_the_exact_target(self):
        ordinary = self.invocation()
        ordinary_plan = build_quality_control_report_plan(
            ordinary, **self.report_arguments()
        )
        self.assertEqual(
            ordinary_plan.input_manifest["inputs"][2],
            {"role": "prior-reports", "files": []},
        )

        targeted = self.invocation(
            target_role="prior-reports",
            target_path="quality-control-reports/older-audit.md",
        )
        targeted_plan = build_quality_control_report_plan(
            targeted, **self.report_arguments()
        )
        self.assertEqual(
            targeted_plan.input_manifest["inputs"][2],
            {
                "role": "prior-reports",
                "files": [
                    {
                        "path": "quality-control-reports/older-audit.md",
                        "sha256": sha256(b"prior report\n"),
                        "size": 13,
                    }
                ],
            },
        )

    def test_missing_or_directory_target_fails_before_run_state_exists(self):
        no_target = self.invocation()
        no_target = type(no_target)(
            skill=no_target.skill,
            inputs=no_target.inputs,
            output_root=no_target.output_root,
            runtime=no_target.runtime,
            internet=no_target.internet,
            target=None,
        )
        (self.filing_root / "folder-target").mkdir()
        for label, invocation in (
            ("missing", no_target),
            (
                "directory",
                self.invocation(target_role="filing", target_path="folder-target"),
            ),
        ):
            with self.subTest(label=label), self.assertRaises(
                QualityControlReportError
            ) as captured:
                build_quality_control_report_plan(invocation, **self.report_arguments())
            self.assertEqual(captured.exception.code, "invalid-quality-control-target")
        self.assertFalse((self.output_root / ".skill-runs").exists())

    def test_publication_preserves_inputs_and_prior_reports_and_binds_receipt(self):
        invocation = self.invocation()
        before = {
            "filing": self.tree_hashes(self.filing_root),
            "authorities": self.tree_hashes(self.authorities_root),
            "prior-reports": self.tree_hashes(self.prior_reports_root),
        }

        receipt = publish_quality_control_report(
            invocation, **self.report_arguments()
        )

        self.assertEqual(receipt["status"], "success")
        self.assertEqual(receipt["mode"], "append-immutable")
        self.assertEqual(len(receipt["artifacts"]), 1)
        report_path = self.output_root / receipt["artifacts"][0]["path"]
        metadata, _ = self.metadata(report_path.read_bytes())
        self.assertEqual(metadata["run_id"], receipt["run_id"])
        self.assertEqual(
            metadata["run_manifest"]["path"],
            f".skill-runs/{receipt['run_id']}/manifest.json",
        )
        manifest_path = self.output_root / metadata["run_manifest"]["path"]
        self.assertEqual(json.loads(manifest_path.read_bytes()), receipt)
        self.assertEqual(
            receipt["input_manifest_sha256"],
            sha256(
                json.dumps(
                    metadata["input_manifest"],
                    ensure_ascii=False,
                    allow_nan=False,
                    separators=(",", ":"),
                    sort_keys=True,
                ).encode("utf-8")
            ),
        )
        self.assertEqual(
            before,
            {
                "filing": self.tree_hashes(self.filing_root),
                "authorities": self.tree_hashes(self.authorities_root),
                "prior-reports": self.tree_hashes(self.prior_reports_root),
            },
        )

    def test_report_collision_never_overwrites_and_never_reports_completion(self):
        invocation = self.invocation()
        plan = build_quality_control_report_plan(invocation, **self.report_arguments())
        destination = self.output_root / plan.relative_path
        destination.parent.mkdir(parents=True)
        destination.write_bytes(b"immutable prior bytes\n")

        with self.assertRaises(OutputError):
            publish_quality_control_report(invocation, **self.report_arguments())

        self.assertEqual(destination.read_bytes(), b"immutable prior bytes\n")
        run_root = self.output_root / ".skill-runs" / self.report_arguments()["run_id"]
        self.assertFalse((run_root / "manifest.json").exists())
        self.assertTrue(
            (run_root / "failure.json").exists()
            or (run_root / "incomplete.json").exists()
        )

    def test_invalid_metadata_fails_before_any_output_mutation(self):
        invocation = self.invocation()
        cases = (
            ("naive-time", {"run_at": datetime(2026, 8, 24)}),
            ("blank-scope", {"scope": ""}),
            ("invalid-result", {"result": "looks good"}),
            ("invalid-body", {"body": b"not markdown text"}),
            ("invalid-findings", {"failed_findings": "none"}),
        )
        for label, override in cases:
            arguments = self.report_arguments()
            arguments.update(override)
            with self.subTest(label=label), self.assertRaises(
                QualityControlReportError
            ):
                publish_quality_control_report(invocation, **arguments)
        self.assertEqual(list(self.output_root.iterdir()), [])

    def test_filtered_manifest_is_derived_from_the_generic_manifest(self):
        invocation = self.invocation()
        generic = build_input_manifest(invocation)
        self.assertEqual(len(generic["inputs"][2]["files"]), 2)

        plan = build_quality_control_report_plan(invocation, **self.report_arguments())

        self.assertEqual(plan.input_manifest["inputs"][:2], generic["inputs"][:2])
        self.assertEqual(plan.input_manifest["inputs"][2]["files"], [])


if __name__ == "__main__":
    unittest.main()
