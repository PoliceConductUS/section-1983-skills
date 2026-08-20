import copy
import json
import unittest

from evaluations.deterministic import grade_candidate


def fixture_with_contract(**contract_changes):
    contract = {
        "required_fields": [],
        "ordered_headings": [],
        "banned_terms": [],
        "banned_patterns": [],
        "required_citations": [],
    }
    contract.update(contract_changes)
    return {
        "id": "deterministic-fixture",
        "source_ids": ["SRC-1", "SRC-2"],
        "deterministic": contract,
    }


def finding_pairs(result):
    return {(finding["id"], finding.get("location")) for finding in result["findings"]}


class DeterministicGraderTest(unittest.TestCase):

    def test_reports_missing_dot_addressed_json_contract_field(self):
        fixture = fixture_with_contract(required_fields=["analysis.result"])

        result = grade_candidate(fixture, json.dumps({"analysis": {}}))

        self.assertFalse(result["passed"])
        self.assertIn(
            ("required-field-missing", "analysis.result"), finding_pairs(result)
        )

    def test_accepts_present_dot_addressed_json_contract_field(self):
        fixture = fixture_with_contract(required_fields=["analysis.result"])

        result = grade_candidate(
            fixture, json.dumps({"analysis": {"result": "supported"}})
        )

        self.assertTrue(result["passed"])
        self.assertEqual(result["findings"], [])

    def test_reports_missing_and_out_of_order_markdown_headings(self):
        fixture = fixture_with_contract(
            ordered_headings=["Facts", "Analysis", "Result"]
        )

        missing = grade_candidate(fixture, "# Facts\n\n# Result\n")
        out_of_order = grade_candidate(
            fixture, "# Analysis\n\n# Facts\n\n# Result\n"
        )

        self.assertIn(("heading-missing", "Analysis"), finding_pairs(missing))
        self.assertIn(
            ("heading-out-of-order", "Analysis"), finding_pairs(out_of_order)
        )

    def test_accepts_complete_markdown_headings_in_required_order(self):
        fixture = fixture_with_contract(
            ordered_headings=["Facts", "Analysis", "Result"]
        )

        result = grade_candidate(
            fixture, "# Facts\n\n# Analysis\n\n# Result\n"
        )

        self.assertTrue(result["passed"])
        self.assertEqual(result["findings"], [])

    def test_reports_configured_banned_term_and_regular_expression(self):
        fixture = fixture_with_contract(
            banned_terms=[{"id": "merely", "term": "merely"}],
            banned_patterns=[
                {
                    "id": "invented-command",
                    "pattern": r"(?i)ran the configured .* checker",
                }
            ],
        )

        result = grade_candidate(
            fixture, "The agent merely ran the configured secret checker."
        )

        self.assertIn(("banned-term", "merely"), finding_pairs(result))
        self.assertIn(
            ("banned-pattern", "invented-command"), finding_pairs(result)
        )

    def test_accepts_text_that_matches_no_banned_term_or_pattern(self):
        fixture = fixture_with_contract(
            banned_terms=[{"id": "merely", "term": "merely"}],
            banned_patterns=[
                {
                    "id": "invented-command",
                    "pattern": r"(?i)ran the configured .* checker",
                }
            ],
        )

        result = grade_candidate(fixture, "The configured checker was unavailable.")

        self.assertTrue(result["passed"])
        self.assertEqual(result["findings"], [])

    def test_reports_missing_required_and_unknown_citation_identifiers(self):
        fixture = fixture_with_contract(required_citations=["SRC-1", "SRC-2"])

        result = grade_candidate(fixture, "The report cites [SRC-1] and [SRC-404].")

        self.assertIn(("citation-missing", "SRC-2"), finding_pairs(result))
        self.assertIn(("citation-unknown", "SRC-404"), finding_pairs(result))

    def test_accepts_required_citations_from_bounded_source_manifest(self):
        fixture = fixture_with_contract(required_citations=["SRC-1", "SRC-2"])

        result = grade_candidate(
            fixture, "The report cites [SRC-1] and [SRC-2]."
        )

        self.assertTrue(result["passed"])
        self.assertEqual(result["findings"], [])

    def test_returns_every_applicable_finding_with_stable_counts(self):
        fixture = fixture_with_contract(
            ordered_headings=["Result"],
            banned_terms=[{"id": "merely", "term": "merely"}],
            required_citations=["SRC-1"],
        )

        result = grade_candidate(fixture, "merely [SRC-404]")

        self.assertEqual(result["fixture_id"], "deterministic-fixture")
        self.assertEqual(result["finding_count"], 4)
        self.assertEqual(
            {finding["id"] for finding in result["findings"]},
            {
                "heading-missing",
                "banned-term",
                "citation-missing",
                "citation-unknown",
            },
        )

    def test_does_not_modify_mutable_candidate_output(self):
        fixture = fixture_with_contract(required_fields=["analysis.result"])
        candidate = {"analysis": {"result": "pass", "citations": ["SRC-1"]}}
        original = copy.deepcopy(candidate)

        grade_candidate(fixture, candidate)

        self.assertEqual(candidate, original)


if __name__ == "__main__":
    unittest.main()
