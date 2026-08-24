import argparse
import hashlib
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path, PurePosixPath


STABLE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
MAX_INPUT_BYTES = 1_000_000
SNAPSHOT_KEYS = {
    "schema_version",
    "snapshot_id",
    "version",
    "checked_through",
    "research_protocol",
    "attorneys",
    "matters",
    "sources",
    "gaps",
}
PROTOCOL_KEYS = {
    "queries",
    "deduplication_method",
    "coverage_status",
    "denominator_definition",
    "candidate_record_count",
    "retrieved_record_count",
    "unresolved_record_count",
    "unavailable_record_count",
}
QUERY_KEYS = {"query_id", "query", "searched_on", "systems", "scope"}
ATTORNEY_KEYS = {"attorney_id", "professional_name"}
MATTER_KEYS = {
    "matter_id",
    "court",
    "docket",
    "posture",
    "represented_party",
    "alignment_group_ids",
}
SOURCE_KEYS = {
    "source_id",
    "source_role",
    "retrieved_on",
    "source_date",
    "actor_ids",
    "matter_id",
    "content",
    "sha256",
}
SOURCE_ROLES = {
    "current-docket-filed-paper",
    "official-court-record",
    "courtlistener-recap",
    "bar-directory",
    "firm-biography",
    "attorney-publication",
    "approved-public-case-artifact",
}
BEHAVIOR_SOURCE_ROLES = {
    "current-docket-filed-paper",
    "official-court-record",
    "courtlistener-recap",
    "approved-public-case-artifact",
}
SNAPSHOT_GAP_KEYS = {
    "gap_id",
    "query_ids",
    "matter_ids",
    "reason",
    "description",
}
SNAPSHOT_GAP_REASONS = {
    "unavailable-public-record",
    "fee-gated",
    "identity-uncertain",
    "coverage-incomplete",
}
OVERLAY_KEYS = {
    "schema_version",
    "overlay_id",
    "version",
    "generated_at",
    "source_snapshot",
    "identity_records",
    "team_records",
    "historical_arguments",
    "judicial_treatments",
    "current_attack_links",
    "patterns",
    "forecasts",
    "overrides",
    "gaps",
    "ledger_fingerprints",
    "review_slices",
}
SNAPSHOT_REFERENCE_KEYS = {"snapshot_id", "version", "sha256", "checked_through"}
IDENTITY_KEYS = {
    "identity_id",
    "attorney_id",
    "professional_name",
    "bar_status",
    "bar_status_checked_on",
    "firm_affiliations",
    "appearances",
    "source_ids",
}
FIRM_KEYS = {"firm_name", "start_date", "end_date", "source_ids"}
APPEARANCE_KEYS = {
    "matter_id",
    "represented_party",
    "start_date",
    "end_date",
    "roles",
    "source_ids",
}
ATTRIBUTION_ROLES = {
    "signer",
    "named-author",
    "oral-advocate",
    "appearance-counsel",
    "listed-counsel",
    "counsel-team",
}
DIRECT_ATTRIBUTION_ROLES = {"signer", "named-author", "oral-advocate"}
TEAM_KEYS = {
    "team_id",
    "matter_id",
    "version",
    "effective_start",
    "effective_end",
    "member_attorney_ids",
    "represented_party",
    "alignment_group_ids",
    "source_ids",
}
LOCATION_KEYS = {"source_id", "page", "heading", "quote"}
ARGUMENT_KEYS = {
    "argument_id",
    "matter_id",
    "team_id",
    "attorney_id",
    "attribution_role",
    "source_ids",
    "source_location",
    "date",
    "posture",
    "represented_party",
    "alignment_group_ids",
    "claim_id",
    "challenged_act_id",
    "element_or_defense",
    "qualified_immunity_prong",
    "requested_relief",
    "status",
}
TREATMENT_KEYS = {
    "treatment_id",
    "argument_id",
    "court_actor",
    "source_ids",
    "source_location",
    "date",
    "treatment",
}
TREATMENTS = {
    "recommended",
    "adopted",
    "rejected",
    "modified",
    "superseded",
    "reversed",
    "vacated",
    "unresolved",
}
ATTACK_LINK_KEYS = {
    "link_id",
    "attack_id",
    "team_id",
    "alignment_group_id",
    "claim_id",
    "defendant_ids",
    "challenged_act_ids",
    "source_ids",
}
MISSINGNESS_KEYS = {"unresolved", "unavailable"}
PATTERN_KEYS = {
    "pattern_id",
    "pattern_type",
    "comparable_argument_ids",
    "scope",
    "selection_method",
    "denominator",
    "coded_record_count",
    "missingness",
    "posture",
    "supporting_argument_ids",
    "contrary_argument_ids",
    "treatment_ids",
    "conclusion",
    "confidence",
    "source_ids",
    "checked_through",
    "limits",
}
PATTERN_TYPES = {
    "recurring-defense",
    "court-documented-loss",
    "cross-case-comparison",
}
FORECAST_KEYS = {
    "forecast_id",
    "professional_move",
    "pattern_ids",
    "comparable_argument_ids",
    "denominator",
    "coded_record_count",
    "missingness",
    "posture",
    "supporting_argument_ids",
    "contrary_argument_ids",
    "confidence",
    "source_ids",
    "checked_through",
    "limits",
}
CONFIDENCE = {"low", "moderate", "high"}
OVERRIDE_KEYS = {
    "override_id",
    "instruction_id",
    "action",
    "scope",
    "affected_ids",
    "rationale",
}
OVERLAY_GAP_KEYS = {"gap_id", "source_gap_ids", "scope", "consequence"}
SLICE_KEYS = {
    "slice_id",
    "job_id",
    "review_kind",
    "alignment_group_id",
    "target_artifact_id",
    "team_ids",
    "identity_ids",
    "historical_argument_ids",
    "treatment_ids",
    "current_attack_link_ids",
    "pattern_ids",
    "forecast_ids",
    "common_attack_ids",
}
PIN_KEYS = {
    "kind",
    "overlay_id",
    "version",
    "sha256",
    "checked_through",
    "validator_result",
    "source_snapshot_id",
    "source_snapshot_version",
    "source_snapshot_sha256",
}
MANIFEST_KEYS = {
    "schema_version",
    "filing_version_id",
    "artifact_id",
    "artifact_sha256",
    "source_snapshot",
    "overlays",
}
LEDGER_NAMES = {
    "identity_records",
    "team_records",
    "historical_arguments",
    "judicial_treatments",
    "current_attack_links",
    "patterns",
    "forecasts",
    "overrides",
    "gaps",
    "review_slices",
}
PERSONAL_TERMS = re.compile(
    r"\b(?:family|politics|private life|protected trait|personality|rumou?r|irrelevant social media)\b",
    re.IGNORECASE,
)
CERTAINTY_TERMS = re.compile(r"\b(?:will|always|never|certain(?:ly|ty)?)\b", re.IGNORECASE)
OUTCOME_TERMS = re.compile(r"\b(?:win|wins|won|lose|loses|lost|case outcome|judge will)\b", re.IGNORECASE)
LEGAL_EFFECT_TERMS = re.compile(
    r"\b(?:automatically|automatic)\b.{0,80}\b(?:waiv|concession|estoppel|misconduct|bad faith)",
    re.IGNORECASE,
)


