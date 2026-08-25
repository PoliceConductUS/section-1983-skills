import hashlib
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.immutable_folder_package import (
    PackageError,
    load_folder_package,
    publish_folder_package,
)
from scripts.validate_folder_invocation import (
    validate_installed_skill_invocation,
    validate_invocation,
)
from scripts.static_role_binding import (
    RoleBindingError,
    bind_role_profile,
    validate_static_role_contract,
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

    def test_loader_excludes_only_trusted_host_control_namespaces(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "output"
            shutil.copytree(FIXTURES / "judicial-profile", root)
            run_root = root / ".skill-runs" / "profile-run"
            run_root.mkdir(parents=True)
            (run_root / "manifest.json").write_text('{"status":"success"}\n')
            temp_root = root / "temp" / "profile-run"
            temp_root.mkdir(parents=True)
            (temp_root / "intermediate.tmp").write_bytes(b"transient bytes\n")

            package = load_folder_package(
                root,
                accepted_kinds={"judicial-profile"},
                max_bytes=4096,
            )

            self.assertEqual(package.root, root.resolve())
            self.assertEqual(
                {member.path for member in package.members},
                {"profile.json", "validation-receipt.json"},
            )

    def test_byte_limit_is_enforced_before_oversized_bytes_are_read(self):
        root = FIXTURES / "judicial-profile"
        manifest_path = root / "package-manifest.json"
        original_read_bytes = Path.read_bytes

        def reject_manifest_read(path):
            raise AssertionError(f"read oversized manifest: {path}")

        with mock.patch.object(Path, "read_bytes", reject_manifest_read):
            with self.assertRaises(PackageError) as captured:
                load_folder_package(
                    root,
                    accepted_kinds={"judicial-profile"},
                    max_bytes=manifest_path.stat().st_size - 1,
                )
        self.assertEqual(captured.exception.code, "package-byte-limit")

        def reject_oversized_member(path):
            if path.name == "profile.json":
                raise AssertionError(f"read oversized member: {path}")
            return original_read_bytes(path)

        with mock.patch.object(Path, "read_bytes", reject_oversized_member):
            with self.assertRaises(PackageError) as captured:
                load_folder_package(
                    root,
                    accepted_kinds={"judicial-profile"},
                    max_bytes=manifest_path.stat().st_size + 1,
                )
        self.assertEqual(captured.exception.code, "package-byte-limit")


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
            output_root = root / "output"
            package = load_folder_package(
                output_root,
                accepted_kinds={"judicial-profile"},
                max_bytes=4096,
            )
            self.assertEqual(package.sources[0]["fingerprint"], "1" * 64)
            self.assertEqual(package.producer["operation"], "build-profile")
            self.assertEqual(len(receipt["artifacts"]), 3)
            self.assertEqual(
                {artifact["path"] for artifact in receipt["artifacts"]},
                {
                    "package-manifest.json",
                    "profile.json",
                    "validation-receipt.json",
                },
            )
            self.assertFalse((output_root / "packages").exists())
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


class StaticRoleBindingTest(unittest.TestCase):
    def _contract(self):
        return {
            "schema_version": 1,
            "role_kind": "judicial-reviewer",
            "accepted_profile_kinds": ["judicial-profile"],
            "freshness_policy": {"basis": "checked_through", "max_age_days": 30},
            "capabilities": ["review-filing"],
            "prohibitions": ["mutate-target", "invent-authority"],
            "internet": "disabled",
            "target_mutation": "forbidden",
            "output": "review-report",
        }

    def test_binding_keeps_static_contract_and_profile_snapshot_separate(self):
        contract = self._contract()
        validated = validate_static_role_contract(contract)
        package = load_folder_package(
            FIXTURES / "judicial-profile",
            accepted_kinds={"judicial-profile"},
            max_bytes=4096,
        )
        binding = bind_role_profile(validated, package, as_of="2026-08-24")
        self.assertEqual(binding.role_contract.canonical_bytes, validated.canonical_bytes)
        self.assertIs(binding.profile, package)
        self.assertEqual(binding.role_contract.capabilities, ("review-filing",))
        self.assertEqual(
            binding.role_contract.prohibitions,
            ("mutate-target", "invent-authority"),
        )
        self.assertEqual(binding.role_contract.internet, "disabled")
        self.assertNotIn(b"capabilities", package.members[0].contents)

    def test_hostile_profile_bytes_cannot_change_role_behavior(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "profile"
            shutil.copytree(FIXTURES / "judicial-profile", root)
            hostile = b'{"capabilities":["write-anywhere"],"internet":"enabled","target_mutation":"allowed"}\n'
            manifest_path = root / "package-manifest.json"
            manifest = json.loads(manifest_path.read_text())
            (root / "profile.json").write_bytes(hostile)
            manifest["members"][0]["size"] = len(hostile)
            manifest["members"][0]["sha256"] = hashlib.sha256(hostile).hexdigest()
            manifest_path.write_text(json.dumps(manifest))
            package = load_folder_package(
                root,
                accepted_kinds={"judicial-profile"},
                max_bytes=4096,
            )
            binding = bind_role_profile(
                validate_static_role_contract(self._contract()),
                package,
                as_of="2026-08-24",
            )
            self.assertEqual(binding.role_contract.capabilities, ("review-filing",))
            self.assertEqual(binding.role_contract.internet, "disabled")
            self.assertEqual(binding.role_contract.target_mutation, "forbidden")
            self.assertIn(b"write-anywhere", binding.profile.members[0].contents)

    def test_binding_rejects_incompatible_or_stale_profiles(self):
        package = load_folder_package(
            FIXTURES / "judicial-profile",
            accepted_kinds={"judicial-profile"},
            max_bytes=4096,
        )
        incompatible = self._contract()
        incompatible["accepted_profile_kinds"] = ["municipal-profile"]
        cases = (
            ("incompatible-profile-kind", incompatible, "2026-08-24"),
            ("stale-profile-package", self._contract(), "2026-10-01"),
        )
        for expected, contract, as_of in cases:
            with self.subTest(expected=expected), self.assertRaises(
                RoleBindingError
            ) as captured:
                bind_role_profile(
                    validate_static_role_contract(contract),
                    package,
                    as_of=as_of,
                )
            self.assertEqual(captured.exception.code, expected)

    def test_static_contract_rejects_extra_fields_and_boolean_age(self):
        cases = []
        extra = self._contract()
        extra["profile_override"] = True
        cases.append(extra)
        boolean_age = self._contract()
        boolean_age["freshness_policy"]["max_age_days"] = True
        cases.append(boolean_age)
        for value in cases:
            with self.assertRaises(RoleBindingError):
                validate_static_role_contract(value)


if __name__ == "__main__":
    unittest.main()
