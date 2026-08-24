import hashlib
import io
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import skill_output_writer
from scripts.skill_output_writer import OutputError, OutputRun
from scripts.validate_folder_invocation import build_input_manifest, validate_invocation


INPUT_MANIFEST_SHA256 = "7fcb5bb404fd81345d585c26eba719249559720fae28d4f95ec670dbebd45ddd"


class FailingBinaryStream:
    def __init__(self):
        self.read_count = 0

    def read(self, _size=-1):
        self.read_count += 1
        if self.read_count == 1:
            return b"partial bytes"
        raise OSError("injected source path /private/case-material")


class SkillOutputWriterTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.record_root = self.root / "record"
        self.authority_root = self.root / "authority"
        self.output_root = self.root / "output"
        self.record_root.mkdir()
        self.authority_root.mkdir()
        self.output_root.mkdir()
        (self.record_root / "source.txt").write_bytes(b"immutable input\n")
        (self.authority_root / "cases.txt").write_bytes(b"authority\n")
        self.invocation = validate_invocation(
            {
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
        )
        self.input_manifest = build_input_manifest(self.invocation)

    def tearDown(self):
        self.temporary_directory.cleanup()

    def start_run(self, run_id, mode="append-immutable"):
        return OutputRun.start(
            self.invocation,
            run_id=run_id,
            skill_version="1.4.0",
            mode=mode,
            input_manifest=self.input_manifest,
        )

    def run_directory(self, run_id):
        return self.output_root / ".skill-runs" / run_id

    def make_relocated_invocation(self, name, *, internet="disabled"):
        relocated_root = self.root / name
        record_root = relocated_root / "record"
        authority_root = relocated_root / "authority"
        output_root = relocated_root / "output"
        record_root.mkdir(parents=True)
        authority_root.mkdir()
        output_root.mkdir()
        (record_root / "source.txt").write_bytes(b"immutable input\n")
        (authority_root / "cases.txt").write_bytes(b"authority\n")
        invocation = validate_invocation(
            {
                "version": 1,
                "skill": "synthetic-skill",
                "inputs": [
                    {"role": "record", "root": str(record_root)},
                    {"role": "authority", "root": str(authority_root)},
                ],
                "output": {"root": str(output_root)},
                "runtime": {"max_seconds": 60, "max_input_bytes": 1048576},
                "internet": internet,
                "isolation": {
                    "inputs": "read-only",
                    "output": "read-write",
                    "undeclared": "none",
                },
            }
        )
        return invocation, build_input_manifest(invocation), output_root

    def valid_internet_source(self, **overrides):
        source = {
            "url": "https://example.test/source",
            "retrieved_at": "2026-08-24T12:34:56Z",
            "sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
        }
        source.update(overrides)
        return source

    def assert_error(self, operation, code=None):
        with self.assertRaises(OutputError) as captured:
            operation()
        if code is not None:
            self.assertEqual(captured.exception.code, code)
            self.assertEqual(str(captured.exception), code)
        self.assertNotIn(str(self.root), str(captured.exception))
        self.assertNotIn("/private/case-material", str(captured.exception))
        return captured.exception

    def assert_terminal_and_closed(self, run):
        operations = (
            ("write", lambda: run.write("reports/late.md", b"must not publish")),
            ("complete", run.complete),
            ("fail", lambda: run.fail("late-failure", "terminal-transition")),
        )
        for label, operation in operations:
            with self.subTest(operation=label):
                self.assert_error(operation, "run-terminal")
        self.assertEqual(run._root_fd, -1)
        self.assertEqual(run._run_fd, -1)
        self.assertEqual(run._staging_fd, -1)

    def snapshot_path(self, path):
        metadata = path.stat()
        return {
            "device": metadata.st_dev,
            "inode": metadata.st_ino,
            "mode": stat.S_IMODE(metadata.st_mode),
            "size": metadata.st_size,
            "modified": metadata.st_mtime_ns,
            "bytes": path.read_bytes(),
        }

    def snapshot_tree_at(self, root):
        root_metadata = root.lstat()
        entries = {
            ".": {
                "device": root_metadata.st_dev,
                "inode": root_metadata.st_ino,
                "mode": root_metadata.st_mode,
                "size": root_metadata.st_size,
                "modified": root_metadata.st_mtime_ns,
            }
        }

        def walk(directory, relative_parent):
            for entry in sorted(os.scandir(directory), key=lambda item: item.name):
                relative = relative_parent / entry.name
                metadata = entry.stat(follow_symlinks=False)
                record = {
                    "device": metadata.st_dev,
                    "inode": metadata.st_ino,
                    "mode": metadata.st_mode,
                    "size": metadata.st_size,
                    "modified": metadata.st_mtime_ns,
                }
                if stat.S_ISREG(metadata.st_mode):
                    record["bytes"] = Path(entry.path).read_bytes()
                elif stat.S_ISLNK(metadata.st_mode):
                    record["target"] = os.readlink(entry.path)
                entries[relative.as_posix()] = record
                if stat.S_ISDIR(metadata.st_mode):
                    walk(Path(entry.path), relative)

        walk(root, Path())
        return entries

    def snapshot_tree(self):
        return self.snapshot_tree_at(self.output_root)

    def assert_failed_write_is_confined(self, relative_path, run_id, before):
        self.assertFalse(os.path.lexists(self.output_root / relative_path))
        after = self.snapshot_tree()
        staging = Path(".skill-runs") / run_id / "staging"
        final_path = Path(relative_path)
        allowed_parent_directories = {
            Path(*final_path.parts[:index])
            for index in range(1, len(final_path.parts))
        }
        for relative in before:
            self.assertIn(relative, after, f"existing output entry removed after failure: {relative}")
        for relative, record in after.items():
            relative_entry = Path(relative)
            if relative in before:
                mutable_directory = stat.S_ISDIR(record["mode"]) and (
                    relative_entry == Path(".")
                    or relative_entry in allowed_parent_directories
                    or relative_entry.is_relative_to(staging)
                )
                if mutable_directory:
                    continue
                self.assertEqual(
                    record,
                    before[relative],
                    f"existing output entry changed after failure: {relative}",
                )
                continue
            mode = record["mode"]
            if stat.S_ISREG(mode):
                self.assertTrue(
                    relative_entry.is_relative_to(staging),
                    f"new failure artifact escaped staging: {relative}",
                )
            elif stat.S_ISDIR(mode):
                self.assertTrue(
                    relative_entry.is_relative_to(staging)
                    or relative_entry in allowed_parent_directories,
                    f"unexpected directory created after failure: {relative}",
                )
            else:
                self.fail(f"symlink or special file created after failure: {relative}")

    def test_writes_utf8_text_with_exact_bytes_hash_and_size(self):
        run = self.start_run("text-run")

        run.write("reports/text.md", "Résumé\n")

        output = self.output_root / "reports" / "text.md"
        self.assertEqual(output.read_bytes(), b"R\xc3\xa9sum\xc3\xa9\n")
        self.assertEqual(output.stat().st_size, 9)
        self.assertEqual(
            hashlib.sha256(output.read_bytes()).hexdigest(),
            "f2289de8b83919a1c37faf51771976cb2e4d8b487544ce76936d34963266d8fd",
        )

    def test_append_immutable_writes_bytes_beside_prior_output(self):
        prior = self.output_root / "prior.txt"
        prior.write_bytes(b"prior immutable output\n")
        prior_snapshot = self.snapshot_path(prior)
        run = self.start_run("bytes-run", mode="append-immutable")

        run.write("artifacts/data.bin", b"\x00\xffbinary\n")

        output = self.output_root / "artifacts" / "data.bin"
        self.assertEqual(output.read_bytes(), b"\x00\xffbinary\n")
        self.assertEqual(output.stat().st_size, 9)
        self.assertEqual(
            hashlib.sha256(output.read_bytes()).hexdigest(),
            "4b76fcf047ba868db30581655ee9f5da76716922488b803869ecdfef4122ed53",
        )
        self.assertEqual(self.snapshot_path(prior), prior_snapshot)

    def test_fresh_regenerable_writes_a_binary_stream_to_an_empty_output(self):
        run = self.start_run("stream-run", mode="fresh-regenerable")

        run.write("exports/stream.bin", io.BytesIO(b"streamed\x00payload"))

        output = self.output_root / "exports" / "stream.bin"
        self.assertEqual(output.read_bytes(), b"streamed\x00payload")
        self.assertEqual(output.stat().st_size, 16)
        self.assertEqual(
            hashlib.sha256(output.read_bytes()).hexdigest(),
            "d0c48210f277d47f32849344d4428a834059861b23e56b3a37fca08dbb84bdc1",
        )

    def test_fresh_regenerable_rejects_nonempty_output_without_changes(self):
        prior = self.output_root / "prior.txt"
        prior.write_bytes(b"prior immutable output\n")
        before = self.snapshot_tree()

        self.assert_error(
            lambda: self.start_run("not-fresh-run", mode="fresh-regenerable"),
            "output-not-fresh",
        )

        self.assertEqual(self.snapshot_tree(), before)
        self.assertEqual(prior.read_bytes(), b"prior immutable output\n")

    def test_rejects_an_unsupported_run_mode_without_output_changes(self):
        before = self.snapshot_tree()

        self.assert_error(
            lambda: self.start_run("unsupported-mode-run", mode="replace-existing"),
            "invalid-run-mode",
        )

        self.assertEqual(self.snapshot_tree(), before)

    def test_rejects_non_string_and_unhashable_run_modes_without_output_changes(self):
        for label, mode in (("none", None), ("list", []), ("dict", {})):
            with self.subTest(case=label):
                before = self.snapshot_tree()

                self.assert_error(
                    lambda value=mode: self.start_run("invalid-mode-run", mode=value),
                    "invalid-run-mode",
                )

                self.assertEqual(self.snapshot_tree(), before)

    def test_input_index_recursion_exhaustion_is_bounded_before_output_changes(self):
        current = self.record_root
        for _ in range(120):
            current = current / "d"
            current.mkdir()
        (current / "deep.txt").write_bytes(b"deep input\n")
        before = self.snapshot_tree()
        original_limit = sys.getrecursionlimit()

        try:
            sys.setrecursionlimit(80)
            self.assert_error(
                lambda: self.start_run("deep-input-run"),
                "input-index-unavailable",
            )
        finally:
            sys.setrecursionlimit(original_limit)

        self.assertEqual(self.snapshot_tree(), before)

    def test_rejects_invalid_run_ids_before_creating_run_state(self):
        cases = (
            ("empty", ""),
            ("dot", "."),
            ("parent", ".."),
            ("parent-traversal", "../escape"),
            ("slash", "nested/run"),
            ("backslash", "nested\\run"),
            ("absolute", "/absolute-run"),
            ("drive-prefix", "C:/run"),
            ("nul", "nul\x00run"),
        )

        for label, run_id in cases:
            with self.subTest(case=label):
                before = self.snapshot_tree()
                self.assert_error(
                    lambda value=run_id: self.start_run(value),
                    "invalid-run-id",
                )
                self.assertEqual(self.snapshot_tree(), before)

        self.assertFalse(os.path.lexists(self.root / "escape"))

    def test_rejects_a_preexisting_symlink_at_the_run_id(self):
        outside = self.root / "outside-run-id"
        outside.mkdir()
        run_namespace = self.output_root / ".skill-runs"
        run_namespace.mkdir()
        (run_namespace / "occupied-run").symlink_to(outside, target_is_directory=True)
        before = self.snapshot_tree()

        self.assert_error(
            lambda: self.start_run("occupied-run"),
            "run-collision",
        )

        self.assertEqual(self.snapshot_tree(), before)
        self.assertEqual(list(outside.iterdir()), [])

    def test_rejects_noncanonical_raw_and_reserved_output_paths(self):
        cases = (
            ("empty", ""),
            ("dot", "."),
            ("parent", ".."),
            ("leading-dot", "./report.md"),
            ("embedded-dot", "reports/./report.md"),
            ("traversal", "reports/../report.md"),
            ("empty-segment", "reports//report.md"),
            ("trailing-slash", "reports/report.md/"),
            ("absolute", "/tmp/report.md"),
            ("nul", "reports/nul\x00name"),
            ("backslash", "reports\\report.md"),
            ("drive-prefix", "C:/report.md"),
            ("reserved-root", ".skill-runs"),
            ("reserved-child", ".skill-runs/foreign/manifest.json"),
            ("reserved-uppercase", ".SKILL-RUNS"),
            ("reserved-mixed-case", ".Skill-Runs/foreign/manifest.json"),
        )

        for index, (label, relative_path) in enumerate(cases):
            with self.subTest(case=label):
                run = self.start_run(f"invalid-path-{index}")
                self.assert_error(
                    lambda path=relative_path: run.write(path, b"must not publish"),
                    "invalid-output-path",
                )

        published_files = [
            path
            for path in self.output_root.rglob("*")
            if path.is_file() and ".skill-runs" not in path.parts
        ]
        self.assertEqual(published_files, [])

    def test_rejects_symlinked_destination_parents_inside_or_outside_output(self):
        outside = self.root / "outside"
        outside.mkdir()
        real_inside = self.output_root / "real-inside"
        real_inside.mkdir()
        (self.output_root / "outside-link").symlink_to(outside, target_is_directory=True)
        (self.output_root / "inside-link").symlink_to(real_inside, target_is_directory=True)

        for index, relative_path in enumerate(("outside-link/report.md", "inside-link/report.md")):
            with self.subTest(path=relative_path):
                run = self.start_run(f"symlink-parent-{index}")
                self.assert_error(
                    lambda path=relative_path: run.write(path, b"must not follow a symlink"),
                    "invalid-output-path",
                )

        self.assertEqual(list(outside.iterdir()), [])
        self.assertEqual(list(real_inside.iterdir()), [])

    def test_rejects_a_symlinked_reserved_run_namespace(self):
        outside = self.root / "outside-runs"
        outside.mkdir()
        (self.output_root / ".skill-runs").symlink_to(outside, target_is_directory=True)

        self.assert_error(lambda: self.start_run("symlinked-runs"))

        self.assertEqual(list(outside.iterdir()), [])

    def test_root_path_rename_and_directory_replacement_cannot_redirect_a_started_run(self):
        run = self.start_run("stable-root-directory-run")
        opened_root = self.root / "opened-output"
        self.output_root.rename(opened_root)
        self.output_root.mkdir()

        run.write("reports/stable.md", b"bound to opened root\n")

        self.assertEqual(
            (opened_root / "reports" / "stable.md").read_bytes(),
            b"bound to opened root\n",
        )
        self.assertEqual(list(self.output_root.iterdir()), [])

    def test_root_path_rename_and_symlink_replacement_cannot_redirect_a_started_run(self):
        run = self.start_run("stable-root-symlink-run")
        opened_root = self.root / "opened-output"
        outside = self.root / "outside-replacement"
        outside.mkdir()
        self.output_root.rename(opened_root)
        self.output_root.symlink_to(outside, target_is_directory=True)

        run.write("reports/stable.md", b"bound to opened root\n")

        self.assertEqual(
            (opened_root / "reports" / "stable.md").read_bytes(),
            b"bound to opened root\n",
        )
        self.assertEqual(list(outside.iterdir()), [])

    def test_post_start_descendant_symlink_swap_is_rejected_without_writing_either_target(self):
        descendant = self.output_root / "reports"
        descendant.mkdir()
        run = self.start_run("descendant-swap-run")
        renamed_descendant = self.output_root / "renamed-reports"
        outside = self.root / "outside-descendant"
        outside.mkdir()
        descendant.rename(renamed_descendant)
        descendant.symlink_to(outside, target_is_directory=True)

        self.assert_error(
            lambda: run.write("reports/stable.md", b"must not follow replacement"),
            "invalid-output-path",
        )

        self.assertEqual(list(renamed_descendant.iterdir()), [])
        self.assertEqual(list(outside.iterdir()), [])

    def test_existing_output_collision_preserves_inode_bytes_and_metadata(self):
        destination = self.output_root / "reports" / "existing.md"
        destination.parent.mkdir()
        destination.write_bytes(b"prior durable bytes\n")
        destination.chmod(0o640)
        before = self.snapshot_path(destination)
        run = self.start_run("collision-run")

        self.assert_error(
            lambda: run.write("reports/existing.md", b"replacement bytes\n"),
            "output-collision",
        )

        self.assertEqual(self.snapshot_path(destination), before)

    def test_input_hard_link_alias_preserves_both_names_inode_bytes_and_metadata(self):
        source = self.record_root / "source.txt"
        source.chmod(0o640)
        alias = self.output_root / "reports" / "input-alias.txt"
        alias.parent.mkdir()
        os.link(source, alias)
        source_before = self.snapshot_path(source)
        alias_before = self.snapshot_path(alias)
        run = self.start_run("input-alias-run")

        self.assert_error(
            lambda: run.write("reports/input-alias.txt", b"replacement bytes\n"),
            "input-alias",
        )

        self.assertEqual(self.snapshot_path(source), source_before)
        self.assertEqual(self.snapshot_path(alias), alias_before)
        self.assertEqual(source.stat().st_ino, alias.stat().st_ino)

    def test_input_symlink_alias_is_classified_without_mutating_or_replacing_it(self):
        source = self.record_root / "source.txt"
        source.chmod(0o640)
        alias = self.output_root / "reports" / "input-alias.txt"
        alias.parent.mkdir()
        alias.symlink_to(source)
        source_before = self.snapshot_path(source)
        alias_before = alias.lstat()
        alias_target_before = os.readlink(alias)
        run = self.start_run("input-symlink-alias-run")

        self.assert_error(
            lambda: run.write("reports/input-alias.txt", b"replacement bytes\n"),
            "input-alias",
        )

        alias_after = alias.lstat()
        self.assertEqual(self.snapshot_path(source), source_before)
        self.assertEqual(os.readlink(alias), alias_target_before)
        self.assertEqual(alias_after.st_dev, alias_before.st_dev)
        self.assertEqual(alias_after.st_ino, alias_before.st_ino)
        self.assertEqual(alias_after.st_mode, alias_before.st_mode)
        self.assertEqual(alias_after.st_mtime_ns, alias_before.st_mtime_ns)

    def test_successful_write_preserves_both_declared_input_trees(self):
        record_before = self.snapshot_tree_at(self.record_root)
        authority_before = self.snapshot_tree_at(self.authority_root)
        run = self.start_run("input-preservation-run")

        run.write("reports/result.md", b"new output only\n")

        self.assertEqual(self.snapshot_tree_at(self.record_root), record_before)
        self.assertEqual(self.snapshot_tree_at(self.authority_root), authority_before)
        self.assertEqual(
            (self.output_root / "reports" / "result.md").read_bytes(),
            b"new output only\n",
        )

    def test_stream_failure_publishes_no_final_artifact_and_confines_staging(self):
        run_id = "stream-failure-run"
        run = self.start_run(run_id)
        before = self.snapshot_tree()

        self.assert_error(
            lambda: run.write("reports/partial.bin", FailingBinaryStream()),
            "stream-failed",
        )

        self.assert_failed_write_is_confined("reports/partial.bin", run_id, before)

    def test_caught_stream_failure_prevents_success_but_allows_failure_receipt(self):
        run_id = "caught-stream-failure-run"
        run = self.start_run(run_id)

        self.assert_error(
            lambda: run.write("reports/partial.bin", FailingBinaryStream()),
            "stream-failed",
        )

        self.assert_error(run.complete, "receipt-unavailable")
        self.assertFalse(os.path.lexists(self.run_directory(run_id) / "manifest.json"))
        self.assertTrue((self.run_directory(run_id) / "incomplete.json").is_file())

        failure = run.fail("stream-failed", "artifact-write")
        self.assertEqual(failure["status"], "failure")
        self.assertEqual(failure["artifacts"], [])
        self.assertEqual(failure["incomplete_artifacts"], [])
        self.assertTrue((self.run_directory(run_id) / "failure.json").is_file())

    def test_text_returning_stream_publishes_no_final_artifact(self):
        run_id = "text-stream-run"
        run = self.start_run(run_id)
        before = self.snapshot_tree()

        self.assert_error(
            lambda: run.write("reports/text-stream.bin", io.StringIO("not binary")),
            "stream-failed",
        )

        self.assert_failed_write_is_confined("reports/text-stream.bin", run_id, before)

    def test_staging_sync_failure_publishes_no_final_artifact_and_confines_staging(self):
        run_id = "sync-failure-run"
        run = self.start_run(run_id)
        before = self.snapshot_tree()

        with mock.patch.object(
            skill_output_writer.os,
            "fsync",
            side_effect=OSError("injected sync path /private/case-material"),
        ):
            self.assert_error(lambda: run.write("reports/unsynced.bin", b"unsynced bytes"))

        self.assert_failed_write_is_confined("reports/unsynced.bin", run_id, before)

    def test_publication_failure_publishes_no_final_artifact_and_confines_staging(self):
        run_id = "publication-failure-run"
        run = self.start_run(run_id)
        before = self.snapshot_tree()

        with mock.patch.object(
            skill_output_writer.os,
            "link",
            side_effect=OSError("injected publication path /private/case-material"),
        ):
            self.assert_error(lambda: run.write("reports/unpublished.bin", b"complete staged bytes"))

        self.assert_failed_write_is_confined("reports/unpublished.bin", run_id, before)

    def test_destination_sync_failure_preserves_linked_staging_and_incomplete_accounting(self):
        run_id = "destination-sync-run"
        (self.output_root / "reports").mkdir()
        run = self.start_run(run_id)
        original_fsync = os.fsync
        calls = 0

        def fail_destination_sync(descriptor):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected destination sync path /private/case-material")
            return original_fsync(descriptor)

        contents = b"linked but incompletely durable\n"
        expected = {
            "path": "reports/incomplete.bin",
            "sha256": hashlib.sha256(contents).hexdigest(),
            "size": len(contents),
        }
        with mock.patch.object(skill_output_writer.os, "fsync", side_effect=fail_destination_sync):
            self.assert_error(
                lambda: run.write(expected["path"], contents),
                "publication-incomplete",
            )

        final = self.output_root / expected["path"]
        staging = self.output_root / ".skill-runs" / run_id / "staging"
        staged_files = list(staging.iterdir())
        self.assertEqual(final.read_bytes(), contents)
        self.assertEqual(len(staged_files), 1)
        self.assertEqual(staged_files[0].read_bytes(), contents)
        self.assertEqual(staged_files[0].stat().st_ino, final.stat().st_ino)
        self.assertEqual(run._artifacts, [])
        self.assertEqual(
            run._incomplete_artifacts,
            [{**expected, "phase": "destination-sync"}],
        )

    def test_staging_unlink_failure_counts_durable_artifact_and_preserves_incomplete_evidence(self):
        run_id = "staging-unlink-run"
        (self.output_root / "reports").mkdir()
        run = self.start_run(run_id)
        contents = b"durable output with stale staging link\n"
        expected = {
            "path": "reports/durable.bin",
            "sha256": hashlib.sha256(contents).hexdigest(),
            "size": len(contents),
        }

        with mock.patch.object(
            skill_output_writer.os,
            "unlink",
            side_effect=OSError("injected unlink path /private/case-material"),
        ):
            self.assert_error(
                lambda: run.write(expected["path"], contents),
                "staging-incomplete",
            )

        final = self.output_root / expected["path"]
        staging = self.output_root / ".skill-runs" / run_id / "staging"
        staged_files = list(staging.iterdir())
        self.assertEqual(final.read_bytes(), contents)
        self.assertEqual(len(staged_files), 1)
        self.assertEqual(staged_files[0].read_bytes(), contents)
        self.assertEqual(staged_files[0].stat().st_ino, final.stat().st_ino)
        self.assertEqual(run._artifacts, [expected])
        self.assertEqual(
            run._incomplete_artifacts,
            [{**expected, "phase": "staging-cleanup"}],
        )

    def test_start_publishes_exact_incomplete_state_before_accepting_artifacts(self):
        run_id = "visible-incomplete-run"

        self.start_run(run_id)

        run_directory = self.run_directory(run_id)
        self.assertEqual(
            (run_directory / "incomplete.json").read_bytes(),
            b'{"run_id":"visible-incomplete-run","schema_version":1,"status":"incomplete"}',
        )
        self.assertFalse(os.path.lexists(run_directory / "manifest.json"))
        self.assertFalse(os.path.lexists(run_directory / "failure.json"))

    def test_complete_publishes_an_exact_canonical_success_receipt(self):
        run_id = "canonical-success-run"
        run = self.start_run(run_id)
        run.write("reports/z.md", b"zulu\n")
        run.write("reports/a.md", b"alpha\n")

        returned = run.complete()

        expected_bytes = (
            b'{"artifacts":[{"path":"reports/a.md","sha256":"b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060","size":6},'
            b'{"path":"reports/z.md","sha256":"4c8e0c0ec12989ff67bc82a6ea812393592d126d87294021b9a469bcbd286a41","size":5}],'
            b'"input_manifest_sha256":"7fcb5bb404fd81345d585c26eba719249559720fae28d4f95ec670dbebd45ddd",'
            b'"internet":{"policy":"disabled","used":false},"mode":"append-immutable","run_id":"canonical-success-run",'
            b'"schema_version":1,"skill":"synthetic-skill","skill_version":"1.4.0","status":"success"}'
        )
        receipt = self.run_directory(run_id) / "manifest.json"
        self.assertEqual(receipt.read_bytes(), expected_bytes)
        self.assertEqual(returned, json.loads(expected_bytes))
        self.assertFalse(os.path.lexists(self.run_directory(run_id) / "incomplete.json"))
        self.assertFalse(os.path.lexists(self.run_directory(run_id) / "failure.json"))

    def test_success_terminal_state_rejects_later_writes_and_transitions(self):
        run = self.start_run("success-terminal-run")
        run.write("reports/result.md", b"durable result\n")
        receipt = run.complete()
        before = self.snapshot_tree()

        operations = (
            ("write", lambda: run.write("reports/later.md", b"must not publish")),
            ("complete", run.complete),
            ("fail", lambda: run.fail("late-failure", "terminal-transition")),
        )
        for label, operation in operations:
            with self.subTest(operation=label):
                self.assert_error(operation, "run-terminal")

        self.assertEqual(self.snapshot_tree(), before)
        self.assertEqual(
            json.loads((self.run_directory("success-terminal-run") / "manifest.json").read_bytes()),
            receipt,
        )

    def test_fail_publishes_an_exact_bounded_failure_receipt_and_becomes_terminal(self):
        run_id = "failure-terminal-run"
        run = self.start_run(run_id)

        returned = run.fail("stream-failed", "artifact-write")

        expected_bytes = (
            b'{"artifacts":[],"failure":{"code":"stream-failed","phase":"artifact-write"},'
            b'"incomplete_artifacts":[],"input_manifest_sha256":"7fcb5bb404fd81345d585c26eba719249559720fae28d4f95ec670dbebd45ddd",'
            b'"internet":{"policy":"disabled","used":false},"mode":"append-immutable","run_id":"failure-terminal-run",'
            b'"schema_version":1,"skill":"synthetic-skill","skill_version":"1.4.0","status":"failure"}'
        )
        receipt = self.run_directory(run_id) / "failure.json"
        self.assertEqual(receipt.read_bytes(), expected_bytes)
        self.assertEqual(returned, json.loads(expected_bytes))
        self.assertFalse(os.path.lexists(self.run_directory(run_id) / "manifest.json"))
        before = self.snapshot_tree()
        operations = (
            ("write", lambda: run.write("reports/later.md", b"must not publish")),
            ("complete", run.complete),
            ("fail", lambda: run.fail("late-failure", "terminal-transition")),
        )
        for label, operation in operations:
            with self.subTest(operation=label):
                self.assert_error(operation, "run-terminal")
        self.assertEqual(self.snapshot_tree(), before)

    def test_interrupted_run_has_only_incomplete_state_and_never_success(self):
        run_id = "interrupted-run"

        run = self.start_run(run_id)
        run.write("reports/published-before-interruption.md", b"artifact without terminal receipt\n")
        del run

        run_directory = self.run_directory(run_id)
        self.assertTrue((run_directory / "incomplete.json").is_file())
        self.assertFalse(os.path.lexists(run_directory / "manifest.json"))
        self.assertFalse(os.path.lexists(run_directory / "failure.json"))
        self.assertEqual(
            (self.output_root / "reports" / "published-before-interruption.md").read_bytes(),
            b"artifact without terminal receipt\n",
        )

    def test_failed_run_retry_requires_a_new_run_id_and_new_artifact_path(self):
        failed_run = self.start_run("first-attempt-run")
        self.assert_error(
            lambda: failed_run.write("reports/missing.bin", FailingBinaryStream()),
            "stream-failed",
        )
        failed_run.fail("stream-failed", "artifact-write")

        self.assert_error(lambda: self.start_run("first-attempt-run"), "run-collision")

        retry = self.start_run("second-attempt-run")
        retry.write("reports/retry.bin", b"complete retry bytes\n")
        retry_manifest = retry.complete()
        self.assertFalse(os.path.lexists(self.output_root / "reports" / "missing.bin"))
        self.assertEqual(
            [artifact["path"] for artifact in retry_manifest["artifacts"]],
            ["reports/retry.bin"],
        )

    def test_equivalent_machine_roots_and_call_orders_have_identical_logical_receipts(self):
        first_run = self.start_run("equivalent-run")
        first_run.write("reports/z.md", b"zulu\n")
        first_run.write("reports/a.md", b"alpha\n")
        first_run.complete()
        first_receipt = (self.run_directory("equivalent-run") / "manifest.json").read_bytes()

        second_invocation, second_manifest, second_output = self.make_relocated_invocation("other-machine-root")
        reordered_manifest = {
            "inputs": [
                {
                    "files": [
                        {
                            "size": 16,
                            "sha256": "0197630d8ecf31b97fb61829e36f4043f943667c79feebc14c0ff65b086909ad",
                            "path": "source.txt",
                        }
                    ],
                    "role": "record",
                },
                {
                    "files": [
                        {
                            "size": 10,
                            "sha256": "17d31c37a2fd6589d7f6807e6e0743b6ab777440f416ab49880c0de1456d97e3",
                            "path": "cases.txt",
                        }
                    ],
                    "role": "authority",
                },
            ]
        }
        self.assertEqual(second_manifest, self.input_manifest)
        second_run = OutputRun.start(
            second_invocation,
            run_id="equivalent-run",
            skill_version="1.4.0",
            mode="append-immutable",
            input_manifest=reordered_manifest,
        )
        second_run.write("reports/a.md", b"alpha\n")
        second_run.write("reports/z.md", b"zulu\n")
        second_run.complete()
        second_receipt = (second_output / ".skill-runs" / "equivalent-run" / "manifest.json").read_bytes()

        self.assertEqual(first_receipt, second_receipt)
        parsed = json.loads(first_receipt)
        self.assertEqual(parsed["input_manifest_sha256"], INPUT_MANIFEST_SHA256)
        self.assertEqual(
            parsed["artifacts"],
            [
                {
                    "path": "reports/a.md",
                    "sha256": "b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060",
                    "size": 6,
                },
                {
                    "path": "reports/z.md",
                    "sha256": "4c8e0c0ec12989ff67bc82a6ea812393592d126d87294021b9a469bcbd286a41",
                    "size": 5,
                },
            ],
        )
        self.assertNotIn(str(self.root).encode("utf-8"), first_receipt)
        self.assertNotIn(str(second_output.parent).encode("utf-8"), second_receipt)

    def test_disabled_internet_rejects_source_records_before_publication(self):
        run = self.start_run("disabled-internet-run")

        self.assert_error(
            lambda: run.write(
                "reports/internet.md",
                b"must not publish",
                internet_sources=(self.valid_internet_source(),),
            ),
            "internet-not-authorized",
        )

        self.assertFalse(os.path.lexists(self.output_root / "reports" / "internet.md"))
        self.assertEqual(run._artifacts, [])

    def test_authorized_internet_records_complete_provenance_and_derives_used(self):
        invocation, input_manifest, output_root = self.make_relocated_invocation(
            "authorized-internet-root",
            internet="authorized",
        )
        run = OutputRun.start(
            invocation,
            run_id="authorized-internet-run",
            skill_version="1.4.0",
            mode="append-immutable",
            input_manifest=input_manifest,
        )
        supplied_url_source_without_context = self.valid_internet_source(
            retrieved_at="2026-08-24T12:34:56+00:00"
        )
        normalized_url_source_without_context = {
            **supplied_url_source_without_context,
            "retrieved_at": "2026-08-24T12:34:56Z",
        }
        identity_source_with_context = {
            "identity": "courtlistener:opinion:12345",
            "retrieved_at": "2026-08-24T13:45:00Z",
            "request_context": "q" * 1024,
            "sha256": "abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789",
        }

        run.write(
            "reports/web.md",
            b"web\n",
            internet_sources=(supplied_url_source_without_context, identity_source_with_context),
        )
        manifest = run.complete()

        expected_manifest = {
            "artifacts": [
                {
                    "path": "reports/web.md",
                    "sha256": "4ded89b3f9f03689b7032b92a091e742e1205e2a54277e52b32498d9fcdf3642",
                    "size": 4,
                    "internet_sources": [normalized_url_source_without_context, identity_source_with_context],
                }
            ],
            "input_manifest_sha256": INPUT_MANIFEST_SHA256,
            "internet": {"policy": "authorized", "used": True},
            "mode": "append-immutable",
            "run_id": "authorized-internet-run",
            "schema_version": 1,
            "skill": "synthetic-skill",
            "skill_version": "1.4.0",
            "status": "success",
        }
        receipt_bytes = (output_root / ".skill-runs" / "authorized-internet-run" / "manifest.json").read_bytes()
        self.assertEqual(manifest, expected_manifest)
        self.assertEqual(json.loads(receipt_bytes), expected_manifest)
        self.assertNotIn(str(output_root).encode("utf-8"), receipt_bytes)

    def test_write_result_is_recursively_detached_from_receipt_provenance(self):
        invocation, input_manifest, output_root = self.make_relocated_invocation(
            "detached-write-result-root",
            internet="authorized",
        )
        run = OutputRun.start(
            invocation,
            run_id="detached-write-result-run",
            skill_version="1.4.0",
            mode="append-immutable",
            input_manifest=input_manifest,
        )
        source = self.valid_internet_source()

        returned = run.write(
            "reports/web.md",
            b"web\n",
            internet_sources=(source,),
        )
        returned["internet_sources"][0]["url"] = "https://mutated.invalid/source"
        returned["internet_sources"].append(self.valid_internet_source(url="https://extra.invalid"))

        manifest = run.complete()
        self.assertEqual(manifest["internet"], {"policy": "authorized", "used": True})
        self.assertEqual(manifest["artifacts"][0]["internet_sources"], [source])
        persisted = json.loads(
            (output_root / ".skill-runs" / "detached-write-result-run" / "manifest.json").read_bytes()
        )
        self.assertEqual(persisted["artifacts"][0]["internet_sources"], [source])

    def test_authorized_internet_without_source_records_derives_unused(self):
        invocation, input_manifest, output_root = self.make_relocated_invocation(
            "authorized-unused-root",
            internet="authorized",
        )
        run = OutputRun.start(
            invocation,
            run_id="authorized-unused-run",
            skill_version="1.4.0",
            mode="append-immutable",
            input_manifest=input_manifest,
        )
        run.write("reports/local.md", b"local only\n")

        manifest = run.complete()

        self.assertEqual(manifest["internet"], {"policy": "authorized", "used": False})
        self.assertNotIn("internet_sources", manifest["artifacts"][0])
        self.assertTrue((output_root / "reports" / "local.md").is_file())

    def test_failed_run_retains_internet_sources_and_derives_used(self):
        invocation, input_manifest, output_root = self.make_relocated_invocation(
            "authorized-failure-root",
            internet="authorized",
        )
        run = OutputRun.start(
            invocation,
            run_id="authorized-failure-run",
            skill_version="1.4.0",
            mode="append-immutable",
            input_manifest=input_manifest,
        )
        supplied_source = self.valid_internet_source(
            retrieved_at="2026-08-24T12:34:56+00:00"
        )
        run.write(
            "reports/internet-before-failure.md",
            b"internet-derived bytes\n",
            internet_sources=(supplied_source,),
        )

        failure = run.fail("later-step-failed", "analysis")

        expected_failure = {
            "artifacts": [
                {
                    "path": "reports/internet-before-failure.md",
                    "sha256": "5ed47fb900159076164815501fdf68987c84affe6e6b6e11e91afecb44ebc7dd",
                    "size": 23,
                    "internet_sources": [
                        {
                            **supplied_source,
                            "retrieved_at": "2026-08-24T12:34:56Z",
                        }
                    ],
                }
            ],
            "failure": {"code": "later-step-failed", "phase": "analysis"},
            "incomplete_artifacts": [],
            "input_manifest_sha256": INPUT_MANIFEST_SHA256,
            "internet": {"policy": "authorized", "used": True},
            "mode": "append-immutable",
            "run_id": "authorized-failure-run",
            "schema_version": 1,
            "skill": "synthetic-skill",
            "skill_version": "1.4.0",
            "status": "failure",
        }
        failure_path = output_root / ".skill-runs" / "authorized-failure-run" / "failure.json"
        self.assertEqual(failure, expected_failure)
        self.assertEqual(json.loads(failure_path.read_bytes()), expected_failure)
        self.assertFalse(
            os.path.lexists(output_root / ".skill-runs" / "authorized-failure-run" / "manifest.json")
        )

    def test_authorized_internet_rejects_invalid_source_records_before_publication(self):
        invocation, input_manifest, output_root = self.make_relocated_invocation(
            "invalid-internet-root",
            internet="authorized",
        )
        run = OutputRun.start(
            invocation,
            run_id="invalid-internet-run",
            skill_version="1.4.0",
            mode="append-immutable",
            input_manifest=input_manifest,
        )
        valid = self.valid_internet_source()
        cases = (
            ("not-an-object", "https://example.test/source"),
            ("missing-identity", {key: value for key, value in valid.items() if key != "url"}),
            ("both-identities", {**valid, "identity": "source:123"}),
            ("empty-url", {**valid, "url": ""}),
            ("non-string-url", {**valid, "url": 7}),
            (
                "empty-identity",
                {**{key: value for key, value in valid.items() if key != "url"}, "identity": ""},
            ),
            (
                "non-string-identity",
                {**{key: value for key, value in valid.items() if key != "url"}, "identity": 7},
            ),
            ("missing-retrieval-time", {key: value for key, value in valid.items() if key != "retrieved_at"}),
            ("non-string-retrieval-time", {**valid, "retrieved_at": 7}),
            ("naive-retrieval-time", {**valid, "retrieved_at": "2026-08-24T12:34:56"}),
            ("nonzero-offset-retrieval-time", {**valid, "retrieved_at": "2026-08-24T12:34:56-05:00"}),
            ("invalid-retrieval-time", {**valid, "retrieved_at": "2026-02-30T12:34:56Z"}),
            ("week-date-retrieval-time", {**valid, "retrieved_at": "2026-W34-1T12:34:56Z"}),
            ("space-retrieval-time", {**valid, "retrieved_at": "2026-08-24 12:34:56Z"}),
            ("minute-only-retrieval-time", {**valid, "retrieved_at": "2026-08-24T12:34Z"}),
            ("missing-hash", {key: value for key, value in valid.items() if key != "sha256"}),
            ("non-string-hash", {**valid, "sha256": 7}),
            ("short-hash", {**valid, "sha256": "a" * 63}),
            ("long-hash", {**valid, "sha256": "a" * 65}),
            ("uppercase-hash", {**valid, "sha256": "A" * 64}),
            ("invalid-hash", {**valid, "sha256": "g" * 64}),
            ("empty-context", {**valid, "request_context": ""}),
            ("oversized-context", {**valid, "request_context": "q" * 1025}),
            ("non-string-context", {**valid, "request_context": 7}),
            ("unknown-field", {**valid, "case_excerpt": "forbidden case bytes"}),
        )

        for index, (label, source) in enumerate(cases):
            with self.subTest(case=label):
                relative_path = f"reports/invalid-source-{index}.md"
                self.assert_error(
                    lambda path=relative_path, record=source: run.write(
                        path,
                        b"must not publish",
                        internet_sources=(record,),
                    ),
                    "invalid-internet-source",
                )
                self.assertFalse(os.path.lexists(output_root / relative_path))

        self.assertEqual(run._artifacts, [])

    def test_failure_code_and_phase_accept_only_bounded_lower_kebab_values(self):
        valid_boundary = "a" * 64
        invalid_values = (
            None,
            "",
            "Uppercase",
            "under_score",
            "path/segment",
            "contains case excerpt",
            "a" * 65,
        )

        for index, value in enumerate(invalid_values):
            with self.subTest(field="code", value=value):
                run = self.start_run(f"invalid-code-{index}")
                self.assert_error(lambda candidate=value: run.fail(candidate, "artifact-write"), "invalid-failure")
                self.assertFalse(os.path.lexists(self.run_directory(f"invalid-code-{index}") / "failure.json"))
            with self.subTest(field="phase", value=value):
                run = self.start_run(f"invalid-phase-{index}")
                self.assert_error(lambda candidate=value: run.fail("stream-failed", candidate), "invalid-failure")
                self.assertFalse(os.path.lexists(self.run_directory(f"invalid-phase-{index}") / "failure.json"))

        boundary_run = self.start_run("failure-boundary-run")
        receipt = boundary_run.fail(valid_boundary, valid_boundary)
        self.assertEqual(receipt["failure"], {"code": valid_boundary, "phase": valid_boundary})

    def test_failure_receipt_excludes_raw_exception_paths_and_case_bytes(self):
        run_id = "bounded-failure-run"
        run = self.start_run(run_id)
        raw_failure = f"{self.root}/private/case.txt: forbidden case excerpt"

        self.assert_error(lambda: run.fail(raw_failure, "artifact-write"), "invalid-failure")
        returned = run.fail("stream-failed", "artifact-write")

        receipt = (self.run_directory(run_id) / "failure.json").read_bytes()
        self.assertEqual(returned["failure"], {"code": "stream-failed", "phase": "artifact-write"})
        self.assertNotIn(str(self.root).encode("utf-8"), receipt)
        self.assertNotIn(b"forbidden case excerpt", receipt)
        self.assertNotIn(b"Traceback", receipt)

    def test_terminal_receipts_are_create_exclusive_and_preserve_collisions(self):
        success_run = self.start_run("success-receipt-collision-run")
        manifest_path = self.run_directory("success-receipt-collision-run") / "manifest.json"
        manifest_path.write_bytes(b"prior immutable manifest\n")
        manifest_before = self.snapshot_path(manifest_path)

        self.assert_error(success_run.complete, "receipt-unavailable")
        self.assertEqual(self.snapshot_path(manifest_path), manifest_before)

        failure_run = self.start_run("failure-receipt-collision-run")
        failure_path = self.run_directory("failure-receipt-collision-run") / "failure.json"
        failure_path.write_bytes(b"prior immutable failure\n")
        failure_before = self.snapshot_path(failure_path)

        self.assert_error(
            lambda: failure_run.fail("stream-failed", "artifact-write"),
            "receipt-unavailable",
        )
        self.assertEqual(self.snapshot_path(failure_path), failure_before)

    def test_complete_uses_stable_run_directory_after_path_rename_and_replacement(self):
        run_id = "stable-success-receipt-run"
        run = self.start_run(run_id)
        original_run_directory = self.run_directory(run_id)
        opened_run_directory = original_run_directory.parent / "renamed-success-run"
        original_run_directory.rename(opened_run_directory)
        original_run_directory.mkdir()

        returned = run.complete()

        self.assertEqual(returned["status"], "success")
        self.assertTrue((opened_run_directory / "manifest.json").is_file())
        self.assertFalse(os.path.lexists(opened_run_directory / "incomplete.json"))
        self.assertEqual(list(original_run_directory.iterdir()), [])

    def test_fail_uses_stable_run_directory_after_path_rename_and_symlink_replacement(self):
        run_id = "stable-failure-receipt-run"
        run = self.start_run(run_id)
        original_run_directory = self.run_directory(run_id)
        opened_run_directory = original_run_directory.parent / "renamed-failure-run"
        outside = self.root / "outside-run-replacement"
        outside.mkdir()
        original_run_directory.rename(opened_run_directory)
        original_run_directory.symlink_to(outside, target_is_directory=True)

        returned = run.fail("stream-failed", "artifact-write")

        self.assertEqual(returned["status"], "failure")
        self.assertTrue((opened_run_directory / "failure.json").is_file())
        self.assertFalse(os.path.lexists(opened_run_directory / "manifest.json"))
        self.assertEqual(list(outside.iterdir()), [])

    def test_terminal_success_publication_and_sync_failures_never_report_success(self):
        publication_run_id = "receipt-publication-failure-run"
        publication_run = self.start_run(publication_run_id)
        with mock.patch.object(
            skill_output_writer.os,
            "link",
            side_effect=OSError("injected receipt publication /private/case-material"),
        ):
            self.assert_error(publication_run.complete, "receipt-unavailable")
        self.assertFalse(os.path.lexists(self.run_directory(publication_run_id) / "manifest.json"))
        self.assertTrue((self.run_directory(publication_run_id) / "incomplete.json").is_file())

        sync_run_id = "receipt-sync-failure-run"
        sync_run = self.start_run(sync_run_id)
        run_directory_metadata = self.run_directory(sync_run_id).stat()
        original_fsync = os.fsync

        def fail_terminal_directory_sync(descriptor):
            metadata = os.fstat(descriptor)
            if (metadata.st_dev, metadata.st_ino) == (
                run_directory_metadata.st_dev,
                run_directory_metadata.st_ino,
            ):
                raise OSError("injected receipt sync /private/case-material")
            return original_fsync(descriptor)

        with mock.patch.object(
            skill_output_writer.os,
            "fsync",
            side_effect=fail_terminal_directory_sync,
        ):
            self.assert_error(sync_run.complete, "receipt-unavailable")
        self.assertTrue((self.run_directory(sync_run_id) / "manifest.json").is_file())
        self.assertTrue((self.run_directory(sync_run_id) / "incomplete.json").is_file())
        self.assert_terminal_and_closed(sync_run)

        cleanup_run_id = "receipt-cleanup-failure-run"
        cleanup_run = self.start_run(cleanup_run_id)
        original_unlink = os.unlink

        def fail_incomplete_cleanup(path, *args, **kwargs):
            if os.fspath(path) == "incomplete.json":
                raise OSError("injected incomplete cleanup /private/case-material")
            return original_unlink(path, *args, **kwargs)

        with mock.patch.object(
            skill_output_writer.os,
            "unlink",
            side_effect=fail_incomplete_cleanup,
        ):
            self.assert_error(cleanup_run.complete, "receipt-unavailable")
        self.assertTrue((self.run_directory(cleanup_run_id) / "manifest.json").is_file())
        self.assertTrue((self.run_directory(cleanup_run_id) / "incomplete.json").is_file())
        self.assert_terminal_and_closed(cleanup_run)

        removed_cleanup_run_id = "receipt-removed-cleanup-failure-run"
        removed_cleanup_run = self.start_run(removed_cleanup_run_id)
        removed_cleanup_directory = self.run_directory(removed_cleanup_run_id)
        removed_cleanup_metadata = removed_cleanup_directory.stat()
        original_unlink = os.unlink
        original_fsync = os.fsync
        incomplete_unlink_failed = False
        recovery_sync_count = 0

        def remove_incomplete_then_report_unlink_error(path, *args, **kwargs):
            nonlocal incomplete_unlink_failed
            if os.fspath(path) == "incomplete.json":
                original_unlink(path, *args, **kwargs)
                incomplete_unlink_failed = True
                raise OSError("injected post-removal unlink error /private/case-material")
            return original_unlink(path, *args, **kwargs)

        def count_restored_incomplete_sync(descriptor):
            nonlocal recovery_sync_count
            metadata = os.fstat(descriptor)
            if (
                (metadata.st_dev, metadata.st_ino)
                == (removed_cleanup_metadata.st_dev, removed_cleanup_metadata.st_ino)
                and incomplete_unlink_failed
                and os.path.lexists(removed_cleanup_directory / "incomplete.json")
            ):
                recovery_sync_count += 1
            return original_fsync(descriptor)

        with mock.patch.object(
            skill_output_writer.os,
            "unlink",
            side_effect=remove_incomplete_then_report_unlink_error,
        ), mock.patch.object(
            skill_output_writer.os,
            "fsync",
            side_effect=count_restored_incomplete_sync,
        ):
            self.assert_error(removed_cleanup_run.complete, "receipt-unavailable")

        manifest_exists = os.path.lexists(removed_cleanup_directory / "manifest.json")
        incomplete_exists = os.path.lexists(removed_cleanup_directory / "incomplete.json")
        self.assertTrue(manifest_exists)
        self.assertTrue(incomplete_exists)
        self.assertFalse(manifest_exists and not incomplete_exists)
        self.assertGreaterEqual(recovery_sync_count, 1)
        self.assert_terminal_and_closed(removed_cleanup_run)

        removal_sync_run_id = "receipt-removal-sync-failure-run"
        removal_sync_run = self.start_run(removal_sync_run_id)
        removal_sync_run_directory = self.run_directory(removal_sync_run_id)
        removal_sync_run_metadata = removal_sync_run_directory.stat()
        injected_removal_sync_failure = False
        recovery_sync_count = 0

        def fail_sync_after_incomplete_removal(descriptor):
            nonlocal injected_removal_sync_failure, recovery_sync_count
            metadata = os.fstat(descriptor)
            is_run_directory = (metadata.st_dev, metadata.st_ino) == (
                removal_sync_run_metadata.st_dev,
                removal_sync_run_metadata.st_ino,
            )
            incomplete_is_absent = not os.path.lexists(removal_sync_run_directory / "incomplete.json")
            if is_run_directory and incomplete_is_absent and not injected_removal_sync_failure:
                injected_removal_sync_failure = True
                raise OSError("injected removal sync /private/case-material")
            if (
                is_run_directory
                and not incomplete_is_absent
                and injected_removal_sync_failure
                and recovery_sync_count == 0
            ):
                result = original_fsync(descriptor)
                recovery_sync_count += 1
                return result
            return original_fsync(descriptor)

        with mock.patch.object(
            skill_output_writer.os,
            "fsync",
            side_effect=fail_sync_after_incomplete_removal,
        ):
            self.assert_error(removal_sync_run.complete, "receipt-unavailable")
        self.assertTrue(injected_removal_sync_failure)
        self.assertEqual(recovery_sync_count, 1)
        self.assertTrue((removal_sync_run_directory / "manifest.json").is_file())
        self.assertEqual(
            (removal_sync_run_directory / "incomplete.json").read_bytes(),
            b'{"run_id":"receipt-removal-sync-failure-run","schema_version":1,"status":"incomplete"}',
        )
        self.assert_terminal_and_closed(removal_sync_run)

    def test_visible_failure_receipt_after_sync_failure_seals_and_closes_run(self):
        run_id = "failure-sync-sealed-run"
        run = self.start_run(run_id)
        run_directory = self.run_directory(run_id)
        run_identity = (run_directory.stat().st_dev, run_directory.stat().st_ino)
        original_fsync = os.fsync

        def fail_failure_directory_sync(descriptor):
            metadata = os.fstat(descriptor)
            if (
                (metadata.st_dev, metadata.st_ino) == run_identity
                and os.path.lexists(run_directory / "failure.json")
            ):
                raise OSError("injected failure receipt sync /private/case-material")
            return original_fsync(descriptor)

        with mock.patch.object(
            skill_output_writer.os,
            "fsync",
            side_effect=fail_failure_directory_sync,
        ):
            self.assert_error(
                lambda: run.fail("stream-failed", "artifact-write"),
                "receipt-unavailable",
            )

        self.assertTrue((run_directory / "failure.json").is_file())
        self.assertTrue((run_directory / "incomplete.json").is_file())
        self.assert_terminal_and_closed(run)

    def test_linked_terminal_receipt_removed_before_sync_failure_still_seals_run(self):
        for status in ("success", "failure"):
            with self.subTest(status=status):
                run_id = f"{status}-linked-receipt-removed-run"
                run = self.start_run(run_id)
                run_directory = self.run_directory(run_id)
                run_metadata = run_directory.stat()
                run_identity = (run_metadata.st_dev, run_metadata.st_ino)
                receipt_name = "manifest.json" if status == "success" else "failure.json"
                receipt_path = run_directory / receipt_name
                original_fsync = os.fsync
                removed_receipt = False

                def remove_receipt_then_fail_sync(descriptor):
                    nonlocal removed_receipt
                    metadata = os.fstat(descriptor)
                    if (
                        not removed_receipt
                        and (metadata.st_dev, metadata.st_ino) == run_identity
                        and os.path.lexists(receipt_path)
                    ):
                        receipt_path.unlink()
                        removed_receipt = True
                        raise OSError("injected post-link removal /private/case-material")
                    return original_fsync(descriptor)

                operation = (
                    run.complete
                    if status == "success"
                    else lambda: run.fail("stream-failed", "artifact-write")
                )
                with mock.patch.object(
                    skill_output_writer.os,
                    "fsync",
                    side_effect=remove_receipt_then_fail_sync,
                ):
                    self.assert_error(operation, "receipt-unavailable")

                self.assertTrue(removed_receipt)
                self.assertFalse(os.path.lexists(receipt_path))
                self.assertTrue((run_directory / "incomplete.json").is_file())
                self.assertTrue(run._terminal)
                self.assert_terminal_and_closed(run)

    def test_internet_use_includes_sources_on_incomplete_artifacts(self):
        invocation, input_manifest, output_root = self.make_relocated_invocation(
            "incomplete-internet-root",
            internet="authorized",
        )
        (output_root / "reports").mkdir()
        run = OutputRun.start(
            invocation,
            run_id="incomplete-internet-run",
            skill_version="1.4.0",
            mode="append-immutable",
            input_manifest=input_manifest,
        )
        original_fsync = os.fsync
        calls = 0

        def fail_destination_sync(descriptor):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected destination sync /private/case-material")
            return original_fsync(descriptor)

        with mock.patch.object(skill_output_writer.os, "fsync", side_effect=fail_destination_sync):
            self.assert_error(
                lambda: run.write(
                    "reports/incomplete-web.md",
                    b"internet bytes\n",
                    internet_sources=(self.valid_internet_source(),),
                ),
                "publication-incomplete",
            )

        failure = run.fail("publication-incomplete", "artifact-write")
        self.assertEqual(failure["internet"], {"policy": "authorized", "used": True})
        self.assertEqual(
            failure["incomplete_artifacts"][0]["internet_sources"],
            [self.valid_internet_source()],
        )

    def test_rejects_unsafe_skill_versions_before_run_state_mutation(self):
        cases = (
            ("non-string", None),
            ("empty", ""),
            ("oversized", "v" * 65),
            ("absolute-path", "/private/case-material"),
            ("windows-path", "C:\\private\\case-material"),
            ("case-excerpt", "forbidden case excerpt"),
            ("control", "1.4.0\nprivate-case"),
        )
        for index, (label, skill_version) in enumerate(cases):
            with self.subTest(case=label):
                before = self.snapshot_tree()
                self.assert_error(
                    lambda version=skill_version, suffix=index: OutputRun.start(
                        self.invocation,
                        run_id=f"invalid-skill-version-{suffix}",
                        skill_version=version,
                        mode="append-immutable",
                        input_manifest=self.input_manifest,
                    ),
                    "invalid-skill-version",
                )
                self.assertEqual(self.snapshot_tree(), before)

        run = OutputRun.start(
            self.invocation,
            run_id="valid-skill-version-run",
            skill_version="1.4.0+build-7",
            mode="append-immutable",
            input_manifest=self.input_manifest,
        )
        self.assertEqual(run.complete()["skill_version"], "1.4.0+build-7")

    def test_rejects_unsafe_or_non_http_source_urls_before_publication(self):
        invocation, input_manifest, output_root = self.make_relocated_invocation(
            "invalid-url-root",
            internet="authorized",
        )
        run = OutputRun.start(
            invocation,
            run_id="invalid-url-run",
            skill_version="1.4.0",
            mode="append-immutable",
            input_manifest=input_manifest,
        )
        cases = (
            ("relative", "example.test/source"),
            ("ftp", "ftp://example.test/source"),
            ("uppercase-http", "HTTP://example.test/source"),
            ("mixed-case-https", "Https://example.test/source"),
            ("missing-host", "https:///source"),
            ("credentials", "https://user:secret@example.test/source"),
            ("control", "https://example.test/source\nprivate-case"),
            ("backslash", "https://example.test\\outside"),
            ("oversized", f"https://example.test/{'a' * 2028}"),
        )
        for index, (label, url) in enumerate(cases):
            with self.subTest(case=label):
                relative_path = f"reports/invalid-url-{index}.md"
                self.assert_error(
                    lambda path=relative_path, value=url: run.write(
                        path,
                        b"must not publish",
                        internet_sources=(self.valid_internet_source(url=value),),
                    ),
                    "invalid-internet-source",
                )
                self.assertFalse(os.path.lexists(output_root / relative_path))
        self.assertEqual(run._artifacts, [])

    def test_existing_terminal_name_seals_on_prelink_receipt_failures(self):
        for status in ("success", "failure"):
            for failure_point in ("staging-create", "staging-write"):
                with self.subTest(status=status, failure_point=failure_point):
                    run_id = f"{status}-{failure_point}-terminal-run"
                    run = self.start_run(run_id)
                    receipt_name = "manifest.json" if status == "success" else "failure.json"
                    receipt_path = self.run_directory(run_id) / receipt_name
                    receipt_path.write_bytes(b"externally visible terminal receipt\n")
                    patch_target = (
                        "_new_staging_file" if failure_point == "staging-create" else "_write_all"
                    )
                    with mock.patch.object(
                        skill_output_writer,
                        patch_target,
                        side_effect=OutputError("receipt-unavailable"),
                    ):
                        operation = (
                            run.complete
                            if status == "success"
                            else lambda: run.fail("stream-failed", "artifact-write")
                        )
                        self.assert_error(operation, "receipt-unavailable")
                    self.assertEqual(receipt_path.read_bytes(), b"externally visible terminal receipt\n")
                    self.assert_terminal_and_closed(run)

    def test_prepublication_staging_cleanup_unlinks_are_directory_synced(self):
        stream_run = self.start_run("stream-cleanup-sync-run")
        stream_staging = self.run_directory("stream-cleanup-sync-run") / "staging"
        stream_staging_identity = (stream_staging.stat().st_dev, stream_staging.stat().st_ino)
        original_fsync = os.fsync
        stream_cleanup_syncs = 0

        def count_stream_cleanup_sync(descriptor):
            nonlocal stream_cleanup_syncs
            metadata = os.fstat(descriptor)
            if (metadata.st_dev, metadata.st_ino) == stream_staging_identity:
                stream_cleanup_syncs += 1
            return original_fsync(descriptor)

        with mock.patch.object(
            skill_output_writer.os,
            "fsync",
            side_effect=count_stream_cleanup_sync,
        ):
            self.assert_error(
                lambda: stream_run.write("reports/partial.bin", FailingBinaryStream()),
                "stream-failed",
            )
        self.assertEqual(stream_cleanup_syncs, 1)

    def test_receipt_prelink_cleanup_unlink_is_directory_synced(self):
        receipt_run = self.start_run("receipt-prelink-cleanup-sync-run")
        receipt_staging = self.run_directory("receipt-prelink-cleanup-sync-run") / "staging"
        receipt_staging_identity = (
            receipt_staging.stat().st_dev,
            receipt_staging.stat().st_ino,
        )
        receipt_cleanup_syncs = 0
        original_fsync = os.fsync

        def count_receipt_cleanup_sync(descriptor):
            nonlocal receipt_cleanup_syncs
            metadata = os.fstat(descriptor)
            if (metadata.st_dev, metadata.st_ino) == receipt_staging_identity:
                receipt_cleanup_syncs += 1
            return original_fsync(descriptor)

        with (
            mock.patch.object(
                skill_output_writer.os,
                "fsync",
                side_effect=count_receipt_cleanup_sync,
            ),
            mock.patch.object(
                skill_output_writer.os,
                "link",
                side_effect=OSError("injected prelink failure /private/case-material"),
            ),
        ):
            self.assert_error(receipt_run.complete, "receipt-unavailable")
        self.assertEqual(receipt_cleanup_syncs, 1)

    def test_cleanup_sync_failure_preserves_the_primary_bounded_failure(self):
        run = self.start_run("primary-failure-cleanup-sync-run")
        staging_path = self.run_directory("primary-failure-cleanup-sync-run") / "staging"
        staging_identity = (staging_path.stat().st_dev, staging_path.stat().st_ino)
        original_fsync = os.fsync
        cleanup_sync_attempted = False

        def fail_cleanup_sync(descriptor):
            nonlocal cleanup_sync_attempted
            metadata = os.fstat(descriptor)
            if (metadata.st_dev, metadata.st_ino) == staging_identity:
                cleanup_sync_attempted = True
                raise OSError("injected cleanup sync /private/case-material")
            return original_fsync(descriptor)

        with mock.patch.object(skill_output_writer.os, "fsync", side_effect=fail_cleanup_sync):
            self.assert_error(
                lambda: run.write("reports/partial.bin", FailingBinaryStream()),
                "stream-failed",
            )
        self.assertTrue(cleanup_sync_attempted)
        self.assertFalse(os.path.lexists(self.output_root / "reports" / "partial.bin"))

    def test_manifest_schema_declares_bounded_skill_versions_and_safe_urls(self):
        schema = json.loads(
            (Path(__file__).resolve().parents[2] / "governance" / "skill-run-manifest.schema.json").read_text()
        )
        self.assertEqual(schema["properties"]["skill_version"], {"$ref": "#/$defs/skillVersion"})
        self.assertEqual(schema["$defs"]["skillVersion"]["maxLength"], 64)
        self.assertEqual(
            schema["$defs"]["skillVersion"]["pattern"],
            "^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$",
        )
        url_schema = schema["$defs"]["internetSource"]["properties"]["url"]
        self.assertEqual(url_schema["format"], "uri")
        self.assertEqual(url_schema["maxLength"], 2048)
        self.assertIn("https?://", url_schema["pattern"])
        self.assertIn("@", url_schema["pattern"])

    def test_artifact_staging_unlink_is_synced_and_sync_failure_is_incomplete(self):
        successful_run = self.start_run("artifact-staging-sync-run")
        staging_path = self.run_directory("artifact-staging-sync-run") / "staging"
        staging_identity = (staging_path.stat().st_dev, staging_path.stat().st_ino)
        original_fsync = os.fsync
        staging_syncs = 0

        def count_staging_sync(descriptor):
            nonlocal staging_syncs
            metadata = os.fstat(descriptor)
            if (metadata.st_dev, metadata.st_ino) == staging_identity:
                staging_syncs += 1
            return original_fsync(descriptor)

        with mock.patch.object(skill_output_writer.os, "fsync", side_effect=count_staging_sync):
            successful_run.write("reports/synced-cleanup.md", b"durable bytes\n")
        self.assertEqual(staging_syncs, 1)

        failed_run = self.start_run("artifact-staging-sync-failure-run")
        failed_staging_path = self.run_directory("artifact-staging-sync-failure-run") / "staging"
        failed_staging_identity = (
            failed_staging_path.stat().st_dev,
            failed_staging_path.stat().st_ino,
        )

        def fail_staging_sync(descriptor):
            metadata = os.fstat(descriptor)
            if (metadata.st_dev, metadata.st_ino) == failed_staging_identity:
                raise OSError("injected staging directory sync /private/case-material")
            return original_fsync(descriptor)

        contents = b"durable output with uncertain staging cleanup\n"
        with mock.patch.object(skill_output_writer.os, "fsync", side_effect=fail_staging_sync):
            self.assert_error(
                lambda: failed_run.write("reports/staging-sync-failed.md", contents),
                "staging-incomplete",
            )
        self.assertEqual(
            failed_run._incomplete_artifacts,
            [
                {
                    "path": "reports/staging-sync-failed.md",
                    "phase": "staging-cleanup",
                    "sha256": hashlib.sha256(contents).hexdigest(),
                    "size": len(contents),
                }
            ],
        )

    def test_receipt_staging_unlink_sync_failure_is_sealed_and_incomplete(self):
        for status in ("success", "failure"):
            with self.subTest(status=status):
                run_id = f"{status}-receipt-staging-sync-run"
                run = self.start_run(run_id)
                run_directory = self.run_directory(run_id)
                staging_path = run_directory / "staging"
                staging_identity = (staging_path.stat().st_dev, staging_path.stat().st_ino)
                receipt_name = "manifest.json" if status == "success" else "failure.json"
                original_fsync = os.fsync

                def fail_receipt_staging_sync(descriptor):
                    metadata = os.fstat(descriptor)
                    if (
                        (metadata.st_dev, metadata.st_ino) == staging_identity
                        and os.path.lexists(run_directory / receipt_name)
                    ):
                        raise OSError("injected receipt staging sync /private/case-material")
                    return original_fsync(descriptor)

                with mock.patch.object(
                    skill_output_writer.os,
                    "fsync",
                    side_effect=fail_receipt_staging_sync,
                ):
                    operation = (
                        run.complete
                        if status == "success"
                        else lambda: run.fail("stream-failed", "artifact-write")
                    )
                    self.assert_error(operation, "receipt-unavailable")
                self.assertTrue((run_directory / receipt_name).is_file())
                self.assertTrue((run_directory / "incomplete.json").is_file())
                self.assert_terminal_and_closed(run)

    def test_terminal_runs_close_descriptors_under_stress(self):
        for index in range(80):
            run = self.start_run(f"fd-stress-{index}")
            descriptors = (run._root_fd, run._run_fd, run._staging_fd)
            if index % 2:
                run.fail("stress-failure", "terminal-transition")
            else:
                run.complete()
            self.assert_terminal_and_closed(run)
            for descriptor in descriptors:
                with self.assertRaises(OSError):
                    os.fstat(descriptor)

    def test_incomplete_artifacts_block_success_and_are_recorded_in_failure_receipts(self):
        destination_sync_run_id = "honest-destination-sync-run"
        (self.output_root / "destination-sync").mkdir()
        destination_sync_run = self.start_run(destination_sync_run_id)
        original_fsync = os.fsync
        calls = 0

        def fail_destination_sync(descriptor):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected destination sync /private/case-material")
            return original_fsync(descriptor)

        destination_bytes = b"linked not synced\n"
        with mock.patch.object(skill_output_writer.os, "fsync", side_effect=fail_destination_sync):
            self.assert_error(
                lambda: destination_sync_run.write("destination-sync/result.bin", destination_bytes),
                "publication-incomplete",
            )
        self.assert_error(destination_sync_run.complete, "receipt-unavailable")
        destination_failure = destination_sync_run.fail("publication-incomplete", "artifact-write")
        self.assertEqual(destination_failure["artifacts"], [])
        self.assertEqual(
            destination_failure["incomplete_artifacts"],
            [
                {
                    "path": "destination-sync/result.bin",
                    "sha256": "8b7dcfc43562caedc9ce045605ec437f1da26e92fa534ad4a45acbb4ebafb71c",
                    "size": 18,
                    "phase": "destination-sync",
                }
            ],
        )
        self.assertFalse(os.path.lexists(self.run_directory(destination_sync_run_id) / "manifest.json"))

        staging_run_id = "honest-staging-run"
        staging_run = self.start_run(staging_run_id)
        staging_bytes = b"durable but staging remains\n"
        with mock.patch.object(
            skill_output_writer.os,
            "unlink",
            side_effect=OSError("injected staging cleanup /private/case-material"),
        ):
            self.assert_error(
                lambda: staging_run.write("staging/result.bin", staging_bytes),
                "staging-incomplete",
            )
        self.assert_error(staging_run.complete, "receipt-unavailable")
        staging_failure = staging_run.fail("staging-incomplete", "artifact-write")
        durable_artifact = {
            "path": "staging/result.bin",
            "sha256": "8222a172347f40f5cab83b1ea3387422f682f96f79e99a8d31415b26c4a73676",
            "size": 28,
        }
        self.assertEqual(staging_failure["artifacts"], [durable_artifact])
        self.assertEqual(
            staging_failure["incomplete_artifacts"],
            [{**durable_artifact, "phase": "staging-cleanup"}],
        )
        self.assertFalse(os.path.lexists(self.run_directory(staging_run_id) / "manifest.json"))


if __name__ == "__main__":
    unittest.main()
