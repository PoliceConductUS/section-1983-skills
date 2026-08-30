import hashlib
import json
import re
from datetime import date
from pathlib import Path, PurePosixPath


MAX_COMPLAINT_BYTES = 5 * 1024 * 1024
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_IDENTITY_STATUSES = frozenset(
    {
        "named-serviceable",
        "unnamed",
        "role-only",
        "misnamed",
        "named-not-serviceable",
    }
)
_AMENDMENT_ACTIONS = frozenset({"unchanged", "added", "identified", "substituted"})
_DEADLINE_STATUSES = frozenset({"not-passed", "passed", "unresolved"})
_ANALYSIS_FIELDS = frozenset({"status", "analysis", "source_refs"})
_DATED_FACT_FIELDS = frozenset({"status", "date", "basis", "source_refs"})
_IDENTIFICATION_FIELDS = _DATED_FACT_FIELDS | frozenset(
    {"identification_source", "identification_method"}
)
_AUTHORITY_ROUTES = frozenset(
    {
        "limitations",
        "rule_15_c_1_a",
        "rule_15_c_1_c",
        "rule_4_m",
        "tolling",
        "concealment",
    }
)


class ComplaintCheckError(Exception):
    def __init__(self, finding_id, message):
        super().__init__(message)
        self.finding_id = finding_id


def _contract_path():
    return Path(__file__).resolve().parents[1] / "references" / "complaint-structure-contract.json"


def _limitations_schema_path():
    return Path(__file__).resolve().parents[1] / "references" / "limitations-record.schema.json"


