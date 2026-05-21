import unittest

from els.wrr import p2_product_statistic
from scripts.analyze_wrr_corrected_distance_aggregate import (
    aggregate,
    corrected_distance_values,
)


class WrrCorrectedDistanceAggregateTests(unittest.TestCase):
    def test_corrected_distance_values_reads_defined_rows_only(self) -> None:
        rows = [
            {"corrected_distance_status": "defined", "corrected_distance": "0.1"},
            {"corrected_distance_status": "ordinary_not_valid", "corrected_distance": ""},
            {"corrected_distance_status": "defined", "corrected_distance": "0.4"},
        ]

        self.assertEqual(corrected_distance_values(rows), [0.1, 0.4])

    def test_aggregate_computes_p1_p2_for_defined_rows(self) -> None:
        rows = [
            {"corrected_distance_status": "defined", "corrected_distance": "0.1"},
            {"corrected_distance_status": "defined", "corrected_distance": "0.4"},
            {"corrected_distance_status": "under_minimum_valid_perturbations", "corrected_distance": ""},
        ]

        summary = aggregate(rows, source="input.csv", p1_threshold=0.2)

        self.assertEqual(summary["rows"], 3)
        self.assertEqual(summary["defined_corrected_distances"], 2)
        self.assertEqual(summary["undefined_rows"], 1)
        self.assertEqual(summary["p1"], "0.36")
        self.assertAlmostEqual(float(summary["p2"]), p2_product_statistic([0.1, 0.4]))
        self.assertEqual(summary["min_corrected_distance"], "0.1")
        self.assertEqual(summary["max_corrected_distance"], "0.4")

    def test_aggregate_handles_no_defined_rows(self) -> None:
        summary = aggregate(
            [{"corrected_distance_status": "ordinary_not_valid", "corrected_distance": ""}],
            source="input.csv",
            p1_threshold=0.2,
        )

        self.assertEqual(summary["defined_corrected_distances"], 0)
        self.assertEqual(summary["p1"], "")
        self.assertEqual(summary["p2"], "")
        self.assertEqual(summary["status"], "no_defined_corrected_distances")


if __name__ == "__main__":
    unittest.main()
