import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_source_transcription_evidence_packet as packet


class WrrSourceTranscriptionEvidencePacketTests(unittest.TestCase):
    def test_build_packet_rows_joins_row_ocr_context(self) -> None:
        action_rows = [
            action_row("2", "wrr2_06_app_03", "B@LM@$YH$M"),
            action_row("3", "wrr2_06_app_04", "B@LM@$YYHWH"),
        ]
        source_rows = [
            source_row("wrr2_06_app_03", "B@LM@$YH$M"),
            source_row("wrr2_06_app_04", "B@LM@$YYHWH"),
        ]
        ocr_rows = [
            row_ocr("wrr2_06_app_01", "ALY@ZR", "matched", "name"),
            row_ocr("wrr2_06_app_03", "B@LM@$YH$M", "not_matched", "name"),
            row_ocr("wrr2_06_app_04", "B@LM@$YYHWH", "not_matched", "name"),
            row_ocr("wrr2_06_date_01", "/KB/TBT", "matched", "date"),
        ]
        bridge_rows = [
            {
                "row_number": "6",
                "current_read": "Primary English row label and secondary WRR2 record align.",
            }
        ]

        rows = packet.build_packet_rows(action_rows, source_rows, ocr_rows, bridge_rows)
        summary = packet.build_row_summary_rows(rows, ocr_rows)

        self.assertEqual(len(rows), 2)
        self.assertIn("wrr2_06_app_01 ALY@ZR", rows[0]["row_matched_terms"])
        self.assertIn("wrr2_06_app_03 B@LM@$YH$M", rows[0]["row_action_not_matched_terms"])
        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0]["action_terms"], 2)
        self.assertEqual(summary[0]["frontier_pairs"], 2)
        self.assertIn("multi-term row cluster", summary[0]["read"])

    def test_main_writes_packet_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            action = root / "action.csv"
            source = root / "source.csv"
            ocr = root / "ocr.csv"
            bridge = root / "bridge.csv"
            out = root / "packet.csv"
            row_summary = root / "rows.csv"
            md = root / "packet.md"
            manifest = root / "manifest.json"
            write_csv(action, [action_row("2", "wrr2_06_app_03", "B@LM@$YH$M")])
            write_csv(source, [source_row("wrr2_06_app_03", "B@LM@$YH$M")])
            write_csv(
                ocr,
                [
                    row_ocr("wrr2_06_app_01", "ALY@ZR", "matched", "name"),
                    row_ocr("wrr2_06_app_03", "B@LM@$YH$M", "not_matched", "name"),
                    row_ocr("wrr2_06_date_01", "/KB/TBT", "matched", "date"),
                ],
            )
            write_csv(
                bridge,
                [
                    {
                        "row_number": "6",
                        "current_read": "Primary English row label and secondary WRR2 record align.",
                    }
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
                    "--table2-bridge",
                    str(bridge),
                    "--out",
                    str(out),
                    "--row-summary-out",
                    str(row_summary),
                    "--markdown-out",
                    str(md),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 1)
            self.assertEqual(
                len(list(csv.DictReader(row_summary.open(encoding="utf-8")))), 1
            )
            self.assertIn(
                "WRR Source-Transcription Evidence Packet",
                md.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["packet_rows"], 1)


def action_row(action_rank: str, term_id: str, term: str) -> dict[str, str]:
    return {
        "run_label": "all_lanes_cap1000",
        "action_rank": action_rank,
        "action_lane": "source_transcription_or_row_alignment",
        "term_id": term_id,
        "term": term,
        "residual_pairs": "1",
        "frontier_pairs": "1",
        "review_buckets": "ocr_not_matched_no_variant_lead",
        "source_queue_best_variant_hits": "0",
        "source_queue_best_variant_rule": "none",
    }


def source_row(term_id: str, term: str) -> dict[str, str]:
    return {
        "term_id": term_id,
        "term": term,
        "concepts": "WRR2 06",
        "row_numbers": "06",
        "row_ocr_status": "not_matched",
        "row_ocr_text_normalized": "אליעזר",
        "best_variant_hit_count": "0",
        "best_variant_rule": "none",
    }


def row_ocr(term_id: str, term: str, status: str, column: str) -> dict[str, str]:
    return {
        "term_id": term_id,
        "row_number": "06",
        "concept": "WRR2 06",
        "category": "wrr_appellation" if "_app_" in term_id else "wrr_date",
        "michigan_term": term,
        "row_ocr_status": status,
        "column": column,
        "row_ocr_text_normalized": "אליעזר",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
