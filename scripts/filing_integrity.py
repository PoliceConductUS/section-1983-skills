"""Folder-native trusted host for the installed Filing CI checker."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from types import ModuleType
from typing import Any

from scripts.skill_output_writer import OutputError, OutputRun
from scripts.validate_folder_invocation import (
    InvocationError,
    ValidatedInvocation,
    build_input_manifest,
    resolve_input_path,
)


_REPOSITORY = Path(__file__).resolve().parents[1]
_CHECKER = _REPOSITORY / "skills" / "filing-ci" / "scripts" / "run_filing_ci.py"
_ROLES = (
    "filing-source",
    "filing-index",
    "record-reference",
    "exhibit",
    "docket-to-appendix",
    "verified-authority",
)
_SOURCE_FIELDS = {
    "schema_version",
    "source_id",
    "source_role",
    "path",
    "sha256",
    "checked_through",
    "classification",
    "validation_status",
}
_SOURCE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_ROLE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_CLASSIFICATION = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_YAML_KEY = re.compile(r"^[a-z][a-z0-9_]*$")
_RUN_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$")
_MAX_SOURCE_DOCUMENT_BYTES = 65_536
_MAX_SELECTIONS = 64
_UNAVAILABLE_CODES = frozenset(
    {
        "checker-unavailable",
        "output-publication-failed",
        "source-content-unavailable",
        "source-documentation-unavailable",
    }
)


class FilingIntegrityError(ValueError):
    """A bounded filing-integrity host failure."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code
        self.exit_class = "unavailable" if code in _UNAVAILABLE_CODES else "invalid"


def _fail(code: str) -> None:
    raise FilingIntegrityError(code)


@dataclass(frozen=True)
class FilingIntegritySelection:
    checker_id: str
    filing_documentation_path: str
    record_documentation_paths: tuple[str, ...]
    exhibit_documentation_paths: tuple[str, ...]
    docket_documentation_path: str
    authority_documentation_paths: tuple[str, ...]


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    source_role: str
    content_path: str
    content_sha256: str
    checked_through: str
    classification: str
    documentation_role: str
    documentation_path: str
    documentation_sha256: str


@dataclass(frozen=True)
class FilingIntegrityResult:
    status: str
    exit_class: str
    findings: tuple[dict[str, Any], ...]


def _yaml_scalar(raw: str) -> str:
    value = raw.strip()
    if not value:
        _fail("invalid-source-documentation")
    if value.startswith('"'):
        try:
            decoded = json.loads(value)
        except (ValueError, json.JSONDecodeError):
            _fail("invalid-source-documentation")
        if not isinstance(decoded, str) or not decoded:
            _fail("invalid-source-documentation")
        return decoded
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            _fail("invalid-source-documentation")
        decoded = value[1:-1].replace("''", "'")
        if not decoded:
            _fail("invalid-source-documentation")
        return decoded
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    if not value or any(character in value for character in "{}[]&*!|>"):
        _fail("invalid-source-documentation")
    return value


def _parse_source_yaml(contents: bytes) -> dict[str, str]:
    if not contents or len(contents) > _MAX_SOURCE_DOCUMENT_BYTES:
        _fail("invalid-source-documentation")
    try:
        text = contents.decode("utf-8", errors="strict")
    except UnicodeError:
        _fail("invalid-source-documentation")
    values: dict[str, str] = {}
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line != raw_line.lstrip() or ":" not in raw_line:
            _fail("invalid-source-documentation")
        key, raw_value = raw_line.split(":", 1)
        if _YAML_KEY.fullmatch(key) is None or key in values:
            _fail("invalid-source-documentation")
        values[key] = _yaml_scalar(raw_value)
    if set(values) != _SOURCE_FIELDS or values["schema_version"] != "1":
        _fail("invalid-source-documentation")
    return values


def _read(path: Path, maximum: int, code: str) -> bytes:
    try:
        size = path.stat().st_size
        if size < 1 or size > maximum:
            _fail(code)
        contents = path.read_bytes()
    except FilingIntegrityError:
        raise
    except OSError:
        _fail(code)
    if len(contents) != size:
        _fail(code)
    return contents


def _date(value: str) -> None:
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        _fail("invalid-source-documentation")


