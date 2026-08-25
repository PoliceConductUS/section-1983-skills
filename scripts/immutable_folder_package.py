"""Trusted-host validation and publication for immutable folder packages."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping

from scripts.skill_output_writer import OutputRun
from scripts.validate_folder_invocation import ValidatedInvocation, build_input_manifest


MANIFEST_NAME = "package-manifest.json"
CONTROL_NAMESPACES = frozenset({".skill-runs", "temp"})
_IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_CLASSIFICATIONS = frozenset(
    {
        "profile",
        "overlay",
        "corpus",
        "source",
        "provenance",
        "classification",
        "assumptions",
        "gaps",
        "validation-receipt",
        "other",
    }
)


class PackageError(ValueError):
    """A bounded immutable-package contract failure."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class PackageMember:
    id: str
    role: str
    classification: str
    path: str
    media_type: str
    size: int
    sha256: str
    contents: bytes


@dataclass(frozen=True)
class ValidatedFolderPackage:
    root: Path
    package_kind: str
    package_id: str
    created_at: str
    freshness: Mapping[str, str | None]
    producer: Mapping[str, str]
    sources: tuple[Mapping[str, str], ...]
    members: tuple[PackageMember, ...]
    validation: Mapping[str, str]
    manifest_sha256: str
    fingerprint: str


def _fail(code: str) -> None:
    raise PackageError(code)


def _sha256(contents: bytes) -> str:
    return hashlib.sha256(contents).hexdigest()


def _object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            _fail("invalid-package-json")
        value[key] = item
    return value


def _identifier(value: Any) -> bool:
    return isinstance(value, str) and _IDENTIFIER.fullmatch(value) is not None


def _date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.tzinfo == timezone.utc


def _relative_path(value: Any) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        _fail("invalid-package-member")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or path.as_posix() != value
        or not path.parts
        or any(part in {"", ".", ".."} for part in path.parts)
        or path.parts[0].casefold() in CONTROL_NAMESPACES
        or value == MANIFEST_NAME
    ):
        _fail("invalid-package-member")
    return path


def _bounded_bytes(path: Path, limit: int) -> bytes:
    try:
        if path.stat().st_size > limit:
            _fail("package-byte-limit")
        with path.open("rb") as source:
            contents = source.read(limit + 1)
    except PackageError:
        raise
    except OSError:
        _fail("invalid-package-root")
    if len(contents) > limit:
        _fail("package-byte-limit")
    return contents


def _manifest(root: Path, max_bytes: int) -> tuple[dict[str, Any], bytes]:
    try:
        selected = root / MANIFEST_NAME
        resolved = selected.resolve(strict=True)
        if resolved != selected:
            _fail("aliased-package-manifest")
        contents = _bounded_bytes(selected, max_bytes)
        value = json.loads(
            contents.decode("utf-8", errors="strict"), object_pairs_hook=_object
        )
    except PackageError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, RuntimeError, ValueError):
        _fail("invalid-package-manifest")
    if type(value) is not dict:
        _fail("invalid-package-manifest")
    return value, contents


def _frozen_object(value: dict[str, str | None]) -> Mapping[str, str | None]:
    return MappingProxyType(dict(value))


def _validate_freshness(value: Any) -> Mapping[str, str | None]:
    if type(value) is not dict or set(value) != {"checked_through", "retrieved_on"}:
        _fail("invalid-package-freshness")
    if any(item is not None and not _date(item) for item in value.values()):
        _fail("invalid-package-freshness")
    return _frozen_object(value)


def _validate_producer(value: Any) -> Mapping[str, str]:
    if type(value) is not dict or set(value) != {"name", "version", "operation", "run_id"}:
        _fail("invalid-package-producer")
    if (
        not isinstance(value["name"], str)
        or not value["name"]
        or not isinstance(value["version"], str)
        or not value["version"]
        or not _identifier(value["operation"])
        or not _identifier(value["run_id"])
    ):
        _fail("invalid-package-producer")
    return MappingProxyType(dict(value))


def _validate_sources(value: Any) -> tuple[Mapping[str, str], ...]:
    if type(value) is not list:
        _fail("invalid-package-sources")
    result = []
    for item in value:
        if (
            type(item) is not dict
            or set(item) != {"role", "source_id", "fingerprint"}
            or not _identifier(item["role"])
            or not isinstance(item["source_id"], str)
            or not item["source_id"]
            or not isinstance(item["fingerprint"], str)
            or _SHA256.fullmatch(item["fingerprint"]) is None
        ):
            _fail("invalid-package-source")
        result.append(MappingProxyType(dict(item)))
    return tuple(result)


