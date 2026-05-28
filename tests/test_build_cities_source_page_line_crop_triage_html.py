import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_source_page_line_crop_triage as triage
from scripts import build_cities_source_page_line_crop_triage_html as triage_html


class CitiesSourcePageLineCropTriageHtmlTests(unittest.TestCase):
    def test_write_triage_html_groups_by_priority_without_source_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "line.png"
            image.write_bytes(b"not really png")
            rows = [
                triage_row("1", "priority_2_medium_text", image),
                triage_row("2", "priority_1_dense_text", image),
            ]
            html_out = root / "triage.html"
            args = argparse_like(html_out)

            summary = triage_html.write_triage_html(rows, args)

            text = html_out.read_text(encoding="utf-8")
            self.assertEqual(summary["html_rows"], 2)
            self.assertEqual(summary["html_line_crop_image_rows"], 2)
            self.assertIn("priority_1_dense_text", text)
            self.assertNotIn("אבג", text)

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "line.png"
            image.write_bytes(b"not really png")
            triage_csv = root / "triage.csv"
            html_out = root / "triage.html"
            summary = root / "summary.csv"
            markdown = root / "triage.md"
            manifest = root / "manifest.json"
            write_csv(triage_csv, [triage_row("1", "priority_1_dense_text", image)])

            rc = triage_html.main(
                [
                    "--triage",
                    str(triage_csv),
                    "--html-out",
                    str(html_out),
                    "--summary-out",
                    str(summary),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertTrue(html_out.exists())
            self.assertIn(
                "Cities Source Page Line Crop Triage HTML",
                markdown.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["source_row_imports"], 0)


def argparse_like(html_out: Path):
    class Args:
        pass

    args = Args()
    args.html_out = html_out
    return args


def triage_row(rank: str, priority: str, image: Path) -> dict[str, str]:
    return {
        "triage_rank": rank,
        "source_order": rank,
        "line_rank": rank,
        "transcription_decision_id": "cities_source_transcription_001",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "page_line_rank": rank,
        "crop_path": str(image),
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


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=triage.FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
