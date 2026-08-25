import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.role_profile_sweeps import (
    RoleSweepError,
    SweepVariant,
    compare_role_runs,
    run_role_sweep,
)
from scripts.static_role_launcher import (
    AdapterAttestation,
    AdapterResult,
    InputRequirement,
    InputSelection,
    ProposedArtifact,
    RoleLaunchDefinition,
    bind_role_launch,
    validate_role_task,
)
from scripts.validate_folder_invocation import validate_invocation


class FakeAdapter:
    def __init__(self, value, *, available=True):
        self.value = value
        self.available = available
        self.calls = []

    def attest(self):
        return AdapterAttestation(
            fixed_adapter=self.available,
            fresh_process=self.available,
            scrubbed_session=self.available,
            undeclared_filesystem_denied=self.available,
            network_enforced=self.available,
            capabilities_enforced=self.available,
        )

    def launch(self, **kwargs):
        self.calls.append(kwargs)
        return AdapterResult(
            stdout=json.dumps(self.value, sort_keys=True).encode(),
            stderr=b"",
            exit_code=0,
            timed_out=False,
        )


def finding(finding_id, category, analysis, *, source_id="source-one"):
    return {
        "id": finding_id,
        "category": category,
        "attacked_quote": "Bounded allegation.",
        "location": f"motion.md, {category}",
        "source_ids": [source_id],
        "analysis": analysis,
        "limitation": "Synthetic finding for orchestration tests.",
    }


class RoleProfileSweepTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.profiles = self.root / "profiles"
        self.filing = self.root / "filing"
        self.sources = self.root / "sources"
        self.sweep_output = self.root / "sweep-output"
        self.runs = self.sweep_output / "runs"
        self.comparison = self.sweep_output / "comparison"
        for path in (
            self.profiles,
            self.filing,
            self.sources,
            self.runs / "variant-a",
            self.runs / "variant-b",
            self.comparison,
        ):
            path.mkdir(parents=True, exist_ok=True)
        (self.profiles / "variant-a.json").write_text('{"profile":"a"}\n')
        (self.profiles / "variant-b.json").write_text('{"profile":"b"}\n')
        (self.filing / "motion.md").write_text("Bounded allegation.\n")
        (self.sources / "source-one.txt").write_text("Approved source.\n")

    def tearDown(self):
        self.temporary_directory.cleanup()

    def invocation(self, output_root):
        return validate_invocation(
            {
                "version": 1,
                "skill": "synthetic-role-sweep",
                "inputs": [
                    {"role": "profile", "root": str(self.profiles)},
                    {"role": "filing", "root": str(self.filing)},
                    {"role": "approved-sources", "root": str(self.sources)},
                ],
                "output": {"root": str(output_root)},
                "runtime": {"max_seconds": 60, "max_input_bytes": 1_000_000},
                "internet": "disabled",
                "isolation": {
                    "inputs": "read-only",
                    "output": "read-write",
                    "undeclared": "none",
                },
            }
        )

    @staticmethod
    def definition(adapter, profile_id):
        def validate_output(value):
            if (
                type(value) is not dict
                or set(value) != {"output_kind", "findings"}
                or value["output_kind"] != "synthetic-findings"
                or type(value["findings"]) is not list
            ):
                raise ValueError("invalid")
            artifact = {
                "schema_version": 1,
                "role": "opposing-counsel",
                "profile_id": profile_id,
                "result": "findings-only",
                "findings": value["findings"],
            }
            return (
                ProposedArtifact(
                    path="reports/findings.json",
                    contents=(
                        json.dumps(artifact, sort_keys=True, separators=(",", ":"))
                        + "\n"
                    ).encode(),
                ),
            )

        return RoleLaunchDefinition(
            role_id="opposing-counsel",
            operations=("opposing-counsel-simulation",),
            input_requirements=(
                InputRequirement("profile", ("profile",), 1, 1),
                InputRequirement("filing-target", ("filing",), 1, 1),
            ),
            capabilities=(),
            prohibitions=("mutate-target", "emit-disposition"),
            internet="disabled",
            target_mutation="forbidden",
            output_kind="synthetic-findings",
            public_instructions=b"Return findings only.\n",
            adapter=adapter,
            input_validator=lambda _inputs: None,
            output_validator=validate_output,
            max_stdout_bytes=1_000_000,
            max_stderr_bytes=8_192,
        )

    def variant(self, variant_id, findings, *, available=True, output_root=None):
        adapter = FakeAdapter(
            {"output_kind": "synthetic-findings", "findings": findings},
            available=available,
        )
        invocation = self.invocation(output_root or self.runs / variant_id)
        binding = bind_role_launch(
            self.definition(adapter, variant_id),
            invocation=invocation,
            task=validate_role_task(
                {
                    "operation": "opposing-counsel-simulation",
                    "instructions": "Return source-bounded findings only.",
                }
            ),
            selections=(
                InputSelection("profile", "profile", f"{variant_id}.json"),
                InputSelection("filing-target", "filing", "motion.md"),
            ),
        )
        return SweepVariant(variant_id=variant_id, binding=binding), adapter

    def input_snapshot(self):
        return {
            path.relative_to(self.root).as_posix(): path.read_bytes()
            for root in (self.profiles, self.filing, self.sources)
            for path in root.rglob("*")
            if path.is_file()
        }

    def test_sweep_runs_each_variant_once_and_publishes_deterministic_comparison(self):
        stable_a = finding("stable-a", "authority-attack", "Stable analysis.")
        stable_b = {**stable_a, "id": "stable-b"}
        flip_a = finding("flip-a", "record-attack", "Variant A analysis.")
        flip_b = finding("flip-b", "record-attack", "Variant B analysis.")
        subset = finding("subset-a", "procedural-attack", "Subset analysis.")
        variant_a, adapter_a = self.variant(
            "variant-a", [stable_a, flip_a, subset]
        )
        variant_b, adapter_b = self.variant("variant-b", [stable_b, flip_b])
        before = self.input_snapshot()

        result = run_role_sweep(
            variants=(variant_b, variant_a),
            comparison_invocation=self.invocation(self.comparison),
            launcher_version="1.0.0",
            producer_version="1.0.0",
        )

        self.assertEqual([run.variant_id for run in result.runs], ["variant-a", "variant-b"])
        self.assertEqual(len(adapter_a.calls), 1)
        self.assertEqual(len(adapter_b.calls), 1)
        for variant_id, adapter in (
            ("variant-a", adapter_a),
            ("variant-b", adapter_b),
        ):
            workspace = Path(adapter.calls[0]["cwd"])
            self.assertEqual(
                workspace.parent, (self.runs / variant_id / "temp").resolve()
            )
            self.assertFalse(workspace.exists())
            self.assertTrue((self.runs / variant_id / "reports/findings.json").is_file())
            receipt = self.runs / variant_id / "run-receipt.yaml"
            self.assertTrue(receipt.is_file())
            receipt_text = receipt.read_text()
            self.assertIn(f'variant_id: "{variant_id}"', receipt_text)
            self.assertIn('path: "motion.md"', receipt_text)
            self.assertNotIn(str(self.root), receipt_text)
            self.assertTrue(
                (self.runs / variant_id / ".skill-runs" / variant_id / "manifest.json").is_file()
            )
        comparison_bytes = (self.comparison / "comparison.json").read_bytes()
        self.assertEqual(comparison_bytes, result.comparison.contents)
        comparison = json.loads(comparison_bytes)
        self.assertEqual(comparison["status"], "complete")
        self.assertEqual(len(comparison["stable_findings"]), 1)
        self.assertEqual(len(comparison["subset_findings"]), 1)
        self.assertEqual(len(comparison["flipped_findings"]), 1)
        self.assertEqual(
            compare_role_runs(tuple(reversed(result.runs))).contents,
            result.comparison.contents,
        )
        self.assertEqual(before, self.input_snapshot())

    def test_failed_variant_is_visible_and_never_becomes_negative_evidence(self):
        variant_a, adapter_a = self.variant(
            "variant-a", [finding("a", "authority-attack", "Available analysis.")]
        )
        variant_b, adapter_b = self.variant("variant-b", [], available=False)

        result = run_role_sweep(
            variants=(variant_a, variant_b),
            comparison_invocation=self.invocation(self.comparison),
            launcher_version="1.0.0",
            producer_version="1.0.0",
        )

        comparison = json.loads(result.comparison.contents)
        self.assertEqual(comparison["status"], "incomplete")
        self.assertEqual(comparison["successful_variants"], ["variant-a"])
        self.assertEqual(
            comparison["failed_variants"],
            [{"code": "isolation-unavailable", "variant_id": "variant-b"}],
        )
        self.assertEqual(comparison["stable_findings"], [])
        self.assertEqual(comparison["subset_findings"], [])
        self.assertEqual(comparison["flipped_findings"], [])
        self.assertEqual(len(adapter_a.calls), 1)
        self.assertEqual(len(adapter_b.calls), 0)
        self.assertFalse((self.runs / "variant-b" / "reports/findings.json").exists())
        self.assertTrue((self.runs / "variant-b" / "run-receipt.yaml").is_file())
        failure = self.runs / "variant-b" / ".skill-runs/variant-b/failure.json"
        self.assertEqual(json.loads(failure.read_text())["status"], "failure")

    def test_target_mismatch_and_wrong_output_shape_fail_before_dispatch(self):
        variant_a, adapter_a = self.variant("variant-a", [])
        (self.filing / "other.md").write_text("Different target.\n")
        adapter_b = FakeAdapter({"output_kind": "synthetic-findings", "findings": []})
        invocation_b = self.invocation(self.runs / "variant-b")
        binding_b = bind_role_launch(
            self.definition(adapter_b, "variant-b"),
            invocation=invocation_b,
            task=validate_role_task(
                {
                    "operation": "opposing-counsel-simulation",
                    "instructions": "Return findings only.",
                }
            ),
            selections=(
                InputSelection("profile", "profile", "variant-b.json"),
                InputSelection("filing-target", "filing", "other.md"),
            ),
        )
        variant_b = SweepVariant("variant-b", binding_b)

        with self.assertRaises(RoleSweepError) as captured:
            run_role_sweep(
                variants=(variant_a, variant_b),
                comparison_invocation=self.invocation(self.comparison),
                launcher_version="1.0.0",
                producer_version="1.0.0",
            )
        self.assertEqual(captured.exception.code, "sweep-target-mismatch")
        self.assertEqual(adapter_a.calls, [])
        self.assertEqual(adapter_b.calls, [])

        misplaced = self.root / "misplaced-output"
        misplaced.mkdir()
        wrong_variant, wrong_adapter = self.variant(
            "variant-a", [], output_root=misplaced
        )
        with self.assertRaises(RoleSweepError) as captured:
            run_role_sweep(
                variants=(wrong_variant,),
                comparison_invocation=self.invocation(self.comparison),
                launcher_version="1.0.0",
                producer_version="1.0.0",
            )
        self.assertEqual(captured.exception.code, "invalid-sweep-output")
        self.assertEqual(wrong_adapter.calls, [])


if __name__ == "__main__":
    unittest.main()
