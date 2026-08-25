"""Deterministic police-policy source record planning and validation."""

from __future__ import annotations

import hashlib
import re
from datetime import date
from pathlib import PurePosixPath
from typing import Any

import yaml


_IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
_URL = re.compile(r"^https?://[^\s/@]+(?::\d+)?(?:/[^\s]*)?$")
_SOURCE_FIELDS = frozenset(
    {
        "source_id",
        "artifact_path",
        "source_documentation_path",
        "artifact_bytes",
        "source_url",
        "query",
        "filters",
        "checked_date",
        "retrieved_at",
        "result_identity",
        "classification",
        "adoption_relationship",
        "review_state",
        "retrieval_result",
        "effective_date",
        "limitations",
        "duplicate_of",
    }
)
_SOURCE_DOCUMENT_FIELDS = frozenset(
    {
        "version",
        "source_id",
        "artifact_path",
        "sha256",
        "source_url",
        "query",
        "filters",
        "checked_date",
        "retrieved_at",
        "result_identity",
        "classification",
        "adoption_relationship",
        "review_state",
        "retrieval_result",
        "effective_date",
        "limitations",
        "duplicate_of",
    }
)
_EFFECTIVE_FIELDS = frozenset({"status", "date", "evidence", "gap"})
_GAP_FIELDS = frozenset(
    {
        "gap_id",
        "gap_type",
        "source_system_id",
        "query",
        "filters",
        "checked_date",
        "coverage_limit",
    }
)
_CANDIDATE_FIELDS = frozenset(
    {
        "source_id",
        "source_documentation_path",
        "artifact_path",
        "sha256",
        "classification",
        "review_state",
    }
)
_CLASSIFICATIONS = frozenset(
    {
        "adopted_policy",
        "statute",
        "regulation",
        "collective_bargaining",
        "accreditation",
        "model_policy",
        "training_material",
        "form",
        "guidance",
        "comparison_source",
    }
)
_ADOPTION = frozenset({"documented", "uncertain", "rejected", "not_applicable"})
_REVIEW = frozenset({"candidate", "rejected"})
_EFFECTIVE_STATUS = frozenset({"documented", "uncertain", "missing"})
_GAP_TYPES = frozenset(
    {"empty", "incomplete", "inaccessible", "paid", "ambiguous", "out_of_scope"}
)
_RESERVED = frozenset({"temp", ".skill-runs"})
_MAX_TEXT = 4096


