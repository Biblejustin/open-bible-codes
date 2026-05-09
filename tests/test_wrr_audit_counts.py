import unittest

from scripts.analyze_wrr_audit_counts import category_summary, summarize_by_concept, top_counts


class WrrAuditCountsTests(unittest.TestCase):
    def test_summary_groups_appellations_and_dates(self) -> None:
        rows = [
            row("wrr2_01_app_01", "WRR2 01", "wrr_appellation", "5"),
            row("wrr2_01_app_02", "WRR2 01", "wrr_appellation", "0"),
            row("wrr2_01_date_01", "WRR2 01", "wrr_date", "2"),
        ]

        summary = summarize_by_concept(rows)

        self.assertEqual(summary[0]["appellation_rows"], 2)
        self.assertEqual(summary[0]["date_rows"], 1)
        self.assertEqual(summary[0]["appellation_hits"], 5)
        self.assertEqual(summary[0]["date_hits"], 2)
        self.assertEqual(summary[0]["zero_appellation_rows"], 1)
        self.assertEqual(summary[0]["best_appellation_term_id"], "wrr2_01_app_01")

    def test_top_counts_orders_by_hits(self) -> None:
        rows = [
            row("a", "WRR2 01", "wrr_appellation", "1"),
            row("b", "WRR2 01", "wrr_date", "3"),
        ]

        top = top_counts(rows, 1)

        self.assertEqual(top[0]["term_id"], "b")

    def test_category_summary_tracks_zero_rows(self) -> None:
        stats = category_summary(
            [
                row("a", "WRR2 01", "wrr_appellation", "0"),
                row("b", "WRR2 01", "wrr_appellation", "2"),
            ]
        )

        self.assertEqual(stats["wrr_appellation"], {"rows": 2, "zero_rows": 1, "total_hits": 2})


def row(term_id: str, concept: str, category: str, hits: str) -> dict[str, str]:
    return {
        "term_id": term_id,
        "concept": concept,
        "category": category,
        "normalized_term": "ABC",
        "normalized_length": "3",
        "hit_count": hits,
        "status": "counted",
    }


if __name__ == "__main__":
    unittest.main()
