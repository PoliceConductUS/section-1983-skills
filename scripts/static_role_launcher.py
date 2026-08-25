"""Trusted-host static-role launch boundary for declared folder inputs."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from scripts.validate_folder_invocation import (
    InvocationError,
    ValidatedInvocation,
    resolve_input_path,
)


_IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_MAX_TASK_BYTES = 16_384
_MAX_ROLE_INSTRUCTION_BYTES = 65_536
_MAX_ARTIFACTS = 32
_MAX_ARTIFACT_BYTES = 1_048_576


class RoleLaunchError(ValueError):
    """A bounded static-role launcher contract failure."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _fail(code: str) -> None:
    raise RoleLaunchError(code)


def _identifier(value: Any) -> bool:
    return isinstance(value, str) and _IDENTIFIER.fullmatch(value) is not None


def _identifier_tuple(value: Any, *, empty: bool) -> bool:
    return (
        type(value) is tuple
        and (empty or bool(value))
        and all(_identifier(item) for item in value)
        and len(value) == len(set(value))
    )


def _relative_parts(value: Any, code: str) -> tuple[str, ...]:
    if not isinstance(value, str) or not value:
        _fail(code)
    segments = value.split("/")
    if (
        "\\" in value
        or "\x00" in value
        or value.startswith("/")
        or re.match(r"^[A-Za-z]:/", value) is not None
        or any(segment in {"", ".", ".."} for segment in segments)
    ):
        _fail(code)
    return tuple(segments)


def _valid_run_id(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError):
        return False
    return parsed.version == 4 and str(parsed) == value


@dataclass(frozen=True)
class AdapterAttestation:
    fixed_adapter: bool
    fresh_process: bool
    scrubbed_session: bool
    undeclared_filesystem_denied: bool
    network_enforced: bool
    capabilities_enforced: bool


@dataclass(frozen=True)
class AdapterResult:
    stdout: bytes
    stderr: bytes
    exit_code: int
    timed_out: bool


@dataclass(frozen=True)
class InputRequirement:
    purpose: str
    roles: tuple[str, ...]
    min_files: int
    max_files: int


@dataclass(frozen=True)
class InputSelection:
    purpose: str
    role: str
    path: str


@dataclass(frozen=True)
class RoleTask:
    operation: str
    instructions: str


@dataclass(frozen=True)
class ProposedArtifact:
    path: str
    contents: bytes


@dataclass(frozen=True)
class SelectedInputSnapshot:
    purpose: str
    role: str
    path: str
    logical_name: str
    sha256: str
    size: int
    contents: bytes


@dataclass(frozen=True)
class RoleLaunchDefinition:
    role_id: str
    operations: tuple[str, ...]
    input_requirements: tuple[InputRequirement, ...]
    capabilities: tuple[str, ...]
    prohibitions: tuple[str, ...]
    internet: str
    target_mutation: str
    output_kind: str
    public_instructions: bytes
    adapter: Any
    output_validator: Callable[[Any], tuple[ProposedArtifact, ...]]
    max_stdout_bytes: int
    max_stderr_bytes: int


@dataclass(frozen=True)
class BoundRoleLaunch:
    definition: RoleLaunchDefinition
    invocation: ValidatedInvocation
    task: RoleTask
    selections: tuple[InputSelection, ...]
    inputs: tuple[SelectedInputSnapshot, ...]


@dataclass(frozen=True)
class RoleLaunchResult:
    success: bool
    code: str
    artifacts: tuple[ProposedArtifact, ...]


def validate_role_task(value: Any) -> RoleTask:
    if type(value) is not dict or set(value) != {"operation", "instructions"}:
        _fail("invalid-role-task")
    operation = value["operation"]
    instructions = value["instructions"]
    if not _identifier(operation) or not isinstance(instructions, str) or not instructions.strip():
        _fail("invalid-role-task")
    try:
        encoded = instructions.encode("utf-8")
    except UnicodeError:
        _fail("invalid-role-task")
    if len(encoded) > _MAX_TASK_BYTES:
        _fail("role-task-too-large")
    return RoleTask(operation=operation, instructions=instructions)


