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
SKILL = REPOSITORY / "skills" / "assessing-police-policy-compliance"
SCRIPT = SKILL / "scripts" / "policy_assessment_records.py"
FIXTURE = (
    REPOSITORY
    / "evaluations"
    / "tests"
    / "fixtures"
    / "policy-assessment"
    / "assessments.json"
)
ROLES = [
    "policy-catalog",
    "actor",
    "event",
    "phase",
    "case-record",
    "assessment-scope",
]


def load_module():
    specification = importlib.util.spec_from_file_location(
        "policy_assessment_records", SCRIPT
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def fixture():
    return json.loads(FIXTURE.read_text())


def source_bytes():
    return b"Fictional adopted policy requires a force report before shift end.\n"


def requirement():
    policy_hash = hashlib.sha256(source_bytes()).hexdigest()
    return {
        "requirement_id": "req-report-force",
        "department_id": "fictional-department",
        "policy_id": "use-of-force",
        "source_id": "src-adopted-policy",
        "effective": {
            "start_date": "2025-01-01",
            "end_date": None,
            "gap": None,
        },
        "quotation": "requires a force report before shift end",
        "pinpoint": "section 4.1",
        "source_path": "sources/use-of-force.txt",
        "source_sha256": policy_hash,
        "actor": "officer",
        "triggers": ["force is reported"],
        "requirement_type": "mandatory",
        "action": "Submit the force report before shift end.",
        "exceptions": [],
        "definitions": [],
        "dependencies": [],
        "cross_references": [],
        "documentation_or_review": ["supervisor review"],
        "gaps": [],
        "operative_markers": {
            "condition_present": True,
            "exception_present": False,
            "discretion_present": False,
            "cross_reference_present": False,
        },
    }


def catalog():
    record = requirement()
    catalog_document = {
        "version": 1,
        "scope": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
        "requirements": [record],
    }
    validation = {
        "schema_version": 1,
        "valid": True,
        "source_ids": ["src-adopted-policy"],
        "source_hashes": {"src-adopted-policy": record["source_sha256"]},
        "requirement_ids": ["req-report-force"],
        "gap_ids": [],
    }
    return {
        "requirements_yaml_bytes": yaml.safe_dump(
            catalog_document, sort_keys=False
        ).encode(),
        "validation_json_bytes": (
            json.dumps(validation, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode(),
    }


def evidence_source(source_id, text):
    contents = text.encode()
    artifact_path = f"evidence/{source_id}.txt"
    source_documentation_path = f"evidence/{source_id}.SOURCE.yaml"
    document = {
        "version": 1,
        "source_id": source_id,
        "artifact_path": artifact_path,
        "sha256": hashlib.sha256(contents).hexdigest(),
        "source_type": "case_record",
        "occurred_at": "2025-06-15",
        "limitations": ["Fictional fixture"],
    }
    return {
        "input_role": "case-record",
        "source_documentation_path": source_documentation_path,
        "source_yaml_bytes": yaml.safe_dump(document, sort_keys=False).encode(),
        "artifact_bytes": contents,
    }


def evidence_sources():
    return [
        evidence_source(
            "src-support",
            "Video shows Officer Alpha used the reporting form before shift end.",
        ),
        evidence_source(
            "src-contrary",
            "Supervisor memorandum disputes whether the report was timely.",
        ),
    ]


def reference(source):
    document = yaml.safe_load(source["source_yaml_bytes"])
    return {
        "source_id": document["source_id"],
        "input_role": source["input_role"],
        "source_path": document["artifact_path"],
        "source_sha256": document["sha256"],
        "location": "line 1",
    }


def fingerprints():
    return {role: hashlib.sha256(role.encode()).hexdigest() for role in ROLES}


def assessment(
    assessment_id,
    *,
    actor_id="actor-alpha",
    event_id="event-one",
    phase_id="phase-one",
    applicability="applies",
    violation="yes",
    evidence="complete",
    supporting=None,
    contrary=None,
    missing=None,
    conflicts=None,
):
    sources = evidence_sources()
    return {
        "assessment_id": assessment_id,
        "requirement_id": "req-report-force",
        "actor_id": actor_id,
        "event_id": event_id,
        "phase_id": phase_id,
        "policy_date": "2025-01-01",
        "event_date": "2025-06-15" if event_id == "event-one" else "2024-12-15",
        "applicability": applicability,
        "violation": violation,
        "evidence": evidence,
        "supporting_sources": (
            [reference(sources[0])] if supporting is None else supporting
        ),
        "contrary_sources": (
            [reference(sources[1])] if contrary is None else contrary
        ),
        "missing_predicates": [] if missing is None else missing,
        "conflicts": [] if conflicts is None else conflicts,
        "explanation": "Fictional bounded policy assessment.",
        "review_state": "proposed",
        "input_fingerprints": fingerprints(),
    }


def assessments():
    sources = evidence_sources()
    support = [reference(sources[0])]
    contrary = [reference(sources[1])]
    return [
        assessment("assessment-yes", phase_id="phase-one", contrary=[]),
        assessment(
            "assessment-likely",
            phase_id="phase-two",
            violation="likely",
            evidence="incomplete",
            contrary=[],
            missing=["supervisor timestamp"],
        ),
        assessment(
            "assessment-unlikely",
            phase_id="phase-three",
            violation="unlikely",
            evidence="disputed",
            conflicts=["timing sources conflict"],
        ),
        assessment(
            "assessment-no",
            actor_id="actor-bravo",
            phase_id="phase-four",
            violation="no",
            evidence="complete",
            supporting=support,
            contrary=[],
        ),
        assessment(
            "assessment-uncertain",
            phase_id="phase-five",
            applicability="uncertain",
            violation="indeterminate",
            evidence="unavailable",
            supporting=[],
            contrary=[],
            missing=["dispatch record"],
        ),
        assessment(
            "assessment-not-applicable",
            actor_id="actor-bravo",
            phase_id="phase-six",
            applicability="not_applicable",
            violation="indeterminate",
            evidence="incomplete",
            supporting=[],
            contrary=[],
            missing=["covered actor predicate"],
        ),
        assessment(
            "assessment-before-policy",
            event_id="event-two",
            phase_id="phase-seven",
            applicability="not_applicable",
            violation="indeterminate",
            evidence="complete",
            supporting=[],
            contrary=contrary,
            missing=[],
        ),
    ]


def artifact(plan, path):
    return next(item for item in plan["artifacts"] if item["path"] == path)


class AssessingPolicePolicyComplianceTest(unittest.TestCase):
    def test_installed_skill_has_exact_offline_folder_contract(self):
        contract = json.loads(
            (SKILL / "references" / "folder-contract.json").read_text()
        )
        self.assertEqual(
            contract,
            {
                "version": 1,
                "skill": "assessing-police-policy-compliance",
                "input_roles": ROLES,
                "target": {"policy": "none", "roles": []},
                "internet": "disabled",
                "output": {"mode": "append-immutable"},
            },
        )
        entrypoint = (SKILL / "SKILL.md").read_text().lower()
        self.assertIn("<output-folder>/temp", entrypoint)
        self.assertIn("no evidence of a violation", entrypoint)
        self.assertIn("policy-assessments.yaml", entrypoint)

    def test_plan_preserves_every_status_and_separate_actor_phase_units(self):
        records = load_module()
        data = fixture()
        plan = records.build_assessment_plan(
            catalog(),
            data["actors"],
            data["events"],
            data["phases"],
            evidence_sources(),
            assessments(),
            [],
            data["scope"],
            fingerprints(),
        )
        repeated = records.build_assessment_plan(
            catalog(),
            data["actors"],
            data["events"],
            data["phases"],
            evidence_sources(),
            assessments(),
            [],
            data["scope"],
            fingerprints(),
        )
        self.assertEqual(plan, repeated)
        output = yaml.safe_load(
            artifact(plan, "policy-assessments.yaml")["bytes"]
        )["assessments"]
        self.assertEqual(
            {record["applicability"] for record in output},
            {"applies", "not_applicable", "uncertain"},
        )
        self.assertEqual(
            {record["violation"] for record in output},
            {"yes", "likely", "unlikely", "no", "indeterminate"},
        )
        self.assertEqual(
            {record["evidence"] for record in output},
            {"complete", "incomplete", "disputed", "unavailable"},
        )
        units = {
            (
                record["requirement_id"],
                record["actor_id"],
                record["event_id"],
                record["phase_id"],
            )
            for record in output
        }
        self.assertEqual(len(units), len(output))

    def test_validator_rejects_unsupported_no_and_wrong_date_selection(self):
        records = load_module()
        data = fixture()
        unsupported_no = assessments()
        unsupported_no[3]["evidence"] = "incomplete"
        with self.assertRaises(records.PolicyAssessmentError) as captured:
            records.build_assessment_plan(
                catalog(),
                data["actors"],
                data["events"],
                data["phases"],
                evidence_sources(),
                unsupported_no,
                [],
                data["scope"],
                fingerprints(),
            )
        self.assertEqual(captured.exception.code, "unsupported-no")

        inapplicable_no = assessments()
        inapplicable_no[5]["violation"] = "no"
        with self.assertRaises(records.PolicyAssessmentError) as captured:
            records.build_assessment_plan(
                catalog(),
                data["actors"],
                data["events"],
                data["phases"],
                evidence_sources(),
                inapplicable_no,
                [],
                data["scope"],
                fingerprints(),
            )
        self.assertEqual(captured.exception.code, "invalid-not-applicable")

        before_policy = assessments()
        before_policy[6]["applicability"] = "applies"
        before_policy[6]["violation"] = "yes"
        with self.assertRaises(records.PolicyAssessmentError) as captured:
            records.build_assessment_plan(
                catalog(),
                data["actors"],
                data["events"],
                data["phases"],
                evidence_sources(),
                before_policy,
                [],
                data["scope"],
                fingerprints(),
            )
        self.assertEqual(captured.exception.code, "policy-not-effective")

    def test_changed_evidence_and_stale_catalog_fail_closed(self):
        records = load_module()
        data = fixture()
        changed_sources = evidence_sources()
        changed_sources[0]["artifact_bytes"] += b"changed\n"
        with self.assertRaises(records.PolicyAssessmentError) as captured:
            records.build_assessment_plan(
                catalog(),
                data["actors"],
                data["events"],
                data["phases"],
                changed_sources,
                assessments(),
                [],
                data["scope"],
                fingerprints(),
            )
        self.assertEqual(captured.exception.code, "source-hash-mismatch")

        stale_catalog = catalog()
        validation = json.loads(stale_catalog["validation_json_bytes"])
        validation["requirement_ids"] = []
        stale_catalog["validation_json_bytes"] = json.dumps(validation).encode()
        with self.assertRaises(records.PolicyAssessmentError) as captured:
            records.build_assessment_plan(
                stale_catalog,
                data["actors"],
                data["events"],
                data["phases"],
                evidence_sources(),
                assessments(),
                [],
                data["scope"],
                fingerprints(),
            )
        self.assertEqual(captured.exception.code, "stale-catalog-validation")

    def test_assessment_scope_rejects_undeclared_source_selection(self):
        records = load_module()
        data = fixture()
        narrowed_scope = copy.deepcopy(data["scope"])
        narrowed_scope["selected_source_paths"].remove(
            "evidence/src-contrary.SOURCE.yaml"
        )
        with self.assertRaises(records.PolicyAssessmentError) as captured:
            records.build_assessment_plan(
                catalog(),
                data["actors"],
                data["events"],
                data["phases"],
                evidence_sources(),
                assessments(),
                [],
                narrowed_scope,
                fingerprints(),
            )
        self.assertEqual(captured.exception.code, "undeclared-source-selection")

    def test_input_fingerprint_mapping_is_exact_but_order_independent(self):
        records = load_module()
        data = fixture()
        reordered = dict(reversed(list(fingerprints().items())))
        proposed = assessments()
        for item in proposed:
            item["input_fingerprints"] = reordered
        plan = records.build_assessment_plan(
            catalog(),
            data["actors"],
            data["events"],
            data["phases"],
            evidence_sources(),
            proposed,
            [],
            data["scope"],
            reordered,
        )
        validation = json.loads(
            artifact(plan, "policy-assessment-validation.json")["bytes"]
        )
        self.assertEqual(list(validation["input_fingerprints"]), sorted(ROLES))

        missing = dict(reordered)
        missing.pop("actor")
        with self.assertRaises(records.PolicyAssessmentError) as captured:
            records.build_assessment_plan(
                catalog(),
                data["actors"],
                data["events"],
                data["phases"],
                evidence_sources(),
                assessments(),
                [],
                data["scope"],
                missing,
            )
        self.assertEqual(captured.exception.code, "invalid-input-fingerprint")

    def test_conflicts_and_missing_material_remain_explicit(self):
        records = load_module()
        data = fixture()
        gap = {
            "gap_id": "gap-dispatch-record",
            "assessment_id": "assessment-uncertain",
            "gap_type": "unavailable_source",
            "description": "The fictional dispatch record is unavailable.",
        }
        plan = records.build_assessment_plan(
            catalog(),
            data["actors"],
            data["events"],
            data["phases"],
            evidence_sources(),
            assessments(),
            [gap],
            data["scope"],
            fingerprints(),
        )
        gaps = yaml.safe_load(
            artifact(plan, "policy-assessment-gaps.yaml")["bytes"]
        )
        self.assertEqual(gaps["gaps"], [gap])
        markdown = artifact(plan, "policy-assessment.md")["bytes"].decode()
        self.assertIn("timing sources conflict", markdown)
        self.assertNotIn("constitutional", markdown.lower())
        self.assertNotIn("monell", markdown.lower())

    def test_trusted_host_publishes_offline_with_output_local_temp(self):
        records = load_module()
        data = fixture()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output"
            output.mkdir()
            role_folders = {}
            for role in ROLES:
                folder = root / role
                folder.mkdir()
                (folder / "input.yaml").write_text(f"role: {role}\n")
                role_folders[role] = folder
            before = {
                role: (folder / "input.yaml").read_bytes()
                for role, folder in role_folders.items()
            }
            invocation = validate_invocation(
                {
                    "version": 1,
                    "skill": "assessing-police-policy-compliance",
                    "inputs": [
                        {"role": role, "root": str(role_folders[role])}
                        for role in ROLES
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
                run_id="323e4567-e89b-42d3-a456-426614174000",
                skill_version="1.0.0",
                mode="append-immutable",
                input_manifest=build_input_manifest(invocation),
            )
            self.assertEqual(
                run.process_configuration()["cwd"], str(output.resolve() / "temp")
            )
            plan = records.build_assessment_plan(
                catalog(),
                data["actors"],
                data["events"],
                data["phases"],
                evidence_sources(),
                assessments(),
                [],
                data["scope"],
                fingerprints(),
            )
            for item in plan["artifacts"]:
                run.write(item["path"], item["bytes"])
            receipt = run.complete()
            self.assertFalse(receipt["internet"]["used"])
            self.assertEqual(
                {
                    role: (folder / "input.yaml").read_bytes()
                    for role, folder in role_folders.items()
                },
                before,
            )


if __name__ == "__main__":
    unittest.main()
