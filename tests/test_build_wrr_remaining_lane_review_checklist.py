import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_remaining_lane_review_checklist as checklist


class WrrRemainingLaneReviewChecklistTests(unittest.TestCase):
    def test_build_checklist_rows_assigns_lane_states(self) -> None:
        rows = checklist.build_checklist_rows(
            [
                packet_row("1", "page_image_near_match_review", "wrr2_19_app_11", "1"),
                packet_row("4", "method_or_pair_universe_review", "wrr2_02_app_03", "1"),
            ]
        )

        self.assertEqual(rows[0]["review_state"], "pending_page_image_lock")
        self.assertEqual(
            rows[1]["review_state"],
            "pending_method_pair_universe_lock",
        )
        self.assertEqual(rows[0]["allowed_without_input"], "organize evidence only")
        self.assertIn("No source correction", rows[0]["no_input_boundary"])

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet = root / "packet.csv"
            summary = root / "summary.csv"
            out = root / "checklist.csv"
            md = root / "checklist.md"
            manifest = root / "manifest.json"
            write_csv(
                packet,
                [
                    packet_row("1", "page_image_near_match_review", "wrr2_19_app_11", "1"),
                    packet_row("4", "method_or_pair_universe_review", "wrr2_02_app_03", "1"),
                ],
            )
            write_csv(
                summary,
                [
                    summary_row("page_image_near_match_review", "1"),
                    summary_row("method_or_pair_universe_review", "1"),
                ],
            )

            rc = checklist.main(
                [
                    "--packet",
                    str(packet),
                    "--summary",
                    str(summary),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(md),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 2)
            self.assertIn(
                "WRR Remaining-Lane Review Checklist",
                md.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 2)
            self.assertEqual(payload["frontier_pairs"], 2)


def packet_row(
    rank: str,
    lane: str,
    term_id: str,
    frontier_pairs: str,
) -> dict[str, str]:
    return {
        "run_label": "all_lanes_cap1000",
        "evidence_rank": rank,
        "action_lane": lane,
        "term_id": term_id,
        "term": "YWSP+RANY" if "19" in term_id else "ZR@ABRHM",
        "concept": "WRR2 19" if "19" in term_id else "WRR2 02",
        "row_number": "19" if "19" in term_id else "02",
        "residual_pairs": "1",
        "frontier_pairs": frontier_pairs,
        "row_ocr_status": "not_matched" if "19" in term_id else "matched",
        "row_ocr_near_match_distance": "1" if "19" in term_id else "0",
        "row_ocr_near_match_text": "יוספטרני" if "19" in term_id else "זרעאברהמ",
        "visual_review_note": "primary page row visibly contains Trani forms"
        if "19" in term_id
        else "",
        "evidence_required": "page-image inspection against near-match OCR"
        if lane == "page_image_near_match_review"
        else "method or pair-universe review for OCR-matched missing ordinary hits",
    }


def summary_row(lane: str, frontier_pairs: str) -> dict[str, str]:
    return {
        "action_lane": lane,
        "action_terms": "1",
        "residual_pairs": "1",
        "frontier_pairs": frontier_pairs,
        "evidence_required": "page-image inspection against near-match OCR"
        if lane == "page_image_near_match_review"
        else "method or pair-universe review for OCR-matched missing ordinary hits",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
