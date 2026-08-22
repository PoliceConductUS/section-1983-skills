import copy
import importlib.util
import json
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPOSITORY_ROOT / "skills" / "studying-rule-59e-decisions"
REFERENCES_ROOT = SKILL_ROOT / "references"
DECISION_SCHEMA = "decision-corpus.schema.json"
TRANSFER_SCHEMA = "transfer-card.schema.json"

REQUIRED_CONTRACTS = {
    (DECISION_SCHEMA, ""): "TOP_LEVEL_REQUIRED",
    (DECISION_SCHEMA, "$defs.study"): "STUDY_REQUIRED",
    (DECISION_SCHEMA, "$defs.study.properties.date_range"): "DATE_RANGE_REQUIRED",
    (DECISION_SCHEMA, "$defs.denominator"): "DENOMINATOR_REQUIRED",
    (DECISION_SCHEMA, "$defs.decisionRecord"): "DECISION_REQUIRED",
    (DECISION_SCHEMA, "$defs.decisionRecord.properties.posture"): "POSTURE_REQUIRED",
    (
        DECISION_SCHEMA,
        "$defs.decisionRecord.properties.ground_children.items",
    ): "GROUND_REQUIRED",
    (
        DECISION_SCHEMA,
        "$defs.decisionRecord.properties.proposed_material",
    ): "PROPOSED_MATERIAL_REQUIRED",
    (
        DECISION_SCHEMA,
        "$defs.decisionRecord.properties.disposition",
    ): "DISPOSITION_REQUIRED",
    (
        DECISION_SCHEMA,
        "$defs.decisionRecord.properties.sources.items",
    ): "SOURCE_REQUIRED",
    (
        DECISION_SCHEMA,
        "$defs.decisionRecord.properties.missing_documents.items",
    ): "MISSING_DOCUMENT_REQUIRED",
    (
        DECISION_SCHEMA,
        "$defs.decisionRecord.properties.appellate_history",
    ): "APPELLATE_HISTORY_REQUIRED",
    (DECISION_SCHEMA, "$defs.retrievalGap"): "GAP_REQUIRED",
    (DECISION_SCHEMA, "$defs.transferCard"): "CARD_REQUIRED",
    (TRANSFER_SCHEMA, ""): "CARD_REQUIRED",
}

ENUM_CONTRACTS = {
    (
        DECISION_SCHEMA,
        "$defs.denominator.properties.sampling_method",
    ): "SAMPLING_METHOD_VALUES",
    (
        DECISION_SCHEMA,
        "$defs.denominator.properties.completeness_status",
    ): "COMPLETENESS_STATUS_VALUES",
    (
        DECISION_SCHEMA,
        "$defs.decisionRecord.properties.decision_type",
    ): "DECISION_TYPES",
    (
        DECISION_SCHEMA,
        "$defs.decisionRecord.properties.posture.properties.rule_subsection",
    ): "RULE_SUBSECTION_VALUES",
    (
        DECISION_SCHEMA,
        "$defs.decisionRecord.properties.posture.properties.representation_status",
    ): "REPRESENTATION_STATUS_VALUES",
    (
        DECISION_SCHEMA,
        "$defs.decisionRecord.properties.proposed_material.properties.status",
    ): "PROPOSED_MATERIAL_VALUES",
    (
        DECISION_SCHEMA,
        "$defs.decisionRecord.properties.independent_reasoning",
    ): "INDEPENDENCE_VALUES",
    (
        DECISION_SCHEMA,
        "$defs.decisionRecord.properties.disposition.properties.code",
    ): "DISPOSITION_VALUES",
    (
        DECISION_SCHEMA,
        "$defs.decisionRecord.properties.disposition.properties.stated_reasons.items",
    ): "STATED_REASON_VALUES",
    (
        DECISION_SCHEMA,
        "$defs.decisionRecord.properties.retrieval_status",
    ): "RETRIEVAL_STATUS_VALUES",
    (
        DECISION_SCHEMA,
        "$defs.decisionRecord.properties.coding_confidence",
    ): "CODING_CONFIDENCE_VALUES",
    (
        DECISION_SCHEMA,
        "$defs.retrievalGap.properties.status",
    ): "GAP_STATUS_VALUES",
    (
        DECISION_SCHEMA,
        "$defs.transferCard.properties.evidence_level",
    ): "EVIDENCE_LEVEL_VALUES",
    (
        DECISION_SCHEMA,
        "$defs.transferCard.properties.metric_type",
    ): "METRIC_TYPE_VALUES",
    (TRANSFER_SCHEMA, "properties.evidence_level"): "EVIDENCE_LEVEL_VALUES",
    (TRANSFER_SCHEMA, "properties.metric_type"): "METRIC_TYPE_VALUES",
}


