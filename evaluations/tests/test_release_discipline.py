import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
README_PATH = REPOSITORY_ROOT / "README.md"
PUBLISHING_PATH = REPOSITORY_ROOT / "PUBLISHING.md"
CONTRIBUTING_PATH = REPOSITORY_ROOT / "CONTRIBUTING.md"
RELEASE_WORKFLOW_PATH = REPOSITORY_ROOT / ".github" / "workflows" / "release.yml"
PINNED_SOURCE = re.compile(
    r"^https://github\.com/PoliceConductUS/section-1983-skills/tree/"
    r"(?P<tag>v\d+\.\d+\.\d+)$"
)


def read(path):
    return path.read_text(encoding="utf-8")


def remote_install_sources(markdown):
    sources = []
    for line in markdown.splitlines():
        command = line.strip()
        if not command.startswith("npx skills add "):
            continue
        source = command.removeprefix("npx skills add ").split()[0]
        if source != ".":
            sources.append(source)
    return sources


class ReleaseDisciplineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = read(README_PATH)
        cls.publishing = read(PUBLISHING_PATH)
        cls.contributing = read(CONTRIBUTING_PATH)
        cls.workflow = read(RELEASE_WORKFLOW_PATH) if RELEASE_WORKFLOW_PATH.exists() else ""

    def assert_workflow_order(self, *commands):
        positions = [self.workflow.find(command) for command in commands]
        self.assertNotIn(-1, positions, f"missing release command: {commands}")
        self.assertEqual(positions, sorted(positions), f"unsafe release order: {commands}")

    def test_every_remote_install_uses_one_immutable_semantic_version_tag(self):
        sources = remote_install_sources(self.readme)
        self.assertGreaterEqual(len(sources), 3)
        tags = []
        for source in sources:
            with self.subTest(source=source):
                match = PINNED_SOURCE.fullmatch(source)
                self.assertIsNotNone(match, f"unpinned remote install source: {source}")
                tags.append(match.group("tag"))
        self.assertEqual(len(set(tags)), 1, f"README install versions differ: {tags}")
        self.assertNotIn("npx skills update", self.readme)

    def test_release_documents_do_not_publish_a_moving_main_branch(self):
        combined = f"{self.readme}\n{self.publishing}\n{self.contributing}".lower()
        self.assertNotRegex(combined, r"main`?\s+is\s+the\s+stable\s+release\s+branch")
        self.assertNotRegex(combined, r"treat\s+`?main`?\s+as\s+the\s+stable")
        self.assertIn("immutable", combined)
        self.assertIn("integration", combined)
        self.assertRegex(
            self.publishing,
            r"gh workflow run release\.yml --ref main -f version=v\d+\.\d+\.\d+",
        )

    def test_release_workflow_is_manual_and_rejects_non_main_refs(self):
        self.assertIn("workflow_dispatch:", self.workflow)
        self.assertNotRegex(self.workflow, r"(?m)^\s+tags:")
        self.assertIn("github.ref == 'refs/heads/main'", self.workflow)
        self.assertRegex(self.workflow, r"(?m)^permissions:\s*\n\s+contents: write$")
        self.assertRegex(
            self.workflow,
            r"(?m)^\s+version:\s*\n(?:\s+.+\n)*?\s+required: true$",
        )

    def test_release_workflow_validates_version_and_remote_tag_before_install(self):
        self.assertRegex(
            self.workflow,
            r"\^v\[0-9\]\+\\\.\[0-9\]\+\\\.\[0-9\]\+\$",
        )
        self.assertIn(
            'git ls-remote --exit-code --tags origin "refs/tags/$RELEASE_VERSION"',
            self.workflow,
        )
        self.assert_workflow_order(
            "git ls-remote --exit-code --tags",
            "npm ci",
            "npm run validate",
        )

    def test_release_workflow_creates_tag_only_after_full_validation(self):
        self.assertIn("uses: actions/checkout@v6", self.workflow)
        self.assertIn("fetch-depth: 0", self.workflow)
        self.assert_workflow_order(
            "npm ci",
            "npm run validate",
            "git tag --annotate",
            "git push origin",
            "gh release create",
        )
        self.assertIn("--verify-tag", self.workflow)
        self.assertIn("--generate-notes", self.workflow)


if __name__ == "__main__":
    unittest.main()
