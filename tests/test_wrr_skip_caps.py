import unittest
from types import SimpleNamespace

from scripts.analyze_wrr_skip_caps import skip_cap_band, skip_cap_markdown_row, summarize


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
            skip_cap_formula="printed",
        )
        rows = [
            row("A", 100, 95, 0, True, True, "cap_le_observed_max_skip"),
            row("B", 600, 600, 2, True, True, "cap_le_1000"),
            row("A", 5000, 5000, 0, False, False, "cap_gt_1000"),
        ]

        summary = summarize(rows, args)

        self.assertEqual(summary["rows"], 3)
        self.assertEqual(summary["unique_normalized_terms"], 2)
        self.assertEqual(summary["cap_le_observed_max_skip"], 1)
        self.assertEqual(summary["cap_le_1000"], 1)
        self.assertEqual(summary["cap_gt_1000"], 1)
        self.assertEqual(summary["program_cap_lt_printed"], 1)
        self.assertEqual(summary["program_cap_eq_printed"], 2)
        self.assertEqual(summary["program_target_unreached_rows"], 1)
        self.assertEqual(summary["target_unreached_rows"], 1)
        self.assertEqual(summary["observed_zero_rows"], 2)

    def test_markdown_row_displays_transliteration_and_english_gloss(self) -> None:
        rendered = skip_cap_markdown_row(
            {
                "term_id": "rashi_h",
                "concept": "Rashi",
                "normalized_term": "רשי",
                "normalized_length": 3,
                "observed_hits": 4,
                "skip_cap": 250,
                "program_skip_cap": 248,
                "expected_at_skip_cap": 10.0,
            }
        )

        self.assertIn("`רשי` (rshy; English: Rashi)", rendered)
        self.assertIn("| 250 | 248 | 10.0 |", rendered)


def row(
    term: str,
    cap: int,
    program_cap: int,
    observed_hits: int,
    target_reached: bool,
    program_target_reached: bool,
    band: str,
) -> dict[str, object]:
    return {
        "normalized_term": term,
        "skip_cap": cap,
        "printed_skip_cap": cap,
        "program_skip_cap": program_cap,
        "observed_hits": observed_hits,
        "target_reached": target_reached,
        "program_target_reached": program_target_reached,
        "skip_cap_band": band,
    }


if __name__ == "__main__":
    unittest.main()
