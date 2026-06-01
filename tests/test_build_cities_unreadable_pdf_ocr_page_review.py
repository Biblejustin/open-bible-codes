import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_unreadable_pdf_ocr_page_review as page_review


class CitiesUnreadablePdfOcrPageReviewTests(unittest.TestCase):
    def test_build_page_review_rows_joins_packet_and_decisions(self) -> None:
        packet_rows = [
            packet_row("cities_pdf_dp365a_p1_4", "3", "page_ocr_empty", "0"),
            packet_row(
                "cities_pdf_dp365a_p5_11",
                "1",
                "page_ocr_text_detected",
                "55",
            ),
        ]
        rows = page_review.build_page_review_rows(
            packet_rows,
            [
                decision_row(
                    "d1",
                    "cities_pdf_dp365a_p1_4",
                    "3",
                    "appendix_toc_or_index_page",
                    "ocr_empty_but_visual_text_present",
                ),
                decision_row(
                    "d2",
                    "cities_pdf_dp365a_p5_11",
                    "1",
                    "title_page",
                    "low_signal_ocr_matches_title_page",
                ),
            ],
        )

        self.assertEqual([row["review_rank"] for row in rows], ["1", "2"])
        self.assertEqual(rows[0]["packet_ocr_status"], "page_ocr_empty")
        self.assertEqual(rows[1]["visual_page_role"], "title_page")
        self.assertEqual(rows[1]["source_row_use"], "no_source_row_use")

    def test_build_page_review_rows_rejects_missing_packet_page(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing packet page"):
            page_review.build_page_review_rows(
                [packet_row("cities_pdf_dp365a_p1_4", "3", "page_ocr_empty", "0")],
                [
                    decision_row(
                        "d1",
                        "cities_pdf_dp365a_p1_4",
                        "4",
                        "blank_or_separator_page",
                        "ocr_empty_matches_near_blank_page",
                    )
                ],
            )

    def test_summary_keeps_source_and_search_counts_zero(self) -> None:
        packet_rows = [
            packet_row("cities_pdf_dp365a_p1_4", "3", "page_ocr_empty", "0"),
            packet_row(
                "cities_pdf_dp365a_p5_11",
                "1",
                "page_ocr_text_detected",
                "55",
            ),
            packet_row(
                "cities_pdf_dp364_short",
                "1",
                "page_ocr_text_detected",
                "44",
            ),
        ]
        rows = page_review.build_page_review_rows(
            packet_rows,
            [
                decision_row(
                    "d1",
                    "cities_pdf_dp365a_p1_4",
                    "3",
                    "appendix_toc_or_index_page",
                    "ocr_empty_but_visual_text_present",
                ),
                decision_row(
                    "d2",
                    "cities_pdf_dp365a_p5_11",
                    "1",
                    "title_page",
                    "low_signal_ocr_matches_title_page",
                ),
            ],
        )

        summary = {
            row["metric"]: row["value"]
            for row in page_review.build_summary_rows(rows, packet_rows)
        }
        self.assertEqual(summary["packet_pages"], "3")
        self.assertEqual(summary["reviewed_packet_pages"], "2")
        self.assertEqual(summary["unreviewed_packet_pages"], "1")
        self.assertEqual(summary["review_rows"], "2")
        self.assertEqual(summary["ocr_empty_pages_reviewed"], "1")
        self.assertEqual(summary["low_signal_pages_reviewed"], "2")
        self.assertEqual(summary["source_row_imports"], "0")
        self.assertEqual(summary["els_runs"], "0")

    def test_main_writes_review_doc_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet = root / "packet.csv"
            decisions = root / "decisions.csv"
            out = root / "review.csv"
            summary = root / "summary.csv"
            markdown = root / "review.md"
            manifest = root / "manifest.json"
            write_csv(
                packet,
                [
                    packet_row("cities_pdf_dp365a_p1_4", "3", "page_ocr_empty", "0"),
                ],
            )
            write_csv(
                decisions,
                [
                    decision_row(
                        "d1",
                        "cities_pdf_dp365a_p1_4",
                        "3",
                        "appendix_toc_or_index_page",
                        "ocr_empty_but_visual_text_present",
                    ),
                ],
            )

            rc = page_review.main(
                [
                    "--packet",
                    str(packet),
                    "--decisions",
                    str(decisions),
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
            self.assertIn("No OCR body text appears", markdown.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)


def packet_row(
    label: str,
    page: str,
    status: str,
    signal_chars: str,
) -> dict[str, str]:
    return {
        "label": label,
        "family": "aumann_committee",
        "lane": "encoding_or_ocr_candidate",
        "page_number": page,
        "image_path": f"reports/pages/{label}_p{page}.png",
        "ocr_status": status,
        "ocr_text_signal_chars": signal_chars,
    }


def decision_row(
    decision_id: str,
    label: str,
    page: str,
    role: str,
    ocr_read_status: str,
) -> dict[str, str]:
    return {
        "decision_id": decision_id,
        "label": label,
        "page_number": page,
        "visual_review_status": "reviewed",
        "visual_page_role": role,
        "visual_text_signal": "text_present",
        "ocr_read_status": ocr_read_status,
        "source_row_use": "no_source_row_use",
        "decision": "no_source_row_import",
        "reviewed_by": "tester",
        "reviewed_at": "2026-05-26",
        "notes": "no source-row use",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
