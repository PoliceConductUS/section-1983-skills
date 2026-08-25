"""Fixed findings roles conditioned on validated ordinary profile files."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

from scripts.adversarial_review_role import ApprovedSourceRecord
from scripts.static_role_launcher import (
    InputRequirement,
    ProposedArtifact,
    RoleLaunchDefinition,
    RoleLaunchError,
    SelectedInputSnapshot,
)
from scripts.validate_folder_invocation import (
    InvocationError,
    ValidatedInvocation,
    resolve_input_path,
)


_REPOSITORY = Path(__file__).resolve().parents[1]
_COUNSEL_VALIDATOR = (
    _REPOSITORY
    / "skills"
    / "building-defense-counsel-overlays"
    / "scripts"
    / "validate_counsel_overlays.py"
)
_JUDICIAL_VALIDATOR = (
    _REPOSITORY
    / "skills"
    / "building-judicial-reasoning-profiles"
    / "scripts"
    / "validate_judicial_profiles.py"
)
_STABLE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_JUDICIAL_SOURCE_ID = re.compile(
    r"(?m)^  - source_id: ([A-Za-z0-9][A-Za-z0-9._:-]*)\s*$"
)
_MAX_PROFILE_BYTES = 2_000_000
_MAX_FINDINGS = 64
_FINDING_FIELDS = {
    "id",
    "category",
    "attacked_quote",
    "location",
    "source_ids",
    "analysis",
    "limitation",
}
_OPPOSING_CATEGORIES = {
    "source-backed-attack",
    "procedural-attack",
    "authority-attack",
    "record-attack",
    "element-attack",
    "remedy-attack",
    "presentation-attack",
    "gap",
}
_JUDICIAL_CATEGORIES = {
    "comprehension",
    "procedural-framing",
    "authority-presentation",
    "record-traceability",
    "gap",
}
_PREDICTION = re.compile(
    r"(?i)\b(?:judge|court)\s+will\b|\bwill\s+(?:grant|deny|dismiss|rule)\b|"
    r"\bpredicted\s+(?:outcome|disposition)\b"
)


@dataclass(frozen=True)
class ValidatedRoleProfile:
    kind: str
    profile_id: str
    checked_through: str
    selected_files: tuple[tuple[str, str], ...]
    source_ids: tuple[str, ...]


def _fail(code: str) -> None:
    raise RoleLaunchError(code)


def _load_module(path: Path, name: str) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        _fail("profile-validator-unavailable")
    module = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(module)
    except (ImportError, OSError, SyntaxError):
        _fail("profile-validator-unavailable")
    return module


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            _fail("invalid-profile-json")
        value[key] = item
    return value


def _read_profile_file(
    invocation: ValidatedInvocation, relative_path: str
) -> tuple[bytes, str]:
    if not isinstance(invocation, ValidatedInvocation):
        _fail("invalid-profile-invocation")
    try:
        path = resolve_input_path(invocation, "profile", relative_path)
        if not path.is_file():
            _fail("invalid-profile-file")
        size = path.stat().st_size
        maximum = min(invocation.runtime["max_input_bytes"], _MAX_PROFILE_BYTES)
        if size < 1 or size > maximum:
            _fail("invalid-profile-file")
        with path.open("rb") as source:
            contents = source.read(maximum + 1)
    except RoleLaunchError:
        raise
    except (InvocationError, OSError, ValueError):
        _fail("invalid-profile-file")
    if len(contents) != size:
        _fail("invalid-profile-file")
    return contents, hashlib.sha256(contents).hexdigest()


def _json(contents: bytes, code: str) -> dict[str, Any]:
    try:
        value = json.loads(
            contents.decode("utf-8", errors="strict"), object_pairs_hook=_object
        )
    except RoleLaunchError:
        raise
    except (UnicodeError, ValueError, json.JSONDecodeError):
        _fail(code)
    if type(value) is not dict:
        _fail(code)
    return value


def load_opposing_counsel_profile(
    *,
    invocation: ValidatedInvocation,
    overlay_path: str,
    snapshot_path: str,
) -> ValidatedRoleProfile:
    overlay_bytes, overlay_hash = _read_profile_file(invocation, overlay_path)
    snapshot_bytes, snapshot_hash = _read_profile_file(invocation, snapshot_path)
    overlay = _json(overlay_bytes, "invalid-opposing-counsel-profile")
    snapshot = _json(snapshot_bytes, "invalid-opposing-counsel-profile")
    validator = _load_module(
        _COUNSEL_VALIDATOR, "_section_1983_counsel_profile_validator"
    )
    try:
        findings = validator.validate_overlay(overlay, snapshot)
    except BaseException:
        _fail("invalid-opposing-counsel-profile")
    if findings:
        _fail("invalid-opposing-counsel-profile")
    source_ids = tuple(
        source["source_id"]
        for source in snapshot["sources"]
        if type(source) is dict and _STABLE_ID.fullmatch(source.get("source_id", ""))
    )
    if not source_ids or len(source_ids) != len(set(source_ids)):
        _fail("invalid-opposing-counsel-profile")
    return ValidatedRoleProfile(
        kind="opposing-counsel",
        profile_id=overlay["overlay_id"],
        checked_through=snapshot["checked_through"],
        selected_files=((overlay_path, overlay_hash), (snapshot_path, snapshot_hash)),
        source_ids=source_ids,
    )


def load_judicial_reviewer_profile(
    *,
    invocation: ValidatedInvocation,
    profile_path: str,
    source_index_path: str,
) -> ValidatedRoleProfile:
    profile_bytes, profile_hash = _read_profile_file(invocation, profile_path)
    index_bytes, index_hash = _read_profile_file(invocation, source_index_path)
    validator = _load_module(
        _JUDICIAL_VALIDATOR, "_section_1983_judicial_profile_validator"
    )
    try:
        profile = validator.validate_profile_bytes(
            profile_bytes, max_bytes=_MAX_PROFILE_BYTES
        )
        index_text = index_bytes.decode("utf-8", errors="strict")
    except BaseException:
        _fail("invalid-judicial-profile")
    expected_header = (
        "schema_version: 1\n"
        f"profile_id: {profile['profile_id']}\n"
        "sources:\n"
    )
    if not index_text.startswith(expected_header):
        _fail("invalid-judicial-profile")
    indexed_source_ids = tuple(_JUDICIAL_SOURCE_ID.findall(index_text))
    required_source_ids = {
        profile["judge_identity"]["source_id"],
        profile["court_scope"]["source_id"],
        *(record["source_id"] for record in profile["records"]),
    }
    if (
        not indexed_source_ids
        or len(indexed_source_ids) != len(set(indexed_source_ids))
        or not required_source_ids.issubset(indexed_source_ids)
    ):
        _fail("invalid-judicial-profile")
    return ValidatedRoleProfile(
        kind="judicial-reviewer",
        profile_id=profile["profile_id"],
        checked_through=profile["checked_through"],
        selected_files=((profile_path, profile_hash), (source_index_path, index_hash)),
        source_ids=tuple(sorted(required_source_ids)),
    )


def _validate_profile_and_sources(
    inputs: tuple[SelectedInputSnapshot, ...],
    profile: ValidatedRoleProfile,
    approved_sources: tuple[ApprovedSourceRecord, ...],
) -> None:
    selected_profile = {
        item.path: item.sha256
        for item in inputs
        if item.purpose == "profile" and item.role == "profile"
    }
    selected_sources = {
        item.path: item.sha256
        for item in inputs
        if item.purpose == "approved-source" and item.role == "approved-sources"
    }
    selected_documentation = {
        item.path: item.sha256
        for item in inputs
        if item.purpose == "source-documentation"
        and item.role == "approved-sources"
    }
    if (
        selected_profile != dict(profile.selected_files)
        or selected_sources
        != {record.content_path: record.sha256 for record in approved_sources}
        or selected_documentation
        != {
            record.documentation_path: record.documentation_sha256
            for record in approved_sources
        }
    ):
        _fail("invalid-role-input-selection")


def _instructions(skill: str) -> bytes:
    path = _REPOSITORY / "skills" / skill / "references" / "static-role-instructions.md"
    try:
        value = path.read_bytes()
        value.decode("utf-8", errors="strict")
    except (OSError, UnicodeError):
        _fail("invalid-role-definition")
    if not value:
        _fail("invalid-role-definition")
    return value


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _output_validator(
    *,
    value: Any,
    expected_kind: str,
    role: str,
    profile: ValidatedRoleProfile,
    approved_sources: tuple[ApprovedSourceRecord, ...],
    categories: set[str],
    path: str,
) -> tuple[ProposedArtifact, ...]:
    approved_source_ids = {record.source_id for record in approved_sources}
    if (
        type(value) is not dict
        or set(value) != {"output_kind", "findings"}
        or value["output_kind"] != expected_kind
        or type(value["findings"]) is not list
        or len(value["findings"]) > _MAX_FINDINGS
    ):
        _fail("child-output-invalid")
    finding_ids: set[str] = set()
    for finding in value["findings"]:
        if type(finding) is not dict or set(finding) != _FINDING_FIELDS:
            _fail("child-output-invalid")
        finding_id = finding["id"]
        source_ids = finding["source_ids"]
        if (
            not isinstance(finding_id, str)
            or _STABLE_ID.fullmatch(finding_id) is None
            or finding_id in finding_ids
            or finding["category"] not in categories
            or type(source_ids) is not list
            or not source_ids
            or len(source_ids) != len(set(source_ids))
            or not set(source_ids).issubset(approved_source_ids)
            or any(
                not _nonempty(finding[key])
                for key in (
                    "attacked_quote",
                    "location",
                    "analysis",
                    "limitation",
                )
            )
            or _PREDICTION.search(finding["analysis"]) is not None
        ):
            _fail("child-output-invalid")
        finding_ids.add(finding_id)
    artifact = {
        "schema_version": 1,
        "role": role,
        "profile_id": profile.profile_id,
        "profile_checked_through": profile.checked_through,
        "result": "findings-only",
        "approved_sources": [
            {
                "source_id": record.source_id,
                "checked_through": record.checked_through,
                "sha256": record.sha256,
            }
            for record in approved_sources
        ],
        "findings": value["findings"],
    }
    contents = (
        json.dumps(artifact, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    return (ProposedArtifact(path=path, contents=contents),)


def _definition(
    *,
    adapter: Any,
    profile: ValidatedRoleProfile,
    approved_sources: tuple[ApprovedSourceRecord, ...],
    expected_kind: str,
    role_id: str,
    operation: str,
    categories: set[str],
    path: str,
) -> RoleLaunchDefinition:
    if (
        not isinstance(profile, ValidatedRoleProfile)
        or type(approved_sources) is not tuple
        or not approved_sources
        or any(not isinstance(item, ApprovedSourceRecord) for item in approved_sources)
    ):
        _fail("invalid-role-definition")
    approved_source_ids = {record.source_id for record in approved_sources}
    if len(approved_source_ids) != len(approved_sources) or not approved_source_ids.issubset(
        profile.source_ids
    ):
        _fail("incompatible-profile-source")
    return RoleLaunchDefinition(
        role_id=role_id,
        operations=(operation,),
        input_requirements=(
            InputRequirement(
                "profile", ("profile",), len(profile.selected_files), len(profile.selected_files)
            ),
            InputRequirement("filing-target", ("filing",), 1, 1),
            InputRequirement(
                "approved-source",
                ("approved-sources",),
                len(approved_sources),
                len(approved_sources),
            ),
            InputRequirement(
                "source-documentation",
                ("approved-sources",),
                len(approved_sources),
                len(approved_sources),
            ),
        ),
        capabilities=(),
        prohibitions=(
            "emit-disposition",
            "concede-claim",
            "select-strategy",
            "mutate-target",
            "remediate-filing",
            "claim-filing-readiness",
            "predict-outcome",
            "impersonate-participant",
        ),
        internet="disabled",
        target_mutation="forbidden",
        output_kind=expected_kind,
        public_instructions=_instructions(role_id),
        adapter=adapter,
        input_validator=lambda inputs: _validate_profile_and_sources(
            inputs, profile, approved_sources
        ),
        output_validator=lambda value: _output_validator(
            value=value,
            expected_kind=expected_kind,
            role=role_id,
            profile=profile,
            approved_sources=approved_sources,
            categories=categories,
            path=path,
        ),
        max_stdout_bytes=1_000_000,
        max_stderr_bytes=8_192,
    )


def build_opposing_counsel_definition(
    *,
    adapter: Any,
    profile: ValidatedRoleProfile,
    approved_sources: tuple[ApprovedSourceRecord, ...],
) -> RoleLaunchDefinition:
    if not isinstance(profile, ValidatedRoleProfile) or profile.kind != "opposing-counsel":
        _fail("incompatible-role-profile")
    return _definition(
        adapter=adapter,
        profile=profile,
        approved_sources=approved_sources,
        expected_kind="opposing-counsel-findings",
        role_id="opposing-counsel",
        operation="opposing-counsel-simulation",
        categories=_OPPOSING_CATEGORIES,
        path="reports/opposing-counsel-findings.json",
    )


def build_judicial_reviewer_definition(
    *,
    adapter: Any,
    profile: ValidatedRoleProfile,
    approved_sources: tuple[ApprovedSourceRecord, ...],
) -> RoleLaunchDefinition:
    if not isinstance(profile, ValidatedRoleProfile) or profile.kind != "judicial-reviewer":
        _fail("incompatible-role-profile")
    return _definition(
        adapter=adapter,
        profile=profile,
        approved_sources=approved_sources,
        expected_kind="judicial-review-findings",
        role_id="judicial-reviewer",
        operation="judicial-review",
        categories=_JUDICIAL_CATEGORIES,
        path="reports/judicial-review-findings.json",
    )
