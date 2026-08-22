import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "section-1983-drafting" / "SKILL.md"
WRITING_SYSTEM = (
    ROOT / "skills" / "section-1983-drafting" / "references" / "writing-system.md"
)


def prose(path):
    text = path.read_text()
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    return re.sub(r"\s+", " ", text).strip().lower()


class DraftLinterContractTest(unittest.TestCase):
    def test_drafting_workflow_requires_complete_residual_reconciliation(self):
        combined = f"{prose(SKILL)} {prose(WRITING_SYSTEM)}"

        self.assertIn("zero unexempted violations", combined)
        self.assertRegex(combined, r"every residual (?:hit|finding).{0,100}exactly once")
        self.assertIn("unexempted violation", combined)
        self.assertIn("accurate quotation", combined)
        self.assertIn("controlling term of art", combined)
        self.assertRegex(
            combined,
            r"accurate quotation.{0,160}verified.{0,80}(?:approved )?source",
        )

    def test_warnings_and_score_deltas_are_feedback_not_verdicts(self):
        combined = f"{prose(SKILL)} {prose(WRITING_SYSTEM)}"

        self.assertRegex(combined, r"warning.{0,100}review heuristic")
        self.assertRegex(combined, r"score delta.{0,100}feedback")
        self.assertRegex(
            combined,
            r"(?:never|not).{0,120}(?:merits verdict|legal sufficiency|filing readiness)",
        )


if __name__ == "__main__":
    unittest.main()
