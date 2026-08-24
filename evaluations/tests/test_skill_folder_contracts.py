import json
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]

CONTRACTS = {
    "adversarial-filing-review": (["filing", "approved-sources"], "required", ["filing"], "authorized"),
    "audit-authorities": (["filing", "authorities"], "required", ["filing"], "authorized"),
    "auditing-section-1983-discovery-responses": (
        ["served-discovery", "responses", "production", "authorities"],
        "optional",
        ["served-discovery", "responses"],
        "disabled",
    ),
    "auditing-section-1983-privilege-logs": (
        ["privilege-log", "served-discovery", "authorities"],
        "optional",
        ["privilege-log"],
        "disabled",
    ),
    "building-defense-counsel-overlays": (
        ["research-snapshot", "case-record"],
        "required",
        ["research-snapshot"],
        "disabled",
    ),
    "building-litigation-alignment-overlays": (
        ["docket-snapshot", "filing"],
        "required",
        ["docket-snapshot"],
        "disabled",
    ),
    "drafting-false-arrest-complaints": (
        ["record", "authorities", "filing"],
        "optional",
        ["filing"],
        "disabled",
    ),
    "drafting-for-judge-scholer": (
        ["filing", "judge-corpus", "court-conduct"],
        "required",
        ["filing"],
        "disabled",
    ),
    "drafting-section-1983-complaints": (
        ["record", "authorities", "filing"],
        "optional",
        ["filing"],
        "disabled",
    ),
    "drafting-section-1983-declarations-and-evidence": (
        ["record", "authorities"],
        "optional",
        ["record"],
        "disabled",
    ),
    "drafting-section-1983-deposition-outlines": (
        ["record", "authorities", "discovery"],
        "optional",
        ["record"],
        "disabled",
    ),
    "drafting-section-1983-meet-and-confer": (
        ["discovery-audit", "served-discovery", "authorities", "conference-record"],
        "required",
        ["discovery-audit"],
        "disabled",
    ),
    "drafting-section-1983-rule-59e": (
        ["record", "authorities", "filing"],
        "optional",
        ["filing"],
        "disabled",
    ),
    "drafting-section-1983-written-discovery": (
        ["record", "authorities", "claim-map"],
        "optional",
        ["claim-map"],
        "disabled",
    ),
    "filing-ci": (["filing", "authorities"], "required", ["filing"], "disabled"),
    "horan-bad-words": (["filing"], "required", ["filing"], "disabled"),
    "rrd": (["motion", "record", "authorities"], "required", ["motion"], "disabled"),
    "rrd-rule12": (["motion", "record", "authorities"], "required", ["motion"], "disabled"),
    "rrd-rule12-city": (["motion", "record", "authorities"], "required", ["motion"], "disabled"),
    "rrd-rule12-officers": (["motion", "record", "authorities"], "required", ["motion"], "disabled"),
    "section-1983-drafting": (
        ["record", "authorities", "strategy", "filing"],
        "optional",
        ["filing"],
        "authorized",
    ),
    "studying-rule-59e-decisions": (
        ["decisions", "authorities"],
        "optional",
        ["decisions"],
        "authorized",
    ),
}


def expected_contract(skill, values):
    input_roles, target_policy, target_roles, internet = values
    return {
        "version": 1,
        "skill": skill,
        "input_roles": input_roles,
        "target": {"policy": target_policy, "roles": target_roles},
        "internet": internet,
        "output": {"mode": "append-immutable"},
    }


class SkillFolderContractsTest(unittest.TestCase):
    def test_matrix_covers_exactly_the_public_skills(self):
        discovered = {
            path.parent.name for path in (REPOSITORY / "skills").glob("*/SKILL.md")
        }
        self.assertEqual(discovered, set(CONTRACTS))

    def test_strict_contract_schema_is_published(self):
        schema = REPOSITORY / "governance" / "skill-folder-contract.schema.json"
        self.assertTrue(schema.is_file(), f"missing contract schema: {schema}")

    def test_every_skill_publishes_its_exact_install_local_contract(self):
        for skill, values in CONTRACTS.items():
            with self.subTest(skill=skill):
                path = REPOSITORY / "skills" / skill / "references" / "folder-contract.json"
                self.assertTrue(path.is_file(), f"missing folder contract: {skill}")
                self.assertEqual(json.loads(path.read_text()), expected_contract(skill, values))


if __name__ == "__main__":
    unittest.main()
