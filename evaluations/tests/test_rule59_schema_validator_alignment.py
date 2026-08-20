import copy
import importlib.util
import json
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPOSITORY_ROOT / "skills" / "studying-rule-59e-decisions"
REFERENCES_ROOT = SKILL_ROOT / "references"
DECISION_SCHEMA_NAME = "decision-corpus.schema.json"
TRANSFER_SCHEMA_NAME = "transfer-card.schema.json"

REQUIRED_CONTRACTS = {
    (DECISION_SCHEMA_NAME,): "TOP_LEVEL_REQUIRED",
    (DECISION_SCHEMA_NAME, "$defs", "study"): "STUDY_REQUIRED",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "study",
        "properties",
        "date_range",
    ): "DATE_RANGE_REQUIRED",
    (DECISION_SCHEMA_NAME, "$defs", "denominator"): "DENOMINATOR_REQUIRED",
    (DECISION_SCHEMA_NAME, "$defs", "decisionRecord"): "DECISION_REQUIRED",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "posture",
    ): "POSTURE_REQUIRED",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "ground_children",
        "items",
    ): "GROUND_REQUIRED",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "proposed_material",
    ): "PROPOSED_MATERIAL_REQUIRED",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "disposition",
    ): "DISPOSITION_REQUIRED",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "sources",
        "items",
    ): "SOURCE_REQUIRED",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "missing_documents",
        "items",
    ): "MISSING_DOCUMENT_REQUIRED",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "appellate_history",
    ): "APPELLATE_HISTORY_REQUIRED",
    (DECISION_SCHEMA_NAME, "$defs", "retrievalGap"): "GAP_REQUIRED",
    (DECISION_SCHEMA_NAME, "$defs", "transferCard"): "CARD_REQUIRED",
    (TRANSFER_SCHEMA_NAME,): "CARD_REQUIRED",
}

ENUM_CONTRACTS = {
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "denominator",
        "properties",
        "sampling_method",
    ): "SAMPLING_METHOD_VALUES",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "denominator",
        "properties",
        "completeness_status",
    ): "COMPLETENESS_STATUS_VALUES",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "decision_type",
    ): "DECISION_TYPES",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "posture",
        "properties",
        "rule_subsection",
    ): "RULE_SUBSECTION_VALUES",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "posture",
        "properties",
        "representation_status",
    ): "REPRESENTATION_STATUS_VALUES",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "proposed_material",
        "properties",
        "status",
    ): "PROPOSED_MATERIAL_VALUES",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "independent_reasoning",
    ): "INDEPENDENCE_VALUES",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "disposition",
        "properties",
        "code",
    ): "DISPOSITION_VALUES",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "disposition",
        "properties",
        "stated_reasons",
        "items",
    ): "STATED_REASON_VALUES",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "retrieval_status",
    ): "RETRIEVAL_STATUS_VALUES",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "decisionRecord",
        "properties",
        "coding_confidence",
    ): "CODING_CONFIDENCE_VALUES",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "retrievalGap",
        "properties",
        "status",
    ): "GAP_STATUS_VALUES",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "transferCard",
        "properties",
        "evidence_level",
    ): "EVIDENCE_LEVEL_VALUES",
    (
        DECISION_SCHEMA_NAME,
        "$defs",
        "transferCard",
        "properties",
        "metric_type",
    ): "METRIC_TYPE_VALUES",
    (
        TRANSFER_SCHEMA_NAME,
        "properties",
        "evidence_level",
    ): "EVIDENCE_LEVEL_VALUES",
    (
        TRANSFER_SCHEMA_NAME,
        "properties",
        "metric_type",
    ): "METRIC_TYPE_VALUES",
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_validator():
    path = SKILL_ROOT / "scripts" / "validate_corpus.py"
    specification = importlib.util.spec_from_file_location("rule59_validator", path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def contract_nodes(schema_name, schema, keyword):
    nodes = {}

    def visit(value, path):
        if isinstance(value, dict):
            if keyword in value:
                nodes[(schema_name, *path)] = value[keyword]
            for key, child in value.items():
                visit(child, (*path, key))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, (*path, str(index)))

    visit(schema, ())
    return nodes


