import unittest

from els.gematria import hebrew_number, hebrew_year_additive, hebrew_year_compact


class GematriaTests(unittest.TestCase):
    def test_hebrew_number_special_cases(self) -> None:
        self.assertEqual(hebrew_number(15), "טו")
        self.assertEqual(hebrew_number(16), "טז")
        self.assertEqual(hebrew_number(785), "תשפה")

    def test_year_encodings(self) -> None:
        self.assertEqual(hebrew_year_compact(2024), "בכד")
        self.assertEqual(hebrew_year_additive(2024), "תתתתתכד")


if __name__ == "__main__":
    unittest.main()