def _finding(finding_id, path, message):
    return {"id": finding_id, "path": path, "message": message}


def _add(findings, finding_id, path, message):
    findings.append(_finding(finding_id, path, message))


def _canonical_sha256(value):
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _text_sha256(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _exact(value, keys):
    return isinstance(value, dict) and set(value) == keys


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip()) and value == value.strip()


def _stable(value):
    return _nonempty(value) and STABLE_ID.fullmatch(value) is not None


def _sha(value):
    return isinstance(value, str) and SHA256.fullmatch(value) is not None


def _date(value):
    if not isinstance(value, str):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _datetime(value):
    if not isinstance(value, str):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def _nonnegative_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _id_list(value, nonempty=False):
    return (
        isinstance(value, list)
        and (not nonempty or bool(value))
        and all(_stable(item) for item in value)
        and len(value) == len(set(value))
    )


def _string_list(value, nonempty=False):
    return (
        isinstance(value, list)
        and (not nonempty or bool(value))
        and all(_nonempty(item) for item in value)
        and len(value) == len(set(value))
    )


def _one_of(value, choices):
    return isinstance(value, str) and value in choices


def _safe_id_set(value):
    return set(value) if _id_list(value) else set()


def _duplicate_ids(records, key):
    values = [record.get(key) for record in records if isinstance(record, dict)]
    return len(values) != len(set(value for value in values if _stable(value)))


def _source_map(snapshot):
    return {
        item.get("source_id"): item
        for item in snapshot.get("sources", [])
        if isinstance(item, dict) and _stable(item.get("source_id"))
    }


def _all_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _all_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _all_strings(item)


def validate_snapshot(snapshot):
    findings = []
    if not _exact(snapshot, SNAPSHOT_KEYS):
        _add(findings, "snapshot-structure-invalid", "$", "snapshot must contain the exact required fields")
        return findings
    if snapshot.get("schema_version") != "1.0" or not _stable(snapshot.get("snapshot_id")) or not _nonempty(snapshot.get("version")) or not _date(snapshot.get("checked_through")):
        _add(findings, "snapshot-structure-invalid", "$", "snapshot root values are invalid")
    protocol = snapshot.get("research_protocol")
    if not _exact(protocol, PROTOCOL_KEYS):
        _add(findings, "snapshot-structure-invalid", "$.research_protocol", "research protocol is invalid")
        protocol = {}
    counts = [
        protocol.get("candidate_record_count"),
        protocol.get("retrieved_record_count"),
        protocol.get("unresolved_record_count"),
        protocol.get("unavailable_record_count"),
    ]
    if protocol.get("coverage_status") not in ("complete", "incomplete") or not _nonempty(protocol.get("deduplication_method")) or not _nonempty(protocol.get("denominator_definition")) or not all(_nonnegative_int(item) for item in counts):
        _add(findings, "snapshot-structure-invalid", "$.research_protocol", "research protocol values are invalid")
    if all(_nonnegative_int(item) for item in counts):
        candidate, retrieved, unresolved, unavailable = counts
        if candidate != retrieved + unresolved + unavailable:
            _add(findings, "snapshot-denominator-invalid", "$.research_protocol", "candidate count must reconcile to retrieved and missing records")
        expected_status = "complete" if unresolved == 0 and unavailable == 0 else "incomplete"
        if protocol.get("coverage_status") != expected_status:
            _add(findings, "snapshot-denominator-invalid", "$.research_protocol.coverage_status", "coverage status does not match missingness")
    queries = protocol.get("queries")
    if not isinstance(queries, list) or not queries:
        _add(findings, "snapshot-structure-invalid", "$.research_protocol.queries", "at least one query is required")
        queries = []
    for index, query in enumerate(queries):
        if not _exact(query, QUERY_KEYS) or not _stable(query.get("query_id")) or not _nonempty(query.get("query")) or not _date(query.get("searched_on")) or not _string_list(query.get("systems"), nonempty=True) or not _nonempty(query.get("scope")):
            _add(findings, "snapshot-structure-invalid", f"$.research_protocol.queries[{index}]", "query is invalid")
    attorneys = snapshot.get("attorneys")
    if not isinstance(attorneys, list) or not attorneys:
        _add(findings, "snapshot-structure-invalid", "$.attorneys", "attorneys must be a nonempty list")
        attorneys = []
    for index, attorney in enumerate(attorneys):
        if not _exact(attorney, ATTORNEY_KEYS) or not _stable(attorney.get("attorney_id")) or not _nonempty(attorney.get("professional_name")):
            _add(findings, "snapshot-structure-invalid", f"$.attorneys[{index}]", "attorney is invalid")
    matters = snapshot.get("matters")
    if not isinstance(matters, list) or not matters:
        _add(findings, "snapshot-structure-invalid", "$.matters", "matters must be a nonempty list")
        matters = []
    for index, matter in enumerate(matters):
        if not _exact(matter, MATTER_KEYS) or not _stable(matter.get("matter_id")) or not all(_nonempty(matter.get(key)) for key in ("court", "docket", "posture", "represented_party")) or not _id_list(matter.get("alignment_group_ids"), nonempty=True):
            _add(findings, "snapshot-structure-invalid", f"$.matters[{index}]", "matter is invalid")
    attorney_ids = {item.get("attorney_id") for item in attorneys if isinstance(item, dict)}
    matter_ids = {item.get("matter_id") for item in matters if isinstance(item, dict)}
    sources = snapshot.get("sources")
    if not isinstance(sources, list) or not sources:
        _add(findings, "snapshot-structure-invalid", "$.sources", "sources must be a nonempty list")
        sources = []
    for index, item in enumerate(sources):
        path = f"$.sources[{index}]"
        if not _exact(item, SOURCE_KEYS) or not _stable(item.get("source_id")) or not _one_of(item.get("source_role"), SOURCE_ROLES) or not _date(item.get("retrieved_on")) or not _date(item.get("source_date")) or not _id_list(item.get("actor_ids")) or not (item.get("matter_id") is None or _stable(item.get("matter_id"))) or not _nonempty(item.get("content")) or not _sha(item.get("sha256")):
            _add(findings, "snapshot-structure-invalid", path, "source is invalid")
            continue
        if item["matter_id"] is not None and item["matter_id"] not in matter_ids:
            _add(findings, "snapshot-source-link-invalid", f"{path}.matter_id", "source matter is unknown")
        if item["retrieved_on"] > snapshot.get("checked_through", ""):
            _add(findings, "snapshot-source-after-check-date", f"{path}.retrieved_on", "source retrieval is after checked-through date")
        if item["sha256"] != _text_sha256(item["content"]):
            _add(findings, "snapshot-source-fingerprint-mismatch", f"{path}.sha256", "source fingerprint does not match content")
        if item["source_role"] in {"bar-directory", "firm-biography", "attorney-publication"} and any(actor not in attorney_ids for actor in item["actor_ids"]):
            _add(findings, "snapshot-source-link-invalid", f"{path}.actor_ids", "professional source actor is unknown")
    gaps = snapshot.get("gaps")
    if not isinstance(gaps, list):
        _add(findings, "snapshot-structure-invalid", "$.gaps", "gaps must be a list")
        gaps = []
    query_ids = {item.get("query_id") for item in queries if isinstance(item, dict)}
    for index, gap in enumerate(gaps):
        if not _exact(gap, SNAPSHOT_GAP_KEYS) or not _stable(gap.get("gap_id")) or not _id_list(gap.get("query_ids"), nonempty=True) or not _id_list(gap.get("matter_ids")) or not _one_of(gap.get("reason"), SNAPSHOT_GAP_REASONS) or not _nonempty(gap.get("description")):
            _add(findings, "snapshot-structure-invalid", f"$.gaps[{index}]", "gap is invalid")
            continue
        if not set(gap["query_ids"]).issubset(query_ids) or not set(gap["matter_ids"]).issubset(matter_ids):
            _add(findings, "snapshot-gap-link-invalid", f"$.gaps[{index}]", "gap references unknown query or matter")
    all_records = [(attorneys, "attorney_id"), (matters, "matter_id"), (sources, "source_id"), (queries, "query_id"), (gaps, "gap_id")]
    if any(_duplicate_ids(records, key) for records, key in all_records):
        _add(findings, "snapshot-duplicate-identifier", "$", "snapshot identifiers must be unique within each record type")
    return findings


