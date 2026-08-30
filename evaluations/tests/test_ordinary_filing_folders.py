import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

OBSOLETE_PATHS = (
    "FILING_PACKETS.md",
    "scripts/filing_packet.py",
    "governance/filing-packet.schema.json",
    "evaluations/filing-packet-fixtures",
    "evaluations/tests/test_filing_packets.py",
    "openspec/specs/filing-packet-lifecycle",
)

FILING_SKILLS = (
    "section-1983-drafting",
    "drafting-section-1983-complaints",
    "drafting-section-1983-rule-59e",
    "drafting-false-arrest-complaints",
    "adversarial-filing-review",
)

CURRENT_GUIDANCE = (
    "README.md",
    "GOVERNANCE.md",
    "FOLDER_OPERATIONS.md",
    "openspec/specs/case-workspace-start-guide/spec.md",
    "openspec/specs/repository-skill-governance/spec.md",
)


class OrdinaryFilingFoldersTest(unittest.TestCase):
    def test_obsolete_filing_packet_implementation_is_deleted(self):
        for relative in OBSOLETE_PATHS:
            with self.subTest(path=relative):
                self.assertFalse((ROOT / relative).exists())

    def test_install_local_filing_packet_contracts_are_deleted(self):
        for skill in FILING_SKILLS:
            reference = (
                ROOT / "skills" / skill / "references" / "filing-packet-contract.md"
            )
            with self.subTest(skill=skill):
                self.assertFalse(reference.exists())

    def test_filing_skills_use_ordinary_folders_and_explicit_targets(self):
        for skill in FILING_SKILLS:
            text = " ".join(
                (ROOT / "skills" / skill / "SKILL.md").read_text().lower().split()
            )
            with self.subTest(skill=skill):
                self.assertIn("## filing folder boundary", text)
                self.assertIn("ordinary files", text)
                self.assertIn("folder-relative path", text)
                self.assertIn("no folder-wide manifest", text)
                self.assertIn("<output-folder>/temp/", text)
                self.assertNotIn("filingpacket", text)
                self.assertNotIn("filing-packet.json", text)

    def test_current_guidance_has_no_filing_packet_contract(self):
        for relative in CURRENT_GUIDANCE:
            text = (ROOT / relative).read_text().lower()
            with self.subTest(path=relative):
                self.assertNotIn("filingpacket", text)
                self.assertNotIn("filing-packet.json", text)
                self.assertNotIn("filing-packet-contract", text)

    def test_public_guidance_states_the_no_replacement_boundary(self):
        for relative in ("README.md", "GOVERNANCE.md", "FOLDER_OPERATIONS.md"):
            text = " ".join((ROOT / relative).read_text().lower().split())
            with self.subTest(path=relative):
                self.assertIn("ordinary filing folder", text)
                self.assertIn("no folder-wide manifest", text)
                self.assertIn("folder-relative path", text)
                self.assertIn("<output-folder>/temp/", text)

    def test_current_code_has_no_replacement_filing_persistence_module(self):
        forbidden = {
            "filing_packet.py",
            "filing_package.py",
            "filing_manifest.py",
            "filing_index.py",
            "filing_registry.py",
            "filing_graph.py",
            "filing_repository.py",
            "filing_datastore.py",
        }
        current = {
            path.name
            for root in (ROOT / "scripts", ROOT / "governance")
            for path in root.rglob("*")
            if path.is_file()
        }
        self.assertTrue(forbidden.isdisjoint(current), forbidden & current)


if __name__ == "__main__":
    unittest.main()
