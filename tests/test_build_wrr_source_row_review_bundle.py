import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_source_row_review_bundle as bundle


class WrrSourceRowReviewBundleTests(unittest.TestCase):
    def test_build_bundle_rows_joins_checklist_crop_and_ocr_words(self) -> None:
        row_checklist = [row_checklist_row()]
        crop_packet = [crop_row()]
        ocr_word_packet = [ocr_word_row()]

        rows = bundle.build_bundle_rows(row_checklist, crop_packet, ocr_word_packet)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["row_number"], "01")
        self.assertEqual(rows[0]["crop_path"], "reports/wrr_1994/row01.png")
        self.assertEqual(rows[0]["word_count"], 3)
        self.assertEqual(rows[0]["low_conf_word_count"], 1)
        self.assertIn("שם", rows[0]["name_column_ocr"])
        self.assertIn("review crop and OCR words", rows[0]["next_manual_action"])

    def test_missing_crop_and_words_keeps_no_input_boundary(self) -> None:
        row = row_checklist_row(frontier_pairs="1")

        rows = bundle.build_bundle_rows([row], [], [])

        self.assertEqual(rows[0]["crop_path"], "")
        self.assertEqual(rows[0]["word_count"], 0)
        self.assertIn("No row transcription", rows[0]["no_input_boundary"])
        self.assertEqual(
            rows[0]["next_manual_action"],
            "retrieve row image before any frontier source decision",
        )

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            row_checklist = root / "row_checklist.csv"
            crop_packet = root / "crop_packet.csv"
            ocr_word_packet = root / "ocr_word_packet.csv"
            out = root / "bundle.csv"
            summary = root / "summary.csv"
            md = root / "bundle.md"
            manifest = root / "manifest.json"
            write_rows(row_checklist, [row_checklist_row()])
            write_rows(crop_packet, [crop_row()])
            write_rows(ocr_word_packet, [ocr_word_row()])

            rc = bundle.main(
                [
                    "--row-checklist",
                    str(row_checklist),
                    "--crop-packet",
                    str(crop_packet),
                    "--ocr-word-packet",
                    str(ocr_word_packet),
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
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 1)
            self.assertIn("WRR Source Row Review Bundle", md.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["summary"]["rows_with_generated_crops"], 1)


def row_checklist_row(frontier_pairs: str = "1") -> dict[str, str]:
    return {
        "run_label": "test",
        "row_rank": "1",
        "row_number": "01",
        "concept": "WRR2 01",
        "review_state": "pending_manual_source_lock",
        "action_terms": "2",
        "residual_pairs": "2",
        "frontier_pairs": frontier_pairs,
        "terms_to_verify": "wrr2_01_app_01 ABC",
        "table2_bridge_read": "bridge read",
    }


def crop_row() -> dict[str, str]:
    return {
        "row_number": "01",
        "crop_path": "reports/wrr_1994/row01.png",
        "crop_exists": "true",
    }


def ocr_word_row() -> dict[str, str]:
    return {
        "row_number": "01",
        "word_count": "3",
        "hebrew_letter_count": "8",
        "low_conf_word_count": "1",
        "min_conf": "12.5",
        "median_conf": "88.8",
        "name_tokens_rtl": "שם אחד",
        "date_tokens_rtl": "א ניסן",
    }


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
