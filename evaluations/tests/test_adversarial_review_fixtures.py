import copy
import unittest
from pathlib import Path

from evaluations.deterministic import grade_candidate
from evaluations.fixtures import load_fixture


REPOSITORY = Path(__file__).resolve().parents[2]
FIXTURES = REPOSITORY / "evaluations" / "fixtures"

EXPECTED = {
    "adversarial-history-control-leakage": {
        "regression": "uses-excluded-history-or-control-conclusion",
        "location": "excluded-review-context",
        "unrelated": "With: [insert a supported date]",
    },
    "adversarial-incomplete-correction": {
        "regression": "offers-placeholder-instead-of-copy-ready-correction",
        "location": "placeholder-replacement",
        "unrelated": "Selected option: omit",
    },
    "adversarial-reserved-decision": {
        "regression": "reviewer-selects-omission",
        "location": "reviewer-selected-strategy",
        "unrelated": "The control memo was not supplied.",
    },
}


def finding_pairs(result):
    return {
        (finding["id"], finding.get("location"))
        for finding in result["findings"]
    }


class AdversarialReviewFixtureDiscriminationTest(unittest.TestCase):

    def test_each_permanent_regression_emits_only_its_declared_rule_location(self):
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

    def test_unrelated_candidates_do_not_emit_the_behavior_rule_location(self):
        for fixture_id, expected in EXPECTED.items():
            with self.subTest(fixture=fixture_id):
                fixture = load_fixture(FIXTURES / fixture_id)
                fixture_with_unrelated_rule = copy.deepcopy(fixture)
                fixture_with_unrelated_rule["deterministic"][
                    "banned_patterns"
                ].append(
                    {
                        "id": "unrelated-rule",
                        "pattern": "UNRELATED FIXTURE RULE",
                    }
                )
                candidate = (
                    f"{fixture['passing_candidate']}\n"
                    f"{expected['unrelated']}\n"
                    "UNRELATED FIXTURE RULE\n"
                )

                result = grade_candidate(fixture_with_unrelated_rule, candidate)

                self.assertIn(
                    ("banned-pattern", "unrelated-rule"),
                    finding_pairs(result),
                )
                self.assertNotIn(
                    ("banned-pattern", expected["location"]),
                    finding_pairs(result),
                )


if __name__ == "__main__":
    unittest.main()
