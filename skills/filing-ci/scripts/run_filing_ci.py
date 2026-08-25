import hashlib
import json
import re
from pathlib import Path, PurePosixPath


CHECKER_ID = "section-1983-complaint-v1"
MAX_FILING_BYTES = 5 * 1024 * 1024
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_SHORT_FORM = re.compile(r"^Ex\. [A-Za-z0-9][A-Za-z0-9.-]*$")


def _bytes(document):
    return (json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _unavailable(checker_id, reason):
    report = {
        "schema_version": 1,
        "checker_id": checker_id,
        "status": "unavailable",
        "reason": reason,
        "findings": [],
    }
    return {
        "status": "unavailable",
        "reason": reason,
        "checker_id": checker_id,
        "report_bytes": _bytes(report),
    }


def _contract():
    path = Path(__file__).resolve().parents[1] / "references" / "complaint-checker-contract.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _target(input_root, relative_target):
    root = Path(input_root).resolve(strict=True)
    if not root.is_dir() or not isinstance(relative_target, str) or not relative_target:
        raise ValueError("invalid-target")
    if "\\" in relative_target or "//" in relative_target:
        raise ValueError("invalid-target")
    logical = PurePosixPath(relative_target)
    if logical.is_absolute() or any(part in {"", ".", ".."} for part in logical.parts):
        raise ValueError("invalid-target")
    candidate = root
    for part in logical.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise ValueError("invalid-target")
    resolved = candidate.resolve(strict=True)
    resolved.relative_to(root)
    if not resolved.is_file():
        raise ValueError("invalid-target")
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


def _numbering(values, target, key, check_id, location):
    if not isinstance(values, list):
        return [_finding(check_id, target, location, "expected an ordered array")]
    numbers = [value.get(key) if isinstance(value, dict) else None for value in values]
    if any(type(number) is not int for number in numbers) or numbers != list(
        range(1, len(numbers) + 1)
    ):
        return [_finding(check_id, target, location, "numbering must be continuous from 1")]
    return []


def _valid_paragraph_reference(value, paragraph_numbers):
    return type(value) is int and value in paragraph_numbers


def _complaint_findings(document, contract, target):
    findings = []
    sections = document.get("sections", []) if isinstance(document, dict) else []
    canonical = [section["id"] for section in contract["sections"]]
    required = [section["id"] for section in contract["sections"] if not section["optional"]]
    if not isinstance(sections, list) or any(not isinstance(value, str) for value in sections):
        findings.append(_finding("section-presence", target, "sections", "sections must be identifiers"))
        sections = []
    for section in required:
        if section not in sections:
            findings.append(_finding("section-presence", target, f"sections.{section}", "required section is missing"))
    known = [section for section in sections if section in canonical]
    if known != sorted(known, key=canonical.index) or len(known) != len(set(known)):
        findings.append(_finding("section-order", target, "sections", "sections are out of order or duplicated"))

    paragraphs = document.get("paragraphs", []) if isinstance(document, dict) else []
    findings.extend(_numbering(paragraphs, target, "number", "paragraph-numbering-continuity", "paragraphs"))
    paragraph_numbers = {
        paragraph.get("number")
        for paragraph in paragraphs
        if isinstance(paragraph, dict) and type(paragraph.get("number")) is int
    }
    for index, paragraph in enumerate(paragraphs if isinstance(paragraphs, list) else []):
        references = paragraph.get("cross_references", []) if isinstance(paragraph, dict) else []
        if not isinstance(references, list) or any(
            not _valid_paragraph_reference(value, paragraph_numbers)
            for value in references
        ):
            findings.append(_finding("cross-reference-target", target, f"paragraphs[{index}].cross_references", "cross-reference target is missing"))

    counts = document.get("counts", []) if isinstance(document, dict) else []
    findings.extend(_numbering(counts, target, "number", "count-numbering-continuity", "counts"))
    count_ids = set()
    cardinalities = set()
    for index, count in enumerate(counts if isinstance(counts, list) else []):
        if not isinstance(count, dict):
            findings.append(_finding("required-count-field-location", target, f"counts[{index}]", "count must be an object"))
            continue
        count_id = count.get("count_id")
        if not isinstance(count_id, str) or not count_id or count_id in count_ids:
            findings.append(_finding("unique-count-id", target, f"counts[{index}].count_id", "count_id must be present and unique"))
        else:
            count_ids.add(count_id)
        cardinality_values = [count.get(field) for field in contract["count_cardinality"]]
        cardinality = tuple(
            json.dumps(value, sort_keys=True, separators=(",", ":"))
            for value in cardinality_values
        )
        if any(
            not isinstance(value, str) or not value.strip()
            for value in cardinality_values
        ) or cardinality in cardinalities:
            findings.append(_finding("claim-defendant-challenged-act-cardinality", target, f"counts[{index}]", "count tuple must be complete and unique"))
        else:
            cardinalities.add(cardinality)
        for field in contract["required_count_fields"]:
            if field not in count or count[field] is None or count[field] == "":
                findings.append(_finding("required-count-field-location", target, f"counts[{index}].{field}", "required count field is missing"))
        incorporated = count.get("incorporated_paragraphs", [])
        if not isinstance(incorporated, list) or any(
            not _valid_paragraph_reference(value, paragraph_numbers)
            for value in incorporated
        ):
            findings.append(_finding("incorporation-target", target, f"counts[{index}].incorporated_paragraphs", "incorporated paragraph target is missing"))
    return findings


def _integrity_findings(document, context, target):
    findings = []
    if not isinstance(document, dict) or not isinstance(context, dict):
        return [_finding("filing-structure", target, "filing", "filing context is invalid")]

    sections = document.get("sections", [])
    owners = document.get("section_owners")
    if not isinstance(owners, dict):
        findings.append(
            _finding("section-owner", target, "section_owners", "section ownership must be an object")
        )
        owners = {}
    for section in sections if isinstance(sections, list) else []:
        owner = owners.get(section)
        if not isinstance(owner, str) or not owner.strip():
            findings.append(
                _finding(
                    "section-owner",
                    target,
                    f"section_owners.{section}",
                    "each declared section requires one owner",
                )
            )

    exhibit_ids = set(context.get("exhibit_ids", []))
    exhibit_references = document.get("exhibit_references")
    if not isinstance(exhibit_references, list):
        findings.append(
            _finding(
                "exhibit-reference",
                target,
                "exhibit_references",
                "exhibit references must be an array",
            )
        )
        exhibit_references = []
    for index, reference in enumerate(exhibit_references):
        location = f"exhibit_references[{index}]"
        if not isinstance(reference, dict):
            findings.append(
                _finding("exhibit-reference", target, location, "exhibit reference must be an object")
            )
            continue
        exhibit_id = reference.get("exhibit_id")
        if exhibit_id not in exhibit_ids:
            findings.append(
                _finding(
                    "exhibit-reference",
                    target,
                    f"{location}.exhibit_id",
                    "exhibit source is not selected",
                )
            )
        start = reference.get("paragraph_start")
        end = reference.get("paragraph_end")
        if (
            type(start) is not int
            or type(end) is not int
            or start < 1
            or end < start
        ):
            findings.append(
                _finding(
                    "exhibit-paragraph-range",
                    target,
                    location,
                    "exhibit paragraph range must be positive and ordered",
                )
            )
        short_form = reference.get("short_form")
        if not isinstance(short_form, str) or _SHORT_FORM.fullmatch(short_form) is None:
            findings.append(
                _finding(
                    "internal-short-form",
                    target,
                    f"{location}.short_form",
                    "exhibit short form must use Ex. plus a stable label",
                )
            )

    docket_entries = context.get("docket_entries", [])
    docket_citations = document.get("docket_citations")
    if not isinstance(docket_citations, list):
        findings.append(
            _finding(
                "docket-appendix-consistency",
                target,
                "docket_citations",
                "docket citations must be an array",
            )
        )
        docket_citations = []
    for index, citation in enumerate(docket_citations):
        matched = False
        if isinstance(citation, dict):
            for entry in docket_entries:
                if (
                    citation.get("docket_entry") == entry["docket_entry"]
                    and citation.get("docket_page") == entry["docket_page"]
                    and type(citation.get("appendix_page")) is int
                    and entry["appendix_start"]
                    <= citation["appendix_page"]
                    <= entry["appendix_end"]
                ):
                    matched = True
                    break
        if not matched:
            findings.append(
                _finding(
                    "docket-appendix-consistency",
                    target,
                    f"docket_citations[{index}]",
                    "docket citation has no selected appendix mapping",
                )
            )

    available_targets = {
        "authority": set(context.get("authority_ids", [])),
        "record": set(context.get("record_ids", [])),
        "exhibit": exhibit_ids,
        "docket": set(context.get("docket_ids", [])),
    }
    citations = document.get("persistent_citations")
    if not isinstance(citations, list):
        findings.append(
            _finding(
                "persistent-citation-id",
                target,
                "persistent_citations",
                "persistent citations must be an array",
            )
        )
        citations = []
    seen_ids = set()
    for index, citation in enumerate(citations):
        location = f"persistent_citations[{index}]"
        if not isinstance(citation, dict):
            findings.append(
                _finding("persistent-citation-id", target, location, "citation must be an object")
            )
            continue
        citation_id = citation.get("id")
        if (
            not isinstance(citation_id, str)
            or _IDENTIFIER.fullmatch(citation_id) is None
            or citation_id in seen_ids
        ):
            findings.append(
                _finding(
                    "persistent-citation-id",
                    target,
                    f"{location}.id",
                    "citation ID must be stable and unique",
                )
            )
        else:
            seen_ids.add(citation_id)
        citation_type = citation.get("type")
        citation_target = citation.get("target")
        if (
            citation_type not in available_targets
            or citation_target not in available_targets.get(citation_type, set())
            or citation.get("status") != "resolved"
            or not isinstance(citation.get("visible_text"), str)
            or not citation["visible_text"].strip()
        ):
            findings.append(
                _finding(
                    "persistent-citation-target",
                    target,
                    location,
                    "citation target or resolution state is unavailable",
                )
            )

    gates = document.get("filing_gates")
    if not isinstance(gates, list):
        findings.append(
            _finding("open-filing-gate", target, "filing_gates", "filing gates must be an array")
        )
        gates = []
    for index, gate in enumerate(gates):
        if not isinstance(gate, dict) or gate.get("status") != "closed":
            findings.append(
                _finding(
                    "open-filing-gate",
                    target,
                    f"filing_gates[{index}]",
                    "filing gate remains open or malformed",
                )
            )
    return findings


def run_filing_ci(filing_root, filing_target, authorities_root, checker_id, context=None):
    if checker_id != CHECKER_ID:
        return _unavailable(checker_id, "checker-unavailable")
    try:
        authority_path = Path(authorities_root).resolve(strict=True)
    except OSError:
        return _unavailable(checker_id, "unresolved-input")
    if not authority_path.is_dir():
        return _unavailable(checker_id, "unresolved-input")
    try:
        target_path, target = _target(filing_root, filing_target)
    except (OSError, ValueError):
        return _unavailable(checker_id, "invalid-target")
    if target_path.suffix != ".json":
        return _unavailable(checker_id, "checker-incompatible")
    try:
        content = target_path.read_bytes()
    except OSError:
        return _unavailable(checker_id, "unreadable-input")
    if len(content) > MAX_FILING_BYTES:
        return _unavailable(checker_id, "unreadable-input")
    try:
        document = json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return _unavailable(checker_id, "malformed-input")
    try:
        contract = _contract()
        findings = _complaint_findings(document, contract, target)
        if context is not None:
            findings.extend(_integrity_findings(document, context, target))
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return _unavailable(checker_id, "unavailable-execution")
    findings = sorted(findings, key=lambda finding: finding["finding_id"])
    status = "failed" if findings else "passed"
    report = {
        "schema_version": 1,
        "checker_id": checker_id,
        "status": status,
        "target": target,
        "target_sha256": hashlib.sha256(content).hexdigest(),
        "authority_role": "verified-authority",
        "findings": findings,
    }
    return {
        "status": status,
        "checker_id": checker_id,
        "findings": findings,
        "report_bytes": _bytes(report),
    }
