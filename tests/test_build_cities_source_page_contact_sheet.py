import csv
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from scripts import build_cities_source_page_contact_sheet as sheet


class CitiesSourcePageContactSheetTests(unittest.TestCase):
    def test_write_contact_sheet_creates_png_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "page.png"
            make_image(image)
            args = make_args(root)
            rows = [bundle_row(image)]

            summary = sheet.write_contact_sheet(rows, args)

            self.assertTrue(args.contact_sheet_out.exists())
            self.assertEqual(summary["contact_sheet_pages"], 1)
            self.assertGreater(summary["contact_sheet_width"], 0)
            self.assertGreater(summary["contact_sheet_height"], 0)

    def test_summary_keeps_zero_result_work(self) -> None:
        rows = [bundle_row(Path("missing.png"))]
        contact_summary = {
            "contact_sheet_exists": True,
            "contact_sheet_path": "contact.png",
            "contact_sheet_pages": 1,
            "contact_sheet_width": 10,
            "contact_sheet_height": 20,
        }
        summary = {row["metric"]: row["value"] for row in sheet.build_summary_rows(rows, contact_summary)}

        self.assertEqual(summary["source_row_imports"], "0")
        self.assertEqual(summary["els_runs"], "0")
        self.assertEqual(summary["p_levels"], "0")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "page.png"
            make_image(image)
            bundle = root / "bundle.csv"
            contact = root / "contact.png"
            summary = root / "summary.csv"
            markdown = root / "contact.md"
            manifest = root / "manifest.json"
            write_csv(bundle, [bundle_row(image)])

            rc = sheet.main(
                [
                    "--bundle",
                    str(bundle),
                    "--contact-sheet-out",
                    str(contact),
                    "--summary-out",
                    str(summary),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                    "--thumb-width",
                    "80",
                    "--thumb-height",
                    "100",
                    "--columns",
                    "1",
                ]
            )

            self.assertEqual(rc, 0)
            self.assertTrue(contact.exists())
            self.assertIn("Cities Source Page Contact Sheet", markdown.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["summary"]["contact_sheet_pages"], "1")


def make_args(root: Path) -> Namespace:
    return Namespace(
        contact_sheet_out=root / "contact.png",
        thumb_width=80,
        thumb_height=100,
        columns=1,
    )


def make_image(path: Path) -> None:
    from PIL import Image

    Image.new("RGB", (60, 80), "white").save(path)


def bundle_row(image: Path) -> dict[str, str]:
    return {
        "bundle_rank": "1",
        "transcription_decision_id": "cities_source_transcription_001",
        "source_lock_decision_id": "cities_source_row_lock_001",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "visual_page_role": "source_table_page",
        "selected_source": "archive",
        "selected_path": "reports/source.pdf",
        "source_sha256": "abc123",
        "page_image_path": str(image),
        "page_image_exists": str(image.exists()).lower(),
        "page_image_width": "60",
        "page_image_height": "80",
        "review_state": "pending_readable_transcription",
        "next_manual_action": "prepare transcription plan",
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "no_input_boundary": "page review only",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
