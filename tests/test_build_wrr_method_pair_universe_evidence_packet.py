import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_method_pair_universe_evidence_packet as packet


class WrrMethodPairUniverseEvidencePacketTests(unittest.TestCase):
    def test_build_packet_rows_keeps_method_lane_and_joined_counts(self) -> None:
        rows = packet.build_packet_rows(
            [
                remaining_row("method_or_pair_universe_review", "wrr2_02_app_03"),
                remaining_row("page_image_near_match_review", "wrr2_19_app_11"),
            ],
            {
                "wrr2_02_app_03": {
                    "term_id": "wrr2_02_app_03",
                    "pair_ids": "wrr2_02_app_03__wrr2_02_date_01",
                    "review_bucket": "ocr_matched_no_variant_lead",
                    "blocking_reasons": "1 ordinary_missing_both_terms",
                }
            },
            {"wrr2_02_app_03": {"term_id": "wrr2_02_app_03", "hit_count": "0"}},
            {
                "wrr2_02_app_03__wrr2_02_date_01": {
                    "pair_id": "wrr2_02_app_03__wrr2_02_date_01",
                    "date_term_id": "wrr2_02_date_01",
                    "appellation_ordinary_hits": "0",
                    "date_ordinary_hits": "0",
                    "pair_valid_perturbations": "0",
                    "corrected_distance_status": "ordinary_not_valid",
                }
            },
        )
        summary = packet.build_summary_rows(rows)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["base_skip_250_hit_count"], 0)
        self.assertEqual(rows[0]["highcap_appellation_ordinary_hits"], 0)
        self.assertIn("both sides have zero", rows[0]["diagnostic_read"])
        self.assertEqual(summary[0]["action_terms"], 1)
        self.assertEqual(summary[0]["both_sides_zero_highcap_pairs"], 1)

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            remaining = root / "remaining.csv"
            source = root / "source.csv"
            counts = root / "counts.csv"
            corrected = root / "corrected.csv"
            out = root / "packet.csv"
            summary = root / "summary.csv"
            markdown = root / "packet.md"
            manifest = root / "manifest.json"
            write_csv(remaining, [remaining_row("method_or_pair_universe_review", "wrr2_02_app_03")])
            write_csv(
                source,
                [
                    {
                        "term_id": "wrr2_02_app_03",
                        "pair_ids": "wrr2_02_app_03__wrr2_02_date_01",
                        "review_bucket": "ocr_matched_no_variant_lead",
                        "blocking_reasons": "1 ordinary_missing_both_terms",
                    }
                ],
            )
            write_csv(counts, [{"term_id": "wrr2_02_app_03", "hit_count": "0"}])
            write_csv(
                corrected,
                [
                    {
                        "pair_id": "wrr2_02_app_03__wrr2_02_date_01",
                        "date_term_id": "wrr2_02_date_01",
                        "appellation_ordinary_hits": "0",
                        "date_ordinary_hits": "0",
                        "pair_valid_perturbations": "0",
                        "corrected_distance_status": "ordinary_not_valid",
                    }
                ],
            )

            rc = packet.main(
                [
                    "--remaining-packet",
                    str(remaining),
                    "--source-queue",
                    str(source),
                    "--counts",
                    str(counts),
                    "--corrected-distance",
                    str(corrected),
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
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 1)
            self.assertIn(
                "WRR Method/Pair-Universe Evidence Packet",
                markdown.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["packet_rows"], 1)


def remaining_row(lane: str, term_id: str) -> dict[str, str]:
    return {
        "run_label": "all_lanes_cap1000",
        "evidence_rank": "1",
        "action_rank": "1",
        "action_lane": lane,
        "term_id": term_id,
        "term": "ZR@ABRHM",
        "concept": "WRR2 02",
        "row_number": "02",
        "residual_pairs": "1",
        "frontier_pairs": "1",
        "review_buckets": "ocr_matched_no_variant_lead",
        "row_ocr_status": "matched",
        "best_variant_hit_count": "0",
        "best_variant_rule": "none",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
