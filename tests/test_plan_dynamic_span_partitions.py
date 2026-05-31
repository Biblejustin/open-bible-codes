import argparse
import unittest
from pathlib import Path

from scripts.plan_dynamic_span_partitions import (
    build_partition_plan,
    estimate_partition_hits,
    partition_ranges,
    select_dense_rows,
)


class DynamicSpanPartitionPlanTests(unittest.TestCase):
    def test_partition_ranges_cover_skip_span_without_overlap(self) -> None:
        self.assertEqual(partition_ranges(2, 11, 3), [(2, 4), (5, 7), (8, 11)])
        self.assertEqual(partition_ranges(2, 4, 10), [(2, 2), (3, 3), (4, 4)])
        self.assertEqual(partition_ranges(5, 4, 2), [])

    def test_estimate_partition_hits_uses_skip_span_width(self) -> None:
        self.assertEqual(estimate_partition_hits(100, 1, 10, 1, 5), 50)
        self.assertEqual(estimate_partition_hits(101, 1, 10, 1, 5), 51)

    def test_select_dense_rows_filters_mode_terms_and_corpora(self) -> None:
        rows = [
            count_row("TR_NT", "keep", "full-span", 51),
            count_row("TR_NT", "small", "full-span", 50),
            count_row("TR_NT", "wrong_mode", "letters-per-term", 100),
            count_row("LXX", "keep", "full-span", 60),
        ]
        args = argparse.Namespace(
            mode=["full-span"],
            term_id=["keep"],
            corpus_label=["TR_NT"],
            dense_threshold=50,
        )

        selected = select_dense_rows(rows, args)

        self.assertEqual([row["term_id"] for row in selected], ["keep"])
        self.assertEqual([row["corpus"] for row in selected], ["TR_NT"])

    def test_build_partition_plan_emits_export_commands(self) -> None:
        args = argparse.Namespace(
            target_hits_per_partition=100,
            partition_dir=Path("reports/dynamic_skip_focus/partitions"),
        )

        plan = build_partition_plan([count_row("TR_NT", "dense", "full-span", 250)], args)

        self.assertEqual(len(plan), 3)
        self.assertEqual([row["min_abs_skip"] for row in plan], ["2", "5", "8"])
        self.assertEqual([row["max_abs_skip"] for row in plan], ["4", "7", "10"])
        self.assertIn("--include-dense", plan[0]["export_command"])
        self.assertIn("--max-abs-skip 4", plan[0]["export_command"])
        self.assertIn("--max-export-hits 0", plan[0]["export_command"])


def count_row(corpus: str, term_id: str, mode: str, hit_count: int) -> dict[str, str]:
    return {
        "corpus": corpus,
        "corpus_language": "greek",
        "term_id": term_id,
        "concept": "Sample",
        "category": "test",
        "term_language": "greek",
        "term": "λογος",
        "normalized_term": "λογος",
        "normalized_length": "5",
        "mode": mode,
        "direction": "both",
        "min_skip": "2",
        "effective_max_skip": "10",
        "hit_count": str(hit_count),
        "count_source_file": "reports/dynamic_skip_focus/sample.csv",
    }


if __name__ == "__main__":
    unittest.main()
