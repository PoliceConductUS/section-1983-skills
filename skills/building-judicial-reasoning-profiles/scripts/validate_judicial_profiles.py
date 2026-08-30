#!/usr/bin/env python3
"""Deterministic install-local Judicial Reasoning Profile validation."""

from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timezone
from typing import Any


_IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_SOURCE_CLASSES = frozenset(
    {
        "revealed_reasoning",
        "stated_philosophy",
        "self_presentation",
        "court_compliance",
    }
)
_ATTRIBUTIONS = frozenset(
    {"independent_reasoning", "adoption_only", "recommendation", "outcome_only"}
)
_COMPARISON_STATES = frozenset(
    {"aligned", "tension", "divergent", "indeterminate"}
)
_PROHIBITED_CHARACTERIZATION = re.compile(
    r"\b(?:averag(?:e|ing)|score|psycholog(?:y|ical)|hypocri(?:sy|tical)|"
    r"prefer(?:s|ence|red)?|bias(?:ed)?|personality|manipulat(?:e|ion)|exploit|"
    r"predict(?:s|ed|ion)?|likely\s+outcome)\b",
    re.IGNORECASE,
)
_TOP_LEVEL = {
    "schema_version",
    "profile_id",
    "checked_through",
    "judge_identity",
    "court_scope",
    "records",
    "comparisons",
    "neutral_transfers",
    "assumptions",
    "gaps",
    "validation",
}


