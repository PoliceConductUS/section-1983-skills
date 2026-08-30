import hashlib
import json
from pathlib import Path, PurePosixPath


MAX_COMPLAINT_BYTES = 5 * 1024 * 1024


class ComplaintCheckError(Exception):
    def __init__(self, finding_id, message):
        super().__init__(message)
        self.finding_id = finding_id


def _contract_path():
    return Path(__file__).resolve().parents[1] / "references" / "complaint-structure-contract.json"


def _load_contract():
    try:
        contract = json.loads(_contract_path().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ComplaintCheckError("complaint-contract-unavailable", str(error)) from error
    if contract.get("owner") != "drafting-section-1983-complaints":
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
