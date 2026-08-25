import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "building-judicial-reasoning-profiles"
FIXTURES = SKILL / "references" / "fixtures"


class JudicialReasoningProfileStructureTest(unittest.TestCase):
    def test_generic_skill_has_exact_install_local_surface(self):
        expected = {
            "SKILL.md",
            "agents/openai.yaml",
            "references/folder-contract.json",
            "references/immutable-folder-package.md",
            "references/judicial-reasoning-profile.schema.json",
            "references/fixtures/complete-profile.json",
            "references/fixtures/thin-profile.json",
            "references/fixtures/adoption-only-profile.json",
            "references/fixtures/hostile-profile.json",
        }
        actual = {
            path.relative_to(SKILL).as_posix()
            for path in SKILL.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        }
        self.assertEqual(actual, expected)

    def test_folder_contract_and_discovery_are_generic(self):
        contract = json.loads(
            (SKILL / "references" / "folder-contract.json").read_text()
        )
        self.assertEqual(
            contract,
            {
                "version": 1,
                "skill": "building-judicial-reasoning-profiles",
                "input_roles": [
                    "judge-identity",
                    "court-scope",
                    "approved-sources",
                    "verified-authorities",
                ],
                "target": {"policy": "none", "roles": []},
                "internet": "authorized",
                "output": {"mode": "append-immutable"},
            },
        )
        skill = (SKILL / "SKILL.md").read_text()
        metadata = (SKILL / "agents" / "openai.yaml").read_text()
        self.assertIn("name: building-judicial-reasoning-profiles", skill)
        self.assertIn("Use when", skill)
        self.assertIn("$building-judicial-reasoning-profiles", metadata)
        self.assertNotIn("Scholer", skill + metadata)

    def test_skill_separates_acquisition_compilation_and_role_behavior(self):
        text = (SKILL / "SKILL.md").read_text().lower()
        self.assertIn("## acquisition operation", text)
        self.assertIn("## compilation operation", text)
        self.assertIn("later invocation", text)
        self.assertIn("internet is `disabled`", text)
        self.assertIn("internet is `authorized`", text)
        self.assertIn("profile data", text)
        self.assertIn("static role", text)
        self.assertIn("does not predict", text)
        self.assertIn("does not generate", text)

    def test_schema_and_fictional_fixtures_define_domain_contract(self):
        schema = json.loads(
            (SKILL / "references" / "judicial-reasoning-profile.schema.json").read_text()
        )
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(
            schema["required"],
            [
                "schema_version",
                "profile_id",
                "checked_through",
                "judge_identity",
                "court_scope",
                "records",
                "comparisons",
                "neutral_transfers",
                "assumptions",
                "gaps",
                "validation",
            ],
        )
        self.assertEqual(
            schema["$defs"]["record"]["properties"]["source_class"]["enum"],
            [
                "revealed_reasoning",
                "stated_philosophy",
                "self_presentation",
                "court_compliance",
            ],
        )
        for name in (
            "complete-profile",
            "thin-profile",
            "adoption-only-profile",
            "hostile-profile",
        ):
            value = json.loads((FIXTURES / f"{name}.json").read_text())
            self.assertTrue(value["judge_identity"]["fictional"], name)
            self.assertNotIn("real", value["profile_id"])


if __name__ == "__main__":
    unittest.main()
