import argparse
import os
import shutil
import unittest

from els.search import count_els_text
from scripts.export_dynamic_span_hits import (
    DEFAULT_BINARY,
    build_binary,
    run_hit_exporter,
    select_count_rows,
)


class DynamicSpanHitExportTests(unittest.TestCase):
    def test_select_count_rows_defers_zero_and_dense_rows(self) -> None:
        rows = [
            {
                "corpus": "TR_NT",
                "term_id": "zero",
                "mode": "full-span",
                "hit_count": "0",
            },
            {
                "corpus": "TR_NT",
                "term_id": "selected",
                "mode": "full-span",
                "hit_count": "10",
            },
            {
                "corpus": "TR_NT",
                "term_id": "dense",
                "mode": "full-span",
                "hit_count": "11",
            },
            {
                "corpus": "TR_NT",
                "term_id": "other_mode",
                "mode": "letters-per-term",
                "hit_count": "1",
            },
        ]
        args = argparse.Namespace(
            mode=["full-span"],
            term_id=[],
            corpus_label=[],
            include_zero=False,
            include_dense=False,
            max_count_row_hits=10,
        )

        selected, skipped = select_count_rows(rows, args)

        self.assertEqual([row["term_id"] for row in selected], ["selected"])
        self.assertEqual(
            [(row["term_id"], row["status"]) for row in skipped],
            [
                ("zero", "skipped_zero_hits"),
                ("dense", "skipped_above_hit_threshold"),
            ],
        )

    def test_compiled_hit_exporter_matches_reference_count_and_offsets(self) -> None:
        compiler = os.environ.get("CXX", "clang++")
        if shutil.which(compiler) is None:
            self.skipTest(f"{compiler} not available")

        text = "αβγγβα"
        query = "αβγ"
        terms = [{"term_id": "sample", "normalized_term": query}]
        binary = build_binary(DEFAULT_BINARY)

        rows = run_hit_exporter(
            binary,
            text,
            terms,
            min_skip=1,
            mode="full-span",
            direction="both",
            max_hits_per_term=100,
        )

        full_span_max = (len(text) - 1) // (len(query) - 1)
        self.assertEqual(
            len(rows),
            count_els_text(text, query, min_skip=1, max_skip=full_span_max, direction="both"),
        )
        self.assertEqual(
            {
                (int(row["skip"]), int(row["start_offset"]), int(row["end_offset"]))
                for row in rows
            },
            {
                (-1, 5, 3),
                (1, 0, 2),
            },
        )
        self.assertTrue(all(row["mode"] == "full-span" for row in rows))
        self.assertTrue(all(row["effective_max_skip"] == str(full_span_max) for row in rows))

    def test_compiled_hit_exporter_respects_max_skip_bound(self) -> None:
        compiler = os.environ.get("CXX", "clang++")
        if shutil.which(compiler) is None:
            self.skipTest(f"{compiler} not available")

        text = "αβγαδβδγ"
        query = "αβγ"
        terms = [{"term_id": "sample", "normalized_term": query}]
        binary = build_binary(DEFAULT_BINARY)

        rows = run_hit_exporter(
            binary,
            text,
            terms,
            min_skip=1,
            max_skip=1,
            mode="full-span",
            direction="forward",
            max_hits_per_term=100,
        )

        self.assertEqual(
            {
                (int(row["skip"]), int(row["start_offset"]), int(row["end_offset"]))
                for row in rows
            },
            {(1, 0, 2)},
        )
        self.assertTrue(all(row["effective_max_skip"] == "1" for row in rows))


if __name__ == "__main__":
    unittest.main()
