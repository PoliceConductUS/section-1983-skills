import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
VALIDATOR = (
    REPOSITORY
    / "skills"
    / "drafting-section-1983-complaints"
    / "scripts"
    / "validate_complaint_handoff.py"
)


def load_validator():
    spec = importlib.util.spec_from_file_location("complaint_validator", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def common_count():
    return {
        "count_id": "count-1",
        "claim": "Fourth Amendment false arrest",
        "constitutional_source": "Fourth Amendment",
        "defendant": "Officer One",
        "capacity": "individual",
        "challenged_act": "arrest",
        "event_stage": "arrest decision",
        "standard": "probable cause",
        "standard_pincite": "Case, 1 F.4th 1, 5",
        "decisive_fact_paragraphs": [21, 22],
        "incorporated_paragraphs": [21, 22],
        "relevant_time_knowledge": "Facts known before arrest",
        "application": "Those facts did not establish the offense.",
        "injury": "custodial arrest",
        "relief": "damages",
        "result": "violation alleged",
        "individual_capacity": {
            "personal_act_or_causal_role": "ordered the arrest",
            "event_stage": "arrest decision",
            "relevant_time": "2023-12-04T22:15:00-06:00",
            "facts_then_known": ["speech", "no observed intoxication fact"],
            "underlying_violation": "arrest without probable cause",
            "application": "The then-known facts did not establish probable cause.",
            "injury": "custodial arrest",
            "causation": "The order caused the arrest.",
        },
        "qualified_immunity": {
            "applies": True,
            "event_date": "2023-12-04",
            "precise_right": "freedom from arrest without probable cause",
            "jurisdiction": "Fifth Circuit",
            "prong_one_result": "violation alleged",
            "prong_two_result": "fair warning alleged",
            "binding_pre_event_authority": ["authority-1"],
            "authority_audit_status": "verified",
            "materially_similar_facts": "same missing offense element",
            "material_differences": "none material",
            "fair_warning": "authority supplied fair warning",
            "rule_of_orderliness_review_status": "complete",
            "later_history_review_status": "complete",
            "later_authority_treatment": "not used for fair warning",
        },
        "monell_paths": [],
    }


def handoff(count=None, assessment=None):
    return {
        "contract_version": 2,
        "document": {
            "path": "complaint.md",
            "sha256": "a" * 64,
            "paragraphs": [21, 22],
        },
        "sections": [
            "caption",
            "jurisdiction-and-venue",
            "parties",
            "statement-of-facts",
            "counts",
            "prayer-for-relief",
            "jury-demand",
            "signature-block",
        ],
        "counts": [count or common_count()],
        "casegraph_assessment": assessment
        or {"status": "not_run_missing", "claim_unit_ids": ["count-1"]},
    }


class MonellContractV2Tests(unittest.TestCase):
    def test_validator_exists_and_accepts_complete_v2_drafting_handoff(self):
        validator = load_validator()
        result = validator.validate_handoff(handoff(), mode="drafting")
        self.assertEqual("pass", result["structural_validation"]["status"])
        self.assertEqual("not_run_missing", result["casegraph_assessment"]["status"])

    def test_version_one_is_rejected_with_stable_code(self):
        validator = load_validator()
        candidate = handoff()
        candidate["contract_version"] = 1
        result = validator.validate_handoff(candidate)
        self.assertIn(
            "unsupported_contract_version",
            {item["code"] for item in result["structural_validation"]["findings"]},
        )

    def test_individual_capacity_and_qi_are_conditionally_required(self):
        validator = load_validator()
        candidate = handoff()
        del candidate["counts"][0]["individual_capacity"]["causation"]
        del candidate["counts"][0]["qualified_immunity"]["fair_warning"]
        result = validator.validate_handoff(candidate)
        codes = {item["code"] for item in result["structural_validation"]["findings"]}
        self.assertIn("missing_individual_capacity_field", codes)
        self.assertIn("missing_qualified_immunity_field", codes)

    def test_monell_path_requires_one_type_and_type_specific_fields(self):
        validator = load_validator()
        count = common_count()
        count["capacity"] = "municipal"
        count["defendant"] = "City"
        count.pop("individual_capacity")
        count["qualified_immunity"] = {"applies": False}
        count["monell_paths"] = [
            {
                "path_id": "policy-1",
                "path_type": ["formal_policy", "custom_or_practice"],
                "challenged_policy_custom_decision_or_omission": "release condition",
            },
            {
                "path_id": "training-1",
                "path_type": "failure_to_train",
                "challenged_policy_custom_decision_or_omission": "FTO instruction",
            },
        ]
        result = validator.validate_handoff(handoff(count))
        codes = {item["code"] for item in result["structural_validation"]["findings"]}
        self.assertIn("invalid_monell_path_type", codes)
        self.assertIn("missing_monell_path_field", codes)

    def test_exact_authority_passage_and_hash_are_verified(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            text = "Page 12\nA municipality is liable only when its policy is the moving force.\n"
            source = root / "opinion.txt"
            source.write_text(text, encoding="utf-8")
            resolution = {
                "status": "resolved",
                "proposition_uid": "prop-1",
                "authority_uid": "auth-1",
                "verified_unit_path": "verified/auth-1",
                "source_metadata_path": "verified/auth-1/SOURCE.yaml",
                "canonical_opinion_path": "opinion.txt",
                "canonical_opinion_sha256": sha256_text(text),
                "text_representation_path": "opinion.txt",
                "text_representation_sha256": sha256_text(text),
                "pinpoint": "12",
                "exact_matched_text": "A municipality is liable only when its policy is the moving force.",
                "stable_locator": "page 12",
                "normalization": "none",
            }
            assessment = {
                "status": "completed",
                "claim_unit_ids": ["count-1"],
                "document_sha256": "a" * 64,
                "authority_resolutions": [resolution],
            }
            result = validator.validate_handoff(handoff(assessment=assessment), root)
            self.assertEqual("completed", result["casegraph_assessment"]["status"])
            self.assertEqual([], result["casegraph_assessment"]["findings"])

            resolution["exact_matched_text"] = "A semantic near match."
            result = validator.validate_handoff(handoff(assessment=assessment), root)
            self.assertIn(
                "text_mismatch",
                {item["code"] for item in result["casegraph_assessment"]["findings"]},
            )

    def test_filing_mode_fails_closed_without_current_complete_assessment(self):
        validator = load_validator()
        result = validator.validate_handoff(handoff(), mode="filing")
        self.assertEqual("fail", result["filing_gate"]["status"])
        self.assertIn("assessment_required", {x["code"] for x in result["filing_gate"]["findings"]})


if __name__ == "__main__":
    unittest.main()