def _required_input_path(
    invocation: ValidatedInvocation,
    role: str,
    relative_path: str,
    *,
    missing_code: str,
) -> Path:
    if not isinstance(relative_path, str) or not relative_path:
        _fail("invalid-source-documentation")
    segments = relative_path.split("/")
    if (
        "\\" in relative_path
        or "\x00" in relative_path
        or re.match(r"^[A-Za-z]:/", relative_path) is not None
        or any(segment in {"", ".", ".."} for segment in segments)
    ):
        _fail("invalid-source-documentation")
    roots = dict(invocation.inputs)
    root = roots.get(role)
    if root is None:
        _fail("invalid-source-documentation")
    candidate = root
    try:
        for segment in segments:
            candidate = candidate / segment
            if candidate.is_symlink():
                _fail("invalid-source-documentation")
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except FilingIntegrityError:
        raise
    except FileNotFoundError:
        _fail(missing_code)
    except (OSError, ValueError):
        _fail("invalid-source-documentation")
    return resolved
    if parsed.isoformat() != value:
        _fail("invalid-source-documentation")


def _load_source_record(
    invocation: ValidatedInvocation,
    *,
    documentation_role: str,
    documentation_path: str,
) -> SourceRecord:
    try:
        document_path = _required_input_path(
            invocation,
            documentation_role,
            documentation_path,
            missing_code="source-documentation-unavailable",
        )
        if not document_path.is_file():
            _fail("invalid-source-documentation")
        document_bytes = _read(
            document_path,
            _MAX_SOURCE_DOCUMENT_BYTES,
            "invalid-source-documentation",
        )
        values = _parse_source_yaml(document_bytes)
        if (
            _SOURCE_ID.fullmatch(values["source_id"]) is None
            or values["source_role"] not in _ROLES
            or _ROLE.fullmatch(values["source_role"]) is None
            or _SHA256.fullmatch(values["sha256"]) is None
            or _CLASSIFICATION.fullmatch(values["classification"]) is None
            or values["validation_status"] != "passed"
        ):
            _fail("invalid-source-documentation")
        _date(values["checked_through"])
        content_path = _required_input_path(
            invocation,
            values["source_role"],
            values["path"],
            missing_code="source-content-unavailable",
        )
        if not content_path.is_file():
            _fail("invalid-source-documentation")
        content = _read(
            content_path,
            invocation.runtime["max_input_bytes"],
            "invalid-source-documentation",
        )
    except FilingIntegrityError:
        raise
    except (InvocationError, OSError, ValueError):
        _fail("invalid-source-documentation")
    if hashlib.sha256(content).hexdigest() != values["sha256"]:
        _fail("source-content-mismatch")
    return SourceRecord(
        source_id=values["source_id"],
        source_role=values["source_role"],
        content_path=values["path"],
        content_sha256=values["sha256"],
        checked_through=values["checked_through"],
        classification=values["classification"],
        documentation_role=documentation_role,
        documentation_path=documentation_path,
        documentation_sha256=hashlib.sha256(document_bytes).hexdigest(),
    )


def _validate_selection(value: Any) -> FilingIntegritySelection:
    if not isinstance(value, FilingIntegritySelection):
        _fail("invalid-filing-integrity-selection")
    path_groups = (
        (value.filing_documentation_path,),
        value.record_documentation_paths,
        value.exhibit_documentation_paths,
        (value.docket_documentation_path,),
        value.authority_documentation_paths,
    )
    if (
        value.checker_id != "section-1983-complaint-v1"
        or any(type(group) is not tuple or not group for group in path_groups)
        or sum(len(group) for group in path_groups) > _MAX_SELECTIONS
        or any(
            not isinstance(path, str) or not path
            for group in path_groups
            for path in group
        )
    ):
        _fail("invalid-filing-integrity-selection")
    return value


