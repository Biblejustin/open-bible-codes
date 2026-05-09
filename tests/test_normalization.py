import unittest

from els.normalization import (
    normalize_english,
    normalize_greek,
    normalize_hebrew,
    normalize_michigan,
)


class NormalizationTests(unittest.TestCase):
    def test_hebrew_strips_marks_and_folds_finals(self) -> None:
        self.assertEqual(normalize_hebrew("בְּרֵאשִׁית"), "בראשית")
        self.assertEqual(normalize_hebrew("מלך"), "מלכ")

    def test_hebrew_can_keep_finals(self) -> None:
        self.assertEqual(normalize_hebrew("מלך", keep_final_forms=True), "מלך")

    def test_greek_strips_marks_and_folds_sigma(self) -> None:
        self.assertEqual(normalize_greek("Ἰησοῦς"), "ιησουσ")
        self.assertEqual(normalize_greek("Θεός"), "θεοσ")

    def test_michigan_keeps_transliteration_or_converts_hebrew(self) -> None:
        self.assertEqual(normalize_michigan("BR)$YT BR)"), "BR)$YTBR)")
        self.assertEqual(normalize_michigan("תורה"), "TWRH")

    def test_michigan_accepts_modified_wrr_source_letters(self) -> None:
        self.assertEqual(normalize_michigan("RBYABRHM"), "RBY)BRHM")
        self.assertEqual(normalize_michigan("B@LHA$KWL"), "B(LH)$KWL")
        self.assertEqual(normalize_michigan("M#H&M"), "M$H$M")

    def test_english_keeps_letters_only(self) -> None:
        self.assertEqual(normalize_english("King James Version, 1769"), "kingjamesversion")
        self.assertEqual(normalize_english("Café déjà vu"), "cafedejavu")


if __name__ == "__main__":
    unittest.main()