def _validate_definition(definition: RoleLaunchDefinition) -> None:
    if (
        not isinstance(definition, RoleLaunchDefinition)
        or not _identifier(definition.role_id)
        or not _identifier_tuple(definition.operations, empty=False)
        or not _identifier_tuple(definition.capabilities, empty=True)
        or not _identifier_tuple(definition.prohibitions, empty=False)
        or definition.internet not in {"disabled", "authorized"}
        or definition.target_mutation != "forbidden"
        or not _identifier(definition.output_kind)
        or type(definition.public_instructions) is not bytes
        or not definition.public_instructions
        or len(definition.public_instructions) > _MAX_ROLE_INSTRUCTION_BYTES
        or not callable(definition.output_validator)
        or not callable(getattr(definition.adapter, "attest", None))
        or not callable(getattr(definition.adapter, "launch", None))
        or type(definition.max_stdout_bytes) is not int
        or definition.max_stdout_bytes < 1
        or type(definition.max_stderr_bytes) is not int
        or definition.max_stderr_bytes < 1
        or type(definition.input_requirements) is not tuple
        or not definition.input_requirements
    ):
        _fail("invalid-role-definition")
    try:
        definition.public_instructions.decode("utf-8")
    except UnicodeError:
        _fail("invalid-role-definition")

    purposes: set[str] = set()
    for requirement in definition.input_requirements:
        if (
            not isinstance(requirement, InputRequirement)
            or not _identifier(requirement.purpose)
            or requirement.purpose in purposes
            or not _identifier_tuple(requirement.roles, empty=False)
            or type(requirement.min_files) is not int
            or type(requirement.max_files) is not int
            or requirement.min_files < 0
            or requirement.max_files < requirement.min_files
        ):
            _fail("invalid-role-definition")
        purposes.add(requirement.purpose)


def _snapshot_selection(
    invocation: ValidatedInvocation,
    selection: InputSelection,
    *,
    remaining_bytes: int,
) -> SelectedInputSnapshot:
    if (
        not isinstance(selection, InputSelection)
        or not _identifier(selection.purpose)
        or not _identifier(selection.role)
    ):
        _fail("invalid-input-selection")
    _relative_parts(selection.path, "invalid-input-selection")
    try:
        path = resolve_input_path(invocation, selection.role, selection.path)
        if not path.is_file():
            _fail("invalid-input-selection")
        size = path.stat().st_size
        if size > remaining_bytes:
            _fail("role-input-byte-limit")
        with path.open("rb") as source:
            contents = source.read(size + 1)
    except RoleLaunchError:
        raise
    except (InvocationError, OSError, ValueError):
        _fail("invalid-input-selection")
    if len(contents) != size:
        _fail("selected-input-mutated")
    try:
        contents.decode("utf-8")
    except UnicodeError:
        _fail("child-input-not-utf8")
    return SelectedInputSnapshot(
        purpose=selection.purpose,
        role=selection.role,
        path=selection.path,
        logical_name=f"{selection.role}:{selection.path}",
        sha256=hashlib.sha256(contents).hexdigest(),
        size=size,
        contents=contents,
    )