def _load_contract():
    try:
        contract = json.loads(_contract_path().read_text(encoding="utf-8"))
        limitations_schema = json.loads(
            _limitations_schema_path().read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as error:
        raise ComplaintCheckError("complaint-contract-unavailable", str(error)) from error
    if (
        contract.get("owner") != "drafting-section-1983-complaints"
        or limitations_schema.get("$id")
        != "https://policeconduct.us/schemas/section-1983-limitations-record-v1.json"
    ):
        raise ComplaintCheckError(
            "complaint-contract-unavailable", "unexpected complaint contract owner"
        )
    return contract


def _target_path(input_root, relative_target):
    root = Path(input_root).resolve(strict=True)
    if not root.is_dir() or not isinstance(relative_target, str) or not relative_target:
        raise ComplaintCheckError("invalid-target", "target must name a declared input file")
    if "\\" in relative_target or "//" in relative_target:
        raise ComplaintCheckError("invalid-target", "target is not canonical")
    logical = PurePosixPath(relative_target)
    if logical.is_absolute() or any(part in {"", ".", ".."} for part in logical.parts):
        raise ComplaintCheckError("invalid-target", "target is not canonical")
    candidate = root.joinpath(*logical.parts)
    current = root
    for part in logical.parts:
        current = current / part
        if current.is_symlink():
            raise ComplaintCheckError("invalid-target", "target crosses a symlink")
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as error:
        raise ComplaintCheckError("invalid-target", "target is outside the declared input root") from error
    if not resolved.is_file():
        raise ComplaintCheckError("invalid-target", "target is not a file")
    return resolved, logical.as_posix()


def _finding(check_id, target, location, message):
    identity = hashlib.sha256(
        f"{check_id}\0{target}\0{location}\0{message}".encode("utf-8")
    ).hexdigest()[:16]
    return {
        "finding_id": f"{check_id}-{identity}",
        "check_id": check_id,
        "severity": "hard",
        "artifact": target,
        "location": location,
        "message": message,
    }


def _sequence_findings(values, key, check_id, target, location):
    numbers = []
    if not isinstance(values, list):
        return [_finding(check_id, target, location, "expected an ordered array")]
    for index, value in enumerate(values):
        number = value.get(key) if isinstance(value, dict) else None
        if type(number) is not int:
            return [
                _finding(
                    check_id,
                    target,
                    f"{location}[{index}]",
                    f"{key} must be an integer",
                )
            ]
        numbers.append(number)
    expected = list(range(1, len(numbers) + 1))
    if numbers != expected:
        return [_finding(check_id, target, location, "numbering must be continuous from 1")]
    return []


def _valid_paragraph_reference(value, paragraph_numbers):
    return type(value) is int and value in paragraph_numbers


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _source_refs(value):
    return (
        isinstance(value, list)
        and bool(value)
        and all(
            _text(item) and _IDENTIFIER.fullmatch(item) is not None for item in value
        )
        and len(value) == len(set(value))
    )


def _iso_date(value, *, nullable=False):
    if value is None:
        return nullable
    if not isinstance(value, str):
        return False
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return False
    return parsed.isoformat() == value


def _analysis_entry(value):
    valid = (
        isinstance(value, dict)
        and set(value) == _ANALYSIS_FIELDS
        and value.get("status") in {"complete", "unresolved"}
        and _text(value.get("analysis"))
        and _source_refs(value.get("source_refs"))
    )
    return valid, isinstance(value, dict) and value.get("status") == "unresolved"


def _dated_fact(value, *, identification=False):
    expected = _IDENTIFICATION_FIELDS if identification else _DATED_FACT_FIELDS
    valid = (
        isinstance(value, dict)
        and set(value) == expected
        and value.get("status") in {"complete", "unresolved"}
        and _text(value.get("basis"))
        and _source_refs(value.get("source_refs"))
        and (
            _iso_date(value.get("date"))
            if value.get("status") == "complete"
            else _iso_date(value.get("date"), nullable=True)
        )
    )
    if identification and isinstance(value, dict):
        valid = valid and _text(value.get("identification_source")) and _text(
            value.get("identification_method")
        )
    return valid, isinstance(value, dict) and value.get("status") == "unresolved"


def _diligence_entry(value):
    return (
        isinstance(value, dict)
        and set(value) == {"date", "action", "result", "source_refs"}
        and _iso_date(value.get("date"))
        and _text(value.get("action"))
        and _text(value.get("result"))
        and _source_refs(value.get("source_refs"))
    )


def _limitations_record_findings(record, target, location):
    findings = []
    unresolved = False

    def invalid(child, message):
        findings.append(
            _finding(
                "limitations-record-structure",
                target,
                f"{location}.{child}",
                message,
            )
        )

    required = {
        "record_id",
        "defendant_id",
        "accrual",
        "limitations_deadline",
        "original_doe_or_role_description",
        "same_transaction_analysis",
        "mistake_versus_lack_of_knowledge",
        "identity_timeline",
        "diligence",
        "record_control_provenance",
        "rule_15_c_1_c_notice",
        "service",
        "rule_4_m",
        "authority_routes",
        "defendant_specific_concealment_or_tolling",
        "fallback_claims_and_severable_relief",
        "filing_critical_gaps",
        "status",
    }
    if not isinstance(record, dict):
        invalid("", "limitations record must be an object")
        return findings, True
    if set(record) != required:
        invalid("", "limitations record fields do not match the schema")
        unresolved = True
    for field in ("record_id", "defendant_id"):
        if not _text(record.get(field)) or _IDENTIFIER.fullmatch(record[field]) is None:
            invalid(field, f"{field} must be a stable identifier")
            unresolved = True

    for field in ("accrual", "limitations_deadline"):
        valid, entry_unresolved = _dated_fact(record.get(field))
        if not valid:
            invalid(field, f"{field} must be a sourced dated fact")
            unresolved = True
        unresolved = unresolved or entry_unresolved

    for field in (
        "original_doe_or_role_description",
        "same_transaction_analysis",
        "mistake_versus_lack_of_knowledge",
        "defendant_specific_concealment_or_tolling",
        "fallback_claims_and_severable_relief",
    ):
        valid, entry_unresolved = _analysis_entry(record.get(field))
        if not valid:
            invalid(field, f"{field} must be a sourced analysis entry")
            unresolved = True
        unresolved = unresolved or entry_unresolved

    timeline = record.get("identity_timeline")
    timeline_fields = {
        "source_first_available",
        "source_first_possessed",
        "objectively_ascertainable",
        "actual_identification",
    }
    if not isinstance(timeline, dict) or set(timeline) != timeline_fields:
        invalid(
            "identity_timeline",
            "identity availability, possession, ascertainability, and identification must be separate",
        )
        unresolved = True
    else:
        for field in timeline_fields:
            valid, entry_unresolved = _dated_fact(
                timeline[field], identification=field == "actual_identification"
            )
            if not valid:
                invalid(
                    f"identity_timeline.{field}",
                    f"{field} must be a separate sourced identity event",
                )
                unresolved = True
            unresolved = unresolved or entry_unresolved

    diligence = record.get("diligence")
    diligence_fields = {
        "pre_limitations",
        "post_filing_pre_identification",
        "post_identification_pre_service",
    }
    if not isinstance(diligence, dict) or set(diligence) != diligence_fields:
        invalid("diligence", "all three diligence stages are required")
        unresolved = True
    else:
        for field in diligence_fields:
            entries = diligence[field]
            if (
                not isinstance(entries, list)
                or not entries
                or not all(_diligence_entry(entry) for entry in entries)
            ):
                invalid(
                    f"diligence.{field}",
                    f"{field} requires dated and sourced diligence entries",
                )
                unresolved = True

    provenance = record.get("record_control_provenance")
    provenance_fields = {
        "record",
        "holder_or_controller",
        "request_recipient",
        "request_date",
        "response_date",
        "denial_date",
        "follow_up_dates",
        "stated_basis",
        "source_refs",
        "attribution",
    }
    if not isinstance(provenance, list) or not provenance:
        invalid(
            "record_control_provenance",
            "at least one record-control provenance entry is required",
        )
        unresolved = True
    else:
        for index, entry in enumerate(provenance):
            child = f"record_control_provenance[{index}]"
            valid = isinstance(entry, dict) and set(entry) == provenance_fields
            if valid:
                valid = (
                    all(
                        _text(entry.get(field))
                        for field in (
                            "record",
                            "holder_or_controller",
                            "request_recipient",
                            "stated_basis",
                        )
                    )
                    and all(
                        _iso_date(entry.get(field), nullable=True)
                        for field in ("request_date", "response_date", "denial_date")
                    )
                    and isinstance(entry.get("follow_up_dates"), list)
                    and all(_iso_date(value) for value in entry["follow_up_dates"])
                    and len(entry["follow_up_dates"])
                    == len(set(entry["follow_up_dates"]))
                    and _source_refs(entry.get("source_refs"))
                )
            attribution = entry.get("attribution") if isinstance(entry, dict) else None
            if not isinstance(attribution, dict) or set(attribution) != {
                "municipality",
                "custodian",
                "individual_defendant",
            }:
                valid = False
            else:
                for actor in (
                    "municipality",
                    "custodian",
                    "individual_defendant",
                ):
                    actor_valid, actor_unresolved = _analysis_entry(attribution[actor])
                    valid = valid and actor_valid
                    unresolved = unresolved or actor_unresolved
            if not valid:
                invalid(child, "record control and actor attribution are malformed")
                unresolved = True

    notice = record.get("rule_15_c_1_c_notice")
    notice_fields = {
        "status",
        "recipient",
        "date",
        "factual_basis",
        "prejudice_analysis",
        "knew_or_should_have_known_but_for_mistake_analysis",
        "source_refs",
    }
    notice_valid = isinstance(notice, dict) and set(notice) == notice_fields
    if notice_valid:
        notice_valid = (
            notice.get("status") in {"complete", "unresolved"}
            and all(
                _text(notice.get(field))
                for field in (
                    "recipient",
                    "factual_basis",
                    "prejudice_analysis",
                    "knew_or_should_have_known_but_for_mistake_analysis",
                )
            )
            and _iso_date(notice.get("date"), nullable=True)
            and _source_refs(notice.get("source_refs"))
        )
        unresolved = unresolved or notice.get("status") == "unresolved"
    if not notice_valid:
        invalid("rule_15_c_1_c_notice", "Rule 15(c)(1)(C) notice facts are malformed")
        unresolved = True

    service = record.get("service")
    service_fields = {
        "status",
        "service_status",
        "date",
        "method",
        "attempts",
        "proof",
        "source_refs",
    }
    service_valid = isinstance(service, dict) and set(service) == service_fields
    if service_valid:
        service_valid = (
            service.get("status") in {"complete", "unresolved"}
            and service.get("service_status")
            in {"not-attempted", "attempted", "served", "unresolved"}
            and all(_text(service.get(field)) for field in ("method", "attempts", "proof"))
            and _iso_date(service.get("date"), nullable=True)
            and _source_refs(service.get("source_refs"))
        )
        unresolved = unresolved or service.get("status") == "unresolved"
        unresolved = unresolved or service.get("service_status") == "unresolved"
    if not service_valid:
        invalid("service", "service facts must remain separate and complete")
        unresolved = True

    rule_4_m = record.get("rule_4_m")
    rule_4_m_fields = {
        "status",
        "deadline",
        "extension_request_status",
        "good_cause_facts",
        "discretionary_extension_facts",
        "requested_relief",
        "source_refs",
    }
    rule_4_m_valid = isinstance(rule_4_m, dict) and set(rule_4_m) == rule_4_m_fields
    if rule_4_m_valid:
        rule_4_m_valid = (
            rule_4_m.get("status") in {"complete", "unresolved"}
            and rule_4_m.get("extension_request_status")
            in {"not-requested", "pending", "granted", "denied", "unresolved"}
            and _iso_date(rule_4_m.get("deadline"), nullable=True)
            and all(
                _text(rule_4_m.get(field))
                for field in (
                    "good_cause_facts",
                    "discretionary_extension_facts",
                    "requested_relief",
                )
            )
            and _source_refs(rule_4_m.get("source_refs"))
        )
        unresolved = unresolved or rule_4_m.get("status") == "unresolved"
        unresolved = unresolved or rule_4_m.get("extension_request_status") == "unresolved"
    if not rule_4_m_valid:
        invalid("rule_4_m", "Rule 4(m) deadline and extension facts are malformed")
        unresolved = True

    routes = record.get("authority_routes")
    if not isinstance(routes, dict) or set(routes) != _AUTHORITY_ROUTES:
        invalid("authority_routes", "all authority routes must be classified separately")
        unresolved = True
    else:
        relied_fields = {
            "status",
            "controlling_jurisdiction",
            "governing_authority",
            "pinpoint",
            "authority_status",
            "supported_proposition",
            "defendant_specific_application",
            "source_refs",
        }
        for route, entry in routes.items():
            valid = isinstance(entry, dict)
            if valid and entry.get("status") == "relied-on":
                valid = (
                    set(entry) == relied_fields
                    and all(
                        _text(entry.get(field))
                        for field in relied_fields - {"status", "source_refs"}
                    )
                    and entry.get("authority_status")
                    in {
                        "binding-current",
                        "binding-status-unresolved",
                        "persuasive-current",
                        "superseded",
                        "unresolved",
                    }
                    and _source_refs(entry.get("source_refs"))
                )
                unresolved = unresolved or entry.get("authority_status") in {
                    "binding-status-unresolved",
                    "unresolved",
                }
            elif valid and entry.get("status") in {"not-relied-on", "unresolved"}:
                valid = (
                    set(entry) == {"status", "reason", "source_refs"}
                    and _text(entry.get("reason"))
                    and _source_refs(entry.get("source_refs"))
                )
                unresolved = unresolved or entry.get("status") == "unresolved"
            else:
                valid = False
            if not valid:
                invalid(
                    f"authority_routes.{route}",
                    f"{route} authority classification is malformed",
                )
                unresolved = True

    gaps = record.get("filing_critical_gaps")
    if (
        not isinstance(gaps, list)
        or any(not _text(gap) for gap in gaps)
        or len(gaps) != len(set(gaps))
    ):
        invalid("filing_critical_gaps", "filing-critical gaps must be unique strings")
        unresolved = True
        gaps = []
    if record.get("status") not in {"clear", "blocked"}:
        invalid("status", "record status must be clear or blocked")
        unresolved = True
    if unresolved or record.get("status") == "blocked" or gaps:
        findings.append(
            _finding(
                "limitations-filing-critical-status",
                target,
                location,
                "missing, malformed, or unresolved limitations material blocks the filing gate",
            )
        )
    return findings, unresolved or record.get("status") == "blocked" or bool(gaps)


def _limitations_findings(document, target):
    if not isinstance(document, dict) or "limitations_gate" not in document:
        return [
            _finding(
                "limitations-gate-presence",
                target,
                "limitations_gate",
                "the complaint handoff requires a limitations_gate object",
            )
        ]
    gate = document["limitations_gate"]
    required = {
        "schema_version",
        "status",
        "intended_individuals",
        "records",
        "filing_critical_gaps",
    }
    if not isinstance(gate, dict) or set(gate) != required or gate.get("schema_version") != 1:
        return [
            _finding(
                "limitations-gate-presence",
                target,
                "limitations_gate",
                "limitations_gate does not match schema version 1",
            )
        ]

    findings = []
    critical = False
    intended = gate.get("intended_individuals")
    if not isinstance(intended, list):
        findings.append(
            _finding(
                "limitations-trigger-structure",
                target,
                "limitations_gate.intended_individuals",
                "intended individuals must be an array",
            )
        )
        intended = []
        critical = True
    affected = set()
    seen_defendants = set()
    expected_intended_fields = {
        "defendant_id",
        "name_or_role",
        "identity_status",
        "amendment_action",
        "deadline_status",
        "risk_raised",
    }
    for index, entry in enumerate(intended):
        location = f"limitations_gate.intended_individuals[{index}]"
        valid = isinstance(entry, dict) and set(entry) == expected_intended_fields
        defendant_id = entry.get("defendant_id") if isinstance(entry, dict) else None
        if valid:
            valid = (
                _text(defendant_id)
                and _IDENTIFIER.fullmatch(defendant_id) is not None
                and defendant_id not in seen_defendants
                and _text(entry.get("name_or_role"))
                and entry.get("identity_status") in _IDENTITY_STATUSES
                and entry.get("amendment_action") in _AMENDMENT_ACTIONS
                and entry.get("deadline_status") in _DEADLINE_STATUSES
                and type(entry.get("risk_raised")) is bool
            )
        if not valid:
            findings.append(
                _finding(
                    "limitations-trigger-structure",
                    target,
                    location,
                    "intended-individual trigger facts are malformed or duplicated",
                )
            )
            critical = True
            continue
        seen_defendants.add(defendant_id)
        if (
            entry["identity_status"] != "named-serviceable"
            or entry["risk_raised"]
            or (
                entry["amendment_action"] in {"added", "identified", "substituted"}
                and entry["deadline_status"] in {"passed", "unresolved"}
            )
        ):
            affected.add(defendant_id)

    records = gate.get("records")
    if not isinstance(records, list):
        findings.append(
            _finding(
                "limitations-record-structure",
                target,
                "limitations_gate.records",
                "limitations records must be an array",
            )
        )
        records = []
        critical = True
    records_by_defendant = {}
    seen_record_ids = set()
    for index, record in enumerate(records):
        location = f"limitations_gate.records[{index}]"
        record_id = record.get("record_id") if isinstance(record, dict) else None
        defendant_id = record.get("defendant_id") if isinstance(record, dict) else None
        if (
            not _text(record_id)
            or _IDENTIFIER.fullmatch(record_id) is None
            or record_id in seen_record_ids
            or not _text(defendant_id)
            or defendant_id in records_by_defendant
        ):
            findings.append(
                _finding(
                    "limitations-record-cardinality",
                    target,
                    location,
                    "record and defendant IDs must be present and unique",
                )
            )
            critical = True
        else:
            seen_record_ids.add(record_id)
            records_by_defendant[defendant_id] = record

    for defendant_id in sorted(affected):
        record = records_by_defendant.get(defendant_id)
        if record is None:
            findings.append(
                _finding(
                    "limitations-record-cardinality",
                    target,
                    f"limitations_gate.records.{defendant_id}",
                    "each affected intended individual requires one limitations record",
                )
            )
            critical = True
            continue
        record_findings, record_critical = _limitations_record_findings(
            record,
            target,
            f"limitations_gate.records.{defendant_id}",
        )
        findings.extend(record_findings)
        critical = critical or record_critical

    gaps = gate.get("filing_critical_gaps")
    if (
        not isinstance(gaps, list)
        or any(not _text(gap) for gap in gaps)
        or len(gaps) != len(set(gaps))
    ):
        findings.append(
            _finding(
                "limitations-filing-critical-status",
                target,
                "limitations_gate.filing_critical_gaps",
                "filing-critical gaps must be unique strings",
            )
        )
        gaps = []
        critical = True
    if gate.get("status") not in {"clear", "blocked"}:
        critical = True
    if critical or gate.get("status") == "blocked" or gaps:
        findings.append(
            _finding(
                "limitations-filing-critical-status",
                target,
                "limitations_gate.status",
                "the limitations gate remains blocked or contains unresolved material",
            )
        )
    return findings


def _mechanical_findings(document, contract, target):
    findings = []
    sections = document.get("sections") if isinstance(document, dict) else None
    section_ids = [section["id"] for section in contract["sections"]]
    required_sections = [
        section["id"] for section in contract["sections"] if not section["optional"]
    ]
    if not isinstance(sections, list) or any(not isinstance(item, str) for item in sections):
        findings.append(_finding("section-presence", target, "sections", "sections must be an array of identifiers"))
        sections = []
    for section_id in required_sections:
        if section_id not in sections:
            findings.append(_finding("section-presence", target, f"sections.{section_id}", "required section is missing"))
    known_sections = [section for section in sections if section in section_ids]
    expected_order = sorted(known_sections, key=section_ids.index)
    if known_sections != expected_order or len(known_sections) != len(set(known_sections)):
        findings.append(_finding("section-order", target, "sections", "sections are out of canonical order or duplicated"))

    paragraphs = document.get("paragraphs", []) if isinstance(document, dict) else []
    findings.extend(_sequence_findings(paragraphs, "number", "paragraph-numbering-continuity", target, "paragraphs"))
    paragraph_numbers = {
        paragraph.get("number")
        for paragraph in paragraphs
        if isinstance(paragraph, dict) and type(paragraph.get("number")) is int
    }
    for index, paragraph in enumerate(paragraphs if isinstance(paragraphs, list) else []):
        references = paragraph.get("cross_references", []) if isinstance(paragraph, dict) else []
        if not isinstance(references, list) or any(
            not _valid_paragraph_reference(reference, paragraph_numbers)
            for reference in references
        ):
            findings.append(_finding("cross-reference-target", target, f"paragraphs[{index}].cross_references", "cross-reference target is missing"))

    counts = document.get("counts", []) if isinstance(document, dict) else []
    findings.extend(_sequence_findings(counts, "number", "count-numbering-continuity", target, "counts"))
    seen_ids = set()
    seen_tuples = set()
    for index, count in enumerate(counts if isinstance(counts, list) else []):
        if not isinstance(count, dict):
            findings.append(_finding("required-count-field-location", target, f"counts[{index}]", "count must be an object"))
            continue
        count_id = count.get("count_id")
        if not isinstance(count_id, str) or not count_id or count_id in seen_ids:
            findings.append(_finding("unique-count-id", target, f"counts[{index}].count_id", "count_id must be present and unique"))
        else:
            seen_ids.add(count_id)
        cardinality_values = [count.get(field) for field in contract["count_cardinality"]]
        cardinality = tuple(
            json.dumps(value, sort_keys=True, separators=(",", ":"))
            for value in cardinality_values
        )
        if any(
            not isinstance(value, str) or not value.strip()
            for value in cardinality_values
        ) or cardinality in seen_tuples:
            findings.append(_finding("claim-defendant-challenged-act-cardinality", target, f"counts[{index}]", "count tuple must be complete and unique"))
        else:
            seen_tuples.add(cardinality)
        for field in contract["required_count_fields"]:
            if field not in count or count[field] is None or count[field] == "":
                findings.append(_finding("required-count-field-location", target, f"counts[{index}].{field}", "required count field is missing"))
        incorporated = count.get("incorporated_paragraphs", [])
        if not isinstance(incorporated, list) or any(
            not _valid_paragraph_reference(number, paragraph_numbers)
            for number in incorporated
        ):
            findings.append(_finding("incorporation-target", target, f"counts[{index}].incorporated_paragraphs", "incorporated paragraph target is missing"))
    findings.extend(_limitations_findings(document, target))
    return findings


def _report_bytes(report):
    return (json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def check_complaint(input_root, relative_target):
    contract = _load_contract()
    target_path, target = _target_path(input_root, relative_target)
    try:
        content = target_path.read_bytes()
    except OSError as error:
        raise ComplaintCheckError("unreadable-input", str(error)) from error
    if len(content) > MAX_COMPLAINT_BYTES:
        raise ComplaintCheckError("input-too-large", "complaint exceeds the packaged checker bound")
    try:
        document = json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ComplaintCheckError("malformed-input", str(error)) from error
    findings = _mechanical_findings(document, contract, target)
    report = {
        "schema_version": 1,
        "checker_id": "section-1983-complaint-v1",
        "target": target,
        "target_sha256": hashlib.sha256(content).hexdigest(),
        "checks": contract["mechanical_checks"],
        "excluded_judgments": contract["excluded_judgments"],
        "status": "failed" if findings else "passed",
        "findings": findings,
    }
    return {
        "status": report["status"],
        "exit_status": 1 if findings else 0,
        "findings": findings,
        "report_bytes": _report_bytes(report),
    }
