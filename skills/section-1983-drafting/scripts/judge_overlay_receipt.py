#!/usr/bin/env python3

import argparse
import copy
import hashlib
import json
import re
import sys
import uuid
from datetime import date, datetime, timezone
from pathlib import Path, PurePosixPath


ROOT_KEYS = {
    "schema_version",
    "audited_version_id",
    "scope",
    "approved_source_ids",
    "artifacts",
    "overlay",
    "corpus",
    "court_conduct_inputs",
    "transfer_cards",
    "prohibited_inference_checks",
    "requested_result",
}
VALIDATION_STATUSES = {"passed", "missing", "stale", "failed", "unavailable"}
ANTI_GAMING_CHECKS = {
    "assignment-manipulation",
    "preference-exploitation",
    "desired-outcome-tailoring",
    "adverse-authority-concealment",
    "record-distortion",
    "court-personalization",
    "outcome-or-behavior-prediction",
    "unsupported-judge-conclusion",
}
STABLE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
SHA256 = re.compile(r"^[a-f0-9]{64}$")


class ReceiptError(ValueError):
    def __init__(self, message, failure_class="packet-invalid"):
        super().__init__(message)
        self.failure_class = failure_class


def _exact(value, keys, path):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ReceiptError(f"{path} must contain exactly {sorted(keys)}")


def _string(value, path):
    if not isinstance(value, str) or not value or value != value.strip():
        raise ReceiptError(f"{path} must be a nonempty trimmed string")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ReceiptError(f"{path} must contain valid Unicode") from error
    return value


def _stable(value, path):
    value = _string(value, path)
    if not STABLE_ID.fullmatch(value):
        raise ReceiptError(f"{path} must be a stable identifier")
    return value


def _sha256(value, path):
    if not isinstance(value, str) or not SHA256.fullmatch(value):
        raise ReceiptError(f"{path} must be a lowercase SHA-256 value")


def _date(value, path):
    value = _string(value, path)
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise ReceiptError(f"{path} must be an ISO date") from error
    if parsed.isoformat() != value:
        raise ReceiptError(f"{path} must be an ISO date")


def _status(value, path):
    if value not in VALIDATION_STATUSES:
        raise ReceiptError(f"{path} has an unknown validation status")


def _list(value, path, nonempty=False):
    if not isinstance(value, list) or (nonempty and not value):
        raise ReceiptError(f"{path} must be{' a nonempty' if nonempty else ''} list")
    return value


def _unique(values, path):
    if len(values) != len(set(values)):
        raise ReceiptError(f"{path} contains duplicate identifiers")


def _validate_artifacts(records):
    paths = []
    for index, record in enumerate(_list(records, "$.artifacts", nonempty=True)):
        path = f"$.artifacts[{index}]"
        _exact(record, {"relative_path", "sha256"}, path)
        paths.append(_string(record["relative_path"], f"{path}.relative_path"))
        _sha256(record["sha256"], f"{path}.sha256")
    _unique(paths, "$.artifacts")


def _validate_overlay(record):
    keys = {"skill_id", "version", "sha256", "checked_on", "validation_status"}
    _exact(record, keys, "$.overlay")
    _stable(record["skill_id"], "$.overlay.skill_id")
    _stable(record["version"], "$.overlay.version")
    _sha256(record["sha256"], "$.overlay.sha256")
    _date(record["checked_on"], "$.overlay.checked_on")
    _status(record["validation_status"], "$.overlay.validation_status")


def _validate_corpus(record):
    keys = {"corpus_id", "version", "sha256", "checked_on", "validation_status"}
    _exact(record, keys, "$.corpus")
    _stable(record["corpus_id"], "$.corpus.corpus_id")
    _stable(record["version"], "$.corpus.version")
    _sha256(record["sha256"], "$.corpus.sha256")
    _date(record["checked_on"], "$.corpus.checked_on")
    _status(record["validation_status"], "$.corpus.validation_status")


def _validate_conduct_inputs(records, approved_sources):
    source_ids = []
    for index, record in enumerate(
        _list(records, "$.court_conduct_inputs", nonempty=True)
    ):
        path = f"$.court_conduct_inputs[{index}]"
        _exact(record, {"source_id", "checked_on", "validation_status"}, path)
        source_id = _stable(record["source_id"], f"{path}.source_id")
        _date(record["checked_on"], f"{path}.checked_on")
        _status(record["validation_status"], f"{path}.validation_status")
        if source_id not in approved_sources:
            raise ReceiptError(f"{path}.source_id is not an approved source")
        source_ids.append(source_id)
    _unique(source_ids, "$.court_conduct_inputs")


