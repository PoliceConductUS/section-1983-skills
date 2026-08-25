"""Folder-native verified-authority loading and audit host."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from scripts.skill_output_writer import OutputError, OutputRun
from scripts.validate_folder_invocation import (
    InvocationError,
    ValidatedInvocation,
    build_input_manifest,
)


_ROLES = ("filing-source", "verified-authority")
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_YAML_KEY = re.compile(r"^[a-z][a-z0-9_]*$")
_CORPUS_FIELDS = frozenset({"schema_version", "corpus_id", "authorities"})
_SOURCE_FIELDS = frozenset(
    {
        "schema_version",
        "source_id",
        "path",
        "sha256",
        "checked_through",
        "retrieved_from",
    }
)
_AUTHORITY_FIELDS = frozenset(
    {
        "schema_version",
        "authority_id",
        "citation",
        "document_path",
        "source_yaml_path",
        "sha256",
        "court",
        "decision_date",
        "publication_status",
        "precedential_status",
        "binding_status",
        "event_date_status",
        "later_history_status",
        "rule_of_orderliness_status",
        "proposition",
        "quotation",
        "pinpoint",
        "text_layer_status",
    }
)
_MAX_DOCUMENTATION_BYTES = 65_536
_RUN_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$")
_CITE_TAG = re.compile(r"<cite\b(?P<attributes>[^>]*)>(?P<text>.*?)</cite>", re.DOTALL)
_CITE_ATTRIBUTE = re.compile(r'([a-z][a-z0-9_-]*)="([^"]+)"')
_PAGE_MARKER = re.compile(r"(?m)^\[page (?P<pinpoint>[^\]\r\n]+)\][ \t]*$")
_UNAVAILABLE_CODES = frozenset(
    {
        "authority-content-unavailable",
        "authority-documentation-unavailable",
        "corpus-documentation-unavailable",
        "eyecite-unavailable",
        "output-publication-failed",
    }
)


class AuthorityAuditError(ValueError):
    """A bounded authority-audit input or host failure."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code
        self.exit_class = "unavailable" if code in _UNAVAILABLE_CODES else "invalid"


def _fail(code: str) -> None:
    raise AuthorityAuditError(code)


@dataclass(frozen=True)
class SourceDocumentation:
    source_id: str
    path: str
    sha256: str
    checked_through: str
    retrieved_from: str
    yaml_path: str
    yaml_sha256: str


@dataclass(frozen=True)
class AuthorityRecord:
    authority_id: str
    citation: str
    document_path: str
    source: SourceDocumentation
    sha256: str
    court: str
    decision_date: str
    publication_status: str
    precedential_status: str
    binding_status: str
    event_date_status: str
    later_history_status: str
    rule_of_orderliness_status: str
    proposition: str
    quotation: str
    pinpoint: str
    text_layer_status: str
    yaml_path: str
    yaml_sha256: str
    document_bytes: bytes


@dataclass(frozen=True)
class AuthorityCorpus:
    corpus_id: str
    authorities: tuple[AuthorityRecord, ...]
    yaml_path: str
    yaml_sha256: str


@dataclass(frozen=True)
class AuthorityAuditResult:
    status: str
    exit_class: str
    findings: tuple[dict[str, Any], ...]


def _scalar(raw: str, code: str) -> str:
    value = raw.strip()
    if not value:
        _fail(code)
    if value.startswith('"'):
        try:
            decoded = json.loads(value)
        except (ValueError, json.JSONDecodeError):
            _fail(code)
        if not isinstance(decoded, str) or not decoded:
            _fail(code)
        return decoded
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            _fail(code)
        decoded = value[1:-1].replace("''", "'")
        if not decoded:
            _fail(code)
        return decoded
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    if not value or any(character in value for character in "{}[]&*!|>"):
        _fail(code)
    return value


def _read(path: Path, maximum: int, code: str) -> bytes:
    try:
        size = path.stat().st_size
        if size < 1 or size > maximum:
            _fail(code)
        contents = path.read_bytes()
    except AuthorityAuditError:
        raise
    except OSError:
        _fail(code)
    if len(contents) != size:
        _fail(code)
    return contents


def _required_path(
    invocation: ValidatedInvocation, relative_path: str, *, missing_code: str
) -> Path:
    if not isinstance(relative_path, str) or not relative_path:
        _fail("invalid-authority-documentation")
    parts = relative_path.split("/")
    if (
        "\\" in relative_path
        or "\x00" in relative_path
        or re.match(r"^[A-Za-z]:/", relative_path) is not None
        or any(part in {"", ".", ".."} for part in parts)
    ):
        _fail("invalid-authority-documentation")
    roots = dict(invocation.inputs)
    root = roots["verified-authority"]
    candidate = root
    try:
        for part in parts:
            candidate = candidate / part
            if candidate.is_symlink():
                _fail("invalid-authority-documentation")
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except AuthorityAuditError:
        raise
    except FileNotFoundError:
        _fail(missing_code)
    except (OSError, ValueError):
        _fail("invalid-authority-documentation")
    return resolved


