import argparse
import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_unreadable_pdf_ocr_feasibility as probe


class CitiesUnreadablePdfOcrFeasibilityTests(unittest.TestCase):
    def test_signal_chars_counts_letters_and_digits(self) -> None:
        self.assertEqual(probe.ocr_text_signal_chars("abc 123 !!!"), 6)

    def test_pages_to_attempt_honors_cap(self) -> None:
        self.assertEqual(probe.pages_to_attempt("7", 0), 7)
        self.assertEqual(probe.pages_to_attempt("7", 2), 2)
        self.assertEqual(probe.pages_to_attempt("", 0), 0)

    def test_classify_ocr_status(self) -> None:
        self.assertEqual(probe.classify_ocr_status(120, 1, []), "ocr_text_detected")
        self.assertEqual(probe.classify_ocr_status(10, 0, []), "low_ocr_text")
        self.assertEqual(probe.classify_ocr_status(0, 0, []), "ocr_empty")
        self.assertEqual(probe.classify_ocr_status(0, 0, ["bad"]), "ocr_error")

    def test_build_probe_rows_and_summary(self) -> None:
        args = make_args()
        rows = probe.build_probe_rows(
            [review_row("one"), review_row("two")],
            {
                "one": probe.OcrResult(2, 2, 200, "ocr_text_detected", ""),
                "two": probe.OcrResult(1, 0, 5, "low_ocr_text", ""),
            },
            args,
        )
        summary = {row["metric"]: row["value"] for row in probe.build_summary(rows)}

        self.assertEqual(summary["rows_reviewed"], "2")
        self.assertEqual(summary["rows_with_ocr_text"], "1")
        self.assertEqual(summary["pages_attempted"], "3")
        self.assertEqual(summary["pages_with_ocr_text"], "2")
        self.assertEqual(summary["ocr_text_signal_chars"], "205")
        self.assertEqual(summary["status_ocr_text_detected"], "1")
        self.assertEqual(summary["status_low_ocr_text"], "1")

    def test_main_writes_outputs_with_blocked_language(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            review = root / "review.csv"
            out = root / "out.csv"
            summary = root / "summary.csv"
            markdown = root / "review.md"
            manifest = root / "manifest.json"
            write_csv(review, [review_row("one")])

            rc = probe.main(
                [
                    "--review",
                    str(review),
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
            self.assertEqual(rows[0]["ocr_status"], "blocked_missing_dependency")
            self.assertIn("OCR feasibility only", markdown.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)


def make_args() -> argparse.Namespace:
    return argparse.Namespace(language="eng", dpi=200, psm="6")


def review_row(label: str) -> dict[str, str]:
    return {
        "label": label,
        "family": "aumann_committee",
        "lane": "ocr_image_only_pdf",
        "pdf_pages": "1",
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
