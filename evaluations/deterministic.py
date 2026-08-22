import json
import re


CITATION_PATTERN = re.compile(r"\[cite:([A-Za-z0-9][A-Za-z0-9_.:-]*)\]")
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)


def _finding(identifier, fixture_id, location):
    return {"id": identifier, "fixture_id": fixture_id, "location": location}


def _has_field(value, address):
    current = value
    for segment in address.split("."):
        if not isinstance(current, dict) or segment not in current:
            return False
        current = current[segment]
    return True


def _candidate_forms(candidate):
    if isinstance(candidate, str):
        text = candidate
        try:
            structured = json.loads(candidate)
        except json.JSONDecodeError:
            structured = None
        return text, structured
    return json.dumps(candidate, sort_keys=True), candidate


def grade_candidate(fixture, candidate):
    fixture_id = fixture["id"]
    contract = fixture["deterministic"]
    text, structured = _candidate_forms(candidate)
    findings = []

    for address in contract.get("required_fields", []):
        if not _has_field(structured, address):
            findings.append(_finding("required-field-missing", fixture_id, address))

    headings = [match.group(1).strip() for match in HEADING_PATTERN.finditer(text)]
    previous_index = -1
    for required in contract.get("ordered_headings", []):
        try:
            index = headings.index(required)
        except ValueError:
            findings.append(_finding("heading-missing", fixture_id, required))
            continue
        if index < previous_index:
            findings.append(_finding("heading-out-of-order", fixture_id, required))
        previous_index = max(previous_index, index)

    folded_text = text.casefold()
    for rule in contract.get("banned_terms", []):
        if rule["term"].casefold() in folded_text:
            findings.append(_finding("banned-term", fixture_id, rule["id"]))
    for rule in contract.get("banned_patterns", []):
        if re.search(rule["pattern"], text):
            findings.append(_finding("banned-pattern", fixture_id, rule["id"]))

    observed_citations = set(CITATION_PATTERN.findall(text))
    for citation in contract.get("required_citations", []):
        if citation not in observed_citations:
            findings.append(_finding("citation-missing", fixture_id, citation))
    for citation in sorted(observed_citations - set(fixture.get("source_ids", []))):
        findings.append(_finding("citation-unknown", fixture_id, citation))

    return {
        "fixture_id": fixture_id,
        "passed": not findings,
        "pass_count": int(not findings),
        "finding_count": len(findings),
        "findings": findings,
    }