def _read_member(root: Path, value: Any, max_bytes: int) -> PackageMember:
    required = {"id", "role", "classification", "path", "media_type", "size", "sha256"}
    if type(value) is not dict or set(value) != required:
        _fail("invalid-package-member")
    if (
        not _identifier(value["id"])
        or not _identifier(value["role"])
        or value["classification"] not in _CLASSIFICATIONS
        or not isinstance(value["media_type"], str)
        or not value["media_type"]
        or type(value["size"]) is not int
        or value["size"] < 0
        or not isinstance(value["sha256"], str)
        or _SHA256.fullmatch(value["sha256"]) is None
    ):
        _fail("invalid-package-member")
    if value["size"] > max_bytes:
        _fail("package-byte-limit")
    relative = _relative_path(value["path"])
    try:
        selected = root / Path(*relative.parts)
        resolved = selected.resolve(strict=True)
        if resolved != selected:
            _fail("aliased-package-member")
        resolved.relative_to(root)
        if not resolved.is_file():
            _fail("missing-package-member")
        contents = _bounded_bytes(resolved, max_bytes)
    except PackageError:
        raise
    except (OSError, RuntimeError, ValueError):
        _fail("missing-package-member")
    if len(contents) != value["size"] or _sha256(contents) != value["sha256"]:
        _fail("package-member-mismatch")
    return PackageMember(contents=contents, **value)


def _complete_membership(root: Path, listed: set[str]) -> None:
    actual = set()
    identities = set()
    for control_name in CONTROL_NAMESPACES:
        control_path = root / control_name
        if control_path.is_symlink() or (
            control_path.exists() and not control_path.is_dir()
        ):
            _fail("invalid-package-control-namespace")
    try:
        for path in root.rglob("*"):
            relative = path.relative_to(root).as_posix()
            top_level = relative.split("/", 1)[0].casefold()
            if top_level in CONTROL_NAMESPACES:
                if path.is_symlink():
                    _fail("invalid-package-control-namespace")
                if path.is_dir() or path.is_file():
                    continue
                _fail("invalid-package-control-namespace")
            if path.is_symlink():
                _fail("aliased-package-member")
            if path.is_dir():
                continue
            if not path.is_file():
                _fail("special-package-member")
            identity = (path.stat().st_dev, path.stat().st_ino)
            if identity in identities:
                _fail("duplicate-package-member")
            identities.add(identity)
            if relative != MANIFEST_NAME:
                actual.add(relative)
    except PackageError:
        raise
    except (OSError, RuntimeError, ValueError):
        _fail("invalid-package-root")
    if actual - listed:
        _fail("unlisted-package-member")
    if listed - actual:
        _fail("missing-package-member")


def load_folder_package(
    package_root, *, accepted_kinds, max_bytes
) -> ValidatedFolderPackage:
    """Validate one ordinary folder package and pin its exact member bytes."""
    if (
        not isinstance(accepted_kinds, (set, frozenset, tuple, list))
        or not accepted_kinds
        or any(not _identifier(kind) for kind in accepted_kinds)
        or len(set(accepted_kinds)) != len(accepted_kinds)
    ):
        _fail("invalid-accepted-package-kinds")
    if type(max_bytes) is not int or max_bytes < 0:
        _fail("invalid-package-byte-limit")
    try:
        selected_root = Path(package_root).resolve(strict=True)
        if not selected_root.is_dir():
            _fail("invalid-package-root")
    except PackageError:
        raise
    except (OSError, RuntimeError, ValueError, TypeError):
        _fail("invalid-package-root")

    value, manifest_bytes = _manifest(selected_root, max_bytes)
    required = {
        "schema_version",
        "package_kind",
        "package_id",
        "created_at",
        "freshness",
        "producer",
        "sources",
        "members",
        "validation",
    }
    if (
        set(value) != required
        or type(value["schema_version"]) is not int
        or value["schema_version"] != 1
        or not _identifier(value["package_kind"])
        or not _identifier(value["package_id"])
        or not _timestamp(value["created_at"])
    ):
        _fail("invalid-package-manifest")
    if value["package_kind"] not in set(accepted_kinds):
        _fail("unsupported-package-kind")
    freshness = _validate_freshness(value["freshness"])
    producer = _validate_producer(value["producer"])
    sources = _validate_sources(value["sources"])
    if type(value["members"]) is not list or not value["members"]:
        _fail("invalid-package-members")
    remaining_bytes = max_bytes - len(manifest_bytes)
    loaded_members = []
    for item in value["members"]:
        member = _read_member(selected_root, item, remaining_bytes)
        loaded_members.append(member)
        remaining_bytes -= member.size
    members = tuple(loaded_members)
    ids = [member.id for member in members]
    paths = [member.path for member in members]
    if len(ids) != len(set(ids)) or len(paths) != len(set(paths)):
        _fail("duplicate-package-member")
    _complete_membership(selected_root, set(paths))
    if len(manifest_bytes) + sum(member.size for member in members) > max_bytes:
        _fail("package-byte-limit")

    validation = value["validation"]
    if (
        type(validation) is not dict
        or set(validation)
        != {"status", "validator", "version", "validated_at", "receipt_member_id"}
        or validation["status"] != "passed"
        or not isinstance(validation["validator"], str)
        or not validation["validator"]
        or not isinstance(validation["version"], str)
        or not validation["version"]
        or not _timestamp(validation["validated_at"])
        or not _identifier(validation["receipt_member_id"])
    ):
        _fail("invalid-package-validation")
    receipt = next(
        (member for member in members if member.id == validation["receipt_member_id"]),
        None,
    )
    if receipt is None or receipt.classification != "validation-receipt":
        _fail("invalid-package-validation-receipt")
    fingerprint = _sha256(manifest_bytes)
    return ValidatedFolderPackage(
        root=selected_root,
        package_kind=value["package_kind"],
        package_id=value["package_id"],
        created_at=value["created_at"],
        freshness=freshness,
        producer=producer,
        sources=sources,
        members=members,
        validation=MappingProxyType(dict(validation)),
        manifest_sha256=fingerprint,
        fingerprint=fingerprint,
    )


