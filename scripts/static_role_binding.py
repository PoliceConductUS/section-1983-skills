"""Protected static-role validation and immutable profile binding."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from typing import Any

from scripts.immutable_folder_package import ValidatedFolderPackage


_IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class RoleBindingError(ValueError):
    """A bounded static-role/profile binding failure."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class ValidatedStaticRoleContract:
    role_kind: str
    accepted_profile_kinds: tuple[str, ...]
    freshness_basis: str
    max_age_days: int
    capabilities: tuple[str, ...]
    prohibitions: tuple[str, ...]
    internet: str
    target_mutation: str
    output: str
    canonical_bytes: bytes


@dataclass(frozen=True)
class RoleProfileBinding:
    role_contract: ValidatedStaticRoleContract
    profile: ValidatedFolderPackage
    as_of: str


def _fail(code: str) -> None:
    raise RoleBindingError(code)


def _identifier(value: Any) -> bool:
    return isinstance(value, str) and _IDENTIFIER.fullmatch(value) is not None


def _identifier_list(value: Any, *, empty: bool) -> tuple[str, ...]:
    if (
        type(value) is not list
        or (not empty and not value)
        or any(not _identifier(item) for item in value)
        or len(set(value)) != len(value)
    ):
        _fail("invalid-static-role-contract")
    return tuple(value)


def _canonical_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError):
        _fail("invalid-static-role-contract")


def validate_static_role_contract(value: Any) -> ValidatedStaticRoleContract:
    """Validate one protected role contract without consulting profile data."""
    required = {
        "schema_version",
        "role_kind",
        "accepted_profile_kinds",
        "freshness_policy",
        "capabilities",
        "prohibitions",
        "internet",
        "target_mutation",
        "output",
    }
    if (
        type(value) is not dict
        or set(value) != required
        or type(value["schema_version"]) is not int
        or value["schema_version"] != 1
        or not _identifier(value["role_kind"])
        or value["internet"] not in {"disabled", "enabled"}
        or value["target_mutation"] != "forbidden"
        or not _identifier(value["output"])
    ):
        _fail("invalid-static-role-contract")
    accepted = _identifier_list(value["accepted_profile_kinds"], empty=False)
    capabilities = _identifier_list(value["capabilities"], empty=True)
    prohibitions = _identifier_list(value["prohibitions"], empty=False)
    policy = value["freshness_policy"]
    if (
        type(policy) is not dict
        or set(policy) != {"basis", "max_age_days"}
        or policy["basis"] not in {"checked_through", "retrieved_on"}
        or type(policy["max_age_days"]) is not int
        or policy["max_age_days"] < 0
    ):
        _fail("invalid-static-role-contract")
    return ValidatedStaticRoleContract(
        role_kind=value["role_kind"],
        accepted_profile_kinds=accepted,
        freshness_basis=policy["basis"],
        max_age_days=policy["max_age_days"],
        capabilities=capabilities,
        prohibitions=prohibitions,
        internet=value["internet"],
        target_mutation=value["target_mutation"],
        output=value["output"],
        canonical_bytes=_canonical_bytes(value),
    )


def bind_role_profile(
    contract: ValidatedStaticRoleContract,
    package: ValidatedFolderPackage,
    *,
    as_of: str,
) -> RoleProfileBinding:
    """Bind a protected static role to a compatible immutable profile snapshot."""
    if not isinstance(contract, ValidatedStaticRoleContract):
        _fail("invalid-static-role-contract")
    if not isinstance(package, ValidatedFolderPackage):
        _fail("invalid-profile-package")
    if package.package_kind not in contract.accepted_profile_kinds:
        _fail("incompatible-profile-kind")
    try:
        selected_date = date.fromisoformat(as_of)
        if selected_date.isoformat() != as_of:
            _fail("invalid-binding-date")
    except (TypeError, ValueError):
        _fail("invalid-binding-date")
    freshness = package.freshness[contract.freshness_basis]
    if freshness is None:
        _fail("missing-profile-freshness")
    try:
        freshness_date = date.fromisoformat(freshness)
    except ValueError:
        _fail("invalid-profile-freshness")
    if (selected_date - freshness_date).days > contract.max_age_days:
        _fail("stale-profile-package")
    return RoleProfileBinding(
        role_contract=contract,
        profile=package,
        as_of=as_of,
    )
