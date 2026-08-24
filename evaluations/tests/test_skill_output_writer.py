import hashlib
import io
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

    def assert_error(self, operation, code=None):
        with self.assertRaises(OutputError) as captured:
            operation()
        if code is not None:
            self.assertEqual(captured.exception.code, code)
            self.assertEqual(str(captured.exception), code)
        self.assertNotIn(str(self.root), str(captured.exception))
        self.assertNotIn("/private/case-material", str(captured.exception))
        return captured.exception

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


if __name__ == "__main__":
    unittest.main()
