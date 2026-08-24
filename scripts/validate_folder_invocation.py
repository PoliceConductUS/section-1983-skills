"""Read-only conformance helpers for the folder-scoped invocation contract."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


_IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_ENVELOPE_FIELDS = frozenset(
    {"version", "skill", "inputs", "output", "runtime", "internet", "isolation", "target"}
)


class InvocationError(ValueError):
    """A bounded, stable conformance failure."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class ValidatedInvocation:
    skill: str
    inputs: tuple[tuple[str, Path], ...]
    output_root: Path
    runtime: dict[str, int]
    internet: str
    target: tuple[str, Path] | None


def _fail(code: str) -> None:
    raise InvocationError(code)


def _is_identifier(value: Any) -> bool:
    return isinstance(value, str) and _IDENTIFIER.fullmatch(value) is not None


def _require_exact_object(value: Any, required: set[str], allowed: set[str], code: str) -> dict[str, Any]:
    if type(value) is not dict or set(value) != required or not set(value).issubset(allowed):
        _fail(code)
    return value


def _require_relative_path(value: Any, code: str) -> Path:
    if not isinstance(value, str) or not value:
        _fail(code)
    segments = value.split("/")
    if (
        "\\" in value
        or "\x00" in value
        or re.match(r"^[A-Za-z]:/", value) is not None
        or any(segment in {"", ".", ".."} for segment in segments)
    ):
        _fail(code)
    try:
        path = Path(value)
        invalid_path = not path.parts or path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts)
    except ValueError:
        _fail(code)
    if invalid_path:
        _fail(code)
    return path


def _resolve_root(value: str, code: str) -> Path:
    try:
        path = Path(value)
        absolute = path.is_absolute()
    except ValueError:
        _fail(code)
    if not absolute:
        _fail(code)
    try:
        resolved = path.resolve(strict=True)
        directory = resolved.is_dir()
    except (OSError, ValueError):
        _fail(code)
    if not directory:
        _fail(code)
    return resolved


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _resolve_existing_child(root: Path, relative_path: Any, code: str) -> Path:
    relative = _require_relative_path(relative_path, code)
    try:
        resolved = (root / relative).resolve(strict=True)
    except (OSError, ValueError):
        _fail(code)
    if not _is_within(resolved, root):
        _fail(code)
    return resolved


def validate_invocation(envelope: dict) -> ValidatedInvocation:
    """Validate one version-1 envelope before any case-material path is accessed."""
    if type(envelope) is not dict:
        _fail("invalid-envelope")
    required_envelope_fields = {"version", "skill", "inputs", "output", "runtime", "internet", "isolation"}
    if "target" in envelope:
        required_envelope_fields.add("target")
    _require_exact_object(envelope, required_envelope_fields, set(_ENVELOPE_FIELDS), "invalid-envelope")

    if type(envelope["version"]) is not int or envelope["version"] != 1:
        _fail("invalid-version")
    if not _is_identifier(envelope["skill"]):
        _fail("invalid-skill")

    inputs_value = envelope["inputs"]
    if type(inputs_value) is not list or not inputs_value:
        _fail("invalid-inputs")
    declared_inputs: list[tuple[str, str]] = []
    roles: set[str] = set()
    for item in inputs_value:
        input_object = _require_exact_object(item, {"role", "root"}, {"role", "root"}, "invalid-input")
        role, root = input_object["role"], input_object["root"]
        if not _is_identifier(role) or not isinstance(root, str) or not root:
            _fail("invalid-input")
        if role in roles:
            _fail("duplicate-input-role")
        roles.add(role)
        declared_inputs.append((role, root))

    output = _require_exact_object(envelope["output"], {"root"}, {"root"}, "invalid-output")
    if not isinstance(output["root"], str) or not output["root"]:
        _fail("invalid-output")

    runtime = _require_exact_object(
        envelope["runtime"], {"max_seconds", "max_input_bytes"}, {"max_seconds", "max_input_bytes"}, "invalid-runtime"
    )
    if (
        type(runtime["max_seconds"]) is not int
        or runtime["max_seconds"] < 1
        or type(runtime["max_input_bytes"]) is not int
        or runtime["max_input_bytes"] < 1
    ):
        _fail("invalid-runtime")
    if not isinstance(envelope["internet"], str) or envelope["internet"] not in {"disabled", "authorized"}:
        _fail("invalid-internet")

    isolation = _require_exact_object(
        envelope["isolation"], {"inputs", "output", "undeclared"}, {"inputs", "output", "undeclared"}, "invalid-isolation"
    )
    if isolation != {"inputs": "read-only", "output": "read-write", "undeclared": "none"}:
        _fail("invalid-isolation")

    target_value = envelope.get("target")
    if "target" in envelope:
        target = _require_exact_object(target_value, {"role", "path"}, {"role", "path"}, "invalid-target")
        if not _is_identifier(target["role"]):
            _fail("invalid-target")
        if target["role"] not in roles:
            _fail("invalid-target")
        _require_relative_path(target["path"], "invalid-target")

    inputs = tuple((role, _resolve_root(root, "invalid-input-root")) for role, root in declared_inputs)
    output_root = _resolve_root(output["root"], "invalid-output-root")
    for _, input_root in inputs:
        if _is_within(output_root, input_root) or _is_within(input_root, output_root):
            _fail("overlapping-input-output")

    resolved_target = None
    if "target" in envelope:
        resolved_target = (target_value["role"], resolve_input_path(
            ValidatedInvocation(
                skill=envelope["skill"],
                inputs=inputs,
                output_root=output_root,
                runtime={"max_seconds": runtime["max_seconds"], "max_input_bytes": runtime["max_input_bytes"]},
                internet=envelope["internet"],
                target=None,
            ),
            target_value["role"],
            target_value["path"],
        ))
    return ValidatedInvocation(
        skill=envelope["skill"],
        inputs=inputs,
        output_root=output_root,
        runtime={"max_seconds": runtime["max_seconds"], "max_input_bytes": runtime["max_input_bytes"]},
        internet=envelope["internet"],
        target=resolved_target,
    )