def schema_value(schema, path, keyword):
    value = schema
    for segment in path[1:]:
        value = value[segment]
    return value[keyword]


def mismatch_message(contract, schema_values, validator_values):
    schema_only = sorted(set(schema_values) - set(validator_values))
    validator_only = sorted(set(validator_values) - set(schema_values))
    return (
        f"{contract}: schema-only={schema_only}; "
        f"validator-only={validator_only}"
    )


class Rule59SchemaValidatorAlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas = {
            DECISION_SCHEMA_NAME: load_json(REFERENCES_ROOT / DECISION_SCHEMA_NAME),
            TRANSFER_SCHEMA_NAME: load_json(REFERENCES_ROOT / TRANSFER_SCHEMA_NAME),
        }
        cls.validator = load_validator()

    def assert_contract_matches(self, contract, schema_values, validator_values):
        self.assertEqual(
            set(schema_values),
            set(validator_values),
            mismatch_message(contract, schema_values, validator_values),
        )

    def test_required_field_inventory_is_complete(self):
        inventory = {}
        for schema_name, schema in self.schemas.items():
            inventory.update(contract_nodes(schema_name, schema, "required"))
        self.assertEqual(set(REQUIRED_CONTRACTS), set(inventory))

    def test_enum_inventory_is_complete(self):
        inventory = {}
        for schema_name, schema in self.schemas.items():
            inventory.update(contract_nodes(schema_name, schema, "enum"))
        self.assertEqual(set(ENUM_CONTRACTS), set(inventory))

    def test_required_fields_match_validator_constants(self):
        for path, constant_name in REQUIRED_CONTRACTS.items():
            with self.subTest(contract="/".join(path)):
                self.assertTrue(
                    hasattr(self.validator, constant_name),
                    f"validator constant missing: {constant_name}",
                )
                self.assert_contract_matches(
                    "/".join(path),
                    schema_value(self.schemas[path[0]], path, "required"),
                    getattr(self.validator, constant_name),
                )

    def test_controlled_values_match_validator_constants(self):
        for path, constant_name in ENUM_CONTRACTS.items():
            with self.subTest(contract="/".join(path)):
                self.assertTrue(
                    hasattr(self.validator, constant_name),
                    f"validator constant missing: {constant_name}",
                )
                self.assert_contract_matches(
                    "/".join(path),
                    schema_value(self.schemas[path[0]], path, "enum"),
                    getattr(self.validator, constant_name),
                )

    def test_required_field_mismatch_identifies_one_sided_values(self):
        schema = copy.deepcopy(self.schemas[DECISION_SCHEMA_NAME])
        schema["$defs"]["study"]["properties"]["date_range"]["required"].append(
            "timezone"
        )
        values = schema_value(
            schema,
            (
                DECISION_SCHEMA_NAME,
                "$defs",
                "study",
                "properties",
                "date_range",
            ),
            "required",
        )
        with self.assertRaisesRegex(AssertionError, "schema-only=\\['timezone'\\]"):
            self.assert_contract_matches(
                "study date range",
                values,
                ("start", "end"),
            )

    def test_enum_mismatch_identifies_one_sided_values(self):
        schema = copy.deepcopy(self.schemas[TRANSFER_SCHEMA_NAME])
        schema["properties"]["metric_type"]["enum"].append("predictive")
        values = schema_value(
            schema,
            (TRANSFER_SCHEMA_NAME, "properties", "metric_type"),
            "enum",
        )
        with self.assertRaisesRegex(AssertionError, "schema-only=\\['predictive'\\]"):
            self.assert_contract_matches(
                "transfer metric type",
                values,
                {"descriptive", "success-rate"},
            )


if __name__ == "__main__":
    unittest.main()
