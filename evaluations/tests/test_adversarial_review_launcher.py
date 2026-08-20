import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch


REPOSITORY = Path(__file__).resolve().parents[2]
LAUNCHER = (
    REPOSITORY
    / "skills"
    / "adversarial-filing-review"
    / "scripts"
    / "launch_review.py"
)

SUPPORTED_FAMILIES = (
    "complaint or amended complaint",
    "motion-to-dismiss response",
    "summary-judgment response",
    "leave to amend",
    "extension motion",
    "R&R objection",
    "R&R response",
)

PACKET_KEYS = {
    "draft",
    "document_family",
    "sources",
    "skill",
    "checklist",
    "capabilities",
}
DRAFT_KEYS = {"content", "version", "sha256"}
SOURCE_KEYS = {"id", "role", "content", "sha256"}
EMBEDDED_PUBLIC_TEXT_KEYS = {"content"}


def sha256(content):
    return hashlib.sha256(content.encode()).hexdigest()


def valid_packet(document_family=SUPPORTED_FAMILIES[0]):
    draft = "# Synthetic Filing\n\nBounded allegation.\n"
    source = "Synthetic approved source.\n"
    return {
        "draft": {
            "content": draft,
            "version": "synthetic-v1",
            "sha256": sha256(draft),
        },
        "document_family": document_family,
        "sources": [
            {
                "id": "SRC-1",
                "role": "record",
                "content": source,
                "sha256": sha256(source),
            }
        ],
        "skill": {"content": "Synthetic public skill content."},
        "checklist": {"content": "Synthetic public checklist content."},
        "capabilities": [],
    }


