import copy
import unittest
from pathlib import Path

from evaluations.deterministic import grade_candidate
from evaluations.fixtures import load_fixture


REPOSITORY = Path(__file__).resolve().parents[2]
FIXTURES = REPOSITORY / "evaluations" / "fixtures"

EXPECTED = {
    "deposition-outline-invented-answer": {
        "target_skill": "drafting-section-1983-deposition-outlines",
        "regression": "invents-expected-deponent-answer",
        "location": "invented-expected-answer",
    },
    "discovery-response-boilerplate-status": {
        "target_skill": "auditing-section-1983-discovery-responses",
        "regression": "accepts-boilerplate-without-production-status",
        "location": "accepted-boilerplate-without-status",
    },
    "meet-and-confer-selected-narrowing": {
        "target_skill": "drafting-section-1983-meet-and-confer",
        "regression": "silently-narrows-served-request",
        "location": "silent-request-narrowing",
    },
    "privilege-log-automatic-waiver": {
        "target_skill": "auditing-section-1983-privilege-logs",
        "regression": "declares-automatic-waiver",
        "location": "automatic-privilege-waiver",
    },
    "written-discovery-assumed-content": {
        "target_skill": "drafting-section-1983-written-discovery",
        "regression": "states-unverified-recording-content-as-fact",
        "location": "assumed-unverified-recording-content",
    },
}


def finding_pairs(result):
    return {
        (finding["id"], finding.get("location"))
        for finding in result["findings"]
    }


class DiscoverySkillFixtureDiscriminationTest(unittest.TestCase):

    def test_named_fixtures_target_their_exact_public_skills(self):
        for fixture_id, expected in EXPECTED.items():
            with self.subTest(fixture=fixture_id):
                fixture = load_fixture(FIXTURES / fixture_id)

                self.assertEqual(fixture["id"], fixture_id)
                self.assertEqual(fixture["target_skill"], expected["target_skill"])

    def test_each_passing_candidate_is_deterministically_clean(self):
        for fixture_id in EXPECTED:
            with self.subTest(fixture=fixture_id):
                fixture = load_fixture(FIXTURES / fixture_id)

                result = grade_candidate(fixture, fixture["passing_candidate"])

                self.assertTrue(result["passed"])
                self.assertEqual(result["findings"], [])

    def test_each_regression_emits_only_its_exact_behavior_finding(self):
        for fixture_id, expected in EXPECTED.items():
            with self.subTest(fixture=fixture_id):
                fixture = load_fixture(FIXTURES / fixture_id)
                self.assertEqual(len(fixture["regressions"]), 1)
                regression = fixture["regressions"][0]
                self.assertEqual(regression["id"], expected["regression"])
                self.assertEqual(regression["expected_findings"], ["banned-pattern"])

                result = grade_candidate(fixture, regression["candidate"])

                self.assertEqual(
                    finding_pairs(result),
                    {("banned-pattern", expected["location"])},
                )

    def test_unrelated_rule_fires_without_the_behavior_rule_location(self):
        for fixture_id, expected in EXPECTED.items():
            with self.subTest(fixture=fixture_id):
                fixture = load_fixture(FIXTURES / fixture_id)
                mutated = copy.deepcopy(fixture)
                mutated["deterministic"]["banned_patterns"].append(
                    {
                        "id": "unrelated-rule",
                        "pattern": "UNRELATED DISCOVERY FIXTURE RULE",
                    }
                )
                candidate = (
                    f"{fixture['passing_candidate']}\n"
                    "UNRELATED DISCOVERY FIXTURE RULE\n"
                )

                result = grade_candidate(mutated, candidate)
                observed = finding_pairs(result)

                self.assertEqual(observed, {("banned-pattern", "unrelated-rule")})
                self.assertNotIn(
                    ("banned-pattern", expected["location"]),
                    observed,
                )


if __name__ == "__main__":
    unittest.main()
