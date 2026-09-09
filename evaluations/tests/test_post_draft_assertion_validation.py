import shutil
import tempfile
import unittest
from pathlib import Path

from evaluations.deterministic import grade_candidate
from evaluations.fixtures import load_fixture
from scripts.validate_governance import validate_assertion_validation_owner


REPOSITORY = Path(__file__).resolve().parents[2]
SKILLS = REPOSITORY / "skills"
OWNER = SKILLS / "validating-court-facing-assertions"
OWNER_SKILL = OWNER / "SKILL.md"
OWNER_CONTRACT = OWNER / "references" / "assertion-validation-contract.md"
FIXTURE = REPOSITORY / "evaluations" / "fixtures" / "post-draft-assertion-validation"

CONSUMERS = {
    "section-1983-drafting": "orchestrates",
    "drafting-section-1983-complaints": "complete complaint candidate",
    "drafting-section-1983-rule-59e": "complete rule 59(e) candidate",
    "drafting-section-1983-monell-claims": "integrated",
    "audit-authorities": "authority-specific findings",
    "adversarial-filing-review": "downstream",
    "filing-ci": "deterministic",
}

REQUIRED_ASSERTION_FIELDS = (
    "assertion id",
    "exact text",
    "location",
    "classification",
    "documentation route",
    "original supporting passage or recording observation",
    "pinpoint",
    "contrary context",
    "inference reasoning",
    "result",
    "corrective action",
)

REQUIRED_STATUSES = (
    "supported assertion",
    "supported inference",
    "contradiction",
    "overstatement",
    "insufficient source",
    "missing documentation link",
    "unchecked assertion",
    "omission",
    "unresolved factual question",
)


class PostDraftAssertionValidationContractTests(unittest.TestCase):
    def test_shared_owner_is_independently_installable_and_folder_scoped(self):
        skill = OWNER_SKILL.read_text(encoding="utf-8").casefold()
        folder_contract = (
            OWNER / "references" / "folder-contract.json"
        ).read_text(encoding="utf-8").casefold()

        self.assertIn("assertion-validation-contract.md", skill)
        self.assertIn("assertion validation contract unavailable", skill)
        self.assertIn("one required target", skill)
        self.assertIn("<output-folder>/temp/", skill)
        self.assertIn('"internet": "disabled"', folder_contract)
        for role in ("filing", "record", "authorities", "strategy"):
            self.assertIn(f'"{role}"', folder_contract)

    def test_owner_contract_defines_complete_report_and_substantive_checks(self):
        contract = OWNER_CONTRACT.read_text(encoding="utf-8").casefold()

        for field in REQUIRED_ASSERTION_FIELDS:
            self.assertIn(field, contract)
        for status in REQUIRED_STATUSES:
            self.assertIn(status, contract)
        for dimension in (
            "actor",
            "conduct",
            "timing",
            "duration",
            "attribution",
            "knowledge",
            "causation",
            "quotation accuracy",
            "degree of certainty",
        ):
            self.assertIn(dimension, contract)
        for marker in (
            "unchanged and inherited text",
            "compound sentence",
            "original sources",
            "applicable control versions",
            "mermaid",
            "rendered-file review",
            "pleading support is not trial proof",
        ):
            self.assertIn(marker, contract)

    def test_freshness_omissions_and_stopping_rules_are_explicit(self):
        contract = OWNER_CONTRACT.read_text(encoding="utf-8").casefold()

        for dependency in (
            "assertion text",
            "source hash",
            "controlling decision",
            "reasoning premise",
        ):
            self.assertIn(dependency, contract)
        for requirement in (
            "approved claim",
            "material source fact",
            "principal correction",
            "authorized unknown",
            "no unchecked assertions",
            "no unresolved drafting defects",
            "no unauthorized omissions",
        ):
            self.assertIn(requirement, contract)
        self.assertIn("missing documentation link", contract)
        self.assertIn("insufficient source", contract)
        self.assertRegex(
            contract,
            r"(?:do not|must not).{0,120}silently (?:drop|dropping).{0,80}(?:claim|theory)",
        )

    def test_specialist_authority_and_persistence_boundaries_are_explicit(self):
        text = "\n".join(
            (
                OWNER_SKILL.read_text(encoding="utf-8"),
                OWNER_CONTRACT.read_text(encoding="utf-8"),
            )
        ).casefold()

        for marker in (
            "actual holding",
            "controlling status",
            "relevant later treatment",
            "factual fit",
            "pre-event clearly established law",
            "defendant knowledge",
            "municipal notice",
            "rule 15(c) notice",
            "stable private current report",
            "trusted case controller",
            "append-immutable receipt",
        ):
            self.assertIn(marker, text)
        self.assertRegex(text, r"(?:does not|must not).{0,100}(?:depend on|require) casegraph")

    def test_every_consumer_references_owner_without_restating_report_schema(self):
        for name, responsibility in CONSUMERS.items():
            with self.subTest(skill=name):
                text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8").casefold()
                self.assertIn("validating-court-facing-assertions", text)
                self.assertIn(responsibility, text)
                self.assertNotIn("assertion-validation-contract.md", text)

    def test_governance_fails_when_owner_or_consumer_reference_is_missing(self):
        self.assertEqual(validate_assertion_validation_owner(REPOSITORY), [])

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(SKILLS, root / "skills")
            shutil.rmtree(root / "skills" / "validating-court-facing-assertions")
            self.assertEqual(
                validate_assertion_validation_owner(root),
                ["assertion-validation-owner-missing"],
            )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(SKILLS, root / "skills")
            consumer = root / "skills" / "filing-ci" / "SKILL.md"
            consumer.write_text(
                consumer.read_text(encoding="utf-8").replace(
                    "validating-court-facing-assertions", "shared-validator"
                ),
                encoding="utf-8",
            )
            self.assertIn(
                "assertion-validation-owner-reference-missing: filing-ci",
                validate_assertion_validation_owner(root),
            )

    def test_deterministic_boundaries_do_not_claim_semantic_judgment(self):
        filing_ci = " ".join(
            (SKILLS / "filing-ci" / "SKILL.md")
            .read_text(encoding="utf-8")
            .casefold()
            .split()
        )
        owner = " ".join(OWNER_SKILL.read_text(encoding="utf-8").casefold().split())

        for text in (filing_ci, owner):
            self.assertRegex(
                text,
                r"deterministic.{0,180}(?:does not|cannot|must not).{0,100}evidentiary support",
            )
            self.assertRegex(
                text,
                r"deterministic.{0,180}(?:does not|cannot|must not).{0,100}legal sufficiency",
            )

    def test_seven_behavioral_regressions_are_permanent_and_discriminating(self):
        fixture = load_fixture(FIXTURE)
        self.assertEqual(fixture["target_skill"], "validating-court-facing-assertions")
        self.assertTrue(grade_candidate(fixture, fixture["passing_candidate"])["passed"])
        self.assertEqual(len(fixture["regressions"]), 7)

        for regression in fixture["regressions"]:
            with self.subTest(regression=regression["id"]):
                result = grade_candidate(fixture, regression["candidate"])
                observed = {finding["location"] for finding in result["findings"]}
                self.assertTrue(set(regression["expected_findings"]).issubset(observed))


if __name__ == "__main__":
    unittest.main()
