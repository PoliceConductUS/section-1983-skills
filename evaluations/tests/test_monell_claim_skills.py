import re
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
SKILLS = REPOSITORY / "skills"
PLANNER = SKILLS / "planning-section-1983-monell-claims"


class MonellPlanningSkillTests(unittest.TestCase):
    def test_planner_has_install_local_path_and_casegraph_contracts(self):
        required = {
            "SKILL.md",
            "agents/openai.yaml",
            "references/path-planning-contract.md",
            "references/casegraph-assessment-contract.md",
        }
        actual = {
            str(path.relative_to(PLANNER))
            for path in PLANNER.rglob("*")
            if path.is_file()
        }
        self.assertTrue(required.issubset(actual), required - actual)

    def test_planner_separates_paths_recommendations_and_reserved_decision(self):
        text = (PLANNER / "SKILL.md").read_text(encoding="utf-8")
        for path_type in (
            "formal_policy",
            "custom_or_practice",
            "final_policymaker_decision",
            "ratification",
            "failure_to_train",
            "failure_to_supervise_or_discipline",
        ):
            self.assertIn(path_type, text)
        for recommendation in (
            "include",
            "include-with-narrowing",
            "preserve-internal",
            "omit",
        ):
            self.assertIn(recommendation, text)
        self.assertRegex(text, r"(?is)one stable record.*one path type")
        self.assertRegex(text, r"(?is)litigation principal.*(?:approves|selects|decision)")
        self.assertRegex(text, r"(?is)contrary material.*missing connections.*consequences")

    def test_planner_keeps_mechanisms_and_temporal_lanes_bounded(self):
        text = (PLANNER / "references/path-planning-contract.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?is)FTO.*mechanism")
        self.assertRegex(text, r"(?is)post-event.*(?:notice|ratification|recurrence|later-injury|corroboration)")
        self.assertRegex(text, r"(?is)post-event.*(?:must not|cannot).*pre-event causation")

    def test_planner_reads_graph_directly_and_fails_closed_on_authority_text(self):
        text = (PLANNER / "references/casegraph-assessment-contract.md").read_text(encoding="utf-8")
        self.assertIn("config.yaml", text)
        self.assertIn("<uid>/root.yaml", text)
        self.assertRegex(text, r"(?is)read-only.*(?:do not|never).*CLI")
        self.assertRegex(text, r"(?is)SOURCE\.yaml.*SHA-256.*pinpoint.*exact matching")
        self.assertRegex(text, r"(?is)fuzzy.*(?:does not|cannot|insufficient)")
        for status in (
            "not_run_missing",
            "not_run_invalid",
            "not_run_incompatible",
            "not_run_stale",
            "partial",
            "completed",
        ):
            self.assertIn(status, text)


if __name__ == "__main__":
    unittest.main()
