import re
import unittest
from pathlib import Path

from evaluations.tests.test_skill_folder_contracts import CONTRACTS


REPOSITORY = Path(__file__).resolve().parents[2]


class SkillFolderGuidanceTest(unittest.TestCase):
    def section(self, skill):
        text = (REPOSITORY / "skills" / skill / "SKILL.md").read_text(
            encoding="utf-8"
        )
        match = re.search(
            r"^## Folder inputs and output\n(?P<section>.*?)(?=^## |\Z)",
            text,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(match, f"missing folder guidance: {skill}")
        return re.sub(r"\s+", " ", match.group("section")).strip().lower()

    def test_every_installed_skill_explains_its_exact_contract(self):
        for skill, values in CONTRACTS.items():
            roles, target_policy, target_roles, internet = values
            with self.subTest(skill=skill):
                section = self.section(skill)
                for role in roles:
                    self.assertIn(f"`{role}`", section)
                if target_policy == "none":
                    self.assertIn("target is none", section)
                else:
                    self.assertIn(
                        f"target is {target_policy} in "
                        + " or ".join(f"`{role}`" for role in target_roles),
                        section,
                    )
                policies = internet if isinstance(internet, list) else [internet]
                for policy in policies:
                    self.assertIn(f"`{policy}`", section)
                self.assertIn("canonical output-relative path", section)
                self.assertIn("append-immutable", section)
                self.assertIn("only the trusted host", section)
                self.assertRegex(section, r"report.{0,220}gap")

    def test_composition_never_unions_skill_authority(self):
        readme = re.sub(
            r"\s+",
            " ",
            (REPOSITORY / "README.md").read_text(encoding="utf-8"),
        ).lower()
        self.assertRegex(
            readme,
            r"(?:compose|composition).{0,240}invok.{0,120}separately",
        )
        self.assertRegex(readme, r"(?:never|does not).{0,100}union.{0,100}roles")
        self.assertRegex(
            readme,
            r"output.{0,160}new invocation.{0,160}declared input role",
        )

    def test_current_public_runtime_instructions_are_folder_native(self):
        roots = [REPOSITORY / "skills", REPOSITORY / "README.md"]
        files = []
        for root in roots:
            files.extend(root.rglob("*.md") if root.is_dir() else [root])
        current = "\n".join(path.read_text(encoding="utf-8") for path in files)
        forbidden = (
            r"project integration",
            r"repository-defined response path",
            r"response path required by the repository",
            r"default to `responses/",
            r"project['’]s existing version and audit system",
            r"project-defined localization",
            r"configured cache",
            r"approved project preflight",
            r"read the repository `agents\.md`",
            r"repository supplies `agents\.md`",
            r"verified-authorities tool or repository",
            r"local authorities repository",
            r"canonical verified-case root from the project",
            r"create it following the project `source\.yaml`",
            r"save to `responses/",
            r"write to two\s+separate folders",
            r"write a new versioned ledger",
            r"write only its designated report",
            r"external[-\s]+checker\s+handoff",
        )
        for pattern in forbidden:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, current, flags=re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