def _validate_source_ids(source_ids, sources, findings, path, nonempty=True):
    if not _id_list(source_ids, nonempty=nonempty):
        _add(findings, "overlay-structure-invalid", path, "source IDs are invalid")
        return set()
    values = set(source_ids)
    if not values.issubset(sources):
        _add(findings, "overlay-unknown-source", path, "record references an unknown source")
    return values


def _validate_location(location, sources, findings, path):
    if not _exact(location, LOCATION_KEYS) or not _stable(location.get("source_id")) or not all(_nonempty(location.get(key)) for key in ("page", "heading", "quote")):
        _add(findings, "source-location-invalid", path, "source location is invalid")
        return None
    source = sources.get(location["source_id"])
    if source is None:
        _add(findings, "overlay-unknown-source", f"{path}.source_id", "location source is unknown")
        return None
    if location["quote"] not in source["content"]:
        _add(findings, "source-quote-mismatch", f"{path}.quote", "quotation does not appear in the source")
    return source


def _validate_identity(records, attorneys, matters, sources, findings):
    identities = {}
    for index, record in enumerate(records if isinstance(records, list) else []):
        path = f"$.identity_records[{index}]"
        if not _exact(record, IDENTITY_KEYS) or not _stable(record.get("identity_id")) or not _stable(record.get("attorney_id")) or not _nonempty(record.get("professional_name")) or record.get("bar_status") not in ("active", "inactive", "unverified") or not _date(record.get("bar_status_checked_on")) or not isinstance(record.get("firm_affiliations"), list) or not isinstance(record.get("appearances"), list):
            _add(findings, "identity-structure-invalid", path, "identity record is invalid")
            continue
        if record["attorney_id"] not in attorneys or attorneys[record["attorney_id"]]["professional_name"] != record["professional_name"]:
            _add(findings, "identity-attorney-link-invalid", path, "identity does not match the snapshot attorney")
        record_source_ids = _validate_source_ids(record.get("source_ids"), sources, findings, f"{path}.source_ids")
        nested_source_ids = set()
        for firm_index, firm in enumerate(record["firm_affiliations"]):
            if not _exact(firm, FIRM_KEYS) or not _nonempty(firm.get("firm_name")) or not _date(firm.get("start_date")) or not (firm.get("end_date") is None or _date(firm.get("end_date"))) or not _id_list(firm.get("source_ids"), nonempty=True):
                _add(findings, "identity-structure-invalid", f"{path}.firm_affiliations[{firm_index}]", "firm affiliation is invalid")
                continue
            firm_sources = set(firm["source_ids"])
            nested_source_ids.update(firm_sources)
            if not firm_sources.issubset(sources) or any(record["attorney_id"] not in sources[source_id]["actor_ids"] or firm["firm_name"] not in sources[source_id]["content"] for source_id in firm_sources if source_id in sources):
                _add(findings, "identity-source-link-invalid", f"{path}.firm_affiliations[{firm_index}]", "firm affiliation is not supported by its sources")
        for appearance_index, appearance in enumerate(record["appearances"]):
            if not _exact(appearance, APPEARANCE_KEYS) or not _stable(appearance.get("matter_id")) or appearance.get("matter_id") not in matters or not _nonempty(appearance.get("represented_party")) or not _date(appearance.get("start_date")) or not (appearance.get("end_date") is None or _date(appearance.get("end_date"))) or not _string_list(appearance.get("roles"), nonempty=True) or not set(appearance.get("roles", [])).issubset(ATTRIBUTION_ROLES) or not _id_list(appearance.get("source_ids"), nonempty=True):
                _add(findings, "identity-structure-invalid", f"{path}.appearances[{appearance_index}]", "appearance is invalid")
                continue
            appearance_sources = set(appearance["source_ids"])
            nested_source_ids.update(appearance_sources)
            if not appearance_sources.issubset(sources) or any(record["attorney_id"] not in sources[source_id]["actor_ids"] or sources[source_id]["matter_id"] != appearance["matter_id"] for source_id in appearance_sources if source_id in sources):
                _add(findings, "identity-source-link-invalid", f"{path}.appearances[{appearance_index}]", "appearance is not supported by its sources")
        if nested_source_ids != record_source_ids:
            _add(findings, "identity-source-link-invalid", f"{path}.source_ids", "identity source IDs must equal the nested source union")
        identities[record["identity_id"]] = record
    if not isinstance(records, list):
        _add(findings, "overlay-structure-invalid", "$.identity_records", "identity records must be a list")
    return identities


