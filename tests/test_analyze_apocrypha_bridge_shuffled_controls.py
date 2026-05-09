import argparse
import tempfile
import unittest
from pathlib import Path

from scripts.analyze_apocrypha_bridge_shuffled_controls import (
    bridge_start_range,
    count_bridge_rows,
    manifest_args,
    read_existing_sample_rows,
    shuffled_text,
    summarize,
)


class ApocryphaBridgeShuffledControlsTests(unittest.TestCase):
    def test_shuffled_text_is_deterministic_and_preserves_letters(self) -> None:
        first = shuffled_text("aabbcc", 7)
        second = shuffled_text("aabbcc", 7)

        self.assertEqual(first, second)
        self.assertEqual(sorted(first), sorted("aabbcc"))

    def test_summarize_uses_add_one_tail_probability(self) -> None:
        args = argparse.Namespace(canonical_label="TEST")
        corpus = argparse.Namespace(text="abcdefgh")
        rows = [
            {"bridge_rows": 2},
            {"bridge_rows": 4},
            {"bridge_rows": 6},
        ]
        observed = [{}, {}, {}, {}]

        summary = {
            row["metric"]: row["value"]
            for row in summarize(
                rows,
                observed,
                corpus,
                {"canonical_prefix_letters": 4, "apocrypha_block_letters": 4},
                args,
            )
        }

        self.assertEqual(summary["observed_bridge_rows"], 4)
        self.assertEqual(summary["samples_ge_observed"], 2)
        self.assertEqual(summary["p_ge"], 0.75)

    def test_manifest_args_converts_term_paths(self) -> None:
        args = argparse.Namespace(terms=[], samples=5)

        self.assertEqual(manifest_args(args), {"terms": [], "samples": 5})

    def test_read_existing_sample_rows_normalizes_numbers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "sample_summary.csv"
            path.write_text(
                "\n".join(
                    [
                        "sample,seed,bridge_rows,terms_with_bridge_rows,canonical_to_apocrypha,apocrypha_to_canonical,multi_segment_bridge",
                        "2,20260510,51,22,26,25,0",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            rows = read_existing_sample_rows(path)

        self.assertEqual(
            rows,
            [
                {
                    "sample": 2,
                    "seed": 20260510,
                    "bridge_rows": 51,
                    "terms_with_bridge_rows": 22,
                    "canonical_to_apocrypha": 26,
                    "apocrypha_to_canonical": 25,
                    "multi_segment_bridge": 0,
                }
            ],
        )

    def test_bridge_start_range_limits_to_boundary_crossing_starts(self) -> None:
        self.assertEqual(
            list(bridge_start_range(6, 3, 2, 1, forward=True)),
            [2],
        )
        self.assertEqual(
            list(bridge_start_range(6, 3, 2, 1, forward=False)),
            [3],
        )

    def test_count_bridge_rows_counts_forward_and_backward_boundary_hits(self) -> None:
        args = argparse.Namespace(min_skip=1, max_skip=1, direction="both", jobs=1)

        total_by_type, term_by_type = count_bridge_rows(
            "abcxyz",
            {
                "cx": [{"term_id": "cx"}],
                "xc": [{"term_id": "xc"}],
            },
            {"canonical_prefix_letters": 3},
            args,
        )

        self.assertEqual(total_by_type["canonical_to_apocrypha"], 1)
        self.assertEqual(total_by_type["apocrypha_to_canonical"], 1)
        self.assertEqual(term_by_type["cx"]["canonical_to_apocrypha"], 1)
        self.assertEqual(term_by_type["xc"]["apocrypha_to_canonical"], 1)