def launcher_module():
    if not LAUNCHER.is_file():
        raise AssertionError(
            f"public launcher is missing: {LAUNCHER.relative_to(REPOSITORY)}"
        )
    specification = importlib.util.spec_from_file_location(
        "adversarial_review_launcher",
        LAUNCHER,
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def write_script(directory, name, body):
    path = Path(directory) / name
    path.write_text(textwrap.dedent(body))
    return path


def spy_script(directory):
    return write_script(
        directory,
        "reviewer_spy.py",
        """
        import json
        import os
        import sys
        import uuid

        PROCESS_START_TOKEN = uuid.uuid4().hex
        request = json.load(sys.stdin)
        scrubbed_names = [
            name
            for name in os.environ
            if name.casefold() in {"pwd", "oldpwd"}
            or any(
                token in name.casefold()
                for token in ("conversation", "session", "thread")
            )
        ]
        print(json.dumps({
            "request": request,
            "process_start_token": PROCESS_START_TOKEN,
            "cwd": os.getcwd(),
            "cwd_entries": os.listdir("."),
            "scrubbed_names": scrubbed_names,
            "argv": sys.argv[1:],
        }))
        """,
    )


class AdversarialReviewLauncherTest(unittest.TestCase):

    def test_validate_packet_accepts_only_exact_fingerprinted_payload(self):
        launcher = launcher_module()
        packet = valid_packet()

        validated = launcher.validate_packet(packet)

        self.assertEqual(validated, packet)
        self.assertEqual(set(validated), PACKET_KEYS)
        self.assertEqual(set(validated["draft"]), DRAFT_KEYS)
        self.assertEqual(set(validated["sources"][0]), SOURCE_KEYS)
        self.assertEqual(set(validated["skill"]), EMBEDDED_PUBLIC_TEXT_KEYS)
        self.assertEqual(set(validated["checklist"]), EMBEDDED_PUBLIC_TEXT_KEYS)
        self.assertEqual(validated["capabilities"], [])

    def test_each_supported_family_is_accepted_and_other_family_rejected(self):
        launcher = launcher_module()

        for family in SUPPORTED_FAMILIES:
            with self.subTest(family=family):
                self.assertEqual(
                    launcher.validate_packet(valid_packet(family))["document_family"],
                    family,
                )

        with self.assertRaises(launcher.PacketValidationError) as captured:
            launcher.validate_packet(valid_packet("nearest-looking-family"))
        self.assertEqual(captured.exception.finding_id, "unsupported-document-family")

    def test_invalid_packets_are_rejected_before_reviewer_execution(self):
        launcher = launcher_module()
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "executed"
            command_script = write_script(
                directory,
                "marker.py",
                """
                import pathlib
                import sys

                pathlib.Path(sys.argv[1]).write_text("executed")
                """,
            )
            command = [sys.executable, str(command_script), str(marker)]
            invalid_packets = []

            extra_top_level = valid_packet()
            extra_top_level["drafting_history"] = "excluded"
            invalid_packets.append(("extra-top-level", extra_top_level))

            top_level_path = valid_packet()
            top_level_path["path"] = "packet.json"
            invalid_packets.append(("top-level-path", top_level_path))

            top_level_url = valid_packet()
            top_level_url["url"] = "https://example.invalid/packet"
            invalid_packets.append(("top-level-url", top_level_url))

            extra_draft_field = valid_packet()
            extra_draft_field["draft"]["path"] = "draft.md"
            invalid_packets.append(("extra-draft-field", extra_draft_field))

            extra_source_field = valid_packet()
            extra_source_field["sources"][0]["path"] = "source.md"
            invalid_packets.append(("extra-source-field", extra_source_field))

            source_url = valid_packet()
            source_url["sources"][0]["url"] = "https://example.invalid/source"
            invalid_packets.append(("source-url", source_url))

            extra_skill_field = valid_packet()
            extra_skill_field["skill"]["path"] = "SKILL.md"
            invalid_packets.append(("extra-skill-field", extra_skill_field))

            extra_checklist_field = valid_packet()
            extra_checklist_field["checklist"]["path"] = "checklist.md"
            invalid_packets.append(("extra-checklist-field", extra_checklist_field))

            missing_top_level = valid_packet()
            missing_top_level.pop("checklist")
            invalid_packets.append(("missing-top-level", missing_top_level))

            path_only_source = valid_packet()
            path_only_source["sources"][0].pop("content")
            path_only_source["sources"][0]["path"] = "source.md"
            invalid_packets.append(("path-only-source", path_only_source))

            path_only_draft = valid_packet()
            path_only_draft["draft"].pop("content")
            path_only_draft["draft"]["path"] = "draft.md"
            invalid_packets.append(("path-only-draft", path_only_draft))

            path_only_skill = valid_packet()
            path_only_skill["skill"] = {"path": "SKILL.md"}
            invalid_packets.append(("path-only-skill", path_only_skill))

            path_only_checklist = valid_packet()
            path_only_checklist["checklist"] = {"path": "checklist.md"}
            invalid_packets.append(("path-only-checklist", path_only_checklist))

            draft_mismatch = valid_packet()
            draft_mismatch["draft"]["sha256"] = "0" * 64
            invalid_packets.append(("draft-fingerprint", draft_mismatch))

            source_mismatch = valid_packet()
            source_mismatch["sources"][0]["sha256"] = "0" * 64
            invalid_packets.append(("source-fingerprint", source_mismatch))

            forbidden_capability = valid_packet()
            forbidden_capability["capabilities"] = ["filesystem"]
            invalid_packets.append(("capability", forbidden_capability))

            for label, packet in invalid_packets:
                with self.subTest(case=label):
                    with self.assertRaises(launcher.PacketValidationError):
                        launcher.launch_review(
                            packet,
                            command,
                            runtime_enforces_empty_capabilities=True,
                        )
                    self.assertFalse(marker.exists())

    def test_runtime_enforcement_is_required_before_execution(self):
        launcher = launcher_module()
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "executed"
            command_script = write_script(
                directory,
                "marker.py",
                """
                import pathlib
                import sys

                pathlib.Path(sys.argv[1]).write_text("executed")
                """,
            )

            with self.assertRaises(launcher.ReviewLaunchError) as captured:
                launcher.launch_review(
                    valid_packet(),
                    [sys.executable, str(command_script), str(marker)],
                    runtime_enforces_empty_capabilities=False,
                )

            self.assertEqual(
                captured.exception.finding_id,
                "independent-review-unavailable",
            )
            self.assertIn("independent review unavailable", str(captured.exception))
            self.assertFalse(marker.exists())

    def test_timeout_must_be_finite_positive_and_not_boolean(self):
        launcher = launcher_module()
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "executed"
            command_script = write_script(
                directory,
                "marker.py",
                """
                import pathlib
                import sys

                pathlib.Path(sys.argv[1]).write_text("executed")
                """,
            )
            command = [sys.executable, str(command_script), str(marker)]
            for timeout_seconds in (
                True,
                False,
                0,
                -1,
                float("inf"),
                float("nan"),
                "1",
            ):
                with self.subTest(timeout=timeout_seconds):
                    with self.assertRaises(ValueError):
                        launcher.launch_review(
                            valid_packet(),
                            command,
                            runtime_enforces_empty_capabilities=True,
                            timeout_seconds=timeout_seconds,
                        )
                    self.assertFalse(marker.exists())

    def test_dispatch_uses_new_empty_process_scrubbed_env_and_no_shell(self):
        launcher = launcher_module()
        packet = valid_packet()
        with tempfile.TemporaryDirectory() as directory:
            script = spy_script(directory)
            literal_argument = "literal;not-a-shell-command"
            command = [sys.executable, str(script), literal_argument]
            inherited = {
                "CONVERSATION_ID": "excluded",
                "PROVIDER_SESSION": "excluded",
                "THREAD_TOKEN": "excluded",
                "PWD": "excluded",
                "OLDPWD": "excluded",
            }
            with patch.dict(os.environ, inherited):
                first = launcher.launch_review(
                    packet,
                    command,
                    runtime_enforces_empty_capabilities=True,
                )
                second = launcher.launch_review(
                    packet,
                    command,
                    runtime_enforces_empty_capabilities=True,
                )

        self.assertEqual(first["dispatch"]["payload"], packet)
        self.assertEqual(first["dispatch"]["capabilities"], [])
        self.assertEqual(first["response"]["request"], packet)
        self.assertEqual(first["response"]["cwd_entries"], [])
        self.assertEqual(first["response"]["scrubbed_names"], [])
        self.assertEqual(first["response"]["argv"], [literal_argument])
        self.assertRegex(
            first["response"]["process_start_token"],
            r"^[0-9a-f]{32}$",
        )
        self.assertNotEqual(
            first["response"]["process_start_token"],
            second["response"]["process_start_token"],
        )
        self.assertNotEqual(first["response"]["cwd"], second["response"]["cwd"])

        with self.assertRaises(ValueError):
            launcher.launch_review(
                packet,
                "python reviewer.py",
                runtime_enforces_empty_capabilities=True,
            )

    def test_launcher_failure_classes_are_stable_and_streams_bounded(self):
        launcher = launcher_module()
        packet = valid_packet()
        with tempfile.TemporaryDirectory() as directory:
            nonzero = write_script(
                directory,
                "nonzero.py",
                """
                import sys

                sys.stdin.buffer.read()
                sys.stdout.write("o" * 9000)
                sys.stderr.write("e" * 9000)
                raise SystemExit(7)
                """,
            )
            timeout = write_script(
                directory,
                "timeout.py",
                """
                import sys
                import time

                sys.stdin.buffer.read()
                time.sleep(1)
                """,
            )
            malformed = write_script(
                directory,
                "malformed.py",
                """
                import sys

                sys.stdin.buffer.read()
                print("not json")
                """,
            )
            invalid_stdout = write_script(
                directory,
                "invalid_stdout.py",
                """
                import sys

                sys.stdin.buffer.read()
                sys.stdout.buffer.write(b"\\xff" + b"o" * 9000)
                """,
            )
            invalid_stderr = write_script(
                directory,
                "invalid_stderr.py",
                """
                import json
                import sys

                sys.stdin.buffer.read()
                sys.stdout.write(json.dumps({"review": "Synthetic response."}))
                sys.stdout.flush()
                sys.stderr.buffer.write(b"\\xff" + b"e" * 9000)
                raise SystemExit(7)
                """,
            )
            cases = (
                (
                    "unavailable",
                    ["synthetic-reviewer-command-that-does-not-exist"],
                    "reviewer-command-unavailable",
                    1,
                ),
                (
                    "nonzero",
                    [sys.executable, str(nonzero)],
                    "reviewer-command-nonzero",
                    1,
                ),
                (
                    "timeout",
                    [sys.executable, str(timeout)],
                    "reviewer-command-timeout",
                    0.05,
                ),
                (
                    "malformed",
                    [sys.executable, str(malformed)],
                    "reviewer-response-malformed-json",
                    1,
                ),
                (
                    "invalid-stdout",
                    [sys.executable, str(invalid_stdout)],
                    "reviewer-response-malformed-json",
                    1,
                ),
                (
                    "invalid-stderr",
                    [sys.executable, str(invalid_stderr)],
                    "reviewer-command-nonzero",
                    1,
                ),
            )
            for label, command, finding_id, timeout_seconds in cases:
                with self.subTest(case=label):
                    with self.assertRaises(launcher.ReviewLaunchError) as captured:
                        launcher.launch_review(
                            packet,
                            command,
                            runtime_enforces_empty_capabilities=True,
                            timeout_seconds=timeout_seconds,
                        )
                    error = captured.exception
                    self.assertEqual(error.finding_id, finding_id)
                    self.assertLessEqual(len(error.stdout), launcher.STREAM_LIMIT)
                    self.assertLessEqual(len(error.stderr), launcher.STREAM_LIMIT)
                    if label == "nonzero":
                        self.assertTrue(
                            error.stdout.endswith(launcher.TRUNCATION_MARKER)
                        )
                        self.assertTrue(
                            error.stderr.endswith(launcher.TRUNCATION_MARKER)
                        )
                    if label == "invalid-stdout":
                        self.assertIn("\ufffd", error.stdout)
                        self.assertTrue(
                            error.stdout.endswith(launcher.TRUNCATION_MARKER)
                        )
                    if label == "invalid-stderr":
                        self.assertIn("\ufffd", error.stderr)
                        self.assertTrue(
                            error.stderr.endswith(launcher.TRUNCATION_MARKER)
                        )

    def test_cli_accepts_packet_and_command_as_json_argv(self):
        launcher_module()
        packet = valid_packet()
        with tempfile.TemporaryDirectory() as directory:
            script = spy_script(directory)
            literal_argument = "literal;still-not-shell"
            command = [sys.executable, str(script), literal_argument]
            completed = subprocess.run(
                [
                    sys.executable,
                    str(LAUNCHER),
                    "--reviewer-command-json",
                    json.dumps(command),
                    "--runtime-enforces-empty-capabilities",
                    "--timeout-seconds",
                    "1",
                ],
                input=json.dumps(packet),
                cwd=REPOSITORY,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["dispatch"]["payload"], packet)
        self.assertEqual(result["dispatch"]["capabilities"], [])
        self.assertEqual(result["response"]["argv"], [literal_argument])

    def test_cli_requires_runtime_enforcement_before_reviewer_execution(self):
        launcher_module()
        packet = valid_packet()
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "executed"
            script = write_script(
                directory,
                "marker.py",
                """
                import pathlib
                import sys

                sys.stdin.buffer.read()
                pathlib.Path(sys.argv[1]).write_text("executed")
                """,
            )
            command = [sys.executable, str(script), str(marker)]
            completed = subprocess.run(
                [
                    sys.executable,
                    str(LAUNCHER),
                    "--reviewer-command-json",
                    json.dumps(command),
                    "--timeout-seconds",
                    "1",
                ],
                input=json.dumps(packet),
                cwd=REPOSITORY,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(marker.exists())
            self.assertIn(
                "independent review unavailable",
                (completed.stdout + completed.stderr).casefold(),
            )


if __name__ == "__main__":
    unittest.main()
