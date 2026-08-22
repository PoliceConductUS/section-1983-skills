import argparse
import hashlib
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_TIMEOUT_SECONDS = 60
STREAM_LIMIT = 8192
PROVIDER_BODY_LIMIT = 1_000_000
TRUNCATION_MARKER = "[truncated]"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
SUPPORTED_FAMILIES = (
    "complaint or amended complaint",
    "motion-to-dismiss response",
    "summary-judgment response",
    "leave to amend",
    "extension motion",
    "R&R objection",
    "R&R response",
)
PACKET_KEYS = {
    "draft",
    "document_family",
    "sources",
    "skill",
    "checklist",
    "capabilities",
}
DRAFT_KEYS = {"content", "version", "sha256"}
SOURCE_KEYS = {"id", "role", "content", "sha256"}
EMBEDDED_TEXT_KEYS = {"content"}
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
STABLE_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
RUN_ID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
REPORT_HEADINGS = (
    "Fatal Defects",
    "Credible Opposition Arguments",
    "Factual Disputes",
    "Discovery Issues",
    "Style Complaints",
)
FINDING_KEYS = {
    "id",
    "attacked_quote",
    "location",
    "source_ids",
    "attack",
    "consequence",
    "status",
    "correction",
    "plaintiff_decision",
}
CORRECTION_KEYS = {"replace", "with"}
DECISION_KEYS = {"question", "choices"}
CHOICE_KEYS = {"option", "consequence"}


class PacketValidationError(ValueError):
    def __init__(self, finding_id, reason):
        super().__init__(f"{finding_id}: {reason}")
        self.finding_id = finding_id
        self.reason = reason


class ReviewLaunchError(RuntimeError):
    def __init__(self, finding_id, reason, stdout="", stderr=""):
        super().__init__(f"{finding_id}: {reason}")
        self.finding_id = finding_id
        self.reason = reason
        self.stdout = _bounded(stdout)
        self.stderr = _bounded(stderr)


def _text(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _bounded(value):
    text = _text(value)
    if len(text) <= STREAM_LIMIT:
        return text
    return text[: STREAM_LIMIT - len(TRUNCATION_MARKER)] + TRUNCATION_MARKER


def _packet_error(reason, finding_id="review-packet-invalid"):
    raise PacketValidationError(finding_id, reason)


def _exact_object(value, keys, label):
    if not isinstance(value, dict) or set(value) != keys:
        _packet_error(f"{label} must contain exactly {', '.join(sorted(keys))}")
    return value


def _nonempty_string(value, label):
    if not isinstance(value, str) or not value.strip():
        _packet_error(f"{label} must be a nonempty string")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        _packet_error(f"{label} must be valid UTF-8 text")
    return value


def _fingerprint(content, supplied, label):
    if not isinstance(supplied, str) or not SHA256_PATTERN.fullmatch(supplied):
        _packet_error(f"{label} sha256 must be a lowercase hexadecimal fingerprint")
    try:
        actual = hashlib.sha256(content.encode("utf-8")).hexdigest()
    except UnicodeEncodeError as error:
        _packet_error(f"{label} content must be valid UTF-8 text")
    if supplied != actual:
        _packet_error(
            f"{label} content does not match its sha256",
            "review-packet-fingerprint-mismatch",
        )


def validate_packet(packet):
    _exact_object(packet, PACKET_KEYS, "review packet")

    draft = _exact_object(packet["draft"], DRAFT_KEYS, "draft")
    draft_content = _nonempty_string(draft["content"], "draft content")
    _nonempty_string(draft["version"], "draft version")
    _fingerprint(draft_content, draft["sha256"], "draft")

    family = packet["document_family"]
    if family not in SUPPORTED_FAMILIES:
        _packet_error(
            f"unsupported document family: {family}",
            "unsupported-document-family",
        )

    sources = packet["sources"]
    if not isinstance(sources, list) or not sources:
        _packet_error("sources must be a nonempty list")
    source_ids = []
    for index, source_value in enumerate(sources):
        source = _exact_object(source_value, SOURCE_KEYS, f"source {index + 1}")
        source_id = _nonempty_string(source["id"], f"source {index + 1} id")
        if not STABLE_ID_PATTERN.fullmatch(source_id):
            _packet_error(f"source {index + 1} id must be a stable identifier")
        _nonempty_string(source["role"], f"source {source_id} role")
        content = _nonempty_string(source["content"], f"source {source_id} content")
        _fingerprint(content, source["sha256"], f"source {source_id}")
        source_ids.append(source_id)
    if len(source_ids) != len(set(source_ids)):
        _packet_error("source identifiers must be unique")

    for label in ("skill", "checklist"):
        embedded = _exact_object(packet[label], EMBEDDED_TEXT_KEYS, label)
        _nonempty_string(embedded["content"], f"{label} content")

    if packet["capabilities"] != []:
        _packet_error("reviewer capabilities must be empty")
    return packet


def _command(command):
    if not isinstance(command, list) or not command or not all(
        isinstance(argument, str) and argument for argument in command
    ):
        raise ValueError("reviewer command must be a nonempty JSON argument array")
    return command


def _positive_timeout(timeout_seconds):
    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, (int, float))
        or not math.isfinite(timeout_seconds)
        or timeout_seconds <= 0
    ):
        raise ValueError("timeout must be a finite positive number")
    return timeout_seconds


