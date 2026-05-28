import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_source_page_line_crop_review_worksheet as worksheet


class CitiesSourcePageLineCropReviewWorksheetTests(unittest.TestCase):
    def test_build_worksheet_rows_keeps_no_result_work(self) -> None:
        rows = worksheet.build_worksheet_rows([packet_row("1")])

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["line_review_id"], "cities_source_line_crop_001")
        self.assertEqual(rows[0]["review_state"], worksheet.REVIEW_STATE)
        self.assertEqual(rows[0]["source_row_import"], "0")
        self.assertEqual(rows[0]["city_name_normalization"], "0")
        self.assertEqual(rows[0]["els_runs"], "0")
        self.assertEqual(rows[0]["p_levels"], "0")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet = root / "packet.csv"
            html = root / "review.html"
            out = root / "worksheet.csv"
            markdown = root / "worksheet.md"
            manifest = root / "manifest.json"
            html.write_text("<html></html>\n", encoding="utf-8")
            write_csv(packet, [packet_row("1"), packet_row("2")])

            rc = worksheet.main(
                [
                    "--packet",
                    str(packet),
                    "--html-review-aid",
                    str(html),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertTrue(out.exists())
            self.assertIn(
                "Cities Source Page Line Crop Review Worksheet",
                markdown.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 2)


def packet_row(line_rank: str) -> dict[str, str]:
    return {
        "line_rank": line_rank,
        "transcription_decision_id": "cities_source_transcription_001",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "page_line_rank": line_rank,
        "page_image_path": "page.png",
        "crop_path": f"line{line_rank}.png",
        "crop_exists": "true",
        "crop_width": "120",
        "crop_height": "20",
        "ocr_word_count": "2",
        "ocr_hebrew_letters": "5",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
