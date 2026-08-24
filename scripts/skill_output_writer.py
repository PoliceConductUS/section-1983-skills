"""Invocation-bound, create-exclusive publication for skill output artifacts."""

from __future__ import annotations

import errno
import hashlib
import os
import re
import secrets
import stat
from pathlib import Path
from typing import Any, BinaryIO

from scripts.validate_folder_invocation import ValidatedInvocation


_RUN_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_MODES = frozenset({"append-immutable", "fresh-regenerable"})
_DIRECTORY_FLAGS = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
_STAGING_CHUNK_SIZE = 1024 * 1024


class OutputError(RuntimeError):
    """A bounded output-persistence failure."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _fail(code: str) -> None:
    raise OutputError(code)


def _valid_run_id(value: Any) -> bool:
    return isinstance(value, str) and _RUN_ID.fullmatch(value) is not None


def _relative_parts(value: Any) -> tuple[str, ...]:
    if not isinstance(value, str) or not value:
        _fail("invalid-output-path")
    parts = value.split("/")
    if (
        "\\" in value
        or "\x00" in value
        or re.match(r"^[A-Za-z]:/", value) is not None
        or any(part in {"", ".", ".."} for part in parts)
        or parts[0].casefold() == ".skill-runs"
    ):
        _fail("invalid-output-path")
    return tuple(parts)


def _open_directory(parent_fd: int, name: str, *, create: bool, error_code: str) -> int:
    try:
        return os.open(name, _DIRECTORY_FLAGS, dir_fd=parent_fd)
    except FileNotFoundError:
        if not create:
            _fail(error_code)
    except OSError:
        _fail(error_code)

    try:
        os.mkdir(name, mode=0o700, dir_fd=parent_fd)
    except FileExistsError:
        pass
    except OSError:
        _fail(error_code)

    directory_fd = -1
    try:
        directory_fd = os.open(name, _DIRECTORY_FLAGS, dir_fd=parent_fd)
        os.fsync(parent_fd)
        return directory_fd
    except OSError:
        if directory_fd >= 0:
            try:
                os.close(directory_fd)
            except OSError:
                pass
        _fail(error_code)


def _input_file_identities(invocation: ValidatedInvocation) -> frozenset[tuple[int, int]]:
    identities: set[tuple[int, int]] = set()

    def walk(directory: Path, root: Path, active: set[tuple[int, int]]) -> None:
        try:
            directory_stat = directory.stat()
            directory_identity = (directory_stat.st_dev, directory_stat.st_ino)
            if directory_identity in active:
                return
            active.add(directory_identity)
            entries = list(os.scandir(directory))
        except OSError:
            _fail("input-index-unavailable")

        try:
            for entry in entries:
                candidate = Path(entry.path)
                try:
                    resolved = candidate.resolve(strict=True)
                    resolved.relative_to(root)
                    metadata = entry.stat(follow_symlinks=True)
                except (OSError, ValueError):
                    _fail("input-index-unavailable")
                if stat.S_ISDIR(metadata.st_mode):
                    walk(resolved, root, active)
                elif stat.S_ISREG(metadata.st_mode):
                    identities.add((metadata.st_dev, metadata.st_ino))
        finally:
            active.remove(directory_identity)

    try:
        for _, root in invocation.inputs:
            walk(root, root, set())
    except RecursionError:
        _fail("input-index-unavailable")
    return frozenset(identities)


def _existing_destination_error(parent_fd: int, leaf: str, input_identities: frozenset[tuple[int, int]]) -> None:
    try:
        metadata = os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return
    except OSError:
        _fail("invalid-output-path")
    if stat.S_ISREG(metadata.st_mode) and (metadata.st_dev, metadata.st_ino) in input_identities:
        _fail("input-alias")
    if stat.S_ISLNK(metadata.st_mode):
        try:
            target_metadata = os.stat(leaf, dir_fd=parent_fd, follow_symlinks=True)
        except OSError:
            _fail("output-collision")
        if stat.S_ISREG(target_metadata.st_mode) and (
            target_metadata.st_dev,
            target_metadata.st_ino,
        ) in input_identities:
            _fail("input-alias")
    _fail("output-collision")


def _write_chunk(destination: BinaryIO, digest: Any, chunk: bytes) -> int:
    destination.write(chunk)
    digest.update(chunk)
    return len(chunk)


def _stage_contents(destination: BinaryIO, contents_or_stream: Any) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    try:
        if isinstance(contents_or_stream, str):
            data = contents_or_stream.encode("utf-8")
            size = _write_chunk(destination, digest, data)
        elif isinstance(contents_or_stream, (bytes, bytearray, memoryview)):
            data = bytes(contents_or_stream)
            size = _write_chunk(destination, digest, data)
        elif callable(getattr(contents_or_stream, "read", None)):
            while True:
                chunk = contents_or_stream.read(_STAGING_CHUNK_SIZE)
                if not isinstance(chunk, bytes):
                    _fail("stream-failed")
                if not chunk:
                    break
                size += _write_chunk(destination, digest, chunk)
        else:
            _fail("stream-failed")
    except OutputError:
        raise
    except Exception:
        _fail("stream-failed")
    return digest.hexdigest(), size


class OutputRun:
    """One output run bound to a stable validated output-root directory."""

    def __init__(
        self,
        invocation: ValidatedInvocation,
        *,
        root_fd: int,
        staging_fd: int,
        run_id: str,
        skill_version: str,
        mode: str,
        input_manifest: Any,
        input_identities: frozenset[tuple[int, int]],
    ):
        self.invocation = invocation
        self.run_id = run_id
        self.skill_version = skill_version
        self.mode = mode
        self.input_manifest = input_manifest
        self._root_fd = root_fd
        self._staging_fd = staging_fd
        self._input_identities = input_identities
        self._artifacts: list[dict[str, Any]] = []
        self._incomplete_artifacts: list[dict[str, Any]] = []

    @classmethod
    def start(
        cls,
        invocation: ValidatedInvocation,
        *,
        run_id: str,
        skill_version: str,
        mode: str,
        input_manifest: Any,
    ) -> "OutputRun":
        if not _valid_run_id(run_id):
            _fail("invalid-run-id")
        if not isinstance(mode, str) or mode not in _MODES:
            _fail("invalid-run-mode")

        try:
            root_fd = os.open(invocation.output_root, _DIRECTORY_FLAGS)
        except (OSError, TypeError, AttributeError):
            _fail("output-unavailable")

        runs_fd = None
        run_fd = None
        staging_fd = None
        try:
            if mode == "fresh-regenerable":
                try:
                    if os.listdir(root_fd):
                        _fail("output-not-fresh")
                except OutputError:
                    raise
                except OSError:
                    _fail("output-unavailable")

            input_identities = _input_file_identities(invocation)
            runs_fd = _open_directory(root_fd, ".skill-runs", create=True, error_code="run-collision")
            try:
                os.mkdir(run_id, mode=0o700, dir_fd=runs_fd)
                os.fsync(runs_fd)
            except OSError as error:
                if error.errno in {errno.EEXIST, errno.ELOOP, errno.ENOTDIR}:
                    _fail("run-collision")
                _fail("run-unavailable")
            run_fd = _open_directory(runs_fd, run_id, create=False, error_code="run-unavailable")
            staging_fd = _open_directory(run_fd, "staging", create=True, error_code="run-unavailable")
            result = cls(
                invocation,
                root_fd=root_fd,
                staging_fd=staging_fd,
                run_id=run_id,
                skill_version=skill_version,
                mode=mode,
                input_manifest=input_manifest,
                input_identities=input_identities,
            )
            root_fd = -1
            staging_fd = -1
            return result
        finally:
            for descriptor in (staging_fd, run_fd, runs_fd, root_fd):
                if descriptor is not None and descriptor >= 0:
                    try:
                        os.close(descriptor)
                    except OSError:
                        pass

    def _destination_parent(self, parts: tuple[str, ...]) -> int:
        descriptor = os.dup(self._root_fd)
        try:
            for part in parts[:-1]:
                next_descriptor = _open_directory(
                    descriptor,
                    part,
                    create=True,
                    error_code="invalid-output-path",
                )
                os.close(descriptor)
                descriptor = next_descriptor
            return descriptor
        except BaseException:
            try:
                os.close(descriptor)
            except OSError:
                pass
            raise

    def _new_staging_name(self) -> tuple[str, int]:
        for _ in range(32):
            name = f"artifact-{secrets.token_hex(16)}.tmp"
            try:
                descriptor = os.open(
                    name,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                    0o600,
                    dir_fd=self._staging_fd,
                )
                return name, descriptor
            except FileExistsError:
                continue
            except OSError:
                _fail("staging-unavailable")
        _fail("staging-unavailable")

    def write(self, relative_path: str, contents_or_stream: Any, *, internet_sources=()):
        parts = _relative_parts(relative_path)
        staging_name, staging_file_fd = self._new_staging_name()
        staged = True
        linked = False
        parent_fd = None
        try:
            try:
                with os.fdopen(staging_file_fd, "wb", closefd=True) as staging_file:
                    sha256, size = _stage_contents(staging_file, contents_or_stream)
                    staging_file.flush()
                    os.fsync(staging_file.fileno())
                staging_file_fd = -1
            except OutputError:
                raise
            except (OSError, ValueError, TypeError):
                _fail("stream-failed")

            parent_fd = self._destination_parent(parts)
            _existing_destination_error(parent_fd, parts[-1], self._input_identities)
            artifact = {"path": relative_path, "sha256": sha256, "size": size}
            try:
                os.link(
                    staging_name,
                    parts[-1],
                    src_dir_fd=self._staging_fd,
                    dst_dir_fd=parent_fd,
                    follow_symlinks=False,
                )
            except FileExistsError:
                _existing_destination_error(parent_fd, parts[-1], self._input_identities)
                _fail("output-collision")
            except (OSError, TypeError):
                _fail("publication-failed")
            linked = True
            try:
                os.fsync(parent_fd)
            except OSError:
                self._incomplete_artifacts.append({**artifact, "phase": "destination-sync"})
                _fail("publication-incomplete")
            self._artifacts.append(artifact)
            try:
                os.unlink(staging_name, dir_fd=self._staging_fd)
                staged = False
            except OSError:
                self._incomplete_artifacts.append({**artifact, "phase": "staging-cleanup"})
                _fail("staging-incomplete")

            return dict(artifact)
        finally:
            if staging_file_fd >= 0:
                try:
                    os.close(staging_file_fd)
                except OSError:
                    pass
            if staged and not linked:
                try:
                    os.unlink(staging_name, dir_fd=self._staging_fd)
                except OSError:
                    pass
            if parent_fd is not None:
                try:
                    os.close(parent_fd)
                except OSError:
                    pass

    def __del__(self):
        for descriptor_name in ("_staging_fd", "_root_fd"):
            descriptor = getattr(self, descriptor_name, -1)
            if descriptor >= 0:
                try:
                    os.close(descriptor)
                except OSError:
                    pass
                setattr(self, descriptor_name, -1)
