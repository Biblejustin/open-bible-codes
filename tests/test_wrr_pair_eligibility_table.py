import unittest

from scripts.build_wrr_pair_eligibility_table import build_pair_rows, summarize


class WrrPairEligibilityTableTests(unittest.TestCase):
    def test_build_pair_rows_labels_current_candidate_lanes(self) -> None:
        terms = [
            term("app_short", "WRR2 01", "wrr_appellation", "SHORT"),
            term("app_ok", "WRR2 01", "wrr_appellation", "APPOK"),
            term("date_ok", "WRR2 01", "wrr_date", "DATEOK"),
            term("date_long", "WRR2 01", "wrr_date", "LONGDATE"),
        ]
        counts = {
            "app_short": count("APPS", 4, 2),
            "app_ok": count("APPOK", 5, 3),
            "date_ok": count("DATEOK", 6, 4),
            "date_long": count("LONGDATE", 9, 5),
        }
        skip_caps = {
            "app_short": cap("10", "true"),
            "app_ok": cap("20", "true"),
            "date_ok": cap("30", "true"),
            "date_long": cap("40", "false"),
        }
        pair_summary = {
            ("app_ok", "date_ok"): {
                "all_pairs_within_gap": "7",
                "strict_pairs_within_gap": "1",
                "best_span_gap": "2",
                "best_center_distance": "3.5",
                "best_example_wrr_alpha": "0.25",
            }
        }

        rows = build_pair_rows(
            terms,
            counts,
            skip_caps,
            pair_summary,
            app_min_length=5,
            min_length=5,
            max_length=8,
        )
        by_pair = {row["pair_id"]: row for row in rows}

        self.assertEqual(
            by_pair["app_short__date_ok"]["candidate_lane"],
            "excluded_by_appellation_min_length",
        )
        self.assertEqual(
            by_pair["app_ok__date_ok"]["candidate_lane"],
            "length_5_8_smoke_candidate",
        )
        self.assertEqual(
            by_pair["app_ok__date_long"]["candidate_lane"],
            "appellation_min_length_candidate",
        )
        self.assertEqual(by_pair["app_ok__date_ok"]["all_pairs_within_gap"], 7)
        self.assertEqual(by_pair["app_ok__date_ok"]["strict_pairs_within_gap"], 1)
        self.assertIn(
            "date expected-count skip cap target not reached",
            by_pair["app_ok__date_long"]["eligibility_notes"],
        )

    def test_zacut_diagnostic_is_flagged_but_not_excluded(self) -> None:
        terms = [
            term("zacut_app", "WRR2 27", "wrr_appellation", "ZKWTA"),
            term("zacut_date", "WRR2 27", "wrr_date", "DATEA"),
        ]
        counts = {
            "zacut_app": count("ZKWTA", 5, 1),
            "zacut_date": count("DATEA", 5, 1),
        }
        skip_caps = {
            "zacut_app": cap("10", "true"),
            "zacut_date": cap("10", "true"),
        }

        rows = build_pair_rows(
            terms,
            counts,
            skip_caps,
            {},
            app_min_length=5,
            min_length=5,
            max_length=8,
        )

        self.assertTrue(rows[0]["wnp_disputed_zacut_appellation"])
        self.assertEqual(
            rows[0]["pair_review_status"],
            "diagnostic_exclusion_candidate_not_locked",
        )
        self.assertEqual(rows[0]["candidate_lane"], "length_5_8_smoke_candidate")

    def test_summarize_reports_gap_counts(self) -> None:
        rows = [
            {
                "concept": "a",
                "appellation_min_length_ok": True,
                "length_filtered_pair_ok": True,
                "wnp_disputed_zacut_appellation": False,
                "appellation_hit_count": 1,
                "date_hit_count": 1,
                "appellation_target_reached": "true",
                "date_target_reached": "true",
                "all_pairs_within_gap": 1,
                "strict_pairs_within_gap": 0,
            },
            {
                "concept": "a",
                "appellation_min_length_ok": True,
                "length_filtered_pair_ok": False,
                "wnp_disputed_zacut_appellation": True,
                "appellation_hit_count": 0,
                "date_hit_count": 1,
                "appellation_target_reached": "false",
                "date_target_reached": "true",
                "all_pairs_within_gap": 0,
                "strict_pairs_within_gap": 0,
            },
        ]

        summary = summarize(rows, expected_published_pairs=3)

        self.assertEqual(summary["pairs"], 2)
        self.assertEqual(summary["concepts"], 1)
        self.assertEqual(summary["appellation_min_length_pairs"], 2)
        self.assertEqual(summary["length_filtered_pairs"], 1)
        self.assertEqual(summary["wnp_disputed_zacut_pairs"], 1)
        self.assertEqual(summary["zero_hit_pairs"], 1)
        self.assertEqual(summary["pairs_with_skip_cap_target_unreached"], 1)
        self.assertEqual(summary["gap_appellation_min_length_to_expected"], 1)
        self.assertEqual(summary["gap_length_filtered_to_expected"], 2)


def term(term_id: str, concept: str, category: str, value: str) -> dict[str, str]:
    return {"term_id": term_id, "concept": concept, "category": category, "term": value}


def count(normalized: str, length: int, hits: int) -> dict[str, str]:
    return {
        "normalized_term": normalized,
        "normalized_length": str(length),
        "hit_count": str(hits),
    }


def cap(skip_cap: str, target_reached: str) -> dict[str, str]:
    return {"skip_cap": skip_cap, "target_reached": target_reached}


if __name__ == "__main__":
    unittest.main()
