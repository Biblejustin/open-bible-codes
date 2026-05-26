import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_source_row_lock_queue as lock_queue


class CitiesSourceRowLockQueueTests(unittest.TestCase):
    def test_build_lock_queue_filters_candidate_roles(self) -> None:
        rows = lock_queue.build_lock_queue_rows(
            [
                page_review_row(
                    "cities_pdf_dp365a_p5_11",
                    "4",
                    "source_table_page",
                ),
                page_review_row(
                    "cities_pdf_dp365a_p1_4",
                    "1",
                    "method_toc_and_prose_page",
                ),
                page_review_row(
                    "cities_pdf_dp365a_appendix_7",
                    "1",
                    "source_list_page",
                ),
            ]
        )

        self.assertEqual([row["lock_rank"] for row in rows], ["1", "2"])
        self.assertEqual(rows[0]["page_class"], "table_candidate_page")
        self.assertEqual(rows[1]["page_class"], "source_list_candidate_page")
        self.assertEqual(rows[0]["source_row_use"], "no_source_row_use")

    def test_build_lock_queue_rejects_imported_source_row(self) -> None:
        imported = page_review_row("cities_pdf_dp365a_p5_11", "4", "source_table_page")
        imported["source_row_use"] = "source_row_candidate"

        with self.assertRaisesRegex(ValueError, "already carries source-row use"):
            lock_queue.build_lock_queue_rows([imported])

    def test_summary_counts_candidate_classes(self) -> None:
        rows = lock_queue.build_lock_queue_rows(
            [
                page_review_row("cities_pdf_dp365a_p5_11", "4", "source_table_page"),
                page_review_row("cities_pdf_dp365a_p5_11", "6", "source_table_and_notes_page"),
                page_review_row("cities_pdf_dp365a_appendix_7", "1", "source_list_page"),
                page_review_row(
                    "cities_pdf_dp365a_p12_17",
                    "2",
                    "source_exception_notes_page",
                ),
            ]
        )

        summary = {
            row["metric"]: row["value"] for row in lock_queue.build_summary_rows(rows)
        }
        self.assertEqual(summary["queue_rows"], "4")
        self.assertEqual(summary["table_candidate_pages"], "2")
        self.assertEqual(summary["source_list_candidate_pages"], "1")
        self.assertEqual(summary["exception_note_candidate_pages"], "1")
        self.assertEqual(summary["source_row_imports"], "0")
        self.assertEqual(summary["els_runs"], "0")

    def test_main_writes_doc_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page_review = root / "page_review.csv"
            out = root / "queue.csv"
            summary = root / "summary.csv"
            markdown = root / "queue.md"
            manifest = root / "manifest.json"
            write_csv(
                page_review,
                [
                    page_review_row("cities_pdf_dp365a_p5_11", "4", "source_table_page"),
                    page_review_row("cities_pdf_dp365a_p1_4", "1", "method_toc_and_prose_page"),
                ],
            )

            rc = lock_queue.main(
                [
                    "--page-review",
                    str(page_review),
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
            self.assertIn("source-row lock planning", markdown.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)


def page_review_row(label: str, page: str, role: str) -> dict[str, str]:
    return {
        "review_rank": "1",
        "decision_id": f"{label}_{page}",
        "label": label,
        "page_number": page,
        "family": "aumann_committee",
        "lane": "encoding_or_ocr_candidate",
        "packet_ocr_status": "page_ocr_text_detected",
        "packet_ocr_text_signal_chars": "900",
        "page_image_path": f"reports/pages/{label}_p{page}.png",
        "visual_review_status": "reviewed",
        "visual_page_role": role,
        "visual_text_signal": "text_present",
        "ocr_read_status": "ocr_signal_present_for_table_page",
        "source_row_use": "no_source_row_use",
        "decision": "no_source_row_import",
        "reviewed_by": "tester",
        "reviewed_at": "2026-05-26",
        "notes": "no source-row use",
        "claim_boundary": "manual page-image review only",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
