import unittest
from types import SimpleNamespace

from scripts.analyze_wrr_skip_caps import skip_cap_band, summarize


class WrrSkipCapsTests(unittest.TestCase):
    def test_skip_cap_band_tracks_observed_and_large_caps(self) -> None:
        args = SimpleNamespace(observed_max_skip=250)

        self.assertEqual(skip_cap_band(250, args), "cap_le_observed_max_skip")
        self.assertEqual(skip_cap_band(251, args), "cap_le_500")
        self.assertEqual(skip_cap_band(750, args), "cap_le_1000")
        self.assertEqual(skip_cap_band(1001, args), "cap_gt_1000")

    def test_summarize_counts_bands_and_zero_rows(self) -> None:
        args = SimpleNamespace(
            observed_max_skip=250,
            target_expected_hits=10.0,
            max_skip_limit=None,
        )
        rows = [
            row("A", 100, 0, True, "cap_le_observed_max_skip"),
            row("B", 600, 2, True, "cap_le_1000"),
            row("A", 5000, 0, False, "cap_gt_1000"),
        ]

        summary = summarize(rows, args)

        self.assertEqual(summary["rows"], 3)
        self.assertEqual(summary["unique_normalized_terms"], 2)
        self.assertEqual(summary["cap_le_observed_max_skip"], 1)
        self.assertEqual(summary["cap_le_1000"], 1)
        self.assertEqual(summary["cap_gt_1000"], 1)
        self.assertEqual(summary["target_unreached_rows"], 1)
        self.assertEqual(summary["observed_zero_rows"], 2)


def row(
    term: str,
    cap: int,
    observed_hits: int,
    target_reached: bool,
    band: str,
) -> dict[str, object]:
    return {
        "normalized_term": term,
        "skip_cap": cap,
        "observed_hits": observed_hits,
        "target_reached": target_reached,
        "skip_cap_band": band,
    }


if __name__ == "__main__":
    unittest.main()
