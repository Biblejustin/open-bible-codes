import csv
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from scripts import build_cities_source_page_line_crop_priority_contact_sheet as sheets
from scripts import build_cities_source_page_line_crop_triage as triage


class CitiesSourcePageLineCropPriorityContactSheetTests(unittest.TestCase):
    def test_write_contact_sheet_creates_png_for_priority(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            crop = root / "line.png"
            make_image(crop)
            out = root / "priority.png"
            args = make_args(root)

            summary = sheets.write_contact_sheet(out, [triage_row(crop, "1")], args)

            self.assertTrue(out.exists())
            self.assertGreater(summary["contact_sheet_width"], 0)
            self.assertGreater(summary["contact_sheet_height"], 0)

    def test_build_rows_keeps_zero_result_work(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            crop = root / "line.png"
            make_image(crop)
            args = make_args(root)

            rows = sheets.build_priority_sheet_rows([triage_row(crop, "1")], args)

            self.assertEqual(len(rows), 4)
            self.assertEqual(rows[0]["review_priority"], "priority_1_dense_text")
            self.assertEqual(rows[0]["line_crop_rows"], "1")
            self.assertEqual(rows[0]["source_row_import"], "0")
            self.assertEqual(rows[0]["city_name_normalization"], "0")
            self.assertEqual(rows[0]["els_runs"], "0")
            self.assertEqual(rows[0]["p_levels"], "0")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            crop = root / "line.png"
            triage_csv = root / "triage.csv"
            out = root / "sheets.csv"
            summary = root / "summary.csv"
            markdown = root / "sheets.md"
            manifest = root / "manifest.json"
            make_image(crop)
            write_csv(triage_csv, [triage_row(crop, "1")])

            rc = sheets.main(
                [
                    "--triage",
                    str(triage_csv),
                    "--base-dir",
                    str(root / "priority_sheets"),
                    "--out",
                    str(out),
                    "--summary-out",
                    str(summary),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                    "--thumb-width",
                    "80",
                    "--thumb-height",
                    "40",
                ]
            )

            self.assertEqual(rc, 0)
            self.assertTrue(out.exists())
            self.assertIn(
                "Cities Source Page Line Crop Priority Contact Sheet",
                markdown.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 4)
            self.assertEqual(payload["line_crop_rows"], 1)


def make_args(root: Path) -> Namespace:
    return Namespace(base_dir=root / "priority_sheets", thumb_width=80, thumb_height=40, columns=1)


def make_image(path: Path) -> None:
    from PIL import Image

    Image.new("RGB", (100, 30), "white").save(path)


def triage_row(crop: Path, rank: str) -> dict[str, str]:
    return {
        "triage_rank": rank,
        "source_order": rank,
        "line_rank": rank,
        "transcription_decision_id": "cities_source_transcription_001",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "page_line_rank": rank,
        "crop_path": str(crop),
        "crop_exists": str(crop.exists()).lower(),
        "line_width": "500",
        "line_height": "24",
        "crop_height": "36",
        "ocr_word_count": "2",
        "ocr_hebrew_letters": "5",
        "review_priority": "priority_1_dense_text",
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


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=triage.FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
