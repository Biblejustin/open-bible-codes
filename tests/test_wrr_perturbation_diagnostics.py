import argparse
import unittest

from scripts.analyze_wrr_perturbation_diagnostics import (
    diagnostic_read,
    display_boundary_term,
    offsets_in_bounds,
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

    def test_diagnostic_read_reports_boundary_states(self) -> None:
        self.assertEqual(diagnostic_read([], 0), "no sampled hits")
        self.assertEqual(diagnostic_read([9], 0), "sample includes fewer than 10 valid perturbations")
        self.assertEqual(diagnostic_read([10], 0), "sample perturbation boundary ok")
        self.assertEqual(diagnostic_read([10], 1), "ordinary hit boundary failure")

    def test_summarize_counts_boundary_limited_rows(self) -> None:
        args = argparse.Namespace(search_max_skip=250, sample_hits_per_query=20)
        rows = [
            row("a", "ABC", 2, 9, 12, 0),
            row("b", "DEF", 0, "", "", 0),
            row("c", "ABC", 1, 20, 30, 1),
        ]

        summary = summarize(rows, args)

        self.assertEqual(summary["rows"], 3)
        self.assertEqual(summary["unique_normalized_terms"], 2)
        self.assertEqual(summary["rows_with_hits"], 2)
        self.assertEqual(summary["rows_without_hits"], 1)
        self.assertEqual(summary["sampled_hits"], 3)
        self.assertEqual(summary["rows_with_sample_under_10_valid"], 1)
        self.assertEqual(summary["min_in_bounds_perturbations"], 9)
        self.assertEqual(summary["max_in_bounds_perturbations"], 20)
        self.assertEqual(summary["ordinary_in_bounds_failures"], 1)

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
    failures: int,
) -> dict[str, object]:
    return {
        "term_id": term_id,
        "normalized_term": normalized,
        "sampled_hits": sampled_hits,
        "min_in_bounds_perturbations": min_valid,
        "max_in_bounds_perturbations": max_valid,
        "ordinary_in_bounds_failures": failures,
    }


if __name__ == "__main__":
    unittest.main()