def _validate_teams(records, attorneys, matters, sources, findings):
    teams = {}
    for index, record in enumerate(records if isinstance(records, list) else []):
        path = f"$.team_records[{index}]"
        if not _exact(record, TEAM_KEYS) or not _stable(record.get("team_id")) or not _stable(record.get("matter_id")) or record.get("matter_id") not in matters or not _nonempty(record.get("version")) or not _date(record.get("effective_start")) or not (record.get("effective_end") is None or _date(record.get("effective_end"))) or not _id_list(record.get("member_attorney_ids"), nonempty=True) or not _nonempty(record.get("represented_party")) or not _id_list(record.get("alignment_group_ids"), nonempty=True):
            _add(findings, "team-structure-invalid", path, "team record is invalid")
            continue
        if not set(record["member_attorney_ids"]).issubset(attorneys):
            _add(findings, "team-attorney-link-invalid", f"{path}.member_attorney_ids", "team references an unknown attorney")
        matter = matters[record["matter_id"]]
        if record["represented_party"] != matter["represented_party"] or not set(record["alignment_group_ids"]).issubset(set(matter["alignment_group_ids"])):
            _add(findings, "team-matter-link-invalid", path, "team party or group does not match its matter")
        team_source_ids = _validate_source_ids(record.get("source_ids"), sources, findings, f"{path}.source_ids")
        if any(sources[source_id]["matter_id"] != record["matter_id"] or not set(sources[source_id]["actor_ids"]).intersection(record["member_attorney_ids"]) or sources[source_id]["source_date"] < record["effective_start"] or (record["effective_end"] is not None and sources[source_id]["source_date"] > record["effective_end"]) for source_id in team_source_ids if source_id in sources):
            _add(findings, "team-source-link-invalid", f"{path}.source_ids", "team sources must match the matter and a team member")
        teams[record["team_id"]] = record
    if not isinstance(records, list):
        _add(findings, "overlay-structure-invalid", "$.team_records", "team records must be a list")
    return teams


def _attribution_supported(record, source):
    attorney_id = record.get("attorney_id")
    role = record.get("attribution_role")
    if role == "counsel-team":
        return attorney_id is None
    if attorney_id is None or role not in DIRECT_ATTRIBUTION_ROLES or attorney_id not in source.get("actor_ids", []):
        return False
    content = source.get("content", "").casefold()
    if role == "signer":
        return "signed by" in content or " signed " in content
    if role == "named-author":
        return "author" in content
    return "oral advocate" in content or "argued by" in content


def _validate_arguments(records, attorneys, matters, teams, sources, findings):
    arguments = {}
    for index, record in enumerate(records if isinstance(records, list) else []):
        path = f"$.historical_arguments[{index}]"
        valid = _exact(record, ARGUMENT_KEYS) and _stable(record.get("argument_id")) and _stable(record.get("matter_id")) and record.get("matter_id") in matters and _stable(record.get("team_id")) and record.get("team_id") in teams and (record.get("attorney_id") is None or (_stable(record.get("attorney_id")) and record.get("attorney_id") in attorneys)) and _one_of(record.get("attribution_role"), ATTRIBUTION_ROLES) and _date(record.get("date")) and all(_nonempty(record.get(key)) for key in ("posture", "represented_party", "claim_id", "challenged_act_id", "element_or_defense", "requested_relief", "status")) and (record.get("qualified_immunity_prong") is None or _nonempty(record.get("qualified_immunity_prong"))) and _id_list(record.get("alignment_group_ids"), nonempty=True)
        if not valid:
            _add(findings, "argument-structure-invalid", path, "historical argument is invalid")
            continue
        source_ids = _validate_source_ids(record.get("source_ids"), sources, findings, f"{path}.source_ids")
        location_source = _validate_location(record.get("source_location"), sources, findings, f"{path}.source_location")
        team = teams[record["team_id"]]
        matter = matters[record["matter_id"]]
        if team["matter_id"] != record["matter_id"] or record["represented_party"] != matter["represented_party"] or record["posture"] != matter["posture"] or not set(record["alignment_group_ids"]).issubset(set(matter["alignment_group_ids"])):
            _add(findings, "argument-matter-link-invalid", path, "argument does not match its team and matter")
        if location_source is not None:
            if location_source["source_id"] not in source_ids:
                _add(findings, "record-source-link-invalid", path, "location source must be listed by the argument")
            if location_source["matter_id"] != record["matter_id"] or location_source["source_date"] != record["date"]:
                _add(findings, "argument-source-link-invalid", path, "argument date or matter does not match its source")
            if location_source["source_role"] not in BEHAVIOR_SOURCE_ROLES:
                _add(findings, "behavior-source-role-invalid", path, "source role cannot establish litigation behavior")
            if not _attribution_supported(record, location_source):
                _add(findings, "individual-attribution-unsupported", path, "individual attribution is not directly supported")
        arguments[record["argument_id"]] = record
    if not isinstance(records, list):
        _add(findings, "overlay-structure-invalid", "$.historical_arguments", "historical arguments must be a list")
    return arguments


def _validate_treatments(records, arguments, sources, findings):
    treatments = {}
    for index, record in enumerate(records if isinstance(records, list) else []):
        path = f"$.judicial_treatments[{index}]"
        if not _exact(record, TREATMENT_KEYS) or not _stable(record.get("treatment_id")) or not _stable(record.get("argument_id")) or not _nonempty(record.get("court_actor")) or not _date(record.get("date")) or not _one_of(record.get("treatment"), TREATMENTS):
            _add(findings, "treatment-structure-invalid", path, "judicial treatment is invalid")
            continue
        source_ids = _validate_source_ids(record.get("source_ids"), sources, findings, f"{path}.source_ids")
        source = _validate_location(record.get("source_location"), sources, findings, f"{path}.source_location")
        if record["argument_id"] not in arguments:
            _add(findings, "treatment-argument-link-invalid", f"{path}.argument_id", "treatment argument is unknown")
        if source is not None and (source["source_id"] not in source_ids or source["source_role"] != "official-court-record" or source["source_date"] != record["date"]):
            _add(findings, "treatment-source-link-invalid", path, "treatment must match an official court source")
        treatments[record["treatment_id"]] = record
    if not isinstance(records, list):
        _add(findings, "overlay-structure-invalid", "$.judicial_treatments", "judicial treatments must be a list")
    return treatments


