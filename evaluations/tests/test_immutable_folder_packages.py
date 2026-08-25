import json
import re
import unittest
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
