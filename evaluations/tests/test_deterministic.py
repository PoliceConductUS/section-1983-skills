import copy
import json
import unittest

from evaluations.deterministic import grade_candidate


def fixture_with_contract(**contract_changes):
    contract = {
        "required_fields": [],
        "required_nonempty_strings": [],
        "required_exact_strings": [],
        "required_object_entries": [],
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

    def test_requires_exact_structured_string_independent_of_key_order(self):
        fixture = fixture_with_contract(
            required_exact_strings=[
                {
                    "id": "pending-decision",
                    "address": "principal_decision.status",
                    "value": "pending",
                }
            ]
        )

        result = grade_candidate(
            fixture,
            {"principal_decision": {"reason": "not yet approved", "status": "approved"}},
        )

        self.assertIn(
            ("required-exact-string", "principal_decision.status"),
            finding_pairs(result),
        )

    def test_requires_nonempty_string_values_at_dot_addresses(self):
        fixture = fixture_with_contract(
            required_nonempty_strings=["analysis.threshold"]
        )

        for invalid in (None, True, 7, "", "   "):
            with self.subTest(invalid=invalid):
                result = grade_candidate(
                    fixture, {"analysis": {"threshold": invalid}}
                )
                self.assertIn(
                    ("required-nonempty-string", "analysis.threshold"),
                    finding_pairs(result),
                )

        self.assertTrue(
            grade_candidate(
                fixture, {"analysis": {"threshold": "source-supported facts"}}
            )["passed"]
        )

    def test_validates_every_member_of_a_required_object_collection(self):
        fixture = fixture_with_contract(
            required_object_entries=[
                {
                    "id": "request-records",
                    "address": "analysis.requests",
                    "key_field": "request_id",
                    "required_nonempty_string_fields": [
                        "request_id",
                        "independent_relevance",
                    ],
                }
            ]
        )
        complete = {
            "analysis": {
                "requests": {
                    "R-001": {
                        "request_id": "R-001",
                        "independent_relevance": "Named live claim and issue.",
                    },
                    "R-002": {
                        "request_id": "R-002",
                        "independent_relevance": "Named live defense and issue.",
                    },
                }
            }
        }

        self.assertTrue(grade_candidate(fixture, complete)["passed"])

        mismatched = copy.deepcopy(complete)
        mismatched["analysis"]["requests"]["R-001"]["request_id"] = "R-999"
        self.assertIn(
            ("required-object-entry-key-mismatch", "analysis.requests.R-001"),
            finding_pairs(grade_candidate(fixture, mismatched)),
        )

        for invalid_entry in (
            {},
            {"request_id": "R-003", "independent_relevance": None},
            {"request_id": "R-003", "independent_relevance": True},
        ):
            with self.subTest(invalid_entry=invalid_entry):
                candidate = copy.deepcopy(complete)
                candidate["analysis"]["requests"]["R-003"] = invalid_entry
                result = grade_candidate(fixture, candidate)
                self.assertIn(
                    (
                        "required-object-entry-invalid",
                        "analysis.requests.R-003",
                    ),
                    finding_pairs(result),
                )

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

        result = grade_candidate(
            fixture, "The report cites [cite:SRC-1] and [cite:SRC-404]."
        )

        self.assertIn(("citation-missing", "SRC-2"), finding_pairs(result))
        self.assertIn(("citation-unknown", "SRC-404"), finding_pairs(result))

    def test_accepts_required_citations_from_bounded_source_manifest(self):
        fixture = fixture_with_contract(required_citations=["SRC-1", "SRC-2"])

        result = grade_candidate(
            fixture, "The report cites [cite:SRC-1] and [cite:SRC-2]."
        )

        self.assertTrue(result["passed"])
        self.assertEqual(result["findings"], [])

    def test_does_not_treat_other_markdown_brackets_as_citation_tokens(self):
        fixture = fixture_with_contract(required_citations=["SRC-1"])
        candidate = """[SRC-1]
[a link](https://example.test/SRC-1)
- [x] reviewed SRC-1
[^SRC-1]
![SRC-1](image.png)
"""

        result = grade_candidate(fixture, candidate)

        self.assertEqual(
            finding_pairs(result),
            {("citation-missing", "SRC-1")},
        )

    def test_returns_every_applicable_finding_with_stable_counts(self):
        fixture = fixture_with_contract(
            ordered_headings=["Result"],
            banned_terms=[{"id": "merely", "term": "merely"}],
            required_citations=["SRC-1"],
        )

        result = grade_candidate(fixture, "merely [cite:SRC-404]")

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