def _runtime_string(value, label, finding_id="independent-review-unavailable"):
    if not isinstance(value, str) or not value.strip():
        raise ReviewLaunchError(finding_id, f"{label} must be a nonempty string")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ReviewLaunchError(finding_id, f"{label} must be valid UTF-8 text") from error
    if "\r" in value or "\n" in value:
        raise ReviewLaunchError(finding_id, f"{label} must be a single line")
    return value


def _api_key(value):
    return _runtime_string(value, "OPENAI_API_KEY")


def _review_schema():
    nonempty_string = {"type": "string", "minLength": 1}
    correction = {
        "anyOf": [
            {"type": "null"},
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "replace": nonempty_string,
                    "with": nonempty_string,
                },
                "required": ["replace", "with"],
            },
        ]
    }
    decision = {
        "anyOf": [
            {"type": "null"},
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "question": nonempty_string,
                    "choices": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "option": nonempty_string,
                                "consequence": nonempty_string,
                            },
                            "required": ["option", "consequence"],
                        },
                    },
                },
                "required": ["question", "choices"],
            },
        ]
    }
    finding = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "id": nonempty_string,
            "attacked_quote": nonempty_string,
            "location": nonempty_string,
            "source_ids": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": nonempty_string,
            },
            "attack": nonempty_string,
            "consequence": nonempty_string,
            "status": nonempty_string,
            "correction": correction,
            "plaintiff_decision": decision,
        },
        "required": sorted(FINDING_KEYS),
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            heading: {"type": "array", "items": finding}
            for heading in REPORT_HEADINGS
        },
        "required": list(REPORT_HEADINGS),
    }


def _provider_request(packet, model):
    packet_text = json.dumps(
        packet,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return {
        "model": model,
        "instructions": (
            "Perform the independent adversarial filing review using only the "
            "validated packet. Apply the embedded public skill and checklist. "
            "Return only the required structured review."
        ),
        "input": [
            {
                "role": "user",
                "content": [{"type": "input_text", "text": packet_text}],
            }
        ],
        "tools": [],
        "tool_choice": "none",
        "store": False,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "adversarial_filing_review",
                "strict": True,
                "schema": _review_schema(),
            }
        },
    }