def _load_records(
    invocation: ValidatedInvocation,
    selection: FilingIntegritySelection,
) -> tuple[SourceRecord, ...]:
    entries = [
        (
            "filing-index",
            selection.filing_documentation_path,
            "filing-source",
            "filing",
        ),
        *(
            ("record-reference", path, "record-reference", "record")
            for path in selection.record_documentation_paths
        ),
        *(
            ("exhibit", path, "exhibit", "exhibit")
            for path in selection.exhibit_documentation_paths
        ),
        (
            "docket-to-appendix",
            selection.docket_documentation_path,
            "docket-to-appendix",
            "docket-to-appendix",
        ),
        *(
            ("verified-authority", path, "verified-authority", "authority")
            for path in selection.authority_documentation_paths
        ),
    ]
    records = tuple(
        _load_source_record(
            invocation,
            documentation_role=role,
            documentation_path=path,
        )
        for role, path, _source_role, _classification in entries
    )
    if any(
        record.source_role != source_role
        or record.classification != classification
        for record, (_role, _path, source_role, classification) in zip(
            records, entries, strict=True
        )
    ):
        _fail("invalid-source-documentation")
    identities = {(record.source_id, record.source_role) for record in records}
    if len(identities) != len(records):
        _fail("invalid-source-documentation")
    filing_records = [
        record for record in records if record.classification == "filing"
    ]
    if len(filing_records) != 1 or invocation.target is None:
        _fail("invalid-filing-target")
    filing = filing_records[0]
    try:
        documented_target = resolve_input_path(
            invocation, filing.source_role, filing.content_path
        )
    except InvocationError:
        _fail("invalid-filing-target")
    if (
        invocation.target[0] != "filing-source"
        or filing.source_role != "filing-source"
        or documented_target != invocation.target[1]
    ):
        _fail("invalid-filing-target")
    return records


def _load_checker() -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        "_section_1983_installed_filing_checker", _CHECKER
    )
    if specification is None or specification.loader is None:
        _fail("checker-unavailable")
    module = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(module)
    except (ImportError, OSError, SyntaxError):
        _fail("checker-unavailable")
    return module


def _checker_context(
    invocation: ValidatedInvocation, records: tuple[SourceRecord, ...]
) -> dict[str, Any]:
    docket_records = [
        record for record in records if record.classification == "docket-to-appendix"
    ]
    if len(docket_records) != 1:
        _fail("invalid-docket-index")
    docket_record = docket_records[0]
    try:
        docket_path = resolve_input_path(
            invocation, docket_record.source_role, docket_record.content_path
        )
        docket_value = json.loads(
            _read(
                docket_path,
                invocation.runtime["max_input_bytes"],
                "invalid-docket-index",
            ).decode("utf-8", errors="strict")
        )
    except FilingIntegrityError:
        raise
    except (InvocationError, UnicodeError, ValueError, json.JSONDecodeError):
        _fail("invalid-docket-index")
    if type(docket_value) is not dict or set(docket_value) != {"entries"}:
        _fail("invalid-docket-index")
    entries = docket_value["entries"]
    required = {
        "docket_entry",
        "docket_page",
        "appendix_start",
        "appendix_end",
        "source_id",
    }
    if type(entries) is not list:
        _fail("invalid-docket-index")
    normalized_entries = []
    for entry in entries:
        if (
            type(entry) is not dict
            or set(entry) != required
            or any(
                type(entry[key]) is not int or entry[key] < 1
                for key in (
                    "docket_entry",
                    "docket_page",
                    "appendix_start",
                    "appendix_end",
                )
            )
            or entry["appendix_end"] < entry["appendix_start"]
            or not isinstance(entry["source_id"], str)
            or _SOURCE_ID.fullmatch(entry["source_id"]) is None
        ):
            _fail("invalid-docket-index")
        normalized_entries.append(entry)
    return {
        "authority_ids": sorted(
            record.source_id
            for record in records
            if record.source_role == "verified-authority"
        ),
        "docket_entries": sorted(
            normalized_entries,
            key=lambda entry: (
                entry["docket_entry"],
                entry["docket_page"],
                entry["appendix_start"],
                entry["appendix_end"],
                entry["source_id"],
            ),
        ),
        "docket_ids": sorted(
            record.source_id
            for record in records
            if record.source_role == "docket-to-appendix"
        ),
        "exhibit_ids": sorted(
            record.source_id
            for record in records
            if record.source_role == "exhibit"
        ),
        "record_ids": sorted(
            record.source_id
            for record in records
            if record.source_role == "record-reference"
        ),
    }


