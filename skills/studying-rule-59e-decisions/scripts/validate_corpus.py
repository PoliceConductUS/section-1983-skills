import argparse
import json
import sys
from datetime import date
from pathlib import Path, PurePosixPath


MAX_INPUT_BYTES = 1_000_000


TOP_LEVEL_REQUIRED = (
    "schema_version",
    "study",
    "denominator",
    "decision_records",
    "retrieval_gaps",
    "transfer_cards",
)

STUDY_REQUIRED = (
    "study_id",
    "version",
    "research_question",
    "governing_circuit",
    "district",
    "decisionmakers",
    "date_range",
    "included_motion_types",
    "case_categories",
    "excluded_categories",
    "databases_searched",
    "search_queries",
    "search_dates",
    "deduplication_method",
    "known_unavailable_sources",
    "denominator_definition",
)

DATE_RANGE_REQUIRED = ("start", "end")

DENOMINATOR_REQUIRED = (
    "defined_universe",
    "sampling_method",
    "candidate_count",
    "coded_pair_count",
    "research_question_complete_count",
    "unresolved_relevant_missingness",
    "completeness_status",
    "limits",
)

DECISION_REQUIRED = (
    "record_id",
    "motion_id",
    "related_stage_ids",
    "case_name",
    "case_number",
    "court",
    "assigned_judge",
    "reasoning_author",
    "recommendation_author",
    "adopting_judge",
    "decision_type",
    "posture",
    "ground_children",
    "requested_relief",
    "proposed_material",
    "independent_reasoning",
    "disposition",
    "sources",
    "missing_documents",
    "appellate_history",
    "retrieval_status",
    "coding_confidence",
)

POSTURE_REQUIRED = (
    "challenged_disposition",
    "judgment_status",
    "rule_subsection",
    "motion_type",
    "case_category",
    "representation_status",
)

GROUND_REQUIRED = (
    "ground_id",
    "asserted_ground",
    "court_treatment",
    "ground_result",
    "supporting_pinpoint",
)

PROPOSED_MATERIAL_REQUIRED = ("status", "description")
DISPOSITION_REQUIRED = ("code", "stated_reasons", "outcome_changing_reason")
SOURCE_REQUIRED = ("source_id", "source_type", "identity", "checked_date")
MISSING_DOCUMENT_REQUIRED = ("gap_id", "document_type", "description")
APPELLATE_HISTORY_REQUIRED = (
    "appeal_taken",
    "review_standard",
    "result",
    "checked_through",
)

GAP_REQUIRED = (
    "gap_id",
    "record_id",
    "candidate_id",
    "document_type",
    "status",
    "retrieval_attempts",
    "limit",
)

CARD_REQUIRED = (
    "card_id",
    "proposition",
    "universe",
    "numerator",
    "denominator",
    "date_range",
    "source_row_ids",
    "evidence_level",
    "missingness",
    "disconfirming_row_ids",
    "permitted_use",
    "prohibited_inference",
    "checked_through",
    "actual_source_identity",
    "source_checked_date",
    "metric_type",
)

DECISION_TYPES = {
    "recommendation",
    "adoption-only-order",
    "independently-reasoned-final-decision",
    "consent-final-decision",
    "outcome-only-order",
}

INDEPENDENCE_VALUES = {
    "independent",
    "adopts-with-additional-reasoning",
    "adopts-without-additional-reasoning",
    "recommendation-only",
    "docket-outcome-only",
    "unclear",
}

PROPOSED_MATERIAL_VALUES = {
    "complete-attached",
    "complete-tendered-separately",
    "cure-explanation-only",
    "neither",
    "not-applicable",
    "unknown",
}

DISPOSITION_VALUES = {
    "grant-full",
    "grant-partial",
    "correction-without-relief",
    "deny",
    "procedural-disposition",
    "administrative-only",
    "withdrawn",
    "unresolved",
}

