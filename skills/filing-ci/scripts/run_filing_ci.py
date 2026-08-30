import hashlib
import json
from pathlib import Path, PurePosixPath


CHECKER_ID = "section-1983-complaint-v1"
REPORT_PATH = "reports/filing-ci.json"
MAX_FILING_BYTES = 5 * 1024 * 1024


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
        "artifact": REPORT_PATH,
        "report_bytes": _bytes(report),
    }


def _contract():
    path = Path(__file__).resolve().parents[1] / "references" / "packaged-complaint-checker.json"
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


def run_filing_ci(filing_root, filing_target, authorities_root, checker_id):
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
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return _unavailable(checker_id, "unavailable-execution")
    status = "failed" if findings else "passed"
    report = {
        "schema_version": 1,
        "checker_id": checker_id,
        "status": status,
        "target": target,
        "target_sha256": hashlib.sha256(content).hexdigest(),
        "authority_role": "authorities",
        "findings": findings,
    }
    return {
        "status": status,
        "checker_id": checker_id,
        "artifact": REPORT_PATH,
        "findings": findings,
        "report_bytes": _bytes(report),
    }