def _validate_transfer_cards(records):
    card_ids = []
    for index, record in enumerate(_list(records, "$.transfer_cards")):
        path = f"$.transfer_cards[{index}]"
        _exact(record, {"card_id", "validation_status", "used"}, path)
        card_ids.append(_stable(record["card_id"], f"{path}.card_id"))
        _status(record["validation_status"], f"{path}.validation_status")
        if not isinstance(record["used"], bool):
            raise ReceiptError(f"{path}.used must be Boolean")
    _unique(card_ids, "$.transfer_cards")


def _validate_checks(records):
    for index, record in enumerate(_list(records, "$.prohibited_inference_checks")):
        path = f"$.prohibited_inference_checks[{index}]"
        _exact(record, {"check_id", "passed"}, path)
        _stable(record["check_id"], f"{path}.check_id")
        if not isinstance(record["passed"], bool):
            raise ReceiptError(f"{path}.passed must be Boolean")


def _validate_requested_result(record):
    keys = {"status", "drafting_changes", "no_change_reason", "failure_class"}
    _exact(record, keys, "$.requested_result")
    if record["status"] not in {"completed", "failed-closed"}:
        raise ReceiptError("$.requested_result.status is invalid")
    change_ids = []
    for index, change in enumerate(
        _list(record["drafting_changes"], "$.requested_result.drafting_changes")
    ):
        path = f"$.requested_result.drafting_changes[{index}]"
        _exact(change, {"change_id", "description", "transfer_card_ids"}, path)
        change_ids.append(_stable(change["change_id"], f"{path}.change_id"))
        _string(change["description"], f"{path}.description")
        card_ids = [
            _stable(value, f"{path}.transfer_card_ids[{card_index}]")
            for card_index, value in enumerate(
                _list(
                    change["transfer_card_ids"],
                    f"{path}.transfer_card_ids",
                    nonempty=True,
                )
            )
        ]
        _unique(card_ids, f"{path}.transfer_card_ids")
    _unique(change_ids, "$.requested_result.drafting_changes")
    if record["no_change_reason"] is not None:
        _string(record["no_change_reason"], "$.requested_result.no_change_reason")
    if record["failure_class"] is not None:
        _stable(record["failure_class"], "$.requested_result.failure_class")


def validate_packet(packet):
    _exact(packet, ROOT_KEYS, "$")
    if packet["schema_version"] != "1.0":
        raise ReceiptError("$.schema_version must equal 1.0")
    _stable(packet["audited_version_id"], "$.audited_version_id")
    _string(packet["scope"], "$.scope")
    approved_sources = [
        _stable(value, f"$.approved_source_ids[{index}]")
        for index, value in enumerate(
            _list(packet["approved_source_ids"], "$.approved_source_ids", nonempty=True)
        )
    ]
    _unique(approved_sources, "$.approved_source_ids")
    _validate_artifacts(packet["artifacts"])
    _validate_overlay(packet["overlay"])
    _validate_corpus(packet["corpus"])
    _validate_conduct_inputs(packet["court_conduct_inputs"], set(approved_sources))
    _validate_transfer_cards(packet["transfer_cards"])
    _validate_checks(packet["prohibited_inference_checks"])
    _validate_requested_result(packet["requested_result"])
    return copy.deepcopy(packet)


def _inside(path, parent):
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _input_root(value):
    try:
        root = Path(value).resolve(strict=True)
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        raise ReceiptError("declared input root is unavailable", "invalid-input-root") from error
    if not root.is_dir():
        raise ReceiptError("declared input root is unavailable", "invalid-input-root")
    return root


def _relative_path(value, label, *, reject_audits=False):
    if not isinstance(value, str) or not value or "\\" in value:
        raise ReceiptError(f"{label} must be a canonical relative path", "invalid-target")
    relative = PurePosixPath(value)
    if (
        relative.is_absolute()
        or relative.as_posix() != value
        or not relative.parts
        or any(part in {"", ".", ".."} for part in relative.parts)
        or (reject_audits and relative.parts[0] == "audits")
    ):
        raise ReceiptError(f"{label} must be a canonical relative path", "invalid-target")
    return relative


def _resolved_file(root, relative, label):
    selected = root.joinpath(*relative.parts)
    try:
        resolved = selected.resolve(strict=True)
    except (OSError, RuntimeError, ValueError) as error:
        raise ReceiptError(f"{label} must identify an existing file", "invalid-target") from error
    if not _inside(resolved, root) or not resolved.is_file():
        raise ReceiptError(f"{label} escapes its declared root", "invalid-target")
    return resolved


def _artifact_records(packet, filing_root):
    records = []
    for record in packet["artifacts"]:
        relative = _relative_path(
            record["relative_path"],
            "artifact path",
            reject_audits=True,
        )
        resolved = _resolved_file(filing_root, relative, "artifact path")
        actual = hashlib.sha256(resolved.read_bytes()).hexdigest()
        records.append(
            {
                "relative_path": relative.as_posix(),
                "expected_sha256": record["sha256"],
                "actual_sha256": actual,
                "matches": actual == record["sha256"],
            }
        )
    return records


