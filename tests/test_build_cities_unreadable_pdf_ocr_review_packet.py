import argparse
import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_unreadable_pdf_ocr_review_packet as packet


class CitiesUnreadablePdfOcrReviewPacketTests(unittest.TestCase):
    def test_ocr_word_and_line_counts_ignore_blank_noise(self) -> None:
        text = "alpha 123 !!!\n\n  beta\n---\n"

        self.assertEqual(packet.ocr_word_count(text), 3)
        self.assertEqual(packet.ocr_line_count(text), 3)

    def test_build_summary_counts_page_sidecars(self) -> None:
        args = make_args()
        rows = [
            packet.page_row(
                review_row("one"),
                1,
                Path("/tmp/one.png"),
                Path("/tmp/one.txt"),
                args,
                "page_ocr_text_detected",
                "",
                signal_chars=100,
                word_count=20,
                line_count=5,
            ),
            packet.page_row(
                review_row("one"),
                2,
                Path("/tmp/two.png"),
                Path("/tmp/two.txt"),
                args,
                "page_ocr_empty",
                "",
            ),
        ]

        summary = {row["metric"]: row["value"] for row in packet.build_summary(rows)}

        self.assertEqual(summary["page_rows"], "2")
        self.assertEqual(summary["pdf_rows"], "1")
        self.assertEqual(summary["pages_with_ocr_text"], "1")
        self.assertEqual(summary["pages_without_ocr_text"], "1")
        self.assertEqual(summary["ocr_text_signal_chars"], "100")
        self.assertEqual(summary["ocr_words"], "20")
        self.assertEqual(summary["ocr_lines"], "5")
        self.assertEqual(summary["status_page_ocr_text_detected"], "1")
        self.assertEqual(summary["status_page_ocr_empty"], "1")

    def test_main_writes_blocked_review_packet_without_source_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            review = root / "review.csv"
            out = root / "out.csv"
            summary = root / "summary.csv"
            markdown = root / "review.md"
            manifest = root / "manifest.json"
            write_csv(review, [review_row("one", pdf_pages="2")])

            rc = packet.main(
                [
                    "--review",
                    str(review),
                    "--base-dir",
                    str(root / "sidecars"),
                    "--language",
                    "missing_test_language",
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
            rows = list(csv.DictReader(out.open(encoding="utf-8")))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["ocr_status"], "blocked_missing_dependency")
            self.assertIn("does not track OCR text", markdown.read_text(encoding="utf-8"))
            self.assertNotIn("alpha", markdown.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 2)


def make_args() -> argparse.Namespace:
    return argparse.Namespace(language="eng", dpi=200, psm="6")


def review_row(label: str, *, pdf_pages: str = "1") -> dict[str, str]:
    return {
        "label": label,
        "family": "aumann_committee",
        "lane": "ocr_image_only_pdf",
        "pdf_pages": pdf_pages,
        "selected_path": f"/tmp/{label}.pdf",
        "url": f"https://example.test/{label}.pdf",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
