#!/usr/bin/env python3
"""Validate the install-local Section 1983 complaint handoff contract v2."""

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path


CONTRACT_VERSION = 2
ASSESSMENT_STATUSES = {
    "completed",
    "partial",
    "not_run_missing",
    "not_run_invalid",
    "not_run_incompatible",
    "not_run_stale",
}
RESOLUTION_STATUSES = {
    "resolved",
    "missing",
    "hash_mismatch",
    "pinpoint_unresolved",
    "text_mismatch",
    "ambiguous_match",
}
COMMON_COUNT_FIELDS = (
    "count_id",
    "claim",
    "constitutional_source",
    "defendant",
    "capacity",
    "challenged_act",
    "event_stage",
    "standard",
    "standard_pincite",
    "decisive_fact_paragraphs",
    "incorporated_paragraphs",
    "relevant_time_knowledge",
    "application",
    "injury",
    "relief",
    "result",
)
INDIVIDUAL_FIELDS = (
    "personal_act_or_causal_role",
    "event_stage",
    "relevant_time",
    "facts_then_known",
    "underlying_violation",
    "application",
    "injury",
    "causation",
)
QI_FIELDS = (
    "event_date",
    "precise_right",
    "jurisdiction",
    "prong_one_result",
    "prong_two_result",
    "binding_pre_event_authority",
    "authority_audit_status",
    "materially_similar_facts",
    "material_differences",
    "fair_warning",
    "rule_of_orderliness_review_status",
    "later_history_review_status",
    "later_authority_treatment",
)
COMMON_MONELL_FIELDS = (
    "path_id",
    "path_type",
    "challenged_policy_custom_decision_or_omission",
    "supporting_facts",
    "complaint_locations",
    "municipal_inference",
    "attribution_route",
    "implementation_or_transmission_mechanism",
    "underlying_constitutional_violation",
    "particular_injury",
    "moving_force_chain",
    "temporal_lanes",
    "information_and_belief_basis",
    "principal_decision",
)
PATH_FIELDS = {
    "formal_policy": (
        "policy_source",
        "operative_status",
        "promulgating_or_adopting_authority",
        "application_to_challenged_conduct",
    ),
    "custom_or_practice": (
        "similar_incidents",
        "similarity_rule",
        "frequency_duration_or_persistence",
        "knowledge_route",
    ),
    "final_policymaker_decision": (
        "decision",
        "decisionmaker",
        "source_of_final_authority",
        "decision_timing",
        "causal_application",
    ),
    "ratification": (
        "subordinate_act_and_basis",
        "policymaker_knowledge",
        "approval_or_adoption",
        "ratification_timing",
        "causable_injury",
    ),
    "failure_to_train": (
        "precise_task_and_deficiency",
        "responsible_authority",
        "notice_basis",
        "deliberate_indifference",
        "training_causal_chain",
    ),
    "failure_to_supervise_or_discipline": (
        "precise_supervisory_or_disciplinary_deficiency",
        "responsible_authority",
        "notice",
        "deliberate_indifference",
        "supervision_causal_chain",
    ),
}
TEMPORAL_LANES = {
    "pre_event_notice",
    "event_implementation",
    "post_event_ratification",
    "recurrence",
    "later_injury",
    "corroboration",
}
AUTHORITY_FIELDS = (
    "status",
    "proposition_uid",
    "authority_uid",
    "verified_unit_path",
    "source_metadata_path",
    "canonical_opinion_path",
    "canonical_opinion_sha256",
    "text_representation_path",
    "text_representation_sha256",
    "pinpoint",
    "exact_matched_text",
    "stable_locator",
    "normalization",
)


def finding(code, location, message):
    return {"code": code, "location": location, "message": message}


def is_present(mapping, key):
    if key not in mapping:
        return False
    value = mapping[key]
    return value is not None and value != "" and value != [] and value != {}


def require_fields(mapping, fields, code, location, findings):
    for field in fields:
        if not is_present(mapping, field):
            findings.append(finding(code, f"{location}.{field}", f"Required field is missing: {field}"))


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_file(base_dir, value):
    if not isinstance(value, str) or not value:
        return None
    candidate = Path(value)
    if not candidate.is_absolute():
        if base_dir is None:
            return None
        candidate = Path(base_dir) / candidate
    resolved = candidate.resolve(strict=False)
    if base_dir is not None:
        boundary = Path(base_dir).resolve()
        try:
            resolved.relative_to(boundary)
        except ValueError:
            return None
    return resolved


