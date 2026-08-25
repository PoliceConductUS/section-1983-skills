"""Deterministic policy requirement planning over validated in-memory data."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import PurePosixPath

import yaml


_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_SOURCE_FIELDS = {
    "version", "source_id", "artifact_path", "sha256", "source_url", "query",
    "filters", "checked_date", "retrieved_at", "result_identity", "classification",
    "adoption_relationship", "review_state", "retrieval_result", "effective_date",
    "limitations", "duplicate_of",
}
_SELECTED_FIELDS = {"source_documentation_path", "source_yaml_bytes", "artifact_bytes", "approval"}
_REQ_FIELDS = {
    "requirement_id", "department_id", "policy_id", "source_id", "effective",
    "quotation", "pinpoint", "actor", "triggers", "requirement_type", "action",
    "exceptions", "definitions", "dependencies", "cross_references",
    "documentation_or_review", "gaps", "operative_markers",
}
_MARKERS = {"condition_present", "exception_present", "discretion_present", "cross_reference_present"}
_TYPES = {"mandatory", "prohibited", "permitted", "discretionary"}
_GAP_TYPES = {
    "missing_page", "illegible_text", "unresolved_history", "uncertain_adoption",
    "ambiguous_cross_reference", "uncertain_effective_date",
}


class PolicyRequirementError(ValueError):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def _fail(code):
    raise PolicyRequirementError(code)


def _exact(value, fields, code):
    if type(value) is not dict or set(value) != set(fields):
        _fail(code)
    return value


def _identifier(value, code):
    if not isinstance(value, str) or _ID.fullmatch(value) is None:
        _fail(code)
    return value


def _text(value, code):
    if not isinstance(value, str) or not value.strip() or len(value) > 4096:
        _fail(code)
    return value


def _iso_date(value, code):
    if not isinstance(value, str):
        _fail(code)
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        _fail(code)
    if parsed.isoformat() != value:
        _fail(code)
    return value


def _relative(value, code):
    if not isinstance(value, str) or not value or "\\" in value:
        _fail(code)
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        _fail(code)
    return path.as_posix()


def _strings(value, code):
    if type(value) is not list:
        _fail(code)
    result = [_text(item, code) for item in value]
    if len(result) != len(set(result)):
        _fail(code)
    return result


def _selected_source(value):
    selection = _exact(value, _SELECTED_FIELDS, "invalid-selected-source")
    metadata_path = _relative(selection["source_documentation_path"], "invalid-selected-source")
    if not metadata_path.endswith(".SOURCE.yaml"):
        _fail("invalid-selected-source")
    if not isinstance(selection["source_yaml_bytes"], bytes) or not isinstance(selection["artifact_bytes"], bytes):
        _fail("invalid-selected-source")
    try:
        source = yaml.safe_load(selection["source_yaml_bytes"])
    except yaml.YAMLError:
        _fail("invalid-source-yaml")
    source = _exact(source, _SOURCE_FIELDS, "invalid-source-yaml")
    if source["version"] != 1:
        _fail("invalid-source-yaml")
    source_id = _identifier(source["source_id"], "invalid-source-yaml")
    artifact_path = _relative(source["artifact_path"], "invalid-source-yaml")
    if PurePosixPath(artifact_path).parent != PurePosixPath(metadata_path).parent:
        _fail("invalid-source-yaml")
    sha256 = hashlib.sha256(selection["artifact_bytes"]).hexdigest()
    if source["sha256"] != sha256:
        _fail("source-hash-mismatch")
    approval = _exact(selection["approval"], {"state", "approved_on", "approved_by"}, "invalid-approval")
    if approval["state"] != "approved_for_analysis":
        _fail("invalid-approval")
    _iso_date(approval["approved_on"], "invalid-approval")
    _text(approval["approved_by"], "invalid-approval")
    if source["classification"] != "adopted_policy" or source["adoption_relationship"] != "documented":
        _fail("source-not-adopted-policy")
    effective = _exact(source["effective_date"], {"status", "date", "evidence", "gap"}, "invalid-source-yaml")
    if effective["status"] != "documented" or effective["gap"] is not None:
        _fail("uncertain-effective-date")
    effective_date = _iso_date(effective["date"], "invalid-source-yaml")
    _text(effective["evidence"], "invalid-source-yaml")
    try:
        source_text = selection["artifact_bytes"].decode("utf-8")
    except UnicodeError:
        _fail("illegible-source")
    return {"source_id": source_id, "artifact_path": artifact_path, "sha256": sha256, "effective_date": effective_date, "text": source_text}


def _scope(value):
    scope = _exact(value, {"start_date", "end_date"}, "invalid-scope")
    start = _iso_date(scope["start_date"], "invalid-scope")
    end = _iso_date(scope["end_date"], "invalid-scope")
    if end < start:
        _fail("invalid-scope")
    return {"start_date": start, "end_date": end}


def _requirement(value, sources, scope):
    record = _exact(value, _REQ_FIELDS, "invalid-requirement")
    source_id = _identifier(record["source_id"], "invalid-requirement")
    if source_id not in sources:
        _fail("unresolved-source")
    source = sources[source_id]
    effective = _exact(record["effective"], {"start_date", "end_date", "gap"}, "invalid-requirement")
    start = _iso_date(effective["start_date"], "invalid-requirement")
    end = effective["end_date"]
    if end is not None:
        end = _iso_date(end, "invalid-requirement")
        if end < start:
            _fail("invalid-requirement")
    if effective["gap"] is not None:
        _text(effective["gap"], "invalid-requirement")
    if start < source["effective_date"]:
        _fail("retroactive-requirement")
    if start > scope["end_date"] or (end is not None and end < scope["start_date"]):
        _fail("requirement-outside-scope")
    quotation = _text(record["quotation"], "invalid-requirement")
    if quotation not in source["text"]:
        _fail("quotation-not-found")
    requirement_type = record["requirement_type"]
    if requirement_type not in _TYPES:
        _fail("invalid-requirement")
    triggers = _strings(record["triggers"], "invalid-requirement")
    exceptions = _strings(record["exceptions"], "invalid-requirement")
    cross_references = _strings(record["cross_references"], "invalid-requirement")
    markers = _exact(record["operative_markers"], _MARKERS, "invalid-requirement")
    if any(type(markers[field]) is not bool for field in _MARKERS):
        _fail("invalid-requirement")
    if (markers["condition_present"] != bool(triggers) or markers["exception_present"] != bool(exceptions) or markers["cross_reference_present"] != bool(cross_references) or markers["discretion_present"] != (requirement_type == "discretionary")):
        _fail("lost-operative-limit")
    return {
        "requirement_id": _identifier(record["requirement_id"], "invalid-requirement"),
        "department_id": _identifier(record["department_id"], "invalid-requirement"),
        "policy_id": _identifier(record["policy_id"], "invalid-requirement"),
        "source_id": source_id,
        "effective": {"start_date": start, "end_date": end, "gap": effective["gap"]},
        "quotation": quotation,
        "pinpoint": _text(record["pinpoint"], "invalid-requirement"),
        "source_path": source["artifact_path"],
        "source_sha256": source["sha256"],
        "actor": _text(record["actor"], "invalid-requirement"),
        "triggers": triggers,
        "requirement_type": requirement_type,
        "action": _text(record["action"], "invalid-requirement"),
        "exceptions": exceptions,
        "definitions": _strings(record["definitions"], "invalid-requirement"),
        "dependencies": _strings(record["dependencies"], "invalid-requirement"),
        "cross_references": cross_references,
        "documentation_or_review": _strings(record["documentation_or_review"], "invalid-requirement"),
        "gaps": _strings(record["gaps"], "invalid-requirement"),
        "operative_markers": dict(markers),
    }


def _gap(value, source_ids):
    record = _exact(value, {"gap_id", "gap_type", "source_id", "location", "description"}, "invalid-gap")
    if record["gap_type"] not in _GAP_TYPES:
        _fail("invalid-gap")
    source_id = _identifier(record["source_id"], "invalid-gap")
    if source_id not in source_ids:
        _fail("unresolved-source")
    return {"gap_id": _identifier(record["gap_id"], "invalid-gap"), "gap_type": record["gap_type"], "source_id": source_id, "location": _text(record["location"], "invalid-gap"), "description": _text(record["description"], "invalid-gap")}


def _yaml(value):
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=True).encode("utf-8")


def build_analysis_plan(selected_sources, requirements, gaps, scope):
    if type(selected_sources) is not list or type(requirements) is not list or type(gaps) is not list:
        _fail("invalid-analysis")
    scope = _scope(scope)
    selected = sorted((_selected_source(value) for value in selected_sources), key=lambda value: value["source_id"])
    source_ids = [value["source_id"] for value in selected]
    if len(source_ids) != len(set(source_ids)):
        _fail("duplicate-source")
    sources = {value["source_id"]: value for value in selected}
    requirement_records = sorted((_requirement(value, sources, scope) for value in requirements), key=lambda value: value["requirement_id"])
    requirement_ids = [value["requirement_id"] for value in requirement_records]
    if len(requirement_ids) != len(set(requirement_ids)):
        _fail("duplicate-requirement")
    gap_records = sorted((_gap(value, set(source_ids)) for value in gaps), key=lambda value: value["gap_id"])
    gap_ids = [value["gap_id"] for value in gap_records]
    if len(gap_ids) != len(set(gap_ids)):
        _fail("duplicate-gap")
    lines = ["# Policy analysis", "", f"Requirements: {len(requirement_records)}", f"Gaps: {len(gap_records)}", ""]
    lines.extend(f"- {value['requirement_id']}: {value['requirement_type']} — {value['action']}" for value in requirement_records)
    lines.extend(f"- GAP {value['gap_id']}: {value['description']}" for value in gap_records)
    validation = {"schema_version": 1, "valid": True, "source_ids": source_ids, "source_hashes": {value["source_id"]: value["sha256"] for value in selected}, "requirement_ids": requirement_ids, "gap_ids": gap_ids}
    artifacts = [
        {"path": "policy-requirements.yaml", "bytes": _yaml({"version": 1, "scope": scope, "requirements": requirement_records}), "internet_sources": []},
        {"path": "policy-analysis-gaps.yaml", "bytes": _yaml({"version": 1, "scope": scope, "gaps": gap_records}), "internet_sources": []},
        {"path": "policy-analysis.md", "bytes": ("\n".join(lines) + "\n").encode(), "internet_sources": []},
        {"path": "policy-analysis-validation.json", "bytes": (json.dumps(validation, sort_keys=True, separators=(",", ":")) + "\n").encode(), "internet_sources": []},
    ]
    return {"scope": scope, "artifacts": artifacts}
