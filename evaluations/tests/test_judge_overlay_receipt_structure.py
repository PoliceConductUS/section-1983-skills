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
SCHOLER_SKILL = ROOT / "skills" / "drafting-for-judge-scholer" / "SKILL.md"


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

    def test_generic_and_assigned_judge_skills_require_receipt_after_composition(self):
        generic = prose(GENERIC_SKILL)
        scholer = prose(SCHOLER_SKILL)

        for label, text in (("generic", generic), ("scholer", scholer)):
            with self.subTest(skill=label):
                self.assertRegex(
                    text,
                    r"judge.{0,80}overlay.{0,160}after.{0,100}(?:document|claim).{0,100}skill",
                )
                self.assertRegex(
                    text,
                    r"immutable.{0,100}(?:execution )?receipt.{0,160}audits/",
                )
                self.assertIn("no judge-specific drafting change", text)
                self.assertRegex(text, r"absence.{0,100}(?:prose|receipt).{0,100}(?:not|does not).{0,100}ran")

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


if __name__ == "__main__":
    unittest.main()
