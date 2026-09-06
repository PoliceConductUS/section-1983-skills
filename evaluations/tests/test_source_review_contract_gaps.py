import copy
import json
import tempfile
import unittest
from pathlib import Path

from evaluations.tests.test_complaint_candor_contract import (
    assert_clause_contains,
    assert_no_clause_contains,
    markdown_sections,
    normalized_prose,
    normalized_value,
)
from evaluations.tests.test_installed_filing_checks import (
    CHECKER_ID,
    COMPLAINT_SCRIPT,
    FILING_CI_SCRIPT,
    complaint_document,
    load_module,
    packaged_complaint_contract,
)


REPOSITORY = Path(__file__).resolve().parents[2]
SKILLS = REPOSITORY / "skills"
GENERAL_PACKAGE = SKILLS / "drafting-section-1983-complaints"
FALSE_ARREST_PACKAGE = SKILLS / "drafting-false-arrest-complaints"
UMBRELLA_PACKAGE = SKILLS / "section-1983-drafting"
FILING_CI_PACKAGE = SKILLS / "filing-ci"
COMPLAINT_CONTRACT = GENERAL_PACKAGE / "references" / "complaint-contract.md"
CLAIM_CONTRACTS = GENERAL_PACKAGE / "references" / "claim-specific-contracts.md"
COMPLETION_AUDIT = GENERAL_PACKAGE / "references" / "completion-audit.md"
STRUCTURE_CONTRACT = GENERAL_PACKAGE / "references" / "complaint-structure-contract.json"
FALSE_ARREST_DELTA = (
    FALSE_ARREST_PACKAGE / "references" / "false-arrest-complaint-delta.md"
)
CASE_MAP = UMBRELLA_PACKAGE / "references" / "case-map.md"
PRIVACY_CHECKS = (
    "privacy-gate-presence",
    "privacy-gate-structure",
    "privacy-filing-critical-status",
)
IDENTIFIER_CATEGORIES = (
    "social-security-number",
    "taxpayer-identification-number",
    "birth-date",
    "financial-account-number",
)


def protected_identifier(category, status="absent", **overrides):
    value = {
        "category": category,
        "status": status,
        "locations": [],
        "authorization_basis": "",
    }
    value.update(overrides)
    return value


def minor_party(party_id="plaintiff-child", name_form="initials", basis=""):
    return {
        "party_id": party_id,
        "name_form": name_form,
        "authorization_basis": basis,
    }


def complaint_checker_findings(document):
    checker = load_module("source_review_complaint_checker", COMPLAINT_SCRIPT)
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "complaint.json").write_text(json.dumps(document))
        result = checker.check_complaint(root, "complaint.json")
    return result


def filing_ci_findings(document):
    filing_ci = load_module("source_review_filing_ci", FILING_CI_SCRIPT)
    with tempfile.TemporaryDirectory() as directory:
        base = Path(directory)
        filing_root = base / "filing"
        authorities_root = base / "authorities"
        filing_root.mkdir()
        authorities_root.mkdir()
        (filing_root / "complaint.json").write_text(json.dumps(document))
        result = filing_ci.run_filing_ci(
            filing_root,
            "complaint.json",
            authorities_root,
            CHECKER_ID,
        )
    return result


def check_ids(result):
    return {finding["check_id"] for finding in result["findings"]}


class CriminalPostureAndAccrualContractTest(unittest.TestCase):
    def test_complaint_contract_owns_criminal_proceeding_posture_and_accrual(self):
        markdown = COMPLAINT_CONTRACT.read_text(encoding="utf-8")
        sections = markdown_sections(
            markdown, r"criminal[- ]proceeding posture"
        )
        self.assertEqual(len(sections), 1, "one criminal-posture section is required")
        text = normalized_value(sections[0])
        for authority in (
            r"heck v\. humphrey",
            r"wallace v\. kato",
            r"mcdonough v\. smith",
            r"thompson v\. clark",
        ):
            with self.subTest(authority=authority):
                self.assertRegex(text, authority)
        assert_clause_contains(self, text, r"false[- ]arrest", r"legal process")
        assert_clause_contains(
            self, text, r"malicious[- ]prosecution", r"ended without a conviction"
        )
        assert_clause_contains(
            self, text, r"fabricated[- ]evidence", r"(?:favor|favorable termination)"
        )
        assert_clause_contains(self, text, r"necessarily imply", r"invalidity")
        assert_clause_contains(self, text, r"pending charge", r"does not delay")
        assert_clause_contains(self, text, r"\bstay\b", r"criminal case")
        assert_clause_contains(
            self, text, r"(?:file|stay|alternative|omit)", r"reserved user decision"
        )
        assert_clause_contains(self, text, r"do not select")
        assert_clause_contains(
            self, text, r"(?:do not|must not)", r"heck[- ]barred", r"filed text"
        )
        assert_clause_contains(
            self, text, r"(?:no charge|pending|dismissed|acquitted|convicted|plea|expunged)"
        )

    def test_false_arrest_delta_routes_criminal_posture_to_the_canonical_contract(self):
        text = normalized_prose(FALSE_ARREST_DELTA)
        assert_clause_contains(
            self, text, r"criminal[- ]proceeding posture", r"canonical"
        )
        assert_clause_contains(self, text, r"accru", r"legal process")
        assert_no_clause_contains(self, text, r"accru", r"favorable termination", r"false[- ]arrest claim accrues")

    def test_entry_skill_case_map_notes_claim_specific_accrual(self):
        text = normalized_value(CASE_MAP.read_text(encoding="utf-8"))
        self.assertRegex(text, r"accrual is federal and differs by claim")


