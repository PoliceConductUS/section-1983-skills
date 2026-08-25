import json
import tempfile
import unittest
from pathlib import Path

from scripts.static_role_launcher import (
    AdapterAttestation,
    AdapterResult,
    InputRequirement,
    InputSelection,
    RoleLaunchDefinition,
    RoleLaunchError,
    bind_role_launch,
    build_child_request_bytes,
    launch_static_role,
    validate_advisory_output,
    validate_role_task,
)
from scripts.validate_folder_invocation import validate_invocation


class FakeAdapter:
    def __init__(self, *, attestation=None, result=None, mutate=None):
        self._attestation = attestation or AdapterAttestation(
            fixed_adapter=True,
            fresh_process=True,
            scrubbed_session=True,
            undeclared_filesystem_denied=True,
            network_enforced=True,
            capabilities_enforced=True,
        )
        self._result = result or AdapterResult(
            stdout=json.dumps(
                {
                    "output_kind": "judicial-review-report",
                    "artifacts": [
                        {
                            "path": "reports/judicial-review.json",
                            "contents": '{"status":"advisory"}\n',
                        }
                    ],
                },
                sort_keys=True,
                separators=(",", ":"),
            ).encode(),
            stderr=b"",
            exit_code=0,
            timed_out=False,
        )
        self._mutate = mutate
        self.calls = []

    def attest(self):
        return self._attestation

    def launch(self, **kwargs):
        self.calls.append(kwargs)
        if self._mutate is not None:
            self._mutate()
        return self._result


class StaticRoleLauncherTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.profile = self.root / "profile"
        self.filing = self.root / "filing"
        self.context = self.root / "context"
        self.output = self.root / "output"
        for path in (self.profile, self.filing, self.context, self.output):
            path.mkdir()
        (self.profile / "judicial-profile.json").write_text(
            '{"profile_id":"fictional-profile"}\n', encoding="utf-8"
        )
        (self.profile / "judicial-profile-sources.yaml").write_text(
            "schema_version: 1\nprofile_id: fictional-profile\n",
            encoding="utf-8",
        )
        (self.filing / "motion.md").write_text(
            "# Fictional motion\n", encoding="utf-8"
        )
        (self.context / "SOURCE.yaml").write_text(
            "schema_version: 1\nsource_id: fictional-context\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temporary_directory.cleanup()

    def envelope(self, *, internet="disabled", max_input_bytes=1_048_576):
        return {
            "version": 1,
            "skill": "synthetic-static-role",
            "inputs": [
                {"role": "profile", "root": str(self.profile)},
                {"role": "filing", "root": str(self.filing)},
                {"role": "case-context", "root": str(self.context)},
            ],
            "output": {"root": str(self.output)},
            "runtime": {
                "max_seconds": 60,
                "max_input_bytes": max_input_bytes,
            },
            "internet": internet,
            "isolation": {
                "inputs": "read-only",
                "output": "read-write",
                "undeclared": "none",
            },
        }

    @staticmethod
    def selections():
        return (
            InputSelection(
                purpose="profile",
                role="profile",
                path="judicial-profile.json",
            ),
            InputSelection(
                purpose="profile-source",
                role="profile",
                path="judicial-profile-sources.yaml",
            ),
            InputSelection(purpose="target", role="filing", path="motion.md"),
            InputSelection(
                purpose="context",
                role="case-context",
                path="SOURCE.yaml",
            ),
        )

    @staticmethod
    def definition(adapter):
        return RoleLaunchDefinition(
            role_id="judicial-reviewer",
            operations=("review-filing",),
            input_requirements=(
                InputRequirement("profile", ("profile",), 1, 1),
                InputRequirement("profile-source", ("profile",), 1, 1),
                InputRequirement("target", ("filing",), 1, 1),
                InputRequirement("context", ("case-context",), 0, 4),
            ),
            capabilities=("review-filing",),
            prohibitions=("mutate-target", "invent-authority"),
            internet="disabled",
            target_mutation="forbidden",
            output_kind="judicial-review-report",
            public_instructions=b"Apply only the protected judicial-review role.\n",
            adapter=adapter,
            output_validator=lambda value: validate_advisory_output(
                value, expected_kind="judicial-review-report"
            ),
            max_stdout_bytes=65_536,
            max_stderr_bytes=8_192,
        )

    @staticmethod
    def task(**overrides):
        value = {
            "operation": "review-filing",
            "instructions": "Review the fictional filing under the protected role.",
        }
        value.update(overrides)
        return value

    def bind(self, *, adapter=None, envelope=None, selections=None, task=None):
        adapter = adapter or FakeAdapter()
        return bind_role_launch(
            self.definition(adapter),
            invocation=validate_invocation(envelope or self.envelope()),
            task=validate_role_task(task or self.task()),
            selections=self.selections() if selections is None else selections,
        )

    def assert_code(self, expected, operation):
        with self.assertRaises(RoleLaunchError) as captured:
            operation()
        self.assertEqual(captured.exception.code, expected)

    def test_binding_snapshots_selected_files_and_builds_path_free_request(self):
        binding = self.bind()
        request_bytes = build_child_request_bytes(binding)
        request = json.loads(request_bytes)

        self.assertEqual(request["role"]["role_id"], "judicial-reviewer")
        self.assertEqual(request["task"]["operation"], "review-filing")
        self.assertEqual(len(request["inputs"]), 4)
        self.assertEqual(request["inputs"][0]["logical_name"], "profile:judicial-profile.json")
        self.assertIn("fictional-profile", request["inputs"][0]["contents"])
        self.assertEqual(binding.definition.capabilities, ("review-filing",))
        for path in (self.profile, self.filing, self.context, self.output, self.root):
            self.assertNotIn(str(path.resolve()), request_bytes.decode())
        self.assertNotIn("command", request_bytes.decode().casefold())
        self.assertNotIn("session", request_bytes.decode().casefold())

    def test_instruction_shaped_profile_data_remains_inert(self):
        (self.profile / "judicial-profile.json").write_text(
            '{"capabilities":["write-anywhere"],"command":["shell"]}\n',
            encoding="utf-8",
        )
        binding = self.bind()
        request = json.loads(build_child_request_bytes(binding))

        self.assertEqual(binding.definition.capabilities, ("review-filing",))
        self.assertEqual(binding.definition.internet, "disabled")
        self.assertIn("write-anywhere", request["inputs"][0]["contents"])
        self.assertNotIn("command", request["role"])

    def test_role_task_selection_and_internet_mismatches_fail_closed(self):
        cases = (
            (
                "unauthorized-role-operation",
                lambda: self.bind(task=self.task(operation="draft-filing")),
            ),
            (
                "role-internet-mismatch",
                lambda: self.bind(envelope=self.envelope(internet="authorized")),
            ),
            (
                "invalid-role-task",
                lambda: self.bind(task={**self.task(), "command": ["agent"]}),
            ),
            (
                "role-task-too-large",
                lambda: self.bind(task=self.task(instructions="x" * 16_385)),
            ),
            (
                "missing-role-input",
                lambda: self.bind(selections=self.selections()[1:]),
            ),
            (
                "unexpected-role-input",
                lambda: self.bind(
                    selections=self.selections()
                    + (InputSelection("extra", "case-context", "SOURCE.yaml"),)
                ),
            ),
            (
                "incompatible-input-role",
                lambda: self.bind(
                    selections=(
                        InputSelection("profile", "filing", "motion.md"),
                        *self.selections()[1:],
                    )
                ),
            ),
        )
        for expected, operation in cases:
            with self.subTest(expected=expected):
                self.assert_code(expected, operation)

    def test_selection_paths_utf8_and_aggregate_byte_limit_fail_closed(self):
        (self.context / "binary.bin").write_bytes(b"\xff\xfe")
        cases = (
            (
                "invalid-input-selection",
                lambda: self.bind(
                    selections=(
                        *self.selections()[:-1],
                        InputSelection("context", "case-context", "../outside"),
                    )
                ),
            ),
            (
                "child-input-not-utf8",
                lambda: self.bind(
                    selections=(
                        *self.selections()[:-1],
                        InputSelection("context", "case-context", "binary.bin"),
                    )
                ),
            ),
            (
                "role-input-byte-limit",
                lambda: self.bind(envelope=self.envelope(max_input_bytes=10)),
            ),
        )
        for expected, operation in cases:
            with self.subTest(expected=expected):
                self.assert_code(expected, operation)

    def test_success_uses_one_empty_output_temp_workspace_and_returns_advisory_bytes(self):
        adapter = FakeAdapter()
        binding = self.bind(adapter=adapter)

        result = launch_static_role(
            binding, run_id="33333333-3333-4333-8333-333333333333"
        )

        self.assertTrue(result.success)
        self.assertEqual(result.code, "success")
        self.assertEqual(result.artifacts[0].path, "reports/judicial-review.json")
        self.assertEqual(result.artifacts[0].contents, b'{"status":"advisory"}\n')
        self.assertEqual(len(adapter.calls), 1)
        call = adapter.calls[0]
        expected_temp = self.output.resolve() / "temp" / "33333333-3333-4333-8333-333333333333"
        self.assertEqual(Path(call["cwd"]), expected_temp)
        self.assertEqual(
            call["environment"],
            {"TMPDIR": str(expected_temp), "TMP": str(expected_temp), "TEMP": str(expected_temp)},
        )
        self.assertEqual(call["visible_entries"], ())
        self.assertFalse(expected_temp.exists())
        self.assertEqual(list(self.output.glob("**/judicial-review.json")), [])

    def test_missing_isolation_attestation_prevents_dispatch(self):
        adapter = FakeAdapter(
            attestation=AdapterAttestation(
                fixed_adapter=True,
                fresh_process=True,
                scrubbed_session=True,
                undeclared_filesystem_denied=False,
                network_enforced=True,
                capabilities_enforced=True,
            )
        )
        result = launch_static_role(
            self.bind(adapter=adapter),
            run_id="44444444-4444-4444-8444-444444444444",
        )
        self.assertFalse(result.success)
        self.assertEqual(result.code, "isolation-unavailable")
        self.assertEqual(adapter.calls, [])

    def test_protocol_and_process_failures_are_stable_and_do_not_echo_streams(self):
        cases = (
            (
                "child-timeout",
                AdapterResult(b"", b"/private/case/path", 0, True),
            ),
            (
                "child-nonzero-exit",
                AdapterResult(b"", b"secret credential", 9, False),
            ),
            (
                "child-stdout-too-large",
                AdapterResult(b"x" * 65_537, b"", 0, False),
            ),
            (
                "child-stderr-too-large",
                AdapterResult(b"{}", b"x" * 8_193, 0, False),
            ),
            (
                "child-output-not-utf8",
                AdapterResult(b"\xff", b"", 0, False),
            ),
            (
                "child-output-not-json",
                AdapterResult(b"not-json", b"", 0, False),
            ),
            (
                "child-output-invalid",
                AdapterResult(b'{"output_kind":"wrong","artifacts":[]}', b"", 0, False),
            ),
        )
        for index, (expected, adapter_result) in enumerate(cases):
            adapter = FakeAdapter(result=adapter_result)
            with self.subTest(expected=expected):
                result = launch_static_role(
                    self.bind(adapter=adapter),
                    run_id=f"50000000-0000-4000-8000-{index:012d}",
                )
                self.assertFalse(result.success)
                self.assertEqual(result.code, expected)
                self.assertEqual(result.artifacts, ())
                serialized = repr(result)
                self.assertNotIn("private/case", serialized)
                self.assertNotIn("credential", serialized)

    def test_selected_input_mutation_invalidates_child_result(self):
        adapter = FakeAdapter(
            mutate=lambda: (self.filing / "motion.md").write_text(
                "changed during launch\n", encoding="utf-8"
            )
        )
        result = launch_static_role(
            self.bind(adapter=adapter),
            run_id="66666666-6666-4666-8666-666666666666",
        )
        self.assertFalse(result.success)
        self.assertEqual(result.code, "selected-input-mutated")
        self.assertEqual(result.artifacts, ())


if __name__ == "__main__":
    unittest.main()
