import argparse
import unittest

from els.wrr import WrrElsOccurrence
from scripts.analyze_wrr_corrected_distance import (
    PairTerm,
    PerturbedTermStats,
    build_corrected_distance_rows,
    collect_perturbed_occurrences_by_term,
    collect_pair_terms,
    select_pair_rows,
    shard_pair_rows,
    summarize,
)


class WrrCorrectedDistanceScriptTests(unittest.TestCase):
    def test_select_pair_rows_can_filter_to_candidate_lane(self) -> None:
        rows = [
            pair("p1", "app", "date", lane="length_5_8_smoke_candidate"),
            pair("p2", "app", "date", lane="excluded_by_appellation_min_length"),
        ]

        selected = select_pair_rows(rows, "length_5_8_smoke_candidate")

        self.assertEqual([row["pair_id"] for row in selected], ["p1"])
        self.assertEqual(select_pair_rows(rows, "all"), rows)

    def test_shard_pair_rows_splits_by_stable_position(self) -> None:
        rows = [
            pair("p0", "app", "date"),
            pair("p1", "app", "date"),
            pair("p2", "app", "date"),
            pair("p3", "app", "date"),
            pair("p4", "app", "date"),
        ]

        self.assertEqual(
            [row["pair_id"] for row in shard_pair_rows(rows, shard_index=0, shard_count=2)],
            ["p0", "p2", "p4"],
        )
        self.assertEqual(
            [row["pair_id"] for row in shard_pair_rows(rows, shard_index=1, shard_count=2)],
            ["p1", "p3"],
        )

    def test_collect_pair_terms_reads_appellation_and_date_normalized_terms(self) -> None:
        terms = collect_pair_terms([pair("p1", "app", "date")])

        self.assertEqual(terms["app"], PairTerm("app", "ABC"))
        self.assertEqual(terms["date"], PairTerm("date", "DEF"))

    def test_collect_perturbed_occurrences_labels_exact_generated_rows(self) -> None:
        terms = {"term": PairTerm("term", "ABCD")}

        occurrences, stats = collect_perturbed_occurrences_by_term(
            "AXBBCCDD",
            terms,
            min_skip=2,
            max_skip=2,
            direction="forward",
            triples=((0, 0, 0), (1, 0, 0)),
        )

        self.assertEqual(stats["term"].ordinary_hits, 1)
        self.assertEqual(stats["term"].exact_perturbed_rows, 2)
        self.assertEqual(stats["term"].defined_perturbed_rows, 2)
        self.assertEqual(set(occurrences["term"]), {(0, 0, 0), (1, 0, 0)})
        self.assertEqual(
            occurrences["term"][(1, 0, 0)],
            (WrrElsOccurrence((0, 3, 5, 7), 2, 0, 8),),
        )

    def test_collect_perturbed_occurrences_skips_too_short_terms(self) -> None:
        terms = {"term": PairTerm("term", "ABC")}

        occurrences, stats = collect_perturbed_occurrences_by_term(
            "ABCABC",
            terms,
            min_skip=2,
            max_skip=2,
            direction="forward",
            triples=((0, 0, 0),),
        )

        self.assertEqual(occurrences["term"], {})
        self.assertEqual(stats["term"].ordinary_hits, 0)
        self.assertEqual(stats["term"].defined_perturbed_rows, 0)

    def test_build_corrected_distance_rows_outputs_defined_rank(self) -> None:
        triples = tuple((index, 0, 0) for index in range(10))
        app_occurrences = {triple: (wrr_occurrence(0),) for triple in triples}
        right_starts = {
            (0, 0, 0): 2,
            (1, 0, 0): 1,
            (2, 0, 0): 40,
            (3, 0, 0): 3,
            (4, 0, 0): 5,
            (5, 0, 0): 15,
            (6, 0, 0): 25,
            (7, 0, 0): 35,
            (8, 0, 0): 45,
            (9, 0, 0): 55,
        }
        date_occurrences = {
            triple: (wrr_occurrence(right_starts[triple]),) for triple in triples
        }

        rows = build_corrected_distance_rows(
            [pair("p1", "app", "date")],
            {"app": app_occurrences, "date": date_occurrences},
            {"app": stats("app", 10), "date": stats("date", 10)},
            text_length=100,
            row_width_count=1,
            minimum_valid=10,
        )

        self.assertEqual(rows[0]["pair_valid_perturbations"], 10)
        self.assertEqual(rows[0]["appellation_starts_with_rabbi_title"], "True")
        self.assertEqual(rows[0]["ordinary_q"], "0.333333333333")
        self.assertEqual(rows[0]["corrected_distance"], "0.3")
        self.assertEqual(rows[0]["corrected_distance_status"], "defined")

    def test_build_corrected_distance_rows_reports_undefined_states(self) -> None:
        rows = build_corrected_distance_rows(
            [
                pair("p1", "app", "missing"),
                pair("p2", "app", "date"),
            ],
            {
                "app": {
                    (0, 0, 0): (wrr_occurrence(0),),
                    (1, 0, 0): (wrr_occurrence(0),),
                },
                "date": {
                    (0, 0, 0): (wrr_occurrence(2),),
                    (1, 0, 0): (wrr_occurrence(3),),
                },
            },
            {"app": stats("app", 2), "date": stats("date", 2)},
            text_length=100,
            row_width_count=1,
            minimum_valid=3,
        )

        self.assertEqual(rows[0]["corrected_distance_status"], "ordinary_not_valid")
        self.assertEqual(
            rows[1]["corrected_distance_status"],
            "under_minimum_valid_perturbations",
        )
        self.assertEqual(rows[1]["ordinary_q"], "0.333333333333")

    def test_summarize_counts_defined_and_undefined_rows(self) -> None:
        args = argparse.Namespace(
            candidate_lane="length_5_8_smoke_candidate",
            search_max_skip=250,
            skip_cap_mode="term",
            skip_cap_formula="printed",
            minimum_valid=10,
            shard_index=1,
            shard_count=3,
        )
        rows = [
            {
                "pair_id": "p1",
                "corrected_distance": "0.2",
                "corrected_distance_status": "defined",
                "pair_valid_perturbations": 10,
            },
            {
                "pair_id": "p2",
                "corrected_distance": "",
                "corrected_distance_status": "ordinary_not_valid",
                "pair_valid_perturbations": 0,
            },
            {
                "pair_id": "p3",
                "corrected_distance": "",
                "corrected_distance_status": "under_minimum_valid_perturbations",
                "pair_valid_perturbations": 5,
            },
        ]

        summary = summarize(rows, args, selected_pair_count=9)

        self.assertEqual(summary["selected_pairs"], 9)
        self.assertEqual(summary["shard_index"], 1)
        self.assertEqual(summary["shard_count"], 3)
        self.assertEqual(summary["pairs"], 3)
        self.assertEqual(summary["defined_corrected_distances"], 1)
        self.assertEqual(summary["ordinary_not_valid_pairs"], 1)
        self.assertEqual(summary["under_minimum_valid_pairs"], 1)
        self.assertEqual(summary["min_corrected_pair_id"], "p1")
        self.assertEqual(summary["max_pair_valid_perturbations"], 10)


def pair(
    pair_id: str,
    app_id: str,
    date_id: str,
    *,
    lane: str = "length_5_8_smoke_candidate",
) -> dict[str, str]:
    return {
        "pair_id": pair_id,
        "concept": "WRR2 01",
        "candidate_lane": lane,
        "pair_review_status": "needs_primary_source_pair_rule",
        "appellation_term_id": app_id,
        "appellation_starts_with_rabbi_title": "True",
        "appellation_normalized": "ABC",
        "date_term_id": date_id,
        "date_normalized": "DEF",
    }


def stats(term_id: str, count: int) -> PerturbedTermStats:
    return PerturbedTermStats(
        term_id,
        term_id.upper(),
        10,
        count,
        count,
        count,
        count,
        count,
    )


def wrr_occurrence(start: int) -> WrrElsOccurrence:
    return WrrElsOccurrence((start, start + 10, start + 20), 10, 0, 100)


if __name__ == "__main__":
    unittest.main()
