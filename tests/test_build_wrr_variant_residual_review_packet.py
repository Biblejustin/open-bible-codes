import csv
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_variant_residual_review_packet as packet


class WrrVariantResidualReviewPacketTests(unittest.TestCase):
    def test_build_detail_rows_keeps_only_residual_pool(self) -> None:
        upper = {
            "run_label": "all_lanes_cap1000",
            "residual_gap_after_simple_variant_upper_bound": "1",
        }
        blocked = {
            "p1": {
                "pair_id": "p1",
                "candidate_lane": "length_5_8_smoke_candidate",
                "pair_review_status": "needs_primary_source_pair_rule",
                "appellation_term_id": "app1",
                "appellation_term": "APP",
                "appellation_ordinary_hits": "0",
                "date_term_id": "wrr2_01_date_01",
                "date_term": "DATE",
                "date_ordinary_hits": "0",
            },
            "p2": {
                "pair_id": "p2",
                "candidate_lane": "appellation_min_length_candidate",
                "pair_review_status": "needs_primary_source_pair_rule",
            },
        }
        variants = [
            {
                "run_label": "all_lanes_cap1000",
                "pair_id": "p0",
                "concept": "WRR2 00",
                "reason": "ordinary_missing_appellation_hits",
                "row_ocr_pair_status": "mixed",
                "impact_status": "all_blocking_terms_have_variant_hit",
                "blocking_term_ids": "app0",
                "blocking_terms": "APP0",
                "blocking_term_variant_hits": "3",
                "blocking_term_variant_rules": "delete_one@1:PP0",
            },
            {
                "run_label": "all_lanes_cap1000",
                "pair_id": "p1",
                "concept": "WRR2 01",
                "reason": "ordinary_missing_both_terms",
                "row_ocr_pair_status": "both_not_matched",
                "impact_status": "some_blocking_terms_have_variant_hit",
                "blocking_term_ids": "app1;wrr2_01_date_01",
                "blocking_terms": "APP;DATE",
                "blocking_term_variant_hits": "2;0",
                "blocking_term_variant_rules": "delete_one@1:PP;none",
            },
            {
                "run_label": "all_lanes_cap1000",
                "pair_id": "p2",
                "concept": "WRR2 02",
                "reason": "ordinary_missing_appellation_hits",
                "row_ocr_pair_status": "both_matched",
                "impact_status": "no_blocking_term_variant_hit",
                "blocking_term_ids": "app2",
                "blocking_terms": "APP2",
                "blocking_term_variant_hits": "0",
                "blocking_term_variant_rules": "none",
            },
        ]
        source_rows = {
            "wrr2_01_date_01": {
                "term_id": "wrr2_01_date_01",
                "review_bucket": "ocr_not_matched_no_variant_lead",
                "row_ocr_status": "not_matched",
                "source_review_flags": "flagged",
                "visual_review_action": "check page",
            },
        }

        rows = packet.build_detail_rows(
            blocked_rows=blocked,
            variant_rows=variants,
            source_rows=source_rows,
            upper=upper,
        )

        self.assertEqual([row["pair_id"] for row in rows], ["p1", "p2"])
        self.assertEqual(rows[0]["unresolved_term_ids"], "wrr2_01_date_01")
        self.assertEqual(rows[0]["unresolved_term_sides"], "date")
        self.assertEqual(rows[0]["within_minimum_residual_frontier"], "true")
        self.assertEqual(rows[1]["within_minimum_residual_frontier"], "false")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            blocked = root / "blocked.csv"
            variants = root / "variants.csv"
            source_queue = root / "source_queue.csv"
            upper = root / "upper.csv"
            out = root / "out.csv"
            summary = root / "summary.csv"
            markdown = root / "out.md"
            manifest = root / "manifest.json"
            write_csv(
                blocked,
                [
                    {
                        "pair_id": "p1",
                        "candidate_lane": "length_5_8_smoke_candidate",
                        "pair_review_status": "needs_primary_source_pair_rule",
                        "appellation_term_id": "app1",
                        "appellation_term": "APP",
                        "appellation_ordinary_hits": "0",
                        "date_term_id": "date1",
                        "date_term": "DATE",
                        "date_ordinary_hits": "0",
                    }
                ],
            )
            write_csv(
                variants,
                [
                    {
                        "run_label": "all_lanes_cap1000",
                        "pair_id": "p1",
                        "concept": "WRR2 01",
                        "reason": "ordinary_missing_both_terms",
                        "row_ocr_pair_status": "mixed",
                        "impact_status": "no_blocking_term_variant_hit",
                        "blocking_term_ids": "app1;date1",
                        "blocking_terms": "APP;DATE",
                        "blocking_term_variant_hits": "0;0",
                        "blocking_term_variant_rules": "none;none",
                    }
                ],
            )
            write_csv(
                source_queue,
                [
                    {
                        "term_id": "app1",
                        "review_bucket": "ocr_matched_no_variant_lead",
                        "row_ocr_status": "matched",
                        "source_review_flags": "",
                        "visual_review_action": "",
                    },
                    {
                        "term_id": "date1",
                        "review_bucket": "ocr_not_matched_no_variant_lead",
                        "row_ocr_status": "not_matched",
                        "source_review_flags": "",
                        "visual_review_action": "",
                    },
                ],
            )
            write_csv(
                upper,
                [
                    {
                        "run_label": "all_lanes_cap1000",
                        "current_defined_distances": "72",
                        "source_cited_defined_distances": "163",
                        "upper_bound_defined_distances": "123",
                        "residual_gap_after_simple_variant_upper_bound": "1",
                    }
                ],
            )

            rc = packet.main(
                [
                    "--blocked-pairs",
                    str(blocked),
                    "--variant-impact",
                    str(variants),
                    "--source-queue",
                    str(source_queue),
                    "--upper-bound",
                    str(upper),
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
            self.assertEqual(rows[0]["candidate_pool_pairs"], "1")
            summary_rows = list(csv.DictReader(summary.open(encoding="utf-8")))
            self.assertEqual(summary_rows[0]["residual_needed"], "1")
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("WRR Variant Residual Review Packet", text)
            self.assertTrue(manifest.exists())


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
