import unittest

from els.term_display import display_center, display_term, normalized_script_key


class TermDisplayTests(unittest.TestCase):
    def test_displays_known_greek_term_with_gloss(self) -> None:
        self.assertEqual(display_term("γωγ"), "`γωγ` (Gog; English: Gog)")

    def test_displays_common_greek_report_term_with_gloss(self) -> None:
        self.assertEqual(display_term("αιμα"), "`αιμα` (haima; English: blood)")
        self.assertEqual(display_term("τερας"), "`τερας` (teras; English: wonder)")
        self.assertEqual(display_term("τερασ"), "`τερασ` (teras; English: wonder)")

    def test_displays_common_hebrew_report_term_with_gloss(self) -> None:
        self.assertEqual(display_term("בבל"), "`בבל` (Bavel; English: Babylon)")

    def test_displays_core_hebrew_report_terms_with_glosses(self) -> None:
        self.assertEqual(display_term("יהוה"), "`יהוה` (YHWH; English: YHWH)")
        self.assertEqual(display_term("ישראל"), "`ישראל` (Yisrael; English: Israel)")

    def test_displays_recurring_hebrew_yhwh_compounds_with_glosses(self) -> None:
        self.assertEqual(display_term("ויהוה"), "`ויהוה` (ve-YHWH; English: and YHWH)")
        self.assertEqual(display_term("ליהוה"), "`ליהוה` (le-YHWH; English: to/for YHWH)")
        self.assertEqual(
            display_term("לביתיהוה"),
            "`לביתיהוה` (le-beit YHWH; English: to the house of YHWH)",
        )
        self.assertEqual(
            display_term("בריתיהוה"),
            "`בריתיהוה` (berit YHWH; English: covenant of YHWH)",
        )

    def test_displays_known_hebrew_term_with_diacritics(self) -> None:
        self.assertEqual(display_term("יֵשׁ֤וּעַ"), "`יֵשׁ֤וּעַ` (Yeshua; English: Yeshua/Jeshua)")
        self.assertEqual(display_term("יְהוָֽה׃"), "`יְהוָֽה׃` (YHWH; English: YHWH)")

    def test_displays_unambiguous_term_csv_concept_as_fallback_gloss(self) -> None:
        self.assertEqual(display_term("קאובוי"), "`קאובוי` (qwbwy; English: Cowboy)")
        self.assertEqual(display_term("καρχηδων"), "`καρχηδων` (karchedon; English: Carthage)")

    def test_displays_known_greek_term_with_breathing_and_final_sigma(self) -> None:
        self.assertEqual(display_term("Ἰησοῦς"), "`Ἰησοῦς` (Iesous; English: Jesus/Joshua)")

    def test_center_display_annotates_original_language_center_word(self) -> None:
        self.assertEqual(
            display_center("EZR 10:18", "יֵשׁ֤וּעַ"),
            "EZR 10:18 `יֵשׁ֤וּעַ` (Yeshua; English: Yeshua/Jeshua)",
        )

    def test_english_term_is_left_plain(self) -> None:
        self.assertEqual(display_term("jesus"), "`jesus`")

    def test_transliteration_override_handles_phrase_collision(self) -> None:
        self.assertEqual(
            display_term("δόξαν ὡς", english="glory as", transliteration="doxan hos"),
            "`δόξαν ὡς` (doxan hos; English: glory as)",
        )

    def test_normalized_script_key_removes_marks_and_spacing(self) -> None:
        self.assertEqual(normalized_script_key("יום יהוה"), "יוםיהוה")
        self.assertEqual(normalized_script_key("יְהוָֽה׃"), "יהוה")


if __name__ == "__main__":
    unittest.main()
