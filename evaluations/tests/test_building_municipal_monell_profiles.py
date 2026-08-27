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
SKILL = REPOSITORY / "skills" / "building-municipal-monell-profiles"
SCRIPT = SKILL / "scripts" / "municipal_profile_records.py"
FIXTURE = (
    REPOSITORY
    / "evaluations"
    / "tests"
    / "fixtures"
    / "municipal-profile"
    / "profile.json"
)
ROLES = [
    "municipality",
    "department",
    "source",
    "policy-catalog",
    "policy-assessment",
    "case-record",
    "verified-authority",
]
DOMAINS = ["Practice", "Knowledge", "Authority", "Causation", "Recurrence"]
CATEGORIES = [
    "formal_policy",
    "custom",
    "training",
    "supervision",
    "fto_transmission",
    "complaint_internal_affairs",
    "ratification_candidate",
    "litigation_position",
    "institutional_feedback",
    "institutional_learning",
]
DIRECTIONS = ["favorable", "unfavorable", "disconfirming", "neutral"]
STAGE_ROLES = {
    "collection": [
        "department-identity",
        "jurisdiction",
        "approved-source-system",
        "research-scope",
    ],
    "analysis": [
        "department-identity",
        "jurisdiction",
        "policy-source",
        "analysis-scope",
    ],
    "assessment": [
        "policy-catalog",
        "actor",
        "event",
        "phase",
        "case-record",
        "assessment-scope",
    ],
    "profile": ROLES,
}