STATED_REASON_VALUES = {
    "manifest-error-not-shown",
    "new-evidence-not-shown",
    "intervening-law-not-shown",
    "rehash-or-available-before-judgment",
    "vehicle-or-timing-defect",
    "rule15-factors",
    "futility",
    "delay-bad-faith-or-prejudice",
    "prior-failure-to-cure",
    "record-or-inference-error",
    "correction-does-not-change-result",
    "other-stated-reason",
}

RETRIEVAL_STATUS_VALUES = {"complete-pair", "ruling-complete", "index-only", "lead-only"}
CODING_CONFIDENCE_VALUES = {"high", "medium", "low"}
SAMPLING_METHOD_VALUES = {"attempted-census", "convenience"}
COMPLETENESS_STATUS_VALUES = {"complete", "incomplete"}
RULE_SUBSECTION_VALUES = {"59(a)", "59(e)", "59-unspecified"}
REPRESENTATION_STATUS_VALUES = {"represented", "pro-se", "unknown"}
GAP_STATUS_VALUES = {"unavailable", "unresolved", "not-found", "unresolved-candidate"}
EVIDENCE_LEVEL_VALUES = {"example", "documented-cluster", "tendency"}
METRIC_TYPE_VALUES = {"descriptive", "success-rate"}


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def nonnegative_integer(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def controlled_value(value, allowed_values):
    return isinstance(value, str) and value in allowed_values


def iso_date(value):
    if not nonblank(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return len(value) == 10


def version_string(value):
    if not nonblank(value):
        return False
    parts = value.split(".")
    return len(parts) == 2 and all(part.isdigit() for part in parts)


def add_malformed(findings, path):
    findings.append(f"malformed-input: {path}")


def validate_object(value, path, required, findings):
    if not isinstance(value, dict):
        add_malformed(findings, path)
        return False
    for field in required:
        if field not in value:
            findings.append(f"missing-required-field: {path}.{field}")
    for field in value:
        if field not in required:
            findings.append(f"unexpected-field: {path}.{field}")
    return True


def validate_nonblank_fields(value, path, fields, findings):
    for field in fields:
        if field in value and not nonblank(value[field]):
            add_malformed(findings, f"{path}.{field}")


def validate_string_list(value, path, findings, require_item=False):
    if not isinstance(value, list):
        add_malformed(findings, path)
        return False
    if require_item and not value:
        add_malformed(findings, path)
    for index, item in enumerate(value):
        if not nonblank(item):
            add_malformed(findings, f"{path}[{index}]")
    return True


def validate_study(study, findings):
    if not validate_object(study, "study", STUDY_REQUIRED, findings):
        return
    validate_nonblank_fields(
        study,
        "study",
        (
            "study_id",
            "version",
            "research_question",
            "governing_circuit",
            "district",
            "deduplication_method",
            "denominator_definition",
        ),
        findings,
    )
    for field in (
        "decisionmakers",
        "included_motion_types",
        "case_categories",
        "excluded_categories",
        "databases_searched",
        "search_queries",
        "known_unavailable_sources",
    ):
        if field in study:
            validate_string_list(study[field], f"study.{field}", findings)
    if "search_dates" in study:
        if validate_string_list(study["search_dates"], "study.search_dates", findings):
            for index, value in enumerate(study["search_dates"]):
                if nonblank(value) and not iso_date(value):
                    add_malformed(findings, f"study.search_dates[{index}]")
    date_range = study.get("date_range")
    if validate_object(date_range, "study.date_range", DATE_RANGE_REQUIRED, findings):
        for field in ("start", "end"):
            if field in date_range and not iso_date(date_range[field]):
                add_malformed(findings, f"study.date_range.{field}")


def validate_denominator(denominator, findings):
    if not validate_object(denominator, "denominator", DENOMINATOR_REQUIRED, findings):
        return
    validate_nonblank_fields(denominator, "denominator", ("defined_universe",), findings)
    if not controlled_value(denominator.get("sampling_method"), SAMPLING_METHOD_VALUES):
        findings.append("controlled-value-invalid: denominator.sampling_method")
    if not controlled_value(
        denominator.get("completeness_status"), COMPLETENESS_STATUS_VALUES
    ):
        findings.append("controlled-value-invalid: denominator.completeness_status")
    for field in (
        "candidate_count",
        "coded_pair_count",
        "research_question_complete_count",
        "unresolved_relevant_missingness",
    ):
        if field in denominator and not nonnegative_integer(denominator[field]):
            add_malformed(findings, f"denominator.{field}")
    if "limits" in denominator:
        validate_string_list(denominator["limits"], "denominator.limits", findings)
    counts = [
        denominator.get("candidate_count"),
        denominator.get("coded_pair_count"),
        denominator.get("research_question_complete_count"),
    ]
    if all(nonnegative_integer(value) for value in counts):
        if not counts[0] >= counts[1] >= counts[2]:
            findings.append("denominator-count-inconsistent")
    if denominator.get("completeness_status") == "incomplete" and not denominator.get("limits"):
        findings.append("denominator-limits-required")


def validate_posture(posture, path, findings):
    if not validate_object(posture, path, POSTURE_REQUIRED, findings):
        return
    validate_nonblank_fields(
        posture,
        path,
        ("challenged_disposition", "judgment_status", "motion_type", "case_category"),
        findings,
    )
    if not controlled_value(posture.get("rule_subsection"), RULE_SUBSECTION_VALUES):
        findings.append(f"controlled-value-invalid: {path}.rule_subsection")
    if not controlled_value(
        posture.get("representation_status"), REPRESENTATION_STATUS_VALUES
    ):
        findings.append(f"controlled-value-invalid: {path}.representation_status")


def validate_ground_children(grounds, path, findings):
    if not isinstance(grounds, list):
        add_malformed(findings, path)
        return
    if not grounds:
        add_malformed(findings, path)
    for index, ground in enumerate(grounds):
        ground_path = f"{path}[{index}]"
        if validate_object(ground, ground_path, GROUND_REQUIRED, findings):
            validate_nonblank_fields(ground, ground_path, GROUND_REQUIRED, findings)


def validate_proposed_material(material, path, findings):
    if not validate_object(material, path, PROPOSED_MATERIAL_REQUIRED, findings):
        return
    if not controlled_value(material.get("status"), PROPOSED_MATERIAL_VALUES):
        findings.append(f"controlled-value-invalid: {path}.status")
    if "description" in material and not nonblank(material["description"]):
        add_malformed(findings, f"{path}.description")


def validate_disposition(disposition, path, findings):
    if not validate_object(disposition, path, DISPOSITION_REQUIRED, findings):
        return
    if not controlled_value(disposition.get("code"), DISPOSITION_VALUES):
        findings.append(f"controlled-value-invalid: {path}.code")
    if "stated_reasons" in disposition:
        validate_string_list(disposition["stated_reasons"], f"{path}.stated_reasons", findings)
        if isinstance(disposition["stated_reasons"], list):
            for index, reason in enumerate(disposition["stated_reasons"]):
                if not controlled_value(reason, STATED_REASON_VALUES):
                    findings.append(
                        f"controlled-value-invalid: {path}.stated_reasons[{index}]"
                    )
    if "outcome_changing_reason" in disposition and not nonblank(
        disposition["outcome_changing_reason"]
    ):
        add_malformed(findings, f"{path}.outcome_changing_reason")


def validate_sources(sources, path, findings):
    if not isinstance(sources, list):
        add_malformed(findings, path)
        return
    if not sources:
        add_malformed(findings, path)
    for index, source in enumerate(sources):
        source_path = f"{path}[{index}]"
        if validate_object(source, source_path, SOURCE_REQUIRED, findings):
            validate_nonblank_fields(source, source_path, SOURCE_REQUIRED[:-1], findings)
            if "checked_date" in source and not iso_date(source["checked_date"]):
                add_malformed(findings, f"{source_path}.checked_date")


def validate_missing_documents(documents, path, findings):
    if not isinstance(documents, list):
        add_malformed(findings, path)
        return
    for index, document in enumerate(documents):
        document_path = f"{path}[{index}]"
        if validate_object(document, document_path, MISSING_DOCUMENT_REQUIRED, findings):
            validate_nonblank_fields(
                document, document_path, MISSING_DOCUMENT_REQUIRED, findings
            )


def validate_appellate_history(history, path, findings):
    if not validate_object(history, path, APPELLATE_HISTORY_REQUIRED, findings):
        return
    if "appeal_taken" in history and not isinstance(history["appeal_taken"], bool):
        add_malformed(findings, f"{path}.appeal_taken")
    validate_nonblank_fields(history, path, ("review_standard", "result"), findings)
    if "checked_through" in history and not iso_date(history["checked_through"]):
        add_malformed(findings, f"{path}.checked_through")


def validate_authorship(record, findings):
    decision_type = record.get("decision_type")
    independence = record.get("independent_reasoning")
    assigned = record.get("assigned_judge")
    reasoning = record.get("reasoning_author")
    recommendation = record.get("recommendation_author")
    adopting = record.get("adopting_judge")
    consistent = True
    if decision_type == "recommendation":
        consistent = (
            independence == "recommendation-only"
            and nonblank(recommendation)
            and recommendation != assigned
            and reasoning == recommendation
            and adopting is None
        )
    elif decision_type == "adoption-only-order":
        consistent = (
            independence == "adopts-without-additional-reasoning"
            and nonblank(adopting)
            and nonblank(recommendation)
            and reasoning is None
        )
    elif decision_type == "independently-reasoned-final-decision":
        consistent = independence == "independent" and nonblank(reasoning)
    elif decision_type == "consent-final-decision":
        consistent = (
            independence == "independent"
            and nonblank(reasoning)
            and recommendation is None
            and adopting is None
        )
    elif decision_type == "outcome-only-order":
        consistent = controlled_value(
            independence, {"docket-outcome-only", "unclear"}
        ) and reasoning is None
    if not consistent:
        findings.append("authorship-stage-inconsistent")


def validate_decision_records(records, findings):
    if not isinstance(records, list):
        add_malformed(findings, "decision_records")
        return []
    if not records:
        add_malformed(findings, "decision_records")
    valid_records = []
    for index, record in enumerate(records):
        path = f"decision_records[{index}]"
        if not validate_object(record, path, DECISION_REQUIRED, findings):
            continue
        valid_records.append(record)
        validate_nonblank_fields(
            record,
            path,
            ("record_id", "motion_id", "case_name", "case_number", "court", "assigned_judge"),
            findings,
        )
        for field in ("reasoning_author", "recommendation_author", "adopting_judge"):
            if field in record and record[field] is not None and not nonblank(record[field]):
                add_malformed(findings, f"{path}.{field}")
        if "related_stage_ids" in record:
            validate_string_list(record["related_stage_ids"], f"{path}.related_stage_ids", findings)
        if not controlled_value(record.get("decision_type"), DECISION_TYPES):
            findings.append(f"controlled-value-invalid: {path}.decision_type")
        if not controlled_value(record.get("independent_reasoning"), INDEPENDENCE_VALUES):
            findings.append(f"controlled-value-invalid: {path}.independent_reasoning")
        if not controlled_value(record.get("retrieval_status"), RETRIEVAL_STATUS_VALUES):
            findings.append(f"controlled-value-invalid: {path}.retrieval_status")
        if not controlled_value(record.get("coding_confidence"), CODING_CONFIDENCE_VALUES):
            findings.append(f"controlled-value-invalid: {path}.coding_confidence")
        if "posture" in record:
            validate_posture(record["posture"], f"{path}.posture", findings)
        if "ground_children" in record:
            validate_ground_children(record["ground_children"], f"{path}.ground_children", findings)
        if "requested_relief" in record:
            validate_string_list(
                record["requested_relief"], f"{path}.requested_relief", findings, True
            )
        if "proposed_material" in record:
            validate_proposed_material(record["proposed_material"], f"{path}.proposed_material", findings)
        if "disposition" in record:
            validate_disposition(record["disposition"], f"{path}.disposition", findings)
        if "sources" in record:
            validate_sources(record["sources"], f"{path}.sources", findings)
        if "missing_documents" in record:
            validate_missing_documents(record["missing_documents"], f"{path}.missing_documents", findings)
        if "appellate_history" in record:
            validate_appellate_history(record["appellate_history"], f"{path}.appellate_history", findings)
        validate_authorship(record, findings)
    return valid_records


def validate_retrieval_gaps(gaps, findings):
    if not isinstance(gaps, list):
        add_malformed(findings, "retrieval_gaps")
        return []
    valid_gaps = []
    for index, gap in enumerate(gaps):
        path = f"retrieval_gaps[{index}]"
        if not validate_object(gap, path, GAP_REQUIRED, findings):
            continue
        valid_gaps.append(gap)
        validate_nonblank_fields(
            gap,
            path,
            ("gap_id", "candidate_id", "document_type", "limit"),
            findings,
        )
        status = gap.get("status")
        record_id = gap.get("record_id")
        if not controlled_value(status, GAP_STATUS_VALUES):
            findings.append(f"controlled-value-invalid: {path}.status")
        if status == "unresolved-candidate":
            if record_id is not None:
                findings.append("gap-scope-inconsistent")
        elif not nonblank(record_id):
            findings.append("gap-scope-inconsistent")
        if "retrieval_attempts" in gap:
            validate_string_list(gap["retrieval_attempts"], f"{path}.retrieval_attempts", findings)
    return valid_gaps


def validate_transfer_cards(cards, findings):
    if not isinstance(cards, list):
        add_malformed(findings, "transfer_cards")
        return []
    valid_cards = []
    for index, card in enumerate(cards):
        path = f"transfer_cards[{index}]"
        if not validate_object(card, path, CARD_REQUIRED, findings):
            continue
        valid_cards.append(card)
        validate_nonblank_fields(
            card,
            path,
            (
                "card_id",
                "proposition",
                "universe",
                "date_range",
                "missingness",
                "permitted_use",
                "prohibited_inference",
                "actual_source_identity",
            ),
            findings,
        )
        for field in ("numerator", "denominator"):
            if field in card and not nonnegative_integer(card[field]):
                add_malformed(findings, f"{path}.{field}")
        for field in ("source_row_ids", "disconfirming_row_ids"):
            if field in card:
                validate_string_list(
                    card[field], f"{path}.{field}", findings, field == "source_row_ids"
                )
                values = card[field]
                if (
                    isinstance(values, list)
                    and all(isinstance(value, str) for value in values)
                    and len(values) != len(set(values))
                ):
                    findings.append("duplicate-card-row-id")
        if not controlled_value(card.get("evidence_level"), EVIDENCE_LEVEL_VALUES):
            findings.append(f"controlled-value-invalid: {path}.evidence_level")
        if not controlled_value(card.get("metric_type"), METRIC_TYPE_VALUES):
            findings.append(f"controlled-value-invalid: {path}.metric_type")
        for field in ("checked_through", "source_checked_date"):
            if field in card and not iso_date(card[field]):
                add_malformed(findings, f"{path}.{field}")
        numerator = card.get("numerator")
        denominator = card.get("denominator")
        if nonnegative_integer(numerator) and nonnegative_integer(denominator):
            if numerator > denominator:
                findings.append("transfer-card-count-inconsistent")
    return valid_cards


def duplicate_findings(items, identifier, finding):
    seen = set()
    results = []
    for item in items:
        value = item.get(identifier)
        if nonblank(value):
            if value in seen:
                results.append(finding)
            seen.add(value)
    return results


def validate_references(records, gaps, cards, findings):
    record_by_id = {
        record.get("record_id"): record
        for record in records
        if nonblank(record.get("record_id"))
    }
    record_ids = set(record_by_id)
    gap_by_id = {gap.get("gap_id"): gap for gap in gaps if nonblank(gap.get("gap_id"))}
    for gap in gaps:
        if (
            gap.get("status") != "unresolved-candidate"
            and nonblank(gap.get("record_id"))
            and gap["record_id"] not in record_ids
        ):
            findings.append("gap-row-reference-invalid")
    for record in records:
        record_id = record.get("record_id")
        related = record.get("related_stage_ids")
        if isinstance(related, list):
            for related_id in related:
                if nonblank(related_id) and related_id not in record_ids:
                    findings.append("related-stage-reference-invalid")
                elif (
                    nonblank(related_id)
                    and record_by_id[related_id].get("motion_id") != record.get("motion_id")
                ):
                    findings.append("related-stage-motion-inconsistent")
        documents = record.get("missing_documents")
        if isinstance(documents, list):
            for document in documents:
                if not isinstance(document, dict):
                    continue
                gap_id = document.get("gap_id")
                gap = gap_by_id.get(gap_id)
                if (
                    gap is None
                    or gap.get("record_id") != record_id
                    or gap.get("document_type") != document.get("document_type")
                    or gap.get("status") == "unresolved-candidate"
                ):
                    findings.append("missing-gap-entry")
    missing_document_keys = {
        (record.get("record_id"), document.get("gap_id"), document.get("document_type"))
        for record in records
        if isinstance(record.get("missing_documents"), list)
        for document in record["missing_documents"]
        if isinstance(document, dict)
        and nonblank(record.get("record_id"))
        and nonblank(document.get("gap_id"))
        and nonblank(document.get("document_type"))
    }
    for gap in gaps:
        if gap.get("status") == "unresolved-candidate":
            continue
        gap_key = (gap.get("record_id"), gap.get("gap_id"), gap.get("document_type"))
        if not all(nonblank(value) for value in gap_key):
            continue
        if gap_key not in missing_document_keys:
            findings.append("missing-gap-entry")
    for card in cards:
        for field in ("source_row_ids", "disconfirming_row_ids"):
            values = card.get(field)
            if isinstance(values, list):
                for value in values:
                    if nonblank(value) and value not in record_ids:
                        findings.append("source-row-reference-invalid")
                    elif (
                        field == "source_row_ids"
                        and nonblank(value)
                        and record_by_id[value].get("retrieval_status")
                        in {"lead-only", "index-only"}
                    ):
                        findings.append("unverified-card-source")


def validate_denominator_semantics(denominator, records, gaps, cards, findings):
    if not isinstance(denominator, dict):
        return
    motion_ids = {record.get("motion_id") for record in records if nonblank(record.get("motion_id"))}
    coded_count = denominator.get("coded_pair_count")
    if nonnegative_integer(coded_count) and coded_count != len(motion_ids):
        findings.append("denominator-coded-pair-count-inconsistent")
    candidate_only_ids = {
        gap.get("candidate_id")
        for gap in gaps
        if gap.get("status") == "unresolved-candidate"
        and gap.get("record_id") is None
        and nonblank(gap.get("candidate_id"))
    }
    unresolved_documents = any(
        isinstance(record.get("missing_documents"), list) and record["missing_documents"]
        for record in records
    )
    unresolved_count = denominator.get("unresolved_relevant_missingness")
    if nonnegative_integer(unresolved_count) and unresolved_count != len(gaps):
        findings.append("denominator-missingness-inconsistent")
    candidate_count = denominator.get("candidate_count")
    research_complete_count = denominator.get("research_question_complete_count")
    if (
        nonnegative_integer(candidate_count)
        and nonnegative_integer(coded_count)
        and candidate_count != coded_count + len(candidate_only_ids)
    ):
        findings.append("candidate-inventory-inconsistent")
    complete_universe = (
        denominator.get("completeness_status") == "complete"
        and denominator.get("sampling_method") == "attempted-census"
        and unresolved_count == 0
        and candidate_count == coded_count
        and research_complete_count == coded_count
        and all(record.get("retrieval_status") == "complete-pair" for record in records)
        and not gaps
        and not unresolved_documents
    )
    if denominator.get("completeness_status") == "complete" and not complete_universe:
        findings.append("denominator-completeness-inconsistent")
    for card in cards:
        if card.get("evidence_level") == "tendency" and not complete_universe:
            findings.append("incomplete-tendency")
        if card.get("metric_type") == "success-rate" and not complete_universe:
            findings.append("incomplete-success-rate")


def validate_corpus(corpus: object) -> list[str]:
    findings = []
    if not isinstance(corpus, dict):
        return ["malformed-input: top-level corpus must be an object"]
    for field in TOP_LEVEL_REQUIRED:
        if field not in corpus:
            findings.append(f"missing-required-field: {field}")
    for field in corpus:
        if field not in TOP_LEVEL_REQUIRED:
            findings.append(f"unexpected-field: {field}")
    if "schema_version" in corpus and not version_string(corpus["schema_version"]):
        add_malformed(findings, "schema_version")
    if "study" in corpus:
        validate_study(corpus["study"], findings)
    if "denominator" in corpus:
        validate_denominator(corpus["denominator"], findings)
    records = validate_decision_records(corpus.get("decision_records"), findings) if "decision_records" in corpus else []
    gaps = validate_retrieval_gaps(corpus.get("retrieval_gaps"), findings) if "retrieval_gaps" in corpus else []
    cards = validate_transfer_cards(corpus.get("transfer_cards"), findings) if "transfer_cards" in corpus else []
    findings.extend(duplicate_findings(records, "record_id", "duplicate-decision-id"))
    findings.extend(duplicate_findings(gaps, "gap_id", "duplicate-gap-id"))
    findings.extend(duplicate_findings(cards, "card_id", "duplicate-card-id"))
    validate_references(records, gaps, cards, findings)
    validate_denominator_semantics(corpus.get("denominator"), records, gaps, cards, findings)
    return list(dict.fromkeys(findings))


def _input_root(value):
    try:
        path = Path(value)
        if not path.is_absolute():
            raise ValueError
        resolved = path.resolve(strict=True)
        if not resolved.is_dir():
            raise ValueError
        return resolved
    except (OSError, RuntimeError, TypeError, ValueError):
        return None


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


def validate_folder_corpus(
    *, decisions_root, corpus_target, max_input_bytes=MAX_INPUT_BYTES
):
    root = _input_root(decisions_root)
    relative = _relative_target(corpus_target)
    if root is None or relative is None or type(max_input_bytes) is not int or max_input_bytes < 1:
        findings = ["input-path-invalid: decisions target"]
    else:
        max_input_bytes = min(max_input_bytes, MAX_INPUT_BYTES)
        try:
            resolved = (root / relative).resolve(strict=True)
            resolved.relative_to(root)
            if not resolved.is_file():
                raise ValueError
            with resolved.open("rb") as source:
                payload = source.read(max_input_bytes + 1)
        except (OSError, RuntimeError, TypeError, ValueError):
            findings = ["input-path-invalid: decisions target"]
        else:
            if len(payload) > max_input_bytes:
                findings = ["input-file-too-large: decisions target"]
            else:
                try:
                    corpus = json.loads(payload.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as error:
                    findings = [f"malformed-input: {error}"]
                else:
                    findings = validate_corpus(corpus)
    return {"passed": not findings, "findings": findings}


def _parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--decisions-root")
    parser.add_argument("--corpus-target")
    return parser


def main(arguments):
    parsed = _parser().parse_args(arguments)
    if (parsed.decisions_root is None) != (parsed.corpus_target is None):
        findings = ["input-path-invalid: decisions root and corpus target are required together"]
    elif parsed.decisions_root is not None:
        findings = validate_folder_corpus(
            decisions_root=parsed.decisions_root,
            corpus_target=parsed.corpus_target,
        )["findings"]
    else:
        stream = getattr(sys.stdin, "buffer", sys.stdin)
        payload = stream.read(MAX_INPUT_BYTES + 1)
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
        if len(payload) > MAX_INPUT_BYTES:
            findings = ["input-file-too-large: corpus input"]
        else:
            try:
                corpus = json.loads(payload.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as error:
                findings = [f"malformed-input: {error}"]
            else:
                findings = validate_corpus(corpus)
    if findings:
        for finding in findings:
            print(finding)
        return 1
    print("corpus validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
