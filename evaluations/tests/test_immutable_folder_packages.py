import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.immutable_folder_package import (
    PackageError,
    load_folder_package,
    publish_folder_package,
)
from scripts.validate_folder_invocation import (
    validate_installed_skill_invocation,
    validate_invocation,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "evaluations" / "folder-package-fixtures"
PACKAGE_KINDS = (
    "judicial-profile",
    "counsel-team-profile",
    "litigation-alignment",
    "municipal-profile",
)


class ImmutableFolderPackageStructureTest(unittest.TestCase):
    def test_public_schemas_are_strict_versioned_contracts(self):
        package = json.loads(
            (ROOT / "governance" / "immutable-folder-package.schema.json").read_text()
        )
        role = json.loads(
            (ROOT / "governance" / "static-role-contract.schema.json").read_text()
        )
        self.assertFalse(package["additionalProperties"])
        self.assertEqual(package["properties"]["schema_version"], {"const": 1, "type": "integer"})
        self.assertEqual(
            package["required"],
            [
                "schema_version",
                "package_kind",
                "package_id",
                "created_at",
                "freshness",
                "producer",
                "sources",
                "members",
                "validation",
            ],
        )
        self.assertFalse(role["additionalProperties"])
        self.assertEqual(role["properties"]["schema_version"], {"const": 1, "type": "integer"})
        self.assertEqual(
            role["required"],
            [
                "schema_version",
                "role_kind",
                "accepted_profile_kinds",
                "freshness_policy",
                "capabilities",
                "prohibitions",
                "internet",
                "target_mutation",
                "output",
            ],
        )
        path_pattern = re.compile(package["$defs"]["member"]["properties"]["path"]["pattern"])
        self.assertIsNotNone(path_pattern.fullmatch("profiles/example.json"))
        for path in ("package-manifest.json", "/absolute", "../escape", "a/../b", "a//b", "a\\b"):
            self.assertIsNone(path_pattern.fullmatch(path), path)

    def test_four_fictional_package_families_have_complete_manifests(self):
        for kind in PACKAGE_KINDS:
            with self.subTest(kind=kind):
                root = FIXTURES / kind
                manifest = json.loads((root / "package-manifest.json").read_text())
                self.assertEqual(manifest["package_kind"], kind)
                self.assertEqual(manifest["schema_version"], 1)
                self.assertTrue(manifest["package_id"].startswith("fictional-"))
                listed = [member["path"] for member in manifest["members"]]
                actual = sorted(
                    path.relative_to(root).as_posix()
                    for path in root.rglob("*")
                    if path.is_file() and path.name != "package-manifest.json"
                )
                self.assertEqual(sorted(listed), actual)
                self.assertIn(manifest["validation"]["receipt_member_id"], {member["id"] for member in manifest["members"]})


class ImmutableFolderPackageLoaderTest(unittest.TestCase):
    def test_loader_pins_complete_verified_member_bytes(self):
        for kind in PACKAGE_KINDS:
            with self.subTest(kind=kind):
                package = load_folder_package(
                    FIXTURES / kind,
                    accepted_kinds={kind},
                    max_bytes=4096,
                )
                self.assertEqual(
                    (package.package_kind, package.package_id),
                    (kind, f"fictional-{kind}"),
                )
                self.assertRegex(package.fingerprint, r"^[0-9a-f]{64}$")
                self.assertEqual(package.fingerprint, package.manifest_sha256)
                self.assertEqual(len(package.members), 2)
                self.assertTrue(
                    all(isinstance(member.contents, bytes) for member in package.members)
                )
                self.assertEqual(package.validation["status"], "passed")

    def test_snapshot_does_not_reread_mutated_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "package"
            shutil.copytree(FIXTURES / "judicial-profile", root)
            package = load_folder_package(
                root, accepted_kinds={"judicial-profile"}, max_bytes=4096
            )
            original = package.members[0].contents
            (root / package.members[0].path).write_text("changed after validation")
            self.assertEqual(package.members[0].contents, original)

    def test_loader_rejects_incomplete_mismatched_aliased_and_oversized_packages(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            cases = {}
            extra = base / "extra"
            shutil.copytree(FIXTURES / "judicial-profile", extra)
            (extra / "unlisted.txt").write_text("unlisted")
            cases["unlisted-package-member"] = extra

            mismatch = base / "mismatch"
            shutil.copytree(FIXTURES / "judicial-profile", mismatch)
            (mismatch / "profile.json").write_text("changed")
            cases["package-member-mismatch"] = mismatch

            alias = base / "alias"
            shutil.copytree(FIXTURES / "judicial-profile", alias)
            (alias / "profile.json").unlink()
            (alias / "profile.json").symlink_to(
                FIXTURES / "judicial-profile" / "profile.json"
            )
            cases["aliased-package-member"] = alias

            for expected, root in cases.items():
                with self.subTest(expected=expected), self.assertRaises(
                    PackageError
                ) as captured:
                    load_folder_package(
                        root,
                        accepted_kinds={"judicial-profile"},
                        max_bytes=4096,
                    )
                self.assertEqual(captured.exception.code, expected)


class ImmutableFolderPackagePublisherTest(unittest.TestCase):
    def _envelope(self, root: Path):
        context = root / "context"
        authorities = root / "authorities"
        filing = root / "filing"
        output = root / "output"
        for folder in (context, authorities, filing, output):
            folder.mkdir()
        (context / "facts.txt").write_text("fictional source\n")
        return {
            "version": 1,
            "skill": "drafting-section-1983-complaints",
            "inputs": [
                {"role": "record", "root": str(context)},
                {"role": "authorities", "root": str(authorities)},
                {"role": "filing", "root": str(filing)},
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

    def test_publisher_writes_one_complete_reloadable_package_and_preserves_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            envelope = self._envelope(root)
            invocation = validate_installed_skill_invocation(
                envelope,
                ROOT / "skills" / "drafting-section-1983-complaints",
            )
            before = (root / "context" / "facts.txt").read_bytes()
            receipt = publish_folder_package(
                invocation,
                package_kind="judicial-profile",
                package_id="generated-judicial-profile",
                created_at="2026-08-24T13:00:00Z",
                freshness={"checked_through": "2026-08-24", "retrieved_on": "2026-08-24"},
                sources=[
                    {
                        "role": "source-package",
                        "source_id": "fictional-source-profile",
                        "fingerprint": "1" * 64,
                    }
                ],
                members=[
                    {
                        "id": "profile",
                        "role": "primary",
                        "classification": "profile",
                        "path": "profile.json",
                        "media_type": "application/json",
                        "contents": '{"fictional":true}\n',
                    },
                    {
                        "id": "validation-receipt",
                        "role": "receipt",
                        "classification": "validation-receipt",
                        "path": "validation-receipt.json",
                        "media_type": "application/json",
                        "contents": '{"status":"passed"}\n',
                    },
                ],
                validation={
                    "status": "passed",
                    "validator": "example-validator",
                    "version": "1",
                    "validated_at": "2026-08-24T13:00:00Z",
                    "receipt_member_id": "validation-receipt",
                },
                operation="build-profile",
                run_id="package-run-1",
                skill_version="1",
            )
            package = load_folder_package(
                root / "output" / "packages" / "generated-judicial-profile",
                accepted_kinds={"judicial-profile"},
                max_bytes=4096,
            )
            self.assertEqual(package.sources[0]["fingerprint"], "1" * 64)
            self.assertEqual(package.producer["operation"], "build-profile")
            self.assertEqual(len(receipt["artifacts"]), 3)
            self.assertEqual((root / "context" / "facts.txt").read_bytes(), before)

    def test_publisher_rejects_invocation_not_bound_to_installed_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            invocation = validate_invocation(self._envelope(root))
            with self.assertRaises(PackageError) as captured:
                publish_folder_package(
                    invocation,
                    package_kind="judicial-profile",
                    package_id="generated-profile",
                    created_at="2026-08-24T13:00:00Z",
                    freshness={"checked_through": None, "retrieved_on": None},
                    sources=[],
                    members=[],
                    validation={},
                    operation="build-profile",
                    run_id="package-run-2",
                    skill_version="1",
                )
            self.assertEqual(captured.exception.code, "unbound-package-invocation")

            with self.assertRaises(PackageError) as captured:
                load_folder_package(
                    FIXTURES / "judicial-profile",
                    accepted_kinds={"judicial-profile"},
                    max_bytes=10,
                )
            self.assertEqual(captured.exception.code, "package-byte-limit")

    def test_loader_rejects_malformed_contract_and_receipt_linkage(self):
        mutations = {
            "invalid-package-manifest": lambda value: value.update(
                schema_version=True
            ),
            "unsupported-package-kind": lambda value: value.update(
                package_kind="municipal-profile"
            ),
            "invalid-package-freshness": lambda value: value["freshness"].update(
                checked_through="08/24/2026"
            ),
            "invalid-package-validation": lambda value: value["validation"].update(
                status="failed"
            ),
            "invalid-package-validation-receipt": lambda value: value[
                "validation"
            ].update(receipt_member_id="profile"),
        }
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            for index, (expected, mutate) in enumerate(mutations.items()):
                root = base / str(index)
                shutil.copytree(FIXTURES / "judicial-profile", root)
                manifest_path = root / "package-manifest.json"
                value = json.loads(manifest_path.read_text())
                mutate(value)
                manifest_path.write_text(json.dumps(value))
                with self.subTest(expected=expected), self.assertRaises(
                    PackageError
                ) as captured:
                    load_folder_package(
                        root,
                        accepted_kinds={"judicial-profile"},
                        max_bytes=4096,
                    )
                self.assertEqual(captured.exception.code, expected)


if __name__ == "__main__":
    unittest.main()