def normalize_passage(value, mode):
    if mode == "none":
        return value
    if mode == "whitespace":
        return re.sub(r"\s+", " ", value).strip()
    if mode == "unicode-punctuation-and-whitespace":
        translated = unicodedata.normalize("NFKC", value).translate(
            str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "–": "-", "—": "-"})
        )
        return re.sub(r"\s+", " ", translated).strip()
    if mode == "pdf-line-breaks-and-whitespace":
        joined = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", value)
        return re.sub(r"\s+", " ", joined).strip()
    raise ValueError(f"unsupported normalization: {mode}")


def validate_authority_resolution(resolution, index, base_dir):
    location = f"casegraph_assessment.authority_resolutions[{index}]"
    findings = []
    require_fields(resolution, AUTHORITY_FIELDS, "missing_authority_resolution_field", location, findings)
    status = resolution.get("status")
    if status not in RESOLUTION_STATUSES:
        findings.append(finding("invalid_authority_resolution_status", f"{location}.status", "Unknown authority-resolution status."))
        return findings
    if status != "resolved":
        findings.append(finding(status, location, "Authority connection is not resolved."))
        return findings

    canonical = resolve_file(base_dir, resolution.get("canonical_opinion_path"))
    text_path = resolve_file(base_dir, resolution.get("text_representation_path"))
    for label, path, expected in (
        ("canonical_opinion", canonical, resolution.get("canonical_opinion_sha256")),
        ("text_representation", text_path, resolution.get("text_representation_sha256")),
    ):
        if path is None or not path.is_file():
            findings.append(finding("missing", f"{location}.{label}_path", f"{label} file is missing or outside the assessment boundary."))
        elif not isinstance(expected, str) or file_sha256(path) != expected.lower():
            findings.append(finding("hash_mismatch", f"{location}.{label}_sha256", f"{label} hash does not match the referenced bytes."))
    if findings or text_path is None:
        return findings

    try:
        text = text_path.read_text(encoding="utf-8")
        mode = resolution.get("normalization")
        haystack = normalize_passage(text, mode)
        needle = normalize_passage(resolution.get("exact_matched_text", ""), mode)
    except (UnicodeDecodeError, ValueError) as error:
        return [finding("text_mismatch", f"{location}.normalization", str(error))]
    matches = haystack.count(needle) if needle else 0
    if matches == 0:
        findings.append(finding("text_mismatch", f"{location}.exact_matched_text", "Exact passage does not occur in the provenance-linked text."))
    elif matches > 1:
        findings.append(finding("ambiguous_match", f"{location}.exact_matched_text", "Exact passage occurs more than once; the receipt is ambiguous."))
    return findings