def _flat_yaml(contents: bytes, expected: frozenset[str], code: str) -> dict[str, str]:
    if not contents or len(contents) > _MAX_DOCUMENTATION_BYTES:
        _fail(code)
    try:
        text = contents.decode("utf-8", errors="strict")
    except UnicodeError:
        _fail(code)
    values: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line != line.lstrip() or ":" not in line:
            _fail(code)
        key, raw = line.split(":", 1)
        if _YAML_KEY.fullmatch(key) is None or key in values:
            _fail(code)
        values[key] = _scalar(raw, code)
    if set(values) != expected or values["schema_version"] != "1":
        _fail(code)
    return values


def _corpus_yaml(contents: bytes) -> tuple[str, tuple[str, ...]]:
    code = "invalid-corpus-documentation"
    if not contents or len(contents) > _MAX_DOCUMENTATION_BYTES:
        _fail(code)
    try:
        lines = contents.decode("utf-8", errors="strict").splitlines()
    except UnicodeError:
        _fail(code)
    values: dict[str, Any] = {}
    authority_paths: list[str] = []
    in_authorities = False
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - "):
            if not in_authorities:
                _fail(code)
            authority_paths.append(_scalar(line[4:], code))
            continue
        if line != line.lstrip() or ":" not in line:
            _fail(code)
        key, raw = line.split(":", 1)
        if _YAML_KEY.fullmatch(key) is None or key in values:
            _fail(code)
        if key == "authorities":
            if raw.strip():
                _fail(code)
            values[key] = authority_paths
            in_authorities = True
        else:
            if in_authorities:
                _fail(code)
            values[key] = _scalar(raw, code)
    if (
        set(values) != _CORPUS_FIELDS
        or values["schema_version"] != "1"
        or _IDENTIFIER.fullmatch(values["corpus_id"]) is None
        or not authority_paths
        or len(authority_paths) != len(set(authority_paths))
    ):
        _fail(code)
    return values["corpus_id"], tuple(authority_paths)


def _iso_date(value: str, code: str) -> None:
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        _fail(code)
    if parsed.isoformat() != value:
        _fail(code)


def _load_source(
    invocation: ValidatedInvocation, source_yaml_path: str
) -> SourceDocumentation:
    path = _required_path(
        invocation,
        source_yaml_path,
        missing_code="authority-documentation-unavailable",
    )
    contents = _read(path, _MAX_DOCUMENTATION_BYTES, "invalid-source-documentation")
    values = _flat_yaml(contents, _SOURCE_FIELDS, "invalid-source-documentation")
    if (
        _IDENTIFIER.fullmatch(values["source_id"]) is None
        or _SHA256.fullmatch(values["sha256"]) is None
        or not values["retrieved_from"].startswith(("https://", "http://"))
    ):
        _fail("invalid-source-documentation")
    _iso_date(values["checked_through"], "invalid-source-documentation")
    return SourceDocumentation(
        source_id=values["source_id"],
        path=values["path"],
        sha256=values["sha256"],
        checked_through=values["checked_through"],
        retrieved_from=values["retrieved_from"],
        yaml_path=source_yaml_path,
        yaml_sha256=hashlib.sha256(contents).hexdigest(),
    )


