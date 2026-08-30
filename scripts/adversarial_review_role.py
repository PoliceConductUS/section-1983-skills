"""Protected adversarial-review role for the declared-folder launcher."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from types import ModuleType
from typing import Any

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
_ROLE_INSTRUCTIONS = (
    _REPOSITORY
    / "skills"
    / "adversarial-filing-review"
    / "references"
    / "static-role-instructions.md"
)
_DOMAIN_RUNTIME = (
    _REPOSITORY
    / "skills"
    / "adversarial-filing-review"
    / "scripts"
    / "launch_review.py"
)
_SOURCE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_SOURCE_ROLE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_YAML_KEY = re.compile(r"^[a-z][a-z0-9_]*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_MAX_SOURCE_IDS = 64
_MAX_SOURCE_DOCUMENT_BYTES = 65_536
_SOURCE_FIELDS = {
    "schema_version",
    "source_id",
    "role",
    "path",
    "sha256",
    "checked_through",
}


@dataclass(frozen=True)
class ApprovedSourceRecord:
    source_id: str
    role: str
    content_path: str
    documentation_path: str
    documentation_sha256: str
    sha256: str
    checked_through: str


def _invalid_definition() -> None:
    raise RoleLaunchError("invalid-role-definition")


def _load_domain_runtime() -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        "_section_1983_adversarial_review_domain", _DOMAIN_RUNTIME
    )
    if specification is None or specification.loader is None:
        _invalid_definition()
    module = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(module)
    except (ImportError, OSError, SyntaxError):
        _invalid_definition()
    return module


def _public_instructions() -> bytes:
    try:
        contents = _ROLE_INSTRUCTIONS.read_bytes()
        contents.decode("utf-8")
    except (OSError, UnicodeError):
        _invalid_definition()
    if not contents:
        _invalid_definition()
    return contents


def _approved_source_ids(values: Any) -> tuple[str, ...]:
    if (
        type(values) is not tuple
        or not values
        or len(values) > _MAX_SOURCE_IDS
        or len(values) != len(set(values))
        or any(
            not isinstance(value, str) or _SOURCE_ID.fullmatch(value) is None
            for value in values
        )
    ):
        _invalid_definition()
    return values


def _source_failure(code: str) -> None:
    raise RoleLaunchError(code)


def _yaml_scalar(value: str) -> str:
    candidate = value.strip()
    if not candidate:
        _source_failure("invalid-source-documentation")
    if candidate.startswith('"'):
        try:
            decoded = json.loads(candidate)
        except (TypeError, ValueError, json.JSONDecodeError):
            _source_failure("invalid-source-documentation")
        if not isinstance(decoded, str) or not decoded:
            _source_failure("invalid-source-documentation")
        return decoded
    if candidate.startswith("'"):
        if len(candidate) < 2 or not candidate.endswith("'"):
            _source_failure("invalid-source-documentation")
        decoded = candidate[1:-1].replace("''", "'")
        if not decoded:
            _source_failure("invalid-source-documentation")
        return decoded
    if " #" in candidate:
        candidate = candidate.split(" #", 1)[0].rstrip()
    if not candidate or any(character in candidate for character in "{}[]&*!|>"):
        _source_failure("invalid-source-documentation")
    return candidate


def _parse_source_document(contents: bytes) -> dict[str, str]:
    if not contents or len(contents) > _MAX_SOURCE_DOCUMENT_BYTES:
        _source_failure("invalid-source-documentation")
    try:
        text = contents.decode("utf-8")
    except UnicodeError:
        _source_failure("invalid-source-documentation")
    values: dict[str, str] = {}
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line != raw_line.lstrip() or ":" not in raw_line:
            _source_failure("invalid-source-documentation")
        key, raw_value = raw_line.split(":", 1)
        if _YAML_KEY.fullmatch(key) is None or key in values:
            _source_failure("invalid-source-documentation")
        values[key] = _yaml_scalar(raw_value)
    if set(values) != _SOURCE_FIELDS or values["schema_version"] != "1":
        _source_failure("invalid-source-documentation")
    return values


def _read_bounded(path: Path, maximum: int, code: str) -> bytes:
    try:
        size = path.stat().st_size
        if size < 1 or size > maximum:
            _source_failure(code)
        with path.open("rb") as source:
            contents = source.read(maximum + 1)
    except RoleLaunchError:
        raise
    except OSError:
        _source_failure(code)
    if len(contents) != size:
        _source_failure(code)
    return contents


def _iso_date(value: Any, code: str) -> date:
    if not isinstance(value, str):
        _source_failure(code)
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        _source_failure(code)
    if parsed.isoformat() != value:
        _source_failure(code)
    return parsed


def load_approved_source_records(
    *,
    invocation: ValidatedInvocation,
    documentation_paths: tuple[str, ...],
    minimum_checked_through: str,
) -> tuple[ApprovedSourceRecord, ...]:
    """Validate adversarial source YAML and its referenced ordinary file."""

    if (
        not isinstance(invocation, ValidatedInvocation)
        or type(documentation_paths) is not tuple
        or not documentation_paths
        or len(documentation_paths) > _MAX_SOURCE_IDS
        or len(documentation_paths) != len(set(documentation_paths))
    ):
        _source_failure("invalid-source-documentation")
    minimum = _iso_date(
        minimum_checked_through, "invalid-source-documentation"
    )
    records: list[ApprovedSourceRecord] = []
    source_ids: set[str] = set()
    content_paths: set[str] = set()
    for documentation_path in documentation_paths:
        try:
            document = resolve_input_path(
                invocation, "approved-sources", documentation_path
            )
            if not document.is_file():
                _source_failure("invalid-source-documentation")
            document_bytes = _read_bounded(
                document,
                _MAX_SOURCE_DOCUMENT_BYTES,
                "invalid-source-documentation",
            )
            values = _parse_source_document(document_bytes)
            source_id = values["source_id"]
            role = values["role"]
            content_path = values["path"]
            expected_hash = values["sha256"]
            checked_through = values["checked_through"]
            if (
                _SOURCE_ID.fullmatch(source_id) is None
                or _SOURCE_ROLE.fullmatch(role) is None
                or _SHA256.fullmatch(expected_hash) is None
                or source_id in source_ids
                or content_path in content_paths
                or content_path == documentation_path
            ):
                _source_failure("invalid-source-documentation")
            checked = _iso_date(
                checked_through, "invalid-source-documentation"
            )
            if checked < minimum:
                _source_failure("stale-source-documentation")
            content = resolve_input_path(
                invocation, "approved-sources", content_path
            )
            if not content.is_file():
                _source_failure("invalid-source-documentation")
            content_bytes = _read_bounded(
                content,
                invocation.runtime["max_input_bytes"],
                "invalid-source-documentation",
            )
            if hashlib.sha256(content_bytes).hexdigest() != expected_hash:
                _source_failure("source-content-mismatch")
        except RoleLaunchError:
            raise
        except (InvocationError, OSError, ValueError):
            _source_failure("invalid-source-documentation")
        source_ids.add(source_id)
        content_paths.add(content_path)
        records.append(
            ApprovedSourceRecord(
                source_id=source_id,
                role=role,
                content_path=content_path,
                documentation_path=documentation_path,
                documentation_sha256=hashlib.sha256(document_bytes).hexdigest(),
                sha256=expected_hash,
                checked_through=checked_through,
            )
        )
    return tuple(records)


def _validate_selected_sources(
    inputs: tuple[SelectedInputSnapshot, ...],
    records: tuple[ApprovedSourceRecord, ...],
) -> None:
    selected_content = {
        item.path: item
        for item in inputs
        if item.purpose == "approved-source" and item.role == "approved-sources"
    }
    selected_documents = {
        item.path: item
        for item in inputs
        if item.purpose == "source-documentation"
        and item.role == "approved-sources"
    }
    if (
        set(selected_content) != {record.content_path for record in records}
        or set(selected_documents)
        != {record.documentation_path for record in records}
        or any(
            selected_content[record.content_path].sha256 != record.sha256
            for record in records
        )
        or any(
            selected_documents[record.documentation_path].sha256
            != record.documentation_sha256
            for record in records
        )
    ):
        _source_failure("invalid-source-selection")


def build_adversarial_review_definition(
    *, adapter: Any, approved_sources: tuple[ApprovedSourceRecord, ...]
) -> RoleLaunchDefinition:
    """Build the fixed role around host-validated folder source identities."""

    if (
        type(approved_sources) is not tuple
        or not approved_sources
        or any(not isinstance(item, ApprovedSourceRecord) for item in approved_sources)
    ):
        _invalid_definition()
    source_ids = _approved_source_ids(
        tuple(record.source_id for record in approved_sources)
    )
    domain = _load_domain_runtime()

    def validate_output(value: Any) -> tuple[ProposedArtifact, ...]:
        if (
            type(value) is not dict
            or set(value) != {"output_kind", "review"}
            or value["output_kind"] != "adversarial-filing-review"
        ):
            raise RoleLaunchError("child-output-invalid")
        domain.validate_review_response(value["review"], set(source_ids))
        report = domain.render_review_markdown(
            value["review"],
            {
                "outcome": "completed",
                "runtime": "shared-static-role",
                "source_ids": list(source_ids),
            },
        ).encode("utf-8")
        return (
            ProposedArtifact(
                path="reports/adversarial-filing-review.md",
                contents=report,
            ),
        )

    return RoleLaunchDefinition(
        role_id="adversarial-filing-reviewer",
        operations=("review-filing",),
        input_requirements=(
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
            "mutate-target",
            "decide-plaintiff-strategy",
            "invent-authority",
            "claim-filing-readiness",
            "remediate-filing",
        ),
        internet="authorized",
        target_mutation="forbidden",
        output_kind="adversarial-filing-review",
        public_instructions=_public_instructions(),
        adapter=adapter,
        input_validator=lambda inputs: _validate_selected_sources(
            inputs, approved_sources
        ),
        output_validator=validate_output,
        max_stdout_bytes=1_000_000,
        max_stderr_bytes=8_192,
    )
