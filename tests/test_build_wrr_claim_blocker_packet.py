import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_claim_blocker_packet as packet


class WrrClaimBlockerPacketTests(unittest.TestCase):
    def test_build_packet_rows_combines_readiness_options_and_source_flags(self) -> None:
        rows = packet.build_packet_rows(
            readiness_rows=[
                {
                    "decision_area": "Pair universe",
                    "status": "open",
                    "ready": "false",
                    "blocker": "Pair universe blocked",
                },
                {
                    "decision_area": "D(w) skip-cap formula",
                    "status": "open",
                    "ready": "false",
                    "blocker": "D blocked",
                },
                {
                    "decision_area": "Aggregate statistic and permutation",
                    "status": "claim_grade_ready",
                    "ready": "true",
                    "blocker": "",
                },
            ],
            lock_rows=[
                {
                    "area": "Pair universe",
                    "option": "working input",
                    "status": "diagnostic_only",
                },
                {
                    "area": "D(w) skip-cap formula",
                    "option": "printed",
                    "status": "primary_text_default",
                },
            ],
            source_rows=[
                {"source_review_flags": "wnp_disputed_zacut_appellation"},
                {"source_review_flags": "wnp_chelm_spelling_context"},
            ],
            method_rows=[
                {
                    "decision_area": "Pair universe",
                    "current_read": "pair read",
                },
                {
                    "decision_area": "D(w) skip-cap formula",
                    "current_read": "formula read",
                },
            ],
        )

        self.assertEqual(len(rows), 2)
        by_area = {row["decision_area"]: row for row in rows}
        self.assertIn("working input [diagnostic_only]", by_area["Pair universe"]["available_options"])
        self.assertIn("2 flagged queued terms", by_area["Pair universe"]["source_review_flags"])
        self.assertEqual(by_area["Pair universe"]["current_read"], "pair read")
        self.assertIn("printed", by_area["D(w) skip-cap formula"]["available_options"])
        self.assertEqual(by_area["D(w) skip-cap formula"]["source_review_flags"], "")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            readiness = root / "readiness.csv"
            lock_options = root / "lock_options.csv"
            source_queue = root / "source_queue.csv"
            method_status = root / "method_status.csv"
            source_policy_scenarios = root / "source_policy_scenarios.csv"
            source_policy_term_impacts = root / "source_policy_term_impacts.csv"
            dw_formula_sensitivity = root / "dw_formula_sensitivity.csv"
            variant_residual_summary = root / "variant_residual_summary.csv"
            variant_residual_packet = root / "variant_residual_packet.csv"
            residual_term_summary = root / "residual_term_summary.csv"
            residual_term_queue = root / "residual_term_queue.csv"
            out = root / "packet.csv"
            markdown = root / "packet.md"
            manifest = root / "manifest.json"
            write_csv(
                readiness,
                [
                    {
                        "decision_area": "Pair universe",
                        "status": "open",
                        "required_statuses": "locked,source_locked",
                        "ready": "false",
                        "blocker": "Pair universe blocked",
                    }
                ],
            )
            write_csv(
                lock_options,
                [
                    {
                        "area": "Pair universe",
                        "option": "working input",
                        "status": "diagnostic_only",
                    }
                ],
            )
            write_csv(
                source_queue,
                [
                    {
                        "priority_rank": "7",
                        "term_id": "wrr2_27_app_06",
                        "term": "M$HZKWTW",
                        "review_bucket": "ocr_near_match_with_variant_lead",
                        "source_review_flags": "wnp_disputed_zacut_appellation",
                        "source_review_action": "diagnostic flag only",
                        "visual_review_note": "primary page row visibly contains Moshe/Zacut forms",
                        "visual_review_action": "check page image before treating as source difference",
                    }
                ],
            )
            write_csv(
                method_status,
                [
                    {
                        "decision_area": "Pair universe",
                        "status": "open",
                        "current_read": "pair read",
                    }
                ],
            )
            write_csv(
                source_policy_scenarios,
                [
                    {
                        "scenario": "exclude_wnp_zacut_only",
                        "policy_type": "diagnostic_exclusion",
                        "excluded_pairs": "8",
                        "remaining_appellation_min_length_pairs": "157",
                        "gap_to_source_cited_163_after_appellation_min_length": "6",
                        "remaining_length_filtered_pairs": "78",
                    }
                ],
            )
            write_csv(
                source_policy_term_impacts,
                [
                    {
                        "term_id": "wrr2_27_app_02",
                        "term": "ZKWTA",
                        "flags": "wnp_disputed_zacut_appellation",
                        "affected_appellation_min_length_pairs": "2",
                        "remaining_appellation_min_length_pairs_if_excluded": "163",
                        "gap_to_source_cited_163_after_appellation_min_length_if_excluded": "0",
                        "closes_appellation_min_length_gap_to_163": "true",
                        "diagnostic_read": "single-term exclusion closes >=5 count gap",
                    }
                ],
            )
            write_csv(
                dw_formula_sensitivity,
                [
                    {
                        "scope": "all_lanes_cap1000",
                        "row_count": "182",
                        "printed_defined_corrected_distances": "72",
                        "program_defined_corrected_distances": "72",
                        "changed_pairs": "0",
                        "diagnostic_read": "row-level printed/program comparison",
                    }
                ],
            )
            write_csv(
                variant_residual_summary,
                [
                    {
                        "run_label": "all_lanes_cap1000",
                        "group": "residual_pool",
                        "value": "candidate_pairs_not_closed_by_all-blocker_simple_variants",
                        "pairs": "59",
                        "residual_needed": "40",
                        "candidate_pool_pairs": "59",
                        "residual_slack_pairs": "19",
                        "read": "at least residual_needed rows from this pool need source-rule or method resolution",
                    },
                    {
                        "run_label": "all_lanes_cap1000",
                        "group": "review_frontier",
                        "value": "minimum_residual_frontier",
                        "pairs": "40",
                        "residual_needed": "40",
                        "candidate_pool_pairs": "59",
                        "residual_slack_pairs": "19",
                        "read": "frontier is a deterministic review priority",
                    },
                ],
            )
            write_csv(
                variant_residual_packet,
                [
                    {
                        "review_rank": "1",
                        "within_minimum_residual_frontier": "true",
                        "pair_id": "wrr2_27_app_13__wrr2_27_date_01",
                        "concept": "WRR2 27",
                        "impact_status": "some_blocking_terms_have_variant_hit",
                        "row_ocr_pair_status": "both_not_matched",
                        "unresolved_terms": "B@LQWLHRMZ",
                        "unresolved_source_flags": "",
                    }
                ],
            )
            write_csv(
                residual_term_summary,
                [
                    {
                        "run_label": "all_lanes_cap1000",
                        "group": "residual_terms",
                        "value": "unique_unresolved_terms",
                        "terms": "58",
                        "residual_pairs": "59",
                        "frontier_pairs": "40",
                        "read": "unique unresolved term targets collapsed from residual pair rows",
                    },
                    {
                        "run_label": "all_lanes_cap1000",
                        "group": "reconciliation_need",
                        "value": "source_policy_or_pair_rule_review",
                        "terms": "1",
                        "residual_pairs": "1",
                        "frontier_pairs": "1",
                        "read": "residual term queue breakdown; diagnostic only",
                    },
                ],
            )
            write_csv(
                residual_term_queue,
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
                        "source_queue_pair_ids": "wrr2_32_app_05__wrr2_32_date_01",
                        "pair_ids": "wrr2_32_app_05__wrr2_32_date_01",
                        "reconciliation_need": "source_policy_or_pair_rule_review",
                        "read": "term carries source-policy context",
                    }
                ],
            )

            rc = packet.main(
                [
                    "--readiness",
                    str(readiness),
                    "--lock-options",
                    str(lock_options),
                    "--source-queue",
                    str(source_queue),
                    "--method-status",
                    str(method_status),
                    "--source-policy-scenarios",
                    str(source_policy_scenarios),
                    "--source-policy-term-impacts",
                    str(source_policy_term_impacts),
                    "--dw-formula-sensitivity",
                    str(dw_formula_sensitivity),
                    "--variant-residual-summary",
                    str(variant_residual_summary),
                    "--variant-residual-packet",
                    str(variant_residual_packet),
                    "--residual-term-summary",
                    str(residual_term_summary),
                    "--residual-term-queue",
                    str(residual_term_queue),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            rows = list(csv.DictReader(out.open(encoding="utf-8")))
            self.assertEqual(rows[0]["decision_area"], "Pair universe")
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("WRR Claim Blocker Packet", text)
            self.assertIn("Flagged Source-Review Rows", text)
            self.assertIn("Visual Triage Highlights", text)
            self.assertIn("primary page row visibly contains Moshe/Zacut forms", text)
            self.assertIn("No visual-review note excludes a pair automatically", text)
            self.assertIn("Source Policy Scenario Impact", text)
            self.assertIn("Single-Term Source Policy Impact", text)
            self.assertIn("wrr2_27_app_02", text)
            self.assertIn("D(w) Formula Sensitivity", text)
            self.assertIn("Exact-WRR Residual Caveat", text)
            self.assertIn("Residual Frontier Sample", text)
            self.assertIn("wrr2_27_app_13__wrr2_27_date_01", text)
            self.assertIn("Residual Term Queue", text)
            self.assertIn("Top Residual Term Targets", text)
            self.assertIn("wrr2_32_app_05", text)
            self.assertIn("source_policy_or_pair_rule_review", text)
            self.assertIn("wnp_chelm_spelling_context", text)
            self.assertIn("exclude_wnp_zacut_only", text)
            self.assertIn("all_lanes_cap1000", text)
            self.assertIn("Pair universe lock: keep_all_working_source", text)
            self.assertIn("D(w) lock: printed WRR formula main", text)
            self.assertTrue(manifest.exists())
            manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(manifest_payload["residual_term_summary_rows"], 2)
            self.assertEqual(manifest_payload["residual_term_queue_rows"], 1)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
