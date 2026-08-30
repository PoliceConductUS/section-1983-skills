import re
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
SKILLS = REPOSITORY / "skills"
PLANNER = SKILLS / "planning-section-1983-monell-claims"
DRAFTER = SKILLS / "drafting-section-1983-monell-claims"


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
        self.assertRegex(text, r"(?is)evaluate all six")
        self.assertRegex(text, r"(?is)every\s+distinct\s+candidate.*multiple.*same.*type")
        self.assertRegex(text, r"(?is)litigation principal.*(?:approves|selects|decision)")
        self.assertRegex(text, r"(?is)contrary material.*missing connections.*consequences")

    def test_planner_keeps_mechanisms_and_temporal_lanes_bounded(self):
        text = (PLANNER / "references/path-planning-contract.md").read_text(encoding="utf-8")
        self.assertIn("principal_decision", text)
        self.assertIn("graph_assessment_status", text)
        self.assertRegex(text, r"(?is)FTO.*mechanism")
        self.assertRegex(text, r"(?is)repeated.*policy.*formal_policy.*information.and.belief")
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
        for value in (
            "satisfied",
            "strong_supported_inference",
            "procedural_usability",
            "plausibly_sufficient_but_vulnerable",
            "indeterminate",
        ):
            self.assertIn(value, text)


class MonellDraftingSkillTests(unittest.TestCase):
    def test_drafter_has_approved_plan_and_delta_contracts(self):
        required = {
            "SKILL.md",
            "agents/openai.yaml",
            "references/approved-planning-handoff.md",
            "references/monell-complaint-delta.md",
        }
        actual = {
            str(path.relative_to(DRAFTER))
            for path in DRAFTER.rglob("*")
            if path.is_file()
        }
        self.assertTrue(required.issubset(actual), required - actual)

    def test_drafter_uses_only_approved_paths_and_returns_to_canonical_owner(self):
        text = (DRAFTER / "SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?is)draft only.*approved.*path")
        self.assertRegex(text, r"(?is)(?:do not|never).*select.*claim")
        self.assertIn("drafting-section-1983-complaints", text)
        self.assertIn("validate_complaint_handoff.py", text)
        self.assertRegex(text, r"(?is)one.*path_id.*one.*path_type")

    def test_delta_preserves_mechanism_information_belief_and_temporal_bounds(self):
        text = (DRAFTER / "references/monell-complaint-delta.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?is)implementation or transmission mechanism")
        self.assertRegex(text, r"(?is)information and belief.*known facts.*controlled")
        self.assertRegex(text, r"(?is)post-event.*(?:cannot|must not).*pre-event\s+causation")
        self.assertRegex(text, r"(?is)moving.force")
        self.assertRegex(text, r"(?is)particular\s+injury")
        for lane in (
            "pre_event_notice",
            "event_implementation",
            "post_event_ratification",
            "recurrence",
            "later_injury",
            "corroboration",
        ):
            self.assertIn(lane, text)
        self.assertRegex(text, r"(?is)formal_policy.*repeated.*information.and.belief.*unresolved")
        self.assertRegex(text, r"(?is)do\s+not\s+silently\s+retype.*custom_or_practice")
        self.assertRegex(text, r"(?is)fuzzy.*cannot.*exact passage")

    def test_drafter_cannot_convert_recommendation_into_approval(self):
        text = (DRAFTER / "references/approved-planning-handoff.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?is)recommendation.*(?:is not|does not).*approval")
        self.assertRegex(text, r"(?is)litigation principal.*(?:approved|approval)")
        self.assertRegex(text, r"(?is)(?:missing|ambiguous).*approval.*stop")
        for field in (
            "status: approved",
            "approver identity",
            "approval scope",
            "approved narrowing",
            "decision-record\nSHA-256",
        ):
            self.assertIn(field, text)


if __name__ == "__main__":
    unittest.main()
