import unittest

from scripts.analyze_wrr_primary_table2_anchors import (
    TABLE2_PERSONALITIES,
    Table2Personality,
    build_anchor_rows,
    find_table2_page,
    fragments_found,
    markdown_cell,
    normalize_space,
    slug,
)


class WrrPrimaryTable2AnchorTests(unittest.TestCase):
    def test_find_table2_page_uses_table_heading(self) -> None:
        pages = ["TABLE 1 first list", "TABLE 2\nThe second list of personalities"]

        self.assertEqual(find_table2_page(pages), 2)

    def test_build_anchor_rows_checks_fragments_on_table2_page(self) -> None:
        rows = build_anchor_rows(
            ["TABLE 2 The second list of personalities Rabbi Moshe Zacuto"],
            (
                Table2Personality(27, "Rabbi Moshe Zacuto", ("Rabbi Moshe", "Zacuto")),
                Table2Personality(28, "Rabbi Moshe Margalith", ("Rabbi Moshe Margalith",)),
            ),
        )

        self.assertEqual(rows[0]["status"], "found")
        self.assertEqual(rows[0]["page"], "1")
        self.assertEqual(rows[1]["status"], "missing")

    def test_fragments_found_normalizes_spacing_and_case(self) -> None:
        self.assertTrue(fragments_found("Rabbi\nMoshe   Zacuto", ("rabbi moshe", "zacuto")))
        self.assertFalse(fragments_found("Rabbi Moshe", ("Zacuto",)))

    def test_default_personality_rows_cover_second_list_count(self) -> None:
        self.assertEqual(len(TABLE2_PERSONALITIES), 32)
        names = {row.english_name for row in TABLE2_PERSONALITIES}
        self.assertIn("Rabbi Moshe Zacuto", names)
        self.assertIn("Rabbi Shelomo of Cheim", names)

    def test_slug_is_stable_for_anchor_ids(self) -> None:
        self.assertEqual(slug("Rabbi Avraham Av-Beit-Din of Narbonne"), "rabbi_avraham_av_beit_din_of_narbonne")

    def test_markdown_cell_escapes_pipes(self) -> None:
        self.assertEqual(markdown_cell("a|b\nc"), "a\\|b c")

    def test_normalize_space_collapses_whitespace(self) -> None:
        self.assertEqual(normalize_space("a\n  b\tc"), "a b c")


if __name__ == "__main__":
    unittest.main()
