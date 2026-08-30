"""Deterministic legal-authority source planning and validation."""

from __future__ import annotations

import hashlib
import re
from datetime import date
from pathlib import PurePosixPath

import yaml


_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
_URL = re.compile(r"^https?://[^\s/@]+(?::\d+)?(?:/[^\s]*)?$")
_SOURCE_FIELDS = {
    "frame_id",
    "source_id",
    "source_system_id",
    "provider_or_product_id",
    "artifact_path",
    "source_documentation_path",
    "artifact_bytes",
    "source_url",
    "query",
    "filters",
    "execution_date",
    "checked_date",
    "retrieved_at",
    "result_identity",
    "retrieval_order",
    "proposed_legal_role",
    "rejection_reason",
    "source_type",
    "decision_date",
    "citation_identity",
    "verification_state",
    "review_state",
    "retrieval_result",
    "limitations",
    "duplicate_of",
}
_SOURCE_DOCUMENT_FIELDS = _SOURCE_FIELDS - {
    "source_documentation_path",
    "artifact_bytes",
} | {"version", "sha256"}
_DATE_FIELDS = {"status", "date", "evidence", "gap"}
_CITATION_FIELDS = {"status", "case_name", "court", "citation", "docket_number"}
_GAP_FIELDS = {
    "frame_id",
    "gap_id",
    "gap_type",
    "source_system_id",
    "query",
    "filters",
    "checked_date",
    "known_missingness",
    "coverage_limit",
}
_CANDIDATE_FIELDS = {
    "frame_id",
    "source_id",
    "source_system_id",
    "provider_or_product_id",
    "source_documentation_path",
    "artifact_path",
    "sha256",
    "result_identity",
    "retrieval_order",
    "proposed_legal_role",
    "rejection_reason",
    "source_type",
    "identity_status",
    "verification_state",
    "review_state",
}
_FRAME_FIELDS = {
    "frame_id",
    "legal_question",
    "governing_jurisdiction",
    "court_hierarchy",
    "operative_date",
    "procedural_posture",
    "statute_or_rule_version",
    "material_factual_trigger",
    "source_universe",
    "access_and_cost_limits",
    "checked_through",
}
_PREMISE_FIELDS = {
    "premise_id",
    "premise_type",
    "statement",
    "status",
    "evidence",
    "correction",
    "gap",
}
_SOURCE_TYPES = {
    "official_text",
    "authenticated_opinion",
    "docket_copy",
    "mirror",
    "citator_record",
    "secondary_material",
    "unverified_reference",
}
_DATE_STATUS = {"documented", "uncertain", "missing"}
_IDENTITY_STATUS = {"proposed", "mistaken"}
_REVIEW = {"candidate", "rejected"}
_PREMISE_TYPES = {
    "case-identity",
    "judge-identity",
    "statute-or-rule-provision",
    "asserted-holding",
    "jurisdiction",
    "operative-date",
    "current-validity",
}
_PREMISE_STATUS = {"verified", "false", "unresolved"}
_REJECTION_REASONS = {
    "wrong-issue",
    "wrong-jurisdiction",
    "wrong-court",
    "wrong-date",
    "wrong-statute",
    "wrong-rule-version",
    "wrong-posture",
    "wrong-authority-level",
    "wrong-treatment",
    "wrong-factual-trigger",
}
_GAP_TYPES = {
    "empty",
    "incomplete",
    "inaccessible",
    "paid",
    "ambiguous",
    "out_of_scope",
}


class AuthoritySourceError(ValueError):
    """A stable bounded authority-source validation failure."""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def _fail(code):
    raise AuthoritySourceError(code)


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


def _optional_text(value, code):
    if value is None:
        return None
    return _text(value, code)


def _positive_integer(value, code):
    if type(value) is not int or value < 1:
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


def _relative(value, code):
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        _fail(code)
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or any(part in {"", ".", ".."} for part in path.parts)
        or path.parts[0] in {"temp", ".skill-runs"}
    ):
        _fail(code)
    return path.as_posix()


