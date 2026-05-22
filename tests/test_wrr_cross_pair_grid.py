import unittest

from els.protocol_runner import load_protocol
from scripts.build_wrr_cross_pair_grid import build_grid_rows, summarize


class WrrCrossPairGridTests(unittest.TestCase):
    def test_build_grid_rows_crosses_all_appellations_and_dates(self) -> None:
        terms = [
            {
                "term_id": "wrr2_01_app_01",
                "concept": "WRR2 01",
                "category": "wrr_appellation",
                "term": "RBYABC",
            },
            {
                "term_id": "wrr2_02_app_01",
                "concept": "WRR2 02",
                "category": "wrr_appellation",
                "term": "XYZ",
            },
            {
                "term_id": "wrr2_01_date_01",
                "concept": "WRR2 01",
                "category": "wrr_date",
                "term": "DATEA",
            },
            {
                "term_id": "wrr2_02_date_01",
                "concept": "WRR2 02",
                "category": "wrr_date",
                "term": "DATEB",
            },
        ]
        counts = {
            "wrr2_01_app_01": count_row("ABCDEF", 6, 1),
            "wrr2_02_app_01": count_row("XYZ", 3, 0),
            "wrr2_01_date_01": count_row("DATEA", 5, 2),
            "wrr2_02_date_01": count_row("DATEB", 5, 3),
        }
        skip_caps = {
            "wrr2_01_app_01": {"skip_cap": "25", "target_reached": "true"},
            "wrr2_02_app_01": {"skip_cap": "25", "target_reached": "false"},
            "wrr2_01_date_01": {"skip_cap": "25", "target_reached": "true"},
            "wrr2_02_date_01": {"skip_cap": "25", "target_reached": "true"},
        }

        rows = build_grid_rows(
            terms,
            counts,
            skip_caps,
            app_min_length=5,
            min_length=5,
            max_length=8,
        )
        summary = summarize(rows)

        self.assertEqual(len(rows), 4)
        self.assertEqual(summary["same_record_pairs"], 2)
        self.assertEqual(summary["cross_record_pairs"], 2)
        self.assertEqual(summary["length_filtered_pairs"], 2)
        self.assertEqual(summary["appellation_min_length_pairs"], 2)
        self.assertEqual(summary["rabbi_title_pairs"], 2)
        cross = next(
            row
            for row in rows
            if row["appellation_term_id"] == "wrr2_01_app_01"
            and row["date_term_id"] == "wrr2_02_date_01"
        )
        self.assertFalse(cross["same_record_pair"])
        self.assertEqual(cross["pair_review_status"], "cross_record_permutation_pair")
        self.assertEqual(cross["candidate_lane"], "length_5_8_permutation_candidate")

    def test_method_status_refresh_declares_scenario_inputs(self) -> None:
        protocol = load_protocol("protocols/wrr_cross_pair_grid.toml")
        steps_by_id = {step["id"]: step for step in protocol["steps"]}
        method_status = steps_by_id["build_wrr_method_status_after_cross_pair"]

        self.assertIn(
            "reports/wrr_1994/wrr_source_policy_scenarios.csv",
            method_status["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_source_policy_term_impacts.csv",
            method_status["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_dw_formula_sensitivity.csv",
            method_status["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_variant_gap_impact_summary.csv",
            method_status["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_variant_residual_review_summary.csv",
            method_status["inputs"],
        )
        self.assertIn("--source-policy-scenarios", method_status["argv"])
        self.assertIn("--variant-residual-summary", method_status["argv"])
        self.assertIn("--source-policy-term-impacts", method_status["argv"])
        self.assertIn("--dw-formula-sensitivity", method_status["argv"])
        self.assertIn("--variant-gap-summary", method_status["argv"])


def count_row(normalized: str, length: int, hits: int) -> dict[str, str]:
    return {
        "normalized_term": normalized,
        "normalized_length": str(length),
        "hit_count": str(hits),
    }


if __name__ == "__main__":
    unittest.main()
