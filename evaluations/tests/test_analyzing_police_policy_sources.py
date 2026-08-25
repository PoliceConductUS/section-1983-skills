import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.skill_output_writer import OutputRun
from scripts.validate_folder_invocation import build_input_manifest, validate_invocation


REPOSITORY = Path(__file__).resolve().parents[2]
SKILL = REPOSITORY / "skills" / "analyzing-police-policy-sources"
SCRIPT = SKILL / "scripts" / "policy_requirement_records.py"
FIXTURE = (
    REPOSITORY
    / "evaluations"
    / "tests"
    / "fixtures"
    / "policy-requirement-analysis"
    / "requirements.json"
)


def load_module():
    specification = importlib.util.spec_from_file_location(
        "policy_requirement_records", SCRIPT
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def source_text():
    return (
        "Fictional Policy\n"
        "An officer must submit a force report before the end of the shift unless a supervisor documents an emergency extension.\n"
        "An officer must not retaliate against a person who requests medical care.\n"
        "An officer may request a supervisor at any time.\n"
        "A supervisor may require additional review when the record is incomplete.\n"
    ).encode("utf-8")


def selected_source(*, classification="adopted_policy", adoption="documented"):
    contents = source_text()
    source_yaml = {
        "version": 1,
        "source_id": "src-adopted-use-of-force",
        "artifact_path": "sources/use-of-force.txt",
        "sha256": hashlib.sha256(contents).hexdigest(),
        "source_url": "https://example.invalid/use-of-force",
        "query": "fictional adopted use of force policy",
        "filters": ["fictional-fixture"],
        "checked_date": "2026-08-25",
        "retrieved_at": "2026-08-25T12:00:00Z",
        "result_identity": "example-invalid:use-of-force",
        "classification": classification,
        "adoption_relationship": adoption,
        "review_state": "candidate",
        "retrieval_result": "retrieved",
        "effective_date": {
            "status": "documented",
            "date": "2025-01-01",
            "evidence": "Fictional adoption record dated 2025-01-01.",
            "gap": None,
        },
        "limitations": ["Fictional fixture"],
        "duplicate_of": [],
    }
    return {
        "source_documentation_path": "sources/use-of-force.SOURCE.yaml",
        "source_yaml_bytes": yaml.safe_dump(source_yaml, sort_keys=False).encode(),
        "artifact_bytes": contents,
        "approval": {
            "state": "approved_for_analysis",
            "approved_on": "2026-08-25",
            "approved_by": "human-review",
        },
    }


def fixture():
    return json.loads(FIXTURE.read_text())


def artifact(plan, path):
    return next(item for item in plan["artifacts"] if item["path"] == path)


class AnalyzingPolicePolicySourcesTest(unittest.TestCase):
    def test_installed_skill_has_exact_offline_folder_contract(self):
        contract = json.loads(
            (SKILL / "references" / "folder-contract.json").read_text()
        )
        self.assertEqual(
            contract,
            {
                "version": 1,
                "skill": "analyzing-police-policy-sources",
                "input_roles": [
                    "department-identity",
                    "jurisdiction",
                    "policy-source",
                    "analysis-scope",
                ],
                "target": {"policy": "none", "roles": []},
                "internet": "disabled",
                "output": {"mode": "append-immutable"},
            },
        )
        entrypoint = (SKILL / "SKILL.md").read_text().lower()
        self.assertIn("<output-folder>/temp", entrypoint)
        self.assertIn("policy-requirements.yaml", entrypoint)
        self.assertIn("never apply a later policy retroactively", entrypoint)

    def test_plan_preserves_all_requirement_types_and_operational_limits(self):
        records = load_module()
        data = fixture()
        plan = records.build_analysis_plan(
            [selected_source()], data["requirements"], [], data["scope"]
        )
        repeated = records.build_analysis_plan(
            [selected_source()], data["requirements"], [], data["scope"]
        )
        self.assertEqual(plan, repeated)
        requirements = yaml.safe_load(
            artifact(plan, "policy-requirements.yaml")["bytes"]
        )["requirements"]
        self.assertEqual(
            {record["requirement_type"] for record in requirements},
            {"mandatory", "prohibited", "permitted", "discretionary"},
        )
        mandatory = next(
            record for record in requirements if record["requirement_id"] == "req-report-force"
        )
        self.assertTrue(mandatory["triggers"])
        self.assertTrue(mandatory["exceptions"])
        self.assertTrue(mandatory["cross_references"])
        self.assertEqual(
            mandatory["source_sha256"], hashlib.sha256(source_text()).hexdigest()
        )
        self.assertEqual(mandatory["source_path"], "sources/use-of-force.txt")
        self.assertNotIn("compliance", json.dumps(requirements).lower())

    def test_validator_rejects_lost_limits_and_retroactive_dates(self):
        records = load_module()
        data = fixture()
        lost_exception = copy.deepcopy(data["requirements"])
        lost_exception[0]["exceptions"] = []
        with self.assertRaises(records.PolicyRequirementError) as captured:
            records.build_analysis_plan(
                [selected_source()], lost_exception, [], data["scope"]
            )
        self.assertEqual(captured.exception.code, "lost-operative-limit")

        collapsed_discretion = copy.deepcopy(data["requirements"])
        collapsed_discretion[3]["requirement_type"] = "mandatory"
        with self.assertRaises(records.PolicyRequirementError) as captured:
            records.build_analysis_plan(
                [selected_source()], collapsed_discretion, [], data["scope"]
            )
        self.assertEqual(captured.exception.code, "lost-operative-limit")

        retroactive = copy.deepcopy(data["requirements"])
        retroactive[0]["effective"]["start_date"] = "2024-01-01"
        with self.assertRaises(records.PolicyRequirementError) as captured:
            records.build_analysis_plan(
                [selected_source()], retroactive, [], data["scope"]
            )
        self.assertEqual(captured.exception.code, "retroactive-requirement")

    def test_model_policy_and_changed_source_cannot_generate_requirements(self):
        records = load_module()
        data = fixture()
        with self.assertRaises(records.PolicyRequirementError) as captured:
            records.build_analysis_plan(
                [selected_source(classification="model_policy", adoption="uncertain")],
                data["requirements"],
                [],
                data["scope"],
            )
        self.assertEqual(captured.exception.code, "source-not-adopted-policy")

        changed = selected_source()
        changed["artifact_bytes"] += b"changed\n"
        with self.assertRaises(records.PolicyRequirementError) as captured:
            records.build_analysis_plan(
                [changed], data["requirements"], [], data["scope"]
            )
        self.assertEqual(captured.exception.code, "source-hash-mismatch")

    def test_gaps_remain_explicit_and_do_not_invent_requirements(self):
        records = load_module()
        data = fixture()
        gap = {
            "gap_id": "gap-illegible-page",
            "gap_type": "illegible_text",
            "source_id": "src-adopted-use-of-force",
            "location": "page 8",
            "description": "The source text is illegible at the cross-reference.",
        }
        plan = records.build_analysis_plan(
            [selected_source()], data["requirements"], [gap], data["scope"]
        )
        gaps = yaml.safe_load(artifact(plan, "policy-analysis-gaps.yaml")["bytes"])
        self.assertEqual(gaps["gaps"], [gap])
        self.assertNotIn("invent", artifact(plan, "policy-analysis.md")["bytes"].decode())

    def test_trusted_host_publishes_offline_with_output_local_temp(self):
        records = load_module()
        data = fixture()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output"
            output.mkdir()
            roles = {}
            for role in (
                "department-identity",
                "jurisdiction",
                "policy-source",
                "analysis-scope",
            ):
                folder = root / role
                folder.mkdir()
                (folder / "input.yaml").write_text(f"role: {role}\n")
                roles[role] = folder
            before = {
                role: (folder / "input.yaml").read_bytes()
                for role, folder in roles.items()
            }
            invocation = validate_invocation(
                {
                    "version": 1,
                    "skill": "analyzing-police-policy-sources",
                    "inputs": [
                        {"role": role, "root": str(roles[role])} for role in roles
                    ],
                    "output": {"root": str(output)},
                    "runtime": {"max_seconds": 60, "max_input_bytes": 1048576},
                    "internet": "disabled",
                    "isolation": {
                        "inputs": "read-only",
                        "output": "read-write",
                        "undeclared": "none",
                    },
                }
            )
            run = OutputRun.start(
                invocation,
                run_id="223e4567-e89b-42d3-a456-426614174000",
                skill_version="1.0.0",
                mode="append-immutable",
                input_manifest=build_input_manifest(invocation),
            )
            expected_temp = str(output.resolve() / "temp")
            self.assertEqual(run.process_configuration()["cwd"], expected_temp)
            plan = records.build_analysis_plan(
                [selected_source()], data["requirements"], [], data["scope"]
            )
            for item in plan["artifacts"]:
                run.write(item["path"], item["bytes"])
            receipt = run.complete()
            self.assertFalse(receipt["internet"]["used"])
            self.assertEqual(
                {
                    role: (folder / "input.yaml").read_bytes()
                    for role, folder in roles.items()
                },
                before,
            )


if __name__ == "__main__":
    unittest.main()