def _openai_transport(body, headers, timeout_seconds):
    request = urllib.request.Request(
        OPENAI_RESPONSES_URL,
        data=body,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return response.status, response.read(PROVIDER_BODY_LIMIT + 1)
    except urllib.error.HTTPError as error:
        return error.code, error.read(PROVIDER_BODY_LIMIT + 1)


def _review_string(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ReviewLaunchError(
            "review-response-invalid",
            f"{label} must be a nonempty string",
        )
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ReviewLaunchError(
            "review-response-invalid",
            f"{label} must be valid UTF-8 text",
        ) from error
    return value


def _exact_review_object(value, keys, label):
    if not isinstance(value, dict) or set(value) != keys:
        raise ReviewLaunchError(
            "review-response-invalid",
            f"{label} must contain exactly {', '.join(sorted(keys))}",
        )
    return value


def validate_review_response(response, approved_source_ids):
    _exact_review_object(response, set(REPORT_HEADINGS), "review response")
    if not isinstance(approved_source_ids, set):
        approved_source_ids = set(approved_source_ids)
    finding_ids = set()
    for heading in REPORT_HEADINGS:
        findings = response[heading]
        if not isinstance(findings, list):
            raise ReviewLaunchError(
                "review-response-invalid",
                f"{heading} must be an array",
            )
        for index, value in enumerate(findings):
            label = f"{heading} finding {index + 1}"
            finding = _exact_review_object(value, FINDING_KEYS, label)
            finding_id = _review_string(finding["id"], f"{label} id")
            if not STABLE_ID_PATTERN.fullmatch(finding_id):
                raise ReviewLaunchError(
                    "review-response-invalid",
                    f"{label} id must be a stable identifier",
                )
            if finding_id in finding_ids:
                raise ReviewLaunchError(
                    "review-response-invalid",
                    f"duplicate finding id: {finding_id}",
                )
            finding_ids.add(finding_id)
            for key in (
                "attacked_quote",
                "location",
                "attack",
                "consequence",
                "status",
            ):
                _review_string(finding[key], f"{label} {key}")
            source_ids = finding["source_ids"]
            if (
                not isinstance(source_ids, list)
                or not source_ids
                or any(
                    not isinstance(source_id, str) or not source_id.strip()
                    for source_id in source_ids
                )
                or len(source_ids) != len(set(source_ids))
                or not set(source_ids).issubset(approved_source_ids)
            ):
                raise ReviewLaunchError(
                    "review-response-invalid",
                    f"{label} must cite unique approved source identifiers",
                )
            correction = finding["correction"]
            decision = finding["plaintiff_decision"]
            if correction is not None:
                correction = _exact_review_object(
                    correction,
                    CORRECTION_KEYS,
                    f"{label} correction",
                )
                replaced = _review_string(
                    correction["replace"],
                    f"{label} correction replace",
                )
                _review_string(correction["with"], f"{label} correction with")
                if replaced != finding["attacked_quote"]:
                    raise ReviewLaunchError(
                        "review-response-invalid",
                        f"{label} correction must replace the exact attacked quote",
                    )
            if decision is not None:
                decision = _exact_review_object(
                    decision,
                    DECISION_KEYS,
                    f"{label} plaintiff decision",
                )
                _review_string(
                    decision["question"],
                    f"{label} plaintiff decision question",
                )
                choices = decision["choices"]
                if not isinstance(choices, list) or not choices:
                    raise ReviewLaunchError(
                        "review-response-invalid",
                        f"{label} plaintiff decision choices must be nonempty",
                    )
                for choice_index, choice_value in enumerate(choices):
                    choice = _exact_review_object(
                        choice_value,
                        CHOICE_KEYS,
                        f"{label} choice {choice_index + 1}",
                    )
                    _review_string(
                        choice["option"],
                        f"{label} choice {choice_index + 1} option",
                    )
                    _review_string(
                        choice["consequence"],
                        f"{label} choice {choice_index + 1} consequence",
                    )
            if correction is not None and decision is not None:
                raise ReviewLaunchError(
                    "review-response-invalid",
                    f"{label} cannot select both a correction and a plaintiff decision",
                )
    return response


def _extract_review(provider_response, approved_source_ids, raw_body):
    if not isinstance(provider_response, dict):
        raise ReviewLaunchError(
            "provider-response-incomplete",
            "Provider response must be a JSON object",
            stdout=raw_body,
        )
    if provider_response.get("status") != "completed":
        raise ReviewLaunchError(
            "provider-response-incomplete",
            "Provider response status was not completed",
        )
    output = provider_response.get("output")
    if not isinstance(output, list):
        raise ReviewLaunchError(
            "provider-response-incomplete",
            "Provider response output must be an array",
            stdout=raw_body,
        )
    texts = []
    for item in output:
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        content = item.get("content")
        if not isinstance(content, list):
            continue
        for part in content:
            if isinstance(part, dict) and part.get("type") == "output_text":
                texts.append(part.get("text"))
    if len(texts) != 1 or not isinstance(texts[0], str):
        raise ReviewLaunchError(
            "provider-response-incomplete",
            "Provider response must contain exactly one output_text value",
            stdout=raw_body,
        )
    try:
        review = json.loads(texts[0])
    except json.JSONDecodeError as error:
        raise ReviewLaunchError(
            "provider-response-malformed-json",
            "Provider output_text was not valid JSON",
            stdout=texts[0],
        ) from error
    return validate_review_response(review, approved_source_ids)


def run_trusted_review(
    packet,
    model,
    api_key,
    timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
    transport=None,
):
    validated = validate_packet(packet)
    validated_model = _runtime_string(model, "model")
    validated_key = _api_key(api_key)
    timeout = _positive_timeout(timeout_seconds)
    request = _provider_request(validated, validated_model)
    body = json.dumps(request, ensure_ascii=False, separators=(",", ":")).encode(
        "utf-8"
    )
    headers = {
        "Authorization": f"Bearer {validated_key}",
        "Content-Type": "application/json",
    }
    provider_transport = transport or _openai_transport
    try:
        status, response_body = provider_transport(body, headers, timeout)
    except TimeoutError as error:
        raise ReviewLaunchError(
            "provider-timeout",
            f"Provider exceeded timeout of {timeout} seconds",
        ) from error
    except OSError as error:
        raise ReviewLaunchError(
            "provider-unavailable",
            f"Provider unavailable: {error}",
        ) from error
    if not isinstance(status, int) or not isinstance(response_body, bytes):
        raise ReviewLaunchError(
            "provider-response-incomplete",
            "Provider transport returned an invalid response",
        )
    if status < 200 or status >= 300:
        raise ReviewLaunchError(
            "provider-http-error",
            f"Provider returned HTTP {status}",
        )
    if len(response_body) > PROVIDER_BODY_LIMIT:
        raise ReviewLaunchError(
            "provider-response-too-large",
            "Provider response exceeded the permitted size",
            stdout=response_body,
        )
    try:
        decoded = response_body.decode("utf-8")
        provider_response = json.loads(decoded)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReviewLaunchError(
            "provider-response-malformed-json",
            "Provider response was not valid UTF-8 JSON",
            stdout=response_body,
        ) from error
    approved_source_ids = {source["id"] for source in validated["sources"]}
    review = _extract_review(provider_response, approved_source_ids, response_body)
    return {
        "dispatch": {
            "payload": validated,
            "capabilities": [],
            "runtime": "openai-responses-stateless",
            "request": request,
        },
        "review": review,
    }


def _labeled_text(label, value):
    lines = value.splitlines() or [""]
    if len(lines) == 1:
        return f"{label}: {lines[0]}"
    quoted = "\n".join(f"> {line}" for line in lines)
    return f"{label}:\n\n{quoted}"


def _inline_text(value):
    return str(value).replace("\r", "\\r").replace("\n", "\\n")


def _receipt_markdown(receipt):
    labels = (
        ("outcome", "Result"),
        ("runtime", "Runtime"),
        ("model", "Model"),
        ("run_id", "Run ID"),
        ("run_time", "UTC time"),
        ("document_family", "Document family"),
        ("draft_version", "Audited version"),
        ("artifact_path", "Audited artifact"),
        ("draft_sha256", "Draft SHA-256"),
        ("packet_sha256", "Packet SHA-256"),
    )
    lines = ["# Adversarial Filing Review", ""]
    for key, label in labels:
        if key in receipt:
            lines.append(f"- {label}: {_inline_text(receipt[key])}")
    source_ids = receipt.get("source_ids", [])
    lines.append(
        f"- Approved sources: {', '.join(_inline_text(value) for value in source_ids) if source_ids else 'None'}"
    )
    if receipt.get("failure_id"):
        lines.append(f"- Failure class: {receipt['failure_id']}")
    return "\n".join(lines)


def render_review_markdown(review, receipt):
    validate_review_response(review, set(receipt.get("source_ids", [])))
    sections = [_receipt_markdown(receipt)]
    for heading in REPORT_HEADINGS:
        sections.extend(["", f"## {heading}", ""])
        findings = review[heading]
        if not findings:
            sections.append("None found")
            continue
        for finding in findings:
            sections.extend(
                [
                    f"### {finding['id']}",
                    "",
                    _labeled_text("Attacked quote", finding["attacked_quote"]),
                    "",
                    _labeled_text("Location", finding["location"]),
                    "",
                    f"Sources: {', '.join(_inline_text(value) for value in finding['source_ids'])}",
                    "",
                    _labeled_text("Attack", finding["attack"]),
                    "",
                    _labeled_text("Consequence", finding["consequence"]),
                    "",
                    _labeled_text("Status", finding["status"]),
                ]
            )
            correction = finding["correction"]
            if correction:
                sections.extend(
                    [
                        "",
                        _labeled_text("Replace", correction["replace"]),
                        "",
                        _labeled_text("With", correction["with"]),
                    ]
                )
            decision = finding["plaintiff_decision"]
            if decision:
                sections.extend(
                    [
                        "",
                        "#### PLAINTIFF DECISION REQUIRED",
                        "",
                        _labeled_text("Question", decision["question"]),
                        "",
                    ]
                )
                for choice_index, choice in enumerate(decision["choices"], start=1):
                    sections.extend(
                        [
                            f"##### Option {choice_index}",
                            "",
                            _labeled_text("Option", choice["option"]),
                            "",
                            _labeled_text("Consequence", choice["consequence"]),
                            "",
                        ]
                    )
    return "\n".join(sections).rstrip() + "\n"


def _canonical_json_sha256(value):
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _inside(path, boundary):
    try:
        path.relative_to(boundary)
    except ValueError:
        return False
    return path != boundary


def _run_identity(now, run_id):
    current = now or datetime.now(timezone.utc)
    if not isinstance(current, datetime) or current.tzinfo is None:
        raise ReviewLaunchError(
            "review-output-invalid",
            "run time must be timezone-aware",
        )
    current = current.astimezone(timezone.utc)
    supplied_run_id = str(run_id or uuid.uuid4())
    if not RUN_ID_PATTERN.fullmatch(supplied_run_id):
        raise ReviewLaunchError(
            "review-output-invalid",
            "run id must be a canonical UUID",
        )
    filename_time = current.strftime("%Y%m%dT%H%M%SZ")
    display_time = current.strftime("%Y-%m-%dT%H:%M:%SZ")
    return filename_time, display_time, supplied_run_id


def _prepare_output(
    packet,
    project_boundary,
    version_folder,
    artifact_path,
    now,
    run_id,
):
    try:
        project = Path(project_boundary).resolve(strict=True)
        version = Path(version_folder).resolve(strict=True)
        artifact = Path(artifact_path).resolve(strict=True)
    except (OSError, TypeError) as error:
        raise ReviewLaunchError(
            "review-output-invalid",
            f"review output preflight failed: {error}",
        ) from error
    if not project.is_dir() or not version.is_dir() or not _inside(version, project):
        raise ReviewLaunchError(
            "review-output-invalid",
            "version folder must be an existing child of the project boundary",
        )
    if not artifact.is_file() or not _inside(artifact, version):
        raise ReviewLaunchError(
            "review-output-invalid",
            "audited artifact must be an existing file inside the version folder",
        )
    artifact_bytes = artifact.read_bytes()
    draft_bytes = packet["draft"]["content"].encode("utf-8")
    artifact_sha256 = hashlib.sha256(artifact_bytes).hexdigest()
    if (
        artifact_bytes != draft_bytes
        or artifact_sha256 != packet["draft"]["sha256"]
    ):
        raise ReviewLaunchError(
            "review-artifact-fingerprint-mismatch",
            "audited artifact does not match the validated packet draft",
        )
    audits = version / "audits"
    if audits.exists() or audits.is_symlink():
        try:
            resolved_audits = audits.resolve(strict=True)
        except OSError as error:
            raise ReviewLaunchError(
                "review-output-invalid",
                f"audits directory cannot be resolved: {error}",
            ) from error
        if not resolved_audits.is_dir() or not _inside(resolved_audits, version):
            raise ReviewLaunchError(
                "review-output-invalid",
                "audits directory resolves outside the version folder",
            )
    else:
        resolved_audits = audits
    filename_time, display_time, supplied_run_id = _run_identity(now, run_id)
    report_path = resolved_audits / (
        f"adversarial-filing-review-{filename_time}-{supplied_run_id}.md"
    )
    if report_path.exists() or report_path.is_symlink():
        raise ReviewLaunchError(
            "review-report-collision",
            "review report path already exists",
        )
    return {
        "version": version,
        "artifact": artifact,
        "audits": resolved_audits,
        "report_path": report_path,
        "run_time": display_time,
        "run_id": supplied_run_id,
    }


def _write_report(output, markdown):
    directory_fd = None
    report_fd = None
    try:
        output["audits"].mkdir(parents=False, exist_ok=True)
        directory_fd = os.open(
            output["audits"],
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
        )
        report_fd = os.open(
            output["report_path"].name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o666,
            dir_fd=directory_fd,
        )
        with os.fdopen(
            report_fd,
            "w",
            encoding="utf-8",
            newline="\n",
        ) as stream:
            report_fd = None
            stream.write(markdown)
    except FileExistsError as error:
        raise ReviewLaunchError(
            "review-report-collision",
            "review report path already exists",
        ) from error
    except OSError as error:
        raise ReviewLaunchError(
            "review-output-unavailable",
            f"review report could not be written: {error}",
        ) from error
    finally:
        if report_fd is not None:
            os.close(report_fd)
        if directory_fd is not None:
            os.close(directory_fd)
    return output["report_path"]


def _receipt(packet, output, model, outcome, failure_id=None):
    receipt = {
        "runtime": "openai-responses-stateless",
        "model": model,
        "run_id": output["run_id"],
        "run_time": output["run_time"],
        "document_family": packet["document_family"],
        "draft_version": packet["draft"]["version"],
        "artifact_path": str(output["artifact"]),
        "draft_sha256": packet["draft"]["sha256"],
        "packet_sha256": _canonical_json_sha256(packet),
        "source_ids": [source["id"] for source in packet["sources"]],
        "outcome": outcome,
    }
    if failure_id:
        receipt["failure_id"] = failure_id
    return receipt


def _unavailable_markdown(receipt, error):
    return (
        _receipt_markdown(receipt)
        + "\n\n## Independent review unavailable\n\n"
        + _labeled_text("Reason", _bounded(error.reason))
        + "\n"
    )


def execute_trusted_review(
    packet,
    model,
    api_key,
    project_boundary,
    version_folder,
    artifact_path,
    timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
    transport=None,
    now=None,
    run_id=None,
):
    validated = validate_packet(packet)
    output = _prepare_output(
        validated,
        project_boundary,
        version_folder,
        artifact_path,
        now,
        run_id,
    )
    try:
        result = run_trusted_review(
            validated,
            model,
            api_key,
            timeout_seconds=timeout_seconds,
            transport=transport,
        )
    except ReviewLaunchError as error:
        safe_model = model if isinstance(model, str) and model.strip() else "unavailable"
        receipt = _receipt(
            validated,
            output,
            safe_model,
            "unavailable",
            error.finding_id,
        )
        report_path = _write_report(output, _unavailable_markdown(receipt, error))
        return {
            "outcome": "unavailable",
            "report_path": str(report_path),
            "error": _error_result(error)["error"],
        }
    receipt = _receipt(validated, output, model, "completed")
    markdown = render_review_markdown(result["review"], receipt)
    report_path = _write_report(output, markdown)
    return {
        "outcome": "completed",
        "report_path": str(report_path),
        "dispatch": {
            "runtime": result["dispatch"]["runtime"],
            "capabilities": result["dispatch"]["capabilities"],
        },
    }


def launch_review(
    packet,
    reviewer_command,
    runtime_enforces_empty_capabilities,
    timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
):
    validate_packet(packet)
    _command(reviewer_command)
    _positive_timeout(timeout_seconds)
    raise ReviewLaunchError(
        "independent-review-unavailable",
        "independent review unavailable: a caller assertion cannot prove command isolation",
    )


def _parser():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--trusted-openai", action="store_true")
    mode.add_argument("--reviewer-command-json")
    parser.add_argument("--runtime-enforces-empty-capabilities", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--model")
    parser.add_argument("--project-boundary")
    parser.add_argument("--version-folder")
    parser.add_argument("--artifact")
    return parser


def _error_result(error):
    result = {
        "error": {
            "id": getattr(error, "finding_id", "review-launch-configuration-invalid"),
            "reason": getattr(error, "reason", str(error)),
        }
    }
    if isinstance(error, ReviewLaunchError):
        result["error"]["stdout"] = error.stdout
        result["error"]["stderr"] = error.stderr
    return result


def main(
    argv=None,
    input_bytes=None,
    transport=None,
    environ=None,
    now=None,
    run_id=None,
):
    arguments = _parser().parse_args(argv)
    source = sys.stdin.buffer.read() if input_bytes is None else input_bytes
    try:
        packet = json.loads(source.decode("utf-8"))
        if arguments.trusted_openai:
            required = {
                "model": arguments.model,
                "project boundary": arguments.project_boundary,
                "version folder": arguments.version_folder,
                "artifact": arguments.artifact,
            }
            missing = [label for label, value in required.items() if not value]
            if missing:
                raise ValueError(f"trusted runtime requires {', '.join(missing)}")
            environment = os.environ if environ is None else environ
            result = execute_trusted_review(
                packet,
                model=arguments.model,
                api_key=environment.get("OPENAI_API_KEY", ""),
                project_boundary=arguments.project_boundary,
                version_folder=arguments.version_folder,
                artifact_path=arguments.artifact,
                timeout_seconds=arguments.timeout_seconds,
                transport=transport,
                now=now,
                run_id=run_id,
            )
            print(json.dumps(result, sort_keys=True))
            return 0 if result["outcome"] == "completed" else 1
        command = json.loads(arguments.reviewer_command_json)
        result = launch_review(
            packet,
            command,
            arguments.runtime_enforces_empty_capabilities,
            arguments.timeout_seconds,
        )
    except (
        PacketValidationError,
        ReviewLaunchError,
        UnicodeDecodeError,
        json.JSONDecodeError,
        ValueError,
    ) as error:
        print(json.dumps(_error_result(error), sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
