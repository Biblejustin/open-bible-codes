import unittest

from els.gematria import (
    greek_standard_value,
    hebrew_number,
    hebrew_standard_value,
    hebrew_year_additive,
    hebrew_year_compact,
    standard_gematria_value,
)


class GematriaTests(unittest.TestCase):
    def test_hebrew_number_special_cases(self) -> None:
        self.assertEqual(hebrew_number(15), "טו")
        self.assertEqual(hebrew_number(16), "טז")
        self.assertEqual(hebrew_number(785), "תשפה")

    def test_year_encodings(self) -> None:
        self.assertEqual(hebrew_year_compact(2024), "בכד")
        self.assertEqual(hebrew_year_additive(2024), "תתתתתכד")

    def test_standard_hebrew_gematria(self) -> None:
        self.assertEqual(hebrew_standard_value("יהוה"), 26)
        self.assertEqual(hebrew_standard_value("משיח"), 358)
        self.assertEqual(hebrew_standard_value("מנצפך"), 280)

    def test_standard_greek_isopsephy(self) -> None:
        self.assertEqual(greek_standard_value("ιησους"), 888)
        self.assertEqual(greek_standard_value("Ἰησοῦς"), 888)
        self.assertEqual(greek_standard_value("χριστος"), 1480)

    def test_standard_gematria_value_detects_supported_scripts(self) -> None:
        self.assertEqual(standard_gematria_value("יהוה"), ("hebrew_standard", 26))
        self.assertEqual(standard_gematria_value("ιησους"), ("greek_standard", 888))
        self.assertEqual(standard_gematria_value("jesus", "english"), ("", 0))


if __name__ == "__main__":
    unittest.main()
