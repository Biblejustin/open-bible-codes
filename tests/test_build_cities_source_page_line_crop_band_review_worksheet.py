import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_source_page_line_crop_band_map as bands
from scripts import build_cities_source_page_line_crop_band_review_worksheet as worksheet


class CitiesSourcePageLineCropBandReviewWorksheetTests(unittest.TestCase):
    def test_build_review_rows_keeps_band_identity(self) -> None:
        rows = worksheet.build_review_rows([band_row("1")])

        self.assertEqual(rows[0]["review_rank"], "1")
        self.assertEqual(rows[0]["band_review_id"], "cities_source_band_review_001")
        self.assertEqual(rows[0]["band_id"], "cities_source_line_band_001")

    def test_build_review_rows_keeps_zero_result_work(self) -> None:
        rows = worksheet.build_review_rows([band_row("1")])

        self.assertEqual(rows[0]["source_row_import"], "0")
        self.assertEqual(rows[0]["city_name_normalization"], "0")
        self.assertEqual(rows[0]["els_runs"], "0")
        self.assertEqual(rows[0]["p_levels"], "0")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            band_csv = root / "bands.csv"
            out = root / "worksheet.csv"
            summary = root / "summary.csv"
            markdown = root / "worksheet.md"
            manifest = root / "manifest.json"
            write_csv(band_csv, bands.FIELDNAMES, [band_row("1")])

            rc = worksheet.main(
                [
                    "--band-map",
                    str(band_csv),
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
                "Cities Source Page Line Crop Band Review Worksheet",
                markdown.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["source_row_imports"], 0)


def band_row(rank: str) -> dict[str, str]:
    return {
        "band_rank": rank,
        "band_id": f"cities_source_line_band_{int(rank):03d}",
        "transcription_decision_id": "cities_source_transcription_001",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "page_band_rank": rank,
        "gap_threshold_px": "40",
        "gap_before_band_px": "0",
        "first_line_rank": "1",
        "last_line_rank": "2",
        "first_page_line_rank": "1",
        "last_page_line_rank": "2",
        "line_crop_rows": "2",
        "crop_images_available": "2",
        "band_top": "10",
        "band_bottom": "50",
        "band_height": "40",
        "max_internal_gap_px": "5",
        "ocr_word_count": "8",
        "ocr_hebrew_letters": "24",
        "priority_1_dense_text": "1",
        "priority_2_medium_text": "1",
        "priority_3_short_text": "0",
        "priority_4_no_text": "0",
        "dominant_review_priority": "priority_1_dense_text",
        "allowed_without_input": "group line crops by coordinate gaps only",
        "next_manual_action": "review only",
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "claim_boundary": bands.CLAIM_BOUNDARY,
    }


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
