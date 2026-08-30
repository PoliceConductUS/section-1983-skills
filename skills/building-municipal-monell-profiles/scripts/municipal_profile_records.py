"""Deterministic municipal-profile planning over validated in-memory data."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import PurePosixPath

import yaml


_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_CONCLUSIVE_LANGUAGE = (
    re.compile(r"\bmonell liability (?:is |was )?(?:established|proved|satisfied)\b", re.I),
    re.compile(r"\blegally sufficient\b", re.I),
    re.compile(r"\belement (?:is |was )?(?:established|proved|satisfied)\b", re.I),
)
_ROLES = (
    "municipality",
    "department",
    "source",
    "policy-catalog",
    "policy-assessment",
    "case-record",
    "verified-authority",
)
_UPSTREAM_ROLES = ("policy-catalog", "policy-assessment", "verified-authority")
_SOURCE_ROLES = {"municipality", "department", "source", "case-record", "verified-authority"}
_DOMAINS = ("Practice", "Knowledge", "Authority", "Causation", "Recurrence")
_CATEGORIES = {
    "formal_policy",
    "custom",
    "training",
    "supervision",
    "fto_transmission",
    "complaint_internal_affairs",
    "ratification_candidate",
    "litigation_position",
    "institutional_feedback",
    "institutional_learning",
}
_DIRECTIONS = {"favorable", "unfavorable", "disconfirming", "neutral"}
_SOURCE_TYPES = {"identity_record", "institutional_record", "case_record", "authority_record"}
_REVIEW = {"proposed", "reviewed", "rejected"}
_ENTITY_TYPES = {"municipality", "department", "division", "unit", "external_body"}
_EVENT_TYPES = {
    "complaint",
    "corrective_review",
    "policy_change",
    "training",
    "supervision",
    "internal_affairs",
    "litigation",
    "institutional_feedback",
    "institutional_learning",
}
_CHAIN_TYPES = {"notice_corrective", "knowledge", "causation"}
_IDENTITY_FIELDS = {"profile_id", "municipality_id", "department_id", "checked_through"}
_VALIDATION_FIELDS = {"valid", "sha256"}
_SOURCE_SELECTION_FIELDS = {
    "input_role",
    "source_documentation_path",
    "source_yaml_bytes",
    "artifact_bytes",
}
_SOURCE_FIELDS = {
    "version",
    "source_id",
    "artifact_path",
    "sha256",
    "source_type",
    "occurred_at",
    "limitations",
}
_EVIDENCE_FIELDS = {
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
}
_ENTITY_FIELDS = {"entity_id", "entity_type", "name", "evidence_ids"}
_EVENT_FIELDS = {
    "event_id",
    "event_type",
    "event_date",
    "entity_ids",
    "evidence_ids",
    "description",
}
_CHAIN_FIELDS = {"chain_id", "chain_type", "event_ids", "evidence_ids", "question"}
_COMPARISON_FIELDS = {
    "comparison_id",
    "target_event_id",
    "candidate_event_ids",
    "feature_ids",
    "evidence_ids",
    "question",
}
_CONTRADICTION_FIELDS = {
    "contradiction_id",
    "left_evidence_id",
    "right_evidence_id",
    "question",
}
_FEATURE_FIELDS = {"feature_id", "label", "definition", "evidence_ids"}
_DOMAIN_FIELDS = {
    "domain",
    "evidence_ids",
    "counterevidence_ids",
    "gap_ids",
    "questions",
}
_GAP_FIELDS = {"gap_id", "domain", "description"}
_PREREQUISITE_STAGES = ("collection", "analysis", "assessment", "profile")
_PREREQUISITE_STATE_FIELDS = {
    "state",
    "terminal_receipt",
    "expected_artifacts",
    "validation_passed",
    "fingerprints_match",
}
_COLLECTION_AUTHORIZATION_FIELDS = {
    "internet",
    "fees_required",
    "fees_approved",
}
_STAGE_CONTRACTS = {
    "collection": {
        "skill": "collecting-police-policy-sources",
        "ready_status": "ready-for-collection",
        "roles": (
            "department-identity",
            "jurisdiction",
            "approved-source-system",
            "research-scope",
        ),
        "internet": "authorized",
        "postconditions": (
            "terminal-run-receipt-success",
            "policy-source-candidates.yaml-present",
            "policy-source-gaps.yaml-present",
            "candidate-source-files-and-SOURCE.yaml-present",
            "domain-validation-passed",
            "input-fingerprints-match",
            "independent-approved-for-analysis-review",
        ),
    },
    "analysis": {
        "skill": "analyzing-police-policy-sources",
        "ready_status": "ready-for-analysis",
        "roles": (
            "department-identity",
            "jurisdiction",
            "policy-source",
            "analysis-scope",
        ),
        "internet": "disabled",
        "postconditions": (
            "terminal-run-receipt-success",
            "policy-requirements.yaml-present",
            "policy-analysis-gaps.yaml-present",
            "policy-analysis.md-present",
            "policy-analysis-validation.json-present",
            "domain-validation-passed",
            "input-fingerprints-match",
        ),
    },
    "assessment": {
        "skill": "assessing-police-policy-compliance",
        "ready_status": "ready-for-assessment",
        "roles": (
            "policy-catalog",
            "actor",
            "event",
            "phase",
            "case-record",
            "assessment-scope",
        ),
        "internet": "disabled",
        "postconditions": (
            "terminal-run-receipt-success",
            "policy-assessments.yaml-present",
            "policy-assessment-gaps.yaml-present",
            "policy-assessment.md-present",
            "policy-assessment-validation.json-present",
            "domain-validation-passed",
            "input-fingerprints-match",
            "actor-event-phase-separation-preserved",
            "unresolved-gaps-preserved",
        ),
    },
    "profile": {
        "skill": "building-municipal-monell-profiles",
        "ready_status": "ready-for-profile",
        "roles": _ROLES,
        "internet": "disabled",
        "postconditions": (
            "terminal-run-receipt-success",
            "municipal-profile.yaml-present",
            "municipal-profile-gaps.yaml-present",
            "municipal-profile.md-present",
            "municipal-profile-validation.json-present",
            "domain-validation-passed",
            "input-fingerprints-match",
        ),
    },
}


class MunicipalProfileError(ValueError):
    """A stable bounded municipal-profile validation failure."""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def _fail(code):
    raise MunicipalProfileError(code)


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


def _question(value, code):
    value = _text(value, code)
    if not value.rstrip().endswith("?"):
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


def _identity(value):
    record = _exact(value, _IDENTITY_FIELDS, "invalid-identity")
    return {
        "profile_id": _identifier(record["profile_id"], "invalid-identity"),
        "municipality_id": _identifier(record["municipality_id"], "invalid-identity"),
        "department_id": _identifier(record["department_id"], "invalid-identity"),
        "checked_through": _date(record["checked_through"], "invalid-identity"),
    }


def _upstream(value):
    if type(value) is not dict or set(value) != set(_UPSTREAM_ROLES):
        _fail("invalid-upstream-validation")
    result = {}
    for role in _UPSTREAM_ROLES:
        record = _exact(value[role], _VALIDATION_FIELDS, "invalid-upstream-validation")
        if record["valid"] is not True:
            _fail("failing-upstream-validation")
        result[role] = {
            "valid": True,
            "sha256": _sha256(record["sha256"], "invalid-upstream-validation"),
        }
    return result


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
    document = _exact(document, _SOURCE_FIELDS, "invalid-source-yaml")
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
    if document["source_type"] not in _SOURCE_TYPES:
        _fail("invalid-source-yaml")
    _date(document["occurred_at"], "invalid-source-yaml")
    _strings(document["limitations"], "invalid-source-yaml")
    return {
        "source_id": source_id,
        "input_role": role,
        "source_path": artifact_path,
        "source_sha256": source_hash,
    }


def _fingerprints(value):
    if type(value) is not dict or set(value) != set(_ROLES):
        _fail("invalid-input-fingerprint")
    return {role: _sha256(value[role], "invalid-input-fingerprint") for role in _ROLES}


def _evidence(value, sources):
    record = _exact(value, _EVIDENCE_FIELDS, "invalid-evidence")
    source_id = _identifier(record["source_id"], "invalid-evidence")
    if source_id not in sources:
        _fail("unresolved-source")
    source = sources[source_id]
    if record["domain"] not in _DOMAINS or record["category"] not in _CATEGORIES:
        _fail("invalid-evidence")
    if record["support_direction"] not in _DIRECTIONS or record["review_state"] not in _REVIEW:
        _fail("invalid-evidence")
    source_path = _relative(record["source_path"], "invalid-evidence")
    source_hash = _sha256(record["source_sha256"], "invalid-evidence")
    if (
        record["input_role"] != source["input_role"]
        or source_path != source["source_path"]
        or source_hash != source["source_sha256"]
    ):
        _fail("stale-source-reference")
    return {
        "evidence_id": _identifier(record["evidence_id"], "invalid-evidence"),
        "domain": record["domain"],
        "category": record["category"],
        "source_id": source_id,
        "input_role": record["input_role"],
        "source_path": source_path,
        "source_sha256": source_hash,
        "location": _text(record["location"], "invalid-evidence"),
        "date": _date(record["date"], "invalid-evidence"),
        "proposition": _text(record["proposition"], "invalid-evidence"),
        "support_direction": record["support_direction"],
        "limitations": _strings(record["limitations"], "invalid-evidence"),
        "review_state": record["review_state"],
    }


def _references(value, available, code):
    references = _strings(value, code, identifiers=True)
    if not set(references).issubset(available):
        _fail(code)
    return references


def _entity(value, evidence_ids):
    record = _exact(value, _ENTITY_FIELDS, "invalid-entity")
    if record["entity_type"] not in _ENTITY_TYPES:
        _fail("invalid-entity")
    return {
        "entity_id": _identifier(record["entity_id"], "invalid-entity"),
        "entity_type": record["entity_type"],
        "name": _text(record["name"], "invalid-entity"),
        "evidence_ids": _references(
            record["evidence_ids"], evidence_ids, "unresolved-evidence"
        ),
    }


def _event(value, entity_ids, evidence_ids):
    record = _exact(value, _EVENT_FIELDS, "invalid-event")
    if record["event_type"] not in _EVENT_TYPES:
        _fail("invalid-event")
    return {
        "event_id": _identifier(record["event_id"], "invalid-event"),
        "event_type": record["event_type"],
        "event_date": _date(record["event_date"], "invalid-event"),
        "entity_ids": _references(record["entity_ids"], entity_ids, "unresolved-entity"),
        "evidence_ids": _references(
            record["evidence_ids"], evidence_ids, "unresolved-evidence"
        ),
        "description": _text(record["description"], "invalid-event"),
    }


def _chain(value, event_ids, evidence_ids):
    record = _exact(value, _CHAIN_FIELDS, "invalid-chain")
    if record["chain_type"] not in _CHAIN_TYPES:
        _fail("invalid-chain")
    return {
        "chain_id": _identifier(record["chain_id"], "invalid-chain"),
        "chain_type": record["chain_type"],
        "event_ids": _references(record["event_ids"], event_ids, "unresolved-event"),
        "evidence_ids": _references(
            record["evidence_ids"], evidence_ids, "unresolved-evidence"
        ),
        "question": _question(record["question"], "invalid-chain"),
    }


def _feature(value, evidence_ids):
    record = _exact(value, _FEATURE_FIELDS, "invalid-feature")
    return {
        "feature_id": _identifier(record["feature_id"], "invalid-feature"),
        "label": _text(record["label"], "invalid-feature"),
        "definition": _text(record["definition"], "invalid-feature"),
        "evidence_ids": _references(
            record["evidence_ids"], evidence_ids, "unresolved-evidence"
        ),
    }


def _comparison(value, event_ids, feature_ids, evidence_ids):
    record = _exact(value, _COMPARISON_FIELDS, "invalid-comparison")
    target = _identifier(record["target_event_id"], "invalid-comparison")
    if target not in event_ids:
        _fail("unresolved-event")
    features = _strings(record["feature_ids"], "invalid-comparison", identifiers=True)
    if not set(features).issubset(feature_ids):
        _fail("unresolved-feature")
    return {
        "comparison_id": _identifier(record["comparison_id"], "invalid-comparison"),
        "target_event_id": target,
        "candidate_event_ids": _references(
            record["candidate_event_ids"], event_ids, "unresolved-event"
        ),
        "feature_ids": features,
        "evidence_ids": _references(
            record["evidence_ids"], evidence_ids, "unresolved-evidence"
        ),
        "question": _question(record["question"], "invalid-comparison"),
    }


def _contradiction(value, evidence_ids):
    record = _exact(value, _CONTRADICTION_FIELDS, "invalid-contradiction")
    left = _identifier(record["left_evidence_id"], "invalid-contradiction")
    right = _identifier(record["right_evidence_id"], "invalid-contradiction")
    if left not in evidence_ids or right not in evidence_ids or left == right:
        _fail("unresolved-evidence")
    return {
        "contradiction_id": _identifier(
            record["contradiction_id"], "invalid-contradiction"
        ),
        "left_evidence_id": left,
        "right_evidence_id": right,
        "question": _question(record["question"], "invalid-contradiction"),
    }


def _gap(value):
    record = _exact(value, _GAP_FIELDS, "invalid-gap")
    if record["domain"] not in _DOMAINS:
        _fail("invalid-gap")
    return {
        "gap_id": _identifier(record["gap_id"], "invalid-gap"),
        "domain": record["domain"],
        "description": _text(record["description"], "invalid-gap"),
    }


def _domain(value, evidence, gaps):
    record = _exact(value, _DOMAIN_FIELDS, "invalid-domain")
    domain = record["domain"]
    if domain not in _DOMAINS:
        _fail("invalid-domain")
    domain_evidence = {
        evidence_id
        for evidence_id, item in evidence.items()
        if item["domain"] == domain
    }
    evidence_ids = _references(
        record["evidence_ids"], domain_evidence, "mixed-domain-evidence"
    )
    counterevidence_ids = _references(
        record["counterevidence_ids"], domain_evidence, "mixed-domain-evidence"
    )
    if set(evidence_ids) & set(counterevidence_ids):
        _fail("invalid-domain")
    if set(evidence_ids) | set(counterevidence_ids) != domain_evidence:
        _fail("unassigned-domain-evidence")
    domain_gaps = {gap_id for gap_id, item in gaps.items() if item["domain"] == domain}
    gap_ids = _references(record["gap_ids"], domain_gaps, "mixed-domain-gap")
    if set(gap_ids) != domain_gaps:
        _fail("unassigned-domain-gap")
    return {
        "domain": domain,
        "evidence_ids": evidence_ids,
        "counterevidence_ids": counterevidence_ids,
        "gap_ids": gap_ids,
        "questions": [_question(item, "invalid-domain") for item in _strings(record["questions"], "invalid-domain")],
    }


def _unique(records, field, code):
    values = [record[field] for record in records]
    if len(values) != len(set(values)):
        _fail(code)
    return {record[field]: record for record in records}


def _yaml(value):
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=True).encode("utf-8")


def _reject_conclusive_language(value):
    rendered = json.dumps(value, sort_keys=True)
    if any(pattern.search(rendered) for pattern in _CONCLUSIVE_LANGUAGE):
        _fail("conclusive-profile-language")


def _prerequisite_state(value, *, name, states):
    if type(value) is not dict:
        _fail(f"invalid-prerequisite-{name}")
    fields = set(value)
    allowed_fields = _PREREQUISITE_STATE_FIELDS | {"substantive_gaps"}
    if fields not in {
        frozenset(_PREREQUISITE_STATE_FIELDS),
        frozenset(allowed_fields),
    }:
        _fail(f"invalid-prerequisite-{name}")
    if value["state"] not in states:
        _fail(f"invalid-prerequisite-{name}")
    for field in _PREREQUISITE_STATE_FIELDS - {"state"}:
        if type(value[field]) is not bool:
            _fail(f"invalid-prerequisite-{name}")
    if "substantive_gaps" in value and type(value["substantive_gaps"]) is not bool:
        _fail(f"invalid-prerequisite-{name}")
    if value["state"] == "absent" and any(
        value[field] for field in _PREREQUISITE_STATE_FIELDS - {"state"}
    ):
        _fail(f"invalid-prerequisite-{name}")
    return {
        field: value[field]
        for field in (
            "state",
            "terminal_receipt",
            "expected_artifacts",
            "validation_passed",
            "fingerprints_match",
        )
    } | {"substantive_gaps": value.get("substantive_gaps", False)}


def _prerequisite_roles(value):
    if type(value) is not dict or set(value) != set(_PREREQUISITE_STAGES):
        _fail("invalid-prerequisite-roles")
    result = {}
    for stage in _PREREQUISITE_STAGES:
        roles = value[stage]
        contract_roles = _STAGE_CONTRACTS[stage]["roles"]
        if (
            type(roles) is not list
            or any(type(role) is not str or role not in contract_roles for role in roles)
            or len(roles) != len(set(roles))
        ):
            _fail("invalid-prerequisite-roles")
        result[stage] = set(roles)
    return result


def _prerequisite_outputs(value):
    if type(value) is not dict or set(value) != set(_PREREQUISITE_STAGES):
        _fail("invalid-prerequisite-output-folders")
    if any(type(value[stage]) is not bool for stage in _PREREQUISITE_STAGES):
        _fail("invalid-prerequisite-output-folders")
    return dict(value)


def _collection_authorization(value):
    record = _exact(
        value,
        _COLLECTION_AUTHORIZATION_FIELDS,
        "invalid-prerequisite-collection-authorization",
    )
    if any(type(record[field]) is not bool for field in record):
        _fail("invalid-prerequisite-collection-authorization")
    return dict(record)


def _mechanical_failure(name, record):
    if record["state"] == "invalid":
        return f"{name}-invalid"
    checks = (
        ("terminal_receipt", "terminal-receipt-missing"),
        ("expected_artifacts", "expected-artifacts-missing"),
        ("validation_passed", "validation-failed"),
        ("fingerprints_match", "fingerprints-mismatch"),
    )
    if record["state"] != "absent":
        for field, suffix in checks:
            if not record[field]:
                return f"{name}-{suffix}"
    return None


def _render_prerequisite_plan(document):
    yaml_bytes = _yaml(document)
    lines = [
        "# Municipal profile prerequisites",
        "",
        f"- Status: `{document['status']}`",
        f"- Next skill: `{document['next_skill'] or 'none'}`",
        f"- Internet: `{document['internet']}`",
        "",
        "## Required roles",
        "",
    ]
    lines.extend(
        [f"- `{role}`" for role in document["required_roles"]] or ["- None"]
    )
    lines.extend(["", "## Missing roles", ""])
    lines.extend(
        [f"- `{role}`" for role in document["missing_roles"]] or ["- None"]
    )
    lines.extend(["", "## Blocking reasons", ""])
    lines.extend(
        [f"- `{reason}`" for reason in document["blocking_reasons"]]
        or ["- None"]
    )
    lines.extend(["", "## Postconditions", ""])
    lines.extend(
        [f"- `{item}`" for item in document["postconditions"]] or ["- None"]
    )
    markdown_bytes = ("\n".join(lines) + "\n").encode()
    return {
        **document,
        "artifacts": [
            {
                "path": "municipal-profile-prerequisites.yaml",
                "bytes": yaml_bytes,
                "internet_sources": [],
            },
            {
                "path": "municipal-profile-prerequisites.md",
                "bytes": markdown_bytes,
                "internet_sources": [],
            },
        ],
    }


def _stage_prerequisite_plan(stage, roles, outputs, authorization):
    contract = _STAGE_CONTRACTS[stage]
    required_roles = list(contract["roles"])
    missing_roles = [role for role in required_roles if role not in roles[stage]]
    output_supplied = outputs[stage]
    blocking_reasons = [f"missing-role:{role}" for role in missing_roles]
    status = contract["ready_status"]
    if missing_roles:
        status = "input-required"
    elif stage == "collection" and not authorization["internet"]:
        status = "authorization-required"
        blocking_reasons = ["bounded-internet-authorization-required"]
    elif (
        stage == "collection"
        and authorization["fees_required"]
        and not authorization["fees_approved"]
    ):
        status = "authorization-required"
        blocking_reasons = ["fee-authorization-required"]
    elif not output_supplied:
        status = "input-required"
        blocking_reasons = ["fresh-output-folder-required"]
    document = {
        "version": 1,
        "workflow": "municipal-profile-prerequisites",
        "status": status,
        "next_skill": contract["skill"],
        "required_roles": required_roles,
        "missing_roles": missing_roles,
        "internet": contract["internet"],
        "output_folder": {"required": True, "supplied": output_supplied},
        "blocking_reasons": blocking_reasons,
        "postconditions": list(contract["postconditions"]),
    }
    return _render_prerequisite_plan(document)


def _blocked_prerequisite_plan(stage, reason, roles):
    contract = _STAGE_CONTRACTS[stage]
    required_roles = list(contract["roles"])
    document = {
        "version": 1,
        "workflow": "municipal-profile-prerequisites",
        "status": "blocked-invalid",
        "next_skill": contract["skill"],
        "required_roles": required_roles,
        "missing_roles": [
            role for role in required_roles if role not in roles[stage]
        ],
        "internet": contract["internet"],
        "output_folder": {"required": True, "supplied": False},
        "blocking_reasons": [reason],
        "postconditions": list(contract["postconditions"]),
    }
    return _render_prerequisite_plan(document)


def build_prerequisite_plan(
    *,
    policy_source_state,
    policy_catalog,
    policy_assessment,
    available_roles,
    output_folders,
    collection_authorization,
):
    """Return one deterministic next-stage plan from trusted-host state."""
    source = _prerequisite_state(
        policy_source_state,
        name="policy-source-state",
        states={"absent", "candidate", "approved", "invalid"},
    )
    catalog = _prerequisite_state(
        policy_catalog,
        name="policy-catalog",
        states={"absent", "valid", "invalid"},
    )
    assessment = _prerequisite_state(
        policy_assessment,
        name="policy-assessment",
        states={"absent", "valid", "invalid"},
    )
    roles = _prerequisite_roles(available_roles)
    outputs = _prerequisite_outputs(output_folders)
    authorization = _collection_authorization(collection_authorization)

    failure = _mechanical_failure("policy-catalog", catalog)
    if failure:
        return _blocked_prerequisite_plan("analysis", failure, roles)
    failure = _mechanical_failure("policy-assessment", assessment)
    if failure:
        return _blocked_prerequisite_plan("assessment", failure, roles)
    if assessment["state"] == "valid" and catalog["state"] != "valid":
        return _blocked_prerequisite_plan(
            "analysis", "policy-assessment-without-valid-catalog", roles
        )
    if catalog["state"] == "valid" and assessment["state"] == "valid":
        return _stage_prerequisite_plan("profile", roles, outputs, authorization)
    if catalog["state"] == "valid":
        return _stage_prerequisite_plan("assessment", roles, outputs, authorization)

    failure = _mechanical_failure("policy-source", source)
    if failure:
        return _blocked_prerequisite_plan("collection", failure, roles)
    if source["state"] == "approved":
        return _stage_prerequisite_plan("analysis", roles, outputs, authorization)
    if source["state"] == "candidate":
        return _render_prerequisite_plan(
            {
                "version": 1,
                "workflow": "municipal-profile-prerequisites",
                "status": "review-required",
                "next_skill": None,
                "required_roles": [],
                "missing_roles": [],
                "internet": "disabled",
                "output_folder": {"required": False, "supplied": False},
                "blocking_reasons": [
                    "independent-policy-source-review-required"
                ],
                "postconditions": ["approved_for_analysis-review-present"],
            }
        )
    return _stage_prerequisite_plan("collection", roles, outputs, authorization)


def build_profile_plan(
    *,
    identity,
    upstream_validations,
    selected_sources,
    evidence,
    entities,
    events,
    chains,
    comparisons,
    contradictions,
    similarity_features,
    domains,
    gaps,
    input_fingerprints,
):
    """Validate proposed records and return deterministic output-relative bytes."""
    if any(
        type(value) is not list
        for value in (
            selected_sources,
            evidence,
            entities,
            events,
            chains,
            comparisons,
            contradictions,
            similarity_features,
            domains,
            gaps,
        )
    ):
        _fail("invalid-profile")
    identity_record = _identity(identity)
    upstream = _upstream(upstream_validations)
    fingerprints = _fingerprints(input_fingerprints)
    source_map = _unique(
        sorted((_selected_source(item) for item in selected_sources), key=lambda item: item["source_id"]),
        "source_id",
        "duplicate-source",
    )
    evidence_map = _unique(
        sorted((_evidence(item, source_map) for item in evidence), key=lambda item: item["evidence_id"]),
        "evidence_id",
        "duplicate-evidence",
    )
    entity_map = _unique(
        sorted((_entity(item, set(evidence_map)) for item in entities), key=lambda item: item["entity_id"]),
        "entity_id",
        "duplicate-entity",
    )
    event_map = _unique(
        sorted(
            (_event(item, set(entity_map), set(evidence_map)) for item in events),
            key=lambda item: item["event_id"],
        ),
        "event_id",
        "duplicate-event",
    )
    feature_map = _unique(
        sorted((_feature(item, set(evidence_map)) for item in similarity_features), key=lambda item: item["feature_id"]),
        "feature_id",
        "duplicate-feature",
    )
    chain_records = sorted(
        (_chain(item, set(event_map), set(evidence_map)) for item in chains),
        key=lambda item: item["chain_id"],
    )
    _unique(chain_records, "chain_id", "duplicate-chain")
    comparison_records = sorted(
        (
            _comparison(item, set(event_map), set(feature_map), set(evidence_map))
            for item in comparisons
        ),
        key=lambda item: item["comparison_id"],
    )
    _unique(comparison_records, "comparison_id", "duplicate-comparison")
    contradiction_records = sorted(
        (_contradiction(item, set(evidence_map)) for item in contradictions),
        key=lambda item: item["contradiction_id"],
    )
    _unique(contradiction_records, "contradiction_id", "duplicate-contradiction")
    gap_map = _unique(
        sorted((_gap(item) for item in gaps), key=lambda item: item["gap_id"]),
        "gap_id",
        "duplicate-gap",
    )
    domain_records = [_domain(item, evidence_map, gap_map) for item in domains]
    if [item["domain"] for item in domain_records] != list(_DOMAINS):
        _fail("invalid-domain-order")
    profile = {
        "version": 1,
        **identity_record,
        "upstream_validations": upstream,
        "input_fingerprints": fingerprints,
        "evidence": list(evidence_map.values()),
        "entities": list(entity_map.values()),
        "events": list(event_map.values()),
        "chains": chain_records,
        "comparisons": comparison_records,
        "contradictions": contradiction_records,
        "similarity_features": list(feature_map.values()),
        "domains": domain_records,
    }
    _reject_conclusive_language(profile)
    lines = ["# Municipal profile", ""]
    for domain in domain_records:
        lines.extend([f"## {domain['domain']}", ""])
        lines.extend(f"- Question: {question}" for question in domain["questions"])
    if gap_map:
        lines.extend(["", "## Gaps", ""])
        lines.extend(f"- {gap['gap_id']}: {gap['description']}" for gap in gap_map.values())
    profile_bytes = _yaml(profile)
    gaps_bytes = _yaml(
        {
            "version": 1,
            "profile_id": identity_record["profile_id"],
            "gaps": list(gap_map.values()),
        }
    )
    markdown_bytes = ("\n".join(lines) + "\n").encode()
    validation = {
        "schema_version": 1,
        "valid": True,
        "profile_id": identity_record["profile_id"],
        "artifact_hashes": {
            "municipal-profile.yaml": hashlib.sha256(profile_bytes).hexdigest(),
            "municipal-profile-gaps.yaml": hashlib.sha256(gaps_bytes).hexdigest(),
            "municipal-profile.md": hashlib.sha256(markdown_bytes).hexdigest(),
        },
        "source_hashes": {
            source_id: source_map[source_id]["source_sha256"] for source_id in sorted(source_map)
        },
        "upstream_hashes": {
            role: upstream[role]["sha256"] for role in _UPSTREAM_ROLES
        },
        "input_fingerprints": fingerprints,
        "evidence_ids": list(evidence_map),
        "entity_ids": list(entity_map),
        "event_ids": list(event_map),
        "chain_ids": [item["chain_id"] for item in chain_records],
        "comparison_ids": [item["comparison_id"] for item in comparison_records],
        "contradiction_ids": [item["contradiction_id"] for item in contradiction_records],
        "feature_ids": list(feature_map),
        "gap_ids": list(gap_map),
    }
    artifacts = [
        {"path": "municipal-profile.yaml", "bytes": profile_bytes, "internet_sources": []},
        {
            "path": "municipal-profile-gaps.yaml",
            "bytes": gaps_bytes,
            "internet_sources": [],
        },
        {
            "path": "municipal-profile.md",
            "bytes": markdown_bytes,
            "internet_sources": [],
        },
        {
            "path": "municipal-profile-validation.json",
            "bytes": (
                json.dumps(validation, sort_keys=True, separators=(",", ":")) + "\n"
            ).encode(),
            "internet_sources": [],
        },
    ]
    return {"identity": identity_record, "artifacts": artifacts}