def _strings(value, code):
    if type(value) is not list:
        _fail(code)
    result = [_text(item, code) for item in value]
    if len(result) != len(set(result)):
        _fail(code)
    return result


def _retrieval_frame(value):
    code = "invalid-retrieval-frame"
    record = _exact(value, _FRAME_FIELDS, code)
    source_universe = [
        _identifier(item, code) for item in _strings(record["source_universe"], code)
    ]
    hierarchy = _strings(record["court_hierarchy"], code)
    limits = _strings(record["access_and_cost_limits"], code)
    if not source_universe or not hierarchy or not limits:
        _fail(code)
    return {
        "frame_id": _identifier(record["frame_id"], code),
        "legal_question": _text(record["legal_question"], code),
        "governing_jurisdiction": _text(record["governing_jurisdiction"], code),
        "court_hierarchy": hierarchy,
        "operative_date": _date(record["operative_date"], code),
        "procedural_posture": _text(record["procedural_posture"], code),
        "statute_or_rule_version": _text(record["statute_or_rule_version"], code),
        "material_factual_trigger": _text(record["material_factual_trigger"], code),
        "source_universe": source_universe,
        "access_and_cost_limits": limits,
        "checked_through": _date(record["checked_through"], code),
    }


def _premise(value):
    code = "invalid-premise-record"
    record = _exact(value, _PREMISE_FIELDS, code)
    status = record["status"]
    if record["premise_type"] not in _PREMISE_TYPES or status not in _PREMISE_STATUS:
        _fail(code)
    evidence = _optional_text(record["evidence"], code)
    correction = _optional_text(record["correction"], code)
    gap = _optional_text(record["gap"], code)
    if status == "verified":
        if evidence is None or correction is not None or gap is not None:
            _fail(code)
    elif status == "false":
        if evidence is None or correction is None or gap is not None:
            _fail(code)
    elif evidence is not None or correction is not None or gap is None:
        _fail(code)
    return {
        "premise_id": _identifier(record["premise_id"], code),
        "premise_type": record["premise_type"],
        "statement": _text(record["statement"], code),
        "status": status,
        "evidence": evidence,
        "correction": correction,
        "gap": gap,
    }


def _url(value, code):
    if (
        not isinstance(value, str)
        or len(value) > 2048
        or _URL.fullmatch(value) is None
        or ".." in value.split("/", 3)[2]
    ):
        _fail(code)
    return value


def _decision_date(value, code):
    record = _exact(value, _DATE_FIELDS, code)
    status = record["status"]
    if status not in _DATE_STATUS:
        _fail(code)
    decision_date = record["date"]
    evidence = record["evidence"]
    gap = record["gap"]
    if status == "documented":
        decision_date = _date(decision_date, code)
        evidence = _text(evidence, code)
        if gap is not None:
            _fail(code)
    else:
        if decision_date is not None:
            decision_date = _date(decision_date, code)
        if evidence is not None:
            evidence = _text(evidence, code)
        gap = _text(gap, code)
    return {
        "status": status,
        "date": decision_date,
        "evidence": evidence,
        "gap": gap,
    }


def _citation_identity(value, code):
    record = _exact(value, _CITATION_FIELDS, code)
    if record["status"] not in _IDENTITY_STATUS:
        _fail(code)
    return {
        "status": record["status"],
        "case_name": _text(record["case_name"], code),
        "court": _text(record["court"], code),
        "citation": _text(record["citation"], code),
        "docket_number": _text(record["docket_number"], code),
    }