class ExcessiveForceSequenceContractTest(unittest.TestCase):
    def test_excessive_force_contract_requires_the_events_preceding_the_force(self):
        markdown = CLAIM_CONTRACTS.read_text(encoding="utf-8")
        sections = markdown_sections(markdown, r"^excessive force$")
        self.assertEqual(len(sections), 1)
        text = normalized_value(sections[0])
        assert_clause_contains(self, text, r"events preceding the force")
        assert_clause_contains(
            self, text, r"(?:do not|must not) confine", r"moment"
        )
        assert_clause_contains(self, text, r"totality", r"no time limit")
        self.assertRegex(text, r"barnes v\. felix")
        self.assertRegex(text, r"2025")

    def test_fair_warning_comparison_includes_pre_force_events(self):
        text = normalized_prose(COMPLAINT_CONTRACT)
        assert_clause_contains(
            self, text, r"force type", r"duration", r"pre[- ]force events"
        )


class PrivacyRedactionContractTest(unittest.TestCase):
    def test_complaint_contract_owns_rule_5_2_privacy_redaction(self):
        markdown = COMPLAINT_CONTRACT.read_text(encoding="utf-8")
        sections = markdown_sections(markdown, r"rule 5\.2")
        self.assertEqual(len(sections), 1, "one Rule 5.2 section is required")
        text = normalized_value(sections[0])
        assert_clause_contains(self, text, r"last four digits", r"social[- ]security")
        assert_clause_contains(self, text, r"year of", r"birth")
        assert_clause_contains(self, text, r"minor", r"initials")
        assert_clause_contains(self, text, r"last four digits", r"financial[- ]account")
        self.assertRegex(text, r"taxpayer[- ]identification")
        self.assertIn("`privacy_gate`", sections[0])
        assert_clause_contains(self, text, r"unredacted", r"reserved (?:user )?decision")
        assert_clause_contains(
            self, text, r"(?:does not|must not) decide", r"authorization basis"
        )

    def test_filing_ci_skill_names_the_privacy_gate_boundary(self):
        text = normalized_prose(FILING_CI_PACKAGE / "SKILL.md")
        assert_clause_contains(self, text, r"privacy_gate")
        assert_clause_contains(
            self, text, r"(?:does not|must not) decide", r"authorization basis"
        )

    def test_machine_contract_declares_the_privacy_checks_and_excluded_judgment(self):
        contract = json.loads(STRUCTURE_CONTRACT.read_text(encoding="utf-8"))
        for check in PRIVACY_CHECKS:
            with self.subTest(check=check):
                self.assertIn(check, contract["mechanical_checks"])
                self.assertIn(check, contract["packaged_checker"]["mechanical_checks"])
        self.assertIn(
            "redaction-authorization", contract["excluded_deterministic_judgments"]
        )
        self.assertIn(
            "redaction-authorization",
            contract["packaged_checker"]["excluded_judgments"],
        )
        installed = json.loads(
            (FILING_CI_PACKAGE / "references" / "complaint-checker-contract.json").read_text()
        )
        self.assertEqual(installed, packaged_complaint_contract())


