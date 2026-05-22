import csv
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_residual_term_reconciliation_queue as queue


class WrrResidualTermReconciliationQueueTests(unittest.TestCase):
    def test_build_term_rows_collapses_repeated_unresolved_terms(self) -> None:
        residual = [
            {
                "run_label": "all_lanes_cap1000",
                "within_minimum_residual_frontier": "true",
                "impact_status": "no_blocking_term_variant_hit",
                "pair_id": "p1",
                "concept": "WRR2 01",
                "row_ocr_pair_status": "mixed",
                "unresolved_term_ids": "wrr2_01_app_01",
                "unresolved_terms": "APP",
                "unresolved_term_sides": "appellation",
                "unresolved_term_buckets": "ocr_not_matched_no_variant_lead",
                "unresolved_term_ocr_statuses": "not_matched",
                "unresolved_source_flags": "",
                "unresolved_visual_actions": "",
            },
            {
                "run_label": "all_lanes_cap1000",
                "within_minimum_residual_frontier": "false",
                "impact_status": "no_blocking_term_variant_hit",
                "pair_id": "p2",
                "concept": "WRR2 01",
                "row_ocr_pair_status": "mixed",
                "unresolved_term_ids": "wrr2_01_app_01",
                "unresolved_terms": "APP",
                "unresolved_term_sides": "appellation",
                "unresolved_term_buckets": "ocr_not_matched_no_variant_lead",
                "unresolved_term_ocr_statuses": "not_matched",
                "unresolved_source_flags": "",
                "unresolved_visual_actions": "",
            },
        ]
        source_rows = {
            "wrr2_01_app_01": {
                "priority_rank": "7",
                "review_bucket": "ocr_not_matched_no_variant_lead",
                "row_ocr_status": "not_matched",
                "best_variant_hit_count": "0",
                "best_variant_rule": "none",
                "best_variant_normalized": "",
                "pair_ids": "p1;p2",
            }
        }

        rows = queue.build_term_rows(residual, source_rows)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["term_id"], "wrr2_01_app_01")
        self.assertEqual(rows[0]["residual_pairs"], 2)
        self.assertEqual(rows[0]["frontier_pairs"], 1)
        self.assertEqual(
            rows[0]["reconciliation_need"],
            "source_transcription_or_row_alignment",
        )

    def test_main_writes_queue_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            residual = root / "residual.csv"
            source = root / "source.csv"
            out = root / "queue.csv"
            summary = root / "summary.csv"
            markdown = root / "queue.md"
            manifest = root / "manifest.json"
            write_csv(
                residual,
                [
                    {
                        "run_label": "all_lanes_cap1000",
                        "within_minimum_residual_frontier": "true",
                        "impact_status": "no_blocking_term_variant_hit",
                        "pair_id": "p1",
                        "concept": "WRR2 32",
                        "row_ocr_pair_status": "mixed",
                        "unresolved_term_ids": "wrr2_32_app_05",
                        "unresolved_terms": "$LMHMX@LMA",
                        "unresolved_term_sides": "appellation",
                        "unresolved_term_buckets": "ocr_not_matched_no_variant_lead",
                        "unresolved_term_ocr_statuses": "not_matched",
                        "unresolved_source_flags": "wnp_chelm_spelling_context",
                        "unresolved_visual_actions": "review source/pair rule",
                    }
                ],
            )
            write_csv(
                source,
                [
                    {
                        "term_id": "wrr2_32_app_05",
                        "priority_rank": "83",
                        "review_bucket": "ocr_not_matched_no_variant_lead",
                        "row_ocr_status": "not_matched",
                        "row_ocr_match_basis": "",
                        "best_variant_hit_count": "0",
                        "best_variant_rule": "none",
                        "best_variant_normalized": "",
                        "pair_ids": "p1",
                        "source_review_action": "source/pair-rule review",
                    }
                ],
            )

            rc = queue.main(
                [
                    "--residual-packet",
                    str(residual),
                    "--source-queue",
                    str(source),
                    "--out",
                    str(out),
                    "--summary-out",
                    str(summary),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            rows = list(csv.DictReader(out.open(encoding="utf-8")))
            self.assertEqual(rows[0]["source_flags"], "wnp_chelm_spelling_context")
            self.assertEqual(
                rows[0]["reconciliation_need"],
                "source_policy_or_pair_rule_review",
            )
            summary_rows = list(csv.DictReader(summary.open(encoding="utf-8")))
            summary_keys = {(row["group"], row["value"]) for row in summary_rows}
            self.assertIn(("residual_terms", "unique_unresolved_terms"), summary_keys)
            self.assertIn(
                ("source_flag", "wnp_chelm_spelling_context"),
                summary_keys,
            )
            self.assertIn(
                "WRR Residual Term Reconciliation Queue",
                markdown.read_text(encoding="utf-8"),
            )
            self.assertTrue(manifest.exists())


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
