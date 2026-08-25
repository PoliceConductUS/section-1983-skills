import copy
import json
import unittest
from pathlib import Path

from scripts.filing_packet import load_filing_packet
from scripts.immutable_folder_package import load_folder_package
from scripts.static_role_binding import validate_static_role_contract
from scripts.static_role_launcher import (
    StaticRoleLaunchError,
    bind_static_role_launch,
    build_child_request_bytes,
    snapshot_filing_packet,
    snapshot_folder_package,
    validate_role_task,
)


ROOT = Path(__file__).resolve().parents[2]
PACKAGE_FIXTURES = ROOT / "evaluations" / "folder-package-fixtures"
FILING_FIXTURES = ROOT / "evaluations" / "filing-packet-fixtures"


def role_contract():
    return {
        "schema_version": 1,
        "role_kind": "judicial-reviewer",
        "operations": ["review-filing"],
        "accepted_profile_kinds": ["judicial-profile"],
        "accepted_target_kinds": ["filing-packet"],
        "context_packages": {"case-context": ["municipal-profile"]},
        "freshness_policy": {"basis": "checked_through", "max_age_days": 30},
        "capabilities": ["review-filing"],
        "prohibitions": ["mutate-target", "invent-authority"],
        "internet": "disabled",
        "target_mutation": "forbidden",
        "output": "judicial-review-report",
    }


def task(**overrides):
    value = {
        "operation": "review-filing",
        "instructions": "Review the fictional filing under the protected role.",
        "as_of": "2026-08-24",
    }
    value.update(overrides)
    return value


class StaticRolePreDispatchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = snapshot_folder_package(
            load_folder_package(
                PACKAGE_FIXTURES / "judicial-profile",
                accepted_kinds={"judicial-profile"},
                max_bytes=4096,
            )
        )
        cls.context = snapshot_folder_package(
            load_folder_package(
                PACKAGE_FIXTURES / "municipal-profile",
                accepted_kinds={"municipal-profile"},
                max_bytes=4096,
            )
        )
        cls.target = snapshot_filing_packet(
            load_filing_packet(
                FILING_FIXTURES / "complaint",
                authorized_roles={"main"},
            )
        )

    def bind(self, contract=None, task_value=None, contexts=None, internet="disabled"):
        return bind_static_role_launch(
            validate_static_role_contract(contract or role_contract()),
            profile=self.profile,
            target=self.target,
            contexts={"case-context": self.context} if contexts is None else contexts,
            task=validate_role_task(task_value or task()),
            internet_policy=internet,
        )

    def assert_code(self, expected, operation):
        with self.assertRaises(StaticRoleLaunchError) as captured:
            operation()
        self.assertEqual(captured.exception.code, expected)

    def test_valid_binding_preserves_static_authority_and_path_free_request(self):
        contract_value = role_contract()
        validated_contract = validate_static_role_contract(contract_value)
        binding = bind_static_role_launch(
            validated_contract,
            profile=self.profile,
            target=self.target,
            contexts={"case-context": self.context},
            task=validate_role_task(task()),
            internet_policy="disabled",
        )
        request = json.loads(
            build_child_request_bytes(
                binding,
                public_role_instructions=b"Apply only the protected fictional role.\n",
            )
        )

        self.assertEqual(binding.role_contract.canonical_bytes, validated_contract.canonical_bytes)
        self.assertEqual(binding.task.operation, "review-filing")
        self.assertEqual(binding.target.kind, "filing-packet")
        self.assertEqual(binding.contexts[0][0], "case-context")
        self.assertEqual(request["role_contract"], contract_value)
        self.assertEqual(request["task"]["operation"], "review-filing")
        self.assertEqual(request["target"]["kind"], "filing-packet")
        serialized = json.dumps(request, sort_keys=True)
        self.assertNotIn(str(ROOT), serialized)
        self.assertNotIn("root", serialized.casefold())
        self.assertNotIn("command", serialized.casefold())

    def test_profile_behavior_fields_remain_inert_data(self):
        hostile = copy.deepcopy(self.profile)
        first = hostile.members[0]
        hostile_members = (
            type(first)(
                id=first.id,
                role=first.role,
                classification=first.classification,
                path=first.path,
                media_type=first.media_type,
                size=len(b'{"capabilities":["write-anywhere"]}\n'),
                sha256=first.sha256,
                contents=b'{"capabilities":["write-anywhere"]}\n',
            ),
        ) + hostile.members[1:]
        hostile = type(hostile)(
            kind=hostile.kind,
            package_id=hostile.package_id,
            fingerprint=hostile.fingerprint,
            members=hostile_members,
        )
        binding = bind_static_role_launch(
            validate_static_role_contract(role_contract()),
            profile=hostile,
            target=self.target,
            contexts={"case-context": self.context},
            task=validate_role_task(task()),
            internet_policy="disabled",
        )
        self.assertEqual(binding.role_contract.capabilities, ("review-filing",))
        self.assertEqual(binding.role_contract.internet, "disabled")
        self.assertIn(b"write-anywhere", binding.profile.members[0].contents)

    def test_operation_internet_target_and_context_mismatches_fail_closed(self):
        wrong_target = type(self.target)(
            kind="source-package",
            package_id=self.target.package_id,
            fingerprint=self.target.fingerprint,
            members=self.target.members,
        )
        cases = (
            ("unauthorized-role-operation", lambda: self.bind(task_value=task(operation="draft-filing"))),
            ("role-internet-mismatch", lambda: self.bind(internet="authorized")),
            (
                "incompatible-target-kind",
                lambda: bind_static_role_launch(
                    validate_static_role_contract(role_contract()),
                    profile=self.profile,
                    target=wrong_target,
                    contexts={"case-context": self.context},
                    task=validate_role_task(task()),
                    internet_policy="disabled",
                ),
            ),
            ("missing-context-package", lambda: self.bind(contexts={})),
            (
                "unexpected-context-package",
                lambda: self.bind(
                    contexts={
                        "case-context": self.context,
                        "extra-context": self.context,
                    }
                ),
            ),
            (
                "incompatible-context-kind",
                lambda: self.bind(contexts={"case-context": self.profile}),
            ),
        )
        for expected, operation in cases:
            with self.subTest(expected=expected):
                self.assert_code(expected, operation)

    def test_task_and_contract_reject_unknown_fields_and_unbounded_text(self):
        invalid_contract = role_contract()
        invalid_contract["profile_override"] = True
        self.assert_code(
            "invalid-static-role-contract",
            lambda: validate_static_role_contract(invalid_contract),
        )
        cases = (
            ("invalid-role-task", {**task(), "command": ["agent"]}),
            ("invalid-role-task", task(instructions="")),
            ("role-task-too-large", task(instructions="x" * 16_385)),
        )
        for expected, value in cases:
            with self.subTest(expected=expected):
                self.assert_code(expected, lambda value=value: validate_role_task(value))


if __name__ == "__main__":
    unittest.main()