def _load_authority(
    invocation: ValidatedInvocation, authority_yaml_path: str
) -> AuthorityRecord:
    yaml_path = _required_path(
        invocation,
        authority_yaml_path,
        missing_code="authority-documentation-unavailable",
    )
    yaml_bytes = _read(
        yaml_path, _MAX_DOCUMENTATION_BYTES, "invalid-authority-documentation"
    )
    values = _flat_yaml(
        yaml_bytes, _AUTHORITY_FIELDS, "invalid-authority-documentation"
    )
    source = _load_source(invocation, values["source_yaml_path"])
    document_path = _required_path(
        invocation,
        values["document_path"],
        missing_code="authority-content-unavailable",
    )
    if not document_path.is_file():
        _fail("invalid-authority-documentation")
    document_bytes = _read(
        document_path,
        invocation.runtime["max_input_bytes"],
        "invalid-authority-documentation",
    )
    digest = hashlib.sha256(document_bytes).hexdigest()
    if digest != values["sha256"] or digest != source.sha256:
        _fail("authority-content-mismatch")
    if source.path != values["document_path"]:
        _fail("invalid-authority-documentation")
    _iso_date(values["decision_date"], "invalid-authority-documentation")
    if (
        _IDENTIFIER.fullmatch(values["authority_id"]) is None
        or _SHA256.fullmatch(values["sha256"]) is None
        or values["publication_status"] not in {"published", "unpublished"}
        or values["precedential_status"]
        not in {"precedential", "nonprecedential", "unknown"}
        or values["binding_status"] not in {"binding", "persuasive", "nonbinding"}
        or values["event_date_status"] not in {"pre-event", "post-event", "unknown"}
        or values["later_history_status"] not in {"checked", "stale", "unknown"}
        or values["rule_of_orderliness_status"]
        not in {"checked", "not-applicable", "unknown"}
        or values["text_layer_status"] not in {"usable", "unusable"}
    ):
        _fail("invalid-authority-documentation")
    return AuthorityRecord(
        authority_id=values["authority_id"],
        citation=values["citation"],
        document_path=values["document_path"],
        source=source,
        sha256=values["sha256"],
        court=values["court"],
        decision_date=values["decision_date"],
        publication_status=values["publication_status"],
        precedential_status=values["precedential_status"],
        binding_status=values["binding_status"],
        event_date_status=values["event_date_status"],
        later_history_status=values["later_history_status"],
        rule_of_orderliness_status=values["rule_of_orderliness_status"],
        proposition=values["proposition"],
        quotation=values["quotation"],
        pinpoint=values["pinpoint"],
        text_layer_status=values["text_layer_status"],
        yaml_path=authority_yaml_path,
        yaml_sha256=hashlib.sha256(yaml_bytes).hexdigest(),
        document_bytes=document_bytes,
    )


def load_verified_authority_corpus(
    invocation: ValidatedInvocation, corpus_documentation_path: str
) -> AuthorityCorpus:
    """Load one selected corpus YAML and its exact authority bytes."""

    if (
        not isinstance(invocation, ValidatedInvocation)
        or tuple(role for role, _root in invocation.inputs) != _ROLES
        or invocation.operation != "audit"
        or invocation.internet != "disabled"
        or invocation.target is None
        or invocation.target[0] != "filing-source"
    ):
        _fail("invalid-authority-audit-invocation")
    corpus_path = _required_path(
        invocation,
        corpus_documentation_path,
        missing_code="corpus-documentation-unavailable",
    )
    corpus_bytes = _read(
        corpus_path, _MAX_DOCUMENTATION_BYTES, "invalid-corpus-documentation"
    )
    corpus_id, authority_paths = _corpus_yaml(corpus_bytes)
    authorities = tuple(
        _load_authority(invocation, authority_path)
        for authority_path in authority_paths
    )
    if (
        len({authority.authority_id for authority in authorities}) != len(authorities)
        or len({authority.citation for authority in authorities}) != len(authorities)
    ):
        _fail("invalid-corpus-documentation")
    return AuthorityCorpus(
        corpus_id=corpus_id,
        authorities=authorities,
        yaml_path=corpus_documentation_path,
        yaml_sha256=hashlib.sha256(corpus_bytes).hexdigest(),
    )


def extract_eyecite_candidates(text: str) -> tuple[dict[str, Any], ...]:
    """Extract citation candidates and antecedents without verifying them."""

    if not isinstance(text, str):
        _fail("invalid-filing-content")
    try:
        from eyecite import get_citations, resolve_citations
    except (ImportError, OSError):
        _fail("eyecite-unavailable")
    try:
        citations = list(get_citations(text))
        resources = resolve_citations(citations)
    except Exception:
        _fail("eyecite-unavailable")
    resolved: dict[int, str] = {}
    for resource, resource_citations in resources.items():
        canonical = resource.citation.matched_text()
        for citation in resource_citations:
            resolved[id(citation)] = canonical
    kinds = {
        "FullCaseCitation": "full",
        "ShortCaseCitation": "short",
        "IdCitation": "id",
        "SupraCitation": "supra",
    }
    candidates = []
    for index, citation in enumerate(citations):
        class_name = type(citation).__name__
        if class_name not in kinds:
            continue
        start, end = citation.span()
        candidates.append(
            {
                "candidate_id": f"citation-{index + 1:04d}",
                "kind": kinds[class_name],
                "matched_text": citation.matched_text(),
                "resolved_citation": resolved.get(id(citation)),
                "span": {"start": start, "end": end},
            }
        )
    return tuple(candidates)