def bind_role_launch(
    definition: RoleLaunchDefinition,
    *,
    invocation: ValidatedInvocation,
    task: RoleTask,
    selections: tuple[InputSelection, ...],
) -> BoundRoleLaunch:
    _validate_definition(definition)
    if not isinstance(invocation, ValidatedInvocation) or not isinstance(task, RoleTask):
        _fail("invalid-role-binding")
    if task.operation not in definition.operations:
        _fail("unauthorized-role-operation")
    if invocation.internet != definition.internet:
        _fail("role-internet-mismatch")
    if type(selections) is not tuple or not selections:
        _fail("invalid-input-selection")

    requirements = {item.purpose: item for item in definition.input_requirements}
    counts = {purpose: 0 for purpose in requirements}
    seen: set[tuple[str, str, str]] = set()
    for selection in selections:
        if not isinstance(selection, InputSelection):
            _fail("invalid-input-selection")
        requirement = requirements.get(selection.purpose)
        if requirement is None:
            _fail("unexpected-role-input")
        if selection.role not in requirement.roles:
            _fail("incompatible-input-role")
        identity = (selection.purpose, selection.role, selection.path)
        if identity in seen:
            _fail("invalid-input-selection")
        seen.add(identity)
        counts[selection.purpose] += 1
    for purpose, requirement in requirements.items():
        if counts[purpose] < requirement.min_files:
            _fail("missing-role-input")
        if counts[purpose] > requirement.max_files:
            _fail("too-many-role-inputs")

    remaining = invocation.runtime["max_input_bytes"]
    snapshots: list[SelectedInputSnapshot] = []
    for selection in selections:
        snapshot = _snapshot_selection(
            invocation, selection, remaining_bytes=remaining
        )
        remaining -= snapshot.size
        snapshots.append(snapshot)
    return BoundRoleLaunch(
        definition=definition,
        invocation=invocation,
        task=task,
        selections=selections,
        inputs=tuple(snapshots),
    )


def _role_object(definition: RoleLaunchDefinition) -> dict[str, Any]:
    return {
        "capabilities": list(definition.capabilities),
        "input_requirements": [
            {
                "max_files": item.max_files,
                "min_files": item.min_files,
                "purpose": item.purpose,
                "roles": list(item.roles),
            }
            for item in definition.input_requirements
        ],
        "internet": definition.internet,
        "operations": list(definition.operations),
        "output_kind": definition.output_kind,
        "prohibitions": list(definition.prohibitions),
        "public_instructions": definition.public_instructions.decode("utf-8"),
        "role_id": definition.role_id,
        "target_mutation": definition.target_mutation,
    }


def build_child_request_bytes(binding: BoundRoleLaunch) -> bytes:
    if not isinstance(binding, BoundRoleLaunch):
        _fail("invalid-role-binding")
    value = {
        "inputs": [
            {
                "contents": item.contents.decode("utf-8"),
                "logical_name": item.logical_name,
                "purpose": item.purpose,
                "role": item.role,
                "sha256": item.sha256,
                "size": item.size,
            }
            for item in binding.inputs
        ],
        "role": _role_object(binding.definition),
        "task": {
            "instructions": binding.task.instructions,
            "operation": binding.task.operation,
        },
    }
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def validate_advisory_output(
    value: Any, *, expected_kind: str
) -> tuple[ProposedArtifact, ...]:
    if (
        not _identifier(expected_kind)
        or type(value) is not dict
        or set(value) != {"output_kind", "artifacts"}
        or value["output_kind"] != expected_kind
        or type(value["artifacts"]) is not list
        or not value["artifacts"]
        or len(value["artifacts"]) > _MAX_ARTIFACTS
    ):
        _fail("child-output-invalid")
    artifacts: list[ProposedArtifact] = []
    paths: set[str] = set()
    total = 0
    for item in value["artifacts"]:
        if type(item) is not dict or set(item) != {"path", "contents"}:
            _fail("child-output-invalid")
        path = item["path"]
        contents = item["contents"]
        parts = _relative_parts(path, "child-output-invalid")
        if parts[0].casefold() == "temp" or not isinstance(contents, str):
            _fail("child-output-invalid")
        try:
            encoded = contents.encode("utf-8")
        except UnicodeError:
            _fail("child-output-invalid")
        total += len(encoded)
        if total > _MAX_ARTIFACT_BYTES or path in paths:
            _fail("child-output-invalid")
        paths.add(path)
        artifacts.append(ProposedArtifact(path=path, contents=encoded))
    return tuple(artifacts)


def _attestation_valid(value: Any) -> bool:
    return isinstance(value, AdapterAttestation) and all(
        field is True
        for field in (
            value.fixed_adapter,
            value.fresh_process,
            value.scrubbed_session,
            value.undeclared_filesystem_denied,
            value.network_enforced,
            value.capabilities_enforced,
        )
    )


