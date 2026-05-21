import unittest

from els.term_display import display_center, display_term, normalized_script_key


class TermDisplayTests(unittest.TestCase):
    def test_displays_known_greek_term_with_gloss(self) -> None:
        self.assertEqual(display_term("γωγ"), "`γωγ` (Gog; English: Gog)")

    def test_displays_common_greek_report_term_with_gloss(self) -> None:
        self.assertEqual(display_term("αιμα"), "`αιμα` (haima; English: blood)")
        self.assertEqual(display_term("σοφια"), "`σοφια` (sophia; English: wisdom)")
        self.assertEqual(display_term("τερας"), "`τερας` (teras; English: wonder)")
        self.assertEqual(display_term("τερασ"), "`τερασ` (teras; English: wonder)")
        self.assertEqual(display_term("Οὐδέποτε"), "`Οὐδέποτε` (oudepote; English: never)")
        self.assertEqual(display_term("δικαιώματα."), "`δικαιώματα.` (dikaiomata; English: ordinances)")
        self.assertEqual(display_term("καρδίαν"), "`καρδίαν` (kardian; English: heart)")
        self.assertEqual(display_term("ὑπεράνω"), "`ὑπεράνω` (uperano; English: above)")
        self.assertEqual(display_term("ελκη"), "`ελκη` (elke; English: boils/sores)")
        self.assertEqual(display_term("σπέρματος"), "`σπέρματος` (spermatos; English: seed/descendant)")
        self.assertEqual(display_term("ἡμέραις"), "`ἡμέραις` (hemerais; English: days)")
        self.assertEqual(display_term("θανάτου"), "`θανάτου` (thanatou; English: death)")
        self.assertEqual(display_term("αἵματι,"), "`αἵματι,` (haimati; English: blood)")
        self.assertEqual(display_term("Βαβυλῶνι"), "`Βαβυλῶνι` (babuloni; English: Babylon)")
        self.assertEqual(display_term("βούλομαι"), "`βούλομαι` (boulomai; English: I want)")
        self.assertEqual(display_term("Μαριάμ"), "`Μαριάμ` (mariam; English: Mary)")
        self.assertEqual(display_term("τοὺς"), "`τοὺς` (tous; English: the/those)")
        self.assertEqual(display_term("ἀποκριθεὶς"), "`ἀποκριθεὶς` (apokritheis; English: having answered)")
        self.assertEqual(display_term("ζωήν"), "`ζωήν` (zoen; English: life)")
        self.assertEqual(display_term("Φαρισαῖος"), "`Φαρισαῖος` (pharisaios; English: Pharisee)")
        self.assertEqual(display_term("ὑμῖν"), "`ὑμῖν` (umin; English: to you)")
        self.assertEqual(display_term("εἰσέλθῃ"), "`εἰσέλθῃ` (eiselthe; English: enter)")
        self.assertEqual(display_term("τὴν"), "`τὴν` (ten; English: the)")
        self.assertEqual(display_term("παιδίον"), "`παιδίον` (paidion; English: child)")
        self.assertEqual(display_term("οὖν"), "`οὖν` (oun; English: therefore)")
        self.assertEqual(display_term("παράκλησις"), "`παράκλησις` (paraklesis; English: comfort/encouragement)")
        self.assertEqual(display_term("Καίσαρος"), "`Καίσαρος` (kaisaros; English: Caesar)")
        self.assertEqual(display_term("ἔργα"), "`ἔργα` (erga; English: works)")
        self.assertEqual(display_term("οἴδαμεν"), "`οἴδαμεν` (oidamen; English: we know)")

    def test_displays_common_hebrew_report_term_with_gloss(self) -> None:
        self.assertEqual(display_term("בבל"), "`בבל` (Bavel; English: Babylon)")
        self.assertEqual(display_term("יעקב"), "`יעקב` (Yaakov; English: Jacob)")
        self.assertEqual(display_term("דבר"), "`דבר` (davar; English: word/matter)")
        self.assertEqual(display_term("חזון"), "`חזון` (chazon; English: vision)")
        self.assertEqual(display_term("דריוש"), "`דריוש` (Daryavesh; English: Darius)")
        self.assertEqual(display_term("שטה"), "`שטה` (shittah; English: acacia)")
        self.assertEqual(display_term("ויקמ"), "`ויקמ` (vayaqom; English: and he arose)")
        self.assertEqual(display_term("מצרימ"), "`מצרימ` (Mitzrayim; English: Egypt)")
        self.assertEqual(display_term("איש"), "`איש` (ish; English: man)")
        self.assertEqual(display_term("בתוכ"), "`בתוכ` (betokh; English: in the midst)")
        self.assertEqual(display_term("דוד"), "`דוד` (David; English: David)")
        self.assertEqual(display_term("כסא"), "`כסא` (kisse; English: throne)")
        self.assertEqual(display_term("ציונ"), "`ציונ` (Tziyon; English: Zion)")
        self.assertEqual(display_term("פסח"), "`פסח` (Pesach; English: Passover)")
        self.assertEqual(display_term("מלכות"), "`מלכות` (malkhut; English: kingdom)")
        self.assertEqual(display_term("חבורה"), "`חבורה` (chabburah; English: stripe/wound)")
        self.assertEqual(display_term("שמע"), "`שמע` (shema; English: hear)")
        self.assertEqual(display_term("לחמ"), "`לחמ` (lechem; English: bread)")
        self.assertEqual(display_term("ארצ"), "`ארצ` (eretz; English: earth/land)")
        self.assertEqual(display_term("עבד"), "`עבד` (eved; English: servant)")
        self.assertEqual(display_term("קבר"), "`קבר` (qever; English: grave)")
        self.assertEqual(display_term("חותם"), "`חותם` (chotam; English: seal)")

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

    def test_ignores_script_text_as_english_override(self) -> None:
        self.assertEqual(
            display_term("ονομα", english="ὄνομα"),
            "`ονομα` (onoma; English: Name)",
        )
        self.assertEqual(
            display_term("יהוה", english="יהוה"),
            "`יהוה` (YHWH; English: YHWH)",
        )

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