def _status_failure(prefix, status):
    if status == "passed":
        return None
    suffix = "invalid" if status == "failed" else status
    return f"{prefix}-{suffix}"


def _normalize(packet, artifacts):
    if any(not record["matches"] for record in artifacts):
        return "failed-closed", "artifact-fingerprint-mismatch", []
    failure = _status_failure("overlay", packet["overlay"]["validation_status"])
    if failure:
        return "failed-closed", failure, []
    failure = _status_failure("corpus", packet["corpus"]["validation_status"])
    if failure:
        return "failed-closed", failure, []
    for record in packet["court_conduct_inputs"]:
        failure = _status_failure(
            "court-conduct-input", record["validation_status"]
        )
        if failure:
            return "failed-closed", failure, []
    for record in packet["transfer_cards"]:
        failure = _status_failure("transfer-card", record["validation_status"])
        if failure:
            return "failed-closed", failure, []
    checks = packet["prohibited_inference_checks"]
    check_ids = [record["check_id"] for record in checks]
    if (
        len(check_ids) != len(set(check_ids))
        or set(check_ids) != ANTI_GAMING_CHECKS
        or any(not record["passed"] for record in checks)
    ):
        return "failed-closed", "prohibited-inference-check-failed", []
    requested = packet["requested_result"]
    if requested["status"] == "failed-closed":
        return (
            "failed-closed",
            requested["failure_class"] or "requested-failed-closed",
            [],
        )
    changes = requested["drafting_changes"]
    cards = {record["card_id"]: record for record in packet["transfer_cards"]}
    if changes:
        referenced = {
            card_id
            for change in changes
            for card_id in change["transfer_card_ids"]
        }
        if (
            requested["no_change_reason"] is not None
            or requested["failure_class"] is not None
            or any(
                card_id not in cards
                or not cards[card_id]["used"]
                or cards[card_id]["validation_status"] != "passed"
                for card_id in referenced
            )
            or {record["card_id"] for record in cards.values() if record["used"]}
            != referenced
        ):
            return "failed-closed", "drafting-change-unsupported", []
        return "judge-specific-drafting-change", None, changes
    if (
        requested["no_change_reason"] is None
        or requested["failure_class"] is not None
        or any(record["used"] for record in packet["transfer_cards"])
    ):
        return "failed-closed", "requested-result-invalid", []
    return "no-judge-specific-drafting-change", None, []


def _display(value):
    return re.sub(r"\s+", " ", value).strip()


def _render(
    packet,
    artifacts,
    timestamp,
    run_id,
    filing_target,
    outcome,
    failure,
    changes,
):
    result = "failed-closed" if outcome == "failed-closed" else "completed"
    outcome_text = (
        "no judge-specific drafting change"
        if outcome == "no-judge-specific-drafting-change"
        else outcome.replace("-", " ")
    )
    lines = [
        "# Judge Overlay Execution Receipt",
        "",
        "Quality-control kind: judge-overlay-execution",
        f"Result: {result}",
        f"Outcome: {outcome_text}",
        f"Audited version ID: {_display(packet['audited_version_id'])}",
        f"Audited filing target: {filing_target}",
        f"UTC run time: {timestamp.isoformat().replace('+00:00', 'Z')}",
        f"Run ID: {run_id}",
        f"Scope: {_display(packet['scope'])}",
        "",
        "## Approved Sources",
        "",
    ]
    lines.extend(f"- {_display(value)}" for value in packet["approved_source_ids"])
    lines.extend(["", "## Audited Artifacts", ""])
    for record in artifacts:
        lines.extend(
            [
                f"- Path: {record['relative_path']}",
                f"  Expected SHA-256: {record['expected_sha256']}",
                f"  Actual SHA-256: {record['actual_sha256']}",
            ]
        )
    overlay = packet["overlay"]
    corpus = packet["corpus"]
    lines.extend(
        [
            "",
            "## Overlay",
            "",
            f"- Skill: {overlay['skill_id']}",
            f"- Version: {overlay['version']}",
            f"- SHA-256: {overlay['sha256']}",
            f"- Checked on: {overlay['checked_on']}",
            f"- Validation: {overlay['validation_status']}",
            "",
            "## Corpus",
            "",
            f"- ID: {corpus['corpus_id']}",
            f"- Version: {corpus['version']}",
            f"- SHA-256: {corpus['sha256']}",
            f"- Checked on: {corpus['checked_on']}",
            f"- Validation: {corpus['validation_status']}",
            "",
            "## Court-Conduct Inputs",
            "",
        ]
    )
    for record in packet["court_conduct_inputs"]:
        lines.append(
            f"- {record['source_id']}: {record['validation_status']} (checked {record['checked_on']})"
        )
    lines.extend(["", "## Transfer Card Inputs", ""])
    if packet["transfer_cards"]:
        for record in packet["transfer_cards"]:
            lines.append(
                f"- {record['card_id']}: {record['validation_status']}; used: {str(record['used']).lower()}"
            )
    else:
        lines.append("None.")
    lines.extend(["", "## Qualifying Neutral Transfer Cards Used", ""])
    used_cards = [record for record in packet["transfer_cards"] if record["used"]]
    if used_cards and outcome == "judge-specific-drafting-change":
        lines.extend(f"- {record['card_id']}" for record in used_cards)
    else:
        lines.append("None.")
    lines.extend(["", "## Prohibited-Inference Checks", ""])
    lines.extend(
        f"- {record['check_id']}: {str(record['passed']).lower()}"
        for record in packet["prohibited_inference_checks"]
    )
    lines.extend(["", "## Drafting Changes", ""])
    if changes:
        for change in changes:
            cards = ", ".join(change["transfer_card_ids"])
            lines.append(
                f"- {change['change_id']}: {_display(change['description'])} Supporting cards: {cards}."
            )
    else:
        lines.append("None.")
    lines.extend(["", "## Bounded Result", ""])
    if failure:
        lines.append(f"Failure class: {failure}")
    elif outcome == "no-judge-specific-drafting-change":
        lines.append(
            f"Bounded reason: {_display(packet['requested_result']['no_change_reason'])}"
        )
    else:
        lines.append("The listed drafting changes are supported by the listed used cards.")
    lines.extend(
        [
            "",
            "Recommendations and drafting changes in this receipt are advisory only.",
            "Implementation requires a separately authorized drafting stage in a new version when versioning applies, followed by a fresh read-only audit.",
            "",
        ]
    )
    return "\n".join(lines)


