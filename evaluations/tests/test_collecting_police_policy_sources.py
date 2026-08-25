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
SKILL = REPOSITORY / "skills" / "collecting-police-policy-sources"
SCRIPT = SKILL / "scripts" / "policy_source_records.py"
FIXTURES = REPOSITORY / "evaluations" / "fixtures" / "policy-source-collection"


def load_module():
    specification = importlib.util.spec_from_file_location(
        "policy_source_records", SCRIPT
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def proposal():
    source = fixture("model-policy.json")["source"]
    source["artifact_bytes"] = source.pop("artifact_text").encode("utf-8")
    return source


def paths(plan):
    return [artifact["path"] for artifact in plan["artifacts"]]


def artifact(plan, path):
    return next(item for item in plan["artifacts"] if item["path"] == path)


class CollectingPolicePolicySourcesTest(unittest.TestCase):
    def test_installed_skill_has_exact_folder_and_network_contract(self):
        contract = json.loads(
            (SKILL / "references" / "folder-contract.json").read_text()
        )
        self.assertEqual(contract["version"], 1)
        self.assertEqual(contract["skill"], "collecting-police-policy-sources")
        self.assertEqual(
            contract["input_roles"],
            [
                "department-identity",
                "jurisdiction",
                "approved-source-system",
                "research-scope",
            ],
        )
        self.assertEqual(contract["target"], {"policy": "none", "roles": []})
        self.assertEqual(contract["internet"], "authorized")
        self.assertEqual(contract["output"], {"mode": "append-immutable"})

        entrypoint = (SKILL / "SKILL.md").read_text()
        self.assertIn("<output-folder>/temp", entrypoint)
        self.assertIn("policy-source-candidates.yaml", entrypoint)
        self.assertIn("policy-source-gaps.yaml", entrypoint)
        self.assertIn("later invocation", entrypoint.lower())
        self.assertIn("never establish that a policy", entrypoint.lower())

    def test_helper_returns_deterministic_output_relative_artifact_plan(self):
        records = load_module()
        gap = fixture("version-gap.json")["gap"]
        first = records.build_collection_plan([proposal()], [gap], "2026-08-25")
        second = records.build_collection_plan([proposal()], [gap], "2026-08-25")

        self.assertEqual(first, second)
        self.assertEqual(
            paths(first),
            [
                "sources/model-use-of-force.txt",
                "sources/model-use-of-force.SOURCE.yaml",
                "policy-source-candidates.yaml",
                "policy-source-gaps.yaml",
            ],
        )
        for item in first["artifacts"]:
            self.assertIsInstance(item["bytes"], bytes)
            self.assertIsInstance(item["internet_sources"], list)
            self.assertFalse(Path(item["path"]).is_absolute())
            self.assertNotIn("..", Path(item["path"]).parts)

        ordinary = artifact(first, "sources/model-use-of-force.txt")
        self.assertEqual(
            ordinary["internet_sources"],
            [
                {
                    "url": "https://example.invalid/model-use-of-force",
                    "retrieved_at": "2026-08-25T12:00:00Z",
                    "sha256": hashlib.sha256(ordinary["bytes"]).hexdigest(),
                }
            ],
        )

        source_yaml = yaml.safe_load(
            artifact(first, "sources/model-use-of-force.SOURCE.yaml")["bytes"]
        )
        self.assertEqual(source_yaml["classification"], "model_policy")
        self.assertEqual(source_yaml["adoption_relationship"], "uncertain")
        self.assertEqual(source_yaml["review_state"], "candidate")
        self.assertEqual(
            source_yaml["sha256"],
            hashlib.sha256(
                artifact(first, "sources/model-use-of-force.txt")["bytes"]
            ).hexdigest(),
        )
        self.assertNotIn("requirements", source_yaml)
        self.assertNotIn("compliance", source_yaml)

    def test_empty_and_incomplete_searches_remain_bounded_gaps(self):
        records = load_module()
        gaps = [
            fixture("version-gap.json")["gap"],
            {
                "gap_id": "gap-empty-archive",
                "gap_type": "empty",
                "source_system_id": "fictional-policy-archive",
                "query": "fictional department policy archive",
                "filters": ["all-years"],
                "checked_date": "2026-08-25",
                "coverage_limit": "The bounded query returned no indexed result; nonexistence is not established.",
            },
        ]
        plan = records.build_collection_plan([], gaps, "2026-08-25")
        gap_yaml = yaml.safe_load(
            artifact(plan, "policy-source-gaps.yaml")["bytes"]
        )
        self.assertEqual(
            [gap["gap_type"] for gap in gap_yaml["gaps"]],
            ["empty", "incomplete"],
        )
        self.assertTrue(
            all("coverage_limit" in gap for gap in gap_yaml["gaps"])
        )

    def test_validator_rejects_changed_bytes_and_untrusted_fields(self):
        records = load_module()
        plan = records.build_collection_plan([proposal()], [], "2026-08-25")
        changed = copy.deepcopy(plan)
        artifact(changed, "sources/model-use-of-force.txt")["bytes"] += b"changed\n"
        with self.assertRaises(records.PolicySourceError) as captured:
            records.validate_collection_plan(changed)
        self.assertEqual(captured.exception.code, "hash-mismatch")

        injected = proposal()
        injected["command"] = ["read", "/undeclared"]
        with self.assertRaises(records.PolicySourceError) as captured:
            records.build_collection_plan([injected], [], "2026-08-25")
        self.assertEqual(captured.exception.code, "invalid-source-record")

    def test_validator_rejects_detached_documentation_and_unknown_duplicates(self):
        records = load_module()
        plan = records.build_collection_plan([proposal()], [], "2026-08-25")

        detached = copy.deepcopy(plan)
        documentation = artifact(
            detached, "sources/model-use-of-force.SOURCE.yaml"
        )
        documentation["path"] = "other/model-use-of-force.SOURCE.yaml"
        candidates = yaml.safe_load(
            artifact(detached, "policy-source-candidates.yaml")["bytes"]
        )
        candidates["sources"][0]["source_documentation_path"] = documentation[
            "path"
        ]
        artifact(detached, "policy-source-candidates.yaml")["bytes"] = (
            yaml.safe_dump(candidates, sort_keys=False).encode("utf-8")
        )
        with self.assertRaises(records.PolicySourceError) as captured:
            records.validate_collection_plan(detached)
        self.assertEqual(captured.exception.code, "invalid-source-yaml")

        unknown_duplicate = copy.deepcopy(plan)
        documentation = artifact(
            unknown_duplicate, "sources/model-use-of-force.SOURCE.yaml"
        )
        source_yaml = yaml.safe_load(documentation["bytes"])
        source_yaml["duplicate_of"] = ["src-not-in-collection"]
        documentation["bytes"] = yaml.safe_dump(source_yaml, sort_keys=False).encode(
            "utf-8"
        )
        with self.assertRaises(records.PolicySourceError) as captured:
            records.validate_collection_plan(unknown_duplicate)
        self.assertEqual(captured.exception.code, "invalid-source-yaml")

        analyzed = proposal()
        analyzed["requirements"] = [{"duty": "must"}]
        with self.assertRaises(records.PolicySourceError) as captured:
            records.build_collection_plan([analyzed], [], "2026-08-25")
        self.assertEqual(captured.exception.code, "invalid-source-record")

    def test_helper_has_no_filesystem_network_or_output_authority(self):
        source = SCRIPT.read_text()
        for forbidden in (
            "output_root",
            "tempfile",
            "subprocess",
            "urllib",
            "requests",
            "socket",
            ".write_text(",
            ".write_bytes(",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)

    def test_plan_can_be_published_only_beneath_explicit_output(self):
        records = load_module()
        gap = fixture("version-gap.json")["gap"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output_root = root / "output"
            output_root.mkdir()
            role_roots = {}
            for role in (
                "department-identity",
                "jurisdiction",
                "approved-source-system",
                "research-scope",
            ):
                role_root = root / role
                role_root.mkdir()
                (role_root / "input.yaml").write_text(f"role: {role}\n")
                role_roots[role] = role_root
            before = {
                role: (role_root / "input.yaml").read_bytes()
                for role, role_root in role_roots.items()
            }

            invocation = validate_invocation(
                {
                    "version": 1,
                    "skill": "collecting-police-policy-sources",
                    "inputs": [
                        {"role": role, "root": str(role_roots[role])}
                        for role in (
                            "department-identity",
                            "jurisdiction",
                            "approved-source-system",
                            "research-scope",
                        )
                    ],
                    "output": {"root": str(output_root)},
                    "runtime": {
                        "max_seconds": 60,
                        "max_input_bytes": 1048576,
                    },
                    "internet": "authorized",
                    "isolation": {
                        "inputs": "read-only",
                        "output": "read-write",
                        "undeclared": "none",
                    },
                }
            )
            run = OutputRun.start(
                invocation,
                run_id="123e4567-e89b-42d3-a456-426614174000",
                skill_version="1.0.0",
                mode="append-immutable",
                input_manifest=build_input_manifest(invocation),
            )
            configuration = run.process_configuration()
            expected_temp = str(output_root.resolve() / "temp")
            self.assertEqual(configuration["cwd"], expected_temp)
            self.assertEqual(
                set(configuration["environment"].values()),
                {expected_temp},
            )

            plan = records.build_collection_plan(
                [proposal()], [gap], "2026-08-25"
            )
            for item in plan["artifacts"]:
                run.write(
                    item["path"],
                    item["bytes"],
                    internet_sources=item["internet_sources"],
                )
            receipt = run.complete()

            self.assertTrue(receipt["internet"]["used"])
            self.assertEqual(
                {
                    role: (role_root / "input.yaml").read_bytes()
                    for role, role_root in role_roots.items()
                },
                before,
            )
            self.assertTrue(
                all(
                    path == output_root or output_root in path.parents
                    for path in output_root.rglob("*")
                )
            )
            self.assertFalse(
                any((role_root / "temp").exists() for role_root in role_roots.values())
            )


if __name__ == "__main__":
    unittest.main()
