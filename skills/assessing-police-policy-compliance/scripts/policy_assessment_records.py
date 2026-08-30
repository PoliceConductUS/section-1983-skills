"""Deterministic policy-assessment planning over validated in-memory data."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import PurePosixPath

import yaml


_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_ROLES = (
    "policy-catalog",
    "actor",
    "event",
    "phase",
    "case-record",
    "assessment-scope",
)
_SOURCE_ROLES = {"actor", "event", "phase", "case-record"}
_SOURCE_TYPES = {
    "actor": "actor_record",
    "event": "event_record",
    "phase": "phase_record",
    "case-record": "case_record",
}
_CATALOG_FIELDS = {"requirements_yaml_bytes", "validation_json_bytes"}
_CATALOG_DOCUMENT_FIELDS = {"version", "scope", "requirements"}
_CATALOG_VALIDATION_FIELDS = {
    "schema_version",
    "valid",
    "source_ids",
    "source_hashes",
    "requirement_ids",
    "gap_ids",
}
_REQUIREMENT_FIELDS = {
    "requirement_id",
    "department_id",
    "policy_id",
    "source_id",
    "effective",
    "quotation",
    "pinpoint",
    "source_path",
    "source_sha256",
    "actor",
    "triggers",
    "requirement_type",
    "action",
    "exceptions",
    "definitions",
    "dependencies",
    "cross_references",
    "documentation_or_review",
    "gaps",
    "operative_markers",
}
_SOURCE_SELECTION_FIELDS = {
    "input_role",
    "source_documentation_path",
    "source_yaml_bytes",
    "artifact_bytes",
}
_SOURCE_DOCUMENT_FIELDS = {
    "version",
    "source_id",
    "artifact_path",
    "sha256",
    "source_type",
    "occurred_at",
    "limitations",
}
_ACTOR_FIELDS = {"actor_id", "display_name", "roles"}
_EVENT_FIELDS = {"event_id", "event_date", "description"}
_PHASE_FIELDS = {"phase_id", "event_id", "label", "sequence"}
_SCOPE_FIELDS = {
    "start_date",
    "end_date",
    "selected_requirement_ids",
    "selected_actor_ids",
    "selected_event_ids",
    "selected_phase_ids",
    "selected_source_paths",
}
_ASSESSMENT_FIELDS = {
    "assessment_id",
    "requirement_id",
    "actor_id",
    "event_id",
    "phase_id",
    "policy_date",
    "event_date",
    "applicability",
    "violation",
    "evidence",
    "supporting_sources",
    "contrary_sources",
    "missing_predicates",
    "conflicts",
    "explanation",
    "review_state",
    "input_fingerprints",
}
_REFERENCE_FIELDS = {
    "source_id",
    "input_role",
    "source_path",
    "source_sha256",
    "location",
}
_GAP_FIELDS = {"gap_id", "assessment_id", "gap_type", "description"}
_APPLICABILITY = {"applies", "not_applicable", "uncertain"}
_VIOLATION = {"yes", "likely", "unlikely", "no", "indeterminate"}
_EVIDENCE = {"complete", "incomplete", "disputed", "unavailable"}
_REVIEW = {"proposed", "reviewed"}
_GAP_TYPES = {
    "missing_predicate",
    "missing_source",
    "disputed_source",
    "uncertain_applicability",
    "unavailable_source",
    "conflicting_evidence",
}


class PolicyAssessmentError(ValueError):
    """A stable bounded policy-assessment validation failure."""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def _fail(code):
    raise PolicyAssessmentError(code)


def _exact(value, fields, code):
    if type(value) is not dict or set(value) != set(fields):
        _fail(code)
    return value


def _identifier(value, code):
    if not isinstance(value, str) or _ID.fullmatch(value) is None:
        _fail(code)
    return value


def _text(value, code):
    if (
        not isinstance(value, str)
        or not value.strip()
        or len(value) > 4096
        or any(ord(character) < 32 and character not in "\t\n\r" for character in value)
    ):
        _fail(code)
    return value


def _date(value, code):
    if not isinstance(value, str):
        _fail(code)
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        _fail(code)
    if parsed.isoformat() != value:
        _fail(code)
    return value


def _sha256(value, code):
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        _fail(code)
    return value


def _relative(value, code):
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        _fail(code)
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        _fail(code)
    return path.as_posix()


def _strings(value, code, *, identifiers=False):
    if type(value) is not list:
        _fail(code)
    parser = _identifier if identifiers else _text
    result = [parser(item, code) for item in value]
    if len(result) != len(set(result)):
        _fail(code)
    return result


def _date_scope(value, code):
    scope = _exact(value, {"start_date", "end_date"}, code)
    start = _date(scope["start_date"], code)
    end = _date(scope["end_date"], code)
    if end < start:
        _fail(code)
    return {"start_date": start, "end_date": end}


def _requirement(value, source_ids, source_hashes):
    record = _exact(value, _REQUIREMENT_FIELDS, "invalid-catalog")
    requirement_id = _identifier(record["requirement_id"], "invalid-catalog")
    source_id = _identifier(record["source_id"], "invalid-catalog")
    if source_id not in source_ids:
        _fail("stale-catalog-validation")
    source_hash = _sha256(record["source_sha256"], "invalid-catalog")
    if source_hashes[source_id] != source_hash:
        _fail("stale-catalog-validation")
    effective = _exact(
        record["effective"], {"start_date", "end_date", "gap"}, "invalid-catalog"
    )
    start = _date(effective["start_date"], "invalid-catalog")
    end = effective["end_date"]
    if end is not None:
        end = _date(end, "invalid-catalog")
        if end < start:
            _fail("invalid-catalog")
    if effective["gap"] is not None:
        _text(effective["gap"], "invalid-catalog")
    _identifier(record["department_id"], "invalid-catalog")
    _identifier(record["policy_id"], "invalid-catalog")
    _text(record["quotation"], "invalid-catalog")
    _text(record["pinpoint"], "invalid-catalog")
    _relative(record["source_path"], "invalid-catalog")
    _text(record["actor"], "invalid-catalog")
    _text(record["action"], "invalid-catalog")
    for field in (
        "triggers",
        "exceptions",
        "definitions",
        "dependencies",
        "cross_references",
        "documentation_or_review",
        "gaps",
    ):
        _strings(record[field], "invalid-catalog")
    if record["requirement_type"] not in {
        "mandatory",
        "prohibited",
        "permitted",
        "discretionary",
    }:
        _fail("invalid-catalog")
    markers = _exact(
        record["operative_markers"],
        {
            "condition_present",
            "exception_present",
            "discretion_present",
            "cross_reference_present",
        },
        "invalid-catalog",
    )
    if any(type(marker) is not bool for marker in markers.values()):
        _fail("invalid-catalog")
    return {
        "requirement_id": requirement_id,
        "source_id": source_id,
        "effective_start": start,
        "effective_end": end,
        "source_sha256": source_hash,
    }


def _catalog(value):
    record = _exact(value, _CATALOG_FIELDS, "invalid-catalog")
    requirements_bytes = record["requirements_yaml_bytes"]
    validation_bytes = record["validation_json_bytes"]
    if not isinstance(requirements_bytes, bytes) or not isinstance(validation_bytes, bytes):
        _fail("invalid-catalog")
    try:
        document = yaml.safe_load(requirements_bytes)
    except yaml.YAMLError:
        _fail("invalid-catalog")
    try:
        validation = json.loads(validation_bytes)
    except (UnicodeError, json.JSONDecodeError):
        _fail("invalid-catalog-validation")
    document = _exact(document, _CATALOG_DOCUMENT_FIELDS, "invalid-catalog")
    validation = _exact(
        validation, _CATALOG_VALIDATION_FIELDS, "invalid-catalog-validation"
    )
    if document["version"] != 1 or validation["schema_version"] != 1:
        _fail("invalid-catalog")
    if validation["valid"] is not True:
        _fail("invalid-catalog-validation")
    _date_scope(document["scope"], "invalid-catalog")
    source_ids = _strings(
        validation["source_ids"], "invalid-catalog-validation", identifiers=True
    )
    source_hashes = validation["source_hashes"]
    if type(source_hashes) is not dict or set(source_hashes) != set(source_ids):
        _fail("invalid-catalog-validation")
    source_hashes = {
        source_id: _sha256(source_hashes[source_id], "invalid-catalog-validation")
        for source_id in source_ids
    }
    requirement_ids = _strings(
        validation["requirement_ids"],
        "invalid-catalog-validation",
        identifiers=True,
    )
    _strings(validation["gap_ids"], "invalid-catalog-validation", identifiers=True)
    if type(document["requirements"]) is not list:
        _fail("invalid-catalog")
    requirements = [
        _requirement(item, set(source_ids), source_hashes)
        for item in document["requirements"]
    ]
    actual_ids = [item["requirement_id"] for item in requirements]
    if len(actual_ids) != len(set(actual_ids)):
        _fail("duplicate-requirement")
    if actual_ids != requirement_ids:
        _fail("stale-catalog-validation")
    return {
        "requirements": {item["requirement_id"]: item for item in requirements},
        "hash": hashlib.sha256(requirements_bytes + validation_bytes).hexdigest(),
    }


def _actor(value):
    record = _exact(value, _ACTOR_FIELDS, "invalid-actor")
    return {
        "actor_id": _identifier(record["actor_id"], "invalid-actor"),
        "display_name": _text(record["display_name"], "invalid-actor"),
        "roles": _strings(record["roles"], "invalid-actor", identifiers=True),
    }


def _event(value):
    record = _exact(value, _EVENT_FIELDS, "invalid-event")
    return {
        "event_id": _identifier(record["event_id"], "invalid-event"),
        "event_date": _date(record["event_date"], "invalid-event"),
        "description": _text(record["description"], "invalid-event"),
    }


def _phase(value, event_ids):
    record = _exact(value, _PHASE_FIELDS, "invalid-phase")
    event_id = _identifier(record["event_id"], "invalid-phase")
    if event_id not in event_ids:
        _fail("unresolved-event")
    sequence = record["sequence"]
    if type(sequence) is not int or sequence < 1:
        _fail("invalid-phase")
    return {
        "phase_id": _identifier(record["phase_id"], "invalid-phase"),
        "event_id": event_id,
        "label": _text(record["label"], "invalid-phase"),
        "sequence": sequence,
    }


def _selected_source(value):
    selection = _exact(value, _SOURCE_SELECTION_FIELDS, "invalid-selected-source")
    role = selection["input_role"]
    if role not in _SOURCE_ROLES:
        _fail("invalid-selected-source")
    documentation_path = _relative(
        selection["source_documentation_path"], "invalid-selected-source"
    )
    if not documentation_path.endswith(".SOURCE.yaml"):
        _fail("invalid-selected-source")
    if not isinstance(selection["source_yaml_bytes"], bytes) or not isinstance(
        selection["artifact_bytes"], bytes
    ):
        _fail("invalid-selected-source")
    try:
        document = yaml.safe_load(selection["source_yaml_bytes"])
    except yaml.YAMLError:
        _fail("invalid-source-yaml")
    document = _exact(document, _SOURCE_DOCUMENT_FIELDS, "invalid-source-yaml")
    if document["version"] != 1:
        _fail("invalid-source-yaml")
    source_id = _identifier(document["source_id"], "invalid-source-yaml")
    artifact_path = _relative(document["artifact_path"], "invalid-source-yaml")
    if (
        PurePosixPath(artifact_path).parent
        != PurePosixPath(documentation_path).parent
        or artifact_path == documentation_path
    ):
        _fail("invalid-source-yaml")
    source_hash = hashlib.sha256(selection["artifact_bytes"]).hexdigest()
    if document["sha256"] != source_hash:
        _fail("source-hash-mismatch")
    if document["source_type"] != _SOURCE_TYPES[role]:
        _fail("invalid-source-yaml")
    _date(document["occurred_at"], "invalid-source-yaml")
    _strings(document["limitations"], "invalid-source-yaml")
    return {
        "source_id": source_id,
        "input_role": role,
        "source_documentation_path": documentation_path,
        "source_path": artifact_path,
        "source_sha256": source_hash,
    }


def _fingerprints(value, code):
    if type(value) is not dict or set(value) != set(_ROLES):
        _fail(code)
    return {role: _sha256(value[role], code) for role in _ROLES}


def _scope(value):
    record = _exact(value, _SCOPE_FIELDS, "invalid-scope")
    start = _date(record["start_date"], "invalid-scope")
    end = _date(record["end_date"], "invalid-scope")
    if end < start:
        _fail("invalid-scope")
    return {
        "start_date": start,
        "end_date": end,
        "selected_requirement_ids": _strings(
            record["selected_requirement_ids"], "invalid-scope", identifiers=True
        ),
        "selected_actor_ids": _strings(
            record["selected_actor_ids"], "invalid-scope", identifiers=True
        ),
        "selected_event_ids": _strings(
            record["selected_event_ids"], "invalid-scope", identifiers=True
        ),
        "selected_phase_ids": _strings(
            record["selected_phase_ids"], "invalid-scope", identifiers=True
        ),
        "selected_source_paths": [
            _relative(path, "invalid-scope")
            for path in _strings(record["selected_source_paths"], "invalid-scope")
        ],
    }


def _reference(value, sources):
    record = _exact(value, _REFERENCE_FIELDS, "invalid-source-reference")
    source_id = _identifier(record["source_id"], "invalid-source-reference")
    if source_id not in sources:
        _fail("unresolved-source")
    source = sources[source_id]
    candidate = {
        "source_id": source_id,
        "input_role": record["input_role"],
        "source_path": _relative(record["source_path"], "invalid-source-reference"),
        "source_sha256": _sha256(
            record["source_sha256"], "invalid-source-reference"
        ),
        "location": _text(record["location"], "invalid-source-reference"),
    }
    if any(
        candidate[field] != source[field]
        for field in ("input_role", "source_path", "source_sha256")
    ):
        _fail("stale-source-reference")
    return candidate


def _assessment(value, catalog, actors, events, phases, sources, scope, fingerprints):
    record = _exact(value, _ASSESSMENT_FIELDS, "invalid-assessment")
    requirement_id = _identifier(record["requirement_id"], "invalid-assessment")
    actor_id = _identifier(record["actor_id"], "invalid-assessment")
    event_id = _identifier(record["event_id"], "invalid-assessment")
    phase_id = _identifier(record["phase_id"], "invalid-assessment")
    if requirement_id not in catalog or requirement_id not in scope["selected_requirement_ids"]:
        _fail("unresolved-requirement")
    if actor_id not in actors or actor_id not in scope["selected_actor_ids"]:
        _fail("unresolved-actor")
    if event_id not in events or event_id not in scope["selected_event_ids"]:
        _fail("unresolved-event")
    if phase_id not in phases or phase_id not in scope["selected_phase_ids"]:
        _fail("unresolved-phase")
    if phases[phase_id]["event_id"] != event_id:
        _fail("phase-event-mismatch")
    event_date = _date(record["event_date"], "invalid-assessment")
    if event_date != events[event_id]["event_date"]:
        _fail("event-date-mismatch")
    policy_date = _date(record["policy_date"], "invalid-assessment")
    requirement = catalog[requirement_id]
    if policy_date != requirement["effective_start"]:
        _fail("policy-date-mismatch")
    applicability = record["applicability"]
    violation = record["violation"]
    evidence = record["evidence"]
    if (
        applicability not in _APPLICABILITY
        or violation not in _VIOLATION
        or evidence not in _EVIDENCE
        or record["review_state"] not in _REVIEW
    ):
        _fail("invalid-assessment")
    effective = event_date >= requirement["effective_start"] and (
        requirement["effective_end"] is None
        or event_date <= requirement["effective_end"]
    )
    if not effective and applicability != "not_applicable":
        _fail("policy-not-effective")
    supporting = [_reference(item, sources) for item in record["supporting_sources"]]
    contrary = [_reference(item, sources) for item in record["contrary_sources"]]
    missing = _strings(record["missing_predicates"], "invalid-assessment")
    conflicts = _strings(record["conflicts"], "invalid-assessment")
    if applicability in {"not_applicable", "uncertain"} and violation != "indeterminate":
        _fail("invalid-not-applicable")
    if violation == "no" and evidence != "complete":
        _fail("unsupported-no")
    if violation == "no" and (not supporting or contrary or missing or conflicts):
        _fail("unsupported-no")
    if evidence == "unavailable" and violation != "indeterminate":
        _fail("invalid-assessment")
    if violation in {"yes", "likely", "unlikely"} and not supporting:
        _fail("unsupported-assessment")
    if evidence == "disputed" and not conflicts:
        _fail("invalid-assessment")
    if _fingerprints(record["input_fingerprints"], "invalid-input-fingerprint") != fingerprints:
        _fail("stale-input-fingerprint")
    return {
        "assessment_id": _identifier(record["assessment_id"], "invalid-assessment"),
        "requirement_id": requirement_id,
        "actor_id": actor_id,
        "event_id": event_id,
        "phase_id": phase_id,
        "policy_date": policy_date,
        "event_date": event_date,
        "applicability": applicability,
        "violation": violation,
        "evidence": evidence,
        "supporting_sources": supporting,
        "contrary_sources": contrary,
        "missing_predicates": missing,
        "conflicts": conflicts,
        "explanation": _text(record["explanation"], "invalid-assessment"),
        "review_state": record["review_state"],
        "input_fingerprints": dict(fingerprints),
    }


def _gap(value, assessment_ids):
    record = _exact(value, _GAP_FIELDS, "invalid-gap")
    assessment_id = _identifier(record["assessment_id"], "invalid-gap")
    if assessment_id not in assessment_ids:
        _fail("unresolved-assessment")
    if record["gap_type"] not in _GAP_TYPES:
        _fail("invalid-gap")
    return {
        "gap_id": _identifier(record["gap_id"], "invalid-gap"),
        "assessment_id": assessment_id,
        "gap_type": record["gap_type"],
        "description": _text(record["description"], "invalid-gap"),
    }


def _unique(records, field, code):
    values = [record[field] for record in records]
    if len(values) != len(set(values)):
        _fail(code)
    return {record[field]: record for record in records}


def _yaml(value):
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=True).encode("utf-8")


def build_assessment_plan(
    catalog,
    actors,
    events,
    phases,
    selected_sources,
    assessments,
    gaps,
    scope,
    input_fingerprints,
):
    """Validate proposed records and return deterministic output-relative bytes."""
    if any(
        type(value) is not list
        for value in (actors, events, phases, selected_sources, assessments, gaps)
    ):
        _fail("invalid-assessment-plan")
    catalog_record = _catalog(catalog)
    scope_record = _scope(scope)
    fingerprints = _fingerprints(input_fingerprints, "invalid-input-fingerprint")
    actor_map = _unique(
        sorted((_actor(item) for item in actors), key=lambda item: item["actor_id"]),
        "actor_id",
        "duplicate-actor",
    )
    event_map = _unique(
        sorted((_event(item) for item in events), key=lambda item: item["event_id"]),
        "event_id",
        "duplicate-event",
    )
    phase_map = _unique(
        sorted(
            (_phase(item, set(event_map)) for item in phases),
            key=lambda item: item["phase_id"],
        ),
        "phase_id",
        "duplicate-phase",
    )
    source_map = _unique(
        sorted(
            (_selected_source(item) for item in selected_sources),
            key=lambda item: item["source_id"],
        ),
        "source_id",
        "duplicate-source",
    )
    if set(scope_record["selected_source_paths"]) != {
        source["source_documentation_path"] for source in source_map.values()
    }:
        _fail("undeclared-source-selection")
    for selected, available, code in (
        (scope_record["selected_requirement_ids"], catalog_record["requirements"], "unresolved-requirement"),
        (scope_record["selected_actor_ids"], actor_map, "unresolved-actor"),
        (scope_record["selected_event_ids"], event_map, "unresolved-event"),
        (scope_record["selected_phase_ids"], phase_map, "unresolved-phase"),
    ):
        if not set(selected).issubset(available):
            _fail(code)
    assessment_records = sorted(
        (
            _assessment(
                item,
                catalog_record["requirements"],
                actor_map,
                event_map,
                phase_map,
                source_map,
                scope_record,
                fingerprints,
            )
            for item in assessments
        ),
        key=lambda item: item["assessment_id"],
    )
    assessment_map = _unique(
        assessment_records, "assessment_id", "duplicate-assessment"
    )
    units = [
        (
            item["requirement_id"],
            item["actor_id"],
            item["event_id"],
            item["phase_id"],
        )
        for item in assessment_records
    ]
    if len(units) != len(set(units)):
        _fail("duplicate-assessment-unit")
    gap_records = sorted(
        (_gap(item, set(assessment_map)) for item in gaps),
        key=lambda item: item["gap_id"],
    )
    _unique(gap_records, "gap_id", "duplicate-gap")
    lines = [
        "# Policy assessment",
        "",
        f"Assessments: {len(assessment_records)}",
        f"Gaps: {len(gap_records)}",
        "",
    ]
    for item in assessment_records:
        lines.append(
            f"- {item['assessment_id']}: {item['applicability']} / "
            f"{item['violation']} / {item['evidence']} — {item['explanation']}"
        )
        lines.extend(f"  - Conflict: {conflict}" for conflict in item["conflicts"])
    lines.extend(f"- GAP {item['gap_id']}: {item['description']}" for item in gap_records)
    validation = {
        "schema_version": 1,
        "valid": True,
        "catalog_sha256": catalog_record["hash"],
        "assessment_ids": [item["assessment_id"] for item in assessment_records],
        "gap_ids": [item["gap_id"] for item in gap_records],
        "source_hashes": {
            source_id: source_map[source_id]["source_sha256"]
            for source_id in sorted(source_map)
        },
        "input_fingerprints": dict(fingerprints),
    }
    artifacts = [
        {
            "path": "policy-assessments.yaml",
            "bytes": _yaml(
                {
                    "version": 1,
                    "scope": scope_record,
                    "assessments": assessment_records,
                }
            ),
            "internet_sources": [],
        },
        {
            "path": "policy-assessment-gaps.yaml",
            "bytes": _yaml({"version": 1, "scope": scope_record, "gaps": gap_records}),
            "internet_sources": [],
        },
        {
            "path": "policy-assessment.md",
            "bytes": ("\n".join(lines) + "\n").encode(),
            "internet_sources": [],
        },
        {
            "path": "policy-assessment-validation.json",
            "bytes": (
                json.dumps(validation, sort_keys=True, separators=(",", ":")) + "\n"
            ).encode(),
            "internet_sources": [],
        },
    ]
    return {"scope": scope_record, "artifacts": artifacts}
