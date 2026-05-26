import argparse
import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_unreadable_pdf_ocr_review_checklist as checklist


class CitiesUnreadablePdfOcrReviewChecklistTests(unittest.TestCase):
    def test_build_checklist_rows_prioritizes_empty_pages(self) -> None:
        args = make_args(Path("/tmp"))
        rows = checklist.build_checklist_rows(
            [
                packet_row("a", 1, "page_ocr_text_detected", "100"),
                packet_row("a", 2, "page_ocr_empty", "0"),
                packet_row("b", 1, "page_ocr_text_detected", "500", lane="ocr_image_only_pdf"),
            ],
            args,
        )

        self.assertEqual(rows[0]["label"], "a")
        self.assertEqual(rows[0]["pages_without_ocr_text"], "1")
        self.assertEqual(rows[0]["low_signal_pages"], "2")
        self.assertEqual(rows[0]["review_priority"], "1_empty_or_low_ocr_pages")
        self.assertEqual(rows[1]["review_priority"], "3_aumann_ocr_image_only")

    def test_write_contact_sheet_creates_image(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "page.png"
            make_image(image)
            args = make_args(root)
            out = root / "sheet.png"

            checklist.write_contact_sheet(
                [packet_row("a", 1, "page_ocr_text_detected", "100", image_path=str(image))],
                out,
                args,
                columns=1,
            )

            self.assertTrue(out.exists())
            self.assertGreater(out.stat().st_size, 0)

    def test_main_writes_no_input_doc_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "page.png"
            make_image(image)
            packet = root / "packet.csv"
            out = root / "out.csv"
            summary = root / "summary.csv"
            markdown = root / "review.md"
            contact = root / "contact.png"
            manifest = root / "manifest.json"
            write_csv(
                packet,
                [
                    packet_row(
                        "a",
                        1,
                        "page_ocr_text_detected",
                        "100",
                        image_path=str(image),
                    )
                ],
            )

            rc = checklist.main(
                [
                    "--packet",
                    str(packet),
                    "--contact-sheet-out",
                    str(contact),
                    "--contact-sheet-dir",
                    str(root / "sheets"),
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
            self.assertTrue(contact.exists())
            self.assertIn("does not track OCR text", markdown.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)


def make_args(root: Path) -> argparse.Namespace:
    return argparse.Namespace(
        contact_sheet_dir=root / "sheets",
        contact_sheet_out=root / "contact.png",
        thumb_width=120,
        thumb_height=160,
    )


def packet_row(
    label: str,
    page: int,
    status: str,
    signal_chars: str,
    *,
    lane: str = "encoding_or_ocr_candidate",
    image_path: str = "/tmp/missing.png",
) -> dict[str, str]:
    return {
        "label": label,
        "family": "aumann_committee",
        "lane": lane,
        "page_number": str(page),
        "image_path": image_path,
        "ocr_text_signal_chars": signal_chars,
        "ocr_word_count": "10",
        "ocr_line_count": "2",
        "ocr_status": status,
    }


def make_image(path: Path) -> None:
    from PIL import Image

    Image.new("RGB", (80, 100), "white").save(path)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
