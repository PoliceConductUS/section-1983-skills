import argparse
import hashlib
import json
import re
import uuid
from datetime import date, datetime
from pathlib import Path


STABLE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SNAPSHOT_KEYS = {
    "schema_version",
    "snapshot_id",
    "version",
    "checked_through",
    "actors",
    "sources",
}
ACTOR_KEYS = {"actor_id", "actor_type", "display_label"}
SOURCE_KEYS = {
    "source_id",
    "docket_entry",
    "filed_date",
    "document_family",
    "filed_by_actor_ids",
    "content",
    "sha256",
}
ACTOR_TYPES = {
    "plaintiff",
    "individual-defendant",
    "municipality-defendant",
    "magistrate-judge",
    "district-judge",
    "appellate-court",
    "other",
}
OVERLAY_REQUIRED_KEYS = {
    "schema_version",
    "overlay_id",
    "version",
    "generated_at",
    "source_snapshot",
    "defendants",
    "generated_groups",
    "overrides",
    "effective_groups",
    "ledgers",
    "ledger_fingerprints",
    "issue_matrix",
    "review_plan",
}
OVERLAY_OPTIONAL_KEYS = {"previous_version_id", "invalidation_events"}
SNAPSHOT_REFERENCE_KEYS = {"snapshot_id", "version", "sha256", "checked_through"}
DEFENDANT_KEYS = {
    "defendant_id",
    "defendant_type",
    "display_label",
    "source_ids",
    "dimensions",
}
DIMENSION_KEYS = {
    "issue_id",
    "claim_id",
    "capacity",
    "challenged_act_id",
    "relevant_time_knowledge_position",
    "qualified_immunity_position",
    "requested_relief",
    "other_material_defense",
}
GROUP_KEYS = {
    "group_id",
    "issue_id",
    "member_defendant_ids",
    "mixed_municipal_alignment_established",
    "source_ids",
    "basis",
    "uncertainty",
}
OVERRIDE_KEYS = {
    "override_id",
    "instruction_id",
    "action",
    "affected_defendant_ids",
    "generated_group_ids",
    "effective_group_ids",
    "rationale",
}
LEDGER_KEYS = {"ledger_id", "version", "records"}
LEDGER_NAMES = {
    "adversary_attacks",
    "plaintiff_responses",
    "judicial_treatments",
}
LOCATION_KEYS = {"source_id", "docket_entry", "page", "heading", "quote"}
ATTACK_KEYS = {
    "attack_id",
    "source_ids",
    "source_location",
    "date",
    "group_id",
    "claim_id",
    "defendant_ids",
    "challenged_act_id",
    "element_or_defense",
    "qualified_immunity_prong",
    "requested_disposition",
    "status",
}
ATTACK_STATUSES = {
    "adversary-asserted",
    "adversary-renewed",
    "adversary-narrowed",
    "adversary-withdrawn",
    "adversary-superseded",
    "adversary-unclear",
}
RESPONSE_KEYS = {
    "response_id",
    "attack_id",
    "source_ids",
    "source_location",
    "date",
    "coverage",
    "coverage_explanation",
}
RESPONSE_STATUSES = {
    "plaintiff-answered",
    "plaintiff-partial",
    "plaintiff-not-answered",
    "plaintiff-superseded",
    "plaintiff-unclear",
}
TREATMENT_KEYS = {
    "treatment_id",
    "attack_id",
    "response_ids",
    "judicial_actor_id",
    "judicial_actor_role",
    "source_ids",
    "source_location",
    "date",
    "treatment",
    "reasoning_type",
    "related_treatment_ids",
    "status",
}
TREATMENTS = {
    "magistrate-judge": {
        "magistrate-judge-recommended-grant",
        "magistrate-judge-recommended-deny",
        "magistrate-judge-recommended-partial",
        "magistrate-judge-recommended-unclear",
    },
    "district-judge": {
        "district-judge-adopted",
        "district-judge-rejected",
        "district-judge-modified",
        "district-judge-independently-granted",
        "district-judge-independently-denied",
        "district-judge-independently-partial",
        "district-judge-unclear",
    },
    "appellate-court": {
        "appellate-court-affirmed",
        "appellate-court-reversed",
        "appellate-court-vacated",
        "appellate-court-modified",
        "appellate-court-remanded",
        "appellate-court-unclear",
    },
}
REASONING_TYPES = {
    "recommendation",
    "adoption-without-independent-reasoning",
    "adoption-with-independent-reasoning",
    "independent-reasoning",
    "appellate-disposition",
    "unclear",
}
MATRIX_KEYS = {
    "row_id",
    "attack_id",
    "response_ids",
    "treatment_ids",
    "response_state",
    "judicial_state",
    "current_procedural_status",
    "current_status_source_ids",
    "source_ids",
}
REVIEW_PLAN_KEYS = {"actual_profile_status", "targets", "jobs"}
TARGET_KEYS = {"artifact_id", "source_id", "sha256", "document_family"}
JOB_KEYS = {
    "job_id",
    "run_id",
    "target_artifact_id",
    "target_sha256",
    "group_id",
    "review_kind",
    "attack_ids",
    "source_ids",
    "prior_review_ids",
}
MANIFEST_KEYS = {
    "schema_version",
    "filing_version_id",
    "artifact_id",
    "artifact_sha256",
    "source_snapshot",
    "overlays",
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
RESPONSIVE_FAMILIES = {
    "motion-to-dismiss",
    "summary-judgment-motion",
    "answer",
    "opposition",
    "reply",
}


def _finding(finding_id, path, message):
    return {"id": finding_id, "path": path, "message": message}


def _canonical_sha256(value):
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _text_sha256(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _exact(value, keys):
    return isinstance(value, dict) and set(value) == keys


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


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
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return True


def _id_list(value, nonempty=False):
    return (
        isinstance(value, list)
        and (not nonempty or bool(value))
        and all(_stable(item) for item in value)
        and len(value) == len(set(value))
    )


def _add(findings, finding_id, path, message):
    findings.append(_finding(finding_id, path, message))


def validate_snapshot(snapshot):
    findings = []
    if not _exact(snapshot, SNAPSHOT_KEYS):
        _add(
            findings,
            "snapshot-structure-invalid",
            "$",
            "snapshot must contain the exact required root fields",
        )
        return findings
    if (
        snapshot["schema_version"] != "1.0"
        or not _stable(snapshot["snapshot_id"])
        or not _nonempty(snapshot["version"])
        or not _date(snapshot["checked_through"])
        or not isinstance(snapshot["actors"], list)
        or not snapshot["actors"]
        or not isinstance(snapshot["sources"], list)
        or not snapshot["sources"]
    ):
        _add(
            findings,
            "snapshot-structure-invalid",
            "$",
            "snapshot root values are invalid",
        )
    actor_ids = []
    for index, actor in enumerate(snapshot["actors"] if isinstance(snapshot["actors"], list) else []):
        path = f"$.actors[{index}]"
        if not _exact(actor, ACTOR_KEYS) or not _stable(actor.get("actor_id")):
            _add(findings, "snapshot-structure-invalid", path, "actor is invalid")
            continue
        if actor["actor_type"] not in ACTOR_TYPES or not _nonempty(actor["display_label"]):
            _add(findings, "snapshot-structure-invalid", path, "actor values are invalid")
        actor_ids.append(actor["actor_id"])
    if len(actor_ids) != len(set(actor_ids)):
        _add(
            findings,
            "snapshot-duplicate-identifier",
            "$.actors",
            "actor identifiers must be unique",
        )
    actor_set = set(actor_ids)
    source_ids = []
    for index, source in enumerate(snapshot["sources"] if isinstance(snapshot["sources"], list) else []):
        path = f"$.sources[{index}]"
        if not _exact(source, SOURCE_KEYS):
            _add(findings, "snapshot-structure-invalid", path, "source is invalid")
            continue
        source_id = source.get("source_id")
        if (
            not _stable(source_id)
            or not _nonempty(source.get("docket_entry"))
            or not _date(source.get("filed_date"))
            or not _nonempty(source.get("document_family"))
            or not _id_list(source.get("filed_by_actor_ids"), nonempty=True)
            or not _nonempty(source.get("content"))
            or not _sha(source.get("sha256"))
        ):
            _add(findings, "snapshot-structure-invalid", path, "source values are invalid")
        if not set(source.get("filed_by_actor_ids", [])).issubset(actor_set):
            _add(findings, "snapshot-unknown-actor", path, "source names an unknown filing actor")
        if _nonempty(source.get("content")) and _sha(source.get("sha256")):
            if _text_sha256(source["content"]) != source["sha256"]:
                _add(
                    findings,
                    "snapshot-source-fingerprint-mismatch",
                    f"{path}.sha256",
                    "source content does not match its fingerprint",
                )
        source_ids.append(source_id)
    if len(source_ids) != len(set(source_ids)):
        _add(
            findings,
            "snapshot-duplicate-identifier",
            "$.sources",
            "source identifiers must be unique",
        )
    return findings


def _validate_snapshot_reference(reference, snapshot, findings):
    expected = {
        "snapshot_id": snapshot.get("snapshot_id"),
        "version": snapshot.get("version"),
        "sha256": _canonical_sha256(snapshot),
        "checked_through": snapshot.get("checked_through"),
    }
    if not _exact(reference, SNAPSHOT_REFERENCE_KEYS) or reference != expected:
        _add(
            findings,
            "overlay-snapshot-fingerprint-mismatch",
            "$.source_snapshot",
            "overlay must pin the exact supplied snapshot",
        )


def _validate_source_ids(values, source_ids, findings, path):
    if not _id_list(values, nonempty=True) or not set(values).issubset(source_ids):
        _add(findings, "overlay-unknown-source", path, "record must name approved source identifiers")


def _validate_location(location, source_map, findings, path):
    if not _exact(location, LOCATION_KEYS):
        _add(findings, "source-location-invalid", path, "source location is incomplete")
        return
    if not all(_nonempty(location.get(key)) for key in ("source_id", "docket_entry", "page", "heading", "quote")):
        _add(findings, "source-location-invalid", path, "source location values are invalid")
        return
    source = source_map.get(location["source_id"])
    if source is None:
        _add(findings, "overlay-unknown-source", path, "source location names an unknown source")
        return
    if source["docket_entry"] != location["docket_entry"] or location["quote"] not in source["content"]:
        _add(findings, "source-quote-mismatch", path, "source location or exact quote does not match the snapshot")


def _validate_defendants(overlay, source_ids, findings):
    defendants = overlay.get("defendants")
    if not isinstance(defendants, list) or not defendants:
        _add(findings, "overlay-structure-invalid", "$.defendants", "defendants must be nonempty")
        return {}, {}
    defendant_map = {}
    dimensions = {}
    for index, defendant in enumerate(defendants):
        path = f"$.defendants[{index}]"
        if not _exact(defendant, DEFENDANT_KEYS):
            _add(findings, "defendant-structure-invalid", path, "defendant is invalid")
            continue
        defendant_id = defendant.get("defendant_id")
        if (
            not _stable(defendant_id)
            or defendant.get("defendant_type") not in {"individual", "municipality"}
            or not _nonempty(defendant.get("display_label"))
            or not isinstance(defendant.get("dimensions"), list)
            or not defendant["dimensions"]
        ):
            _add(findings, "defendant-structure-invalid", path, "defendant values are invalid")
            continue
        _validate_source_ids(defendant.get("source_ids"), source_ids, findings, f"{path}.source_ids")
        if defendant_id in defendant_map:
            _add(findings, "overlay-duplicate-identifier", path, "defendant identifier is duplicated")
        defendant_map[defendant_id] = defendant
        for dimension_index, dimension in enumerate(defendant["dimensions"]):
            dimension_path = f"{path}.dimensions[{dimension_index}]"
            if not _exact(dimension, DIMENSION_KEYS) or not all(
                _nonempty(dimension.get(key)) for key in DIMENSION_KEYS
            ):
                _add(findings, "dimension-structure-invalid", dimension_path, "alignment dimension is invalid")
                continue
            key = (defendant_id, dimension["issue_id"])
            if key in dimensions:
                _add(findings, "overlay-duplicate-identifier", dimension_path, "defendant issue dimension is duplicated")
            dimensions[key] = dimension
    return defendant_map, dimensions


def _validate_groups(groups, label, defendant_map, dimensions, source_ids, findings):
    if not isinstance(groups, list) or not groups:
        _add(findings, "group-structure-invalid", f"$.{label}", "groups must be nonempty")
        return {}, {}
    group_map = {}
    assignments = {}
    for index, group in enumerate(groups):
        path = f"$.{label}[{index}]"
        if not _exact(group, GROUP_KEYS):
            _add(findings, "group-structure-invalid", path, "group is invalid")
            continue
        group_id = group.get("group_id")
        issue_id = group.get("issue_id")
        members = group.get("member_defendant_ids")
        if (
            not _stable(group_id)
            or not _stable(issue_id)
            or not _id_list(members, nonempty=True)
            or not isinstance(group.get("mixed_municipal_alignment_established"), bool)
            or not _nonempty(group.get("basis"))
            or not (group.get("uncertainty") is None or _nonempty(group.get("uncertainty")))
        ):
            _add(findings, "group-structure-invalid", path, "group values are invalid")
            continue
        _validate_source_ids(group.get("source_ids"), source_ids, findings, f"{path}.source_ids")
        if group_id in group_map:
            _add(findings, "overlay-duplicate-identifier", path, "group identifier is duplicated")
        group_map[group_id] = group
        member_dimensions = []
        member_types = set()
        for defendant_id in members:
            defendant = defendant_map.get(defendant_id)
            if defendant is None:
                _add(findings, "defendant-group-assignment-invalid", path, "group names an unknown defendant")
                continue
            member_types.add(defendant["defendant_type"])
            dimension = dimensions.get((defendant_id, issue_id))
            if dimension is None:
                _add(findings, "defendant-group-assignment-invalid", path, "group member lacks the issue dimension")
                continue
            member_dimensions.append(dimension)
            assignments[(defendant_id, issue_id)] = assignments.get((defendant_id, issue_id), 0) + 1
        if len({_canonical_sha256(value) for value in member_dimensions}) > 1:
            _add(findings, "alignment-dimensions-diverge", path, "group members have materially different alignment dimensions")
        if member_types == {"individual", "municipality"} and not group["mixed_municipal_alignment_established"]:
            _add(findings, "municipality-alignment-unproved", path, "mixed municipal alignment requires explicit record support")
    return group_map, assignments


def _validate_overrides(overlay, generated_groups, effective_groups, defendant_map, findings):
    overrides = overlay.get("overrides")
    if not isinstance(overrides, list):
        _add(findings, "override-provenance-invalid", "$.overrides", "overrides must be an array")
        return
    generated_ids = set(generated_groups)
    effective_ids = set(effective_groups)
    changed = generated_ids != effective_ids or any(
        generated_groups.get(group_id, {}).get("member_defendant_ids")
        != effective_groups.get(group_id, {}).get("member_defendant_ids")
        for group_id in generated_ids & effective_ids
    )
    if changed and not overrides:
        _add(findings, "override-provenance-invalid", "$.overrides", "effective groups differ without an explicit override")
    covered_generated = set()
    covered_effective = set()
    for index, override in enumerate(overrides):
        path = f"$.overrides[{index}]"
        if not _exact(override, OVERRIDE_KEYS):
            _add(findings, "override-provenance-invalid", path, "override is invalid")
            continue
        if (
            not _stable(override.get("override_id"))
            or not _stable(override.get("instruction_id"))
            or override.get("action") not in {"add", "exclude", "regroup"}
            or not _id_list(override.get("affected_defendant_ids"), nonempty=True)
            or not set(override["affected_defendant_ids"]).issubset(defendant_map)
            or not _id_list(override.get("generated_group_ids"))
            or not _id_list(override.get("effective_group_ids"))
            or not _nonempty(override.get("rationale"))
        ):
            _add(findings, "override-provenance-invalid", path, "override values are invalid")
            continue
        covered_generated.update(override["generated_group_ids"])
        covered_effective.update(override["effective_group_ids"])
    if changed and (
        not (generated_ids - effective_ids).issubset(covered_generated)
        or not (effective_ids - generated_ids).issubset(covered_effective)
    ):
        _add(findings, "override-provenance-invalid", "$.overrides", "override does not explain changed groups")


def _validate_ledgers(overlay, snapshot, effective_groups, defendant_map, findings):
    ledgers = overlay.get("ledgers")
    fingerprints = overlay.get("ledger_fingerprints")
    if not _exact(ledgers, LEDGER_NAMES) or not _exact(fingerprints, LEDGER_NAMES):
        _add(findings, "overlay-structure-invalid", "$.ledgers", "three exact ledgers and fingerprints are required")
        return {}, {}, {}
    for name, ledger in ledgers.items():
        if not _exact(ledger, LEDGER_KEYS) or not _stable(ledger.get("ledger_id")) or not _nonempty(ledger.get("version")) or not isinstance(ledger.get("records"), list):
            _add(findings, "ledger-structure-invalid", f"$.ledgers.{name}", "ledger is invalid")
            continue
        if not _sha(fingerprints.get(name)) or fingerprints[name] != _canonical_sha256(ledger):
            _add(findings, "ledger-fingerprint-mismatch", f"$.ledger_fingerprints.{name}", "ledger fingerprint does not match canonical content")
    source_map = {source["source_id"]: source for source in snapshot.get("sources", []) if isinstance(source, dict) and "source_id" in source}
    source_ids = set(source_map)
    attacks = {}
    attack_records = ledgers.get("adversary_attacks", {}).get("records", [])
    for index, attack in enumerate(attack_records if isinstance(attack_records, list) else []):
        path = f"$.ledgers.adversary_attacks.records[{index}]"
        if not isinstance(attack, dict):
            _add(findings, "attack-structure-invalid", path, "attack must be an object")
            continue
        extra = set(attack) - ATTACK_KEYS
        if any(
            key.startswith(("plaintiff", "judge", "court", "magistrate", "district", "appellate"))
            for key in extra
        ):
            _add(findings, "attack-role-contamination", path, "attack contains another actor's field")
        if set(attack) != ATTACK_KEYS:
            _add(findings, "attack-structure-invalid", path, "attack fields are incomplete or extra")
            continue
        attack_id = attack["attack_id"]
        if not _stable(attack_id) or attack_id in attacks:
            _add(findings, "overlay-duplicate-identifier", path, "attack identifier is invalid or duplicated")
        attacks[attack_id] = attack
        if attack["status"] not in ATTACK_STATUSES:
            _add(findings, "attack-status-invalid", f"{path}.status", "attack status must be adversary-prefixed")
        if not _date(attack["date"]) or not _stable(attack["claim_id"]) or not _stable(attack["challenged_act_id"]) or not _nonempty(attack["element_or_defense"]) or not _nonempty(attack["requested_disposition"]) or attack["qualified_immunity_prong"] not in {"prong-one", "prong-two", None}:
            _add(findings, "attack-structure-invalid", path, "attack values are invalid")
        _validate_source_ids(attack["source_ids"], source_ids, findings, f"{path}.source_ids")
        _validate_location(attack["source_location"], source_map, findings, f"{path}.source_location")
        group = effective_groups.get(attack["group_id"])
        if group is None or not _id_list(attack["defendant_ids"], nonempty=True) or not set(attack["defendant_ids"]).issubset(set(group.get("member_defendant_ids", []))) or not set(attack["defendant_ids"]).issubset(defendant_map):
            _add(findings, "attack-group-link-invalid", path, "attack must link only to defendants in its effective group")
    responses = {}
    response_records = ledgers.get("plaintiff_responses", {}).get("records", [])
    for index, response in enumerate(response_records if isinstance(response_records, list) else []):
        path = f"$.ledgers.plaintiff_responses.records[{index}]"
        if not _exact(response, RESPONSE_KEYS):
            _add(findings, "response-structure-invalid", path, "response is invalid")
            continue
        response_id = response["response_id"]
        if not _stable(response_id) or response_id in responses:
            _add(findings, "overlay-duplicate-identifier", path, "response identifier is invalid or duplicated")
        responses[response_id] = response
        if response["coverage"] not in RESPONSE_STATUSES:
            _add(findings, "response-status-invalid", f"{path}.coverage", "response coverage must be plaintiff-prefixed")
        if response["attack_id"] not in attacks or not _date(response["date"]) or not _nonempty(response["coverage_explanation"]):
            _add(findings, "response-structure-invalid", path, "response linkage or values are invalid")
        _validate_source_ids(response["source_ids"], source_ids, findings, f"{path}.source_ids")
        _validate_location(response["source_location"], source_map, findings, f"{path}.source_location")
    treatments = {}
    treatment_records = ledgers.get("judicial_treatments", {}).get("records", [])
    actor_map = {actor["actor_id"]: actor for actor in snapshot.get("actors", []) if isinstance(actor, dict) and "actor_id" in actor}
    for index, treatment in enumerate(treatment_records if isinstance(treatment_records, list) else []):
        path = f"$.ledgers.judicial_treatments.records[{index}]"
        if not _exact(treatment, TREATMENT_KEYS):
            _add(findings, "treatment-structure-invalid", path, "judicial treatment is invalid")
            continue
        treatment_id = treatment["treatment_id"]
        if not _stable(treatment_id) or treatment_id in treatments:
            _add(findings, "overlay-duplicate-identifier", path, "treatment identifier is invalid or duplicated")
        treatments[treatment_id] = treatment
        role = treatment["judicial_actor_role"]
        actor = actor_map.get(treatment["judicial_actor_id"])
        if (
            role not in TREATMENTS
            or treatment["treatment"] not in TREATMENTS.get(role, set())
            or actor is None
            or actor.get("actor_type") != role
            or treatment["reasoning_type"] not in REASONING_TYPES
        ):
            _add(findings, "judicial-stage-conflation", path, "judicial actor, role, treatment, and reasoning stage must agree")
        if treatment["attack_id"] not in attacks or not _id_list(treatment["response_ids"]) or not set(treatment["response_ids"]).issubset(responses) or not _id_list(treatment["related_treatment_ids"]) or not _date(treatment["date"]):
            _add(findings, "treatment-structure-invalid", path, "judicial treatment linkage or values are invalid")
        _validate_source_ids(treatment["source_ids"], source_ids, findings, f"{path}.source_ids")
        _validate_location(treatment["source_location"], source_map, findings, f"{path}.source_location")
    for treatment_id, treatment in treatments.items():
        path = f"$.ledgers.judicial_treatments.records[{treatment_id}]"
        related = [treatments.get(value) for value in treatment["related_treatment_ids"]]
        if any(value is None for value in related):
            _add(findings, "treatment-structure-invalid", path, "related treatment is unknown")
            continue
        role = treatment["judicial_actor_role"]
        if role == "magistrate-judge" and (treatment["reasoning_type"] != "recommendation" or related):
            _add(findings, "judicial-stage-conflation", path, "magistrate recommendation cannot adopt another stage")
        if role == "district-judge" and treatment["treatment"] in {"district-judge-adopted", "district-judge-rejected", "district-judge-modified"}:
            if not related or any(value["judicial_actor_role"] != "magistrate-judge" or value["attack_id"] != treatment["attack_id"] for value in related):
                _add(findings, "judicial-stage-conflation", path, "district treatment must link to the magistrate recommendation")
            if treatment["reasoning_type"] not in {"adoption-without-independent-reasoning", "adoption-with-independent-reasoning"}:
                _add(findings, "judicial-stage-conflation", path, "district adoption reasoning must remain distinct")
        if role == "appellate-court":
            if treatment["reasoning_type"] != "appellate-disposition" or not related or any(value["judicial_actor_role"] != "district-judge" for value in related):
                _add(findings, "judicial-stage-conflation", path, "appellate treatment must link to a district disposition")
    return attacks, responses, treatments


def _validate_matrix(overlay, attacks, responses, treatments, findings):
    matrix = overlay.get("issue_matrix")
    if not isinstance(matrix, list):
        _add(findings, "overlay-structure-invalid", "$.issue_matrix", "issue matrix must be an array")
        return
    seen_attacks = set()
    for index, row in enumerate(matrix):
        path = f"$.issue_matrix[{index}]"
        if not isinstance(row, dict):
            _add(findings, "matrix-role-contamination", path, "matrix row must be an object")
            continue
        if set(row) != MATRIX_KEYS:
            _add(findings, "matrix-role-contamination", path, "matrix may contain only canonical foreign keys and states")
            continue
        attack = attacks.get(row["attack_id"])
        if attack is None or row["attack_id"] in seen_attacks or not _id_list(row["response_ids"]) or not set(row["response_ids"]).issubset(responses) or not _id_list(row["treatment_ids"]) or not set(row["treatment_ids"]).issubset(treatments) or not _id_list(row["current_status_source_ids"], nonempty=True) or not _id_list(row["source_ids"], nonempty=True):
            _add(findings, "matrix-link-invalid", path, "matrix foreign keys are invalid")
            continue
        seen_attacks.add(row["attack_id"])
        expected_sources = set(attack["source_ids"]) | set(row["current_status_source_ids"])
        for response_id in row["response_ids"]:
            expected_sources.update(responses[response_id]["source_ids"])
        for treatment_id in row["treatment_ids"]:
            expected_sources.update(treatments[treatment_id]["source_ids"])
        if set(row["source_ids"]) != expected_sources:
            _add(findings, "matrix-source-union-mismatch", f"{path}.source_ids", "matrix source IDs must equal the linked source union")
        if not row["response_ids"] and row["response_state"] != "plaintiff-response-unavailable":
            _add(findings, "matrix-silence-inferred", f"{path}.response_state", "silence must remain plaintiff response unavailable")
        if not row["treatment_ids"] and row["judicial_state"] != "judicial-treatment-unavailable":
            _add(findings, "matrix-silence-inferred", f"{path}.judicial_state", "silence must remain judicial treatment unavailable")
        if row["response_ids"] and row["response_state"] not in {responses[value]["coverage"] for value in row["response_ids"]}:
            _add(findings, "matrix-link-invalid", f"{path}.response_state", "response state must come from a linked response")
        if row["treatment_ids"] and row["judicial_state"] not in {treatments[value]["treatment"] for value in row["treatment_ids"]}:
            _add(findings, "matrix-link-invalid", f"{path}.judicial_state", "judicial state must come from a linked treatment")
    if set(attacks) != seen_attacks:
        _add(findings, "matrix-link-invalid", "$.issue_matrix", "every attack must have exactly one matrix row")


def _validate_review_plan(overlay, snapshot, effective_groups, attacks, findings):
    plan = overlay.get("review_plan")
    if not _exact(plan, REVIEW_PLAN_KEYS) or plan.get("actual_profile_status") not in {"available", "actual-adversary-unavailable"} or not isinstance(plan.get("targets"), list) or not plan["targets"] or not isinstance(plan.get("jobs"), list) or not plan["jobs"]:
        _add(findings, "review-plan-structure-invalid", "$.review_plan", "review plan is invalid")
        return
    source_map = {source["source_id"]: source for source in snapshot.get("sources", []) if isinstance(source, dict) and "source_id" in source}
    targets = {}
    for index, target in enumerate(plan["targets"]):
        path = f"$.review_plan.targets[{index}]"
        if not _exact(target, TARGET_KEYS) or not _stable(target.get("artifact_id")) or not _stable(target.get("source_id")) or not _sha(target.get("sha256")) or not _nonempty(target.get("document_family")):
            _add(findings, "review-plan-structure-invalid", path, "review target is invalid")
            continue
        source = source_map.get(target["source_id"])
        if source is None or source["sha256"] != target["sha256"]:
            _add(findings, "review-plan-structure-invalid", path, "review target must pin a snapshot source")
        targets[target["artifact_id"]] = target
    run_ids = []
    job_ids = []
    jobs_by_pair = {}
    for index, job in enumerate(plan["jobs"]):
        path = f"$.review_plan.jobs[{index}]"
        if not _exact(job, JOB_KEYS):
            _add(findings, "review-plan-structure-invalid", path, "review job is invalid")
            continue
        try:
            canonical_run = str(uuid.UUID(job["run_id"])) == job["run_id"]
        except (ValueError, AttributeError, TypeError):
            canonical_run = False
        if not _stable(job["job_id"]) or not canonical_run or job["review_kind"] not in {"blind-common-attack", "actual-adversary"} or not _id_list(job["attack_ids"]) or not _id_list(job["source_ids"], nonempty=True) or not _id_list(job["prior_review_ids"]):
            _add(findings, "review-plan-structure-invalid", path, "review job values are invalid")
            continue
        target = targets.get(job["target_artifact_id"])
        if target is None or job["target_sha256"] != target["sha256"] or job["group_id"] not in effective_groups:
            _add(findings, "review-plan-structure-invalid", path, "review job target or group is invalid")
            continue
        run_ids.append(job["run_id"])
        job_ids.append(job["job_id"])
        if job["prior_review_ids"]:
            _add(findings, "review-run-not-fresh", f"{path}.prior_review_ids", "fresh review jobs cannot consume prior reviews")
        pair = (job["target_artifact_id"], job["group_id"])
        jobs_by_pair.setdefault(pair, []).append(job)
        target_source_id = target["source_id"]
        if job["review_kind"] == "blind-common-attack":
            if job["attack_ids"] or set(job["source_ids"]) != {target_source_id}:
                _add(findings, "blind-review-overlay-leak", path, "blind review contains adversary overlay material")
        else:
            expected_attacks = {attack_id for attack_id, attack in attacks.items() if attack["group_id"] == job["group_id"]}
            expected_sources = {target_source_id}
            for attack_id in expected_attacks:
                expected_sources.update(attacks[attack_id]["source_ids"])
            if set(job["attack_ids"]) != expected_attacks or set(job["source_ids"]) != expected_sources:
                _add(findings, "actual-review-scope-leak", path, "actual review slice is not exact for its group")
    if len(run_ids) != len(set(run_ids)) or len(job_ids) != len(set(job_ids)):
        _add(findings, "review-run-not-fresh", "$.review_plan.jobs", "job and run identifiers must be unique")
    expected_pairs = {(target_id, group_id) for target_id in targets for group_id in effective_groups}
    if set(jobs_by_pair) != expected_pairs:
        _add(findings, "review-plan-cardinality-invalid", "$.review_plan.jobs", "every target and group requires review jobs")
    unavailable = plan["actual_profile_status"] == "actual-adversary-unavailable"
    for pair in expected_pairs:
        pair_jobs = jobs_by_pair.get(pair, [])
        kinds = [job["review_kind"] for job in pair_jobs]
        if unavailable:
            if len(pair_jobs) != 2 or set(kinds) != {"blind-common-attack"}:
                _add(findings, "actual-profile-unavailable-invented", "$.review_plan.jobs", "unavailable actual profile requires two blind jobs only")
        elif len(pair_jobs) != 2 or sorted(kinds) != ["actual-adversary", "blind-common-attack"]:
            _add(findings, "review-plan-cardinality-invalid", "$.review_plan.jobs", "available profile requires one blind and one actual job")
    if unavailable and attacks:
        _add(findings, "actual-profile-unavailable-invented", "$.review_plan.actual_profile_status", "an attack ledger cannot be hidden as unavailable")
    if unavailable and any(source.get("document_family") in RESPONSIVE_FAMILIES for source in snapshot.get("sources", [])):
        _add(findings, "actual-profile-unavailable-invented", "$.review_plan.actual_profile_status", "responsive filing exists in the snapshot")


def validate_overlay(overlay, snapshot):
    findings = []
    if not isinstance(overlay, dict) or not OVERLAY_REQUIRED_KEYS.issubset(overlay) or not set(overlay).issubset(OVERLAY_REQUIRED_KEYS | OVERLAY_OPTIONAL_KEYS):
        _add(findings, "overlay-structure-invalid", "$", "overlay must contain the exact permitted root fields")
        return findings
    if overlay.get("schema_version") != "1.0" or not _stable(overlay.get("overlay_id")) or not _nonempty(overlay.get("version")) or not _datetime(overlay.get("generated_at")):
        _add(findings, "overlay-structure-invalid", "$", "overlay root values are invalid")
    _validate_snapshot_reference(overlay.get("source_snapshot"), snapshot, findings)
    source_ids = {source.get("source_id") for source in snapshot.get("sources", []) if isinstance(source, dict)}
    defendant_map, dimensions = _validate_defendants(overlay, source_ids, findings)
    generated_groups, _ = _validate_groups(overlay.get("generated_groups"), "generated_groups", defendant_map, dimensions, source_ids, findings)
    effective_groups, assignments = _validate_groups(overlay.get("effective_groups"), "effective_groups", defendant_map, dimensions, source_ids, findings)
    for key in dimensions:
        if assignments.get(key) != 1:
            _add(findings, "defendant-group-assignment-invalid", "$.effective_groups", "every defendant issue dimension must belong to exactly one group")
    _validate_overrides(overlay, generated_groups, effective_groups, defendant_map, findings)
    attacks, responses, treatments = _validate_ledgers(overlay, snapshot, effective_groups, defendant_map, findings)
    _validate_matrix(overlay, attacks, responses, treatments, findings)
    _validate_review_plan(overlay, snapshot, effective_groups, attacks, findings)
    return findings


def validate_filing_manifest(manifest, overlay, snapshot):
    findings = []
    if not _exact(manifest, MANIFEST_KEYS):
        _add(findings, "manifest-structure-invalid", "$", "manifest must contain the exact required fields")
        return findings
    if manifest.get("schema_version") != "1.0" or not _stable(manifest.get("filing_version_id")) or not _stable(manifest.get("artifact_id")) or not _sha(manifest.get("artifact_sha256")) or not isinstance(manifest.get("overlays"), list) or not manifest["overlays"]:
        _add(findings, "manifest-structure-invalid", "$", "manifest root values are invalid")
    expected_snapshot = {
        "snapshot_id": snapshot.get("snapshot_id"),
        "version": snapshot.get("version"),
        "sha256": _canonical_sha256(snapshot),
        "checked_through": snapshot.get("checked_through"),
    }
    if not _exact(manifest.get("source_snapshot"), SNAPSHOT_REFERENCE_KEYS) or manifest["source_snapshot"] != expected_snapshot:
        _add(findings, "manifest-overlay-stale", "$.source_snapshot", "manifest must pin the current snapshot")
    pin_ids = []
    for index, pin in enumerate(manifest.get("overlays", []) if isinstance(manifest.get("overlays"), list) else []):
        path = f"$.overlays[{index}]"
        if not _exact(pin, PIN_KEYS) or pin.get("kind") not in {"litigation-alignment", "judge"} or not _stable(pin.get("overlay_id")) or not _nonempty(pin.get("version")) or not _sha(pin.get("sha256")) or not _date(pin.get("checked_through")) or not _stable(pin.get("source_snapshot_id")) or not _nonempty(pin.get("source_snapshot_version")) or not _sha(pin.get("source_snapshot_sha256")):
            _add(findings, "manifest-structure-invalid", path, "overlay pin is invalid")
            continue
        pin_ids.append((pin["kind"], pin["overlay_id"]))
        if pin["validator_result"] != "passed":
            _add(findings, "manifest-validator-failed", f"{path}.validator_result", "only a passing overlay may affect drafting")
        if pin["kind"] == "litigation-alignment":
            if pin["overlay_id"] != overlay.get("overlay_id") or pin["version"] != overlay.get("version") or pin["sha256"] != _canonical_sha256(overlay):
                _add(findings, "manifest-overlay-fingerprint-mismatch", path, "manifest pin does not match the supplied overlay")
            if pin["checked_through"] != snapshot.get("checked_through") or pin["source_snapshot_id"] != snapshot.get("snapshot_id") or pin["source_snapshot_version"] != snapshot.get("version") or pin["source_snapshot_sha256"] != _canonical_sha256(snapshot):
                _add(findings, "manifest-overlay-stale", path, "overlay pin is stale for the current snapshot")
    if len(pin_ids) != len(set(pin_ids)):
        _add(findings, "manifest-structure-invalid", "$.overlays", "overlay pins must be unique")
    return findings


def _load(path):
    try:
        return json.loads(Path(path).read_bytes().decode("utf-8")), None
    except OSError as error:
        return None, _finding("input-file-unavailable", str(path), f"input file unavailable: {error}")
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        return None, _finding("input-file-malformed-json", str(path), f"input file is not valid UTF-8 JSON: {error}")


def _parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot")
    parser.add_argument("overlay")
    parser.add_argument("--filing-manifest")
    return parser


def main(argv=None):
    arguments = _parser().parse_args(argv)
    snapshot, snapshot_error = _load(arguments.snapshot)
    overlay, overlay_error = _load(arguments.overlay)
    findings = [error for error in (snapshot_error, overlay_error) if error]
    manifest = None
    if arguments.filing_manifest:
        manifest, manifest_error = _load(arguments.filing_manifest)
        if manifest_error:
            findings.append(manifest_error)
    if not findings:
        findings.extend(validate_snapshot(snapshot))
        findings.extend(validate_overlay(overlay, snapshot))
        if manifest is not None:
            findings.extend(validate_filing_manifest(manifest, overlay, snapshot))
    result = {"passed": not findings, "findings": findings}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
