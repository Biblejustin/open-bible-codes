import unittest

from scripts.analyze_wrr_perturbation_pair_readiness import (
    build_pair_rows,
    pair_status,
    summarize,
)


class WrrPerturbationPairReadinessTests(unittest.TestCase):
    def test_pair_status_reports_outside_sample_scope(self) -> None:
        status, note = pair_status(
            "appellation_min_length_candidate",
            None,
            perturbation("2", "125", "1"),
        )

        self.assertEqual(status, "outside_sample_scope")
        self.assertEqual(note, "candidate lane appellation_min_length_candidate not sampled")

    def test_pair_status_reports_missing_diagnostic_inside_scope(self) -> None:
        status, note = pair_status(
            "length_5_8_smoke_candidate",
            None,
            perturbation("2", "125", "1"),
        )

        self.assertEqual(status, "missing_diagnostic")
        self.assertEqual(note, "missing diagnostic: appellation")

    def test_pair_status_reports_missing_samples(self) -> None:
        status, note = pair_status(
            "length_5_8_smoke_candidate",
            perturbation("0", "", ""),
            perturbation("2", "125", "1"),
        )

        self.assertEqual(status, "missing_sampled_hits")
        self.assertEqual(note, "no sampled hits: appellation")

    def test_pair_status_reports_under_10_exact_matches(self) -> None:
        status, note = pair_status(
            "length_5_8_smoke_candidate",
            perturbation("2", "125", "1"),
            perturbation("2", "125", "12"),
        )

        self.assertEqual(status, "under_10_exact_matches")
        self.assertEqual(note, "min exact 1")

    def test_pair_status_reports_sample_ready(self) -> None:
        status, note = pair_status(
            "length_5_8_smoke_candidate",
            perturbation("2", "125", "10"),
            perturbation("2", "125", "12"),
        )

        self.assertEqual(status, "sample_ready")
        self.assertEqual(note, "sample has >=10 exact perturbed matches on both terms")

    def test_build_pair_rows_joins_appellation_and_date_diagnostics(self) -> None:
        rows = build_pair_rows(
            [
                pair("p1", "length_5_8_smoke_candidate", "app_1", "date_1"),
                pair("p2", "excluded_by_appellation_min_length", "missing", "date_1"),
            ],
            {
                "app_1": perturbation("3", "125", "1"),
                "date_1": perturbation("4", "125", "12"),
            },
        )

        self.assertEqual(rows[0]["appellation_min_exact"], "1")
        self.assertEqual(rows[0]["date_min_exact"], "12")
        self.assertEqual(rows[0]["perturbation_sample_status"], "under_10_exact_matches")
        self.assertEqual(rows[1]["perturbation_sample_status"], "outside_sample_scope")

    def test_summarize_counts_pair_statuses(self) -> None:
        rows = build_pair_rows(
            [
                pair("p1", "length_5_8_smoke_candidate", "app_1", "date_1"),
                pair("p2", "length_5_8_smoke_candidate", "app_2", "date_2"),
                pair("p3", "excluded_by_appellation_min_length", "missing", "date_2"),
            ],
            {
                "app_1": perturbation("3", "125", "1"),
                "date_1": perturbation("4", "125", "12"),
                "app_2": perturbation("4", "125", "10"),
                "date_2": perturbation("4", "125", "12"),
            },
        )

        summary = summarize(rows)

        self.assertEqual(summary["pairs"], 3)
        self.assertEqual(summary["length_5_8_smoke_candidate_pairs"], 2)
        self.assertEqual(summary["pairs_outside_sample_scope"], 1)
        self.assertEqual(summary["pairs_under_10_exact_matches"], 1)
        self.assertEqual(summary["pairs_sample_ready"], 1)
        self.assertEqual(summary["pairs_missing_diagnostic"], 0)


def pair(
    pair_id: str,
    lane: str,
    app_id: str,
    date_id: str,
) -> dict[str, str]:
    return {
        "pair_id": pair_id,
        "concept": "WRR2 01",
        "candidate_lane": lane,
        "appellation_term_id": app_id,
        "date_term_id": date_id,
    }


def perturbation(
    sampled_hits: str,
    min_in_bound: str,
    min_exact: str,
) -> dict[str, str]:
    return {
        "term_id": "term",
        "sampled_hits": sampled_hits,
        "min_in_bounds_perturbations": min_in_bound,
        "min_exact_perturbation_matches": min_exact,
        "read": "read",
    }


if __name__ == "__main__":
    unittest.main()
