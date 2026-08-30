import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.verified_authority_audit import (
    AuthorityAuditError,
    extract_eyecite_candidates,
    load_verified_authority_corpus,
    run_and_publish_authority_audit,
)
from scripts.validate_folder_invocation import validate_invocation


REPOSITORY = Path(__file__).resolve().parents[2]
SKILL = REPOSITORY / "skills" / "audit-authorities"


class VerifiedAuthorityAuditTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.filing = self.root / "filing-source"
        self.authorities = self.root / "verified-authority"
        self.output = self.root / "output"
        for path in (self.filing, self.authorities, self.output):
            path.mkdir()
        (self.filing / "motion.md").write_text(
            "Ashcroft v. Iqbal, 556 U.S. 662, 678 (2009).\n",
            encoding="utf-8",
        )
        self.opinion = self.authorities / "iqbal.txt"
        self.opinion.write_text(
            "[page 678]\nA claim has facial plausibility when the plaintiff "
            "pleads factual content.\n[page 679]\nAdditional text.\n",
            encoding="utf-8",
        )
        digest = hashlib.sha256(self.opinion.read_bytes()).hexdigest()
        (self.authorities / "iqbal.SOURCE.yaml").write_text(
            "schema_version: 1\n"
            "source_id: iqbal-opinion\n"
            "path: iqbal.txt\n"
            f"sha256: {digest}\n"
            "checked_through: 2026-08-25\n"
            "retrieved_from: https://www.supremecourt.gov/opinions/boundvolumes/556bv.pdf\n",
            encoding="utf-8",
        )
        (self.authorities / "iqbal.AUTHORITY.yaml").write_text(
            "schema_version: 1\n"
            "authority_id: ashcroft-v-iqbal\n"
            "citation: 556 U.S. 662\n"
            "document_path: iqbal.txt\n"
            "source_yaml_path: iqbal.SOURCE.yaml\n"
            f"sha256: {digest}\n"
            "court: Supreme Court of the United States\n"
            "decision_date: 2009-05-18\n"
            "publication_status: published\n"
            "precedential_status: precedential\n"
            "binding_status: binding\n"
            "event_date_status: pre-event\n"
            "later_history_status: checked\n"
            "rule_of_orderliness_status: checked\n"
            "proposition: plausibility standard\n"
            "quotation: A claim has facial plausibility when the plaintiff pleads factual content.\n"
            "pinpoint: 678\n"
            "text_layer_status: usable\n",
            encoding="utf-8",
        )
        (self.authorities / "selected.CORPUS.yaml").write_text(
            "schema_version: 1\n"
            "corpus_id: federal-authorities\n"
            "authorities:\n"
            "  - iqbal.AUTHORITY.yaml\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temporary_directory.cleanup()

    def invocation(self, output=None):
        return validate_invocation(
            {
                "version": 1,
                "skill": "audit-authorities",
                "operation": "audit",
                "inputs": [
                    {"role": "filing-source", "root": str(self.filing)},
                    {
                        "role": "verified-authority",
                        "root": str(self.authorities),
                    },
                ],
                "output": {"root": str(output or self.output)},
                "runtime": {"max_seconds": 60, "max_input_bytes": 5_242_880},
                "internet": "disabled",
                "isolation": {
                    "inputs": "read-only",
                    "output": "read-write",
                    "undeclared": "none",
                },
                "target": {"role": "filing-source", "path": "motion.md"},
            }
        )

    def test_public_contract_is_two_folder_operation_specific_and_not_packaged(self):
        contract = (SKILL / "references/folder-contract.json").read_text()
        self.assertIn('"filing-source"', contract)
        self.assertIn('"verified-authority"', contract)
        self.assertNotIn('"filing"', contract)
        self.assertNotIn('"authorities"', contract)
        text = "\n".join(
            path.read_text()
            for path in SKILL.rglob("*")
            if path.is_file() and path.suffix in {".md", ".json", ".py"}
        ).casefold()
        for forbidden in (
            "filingpacket",
            "canonical verified-case root",
            "installed package",
            "casegraph",
        ):
            self.assertNotIn(forbidden, text)

    def test_strict_selected_yaml_binds_exact_ordinary_authority_bytes(self):
        corpus = load_verified_authority_corpus(
            self.invocation(), "selected.CORPUS.yaml"
        )

        self.assertEqual(corpus.corpus_id, "federal-authorities")
        self.assertEqual(len(corpus.authorities), 1)
        authority = corpus.authorities[0]
        self.assertEqual(authority.authority_id, "ashcroft-v-iqbal")
        self.assertEqual(authority.citation, "556 U.S. 662")
        self.assertEqual(authority.document_path, "iqbal.txt")

    def test_hash_mismatch_is_invalid_before_output(self):
        self.opinion.write_text("changed\n", encoding="utf-8")

        with self.assertRaises(AuthorityAuditError) as captured:
            load_verified_authority_corpus(
                self.invocation(), "selected.CORPUS.yaml"
            )

        self.assertEqual(captured.exception.code, "authority-content-mismatch")
        self.assertEqual(captured.exception.exit_class, "invalid")
        self.assertEqual(list(self.output.iterdir()), [])

    def test_missing_selected_corpus_yaml_is_unavailable_before_output(self):
        (self.authorities / "selected.CORPUS.yaml").unlink()

        with self.assertRaises(AuthorityAuditError) as captured:
            load_verified_authority_corpus(
                self.invocation(), "selected.CORPUS.yaml"
            )

        self.assertEqual(captured.exception.code, "corpus-documentation-unavailable")
        self.assertEqual(captured.exception.exit_class, "unavailable")
        self.assertEqual(list(self.output.iterdir()), [])

    def test_eyecite_extracts_and_resolves_without_claiming_verification(self):
        candidates = extract_eyecite_candidates(
            "Ashcroft v. Iqbal, 556 U.S. 662, 678 (2009). "
            "Iqbal, 556 U.S. at 679. Id. at 680. Iqbal, supra, at 681."
        )

        self.assertEqual(
            [candidate["kind"] for candidate in candidates],
            ["full", "short", "id", "supra"],
        )
        self.assertEqual(
            {candidate["resolved_citation"] for candidate in candidates},
            {"556 U.S. 662"},
        )
        self.assertTrue(all("verified" not in candidate for candidate in candidates))

    def test_valid_audit_publishes_folder_native_reports_and_preserves_inputs(self):
        before = {
            path.relative_to(self.root).as_posix(): path.read_bytes()
            for root in (self.filing, self.authorities)
            for path in root.rglob("*")
            if path.is_file()
        }

        result = run_and_publish_authority_audit(
            invocation=self.invocation(),
            corpus_documentation_path="selected.CORPUS.yaml",
            run_id="authority-audit-one",
            skill_version="1.0.0",
        )

        self.assertEqual(result.status, "passed")
        self.assertEqual(result.exit_class, "passed")
        self.assertEqual(result.findings, ())
        report = self.output / "reports/authority-audit.json"
        self.assertTrue(report.is_file())
        self.assertTrue((self.output / "reports/authority-audit.md").is_file())
        self.assertTrue((self.output / "run-receipt.yaml").is_file())
        self.assertNotIn(str(self.root), report.read_text())
        after = {
            path.relative_to(self.root).as_posix(): path.read_bytes()
            for root in (self.filing, self.authorities)
            for path in root.rglob("*")
            if path.is_file()
        }
        self.assertEqual(before, after)

    def test_missing_authority_and_bad_quote_are_stable_hard_findings(self):
        (self.filing / "motion.md").write_text(
            "Monell v. Department of Social Services, 436 U.S. 658 (1978).\n",
            encoding="utf-8",
        )
        authority_yaml = self.authorities / "iqbal.AUTHORITY.yaml"
        authority_yaml.write_text(
            authority_yaml.read_text().replace(
                "quotation: A claim has facial plausibility when the plaintiff pleads factual content.\n",
                "quotation: This quotation is not in the opinion.\n",
            ),
            encoding="utf-8",
        )

        result = run_and_publish_authority_audit(
            invocation=self.invocation(),
            corpus_documentation_path="selected.CORPUS.yaml",
            run_id="authority-audit-findings",
            skill_version="1.0.0",
        )

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.exit_class, "findings")
        self.assertEqual(
            {finding["check_id"] for finding in result.findings},
            {"missing-authority", "quotation-not-found"},
        )
        self.assertTrue(all(finding["severity"] == "hard" for finding in result.findings))

    def test_quotation_must_occur_at_the_asserted_pinpoint(self):
        original_digest = hashlib.sha256(self.opinion.read_bytes()).hexdigest()
        self.opinion.write_text(
            "[page 678]\nDifferent text.\n[page 679]\n"
            "A claim has facial plausibility when the plaintiff pleads factual content.\n",
            encoding="utf-8",
        )
        replacement_digest = hashlib.sha256(self.opinion.read_bytes()).hexdigest()
        for path in (
            self.authorities / "iqbal.SOURCE.yaml",
            self.authorities / "iqbal.AUTHORITY.yaml",
        ):
            path.write_text(
                path.read_text().replace(original_digest, replacement_digest),
                encoding="utf-8",
            )

        result = run_and_publish_authority_audit(
            invocation=self.invocation(),
            corpus_documentation_path="selected.CORPUS.yaml",
            run_id="authority-audit-pinpoint",
            skill_version="1.0.0",
        )

        self.assertEqual(result.exit_class, "findings")
        self.assertEqual(
            {finding["check_id"] for finding in result.findings},
            {"quotation-pinpoint-mismatch"},
        )

    def test_persistent_markup_resolves_by_authority_id_and_unusable_text_never_passes(self):
        (self.filing / "motion.md").write_text(
            '<cite id="cite-iqbal" authority="ashcroft-v-iqbal">'
            "Ashcroft v. Iqbal, 556 U.S. 662, 678 (2009)</cite>.\n",
            encoding="utf-8",
        )
        authority_yaml = self.authorities / "iqbal.AUTHORITY.yaml"
        authority_yaml.write_text(
            authority_yaml.read_text().replace(
                "text_layer_status: usable\n", "text_layer_status: unusable\n"
            ),
            encoding="utf-8",
        )

        result = run_and_publish_authority_audit(
            invocation=self.invocation(),
            corpus_documentation_path="selected.CORPUS.yaml",
            run_id="authority-audit-visual",
            skill_version="1.0.0",
        )

        self.assertEqual(result.exit_class, "findings")
        self.assertEqual(
            {finding["check_id"] for finding in result.findings},
            {"visual-review-required"},
        )
        report = json.loads(
            (self.output / "reports/authority-audit.json").read_text()
        )
        self.assertEqual(
            report["persistent_citations"],
            [
                {
                    "authority_id": "ashcroft-v-iqbal",
                    "authority_yaml_path": "iqbal.AUTHORITY.yaml",
                    "citation_id": "cite-iqbal",
                    "document_path": "iqbal.txt",
                    "source_yaml_path": "iqbal.SOURCE.yaml",
                }
            ],
        )

    def test_report_bytes_are_deterministic_and_transient_files_are_output_local(self):
        second_output = self.root / "second-output"
        second_output.mkdir()

        first = run_and_publish_authority_audit(
            invocation=self.invocation(),
            corpus_documentation_path="selected.CORPUS.yaml",
            run_id="authority-audit-repeat",
            skill_version="1.0.0",
        )
        second = run_and_publish_authority_audit(
            invocation=self.invocation(second_output),
            corpus_documentation_path="selected.CORPUS.yaml",
            run_id="authority-audit-repeat",
            skill_version="1.0.0",
        )

        self.assertEqual(first, second)
        for relative_path in (
            "reports/authority-audit.json",
            "reports/authority-audit.md",
            "run-receipt.yaml",
            ".skill-runs/authority-audit-repeat/manifest.json",
        ):
            self.assertEqual(
                (self.output / relative_path).read_bytes(),
                (second_output / relative_path).read_bytes(),
            )
        for output in (self.output, second_output):
            temp = output / "temp"
            self.assertTrue(temp.is_dir())
            self.assertEqual(
                [path for path in temp.rglob("*") if path.is_file()],
                [],
            )


if __name__ == "__main__":
    unittest.main()