def _source_document(value, retrieval_frame):
    record = _exact(value, _SOURCE_FIELDS, "invalid-source-record")
    if record["frame_id"] != retrieval_frame["frame_id"]:
        _fail("invalid-source-record")
    source_id = _identifier(record["source_id"], "invalid-source-record")
    source_system_id = _identifier(
        record["source_system_id"], "invalid-source-record"
    )
    if source_system_id not in retrieval_frame["source_universe"]:
        _fail("invalid-source-record")
    artifact_path = _relative(record["artifact_path"], "invalid-source-record")
    documentation_path = _relative(
        record["source_documentation_path"], "invalid-source-record"
    )
    artifact = PurePosixPath(artifact_path)
    documentation = PurePosixPath(documentation_path)
    if (
        artifact.parts[0] != "sources"
        or documentation.parts[0] != "sources"
        or artifact.parent != documentation.parent
        or not documentation.name.endswith(".SOURCE.yaml")
        or artifact_path == documentation_path
    ):
        _fail("invalid-source-record")
    contents = record["artifact_bytes"]
    if not isinstance(contents, bytes) or not contents:
        _fail("invalid-source-record")
    checked_date = _date(record["checked_date"], "invalid-source-record")
    execution_date = _date(record["execution_date"], "invalid-source-record")
    if checked_date > retrieval_frame["checked_through"] or execution_date > checked_date:
        _fail("invalid-source-record")
    retrieved_at = record["retrieved_at"]
    if not isinstance(retrieved_at, str) or _UTC.fullmatch(retrieved_at) is None:
        _fail("invalid-source-record")
    source_type = record["source_type"]
    review_state = record["review_state"]
    rejection_reason = record["rejection_reason"]
    if (
        source_type not in _SOURCE_TYPES
        or record["verification_state"] != "unverified"
        or review_state not in _REVIEW
        or record["retrieval_result"] != "retrieved"
    ):
        _fail("invalid-source-record")
    if (review_state == "candidate" and rejection_reason is not None) or (
        review_state == "rejected" and rejection_reason not in _REJECTION_REASONS
    ):
        _fail("invalid-source-record")
    filters = _strings(record["filters"], "invalid-source-record")
    limitations = _strings(record["limitations"], "invalid-source-record")
    duplicate_of = [
        _identifier(item, "invalid-source-record")
        for item in _strings(record["duplicate_of"], "invalid-source-record")
    ]
    if source_id in duplicate_of:
        _fail("invalid-source-record")
    identity = _citation_identity(record["citation_identity"], "invalid-source-record")
    if identity["status"] == "mistaken" and review_state != "rejected":
        _fail("invalid-source-record")
    document = {
        "version": 1,
        "frame_id": retrieval_frame["frame_id"],
        "source_id": source_id,
        "source_system_id": source_system_id,
        "provider_or_product_id": _optional_text(
            record["provider_or_product_id"], "invalid-source-record"
        ),
        "artifact_path": artifact_path,
        "sha256": hashlib.sha256(contents).hexdigest(),
        "source_url": _url(record["source_url"], "invalid-source-record"),
        "query": _text(record["query"], "invalid-source-record"),
        "filters": filters,
        "execution_date": execution_date,
        "checked_date": checked_date,
        "retrieved_at": retrieved_at,
        "result_identity": _text(record["result_identity"], "invalid-source-record"),
        "retrieval_order": _positive_integer(
            record["retrieval_order"], "invalid-source-record"
        ),
        "proposed_legal_role": _text(
            record["proposed_legal_role"], "invalid-source-record"
        ),
        "rejection_reason": rejection_reason,
        "source_type": source_type,
        "decision_date": _decision_date(
            record["decision_date"], "invalid-source-record"
        ),
        "citation_identity": identity,
        "verification_state": "unverified",
        "review_state": review_state,
        "retrieval_result": "retrieved",
        "limitations": limitations,
        "duplicate_of": duplicate_of,
    }
    return document, documentation_path


def _gap(value, retrieval_frame):
    record = _exact(value, _GAP_FIELDS, "invalid-gap-record")
    checked_date = _date(record["checked_date"], "invalid-gap-record")
    if (
        record["frame_id"] != retrieval_frame["frame_id"]
        or checked_date > retrieval_frame["checked_through"]
        or record["gap_type"] not in _GAP_TYPES
    ):
        _fail("invalid-gap-record")
    source_system_id = _identifier(
        record["source_system_id"], "invalid-gap-record"
    )
    if source_system_id not in retrieval_frame["source_universe"]:
        _fail("invalid-gap-record")
    return {
        "frame_id": retrieval_frame["frame_id"],
        "gap_id": _identifier(record["gap_id"], "invalid-gap-record"),
        "gap_type": record["gap_type"],
        "source_system_id": source_system_id,
        "query": _text(record["query"], "invalid-gap-record"),
        "filters": _strings(record["filters"], "invalid-gap-record"),
        "checked_date": checked_date,
        "known_missingness": _text(
            record["known_missingness"], "invalid-gap-record"
        ),
        "coverage_limit": _text(record["coverage_limit"], "invalid-gap-record"),
    }


