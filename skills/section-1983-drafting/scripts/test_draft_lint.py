import unittest

from draft_lint import lint


class LintTest(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()
