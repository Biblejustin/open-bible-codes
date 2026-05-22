import csv
import tempfile
import unittest
from pathlib import Path

from scripts import analyze_wrr_defined_pair_set as audit


class WrrDefinedPairSetTests(unittest.TestCase):
    def test_summarize_run_counts_gap_to_source_cited_count(self) -> None:
        run = audit.RunSpec("sample", Path("sample.csv"))
        rows = [
            {"corrected_distance_status": "defined"},
            {"corrected_distance_status": "ordinary_not_valid"},
            {"corrected_distance_status": "under_minimum_valid_perturbations"},
            {"corrected_distance_status": "other"},
        ]

        summary = audit.summarize_run(run, rows, expected_defined=10)

        self.assertEqual(summary["defined"], 1)
        self.assertEqual(summary["ordinary_not_valid"], 1)
        self.assertEqual(summary["under_minimum_valid"], 1)
        self.assertEqual(summary["other_statuses"], 1)
        self.assertEqual(summary["defined_gap_to_source_cited"], 9)

    def test_breakdown_run_groups_by_candidate_and_review_fields(self) -> None:
        run = audit.RunSpec("sample", Path("sample.csv"))
        rows = [
            {
                "candidate_lane": "length_5_8_smoke_candidate",
                "pair_review_status": "needs_primary_source_pair_rule",
                "wnp_disputed_zacut_appellation": "False",
                "corrected_distance_status": "defined",
            },
            {
                "candidate_lane": "appellation_min_length_candidate",
                "pair_review_status": "diagnostic_exclusion_candidate_not_locked",
                "wnp_disputed_zacut_appellation": "True",
                "corrected_distance_status": "ordinary_not_valid",
            },
        ]

        detail = audit.breakdown_run(run, rows, expected_defined=3)
        by_group_value = {(row["group"], row["value"]): row for row in detail}

        self.assertEqual(by_group_value[("candidate_lane", "length_5_8_smoke_candidate")]["defined"], 1)
        self.assertEqual(by_group_value[("wnp_disputed_zacut_appellation", "True")]["ordinary_not_valid"], 1)
        self.assertEqual(
            by_group_value[("pair_review_status", "diagnostic_exclusion_candidate_not_locked")]["pairs"],
            1,
        )

    def test_main_writes_csv_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pair_summary = root / "pair_summary.csv"
            pair_table = root / "pair_table.csv"
            corrected = root / "corrected.csv"
            out = root / "out.csv"
            summary_out = root / "summary.csv"
            markdown = root / "out.md"
            manifest = root / "manifest.json"
            write_csv(pair_summary, [{"expected_published_pairs": "3"}])
            write_csv(
                pair_table,
                [
                    {
                        "pair_id": "p1",
                        "candidate_lane": "length_5_8_smoke_candidate",
                        "pair_review_status": "needs_primary_source_pair_rule",
                        "wnp_disputed_zacut_appellation": "False",
                    },
                    {
                        "pair_id": "p2",
                        "candidate_lane": "appellation_min_length_candidate",
                        "pair_review_status": "needs_primary_source_pair_rule",
                        "wnp_disputed_zacut_appellation": "True",
                    },
                ],
            )
            write_csv(
                corrected,
                [
                    {"pair_id": "p1", "corrected_distance_status": "defined"},
                    {"pair_id": "p2", "corrected_distance_status": "ordinary_not_valid"},
                ],
            )

            rc = audit.main(
                [
                    "--pair-summary",
                    str(pair_summary),
                    "--pair-table",
                    str(pair_table),
                    "--run",
                    f"sample={corrected}",
                    "--out",
                    str(out),
                    "--summary-out",
                    str(summary_out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            summary_rows = list(csv.DictReader(summary_out.open(encoding="utf-8")))
            self.assertEqual(summary_rows[0]["defined"], "1")
            self.assertEqual(summary_rows[0]["defined_gap_to_source_cited"], "2")
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("WRR Defined Pair-Set Audit", text)
            self.assertIn("Gap to the source-cited count remains 2", text)
            self.assertTrue(manifest.exists())


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