def _validate_attack_links(records, teams, sources, findings):
    links = {}
    for index, record in enumerate(records if isinstance(records, list) else []):
        path = f"$.current_attack_links[{index}]"
        if not _exact(record, ATTACK_LINK_KEYS) or not all(_stable(record.get(key)) for key in ("link_id", "attack_id", "team_id", "alignment_group_id", "claim_id")) or record.get("team_id") not in teams or not _id_list(record.get("defendant_ids"), nonempty=True) or not _id_list(record.get("challenged_act_ids"), nonempty=True):
            _add(findings, "current-attack-structure-invalid", path, "current attack link is invalid")
            continue
        link_source_ids = _validate_source_ids(record.get("source_ids"), sources, findings, f"{path}.source_ids")
        if record["alignment_group_id"] not in teams[record["team_id"]]["alignment_group_ids"]:
            _add(findings, "current-attack-team-link-invalid", path, "current attack group does not match counsel team")
        team = teams[record["team_id"]]
        if not link_source_ids.issubset(set(team["source_ids"])) or any(sources[source_id]["matter_id"] != team["matter_id"] or sources[source_id]["source_role"] not in BEHAVIOR_SOURCE_ROLES for source_id in link_source_ids if source_id in sources):
            _add(findings, "current-attack-source-link-invalid", f"{path}.source_ids", "current attack sources must match the effective team and matter")
        links[record["link_id"]] = record
    if not isinstance(records, list):
        _add(findings, "overlay-structure-invalid", "$.current_attack_links", "current attack links must be a list")
    return links


def _validate_missingness(value, path, findings):
    if not _exact(value, MISSINGNESS_KEYS) or not all(_nonnegative_int(value.get(key)) for key in MISSINGNESS_KEYS):
        _add(findings, "pattern-structure-invalid", path, "missingness is invalid")
        return None
    return value


def _validate_patterns(records, snapshot, arguments, treatments, sources, findings):
    patterns = {}
    protocol = snapshot.get("research_protocol", {})
    for index, record in enumerate(records if isinstance(records, list) else []):
        path = f"$.patterns[{index}]"
        valid = _exact(record, PATTERN_KEYS) and _stable(record.get("pattern_id")) and _one_of(record.get("pattern_type"), PATTERN_TYPES) and _id_list(record.get("comparable_argument_ids"), nonempty=True) and all(_nonempty(record.get(key)) for key in ("scope", "selection_method", "posture", "conclusion", "limits")) and _nonnegative_int(record.get("denominator")) and _nonnegative_int(record.get("coded_record_count")) and _id_list(record.get("supporting_argument_ids"), nonempty=True) and _id_list(record.get("contrary_argument_ids"), nonempty=True) and _id_list(record.get("treatment_ids")) and _one_of(record.get("confidence"), CONFIDENCE) and _date(record.get("checked_through"))
        if not valid:
            _add(findings, "pattern-structure-invalid", path, "pattern is invalid")
            continue
        missingness = _validate_missingness(record.get("missingness"), f"{path}.missingness", findings)
        _validate_source_ids(record.get("source_ids"), sources, findings, f"{path}.source_ids")
        comparable = set(record["comparable_argument_ids"])
        support = set(record["supporting_argument_ids"])
        contrary = set(record["contrary_argument_ids"])
        if not comparable.issubset(arguments) or not support.issubset(comparable) or not contrary.issubset(comparable) or not set(record["treatment_ids"]).issubset(treatments):
            _add(findings, "pattern-evidence-link-invalid", path, "pattern evidence links are invalid")
        elif support.intersection(contrary) or support.union(contrary) != comparable or any(treatments[item]["argument_id"] not in comparable for item in record["treatment_ids"]):
            _add(findings, "pattern-evidence-link-invalid", path, "pattern support, contrary evidence, and treatments must reconcile to the comparable set")
        expected_sources = {
            source_id
            for argument_id in comparable
            if argument_id in arguments
            for source_id in arguments[argument_id]["source_ids"]
            if _stable(source_id)
        }.union(
            source_id
            for treatment_id in record["treatment_ids"]
            if treatment_id in treatments
            for source_id in treatments[treatment_id]["source_ids"]
            if _stable(source_id)
        )
        if _safe_id_set(record.get("source_ids")) != expected_sources:
            _add(findings, "pattern-source-union-invalid", f"{path}.source_ids", "pattern source IDs must equal the linked evidence union")
        if record["denominator"] != len(comparable) or record["coded_record_count"] != len(comparable) or record["denominator"] != protocol.get("candidate_record_count"):
            _add(findings, "pattern-denominator-invalid", path, "pattern denominator must equal the declared complete comparable set")
        if missingness is not None and (missingness["unresolved"] != protocol.get("unresolved_record_count") or missingness["unavailable"] != protocol.get("unavailable_record_count")):
            _add(findings, "pattern-denominator-invalid", f"{path}.missingness", "pattern missingness must match the snapshot")
        if protocol.get("coverage_status") != "complete" or (missingness and any(missingness.values())):
            _add(findings, "pattern-incomplete-corpus", path, "an incomplete corpus cannot support a pattern")
        if any(arguments[item]["posture"] != record["posture"] for item in comparable if item in arguments):
            _add(findings, "pattern-posture-mismatch", path, "comparable arguments must share the declared posture")
        if record["checked_through"] != snapshot.get("checked_through"):
            _add(findings, "pattern-stale", f"{path}.checked_through", "pattern checked-through date is stale")
        if LEGAL_EFFECT_TERMS.search(record["conclusion"]):
            _add(findings, "automatic-legal-effect-prohibited", f"{path}.conclusion", "cross-case comparison cannot create an automatic legal effect")
        patterns[record["pattern_id"]] = record
    if not isinstance(records, list):
        _add(findings, "overlay-structure-invalid", "$.patterns", "patterns must be a list")
    return patterns


