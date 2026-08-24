import tempfile
import unittest
from pathlib import Path

from scripts.validate_folder_invocation import (
    InvocationError,
    build_input_manifest,
    resolve_input_path,
    resolve_output_path,
    validate_invocation,
)


class FolderScopedExecutionTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.record_root = self.root / "record"
        self.authority_root = self.root / "authority"
        self.output_root = self.root / "output"
        self.record_root.mkdir()
        self.authority_root.mkdir()
        self.output_root.mkdir()
        (self.record_root / "memo.txt").write_text("alpha\n", encoding="utf-8")
        (self.record_root / "exhibits").mkdir()
        (self.record_root / "exhibits" / "image.bin").write_bytes(b"\x00\x01\x02")
        (self.authority_root / "cases.txt").write_text("beta\n", encoding="utf-8")

    def tearDown(self):
        self.temporary_directory.cleanup()

    def envelope(self):
        return {
            "version": 1,
            "skill": "synthetic-skill",
            "inputs": [
                {"role": "record", "root": str(self.record_root)},
                {"role": "authority", "root": str(self.authority_root)},
            ],
            "output": {"root": str(self.output_root)},
            "runtime": {"max_seconds": 60, "max_input_bytes": 1048576},
            "internet": "disabled",
            "isolation": {
                "inputs": "read-only",
                "output": "read-write",
                "undeclared": "none",
            },
        }

    def assert_invocation_error(self, envelope):
        with self.assertRaises(InvocationError) as captured:
            validate_invocation(envelope)
        self.assertIsInstance(captured.exception.code, str)
        self.assertTrue(captured.exception.code)

    def test_validates_two_named_roots_with_literal_canonical_paths(self):
        declared_record_root = self.root / "declared-record"
        declared_authority_root = self.root / "declared-authority"
        declared_output_root = self.root / "declared-output"
        declared_record_root.symlink_to(self.record_root, target_is_directory=True)
        declared_authority_root.symlink_to(self.authority_root, target_is_directory=True)
        declared_output_root.symlink_to(self.output_root, target_is_directory=True)
        envelope = self.envelope()
        envelope["inputs"] = [
            {"role": "record", "root": str(declared_record_root)},
            {"role": "authority", "root": str(declared_authority_root)},
        ]
        envelope["output"] = {"root": str(declared_output_root)}

        invocation = validate_invocation(envelope)

        self.assertEqual(invocation.skill, "synthetic-skill")
        self.assertEqual(
            invocation.inputs,
            (
                ("record", self.record_root.resolve()),
                ("authority", self.authority_root.resolve()),
            ),
        )
        self.assertEqual(invocation.output_root, self.output_root.resolve())
        self.assertEqual(invocation.runtime, {"max_seconds": 60, "max_input_bytes": 1048576})
        self.assertEqual(invocation.internet, "disabled")
        self.assertIsNone(invocation.target)

    def test_rejects_invalid_envelopes_before_case_material_is_read(self):
        missing_root = self.root / "missing"
        missing_output_root = self.root / "missing-output"
        plain_file = self.root / "not-a-directory.txt"
        plain_file.write_text("not a directory\n", encoding="utf-8")
        cases = []
        for field in ("version", "skill", "inputs", "output", "runtime", "internet", "isolation"):
            envelope = self.envelope()
            del envelope[field]
            cases.append((f"missing-{field}", envelope))
        extra = self.envelope()
        extra["unexpected"] = True
        cases.extend(
            (
                ("extra-envelope-field", extra),
                ("duplicate-role", {**self.envelope(), "inputs": [
                    {"role": "record", "root": str(self.record_root)},
                    {"role": "record", "root": str(self.authority_root)},
                ]}),
                ("relative-root", {**self.envelope(), "inputs": [
                    {"role": "record", "root": "record"},
                    {"role": "authority", "root": str(self.authority_root)},
                ]}),
                ("input-missing-role", {**self.envelope(), "inputs": [
                    {"root": str(self.record_root)},
                    {"role": "authority", "root": str(self.authority_root)},
                ]}),
                ("input-missing-root", {**self.envelope(), "inputs": [
                    {"role": "record"},
                    {"role": "authority", "root": str(self.authority_root)},
                ]}),
                ("input-unknown-field", {**self.envelope(), "inputs": [
                    {"role": "record", "root": str(self.record_root), "unexpected": True},
                    {"role": "authority", "root": str(self.authority_root)},
                ]}),
                ("missing-root", {**self.envelope(), "inputs": [
                    {"role": "record", "root": str(missing_root)},
                    {"role": "authority", "root": str(self.authority_root)},
                ]}),
                ("non-directory-input-root", {**self.envelope(), "inputs": [
                    {"role": "record", "root": str(plain_file)},
                    {"role": "authority", "root": str(self.authority_root)},
                ]}),
                ("missing-output-root", {**self.envelope(), "output": {"root": str(missing_output_root)}}),
                ("output-missing-root", {**self.envelope(), "output": {}}),
                ("output-unknown-field", {**self.envelope(), "output": {
                    "root": str(self.output_root), "unexpected": True,
                }}),
                ("non-directory-output-root", {**self.envelope(), "output": {"root": str(plain_file)}}),
                ("runtime-missing-seconds", {**self.envelope(), "runtime": {
                    "max_input_bytes": 1048576,
                }}),
                ("runtime-missing-bytes", {**self.envelope(), "runtime": {
                    "max_seconds": 60,
                }}),
                ("runtime-unknown-field", {**self.envelope(), "runtime": {
                    "max_seconds": 60, "max_input_bytes": 1048576, "unexpected": True,
                }}),
                ("isolation-missing-inputs", {**self.envelope(), "isolation": {
                    "output": "read-write", "undeclared": "none",
                }}),
                ("isolation-missing-output", {**self.envelope(), "isolation": {
                    "inputs": "read-only", "undeclared": "none",
                }}),
                ("isolation-missing-undeclared", {**self.envelope(), "isolation": {
                    "inputs": "read-only", "output": "read-write",
                }}),
                ("isolation-unknown-field", {**self.envelope(), "isolation": {
                    "inputs": "read-only", "output": "read-write", "undeclared": "none",
                    "unexpected": True,
                }}),
                ("invalid-isolation-inputs", {**self.envelope(), "isolation": {
                    "inputs": "read-write", "output": "read-write", "undeclared": "none",
                }}),
                ("invalid-isolation-output", {**self.envelope(), "isolation": {
                    "inputs": "read-only", "output": "read-only", "undeclared": "none",
                }}),
                ("invalid-isolation-undeclared", {**self.envelope(), "isolation": {
                    "inputs": "read-only", "output": "read-write", "undeclared": "available",
                }}),
                ("invalid-internet", {**self.envelope(), "internet": "enabled"}),
                ("invalid-runtime-seconds", {**self.envelope(), "runtime": {
                    "max_seconds": 0, "max_input_bytes": 1048576,
                }}),
                ("invalid-runtime-bytes", {**self.envelope(), "runtime": {
                    "max_seconds": 60, "max_input_bytes": 0,
                }}),
            )
        )

        for label, envelope in cases:
            with self.subTest(case=label):
                self.assert_invocation_error(envelope)

    def test_rejects_roots_contained_by_each_other(self):
        inside_input = self.record_root / "output"
        inside_input.mkdir()
        output_inside_input = self.envelope()
        output_inside_input["output"] = {"root": str(inside_input)}
        self.assert_invocation_error(output_inside_input)

        inside_output = self.output_root / "record"
        inside_output.mkdir()
        input_inside_output = self.envelope()
        input_inside_output["inputs"] = [
            {"role": "record", "root": str(inside_output)},
            {"role": "authority", "root": str(self.authority_root)},
        ]
        self.assert_invocation_error(input_inside_output)

    def test_rejects_invalid_target_selection(self):
        outside = self.root / "outside.txt"
        outside.write_text("outside\n", encoding="utf-8")
        (self.record_root / "escape.txt").symlink_to(outside)
        cases = (
            ("absolute-child", "/etc/passwd"),
            ("parent-traversal", "../outside.txt"),
            ("missing-target", "missing.txt"),
            ("symlink-escape", "escape.txt"),
        )

        for label, path in cases:
            with self.subTest(case=label):
                envelope = self.envelope()
                envelope["target"] = {"role": "record", "path": path}
                self.assert_invocation_error(envelope)

    def test_resolves_only_existing_confined_input_children(self):
        invocation = validate_invocation(self.envelope())

        self.assertEqual(
            resolve_input_path(invocation, "record", "exhibits/image.bin"),
            self.record_root / "exhibits" / "image.bin",
        )
        for role, path in (
            ("record", "/etc/passwd"),
            ("record", "../outside.txt"),
            ("record", "missing.txt"),
            ("unknown", "memo.txt"),
        ):
            with self.subTest(role=role, path=path):
                with self.assertRaises(InvocationError):
                    resolve_input_path(invocation, role, path)

    def test_resolves_only_confined_output_children_without_writing(self):
        invocation = validate_invocation(self.envelope())

        resolved = resolve_output_path(invocation, "drafts/result.md")
        self.assertEqual(resolved, self.output_root / "drafts" / "result.md")
        self.assertFalse(resolved.exists())
        for path in ("/tmp/result.md", "../result.md"):
            with self.subTest(path=path):
                with self.assertRaises(InvocationError):
                    resolve_output_path(invocation, path)

    def test_builds_hand_derived_logical_manifest(self):
        invocation = validate_invocation(self.envelope())

        self.assertEqual(
            build_input_manifest(invocation),
            {
                "inputs": [
                    {
                        "role": "record",
                        "files": [
                            {
                                "path": "exhibits/image.bin",
                                "size": 3,
                                "sha256": "ae4b3280e56e2faf83f414a6e3dabe9d5fbe18976544c05fed121accb85b53fc",
                            },
                            {
                                "path": "memo.txt",
                                "size": 6,
                                "sha256": "b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060",
                            },
                        ],
                    },
                    {
                        "role": "authority",
                        "files": [
                            {
                                "path": "cases.txt",
                                "size": 5,
                                "sha256": "f2c82decdd7181cf98945929a62598db7e6b477e11f6e0eb0ae97020eff151ad",
                            }
                        ],
                    },
                ]
            },
        )

    def test_manifest_is_logical_across_different_absolute_roots(self):
        invocation = validate_invocation(self.envelope())
        with tempfile.TemporaryDirectory() as directory:
            relocated_root = Path(directory)
            relocated_record = relocated_root / "record"
            relocated_authority = relocated_root / "authority"
            relocated_output = relocated_root / "output"
            relocated_record.mkdir()
            relocated_authority.mkdir()
            relocated_output.mkdir()
            (relocated_record / "memo.txt").write_text("alpha\n", encoding="utf-8")
            (relocated_record / "exhibits").mkdir()
            (relocated_record / "exhibits" / "image.bin").write_bytes(b"\x00\x01\x02")
            (relocated_authority / "cases.txt").write_text("beta\n", encoding="utf-8")
            relocated_envelope = self.envelope()
            relocated_envelope["inputs"] = [
                {"role": "record", "root": str(relocated_record)},
                {"role": "authority", "root": str(relocated_authority)},
            ]
            relocated_envelope["output"] = {"root": str(relocated_output)}

            self.assertEqual(
                build_input_manifest(invocation),
                build_input_manifest(validate_invocation(relocated_envelope)),
            )

    def test_manifest_allows_internal_file_symlinks(self):
        (self.record_root / "memo-link.txt").symlink_to("memo.txt")
        invocation = validate_invocation(self.envelope())

        manifest = build_input_manifest(invocation)

        self.assertEqual(manifest["inputs"][0]["files"][1], {
            "path": "memo-link.txt",
            "size": 6,
            "sha256": "b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060",
        })

    def test_manifest_rejects_external_file_and_directory_symlinks(self):
        external_file = self.root / "outside.txt"
        external_directory = self.root / "outside-directory"
        external_file.write_text("outside\n", encoding="utf-8")
        external_directory.mkdir()
        (external_directory / "outside.txt").write_text("outside\n", encoding="utf-8")
        invocation = validate_invocation(self.envelope())

        for link_name, target in (("file-link", external_file), ("directory-link", external_directory)):
            with self.subTest(link=link_name):
                (self.record_root / link_name).symlink_to(target)
                with self.assertRaises(InvocationError):
                    build_input_manifest(invocation)
                (self.record_root / link_name).unlink()

    def test_manifest_rejects_directory_symlink_cycles(self):
        cycle_directory = self.record_root / "cycle"
        cycle_directory.mkdir()
        (cycle_directory / "again").symlink_to("..")
        invocation = validate_invocation(self.envelope())

        with self.assertRaises(InvocationError):
            build_input_manifest(invocation)


if __name__ == "__main__":
    unittest.main()
