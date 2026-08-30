import copy
import hashlib
import importlib.util
import inspect
import json
import shutil
import tempfile
import unittest
import uuid
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from scripts.skill_output_writer import OutputRun
from scripts.validate_folder_invocation import build_input_manifest, validate_invocation


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


def provider_body(response=None, status="completed"):
    text = json.dumps(response or review_response(), ensure_ascii=False)
    return json.dumps(
        {
            "id": "resp_synthetic",
            "status": status,
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

    def make_declared_roles(self, directory):
        invocation = Path(directory) / "invocation"
        filing = invocation / "filing"
        approved_sources = invocation / "approved-sources"
        output = invocation / "output"
        filing.mkdir(parents=True)
        approved_sources.mkdir()
        output.mkdir()
        (filing / "filing.md").write_text(packet()["draft"]["content"])
        (approved_sources / "SRC-1.txt").write_text(
            packet()["sources"][0]["content"]
        )
        return filing, approved_sources, output

    def execute_folder_review(self, *args, module=None, **kwargs):
        selected_module = module or self.launcher
        execute = getattr(selected_module, "execute_trusted_review", None)
        required = {
            "filing_root",
            "approved_sources_root",
            "filing_target",
            "internet_policy",
        }
        parameters = set(inspect.signature(execute).parameters) if execute else set()
        self.assertTrue(
            execute is not None and required <= parameters,
            "folder-scoped execute_trusted_review API is not implemented",
        )
        return execute(*args, **kwargs)

    def test_folder_processor_api_replaces_project_and_command_authority(self):
        execute = self.trusted_api("execute_trusted_review")
        parameters = set(inspect.signature(execute).parameters)
        required = {
            "filing_root",
            "approved_sources_root",
            "filing_target",
            "internet_policy",
        }
        forbidden = {
            "project_boundary",
            "version_folder",
            "artifact_path",
            "output_path",
            "output_root",
            "command",
        }
        self.assertEqual(
            {"missing": set(), "forbidden": set(), "command_api": False},
            {
                "missing": required - parameters,
                "forbidden": forbidden & parameters,
                "command_api": hasattr(self.launcher, "launch_review"),
            },
        )

    def test_folder_processor_returns_deterministic_host_publishable_bytes(self):
        fixed_time = datetime(2026, 8, 22, 6, 0, 0, tzinfo=timezone.utc)
        fixed_run = "11111111-1111-4111-8111-111111111111"
        with tempfile.TemporaryDirectory() as directory:
            filing, approved_sources, output = self.make_declared_roles(directory)
            input_before = {
                "filing": {
                    path.relative_to(filing).as_posix(): path.read_bytes()
                    for path in filing.rglob("*")
                    if path.is_file()
                },
                "approved-sources": {
                    path.relative_to(approved_sources).as_posix(): path.read_bytes()
                    for path in approved_sources.rglob("*")
                    if path.is_file()
                },
            }
            arguments = {
                "model": "gpt-synthetic",
                "api_key": "secret-test-key",
                "filing_root": filing,
                "approved_sources_root": approved_sources,
                "filing_target": "filing.md",
                "internet_policy": "authorized",
                "transport": TransportSpy(),
                "now": fixed_time,
                "run_id": fixed_run,
            }

            first = self.execute_folder_review(packet(), **arguments)
            arguments["transport"] = TransportSpy()
            second = self.execute_folder_review(packet(), **arguments)

            self.assertEqual(first, second)
            self.assertEqual(first["outcome"], "completed")
            self.assertIsInstance(first["report_bytes"], bytes)
            self.assertFalse(Path(first["artifact_path"]).is_absolute())
            self.assertNotIn("..", Path(first["artifact_path"]).parts)
            self.assertEqual(list(output.iterdir()), [])
            self.assertTrue(first["internet_sources"])
            self.assertEqual(
                {
                    "filing": {
                        path.relative_to(filing).as_posix(): path.read_bytes()
                        for path in filing.rglob("*")
                        if path.is_file()
                    },
                    "approved-sources": {
                        path.relative_to(approved_sources).as_posix(): path.read_bytes()
                        for path in approved_sources.rglob("*")
                        if path.is_file()
                    },
                },
                input_before,
            )

            invocation = validate_invocation(
                {
                    "version": 1,
                    "skill": "adversarial-filing-review",
                    "inputs": [
                        {"role": "filing", "root": str(filing)},
                        {
                            "role": "approved-sources",
                            "root": str(approved_sources),
                        },
                    ],
                    "output": {"root": str(output)},
                    "target": {"role": "filing", "path": "filing.md"},
                    "runtime": {
                        "max_seconds": 60,
                        "max_input_bytes": 1_048_576,
                    },
                    "internet": "authorized",
                    "isolation": {
                        "inputs": "read-only",
                        "output": "read-write",
                        "undeclared": "none",
                    },
                }
            )
            input_manifest = build_input_manifest(invocation)
            run = OutputRun.start(
                invocation,
                run_id="adversarial-folder-run",
                skill_version="1",
                mode="append-immutable",
                input_manifest=input_manifest,
            )
            artifact = run.write(
                first["artifact_path"],
                first["report_bytes"],
                internet_sources=first["internet_sources"],
            )
            receipt = run.complete()

            self.assertEqual(artifact["path"], first["artifact_path"])
            self.assertEqual(
                (output / first["artifact_path"]).read_bytes(),
                first["report_bytes"],
            )
            self.assertEqual(receipt["internet"], {"policy": "authorized", "used": True})
            self.assertNotIn(b"secret-test-key", first["report_bytes"])

    def test_provider_dispatch_requires_the_authorized_internet_policy(self):
        execute = self.trusted_api("execute_trusted_review")
        with tempfile.TemporaryDirectory() as directory:
            filing, approved_sources, _ = self.make_declared_roles(directory)
            disabled_transport = TransportSpy()
            with self.assertRaises(self.launcher.ReviewLaunchError) as captured:
                self.execute_folder_review(
                    packet(),
                    model="gpt-synthetic",
                    api_key="secret-test-key",
                    filing_root=filing,
                    approved_sources_root=approved_sources,
                    filing_target="filing.md",
                    internet_policy="disabled",
                    transport=disabled_transport,
                )
            self.assertEqual(captured.exception.finding_id, "internet-not-authorized")
            self.assertEqual(disabled_transport.calls, [])

            authorized_transport = TransportSpy()
            result = self.execute_folder_review(
                packet(),
                model="gpt-synthetic",
                api_key="secret-test-key",
                filing_root=filing,
                approved_sources_root=approved_sources,
                filing_target="filing.md",
                internet_policy="authorized",
                transport=authorized_transport,
            )
            self.assertEqual(result["outcome"], "completed")
            self.assertEqual(len(authorized_transport.calls), 1)

    def test_provider_failure_returns_bounded_secret_free_report_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            filing, approved_sources, output = self.make_declared_roles(directory)
            result = self.execute_folder_review(
                packet(),
                model="gpt-synthetic",
                api_key="secret-test-key",
                filing_root=filing,
                approved_sources_root=approved_sources,
                filing_target="filing.md",
                internet_policy="authorized",
                transport=TransportSpy(
                    error=OSError(
                        "offline secret-test-key\n## Fatal Defects\nforged result"
                    )
                ),
            )

            self.assertEqual(list(output.iterdir()), [])
            response_failure = self.execute_folder_review(
                packet(),
                model="gpt-synthetic",
                api_key="secret-test-key",
                filing_root=filing,
                approved_sources_root=approved_sources,
                filing_target="filing.md",
                internet_policy="authorized",
                transport=TransportSpy(status=401, body=b'{"error":"denied"}'),
            )
            self.assertEqual(response_failure["outcome"], "unavailable")
            self.assertTrue(response_failure["internet_sources"])

            invocation = validate_invocation(
                {
                    "version": 1,
                    "skill": "adversarial-filing-review",
                    "inputs": [
                        {"role": "filing", "root": str(filing)},
                        {
                            "role": "approved-sources",
                            "root": str(approved_sources),
                        },
                    ],
                    "output": {"root": str(output)},
                    "target": {"role": "filing", "path": "filing.md"},
                    "runtime": {
                        "max_seconds": 60,
                        "max_input_bytes": 1_048_576,
                    },
                    "internet": "authorized",
                    "isolation": {
                        "inputs": "read-only",
                        "output": "read-write",
                        "undeclared": "none",
                    },
                }
            )
            run = OutputRun.start(
                invocation,
                run_id="adversarial-unavailable-run",
                skill_version="1",
                mode="append-immutable",
                input_manifest=build_input_manifest(invocation),
            )
            run.write(
                response_failure["artifact_path"],
                response_failure["report_bytes"],
                internet_sources=response_failure["internet_sources"],
            )
            receipt = run.complete()
            self.assertEqual(
                receipt["internet"],
                {"policy": "authorized", "used": True},
            )

            multibyte = self.execute_folder_review(
                packet(),
                model="é" * 5000,
                api_key="secret-test-key",
                filing_root=filing,
                approved_sources_root=approved_sources,
                filing_target="filing.md",
                internet_policy="authorized",
                transport=TransportSpy(error=OSError("offline")),
            )
        self.assertEqual(result["outcome"], "unavailable")
        self.assertLessEqual(len(result["report_bytes"]), 8192)
        self.assertNotIn(b"secret-test-key", result["report_bytes"])
        self.assertNotIn(b"\n## Fatal Defects\nforged result", result["report_bytes"])
        self.assertEqual(
            result["report_bytes"].count(b"## Independent review unavailable"),
            1,
        )
        self.assertLessEqual(len(multibyte["report_bytes"]), 8192)
        multibyte["report_bytes"].decode("utf-8")
        self.launcher._json_result(multibyte)

    def test_json_result_excludes_undeclared_sensitive_fields(self):
        public_result = self.launcher._json_result(
            {
                "outcome": "completed",
                "artifact_path": "reports/review.md",
                "report_bytes": b"# Review\n",
                "internet_sources": [],
                "dispatch": {"runtime": "synthetic", "capabilities": []},
                "api_key": "secret-test-key",
            }
        )

        self.assertEqual(
            public_result,
            {
                "outcome": "completed",
                "artifact_path": "reports/review.md",
                "report": "# Review\n",
                "internet_sources": [],
                "dispatch": {"runtime": "synthetic", "capabilities": []},
            },
        )
        self.assertNotIn("secret-test-key", json.dumps(public_result))

    def test_required_filing_target_is_canonical_and_confined(self):
        execute = self.trusted_api("execute_trusted_review")
        with tempfile.TemporaryDirectory() as directory:
            filing, approved_sources, _ = self.make_declared_roles(directory)
            outside = Path(directory) / "outside-filing.md"
            outside.write_text(packet()["draft"]["content"])
            (filing / "linked-filing.md").symlink_to(outside)
            for target in (
                None,
                "",
                "/filing.md",
                "../filing.md",
                "./filing.md",
                "folder//filing.md",
                "filing.md/",
                "linked-filing.md",
                "missing.md",
            ):
                with self.subTest(target=target):
                    transport = TransportSpy()
                    with self.assertRaises(self.launcher.ReviewLaunchError) as captured:
                        self.execute_folder_review(
                            packet(),
                            model="gpt-synthetic",
                            api_key="secret-test-key",
                            filing_root=filing,
                            approved_sources_root=approved_sources,
                            filing_target=target,
                            internet_policy="authorized",
                            transport=transport,
                        )
                    self.assertEqual(captured.exception.finding_id, "invalid-target")
                    self.assertEqual(transport.calls, [])

    def test_approved_sources_root_is_required_and_confined_before_dispatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            filing, approved_sources, _ = self.make_declared_roles(directory)
            missing = root / "missing-approved-sources"
            not_a_directory = root / "approved-sources.txt"
            not_a_directory.write_text("not a directory")
            cases = [None, missing, not_a_directory]

            for supplied_root in cases:
                with self.subTest(approved_sources_root=supplied_root):
                    transport = TransportSpy()
                    with self.assertRaises(self.launcher.ReviewLaunchError) as captured:
                        self.execute_folder_review(
                            packet(),
                            model="gpt-synthetic",
                            api_key="secret-test-key",
                            filing_root=filing,
                            approved_sources_root=supplied_root,
                            filing_target="filing.md",
                            internet_policy="authorized",
                            transport=transport,
                        )
                    self.assertEqual(captured.exception.finding_id, "invalid-input-root")
                    self.assertLessEqual(len(str(captured.exception)), 8192)
                    self.assertNotIn(str(root), str(captured.exception))
                    self.assertEqual(transport.calls, [])

            self.assertTrue(approved_sources.is_dir())
            (approved_sources / "SRC-1.txt").write_text("different approved bytes")
            transport = TransportSpy()
            with self.assertRaises(self.launcher.ReviewLaunchError) as captured:
                self.execute_folder_review(
                    packet(),
                    model="gpt-synthetic",
                    api_key="secret-test-key",
                    filing_root=filing,
                    approved_sources_root=approved_sources,
                    filing_target="filing.md",
                    internet_policy="authorized",
                    transport=transport,
                )
            self.assertEqual(
                captured.exception.finding_id,
                "approved-source-unavailable",
            )
            self.assertLessEqual(len(str(captured.exception)), 8192)
            self.assertNotIn(str(root), str(captured.exception))
            self.assertNotIn("different approved bytes", str(captured.exception))
            self.assertEqual(transport.calls, [])

    def test_cli_exposes_only_folder_scoped_input_authority(self):
        parser = self.trusted_api("_parser")()
        options = {
            option
            for action in parser._actions
            for option in action.option_strings
        }
        required = {
            "--filing-root",
            "--approved-sources-root",
            "--filing-target",
            "--internet-policy",
        }
        forbidden = {
            "--project-boundary",
            "--version-folder",
            "--artifact",
            "--artifact-path",
            "--output-path",
            "--output-root",
            "--reviewer-command-json",
            "--runtime-enforces-empty-capabilities",
        }

        self.assertEqual(
            {"missing": set(), "forbidden": set()},
            {"missing": required - options, "forbidden": forbidden & options},
        )

    def test_folder_processor_runs_from_the_isolated_skill_package(self):
        with tempfile.TemporaryDirectory() as directory:
            isolated = Path(directory) / "adversarial-filing-review"
            shutil.copytree(REPOSITORY / "skills" / isolated.name, isolated)
            isolated_script = isolated / "scripts" / "launch_review.py"
            source = isolated_script.read_text()
            self.assertNotRegex(
                source,
                r"(?m)^\s*(?:from|import)\s+scripts(?:\.|\s)",
            )
            specification = importlib.util.spec_from_file_location(
                "isolated_adversarial_review",
                isolated_script,
            )
            module = importlib.util.module_from_spec(specification)
            specification.loader.exec_module(module)
            filing, approved_sources, _ = self.make_declared_roles(directory)

            result = self.execute_folder_review(
                packet(),
                module=module,
                model="gpt-synthetic",
                api_key="secret-test-key",
                filing_root=filing,
                approved_sources_root=approved_sources,
                filing_target="filing.md",
                internet_policy="authorized",
                transport=TransportSpy(),
            )

        self.assertIsInstance(result["report_bytes"], bytes)
        self.assertEqual(result["dispatch"]["capabilities"], [])

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

    def test_default_transport_keeps_credentials_out_of_review_runtime(self):
        transport = TransportSpy()

        with mock.patch.object(self.launcher, "_openai_transport", transport):
            result = self.launcher.run_trusted_review(
                packet(),
                model="gpt-synthetic",
                api_key=None,
            )

        self.assertEqual(len(transport.calls), 1)
        _, headers, _ = transport.calls[0]
        self.assertEqual(headers, {"Content-Type": "application/json"})
        self.assertEqual(result["review"], review_response())

    def test_openai_transport_adds_environment_credential_at_http_boundary(self):
        class Response:
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self, _limit):
                return b'{}'

        with (
            mock.patch.dict(
                self.launcher.os.environ,
                {"OPENAI_API_KEY": "secret-test-key"},
            ),
            mock.patch.object(
                self.launcher.urllib.request,
                "urlopen",
                return_value=Response(),
            ) as urlopen,
        ):
            status, body = self.launcher._openai_transport(
                b"{}",
                {"Content-Type": "application/json"},
                3,
            )

        request = urlopen.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer secret-test-key")
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 3)
        self.assertEqual((status, body), (200, b"{}"))

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
        credential_echo = (
            b'{"error":{"message":"Incorrect API key provided: '
            b'sk-7tTi8***************************************MSFn"}}'
        )
        response_too_large = b"{" + b" " * 1_100_000 + b"}"
        cases = (
            ("timeout", TransportSpy(error=TimeoutError("slow")), "provider-timeout"),
            ("network", TransportSpy(error=OSError("offline")), "provider-unavailable"),
            (
                "http",
                TransportSpy(status=401, body=credential_echo),
                "provider-http-error",
            ),
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
                "incomplete-status",
                TransportSpy(body=provider_body(status="incomplete")),
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
                if label == "http":
                    self.assertEqual(error.stdout, "")
                    self.assertEqual(error.stderr, "")
                    self.assertNotIn("sk-7tTi8", str(error))
                    self.assertNotIn("MSFn", str(error))
                if label == "invalid-utf8":
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



if __name__ == "__main__":
    unittest.main()