class PolicySourceError(ValueError):
    """A stable bounded policy-source validation failure."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _fail(code: str) -> None:
    raise PolicySourceError(code)


def _exact(value: Any, fields: frozenset[str], code: str) -> dict[str, Any]:
    if type(value) is not dict or set(value) != fields:
        _fail(code)
    return value


def _text(value: Any, code: str, *, allow_empty: bool = False) -> str:
    if (
        not isinstance(value, str)
        or len(value) > _MAX_TEXT
        or (not allow_empty and not value.strip())
        or any(ord(character) < 32 and character not in "\t\n\r" for character in value)
    ):
        _fail(code)
    return value


def _identifier(value: Any, code: str) -> str:
    if not isinstance(value, str) or _IDENTIFIER.fullmatch(value) is None:
        _fail(code)
    return value


def _date(value: Any, code: str) -> str:
    if not isinstance(value, str):
        _fail(code)
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        _fail(code)
    if parsed.isoformat() != value:
        _fail(code)
    return value


def _relative(value: Any, code: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        _fail(code)
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or any(part in {"", ".", ".."} for part in path.parts)
        or path.parts[0] in _RESERVED
    ):
        _fail(code)
    return path.as_posix()


def _strings(value: Any, code: str) -> list[str]:
    if type(value) is not list:
        _fail(code)
    result = [_text(item, code) for item in value]
    if len(result) != len(set(result)):
        _fail(code)
    return result


def _effective(value: Any, code: str) -> dict[str, Any]:
    record = _exact(value, _EFFECTIVE_FIELDS, code)
    status = record["status"]
    if status not in _EFFECTIVE_STATUS:
        _fail(code)
    effective_date = record["date"]
    evidence = record["evidence"]
    gap = record["gap"]
    if status == "documented":
        _date(effective_date, code)
        _text(evidence, code)
        if gap is not None:
            _fail(code)
    else:
        if effective_date is not None:
            _date(effective_date, code)
        if evidence is not None:
            _text(evidence, code)
        _text(gap, code)
    return {
        "status": status,
        "date": effective_date,
        "evidence": evidence,
        "gap": gap,
    }


def _url(value: Any, code: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) > 2048
        or _URL.fullmatch(value) is None
        or ".." in value.split("/", 3)[2]
    ):
        _fail(code)
    return value


def _source_document(source: Any, checked_through: str) -> tuple[dict[str, Any], str]:
    record = _exact(source, _SOURCE_FIELDS, "invalid-source-record")
    source_id = _identifier(record["source_id"], "invalid-source-record")
    artifact_path = _relative(record["artifact_path"], "invalid-source-record")
    documentation_path = _relative(
        record["source_documentation_path"], "invalid-source-record"
    )
    artifact_logical = PurePosixPath(artifact_path)
    documentation_logical = PurePosixPath(documentation_path)
    if (
        artifact_logical.parts[0] != "sources"
        or documentation_logical.parts[0] != "sources"
        or artifact_logical.parent != documentation_logical.parent
        or not documentation_logical.name.endswith(".SOURCE.yaml")
        or artifact_path == documentation_path
    ):
        _fail("invalid-source-record")
    contents = record["artifact_bytes"]
    if not isinstance(contents, bytes) or not contents:
        _fail("invalid-source-record")
    checked_date = _date(record["checked_date"], "invalid-source-record")
    if checked_date > checked_through:
        _fail("invalid-source-record")
    if not isinstance(record["retrieved_at"], str) or _UTC.fullmatch(record["retrieved_at"]) is None:
        _fail("invalid-source-record")
    classification = record["classification"]
    adoption = record["adoption_relationship"]
    review = record["review_state"]
    if (
        classification not in _CLASSIFICATIONS
        or adoption not in _ADOPTION
        or review not in _REVIEW
        or record["retrieval_result"] != "retrieved"
    ):
        _fail("invalid-source-record")
    filters = _strings(record["filters"], "invalid-source-record")
    limitations = _strings(record["limitations"], "invalid-source-record")
    duplicate_of = [
        _identifier(value, "invalid-source-record")
        for value in _strings(record["duplicate_of"], "invalid-source-record")
    ]
    if source_id in duplicate_of:
        _fail("invalid-source-record")
    document = {
        "version": 1,
        "source_id": source_id,
        "artifact_path": artifact_path,
        "sha256": hashlib.sha256(contents).hexdigest(),
        "source_url": _url(record["source_url"], "invalid-source-record"),
        "query": _text(record["query"], "invalid-source-record"),
        "filters": filters,
        "checked_date": checked_date,
        "retrieved_at": record["retrieved_at"],
        "result_identity": _text(record["result_identity"], "invalid-source-record"),
        "classification": classification,
        "adoption_relationship": adoption,
        "review_state": review,
        "retrieval_result": "retrieved",
        "effective_date": _effective(record["effective_date"], "invalid-source-record"),
        "limitations": limitations,
        "duplicate_of": duplicate_of,
    }
    return document, documentation_path


def _gap(gap: Any, checked_through: str) -> dict[str, Any]:
    record = _exact(gap, _GAP_FIELDS, "invalid-gap-record")
    checked_date = _date(record["checked_date"], "invalid-gap-record")
    if checked_date > checked_through or record["gap_type"] not in _GAP_TYPES:
        _fail("invalid-gap-record")
    return {
        "gap_id": _identifier(record["gap_id"], "invalid-gap-record"),
        "gap_type": record["gap_type"],
        "source_system_id": _identifier(
            record["source_system_id"], "invalid-gap-record"
        ),
        "query": _text(record["query"], "invalid-gap-record"),
        "filters": _strings(record["filters"], "invalid-gap-record"),
        "checked_date": checked_date,
        "coverage_limit": _text(record["coverage_limit"], "invalid-gap-record"),
    }


def _yaml_bytes(document: dict[str, Any]) -> bytes:
    return yaml.safe_dump(
        document,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    ).encode("utf-8")


def build_collection_plan(
    sources: list[dict[str, Any]], gaps: list[dict[str, Any]], checked_through: str
) -> dict[str, Any]:
    """Return deterministic output-relative artifacts without writing them."""
    if type(sources) is not list or type(gaps) is not list:
        _fail("invalid-collection")
    checked_through = _date(checked_through, "invalid-collection")
    prepared = [_source_document(source, checked_through) for source in sources]
    prepared.sort(key=lambda item: item[0]["source_id"])
    source_ids = [item[0]["source_id"] for item in prepared]
    documentation_paths = [item[1] for item in prepared]
    artifact_paths = [item[0]["artifact_path"] for item in prepared]
    if (
        len(source_ids) != len(set(source_ids))
        or len(documentation_paths) != len(set(documentation_paths))
        or len(artifact_paths) != len(set(artifact_paths))
        or set(documentation_paths) & set(artifact_paths)
    ):
        _fail("duplicate-source")
    known_ids = set(source_ids)
    if any(
        duplicate not in known_ids
        for document, _ in prepared
        for duplicate in document["duplicate_of"]
    ):
        _fail("invalid-source-record")

    original_by_id = {source["source_id"]: source for source in sources}
    artifacts = []
    candidates = []
    for document, documentation_path in prepared:
        contents = bytes(original_by_id[document["source_id"]]["artifact_bytes"])
        artifacts.append({"path": document["artifact_path"], "bytes": contents})
        artifacts.append({"path": documentation_path, "bytes": _yaml_bytes(document)})
        candidates.append(
            {
                "source_id": document["source_id"],
                "source_documentation_path": documentation_path,
                "artifact_path": document["artifact_path"],
                "sha256": document["sha256"],
                "classification": document["classification"],
                "review_state": document["review_state"],
            }
        )

    gap_records = [_gap(value, checked_through) for value in gaps]
    gap_records.sort(key=lambda value: value["gap_id"])
    gap_ids = [value["gap_id"] for value in gap_records]
    if len(gap_ids) != len(set(gap_ids)):
        _fail("duplicate-gap")
    artifacts.extend(
        [
            {
                "path": "policy-source-candidates.yaml",
                "bytes": _yaml_bytes(
                    {
                        "version": 1,
                        "checked_through": checked_through,
                        "sources": candidates,
                    }
                ),
            },
            {
                "path": "policy-source-gaps.yaml",
                "bytes": _yaml_bytes(
                    {
                        "version": 1,
                        "checked_through": checked_through,
                        "gaps": gap_records,
                    }
                ),
            },
        ]
    )
    plan = {"checked_through": checked_through, "artifacts": artifacts}
    validate_collection_plan(plan)
    return plan


def _load_yaml(contents: bytes, code: str) -> dict[str, Any]:
    try:
        document = yaml.safe_load(contents)
    except (UnicodeError, yaml.YAMLError):
        _fail(code)
    if type(document) is not dict:
        _fail(code)
    return document


def _validate_source_yaml(document: Any, checked_through: str) -> dict[str, Any]:
    record = _exact(document, _SOURCE_DOCUMENT_FIELDS, "invalid-source-yaml")
    if record["version"] != 1:
        _fail("invalid-source-yaml")
    source_id = _identifier(record["source_id"], "invalid-source-yaml")
    artifact_path = _relative(record["artifact_path"], "invalid-source-yaml")
    if PurePosixPath(artifact_path).parts[0] != "sources":
        _fail("invalid-source-yaml")
    sha256 = record["sha256"]
    if not isinstance(sha256, str) or _SHA256.fullmatch(sha256) is None:
        _fail("invalid-source-yaml")
    checked_date = _date(record["checked_date"], "invalid-source-yaml")
    if checked_date > checked_through:
        _fail("invalid-source-yaml")
    if not isinstance(record["retrieved_at"], str) or _UTC.fullmatch(record["retrieved_at"]) is None:
        _fail("invalid-source-yaml")
    if (
        record["classification"] not in _CLASSIFICATIONS
        or record["adoption_relationship"] not in _ADOPTION
        or record["review_state"] not in _REVIEW
        or record["retrieval_result"] != "retrieved"
    ):
        _fail("invalid-source-yaml")
    _url(record["source_url"], "invalid-source-yaml")
    _text(record["query"], "invalid-source-yaml")
    _strings(record["filters"], "invalid-source-yaml")
    _text(record["result_identity"], "invalid-source-yaml")
    _effective(record["effective_date"], "invalid-source-yaml")
    _strings(record["limitations"], "invalid-source-yaml")
    duplicates = [
        _identifier(value, "invalid-source-yaml")
        for value in _strings(record["duplicate_of"], "invalid-source-yaml")
    ]
    if source_id in duplicates:
        _fail("invalid-source-yaml")
    return record


def validate_collection_plan(plan: Any) -> bool:
    """Validate one complete artifact plan and every documented hash."""
    value = _exact(plan, frozenset({"checked_through", "artifacts"}), "invalid-plan")
    checked_through = _date(value["checked_through"], "invalid-plan")
    if type(value["artifacts"]) is not list:
        _fail("invalid-plan")
    by_path = {}
    for artifact in value["artifacts"]:
        item = _exact(artifact, frozenset({"path", "bytes"}), "invalid-plan")
        path = _relative(item["path"], "invalid-plan")
        if path in by_path or not isinstance(item["bytes"], bytes):
            _fail("invalid-plan")
        by_path[path] = item["bytes"]
    fixed_paths = {"policy-source-candidates.yaml", "policy-source-gaps.yaml"}
    if not fixed_paths.issubset(by_path):
        _fail("invalid-plan")

    candidates = _load_yaml(
        by_path["policy-source-candidates.yaml"], "invalid-candidate-index"
    )
    if (
        set(candidates) != {"version", "checked_through", "sources"}
        or candidates["version"] != 1
        or candidates["checked_through"] != checked_through
        or type(candidates["sources"]) is not list
    ):
        _fail("invalid-candidate-index")
    source_ids = []
    expected_paths = set(fixed_paths)
    for candidate in candidates["sources"]:
        entry = _exact(candidate, _CANDIDATE_FIELDS, "invalid-candidate-index")
        source_id = _identifier(entry["source_id"], "invalid-candidate-index")
        documentation_path = _relative(
            entry["source_documentation_path"], "invalid-candidate-index"
        )
        artifact_path = _relative(entry["artifact_path"], "invalid-candidate-index")
        if documentation_path not in by_path or artifact_path not in by_path:
            _fail("invalid-candidate-index")
        document = _validate_source_yaml(
            _load_yaml(by_path[documentation_path], "invalid-source-yaml"),
            checked_through,
        )
        if (
            document["source_id"] != source_id
            or document["artifact_path"] != artifact_path
            or document["sha256"] != entry["sha256"]
            or document["classification"] != entry["classification"]
            or document["review_state"] != entry["review_state"]
        ):
            _fail("invalid-candidate-index")
        if hashlib.sha256(by_path[artifact_path]).hexdigest() != document["sha256"]:
            _fail("hash-mismatch")
        source_ids.append(source_id)
        expected_paths.update({documentation_path, artifact_path})
    if source_ids != sorted(source_ids) or len(source_ids) != len(set(source_ids)):
        _fail("invalid-candidate-index")

    gaps = _load_yaml(by_path["policy-source-gaps.yaml"], "invalid-gap-index")
    if (
        set(gaps) != {"version", "checked_through", "gaps"}
        or gaps["version"] != 1
        or gaps["checked_through"] != checked_through
        or type(gaps["gaps"]) is not list
    ):
        _fail("invalid-gap-index")
    gap_records = [_gap(record, checked_through) for record in gaps["gaps"]]
    gap_ids = [record["gap_id"] for record in gap_records]
    if gap_ids != sorted(gap_ids) or len(gap_ids) != len(set(gap_ids)):
        _fail("invalid-gap-index")
    if set(by_path) != expected_paths:
        _fail("invalid-plan")
    return True
