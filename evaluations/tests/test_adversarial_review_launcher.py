import hashlib
import importlib.util
import unittest
from pathlib import Path


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

    def test_invalid_packets_are_rejected_before_provider_execution(self):
        launcher = launcher_module()
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

        for label, packet_value in invalid_packets:
            with self.subTest(case=label):
                with self.assertRaises(launcher.PacketValidationError):
                    launcher.validate_packet(packet_value)


    def test_whitespace_only_metadata_is_rejected_before_dispatch(self):
        launcher = launcher_module()
        mutations = {
            "draft-version": lambda packet: packet["draft"].update({"version": " \t\n"}),
            "source-id": lambda packet: packet["sources"][0].update({"id": " \t\n"}),
            "source-role": lambda packet: packet["sources"][0].update({"role": " \t\n"}),
            "skill-content": lambda packet: packet["skill"].update({"content": " \t\n"}),
            "checklist-content": lambda packet: packet["checklist"].update({"content": " \t\n"}),
        }
        for label, mutate in mutations.items():
            with self.subTest(field=label):
                packet_value = valid_packet()
                mutate(packet_value)
                with self.assertRaises(launcher.PacketValidationError):
                    launcher.validate_packet(packet_value)

    def test_unpaired_surrogate_in_every_string_field_is_rejected_before_dispatch(self):
        launcher = launcher_module()
        mutations = {
            "draft-content": lambda packet: packet["draft"].update({"content": "\ud800"}),
            "draft-version": lambda packet: packet["draft"].update({"version": "\ud800"}),
            "draft-sha256": lambda packet: packet["draft"].update({"sha256": "\ud800"}),
            "document-family": lambda packet: packet.update({"document_family": "\ud800"}),
            "source-id": lambda packet: packet["sources"][0].update({"id": "\ud800"}),
            "source-role": lambda packet: packet["sources"][0].update({"role": "\ud800"}),
            "source-content": lambda packet: packet["sources"][0].update({"content": "\ud800"}),
            "source-sha256": lambda packet: packet["sources"][0].update({"sha256": "\ud800"}),
            "skill-content": lambda packet: packet["skill"].update({"content": "\ud800"}),
            "checklist-content": lambda packet: packet["checklist"].update({"content": "\ud800"}),
        }
        for label, mutate in mutations.items():
            with self.subTest(field=label):
                packet_value = valid_packet()
                mutate(packet_value)
                with self.assertRaises(launcher.PacketValidationError):
                    launcher.validate_packet(packet_value)

    def test_content_hashes_use_exact_untrimmed_text(self):
        launcher = launcher_module()
        packet = valid_packet()
        draft_content = "  Synthetic draft with exact whitespace.  \n"
        source_content = "\tSynthetic source with exact whitespace. \n"
        packet["draft"]["content"] = draft_content
        packet["draft"]["sha256"] = sha256(draft_content)
        packet["sources"][0]["content"] = source_content
        packet["sources"][0]["sha256"] = sha256(source_content)

        validated = launcher.validate_packet(packet)

        self.assertEqual(validated["draft"]["content"], draft_content)
        self.assertEqual(validated["draft"]["sha256"], sha256(draft_content))
        self.assertEqual(validated["sources"][0]["content"], source_content)
        self.assertEqual(
            validated["sources"][0]["sha256"],
            sha256(source_content),
        )

    def test_timeout_must_be_finite_positive_and_not_boolean(self):
        launcher = launcher_module()
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
                    launcher._positive_timeout(timeout_seconds)



if __name__ == "__main__":
    unittest.main()
