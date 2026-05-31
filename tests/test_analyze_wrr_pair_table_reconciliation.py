import argparse
import unittest

from scripts.analyze_wrr_pair_table_reconciliation import reconcile_concepts, summarize
from scripts.import_wrr_terms import WrrRecord


class WrrPairTableReconciliationTests(unittest.TestCase):
    def test_reconcile_concepts_counts_length_filter_pair_losses(self) -> None:
        rows = [
            term("app_ok", "WRR2 01", "wrr_appellation", "APP"),
            term("app_short", "WRR2 01", "wrr_appellation", "SHORT"),
            term("date_ok", "WRR2 01", "wrr_date", "DATE"),
            term("date_long", "WRR2 01", "wrr_date", "LONGDATE"),
        ]
        counts = {
            "app_ok": {"normalized_length": "5"},
            "app_short": {"normalized_length": "4"},
            "date_ok": {"normalized_length": "8"},
            "date_long": {"normalized_length": "9"},
        }

        result = reconcile_concepts(rows, counts, min_length=5, max_length=8, app_min_length=5)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["same_record_pairs"], 4)
        self.assertEqual(result[0]["appellation_min_length_pairs"], 2)
        self.assertEqual(result[0]["length_filtered_pairs"], 1)
        self.assertEqual(result[0]["pairs_dropped_by_appellation_length"], 1)
        self.assertEqual(result[0]["pairs_dropped_by_date_length"], 1)
        self.assertEqual(result[0]["pairs_dropped_by_both_lengths"], 1)

    def test_zacut_diagnostic_counts_hypothetical_exclusion_delta(self) -> None:
        rows = [
            term("zacut_a", "WRR2 27", "wrr_appellation", "ZKWTA"),
            term("zacut_b", "WRR2 27", "wrr_appellation", "ZKWTW"),
            term("zacut_c", "WRR2 27", "wrr_appellation", "M$HZKWTA"),
            term("zacut_d", "WRR2 27", "wrr_appellation", "M$HZKWTW"),
            term("zacut_keep", "WRR2 27", "wrr_appellation", "M$HZKWT"),
            term("date_a", "WRR2 27", "wrr_date", "DATEA"),
            term("date_b", "WRR2 27", "wrr_date", "DATEB"),
        ]
        counts = {row["term_id"]: {"normalized_length": "5"} for row in rows}

        result = reconcile_concepts(rows, counts, min_length=5, max_length=8, app_min_length=5)
        summary = summarize(
            [WrrRecord(27, tuple(row["term"] for row in rows[:5]), ("date_a", "date_b"))],
            result,
            argparse.Namespace(
                appellation_min_term_length=5,
                min_term_length=5,
                max_term_length=8,
                expected_published_pairs=8,
            ),
        )

        self.assertEqual(result[0]["wnp_disputed_zacut_appellation_rows"], 4)
        self.assertEqual(result[0]["wnp_disputed_zacut_appellation_min_length_pairs"], 8)
        self.assertEqual(summary["appellation_min_length_same_record_pairs"], 10)
        self.assertEqual(summary["appellation_min_length_pairs_after_wnp_disputed_zacut_excluded"], 2)
        self.assertEqual(summary["one_zacut_appellation_min_length_pair_delta"], 2)
        self.assertEqual(summary["appellation_min_length_pairs_after_one_zacut_appellation_excluded"], 8)
        self.assertEqual(summary["appellation_min_length_gap_after_one_zacut_appellation_excluded"], 0)

    def test_summarize_reports_gap_to_expected_pair_count(self) -> None:
        source_records = [
            WrrRecord(1, ("app1", "app2"), ("date1",)),
            WrrRecord(2, ("undated",), ()),
        ]
        rows = [
            {
                "concept": "WRR2 01",
                "appellation_rows": 2,
                "date_rows": 1,
                "same_record_pairs": 2,
                "appellation_min_length_pairs": 2,
                "length_filtered_appellation_rows": 1,
                "length_filtered_date_rows": 1,
                "length_filtered_pairs": 1,
                "pairs_dropped_by_appellation_length": 1,
                "pairs_dropped_by_date_length": 0,
                "pairs_dropped_by_both_lengths": 0,
            }
        ]
        args = argparse.Namespace(
            appellation_min_term_length=5,
            min_term_length=5,
            max_term_length=8,
            expected_published_pairs=163,
        )

        summary = summarize(source_records, rows, args)

        self.assertEqual(summary["source_records"], 2)
        self.assertEqual(summary["source_undated_records"], 1)
        self.assertEqual(summary["source_same_record_pairs"], 2)
        self.assertEqual(summary["imported_same_record_pairs"], 2)
        self.assertEqual(summary["appellation_min_length_same_record_pairs"], 2)
        self.assertEqual(summary["length_filtered_same_record_pairs"], 1)
        self.assertEqual(summary["appellation_min_length_gap_to_expected"], 161)
        self.assertEqual(summary["imported_pair_gap_to_expected"], 161)
        self.assertEqual(summary["length_filtered_gap_to_expected"], 162)


def term(term_id: str, concept: str, category: str, value: str = "") -> dict[str, str]:
    return {"term_id": term_id, "concept": concept, "category": category, "term": value}


if __name__ == "__main__":
    unittest.main()
