import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_governance import (
    APPROVED_FOLDER_CONTRACTS,
    validate_folder_contract_document,
    validate_skill_folder_contracts,
)


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
        document = json.loads(schema.read_text())
        self.assertFalse(document["additionalProperties"])
        self.assertEqual(
            document["required"],
            ["version", "skill", "input_roles", "target", "internet", "output"],
        )
        self.assertFalse(document["properties"]["target"]["additionalProperties"])
        self.assertFalse(document["properties"]["output"]["additionalProperties"])

    def test_every_skill_publishes_its_exact_install_local_contract(self):
        for skill, values in CONTRACTS.items():
            with self.subTest(skill=skill):
                path = REPOSITORY / "skills" / skill / "references" / "folder-contract.json"
                self.assertTrue(path.is_file(), f"missing folder contract: {skill}")
                self.assertEqual(json.loads(path.read_text()), expected_contract(skill, values))

    def test_governance_matrix_matches_the_approved_contracts(self):
        expected = {
            skill: expected_contract(skill, values) for skill, values in CONTRACTS.items()
        }
        self.assertEqual(APPROVED_FOLDER_CONTRACTS, expected)

    def test_document_validation_rejects_contract_mutations_with_stable_findings(self):
        valid = expected_contract("filing-ci", CONTRACTS["filing-ci"])
        mutations = (
            ("extra", {**valid, "extra": True}, "invalid-folder-contract-shape"),
            ("version", {**valid, "version": 2}, "invalid-folder-contract-version"),
            ("skill", {**valid, "skill": "other"}, "skill-folder-contract-mismatch"),
            (
                "missing roles",
                {**valid, "input_roles": []},
                "invalid-folder-contract-input-roles",
            ),
            (
                "duplicate roles",
                {**valid, "input_roles": ["filing", "filing"]},
                "invalid-folder-contract-input-roles",
            ),
            (
                "unsafe role",
                {**valid, "input_roles": ["../filing", "authorities"]},
                "invalid-folder-contract-input-roles",
            ),
            (
                "target policy",
                {**valid, "target": {"policy": "sometimes", "roles": ["filing"]}},
                "invalid-folder-contract-target",
            ),
            (
                "target role",
                {**valid, "target": {"policy": "required", "roles": ["other"]}},
                "invalid-folder-contract-target",
            ),
            (
                "internet",
                {**valid, "internet": "ambient"},
                "invalid-folder-contract-internet",
            ),
            (
                "output",
                {**valid, "output": {"mode": "overwrite"}},
                "invalid-folder-contract-output",
            ),
        )
        self.assertEqual(validate_folder_contract_document(valid, "filing-ci"), [])
        for label, document, finding in mutations:
            with self.subTest(mutation=label):
                self.assertIn(
                    finding,
                    validate_folder_contract_document(document, "filing-ci"),
                )

    def test_governance_rejects_missing_and_reordered_live_contracts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(REPOSITORY / "skills", root / "skills")
            contract = (
                root
                / "skills"
                / "filing-ci"
                / "references"
                / "folder-contract.json"
            )
            contract.unlink()
            self.assertIn(
                "skill-folder-contract-missing: filing-ci",
                validate_skill_folder_contracts(root),
            )

            contract.write_text(
                json.dumps(
                    {
                        **expected_contract("filing-ci", CONTRACTS["filing-ci"]),
                        "input_roles": ["authorities", "filing"],
                    }
                )
            )
            self.assertIn(
                "skill-folder-contract-mismatch: filing-ci",
                validate_skill_folder_contracts(root),
            )

    def test_each_isolated_package_retains_its_contract_and_local_link(self):
        for skill in CONTRACTS:
            with self.subTest(skill=skill), tempfile.TemporaryDirectory() as directory:
                package = Path(directory) / skill
                shutil.copytree(REPOSITORY / "skills" / skill, package)
                contract = package / "references" / "folder-contract.json"
                self.assertTrue(contract.is_file())
                entrypoint = (package / "SKILL.md").read_text()
                self.assertIn(
                    "[folder contract](references/folder-contract.json)",
                    entrypoint.lower(),
                )


if __name__ == "__main__":
    unittest.main()