def validate_handoff(data, base_dir=None, mode="drafting"):
    structural = []
    if not isinstance(data, dict):
        data = {}
        structural.append(finding("invalid_handoff", "$", "Handoff must be a JSON object."))
    if data.get("contract_version") != CONTRACT_VERSION:
        structural.append(finding("unsupported_contract_version", "contract_version", "Only contract version 2 is accepted; migrate the handoff before validation."))

    document = data.get("document")
    if not isinstance(document, dict):
        structural.append(finding("missing_document", "document", "Document fingerprint record is required."))
        document = {}
    require_fields(document, ("path", "sha256", "paragraphs"), "missing_document_field", "document", structural)

    counts = data.get("counts")
    if not isinstance(counts, list) or not counts:
        structural.append(finding("missing_counts", "counts", "At least one count unit is required."))
        counts = []
    seen_count_ids = set()
    seen_path_ids = set()
    for index, count in enumerate(counts):
        location = f"counts[{index}]"
        if not isinstance(count, dict):
            structural.append(finding("invalid_count", location, "Count unit must be an object."))
            continue
        require_fields(count, COMMON_COUNT_FIELDS, "missing_count_field", location, structural)
        count_id = count.get("count_id")
        if count_id in seen_count_ids:
            structural.append(finding("duplicate_count_id", f"{location}.count_id", "Count IDs must be unique."))
        seen_count_ids.add(count_id)
        for field in ("decisive_fact_paragraphs", "incorporated_paragraphs"):
            values = count.get(field, [])
            known = set(document.get("paragraphs", []))
            if isinstance(values, list) and any(value not in known for value in values):
                structural.append(finding("unresolved_paragraph_reference", f"{location}.{field}", "Paragraph reference does not resolve in the document record."))

        capacity = count.get("capacity")
        if capacity == "individual":
            individual = count.get("individual_capacity")
            if not isinstance(individual, dict):
                structural.append(finding("missing_individual_capacity_unit", f"{location}.individual_capacity", "Individual-capacity analysis is required."))
            else:
                require_fields(individual, INDIVIDUAL_FIELDS, "missing_individual_capacity_field", f"{location}.individual_capacity", structural)
        qi = count.get("qualified_immunity")
        if not isinstance(qi, dict) or "applies" not in qi:
            structural.append(finding("missing_qualified_immunity_unit", f"{location}.qualified_immunity", "Qualified-immunity applicability must be explicit."))
        elif qi.get("applies") is True:
            require_fields(qi, QI_FIELDS, "missing_qualified_immunity_field", f"{location}.qualified_immunity", structural)

        paths = count.get("monell_paths", [])
        if capacity == "municipal" and (not isinstance(paths, list) or not paths):
            structural.append(finding("missing_monell_path", f"{location}.monell_paths", "A municipal count requires at least one separated Monell path."))
            paths = []
        if not isinstance(paths, list):
            structural.append(finding("invalid_monell_paths", f"{location}.monell_paths", "Monell paths must be an array."))
            paths = []
        for path_index, path in enumerate(paths):
            path_location = f"{location}.monell_paths[{path_index}]"
            if not isinstance(path, dict):
                structural.append(finding("invalid_monell_path", path_location, "Monell path must be an object."))
                continue
            path_type = path.get("path_type")
            if not isinstance(path_type, str) or path_type not in PATH_FIELDS:
                structural.append(finding("invalid_monell_path_type", f"{path_location}.path_type", "Each path must have exactly one recognized path type."))
                required = COMMON_MONELL_FIELDS
            else:
                required = COMMON_MONELL_FIELDS + PATH_FIELDS[path_type]
            require_fields(path, required, "missing_monell_path_field", path_location, structural)
            supporting_facts = path.get("supporting_facts")
            fact_ids = set()
            if not isinstance(supporting_facts, list) or not supporting_facts:
                structural.append(finding("invalid_supporting_facts", f"{path_location}.supporting_facts", "Supporting facts must be typed records with stable fact IDs."))
            else:
                for fact_index, fact in enumerate(supporting_facts):
                    fact_location = f"{path_location}.supporting_facts[{fact_index}]"
                    if not isinstance(fact, dict) or not is_present(fact, "fact_id"):
                        structural.append(finding("invalid_supporting_fact", fact_location, "Each supporting fact requires a stable fact_id."))
                        continue
                    if fact["fact_id"] in fact_ids:
                        structural.append(finding("duplicate_supporting_fact_id", f"{fact_location}.fact_id", "Supporting fact IDs must be unique within a path."))
                    fact_ids.add(fact["fact_id"])
            lanes = path.get("temporal_lanes")
            mapped_fact_ids = set()
            if not isinstance(lanes, list) or not lanes:
                structural.append(finding("invalid_temporal_lanes", f"{path_location}.temporal_lanes", "Temporal lanes must map supporting facts to one or more recognized lanes."))
            else:
                for lane_index, lane in enumerate(lanes):
                    lane_location = f"{path_location}.temporal_lanes[{lane_index}]"
                    if not isinstance(lane, dict) or lane.get("lane") not in TEMPORAL_LANES or not is_present(lane, "supporting_fact_refs"):
                        structural.append(finding("invalid_temporal_lane", lane_location, "Each temporal-lane record requires a recognized lane and supporting fact references."))
                    else:
                        for fact_ref in lane["supporting_fact_refs"]:
                            mapped_fact_ids.add(fact_ref)
                            if fact_ref not in fact_ids:
                                structural.append(finding("unresolved_temporal_fact_reference", f"{lane_location}.supporting_fact_refs", f"Temporal fact reference does not resolve: {fact_ref}"))
            for fact_id in fact_ids - mapped_fact_ids:
                structural.append(finding("unmapped_supporting_fact", f"{path_location}.temporal_lanes", f"Supporting fact is not assigned to a temporal lane: {fact_id}"))
            belief = path.get("information_and_belief_basis")
            if not isinstance(belief, dict) or not isinstance(belief.get("used"), bool):
                structural.append(finding("invalid_information_and_belief_basis", f"{path_location}.information_and_belief_basis", "Information-and-belief basis must explicitly state whether it is used."))
            elif belief["used"]:
                require_fields(belief, ("known_facts", "expected_information", "controller", "inference", "affected_fields"), "missing_information_and_belief_field", f"{path_location}.information_and_belief_basis", structural)
            decision = path.get("principal_decision")
            if not isinstance(decision, dict) or decision.get("status") != "approved":
                structural.append(finding("monell_path_not_approved", f"{path_location}.principal_decision", "A drafted Monell path requires the litigation principal's typed approved decision."))
            else:
                require_fields(decision, ("approver", "scope", "approved_narrowing", "decision_record_path", "decision_record_sha256"), "missing_principal_decision_field", f"{path_location}.principal_decision", structural)
                decision_path = resolve_file(base_dir, decision.get("decision_record_path"))
                if base_dir is None:
                    structural.append(finding("principal_decision_verification_unavailable", f"{path_location}.principal_decision.decision_record_path", "A validation boundary is required to verify the decision record and hash."))
                elif decision_path is None or not decision_path.is_file():
                    structural.append(finding("missing_principal_decision_record", f"{path_location}.principal_decision.decision_record_path", "Decision record is missing or outside the validation boundary."))
                elif base_dir is not None and file_sha256(decision_path) != str(decision.get("decision_record_sha256", "")).lower():
                    structural.append(finding("principal_decision_hash_mismatch", f"{path_location}.principal_decision.decision_record_sha256", "Decision-record hash does not match the referenced bytes."))
            path_id = path.get("path_id")
            if path_id in seen_path_ids:
                structural.append(finding("duplicate_monell_path_id", f"{path_location}.path_id", "Monell path IDs must be unique."))
            seen_path_ids.add(path_id)

    assessment = data.get("casegraph_assessment")
    assessment_findings = []
    if not isinstance(assessment, dict):
        assessment = {"status": "not_run_missing", "claim_unit_ids": []}
        assessment_findings.append(finding("missing_assessment_receipt", "casegraph_assessment", "Assessment receipt is absent."))
    status = assessment.get("status")
    if status not in ASSESSMENT_STATUSES:
        assessment_findings.append(finding("invalid_assessment_status", "casegraph_assessment.status", "Unknown assessment status."))
        status = "not_run_invalid"
    assessed_ids = set(assessment.get("claim_unit_ids", [])) if isinstance(assessment.get("claim_unit_ids"), list) else set()
    expected_ids = {count.get("count_id") for count in counts if isinstance(count, dict)}
    if status in {"completed", "partial"}:
        if assessment.get("document_sha256") != document.get("sha256"):
            assessment_findings.append(finding("assessment_document_fingerprint_mismatch", "casegraph_assessment.document_sha256", "Assessment was not run against the current document fingerprint."))
            status = "not_run_stale"
        if assessed_ids != expected_ids:
            assessment_findings.append(finding("assessment_claim_coverage_mismatch", "casegraph_assessment.claim_unit_ids", "Assessment does not cover every and only current claim unit."))
        resolutions = assessment.get("authority_resolutions", [])
        if not isinstance(resolutions, list):
            assessment_findings.append(finding("invalid_authority_resolutions", "casegraph_assessment.authority_resolutions", "Authority resolutions must be an array."))
        else:
            for index, resolution in enumerate(resolutions):
                if not isinstance(resolution, dict):
                    assessment_findings.append(finding("invalid_authority_resolution", f"casegraph_assessment.authority_resolutions[{index}]", "Authority resolution must be an object."))
                else:
                    assessment_findings.extend(validate_authority_resolution(resolution, index, base_dir))

    structural_result = {"status": "fail" if structural else "pass", "findings": structural}
    assessment_result = {"status": status, "findings": assessment_findings}
    filing_findings = []
    if structural:
        filing_findings.append(finding("structural_validation_failed", "structural_validation", "Structural validation failed."))
    if mode == "filing" and (status != "completed" or assessment_findings):
        filing_findings.append(finding("assessment_required", "casegraph_assessment", "Filing mode requires a current completed assessment with no unresolved receipt findings."))
    filing_gate = {"status": "fail" if filing_findings else "pass", "findings": filing_findings}
    return {
        "contract_version": CONTRACT_VERSION,
        "mode": mode,
        "structural_validation": structural_result,
        "casegraph_assessment": assessment_result,
        "filing_gate": filing_gate,
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("handoff", type=Path)
    parser.add_argument("--base-dir", type=Path)
    parser.add_argument("--mode", choices=("drafting", "filing"), default="drafting")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.handoff.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error)}, indent=2))
        return 2
    result = validate_handoff(data, args.base_dir or args.handoff.parent, args.mode)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["filing_gate"]["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
