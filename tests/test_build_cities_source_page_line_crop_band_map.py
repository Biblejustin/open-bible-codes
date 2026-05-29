import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_source_page_line_crop_band_map as bands
from scripts import build_cities_source_page_line_crop_packet as packet
from scripts import build_cities_source_page_line_crop_triage as triage


class CitiesSourcePageLineCropBandMapTests(unittest.TestCase):
    def test_build_band_rows_splits_on_gap_threshold(self) -> None:
        packet_rows = [
            packet_row("1", top=10, bottom=20),
            packet_row("2", top=25, bottom=35),
            packet_row("3", top=90, bottom=100),
        ]
        triage_rows = [triage_row("1"), triage_row("2"), triage_row("3")]

        rows = bands.build_band_rows(packet_rows, triage_rows, gap_threshold=40)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["first_page_line_rank"], "1")
        self.assertEqual(rows[0]["last_page_line_rank"], "2")
        self.assertEqual(rows[1]["gap_before_band_px"], "55")

    def test_build_band_rows_keeps_zero_result_work(self) -> None:
        rows = bands.build_band_rows([packet_row("1", top=10, bottom=20)], [triage_row("1")])

        self.assertEqual(rows[0]["source_row_import"], "0")
        self.assertEqual(rows[0]["city_name_normalization"], "0")
        self.assertEqual(rows[0]["els_runs"], "0")
        self.assertEqual(rows[0]["p_levels"], "0")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet_csv = root / "packet.csv"
            triage_csv = root / "triage.csv"
            out = root / "bands.csv"
            summary = root / "summary.csv"
            markdown = root / "bands.md"
            manifest = root / "manifest.json"
            write_csv(packet_csv, packet.FIELDNAMES, [packet_row("1", top=10, bottom=20)])
            write_csv(triage_csv, triage.FIELDNAMES, [triage_row("1")])

            rc = bands.main(
                [
                    "--packet",
                    str(packet_csv),
                    "--triage",
                    str(triage_csv),
                    "--gap-threshold",
                    "40",
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
            self.assertTrue(out.exists())
            self.assertIn(
                "Cities Source Page Line Crop Band Map",
                markdown.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["source_row_imports"], 0)


def packet_row(rank: str, *, top: int, bottom: int) -> dict[str, str]:
    return {
        "line_rank": rank,
        "transcription_decision_id": "cities_source_transcription_001",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "page_line_rank": rank,
        "page_image_path": "page.png",
        "tsv_path": "page.tsv",
        "tsv_exists": "true",
        "line_left": "10",
        "line_top": str(top),
        "line_right": "100",
        "line_bottom": str(bottom),
        "line_width": "90",
        "line_height": str(bottom - top),
        "crop_left": "0",
        "crop_top": str(top - 5),
        "crop_right": "120",
        "crop_bottom": str(bottom + 5),
        "crop_width": "120",
        "crop_height": str(bottom - top + 10),
        "crop_path": f"line{rank}.png",
        "crop_exists": "true",
        "ocr_word_count": "4",
        "ocr_hebrew_letters": "12",
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "no_input_boundary": packet.NO_INPUT_BOUNDARY,
        "next_manual_action": "review only",
    }


def triage_row(rank: str) -> dict[str, str]:
    return {
        "triage_rank": rank,
        "source_order": rank,
        "line_rank": rank,
        "transcription_decision_id": "cities_source_transcription_001",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "page_line_rank": rank,
        "crop_path": f"line{rank}.png",
        "crop_exists": "true",
        "line_width": "90",
        "line_height": "10",
        "crop_height": "20",
        "ocr_word_count": "4",
        "ocr_hebrew_letters": "12",
        "review_priority": "priority_2_medium_text",
        "review_bucket": "likely_row_or_header",
        "triage_reason": "medium OCR signal",
        "allowed_without_input": "rank line-crop visual review only",
        "next_manual_action": "review crop image",
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "claim_boundary": triage.CLAIM_BOUNDARY,
    }


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