def load_schema(name):
    return json.loads((REFERENCES_ROOT / name).read_text(encoding="utf-8"))


def load_validator():
    path = SKILL_ROOT / "scripts" / "validate_corpus.py"
    specification = importlib.util.spec_from_file_location("rule59_validator", path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def nested_value(schema, path):
    value = schema
    for segment in filter(None, path.split(".")):
        value = value[segment]
    return value


def inventory(schema_name, schema, keyword):
    nodes = set()

    def visit(value, path):
        if isinstance(value, dict):
            if keyword in value:
                nodes.add((schema_name, ".".join(path)))
            for key, child in value.items():
                visit(child, (*path, key))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, (*path, str(index)))

    visit(schema, ())
    return nodes


class Rule59SchemaValidatorAlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas = {
            DECISION_SCHEMA: load_schema(DECISION_SCHEMA),
            TRANSFER_SCHEMA: load_schema(TRANSFER_SCHEMA),
        }
        cls.validator = load_validator()

    def assert_contract_matches(self, contract, schema_values, validator_values):
        schema_only = sorted(set(schema_values) - set(validator_values))
        validator_only = sorted(set(validator_values) - set(schema_values))
        self.assertFalse(
            schema_only or validator_only,
            f"{contract}: schema-only={schema_only}; validator-only={validator_only}",
        )

    def assert_inventory_matches(self, keyword, contracts):
        actual = set()
        for schema_name, schema in self.schemas.items():
            actual.update(inventory(schema_name, schema, keyword))
        self.assertEqual(set(contracts), actual)

    def assert_constants_match(self, keyword, contracts):
        for (schema_name, path), constant_name in contracts.items():
            contract = f"{schema_name}:{path or '<root>'}"
            with self.subTest(contract=contract):
                self.assertTrue(
                    hasattr(self.validator, constant_name),
                    f"validator constant missing: {constant_name}",
                )
                schema_values = nested_value(self.schemas[schema_name], path)[keyword]
                self.assert_contract_matches(
                    contract,
                    schema_values,
                    getattr(self.validator, constant_name),
                )

    def test_required_field_inventory_is_complete(self):
        self.assert_inventory_matches("required", REQUIRED_CONTRACTS)

    def test_enum_inventory_is_complete(self):
        self.assert_inventory_matches("enum", ENUM_CONTRACTS)

    def test_required_fields_match_validator_constants(self):
        self.assert_constants_match("required", REQUIRED_CONTRACTS)

    def test_controlled_values_match_validator_constants(self):
        self.assert_constants_match("enum", ENUM_CONTRACTS)

    def test_required_field_mismatch_identifies_one_sided_values(self):
        schema = copy.deepcopy(self.schemas[DECISION_SCHEMA])
        node = nested_value(schema, "$defs.study.properties.date_range")
        node["required"].append("timezone")
        with self.assertRaisesRegex(AssertionError, "schema-only=\\['timezone'\\]"):
            self.assert_contract_matches(
                "study date range", node["required"], ("start", "end")
            )

    def test_enum_mismatch_identifies_one_sided_values(self):
        schema = copy.deepcopy(self.schemas[TRANSFER_SCHEMA])
        node = nested_value(schema, "properties.metric_type")
        node["enum"].append("predictive")
        with self.assertRaisesRegex(AssertionError, "schema-only=\\['predictive'\\]"):
            self.assert_contract_matches(
                "transfer metric type",
                node["enum"],
                {"descriptive", "success-rate"},
            )


if __name__ == "__main__":
    unittest.main()
