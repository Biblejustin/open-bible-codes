import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_remaining_lane_evidence_packets as packet


class WrrRemainingLaneEvidencePacketTests(unittest.TestCase):
    def test_build_packet_rows_keeps_remaining_lanes(self) -> None:
        rows = packet.build_packet_rows(
            [
                action_row("45", "page_image_near_match_review", "wrr2_19_app_11", "YWSP+RANY"),
                action_row("48", "method_or_pair_universe_review", "wrr2_02_app_03", "ZR@ABRHM"),
                action_row("2", "source_transcription_or_row_alignment", "wrr2_01_app_06", "B@LHA$KWL"),
            ],
            [
                source_row("wrr2_19_app_11", "WRR2 19", "not_matched", "1", "יוסףטרני"),
                source_row("wrr2_02_app_03", "WRR2 02", "matched", "", ""),
            ],
            [
                row_ocr("wrr2_19_app_11", "WRR2 19", "not_matched"),
                row_ocr("wrr2_02_app_03", "WRR2 02", "matched"),
            ],
        )
        summary = packet.build_summary_rows(rows)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["action_lane"], "page_image_near_match_review")
        self.assertIn("page-image", rows[0]["evidence_required"])
        self.assertIn("visual note", rows[0]["visual_review_note"])
        self.assertEqual(rows[1]["action_lane"], "method_or_pair_universe_review")
        self.assertEqual(len(summary), 2)

    def test_main_writes_packet_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            action = root / "action.csv"
            source = root / "source.csv"
            ocr = root / "ocr.csv"
            out = root / "packet.csv"
            summary = root / "summary.csv"
            md = root / "packet.md"
            manifest = root / "manifest.json"
            write_csv(
                action,
                [
                    action_row("45", "page_image_near_match_review", "wrr2_19_app_11", "YWSP+RANY"),
                    action_row("48", "method_or_pair_universe_review", "wrr2_02_app_03", "ZR@ABRHM"),
                ],
            )
            write_csv(
                source,
                [
                    source_row("wrr2_19_app_11", "WRR2 19", "not_matched", "1", "יוסףטרני"),
                    source_row("wrr2_02_app_03", "WRR2 02", "matched", "", ""),
                ],
            )
            write_csv(
                ocr,
                [
                    row_ocr("wrr2_19_app_11", "WRR2 19", "not_matched"),
                    row_ocr("wrr2_02_app_03", "WRR2 02", "matched"),
                ],
            )

            rc = packet.main(
                [
                    "--action-plan",
                    str(action),
                    "--source-queue",
                    str(source),
                    "--row-ocr",
                    str(ocr),
                    "--out",
                    str(out),
                    "--summary-out",
                    str(summary),
                    "--markdown-out",
                    str(md),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 2)
            self.assertEqual(len(list(csv.DictReader(summary.open(encoding="utf-8")))), 2)
            self.assertIn("WRR Remaining-Lane Evidence Packets", md.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["packet_rows"], 2)


def action_row(action_rank: str, lane: str, term_id: str, term: str) -> dict[str, str]:
    return {
        "run_label": "all_lanes_cap1000",
        "action_rank": action_rank,
        "action_lane": lane,
        "term_id": term_id,
        "term": term,
        "residual_pairs": "1",
        "frontier_pairs": "1",
        "review_buckets": "ocr_near_match_no_variant_lead",
        "source_queue_best_variant_hits": "0",
        "source_queue_best_variant_rule": "none",
    }


def source_row(
    term_id: str, concept: str, status: str, distance: str, near_text: str
) -> dict[str, str]:
    return {
        "term_id": term_id,
        "concepts": concept,
        "row_numbers": concept.split()[-1],
        "row_ocr_status": status,
        "row_ocr_near_match_distance": distance,
        "row_ocr_near_match_text": near_text,
        "best_variant_hit_count": "0",
        "best_variant_rule": "none",
        "visual_review_note": "visual note",
        "visual_review_action": "visual action",
    }


def row_ocr(term_id: str, concept: str, status: str) -> dict[str, str]:
    return {
        "term_id": term_id,
        "row_number": concept.split()[-1],
        "concept": concept,
        "michigan_term": "TERM",
        "row_ocr_status": status,
        "row_ocr_text_normalized": "normalized",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
