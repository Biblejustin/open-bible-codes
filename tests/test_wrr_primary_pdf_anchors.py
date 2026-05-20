import unittest

from scripts.analyze_wrr_primary_pdf_anchors import (
    ANCHORS,
    Anchor,
    build_anchor_rows,
    find_page,
    markdown_cell,
    normalize_space,
)


class WrrPrimaryPdfAnchorTests(unittest.TestCase):
    def test_find_page_normalizes_spacing_and_case(self) -> None:
        pages = ["first page", "The Koren\ntext   is precisely here"]
        self.assertEqual(find_page(pages, "koren text is precisely"), 2)
        self.assertIsNone(find_page(pages, "missing anchor"))

    def test_build_anchor_rows_marks_found_and_missing(self) -> None:
        rows = build_anchor_rows(
            ["sample has 298 word pairs", "other page"],
            (
                Anchor("sample", "pair_universe", "298 word pairs", "sample read"),
                Anchor("missing", "pair_universe", "not present", "missing read"),
            ),
        )

        self.assertEqual(rows[0]["status"], "found")
        self.assertEqual(rows[0]["page"], "1")
        self.assertEqual(rows[1]["status"], "missing")
        self.assertEqual(rows[1]["page"], "")

    def test_default_anchor_ids_cover_current_method_status_needs(self) -> None:
        anchor_ids = {anchor.anchor_id for anchor in ANCHORS}
        self.assertIn("sample_298_word_pairs", anchor_ids)
        self.assertIn("koren_text", anchor_ids)
        self.assertIn("permutation_count", anchor_ids)
        self.assertIn("expected_els_target", anchor_ids)

    def test_markdown_cell_escapes_pipes(self) -> None:
        self.assertEqual(markdown_cell("a|b\nc"), "a\\|b c")

    def test_normalize_space_collapses_whitespace(self) -> None:
        self.assertEqual(normalize_space("a\n  b\tc"), "a b c")


if __name__ == "__main__":
    unittest.main()