def _finding(
    check_id: str, location: str, message: str, *, authority_id: str | None = None
) -> dict[str, Any]:
    identity = hashlib.sha256(
        f"{check_id}\0{location}\0{message}\0{authority_id or ''}".encode("utf-8")
    ).hexdigest()[:16]
    finding = {
        "finding_id": f"{check_id}-{identity}",
        "check_id": check_id,
        "severity": "hard",
        "location": location,
        "message": message,
    }
    if authority_id is not None:
        finding["authority_id"] = authority_id
    return finding


def _persistent_markup_findings(
    filing_text: str, authorities: dict[str, AuthorityRecord]
) -> list[dict[str, Any]]:
    findings = []
    seen_ids: set[str] = set()
    for index, match in enumerate(_CITE_TAG.finditer(filing_text)):
        attributes = dict(_CITE_ATTRIBUTE.findall(match.group("attributes")))
        location = f"persistent_citations[{index}]"
        citation_id = attributes.get("id")
        authority_id = attributes.get("authority")
        if (
            set(attributes) != {"id", "authority"}
            or citation_id is None
            or _IDENTIFIER.fullmatch(citation_id) is None
            or citation_id in seen_ids
        ):
            findings.append(
                _finding(
                    "persistent-citation-id",
                    location,
                    "citation markup requires one unique stable ID",
                )
            )
        else:
            seen_ids.add(citation_id)
        if authority_id not in authorities:
            findings.append(
                _finding(
                    "persistent-authority-target",
                    location,
                    "citation markup authority is not selected",
                    authority_id=authority_id,
                )
            )
    return findings


def _pinpoint_segment(opinion_text: str, pinpoint: str) -> str | None:
    markers = list(_PAGE_MARKER.finditer(opinion_text))
    for index, marker in enumerate(markers):
        if marker.group("pinpoint") != pinpoint:
            continue
        start = marker.end()
        end = markers[index + 1].start() if index + 1 < len(markers) else len(opinion_text)
        return opinion_text[start:end]
    return None


def _audit_findings(
    filing_text: str,
    candidates: tuple[dict[str, Any], ...],
    corpus: AuthorityCorpus,
) -> list[dict[str, Any]]:
    authorities_by_id = {
        authority.authority_id: authority for authority in corpus.authorities
    }
    authorities_by_citation = {
        authority.citation: authority for authority in corpus.authorities
    }
    findings = _persistent_markup_findings(filing_text, authorities_by_id)
    resolved_citations = {
        candidate["resolved_citation"]
        for candidate in candidates
        if candidate["resolved_citation"] is not None
    }
    unresolved = [
        candidate
        for candidate in candidates
        if candidate["kind"] in {"short", "id", "supra"}
        and candidate["resolved_citation"] is None
    ]
    for candidate in unresolved:
        findings.append(
            _finding(
                "unresolved-antecedent",
                candidate["candidate_id"],
                "short-form citation antecedent did not resolve",
            )
        )
    for citation in sorted(resolved_citations):
        if citation not in authorities_by_citation:
            findings.append(
                _finding(
                    "missing-authority",
                    citation,
                    "extracted citation is absent from the selected authority corpus",
                )
            )
    for authority in corpus.authorities:
        if authority.text_layer_status == "unusable":
            findings.append(
                _finding(
                    "visual-review-required",
                    authority.document_path,
                    "authority text layer is unusable and requires visual review",
                    authority_id=authority.authority_id,
                )
            )
            continue
        try:
            opinion_text = authority.document_bytes.decode("utf-8", errors="strict")
        except UnicodeError:
            findings.append(
                _finding(
                    "visual-review-required",
                    authority.document_path,
                    "authority bytes do not provide a usable UTF-8 text layer",
                    authority_id=authority.authority_id,
                )
            )
            continue
        quotation_present = authority.quotation in opinion_text
        if not quotation_present:
            findings.append(
                _finding(
                    "quotation-not-found",
                    authority.document_path,
                    "asserted quotation is absent from the exact authority document",
                    authority_id=authority.authority_id,
                )
            )
        pinpoint_segment = _pinpoint_segment(opinion_text, authority.pinpoint)
        if pinpoint_segment is None:
            findings.append(
                _finding(
                    "pinpoint-not-found",
                    authority.document_path,
                    "asserted pinpoint is absent from the usable authority text",
                    authority_id=authority.authority_id,
                )
            )
        elif quotation_present and authority.quotation not in pinpoint_segment:
            findings.append(
                _finding(
                    "quotation-pinpoint-mismatch",
                    authority.document_path,
                    "asserted quotation occurs outside the asserted pinpoint",
                    authority_id=authority.authority_id,
                )
            )
        if (
            authority.later_history_status != "checked"
            or authority.rule_of_orderliness_status == "unknown"
            or authority.event_date_status == "unknown"
            or authority.precedential_status == "unknown"
        ):
            findings.append(
                _finding(
                    "authority-status-unresolved",
                    authority.yaml_path,
                    "required authority status remains stale or unknown",
                    authority_id=authority.authority_id,
                )
            )
    return sorted(findings, key=lambda finding: finding["finding_id"])


