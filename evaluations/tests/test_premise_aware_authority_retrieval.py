import copy
import importlib.util
import json
import unittest
from pathlib import Path

import yaml

from evaluations.deterministic import grade_candidate
from evaluations.fixtures import load_fixture


REPOSITORY = Path(__file__).resolve().parents[2]
SKILL = REPOSITORY / "skills" / "collecting-legal-authority-sources"
SCRIPT = SKILL / "scripts" / "authority_source_records.py"
TEST_FIXTURES = (
    REPOSITORY / "evaluations/tests/fixtures/authority-source-collection"
)
EVALUATION_FIXTURE = (
    REPOSITORY / "evaluations/fixtures/authority-retrieval-premise-failures"
)


def load_module():
    specification = importlib.util.spec_from_file_location(
        "premise_aware_authority_source_records", SCRIPT
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def fixture(name):
    return json.loads((TEST_FIXTURES / name).read_text(encoding="utf-8"))


def frame():
    return fixture("retrieval-frame.json")["frame"]


def premises():
    return fixture("premises.json")["premises"]


def source():
    value = fixture("mirror-opinion.json")["source"]
    value["artifact_bytes"] = value.pop("artifact_text").encode()
    value.update(
        {
            "frame_id": "frame-qualified-immunity-notice",
            "source_system_id": "fictional-official-search",
            "provider_or_product_id": "fictional-search-v1",
            "execution_date": "2026-08-25",
            "retrieval_order": 2,
            "proposed_legal_role": "candidate pre-event circuit authority",
            "rejection_reason": None,
        }
    )
    return value


def gap():
    value = fixture("coverage-gap.json")["gap"]
    value.update(
        {
            "frame_id": "frame-qualified-immunity-notice",
            "known_missingness": "The index omits sealed and unindexed dockets.",
        }
    )
    return value


def artifact(plan, path):
    return next(item for item in plan["artifacts"] if item["path"] == path)


class PremiseAwareAuthorityRetrievalTest(unittest.TestCase):
    def test_plan_publishes_strict_frame_premises_and_expanded_source_provenance(self):
        records = load_module()

        plan = records.build_collection_plan(frame(), premises(), [source()], [gap()])

        self.assertEqual(
            [item["path"] for item in plan["artifacts"]],
            [
                "sources/fictional-opinion-mirror.txt",
                "sources/fictional-opinion-mirror.SOURCE.yaml",
                "authority-retrieval-frame.yaml",
                "authority-retrieval-premises.yaml",
                "authority-source-candidates.yaml",
                "authority-source-gaps.yaml",
            ],
        )
        retrieval_frame = yaml.safe_load(
            artifact(plan, "authority-retrieval-frame.yaml")["bytes"]
        )
        self.assertEqual(retrieval_frame, {"version": 1, **frame()})
        premise_document = yaml.safe_load(
            artifact(plan, "authority-retrieval-premises.yaml")["bytes"]
        )
        self.assertEqual(
            premise_document["premises"],
            sorted(premises(), key=lambda item: item["premise_id"]),
        )

        source_yaml = yaml.safe_load(
            artifact(plan, "sources/fictional-opinion-mirror.SOURCE.yaml")["bytes"]
        )
        for field in (
            "frame_id",
            "source_system_id",
            "provider_or_product_id",
            "execution_date",
            "query",
            "filters",
            "result_identity",
            "retrieval_order",
            "proposed_legal_role",
            "rejection_reason",
        ):
            self.assertIn(field, source_yaml)
        self.assertEqual(source_yaml["retrieval_order"], 2)

    def test_false_and_unresolved_premises_require_correction_or_gap(self):
        records = load_module()
        cases = []
        false_without_correction = premises()
        false_without_correction[1]["correction"] = None
        cases.append(false_without_correction)
        unresolved_without_gap = premises()
        unresolved_without_gap[2]["gap"] = None
        cases.append(unresolved_without_gap)
        verified_with_correction = premises()
        verified_with_correction[0]["correction"] = "unexpected"
        cases.append(verified_with_correction)

        for premise_records in cases:
            with self.subTest(premises=premise_records):
                with self.assertRaises(records.AuthoritySourceError) as captured:
                    records.build_collection_plan(
                        frame(), premise_records, [source()], [gap()]
                    )
                self.assertEqual(captured.exception.code, "invalid-premise-record")

    def test_rejected_candidates_preserve_stable_reason_and_original_order(self):
        records = load_module()
        accepted = source()
        accepted["source_id"] = "src-later-result"
        accepted["artifact_path"] = "sources/later-result.txt"
        accepted["source_documentation_path"] = "sources/later-result.SOURCE.yaml"
        accepted["result_identity"] = "fictional:later-result"
        accepted["retrieval_order"] = 2
        rejected = source()
        rejected["source_id"] = "src-first-result"
        rejected["artifact_path"] = "sources/first-result.txt"
        rejected["source_documentation_path"] = "sources/first-result.SOURCE.yaml"
        rejected["result_identity"] = "fictional:first-result"
        rejected["retrieval_order"] = 1
        rejected["review_state"] = "rejected"
        rejected["rejection_reason"] = "wrong-statute"

        plan = records.build_collection_plan(
            frame(), premises(), [accepted, rejected], [gap()]
        )
        candidates = yaml.safe_load(
            artifact(plan, "authority-source-candidates.yaml")["bytes"]
        )["sources"]
        self.assertEqual(
            [item["source_id"] for item in candidates],
            ["src-first-result", "src-later-result"],
        )
        self.assertEqual(candidates[0]["rejection_reason"], "wrong-statute")
        self.assertIsNone(candidates[1]["rejection_reason"])

        invalid = copy.deepcopy(rejected)
        invalid["rejection_reason"] = None
        with self.assertRaises(records.AuthoritySourceError) as captured:
            records.build_collection_plan(frame(), premises(), [invalid], [gap()])
        self.assertEqual(captured.exception.code, "invalid-source-record")

    def test_gaps_preserve_frame_known_missingness_and_nonexistence_boundary(self):
        records = load_module()
        plan = records.build_collection_plan(frame(), premises(), [], [gap()])

        gap_record = yaml.safe_load(
            artifact(plan, "authority-source-gaps.yaml")["bytes"]
        )["gaps"][0]
        self.assertEqual(gap_record["frame_id"], frame()["frame_id"])
        self.assertTrue(gap_record["known_missingness"])
        self.assertIn("omits", gap_record["coverage_limit"])

    def test_skill_states_candidate_only_boundary_and_complete_frame(self):
        text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SKILL.rglob("*")
            if path.is_file() and path.suffix in {".md", ".py"}
        ).casefold()
        for required in (
            "retrieval lead",
            "governing jurisdiction",
            "operative date",
            "statute or rule version",
            "material factual trigger",
            "verified`, `false`, or `unresolved",
            "wrong-statute",
            "retrieval order",
            "known missingness",
            "never establish that no authority exists",
        ):
            self.assertIn(required, text)

    def test_required_failure_taxonomy_has_one_passing_and_nine_regressions(self):
        retrieval_fixture = load_fixture(EVALUATION_FIXTURE)

        self.assertEqual(
            retrieval_fixture["id"], "authority-retrieval-premise-failures"
        )
        self.assertEqual(
            retrieval_fixture["target_skill"],
            "collecting-legal-authority-sources",
        )
        self.assertTrue(
            grade_candidate(
                retrieval_fixture, retrieval_fixture["passing_candidate"]
            )["passed"]
        )
        self.assertEqual(len(retrieval_fixture["regressions"]), 9)
        for regression in retrieval_fixture["regressions"]:
            observed = {
                finding["id"]
                for finding in grade_candidate(
                    retrieval_fixture, regression["candidate"]
                )["findings"]
            }
            self.assertTrue(set(regression["expected_findings"]).issubset(observed))


if __name__ == "__main__":
    unittest.main()
