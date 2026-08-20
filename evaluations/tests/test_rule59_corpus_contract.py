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
                output = validator_output(completed)
                self.assertEqual(completed.returncode, expected_returncode, output)
                if finding is not None:
                    self.assertIn(finding, output)
                    self.assertNotIn("Traceback", output)

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
