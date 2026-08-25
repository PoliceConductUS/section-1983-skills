import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from evaluations.tests.test_installed_filing_checks import complaint_document
from scripts.filing_integrity import (
    FilingIntegrityError,
    FilingIntegritySelection,
    run_and_publish_filing_integrity,
)
from scripts.validate_folder_invocation import validate_invocation


REPOSITORY = Path(__file__).resolve().parents[2]
SKILL = REPOSITORY / "skills" / "filing-ci"
ROLES = (
    "filing-source",
    "filing-index",
    "record-reference",
    "exhibit",
    "docket-to-appendix",
    "verified-authority",
)


class FolderNativeFilingIntegrityTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.inputs = {role: self.root / role for role in ROLES}
        self.output = self.root / "output"
        for path in (*self.inputs.values(), self.output):
            path.mkdir()

        filing = complaint_document()
        filing.update(
            {
                "section_owners": {
                    section: "plaintiff" for section in filing["sections"]
                },
                "exhibit_references": [],
                "docket_citations": [],
                "persistent_citations": [],
                "filing_gates": [],
            }
        )
        (self.inputs["filing-source"] / "complaint.json").write_text(
            json.dumps(filing, sort_keys=True), encoding="utf-8"
        )
        (self.inputs["record-reference"] / "record.txt").write_text(
            "Synthetic record.\n", encoding="utf-8"
        )
        (self.inputs["exhibit"] / "exhibit-a.txt").write_text(
            "Synthetic exhibit.\n", encoding="utf-8"
        )
        (self.inputs["docket-to-appendix"] / "map.json").write_text(
            json.dumps({"entries": []}), encoding="utf-8"
        )
        (self.inputs["verified-authority"] / "authority.txt").write_text(
            "Synthetic authority.\n", encoding="utf-8"
        )
        self.write_source_yaml(
            documentation_role="filing-index",
            documentation_path="filing.SOURCE.yaml",
            source_id="filing-current",
            source_role="filing-source",
            source_path="complaint.json",
            classification="filing",
        )
        self.write_source_yaml(
            documentation_role="record-reference",
            documentation_path="record.SOURCE.yaml",
            source_id="record-one",
            source_role="record-reference",
            source_path="record.txt",
            classification="record",
        )
        self.write_source_yaml(
            documentation_role="exhibit",
            documentation_path="exhibit-a.SOURCE.yaml",
            source_id="exhibit-a",
            source_role="exhibit",
            source_path="exhibit-a.txt",
            classification="exhibit",
        )
        self.write_source_yaml(
            documentation_role="docket-to-appendix",
            documentation_path="map.SOURCE.yaml",
            source_id="docket-map",
            source_role="docket-to-appendix",
            source_path="map.json",
            classification="docket-to-appendix",
        )
        self.write_source_yaml(
            documentation_role="verified-authority",
            documentation_path="authority.SOURCE.yaml",
            source_id="authority-one",
            source_role="verified-authority",
            source_path="authority.txt",
            classification="authority",
        )

    def tearDown(self):
        self.temporary_directory.cleanup()

    def write_source_yaml(
        self,
        *,
        documentation_role,
        documentation_path,
        source_id,
        source_role,
        source_path,
        classification,
    ):
        source = self.inputs[source_role] / source_path
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        (self.inputs[documentation_role] / documentation_path).write_text(
            "schema_version: 1\n"
            f"source_id: {source_id}\n"
            f"source_role: {source_role}\n"
            f"path: {source_path}\n"
            f"sha256: {digest}\n"
            "checked_through: 2026-08-25\n"
            f"classification: {classification}\n"
            "validation_status: passed\n",
            encoding="utf-8",
        )

    def invocation(self):
        return validate_invocation(
            {
                "version": 1,
                "skill": "filing-ci",
                "inputs": [
                    {"role": role, "root": str(self.inputs[role])}
                    for role in ROLES
                ],
                "output": {"root": str(self.output)},
                "runtime": {"max_seconds": 60, "max_input_bytes": 5_242_880},
                "internet": "disabled",
                "isolation": {
                    "inputs": "read-only",
                    "output": "read-write",
                    "undeclared": "none",
                },
                "target": {"role": "filing-source", "path": "complaint.json"},
            }
        )

    @staticmethod
    def selection():
        return FilingIntegritySelection(
            checker_id="section-1983-complaint-v1",
            filing_documentation_path="filing.SOURCE.yaml",
            record_documentation_paths=("record.SOURCE.yaml",),
            exhibit_documentation_paths=("exhibit-a.SOURCE.yaml",),
            docket_documentation_path="map.SOURCE.yaml",
            authority_documentation_paths=("authority.SOURCE.yaml",),
        )

    def input_snapshot(self):
        return {
            path.relative_to(self.root).as_posix(): path.read_bytes()
            for root in self.inputs.values()
            for path in root.rglob("*")
            if path.is_file()
        }

    def test_public_skill_uses_exact_folder_contract_and_no_package_metadata(self):
        contract = json.loads((SKILL / "references/folder-contract.json").read_text())
        self.assertEqual(contract["input_roles"], list(ROLES))
        self.assertEqual(
            contract["target"],
            {"policy": "required", "roles": ["filing-source"]},
        )
        self.assertTrue(
            (SKILL / "references/complaint-checker-contract.json").is_file()
        )
        self.assertFalse(
            (SKILL / "references/packaged-complaint-checker.json").exists()
        )
        text = "\n".join(
            path.read_text()
            for path in SKILL.rglob("*")
            if path.is_file() and path.suffix in {".md", ".py", ".json"}
        ).casefold()
        self.assertNotIn("packaged checker", text)
        self.assertNotIn("skill package", text)
        self.assertNotIn("casegraph", text)

    def test_valid_selected_source_yaml_publishes_outputs_and_preserves_inputs(self):
        before = self.input_snapshot()

        result = run_and_publish_filing_integrity(
            invocation=self.invocation(),
            selection=self.selection(),
            run_id="filing-integrity-one",
            skill_version="1.0.0",
        )

        self.assertEqual(result.status, "passed")
        self.assertEqual(result.exit_class, "passed")
        self.assertTrue((self.output / "reports/filing-integrity.json").is_file())
        self.assertTrue((self.output / "reports/filing-integrity.md").is_file())
        receipt = self.output / "run-receipt.yaml"
        self.assertTrue(receipt.is_file())
        self.assertIn('path: "complaint.json"', receipt.read_text())
        self.assertNotIn(str(self.root), receipt.read_text())
        self.assertTrue(
            (self.output / ".skill-runs/filing-integrity-one/manifest.json").is_file()
        )
        self.assertEqual(before, self.input_snapshot())
        self.assertEqual(
            [path for path in (self.output / "temp").rglob("*") if path.is_file()],
            [],
        )

    def test_hash_mismatch_and_instruction_shaped_yaml_fail_before_output(self):
        target = self.inputs["filing-source"] / "complaint.json"
        target.write_text(target.read_text() + "\n", encoding="utf-8")
        with self.assertRaises(FilingIntegrityError) as captured:
            run_and_publish_filing_integrity(
                invocation=self.invocation(),
                selection=self.selection(),
                run_id="filing-integrity-mismatch",
                skill_version="1.0.0",
            )
        self.assertEqual(captured.exception.code, "source-content-mismatch")
        self.assertEqual(list(self.output.iterdir()), [])

        self.output.mkdir(exist_ok=True)
        self.write_source_yaml(
            documentation_role="filing-index",
            documentation_path="filing.SOURCE.yaml",
            source_id="filing-current",
            source_role="filing-source",
            source_path="complaint.json",
            classification="filing",
        )
        documentation = self.inputs["filing-index"] / "filing.SOURCE.yaml"
        documentation.write_text(
            documentation.read_text() + "command: /bin/sh\n", encoding="utf-8"
        )
        with self.assertRaises(FilingIntegrityError) as captured:
            run_and_publish_filing_integrity(
                invocation=self.invocation(),
                selection=self.selection(),
                run_id="filing-integrity-hostile",
                skill_version="1.0.0",
            )
        self.assertEqual(captured.exception.code, "invalid-source-documentation")
        self.assertEqual(list(self.output.iterdir()), [])

    def test_initial_mechanical_failures_are_stable_findings_not_legal_judgments(self):
        target = self.inputs["filing-source"] / "complaint.json"
        filing = json.loads(target.read_text())
        filing["section_owners"].pop("jury-demand")
        filing["exhibit_references"] = [
            {
                "exhibit_id": "missing-exhibit",
                "paragraph_start": 3,
                "paragraph_end": 2,
                "short_form": "the attachment",
            }
        ]
        filing["docket_citations"] = [
            {"docket_entry": 29, "docket_page": 2, "appendix_page": 99}
        ]
        filing["persistent_citations"] = [
            {
                "id": "cite-one",
                "type": "authority",
                "target": "authority-one",
                "visible_text": "Synthetic Authority",
                "status": "resolved",
            },
            {
                "id": "cite-one",
                "type": "record",
                "target": "missing-record",
                "visible_text": "Record citation",
                "status": "unresolved",
            },
        ]
        filing["filing_gates"] = [
            {"id": "gate-one", "status": "open", "message": "Resolve gate."}
        ]
        target.write_text(json.dumps(filing, sort_keys=True), encoding="utf-8")
        self.write_source_yaml(
            documentation_role="filing-index",
            documentation_path="filing.SOURCE.yaml",
            source_id="filing-current",
            source_role="filing-source",
            source_path="complaint.json",
            classification="filing",
        )

        result = run_and_publish_filing_integrity(
            invocation=self.invocation(),
            selection=self.selection(),
            run_id="filing-integrity-findings",
            skill_version="1.0.0",
        )

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.exit_class, "findings")
        check_ids = {finding["check_id"] for finding in result.findings}
        self.assertTrue(
            {
                "section-owner",
                "exhibit-paragraph-range",
                "exhibit-reference",
                "internal-short-form",
                "docket-appendix-consistency",
                "persistent-citation-id",
                "persistent-citation-target",
                "open-filing-gate",
            }.issubset(check_ids)
        )
        report = json.loads(
            (self.output / "reports/filing-integrity.json").read_text()
        )
        self.assertEqual(report["status"], "failed")
        self.assertNotIn("legal_sufficiency", report)
        self.assertNotIn("filing_ready", report)


if __name__ == "__main__":
    unittest.main()
