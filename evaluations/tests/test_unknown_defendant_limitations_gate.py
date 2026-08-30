import re
import unittest
from pathlib import Path

import yaml


REPOSITORY = Path(__file__).resolve().parents[2]
SCENARIOS = (
    REPOSITORY
    / "evaluations"
    / "unknown-defendant-limitations"
    / "v1"
    / "scenarios.yaml"
)
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


def normalize(text):
    return re.sub(r"\s+", " ", text).strip().casefold()


def unresolved(value):
    return value is None or value == "" or (
        isinstance(value, str) and value.casefold() in {"missing", "unsupported", "unresolved"}
    )


def scenario_findings(scenario, candidate, required_fields):
    findings = []
    gate_required = bool(
        scenario["calculated_deadline_passed"] or scenario["raised_risks"]
    )
    records = candidate.get("records", {})
    unresolved_entries = []
    declared_gaps = set(candidate.get("filing_critical_gaps", []))

    if gate_required and not candidate.get("gate_applied"):
        findings.append("gate-required")

    if gate_required:
        for defendant in scenario["affected_defendants"]:
            record = records.get(defendant)
            if record is None:
                entry = f"{defendant}:record"
                if entry not in declared_gaps:
                    findings.append(f"missing-record:{defendant}")
                unresolved_entries.append(entry)
                continue
            for field in required_fields:
                if unresolved(record.get(field)):
                    entry = f"{defendant}:{field}"
                    if entry not in declared_gaps:
                        findings.append(f"missing-entry:{entry}")
                    unresolved_entries.append(entry)

    if unresolved_entries and candidate.get("filing_ready"):
        findings.append("filing-ready-with-unresolved-limitations")
    elif unresolved_entries and not set(unresolved_entries).issubset(declared_gaps):
        findings.append("unresolved-entry-not-filing-critical")

    return sorted(findings)


class UnknownDefendantLimitationsGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = yaml.safe_load(SCENARIOS.read_text(encoding="utf-8"))

    def test_synthetic_scenarios_cover_the_approved_gate(self):
        self.assertEqual(self.corpus["schema_version"], 1)
        self.assertEqual(
            [scenario["id"] for scenario in self.corpus["scenarios"]],
            [
                "passed-deadline-complete-record",
                "identified-pre-deadline-risk",
                "separate-record-per-affected-defendant",
                "unresolved-entry-fails-closed",
                "no-identified-limitations-risk",
            ],
        )

        required_fields = self.corpus["required_record_fields"]
        self.assertEqual(len(required_fields), 12)
        for scenario in self.corpus["scenarios"]:
            with self.subTest(scenario=scenario["id"], candidate="passing"):
                self.assertEqual(
                    scenario_findings(
                        scenario, scenario["passing_candidate"], required_fields
                    ),
                    [],
                )
            for regression in scenario["regressions"]:
                with self.subTest(
                    scenario=scenario["id"], regression=regression["id"]
                ):
                    self.assertEqual(
                        scenario_findings(
                            scenario, regression["candidate"], required_fields
                        ),
                        sorted(regression["expected_findings"]),
                    )

    def test_contract_uses_record_driven_trigger_without_a_day_count(self):
        text = normalize(COMPLAINT_CONTRACT.read_text(encoding="utf-8"))

        self.assertRegex(
            text,
            r"adds?.{0,80}(?:identifies|names).{0,80}substitutes?.{0,180}individual defendant",
        )
        self.assertRegex(
            text,
            r"calculated limitations deadline.{0,100}(?:passed|expired)",
        )
        for source in ("supplied record", "opposing party", "court", "caller"):
            with self.subTest(source=source):
                self.assertIn(source, text)
        self.assertRegex(
            text,
            r"(?:does not|must not|never).{0,120}universal.{0,80}(?:day|numeric).{0,80}(?:near limitations|threshold)",
        )

    def test_contract_requires_every_defendant_specific_entry(self):
        text = normalize(COMPLAINT_CONTRACT.read_text(encoding="utf-8"))

        self.assertRegex(text, r"separate.{0,100}(?:record|analysis).{0,100}(?:each|every).{0,80}individual")
        required_phrases = (
            "accrual date",
            "limitations deadline",
            "doe",
            "role description",
            "same transaction",
            "rule 15(c)(1)(a)",
            "rule 15(c)(1)(c)",
            "mistake",
            "lack of knowledge",
            "rule 4(m)",
            "notice",
            "service",
            "source first became available",
            "first possessed",
            "objectively ascertainable",
            "actual identification",
            "identification source and method",
            "pre-limitations diligence",
            "post-filing/pre-identification diligence",
            "post-identification/pre-service diligence",
            "holder or controller",
            "request recipient",
            "denial date",
            "follow-up dates",
            "notice recipient",
            "service status",
            "extension-request status",
            "controlling jurisdiction",
            "governing authority",
            "pinpoint",
            "defendant-specific application",
            "concealment",
            "tolling",
            "fallback claims",
            "severable relief",
        )
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertRegex(
            text,
            r"rule 15\(c\)\(1\)\(a\).{0,180}separate.{0,180}rule 15\(c\)\(1\)\(c\)",
        )

    def test_audit_fails_closed_for_every_unresolved_entry(self):
        text = normalize(COMPLETION_AUDIT.read_text(encoding="utf-8"))

        self.assertRegex(
            text,
            r"(?:each|every).{0,100}affected individual.{0,180}(?:limitations record|record).{0,180}complete",
        )
        self.assertRegex(
            text,
            r"(?:missing|unsupported|unresolved).{0,160}(?:entry|field).{0,160}filing-critical gap",
        )
        self.assertRegex(
            text,
            r"filing-critical gap.{0,120}(?:blocks|must not|do not mark).{0,100}filing-ready",
        )


if __name__ == "__main__":
    unittest.main()
