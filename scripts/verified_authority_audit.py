"""Folder-native verified-authority loading and audit host."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from scripts.validate_folder_invocation import ValidatedInvocation


_ROLES = ("filing-source", "verified-authority")
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_YAML_KEY = re.compile(r"^[a-z][a-z0-9_]*$")
_CORPUS_FIELDS = frozenset({"schema_version", "corpus_id", "authorities"})
_SOURCE_FIELDS = frozenset(
    {
        "schema_version",
        "source_id",
        "path",
        "sha256",
        "checked_through",
        "retrieved_from",
    }
)
_AUTHORITY_FIELDS = frozenset(
    {
        "schema_version",
        "authority_id",
        "citation",
        "document_path",
        "source_yaml_path",
        "sha256",
        "court",
        "decision_date",
        "publication_status",
        "precedential_status",
        "binding_status",
        "event_date_status",
        "later_history_status",
        "rule_of_orderliness_status",
        "proposition",
        "quotation",
        "pinpoint",
        "text_layer_status",
    }
)
_MAX_DOCUMENTATION_BYTES = 65_536
_UNAVAILABLE_CODES = frozenset(
    {
        "authority-content-unavailable",
        "authority-documentation-unavailable",
        "corpus-documentation-unavailable",
    }
)


class AuthorityAuditError(ValueError):
    """A bounded authority-audit input or host failure."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code
        self.exit_class = "unavailable" if code in _UNAVAILABLE_CODES else "invalid"


def _fail(code: str) -> None:
    raise AuthorityAuditError(code)


@dataclass(frozen=True)
class SourceDocumentation:
    source_id: str
    path: str
    sha256: str
    checked_through: str
    retrieved_from: str
    yaml_path: str
    yaml_sha256: str


@dataclass(frozen=True)
class AuthorityRecord:
    authority_id: str
    citation: str
    document_path: str
    source: SourceDocumentation
    sha256: str
    court: str
    decision_date: str
    publication_status: str
    precedential_status: str
    binding_status: str
    event_date_status: str
    later_history_status: str
    rule_of_orderliness_status: str
    proposition: str
    quotation: str
    pinpoint: str
    text_layer_status: str
    yaml_path: str
    yaml_sha256: str
    document_bytes: bytes


@dataclass(frozen=True)
class AuthorityCorpus:
    corpus_id: str
    authorities: tuple[AuthorityRecord, ...]
    yaml_path: str
    yaml_sha256: str


def _scalar(raw: str, code: str) -> str:
    value = raw.strip()
    if not value:
        _fail(code)
    if value.startswith('"'):
        try:
            decoded = json.loads(value)
        except (ValueError, json.JSONDecodeError):
            _fail(code)
        if not isinstance(decoded, str) or not decoded:
            _fail(code)
        return decoded
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            _fail(code)
        decoded = value[1:-1].replace("''", "'")
        if not decoded:
            _fail(code)
        return decoded
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    if not value or any(character in value for character in "{}[]&*!|>"):
        _fail(code)
    return value


def _read(path: Path, maximum: int, code: str) -> bytes:
    try:
        size = path.stat().st_size
        if size < 1 or size > maximum:
            _fail(code)
        contents = path.read_bytes()
    except AuthorityAuditError:
        raise
    except OSError:
        _fail(code)
    if len(contents) != size:
        _fail(code)
    return contents


def _required_path(
    invocation: ValidatedInvocation, relative_path: str, *, missing_code: str
) -> Path:
    if not isinstance(relative_path, str) or not relative_path:
        _fail("invalid-authority-documentation")
    parts = relative_path.split("/")
    if (
        "\\" in relative_path
        or "\x00" in relative_path
        or re.match(r"^[A-Za-z]:/", relative_path) is not None
        or any(part in {"", ".", ".."} for part in parts)
    ):
        _fail("invalid-authority-documentation")
    roots = dict(invocation.inputs)
    root = roots["verified-authority"]
    candidate = root
    try:
        for part in parts:
            candidate = candidate / part
            if candidate.is_symlink():
                _fail("invalid-authority-documentation")
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except AuthorityAuditError:
        raise
    except FileNotFoundError:
        _fail(missing_code)
    except (OSError, ValueError):
        _fail("invalid-authority-documentation")
    return resolved


