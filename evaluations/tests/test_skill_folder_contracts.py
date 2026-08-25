import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_folder_invocation import (
    InvocationError,
    validate_installed_skill_invocation,
)
from scripts.validate_governance import (
    APPROVED_FOLDER_CONTRACTS,
    validate_folder_contract_document,
    validate_skill_folder_contracts,
)


REPOSITORY = Path(__file__).resolve().parents[2]

CONTRACTS = {
    "adversarial-filing-review": (["filing", "approved-sources"], "required", ["filing"], "authorized"),
    "audit-authorities": (
        ["filing-source", "verified-authority"],
        "required",
        ["filing-source"],
        {"audit": "disabled", "freshness-research": "authorized"},
    ),
    "auditing-section-1983-discovery-responses": (
        ["served-discovery", "responses", "production", "authorities"],
        "required",
        ["served-discovery", "responses"],
        "disabled",
    ),
    "auditing-section-1983-privilege-logs": (
        ["privilege-log", "served-discovery", "authorities"],
        "required",
        ["privilege-log"],
        "disabled",
    ),
    "building-defense-counsel-overlays": (
        ["research-snapshot", "case-record"],
        "required",
        ["research-snapshot"],
        "disabled",
    ),
    "building-judicial-reasoning-profiles": (
        [
            "judge-identity",
            "court-scope",
            "approved-sources",
            "verified-authorities",
        ],
        "none",
        [],
        {"acquisition": "authorized", "compilation": "disabled"},
    ),
    "judicial-reviewer": (
        ["profile", "filing", "approved-sources"],
        "required",
        ["filing"],
        "disabled",
    ),
    "opposing-counsel": (
        ["profile", "filing", "approved-sources"],
        "required",
        ["filing"],
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
    "filing-ci": (
        [
            "filing-source",
            "filing-index",
            "record-reference",
            "exhibit",
            "docket-to-appendix",
            "verified-authority",
        ],
        "required",
        ["filing-source"],
        "disabled",
    ),
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


def schema_errors(instance, schema, path="$"):
    errors = []
    if "oneOf" in schema:
        matches = [
            candidate
            for candidate in schema["oneOf"]
            if not schema_errors(instance, candidate, path)
        ]
        return [] if len(matches) == 1 else [f"{path}: oneOf mismatch"]
    expected_type = schema.get("type")
    type_matches = {
        "object": isinstance(instance, dict),
        "array": isinstance(instance, list),
        "string": isinstance(instance, str),
        "integer": type(instance) is int,
    }
    if expected_type and not type_matches[expected_type]:
        return [f"{path}: expected {expected_type}"]
    if "const" in schema and (
        type(instance) is not type(schema["const"]) or instance != schema["const"]
    ):
        errors.append(f"{path}: const mismatch")
    if "enum" in schema and not any(
        type(instance) is type(value) and instance == value for value in schema["enum"]
    ):
        errors.append(f"{path}: enum mismatch")
    if isinstance(instance, dict):
        required = schema.get("required", [])
        errors.extend(f"{path}: missing {key}" for key in required if key not in instance)
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            errors.extend(
                f"{path}: unexpected {key}" for key in instance if key not in properties
            )
        for key, value in instance.items():
            if key in properties:
                errors.extend(schema_errors(value, properties[key], f"{path}.{key}"))
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            errors.append(f"{path}: too few items")
        if schema.get("uniqueItems"):
            canonical = [json.dumps(item, sort_keys=True) for item in instance]
            if len(canonical) != len(set(canonical)):
                errors.append(f"{path}: duplicate items")
        item_schema = schema.get("items")
        if item_schema:
            for index, value in enumerate(instance):
                errors.extend(schema_errors(value, item_schema, f"{path}[{index}]"))
    if isinstance(instance, str) and "pattern" in schema:
        if re.fullmatch(schema["pattern"], instance) is None:
            errors.append(f"{path}: pattern mismatch")
    return errors


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
        schema = json.loads(
            (REPOSITORY / "governance" / "skill-folder-contract.schema.json").read_text()
        )
        for skill, values in CONTRACTS.items():
            with self.subTest(skill=skill):
                path = REPOSITORY / "skills" / skill / "references" / "folder-contract.json"
                self.assertTrue(path.is_file(), f"missing folder contract: {skill}")
                document = json.loads(path.read_text())
                self.assertEqual(schema_errors(document, schema), [])
                self.assertEqual(document, expected_contract(skill, values))

    def test_governance_matrix_matches_the_approved_contracts(self):
        expected = {
            skill: expected_contract(skill, values) for skill, values in CONTRACTS.items()
        }
        self.assertEqual(APPROVED_FOLDER_CONTRACTS, expected)

    def test_composed_skill_roles_cannot_be_unionized_into_either_contract(self):
        first = expected_contract("rrd-rule12", CONTRACTS["rrd-rule12"])
        second = expected_contract(
            "drafting-section-1983-complaints",
            CONTRACTS["drafting-section-1983-complaints"],
        )
        union = list(dict.fromkeys(first["input_roles"] + second["input_roles"]))
        self.assertIn(
            "skill-folder-contract-mismatch",
            validate_folder_contract_document(
                {**first, "input_roles": union}, "rrd-rule12"
            ),
        )
        self.assertIn(
            "skill-folder-contract-mismatch",
            validate_folder_contract_document(
                {**second, "input_roles": union},
                "drafting-section-1983-complaints",
            ),
        )

    def test_document_validation_rejects_contract_mutations_with_stable_findings(self):
        valid = expected_contract("filing-ci", CONTRACTS["filing-ci"])
        mutations = (
            ("extra", {**valid, "extra": True}, "invalid-folder-contract-shape"),
            (
                "missing field",
                {key: value for key, value in valid.items() if key != "internet"},
                "invalid-folder-contract-shape",
            ),
            ("version", {**valid, "version": 2}, "invalid-folder-contract-version"),
            (
                "boolean version",
                {**valid, "version": True},
                "invalid-folder-contract-version",
            ),
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
        schema = json.loads(
            (REPOSITORY / "governance" / "skill-folder-contract.schema.json").read_text()
        )
        self.assertEqual(validate_folder_contract_document(valid, "filing-ci"), [])
        for label, document, finding in mutations:
            with self.subTest(mutation=label):
                if label in {"skill", "target role"}:
                    self.assertEqual(schema_errors(document, schema), [])
                else:
                    self.assertTrue(schema_errors(document, schema))
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

    def test_governance_rejects_removed_or_unknown_public_skills(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(REPOSITORY / "skills", root / "skills")
            shutil.rmtree(root / "skills" / "filing-ci")
            self.assertIn(
                "approved-skill-folder-contract-missing: filing-ci",
                validate_skill_folder_contracts(root),
            )

            unknown = root / "skills" / "unknown-skill"
            (unknown / "references").mkdir(parents=True)
            (unknown / "SKILL.md").write_text(
                "# Unknown\n\n[Folder contract](references/folder-contract.json)\n"
            )
            (unknown / "references" / "folder-contract.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "skill": "unknown-skill",
                        "input_roles": ["filing"],
                        "target": {"policy": "required", "roles": ["filing"]},
                        "internet": "disabled",
                        "output": {"mode": "append-immutable"},
                    }
                )
            )
            findings = validate_skill_folder_contracts(root)
            self.assertIn("unapproved-skill-folder-contract: unknown-skill", findings)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            unknown = root / "skills" / "unknown-skill"
            (unknown / "references").mkdir(parents=True)
            (unknown / "SKILL.md").write_text(
                "# Unknown\n\n[Folder contract](references/folder-contract.json)\n"
            )
            (unknown / "references" / "folder-contract.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "skill": "unknown-skill",
                        "input_roles": ["filing"],
                        "target": {"policy": "required", "roles": ["filing"]},
                        "internet": "disabled",
                        "output": {"mode": "append-immutable"},
                    }
                )
            )
            findings = validate_skill_folder_contracts(root)
            self.assertIn("unapproved-skill-folder-contract: unknown-skill", findings)
            self.assertIn(
                "approved-skill-folder-contract-missing: filing-ci", findings
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

    def test_each_isolated_contract_enforces_its_exact_invocation_authority(self):
        for skill, values in CONTRACTS.items():
            with self.subTest(skill=skill), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                package = root / "installed" / skill
                shutil.copytree(REPOSITORY / "skills" / skill, package)
                input_roles, target_policy, target_roles, internet = values
                inputs = []
                for role in input_roles:
                    role_root = root / "inputs" / role
                    role_root.mkdir(parents=True)
                    (role_root / "target.txt").write_text(
                        f"{skill}:{role}\n", encoding="utf-8"
                    )
                    inputs.append({"role": role, "root": str(role_root)})
                output_root = root / "output"
                output_root.mkdir()
                if isinstance(internet, dict):
                    operation, invocation_internet = next(iter(internet.items()))
                else:
                    operation, invocation_internet = None, internet
                envelope = {
                    "version": 1,
                    "skill": skill,
                    "inputs": inputs,
                    "output": {"root": str(output_root)},
                    "runtime": {"max_seconds": 60, "max_input_bytes": 1048576},
                    "internet": invocation_internet,
                    "isolation": {
                        "inputs": "read-only",
                        "output": "read-write",
                        "undeclared": "none",
                    },
                }
                if operation is not None:
                    envelope["operation"] = operation
                if target_policy == "required":
                    envelope["target"] = {
                        "role": target_roles[0],
                        "path": "target.txt",
                    }

                validated = validate_installed_skill_invocation(envelope, package)
                self.assertEqual(validated.skill, skill)

                mutations = []
                missing = {**envelope, "inputs": inputs[:-1]}
                mutations.append(("missing-role", missing, "contract-input-roles"))
                extra_root = root / "inputs" / "extra"
                extra_root.mkdir()
                extra = {
                    **envelope,
                    "inputs": inputs
                    + [{"role": "extra", "root": str(extra_root)}],
                }
                mutations.append(("extra-role", extra, "contract-input-roles"))
                if len(inputs) > 1:
                    reordered = {**envelope, "inputs": list(reversed(inputs))}
                    mutations.append(
                        ("reordered-roles", reordered, "contract-input-roles")
                    )
                if isinstance(internet, str):
                    mutations.append(
                        (
                            "internet-mismatch",
                            {
                                **envelope,
                                "internet": (
                                    "authorized"
                                    if internet == "disabled"
                                    else "disabled"
                                ),
                            },
                            "contract-internet",
                        )
                    )
                else:
                    alternate_policy = (
                        "disabled"
                        if invocation_internet == "authorized"
                        else "authorized"
                    )
                    mutations.append(
                        (
                            "operation-internet-mismatch",
                            {**envelope, "internet": alternate_policy},
                            "contract-internet",
                        )
                    )
                    mutations.append(
                        (
                            "unknown-operation",
                            {**envelope, "operation": "unknown-operation"},
                            "contract-operation",
                        )
                    )
                if target_policy == "required":
                    without_target = dict(envelope)
                    del without_target["target"]
                    mutations.append(
                        ("missing-required-target", without_target, "contract-target")
                    )
                invalid_target_roles = [
                    role for role in input_roles if role not in target_roles
                ]
                if invalid_target_roles:
                    mutations.append(
                        (
                            "wrong-target-role",
                            {
                                **envelope,
                                "target": {
                                    "role": invalid_target_roles[0],
                                    "path": "target.txt",
                                },
                            },
                            "contract-target",
                        )
                    )

                for label, mutation, code in mutations:
                    with self.subTest(skill=skill, mutation=label):
                        with self.assertRaises(InvocationError) as captured:
                            validate_installed_skill_invocation(mutation, package)
                        self.assertEqual(captured.exception.code, code)


if __name__ == "__main__":
    unittest.main()