def _canonical_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError):
        _fail("invalid-package-json")


def _proposed_members(value: Any) -> tuple[tuple[dict[str, Any], bytes], ...]:
    if type(value) is not list or not value:
        _fail("invalid-package-members")
    result = []
    required = {"id", "role", "classification", "path", "media_type", "contents"}
    for item in value:
        if type(item) is not dict or set(item) != required:
            _fail("invalid-package-member")
        if (
            not _identifier(item["id"])
            or not _identifier(item["role"])
            or item["classification"] not in _CLASSIFICATIONS
            or not isinstance(item["media_type"], str)
            or not item["media_type"]
        ):
            _fail("invalid-package-member")
        path = _relative_path(item["path"]).as_posix()
        contents = item["contents"]
        if isinstance(contents, str):
            contents = contents.encode("utf-8")
        if not isinstance(contents, bytes):
            _fail("invalid-package-contents")
        result.append(
            (
                {
                    "id": item["id"],
                    "role": item["role"],
                    "classification": item["classification"],
                    "path": path,
                    "media_type": item["media_type"],
                    "size": len(contents),
                    "sha256": _sha256(contents),
                },
                contents,
            )
        )
    ids = [item[0]["id"] for item in result]
    paths = [item[0]["path"] for item in result]
    if len(ids) != len(set(ids)) or len(paths) != len(set(paths)):
        _fail("duplicate-package-member")
    return tuple(result)


def _publication_validation(value: Any, members) -> dict[str, str]:
    if (
        type(value) is not dict
        or set(value)
        != {"status", "validator", "version", "validated_at", "receipt_member_id"}
        or value["status"] != "passed"
        or not isinstance(value["validator"], str)
        or not value["validator"]
        or not isinstance(value["version"], str)
        or not value["version"]
        or not _timestamp(value["validated_at"])
        or not _identifier(value["receipt_member_id"])
    ):
        _fail("invalid-package-validation")
    receipt = next(
        (item[0] for item in members if item[0]["id"] == value["receipt_member_id"]),
        None,
    )
    if receipt is None or receipt["classification"] != "validation-receipt":
        _fail("invalid-package-validation-receipt")
    return dict(value)


def publish_folder_package(
    invocation: ValidatedInvocation,
    *,
    package_kind: str,
    package_id: str,
    created_at: str,
    freshness,
    sources,
    members,
    validation,
    operation: str,
    run_id: str,
    skill_version: str,
) -> dict[str, Any]:
    """Publish one complete package beneath an explicit fresh output folder."""
    if not isinstance(invocation, ValidatedInvocation):
        _fail("invalid-package-invocation")
    if (
        invocation.contract_target_policy not in {"required", "optional", "none"}
        or invocation.contract_target_roles is None
    ):
        _fail("unbound-package-invocation")
    if (
        not _identifier(package_kind)
        or not _identifier(package_id)
        or not _timestamp(created_at)
        or not _identifier(operation)
        or not _identifier(run_id)
        or not isinstance(skill_version, str)
        or not skill_version
    ):
        _fail("invalid-package-publication")
    normalized_freshness = dict(_validate_freshness(freshness))
    normalized_sources = [dict(item) for item in _validate_sources(sources)]
    proposed = _proposed_members(members)
    normalized_validation = _publication_validation(validation, proposed)
    manifest = {
        "schema_version": 1,
        "package_kind": package_kind,
        "package_id": package_id,
        "created_at": created_at,
        "freshness": normalized_freshness,
        "producer": {
            "name": invocation.skill,
            "version": skill_version,
            "operation": operation,
            "run_id": run_id,
        },
        "sources": normalized_sources,
        "members": [item for item, _ in proposed],
        "validation": normalized_validation,
    }
    input_manifest = build_input_manifest(invocation)
    run = OutputRun.start(
        invocation,
        run_id=run_id,
        skill_version=skill_version,
        mode="fresh-regenerable",
        input_manifest=input_manifest,
    )
    try:
        for member, contents in proposed:
            run.write(member["path"], contents)
        run.write(MANIFEST_NAME, _canonical_bytes(manifest))
        return run.complete()
    except Exception:
        try:
            run.fail("folder-package-publication", "publish")
        except Exception:
            pass
        raise
