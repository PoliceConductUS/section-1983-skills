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
SKILL = REPOSITORY / "skills" / "collecting-legal-authority-sources"
SCRIPT = SKILL / "scripts" / "authority_source_records.py"
FIXTURES = (
    REPOSITORY / "evaluations" / "tests" / "fixtures" / "authority-source-collection"
)
ROLES = [
    "legal-question",
    "jurisdiction",
    "court-hierarchy",
    "relevant-date",
    "seed-authority",
    "approved-source-system",
]


def load_module():
    specification = importlib.util.spec_from_file_location(
        "authority_source_records", SCRIPT
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def fixture(name):
    return json.loads((FIXTURES / name).read_text())


def proposal():
    source = fixture("mirror-opinion.json")["source"]
    source["artifact_bytes"] = source.pop("artifact_text").encode()
    return source


def gap():
    return fixture("coverage-gap.json")["gap"]


def artifact(plan, path):
    return next(item for item in plan["artifacts"] if item["path"] == path)


def paths(plan):
    return [item["path"] for item in plan["artifacts"]]


class CollectingLegalAuthoritySourcesTest(unittest.TestCase):
    def test_installed_skill_has_exact_folder_and_network_contract(self):
        contract = json.loads(
            (SKILL / "references" / "folder-contract.json").read_text()
        )
        self.assertEqual(
            contract,
            {
                "version": 1,
                "skill": "collecting-legal-authority-sources",
                "input_roles": ROLES,
                "target": {"policy": "none", "roles": []},
                "internet": "authorized",
                "output": {"mode": "append-immutable"},
            },
        )
        entrypoint = (SKILL / "SKILL.md").read_text().lower()
        self.assertIn("<output-folder>/temp", entrypoint)
        self.assertIn("authority-source-candidates.yaml", entrypoint)
        self.assertIn("authority-source-gaps.yaml", entrypoint)
        self.assertIn("audit-authorities", entrypoint)
        self.assertIn("never establish that no authority exists", entrypoint)

    def test_helper_returns_deterministic_ordinary_files_and_source_yaml(self):
        records = load_module()
        first = records.build_collection_plan([proposal()], [gap()], "2026-08-25")
        second = records.build_collection_plan([proposal()], [gap()], "2026-08-25")
        self.assertEqual(first, second)
        self.assertEqual(
            paths(first),
            [
                "sources/fictional-opinion-mirror.txt",
                "sources/fictional-opinion-mirror.SOURCE.yaml",
                "authority-source-candidates.yaml",
                "authority-source-gaps.yaml",
            ],
        )
        ordinary = artifact(first, "sources/fictional-opinion-mirror.txt")
        self.assertEqual(
            ordinary["internet_sources"],
            [
                {
                    "url": "https://example.invalid/fictional-opinion",
                    "retrieved_at": "2026-08-25T12:00:00Z",
                    "sha256": hashlib.sha256(ordinary["bytes"]).hexdigest(),
                }
            ],
        )
        source_yaml = yaml.safe_load(
            artifact(first, "sources/fictional-opinion-mirror.SOURCE.yaml")[
                "bytes"
            ]
        )
        self.assertEqual(source_yaml["source_type"], "mirror")
        self.assertEqual(source_yaml["citation_identity"]["status"], "proposed")
        self.assertEqual(source_yaml["verification_state"], "unverified")
        self.assertNotIn("binding", source_yaml)
        self.assertNotIn("proposition_fit", source_yaml)
        self.assertNotIn("fair_warning", source_yaml)

    def test_empty_and_incomplete_searches_remain_bounded_gaps(self):
        records = load_module()
        empty = {
            "gap_id": "gap-empty-official-search",
            "gap_type": "empty",
            "source_system_id": "fictional-official-search",
            "query": "fictional controlling authority",
            "filters": ["before:2025-06-15"],
            "checked_date": "2026-08-25",
            "coverage_limit": "The bounded query returned no result; nonexistence is not established.",
        }
        plan = records.build_collection_plan([], [gap(), empty], "2026-08-25")
        gaps = yaml.safe_load(
            artifact(plan, "authority-source-gaps.yaml")["bytes"]
        )["gaps"]
        self.assertEqual(
            [item["gap_type"] for item in gaps], ["empty", "incomplete"]
        )
        self.assertTrue(all(item["coverage_limit"] for item in gaps))

    def test_changed_bytes_and_untrusted_fields_fail_closed(self):
        records = load_module()
        plan = records.build_collection_plan([proposal()], [], "2026-08-25")
        changed = copy.deepcopy(plan)
        artifact(changed, "sources/fictional-opinion-mirror.txt")[
            "bytes"
        ] += b"changed\n"
        with self.assertRaises(records.AuthoritySourceError) as captured:
            records.validate_collection_plan(changed)
        self.assertEqual(captured.exception.code, "hash-mismatch")

        injected = proposal()
        injected["command"] = ["read", "/undeclared"]
        with self.assertRaises(records.AuthoritySourceError) as captured:
            records.build_collection_plan([injected], [], "2026-08-25")
        self.assertEqual(captured.exception.code, "invalid-source-record")

    def test_duplicates_mistaken_identity_and_unofficial_sources_stay_explicit(self):
        records = load_module()
        mirror = proposal()
        mistaken = proposal()
        mistaken["source_id"] = "src-mistaken-opinion"
        mistaken["artifact_path"] = "sources/mistaken-opinion.txt"
        mistaken["source_documentation_path"] = "sources/mistaken-opinion.SOURCE.yaml"
        mistaken["result_identity"] = "example-invalid:mistaken-opinion"
        mistaken["citation_identity"]["status"] = "mistaken"
        mistaken["review_state"] = "rejected"
        mistaken["duplicate_of"] = [mirror["source_id"]]
        plan = records.build_collection_plan(
            [mistaken, mirror], [], "2026-08-25"
        )
        candidates = yaml.safe_load(
            artifact(plan, "authority-source-candidates.yaml")["bytes"]
        )["sources"]
        rejected = next(
            item for item in candidates if item["source_id"] == "src-mistaken-opinion"
        )
        self.assertEqual(rejected["identity_status"], "mistaken")
        self.assertEqual(rejected["review_state"], "rejected")
        official = next(
            item
            for item in candidates
            if item["source_id"] == "src-fictional-opinion-mirror"
        )
        self.assertEqual(official["source_type"], "mirror")

        unknown = copy.deepcopy(plan)
        documentation = artifact(
            unknown, "sources/mistaken-opinion.SOURCE.yaml"
        )
        source_yaml = yaml.safe_load(documentation["bytes"])
        source_yaml["duplicate_of"] = ["src-unknown"]
        documentation["bytes"] = yaml.safe_dump(source_yaml, sort_keys=False).encode()
        with self.assertRaises(records.AuthoritySourceError) as captured:
            records.validate_collection_plan(unknown)
        self.assertEqual(captured.exception.code, "invalid-source-yaml")

        second = proposal()
        second["source_id"] = "src-second-opinion"
        second["artifact_path"] = "sources/second-opinion.txt"
        second["source_documentation_path"] = "sources/second-opinion.SOURCE.yaml"
        second["result_identity"] = "example-invalid:second-opinion"
        duplicate_identity = records.build_collection_plan(
            [proposal(), second], [], "2026-08-25"
        )
        second_documentation = artifact(
            duplicate_identity, "sources/second-opinion.SOURCE.yaml"
        )
        second_yaml = yaml.safe_load(second_documentation["bytes"])
        second_yaml["result_identity"] = "example-invalid:fictional-opinion"
        second_documentation["bytes"] = yaml.safe_dump(
            second_yaml, sort_keys=False
        ).encode()
        with self.assertRaises(records.AuthoritySourceError) as captured:
            records.validate_collection_plan(duplicate_identity)
        self.assertEqual(captured.exception.code, "duplicate-result-identity")

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

    def test_trusted_host_publishes_with_output_local_temp_and_provenance(self):
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
                    "skill": "collecting-legal-authority-sources",
                    "inputs": [
                        {"role": role, "root": str(role_folders[role])}
                        for role in ROLES
                    ],
                    "output": {"root": str(output)},
                    "runtime": {"max_seconds": 60, "max_input_bytes": 1048576},
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
                run_id="423e4567-e89b-42d3-a456-426614174000",
                skill_version="1.0.0",
                mode="append-immutable",
                input_manifest=build_input_manifest(invocation),
            )
            expected_temp = str(output.resolve() / "temp")
            self.assertEqual(run.process_configuration()["cwd"], expected_temp)
            plan = records.build_collection_plan(
                [proposal()], [gap()], "2026-08-25"
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
                    role: (folder / "input.yaml").read_bytes()
                    for role, folder in role_folders.items()
                },
                before,
            )
            self.assertFalse(
                any((folder / "temp").exists() for folder in role_folders.values())
            )


if __name__ == "__main__":
    unittest.main()
