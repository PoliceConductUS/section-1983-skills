import copy
import json
import re
import unittest
from pathlib import Path

from evaluations.deterministic import grade_candidate
from evaluations.fixtures import load_fixture


REPOSITORY = Path(__file__).resolve().parents[2]
SKILLS = REPOSITORY / "skills"
PLANNER = SKILLS / "planning-section-1983-monell-claims"
DRAFTER = SKILLS / "drafting-section-1983-monell-claims"
STAGED_FIXTURE = REPOSITORY / "evaluations" / "fixtures" / "monell-staged-development"


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

    def test_planner_classifies_every_monell_proposition(self):
        text = (PLANNER / "references/path-planning-contract.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?is)common record.*propositions")
        for proposition_class in (
            "source-documented fact",
            "supported inference",
            "expected-discovery proposition",
        ):
            self.assertIn(proposition_class, text)
        self.assertRegex(
            text,
            r"(?is)supported\s+inference.*identified\s+pleaded\s+facts",
        )
        self.assertRegex(
            text,
            r"(?is)expected-discovery\s+proposition.*(?:not|never).*present\s+fact.*evidence",
        )

    def test_planner_defines_complete_staged_development_record(self):
        skill = (PLANNER / "SKILL.md").read_text(encoding="utf-8")
        contract = (PLANNER / "references/path-planning-contract.md").read_text(
            encoding="utf-8"
        )
        text = "\n".join((skill, contract))
        normalized = text.casefold().replace("_", " ").replace("-", " ")

        self.assertRegex(
            text,
            r"(?is)presently supportable.*narrowest\s+(?:factually\s+)?plausible",
        )
        self.assertRegex(text, r"(?is)(?:do not|must not).*speculative.*placeholder")
        self.assertRegex(text, r"(?is)preserve-internal.*staged.development")
        self.assertRegex(
            text,
            r"(?is)relative (?:deadline )?interval.*not (?:an exact date|enough)",
        )
        self.assertRegex(
            text,
            r"(?is)do\s+not\s+(?:calculate|derive).*source-backed as-of date",
        )
        for field in (
            "missing connection",
            "expected records or testimony",
            "information controller",
            "independent relevance",
            "anticipated discovery restrictions or stays",
            "requested at",
            "produced at",
            "first reasonably knowable at",
            "diligence record",
            "pleading amendment deadline",
            "evidence threshold",
            "limitations or relation back risk",
        ):
            self.assertIn(field, normalized)

    def test_planner_keeps_discovery_and_amendment_conditional(self):
        text = "\n".join(
            (
                (PLANNER / "SKILL.md").read_text(encoding="utf-8"),
                (PLANNER / "references/path-planning-contract.md").read_text(
                    encoding="utf-8"
                ),
            )
        )
        self.assertRegex(
            text,
            r"(?is)(?:does not|must not).*assume.*discovery.*individual claim.*surviv",
        )
        self.assertRegex(text, r"(?is)each.*request.*independent relevance.*live claim or defense")
        self.assertRegex(text, r"(?is)responsive material.*before.*amendment deadline")
        self.assertRegex(text, r"(?is)after.*deadline.*Rule 16.*good cause.*before.*Rule 15")
        self.assertRegex(text, r"(?is)litigation principal.*approv.*amend")

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

    def test_delta_places_monell_propositions_by_class(self):
        text = (DRAFTER / "references/monell-complaint-delta.md").read_text(encoding="utf-8")
        self.assertRegex(
            text,
            r"(?is)complaint\s+may\s+allege.*source-documented\s+facts.*supported\s+inferences",
        )
        self.assertRegex(
            text,
            r"(?is)expected-discovery\s+propositions.*not\s+present\s+facts\s+or\s+evidence.*discovery\s+plan",
        )
        self.assertRegex(
            text,
            r"(?is)supporting\s+brief.*may\s+explain.*reasonable\s+inference.*may\s+not\s+supply.*missing\s+complaint-\s*level\s+factual\s+basis",
        )
        self.assertRegex(text, r"(?is)typed delta.*propositions")

    def test_delta_bars_placeholder_preservation_and_gates_later_amendment(self):
        skill = (DRAFTER / "SKILL.md").read_text(encoding="utf-8")
        delta = (DRAFTER / "references/monell-complaint-delta.md").read_text(
            encoding="utf-8"
        )
        text = "\n".join((skill, delta))

        for forbidden_basis in ("boilerplate", "underlying incident alone", "expected-discovery"):
            self.assertIn(forbidden_basis, text.casefold())
        self.assertRegex(text, r"(?is)(?:do not|must not).*placeholder.*preserve")
        self.assertRegex(text, r"(?is)evidence threshold.*met")
        self.assertRegex(text, r"(?is)applicable amendment gate.*satisfied")
        self.assertRegex(text, r"(?is)litigation principal.*approv.*amend")

    def test_approved_handoff_preserves_proposition_records(self):
        text = (DRAFTER / "references/approved-planning-handoff.md").read_text(
            encoding="utf-8"
        )
        self.assertRegex(
            text,
            r"(?is)carry\s+forward.*proposition\s+record.*classification.*placement",
        )

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

    def test_staged_development_regressions_are_permanent_and_discriminating(self):
        fixture = load_fixture(STAGED_FIXTURE)
        self.assertEqual(fixture["target_skill"], "planning-section-1983-monell-claims")
        self.assertTrue(grade_candidate(fixture, fixture["passing_candidate"])["passed"])
        self.assertEqual(len(fixture["regressions"]), 14)

        required_fields = set(fixture["deterministic"]["required_fields"])
        for field in (
            "staged_development.discovery_requests",
            "staged_development.diligence_record.current_chronology",
            "staged_development.pleading_amendment_deadline.resolution_step",
            "staged_development.evidence_threshold_for_amendment",
            "staged_development.reassessment_triggers.before_deadline",
            "staged_development.limitations_or_relation_back_risk",
            "staged_development.amendment_conditions.rule16_before_rule15_after_deadline",
            "staged_development.amendment_conditions.principal_approval_required",
        ):
            self.assertIn(field, required_fields)

        request_rules = fixture["deterministic"]["required_object_entries"]
        self.assertEqual(len(request_rules), 1)
        self.assertEqual(
            request_rules[0]["address"], "staged_development.discovery_requests"
        )
        self.assertEqual(
            set(request_rules[0]["required_nonempty_string_fields"]),
            {
                "request_id",
                "target_material",
                "independent_relevance",
                "anticipated_restrictions_or_stays",
                "requested_at",
                "produced_at",
                "first_reasonably_knowable_at",
            },
        )

        for regression in fixture["regressions"]:
            with self.subTest(regression=regression["id"]):
                result = grade_candidate(fixture, regression["candidate"])
                observed_ids = {finding["id"] for finding in result["findings"]}
                self.assertTrue(
                    set(regression["expected_findings"]).issubset(observed_ids)
                )
                self.assertEqual(len(result["findings"]), 1)

    def test_staged_fixture_rejects_invalid_gate_values(self):
        fixture = load_fixture(STAGED_FIXTURE)
        passing = json.loads(fixture["passing_candidate"])
        requests = passing["staged_development"]["discovery_requests"]
        self.assertIsInstance(requests, dict)
        self.assertGreaterEqual(len(requests), 2)

        mutations = (
            lambda candidate: candidate.__setitem__("recommendation", "include"),
            lambda candidate: candidate["principal_decision"].__setitem__(
                "status", "approved"
            ),
            lambda candidate: candidate.__setitem__(
                "principal_decision",
                {"reason": "not yet approved", "status": "approved"},
            ),
            lambda candidate: candidate["staged_development"]["discovery_requests"][
                "R-001"
            ].__setitem__("request_id", "R-999"),
            lambda candidate: candidate["staged_development"]["discovery_requests"][
                "R-001"
            ].__setitem__("independent_relevance", ""),
            lambda candidate: candidate["staged_development"]["discovery_requests"][
                "R-001"
            ].__setitem__("anticipated_restrictions_or_stays", ""),
            lambda candidate: candidate["staged_development"].__setitem__(
                "evidence_threshold_for_amendment", ""
            ),
            lambda candidate: candidate["staged_development"].__setitem__(
                "evidence_threshold_for_amendment", True
            ),
            lambda candidate: candidate["staged_development"][
                "reassessment_triggers"
            ].__setitem__("on_responsive_material", "not required"),
            lambda candidate: candidate["staged_development"][
                "reassessment_triggers"
            ].__setitem__("before_deadline", "optional"),
            lambda candidate: candidate["staged_development"]["discovery_requests"][
                "R-001"
            ].__setitem__("independent_relevance", None),
            lambda candidate: candidate["staged_development"]["discovery_requests"].__setitem__(
                "R-003", {}
            ),
            lambda candidate: candidate["staged_development"][
                "amendment_conditions"
            ].__setitem__("rule16_before_rule15_after_deadline", "not required"),
            lambda candidate: candidate["staged_development"][
                "amendment_conditions"
            ].__setitem__("principal_approval_required", "no"),
            lambda candidate: candidate["validation"].__setitem__(
                "expected_discovery_treatment", "May be treated as fact"
            ),
            lambda candidate: candidate["validation"].__setitem__(
                "brief_cure", "The brief may cure the omission"
            ),
        )

        for index, mutate in enumerate(mutations):
            with self.subTest(invalid_case=index):
                candidate = copy.deepcopy(passing)
                mutate(candidate)
                self.assertFalse(grade_candidate(fixture, candidate)["passed"])


if __name__ == "__main__":
    unittest.main()
