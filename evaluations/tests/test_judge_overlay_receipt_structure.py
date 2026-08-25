import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "skills" / "section-1983-drafting"
SCHEMA = PACKAGE / "references" / "judge-overlay-execution.schema.json"
SCRIPT = PACKAGE / "scripts" / "judge_overlay_receipt.py"
JUDGE_GUIDE = ROOT / "JUDGE_OVERLAYS.md"
GENERIC_SKILL = PACKAGE / "SKILL.md"


def prose(path):
    text = path.read_text()
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    return re.sub(r"\s+", " ", text).strip().casefold()


class JudgeOverlayReceiptStructureTest(unittest.TestCase):
    def test_public_schema_and_script_are_install_local(self):
        self.assertTrue(SCHEMA.is_file(), SCHEMA)
        self.assertTrue(SCRIPT.is_file(), SCRIPT)

        schema = json.loads(SCHEMA.read_text())
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(schema["type"], "object")
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(
            set(schema["required"]),
            {
                "schema_version",
                "audited_version_id",
                "scope",
                "approved_source_ids",
                "artifacts",
                "overlay",
                "corpus",
                "court_conduct_inputs",
                "transfer_cards",
                "prohibited_inference_checks",
                "requested_result",
            },
        )
        self.assertEqual(
            schema["$defs"]["validationStatus"]["enum"],
            ["passed", "missing", "stale", "failed", "unavailable"],
        )

    def test_generic_drafting_skill_requires_folder_native_receipt_after_composition(self):
        generic = prose(GENERIC_SKILL)
        self.assertIn("building-judicial-reasoning-profiles", generic)
        self.assertRegex(generic, r"profile-backed review.{0,100}separate.{0,100}invocation")
        self.assertNotRegex(
            generic,
            r"(?is)(?:--project-boundary|--version-folder|<version-folder>/audits/|canonical `audits/`)",
        )

    def test_judge_guide_routes_to_schema_script_and_quality_control_boundary(self):
        guide = JUDGE_GUIDE.read_text()
        lower = prose(JUDGE_GUIDE)

        self.assertIn(
            "skills/section-1983-drafting/references/judge-overlay-execution.schema.json",
            guide,
        )
        self.assertIn(
            "skills/section-1983-drafting/scripts/judge_overlay_receipt.py",
            guide,
        )
        self.assertRegex(lower, r"no judge-specific drafting change.{0,160}bounded reason")
        self.assertRegex(lower, r"missing.{0,50}stale.{0,50}(?:invalid|failed).{0,50}unavailable.{0,100}fail")
        self.assertRegex(lower, r"must not.{0,100}(?:edit|modify).{0,100}(?:filing|artifact)")
        self.assertRegex(lower, r"declared.{0,100}filing.{0,100}(?:role|root)")
        self.assertRegex(lower, r"judge-corpus.{0,100}court-conduct")
        self.assertRegex(lower, r"required.{0,80}filing target")
        self.assertRegex(lower, r"(?:trusted host|outputrun).{0,120}(?:publish|write)")
        self.assertNotRegex(
            lower,
            r"(?:project boundary|version folder|canonical `?audits/?`? directory)",
        )


if __name__ == "__main__":
    unittest.main()