def _validate_forecasts(records, snapshot, patterns, arguments, sources, findings):
    forecasts = {}
    protocol = snapshot.get("research_protocol", {})
    for index, record in enumerate(records if isinstance(records, list) else []):
        path = f"$.forecasts[{index}]"
        valid = _exact(record, FORECAST_KEYS) and _stable(record.get("forecast_id")) and _nonempty(record.get("professional_move")) and _id_list(record.get("pattern_ids"), nonempty=True) and _id_list(record.get("comparable_argument_ids"), nonempty=True) and _nonnegative_int(record.get("denominator")) and _nonnegative_int(record.get("coded_record_count")) and _nonempty(record.get("posture")) and _id_list(record.get("supporting_argument_ids"), nonempty=True) and _id_list(record.get("contrary_argument_ids"), nonempty=True) and _one_of(record.get("confidence"), CONFIDENCE) and _date(record.get("checked_through")) and _nonempty(record.get("limits"))
        if not valid:
            _add(findings, "forecast-evidence-incomplete", path, "forecast evidence is incomplete")
            continue
        missingness = _validate_missingness(record.get("missingness"), f"{path}.missingness", findings)
        _validate_source_ids(record.get("source_ids"), sources, findings, f"{path}.source_ids")
        comparable = set(record["comparable_argument_ids"])
        support = set(record["supporting_argument_ids"])
        contrary = set(record["contrary_argument_ids"])
        if not set(record["pattern_ids"]).issubset(patterns) or not comparable.issubset(arguments) or not support.issubset(comparable) or not contrary.issubset(comparable):
            _add(findings, "forecast-evidence-incomplete", path, "forecast evidence links are invalid")
        elif support.intersection(contrary) or support.union(contrary) != comparable or any(set(patterns[item]["comparable_argument_ids"]) != comparable or patterns[item]["posture"] != record["posture"] for item in record["pattern_ids"]):
            _add(findings, "forecast-evidence-incomplete", path, "forecast evidence must reconcile to its patterns and comparable set")
        expected_sources = {
            source_id
            for argument_id in comparable
            if argument_id in arguments
            for source_id in arguments[argument_id]["source_ids"]
            if _stable(source_id)
        }
        if _safe_id_set(record.get("source_ids")) != expected_sources:
            _add(findings, "forecast-source-union-invalid", f"{path}.source_ids", "forecast source IDs must equal the comparable argument source union")
        if record["denominator"] != len(comparable) or record["coded_record_count"] != len(comparable) or record["denominator"] != protocol.get("candidate_record_count") or protocol.get("coverage_status") != "complete" or (missingness and any(missingness.values())):
            _add(findings, "forecast-evidence-incomplete", path, "forecast requires the complete declared corpus")
        if any(arguments[item]["posture"] != record["posture"] for item in comparable if item in arguments):
            _add(findings, "forecast-posture-mismatch", path, "forecast posture does not match comparable arguments")
        if record["checked_through"] != snapshot.get("checked_through"):
            _add(findings, "forecast-evidence-incomplete", f"{path}.checked_through", "forecast is stale")
        if CERTAINTY_TERMS.search(record["professional_move"]):
            _add(findings, "forecast-certainty-prohibited", f"{path}.professional_move", "forecast cannot state certainty")
        if OUTCOME_TERMS.search(record["professional_move"]):
            _add(findings, "forecast-outcome-prohibited", f"{path}.professional_move", "forecast cannot predict a case outcome or judge")
        forecasts[record["forecast_id"]] = record
    if not isinstance(records, list):
        _add(findings, "overlay-structure-invalid", "$.forecasts", "forecasts must be a list")
    return forecasts


def _validate_overrides(records, findings):
    for index, record in enumerate(records if isinstance(records, list) else []):
        path = f"$.overrides[{index}]"
        if not _exact(record, OVERRIDE_KEYS) or not all(_stable(record.get(key)) for key in ("override_id", "instruction_id")) or record.get("action") not in ("include", "exclude") or not _nonempty(record.get("scope")) or not _id_list(record.get("affected_ids"), nonempty=True) or not _nonempty(record.get("rationale")):
            if isinstance(record, dict) and record.get("action") not in ("include", "exclude"):
                _add(findings, "override-provenance-rewrite-prohibited", f"{path}.action", "override may change scope only")
            else:
                _add(findings, "override-structure-invalid", path, "override is invalid")
    if not isinstance(records, list):
        _add(findings, "overlay-structure-invalid", "$.overrides", "overrides must be a list")


def _validate_gaps(records, snapshot, findings):
    source_gap_ids = {item.get("gap_id") for item in snapshot.get("gaps", []) if isinstance(item, dict)}
    for index, record in enumerate(records if isinstance(records, list) else []):
        path = f"$.gaps[{index}]"
        if not _exact(record, OVERLAY_GAP_KEYS) or not _stable(record.get("gap_id")) or not _id_list(record.get("source_gap_ids"), nonempty=True) or not _nonempty(record.get("scope")) or not _nonempty(record.get("consequence")):
            _add(findings, "overlay-gap-structure-invalid", path, "overlay gap is invalid")
        elif not set(record["source_gap_ids"]).issubset(source_gap_ids):
            _add(findings, "overlay-gap-link-invalid", path, "overlay gap references unknown source gaps")


def _validate_slices(records, identities, teams, arguments, treatments, links, patterns, forecasts, findings):
    for index, record in enumerate(records if isinstance(records, list) else []):
        path = f"$.review_slices[{index}]"
        valid = _exact(record, SLICE_KEYS) and all(_stable(record.get(key)) for key in ("slice_id", "job_id", "alignment_group_id", "target_artifact_id")) and record.get("review_kind") in ("blind-common-attack", "actual-adversary") and all(_id_list(record.get(key)) for key in ("team_ids", "identity_ids", "historical_argument_ids", "treatment_ids", "current_attack_link_ids", "pattern_ids", "forecast_ids", "common_attack_ids"))
        if not valid:
            _add(findings, "review-slice-structure-invalid", path, "review slice is invalid")
            continue
        counsel_lists = [record[key] for key in ("team_ids", "identity_ids", "historical_argument_ids", "treatment_ids", "current_attack_link_ids", "pattern_ids", "forecast_ids")]
        if record["review_kind"] == "blind-common-attack" and any(counsel_lists):
            _add(findings, "blind-review-counsel-leak", path, "blind review cannot receive counsel material")
            continue
        if record["review_kind"] == "actual-adversary":
            if not record["team_ids"] or not set(record["team_ids"]).issubset(teams) or not set(record["identity_ids"]).issubset(identities) or not set(record["historical_argument_ids"]).issubset(arguments) or not set(record["treatment_ids"]).issubset(treatments) or not set(record["current_attack_link_ids"]).issubset(links) or not set(record["pattern_ids"]).issubset(patterns) or not set(record["forecast_ids"]).issubset(forecasts):
                _add(findings, "actual-review-scope-invalid", path, "actual review references unknown counsel material")
                continue
            current_teams = [teams[item] for item in record["team_ids"]]
            if any(record["alignment_group_id"] not in team["alignment_group_ids"] for team in current_teams):
                _add(findings, "actual-review-scope-invalid", path, "actual review team does not match target group")
            current_members = {attorney for team in current_teams for attorney in team["member_attorney_ids"]}
            identity_attorneys = {identities[item]["attorney_id"] for item in record["identity_ids"]}
            if not identity_attorneys.issubset(current_members):
                _add(findings, "actual-review-scope-invalid", path, "actual review identity is not on the current team")
            for argument_id in record["historical_argument_ids"]:
                argument = arguments[argument_id]
                if argument["attorney_id"] is not None and argument["attorney_id"] not in current_members:
                    _add(findings, "actual-review-scope-invalid", path, "historical argument is not attributable to the current team")
            for link_id in record["current_attack_link_ids"]:
                link = links[link_id]
                if link["alignment_group_id"] != record["alignment_group_id"] or link["team_id"] not in record["team_ids"]:
                    _add(findings, "actual-review-scope-invalid", path, "current attack link does not match target group and team")
        if not record["common_attack_ids"]:
            _add(findings, "common-attack-pass-suppressed", f"{path}.common_attack_ids", "common attacks cannot be suppressed")
    if not isinstance(records, list):
        _add(findings, "overlay-structure-invalid", "$.review_slices", "review slices must be a list")


