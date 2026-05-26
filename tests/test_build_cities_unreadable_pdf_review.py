import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_unreadable_pdf_review as review


class CitiesUnreadablePdfReviewTests(unittest.TestCase):
    def test_source_role_hint_marks_known_rows(self) -> None:
        self.assertEqual(
            review.source_role_hint("cities_pdf_wrr"),
            "wrr_context_paper",
        )
        self.assertEqual(
            review.source_role_hint("cities_pdf_dp365a_appendix_6"),
            "aumann_committee_recovered_segment",
        )

    def test_build_review_rows_filters_unreadable_lanes(self) -> None:
        rows = review.build_review_rows(
            [
                queue_row("good", "review_extractable_text", "extractable_text", "10"),
                queue_row("zero", "ocr_image_only_pdf", "zero_extractable_text", "0"),
                queue_row(
                    "garbled",
                    "encoding_or_ocr_candidate",
                    "extractable_but_garbled_or_nonlatin",
                    "25",
                ),
            ]
        )

        self.assertEqual([row["label"] for row in rows], ["garbled", "zero"])
        self.assertEqual(rows[0]["review_route"], "alternate_extraction_or_ocr_fallback")
        self.assertEqual(rows[1]["review_route"], "page_image_or_ocr_review")

    def test_build_summary_counts_routes(self) -> None:
        rows = review.build_review_rows(
            [
                queue_row("zero", "ocr_image_only_pdf", "zero_extractable_text", "0", pages="2"),
                queue_row(
                    "garbled",
                    "encoding_or_ocr_candidate",
                    "extractable_but_garbled_or_nonlatin",
                    "25",
                    pages="3",
                ),
            ]
        )

        summary = {row["metric"]: row["value"] for row in review.build_summary(rows)}

        self.assertEqual(summary["unreadable_rows_reviewed"], "2")
        self.assertEqual(summary["ocr_image_only_rows"], "1")
        self.assertEqual(summary["encoding_or_ocr_candidate_rows"], "1")
        self.assertEqual(summary["total_pages_needing_review"], "5")
        self.assertEqual(summary["garbled_text_chars"], "25")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            queue = root / "queue.csv"
            out = root / "review.csv"
            summary = root / "summary.csv"
            markdown = root / "review.md"
            manifest = root / "manifest.json"
            write_csv(queue, [queue_row("zero", "ocr_image_only_pdf", "zero_extractable_text", "0")])

            rc = review.main(
                [
                    "--queue",
                    str(queue),
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
            self.assertEqual(rows[0]["lane"], "ocr_image_only_pdf")
            self.assertIn("OCR/encoding planning only", markdown.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)


def queue_row(
    label: str,
    lane: str,
    text_status: str,
    normalized_text_chars: str,
    *,
    pages: str = "1",
    family: str = "aumann_committee",
) -> dict[str, str]:
    return {
        "label": label,
        "family": family,
        "lane": lane,
        "text_status": text_status,
        "pdf_pages": pages,
        "normalized_text_chars": normalized_text_chars,
        "selected_path": f"/tmp/{label}.pdf",
        "sha256": f"{label}-sha",
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
