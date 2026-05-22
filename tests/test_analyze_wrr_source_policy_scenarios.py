import csv
import tempfile
import unittest
from pathlib import Path

from scripts import analyze_wrr_source_policy_scenarios as scenarios


class WrrSourcePolicyScenarioTests(unittest.TestCase):
    def test_analyze_scenarios_counts_diagnostic_impacts(self) -> None:
        pair_rows = sample_pair_rows()
        source_rows = sample_source_rows()
        term_index = scenarios.build_flagged_term_index(pair_rows, source_rows)
        summary_rows, detail_rows = scenarios.analyze_scenarios(
            pair_rows,
            term_index,
            expected_pairs=3,
        )
        term_impact_rows = scenarios.build_term_impact_rows(
            pair_rows,
            term_index,
            expected_pairs=3,
        )

        by_name = {row["scenario"]: row for row in summary_rows}
        self.assertEqual(by_name["keep_all_working_source"]["excluded_pairs"], 0)
        self.assertEqual(
            by_name["keep_all_working_source"][
                "remaining_appellation_min_length_pairs"
            ],
            3,
        )
        self.assertEqual(by_name["exclude_wnp_zacut_only"]["excluded_pairs"], 1)
        self.assertEqual(
            by_name["exclude_wnp_zacut_only"][
                "gap_to_source_cited_163_after_appellation_min_length"
            ],
            1,
        )
        self.assertEqual(by_name["exclude_book_title_only"]["excluded_pairs"], 1)
        self.assertEqual(by_name["review_chelm_spelling_only"]["excluded_pairs"], 0)
        self.assertEqual(by_name["review_chelm_spelling_only"]["review_only_pairs"], 1)
        self.assertEqual(by_name["exclude_all_source_review_flags"]["excluded_pairs"], 3)

        excluded = [
            row
            for row in detail_rows
            if row["scenario"] == "exclude_all_source_review_flags"
            and row["scenario_action"] == "excluded"
        ]
        self.assertEqual({row["pair_id"] for row in excluded}, {"p2", "p3", "p4"})
        by_term = {row["term_id"]: row for row in term_impact_rows}
        self.assertEqual(by_term["wrr2_27_app_05"]["affected_pairs"], 1)
        self.assertEqual(
            by_term["wrr2_27_app_05"][
                "remaining_appellation_min_length_pairs_if_excluded"
            ],
            2,
        )

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pair_table = root / "pairs.csv"
            source_queue = root / "source_queue.csv"
            out = root / "summary.csv"
            pair_out = root / "pairs_out.csv"
            term_impact_out = root / "term_impacts.csv"
            markdown = root / "scenarios.md"
            manifest = root / "manifest.json"
            write_csv(pair_table, sample_pair_rows())
            write_csv(source_queue, sample_source_rows())

            rc = scenarios.main(
                [
                    "--pair-table",
                    str(pair_table),
                    "--source-queue",
                    str(source_queue),
                    "--expected-published-pairs",
                    "3",
                    "--out",
                    str(out),
                    "--pair-out",
                    str(pair_out),
                    "--term-impact-out",
                    str(term_impact_out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            summary = list(csv.DictReader(out.open(encoding="utf-8")))
            self.assertEqual(len(summary), 5)
            detail = list(csv.DictReader(pair_out.open(encoding="utf-8")))
            self.assertTrue(any(row["scenario_action"] == "review_only_no_exclusion" for row in detail))
            impacts = list(csv.DictReader(term_impact_out.open(encoding="utf-8")))
            self.assertEqual(len(impacts), 3)
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("WRR Source Policy Scenario Impact", text)
            self.assertIn("Single-Term Impact", text)
            self.assertIn("No source policy is selected", text)
            self.assertIn("Visual-review notes remain triage only", text)
            self.assertTrue(manifest.exists())


def sample_pair_rows() -> list[dict[str, str]]:
    return [
        pair_row(
            "p1",
            "WRR2 01",
            "app1",
            "AAA",
            "date1",
            "DDD",
            app_min=True,
            length=True,
            wnp=False,
        ),
        pair_row(
            "p2",
            "WRR2 27",
            "wrr2_27_app_05",
            "M$HZKWTA",
            "date2",
            "EEE",
            app_min=True,
            length=False,
            wnp=True,
        ),
        pair_row(
            "p3",
            "WRR2 30",
            "wrr2_30_app_05",
            "B@LY$RLBB",
            "date3",
            "FFF",
            app_min=True,
            length=True,
            wnp=False,
        ),
        pair_row(
            "p4",
            "WRR2 32",
            "wrr2_32_app_04",
            "$LMHMXLMA",
            "date4",
            "GGG",
            app_min=False,
            length=False,
            wnp=False,
        ),
    ]


def sample_source_rows() -> list[dict[str, str]]:
    return [
        {
            "term_id": "wrr2_27_app_05",
            "term": "M$HZKWTA",
            "term_side": "appellation",
            "concepts": "WRR2 27",
            "source_review_flags": "wnp_disputed_zacut_appellation",
            "source_review_action": "diagnostic flag only",
        },
        {
            "term_id": "wrr2_30_app_05",
            "term": "B@LY$RLBB",
            "term_side": "appellation",
            "concepts": "WRR2 30",
            "source_review_flags": "wnp_book_title_appellation_dispute",
            "source_review_action": "source/title-prefix rule review",
        },
        {
            "term_id": "wrr2_32_app_04",
            "term": "$LMHMXLMA",
            "term_side": "appellation",
            "concepts": "WRR2 32",
            "source_review_flags": "wnp_chelm_spelling_context",
            "source_review_action": "source/pair-rule review",
        },
    ]


def pair_row(
    pair_id: str,
    concept: str,
    app_id: str,
    app_term: str,
    date_id: str,
    date_term: str,
    *,
    app_min: bool,
    length: bool,
    wnp: bool,
) -> dict[str, str]:
    return {
        "pair_id": pair_id,
        "concept": concept,
        "appellation_term_id": app_id,
        "appellation_term": app_term,
        "date_term_id": date_id,
        "date_term": date_term,
        "appellation_min_length_ok": str(app_min),
        "length_filtered_pair_ok": str(length),
        "appellation_starts_with_rabbi_title": "False",
        "wnp_disputed_zacut_appellation": str(wnp),
        "candidate_lane": "length_5_8_smoke_candidate" if length else "appellation_min_length_candidate",
        "pair_review_status": "needs_primary_source_pair_rule",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
