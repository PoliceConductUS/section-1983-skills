import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile


DEFAULT_TIMEOUT_SECONDS = 60
STREAM_LIMIT = 8192
TRUNCATION_MARKER = "[truncated]"
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
CHILD_ENVIRONMENT_KEYS = (
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "PATH",
    "PATHEXT",
    "SYSTEMROOT",
    "WINDIR",
)


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


def _child_environment():
    return {
        key: os.environ[key]
        for key in CHILD_ENVIRONMENT_KEYS
        if key in os.environ
    }


def launch_review(
    packet,
    reviewer_command,
    runtime_enforces_empty_capabilities,
    timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
):
    validated = validate_packet(packet)
    command = _command(reviewer_command)
    timeout = _positive_timeout(timeout_seconds)
    if runtime_enforces_empty_capabilities is not True:
        raise ReviewLaunchError(
            "independent-review-unavailable",
            "independent review unavailable: runtime cannot enforce empty reviewer capabilities.",
        )

    payload = json.dumps(validated, ensure_ascii=False).encode("utf-8")
    try:
        with tempfile.TemporaryDirectory(prefix="adversarial-filing-review-") as directory:
            completed = subprocess.run(
                command,
                input=payload,
                capture_output=True,
                cwd=directory,
                env=_child_environment(),
                timeout=timeout,
                check=False,
                shell=False,
            )
    except FileNotFoundError as error:
        raise ReviewLaunchError(
            "reviewer-command-unavailable",
            f"Reviewer command unavailable: {error}",
        ) from error
    except OSError as error:
        raise ReviewLaunchError(
            "reviewer-command-unavailable",
            f"Reviewer command unavailable: {error}",
        ) from error
    except subprocess.TimeoutExpired as error:
        raise ReviewLaunchError(
            "reviewer-command-timeout",
            f"Reviewer command exceeded timeout of {timeout} seconds",
            stdout=error.stdout,
            stderr=error.stderr,
        ) from error

    stdout = _bounded(completed.stdout)
    stderr = _bounded(completed.stderr)
    if completed.returncode != 0:
        raise ReviewLaunchError(
            "reviewer-command-nonzero",
            f"Reviewer command exited {completed.returncode}",
            stdout=stdout,
            stderr=stderr,
        )
    try:
        response = json.loads(completed.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReviewLaunchError(
            "reviewer-response-malformed-json",
            "Reviewer response was not valid UTF-8 JSON",
            stdout=stdout,
            stderr=stderr,
        ) from error
    if not isinstance(response, dict):
        raise ReviewLaunchError(
            "reviewer-response-incomplete",
            "Reviewer response must be a JSON object",
            stdout=stdout,
            stderr=stderr,
        )
    return {
        "dispatch": {"payload": validated, "capabilities": []},
        "response": response,
    }


def _parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviewer-command-json", required=True)
    parser.add_argument("--runtime-enforces-empty-capabilities", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
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


def main(argv=None):
    arguments = _parser().parse_args(argv)
    try:
        command = json.loads(arguments.reviewer_command_json)
        packet = json.loads(sys.stdin.buffer.read().decode("utf-8"))
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
