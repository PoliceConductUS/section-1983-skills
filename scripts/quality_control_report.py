"""Trusted-host publication for one immutable quality-control report."""

from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from scripts.skill_output_writer import OutputError, OutputRun
from scripts.validate_folder_invocation import (
    ValidatedInvocation,
    build_input_manifest,
)


_IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_UUID_V4 = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
_SKILL_VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_UTC_RUN_TIME = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$"
)
_REPORT_PREFIX = "quality-control-reports"
_METADATA_FENCE = b"```quality-control-report+json\n"
_REPORT_METADATA_KEYS = {
    "approved_source_identities",
    "failed_findings",
    "input_manifest",
    "passing_but_suboptimal_recommendations",
    "quality_control_kind",
    "result",
    "run_at",
    "run_id",
    "run_manifest",
    "schema_version",
    "scope",
    "skill",
    "skill_version",
    "target",
}


class QualityControlReportError(ValueError):
    """A bounded quality-control report contract failure."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class QualityControlReportPlan:
    """Detached report bytes and logical inputs awaiting host publication."""

    relative_path: str
    contents: bytes
    input_manifest: dict[str, list[dict[str, Any]]]


def _fail(code: str) -> None:
    raise QualityControlReportError(code)


def _canonical_value(value: Any, code: str) -> Any:
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return json.loads(encoded)
    except (TypeError, ValueError, UnicodeError, json.JSONDecodeError):
        _fail(code)


def _canonical_bytes(value: Any, code: str) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError):
        _fail(code)


def _valid_identifier(value: Any) -> bool:
    return isinstance(value, str) and _IDENTIFIER.fullmatch(value) is not None


def _valid_manifest_identity(value: Any) -> bool:
    if type(value) is not dict or set(value) != {"inputs"}:
        return False
    inputs = value["inputs"]
    if type(inputs) is not list:
        return False
    for input_role in inputs:
        if type(input_role) is not dict or set(input_role) != {"role", "files"}:
            return False
        if not _valid_identifier(input_role["role"]) or type(input_role["files"]) is not list:
            return False
        for file_identity in input_role["files"]:
            if type(file_identity) is not dict or set(file_identity) != {
                "path",
                "sha256",
                "size",
            }:
                return False
            if (
                not isinstance(file_identity["path"], str)
                or not file_identity["path"]
                or not isinstance(file_identity["sha256"], str)
                or _SHA256.fullmatch(file_identity["sha256"]) is None
                or type(file_identity["size"]) is not int
                or file_identity["size"] < 0
            ):
                return False
    return True


def _valid_report_metadata(value: Any, encoded: bytes) -> bool:
    if type(value) is not dict or set(value) != _REPORT_METADATA_KEYS:
        return False
    run_id = value["run_id"]
    run_manifest = value["run_manifest"]
    target = value["target"]
    if (
        value["schema_version"] != 1
        or not _valid_identifier(value["skill"])
        or not isinstance(value["skill_version"], str)
        or _SKILL_VERSION.fullmatch(value["skill_version"]) is None
        or not _valid_identifier(value["quality_control_kind"])
        or not isinstance(value["run_at"], str)
        or _UTC_RUN_TIME.fullmatch(value["run_at"]) is None
        or not isinstance(run_id, str)
        or _UUID_V4.fullmatch(run_id) is None
        or not isinstance(value["scope"], str)
        or not value["scope"].strip()
        or not _valid_identifier(value["result"])
        or type(value["approved_source_identities"]) is not list
        or any(
            not isinstance(identity, str) or not identity.strip()
            for identity in value["approved_source_identities"]
        )
        or type(value["failed_findings"]) is not list
        or type(value["passing_but_suboptimal_recommendations"]) is not list
        or not _valid_manifest_identity(value["input_manifest"])
        or type(target) is not dict
        or set(target) != {"path", "role", "sha256", "size"}
        or not isinstance(target["path"], str)
        or not target["path"]
        or not _valid_identifier(target["role"])
        or not isinstance(target["sha256"], str)
        or _SHA256.fullmatch(target["sha256"]) is None
        or type(target["size"]) is not int
        or target["size"] < 0
        or type(run_manifest) is not dict
        or set(run_manifest) != {"path", "run_id"}
        or run_manifest["run_id"] != run_id
        or run_manifest["path"] != f".skill-runs/{run_id}/manifest.json"
    ):
        return False
    return _canonical_bytes(value, "invalid-quality-control-metadata") == encoded


def _has_canonical_report_envelope(path: Path) -> bool:
    try:
        with path.open("rb") as candidate:
            if candidate.readline() != _METADATA_FENCE:
                return False
            metadata_line = candidate.readline(1_000_001)
            if not metadata_line.endswith(b"\n") or len(metadata_line) > 1_000_000:
                return False
            if candidate.readline() != b"```\n":
                return False
    except OSError:
        _fail("quality-control-input-unavailable")
    try:
        metadata = json.loads(metadata_line[:-1])
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False
    return _valid_report_metadata(metadata, metadata_line[:-1])


def _validate_contract_target(invocation: ValidatedInvocation) -> None:
    if (
        invocation.contract_target_policy not in {"required", "optional"}
        or invocation.contract_target_roles is None
    ):
        _fail("quality-control-contract-unbound")
    if invocation.target is None:
        _fail("invalid-quality-control-target")
    if invocation.target[0] not in invocation.contract_target_roles:
        _fail("quality-control-contract-target")


def _target_identity(
    invocation: ValidatedInvocation,
    manifest: dict[str, list[dict[str, Any]]],
) -> tuple[dict[str, Any], str, str]:
    if invocation.target is None:
        _fail("invalid-quality-control-target")
    target_role, target_path = invocation.target
    if not target_path.is_file():
        _fail("invalid-quality-control-target")

    role_root = next(
        (root for role, root in invocation.inputs if role == target_role), None
    )
    if role_root is None:
        _fail("invalid-quality-control-target")
    try:
        relative_path = target_path.relative_to(role_root).as_posix()
    except ValueError:
        _fail("invalid-quality-control-target")

    for input_role in manifest["inputs"]:
        if input_role["role"] != target_role:
            continue
        for file_identity in input_role["files"]:
            if file_identity["path"] == relative_path:
                return (
                    {
                        "path": relative_path,
                        "role": target_role,
                        "sha256": file_identity["sha256"],
                        "size": file_identity["size"],
                    },
                    target_role,
                    relative_path,
                )
    _fail("invalid-quality-control-target")


def _is_generated_report(
    invocation: ValidatedInvocation,
    role: str,
    relative_path: str,
) -> bool:
    if relative_path.startswith(f"{_REPORT_PREFIX}/"):
        return True
    role_root = next((root for name, root in invocation.inputs if name == role), None)
    if role_root is None:
        _fail("quality-control-contract-target")
    return _has_canonical_report_envelope(role_root / Path(relative_path))


def _filtered_input_manifest(
    invocation: ValidatedInvocation,
    manifest: dict[str, list[dict[str, Any]]],
    target_role: str,
    target_path: str,
) -> dict[str, list[dict[str, Any]]]:
    return {
        "inputs": [
            {
                "role": input_role["role"],
                "files": [
                    copy.deepcopy(file_identity)
                    for file_identity in input_role["files"]
                    if not _is_generated_report(
                        invocation, input_role["role"], file_identity["path"]
                    )
                    or (
                        input_role["role"] == target_role
                        and file_identity["path"] == target_path
                    )
                ],
            }
            for input_role in manifest["inputs"]
        ]
    }


def _utc_values(run_at: Any) -> tuple[str, str]:
    if (
        not isinstance(run_at, datetime)
        or run_at.tzinfo is None
        or run_at.utcoffset() != timedelta(0)
    ):
        _fail("invalid-quality-control-run-time")
    utc_text = run_at.isoformat(
        timespec="microseconds" if run_at.microsecond else "seconds"
    ).replace("+00:00", "Z")
    path_time = run_at.strftime(
        "%Y%m%dT%H%M%S%fZ" if run_at.microsecond else "%Y%m%dT%H%M%SZ"
    )
    return utc_text, path_time


def build_quality_control_report_plan(
    invocation: ValidatedInvocation,
    *,
    skill_version: str,
    quality_control_kind: str,
    run_id: str,
    run_at: datetime,
    scope: str,
    result: str,
    approved_source_identities: list[str],
    failed_findings: list[Any],
    passing_but_suboptimal_recommendations: list[Any],
    body: str,
) -> QualityControlReportPlan:
    """Build one detached QC report plan without mutating output state."""
    if not isinstance(invocation, ValidatedInvocation):
        _fail("invalid-quality-control-invocation")
    if not isinstance(skill_version, str) or _SKILL_VERSION.fullmatch(skill_version) is None:
        _fail("invalid-quality-control-skill-version")
    if not _valid_identifier(quality_control_kind):
        _fail("invalid-quality-control-kind")
    if not isinstance(run_id, str) or _UUID_V4.fullmatch(run_id) is None:
        _fail("invalid-quality-control-run-id")
    if not isinstance(scope, str) or not scope.strip():
        _fail("invalid-quality-control-scope")
    if not _valid_identifier(result):
        _fail("invalid-quality-control-result")
    if (
        type(approved_source_identities) is not list
        or any(
            not isinstance(identity, str) or not identity.strip()
            for identity in approved_source_identities
        )
        or len(approved_source_identities) != len(set(approved_source_identities))
    ):
        _fail("invalid-quality-control-source-identities")
    if type(failed_findings) is not list:
        _fail("invalid-quality-control-findings")
    if type(passing_but_suboptimal_recommendations) is not list:
        _fail("invalid-quality-control-recommendations")
    if not isinstance(body, str):
        _fail("invalid-quality-control-body")

    run_at_text, path_time = _utc_values(run_at)
    _validate_contract_target(invocation)
    generic_manifest = build_input_manifest(invocation)
    target, target_role, target_path = _target_identity(invocation, generic_manifest)
    input_manifest = _filtered_input_manifest(
        invocation, generic_manifest, target_role, target_path
    )
    target, _, _ = _target_identity(invocation, input_manifest)

    metadata = {
        "approved_source_identities": copy.deepcopy(approved_source_identities),
        "failed_findings": _canonical_value(
            failed_findings, "invalid-quality-control-findings"
        ),
        "input_manifest": input_manifest,
        "passing_but_suboptimal_recommendations": _canonical_value(
            passing_but_suboptimal_recommendations,
            "invalid-quality-control-recommendations",
        ),
        "quality_control_kind": quality_control_kind,
        "result": result,
        "run_at": run_at_text,
        "run_id": run_id,
        "run_manifest": {
            "path": f".skill-runs/{run_id}/manifest.json",
            "run_id": run_id,
        },
        "schema_version": 1,
        "scope": scope,
        "skill": invocation.skill,
        "skill_version": skill_version,
        "target": target,
    }
    metadata_bytes = _canonical_bytes(metadata, "invalid-quality-control-metadata")
    try:
        body_bytes = body.encode("utf-8")
    except UnicodeError:
        _fail("invalid-quality-control-body")
    relative_path = (
        f"{_REPORT_PREFIX}/{quality_control_kind}-{path_time}-{run_id}.md"
    )
    return QualityControlReportPlan(
        relative_path=relative_path,
        contents=_METADATA_FENCE + metadata_bytes + b"\n```\n\n" + body_bytes,
        input_manifest=copy.deepcopy(input_manifest),
    )


def publish_quality_control_report(
    invocation: ValidatedInvocation,
    *,
    skill_version: str,
    quality_control_kind: str,
    run_id: str,
    run_at: datetime,
    scope: str,
    result: str,
    approved_source_identities: list[str],
    failed_findings: list[Any],
    passing_but_suboptimal_recommendations: list[Any],
    body: str,
    internet_sources=(),
) -> dict[str, Any]:
    """Publish one planned report and return only a durable success receipt."""
    plan = build_quality_control_report_plan(
        invocation,
        skill_version=skill_version,
        quality_control_kind=quality_control_kind,
        run_id=run_id,
        run_at=run_at,
        scope=scope,
        result=result,
        approved_source_identities=approved_source_identities,
        failed_findings=failed_findings,
        passing_but_suboptimal_recommendations=(
            passing_but_suboptimal_recommendations
        ),
        body=body,
    )
    run = OutputRun.start(
        invocation,
        run_id=run_id,
        skill_version=skill_version,
        mode="append-immutable",
        input_manifest=plan.input_manifest,
    )
    try:
        run.write(
            plan.relative_path,
            plan.contents,
            internet_sources=internet_sources,
        )
    except OutputError as error:
        try:
            run.fail(error.code, "quality-control-report-publication")
        except OutputError:
            pass
        raise
    return run.complete()
