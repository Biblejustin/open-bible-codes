import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_source_page_ocr_review_html as review_html


class CitiesSourcePageOcrReviewHtmlTests(unittest.TestCase):
    def test_write_review_html_embeds_local_ocr_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "page.png"
            text = root / "ocr.txt"
            html_path = root / "review.html"
            image.write_bytes(b"fake")
            text.write_text("אבג\n", encoding="utf-8")
            args = make_args(root, html_path)

            summary = review_html.write_review_html([packet_row(image, text)], args)

            rendered = html_path.read_text(encoding="utf-8")
            self.assertTrue(summary["html_exists"])
            self.assertEqual(summary["html_embedded_ocr_text_rows"], 1)
            self.assertIn("אבג", rendered)
            self.assertIn('<section class="page">', rendered)

    def test_summary_keeps_zero_result_work(self) -> None:
        rows = [packet_row(Path("page.png"), Path("ocr.txt"))]
        summary = {
            row["metric"]: row["value"]
            for row in review_html.build_summary_rows(
                rows,
                {
                    "html_exists": True,
                    "html_path": "review.html",
                    "html_rows": 1,
                    "html_embedded_ocr_text_rows": 1,
                },
            )
        }

        self.assertEqual(summary["source_row_imports"], "0")
        self.assertEqual(summary["city_name_normalization"], "0")
        self.assertEqual(summary["els_runs"], "0")
        self.assertEqual(summary["p_levels"], "0")
        self.assertEqual(summary["html_embeds_ocr_text"], "true")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "page.png"
            text = root / "ocr.txt"
            packet = root / "packet.csv"
            html_path = root / "review.html"
            summary = root / "summary.csv"
            markdown = root / "review.md"
            manifest = root / "manifest.json"
            image.write_bytes(b"fake")
            text.write_text("אבג\n", encoding="utf-8")
            write_csv(packet, [packet_row(image, text)])

            rc = review_html.main(
                [
                    "--packet",
                    str(packet),
                    "--html-out",
                    str(html_path),
                    "--summary-out",
                    str(summary),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertTrue(html_path.exists())
            self.assertIn("Cities Source Page OCR Review HTML", markdown.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)


def make_args(root: Path, html_path: Path):
    class Args:
        html_out = html_path

    return Args()


def packet_row(image: Path, text: Path) -> dict[str, str]:
    return {
        "ocr_rank": "1",
        "transcription_decision_id": "cities_source_transcription_001",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "page_image_path": str(image),
        "page_image_exists": "true",
        "ocr_text_path": str(text),
        "ocr_text_exists": "true",
        "ocr_status": "source_page_ocr_text_detected",
        "ocr_hebrew_letters": "3",
        "ocr_word_count": "1",
        "ocr_line_count": "1",
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
