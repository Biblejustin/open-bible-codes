import csv
import tempfile
import unittest
from pathlib import Path

from scripts.analyze_synthetic_pair_baselines import (
    comparison_rows,
    build_parser,
    synthetic_read,
)


class SyntheticPairBaselinesTests(unittest.TestCase):
    def test_parser_accepts_hit_jobs(self) -> None:
        args = build_parser().parse_args(["--hit-jobs", "2", "--corpus-label", "UHB"])

        self.assertEqual(args.hit_jobs, 2)
        self.assertEqual(args.corpus_label, "UHB")

    def test_synthetic_read_flags_sampled_exceedance(self) -> None:
        self.assertEqual(
            synthetic_read(1, 0),
            "synthetic samples can match or exceed target density",
        )
        self.assertEqual(
            synthetic_read(0, 0),
            "target exceeds sampled synthetic density",
        )

    def test_comparison_rows_filters_by_corpus_label(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "pair_baselines.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "pair_label",
                        "corpus",
                        "observed_pairs_within_gap",
                        "observed_overlap_pairs",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "pair_label": "Gog/Magog",
                        "corpus": "MT_WLC",
                        "observed_pairs_within_gap": "99",
                        "observed_overlap_pairs": "9",
                    }
                )
                writer.writerow(
                    {
                        "pair_label": "Gog/Magog",
                        "corpus": "UHB",
                        "observed_pairs_within_gap": "1",
                        "observed_overlap_pairs": "0",
                    }
                )

            rows = comparison_rows(
                [{"pairs_within_gap": 2, "overlap_pairs": 0}],
                path,
                "UHB",
            )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["target_pairs_within_gap"], 1)


if __name__ == "__main__":
    unittest.main()