def resolve_input_path(invocation: ValidatedInvocation, role: str, relative_path: str) -> Path:
    """Resolve one existing regular or directory input child without escaping its role."""
    for input_role, root in invocation.inputs:
        if input_role == role:
            return _resolve_existing_child(root, relative_path, "invalid-input-path")
    _fail("unknown-input-role")


def resolve_output_path(invocation: ValidatedInvocation, relative_path: str) -> Path:
    """Resolve an output child without creating it or following an escaping symlink."""
    relative = _require_relative_path(relative_path, "invalid-output-path")
    current = invocation.output_root
    for index, part in enumerate(relative.parts):
        candidate = current / part
        if candidate.exists() or candidate.is_symlink():
            try:
                current = candidate.resolve(strict=True)
            except (OSError, ValueError):
                _fail("invalid-output-path")
            if not _is_within(current, invocation.output_root):
                _fail("invalid-output-path")
            if index < len(relative.parts) - 1 and not current.is_dir():
                _fail("invalid-output-path")
        else:
            current = candidate
    return current


def _directory_identity(path: Path) -> tuple[int, int]:
    try:
        stat = path.stat()
    except OSError:
        _fail("manifest-unavailable")
    return stat.st_dev, stat.st_ino


def _hash_file(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as source:
            while chunk := source.read(1024 * 1024):
                digest.update(chunk)
        size = path.stat().st_size
    except OSError:
        _fail("manifest-unavailable")
    return size, digest.hexdigest()


def _manifest_files(root: Path) -> list[dict[str, Any]]:
    files: list[dict[str, Any]] = []

    def walk(directory: Path, logical_parent: Path, active_directories: set[tuple[int, int]]) -> None:
        identity = _directory_identity(directory)
        if identity in active_directories:
            _fail("directory-symlink-cycle")
        active_directories.add(identity)
        try:
            entries = sorted(os.scandir(directory), key=lambda entry: entry.name)
            for entry in entries:
                logical_path = logical_parent / entry.name
                candidate = Path(entry.path)
                try:
                    resolved = candidate.resolve(strict=True)
                except OSError:
                    _fail("manifest-unavailable")
                if not _is_within(resolved, root):
                    _fail("escaping-input-symlink")
                if entry.is_dir(follow_symlinks=True):
                    walk(resolved, logical_path, active_directories)
                elif entry.is_file(follow_symlinks=True):
                    size, sha256 = _hash_file(resolved)
                    files.append({"path": logical_path.as_posix(), "size": size, "sha256": sha256})
                else:
                    _fail("unsupported-input-entry")
        except OSError:
            _fail("manifest-unavailable")
        finally:
            active_directories.remove(identity)

    try:
        walk(root, Path(), set())
    except RecursionError:
        _fail("manifest-unavailable")
    return sorted(files, key=lambda item: item["path"])


def build_input_manifest(invocation: ValidatedInvocation) -> dict[str, list[dict[str, Any]]]:
    """Build a deterministic, logical-only SHA-256 manifest for declared inputs."""
    return {
        "inputs": [
            {"role": role, "files": _manifest_files(root)}
            for role, root in invocation.inputs
        ]
    }


def main() -> int:
    try:
        envelope = json.load(sys.stdin)
        manifest = build_input_manifest(validate_invocation(envelope))
    except InvocationError as error:
        print(json.dumps({"error": {"code": error.code}}, separators=(",", ":")))
        return 1
    except (json.JSONDecodeError, OSError, UnicodeDecodeError, RecursionError):
        print(json.dumps({"error": {"code": "invalid-json"}}, separators=(",", ":")))
        return 1
    except ValueError:
        print(json.dumps({"error": {"code": "invalid-invocation"}}, separators=(",", ":")))
        return 1
    print(json.dumps(manifest, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
