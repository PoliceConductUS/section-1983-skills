import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]


class SourceDocumentedFoldersTest(unittest.TestCase):
    def test_generic_package_layer_is_absent(self):
        rejected_paths = (
            "FOLDER_PACKAGES.md",
            "governance/immutable-folder-package.schema.json",
            "governance/static-role-contract.schema.json",
            "scripts/immutable_folder_package.py",
            "scripts/static_role_binding.py",
            "evaluations/folder-package-fixtures",
            "openspec/specs/immutable-folder-packages",
        )

        for relative_path in rejected_paths:
            with self.subTest(path=relative_path):
                path = REPOSITORY / relative_path
                self.assertFalse(
                    path.is_file()
                    or (path.is_dir() and any(item.is_file() for item in path.rglob("*")))
                )

    def test_public_guide_uses_declared_folders_and_domain_yaml(self):
        guide = REPOSITORY / "SOURCE_DOCUMENTED_FOLDERS.md"
        self.assertTrue(guide.is_file())
        text = guide.read_text(encoding="utf-8").lower()

        for required in (
            "declared input folders",
            "recursive read-only",
            "explicit output folder",
            "<output-folder>/temp/",
            "domain-owned yaml",
            "source.yaml",
            "folder-relative",
            "sha-256",
            "protected behavior",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

        for rejected in (
            "package-manifest.json",
            "package loader",
            "package publisher",
            "package registry",
        ):
            with self.subTest(rejected=rejected):
                self.assertNotIn(rejected, text)

    def test_repository_and_overlay_guidance_do_not_require_packages(self):
        paths = (
            "README.md",
            "FOLDER_OPERATIONS.md",
            "GOVERNANCE.md",
            "skills/building-defense-counsel-overlays/SKILL.md",
            "skills/building-litigation-alignment-overlays/SKILL.md",
        )
        rejected = (
            "immutable folder package",
            "profile package",
            "package-manifest.json",
        )

        for relative_path in paths:
            text = (REPOSITORY / relative_path).read_text(encoding="utf-8").lower()
            for phrase in rejected:
                with self.subTest(path=relative_path, phrase=phrase):
                    self.assertNotIn(phrase, text)

        readme = (REPOSITORY / "README.md").read_text(encoding="utf-8")
        self.assertIn("SOURCE_DOCUMENTED_FOLDERS.md", readme)

    def test_overlay_skills_link_to_source_documentation_guidance(self):
        for skill in (
            "building-defense-counsel-overlays",
            "building-litigation-alignment-overlays",
        ):
            skill_root = REPOSITORY / "skills" / skill
            reference = skill_root / "references" / "source-documented-folders.md"
            with self.subTest(skill=skill):
                self.assertTrue(reference.is_file())
                entrypoint = (skill_root / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("references/source-documented-folders.md", entrypoint)
                self.assertFalse(
                    (skill_root / "references" / "immutable-folder-package.md").exists()
                )


if __name__ == "__main__":
    unittest.main()