def _create_workspace(invocation: ValidatedInvocation, run_id: str) -> Path:
    if not _valid_run_id(run_id):
        _fail("invalid-run-id")
    output = invocation.output_root
    temp = output / "temp"
    try:
        if temp.exists() or temp.is_symlink():
            if temp.is_symlink() or not temp.is_dir() or temp.resolve() != temp:
                _fail("isolation-unavailable")
        else:
            temp.mkdir(mode=0o700)
        workspace = temp / run_id
        workspace.mkdir(mode=0o700)
        if workspace.resolve() != workspace or any(workspace.iterdir()):
            _fail("isolation-unavailable")
        return workspace
    except RoleLaunchError:
        raise
    except OSError:
        _fail("isolation-unavailable")


def _remove_workspace(workspace: Path) -> None:
    try:
        temp = workspace.parent.resolve(strict=True)
        output = temp.parent.resolve(strict=True)
        if (
            temp.name != "temp"
            or workspace.parent != temp
            or workspace == temp
            or output == temp
        ):
            return
        shutil.rmtree(workspace)
    except OSError:
        pass


def _inputs_unchanged(binding: BoundRoleLaunch) -> bool:
    for selection, expected in zip(binding.selections, binding.inputs, strict=True):
        try:
            current = _snapshot_selection(
                binding.invocation,
                selection,
                remaining_bytes=binding.invocation.runtime["max_input_bytes"],
            )
        except RoleLaunchError:
            return False
        if current.size != expected.size or current.sha256 != expected.sha256:
            return False
    return True


def _failure(code: str) -> RoleLaunchResult:
    return RoleLaunchResult(success=False, code=code, artifacts=())


def launch_static_role(binding: BoundRoleLaunch, *, run_id: str) -> RoleLaunchResult:
    if not isinstance(binding, BoundRoleLaunch):
        _fail("invalid-role-binding")
    try:
        attestation = binding.definition.adapter.attest()
    except BaseException:
        return _failure("isolation-unavailable")
    if not _attestation_valid(attestation):
        return _failure("isolation-unavailable")

    workspace: Path | None = None
    try:
        workspace = _create_workspace(binding.invocation, run_id)
        workspace_string = str(workspace)
        environment = {
            "TMPDIR": workspace_string,
            "TMP": workspace_string,
            "TEMP": workspace_string,
        }
        request = build_child_request_bytes(binding)
        try:
            response = binding.definition.adapter.launch(
                request=request,
                cwd=workspace_string,
                environment=environment,
                max_seconds=binding.invocation.runtime["max_seconds"],
                max_stdout_bytes=binding.definition.max_stdout_bytes,
                max_stderr_bytes=binding.definition.max_stderr_bytes,
                visible_entries=tuple(item.name for item in workspace.iterdir()),
            )
        except BaseException:
            return _failure("adapter-failed")
        if not _inputs_unchanged(binding):
            return _failure("selected-input-mutated")
        if not isinstance(response, AdapterResult):
            return _failure("adapter-failed")
        if response.timed_out:
            return _failure("child-timeout")
        if type(response.stdout) is not bytes or type(response.stderr) is not bytes:
            return _failure("adapter-failed")
        if len(response.stdout) > binding.definition.max_stdout_bytes:
            return _failure("child-stdout-too-large")
        if len(response.stderr) > binding.definition.max_stderr_bytes:
            return _failure("child-stderr-too-large")
        if type(response.exit_code) is not int or response.exit_code != 0:
            return _failure("child-nonzero-exit")
        try:
            text = response.stdout.decode("utf-8")
        except UnicodeError:
            return _failure("child-output-not-utf8")
        try:
            value = json.loads(text)
        except (ValueError, json.JSONDecodeError):
            return _failure("child-output-not-json")
        try:
            artifacts = binding.definition.output_validator(value)
        except BaseException:
            return _failure("child-output-invalid")
        if (
            type(artifacts) is not tuple
            or not artifacts
            or any(not isinstance(item, ProposedArtifact) for item in artifacts)
        ):
            return _failure("child-output-invalid")
        return RoleLaunchResult(success=True, code="success", artifacts=artifacts)
    except RoleLaunchError as error:
        return _failure(error.code)
    finally:
        if workspace is not None:
            _remove_workspace(workspace)
