"""Validate ordinary municipal-profile files supplied by a trusted folder host."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date

import yaml


_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_REQUIRED_FILES = {
    "municipal-profile.yaml",
    "municipal-profile-gaps.yaml",
    "municipal-profile.md",
    "municipal-profile-validation.json",
}
_HASHED_ARTIFACTS = (
    "municipal-profile.yaml",
    "municipal-profile-gaps.yaml",
    "municipal-profile.md",
)
_PROFILE_FIELDS = {
    "version",
    "profile_id",
    "municipality_id",
    "department_id",
    "checked_through",
    "upstream_validations",
    "input_fingerprints",
    "evidence",
    "entities",
    "events",
    "chains",
    "comparisons",
    "contradictions",
    "similarity_features",
    "domains",
}
_GAPS_FIELDS = {"version", "profile_id", "gaps"}
_VALIDATION_FIELDS = {
    "schema_version",
    "valid",
    "profile_id",
    "artifact_hashes",
    "source_hashes",
    "upstream_hashes",
    "input_fingerprints",
    "evidence_ids",
    "entity_ids",
    "event_ids",
    "chain_ids",
    "comparison_ids",
    "contradiction_ids",
    "feature_ids",
    "gap_ids",
}
_UPSTREAM_ROLES = ("policy-catalog", "policy-assessment", "verified-authority")
_INPUT_ROLES = (
    "municipality",
    "department",
    "source",
    "policy-catalog",
    "policy-assessment",
    "case-record",
    "verified-authority",
)
_ID_FIELDS = {
    "evidence_ids": ("evidence", "evidence_id"),
    "entity_ids": ("entities", "entity_id"),
    "event_ids": ("events", "event_id"),
    "chain_ids": ("chains", "chain_id"),
    "comparison_ids": ("comparisons", "comparison_id"),
    "contradiction_ids": ("contradictions", "contradiction_id"),
    "feature_ids": ("similarity_features", "feature_id"),
}
_DOMAINS = ("Practice", "Knowledge", "Authority", "Causation", "Recurrence")
_RECORD_FIELDS = {
    "evidence": {
        "evidence_id",
        "domain",
        "category",
        "source_id",
        "input_role",
        "source_path",
        "source_sha256",
        "location",
        "date",
        "proposition",
        "support_direction",
        "limitations",
        "review_state",
    },
    "entities": {"entity_id", "entity_type", "name", "evidence_ids"},
    "events": {
        "event_id",
        "event_type",
        "event_date",
        "entity_ids",
        "evidence_ids",
        "description",
    },
    "chains": {"chain_id", "chain_type", "event_ids", "evidence_ids", "question"},
    "comparisons": {
        "comparison_id",
        "target_event_id",
        "candidate_event_ids",
        "feature_ids",
        "evidence_ids",
        "question",
    },
    "contradictions": {
        "contradiction_id",
        "left_evidence_id",
        "right_evidence_id",
        "question",
    },
    "similarity_features": {"feature_id", "label", "definition", "evidence_ids"},
    "domains": {
        "domain",
        "evidence_ids",
        "counterevidence_ids",
        "gap_ids",
        "questions",
    },
}
_GAP_RECORD_FIELDS = {"gap_id", "domain", "description"}


class MunicipalProfileInputError(ValueError):
    """A stable bounded profile-input validation failure."""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def _fail(code):
    raise MunicipalProfileInputError(code)


def _exact(value, fields, code):
    if type(value) is not dict or set(value) != set(fields):
        _fail(code)
    return value


def _sha256(value, code):
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
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
    return parsed


def _bytes(files, name):
    value = files[name]
    if not isinstance(value, bytes) or not value or len(value) > 8 * 1024 * 1024:
        _fail("invalid-profile-file")
    return value


def _yaml(files, name, code):
    try:
        return yaml.safe_load(_bytes(files, name))
    except (UnicodeDecodeError, yaml.YAMLError):
        _fail(code)


def _json(files, name, code):
    try:
        return json.loads(_bytes(files, name))
    except (UnicodeDecodeError, json.JSONDecodeError):
        _fail(code)


def _id_list(records, field, code):
    if type(records) is not list:
        _fail(code)
    values = []
    for record in records:
        if type(record) is not dict or not isinstance(record.get(field), str):
            _fail(code)
        values.append(record[field])
    if len(values) != len(set(values)):
        _fail(code)
    return values


def _hash_map(value, keys, code):
    if type(value) is not dict or set(value) != set(keys):
        _fail(code)
    return {key: _sha256(value[key], code) for key in keys}


def _validate_upstream(profile, validation):
    upstream = profile["upstream_validations"]
    if type(upstream) is not dict or set(upstream) != set(_UPSTREAM_ROLES):
        _fail("invalid-profile")
    expected = {}
    for role in _UPSTREAM_ROLES:
        record = _exact(upstream[role], {"valid", "sha256"}, "invalid-profile")
        if record["valid"] is not True:
            _fail("failing-profile-validation")
        expected[role] = _sha256(record["sha256"], "invalid-profile")
    actual = _hash_map(
        validation["upstream_hashes"], _UPSTREAM_ROLES, "invalid-profile-validation"
    )
    if actual != expected:
        _fail("profile-upstream-hash-mismatch")


def _validate_source_hashes(profile, validation):
    evidence = profile["evidence"]
    if type(evidence) is not list:
        _fail("invalid-profile")
    source_hashes = {}
    for record in evidence:
        if type(record) is not dict:
            _fail("invalid-profile")
        source_id = record.get("source_id")
        source_hash = record.get("source_sha256")
        if not isinstance(source_id, str):
            _fail("invalid-profile")
        source_hash = _sha256(source_hash, "invalid-profile")
        if source_id in source_hashes and source_hashes[source_id] != source_hash:
            _fail("profile-source-hash-mismatch")
        source_hashes[source_id] = source_hash
    actual = validation["source_hashes"]
    if type(actual) is not dict:
        _fail("invalid-profile-validation")
    actual = {
        source_id: _sha256(source_hash, "invalid-profile-validation")
        for source_id, source_hash in actual.items()
        if isinstance(source_id, str)
    }
    if actual != source_hashes:
        _fail("profile-source-hash-mismatch")
    return sorted(source_hashes)


def _validate_ids(profile, gaps, validation):
    for validation_field, (profile_field, record_field) in _ID_FIELDS.items():
        expected = _id_list(profile[profile_field], record_field, "invalid-profile")
        if validation[validation_field] != expected:
            _fail("profile-id-mismatch")
    expected_gaps = _id_list(gaps["gaps"], "gap_id", "invalid-profile-gaps")
    if validation["gap_ids"] != expected_gaps:
        _fail("profile-id-mismatch")

    evidence_ids = set(validation["evidence_ids"])
    gap_ids = set(validation["gap_ids"])
    domains = profile["domains"]
    if type(domains) is not list or any(type(item) is not dict for item in domains):
        _fail("invalid-profile")
    if [item.get("domain") for item in domains] != list(_DOMAINS):
        _fail("invalid-profile")
    referenced_evidence = set()
    referenced_gaps = set()
    for domain in domains:
        if type(domain) is not dict:
            _fail("invalid-profile")
        supporting = domain.get("evidence_ids")
        contrary = domain.get("counterevidence_ids")
        domain_gaps = domain.get("gap_ids")
        if not all(type(value) is list for value in (supporting, contrary, domain_gaps)):
            _fail("invalid-profile")
        referenced_evidence.update(supporting)
        referenced_evidence.update(contrary)
        referenced_gaps.update(domain_gaps)
    if referenced_evidence != evidence_ids or referenced_gaps != gap_ids:
        _fail("profile-id-mismatch")


def _validate_record_shapes(profile, gaps):
    for collection, fields in _RECORD_FIELDS.items():
        records = profile[collection]
        if type(records) is not list:
            _fail("invalid-profile")
        for record in records:
            _exact(record, fields, "invalid-profile")
    if type(gaps["gaps"]) is not list:
        _fail("invalid-profile-gaps")
    for record in gaps["gaps"]:
        _exact(record, _GAP_RECORD_FIELDS, "invalid-profile-gaps")


def _validate_artifact_hashes(files, validation):
    expected = _hash_map(
        validation["artifact_hashes"],
        _HASHED_ARTIFACTS,
        "invalid-profile-validation",
    )
    actual = {
        name: hashlib.sha256(_bytes(files, name)).hexdigest()
        for name in _HASHED_ARTIFACTS
    }
    if actual != expected:
        _fail("profile-artifact-hash-mismatch")


def validate_profile_files(
    files,
    *,
    actual_folder_fingerprint,
    expected_folder_fingerprint,
    earliest_checked_through,
):
    """Validate supplied bytes and return a non-authoritative input receipt."""
    if type(files) is not dict:
        _fail("invalid-profile-files")
    if not _REQUIRED_FILES.issubset(files):
        _fail("missing-profile-file")
    actual_fingerprint = _sha256(
        actual_folder_fingerprint, "invalid-folder-fingerprint"
    )
    expected_fingerprint = _sha256(
        expected_folder_fingerprint, "invalid-folder-fingerprint"
    )
    if actual_fingerprint != expected_fingerprint:
        _fail("profile-folder-changed")

    profile = _exact(
        _yaml(files, "municipal-profile.yaml", "invalid-profile"),
        _PROFILE_FIELDS,
        "invalid-profile",
    )
    gaps = _exact(
        _yaml(files, "municipal-profile-gaps.yaml", "invalid-profile-gaps"),
        _GAPS_FIELDS,
        "invalid-profile-gaps",
    )
    validation = _exact(
        _json(
            files,
            "municipal-profile-validation.json",
            "invalid-profile-validation",
        ),
        _VALIDATION_FIELDS,
        "invalid-profile-validation",
    )
    try:
        markdown = _bytes(files, "municipal-profile.md").decode("utf-8")
    except UnicodeDecodeError:
        _fail("invalid-profile-markdown")
    if not markdown.strip():
        _fail("invalid-profile-markdown")

    if profile["version"] != 1 or gaps["version"] != 1:
        _fail("invalid-profile")
    if validation["schema_version"] != 1:
        _fail("invalid-profile-validation")
    if validation["valid"] is not True:
        _fail("failing-profile-validation")
    profile_id = profile["profile_id"]
    if (
        not isinstance(profile_id, str)
        or not profile_id
        or gaps["profile_id"] != profile_id
        or validation["profile_id"] != profile_id
    ):
        _fail("profile-identity-mismatch")

    checked_through = _date(profile["checked_through"], "invalid-profile")
    earliest = _date(earliest_checked_through, "invalid-checked-through-date")
    if checked_through < earliest:
        _fail("stale-profile")

    _validate_record_shapes(profile, gaps)

    fingerprints = _hash_map(
        profile["input_fingerprints"], _INPUT_ROLES, "invalid-profile"
    )
    validation_fingerprints = _hash_map(
        validation["input_fingerprints"],
        _INPUT_ROLES,
        "invalid-profile-validation",
    )
    if validation_fingerprints != fingerprints:
        _fail("profile-input-fingerprint-mismatch")

    _validate_upstream(profile, validation)
    source_ids = _validate_source_hashes(profile, validation)
    _validate_ids(profile, gaps, validation)
    _validate_artifact_hashes(files, validation)

    return {
        "valid": True,
        "profile_id": profile_id,
        "municipality_id": profile["municipality_id"],
        "department_id": profile["department_id"],
        "checked_through": checked_through.isoformat(),
        "folder_fingerprint": actual_fingerprint,
        "source_ids": source_ids,
    }
