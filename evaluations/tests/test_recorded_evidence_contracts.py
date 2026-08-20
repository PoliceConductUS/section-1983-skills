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
    "visible event or conduct": r"event or conduct.{0,80}visible.{0,40}video",
    "verified transcript": r"verified transcript",
    "exact quotation": r"exact quotation.{0,60}match.{0,40}exact",
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


class RecordedEvidenceContractTest(unittest.TestCase):
    def test_every_public_contract_contains_every_recorded_evidence_obligation(self):
        for contract_id, path in CONTRACT_PATHS.items():
            contract = normalized_contract(path)
            for obligation, pattern in OBLIGATIONS.items():
                with self.subTest(contract=contract_id, obligation=obligation):
                    self.assertRegex(contract, pattern)

    def test_rule_59_final_review_numbering_is_continuous(self):
        skill = CONTRACT_PATHS["rule-59"].read_text(encoding="utf-8")
        final_review = skill.split("Reject the packet unless:", 1)[1].split(
            "Do not call the packet filing-ready", 1
        )[0]
        numbers = [int(value) for value in re.findall(r"(?m)^(\d+)\.", final_review)]
        self.assertGreaterEqual(len(numbers), 1)
        self.assertEqual(numbers, list(range(1, len(numbers) + 1)))


if __name__ == "__main__":
    unittest.main()
