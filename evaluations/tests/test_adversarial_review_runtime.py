import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
import uuid
from datetime import datetime, timezone
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
LAUNCHER = (
    REPOSITORY
    / "skills"
    / "adversarial-filing-review"
    / "scripts"
    / "launch_review.py"
)
HEADINGS = (
    "Fatal Defects",
    "Credible Opposition Arguments",
    "Factual Disputes",
    "Discovery Issues",
    "Style Complaints",
)


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def packet():
    draft = "# Synthetic Filing\n\nBounded allegation.\n"
    source = "Synthetic approved record.\n"
    return {
        "draft": {
            "content": draft,
            "version": "synthetic-v1",
            "sha256": sha256(draft),
        },
        "document_family": "complaint or amended complaint",
        "sources": [
            {
                "id": "SRC-1",
                "role": "record",
                "content": source,
                "sha256": sha256(source),
            }
        ],
        "skill": {"content": "Synthetic public review instructions."},
        "checklist": {"content": "Synthetic complaint attack checklist."},
        "capabilities": [],
    }


def finding(
    finding_id="FATAL-001",
    correction=None,
    plaintiff_decision=None,
):
    return {
        "id": finding_id,
        "attacked_quote": "Bounded allegation.",
        "location": "Synthetic Filing, paragraph 1",
        "source_ids": ["SRC-1"],
        "attack": "The allegation omits the fictional date required by the source.",
        "consequence": "The synthetic pleading does not identify when the event occurred.",
        "status": "open",
        "correction": correction,
        "plaintiff_decision": plaintiff_decision,
    }


def review_response():
    return {
        "Fatal Defects": [
            finding(
                correction={
                    "replace": "Bounded allegation.",
                    "with": "On January 15, 2026, the bounded event occurred.",
                }
            )
        ],
        "Credible Opposition Arguments": [
            finding(
                finding_id="ARG-001",
                plaintiff_decision={
                    "question": "Whether to retain the synthetic theory",
                    "choices": [
                        {
                            "option": "Retain the theory",
                            "consequence": "The stated opposition argument remains.",
                        },
                        {
                            "option": "Omit the theory",
                            "consequence": "The theory will not appear in the filing.",
                        },
                    ],
                },
            )
        ],
        "Factual Disputes": [],
        "Discovery Issues": [],
        "Style Complaints": [],
    }


def provider_body(response=None):
    text = json.dumps(response or review_response(), ensure_ascii=False)
    return json.dumps(
        {
            "id": "resp_synthetic",
            "output": [
                {
                    "type": "message",
                    "content": [{"type": "output_text", "text": text}],
                }
            ],
        }
    ).encode("utf-8")


