import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATHS = {
    "complaint-completion": REPOSITORY_ROOT
    / "skills"
    / "drafting-section-1983-complaints"
    / "references"
    / "completion-audit.md",
    "complaint-claims": REPOSITORY_ROOT
    / "skills"
    / "drafting-section-1983-complaints"
    / "references"
    / "claim-specific-contracts.md",
    "rule-59": REPOSITORY_ROOT
    / "skills"
    / "drafting-section-1983-rule-59e"
    / "SKILL.md",
}
OBLIGATIONS = {
    "recorded interval": r"recorded interval",
    "visible event or conduct": r"event or conduct (?:is|must be) visible.{0,40}video",
    "verified transcript": r"verified transcript",
    "exact quotation": (
        r"exact quotations? (?:must )?match(?:ing)?"
        r"(?: the transcript)? exact(?:ly)?"
    ),
    "bounded paraphrase": r"paraphrase.{0,40}(?:add(?:ing)? no content|may not add content)",
    "uncertain speaker": r"uncertain speaker attribution.{0,60}(?:preserved|remain uncertain)",
    "present recollection": r"present recollection",
    "unresolved recording": r"recordings.{0,40}(?:available|presently available).{0,40}do not resolve",
    "later correction": r"subject to correction",
    "additional recording": r"additional recordings.{0,40}produced or located",
    "fail closed": r"(?:complete only if|fail validation|fail packet validation)",
}


def normalized_contract(path):
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8").lower())


def rule_59_final_review_items(skill):
    final_review = skill.split("Reject the packet unless:", 1)[1].split(
        "Do not call the packet filing-ready", 1
    )[0]
    matches = list(re.finditer(r"(?m)^(\d+)\. ", final_review))
    return [
        (
            int(match.group(1)),
            re.sub(
                r"\s+",
                " ",
                final_review[
                    match.end() : matches[index + 1].start()
                    if index + 1 < len(matches)
                    else len(final_review)
                ],
            ).lower(),
        )
        for index, match in enumerate(matches)
    ]


class RecordedEvidenceContractTest(unittest.TestCase):
    def test_every_public_contract_contains_every_recorded_evidence_obligation(self):
        for contract_id, path in CONTRACT_PATHS.items():
            contract = normalized_contract(path)
            for obligation, pattern in OBLIGATIONS.items():
                with self.subTest(contract=contract_id, obligation=obligation):
                    self.assertRegex(contract, pattern)

    def test_rule_59_final_review_numbering_is_continuous(self):
        skill = CONTRACT_PATHS["rule-59"].read_text(encoding="utf-8")
        numbers = [number for number, _ in rule_59_final_review_items(skill)]
        self.assertGreaterEqual(len(numbers), 1)
        self.assertEqual(numbers, list(range(1, len(numbers) + 1)))

    def test_rule_59_final_review_contains_recorded_evidence_checkpoint(self):
        skill = CONTRACT_PATHS["rule-59"].read_text(encoding="utf-8")
        recorded_items = [
            item for _, item in rule_59_final_review_items(skill) if "recorded interval" in item
        ]
        self.assertEqual(len(recorded_items), 1)
        item = recorded_items[0]
        checkpoint_obligations = {
            "visible event or conduct": OBLIGATIONS["visible event or conduct"],
            "transcript-backed statement": (
                r"quoted, paraphrased, or attributed recorded statement"
                r" appears in the verified transcript"
            ),
            "event alternative route": (
                r"or satisfies the express present-recollection route above"
            ),
            "statement alternative route": r"or satisfies that same route",
        }
        for obligation, pattern in checkpoint_obligations.items():
            with self.subTest(obligation=obligation):
                self.assertRegex(item, pattern)

    def test_obligation_patterns_reject_reversed_semantics(self):
        mutations = {
            "visible event or conduct": "event or conduct need not be visible in the video",
            "exact quotation": "exact quotation need not match the transcript exactly",
        }
        for obligation, mutation in mutations.items():
            with self.subTest(obligation=obligation):
                self.assertNotRegex(mutation, OBLIGATIONS[obligation])


if __name__ == "__main__":
    unittest.main()
