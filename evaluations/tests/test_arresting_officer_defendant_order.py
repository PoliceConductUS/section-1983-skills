import re
import unittest
from pathlib import Path

import yaml


REPOSITORY = Path(__file__).resolve().parents[2]
SCENARIOS = (
    REPOSITORY
    / "evaluations"
    / "arresting-officer-defendant-order"
    / "v1"
    / "scenarios.yaml"
)
UMBRELLA = REPOSITORY / "skills" / "section-1983-drafting" / "SKILL.md"
COMPLAINT_CONTRACT = (
    REPOSITORY
    / "skills"
    / "drafting-section-1983-complaints"
    / "references"
    / "complaint-contract.md"
)
COMPLETION_AUDIT = (
    REPOSITORY
    / "skills"
    / "drafting-section-1983-complaints"
    / "references"
    / "completion-audit.md"
)
FALSE_ARREST_DELTA = (
    REPOSITORY
    / "skills"
    / "drafting-false-arrest-complaints"
    / "references"
    / "false-arrest-complaint-delta.md"
)


def normalize(text):
    return re.sub(r"\s+", " ", text).strip().casefold()


def scenario_findings(scenario, candidate):
    findings = []
    arresting_officers = scenario["arresting_officers"]
    designated_primary = scenario["designated_primary"]
    presentations = candidate.get("defendant_presentations", {})

    if scenario["arrest_involved"] and len(arresting_officers) > 1 and not designated_primary:
        if candidate.get("outcome") != "clarification-required":
            findings.append("clarification-required")
        if candidate.get("outcome") == "filing" or presentations:
            findings.append("draft-before-primary-designation")
        return sorted(findings)

    if candidate.get("outcome") != "filing":
        findings.append("filing-missing")
        return findings

    if scenario["arrest_involved"]:
        primary = designated_primary or arresting_officers[0]
        for presentation in scenario["required_presentations"]:
            order = presentations.get(presentation)
            if not order:
                findings.append(f"presentation-missing:{presentation}")
            elif order[0] != primary:
                findings.append(f"primary-not-first:{presentation}")
    else:
        for presentation in scenario["required_presentations"]:
            order = presentations.get(presentation)
            if not order:
                findings.append(f"presentation-missing:{presentation}")
            elif order != scenario["caller_defendant_order"]:
                findings.append(f"no-arrest-order-changed:{presentation}")

    if candidate.get("factual_chronology") != scenario["expected_chronology"]:
        findings.append("chronology-reordered")

    return sorted(findings)


class ArrestingOfficerDefendantOrderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = yaml.safe_load(SCENARIOS.read_text(encoding="utf-8"))

    def test_synthetic_scenarios_cover_every_approved_decision_branch(self):
        scenarios = self.corpus["scenarios"]
        self.assertEqual(self.corpus["schema_version"], 1)
        self.assertEqual(
            [scenario["id"] for scenario in scenarios],
            [
                "one-arresting-officer",
                "legacy-order-corrected",
                "several-officers-with-designated-primary",
                "several-officers-without-designated-primary",
                "no-arrest",
            ],
        )

        for scenario in scenarios:
            with self.subTest(scenario=scenario["id"], candidate="passing"):
                self.assertEqual(
                    scenario_findings(scenario, scenario["passing_candidate"]), []
                )
            for regression in scenario["regressions"]:
                with self.subTest(
                    scenario=scenario["id"], regression=regression["id"]
                ):
                    self.assertEqual(
                        scenario_findings(scenario, regression["candidate"]),
                        sorted(regression["expected_findings"]),
                    )

    def test_umbrella_audits_arrest_and_controls_ordered_presentations(self):
        text = normalize(UMBRELLA.read_text(encoding="utf-8"))

        self.assertRegex(
            text,
            r"before (?:drafting|generating).{0,120}materially revising.{0,220}audit.{0,120}whether an arrest occurred",
        )
        for presentation in (
            "caption",
            "parties section",
            "defendant list",
            "defendant-grouped",
        ):
            with self.subTest(presentation=presentation):
                self.assertIn(presentation, text)
        self.assertRegex(
            text,
            r"(?:prior|earlier|existing) filing.{0,120}(?:does not|must not).{0,80}control",
        )
        self.assertRegex(
            text,
            r"multiple arresting officers.{0,220}(?:stop|ask).{0,100}(?:do not|never|must not) infer",
        )
        self.assertRegex(text, r"no arrest.{0,120}preserve.{0,100}caller.{0,80}order")
        self.assertRegex(
            text,
            r"(?:does not|must not|do not) reorder.{0,100}(?:factual )?chronology",
        )

    def test_canonical_complaint_contract_and_audit_enforce_the_same_result(self):
        contract = normalize(COMPLAINT_CONTRACT.read_text(encoding="utf-8"))
        audit = normalize(COMPLETION_AUDIT.read_text(encoding="utf-8"))

        self.assertRegex(
            contract,
            r"primary arresting officer.{0,180}first.{0,180}caption.{0,180}parties",
        )
        self.assertRegex(
            contract,
            r"multiple arresting officers.{0,220}(?:stop|ask).{0,100}(?:do not|never|must not) infer",
        )
        self.assertRegex(
            audit,
            r"arrest.{0,160}primary arresting officer.{0,160}first",
        )

    def test_false_arrest_actor_audit_records_primary_designation_state(self):
        text = normalize(FALSE_ARREST_DELTA.read_text(encoding="utf-8"))

        self.assertRegex(
            text,
            r"actor matrix.{0,500}arresting[- ]officer status.{0,300}caller[- ]declared primary",
        )
        self.assertRegex(
            text,
            r"more than one arresting officer.{0,180}(?:stop|ask).{0,120}(?:do not|never|must not) infer",
        )

    def test_markham_is_only_fixture_data_not_a_public_skill_default(self):
        skill_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (UMBRELLA, COMPLAINT_CONTRACT, COMPLETION_AUDIT, FALSE_ARREST_DELTA)
        ).casefold()
        fixture_text = SCENARIOS.read_text(encoding="utf-8").casefold()

        self.assertNotIn("markham", skill_text)
        self.assertIn("officer markham", fixture_text)


if __name__ == "__main__":
    unittest.main()