def _yaml(value):
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=True).encode("utf-8")


def _internet_source(value, code):
    record = _exact(value, {"url", "retrieved_at", "sha256"}, code)
    if (
        not isinstance(record["retrieved_at"], str)
        or _UTC.fullmatch(record["retrieved_at"]) is None
        or not isinstance(record["sha256"], str)
        or _SHA256.fullmatch(record["sha256"]) is None
    ):
        _fail(code)
    return {
        "url": _url(record["url"], code),
        "retrieved_at": record["retrieved_at"],
        "sha256": record["sha256"],
    }


def _validate_result_identities(documents):
    result_identities = {}
    for document in documents:
        result_identities.setdefault(document["result_identity"], []).append(document)
    for duplicates in result_identities.values():
        if len(duplicates) > 1:
            source_ids = {document["source_id"] for document in duplicates}
            if not any(
                source_ids & set(document["duplicate_of"])
                for document in duplicates
            ):
                _fail("duplicate-result-identity")


def build_collection_plan(retrieval_frame, premises, sources, gaps):
    """Return one bounded deterministic retrieval artifact plan."""
    if type(premises) is not list or type(sources) is not list or type(gaps) is not list:
        _fail("invalid-collection")
    retrieval_frame = _retrieval_frame(retrieval_frame)
    premise_records = sorted(
        (_premise(item) for item in premises), key=lambda item: item["premise_id"]
    )
    premise_ids = [item["premise_id"] for item in premise_records]
    if not premise_ids or len(premise_ids) != len(set(premise_ids)):
        _fail("invalid-premise-record")
    prepared = [
        _source_document(source, retrieval_frame) for source in sources
    ]
    prepared.sort(key=lambda item: item[0]["retrieval_order"])
    source_ids = [item[0]["source_id"] for item in prepared]
    retrieval_orders = [item[0]["retrieval_order"] for item in prepared]
    documentation_paths = [item[1] for item in prepared]
    artifact_paths = [item[0]["artifact_path"] for item in prepared]
    if (
        len(source_ids) != len(set(source_ids))
        or len(retrieval_orders) != len(set(retrieval_orders))
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
    _validate_result_identities([document for document, _ in prepared])

    originals = {source["source_id"]: source for source in sources}
    artifacts = []
    candidates = []
    candidate_internet_sources = []
    for document, documentation_path in prepared:
        contents = bytes(originals[document["source_id"]]["artifact_bytes"])
        internet_sources = [
            {
                "url": document["source_url"],
                "retrieved_at": document["retrieved_at"],
                "sha256": document["sha256"],
            }
        ]
        candidate_internet_sources.extend(internet_sources)
        artifacts.extend(
            [
                {
                    "path": document["artifact_path"],
                    "bytes": contents,
                    "internet_sources": internet_sources,
                },
                {
                    "path": documentation_path,
                    "bytes": _yaml(document),
                    "internet_sources": internet_sources,
                },
            ]
        )
        candidates.append(
            {
                "frame_id": document["frame_id"],
                "source_id": document["source_id"],
                "source_system_id": document["source_system_id"],
                "provider_or_product_id": document["provider_or_product_id"],
                "source_documentation_path": documentation_path,
                "artifact_path": document["artifact_path"],
                "sha256": document["sha256"],
                "result_identity": document["result_identity"],
                "retrieval_order": document["retrieval_order"],
                "proposed_legal_role": document["proposed_legal_role"],
                "rejection_reason": document["rejection_reason"],
                "source_type": document["source_type"],
                "identity_status": document["citation_identity"]["status"],
                "verification_state": "unverified",
                "review_state": document["review_state"],
            }
        )
    gap_records = sorted(
        (_gap(item, retrieval_frame) for item in gaps),
        key=lambda item: item["gap_id"],
    )
    gap_ids = [item["gap_id"] for item in gap_records]
    if len(gap_ids) != len(set(gap_ids)):
        _fail("duplicate-gap")
    artifacts.extend(
        [
            {
                "path": "authority-retrieval-frame.yaml",
                "bytes": _yaml({"version": 1, **retrieval_frame}),
                "internet_sources": [],
            },
            {
                "path": "authority-retrieval-premises.yaml",
                "bytes": _yaml(
                    {
                        "version": 1,
                        "frame_id": retrieval_frame["frame_id"],
                        "premises": premise_records,
                    }
                ),
                "internet_sources": [],
            },
            {
                "path": "authority-source-candidates.yaml",
                "bytes": _yaml(
                    {
                        "version": 1,
                        "frame_id": retrieval_frame["frame_id"],
                        "checked_through": retrieval_frame["checked_through"],
                        "sources": candidates,
                    }
                ),
                "internet_sources": candidate_internet_sources,
            },
            {
                "path": "authority-source-gaps.yaml",
                "bytes": _yaml(
                    {
                        "version": 1,
                        "frame_id": retrieval_frame["frame_id"],
                        "checked_through": retrieval_frame["checked_through"],
                        "gaps": gap_records,
                    }
                ),
                "internet_sources": [],
            },
        ]
    )
    plan = {
        "frame_id": retrieval_frame["frame_id"],
        "checked_through": retrieval_frame["checked_through"],
        "artifacts": artifacts,
    }
    validate_collection_plan(plan)
    return plan


def _load_yaml(contents, code):
    try:
        document = yaml.safe_load(contents)
    except (UnicodeError, yaml.YAMLError):
        _fail(code)
    if type(document) is not dict:
        _fail(code)
    return document


def _validate_source_yaml(value, retrieval_frame):
    record = _exact(value, _SOURCE_DOCUMENT_FIELDS, "invalid-source-yaml")
    if (
        record["version"] != 1
        or record["frame_id"] != retrieval_frame["frame_id"]
    ):
        _fail("invalid-source-yaml")
    source_id = _identifier(record["source_id"], "invalid-source-yaml")
    source_system_id = _identifier(
        record["source_system_id"], "invalid-source-yaml"
    )
    if source_system_id not in retrieval_frame["source_universe"]:
        _fail("invalid-source-yaml")
    artifact_path = _relative(record["artifact_path"], "invalid-source-yaml")
    if PurePosixPath(artifact_path).parts[0] != "sources":
        _fail("invalid-source-yaml")
    if not isinstance(record["sha256"], str) or _SHA256.fullmatch(record["sha256"]) is None:
        _fail("invalid-source-yaml")
    checked_date = _date(record["checked_date"], "invalid-source-yaml")
    execution_date = _date(record["execution_date"], "invalid-source-yaml")
    if checked_date > retrieval_frame["checked_through"] or execution_date > checked_date:
        _fail("invalid-source-yaml")
    if not isinstance(record["retrieved_at"], str) or _UTC.fullmatch(record["retrieved_at"]) is None:
        _fail("invalid-source-yaml")
    if (
        record["source_type"] not in _SOURCE_TYPES
        or record["verification_state"] != "unverified"
        or record["review_state"] not in _REVIEW
        or record["retrieval_result"] != "retrieved"
    ):
        _fail("invalid-source-yaml")
    _url(record["source_url"], "invalid-source-yaml")
    _optional_text(record["provider_or_product_id"], "invalid-source-yaml")
    _text(record["query"], "invalid-source-yaml")
    _strings(record["filters"], "invalid-source-yaml")
    _text(record["result_identity"], "invalid-source-yaml")
    _positive_integer(record["retrieval_order"], "invalid-source-yaml")
    _text(record["proposed_legal_role"], "invalid-source-yaml")
    _decision_date(record["decision_date"], "invalid-source-yaml")
    identity = _citation_identity(record["citation_identity"], "invalid-source-yaml")
    if identity["status"] == "mistaken" and record["review_state"] != "rejected":
        _fail("invalid-source-yaml")
    rejection_reason = record["rejection_reason"]
    if (record["review_state"] == "candidate" and rejection_reason is not None) or (
        record["review_state"] == "rejected"
        and rejection_reason not in _REJECTION_REASONS
    ):
        _fail("invalid-source-yaml")
    _strings(record["limitations"], "invalid-source-yaml")
    duplicates = [
        _identifier(item, "invalid-source-yaml")
        for item in _strings(record["duplicate_of"], "invalid-source-yaml")
    ]
    if source_id in duplicates:
        _fail("invalid-source-yaml")
    return record


def validate_collection_plan(plan):
    """Validate a complete artifact plan and every documented hash."""
    value = _exact(
        plan, {"frame_id", "checked_through", "artifacts"}, "invalid-plan"
    )
    frame_id = _identifier(value["frame_id"], "invalid-plan")
    checked_through = _date(value["checked_through"], "invalid-plan")
    if type(value["artifacts"]) is not list:
        _fail("invalid-plan")
    by_path = {}
    internet_by_path = {}
    for artifact in value["artifacts"]:
        item = _exact(artifact, {"path", "bytes", "internet_sources"}, "invalid-plan")
        path = _relative(item["path"], "invalid-plan")
        if (
            path in by_path
            or not isinstance(item["bytes"], bytes)
            or type(item["internet_sources"]) is not list
        ):
            _fail("invalid-plan")
        by_path[path] = item["bytes"]
        internet_by_path[path] = [
            _internet_source(source, "invalid-internet-source")
            for source in item["internet_sources"]
        ]
    fixed_paths = {
        "authority-retrieval-frame.yaml",
        "authority-retrieval-premises.yaml",
        "authority-source-candidates.yaml",
        "authority-source-gaps.yaml",
    }
    if not fixed_paths.issubset(by_path):
        _fail("invalid-plan")

    frame_document = _load_yaml(
        by_path["authority-retrieval-frame.yaml"], "invalid-retrieval-frame"
    )
    if set(frame_document) != {"version", *_FRAME_FIELDS} or frame_document.pop(
        "version"
    ) != 1:
        _fail("invalid-retrieval-frame")
    retrieval_frame = _retrieval_frame(frame_document)
    if (
        retrieval_frame["frame_id"] != frame_id
        or retrieval_frame["checked_through"] != checked_through
        or internet_by_path["authority-retrieval-frame.yaml"]
    ):
        _fail("invalid-retrieval-frame")

    premise_document = _load_yaml(
        by_path["authority-retrieval-premises.yaml"], "invalid-premise-record"
    )
    if (
        set(premise_document) != {"version", "frame_id", "premises"}
        or premise_document["version"] != 1
        or premise_document["frame_id"] != frame_id
        or type(premise_document["premises"]) is not list
        or internet_by_path["authority-retrieval-premises.yaml"]
    ):
        _fail("invalid-premise-record")
    premise_records = [_premise(item) for item in premise_document["premises"]]
    premise_ids = [item["premise_id"] for item in premise_records]
    if (
        not premise_ids
        or premise_ids != sorted(premise_ids)
        or len(premise_ids) != len(set(premise_ids))
    ):
        _fail("invalid-premise-record")

    candidates = _load_yaml(
        by_path["authority-source-candidates.yaml"], "invalid-candidate-index"
    )
    if (
        set(candidates) != {"version", "frame_id", "checked_through", "sources"}
        or candidates["version"] != 1
        or candidates["frame_id"] != frame_id
        or candidates["checked_through"] != checked_through
        or type(candidates["sources"]) is not list
    ):
        _fail("invalid-candidate-index")
    source_ids = []
    documents = []
    expected_paths = set(fixed_paths)
    for candidate in candidates["sources"]:
        entry = _exact(candidate, _CANDIDATE_FIELDS, "invalid-candidate-index")
        source_id = _identifier(entry["source_id"], "invalid-candidate-index")
        documentation_path = _relative(
            entry["source_documentation_path"], "invalid-candidate-index"
        )
        artifact_path = _relative(entry["artifact_path"], "invalid-candidate-index")
        documentation = PurePosixPath(documentation_path)
        artifact = PurePosixPath(artifact_path)
        if (
            documentation.parts[0] != "sources"
            or documentation.parent != artifact.parent
            or not documentation.name.endswith(".SOURCE.yaml")
            or documentation_path not in by_path
            or artifact_path not in by_path
        ):
            _fail("invalid-source-yaml")
        document = _validate_source_yaml(
            _load_yaml(by_path[documentation_path], "invalid-source-yaml"),
            retrieval_frame,
        )
        if (
            document["frame_id"] != entry["frame_id"]
            or document["source_id"] != source_id
            or document["source_system_id"] != entry["source_system_id"]
            or document["provider_or_product_id"]
            != entry["provider_or_product_id"]
            or document["artifact_path"] != artifact_path
            or document["sha256"] != entry["sha256"]
            or document["result_identity"] != entry["result_identity"]
            or document["retrieval_order"] != entry["retrieval_order"]
            or document["proposed_legal_role"] != entry["proposed_legal_role"]
            or document["rejection_reason"] != entry["rejection_reason"]
            or document["source_type"] != entry["source_type"]
            or document["citation_identity"]["status"] != entry["identity_status"]
            or document["verification_state"] != entry["verification_state"]
            or document["review_state"] != entry["review_state"]
        ):
            _fail("invalid-candidate-index")
        if hashlib.sha256(by_path[artifact_path]).hexdigest() != document["sha256"]:
            _fail("hash-mismatch")
        expected_internet = [
            {
                "url": document["source_url"],
                "retrieved_at": document["retrieved_at"],
                "sha256": document["sha256"],
            }
        ]
        if (
            internet_by_path[artifact_path] != expected_internet
            or internet_by_path[documentation_path] != expected_internet
        ):
            _fail("invalid-internet-source")
        source_ids.append(source_id)
        documents.append(document)
        expected_paths.update({artifact_path, documentation_path})
    retrieval_orders = [
        document["retrieval_order"] for document in documents
    ]
    if (
        retrieval_orders != sorted(retrieval_orders)
        or len(retrieval_orders) != len(set(retrieval_orders))
        or len(source_ids) != len(set(source_ids))
    ):
        _fail("invalid-candidate-index")
    known_ids = set(source_ids)
    if any(
        duplicate not in known_ids
        for document in documents
        for duplicate in document["duplicate_of"]
    ):
        _fail("invalid-source-yaml")
    _validate_result_identities(documents)
    gaps = _load_yaml(by_path["authority-source-gaps.yaml"], "invalid-gap-index")
    if (
        set(gaps) != {"version", "frame_id", "checked_through", "gaps"}
        or gaps["version"] != 1
        or gaps["frame_id"] != frame_id
        or gaps["checked_through"] != checked_through
        or type(gaps["gaps"]) is not list
    ):
        _fail("invalid-gap-index")
    gap_records = [_gap(item, retrieval_frame) for item in gaps["gaps"]]
    gap_ids = [item["gap_id"] for item in gap_records]
    if gap_ids != sorted(gap_ids) or len(gap_ids) != len(set(gap_ids)):
        _fail("invalid-gap-index")
    expected_candidate_internet = [
        source
        for candidate in candidates["sources"]
        for source in internet_by_path[candidate["artifact_path"]]
    ]
    if (
        internet_by_path["authority-source-candidates.yaml"]
        != expected_candidate_internet
        or internet_by_path["authority-source-gaps.yaml"]
    ):
        _fail("invalid-internet-source")
    if set(by_path) != expected_paths:
        _fail("invalid-plan")
    return True
