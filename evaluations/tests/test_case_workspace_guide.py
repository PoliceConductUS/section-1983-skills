import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
README_PATH = REPOSITORY_ROOT / "README.md"
GUIDE_PATH = REPOSITORY_ROOT / "CASE_WORKSPACE.md"
PINNED_INSTALL_SOURCE = re.compile(
    r"https://github\.com/PoliceConductUS/section-1983-skills/tree/"
    r"v(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)$"
)
SAFETY_OBLIGATIONS = {
    "source classification": (
        r"without converting an allegation or inference into a fact"
    ),
    "human approval": (
        r"only an actual user approval changes a protected decision"
        r" to `status: approved`"
    ),
    "immutable inputs": r"never overwrite immutable inputs",
    "configured validation": r"run only validation commands configured by the project",
    "not filing ready": r"workspace is not filing-ready",
}


def prose_markdown(markdown):
    return re.sub(r"(?ms)^```.*?^```\s*", "", markdown)


def case_workspace_link_destinations(markdown):
    return [
        destination
        for label, destination in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", prose_markdown(markdown))
        if "case workspace" in label.lower()
    ]


def remote_install_sources(markdown):
    return [
        match.group(1)
        for match in re.finditer(r"(?m)^npx skills add (https://\S+)(?:\s|$)", markdown)
    ]


class CaseWorkspaceGuideTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = README_PATH.read_text(encoding="utf-8")
        cls.guide = GUIDE_PATH.read_text(encoding="utf-8") if GUIDE_PATH.exists() else ""
        cls.normalized = " ".join(cls.guide.lower().split())

    def test_readme_links_install_local_guide(self):
        self.assertTrue(GUIDE_PATH.is_file())
        destinations = case_workspace_link_destinations(self.readme)
        self.assertEqual(destinations, ["CASE_WORKSPACE.md"])
        resolved = (REPOSITORY_ROOT / destinations[0]).resolve()
        resolved.relative_to(REPOSITORY_ROOT.resolve())
        self.assertEqual(resolved, GUIDE_PATH.resolve())

    def test_link_guard_rejects_traversal_and_fenced_decoy(self):
        mutated = self.readme.replace(
            "(CASE_WORKSPACE.md)", "(../outside/CASE_WORKSPACE.md)"
        )
        mutated += "\n```markdown\n[Start a case workspace](CASE_WORKSPACE.md)\n```\n"
        self.assertNotEqual(
            case_workspace_link_destinations(mutated), ["CASE_WORKSPACE.md"]
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

    def test_safety_obligations_reject_reversed_semantics(self):
        for obligation, pattern in SAFETY_OBLIGATIONS.items():
            with self.subTest(obligation=obligation):
                self.assertRegex(self.normalized, pattern)
        mutations = {
            "source classification": "convert an allegation or inference into a fact",
            "human approval": (
                "no actual user approval is required to change a protected decision "
                "to `status: approved`"
            ),
            "immutable inputs": "overwrite immutable inputs",
            "configured validation": "run guessed validation commands",
            "not filing ready": "workspace is filing-ready",
        }
        for obligation, mutation in mutations.items():
            with self.subTest(inversion=obligation):
                self.assertNotRegex(mutation, SAFETY_OBLIGATIONS[obligation])

    def test_install_is_pinned_and_examples_are_generic(self):
        sources = remote_install_sources(self.guide)
        self.assertEqual(len(sources), 1)
        self.assertIsNotNone(PINNED_INSTALL_SOURCE.fullmatch(sources[0]))
        self.assertIn("npx skills add . --list", self.guide)
        self.assertIn("tag has not been published", self.normalized)
        self.assertIn("do not substitute `main`", self.normalized)
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

    def test_tag_guard_rejects_noncanonical_suffix(self):
        mutated = self.guide.replace("/tree/v0.1.0", "/tree/v0.1.0-main")
        sources = remote_install_sources(mutated)
        self.assertEqual(len(sources), 1)
        self.assertIsNone(PINNED_INSTALL_SOURCE.fullmatch(sources[0]))

    def test_deliverable_does_not_create_scaffolding(self):
        self.assertFalse((REPOSITORY_ROOT / "templates").exists())
        self.assertFalse((REPOSITORY_ROOT / "scripts" / "scaffold_case.py").exists())
        self.assertIn("does not create", self.normalized)
        self.assertIn("template", self.normalized)
        self.assertIn("scaffolding", self.normalized)


if __name__ == "__main__":
    unittest.main()
