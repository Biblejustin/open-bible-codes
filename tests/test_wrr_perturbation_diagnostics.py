import argparse
import unittest

from scripts.analyze_wrr_perturbation_diagnostics import (
    diagnostic_read,
    display_boundary_term,
    exact_perturbation_match_count,
    offsets_in_bounds,
    sample_cap,
    sample_label,
    summarize,
    valid_perturbation_count,
)


class WrrPerturbationDiagnosticsTests(unittest.TestCase):
    def test_offsets_in_bounds_rejects_boundary_crossing(self) -> None:
        self.assertTrue(offsets_in_bounds((0, 4, 9), 10))
        self.assertFalse(offsets_in_bounds((-1, 4, 9), 10))
        self.assertFalse(offsets_in_bounds((0, 4, 10), 10))

    def test_valid_perturbation_count_counts_in_bound_triples(self) -> None:
        triples = ((0, 0, 0), (5, 0, 0), (-5, 0, 0))

        count = valid_perturbation_count(
            start=2,
            skip=2,
            word_length=4,
            text_length=20,
            triples=triples,
        )

        self.assertEqual(count, 2)

    def test_sample_cap_zero_means_all_hits(self) -> None:
        self.assertIsNone(sample_cap(0))
        self.assertIsNone(sample_cap(-1))
        self.assertEqual(sample_cap(20), 20)
        self.assertEqual(sample_label(0), "all")
        self.assertEqual(sample_label(20), 20)

    def test_exact_perturbation_match_count_checks_letters(self) -> None:
        triples = ((0, 0, 0), (1, 0, 0), (-5, 0, 0))

        count = exact_perturbation_match_count(
            text="AXXBXCXD",
            word="ABCD",
            start=0,
            skip=2,
            triples=triples,
        )

        self.assertEqual(count, 1)

    def test_diagnostic_read_reports_boundary_states(self) -> None:
        self.assertEqual(diagnostic_read([], [], 0, 0), "no checked hits")
        self.assertEqual(
            diagnostic_read([9], [9], 0, 0),
            "checked hits include fewer than 10 in-bound perturbations",
        )
        self.assertEqual(
            diagnostic_read([10], [9], 0, 0),
            "checked hits include fewer than 10 exact perturbation matches",
        )
        self.assertEqual(
            diagnostic_read([10], [10], 0, 0),
            "checked perturbation exact-match ok",
        )
        self.assertEqual(diagnostic_read([10], [10], 1, 0), "ordinary hit boundary failure")
        self.assertEqual(diagnostic_read([10], [10], 0, 1), "ordinary hit exact-match failure")

    def test_summarize_counts_boundary_limited_rows(self) -> None:
        args = argparse.Namespace(search_max_skip=250, sample_hits_per_query=20)
        rows = [
            row("a", "ABC", 2, 9, 12, 1, 3, 0, 0),
            row("b", "DEF", 0, "", "", "", "", 0, 0),
            row("c", "ABC", 1, 20, 30, 12, 14, 1, 2),
        ]

        summary = summarize(rows, args)

        self.assertEqual(summary["rows"], 3)
        self.assertEqual(summary["unique_normalized_terms"], 2)
        self.assertEqual(summary["rows_with_hits"], 2)
        self.assertEqual(summary["rows_without_hits"], 1)
        self.assertEqual(summary["sampled_hits"], 3)
        self.assertEqual(summary["rows_with_sample_under_10_valid"], 1)
        self.assertEqual(summary["rows_with_sample_under_10_exact_matches"], 1)
        self.assertEqual(summary["min_in_bounds_perturbations"], 9)
        self.assertEqual(summary["max_in_bounds_perturbations"], 20)
        self.assertEqual(summary["min_exact_perturbation_matches"], 1)
        self.assertEqual(summary["max_exact_perturbation_matches"], 12)
        self.assertEqual(summary["ordinary_in_bounds_failures"], 1)
        self.assertEqual(summary["ordinary_exact_match_failures"], 2)

    def test_boundary_term_displays_transliteration_and_english_gloss(self) -> None:
        rendered = display_boundary_term(
            {
                "term_id": "rashi_h",
                "concept": "Rashi",
                "normalized_term": "רשי",
            }
        )

        self.assertEqual(rendered, "`rashi_h` `רשי` (rshy; English: Rashi)")


def row(
    term_id: str,
    normalized: str,
    sampled_hits: int,
    min_valid: object,
    max_valid: object,
    min_exact: object,
    max_exact: object,
    failures: int,
    exact_failures: int,
) -> dict[str, object]:
    return {
        "term_id": term_id,
        "normalized_term": normalized,
        "sampled_hits": sampled_hits,
        "min_in_bounds_perturbations": min_valid,
        "max_in_bounds_perturbations": max_valid,
        "min_exact_perturbation_matches": min_exact,
        "max_exact_perturbation_matches": max_exact,
        "ordinary_in_bounds_failures": failures,
        "ordinary_exact_match_failures": exact_failures,
    }


if __name__ == "__main__":
    unittest.main()