def _canonical_json(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _markdown(report: dict[str, Any]) -> bytes:
    lines = [
        "# Authority audit findings",
        "",
        f"Status: {report['status']}",
        f"Corpus: {report['corpus_id']}",
        "",
    ]
    if not report["findings"]:
        lines.append("No deterministic authority findings.")
    else:
        for finding in report["findings"]:
            lines.extend(
                (
                    f"## {finding['finding_id']}",
                    "",
                    f"- Check: {finding['check_id']}",
                    f"- Severity: {finding['severity']}",
                    f"- Location: {finding['location']}",
                    f"- Message: {finding['message']}",
                    "",
                )
            )
    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def _yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _receipt(corpus: AuthorityCorpus, status: str) -> bytes:
    lines = [
        "schema_version: 1",
        f"status: {_yaml_string(status)}",
        f"corpus_id: {_yaml_string(corpus.corpus_id)}",
        f"corpus_yaml_path: {_yaml_string(corpus.yaml_path)}",
        f"corpus_yaml_sha256: {_yaml_string(corpus.yaml_sha256)}",
        "authorities:",
    ]
    for authority in corpus.authorities:
        lines.extend(
            (
                f"  - authority_id: {_yaml_string(authority.authority_id)}",
                f"    citation: {_yaml_string(authority.citation)}",
                f"    document_path: {_yaml_string(authority.document_path)}",
                f"    sha256: {_yaml_string(authority.sha256)}",
                f"    authority_yaml_path: {_yaml_string(authority.yaml_path)}",
                f"    authority_yaml_sha256: {_yaml_string(authority.yaml_sha256)}",
                f"    source_id: {_yaml_string(authority.source.source_id)}",
                f"    source_yaml_path: {_yaml_string(authority.source.yaml_path)}",
                f"    source_yaml_sha256: {_yaml_string(authority.source.yaml_sha256)}",
                f"    checked_through: {_yaml_string(authority.source.checked_through)}",
            )
        )
    return ("\n".join(lines) + "\n").encode("utf-8")


def run_and_publish_authority_audit(
    *,
    invocation: ValidatedInvocation,
    corpus_documentation_path: str,
    run_id: str,
    skill_version: str,
) -> AuthorityAuditResult:
    """Run one deterministic offline authority audit and publish its reports."""

    if (
        _RUN_ID.fullmatch(run_id or "") is None
        or _VERSION.fullmatch(skill_version or "") is None
    ):
        _fail("invalid-authority-audit-invocation")
    corpus = load_verified_authority_corpus(
        invocation, corpus_documentation_path
    )
    try:
        target_path = invocation.target[1]
        filing_bytes = _read(
            target_path,
            invocation.runtime["max_input_bytes"],
            "invalid-filing-content",
        )
        filing_text = filing_bytes.decode("utf-8", errors="strict")
    except AuthorityAuditError:
        raise
    except (AttributeError, IndexError, UnicodeError):
        _fail("invalid-filing-content")
    candidates = extract_eyecite_candidates(filing_text)
    findings = _audit_findings(filing_text, candidates, corpus)
    status = "failed" if findings else "passed"
    exit_class = "findings" if findings else "passed"
    report = {
        "schema_version": 1,
        "status": status,
        "corpus_id": corpus.corpus_id,
        "target": target_path.name,
        "target_sha256": hashlib.sha256(filing_bytes).hexdigest(),
        "candidates": list(candidates),
        "findings": findings,
    }
    report_bytes = _canonical_json(report)
    try:
        output = OutputRun.start(
            invocation,
            run_id=run_id,
            skill_version=skill_version,
            mode="append-immutable",
            input_manifest=build_input_manifest(invocation),
        )
        output.write("reports/authority-audit.json", report_bytes)
        output.write("reports/authority-audit.md", _markdown(report))
        output.write("run-receipt.yaml", _receipt(corpus, exit_class))
        output.complete()
    except (OutputError, InvocationError, OSError, ValueError):
        _fail("output-publication-failed")
    return AuthorityAuditResult(
        status=status,
        exit_class=exit_class,
        findings=tuple(findings),
    )