def _flat_yaml(contents: bytes, expected: frozenset[str], code: str) -> dict[str, str]:
    if not contents or len(contents) > _MAX_DOCUMENTATION_BYTES:
        _fail(code)
    try:
        text = contents.decode("utf-8", errors="strict")
    except UnicodeError:
        _fail(code)
    values: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line != line.lstrip() or ":" not in line:
            _fail(code)
        key, raw = line.split(":", 1)
        if _YAML_KEY.fullmatch(key) is None or key in values:
            _fail(code)
        values[key] = _scalar(raw, code)
    if set(values) != expected or values["schema_version"] != "1":
        _fail(code)
    return values


def _corpus_yaml(contents: bytes) -> tuple[str, tuple[str, ...]]:
    code = "invalid-corpus-documentation"
    if not contents or len(contents) > _MAX_DOCUMENTATION_BYTES:
        _fail(code)
    try:
        lines = contents.decode("utf-8", errors="strict").splitlines()
    except UnicodeError:
        _fail(code)
    values: dict[str, Any] = {}
    authority_paths: list[str] = []
    in_authorities = False
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - "):
            if not in_authorities:
                _fail(code)
            authority_paths.append(_scalar(line[4:], code))
            continue
        if line != line.lstrip() or ":" not in line:
            _fail(code)
        key, raw = line.split(":", 1)
        if _YAML_KEY.fullmatch(key) is None or key in values:
            _fail(code)
        if key == "authorities":
            if raw.strip():
                _fail(code)
            values[key] = authority_paths
            in_authorities = True
        else:
            if in_authorities:
                _fail(code)
            values[key] = _scalar(raw, code)
    if (
        set(values) != _CORPUS_FIELDS
        or values["schema_version"] != "1"
        or _IDENTIFIER.fullmatch(values["corpus_id"]) is None
        or not authority_paths
        or len(authority_paths) != len(set(authority_paths))
    ):
        _fail(code)
    return values["corpus_id"], tuple(authority_paths)


def _iso_date(value: str, code: str) -> None:
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        _fail(code)
    if parsed.isoformat() != value:
        _fail(code)


def _load_source(
    invocation: ValidatedInvocation, source_yaml_path: str
) -> SourceDocumentation:
    path = _required_path(
        invocation,
        source_yaml_path,
        missing_code="authority-documentation-unavailable",
    )
    contents = _read(path, _MAX_DOCUMENTATION_BYTES, "invalid-source-documentation")
    values = _flat_yaml(contents, _SOURCE_FIELDS, "invalid-source-documentation")
    if (
        _IDENTIFIER.fullmatch(values["source_id"]) is None
        or _SHA256.fullmatch(values["sha256"]) is None
        or not values["retrieved_from"].startswith(("https://", "http://"))
    ):
        _fail("invalid-source-documentation")
    _iso_date(values["checked_through"], "invalid-source-documentation")
    return SourceDocumentation(
        source_id=values["source_id"],
        path=values["path"],
        sha256=values["sha256"],
        checked_through=values["checked_through"],
        retrieved_from=values["retrieved_from"],
        yaml_path=source_yaml_path,
        yaml_sha256=hashlib.sha256(contents).hexdigest(),
    )