def load_module():
    specification = importlib.util.spec_from_file_location(
        "municipal_profile_records", SCRIPT
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def fixture():
    return json.loads(FIXTURE.read_text())


def source_text():
    return (
        "Fictional municipal source record.\n"
        "It contains policy, training, complaint, review, and learning entries.\n"
    ).encode()


def selected_source():
    contents = source_text()
    document = {
        "version": 1,
        "source_id": "src-institutional-record",
        "artifact_path": "records/institutional-record.txt",
        "sha256": hashlib.sha256(contents).hexdigest(),
        "source_type": "institutional_record",
        "occurred_at": "2025-03-01",
        "limitations": ["Fictional fixture with incomplete coverage"],
    }
    return {
        "input_role": "source",
        "source_documentation_path": "records/institutional-record.SOURCE.yaml",
        "source_yaml_bytes": yaml.safe_dump(document, sort_keys=False).encode(),
        "artifact_bytes": contents,
    }


def fingerprints():
    return {role: hashlib.sha256(role.encode()).hexdigest() for role in ROLES}


def upstream_validations():
    return {
        role: {"valid": True, "sha256": hashlib.sha256(role.encode()).hexdigest()}
        for role in ("policy-catalog", "policy-assessment", "verified-authority")
    }


def prerequisite_state(state, *, complete=None, substantive_gaps=False):
    if complete is None:
        complete = state not in {"absent", "invalid"}
    record = {
        "state": state,
        "terminal_receipt": complete,
        "expected_artifacts": complete,
        "validation_passed": complete,
        "fingerprints_match": complete,
    }
    if substantive_gaps:
        record["substantive_gaps"] = True
    return record


def prerequisite_arguments(**overrides):
    arguments = {
        "policy_source_state": prerequisite_state("absent"),
        "policy_catalog": prerequisite_state("absent"),
        "policy_assessment": prerequisite_state("absent"),
        "available_roles": copy.deepcopy(STAGE_ROLES),
        "output_folders": {
            "collection": True,
            "analysis": True,
            "assessment": True,
            "profile": True,
        },
        "collection_authorization": {
            "internet": True,
            "fees_required": False,
            "fees_approved": False,
        },
    }
    arguments.update(overrides)
    return arguments


def evidence_records():
    source_hash = hashlib.sha256(source_text()).hexdigest()
    records = []
    for index, category in enumerate(CATEGORIES):
        records.append(
            {
                "evidence_id": f"evidence-{category.replace('_', '-')}",
                "domain": DOMAINS[index % len(DOMAINS)],
                "category": category,
                "source_id": "src-institutional-record",
                "input_role": "source",
                "source_path": "records/institutional-record.txt",
                "source_sha256": source_hash,
                "location": f"fictional entry {index + 1}",
                "date": "2025-03-01",
                "proposition": f"The fictional record contains a bounded {category} entry.",
                "support_direction": DIRECTIONS[index % len(DIRECTIONS)],
                "limitations": ["Fictional fixture; corroboration not established"],
                "review_state": "proposed",
            }
        )
    return records


def domain_records():
    evidence = evidence_records()
    gaps_by_domain = {domain: [] for domain in DOMAINS}
    gaps_by_domain["Recurrence"] = ["gap-recurrence-denominator"]
    records = []
    for domain in DOMAINS:
        domain_evidence = [item for item in evidence if item["domain"] == domain]
        favorable = [
            item["evidence_id"]
            for item in domain_evidence
            if item["support_direction"] in {"favorable", "neutral"}
        ]
        counter = [
            item["evidence_id"]
            for item in domain_evidence
            if item["support_direction"] in {"unfavorable", "disconfirming"}
        ]
        records.append(
            {
                "domain": domain,
                "evidence_ids": favorable,
                "counterevidence_ids": counter,
                "gap_ids": gaps_by_domain[domain],
                "questions": [f"What further source-bounded review does {domain} require?"],
            }
        )
    return records


def artifact(plan, path):
    return next(item for item in plan["artifacts"] if item["path"] == path)


def build(records, data=None, **overrides):
    data = fixture() if data is None else data
    arguments = {
        "identity": data["identity"],
        "upstream_validations": upstream_validations(),
        "selected_sources": [selected_source()],
        "evidence": evidence_records(),
        "entities": data["entities"],
        "events": data["events"],
        "chains": data["chains"],
        "comparisons": data["comparisons"],
        "contradictions": data["contradictions"],
        "similarity_features": data["similarity_features"],
        "domains": domain_records(),
        "gaps": data["gaps"],
        "input_fingerprints": fingerprints(),
    }
    arguments.update(overrides)
    return records.build_profile_plan(**arguments)


class BuildingMunicipalMonellProfilesTest(unittest.TestCase):
    def test_installed_skill_has_exact_offline_folder_contract(self):
        contract = json.loads(
            (SKILL / "references" / "folder-contract.json").read_text()
        )
        self.assertEqual(
            contract,
            {
                "version": 1,
                "skill": "building-municipal-monell-profiles",
                "input_roles": ROLES,
                "target": {"policy": "none", "roles": []},
                "internet": "disabled",
                "output": {"mode": "append-immutable"},
            },
        )
        entrypoint = (SKILL / "SKILL.md").read_text().lower()
        self.assertIn("<output-folder>/temp", entrypoint)
        self.assertIn("municipal-profile.yaml", entrypoint)
        self.assertIn("not proof", entrypoint)

    def test_profile_preserves_domains_categories_directions_and_provenance(self):
        records = load_module()
        plan = build(records)
        repeated = build(records)
        self.assertEqual(plan, repeated)
        profile = yaml.safe_load(artifact(plan, "municipal-profile.yaml")["bytes"])
        self.assertEqual(
            [item["domain"] for item in profile["domains"]], DOMAINS
        )
        self.assertEqual(
            {item["category"] for item in profile["evidence"]}, set(CATEGORIES)
        )
        self.assertEqual(
            {item["support_direction"] for item in profile["evidence"]},
            set(DIRECTIONS),
        )
        self.assertTrue(
            all(item["source_sha256"] for item in profile["evidence"])
        )
        validation = json.loads(
            artifact(plan, "municipal-profile-validation.json")["bytes"]
        )
        self.assertEqual(
            validation["artifact_hashes"],
            {
                path: hashlib.sha256(artifact(plan, path)["bytes"]).hexdigest()
                for path in (
                    "municipal-profile.yaml",
                    "municipal-profile-gaps.yaml",
                    "municipal-profile.md",
                )
            },
        )
        self.assertNotIn("element_satisfied", json.dumps(profile))
        self.assertNotIn("liability", json.dumps(profile).lower())

    def test_profile_preserves_linked_institutional_records_as_questions(self):
        records = load_module()
        profile = yaml.safe_load(
            artifact(build(records), "municipal-profile.yaml")["bytes"]
        )
        self.assertEqual(len(profile["entities"]), 2)
        self.assertEqual(len(profile["events"]), 2)
        self.assertEqual(len(profile["chains"]), 1)
        self.assertEqual(len(profile["comparisons"]), 1)
        self.assertEqual(len(profile["contradictions"]), 1)
        self.assertEqual(len(profile["similarity_features"]), 1)
        self.assertTrue(profile["comparisons"][0]["question"].endswith("?"))
        self.assertTrue(profile["chains"][0]["question"].endswith("?"))

    def test_changed_source_and_failing_upstream_validation_fail_closed(self):
        records = load_module()
        changed = selected_source()
        changed["artifact_bytes"] += b"changed\n"
        with self.assertRaises(records.MunicipalProfileError) as captured:
            build(records, selected_sources=[changed])
        self.assertEqual(captured.exception.code, "source-hash-mismatch")

        failing = upstream_validations()
        failing["verified-authority"]["valid"] = False
        with self.assertRaises(records.MunicipalProfileError) as captured:
            build(records, upstream_validations=failing)
        self.assertEqual(captured.exception.code, "failing-upstream-validation")

    def test_unresolved_links_and_conclusion_fields_are_rejected(self):
        records = load_module()
        data = fixture()
        unresolved = copy.deepcopy(data["comparisons"])
        unresolved[0]["feature_ids"] = ["feature-not-present"]
        with self.assertRaises(records.MunicipalProfileError) as captured:
            build(records, comparisons=unresolved)
        self.assertEqual(captured.exception.code, "unresolved-feature")

        conclusive = evidence_records()
        conclusive[0]["element_satisfied"] = True
        with self.assertRaises(records.MunicipalProfileError) as captured:
            build(records, evidence=conclusive)
        self.assertEqual(captured.exception.code, "invalid-evidence")

        conclusive = evidence_records()
        conclusive[0]["proposition"] = "Monell liability is established."
        with self.assertRaises(records.MunicipalProfileError) as captured:
            build(records, evidence=conclusive)
        self.assertEqual(captured.exception.code, "conclusive-profile-language")

    def test_gaps_remain_explicit_and_do_not_become_proof(self):
        records = load_module()
        plan = build(records)
        gaps = yaml.safe_load(
            artifact(plan, "municipal-profile-gaps.yaml")["bytes"]
        )["gaps"]
        self.assertEqual(gaps, fixture()["gaps"])
        markdown = artifact(plan, "municipal-profile.md")["bytes"].decode().lower()
        self.assertIn("complete recurrence denominator", markdown)
        self.assertNotIn("monell liability", markdown)
        self.assertNotIn("legally sufficient", markdown)

    def test_trusted_host_publishes_offline_with_output_local_temp(self):
        records = load_module()
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
                    "skill": "building-municipal-monell-profiles",
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
                run_id="523e4567-e89b-42d3-a456-426614174000",
                skill_version="1.0.0",
                mode="append-immutable",
                input_manifest=build_input_manifest(invocation),
            )
            self.assertEqual(
                run.process_configuration()["cwd"], str(output.resolve() / "temp")
            )
            plan = build(records)
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

    def test_prerequisite_plan_routes_absent_sources_to_collection(self):
        records = load_module()
        plan = records.build_prerequisite_plan(**prerequisite_arguments())
        repeated = records.build_prerequisite_plan(**prerequisite_arguments())
        self.assertEqual(plan, repeated)
        self.assertEqual(plan["status"], "ready-for-collection")
        self.assertEqual(plan["next_skill"], "collecting-police-policy-sources")
        self.assertEqual(plan["required_roles"], STAGE_ROLES["collection"])
        self.assertEqual(plan["missing_roles"], [])
        self.assertEqual(plan["internet"], "authorized")
        self.assertEqual(
            [item["path"] for item in plan["artifacts"]],
            [
                "municipal-profile-prerequisites.yaml",
                "municipal-profile-prerequisites.md",
            ],
        )
        document = yaml.safe_load(plan["artifacts"][0]["bytes"])
        self.assertEqual(document["status"], "ready-for-collection")
        self.assertNotIn("artifacts", document)

    def test_prerequisite_plan_requires_collection_authority(self):
        records = load_module()
        cases = [
            (
                {"internet": False, "fees_required": False, "fees_approved": False},
                ["bounded-internet-authorization-required"],
            ),
            (
                {"internet": True, "fees_required": True, "fees_approved": False},
                ["fee-authorization-required"],
            ),
        ]
        for authorization, reasons in cases:
            with self.subTest(authorization=authorization):
                plan = records.build_prerequisite_plan(
                    **prerequisite_arguments(
                        collection_authorization=authorization
                    )
                )
                self.assertEqual(plan["status"], "authorization-required")
                self.assertEqual(plan["blocking_reasons"], reasons)
                self.assertEqual(
                    plan["next_skill"], "collecting-police-policy-sources"
                )

    def test_prerequisite_plan_stops_candidate_sources_for_review(self):
        records = load_module()
        plan = records.build_prerequisite_plan(
            **prerequisite_arguments(
                policy_source_state=prerequisite_state("candidate")
            )
        )
        self.assertEqual(plan["status"], "review-required")
        self.assertIsNone(plan["next_skill"])
        self.assertEqual(plan["required_roles"], [])
        self.assertEqual(
            plan["blocking_reasons"],
            ["independent-policy-source-review-required"],
        )

    def test_prerequisite_plan_routes_approved_sources_to_analysis(self):
        records = load_module()
        plan = records.build_prerequisite_plan(
            **prerequisite_arguments(
                policy_source_state=prerequisite_state("approved")
            )
        )
        self.assertEqual(plan["status"], "ready-for-analysis")
        self.assertEqual(plan["next_skill"], "analyzing-police-policy-sources")
        self.assertEqual(plan["required_roles"], STAGE_ROLES["analysis"])
        self.assertEqual(plan["internet"], "disabled")
        self.assertEqual(
            plan["postconditions"],
            [
                "terminal-run-receipt-success",
                "policy-requirements.yaml-present",
                "policy-gaps.yaml-present",
                "policy-analysis.md-present",
                "policy-analysis-validation.json-present",
                "domain-validation-passed",
                "input-fingerprints-match",
            ],
        )

    def test_prerequisite_plan_routes_valid_catalog_to_assessment(self):
        records = load_module()
        plan = records.build_prerequisite_plan(
            **prerequisite_arguments(
                policy_catalog=prerequisite_state("valid")
            )
        )
        self.assertEqual(plan["status"], "ready-for-assessment")
        self.assertEqual(
            plan["next_skill"], "assessing-police-policy-compliance"
        )
        self.assertEqual(plan["required_roles"], STAGE_ROLES["assessment"])
        self.assertEqual(plan["internet"], "disabled")

    def test_prerequisite_plan_resumes_profile_only_when_all_roles_are_ready(self):
        records = load_module()
        ready = prerequisite_arguments(
            policy_catalog=prerequisite_state("valid"),
            policy_assessment=prerequisite_state("valid"),
        )
        plan = records.build_prerequisite_plan(**ready)
        self.assertEqual(plan["status"], "ready-for-profile")
        self.assertEqual(
            plan["next_skill"], "building-municipal-monell-profiles"
        )
        self.assertEqual(plan["required_roles"], ROLES)

        roles = copy.deepcopy(STAGE_ROLES)
        roles["profile"].remove("verified-authority")
        missing = records.build_prerequisite_plan(
            **prerequisite_arguments(
                policy_catalog=prerequisite_state("valid"),
                policy_assessment=prerequisite_state("valid"),
                available_roles=roles,
            )
        )
        self.assertEqual(missing["status"], "input-required")
        self.assertEqual(missing["missing_roles"], ["verified-authority"])

    def test_prerequisite_plan_requires_fresh_output_folder_for_next_stage(self):
        records = load_module()
        outputs = {
            "collection": True,
            "analysis": False,
            "assessment": True,
            "profile": True,
        }
        plan = records.build_prerequisite_plan(
            **prerequisite_arguments(
                policy_source_state=prerequisite_state("approved"),
                output_folders=outputs,
            )
        )
        self.assertEqual(plan["status"], "input-required")
        self.assertEqual(plan["missing_roles"], [])
        self.assertEqual(
            plan["output_folder"], {"required": True, "supplied": False}
        )
        self.assertEqual(
            plan["blocking_reasons"], ["fresh-output-folder-required"]
        )

    def test_prerequisite_plan_blocks_invalid_mechanical_state_but_not_gaps(self):
        records = load_module()
        invalid_catalog = prerequisite_state("valid")
        invalid_catalog["fingerprints_match"] = False
        blocked = records.build_prerequisite_plan(
            **prerequisite_arguments(policy_catalog=invalid_catalog)
        )
        self.assertEqual(blocked["status"], "blocked-invalid")
        self.assertEqual(
            blocked["blocking_reasons"],
            ["policy-catalog-fingerprints-mismatch"],
        )

        eligible = records.build_prerequisite_plan(
            **prerequisite_arguments(
                policy_catalog=prerequisite_state(
                    "valid", substantive_gaps=True
                )
            )
        )
        self.assertEqual(eligible["status"], "ready-for-assessment")

    def test_prerequisite_plan_rejects_unknown_or_inexact_state(self):
        records = load_module()
        cases = []
        unknown_state = prerequisite_state("unknown")
        cases.append(
            prerequisite_arguments(policy_source_state=unknown_state)
        )
        extra_field = prerequisite_state("approved")
        extra_field["unexpected"] = True
        cases.append(
            prerequisite_arguments(policy_source_state=extra_field)
        )
        duplicate_roles = copy.deepcopy(STAGE_ROLES)
        duplicate_roles["analysis"].append("policy-source")
        cases.append(prerequisite_arguments(available_roles=duplicate_roles))
        invalid_outputs = {
            "collection": True,
            "analysis": True,
            "assessment": True,
            "profile": "yes",
        }
        cases.append(prerequisite_arguments(output_folders=invalid_outputs))
        for arguments in cases:
            with self.subTest(arguments=arguments):
                with self.assertRaises(records.MunicipalProfileError) as captured:
                    records.build_prerequisite_plan(**arguments)
                self.assertTrue(
                    captured.exception.code.startswith("invalid-prerequisite-")
                )


if __name__ == "__main__":
    unittest.main()
