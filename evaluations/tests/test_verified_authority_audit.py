import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.verified_authority_audit import (
    AuthorityAuditError,
    load_verified_authority_corpus,
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
            "At page 678: A claim has facial plausibility when the plaintiff "
            "pleads factual content.\n",
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

    def invocation(self):
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
                "output": {"root": str(self.output)},
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


if __name__ == "__main__":
    unittest.main()