def validate_overlay(overlay, snapshot):
    findings = []
    if validate_snapshot(snapshot):
        return [
            _finding(
                "snapshot-invalid-for-overlay",
                "$.source_snapshot",
                "overlay semantics require a valid source snapshot",
            )
        ]
    if not _exact(overlay, OVERLAY_KEYS):
        _add(findings, "overlay-structure-invalid", "$", "overlay must contain the exact required fields")
        return findings
    if overlay.get("schema_version") != "1.0" or not _stable(overlay.get("overlay_id")) or not _nonempty(overlay.get("version")) or not _datetime(overlay.get("generated_at")):
        _add(findings, "overlay-structure-invalid", "$", "overlay root values are invalid")
    expected_reference = {
        "snapshot_id": snapshot.get("snapshot_id"),
        "version": snapshot.get("version"),
        "sha256": _canonical_sha256(snapshot),
        "checked_through": snapshot.get("checked_through"),
    }
    if not _exact(overlay.get("source_snapshot"), SNAPSHOT_REFERENCE_KEYS) or overlay.get("source_snapshot") != expected_reference:
        _add(findings, "overlay-snapshot-fingerprint-mismatch", "$.source_snapshot", "overlay must pin the supplied snapshot")
    sources = _source_map(snapshot)
    attorneys = {item.get("attorney_id"): item for item in snapshot.get("attorneys", []) if isinstance(item, dict)}
    matters = {item.get("matter_id"): item for item in snapshot.get("matters", []) if isinstance(item, dict)}
    identities = _validate_identity(overlay.get("identity_records"), attorneys, matters, sources, findings)
    teams = _validate_teams(overlay.get("team_records"), attorneys, matters, sources, findings)
    arguments = _validate_arguments(overlay.get("historical_arguments"), attorneys, matters, teams, sources, findings)
    treatments = _validate_treatments(overlay.get("judicial_treatments"), arguments, sources, findings)
    links = _validate_attack_links(overlay.get("current_attack_links"), teams, sources, findings)
    patterns = _validate_patterns(overlay.get("patterns"), snapshot, arguments, treatments, sources, findings)
    forecasts = _validate_forecasts(overlay.get("forecasts"), snapshot, patterns, arguments, sources, findings)
    _validate_overrides(overlay.get("overrides"), findings)
    _validate_gaps(overlay.get("gaps"), snapshot, findings)
    _validate_slices(overlay.get("review_slices"), identities, teams, arguments, treatments, links, patterns, forecasts, findings)
    record_groups = [
        (overlay.get("identity_records"), "identity_id"),
        (overlay.get("team_records"), "team_id"),
        (overlay.get("historical_arguments"), "argument_id"),
        (overlay.get("judicial_treatments"), "treatment_id"),
        (overlay.get("current_attack_links"), "link_id"),
        (overlay.get("patterns"), "pattern_id"),
        (overlay.get("forecasts"), "forecast_id"),
        (overlay.get("overrides"), "override_id"),
        (overlay.get("gaps"), "gap_id"),
        (overlay.get("review_slices"), "slice_id"),
    ]
    if any(isinstance(records, list) and _duplicate_ids(records, key) for records, key in record_groups):
        _add(findings, "overlay-duplicate-identifier", "$", "overlay identifiers must be unique within each record type")
    fingerprints = overlay.get("ledger_fingerprints")
    if not isinstance(fingerprints, dict) or set(fingerprints) != LEDGER_NAMES or any(not _sha(value) for value in fingerprints.values()):
        _add(findings, "ledger-fingerprint-mismatch", "$.ledger_fingerprints", "ledger fingerprints are incomplete")
    else:
        for name in LEDGER_NAMES:
            if fingerprints[name] != _canonical_sha256(overlay.get(name)):
                _add(findings, "ledger-fingerprint-mismatch", f"$.ledger_fingerprints.{name}", "ledger fingerprint does not match records")
    for value in _all_strings({key: overlay[key] for key in ("identity_records", "patterns", "forecasts") if key in overlay}):
        if PERSONAL_TERMS.search(value):
            _add(findings, "personal-profile-prohibited", "$", "personal or private profiling is prohibited")
            break
    return findings


def validate_filing_pins(pins, overlay, snapshot):
    findings = []
    if not isinstance(pins, list) or not pins:
        return [_finding("counsel-pin-structure-invalid", "$", "counsel pins must be a nonempty list")]
    required_kinds = {"counsel-identity", "counsel-team"}
    seen = set()
    for index, pin in enumerate(pins):
        path = f"$[{index}]"
        if not _exact(pin, PIN_KEYS) or pin.get("kind") not in required_kinds or not _stable(pin.get("overlay_id")) or not _nonempty(pin.get("version")) or not _sha(pin.get("sha256")) or not _date(pin.get("checked_through")) or not _stable(pin.get("source_snapshot_id")) or not _nonempty(pin.get("source_snapshot_version")) or not _sha(pin.get("source_snapshot_sha256")):
            _add(findings, "counsel-pin-structure-invalid", path, "counsel pin is invalid")
            continue
        seen.add(pin["kind"])
        if pin["validator_result"] != "passed":
            _add(findings, "counsel-pin-validator-failed", f"{path}.validator_result", "only a passing counsel overlay may affect drafting")
        if pin["overlay_id"] != overlay.get("overlay_id") or pin["version"] != overlay.get("version") or pin["sha256"] != _canonical_sha256(overlay):
            _add(findings, "counsel-pin-fingerprint-mismatch", path, "counsel pin does not match the supplied overlay")
        if pin["checked_through"] != snapshot.get("checked_through") or pin["source_snapshot_id"] != snapshot.get("snapshot_id") or pin["source_snapshot_version"] != snapshot.get("version") or pin["source_snapshot_sha256"] != _canonical_sha256(snapshot):
            _add(findings, "counsel-pin-stale", path, "counsel pin is stale for the supplied snapshot")
    if seen != required_kinds:
        _add(findings, "counsel-pin-structure-invalid", "$", "identity and team pins are both required")
    return findings