class ProfileError(ValueError):
    """A bounded Judicial Reasoning Profile contract failure."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _fail(code: str) -> None:
    raise ProfileError(code)


def _object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            _fail("invalid-profile-json")
        value[key] = item
    return value


def _identifier(value: Any) -> bool:
    return isinstance(value, str) and _IDENTIFIER.fullmatch(value) is not None


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


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


def _string_list(value: Any) -> bool:
    return (
        type(value) is list
        and all(_nonempty(item) for item in value)
        and len(value) == len(set(value))
    )


def _identifier_list(value: Any, *, required: bool = False) -> bool:
    return (
        type(value) is list
        and (not required or bool(value))
        and all(_identifier(item) for item in value)
        and len(value) == len(set(value))
    )


def _validate_identity(value: Any) -> None:
    required = {"subject_id", "display_name", "fictional", "source_id", "checked_on"}
    if (
        type(value) is not dict
        or set(value) != required
        or not _identifier(value["subject_id"])
        or not _nonempty(value["display_name"])
        or type(value["fictional"]) is not bool
        or not _identifier(value["source_id"])
        or not _date(value["checked_on"])
    ):
        _fail("invalid-profile-identity")


def _validate_court_scope(value: Any) -> None:
    required = {
        "court_id",
        "jurisdiction",
        "tenure_start",
        "tenure_end",
        "source_id",
        "checked_on",
    }
    if (
        type(value) is not dict
        or set(value) != required
        or not _identifier(value["court_id"])
        or not _nonempty(value["jurisdiction"])
        or any(
            item is not None and not _date(item)
            for item in (value["tenure_start"], value["tenure_end"])
        )
        or not _identifier(value["source_id"])
        or not _date(value["checked_on"])
    ):
        _fail("invalid-profile-court-scope")
    if (
        value["tenure_start"] is not None
        and value["tenure_end"] is not None
        and value["tenure_end"] < value["tenure_start"]
    ):
        _fail("invalid-profile-court-scope")


def _validate_record(value: Any) -> dict[str, Any]:
    required = {
        "id",
        "source_class",
        "proposition",
        "source_id",
        "source_date",
        "issue",
        "posture",
        "attribution",
        "permitted_uses",
        "prohibited_uses",
    }
    if (
        type(value) is not dict
        or set(value) != required
        or not _identifier(value["id"])
        or value["source_class"] not in _SOURCE_CLASSES
        or not _nonempty(value["proposition"])
        or not _identifier(value["source_id"])
        or not _date(value["source_date"])
        or not _identifier(value["issue"])
        or not _identifier(value["posture"])
        or value["attribution"] not in _ATTRIBUTIONS
        or not _string_list(value["permitted_uses"])
        or not _string_list(value["prohibited_uses"])
    ):
        _fail("invalid-profile-record")
    return value


def _validate_comparison(value: Any, records: dict[str, dict[str, Any]]) -> None:
    required = {
        "id",
        "left_record_id",
        "left_proposition",
        "left_source_id",
        "left_source_date",
        "left_issue",
        "left_posture",
        "right_record_id",
        "right_proposition",
        "right_source_id",
        "right_source_date",
        "right_issue",
        "right_posture",
        "similarities",
        "differences",
        "state",
    }
    if (
        type(value) is not dict
        or set(value) != required
        or not _identifier(value["id"])
        or value["left_record_id"] == value["right_record_id"]
        or value["state"] not in _COMPARISON_STATES
        or not _string_list(value["similarities"])
        or not _string_list(value["differences"])
    ):
        _fail("invalid-profile-comparison")
    left = records.get(value["left_record_id"])
    right = records.get(value["right_record_id"])
    if left is None or right is None:
        _fail("unknown-comparison-record")
    copied = (
        ("left_proposition", left["proposition"]),
        ("left_source_id", left["source_id"]),
        ("left_source_date", left["source_date"]),
        ("left_issue", left["issue"]),
        ("left_posture", left["posture"]),
        ("right_proposition", right["proposition"]),
        ("right_source_id", right["source_id"]),
        ("right_source_date", right["source_date"]),
        ("right_issue", right["issue"]),
        ("right_posture", right["posture"]),
    )
    if any(value[field] != expected for field, expected in copied):
        _fail("comparison-record-mismatch")
    if any(
        _PROHIBITED_CHARACTERIZATION.search(item)
        for item in value["similarities"] + value["differences"]
    ):
        _fail("prohibited-profile-characterization")


def _validate_transfer(value: Any, records: dict[str, dict[str, Any]]) -> None:
    required = {"id", "issue", "posture", "instruction", "supporting_record_ids"}
    if (
        type(value) is not dict
        or set(value) != required
        or not _identifier(value["id"])
        or not _identifier(value["issue"])
        or not _identifier(value["posture"])
        or not _nonempty(value["instruction"])
        or not _identifier_list(value["supporting_record_ids"], required=True)
    ):
        _fail("invalid-neutral-transfer")
    if _PROHIBITED_CHARACTERIZATION.search(value["instruction"]):
        _fail("prohibited-profile-characterization")
    for record_id in value["supporting_record_ids"]:
        record = records.get(record_id)
        if (
            record is None
            or record["source_class"] != "revealed_reasoning"
            or record["attribution"] != "independent_reasoning"
            or record["issue"] != value["issue"]
            or record["posture"] != value["posture"]
        ):
            _fail("ineligible-neutral-transfer")


def _validate_annotations(value: Any, code: str) -> None:
    if type(value) is not list:
        _fail(code)
    ids = []
    for item in value:
        if (
            type(item) is not dict
            or set(item) != {"id", "description", "source_ids"}
            or not _identifier(item["id"])
            or not _nonempty(item["description"])
            or not _identifier_list(item["source_ids"])
        ):
            _fail(code)
        ids.append(item["id"])
    if len(ids) != len(set(ids)):
        _fail(code)


def _validate_result(value: Any) -> None:
    if (
        type(value) is not dict
        or set(value) != {"status", "validator", "version", "validated_at"}
        or value["status"] != "passed"
        or not _nonempty(value["validator"])
        or not _nonempty(value["version"])
        or not _timestamp(value["validated_at"])
    ):
        _fail("invalid-profile-validation")


def validate_profile_bytes(contents: bytes, *, max_bytes: int) -> dict[str, Any]:
    """Validate bounded UTF-8 JSON bytes and return the detached profile object."""
    if type(max_bytes) is not int or max_bytes < 0:
        _fail("invalid-profile-byte-limit")
    if not isinstance(contents, bytes):
        _fail("invalid-profile-bytes")
    if len(contents) > max_bytes:
        _fail("profile-byte-limit")
    try:
        value = json.loads(
            contents.decode("utf-8", errors="strict"), object_pairs_hook=_object
        )
    except ProfileError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        _fail("invalid-profile-json")
    if (
        type(value) is not dict
        or set(value) != _TOP_LEVEL
        or type(value["schema_version"]) is not int
        or value["schema_version"] != 1
        or not _identifier(value["profile_id"])
    ):
        _fail("invalid-profile-shape")
    if not _date(value["checked_through"]):
        _fail("invalid-profile-date")
    _validate_identity(value["judge_identity"])
    _validate_court_scope(value["court_scope"])
    if type(value["records"]) is not list:
        _fail("invalid-profile-records")
    records = [_validate_record(item) for item in value["records"]]
    record_by_id = {record["id"]: record for record in records}
    if len(record_by_id) != len(records):
        _fail("duplicate-profile-record")
    if type(value["comparisons"]) is not list:
        _fail("invalid-profile-comparisons")
    comparison_ids = []
    for comparison in value["comparisons"]:
        _validate_comparison(comparison, record_by_id)
        comparison_ids.append(comparison["id"])
    if len(comparison_ids) != len(set(comparison_ids)):
        _fail("duplicate-profile-comparison")
    if type(value["neutral_transfers"]) is not list:
        _fail("invalid-neutral-transfers")
    transfer_ids = []
    for transfer in value["neutral_transfers"]:
        _validate_transfer(transfer, record_by_id)
        transfer_ids.append(transfer["id"])
    if len(transfer_ids) != len(set(transfer_ids)):
        _fail("duplicate-neutral-transfer")
    _validate_annotations(value["assumptions"], "invalid-profile-assumptions")
    _validate_annotations(value["gaps"], "invalid-profile-gaps")
    _validate_result(value["validation"])
    return value


def main() -> int:
    try:
        value = validate_profile_bytes(sys.stdin.buffer.read(1_048_577), max_bytes=1_048_576)
    except ProfileError as error:
        print(json.dumps({"error": error.code}, sort_keys=True))
        return 1
    print(json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
