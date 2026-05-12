import unittest

from scripts.build_broad_surface_followup_report import (
    context_sort_key,
    exact_hit_row,
    is_true,
    markdown_cell,
)


class BroadSurfaceFollowupReportTests(unittest.TestCase):
    def test_is_true_only_accepts_exported_true_value(self) -> None:
        self.assertTrue(is_true("True"))
        self.assertFalse(is_true("true"))
        self.assertFalse(is_true(""))

    def test_context_sort_key_prioritizes_exact_center_word(self) -> None:
        exact_word = {
            "exact_center_word_hits": "1",
            "exact_center_hits": "1",
            "context_hit_count": "1",
            "hit_count": "1",
        }
        broad_context = {
            "exact_center_word_hits": "0",
            "exact_center_hits": "10",
            "context_hit_count": "20",
            "hit_count": "20",
        }

        self.assertGreater(context_sort_key(exact_word), context_sort_key(broad_context))

    def test_exact_hit_row_includes_surface_word_and_path(self) -> None:
        row = {
            "term_id": "jesus_g",
            "normalized_term": "ιησουσ",
            "concept": "Jesus",
            "corpus": "SBLGNT",
            "skip": "-141",
            "center_ref": "Heb 13:8",
            "center_word": "Ἰησοῦς",
            "start_ref": "Heb 13:12",
            "end_ref": "Heb 13:3",
            "span_exact_refs": "Heb 13:8",
            "span_same_category_refs": "",
        }

        text = exact_hit_row(row)

        self.assertIn("`Ἰησοῦς`", text)
        self.assertIn("Heb 13:12 -> Heb 13:3", text)

    def test_exact_hit_row_adds_center_verse_text_when_available(self) -> None:
        row = {
            "term_id": "lord_g",
            "normalized_term": "κυριοσ",
            "concept": "Lord",
            "corpus": "LXX",
            "skip": "277",
            "center_ref": "PSA 117:24",
            "center_word": "Κύριος",
            "start_ref": "PSA 117:12",
            "end_ref": "PSA 118:6",
            "span_exact_refs": "PSA 117:24",
            "span_same_category_refs": "",
        }

        text = exact_hit_row(row, {("LXX", "PSA 117:24"): "This is the day of the Lord"})

        self.assertIn("This is the day of the Lord", text)

    def test_markdown_cell_escapes_pipes(self) -> None:
        self.assertEqual(markdown_cell("left | right"), "left \\| right")


if __name__ == "__main__":
    unittest.main()
