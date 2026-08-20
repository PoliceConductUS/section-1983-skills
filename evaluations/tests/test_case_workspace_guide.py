import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
README_PATH = REPOSITORY_ROOT / "README.md"
GUIDE_PATH = REPOSITORY_ROOT / "CASE_WORKSPACE.md"
PINNED_INSTALL = re.compile(
    r"npx skills add "
    r"https://github\.com/PoliceConductUS/section-1983-skills/tree/"
    r"v(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
)


class CaseWorkspaceGuideTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = README_PATH.read_text(encoding="utf-8")
        cls.guide = GUIDE_PATH.read_text(encoding="utf-8") if GUIDE_PATH.exists() else ""
        cls.normalized = " ".join(cls.guide.lower().split())

    def test_readme_links_install_local_guide(self):
        self.assertTrue(GUIDE_PATH.is_file())
        self.assertRegex(
            self.readme,
            r"\[[^\]]*(?:start|starting)[^\]]*case workspace[^\]]*\]"
            r"\(CASE_WORKSPACE\.md\)",
        )
        self.assertNotRegex(
            self.readme,
            r"\[[^\]]*case workspace[^\]]*\]\((?:https?://|/)",
        )

    def test_first_hour_flow_is_complete_and_ordered(self):
        headings = (
            "## 1. Choose a workspace root",
            "## 2. Record approved sources",
            "## 3. Add a chronology entry",
            "## 4. Record a protected decision",
            "## 5. Separate inputs from generated artifacts",
            "## 6. Run available validation",
        )
        positions = [self.guide.find(heading) for heading in headings]
        self.assertNotIn(-1, positions)
        self.assertEqual(positions, sorted(positions))
        for role in (
            "strategy",
            "chronology",
            "approved source",
            "verified authorit",
            "protected decision",
            "gap",
            "immutable input",
            "generated artifact",
        ):
            with self.subTest(role=role):
                self.assertIn(role, self.normalized)

    def test_examples_are_source_bounded_and_portable(self):
        self.assertIn("SRC-001", self.guide)
        self.assertRegex(self.guide, r"source_ids:\s*\[SRC-001\]")
        self.assertRegex(self.guide, r"status:\s*approved")
        self.assertRegex(
            self.normalized,
            r"(?:rename|different name).{0,160}(?:equivalent role|role mapping)",
        )
        self.assertIn("example paths", self.normalized)
        self.assertIn("not mandatory", self.normalized)

    def test_missing_material_and_tools_never_masquerade_as_ready(self):
        for phrase in (
            "do not invent",
            "validation unavailable",
            "record a gap",
            "not filing-ready",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.normalized)

    def test_install_is_pinned_and_examples_are_generic(self):
        self.assertRegex(self.guide, PINNED_INSTALL)
        for private_marker in (
            "/Users/",
            "C:\\Users\\",
            "3-25-CV",
            "Lotts",
            "Irving",
        ):
            with self.subTest(private_marker=private_marker):
                self.assertNotIn(private_marker, self.guide)
        self.assertIn("generic synthetic example", self.normalized)

    def test_deliverable_does_not_create_scaffolding(self):
        self.assertFalse((REPOSITORY_ROOT / "templates").exists())
        self.assertFalse((REPOSITORY_ROOT / "scripts" / "scaffold_case.py").exists())
        self.assertIn("does not create", self.normalized)
        self.assertIn("template", self.normalized)
        self.assertIn("scaffolding", self.normalized)


if __name__ == "__main__":
    unittest.main()