def validate_filing_manifest(manifest, overlay, snapshot):
    if not _exact(manifest, MANIFEST_KEYS) or manifest.get("schema_version") != "1.0" or not _stable(manifest.get("filing_version_id")) or not _stable(manifest.get("artifact_id")) or not _sha(manifest.get("artifact_sha256")) or not _exact(manifest.get("source_snapshot"), SNAPSHOT_REFERENCE_KEYS) or not isinstance(manifest.get("overlays"), list):
        return [
            _finding(
                "counsel-manifest-structure-invalid",
                "$",
                "filing manifest must contain the exact required structure",
            )
        ]
    counsel_pins = [
        pin
        for pin in manifest["overlays"]
        if isinstance(pin, dict)
        and pin.get("kind") in ("counsel-identity", "counsel-team")
    ]
    return validate_filing_pins(counsel_pins, overlay, snapshot)


def _input_root(value, role):
    try:
        path = Path(value)
        if not path.is_absolute():
            raise ValueError
        resolved = path.resolve(strict=True)
        if not resolved.is_dir():
            raise ValueError
        return resolved, None
    except (OSError, RuntimeError, TypeError, ValueError):
        return None, _finding(
            "input-path-invalid", role, f"{role} root must be an absolute existing directory"
        )


def _relative_target(value):
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or "\x00" in value
        or (len(value) >= 3 and value[0].isalpha() and value[1:3] == ":/")
    ):
        return None
    try:
        relative = PurePosixPath(value)
    except (TypeError, ValueError):
        return None
    if (
        relative.is_absolute()
        or str(relative) != value
        or any(part in {"", ".", ".."} for part in value.split("/"))
    ):
        return None
    return Path(*relative.parts)


def _load_target(root_value, target, role, max_input_bytes):
    root, root_error = _input_root(root_value, role)
    relative = _relative_target(target)
    if root_error or relative is None or type(max_input_bytes) is not int or max_input_bytes < 1:
        return None, root_error or _finding(
            "input-path-invalid", str(target), f"{role} target must be a canonical relative path"
        )
    max_input_bytes = min(max_input_bytes, MAX_INPUT_BYTES)
    try:
        resolved = (root / relative).resolve(strict=True)
    except FileNotFoundError:
        return None, _finding(
            "input-file-unavailable", target, f"{role} target is unavailable"
        )
    except (OSError, RuntimeError, TypeError, ValueError):
        return None, _finding(
            "input-path-invalid", target, f"{role} target is unavailable or outside its declared root"
        )
    try:
        resolved.relative_to(root)
        if not resolved.is_file():
            raise ValueError
        with resolved.open("rb") as source:
            payload = source.read(max_input_bytes + 1)
    except (OSError, RuntimeError, TypeError, ValueError):
        return None, _finding(
            "input-path-invalid", target, f"{role} target is unavailable or outside its declared root"
        )
    if len(payload) > max_input_bytes:
        return None, _finding(
            "input-file-too-large", target, f"{role} target exceeds the input byte limit"
        )
    try:
        return json.loads(payload.decode("utf-8")), None
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as error:
        return None, _finding(
            "input-file-malformed-json", target, f"input file is not valid UTF-8 JSON: {error}"
        )


def validate_folder_overlay(
    *,
    research_snapshot_root,
    research_snapshot_target,
    overlay,
    case_record_root=None,
    filing_manifest_target=None,
    max_input_bytes=MAX_INPUT_BYTES,
):
    snapshot, snapshot_error = _load_target(
        research_snapshot_root,
        research_snapshot_target,
        "research-snapshot",
        max_input_bytes,
    )
    findings = [snapshot_error] if snapshot_error else []
    manifest = None
    if (case_record_root is None) != (filing_manifest_target is None):
        findings.append(
            _finding(
                "input-path-invalid",
                "case-record",
                "case-record root and filing manifest target must be supplied together",
            )
        )
    elif case_record_root is not None:
        manifest, manifest_error = _load_target(
            case_record_root,
            filing_manifest_target,
            "case-record",
            max_input_bytes,
        )
        if manifest_error:
            findings.append(manifest_error)
    if not findings:
        findings.extend(validate_snapshot(snapshot))
        findings.extend(validate_overlay(overlay, snapshot))
        if manifest is not None:
            findings.extend(validate_filing_manifest(manifest, overlay, snapshot))
    return {"findings": findings, "passed": not findings}


def _parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--research-snapshot-root", required=True)
    parser.add_argument("--research-snapshot-target", required=True)
    parser.add_argument("--case-record-root")
    parser.add_argument("--filing-manifest-target")
    return parser


def main(argv=None):
    arguments = _parser().parse_args(argv)
    stream = getattr(sys.stdin, "buffer", sys.stdin)
    payload = stream.read(MAX_INPUT_BYTES + 1)
    if isinstance(payload, str):
        payload = payload.encode("utf-8")
    if len(payload) > MAX_INPUT_BYTES:
        result = {
            "findings": [
                _finding(
                    "input-file-too-large", "<stdin>", "overlay input exceeds the input byte limit"
                )
            ],
            "passed": False,
        }
    else:
        try:
            overlay = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as error:
            result = {
                "findings": [
                    _finding(
                        "input-file-malformed-json",
                        "<stdin>",
                        f"overlay input is not valid UTF-8 JSON: {error}",
                    )
                ],
                "passed": False,
            }
        else:
            result = validate_folder_overlay(
                research_snapshot_root=arguments.research_snapshot_root,
                research_snapshot_target=arguments.research_snapshot_target,
                overlay=overlay,
                case_record_root=arguments.case_record_root,
                filing_manifest_target=arguments.filing_manifest_target,
            )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
