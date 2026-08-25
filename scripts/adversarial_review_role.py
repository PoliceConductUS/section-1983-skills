"""Protected adversarial-review role for the declared-folder launcher."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from types import ModuleType
from typing import Any

from scripts.static_role_launcher import (
    InputRequirement,
    ProposedArtifact,
    RoleLaunchDefinition,
    RoleLaunchError,
)


_REPOSITORY = Path(__file__).resolve().parents[1]
_ROLE_INSTRUCTIONS = (
    _REPOSITORY
    / "skills"
    / "adversarial-filing-review"
    / "references"
    / "static-role-instructions.md"
)
_DOMAIN_RUNTIME = (
    _REPOSITORY
    / "skills"
    / "adversarial-filing-review"
    / "scripts"
    / "launch_review.py"
)
_SOURCE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_MAX_SOURCE_IDS = 64


def _invalid_definition() -> None:
    raise RoleLaunchError("invalid-role-definition")


def _load_domain_runtime() -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        "_section_1983_adversarial_review_domain", _DOMAIN_RUNTIME
    )
    if specification is None or specification.loader is None:
        _invalid_definition()
    module = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(module)
    except (ImportError, OSError, SyntaxError):
        _invalid_definition()
    return module


def _public_instructions() -> bytes:
    try:
        contents = _ROLE_INSTRUCTIONS.read_bytes()
        contents.decode("utf-8")
    except (OSError, UnicodeError):
        _invalid_definition()
    if not contents:
        _invalid_definition()
    return contents


def _approved_source_ids(values: Any) -> tuple[str, ...]:
    if (
        type(values) is not tuple
        or not values
        or len(values) > _MAX_SOURCE_IDS
        or len(values) != len(set(values))
        or any(
            not isinstance(value, str) or _SOURCE_ID.fullmatch(value) is None
            for value in values
        )
    ):
        _invalid_definition()
    return values


def build_adversarial_review_definition(
    *, adapter: Any, approved_source_ids: tuple[str, ...]
) -> RoleLaunchDefinition:
    """Build the fixed role around host-validated folder source identities."""

    source_ids = _approved_source_ids(approved_source_ids)
    domain = _load_domain_runtime()

    def validate_output(value: Any) -> tuple[ProposedArtifact, ...]:
        if (
            type(value) is not dict
            or set(value) != {"output_kind", "review"}
            or value["output_kind"] != "adversarial-filing-review"
        ):
            raise RoleLaunchError("child-output-invalid")
        domain.validate_review_response(value["review"], set(source_ids))
        report = domain.render_review_markdown(
            value["review"],
            {
                "outcome": "completed",
                "runtime": "shared-static-role",
                "source_ids": list(source_ids),
            },
        ).encode("utf-8")
        return (
            ProposedArtifact(
                path="reports/adversarial-filing-review.md",
                contents=report,
            ),
        )

    return RoleLaunchDefinition(
        role_id="adversarial-filing-reviewer",
        operations=("review-filing",),
        input_requirements=(
            InputRequirement("filing-target", ("filing",), 1, 1),
            InputRequirement(
                "approved-source", ("approved-sources",), 1, _MAX_SOURCE_IDS
            ),
            InputRequirement(
                "source-documentation", ("approved-sources",), 1, _MAX_SOURCE_IDS
            ),
        ),
        capabilities=(),
        prohibitions=(
            "mutate-target",
            "decide-plaintiff-strategy",
            "invent-authority",
            "claim-filing-readiness",
            "remediate-filing",
        ),
        internet="authorized",
        target_mutation="forbidden",
        output_kind="adversarial-filing-review",
        public_instructions=_public_instructions(),
        adapter=adapter,
        output_validator=validate_output,
        max_stdout_bytes=1_000_000,
        max_stderr_bytes=8_192,
    )
