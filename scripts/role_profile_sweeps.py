"""Trusted-host orchestration for fixed roles over declared folder inputs."""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from scripts.skill_output_writer import OutputError, OutputRun
from scripts.static_role_launcher import (
    BoundRoleLaunch,
    ProposedArtifact,
    RoleLaunchResult,
    SelectedInputSnapshot,
    launch_static_role,
)
from scripts.validate_folder_invocation import (
    ValidatedInvocation,
    build_input_manifest,
)


_IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$")
_MAX_VARIANTS = 64
_COMPARISON_FIELDS = (
    "category",
    "attacked_quote",
    "location",
    "source_ids",
    "analysis",
    "limitation",
)


class RoleSweepError(ValueError):
    """A bounded role-sweep contract failure."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _fail(code: str) -> None:
    raise RoleSweepError(code)


@dataclass(frozen=True)
class SweepVariant:
    variant_id: str
    binding: BoundRoleLaunch


@dataclass(frozen=True)
class PublishedArtifact:
    path: str
    sha256: str
    size: int


@dataclass(frozen=True)
class RoleRunRecord:
    variant_id: str
    role_id: str
    operation: str
    status: str
    code: str
    output_root: Path
    artifacts: tuple[PublishedArtifact, ...]
    findings: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class SweepResult:
    runs: tuple[RoleRunRecord, ...]
    comparison: ProposedArtifact


@dataclass(frozen=True)
class PersistedArtifact:
    hop_id: str
    output_root: Path
    path: str
    sha256: str
    size: int


@dataclass(frozen=True)
class SequenceHop:
    hop_id: str
    prior_artifact_path: str
    binder: Callable[[PersistedArtifact], BoundRoleLaunch]


@dataclass(frozen=True)
class SequenceResult:
    status: str
    runs: tuple[RoleRunRecord, ...]


def _valid_identifier(value: Any) -> bool:
    return isinstance(value, str) and _IDENTIFIER.fullmatch(value) is not None


def _validate_version(value: Any) -> None:
    if not isinstance(value, str) or _VERSION.fullmatch(value) is None:
        _fail("invalid-sweep-version")


def _definition_signature(binding: BoundRoleLaunch) -> tuple[Any, ...]:
    definition = binding.definition
    return (
        definition.role_id,
        definition.operations,
        tuple(
            (item.purpose, item.roles, item.min_files, item.max_files)
            for item in definition.input_requirements
        ),
        definition.capabilities,
        definition.prohibitions,
        definition.internet,
        definition.target_mutation,
        definition.output_kind,
        definition.public_instructions,
        definition.max_stdout_bytes,
        definition.max_stderr_bytes,
        type(definition.adapter),
        binding.task.operation,
        binding.task.instructions,
    )


def _purpose_inputs(
    binding: BoundRoleLaunch, purpose: str
) -> tuple[SelectedInputSnapshot, ...]:
    return tuple(item for item in binding.inputs if item.purpose == purpose)


def _validate_variants(
    variants: Any, comparison_invocation: ValidatedInvocation
) -> tuple[SweepVariant, ...]:
    if (
        type(variants) is not tuple
        or not variants
        or len(variants) > _MAX_VARIANTS
        or not isinstance(comparison_invocation, ValidatedInvocation)
    ):
        _fail("invalid-sweep")
    normalized: list[SweepVariant] = []
    variant_ids: set[str] = set()
    output_roots: set[Path] = set()
    signature: tuple[Any, ...] | None = None
    target_identity: tuple[str, str, int, bytes] | None = None
    sweep_root = comparison_invocation.output_root.parent
    expected_runs_root = sweep_root / "runs"
    if comparison_invocation.output_root.name != "comparison":
        _fail("invalid-sweep-output")
    for variant in variants:
        if (
            not isinstance(variant, SweepVariant)
            or not _valid_identifier(variant.variant_id)
            or variant.variant_id in variant_ids
            or not isinstance(variant.binding, BoundRoleLaunch)
        ):
            _fail("invalid-sweep-variant")
        binding = variant.binding
        profiles = _purpose_inputs(binding, "profile")
        targets = _purpose_inputs(binding, "filing-target")
        if not profiles or len(targets) != 1:
            _fail("invalid-sweep-variant")
        output_root = binding.invocation.output_root
        if (
            output_root.parent != expected_runs_root
            or output_root.name != variant.variant_id
            or output_root in output_roots
        ):
            _fail("invalid-sweep-output")
        current_signature = _definition_signature(binding)
        if signature is None:
            signature = current_signature
        elif current_signature != signature:
            _fail("sweep-role-mismatch")
        target = targets[0]
        current_target = (
            target.logical_name,
            target.sha256,
            target.size,
            target.contents,
        )
        if target_identity is None:
            target_identity = current_target
        elif current_target != target_identity:
            _fail("sweep-target-mismatch")
        variant_ids.add(variant.variant_id)
        output_roots.add(output_root)
        normalized.append(variant)
    return tuple(sorted(normalized, key=lambda item: item.variant_id))


def _extract_findings(artifacts: tuple[ProposedArtifact, ...]) -> tuple[dict[str, Any], ...]:
    candidates: list[list[Any]] = []
    for artifact in artifacts:
        try:
            value = json.loads(artifact.contents.decode("utf-8", errors="strict"))
        except (UnicodeError, ValueError, json.JSONDecodeError):
            continue
        if type(value) is dict and type(value.get("findings")) is list:
            candidates.append(value["findings"])
    if len(candidates) != 1:
        _fail("invalid-comparison-findings")
    findings: list[dict[str, Any]] = []
    for finding in candidates[0]:
        if type(finding) is not dict:
            _fail("invalid-comparison-findings")
        normalized: dict[str, Any] = {}
        for field in _COMPARISON_FIELDS:
            value = finding.get(field)
            if field == "source_ids":
                if (
                    type(value) is not list
                    or not value
                    or any(not isinstance(item, str) or not item for item in value)
                ):
                    _fail("invalid-comparison-findings")
                normalized[field] = sorted(set(value))
            elif not isinstance(value, str) or not value.strip():
                _fail("invalid-comparison-findings")
            else:
                normalized[field] = value
        findings.append(normalized)
    return tuple(findings)


def _published(artifact: ProposedArtifact) -> PublishedArtifact:
    return PublishedArtifact(
        path=artifact.path,
        sha256=hashlib.sha256(artifact.contents).hexdigest(),
        size=len(artifact.contents),
    )


def _yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _run_receipt(
    *,
    variant: SweepVariant,
    result: RoleLaunchResult,
    launcher_version: str,
    producer_version: str,
    artifacts: tuple[PublishedArtifact, ...],
) -> bytes:
    lines = [
        "schema_version: 1",
        f"variant_id: {_yaml_string(variant.variant_id)}",
        f"role: {_yaml_string(variant.binding.definition.role_id)}",
        f"operation: {_yaml_string(variant.binding.task.operation)}",
        f"launcher_version: {_yaml_string(launcher_version)}",
        f"producer_version: {_yaml_string(producer_version)}",
        f"status: {_yaml_string('success' if result.success else 'failure')}",
        f"code: {_yaml_string(result.code)}",
        "selected_inputs:",
    ]
    for item in sorted(
        variant.binding.inputs,
        key=lambda value: (value.purpose, value.role, value.path),
    ):
        lines.extend(
            (
                f"  - purpose: {_yaml_string(item.purpose)}",
                f"    role: {_yaml_string(item.role)}",
                f"    path: {_yaml_string(item.path)}",
                f"    sha256: {_yaml_string(item.sha256)}",
                f"    size: {item.size}",
            )
        )
    lines.append("outputs:")
    for artifact in sorted(artifacts, key=lambda item: item.path):
        lines.extend(
            (
                f"  - path: {_yaml_string(artifact.path)}",
                f"    sha256: {_yaml_string(artifact.sha256)}",
                f"    size: {artifact.size}",
            )
        )
    if not artifacts:
        lines[-1] = "outputs: []"
    return ("\n".join(lines) + "\n").encode("utf-8")


def _publish_run(
    *,
    variant: SweepVariant,
    result: RoleLaunchResult,
    findings: tuple[dict[str, Any], ...],
    launcher_version: str,
    producer_version: str,
) -> RoleRunRecord:
    proposed = result.artifacts if result.success else ()
    artifacts = tuple(_published(item) for item in proposed)
    try:
        publication = OutputRun.start(
            variant.binding.invocation,
            run_id=variant.variant_id,
            skill_version=producer_version,
            mode="append-immutable",
            input_manifest=build_input_manifest(variant.binding.invocation),
        )
        for artifact in proposed:
            publication.write(artifact.path, artifact.contents)
        publication.write(
            "run-receipt.yaml",
            _run_receipt(
                variant=variant,
                result=result,
                launcher_version=launcher_version,
                producer_version=producer_version,
                artifacts=artifacts,
            ),
        )
        if result.success:
            publication.complete()
        else:
            publication.fail(result.code, "role-launch")
    except (OutputError, OSError, ValueError):
        _fail("sweep-publication-failed")
    return RoleRunRecord(
        variant_id=variant.variant_id,
        role_id=variant.binding.definition.role_id,
        operation=variant.binding.task.operation,
        status="success" if result.success else "failure",
        code=result.code,
        output_root=variant.binding.invocation.output_root,
        artifacts=artifacts,
        findings=findings if result.success else (),
    )


def _launch_variant(
    variant: SweepVariant,
) -> tuple[RoleLaunchResult, tuple[dict[str, Any], ...]]:
    result = launch_static_role(variant.binding, run_id=str(uuid.uuid4()))
    findings: tuple[dict[str, Any], ...] = ()
    if result.success:
        try:
            findings = _extract_findings(result.artifacts)
        except RoleSweepError as error:
            result = RoleLaunchResult(
                success=False,
                code=error.code,
                artifacts=(),
            )
    return result, findings


def run_role_attack(
    *,
    variant: SweepVariant,
    launcher_version: str,
    producer_version: str,
) -> RoleRunRecord:
    """Run and publish one already validated fixed-role attack."""

    _validate_version(launcher_version)
    _validate_version(producer_version)
    if (
        not isinstance(variant, SweepVariant)
        or not _valid_identifier(variant.variant_id)
        or not isinstance(variant.binding, BoundRoleLaunch)
        or not _purpose_inputs(variant.binding, "profile")
        or len(_purpose_inputs(variant.binding, "filing-target")) != 1
    ):
        _fail("invalid-attack")
    result, findings = _launch_variant(variant)
    return _publish_run(
        variant=variant,
        result=result,
        findings=findings,
        launcher_version=launcher_version,
        producer_version=producer_version,
    )


def _finding_key(finding: dict[str, Any]) -> tuple[str, str, str]:
    return (
        finding["category"],
        finding["attacked_quote"],
        finding["location"],
    )


def _finding_value(finding: dict[str, Any]) -> tuple[tuple[str, ...], str, str]:
    return (
        tuple(sorted(finding["source_ids"])),
        finding["analysis"],
        finding["limitation"],
    )


def _finding_record(
    key: tuple[str, str, str],
    value: tuple[tuple[str, ...], str, str],
    variants: set[str],
) -> dict[str, Any]:
    return {
        "analysis": value[1],
        "attacked_quote": key[1],
        "category": key[0],
        "limitation": value[2],
        "location": key[2],
        "source_ids": list(value[0]),
        "variant_ids": sorted(variants),
    }


def compare_role_runs(runs: tuple[RoleRunRecord, ...]) -> ProposedArtifact:
    if (
        type(runs) is not tuple
        or not runs
        or any(not isinstance(run, RoleRunRecord) for run in runs)
        or len({run.variant_id for run in runs}) != len(runs)
        or len({(run.role_id, run.operation) for run in runs}) != 1
    ):
        _fail("invalid-sweep-runs")
    ordered = tuple(sorted(runs, key=lambda run: run.variant_id))
    successful = [run.variant_id for run in ordered if run.status == "success"]
    failed = [
        {"code": run.code, "variant_id": run.variant_id}
        for run in ordered
        if run.status != "success"
    ]
    stable: list[dict[str, Any]] = []
    subset: list[dict[str, Any]] = []
    flipped: list[dict[str, Any]] = []
    if not failed:
        occurrences: dict[
            tuple[str, str, str],
            dict[tuple[tuple[str, ...], str, str], set[str]],
        ] = {}
        for run in ordered:
            for finding in run.findings:
                key = _finding_key(finding)
                value = _finding_value(finding)
                occurrences.setdefault(key, {}).setdefault(value, set()).add(
                    run.variant_id
                )
        all_variants = {run.variant_id for run in ordered}
        for key in sorted(occurrences):
            values = occurrences[key]
            if len(values) > 1:
                flipped.append(
                    {
                        "attacked_quote": key[1],
                        "category": key[0],
                        "location": key[2],
                        "values": [
                            {
                                "analysis": value[1],
                                "limitation": value[2],
                                "source_ids": list(value[0]),
                                "variant_ids": sorted(values[value]),
                            }
                            for value in sorted(values)
                        ],
                    }
                )
                continue
            value, supporting = next(iter(values.items()))
            record = _finding_record(key, value, supporting)
            if supporting == all_variants:
                stable.append(record)
            else:
                subset.append(record)
    value = {
        "failed_variants": failed,
        "flipped_findings": flipped,
        "operation": ordered[0].operation,
        "role": ordered[0].role_id,
        "schema_version": 1,
        "stable_findings": stable,
        "status": "incomplete" if failed else "complete",
        "subset_findings": subset,
        "successful_variants": successful,
    }
    contents = (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    return ProposedArtifact(path="comparison.json", contents=contents)


def _publish_comparison(
    invocation: ValidatedInvocation,
    artifact: ProposedArtifact,
    *,
    producer_version: str,
) -> None:
    try:
        publication = OutputRun.start(
            invocation,
            run_id="comparison",
            skill_version=producer_version,
            mode="append-immutable",
            input_manifest=build_input_manifest(invocation),
        )
        publication.write(artifact.path, artifact.contents)
        publication.complete()
    except (OutputError, OSError, ValueError):
        _fail("sweep-publication-failed")


def run_role_sweep(
    *,
    variants: tuple[SweepVariant, ...],
    comparison_invocation: ValidatedInvocation,
    launcher_version: str,
    producer_version: str,
) -> SweepResult:
    """Run and publish one deterministic profile sweep."""

    _validate_version(launcher_version)
    _validate_version(producer_version)
    ordered = _validate_variants(variants, comparison_invocation)
    records: list[RoleRunRecord] = []
    for variant in ordered:
        result, findings = _launch_variant(variant)
        records.append(
            _publish_run(
                variant=variant,
                result=result,
                findings=findings,
                launcher_version=launcher_version,
                producer_version=producer_version,
            )
        )
    comparison = compare_role_runs(tuple(records))
    _publish_comparison(
        comparison_invocation,
        comparison,
        producer_version=producer_version,
    )
    return SweepResult(runs=tuple(records), comparison=comparison)


def _relative_artifact_path(value: Any) -> tuple[str, ...]:
    if not isinstance(value, str) or not value:
        _fail("invalid-sequence-link")
    parts = tuple(value.split("/"))
    if (
        "\\" in value
        or value.startswith("/")
        or any(part in {"", ".", ".."} for part in parts)
        or parts[0] in {"temp", ".skill-runs"}
    ):
        _fail("invalid-sequence-link")
    return parts


def _tree_snapshot(root: Path) -> tuple[tuple[Any, ...], ...]:
    records: list[tuple[Any, ...]] = []
    try:
        canonical = root.resolve(strict=True)
        for path in sorted(canonical.rglob("*")):
            relative = path.relative_to(canonical).as_posix()
            if path.is_symlink():
                _fail("invalid-sequence-link")
            if path.is_dir():
                records.append(("directory", relative))
            elif path.is_file():
                contents = path.read_bytes()
                records.append(
                    (
                        "file",
                        relative,
                        len(contents),
                        hashlib.sha256(contents).hexdigest(),
                    )
                )
            else:
                _fail("invalid-sequence-link")
    except RoleSweepError:
        raise
    except (OSError, ValueError):
        _fail("invalid-sequence-link")
    return tuple(records)


def _persisted_artifact(
    run: RoleRunRecord, *, hop_id: str, relative_path: str
) -> PersistedArtifact:
    _relative_artifact_path(relative_path)
    matches = [artifact for artifact in run.artifacts if artifact.path == relative_path]
    if len(matches) != 1:
        _fail("invalid-sequence-link")
    artifact = matches[0]
    try:
        root = run.output_root.resolve(strict=True)
        path = (root / relative_path).resolve(strict=True)
        if path.parent == root:
            contained = True
        else:
            path.relative_to(root)
            contained = True
        contents = path.read_bytes()
    except (OSError, ValueError):
        _fail("invalid-sequence-link")
    if (
        not contained
        or not path.is_file()
        or len(contents) != artifact.size
        or hashlib.sha256(contents).hexdigest() != artifact.sha256
    ):
        _fail("invalid-sequence-link")
    return PersistedArtifact(
        hop_id=hop_id,
        output_root=root,
        path=relative_path,
        sha256=artifact.sha256,
        size=artifact.size,
    )


def _validate_sequence_binding(
    binding: Any,
    prior: PersistedArtifact,
    previous_outputs: set[Path],
) -> BoundRoleLaunch:
    if not isinstance(binding, BoundRoleLaunch):
        _fail("invalid-sequence-link")
    matches = [
        item
        for item in binding.inputs
        if item.path == prior.path
        and item.sha256 == prior.sha256
        and item.size == prior.size
    ]
    if len(matches) != 1:
        _fail("invalid-sequence-link")
    selected = matches[0]
    roots = {
        role: root.resolve()
        for role, root in binding.invocation.inputs
        if role == selected.role
    }
    if roots != {selected.role: prior.output_root}:
        _fail("invalid-sequence-link")
    output = binding.invocation.output_root.resolve()
    for previous in previous_outputs:
        if output.is_relative_to(previous) or previous.is_relative_to(output):
            _fail("invalid-sequence-output")
    return binding


def run_role_sequence(
    *,
    first: SweepVariant,
    hops: tuple[SequenceHop, ...],
    launcher_version: str,
    producer_version: str,
) -> SequenceResult:
    """Run fresh role hops joined only by selected persisted ordinary files."""

    _validate_version(launcher_version)
    _validate_version(producer_version)
    if (
        not isinstance(first, SweepVariant)
        or not _valid_identifier(first.variant_id)
        or not isinstance(first.binding, BoundRoleLaunch)
        or type(hops) is not tuple
    ):
        _fail("invalid-sequence")
    hop_ids = {first.variant_id}
    for hop in hops:
        if (
            not isinstance(hop, SequenceHop)
            or not _valid_identifier(hop.hop_id)
            or hop.hop_id in hop_ids
            or not callable(hop.binder)
        ):
            _fail("invalid-sequence")
        _relative_artifact_path(hop.prior_artifact_path)
        hop_ids.add(hop.hop_id)

    records: list[RoleRunRecord] = []
    result, findings = _launch_variant(first)
    records.append(
        _publish_run(
            variant=first,
            result=result,
            findings=findings,
            launcher_version=launcher_version,
            producer_version=producer_version,
        )
    )
    if not result.success:
        return SequenceResult(status="failure", runs=tuple(records))

    previous_outputs = {records[0].output_root.resolve()}
    for hop in hops:
        prior_run = records[-1]
        prior = _persisted_artifact(
            prior_run,
            hop_id=prior_run.variant_id,
            relative_path=hop.prior_artifact_path,
        )
        prior_tree = _tree_snapshot(prior.output_root)
        try:
            binding = hop.binder(prior)
        except BaseException:
            _fail("invalid-sequence-link")
        binding = _validate_sequence_binding(binding, prior, previous_outputs)
        if _tree_snapshot(prior.output_root) != prior_tree:
            _fail("prior-output-mutated")
        variant = SweepVariant(variant_id=hop.hop_id, binding=binding)
        hop_result, hop_findings = _launch_variant(variant)
        if _tree_snapshot(prior.output_root) != prior_tree:
            hop_result = RoleLaunchResult(
                success=False,
                code="prior-output-mutated",
                artifacts=(),
            )
            hop_findings = ()
        record = _publish_run(
            variant=variant,
            result=hop_result,
            findings=hop_findings,
            launcher_version=launcher_version,
            producer_version=producer_version,
        )
        records.append(record)
        previous_outputs.add(record.output_root.resolve())
        if not hop_result.success:
            return SequenceResult(status="failure", runs=tuple(records))
    return SequenceResult(status="complete", runs=tuple(records))
