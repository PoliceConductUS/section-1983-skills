"""Invocation-bound, create-exclusive publication for skill output artifacts."""

from __future__ import annotations

import errno
import hashlib
import json
import os
import re
import secrets
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, BinaryIO
from urllib.parse import urlsplit

from scripts.validate_folder_invocation import ValidatedInvocation


_RUN_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_SKILL_VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$")
_FAILURE_VALUE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_MODES = frozenset({"append-immutable", "fresh-regenerable"})
_DIRECTORY_FLAGS = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
_STAGING_CHUNK_SIZE = 1024 * 1024
_INCOMPLETE_NAME = "incomplete.json"
_MANIFEST_NAME = "manifest.json"
_FAILURE_NAME = "failure.json"


class OutputError(RuntimeError):
    """A bounded output-persistence failure."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _fail(code: str) -> None:
    raise OutputError(code)


def _valid_run_id(value: Any) -> bool:
    return isinstance(value, str) and _RUN_ID.fullmatch(value) is not None


def _canonical_json(value: Any, error_code: str) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError):
        _fail(error_code)


def _write_all(descriptor: int, contents: bytes, error_code: str) -> None:
    offset = 0
    try:
        while offset < len(contents):
            written = os.write(descriptor, contents[offset:])
            if written <= 0:
                _fail(error_code)
            offset += written
        os.fsync(descriptor)
    except OutputError:
        raise
    except OSError:
        _fail(error_code)


def _new_staging_file(staging_fd: int, prefix: str, error_code: str) -> tuple[str, int]:
    for _ in range(32):
        name = f"{prefix}-{secrets.token_hex(16)}.tmp"
        try:
            descriptor = os.open(
                name,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                0o600,
                dir_fd=staging_fd,
            )
            return name, descriptor
        except FileExistsError:
            continue
        except OSError:
            _fail(error_code)
    _fail(error_code)


def _entry_exists(directory_fd: int, name: str) -> bool:
    try:
        os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    except FileNotFoundError:
        return False
    except OSError:
        return True
    return True


def _unlink_and_sync(directory_fd: int, name: str, error_code: str) -> None:
    try:
        os.unlink(name, dir_fd=directory_fd)
        os.fsync(directory_fd)
    except OSError:
        _fail(error_code)


def _publish_record(
    staging_fd: int,
    run_fd: int,
    name: str,
    contents: bytes,
    *,
    on_visible=None,
) -> None:
    staging_name = None
    descriptor = -1
    linked = False
    try:
        staging_name, descriptor = _new_staging_file(staging_fd, "receipt", "receipt-unavailable")
        try:
            _write_all(descriptor, contents, "receipt-unavailable")
        finally:
            try:
                os.close(descriptor)
            except OSError:
                pass
            descriptor = -1
        try:
            os.link(
                staging_name,
                name,
                src_dir_fd=staging_fd,
                dst_dir_fd=run_fd,
                follow_symlinks=False,
            )
            linked = True
            os.fsync(run_fd)
            _unlink_and_sync(staging_fd, staging_name, "receipt-unavailable")
        except OutputError:
            raise
        except (OSError, TypeError):
            _fail("receipt-unavailable")
    finally:
        if descriptor >= 0:
            try:
                os.close(descriptor)
            except OSError:
                pass
        if staging_name is not None and not linked:
            try:
                _unlink_and_sync(staging_fd, staging_name, "receipt-unavailable")
            except OutputError:
                pass
        if on_visible is not None and _entry_exists(run_fd, name):
            on_visible()


def _restore_incomplete(run_fd: int, contents: bytes) -> None:
    descriptor = -1
    try:
        try:
            descriptor = os.open(
                _INCOMPLETE_NAME,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                0o600,
                dir_fd=run_fd,
            )
            _write_all(descriptor, contents, "receipt-unavailable")
        except FileExistsError:
            pass
        finally:
            if descriptor >= 0:
                try:
                    os.close(descriptor)
                except OSError:
                    pass
        os.fsync(run_fd)
    except (OSError, OutputError):
        _fail("receipt-unavailable")


def _normalize_internet_sources(value: Any) -> tuple[dict[str, Any], ...]:
    try:
        sources = tuple(value)
    except (TypeError, ValueError):
        _fail("invalid-internet-source")

    normalized: list[dict[str, Any]] = []
    for source in sources:
        if type(source) is not dict:
            _fail("invalid-internet-source")
        identity_fields = {field for field in ("url", "identity") if field in source}
        allowed_fields = {"url", "identity", "retrieved_at", "request_context", "sha256"}
        required_fields = identity_fields | {"retrieved_at", "sha256"}
        if (
            len(identity_fields) != 1
            or set(source) != required_fields | ({"request_context"} if "request_context" in source else set())
            or not set(source).issubset(allowed_fields)
        ):
            _fail("invalid-internet-source")

        identity_field = next(iter(identity_fields))
        identity = source[identity_field]
        retrieved_at = source["retrieved_at"]
        sha256 = source["sha256"]
        if not isinstance(identity, str) or not identity:
            _fail("invalid-internet-source")
        if identity_field == "url":
            if (
                len(identity) > 2048
                or not identity.startswith(("http://", "https://"))
                or "\\" in identity
                or any(ord(character) < 33 or ord(character) > 126 for character in identity)
            ):
                _fail("invalid-internet-source")
            try:
                parsed_url = urlsplit(identity)
                invalid_url = (
                    parsed_url.scheme not in {"http", "https"}
                    or not parsed_url.netloc
                    or not parsed_url.hostname
                    or parsed_url.username is not None
                    or parsed_url.password is not None
                )
                parsed_url.port
            except (TypeError, ValueError):
                _fail("invalid-internet-source")
            if invalid_url:
                _fail("invalid-internet-source")
        if not isinstance(retrieved_at, str) or not (
            retrieved_at.endswith("Z") or retrieved_at.endswith("+00:00")
        ):
            _fail("invalid-internet-source")
        try:
            parsed_time = datetime.fromisoformat(retrieved_at.replace("Z", "+00:00"))
        except ValueError:
            _fail("invalid-internet-source")
        if parsed_time.utcoffset() != timezone.utc.utcoffset(None):
            _fail("invalid-internet-source")
        if not isinstance(sha256, str) or _SHA256.fullmatch(sha256) is None:
            _fail("invalid-internet-source")

        normalized_source = dict(source)
        if retrieved_at.endswith("+00:00"):
            normalized_source["retrieved_at"] = f"{retrieved_at[:-6]}Z"
        if "request_context" in source:
            context = source["request_context"]
            if not isinstance(context, str) or not context or len(context) > 1024:
                _fail("invalid-internet-source")
        normalized.append(normalized_source)
    return tuple(normalized)


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
        run_fd: int,
        staging_fd: int,
        run_id: str,
        skill_version: str,
        mode: str,
        input_manifest: Any,
        input_manifest_sha256: str,
        incomplete_bytes: bytes,
        input_identities: frozenset[tuple[int, int]],
    ):
        self.invocation = invocation
        self.run_id = run_id
        self.skill_version = skill_version
        self.mode = mode
        self.input_manifest = input_manifest
        self._root_fd = root_fd
        self._run_fd = run_fd
        self._staging_fd = staging_fd
        self._input_manifest_sha256 = input_manifest_sha256
        self._incomplete_bytes = incomplete_bytes
        self._input_identities = input_identities
        self._artifacts: list[dict[str, Any]] = []
        self._incomplete_artifacts: list[dict[str, Any]] = []
        self._terminal = False

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
        if not isinstance(skill_version, str) or _SKILL_VERSION.fullmatch(skill_version) is None:
            _fail("invalid-skill-version")

        input_manifest_bytes = _canonical_json(input_manifest, "invalid-input-manifest")
        input_manifest_sha256 = hashlib.sha256(input_manifest_bytes).hexdigest()
        incomplete_bytes = _canonical_json(
            {"run_id": run_id, "schema_version": 1, "status": "incomplete"},
            "receipt-unavailable",
        )

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
            _publish_record(staging_fd, run_fd, _INCOMPLETE_NAME, incomplete_bytes)
            result = cls(
                invocation,
                root_fd=root_fd,
                run_fd=run_fd,
                staging_fd=staging_fd,
                run_id=run_id,
                skill_version=skill_version,
                mode=mode,
                input_manifest=input_manifest,
                input_manifest_sha256=input_manifest_sha256,
                incomplete_bytes=incomplete_bytes,
                input_identities=input_identities,
            )
            root_fd = -1
            run_fd = -1
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
        return _new_staging_file(self._staging_fd, "artifact", "staging-unavailable")

    def write(self, relative_path: str, contents_or_stream: Any, *, internet_sources=()):
        if self._terminal:
            _fail("run-terminal")
        parts = _relative_parts(relative_path)
        normalized_sources = _normalize_internet_sources(internet_sources)
        if normalized_sources and self.invocation.internet == "disabled":
            _fail("internet-not-authorized")
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
            if normalized_sources:
                artifact["internet_sources"] = list(normalized_sources)
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
                _unlink_and_sync(self._staging_fd, staging_name, "staging-incomplete")
                staged = False
            except OutputError:
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
                    _unlink_and_sync(self._staging_fd, staging_name, "staging-incomplete")
                except OutputError:
                    pass
            if parent_fd is not None:
                try:
                    os.close(parent_fd)
                except OSError:
                    pass

    def _internet_status(self) -> dict[str, Any]:
        used = any(
            artifact.get("internet_sources")
            for artifact in (*self._artifacts, *self._incomplete_artifacts)
        )
        return {"policy": self.invocation.internet, "used": used}

    def _seal(self) -> None:
        self._terminal = True

    def _close_descriptors(self) -> None:
        for descriptor_name in ("_staging_fd", "_run_fd", "_root_fd"):
            descriptor = getattr(self, descriptor_name, -1)
            if descriptor >= 0:
                try:
                    os.close(descriptor)
                except OSError:
                    pass
                setattr(self, descriptor_name, -1)

    def _receipt(self, status: str) -> dict[str, Any]:
        return {
            "artifacts": sorted(self._artifacts, key=lambda artifact: artifact["path"]),
            "input_manifest_sha256": self._input_manifest_sha256,
            "internet": self._internet_status(),
            "mode": self.mode,
            "run_id": self.run_id,
            "schema_version": 1,
            "skill": self.invocation.skill,
            "skill_version": self.skill_version,
            "status": status,
        }

    def complete(self) -> dict[str, Any]:
        if self._terminal:
            _fail("run-terminal")
        if self._incomplete_artifacts:
            _fail("receipt-unavailable")

        receipt = self._receipt("success")
        receipt_bytes = _canonical_json(receipt, "receipt-unavailable")
        try:
            _publish_record(
                self._staging_fd,
                self._run_fd,
                _MANIFEST_NAME,
                receipt_bytes,
                on_visible=self._seal,
            )
            try:
                os.unlink(_INCOMPLETE_NAME, dir_fd=self._run_fd)
            except OSError:
                _fail("receipt-unavailable")
            try:
                os.fsync(self._run_fd)
            except OSError:
                _restore_incomplete(self._run_fd, self._incomplete_bytes)
                _fail("receipt-unavailable")
        except BaseException:
            if self._terminal:
                self._close_descriptors()
            raise

        self._close_descriptors()
        return receipt

    def fail(self, code: str, phase: str) -> dict[str, Any]:
        if self._terminal:
            _fail("run-terminal")
        if (
            not isinstance(code, str)
            or len(code) > 64
            or _FAILURE_VALUE.fullmatch(code) is None
            or not isinstance(phase, str)
            or len(phase) > 64
            or _FAILURE_VALUE.fullmatch(phase) is None
        ):
            _fail("invalid-failure")

        receipt = self._receipt("failure")
        receipt["failure"] = {"code": code, "phase": phase}
        receipt["incomplete_artifacts"] = sorted(
            self._incomplete_artifacts,
            key=lambda artifact: (artifact["path"], artifact["phase"]),
        )
        receipt_bytes = _canonical_json(receipt, "receipt-unavailable")
        try:
            _publish_record(
                self._staging_fd,
                self._run_fd,
                _FAILURE_NAME,
                receipt_bytes,
                on_visible=self._seal,
            )
        except BaseException:
            if self._terminal:
                self._close_descriptors()
            raise
        self._close_descriptors()
        return receipt

    def __del__(self):
        self._close_descriptors()