def _markdown(report: dict[str, Any]) -> bytes:
    lines = [
        "# Filing integrity findings",
        "",
        f"Status: {report['status']}",
        f"Checker: {report['checker_id']}",
        "",
    ]
    findings = report.get("findings", [])
    if not findings:
        lines.append("No deterministic mechanical findings.")
    else:
        for finding in findings:
            lines.extend(
                (
                    f"## {finding['finding_id']}",
                    "",
                    f"- Severity: {finding['severity']}",
                    f"- Location: {finding['location']}",
                    f"- Message: {finding['message']}",
                    "",
                )
            )
    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def _yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _receipt(
    records: tuple[SourceRecord, ...],
    *,
    status: str,
    checker_id: str,
) -> bytes:
    lines = [
        "schema_version: 1",
        f"checker_id: {_yaml_string(checker_id)}",
        f"status: {_yaml_string(status)}",
        "selected_sources:",
    ]
    for record in sorted(records, key=lambda item: (item.source_role, item.source_id)):
        lines.extend(
            (
                f"  - source_id: {_yaml_string(record.source_id)}",
                f"    role: {_yaml_string(record.source_role)}",
                f"    path: {_yaml_string(record.content_path)}",
                f"    sha256: {_yaml_string(record.content_sha256)}",
                f"    checked_through: {_yaml_string(record.checked_through)}",
                f"    source_yaml_role: {_yaml_string(record.documentation_role)}",
                f"    source_yaml_path: {_yaml_string(record.documentation_path)}",
                f"    source_yaml_sha256: {_yaml_string(record.documentation_sha256)}",
            )
        )
    return ("\n".join(lines) + "\n").encode("utf-8")


def run_and_publish_filing_integrity(
    *,
    invocation: ValidatedInvocation,
    selection: FilingIntegritySelection,
    run_id: str,
    skill_version: str,
) -> FilingIntegrityResult:
    """Validate selected folders, run the installed checker, and publish output."""

    if (
        not isinstance(invocation, ValidatedInvocation)
        or tuple(role for role, _root in invocation.inputs) != _ROLES
        or invocation.internet != "disabled"
        or _RUN_ID.fullmatch(run_id or "") is None
        or _VERSION.fullmatch(skill_version or "") is None
    ):
        _fail("invalid-filing-integrity-invocation")
    selection = _validate_selection(selection)
    records = _load_records(invocation, selection)
    filing = next(record for record in records if record.classification == "filing")
    checker = _load_checker()
    roots = dict(invocation.inputs)
    context = _checker_context(invocation, records)
    try:
        checker_result = checker.run_filing_ci(
            roots["filing-source"],
            filing.content_path,
            roots["verified-authority"],
            selection.checker_id,
            context,
        )
    except BaseException:
        _fail("checker-unavailable")
    if type(checker_result) is not dict or checker_result.get("status") not in {
        "passed",
        "failed",
        "unavailable",
    }:
        _fail("checker-output-invalid")
    try:
        report_bytes = checker_result["report_bytes"]
        report = json.loads(report_bytes.decode("utf-8", errors="strict"))
        findings = checker_result.get("findings", [])
    except (KeyError, UnicodeError, ValueError, json.JSONDecodeError):
        _fail("checker-output-invalid")
    if type(report_bytes) is not bytes or type(findings) is not list:
        _fail("checker-output-invalid")
    status = checker_result["status"]
    exit_class = {
        "passed": "passed",
        "failed": "findings",
        "unavailable": "unavailable",
    }[status]
    markdown = _markdown(report)
    try:
        output = OutputRun.start(
            invocation,
            run_id=run_id,
            skill_version=skill_version,
            mode="append-immutable",
            input_manifest=build_input_manifest(invocation),
        )
        output.write("reports/filing-integrity.json", report_bytes)
        output.write("reports/filing-integrity.md", markdown)
        output.write(
            "run-receipt.yaml",
            _receipt(
                records,
                status=exit_class,
                checker_id=selection.checker_id,
            ),
        )
        if exit_class in {"passed", "findings"}:
            output.complete()
        else:
            output.fail("checker-unavailable", "checker-execution")
    except (OutputError, InvocationError, OSError, ValueError):
        _fail("output-publication-failed")
    return FilingIntegrityResult(
        status=status,
        exit_class=exit_class,
        findings=tuple(findings),
    )
