import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

import yaml


REPOSITORY = Path(__file__).resolve().parents[2]
SKILL = REPOSITORY / "skills" / "audit-authorities"
SCHEMA = SKILL / "references" / "proposition-audit.schema.json"
SUPERVISION = SKILL / "scripts" / "legal_rag_supervision.py"
CORPUS = REPOSITORY / "evaluations" / "legal-rag-regression-corpus" / "v1"

TAXONOMY = (
    "inverted-holding",
    "party-argument-as-holding",
    "lower-court-as-appellate-voice",
    "superseded-panel",
    "overruled-authority",
    "wrong-jurisdiction",
    "wrong-statute",
    "wrong-date",
    "wrong-posture",
    "irrelevant-citation",
    "split-support",
    "uncited-material-proposition",
    "fictional-judge",
    "nonexistent-rule-provision",
    "false-premise",
)

SOURCE_VOICES = {
    "majority-holding",
    "court-dicta",
    "party-argument",
    "lower-court-ruling-under-review",
    "factual-or-procedural-background",
    "concurrence",
    "dissent",
    "quoted-secondary-authority",
    "none",
}


def load_module():
    spec = importlib.util.spec_from_file_location("legal_rag_supervision", SUPERVISION)
    if spec is None or spec.loader is None:
        raise AssertionError("missing supervision module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fingerprint(role, path, digest, source_id=None):
    value = {"role": role, "path": path, "sha256": digest}
    if source_id is not None:
        value["source_id"] = source_id
    return value


def proposition(correctness="verified", groundedness="grounded"):
    return {
        "proposition_id": "prop-1",
        "filing_location": {
            "document_path": "draft.md",
            "section": "Argument",
            "paragraph": 1,
            "sentence": 1,
        },
        "text": "Synthetic proposition.",
        "type": "legal-standard",
        "materiality": "material",
        "correctness": correctness,
        "groundedness": groundedness,
        "source_support": [],
        "verification_provenance": {
            "audit_stage": "independent-authority-audit",
            "input_fingerprints": ["b" * 64, "c" * 64],
            "selected_source_ids": ["authority-1"],
            "executed_at": "2026-08-25T12:05:00Z",
        },
    }


def record():
    target = fingerprint("filing-source", "draft.md", "b" * 64)
    source = fingerprint(
        "verified-authority", "authority-1.txt", "c" * 64, "authority-1"
    )
    return {
        "schema_version": 1,
        "audit_id": "audit-1",
        "target": {"role": "filing-source", "path": "draft.md"},
        "target_sha256": "b" * 64,
        "checked_through": "2026-08-25T12:05:00Z",
        "overall_result": "passed",
        "human_approval": "not-provided",
        "generation_stage": {
            "stage_id": "generation-1",
            "invocation_id": "invocation-generation-1",
            "stage_kind": "material-revision",
            "model_or_provider": "synthetic-generator-v1",
            "input_fingerprints": [
                fingerprint("case-record", "facts.md", "a" * 64)
            ],
            "output": target,
            "output_folder_fingerprint": "d" * 64,
            "executed_at": "2026-08-25T12:00:00Z",
        },
        "audit_stage": {
            "stage_id": "authority-audit-1",
            "invocation_id": "invocation-audit-1",
            "stage_kind": "independent-authority-audit",
            "review_relationship": "independent-stage",
            "model_or_provider": "synthetic-auditor-v1",
            "input_fingerprints": [target, source],
            "selected_source_ids": ["authority-1"],
            "output_folder_fingerprint": "e" * 64,
            "executed_at": "2026-08-25T12:05:00Z",
            "execution_outcome": "successful-independent-execution",
        },
        "propositions": [proposition()],
    }


def current_fingerprints():
    return [
        fingerprint("filing-source", "draft.md", "b" * 64),
        fingerprint(
            "verified-authority", "authority-1.txt", "c" * 64, "authority-1"
        ),
    ]


class IndependentLegalRagSupervisionTest(unittest.TestCase):
    def test_schema_requires_both_stages_exact_fingerprints_and_no_human_approval_claim(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

        self.assertTrue(
            {"generation_stage", "audit_stage", "human_approval"}.issubset(
                schema["required"]
            )
        )
        self.assertEqual(schema["properties"]["human_approval"]["const"], "not-provided")
        for definition in ("generation_stage", "audit_stage"):
            required = set(schema["$defs"][definition]["required"])
            self.assertTrue(
                {
                    "stage_id",
                    "invocation_id",
                    "model_or_provider",
                    "input_fingerprints",
                    "output_folder_fingerprint",
                    "executed_at",
                }.issubset(required)
            )
        self.assertEqual(
            schema["$defs"]["audit_stage"]["properties"]["execution_outcome"]["enum"],
            [
                "successful-independent-execution",
                "independent-execution-unavailable",
                "malformed-audit-output",
            ],
        )

    def test_success_requires_separate_stage_distinct_output_and_unchanged_exact_inputs(self):
        classifier = load_module().classify_supervision

        result = classifier(record(), current_fingerprints())

        self.assertEqual(
            result,
            {
                "execution_outcome": "successful-independent-execution",
                "proposition_outcomes": ["completed-grounded-propositions"],
                "supervision_result": "passed",
            },
        )

    def test_self_review_missing_stage_changed_input_and_reused_output_fail_closed(self):
        classifier = load_module().classify_supervision
        cases = []

        self_review = record()
        self_review["audit_stage"]["stage_id"] = self_review["generation_stage"][
            "stage_id"
        ]
        cases.append(("generator-self-review", self_review, current_fingerprints()))

        missing = record()
        missing.pop("audit_stage")
        cases.append(("missing-independent-stage", missing, current_fingerprints()))

        changed = current_fingerprints()
        changed[1]["sha256"] = "f" * 64
        cases.append(("changed-input", record(), changed))

        reused_output = record()
        reused_output["audit_stage"]["output_folder_fingerprint"] = reused_output[
            "generation_stage"
        ]["output_folder_fingerprint"]
        cases.append(("reused-output-folder", reused_output, current_fingerprints()))

        for expected, supplied_record, fingerprints in cases:
            with self.subTest(expected=expected):
                result = classifier(supplied_record, fingerprints)
                self.assertEqual(result["supervision_result"], expected)
                self.assertNotEqual(result["supervision_result"], "passed")

    def test_execution_and_every_proposition_failure_class_remain_distinct(self):
        classifier = load_module().classify_supervision

        cases = (
            ("independent-execution-unavailable", None, None),
            ("malformed-audit-output", None, None),
            ("successful-independent-execution", "unresolved", "not-applicable"),
            ("successful-independent-execution", "incorrect", "not-applicable"),
            ("successful-independent-execution", "verified", "misgrounded"),
            ("successful-independent-execution", "verified", "ungrounded"),
        )
        expected = (
            "independent-execution-unavailable",
            "malformed-audit-output",
            "unresolved-source-gaps",
            "incorrect-propositions",
            "misgrounded-propositions",
            "ungrounded-propositions",
        )

        for values, expected_result in zip(cases, expected):
            execution, correctness, groundedness = values
            supplied = record()
            supplied["audit_stage"]["execution_outcome"] = execution
            supplied["overall_result"] = "unavailable" if correctness is None else "findings"
            if correctness is not None:
                supplied["propositions"] = [proposition(correctness, groundedness)]
            else:
                supplied["propositions"] = []
            with self.subTest(expected=expected_result):
                result = classifier(supplied, current_fingerprints())
                self.assertEqual(result["supervision_result"], expected_result)
                self.assertNotEqual(result["supervision_result"], "passed")

    def test_credentials_continuation_state_and_ai_human_approval_are_rejected(self):
        classifier = load_module().classify_supervision
        cases = []
        for key in (
            "api_key",
            "access_token",
            "continuation_state",
            "conversation_id",
            "provider_session_id",
            "session_id",
        ):
            supplied = record()
            supplied["audit_stage"][key] = "secret-value"
            cases.append(supplied)
        approval = record()
        approval["human_approval"] = "approved"
        cases.append(approval)

        for supplied in cases:
            with self.subTest(keys=tuple(supplied["audit_stage"])):
                self.assertEqual(
                    classifier(supplied, current_fingerprints())[
                        "supervision_result"
                    ],
                    "invalid-supervision-record",
                )

    def test_skill_requires_new_invocation_new_output_exact_bytes_and_human_decision(self):
        text = " ".join(
            path.read_text(encoding="utf-8")
            for path in SKILL.rglob("*")
            if path.is_file() and path.suffix in {".md", ".json", ".py"}
        ).casefold()
        text = " ".join(text.split())
        for required in (
            "separate non-mutating",
            "new output folder",
            "generation stage",
            "audit stage",
            "changed input",
            "generator self-review",
            "human approval",
            "human-reserved",
            "not-provided",
            "historical benchmark",
            "query distribution",
            "sample size",
            "current vendor reliability rate",
        ):
            self.assertIn(required, text)

    def test_versioned_yaml_corpus_has_complete_strict_network_independent_taxonomy(self):
        manifest = yaml.safe_load((CORPUS / "manifest.yaml").read_text(encoding="utf-8"))

        self.assertEqual(manifest, {"version": 1, "fixtures": list(TAXONOMY)})
        self.assertEqual(
            sorted(path.stem for path in CORPUS.glob("*.yaml") if path.name != "manifest.yaml"),
            sorted(TAXONOMY),
        )
        for fixture_id in TAXONOMY:
            with self.subTest(fixture=fixture_id):
                fixture = yaml.safe_load(
                    (CORPUS / f"{fixture_id}.yaml").read_text(encoding="utf-8")
                )
                self.assertEqual(
                    set(fixture),
                    {
                        "version",
                        "id",
                        "source",
                        "challenged_text",
                        "expected_propositions",
                        "pass_allowed",
                        "reason",
                    },
                )
                self.assertEqual((fixture["version"], fixture["id"]), (1, fixture_id))
                self.assertEqual(
                    hashlib.sha256(fixture["source"]["text"].encode("utf-8")).hexdigest(),
                    fixture["source"]["sha256"],
                )
                self.assertFalse(fixture["pass_allowed"])
                self.assertTrue(fixture["challenged_text"].strip())
                self.assertTrue(fixture["reason"].strip())
                self.assertNotIn("http://", str(fixture).casefold())
                self.assertNotIn("https://", str(fixture).casefold())
                self.assertGreaterEqual(len(fixture["expected_propositions"]), 1)
                for proposition_result in fixture["expected_propositions"]:
                    self.assertEqual(
                        set(proposition_result),
                        {
                            "proposition_id",
                            "correctness",
                            "groundedness",
                            "source_voice",
                        },
                    )
                    self.assertIn(
                        proposition_result["correctness"],
                        {"verified", "incorrect", "unresolved"},
                    )
                    self.assertIn(
                        proposition_result["groundedness"],
                        {"grounded", "misgrounded", "ungrounded", "not-applicable"},
                    )
                    self.assertIn(proposition_result["source_voice"], SOURCE_VOICES)


if __name__ == "__main__":
    unittest.main()
