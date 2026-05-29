import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_source_page_line_crop_priority_contact_sheet as contact
from scripts import build_cities_source_page_line_crop_priority_review_worksheet as worksheet
from scripts import build_cities_source_page_line_crop_triage as triage


class CitiesSourcePageLineCropPriorityReviewWorksheetTests(unittest.TestCase):
    def test_build_rows_preserves_triage_order_and_contact_path(self) -> None:
        rows = worksheet.build_priority_review_rows(
            [triage_row("1", "priority_1_dense_text")],
            [contact_row("priority_1_dense_text", "priority1.png")],
        )

        self.assertEqual(rows[0]["review_rank"], "1")
        self.assertEqual(rows[0]["triage_rank"], "1")
        self.assertEqual(rows[0]["priority_contact_sheet_path"], "priority1.png")

    def test_build_rows_keeps_zero_result_work(self) -> None:
        rows = worksheet.build_priority_review_rows(
            [triage_row("1", "priority_1_dense_text")],
            [contact_row("priority_1_dense_text", "priority1.png")],
        )

        self.assertEqual(rows[0]["source_row_import"], "0")
        self.assertEqual(rows[0]["city_name_normalization"], "0")
        self.assertEqual(rows[0]["els_runs"], "0")
        self.assertEqual(rows[0]["p_levels"], "0")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            triage_csv = root / "triage.csv"
            contact_csv = root / "contact.csv"
            out = root / "worksheet.csv"
            summary = root / "summary.csv"
            markdown = root / "worksheet.md"
            manifest = root / "manifest.json"
            write_csv(triage_csv, triage.FIELDNAMES, [triage_row("1", "priority_1_dense_text")])
            write_csv(
                contact_csv,
                contact.FIELDNAMES,
                [contact_row("priority_1_dense_text", "priority1.png")],
            )

            rc = worksheet.main(
                [
                    "--triage",
                    str(triage_csv),
                    "--priority-contact",
                    str(contact_csv),
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
                "Cities Source Page Line Crop Priority Review Worksheet",
                markdown.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["source_row_imports"], 0)


def triage_row(rank: str, priority: str) -> dict[str, str]:
    return {
        "triage_rank": rank,
        "source_order": rank,
        "line_rank": rank,
        "transcription_decision_id": "cities_source_transcription_001",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "page_line_rank": rank,
        "crop_path": "line.png",
        "crop_exists": "true",
        "line_width": "500",
        "line_height": "24",
        "crop_height": "36",
        "ocr_word_count": "6",
        "ocr_hebrew_letters": "20",
        "review_priority": priority,
        "review_bucket": "likely_row_or_header",
        "triage_reason": "dense OCR signal",
        "allowed_without_input": "rank line-crop visual review only",
        "next_manual_action": "review crop image",
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "claim_boundary": triage.CLAIM_BOUNDARY,
    }


def contact_row(priority: str, path: str) -> dict[str, str]:
    return {
        "sheet_rank": "1",
        "review_priority": priority,
        "line_crop_rows": "1",
        "line_crop_images_found": "1",
        "unique_table_pages": "1",
        "ocr_word_count": "6",
        "ocr_hebrew_letters": "20",
        "contact_sheet_path": path,
        "contact_sheet_exists": "true",
        "contact_sheet_width": "80",
        "contact_sheet_height": "40",
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "no_input_boundary": contact.NO_INPUT_BOUNDARY,
    }


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
