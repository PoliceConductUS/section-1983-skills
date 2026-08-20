import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPOSITORY / "skills" / "studying-rule-59e-decisions"
DECISION_SCHEMA = SKILL_ROOT / "references" / "decision-corpus.schema.json"
TRANSFER_SCHEMA = SKILL_ROOT / "references" / "transfer-card.schema.json"
FIXTURE_DIRECTORY = SKILL_ROOT / "references" / "fixtures"
VALIDATOR = SKILL_ROOT / "scripts" / "validate_corpus.py"

FIXTURE_OUTCOMES = {
    "valid-complete.json": (0, None),
    "valid-incomplete-example.json": (0, None),
    "invalid-incomplete-tendency.json": (1, "incomplete-tendency"),
    "invalid-authorship-stage.json": (1, "authorship-stage-inconsistent"),
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_local_reference(schema, value):
    while isinstance(value, dict) and "$ref" in value:
        reference = value["$ref"]
        if not reference.startswith("#/"):
            raise AssertionError(f"expected a local schema reference, got {reference}")
        target = schema
        for part in reference.removeprefix("#/").split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
        value = target
    return value


def schema_property_enums(contract):
    return {
        name: tuple(value["enum"])
        for name, value in contract["properties"].items()
        if isinstance(value, dict) and isinstance(value.get("enum"), list)
    }


def run_validator(path):
    return subprocess.run(
        ["python3", str(VALIDATOR), str(path)],
        cwd=REPOSITORY,
        text=True,
        capture_output=True,
        check=False,
    )


def validator_output(completed):
    return f"{completed.stdout}{completed.stderr}"


def validator_lines(completed):
    return [line for line in validator_output(completed).splitlines() if line.strip()]


def schema_allows_null(contract):
    if not isinstance(contract, dict):
        return False
    value_type = contract.get("type")
    if value_type == "null" or (isinstance(value_type, list) and "null" in value_type):
        return True
    return any(
        any(schema_allows_null(option) for option in contract.get(keyword, []))
        for keyword in ("anyOf", "oneOf")
    )


def candidate_only_ids(corpus):
    return {
        gap["candidate_id"]
        for gap in corpus["retrieval_gaps"]
        if gap["status"] == "unresolved-candidate" and gap["record_id"] is None
    }


def write_json(directory, name, corpus):
    path = Path(directory) / name
    path.write_text(json.dumps(corpus), encoding="utf-8")
    return path


class Rule59CorpusContractTest(unittest.TestCase):

    def assert_invalid(self, path, finding):
        completed = run_validator(path)
        output = validator_output(completed)
        self.assertNotEqual(completed.returncode, 0, output)
        self.assertIn(finding, output)
        self.assertNotIn("Traceback", output)

    def fixture(self, name):
        return load_json(FIXTURE_DIRECTORY / name)

    def test_decision_schema_requires_canonical_public_components(self):
        schema = load_json(DECISION_SCHEMA)

        self.assertEqual(
            schema["$schema"], "https://json-schema.org/draft/2020-12/schema"
        )
        self.assertTrue(
            {
                "schema_version",
                "study",
                "denominator",
                "decision_records",
                "retrieval_gaps",
                "transfer_cards",
            }.issubset(schema["required"])
        )

    def test_decision_schema_exposes_required_stage_and_record_fields(self):
        schema = load_json(DECISION_SCHEMA)
        decision_records = resolve_local_reference(
            schema, schema["properties"]["decision_records"]
        )
        decision_record = resolve_local_reference(schema, decision_records["items"])

        self.assertTrue(
            {
                "court",
                "assigned_judge",
                "reasoning_author",
                "recommendation_author",
                "adopting_judge",
                "decision_type",
                "posture",
                "ground_children",
                "requested_relief",
                "proposed_material",
                "independent_reasoning",
                "disposition",
                "sources",
                "missing_documents",
                "appellate_history",
            }.issubset(decision_record["required"])
        )
        self.assertTrue(
            {
                "recommendation",
                "adoption-only-order",
                "independently-reasoned-final-decision",
                "consent-final-decision",
                "outcome-only-order",
            }.issubset(
                decision_record["properties"]["decision_type"]["enum"]
            )
        )

    def test_decision_schema_requires_controlled_retrieval_and_reason_fields(self):
        schema = load_json(DECISION_SCHEMA)
        decision_records = resolve_local_reference(
            schema, schema["properties"]["decision_records"]
        )
        decision_record = resolve_local_reference(schema, decision_records["items"])
        disposition = resolve_local_reference(
            schema, decision_record["properties"]["disposition"]
        )
        stated_reasons = resolve_local_reference(
            schema, disposition["properties"]["stated_reasons"]
        )
        reason_item = resolve_local_reference(schema, stated_reasons["items"])

        self.assertTrue(
            {"retrieval_status", "coding_confidence"}.issubset(
                decision_record["required"]
            )
        )
        self.assertTrue(
            {"complete-pair", "ruling-complete", "index-only", "lead-only"}.issubset(
                decision_record["properties"]["retrieval_status"]["enum"]
            )
        )
        self.assertTrue(
            {"high", "medium", "low"}.issubset(
                decision_record["properties"]["coding_confidence"]["enum"]
            )
        )
        self.assertTrue(
            {
                "manifest-error-not-shown",
                "new-evidence-not-shown",
                "intervening-law-not-shown",
                "rehash-or-available-before-judgment",
                "vehicle-or-timing-defect",
                "rule15-factors",
                "futility",
                "delay-bad-faith-or-prejudice",
                "prior-failure-to-cure",
                "record-or-inference-error",
                "correction-does-not-change-result",
                "other-stated-reason",
            }.issubset(reason_item["enum"])
        )

    def test_complete_fixture_uses_controlled_retrieval_and_confidence_values(self):
        corpus = self.fixture("valid-complete.json")

        for record in corpus["decision_records"]:
            with self.subTest(record=record["record_id"]):
                self.assertIn(
                    record["retrieval_status"],
                    {"complete-pair", "ruling-complete", "index-only", "lead-only"},
                )
                self.assertIn(record["coding_confidence"], {"high", "medium", "low"})

        completed = run_validator(FIXTURE_DIRECTORY / "valid-complete.json")
        self.assertEqual(completed.returncode, 0, validator_output(completed))

    def test_transfer_card_schema_requires_neutral_evidence_and_source_limits(self):
        schema = load_json(TRANSFER_SCHEMA)

        self.assertEqual(
            schema["$schema"], "https://json-schema.org/draft/2020-12/schema"
        )
        self.assertTrue(
            {
                "card_id",
                "proposition",
                "universe",
                "numerator",
                "denominator",
                "date_range",
                "source_row_ids",
                "evidence_level",
                "missingness",
                "disconfirming_row_ids",
                "permitted_use",
                "prohibited_inference",
                "checked_through",
                "actual_source_identity",
                "source_checked_date",
                "metric_type",
            }.issubset(schema["required"])
        )
        self.assertTrue(
            {"example", "documented-cluster", "tendency"}.issubset(
                schema["properties"]["evidence_level"]["enum"]
            )
        )
        self.assertIn("success-rate", schema["properties"]["metric_type"]["enum"])
        self.assertTrue(schema["properties"]["source_row_ids"]["uniqueItems"])
        self.assertTrue(schema["properties"]["disconfirming_row_ids"]["uniqueItems"])

    def test_embedded_transfer_cards_match_the_standalone_contract(self):
        decision_schema = load_json(DECISION_SCHEMA)
        transfer_schema = load_json(TRANSFER_SCHEMA)
        transfer_cards = resolve_local_reference(
            decision_schema,
            decision_schema["properties"]["transfer_cards"],
        )
        embedded_card = resolve_local_reference(
            decision_schema, transfer_cards["items"]
        )

        self.assertEqual(
            set(embedded_card["properties"]), set(transfer_schema["properties"])
        )
        self.assertEqual(
            embedded_card["required"], transfer_schema["required"]
        )
        self.assertEqual(
            schema_property_enums(embedded_card),
            schema_property_enums(transfer_schema),
        )

    def test_checked_in_fixtures_have_declared_cli_outcomes(self):
        for name, (expected_returncode, finding) in FIXTURE_OUTCOMES.items():
            with self.subTest(fixture=name):
                path = FIXTURE_DIRECTORY / name
                self.assertTrue(path.is_file())
                completed = run_validator(path)
                self.assertEqual(
                    completed.returncode,
                    expected_returncode,
                    validator_output(completed),
                )
                expected_lines = ["corpus validation passed"]
                if finding is not None:
                    expected_lines = [finding]
                self.assertEqual(validator_lines(completed), expected_lines)

    def test_checked_in_fixtures_are_generic_synthetic_material(self):
        for name in FIXTURE_OUTCOMES:
            with self.subTest(fixture=name):
                serialized = json.dumps(self.fixture(name))
                self.assertIn("Example District", serialized)
                self.assertNotIn("/Users/", serialized)
                self.assertNotIn("/private/", serialized)
                self.assertNotIn("PoliceConductUS", serialized)
                self.assertNotIn("3-25-CV-", serialized)

    def test_complete_fixture_preserves_three_distinct_judicial_stages(self):
        corpus = self.fixture("valid-complete.json")
        decision_types = {
            record["decision_type"] for record in corpus["decision_records"]
        }

        self.assertTrue(
            {
                "recommendation",
                "adoption-only-order",
                "independently-reasoned-final-decision",
            }.issubset(decision_types)
        )

    def test_incomplete_fixture_limits_transfer_to_bounded_evidence(self):
        corpus = self.fixture("valid-incomplete-example.json")
        evidence_levels = {
            card["evidence_level"] for card in corpus["transfer_cards"]
        }
        denominator = corpus["denominator"]

        self.assertTrue(evidence_levels.issubset({"example", "documented-cluster"}))
        self.assertEqual(denominator["completeness_status"], "incomplete")
        self.assertTrue(denominator["limits"])

    def test_incomplete_fixture_candidate_count_matches_its_inventory(self):
        corpus = self.fixture("valid-incomplete-example.json")
        denominator = corpus["denominator"]

        self.assertEqual(
            denominator["candidate_count"],
            denominator["coded_pair_count"] + len(candidate_only_ids(corpus)),
        )

    def test_corrected_candidate_inventory_is_a_valid_bounded_example(self):
        corpus = self.fixture("valid-incomplete-example.json")
        denominator = corpus["denominator"]
        denominator["candidate_count"] = denominator["coded_pair_count"] + len(
            candidate_only_ids(corpus)
        )

        with tempfile.TemporaryDirectory() as directory:
            path = write_json(directory, "corrected-candidate-inventory.json", corpus)
            completed = run_validator(path)
            self.assertEqual(completed.returncode, 0, validator_output(completed))

    def test_inconsistent_candidate_inventory_has_stable_finding(self):
        corpus = self.fixture("valid-incomplete-example.json")
        denominator = corpus["denominator"]
        denominator["candidate_count"] = (
            denominator["coded_pair_count"] + len(candidate_only_ids(corpus)) + 1
        )

        with tempfile.TemporaryDirectory() as directory:
            path = write_json(directory, "inconsistent-candidate-inventory.json", corpus)
            self.assert_invalid(path, "candidate-inventory-inconsistent")

    def test_malformed_json_and_types_fail_cleanly(self):
        with tempfile.TemporaryDirectory() as directory:
            malformed = Path(directory) / "malformed.json"
            malformed.write_text("{", encoding="utf-8")
            wrong_top_level_type = Path(directory) / "wrong-top-level-type.json"
            wrong_top_level_type.write_text("[]", encoding="utf-8")
            wrong_field_type = self.fixture("valid-complete.json")
            wrong_field_type["decision_records"] = "not-a-list"
            wrong_field_type_path = write_json(
                directory, "wrong-field-type.json", wrong_field_type
            )

            for path in (malformed, wrong_top_level_type, wrong_field_type_path):
                with self.subTest(path=path.name):
                    self.assert_invalid(path, "malformed-input")

    def test_missing_canonical_component_has_stable_finding(self):
        corpus = self.fixture("valid-complete.json")
        corpus.pop("denominator")

        with tempfile.TemporaryDirectory() as directory:
            path = write_json(directory, "missing-denominator.json", corpus)
            self.assert_invalid(path, "missing-required-field: denominator")

    def test_duplicate_decision_gap_and_card_identifiers_fail(self):
        cases = []

        duplicate_decision = self.fixture("valid-complete.json")
        duplicate_decision["decision_records"].append(
            dict(duplicate_decision["decision_records"][0])
        )
        cases.append(("duplicate-decision.json", duplicate_decision, "duplicate-decision-id"))

        duplicate_gap = self.fixture("valid-incomplete-example.json")
        duplicate_gap["retrieval_gaps"].append(
            dict(duplicate_gap["retrieval_gaps"][0])
        )
        cases.append(("duplicate-gap.json", duplicate_gap, "duplicate-gap-id"))

        duplicate_card = self.fixture("valid-complete.json")
        duplicate_card["transfer_cards"].append(
            dict(duplicate_card["transfer_cards"][0])
        )
        cases.append(("duplicate-card.json", duplicate_card, "duplicate-card-id"))

        with tempfile.TemporaryDirectory() as directory:
            for name, corpus, finding in cases:
                with self.subTest(path=name):
                    self.assert_invalid(write_json(directory, name, corpus), finding)

    def test_broken_transfer_source_row_reference_has_stable_finding(self):
        corpus = self.fixture("valid-complete.json")
        corpus["transfer_cards"][0]["source_row_ids"] = ["DECISION-404"]

        with tempfile.TemporaryDirectory() as directory:
            path = write_json(directory, "broken-source-row.json", corpus)
            self.assert_invalid(path, "source-row-reference-invalid")

    def test_example_card_rejects_unverified_source_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            for retrieval_status in ("lead-only", "index-only"):
                with self.subTest(retrieval_status=retrieval_status):
                    corpus = self.fixture("valid-complete.json")
                    card = corpus["transfer_cards"][0]
                    card["evidence_level"] = "example"
                    source_record = next(
                        record
                        for record in corpus["decision_records"]
                        if record["record_id"] == card["source_row_ids"][0]
                    )
                    source_record["retrieval_status"] = retrieval_status
                    path = write_json(
                        directory,
                        f"example-{retrieval_status}-source.json",
                        corpus,
                    )
                    self.assert_invalid(path, "unverified-card-source")

    def test_unverified_coded_record_blocks_tendency_even_when_not_a_card_source(self):
        with tempfile.TemporaryDirectory() as directory:
            for retrieval_status in ("lead-only", "index-only"):
                with self.subTest(retrieval_status=retrieval_status):
                    corpus = self.fixture("valid-complete.json")
                    card_sources = set(corpus["transfer_cards"][0]["source_row_ids"])
                    non_source_record = next(
                        record
                        for record in corpus["decision_records"]
                        if record["record_id"] not in card_sources
                    )
                    non_source_record["retrieval_status"] = retrieval_status
                    path = write_json(
                        directory,
                        f"tendency-with-{retrieval_status}-record.json",
                        corpus,
                    )
                    self.assert_invalid(path, "incomplete-tendency")

    def test_unpublished_stated_reason_has_controlled_value_finding(self):
        corpus = self.fixture("valid-complete.json")
        corpus["decision_records"][0]["disposition"]["stated_reasons"] = [
            "unpublished-reason-code"
        ]

        with tempfile.TemporaryDirectory() as directory:
            path = write_json(directory, "unpublished-stated-reason.json", corpus)
            self.assert_invalid(
                path,
                "controlled-value-invalid: decision_records[0].disposition.stated_reasons[0]",
            )

    def test_related_stages_with_different_motion_ids_have_stable_finding(self):
        corpus = self.fixture("valid-complete.json")
        adoption = next(
            record
            for record in corpus["decision_records"]
            if record["decision_type"] == "adoption-only-order"
        )
        adoption["motion_id"] = "EXAMPLE-MOTION-UNLINKED"
        corpus["denominator"]["candidate_count"] = 3
        corpus["denominator"]["coded_pair_count"] = 3
        corpus["denominator"]["research_question_complete_count"] = 3

        with tempfile.TemporaryDirectory() as directory:
            path = write_json(directory, "related-stage-motion-mismatch.json", corpus)
            self.assert_invalid(path, "related-stage-motion-inconsistent")

    def test_denominator_missingness_must_match_document_and_gap_inventory(self):
        corpus = self.fixture("valid-incomplete-example.json")
        corpus["denominator"]["unresolved_relevant_missingness"] = 1

        with tempfile.TemporaryDirectory() as directory:
            path = write_json(directory, "denominator-missingness-mismatch.json", corpus)
            self.assert_invalid(path, "denominator-missingness-inconsistent")

    def test_missing_document_gap_must_match_the_document_type(self):
        corpus = self.fixture("valid-incomplete-example.json")
        corpus["decision_records"][0]["missing_documents"][0]["document_type"] = "reply"

        with tempfile.TemporaryDirectory() as directory:
            path = write_json(directory, "missing-gap-document-type-mismatch.json", corpus)
            self.assert_invalid(path, "missing-gap-entry")

    def test_duplicate_transfer_card_row_ids_have_stable_finding(self):
        source_rows = self.fixture("valid-complete.json")
        source_id = source_rows["transfer_cards"][0]["source_row_ids"][0]
        source_rows["transfer_cards"][0]["source_row_ids"] = [source_id, source_id]

        disconfirming_rows = self.fixture("valid-complete.json")
        disconfirming_id = disconfirming_rows["decision_records"][0]["record_id"]
        disconfirming_rows["transfer_cards"][0]["disconfirming_row_ids"] = [
            disconfirming_id,
            disconfirming_id,
        ]

        with tempfile.TemporaryDirectory() as directory:
            cases = (
                ("duplicate-source-row.json", source_rows),
                ("duplicate-disconfirming-row.json", disconfirming_rows),
            )
            for name, corpus in cases:
                with self.subTest(path=name):
                    self.assert_invalid(
                        write_json(directory, name, corpus), "duplicate-card-row-id"
                    )

    def test_authorship_stage_contract_rejects_each_invalid_judicial_role(self):
        cases = []

        recommendation_missing_author = self.fixture("valid-complete.json")
        recommendation = next(
            record
            for record in recommendation_missing_author["decision_records"]
            if record["decision_type"] == "recommendation"
        )
        recommendation.pop("recommendation_author")
        cases.append(("recommendation-missing-author.json", recommendation_missing_author))

        recommendation_wrong_author = self.fixture("valid-complete.json")
        recommendation = next(
            record
            for record in recommendation_wrong_author["decision_records"]
            if record["decision_type"] == "recommendation"
        )
        recommendation["recommendation_author"] = recommendation["assigned_judge"]
        cases.append(("recommendation-wrong-author.json", recommendation_wrong_author))

        recommendation_wrong_independence = self.fixture("valid-complete.json")
        recommendation = next(
            record
            for record in recommendation_wrong_independence["decision_records"]
            if record["decision_type"] == "recommendation"
        )
        recommendation["independent_reasoning"] = "independent"
        cases.append(
            ("recommendation-wrong-independence.json", recommendation_wrong_independence)
        )

        adoption_missing_author = self.fixture("valid-complete.json")
        adoption = next(
            record
            for record in adoption_missing_author["decision_records"]
            if record["decision_type"] == "adoption-only-order"
        )
        adoption.pop("adopting_judge")
        cases.append(("adoption-missing-author.json", adoption_missing_author))

        adoption_missing_recommendation_author = self.fixture("valid-complete.json")
        adoption = next(
            record
            for record in adoption_missing_recommendation_author["decision_records"]
            if record["decision_type"] == "adoption-only-order"
        )
        adoption["recommendation_author"] = None
        cases.append(
            (
                "adoption-missing-recommendation-author.json",
                adoption_missing_recommendation_author,
            )
        )

        adoption_attributes_recommendation_reasoning = self.fixture("valid-complete.json")
        adoption = next(
            record
            for record in adoption_attributes_recommendation_reasoning["decision_records"]
            if record["decision_type"] == "adoption-only-order"
        )
        adoption["reasoning_author"] = adoption["adopting_judge"]
        cases.append(
            (
                "adoption-attributes-recommendation-reasoning.json",
                adoption_attributes_recommendation_reasoning,
            )
        )

        adoption_wrong_independence = self.fixture("valid-complete.json")
        adoption = next(
            record
            for record in adoption_wrong_independence["decision_records"]
            if record["decision_type"] == "adoption-only-order"
        )
        adoption["independent_reasoning"] = "independent"
        cases.append(("adoption-wrong-independence.json", adoption_wrong_independence))

        final_missing_author = self.fixture("valid-complete.json")
        final_decision = next(
            record
            for record in final_missing_author["decision_records"]
            if record["decision_type"] == "independently-reasoned-final-decision"
        )
        final_decision.pop("reasoning_author")
        cases.append(("final-missing-author.json", final_missing_author))

        final_wrong_independence = self.fixture("valid-complete.json")
        final_decision = next(
            record
            for record in final_wrong_independence["decision_records"]
            if record["decision_type"] == "independently-reasoned-final-decision"
        )
        final_decision["independent_reasoning"] = "recommendation-only"
        cases.append(("final-wrong-independence.json", final_wrong_independence))

        with tempfile.TemporaryDirectory() as directory:
            for name, corpus in cases:
                with self.subTest(path=name):
                    self.assert_invalid(
                        write_json(directory, name, corpus),
                        "authorship-stage-inconsistent",
                    )

    def test_missing_document_without_matching_gap_has_stable_finding(self):
        corpus = self.fixture("valid-incomplete-example.json")
        record = corpus["decision_records"][0]
        missing_documents = record["missing_documents"]

        self.assertGreaterEqual(len(missing_documents), 2)
        matching_gap_ids = {gap["gap_id"] for gap in corpus["retrieval_gaps"]}
        self.assertTrue(
            {document["gap_id"] for document in missing_documents}.issubset(
                matching_gap_ids
            )
        )
        record["missing_documents"][0]["gap_id"] = "GAP-UNLOGGED"
        self.assertTrue(
            any(
                document["gap_id"] in matching_gap_ids
                for document in record["missing_documents"][1:]
            )
        )

        with tempfile.TemporaryDirectory() as directory:
            path = write_json(directory, "missing-gap-entry.json", corpus)
            self.assert_invalid(path, "missing-gap-entry")

    def test_retrieval_gap_schema_supports_candidate_only_gaps(self):
        schema = load_json(DECISION_SCHEMA)
        retrieval_gaps = resolve_local_reference(
            schema, schema["properties"]["retrieval_gaps"]
        )
        retrieval_gap = resolve_local_reference(schema, retrieval_gaps["items"])
        record_id = resolve_local_reference(
            schema, retrieval_gap["properties"]["record_id"]
        )

        self.assertIn("candidate_id", retrieval_gap["required"])
        self.assertTrue(schema_allows_null(record_id))
        self.assertIn(
            "unresolved-candidate",
            retrieval_gap["properties"]["status"]["enum"],
        )

    def test_candidate_only_gap_validates_without_a_fabricated_decision_record(self):
        corpus = self.fixture("valid-incomplete-example.json")
        denominator = corpus["denominator"]
        denominator["candidate_count"] = denominator["coded_pair_count"] + len(
            candidate_only_ids(corpus)
        )
        denominator["candidate_count"] += 1
        denominator["unresolved_relevant_missingness"] += 1
        denominator["completeness_status"] = "incomplete"
        denominator["limits"].append(
            "One synthetic candidate docket remains unresolved without a decision record"
        )
        corpus["retrieval_gaps"].append(
            {
                "gap_id": "EXAMPLE-CANDIDATE-GAP-003",
                "record_id": None,
                "candidate_id": "EXAMPLE-CANDIDATE-003",
                "document_type": "candidate docket",
                "status": "unresolved-candidate",
                "retrieval_attempts": [
                    "Reviewed the Example District synthetic candidate index"
                ],
                "limit": "No decision record is fabricated for the unresolved candidate",
            }
        )

        with tempfile.TemporaryDirectory() as directory:
            path = write_json(directory, "candidate-only-gap.json", corpus)
            completed = run_validator(path)
            self.assertEqual(completed.returncode, 0, validator_output(completed))

    def test_gap_scope_requires_candidate_and_document_shapes_to_stay_distinct(self):
        ordinary_gap = self.fixture("valid-incomplete-example.json")
        ordinary_gap["retrieval_gaps"][0]["record_id"] = None

        candidate_gap = self.fixture("valid-incomplete-example.json")
        denominator = candidate_gap["denominator"]
        denominator["candidate_count"] = denominator["coded_pair_count"] + len(
            candidate_only_ids(candidate_gap)
        )
        denominator["unresolved_relevant_missingness"] += 1
        denominator["limits"].append(
            "One synthetic candidate docket is included only to test gap scope"
        )
        candidate_gap["retrieval_gaps"].append(
            {
                "gap_id": "EXAMPLE-CANDIDATE-GAP-SCOPE-003",
                "record_id": candidate_gap["decision_records"][0]["record_id"],
                "candidate_id": "EXAMPLE-CANDIDATE-SCOPE-003",
                "document_type": "candidate docket",
                "status": "unresolved-candidate",
                "retrieval_attempts": [
                    "Reviewed the Example District synthetic candidate index"
                ],
                "limit": "The candidate-only gap must not claim a decision record",
            }
        )

        with tempfile.TemporaryDirectory() as directory:
            cases = (
                ("ordinary-gap-without-record.json", ordinary_gap),
                ("candidate-gap-with-record.json", candidate_gap),
            )
            for name, corpus in cases:
                with self.subTest(path=name):
                    self.assert_invalid(
                        write_json(directory, name, corpus), "gap-scope-inconsistent"
                    )

    def test_incomplete_corpus_rejects_tendency_and_success_rate(self):
        tendency = self.fixture("valid-incomplete-example.json")
        tendency["transfer_cards"][0]["evidence_level"] = "tendency"

        success_rate = self.fixture("valid-incomplete-example.json")
        success_rate["transfer_cards"][0]["metric_type"] = "success-rate"

        with tempfile.TemporaryDirectory() as directory:
            tendency_path = write_json(directory, "incomplete-tendency.json", tendency)
            success_rate_path = write_json(
                directory, "incomplete-success-rate.json", success_rate
            )
            self.assert_invalid(tendency_path, "incomplete-tendency")
            self.assert_invalid(success_rate_path, "incomplete-success-rate")

    def test_unresolved_missingness_rejects_strong_cards_despite_complete_status(self):
        tendency = self.fixture("valid-incomplete-example.json")
        tendency["denominator"]["completeness_status"] = "complete"
        tendency["transfer_cards"][0]["evidence_level"] = "tendency"

        success_rate = self.fixture("valid-incomplete-example.json")
        success_rate["denominator"]["completeness_status"] = "complete"
        success_rate["transfer_cards"][0]["metric_type"] = "success-rate"

        for corpus in (tendency, success_rate):
            self.assertTrue(corpus["retrieval_gaps"])
            self.assertTrue(corpus["decision_records"][0]["missing_documents"])

        with tempfile.TemporaryDirectory() as directory:
            tendency_path = write_json(
                directory, "complete-status-unresolved-tendency.json", tendency
            )
            success_rate_path = write_json(
                directory,
                "complete-status-unresolved-success-rate.json",
                success_rate,
            )
            self.assert_invalid(tendency_path, "incomplete-tendency")
            self.assert_invalid(success_rate_path, "incomplete-success-rate")
