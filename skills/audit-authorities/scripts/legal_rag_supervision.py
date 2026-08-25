"""Pure relationship checks for an independent authority-audit record.

The trusted host supplies already-computed fingerprints. This module performs
no filesystem, network, output, or substantive legal-authority work.
"""

import re


_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_FORBIDDEN_KEYS = {
    "api_key",
    "access_token",
    "credential",
    "credentials",
    "continuation_state",
    "conversation_id",
    "provider_session_id",
    "session_id",
}
_PROPOSITION_ORDER = (
    "unresolved-source-gaps",
    "incorrect-propositions",
    "misgrounded-propositions",
    "ungrounded-propositions",
    "completed-grounded-propositions",
)


def _result(supervision_result, execution=None, propositions=()):
    value = {
        "execution_outcome": execution,
        "proposition_outcomes": list(propositions),
        "supervision_result": supervision_result,
    }
    if execution is None:
        value.pop("execution_outcome")
    return value


def _contains_forbidden_key(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            lowered = str(key).casefold()
            if (
                lowered in _FORBIDDEN_KEYS
                or "credential" in lowered
                or lowered.endswith("_token")
            ):
                return True
            if _contains_forbidden_key(nested):
                return True
    elif isinstance(value, list):
        return any(_contains_forbidden_key(item) for item in value)
    return False


def _identifier(value):
    return isinstance(value, str) and bool(value.strip())


def _fingerprint(value):
    if not isinstance(value, dict):
        return None
    allowed = {"role", "path", "sha256", "source_id"}
    if set(value) - allowed or not {"role", "path", "sha256"}.issubset(value):
        return None
    if not _identifier(value["role"]) or not _identifier(value["path"]):
        return None
    if value["path"].startswith("/") or ".." in value["path"].split("/"):
        return None
    if not isinstance(value["sha256"], str) or not _SHA256.fullmatch(
        value["sha256"]
    ):
        return None
    source_id = value.get("source_id")
    if source_id is not None and not _identifier(source_id):
        return None
    return (value["role"], value["path"], value["sha256"], source_id)


def _fingerprint_set(values):
    if not isinstance(values, list):
        return None
    normalized = [_fingerprint(item) for item in values]
    if any(item is None for item in normalized) or len(normalized) != len(
        set(normalized)
    ):
        return None
    return set(normalized)


def _valid_stage_identity(stage):
    return isinstance(stage, dict) and all(
        _identifier(stage.get(field))
        for field in ("stage_id", "invocation_id", "stage_kind", "executed_at")
    )


def classify_supervision(record, current_fingerprints):
    """Classify supervision relationships without deciding any legal question."""

    if not isinstance(record, dict) or _contains_forbidden_key(record):
        return _result("invalid-supervision-record")
    if record.get("human_approval") != "not-provided":
        return _result("invalid-supervision-record")
    generation = record.get("generation_stage")
    audit = record.get("audit_stage")
    if audit is None:
        return _result("missing-independent-stage")
    if not _valid_stage_identity(generation) or not _valid_stage_identity(audit):
        return _result("invalid-supervision-record")
    if (
        audit.get("review_relationship") != "independent-stage"
        or generation["stage_id"] == audit["stage_id"]
        or generation["invocation_id"] == audit["invocation_id"]
    ):
        return _result("generator-self-review")
    generation_folder = generation.get("output_folder_fingerprint")
    audit_folder = audit.get("output_folder_fingerprint")
    if (
        not isinstance(generation_folder, str)
        or not _SHA256.fullmatch(generation_folder)
        or not isinstance(audit_folder, str)
        or not _SHA256.fullmatch(audit_folder)
    ):
        return _result("invalid-supervision-record")
    if generation_folder == audit_folder:
        return _result("reused-output-folder")

    recorded_inputs = _fingerprint_set(audit.get("input_fingerprints"))
    current_inputs = _fingerprint_set(current_fingerprints)
    generation_output = _fingerprint(generation.get("output"))
    if recorded_inputs is None or current_inputs is None or generation_output is None:
        return _result("invalid-supervision-record")
    if recorded_inputs != current_inputs:
        return _result("changed-input")

    target = record.get("target")
    target_sha256 = record.get("target_sha256")
    if not isinstance(target, dict) or set(target) != {"role", "path"}:
        return _result("invalid-supervision-record")
    target_tuple = (target.get("role"), target.get("path"), target_sha256, None)
    if generation_output != target_tuple or target_tuple not in recorded_inputs:
        return _result("changed-input")
    selected_source_ids = audit.get("selected_source_ids")
    if not isinstance(selected_source_ids, list) or any(
        not _identifier(item) for item in selected_source_ids
    ):
        return _result("invalid-supervision-record")
    recorded_source_ids = {item[3] for item in recorded_inputs if item[3] is not None}
    if len(selected_source_ids) != len(set(selected_source_ids)) or set(
        selected_source_ids
    ) != recorded_source_ids:
        return _result("changed-input")

    execution = audit.get("execution_outcome")
    if execution == "independent-execution-unavailable":
        return _result(execution, execution)
    if execution == "malformed-audit-output":
        return _result(execution, execution)
    if execution != "successful-independent-execution":
        return _result("invalid-supervision-record")

    propositions = record.get("propositions")
    if not isinstance(propositions, list) or not propositions:
        return _result("malformed-audit-output", "malformed-audit-output")
    observed = set()
    for proposition in propositions:
        if not isinstance(proposition, dict):
            return _result("malformed-audit-output", "malformed-audit-output")
        if proposition.get("materiality") != "material":
            continue
        correctness = proposition.get("correctness")
        groundedness = proposition.get("groundedness")
        if correctness == "unresolved" and groundedness == "not-applicable":
            observed.add("unresolved-source-gaps")
        elif correctness == "incorrect" and groundedness == "not-applicable":
            observed.add("incorrect-propositions")
        elif correctness == "verified" and groundedness == "misgrounded":
            observed.add("misgrounded-propositions")
        elif correctness == "verified" and groundedness == "ungrounded":
            observed.add("ungrounded-propositions")
        elif correctness == "verified" and groundedness == "grounded":
            observed.add("completed-grounded-propositions")
        else:
            return _result("malformed-audit-output", "malformed-audit-output")
    if not observed:
        return _result("malformed-audit-output", "malformed-audit-output")
    ordered = [item for item in _PROPOSITION_ORDER if item in observed]
    failures = [item for item in ordered if item != "completed-grounded-propositions"]
    supervision_result = "passed" if not failures else (
        failures[0] if len(failures) == 1 else "proposition-findings"
    )
    return _result(supervision_result, execution, ordered)