def _load_authority(
    invocation: ValidatedInvocation, authority_yaml_path: str
) -> AuthorityRecord:
    yaml_path = _required_path(
        invocation,
        authority_yaml_path,
        missing_code="authority-documentation-unavailable",
    )
    yaml_bytes = _read(
        yaml_path, _MAX_DOCUMENTATION_BYTES, "invalid-authority-documentation"
    )
    values = _flat_yaml(
        yaml_bytes, _AUTHORITY_FIELDS, "invalid-authority-documentation"
    )
    source = _load_source(invocation, values["source_yaml_path"])
    document_path = _required_path(
        invocation,
        values["document_path"],
        missing_code="authority-content-unavailable",
    )
    if not document_path.is_file():
        _fail("invalid-authority-documentation")
    document_bytes = _read(
        document_path,
        invocation.runtime["max_input_bytes"],
        "invalid-authority-documentation",
    )
    digest = hashlib.sha256(document_bytes).hexdigest()
    if digest != values["sha256"] or digest != source.sha256:
        _fail("authority-content-mismatch")
    if source.path != values["document_path"]:
        _fail("invalid-authority-documentation")
    _iso_date(values["decision_date"], "invalid-authority-documentation")
    if (
        _IDENTIFIER.fullmatch(values["authority_id"]) is None
        or _SHA256.fullmatch(values["sha256"]) is None
        or values["publication_status"] not in {"published", "unpublished"}
        or values["precedential_status"]
        not in {"precedential", "nonprecedential", "unknown"}
        or values["binding_status"] not in {"binding", "persuasive", "nonbinding"}
        or values["event_date_status"] not in {"pre-event", "post-event", "unknown"}
        or values["later_history_status"] not in {"checked", "stale", "unknown"}
        or values["rule_of_orderliness_status"]
        not in {"checked", "not-applicable", "unknown"}
        or values["text_layer_status"] not in {"usable", "unusable"}
    ):
        _fail("invalid-authority-documentation")
    return AuthorityRecord(
        authority_id=values["authority_id"],
        citation=values["citation"],
        document_path=values["document_path"],
        source=source,
        sha256=values["sha256"],
        court=values["court"],
        decision_date=values["decision_date"],
        publication_status=values["publication_status"],
        precedential_status=values["precedential_status"],
        binding_status=values["binding_status"],
        event_date_status=values["event_date_status"],
        later_history_status=values["later_history_status"],
        rule_of_orderliness_status=values["rule_of_orderliness_status"],
        proposition=values["proposition"],
        quotation=values["quotation"],
        pinpoint=values["pinpoint"],
        text_layer_status=values["text_layer_status"],
        yaml_path=authority_yaml_path,
        yaml_sha256=hashlib.sha256(yaml_bytes).hexdigest(),
        document_bytes=document_bytes,
    )


def load_verified_authority_corpus(
    invocation: ValidatedInvocation, corpus_documentation_path: str
) -> AuthorityCorpus:
    """Load one selected corpus YAML and its exact authority bytes."""

    if (
        not isinstance(invocation, ValidatedInvocation)
        or tuple(role for role, _root in invocation.inputs) != _ROLES
        or invocation.operation != "audit"
        or invocation.internet != "disabled"
        or invocation.target is None
        or invocation.target[0] != "filing-source"
    ):
        _fail("invalid-authority-audit-invocation")
    corpus_path = _required_path(
        invocation,
        corpus_documentation_path,
        missing_code="corpus-documentation-unavailable",
    )
    corpus_bytes = _read(
        corpus_path, _MAX_DOCUMENTATION_BYTES, "invalid-corpus-documentation"
    )
    corpus_id, authority_paths = _corpus_yaml(corpus_bytes)
    authorities = tuple(
        _load_authority(invocation, authority_path)
        for authority_path in authority_paths
    )
    if (
        len({authority.authority_id for authority in authorities}) != len(authorities)
        or len({authority.citation for authority in authorities}) != len(authorities)
    ):
        _fail("invalid-corpus-documentation")
    return AuthorityCorpus(
        corpus_id=corpus_id,
        authorities=authorities,
        yaml_path=corpus_documentation_path,
        yaml_sha256=hashlib.sha256(corpus_bytes).hexdigest(),
    )
