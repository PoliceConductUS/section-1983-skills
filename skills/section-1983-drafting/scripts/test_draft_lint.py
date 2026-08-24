import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from draft_lint import EXEMPT_PHRASES, LintInputError, lint, lint_folder_target


class LintTest(unittest.TestCase):

    def lint_artifact(self, text, artifact="draft.md"):
        try:
            return lint(text, artifact=artifact)
        except TypeError as error:
            self.fail(f"lint must accept an artifact label: {error}")

    def test_clean_factual_sentence_scores_zero(self):
        report = lint("Officer Doe struck the handcuffed plaintiff four times.")

        self.assertEqual(report["total"], 0)

    def test_top_fifty_word_is_counted(self):
        report = lint("The claim is clearly and obviously meritless.")

        self.assertEqual(report["violations"]["top_fifty_word"], 3)

    def test_more_word_is_counted(self):
        report = lint("Plaintiff has utterly failed in this egregious case.")

        self.assertEqual(report["violations"]["more_word"], 2)
        self.assertEqual(report["violations"]["top_fifty_word"], 1)

    def test_bonus_word_is_counted(self):
        report = lint("Frankly, the order is void.")

        self.assertEqual(report["violations"]["bonus_word"], 1)
        self.assertEqual(report["violations"]["more_word"], 1)

    def test_terms_of_art_are_exempt(self):
        report = lint("The right was clearly established in 2019.")

        self.assertEqual(report["violations"]["top_fifty_word"], 0)

    def test_formal_word_is_counted(self):
        report = lint("Defendants utilize force prior to any warning.")

        self.assertEqual(report["violations"]["formal_word"], 2)

    def test_marketing_adjective_is_counted(self):
        report = lint("The department has a robust training program.")

        self.assertEqual(report["violations"]["marketing_adjective"], 1)

    def test_semicolon_contraction_and_em_dash_are_counted(self):
        report = lint("Doe didn't stop; he continued — twice.")

        self.assertEqual(report["violations"]["semicolon"], 1)
        self.assertEqual(report["violations"]["contraction"], 1)
        self.assertEqual(report["violations"]["em_dash"], 1)

    def test_passive_voice_is_counted(self):
        report = lint("The car was searched at the scene.")

        self.assertEqual(report["violations"]["passive_voice"], 1)

    def test_long_sentence_is_counted(self):
        long_sentence = " ".join(["word"] * 26) + "."

        report = lint(long_sentence)

        self.assertEqual(report["violations"]["long_sentence"], 1)

    def test_empty_opener_is_counted(self):
        report = lint("There are three officers who saw the arrest.")

        self.assertEqual(report["violations"]["empty_opener"], 1)

    def test_score_is_normalized_per_hundred_words(self):
        report = lint("Doe clearly lied. " * 25)

        self.assertAlmostEqual(report["total_per_hundred_words"], 33.33, places=1)

    def test_exempt_section_1983_terms_of_art_score_zero(self):
        text = (
            "Officer Doe used excessive force. "
            "Nurse Roe was deliberately indifferent to serious medical needs. "
            "The right was clearly established. "
            "Plaintiff seeks actual damages and punitive damages."
        )

        report = lint(text)

        self.assertEqual(report["violations"]["top_fifty_word"], 0)
        self.assertEqual(report["violations"]["more_word"], 0)
        self.assertEqual(report["violations"]["bonus_word"], 0)

    def test_proven_current_false_positives_are_new_exemptions(self):
        proven = (
            "active resistance",
            "materially similar",
            "reasonably trustworthy",
        )

        for phrase in proven:
            with self.subTest(phrase=phrase):
                report = self.lint_artifact(f"The rule requires {phrase}.")
                self.assertEqual(report["total"], 0)
                self.assertEqual(
                    [item["phrase"] for item in report["exemptions"]], [phrase]
                )
                self.assertEqual(
                    report["exemptions"][0]["classification"],
                    "controlling_term_of_art",
                )

    def test_already_clean_phrases_do_not_gain_inert_exemptions(self):
        already_clean = (
            "arguable probable cause",
            "particularized right",
            "moving force",
            "probable cause",
        )

        for phrase in already_clean:
            with self.subTest(phrase=phrase):
                report = lint(f"The rule requires {phrase}.")
                self.assertEqual(report["total"], 0)
                self.assertNotIn(phrase, EXEMPT_PHRASES)

    def test_repeated_exemptions_have_unique_stable_ids(self):
        report = self.lint_artifact(
            "The cases are materially similar and materially similar."
        )

        exemption_ids = [item["exemption_id"] for item in report["exemptions"]]
        self.assertEqual(
            exemption_ids,
            [
                "paragraph-1:controlling-term:materially-similar:1",
                "paragraph-1:controlling-term:materially-similar:2",
            ],
        )

    def test_findings_identify_artifact_paragraph_and_source_lines(self):
        text = (
            "Officer Doe waited for five minutes.\n"
            "The delay was unbearably long.\n"
            "\n"
            "Officer Roe acted almost immediately."
        )

        report = self.lint_artifact(text, artifact="versions/v2/draft.md")

        observed = [
            (
                finding["finding_id"],
                finding["check"],
                finding["artifact"],
                finding["paragraph"],
                finding["start_line"],
                finding["end_line"],
                finding["count"],
                finding["classification"],
            )
            for finding in report["findings"]
        ]
        self.assertEqual(
            observed,
            [
                (
                    "paragraph-1:more_word",
                    "more_word",
                    "versions/v2/draft.md",
                    1,
                    1,
                    2,
                    1,
                    "unexempted_violation",
                ),
                (
                    "paragraph-2:top_fifty_word",
                    "top_fifty_word",
                    "versions/v2/draft.md",
                    2,
                    4,
                    4,
                    1,
                    "unexempted_violation",
                ),
                (
                    "paragraph-2:more_word",
                    "more_word",
                    "versions/v2/draft.md",
                    2,
                    4,
                    4,
                    1,
                    "unexempted_violation",
                ),
            ],
        )
        for check, count in report["violations"].items():
            self.assertEqual(
                sum(item["count"] for item in report["findings"] if item["check"] == check),
                count,
            )

    def test_lint_target_confines_one_relative_filing_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "draft.md"
            target.write_text("The delay was unbearably long.")
            before = hashlib.sha256(target.read_bytes()).hexdigest()

            report = lint_folder_target(
                filing_root=root,
                filing_target="draft.md",
            )

            self.assertIn("findings", report)
            self.assertEqual(report["findings"][0]["artifact"], "draft.md")
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), before)

            for path, code in (
                ("../draft.md", "invalid-target"),
                ("/absolute.md", "invalid-target"),
                ("./draft.md", "invalid-target"),
                ("bad\x00name", "invalid-target"),
                ("missing.md", "invalid-target"),
            ):
                with self.subTest(path=path):
                    with self.assertRaises(LintInputError) as captured:
                        lint_folder_target(filing_root=root, filing_target=path)
                    self.assertEqual(captured.exception.code, code)

            with self.assertRaises(LintInputError) as captured:
                lint_folder_target(
                    filing_root=root,
                    filing_target="draft.md",
                    max_input_bytes=1,
                )
            self.assertEqual(captured.exception.code, "input-too-large")

    def test_long_sentence_density_is_a_non_gating_paragraph_warning(self):
        long_sentence = " ".join(["word"] * 26) + "."

        report = self.lint_artifact(f"{long_sentence} {long_sentence}")

        self.assertEqual(report["violations"]["long_sentence"], 2)
        self.assertEqual(report["total"], 2)
        self.assertEqual(
            report["warnings"],
            [
                {
                    "warning_id": "paragraph-1:long_sentence_density",
                    "check": "long_sentence_density",
                    "artifact": "draft.md",
                    "paragraph": 1,
                    "start_line": 1,
                    "end_line": 1,
                    "observed": 2,
                    "threshold": 2,
                    "classification": "review_heuristic",
                }
            ],
        )

    def test_case_citation_density_warns_at_four_but_not_three(self):
        citations = [
            "Alpha v. Beta, 101 F.3d 201",
            "Gamma v. Delta, 102 F.3d 202",
            "Epsilon v. Zeta, 103 F.3d 203",
            "Eta v. Theta, 104 F.3d 204",
        ]

        below = self.lint_artifact("; ".join(citations[:3]) + ".")
        at_threshold = self.lint_artifact("; ".join(citations) + ".")

        self.assertNotIn(
            "case_citation_density", [item["check"] for item in below["warnings"]]
        )
        warning = next(
            item
            for item in at_threshold["warnings"]
            if item["check"] == "case_citation_density"
        )
        self.assertEqual(warning["observed"], 4)
        self.assertEqual(warning["threshold"], 4)
        self.assertEqual(warning["classification"], "review_heuristic")
        self.assertEqual(at_threshold["total"], sum(at_threshold["violations"].values()))

    def test_compliant_legal_analysis_does_not_trigger_density_warning(self):
        text = (
            "The right was clearly established by Smith v. Jones, 501 F.3d 101. "
            "That case required materially similar facts."
        )

        report = self.lint_artifact(text)

        self.assertEqual(report["total"], 0)
        self.assertEqual(report["warnings"], [])

    def test_quoted_rhetoric_is_not_automatically_called_accurate(self):
        report = self.lint_artifact('The brief called the delay "unbearably long."')

        self.assertEqual(report["findings"][0]["classification"], "unexempted_violation")
        self.assertNotIn(
            "accurate_quotation",
            {item.get("classification") for item in report["findings"]},
        )

    def test_public_cli_uses_stdin_artifact_and_parseable_json(self):
        script = Path(__file__).with_name("draft_lint.py")

        result = subprocess.run(
            [sys.executable, str(script)],
            input="The delay was unbearably long.",
            text=True,
            capture_output=True,
            check=True,
        )

        report = json.loads(result.stdout)
        self.assertIn("findings", report)
        self.assertEqual(report["findings"][0]["artifact"], "<stdin>")

    def test_public_cli_uses_filing_root_and_relative_target(self):
        script = Path(__file__).with_name("draft_lint.py")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory, "draft.md")
            target.write_text("The delay was unbearably long.", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--filing-root",
                    directory,
                    "--filing-target",
                    "draft.md",
                ],
                text=True,
                capture_output=True,
                check=True,
            )
        report = json.loads(result.stdout)
        self.assertEqual(report["findings"][0]["artifact"], "draft.md")


if __name__ == "__main__":
    unittest.main()
