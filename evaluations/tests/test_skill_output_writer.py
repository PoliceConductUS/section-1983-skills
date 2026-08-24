import hashlib
import io
import os
import stat
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

    def snapshot_tree(self):
        entries = {}
        for path in self.output_root.rglob("*"):
            metadata = path.lstat()
            entries[path.relative_to(self.output_root).as_posix()] = metadata.st_mode
        return entries

    def assert_failed_write_is_confined(self, relative_path, run_id, before):
        self.assertFalse((self.output_root / relative_path).exists())
        after = self.snapshot_tree()
        staging = Path(".skill-runs") / run_id / "staging"
        for relative, mode in after.items():
            if relative in before or not stat.S_ISREG(mode):
                continue
            self.assertTrue(
                Path(relative).is_relative_to(staging),
                f"new failure artifact escaped staging: {relative}",
            )

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


if __name__ == "__main__":
    unittest.main()
