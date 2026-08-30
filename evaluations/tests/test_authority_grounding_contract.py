import json
import unittest
from pathlib import Path

from evaluations.deterministic import grade_candidate
from evaluations.fixtures import load_fixture


REPOSITORY = Path(__file__).resolve().parents[2]
AUDIT_SKILL = REPOSITORY / "skills" / "audit-authorities"
SCHEMA = AUDIT_SKILL / "references" / "proposition-audit.schema.json"
FIXTURE_IDS = (
    "authority-grounding-inverted-holding",
    "authority-grounding-party-argument",
    "authority-grounding-lower-court-voice",
    "authority-grounding-superseded-panel",
    "authority-grounding-irrelevant-citation",
    "authority-grounding-split-support",
)


class AuthorityGroundingContractTest(unittest.TestCase):
    def test_machine_record_schema_has_atomic_status_source_and_provenance_fields(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

        self.assertEqual(
            schema["properties"]["propositions"]["items"]["$ref"],
            "#/$defs/proposition",
        )
        proposition = schema["$defs"]["proposition"]
        self.assertTrue(
            {
                "proposition_id",
                "filing_location",
                "text",
                "type",
                "materiality",
                "correctness",
                "groundedness",
                "source_support",
                "verification_provenance",
            }.issubset(proposition["required"])
        )
        self.assertEqual(
            proposition["properties"]["correctness"]["enum"],
            ["verified", "incorrect", "unresolved"],
        )
        self.assertEqual(
            proposition["properties"]["groundedness"]["enum"],
            ["grounded", "misgrounded", "ungrounded", "not-applicable"],
        )
        self.assertEqual(
            proposition["allOf"][0]["then"]["properties"]["groundedness"]["enum"],
            ["grounded", "misgrounded", "ungrounded"],
        )
        self.assertEqual(
            proposition["allOf"][0]["else"]["properties"]["groundedness"]["const"],
            "not-applicable",
        )

        source_support = schema["$defs"]["source_support"]
        self.assertTrue(
            {
                "authority_id",
                "authority_yaml_path",
                "source_yaml_path",
                "artifact_path",
                "artifact_sha256",
                "pinpoint",
                "source_text",
                "scope_and_qualifiers",
                "jurisdiction",
                "decision_date",
                "procedural_posture",
                "precedential_force",
                "source_voice",
                "support_status",
            }.issubset(source_support["required"])
        )
        self.assertEqual(
            source_support["properties"]["source_voice"]["enum"],
            [
                "majority-holding",
                "court-dicta",
                "party-argument",
                "lower-court-ruling-under-review",
                "factual-or-procedural-background",
                "concurrence",
                "dissent",
                "quoted-secondary-authority",
            ],
        )

    def test_audit_and_shared_drafting_protocols_require_proposition_level_review(self):
        audit_text = "\n".join(
            (
                (AUDIT_SKILL / "SKILL.md").read_text(encoding="utf-8"),
                (AUDIT_SKILL / "references/full-audit-workflow.md").read_text(
                    encoding="utf-8"
                ),
                (AUDIT_SKILL / "references/audit-record-schema.md").read_text(
                    encoding="utf-8"
                ),
            )
        ).casefold()
        drafting_text = (
            REPOSITORY
            / "skills/section-1983-drafting/references/authorities.md"
        ).read_text(encoding="utf-8").casefold()

        for required in (
            "atomic proposition",
            "correctness",
            "groundedness",
            "source voice",
            "majority holding",
            "party argument",
            "lower-court ruling under review",
            "quoted secondary authority",
            "working link",
            "positive treatment",
            "proposition-audit.schema.json",
            "no aggregate pass",
        ):
            self.assertIn(required, audit_text)
        for required in (
            "atomic proposition",
            "retrieval lead",
            "exact source",
            "source voice",
            "working link",
            "positive treatment",
        ):
            self.assertIn(required, drafting_text)

    def test_six_required_failure_modes_have_passing_and_permanent_regression_fixtures(self):
        fixture_root = REPOSITORY / "evaluations/fixtures"

        for fixture_id in FIXTURE_IDS:
            with self.subTest(fixture=fixture_id):
                fixture = load_fixture(fixture_root / fixture_id)
                self.assertEqual(fixture["id"], fixture_id)
                self.assertEqual(fixture["target_skill"], "audit-authorities")
                self.assertTrue(grade_candidate(fixture, fixture["passing_candidate"])["passed"])
                self.assertEqual(len(fixture["regressions"]), 1)
                regression = fixture["regressions"][0]
                observed = {
                    finding["id"]
                    for finding in grade_candidate(
                        fixture, regression["candidate"]
                    )["findings"]
                }
                self.assertTrue(set(regression["expected_findings"]).issubset(observed))


if __name__ == "__main__":
    unittest.main()
