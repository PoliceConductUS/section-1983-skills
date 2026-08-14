import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


def normalized(text):
    return " ".join(text.split())


class ConcessionPolicyTest(unittest.TestCase):

    def test_skill_makes_express_user_approval_the_default_gate(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text()

        self.assertIn("No concession by default", skill)
        self.assertIn("express user approval", skill)

    def test_writing_system_requires_attribution_and_forbids_speculation(self):
        writing_system = (
            SKILL_ROOT / "references" / "writing-system.md"
        ).read_text()

        self.assertIn("## PARTY POSITIONS AND CONCESSIONS", writing_system)
        self.assertIn("Attribute an adverse characterization", writing_system)
        self.assertIn("Do not speculate against the client", writing_system)

    def test_objection_framework_does_not_recommend_harmless_concessions(self):
        objection = (
            SKILL_ROOT / "references" / "documents" / "rr-objection.md"
        ).read_text()

        objection = normalized(objection)

        self.assertNotIn("conceding a harmless point costs nothing", objection)
        self.assertIn("Omit a harmless point without conceding it", objection)


if __name__ == "__main__":
    unittest.main()
