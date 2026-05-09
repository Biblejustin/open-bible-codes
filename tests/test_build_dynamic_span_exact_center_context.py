import unittest

from els.demo import demo_corpus
from scripts.build_dynamic_span_exact_center_context import (
    clean_text,
    context_row,
    reproduce_command,
    select_queue_rows,
)


class BuildDynamicSpanExactCenterContextTests(unittest.TestCase):
    def test_context_row_includes_center_word_window_and_verse_text(self) -> None:
        corpus = demo_corpus()
        row = {
            "rank": "1",
            "corpus_class": "bible",
            "corpus": "KJV",
            "term_id": "dyn_beta_e",
            "normalized_term": "beta",
            "center_ref": "Demo 1:1",
            "center_source": "demo",
            "center_word_index": "2",
            "center_word": "beta",
            "exact_center_paths": "2",
            "review_bucket": "bible low-count review",
            "example_skip": "3",
            "example_direction": "forward",
            "example_start_ref": "Demo 1:1",
            "example_end_ref": "Demo 1:1",
            "example_start_offset": "0",
            "example_center_offset": "6",
            "example_end_offset": "12",
        }

        output = context_row(row, corpus)

        self.assertEqual(output["center_verse_text"], "alpha beta gamma")
        self.assertEqual(output["start_verse_text"], "alpha beta gamma")
        self.assertEqual(output["end_verse_text"], "alpha beta gamma")
        self.assertEqual(output["center_word_context"], "alpha [beta] gamma")

    def test_clean_text_collapses_whitespace_and_truncates(self) -> None:
        self.assertEqual(clean_text("alpha\n\n beta\tgamma", 100), "alpha beta gamma")
        self.assertEqual(clean_text("abcdef", 5), "ab...")

    def test_select_queue_rows_limits_by_class(self) -> None:
        rows = [
            {"corpus_class": "bible", "rank": "1"},
            {"corpus_class": "bible", "rank": "2"},
            {"corpus_class": "control", "rank": "3"},
            {"corpus_class": "control", "rank": "4"},
        ]
        args = type("Args", (), {"bible_limit": 1, "control_limit": 1})()

        selected = select_queue_rows(rows, args)

        self.assertEqual([row["rank"] for row in selected], ["1", "3"])

    def test_reproduce_command_includes_selection_limits(self) -> None:
        args = type(
            "Args",
            (),
            {
                "queue": "queue.csv",
                "out": "context.csv",
                "markdown_out": "context.md",
                "manifest_out": "context.manifest.json",
                "bible_limit": 453,
                "control_limit": 84,
                "markdown_row_limit": 120,
                "text_limit": 2000,
            },
        )()

        command = reproduce_command(args)

        self.assertIn("--bible-limit 453", command)
        self.assertIn("--control-limit 84", command)
        self.assertIn("--markdown-row-limit 120", command)
        self.assertIn("--text-limit 2000", command)


if __name__ == "__main__":
    unittest.main()
