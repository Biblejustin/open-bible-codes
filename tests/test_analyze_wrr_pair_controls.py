import unittest

from scripts.analyze_wrr_pair_controls import annotate_q_values, select_top_pairs


class WrrPairControlsTests(unittest.TestCase):
    def test_select_top_pairs_prefers_strict_then_close_pairs(self) -> None:
        rows = [
            row("a", strict=0, close=100, best_gap=0),
            row("b", strict=2, close=10, best_gap=4),
            row("c", strict=0, close=0, best_gap=0),
            row("d", strict=2, close=20, best_gap=10),
        ]

        selected = select_top_pairs(rows, 2)

        self.assertEqual([item["appellation_term_id"] for item in selected], ["d", "b"])

    def test_annotate_q_values_labels_not_unusual_rows(self) -> None:
        rows = [
            {
                "combined_min_p": 0.5,
                "band": "",
                "read": "",
            }
        ]

        annotate_q_values(rows)

        self.assertEqual(rows[0]["band"], "not_unusual")
        self.assertEqual(rows[0]["read"], "not unusual under top-pair controls")


def row(term_id: str, strict: int, close: int, best_gap: int) -> dict[str, str]:
    return {
        "corpus": "SAMPLE",
        "concept": "WRR2 01",
        "appellation_term_id": term_id,
        "appellation_normalized": "ABC",
        "date_term_id": f"{term_id}_date",
        "date_normalized": "DEF",
        "all_pairs_within_gap": str(close),
        "strict_pairs_within_gap": str(strict),
        "best_span_gap": str(best_gap),
        "best_center_distance": str(best_gap + 1),
    }


if __name__ == "__main__":
    unittest.main()
