import copy
import unittest
from pathlib import Path

from evaluations.deterministic import grade_candidate
from evaluations.fixtures import load_fixture


REPOSITORY = Path(__file__).resolve().parents[2]
FIXTURES = REPOSITORY / "evaluations" / "fixtures"

EXPECTED = {
    "declaration-attributed-record-laundering": {
        "regressions": {
            "recasts-recorded-event-as-firsthand-knowledge": (
                "attributed-event-laundered-as-firsthand"
            ),
        },
    },
    "declaration-derived-analysis-retained": {
        "regressions": {
            "retains-derived-analysis-in-declaration": (
                "derived-analysis-retained-in-declaration"
            ),
        },
    },
    "declaration-discovery-expectation-as-knowledge": {
        "regressions": {
            "states-expected-discovery-as-personal-knowledge": (
                "expected-discovery-stated-as-known"
            ),
        },
    },
    "declaration-premature-execution": {
        "regressions": {
            "claims-execution-readiness-while-statement-pending": (
                "execution-ready-while-pending"
            ),
            "selects-domestic-form-from-texas-status": (
                "domestic-form-selected-from-residence-venue-custody"
            ),
            "retains-approval-after-statement-text-changes": (
                "changed-statement-keeps-stale-approval"
            ),
        },
    },
    "declaration-unsupported-exhibit-foundation": {
        "regressions": {
            "invents-exhibit-authentication-foundation": (
                "unsupported-exhibit-authentication"
            ),
        },
    },
}

TARGET_SKILL = "drafting-section-1983-declarations-and-evidence"


def finding_pairs(result):
    return {
        (finding["id"], finding.get("location"))
        for finding in result["findings"]
    }


class DeclarationEvidenceFixtureDiscriminationTest(unittest.TestCase):

    def test_named_fixtures_target_the_exact_public_skill(self):
        for fixture_id in EXPECTED:
            with self.subTest(fixture=fixture_id):
                fixture = load_fixture(FIXTURES / fixture_id)

                self.assertEqual(fixture["id"], fixture_id)
                self.assertEqual(fixture["target_skill"], TARGET_SKILL)

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
                regressions = {
                    regression["id"]: regression
                    for regression in fixture["regressions"]
                }
                self.assertEqual(set(regressions), set(expected["regressions"]))

                for regression_id, location in expected["regressions"].items():
                    with self.subTest(regression=regression_id):
                        regression = regressions[regression_id]
                        self.assertEqual(
                            regression["expected_findings"], ["banned-pattern"]
                        )

                        result = grade_candidate(fixture, regression["candidate"])

                        self.assertEqual(
                            finding_pairs(result),
                            {("banned-pattern", location)},
                        )

    def test_unrelated_rule_fires_without_the_behavior_rule_location(self):
        for fixture_id, expected in EXPECTED.items():
            with self.subTest(fixture=fixture_id):
                fixture = load_fixture(FIXTURES / fixture_id)
                mutated = copy.deepcopy(fixture)
                mutated["deterministic"]["banned_patterns"].append(
                    {
                        "id": "unrelated-rule",
                        "pattern": "UNRELATED DECLARATION FIXTURE RULE",
                    }
                )
                candidate = (
                    f"{fixture['passing_candidate']}\n"
                    "UNRELATED DECLARATION FIXTURE RULE\n"
                )

                result = grade_candidate(mutated, candidate)
                observed = finding_pairs(result)

                self.assertEqual(observed, {("banned-pattern", "unrelated-rule")})
                for location in expected["regressions"].values():
                    self.assertNotIn(("banned-pattern", location), observed)


if __name__ == "__main__":
    unittest.main()