def launcher_module():
    specification = importlib.util.spec_from_file_location(
        f"adversarial_review_runtime_{uuid.uuid4().hex}",
        LAUNCHER,
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class TransportSpy:
    def __init__(self, status=200, body=None, error=None):
        self.status = status
        self.body = provider_body() if body is None else body
        self.error = error
        self.calls = []

    def __call__(self, body, headers, timeout_seconds):
        self.calls.append((body, headers, timeout_seconds))
        if self.error:
            raise self.error
        return self.status, self.body


class AdversarialReviewRuntimeTest(unittest.TestCase):
    def setUp(self):
        self.launcher = launcher_module()

    def trusted_api(self, name):
        self.assertTrue(
            hasattr(self.launcher, name),
            f"trusted runtime API is missing: {name}",
        )
        return getattr(self.launcher, name)

    def make_version(self, directory):
        project = Path(directory) / "synthetic-project"
        version = project / "generated" / "motion" / "v1"
        version.mkdir(parents=True)
        artifact = version / "filing.md"
        artifact.write_text(packet()["draft"]["content"])
        return project, version, artifact

    def test_trusted_request_disables_tools_storage_and_session_continuation(self):
        run_trusted_review = self.trusted_api("run_trusted_review")
        transport = TransportSpy()

        result = run_trusted_review(
            packet(),
            model="gpt-synthetic",
            api_key="secret-test-key",
            timeout_seconds=3,
            transport=transport,
        )

        self.assertEqual(len(transport.calls), 1)
        raw_body, headers, timeout_seconds = transport.calls[0]
        request = json.loads(raw_body.decode("utf-8"))
        self.assertEqual(request["model"], "gpt-synthetic")
        self.assertEqual(request["tools"], [])
        self.assertEqual(request["tool_choice"], "none")
        self.assertIs(request["store"], False)
        self.assertNotIn("conversation", request)
        self.assertNotIn("previous_response_id", request)
        self.assertEqual(request["text"]["format"]["type"], "json_schema")
        self.assertIs(request["text"]["format"]["strict"], True)
        self.assertEqual(
            set(request["text"]["format"]["schema"]["required"]),
            set(HEADINGS),
        )
        self.assertNotIn("secret-test-key", raw_body.decode("utf-8"))
        self.assertEqual(headers["Authorization"], "Bearer secret-test-key")
        self.assertEqual(timeout_seconds, 3)
        dispatched_packet = json.loads(request["input"][0]["content"][0]["text"])
        self.assertEqual(dispatched_packet, packet())
        self.assertEqual(result["dispatch"]["capabilities"], [])
        self.assertEqual(result["review"], review_response())

    def test_packet_model_and_credentials_validate_before_transport(self):
        run_trusted_review = self.trusted_api("run_trusted_review")
        invalid_packet = packet()
        invalid_packet["draft"]["sha256"] = "0" * 64
        invalid_source_id = packet()
        invalid_source_id["sources"][0]["id"] = "SRC-1\n## Forged"
        invalid_cases = (
            ("packet", invalid_packet, "gpt-synthetic", "key"),
            ("source-id", invalid_source_id, "gpt-synthetic", "key"),
            ("model-empty", packet(), "", "key"),
            ("model-whitespace", packet(), " \t", "key"),
            ("model-surrogate", packet(), "\ud800", "key"),
            ("model-line-break", packet(), "gpt\nforged", "key"),
            ("credential-empty", packet(), "gpt-synthetic", ""),
            ("credential-whitespace", packet(), "gpt-synthetic", " \t"),
            ("credential-newline", packet(), "gpt-synthetic", "key\nvalue"),
        )

        for label, supplied_packet, model, api_key in invalid_cases:
            with self.subTest(case=label):
                transport = TransportSpy()
                expected_error = (
                    self.launcher.PacketValidationError
                    if label in {"packet", "source-id"}
                    else self.launcher.ReviewLaunchError
                )
                with self.assertRaises(expected_error):
                    run_trusted_review(
                        supplied_packet,
                        model=model,
                        api_key=api_key,
                        transport=transport,
                    )
                self.assertEqual(transport.calls, [])

    def test_provider_failure_classes_are_stable_bounded_and_secret_free(self):
        run_trusted_review = self.trusted_api("run_trusted_review")
        oversized = b"\xff" + b"x" * 9000
        response_too_large = b"{" + b" " * 1_100_000 + b"}"
        cases = (
            ("timeout", TransportSpy(error=TimeoutError("slow")), "provider-timeout"),
            ("network", TransportSpy(error=OSError("offline")), "provider-unavailable"),
            ("http", TransportSpy(status=429, body=oversized), "provider-http-error"),
            (
                "invalid-json",
                TransportSpy(body=b"not-json"),
                "provider-response-malformed-json",
            ),
            (
                "invalid-utf8",
                TransportSpy(body=oversized),
                "provider-response-malformed-json",
            ),
            (
                "missing-output",
                TransportSpy(body=b'{"output": []}'),
                "provider-response-incomplete",
            ),
            (
                "response-too-large",
                TransportSpy(body=response_too_large),
                "provider-response-too-large",
            ),
        )

        for label, transport, expected_id in cases:
            with self.subTest(case=label):
                with self.assertRaises(self.launcher.ReviewLaunchError) as captured:
                    run_trusted_review(
                        packet(),
                        model="gpt-synthetic",
                        api_key="secret-test-key",
                        transport=transport,
                    )
                error = captured.exception
                self.assertEqual(error.finding_id, expected_id)
                self.assertNotIn("secret-test-key", str(error))
                self.assertLessEqual(len(getattr(error, "stdout", "")), 8192)
                self.assertLessEqual(len(getattr(error, "stderr", "")), 8192)
                if label in {"http", "invalid-utf8"}:
                    retained = getattr(error, "stdout", "") + getattr(
                        error, "stderr", ""
                    )
                    self.assertIn("\ufffd", retained)
                    self.assertIn("[truncated]", retained)

    def test_review_protocol_accepts_complete_response_and_rejects_mutations(self):
        validate_review_response = self.trusted_api("validate_review_response")
        valid = review_response()

        self.assertEqual(
            validate_review_response(valid, {"SRC-1"}),
            valid,
        )

        mutations = {}
        missing_category = copy.deepcopy(valid)
        missing_category.pop("Style Complaints")
        mutations["missing-category"] = missing_category
        extra_category = copy.deepcopy(valid)
        extra_category["Other"] = []
        mutations["extra-category"] = extra_category
        missing_field = copy.deepcopy(valid)
        missing_field["Fatal Defects"][0].pop("location")
        mutations["missing-field"] = missing_field
        extra_field = copy.deepcopy(valid)
        extra_field["Fatal Defects"][0]["provider_note"] = "not allowed"
        mutations["extra-field"] = extra_field
        unknown_source = copy.deepcopy(valid)
        unknown_source["Fatal Defects"][0]["source_ids"] = ["SRC-404"]
        mutations["unknown-source"] = unknown_source
        empty_sources = copy.deepcopy(valid)
        empty_sources["Fatal Defects"][0]["source_ids"] = []
        mutations["empty-sources"] = empty_sources
        duplicate_sources = copy.deepcopy(valid)
        duplicate_sources["Fatal Defects"][0]["source_ids"] = ["SRC-1", "SRC-1"]
        mutations["duplicate-sources"] = duplicate_sources
        duplicate_id = copy.deepcopy(valid)
        duplicate_id["Style Complaints"] = [finding("FATAL-001")]
        mutations["duplicate-id"] = duplicate_id
        invalid_id = copy.deepcopy(valid)
        invalid_id["Fatal Defects"][0]["id"] = "FATAL-001\n## Forged"
        mutations["invalid-id"] = invalid_id
        partial_correction = copy.deepcopy(valid)
        partial_correction["Fatal Defects"][0]["correction"].pop("with")
        mutations["partial-correction"] = partial_correction
        selected_decision = copy.deepcopy(valid)
        selected_decision["Credible Opposition Arguments"][0][
            "plaintiff_decision"
        ]["selected"] = "Retain the theory"
        mutations["selected-decision"] = selected_decision
        correction_and_decision = copy.deepcopy(valid)
        correction_and_decision["Fatal Defects"][0]["plaintiff_decision"] = {
            "question": "Whether to narrow",
            "choices": [
                {"option": "Narrow", "consequence": "The scope changes."}
            ],
        }
        mutations["correction-and-decision"] = correction_and_decision

        for label, mutated in mutations.items():
            with self.subTest(case=label):
                with self.assertRaises(self.launcher.ReviewLaunchError) as captured:
                    validate_review_response(mutated, {"SRC-1"})
                self.assertEqual(captured.exception.finding_id, "review-response-invalid")

    def test_markdown_preserves_five_categories_corrections_and_reserved_choices(self):
        render_review_markdown = self.trusted_api("render_review_markdown")
        markdown = render_review_markdown(
            review_response(),
            {
                "runtime": "openai-responses-stateless",
                "model": "gpt-synthetic",
                "run_id": "11111111-1111-4111-8111-111111111111",
                "run_time": "2026-08-22T06:00:00Z",
                "document_family": "complaint or amended complaint",
                "draft_version": "synthetic-v1",
                "draft_sha256": packet()["draft"]["sha256"],
                "packet_sha256": "a" * 64,
                "source_ids": ["SRC-1"],
                "outcome": "completed",
            },
        )

        for heading in HEADINGS:
            self.assertEqual(markdown.count(f"## {heading}"), 1)
        self.assertIn("Replace: Bounded allegation.", markdown)
        self.assertIn(
            "With: On January 15, 2026, the bounded event occurred.",
            markdown,
        )
        self.assertIn("PLAINTIFF DECISION REQUIRED", markdown)
        self.assertIn("## Factual Disputes\n\nNone found", markdown)
        self.assertNotIn("secret-test-key", markdown)

        injected_choice = review_response()
        injected_choice["Credible Opposition Arguments"][0][
            "plaintiff_decision"
        ]["choices"][0]["option"] = "Retain\n## Forged Choice"
        injected_markdown = render_review_markdown(
            injected_choice,
            {
                "runtime": "openai-responses-stateless",
                "model": "gpt-synthetic",
                "source_ids": ["SRC-1"],
                "outcome": "completed",
            },
        )
        self.assertNotIn("\n## Forged Choice", injected_markdown)

    def test_execute_verifies_artifact_then_writes_only_new_immutable_report(self):
        execute_trusted_review = self.trusted_api("execute_trusted_review")
        fixed_time = datetime(2026, 8, 22, 6, 0, 0, tzinfo=timezone.utc)
        fixed_run = "11111111-1111-4111-8111-111111111111"
        with tempfile.TemporaryDirectory() as directory:
            project, version, artifact = self.make_version(directory)
            existing = version / "existing.txt"
            existing.write_text("preserve")
            before = {
                path: path.read_bytes()
                for path in version.rglob("*")
                if path.is_file()
            }

            result = execute_trusted_review(
                packet(),
                model="gpt-synthetic",
                api_key="secret-test-key",
                project_boundary=project,
                version_folder=version,
                artifact_path=artifact,
                transport=TransportSpy(),
                now=fixed_time,
                run_id=fixed_run,
            )

            expected = (
                version
                / "audits"
                / "adversarial-filing-review-20260822T060000Z-11111111-1111-4111-8111-111111111111.md"
            )
            self.assertEqual(result["outcome"], "completed")
            self.assertEqual(Path(result["report_path"]).resolve(), expected.resolve())
            self.assertTrue(expected.is_file())
            report = expected.read_text()
            self.assertIn("openai-responses-stateless", report)
            self.assertIn("gpt-synthetic", report)
            self.assertIn("SRC-1", report)
            self.assertIn(packet()["draft"]["sha256"], report)
            self.assertIn(str(artifact), report)
            self.assertNotIn("secret-test-key", report)
            for path, content in before.items():
                self.assertEqual(path.read_bytes(), content)
            self.assertEqual(
                sorted(
                    path.relative_to(version).as_posix()
                    for path in version.rglob("*")
                    if path.is_file() and path not in before
                ),
                [
                    "audits/adversarial-filing-review-20260822T060000Z-11111111-1111-4111-8111-111111111111.md"
                ],
            )

    def test_artifact_and_path_failures_happen_before_provider_execution(self):
        execute_trusted_review = self.trusted_api("execute_trusted_review")
        with tempfile.TemporaryDirectory() as directory:
            project, version, artifact = self.make_version(directory)
            outside_version = Path(directory) / "outside-version"
            outside_version.mkdir()
            outside_artifact = outside_version / "filing.md"
            outside_artifact.write_text(packet()["draft"]["content"])
            mismatched = version / "mismatched.md"
            mismatched.write_text("different bytes")
            cases = (
                ("outside-version", outside_version, outside_artifact),
                ("outside-artifact", version, outside_artifact),
                ("mismatched-artifact", version, mismatched),
                ("missing-artifact", version, version / "missing.md"),
            )
            for label, supplied_version, supplied_artifact in cases:
                with self.subTest(case=label):
                    transport = TransportSpy()
                    with self.assertRaises(self.launcher.ReviewLaunchError):
                        execute_trusted_review(
                            packet(),
                            model="gpt-synthetic",
                            api_key="secret-test-key",
                            project_boundary=project,
                            version_folder=supplied_version,
                            artifact_path=supplied_artifact,
                            transport=transport,
                        )
                    self.assertEqual(transport.calls, [])

    def test_audits_escape_and_report_collision_preserve_existing_bytes(self):
        execute_trusted_review = self.trusted_api("execute_trusted_review")
        fixed_time = datetime(2026, 8, 22, 6, 0, 0, tzinfo=timezone.utc)
        fixed_run = "11111111-1111-4111-8111-111111111111"
        with tempfile.TemporaryDirectory() as directory:
            project, version, artifact = self.make_version(directory)
            audits = version / "audits"
            audits.mkdir()
            collision = (
                audits
                / "adversarial-filing-review-20260822T060000Z-11111111-1111-4111-8111-111111111111.md"
            )
            collision.write_text("immutable prior report")

            collision_transport = TransportSpy()
            with self.assertRaises(self.launcher.ReviewLaunchError):
                execute_trusted_review(
                    packet(),
                    model="gpt-synthetic",
                    api_key="secret-test-key",
                    project_boundary=project,
                    version_folder=version,
                    artifact_path=artifact,
                    transport=collision_transport,
                    now=fixed_time,
                    run_id=fixed_run,
                )
            self.assertEqual(collision.read_text(), "immutable prior report")
            self.assertEqual(collision_transport.calls, [])

        if os.name != "nt":
            with tempfile.TemporaryDirectory() as directory:
                project, version, artifact = self.make_version(directory)
                outside = Path(directory) / "outside-audits"
                outside.mkdir()
                (version / "audits").symlink_to(outside, target_is_directory=True)
                transport = TransportSpy()
                with self.assertRaises(self.launcher.ReviewLaunchError):
                    execute_trusted_review(
                        packet(),
                        model="gpt-synthetic",
                        api_key="secret-test-key",
                        project_boundary=project,
                        version_folder=version,
                        artifact_path=artifact,
                        transport=transport,
                    )
                self.assertEqual(transport.calls, [])
                self.assertEqual(list(outside.iterdir()), [])

        with tempfile.TemporaryDirectory() as directory:
            project, version, artifact = self.make_version(directory)
            transport = TransportSpy()
            with self.assertRaises(self.launcher.ReviewLaunchError):
                execute_trusted_review(
                    packet(),
                    model="gpt-synthetic",
                    api_key="secret-test-key",
                    project_boundary=project,
                    version_folder=version,
                    artifact_path=artifact,
                    transport=transport,
                    run_id="../escape",
                )
            self.assertEqual(transport.calls, [])

    def test_cli_success_and_unavailable_results_are_distinct_and_reported(self):
        main = self.trusted_api("main")
        with tempfile.TemporaryDirectory() as directory:
            project, version, artifact = self.make_version(directory)
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                exit_code = main(
                    [
                        "--trusted-openai",
                        "--model",
                        "gpt-synthetic",
                        "--project-boundary",
                        str(project),
                        "--version-folder",
                        str(version),
                        "--artifact",
                        str(artifact),
                    ],
                    input_bytes=json.dumps(packet()).encode("utf-8"),
                    transport=TransportSpy(),
                    environ={"OPENAI_API_KEY": "secret-test-key"},
                )
            result = json.loads(stdout.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertEqual(result["outcome"], "completed")
            self.assertTrue(Path(result["report_path"]).is_file())

            unavailable_stdout = io.StringIO()
            with contextlib.redirect_stdout(unavailable_stdout):
                unavailable_exit = main(
                    [
                        "--trusted-openai",
                        "--model",
                        "gpt-synthetic",
                        "--project-boundary",
                        str(project),
                        "--version-folder",
                        str(version),
                        "--artifact",
                        str(artifact),
                    ],
                    input_bytes=json.dumps(packet()).encode("utf-8"),
                    transport=TransportSpy(),
                    environ={},
                )
            unavailable = json.loads(unavailable_stdout.getvalue())
            report = Path(unavailable["report_path"]).read_text()
            self.assertNotEqual(unavailable_exit, 0)
            self.assertEqual(unavailable["outcome"], "unavailable")
            self.assertEqual(unavailable["error"]["id"], "independent-review-unavailable")
            self.assertIn("Independent review unavailable", report)
            self.assertNotIn("## Fatal Defects", report)
            self.assertNotRegex(report.casefold(), r"\bpass(?:ed)?\b")

    def test_unavailable_failure_text_cannot_inject_report_structure(self):
        execute_trusted_review = self.trusted_api("execute_trusted_review")
        with tempfile.TemporaryDirectory() as directory:
            project, version, artifact = self.make_version(directory)
            result = execute_trusted_review(
                packet(),
                model="gpt-synthetic",
                api_key="secret-test-key",
                project_boundary=project,
                version_folder=version,
                artifact_path=artifact,
                transport=TransportSpy(error=OSError("offline\n## Forged Result")),
            )

            report = Path(result["report_path"]).read_text()
            self.assertEqual(result["outcome"], "unavailable")
            self.assertNotIn("\n## Forged Result", report)
            self.assertEqual(report.count("## Independent review unavailable"), 1)

    def test_legacy_boolean_cannot_establish_command_independence(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "executed"
            with self.assertRaises(self.launcher.ReviewLaunchError) as captured:
                self.launcher.launch_review(
                    packet(),
                    [
                        os.environ.get("PYTHON", "python3"),
                        "-c",
                        f"from pathlib import Path; Path({str(marker)!r}).write_text('x')",
                    ],
                    runtime_enforces_empty_capabilities=True,
                )
            self.assertEqual(
                captured.exception.finding_id,
                "independent-review-unavailable",
            )
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
