import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_residual_reconciliation_action_plan as plan


class WrrResidualReconciliationActionPlanTests(unittest.TestCase):
    def test_build_action_rows_maps_reconciliation_need_to_evidence(self) -> None:
        rows = plan.build_action_rows(
            [
                {
                    "run_label": "all_lanes_cap1000",
                    "priority_rank": "2",
                    "term_id": "wrr2_27_app_13",
                    "term": "B@LQWLHRMZ",
                    "term_side": "appellation",
                    "residual_pairs": "2",
                    "frontier_pairs": "1",
                    "review_buckets": "ocr_not_matched_no_variant_lead",
                    "term_ocr_statuses": "not_matched",
                    "source_flags": "",
                    "source_queue_rank": "40",
                    "source_queue_ocr_status": "not_matched",
                    "source_queue_best_variant_hits": "0",
                    "source_queue_best_variant_rule": "none",
                    "source_review_action": "",
                    "visual_review_action": "",
                    "pair_ids": "p1;p2",
                    "reconciliation_need": "source_transcription_or_row_alignment",
                }
            ]
        )

        self.assertEqual(rows[0]["action_lane"], "source_transcription_or_row_alignment")
        self.assertIn("primary table row transcription", rows[0]["evidence_required"])
        self.assertIn("do not correct transcription", rows[0]["no_input_boundary"])

    def test_main_writes_action_plan_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            queue = root / "queue.csv"
            out = root / "action_plan.csv"
            summary = root / "summary.csv"
            markdown = root / "plan.md"
            manifest = root / "manifest.json"
            write_csv(
                queue,
                [
                    {
                        "run_label": "all_lanes_cap1000",
                        "priority_rank": "1",
                        "term_id": "wrr2_32_app_05",
                        "term": "$LMHMX@LMA",
                        "term_side": "appellation",
                        "residual_pairs": "1",
                        "frontier_pairs": "1",
                        "concepts": "WRR2 32",
                        "impact_statuses": "1 no_blocking_term_variant_hit",
                        "row_ocr_pair_statuses": "1 mixed",
                        "review_buckets": "ocr_not_matched_no_variant_lead",
                        "term_ocr_statuses": "not_matched",
                        "source_flags": "wnp_chelm_spelling_context",
                        "source_review_action": "source/pair-rule review",
                        "visual_review_action": "",
                        "source_queue_rank": "83",
                        "source_queue_bucket": "ocr_not_matched_no_variant_lead",
                        "source_queue_ocr_status": "not_matched",
                        "source_queue_row_ocr_basis": "row OCR",
                        "source_queue_best_variant_hits": "0",
                        "source_queue_best_variant_rule": "none",
                        "source_queue_best_variant_normalized": "",
                        "source_queue_pair_ids": "p1",
                        "pair_ids": "p1",
                        "reconciliation_need": "source_policy_or_pair_rule_review",
                        "read": "term carries source-policy context",
                    },
                    {
                        "run_label": "all_lanes_cap1000",
                        "priority_rank": "2",
                        "term_id": "wrr2_27_app_13",
                        "term": "B@LQWLHRMZ",
                        "term_side": "appellation",
                        "residual_pairs": "2",
                        "frontier_pairs": "1",
                        "concepts": "WRR2 27",
                        "impact_statuses": "2 no_blocking_term_variant_hit",
                        "row_ocr_pair_statuses": "1 mixed",
                        "review_buckets": "ocr_not_matched_no_variant_lead",
                        "term_ocr_statuses": "not_matched",
                        "source_flags": "",
                        "source_review_action": "",
                        "visual_review_action": "",
                        "source_queue_rank": "40",
                        "source_queue_bucket": "ocr_not_matched_no_variant_lead",
                        "source_queue_ocr_status": "not_matched",
                        "source_queue_row_ocr_basis": "row OCR",
                        "source_queue_best_variant_hits": "0",
                        "source_queue_best_variant_rule": "none",
                        "source_queue_best_variant_normalized": "",
                        "source_queue_pair_ids": "p2;p3",
                        "pair_ids": "p2;p3",
                        "reconciliation_need": "source_transcription_or_row_alignment",
                        "read": "term has no simple variant lead",
                    },
                ],
            )

            rc = plan.main(
                [
                    "--residual-term-queue",
                    str(queue),
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
            self.assertEqual(rows[0]["action_lane"], "source_policy_or_pair_rule_review")
            self.assertEqual(rows[1]["action_lane"], "source_transcription_or_row_alignment")
            summary_rows = list(csv.DictReader(summary.open(encoding="utf-8")))
            self.assertEqual(len(summary_rows), 2)
            self.assertIn(
                "WRR Residual Reconciliation Action Plan",
                markdown.read_text(encoding="utf-8"),
            )
            manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(manifest_payload["action_rows"], 2)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
