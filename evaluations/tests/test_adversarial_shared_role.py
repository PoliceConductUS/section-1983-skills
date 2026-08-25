import hashlib
import json
import tempfile
import unittest
import uuid
from pathlib import Path

from scripts.adversarial_review_role import (
    build_adversarial_review_definition,
    load_approved_source_records,
)
from scripts.static_role_launcher import (
    AdapterAttestation,
    AdapterResult,
    InputSelection,
    RoleLaunchError,
    bind_role_launch,
    build_child_request_bytes,
    launch_static_role,
    validate_role_task,
)
from scripts.validate_folder_invocation import validate_invocation


def finding(finding_id, *, correction=None, plaintiff_decision=None):
    return {
        "id": finding_id,
        "attacked_quote": "Bounded allegation.",
        "location": "Synthetic filing, paragraph 1",
        "source_ids": ["SRC-1"],
        "attack": "The allegation omits a source-supported date.",
        "consequence": "The chronology is vulnerable.",
        "status": "open",
        "correction": correction,
        "plaintiff_decision": plaintiff_decision,
    }


def valid_review():
    return {
        "Fatal Defects": [
            finding(
                "FATAL-001",
                correction={
                    "replace": "Bounded allegation.",
                    "with": "On January 15, 2026, the bounded event occurred.",
                },
            )
        ],
        "Credible Opposition Arguments": [
            finding(
                "ARG-001",
                plaintiff_decision={
                    "question": "Whether to retain the synthetic theory",
                    "choices": [
                        {
                            "option": "Retain it",
                            "consequence": "The identified attack remains.",
                        },
                        {
                            "option": "Omit it",
                            "consequence": "The theory is removed.",
                        },
                    ],
                },
            )
        ],
        "Factual Disputes": [],
        "Discovery Issues": [],
        "Style Complaints": [],
    }


class FakeAdapter:
    def __init__(self, value=None, *, error=None):
        self.value = value or {
            "output_kind": "adversarial-filing-review",
            "review": valid_review(),
        }
        self.error = error
        self.calls = []

    def attest(self):
        return AdapterAttestation(
            fixed_adapter=True,
            fresh_process=True,
            scrubbed_session=True,
            undeclared_filesystem_denied=True,
            network_enforced=True,
            capabilities_enforced=True,
        )

    def launch(self, **kwargs):
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        return AdapterResult(
            stdout=json.dumps(self.value, sort_keys=True).encode("utf-8"),
            stderr=b"",
            exit_code=0,
            timed_out=False,
        )


class AdversarialSharedRoleTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.filing = self.root / "filing"
        self.sources = self.root / "approved-sources"
        self.output = self.root / "output"
        for path in (self.filing, self.sources, self.output):
            path.mkdir()
        (self.filing / "motion.md").write_text(
            "# Synthetic filing\n\nBounded allegation.\n", encoding="utf-8"
        )
        (self.sources / "record.txt").write_text(
            "Synthetic approved record.\n", encoding="utf-8"
        )
        source_hash = hashlib.sha256(
            (self.sources / "record.txt").read_bytes()
        ).hexdigest()
        (self.sources / "SOURCE.yaml").write_text(
            "schema_version: 1\n"
            "source_id: SRC-1\n"
            "role: record\n"
            "path: record.txt\n"
            f"sha256: {source_hash}\n"
            "checked_through: 2026-08-25\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temporary_directory.cleanup()

    def invocation(self):
        return validate_invocation(
            {
                "version": 1,
                "skill": "adversarial-filing-review",
                "inputs": [
                    {"role": "filing", "root": str(self.filing)},
                    {"role": "approved-sources", "root": str(self.sources)},
                ],
                "output": {"root": str(self.output)},
                "runtime": {"max_seconds": 60, "max_input_bytes": 1_048_576},
                "internet": "authorized",
                "isolation": {
                    "inputs": "read-only",
                    "output": "read-write",
                    "undeclared": "none",
                },
            }
        )

    @staticmethod
    def selections():
        return (
            InputSelection("filing-target", "filing", "motion.md"),
            InputSelection("approved-source", "approved-sources", "record.txt"),
            InputSelection(
                "source-documentation", "approved-sources", "SOURCE.yaml"
            ),
        )

    def binding(self, adapter):
        invocation = self.invocation()
        records = load_approved_source_records(
            invocation=invocation,
            documentation_paths=("SOURCE.yaml",),
            minimum_checked_through="2026-08-01",
        )
        return bind_role_launch(
            build_adversarial_review_definition(
                adapter=adapter,
                approved_sources=records,
            ),
            invocation=invocation,
            task=validate_role_task(
                {
                    "operation": "review-filing",
                    "instructions": "Review the selected synthetic filing.",
                }
            ),
            selections=self.selections(),
        )

    def test_definition_uses_only_declared_folder_files_and_fixed_role_behavior(self):
        adapter = FakeAdapter()
        binding = self.binding(adapter)
        request_bytes = build_child_request_bytes(binding)
        request = json.loads(request_bytes)

        self.assertEqual(binding.definition.role_id, "adversarial-filing-reviewer")
        self.assertEqual(binding.definition.capabilities, ())
        self.assertEqual(binding.definition.internet, "authorized")
        self.assertEqual(binding.definition.target_mutation, "forbidden")
        self.assertEqual(
            [item["purpose"] for item in request["inputs"]],
            ["filing-target", "approved-source", "source-documentation"],
        )
        self.assertIn("source_id: SRC-1", request["inputs"][2]["contents"])
        self.assertNotIn("package", request["role"]["public_instructions"].casefold())
        self.assertNotIn("graph", request["role"]["public_instructions"].casefold())
        for path in (self.filing, self.sources, self.output, self.root):
            self.assertNotIn(str(path.resolve()), request_bytes.decode("utf-8"))

    def test_five_category_review_renders_advisory_report_without_mutating_inputs(self):
        adapter = FakeAdapter()
        before = {
            path.relative_to(self.root).as_posix(): path.read_bytes()
            for path in self.root.rglob("*")
            if path.is_file()
        }

        result = launch_static_role(self.binding(adapter), run_id=str(uuid.uuid4()))

        self.assertTrue(result.success)
        self.assertEqual(result.code, "success")
        self.assertEqual(len(result.artifacts), 1)
        self.assertEqual(
            result.artifacts[0].path,
            "reports/adversarial-filing-review.md",
        )
        report = result.artifacts[0].contents.decode("utf-8")
        for heading in (
            "Fatal Defects",
            "Credible Opposition Arguments",
            "Factual Disputes",
            "Discovery Issues",
            "Style Complaints",
        ):
            self.assertIn(f"## {heading}", report)
        self.assertIn("Replace: Bounded allegation.", report)
        self.assertIn("PLAINTIFF DECISION REQUIRED", report)
        self.assertEqual(
            before,
            {
                path.relative_to(self.root).as_posix(): path.read_bytes()
                for path in self.root.rglob("*")
                if path.is_file()
            },
        )
        self.assertFalse((self.output / "temp").joinpath("unused").exists())

    def test_invalid_review_and_provider_failure_remain_bounded(self):
        invalid = valid_review()
        invalid.pop("Style Complaints")
        invalid_result = launch_static_role(
            self.binding(
                FakeAdapter(
                    {
                        "output_kind": "adversarial-filing-review",
                        "review": invalid,
                    }
                )
            ),
            run_id=str(uuid.uuid4()),
        )
        provider_result = launch_static_role(
            self.binding(FakeAdapter(error=OSError(str(self.root)))),
            run_id=str(uuid.uuid4()),
        )

        self.assertEqual((invalid_result.success, invalid_result.code), (False, "child-output-invalid"))
        self.assertEqual((provider_result.success, provider_result.code), (False, "adapter-failed"))
        self.assertNotIn(str(self.root), invalid_result.code)
        self.assertNotIn(str(self.root), provider_result.code)

    def test_source_documentation_hash_and_checked_through_fail_before_dispatch(self):
        cases = (
            (
                "source-content-mismatch",
                lambda: (self.sources / "record.txt").write_text(
                    "Changed source.\n", encoding="utf-8"
                ),
            ),
            (
                "stale-source-documentation",
                lambda: None,
            ),
        )
        for expected, mutate in cases:
            with self.subTest(expected=expected):
                mutate()
                minimum = (
                    "2026-09-01"
                    if expected == "stale-source-documentation"
                    else "2026-08-01"
                )
                with self.assertRaises(RoleLaunchError) as captured:
                    load_approved_source_records(
                        invocation=self.invocation(),
                        documentation_paths=("SOURCE.yaml",),
                        minimum_checked_through=minimum,
                    )
                self.assertEqual(captured.exception.code, expected)
                if expected == "source-content-mismatch":
                    (self.sources / "record.txt").write_text(
                        "Synthetic approved record.\n", encoding="utf-8"
                    )


if __name__ == "__main__":
    unittest.main()