class PrivacyGateCheckerTest(unittest.TestCase):
    def assert_both_checkers(self, document, expected_present, expected_absent=()):
        for name, result in (
            ("complaint-checker", complaint_checker_findings(document)),
            ("filing-ci", filing_ci_findings(document)),
        ):
            with self.subTest(checker=name):
                ids = check_ids(result)
                for check in expected_present:
                    self.assertIn(check, ids)
                for check in expected_absent:
                    self.assertNotIn(check, ids)
                if expected_present:
                    self.assertEqual(result["status"], "failed")

    def test_clear_privacy_gate_adds_no_finding(self):
        document = complaint_document()
        for name, result in (
            ("complaint-checker", complaint_checker_findings(document)),
            ("filing-ci", filing_ci_findings(document)),
        ):
            with self.subTest(checker=name):
                self.assertEqual(result["status"], "passed", result["findings"])

    def test_both_installed_checkers_require_the_privacy_gate(self):
        document = complaint_document()
        document.pop("privacy_gate")
        self.assert_both_checkers(document, {"privacy-gate-presence"})

    def test_privacy_gate_requires_every_rule_5_2_category_once(self):
        document = complaint_document()
        document["privacy_gate"]["protected_identifiers"].pop()
        self.assert_both_checkers(document, {"privacy-gate-structure"})
        document = complaint_document()
        document["privacy_gate"]["protected_identifiers"].append(
            protected_identifier("birth-date")
        )
        self.assert_both_checkers(document, {"privacy-gate-structure"})

    def test_minor_party_full_name_requires_an_authorization_basis(self):
        document = complaint_document()
        document["privacy_gate"]["minor_parties"] = [
            minor_party(name_form="full-name-authorized")
        ]
        self.assert_both_checkers(document, {"privacy-gate-structure"})
        document["privacy_gate"]["minor_parties"] = [
            minor_party(
                name_form="full-name-authorized",
                basis="Court order of 2026-02-01 under Rule 5.2(e).",
            )
        ]
        self.assert_both_checkers(document, set(), PRIVACY_CHECKS)
        document["privacy_gate"]["minor_parties"] = [minor_party(), minor_party()]
        self.assert_both_checkers(document, {"privacy-gate-structure"})

    def test_unredacted_identifier_requires_an_authorization_basis(self):
        document = complaint_document()
        document["privacy_gate"]["protected_identifiers"][2] = protected_identifier(
            "birth-date", status="unredacted-authorized", locations=[1]
        )
        self.assert_both_checkers(document, {"privacy-gate-structure"})
        document["privacy_gate"]["protected_identifiers"][2] = protected_identifier(
            "birth-date",
            status="unredacted-authorized",
            locations=[1],
            authorization_basis="Plaintiff waived protection of his own birth date under Rule 5.2(h).",
        )
        self.assert_both_checkers(document, set(), PRIVACY_CHECKS)

    def test_privacy_locations_must_reference_existing_paragraphs(self):
        document = complaint_document()
        document["privacy_gate"]["protected_identifiers"][0] = protected_identifier(
            "social-security-number", status="redacted", locations=[99]
        )
        self.assert_both_checkers(document, {"privacy-gate-structure"})

    def test_unresolved_privacy_material_is_filing_critical(self):
        document = complaint_document()
        document["privacy_gate"]["status"] = "blocked"
        document["privacy_gate"]["protected_identifiers"][3] = protected_identifier(
            "financial-account-number", status="unresolved"
        )
        self.assert_both_checkers(
            document, {"privacy-filing-critical-status"}, {"privacy-gate-structure"}
        )
        document = complaint_document()
        document["privacy_gate"]["protected_identifiers"][3] = protected_identifier(
            "financial-account-number", status="unresolved"
        )
        self.assert_both_checkers(document, {"privacy-filing-critical-status"})
        document = complaint_document()
        document["privacy_gate"]["status"] = "blocked"
        self.assert_both_checkers(document, {"privacy-filing-critical-status"})

    def test_privacy_checker_reports_structure_only(self):
        result = complaint_checker_findings(complaint_document())
        report = json.loads(result["report_bytes"])
        self.assertIn("redaction-authorization", report["excluded_judgments"])
        for check in PRIVACY_CHECKS:
            self.assertIn(check, report["checks"])


class CapacityAndReliefContractTest(unittest.TestCase):
    def test_complaint_contract_states_the_official_capacity_rule(self):
        text = normalized_prose(COMPLAINT_CONTRACT)
        assert_clause_contains(
            self, text, r"official[- ]capacity", r"claim against the entity"
        )
        self.assertRegex(text, r"kentucky v\. graham")
        assert_clause_contains(
            self,
            text,
            r"(?:do not|must not) plead",
            r"official[- ]capacity count",
            r"duplicates",
            r"municipal count",
        )

    def test_complaint_contract_limits_punitive_damages_by_capacity(self):
        text = normalized_prose(COMPLAINT_CONTRACT)
        assert_clause_contains(
            self, text, r"punitive damages", r"only", r"individual capacity"
        )
        assert_clause_contains(self, text, r"municipality", r"immune from punitive damages")
        self.assertRegex(text, r"city of newport v\. fact concerts")


class CompletionAuditCoverageTest(unittest.TestCase):
    def test_completion_audit_checks_each_new_contract_item(self):
        text = normalized_prose(COMPLETION_AUDIT)
        for pattern in (
            r"criminal[- ]proceeding posture",
            r"accrual event",
            r"necessarily imply",
            r"events preceding the force",
            r"rule 5\.2",
            r"privacy_gate",
            r"official[- ]capacity count.{0,80}duplicat",
            r"punitive damages.{0,80}(?:municipality|official[- ]capacity)",
        ):
            with self.subTest(pattern=pattern):
                self.assertRegex(text, pattern)


if __name__ == "__main__":
    unittest.main()
