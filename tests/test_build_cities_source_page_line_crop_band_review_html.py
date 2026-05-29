import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_source_page_line_crop_band_contact_sheet as contact
from scripts import build_cities_source_page_line_crop_band_review_html as html_builder


class CitiesSourcePageLineCropBandReviewHtmlTests(unittest.TestCase):
    def test_write_band_html_uses_contact_sheet_images_without_source_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "band.png"
            image.write_bytes(b"not really png")
            rows = [contact_row("1", image)]
            html_out = root / "band_review.html"
            args = argparse_like(html_out)

            summary = html_builder.write_band_html(rows, args)

            text = html_out.read_text(encoding="utf-8")
            self.assertEqual(summary["html_rows"], 1)
            self.assertEqual(summary["html_band_image_rows"], 1)
            self.assertIn("cities_source_band_review_001", text)
            self.assertNotIn("אבג", text)

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "band.png"
            image.write_bytes(b"not really png")
            contact_csv = root / "band_contact.csv"
            html_out = root / "band_review.html"
            summary = root / "summary.csv"
            markdown = root / "band_review.md"
            manifest = root / "manifest.json"
            write_csv(contact_csv, [contact_row("1", image)])

            rc = html_builder.main(
                [
                    "--band-contact",
                    str(contact_csv),
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
                "Cities Source Page Line Crop Band Review HTML",
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


def contact_row(rank: str, image: Path) -> dict[str, str]:
    return {
        "sheet_rank": rank,
        "band_review_id": f"cities_source_band_review_{int(rank):03d}",
        "band_rank": rank,
        "band_id": f"cities_source_line_band_{int(rank):03d}",
        "transcription_decision_id": "cities_source_transcription_001",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "page_band_rank": rank,
        "first_page_line_rank": "1",
        "last_page_line_rank": "2",
        "line_crop_rows": "2",
        "line_crop_images_found": "2",
        "ocr_word_count": "4",
        "ocr_hebrew_letters": "10",
        "contact_sheet_path": str(image),
        "contact_sheet_exists": str(image.exists()).lower(),
        "contact_sheet_width": "80",
        "contact_sheet_height": "40",
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "no_input_boundary": contact.NO_INPUT_BOUNDARY,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=contact.FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
