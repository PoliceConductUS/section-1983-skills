import re
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
FILING_CI = REPOSITORY / "skills" / "filing-ci" / "SKILL.md"


class MonellFilingCiTests(unittest.TestCase):
    def test_filing_ci_uses_canonical_v2_validator_and_separate_layers(self):
        text = FILING_CI.read_text(encoding="utf-8")
        self.assertIn("validate_complaint_handoff.py", text)
        self.assertIn("contract version 2", text)
        self.assertIn("structural_validation", text)
        self.assertIn("casegraph_assessment", text)
        self.assertRegex(text, r"(?is)(?:do not|never).*collapse.*(?:unqualified|overall).*pass")

    def test_drafting_and_filing_modes_have_distinct_graph_gates(self):
        text = FILING_CI.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?is)drafting mode.*(?:may|can).*not_run_missing")
        self.assertRegex(text, r"(?is)filing mode.*requires.*every included.*claim")
        for status in (
            "completed",
            "partial",
            "not_run_missing",
            "not_run_invalid",
            "not_run_incompatible",
            "not_run_stale",
        ):
            self.assertIn(status, text)

    def test_unresolved_exact_authority_text_keeps_filing_gate_open(self):
        text = FILING_CI.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?is)authority.*pinpoint.*exact.*passage")
        self.assertRegex(text, r"(?is)(?:missing|ambiguous|nonmatching).*filing gate.*open")


if __name__ == "__main__":
    unittest.main()
