import csv
import tempfile
import unittest
from pathlib import Path

import pytest

from els.report_db import import_csv_table
from scripts.summarize_dynamic_span_hits import (
    build_version_presence_rows,
    display_center_word,
    display_top_center_words,
    summarize_hit_file,
    summarize_hit_table,
)


class DynamicSpanHitSummaryTests(unittest.TestCase):
    def test_summarize_hit_file_keeps_all_hits_and_flags_exact_center(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hits.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "corpus",
                        "corpus_language",
                        "term_id",
                        "concept",
                        "category",
                        "term_language",
                        "term",
                        "normalized_term",
                        "mode",
                        "count_row_hit_count",
                        "skip",
                        "direction",
                        "span_letters",
                        "start_ref",
                        "center_ref",
                        "end_ref",
                        "center_word",
                        "center_normalized_word",
                    ],
                )
                writer.writeheader()
                writer.writerow(hit_row("TR_NT", "dyn_sample_g", "λογος", "λογος", "forward", 2, "MAT 1:1"))
                writer.writerow(hit_row("TR_NT", "dyn_sample_g", "λογος", "και", "backward", -3, "MAT 1:2"))

            summary, examples = summarize_hit_file(path, low_count_threshold=5, examples_per_group=5)

        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0]["exported_hits"], 2)
        self.assertEqual(summary[0]["forward_hits"], 1)
        self.assertEqual(summary[0]["backward_hits"], 1)
        self.assertEqual(summary[0]["exact_center_word_hits"], 1)
        self.assertEqual(summary[0]["distinct_center_refs"], 2)
        self.assertIn("λογος=1", summary[0]["top_center_words"])
        self.assertEqual({row["example_type"] for row in examples}, {"exact_center_word", "low_count"})

    def test_summarize_hit_table_matches_csv_summary(self) -> None:
        pytest.importorskip("duckdb")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hits.csv"
            db = Path(tmp) / "reports" / "db.duckdb"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "corpus",
                        "corpus_language",
                        "term_id",
                        "concept",
                        "category",
                        "term_language",
                        "term",
                        "normalized_term",
                        "mode",
                        "count_row_hit_count",
                        "skip",
                        "direction",
                        "span_letters",
                        "start_ref",
                        "center_ref",
                        "end_ref",
                        "center_word",
                        "center_normalized_word",
                    ],
                )
                writer.writeheader()
                writer.writerow(hit_row("TR_NT", "dyn_sample_g", "λογος", "λογος", "forward", 2, "MAT 1:1"))
                writer.writerow(hit_row("TR_NT", "dyn_sample_g", "λογος", "και", "backward", -3, "MAT 1:2"))
            import_csv_table(db_path=db, csv_path=path, table_name="hits")

            csv_summary, csv_examples = summarize_hit_file(path, low_count_threshold=5, examples_per_group=5)
            db_summary, db_examples = summarize_hit_table(
                db_path=db,
                table_name="hits",
                source_path=path,
                low_count_threshold=5,
                examples_per_group=5,
            )

        self.assertEqual(db_summary, csv_summary)
        self.assertEqual(db_examples, csv_examples)

    def test_build_version_presence_rows_separates_bible_and_controls(self) -> None:
        rows = [
            count_row("TR_NT", "dyn_sample_g", 1),
            count_row("SBLGNT", "dyn_sample_g", 0),
            count_row("GRC_PERSEUS_ILIAD", "dyn_sample_g", 2),
            count_row("GRC_PERSEUS_ODYSSEY", "dyn_sample_g", 0),
            count_row("TR_NT", "dyn_other_g", 0),
        ]

        presence = build_version_presence_rows(rows, mode="full-span")
        by_term = {row["term_id"]: row for row in presence}

        self.assertEqual(by_term["dyn_sample_g"]["bible_present_corpora"], "TR_NT=1")
        self.assertEqual(by_term["dyn_sample_g"]["control_present_corpora"], "GRC_PERSEUS_ILIAD=2")
        self.assertEqual(by_term["dyn_sample_g"]["bible_zero_corpora"], "SBLGNT")
        self.assertEqual(by_term["dyn_sample_g"]["control_zero_corpora"], "GRC_PERSEUS_ODYSSEY")
        self.assertEqual(by_term["dyn_other_g"]["bible_max_hit_count"], "0")

    def test_display_center_word_annotates_exact_script_match_with_concept(self) -> None:
        row = hit_row("TR_NT", "dyn_sample_g", "λογος", "λόγος", "forward", 2, "MAT 1:1")
        row["concept"] = "Word"
        row["center_normalized_word"] = "λογος"

        self.assertEqual(display_center_word(row), "`λόγος` (logos; English: Word)")

    def test_display_top_center_words_annotates_script_values_only(self) -> None:
        self.assertEqual(
            display_top_center_words("λογος=2; and=1"),
            "`λογος` (logos; English: Word)=2; and=1",
        )


def hit_row(
    corpus: str,
    term_id: str,
    normalized_term: str,
    center_word: str,
    direction: str,
    skip: int,
    center_ref: str,
) -> dict[str, str]:
    return {
        "corpus": corpus,
        "corpus_language": "greek",
        "term_id": term_id,
        "concept": "Sample",
        "category": "test",
        "term_language": "greek",
        "term": normalized_term,
        "normalized_term": normalized_term,
        "mode": "full-span",
        "count_row_hit_count": "2",
        "skip": str(skip),
        "direction": direction,
        "span_letters": "10",
        "start_ref": "MAT 1:1",
        "center_ref": center_ref,
        "end_ref": "REV 1:1",
        "center_word": center_word,
        "center_normalized_word": center_word,
    }


def count_row(corpus: str, term_id: str, hit_count: int) -> dict[str, str]:
    return {
        "corpus": corpus,
        "term_id": term_id,
        "concept": "Sample",
        "term_language": "greek",
        "term": "λογος",
        "normalized_term": "λογος",
        "mode": "full-span",
        "hit_count": str(hit_count),
    }


if __name__ == "__main__":
    unittest.main()