def _utc_time(value):
    selected = value or datetime.now(timezone.utc)
    if not isinstance(selected, datetime) or selected.tzinfo is None:
        raise ReceiptError("now must be a timezone-aware datetime")
    return selected.astimezone(timezone.utc)


def _run_id(value):
    selected = value or str(uuid.uuid4())
    try:
        parsed = uuid.UUID(selected)
    except (ValueError, AttributeError, TypeError) as error:
        raise ReceiptError("run_id must be a canonical UUID") from error
    if str(parsed) != selected:
        raise ReceiptError("run_id must be a canonical UUID")
    return selected


def execute_receipt(
    packet,
    *,
    filing_root,
    judge_corpus_root,
    court_conduct_root,
    filing_target,
    now=None,
    run_id=None,
):
    validated = validate_packet(packet)
    filing = _input_root(filing_root)
    _input_root(judge_corpus_root)
    _input_root(court_conduct_root)
    target = _relative_path(filing_target, "filing target", reject_audits=True)
    _resolved_file(filing, target, "filing target")
    artifacts = _artifact_records(validated, filing)
    if target.as_posix() not in {
        record["relative_path"] for record in artifacts
    }:
        raise ReceiptError(
            "filing target is not listed in packet artifacts",
            "invalid-target",
        )
    outcome, failure_class, changes = _normalize(validated, artifacts)
    timestamp = _utc_time(now)
    selected_run_id = _run_id(run_id)
    report = _render(
        validated,
        artifacts,
        timestamp,
        selected_run_id,
        target.as_posix(),
        outcome,
        failure_class,
        changes,
    )
    return {
        "outcome": outcome,
        "failure_class": failure_class,
        "report_bytes": report.encode("utf-8"),
    }


def _json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ReceiptError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _read_packet():
    raw = sys.stdin.buffer.read(1_000_001)
    if len(raw) > 1_000_000:
        raise ReceiptError("packet exceeds 1000000 bytes")
    try:
        text = raw.decode("utf-8", errors="strict")
        return json.loads(text, object_pairs_hook=_json_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReceiptError("packet is not valid UTF-8 JSON") from error


def _parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filing-root", required=True)
    parser.add_argument("--judge-corpus-root", required=True)
    parser.add_argument("--court-conduct-root", required=True)
    parser.add_argument("--filing-target", required=True)
    return parser


def _json_response(response):
    value = dict(response)
    value["report"] = value.pop("report_bytes").decode("utf-8")
    return value


def main(argv=None):
    args = _parser().parse_args(argv)
    try:
        response = execute_receipt(
            _read_packet(),
            filing_root=args.filing_root,
            judge_corpus_root=args.judge_corpus_root,
            court_conduct_root=args.court_conduct_root,
            filing_target=args.filing_target,
        )
    except ReceiptError as error:
        print(
            json.dumps(
                {"error": str(error), "failure_class": error.failure_class},
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(_json_response(response), sort_keys=True))
    return 1 if response["outcome"] == "failed-closed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
