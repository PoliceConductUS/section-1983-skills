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


if __name__ == "__main__":
    unittest.main()
