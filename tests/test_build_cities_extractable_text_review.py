import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_extractable_text_review as review


class CitiesExtractableTextReviewTests(unittest.TestCase):
    def test_classify_source_role_marks_known_rows(self) -> None:
        role, status, read, action = review.classify_source_role("cities_pdf_communities_data")

        self.assertEqual(role, "communities_data_table")
        self.assertEqual(status, "data_bearing_candidate")
        self.assertIn("table", read)
        self.assertIn("source-row", action)

    def test_build_review_rows_filters_extractable_lane(self) -> None:
        rows = review.build_review_rows(
            [
                queue_row("cities_pdf_communities_data", "review_extractable_text"),
                queue_row("cities_pdf_wrr", "ocr_image_only_pdf"),
            ],
            {"cities_pdf_communities_data": text_row("cities_pdf_communities_data")},
            [anchor_row("cities_pdf_communities_data")],
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["data_bearing_status"], "data_bearing_candidate")
        self.assertEqual(rows[0]["anchor_status"], "found")

    def test_build_review_rows_links_existing_gans_audit(self) -> None:
        rows = review.build_review_rows(
            [queue_row("cities_pdf_communities_data", "review_extractable_text")],
            {"cities_pdf_communities_data": text_row("cities_pdf_communities_data")},
            [anchor_row("cities_pdf_communities_data")],
            gans_summary_row(),
        )

        self.assertEqual(rows[0]["existing_source_audit"], review.GANS_SOURCE_AUDIT_DOC)
        self.assertEqual(
            rows[0]["existing_source_audit_status"],
            review.GANS_SOURCE_AUDIT_STATUS,
        )
        self.assertEqual(rows[0]["existing_records"], "66")
        self.assertEqual(rows[0]["existing_community_rows"], "210")
        self.assertIn("locked preregistration", rows[0]["next_action"])

    def test_build_summary_counts_roles(self) -> None:
        rows = review.build_review_rows(
            [
                queue_row("cities_pdf_communities_data", "review_extractable_text"),
                queue_row("cities_pdf_gans", "review_extractable_text"),
                queue_row("cities_pdf_dp_365_1", "review_extractable_text"),
            ],
            {},
            [
                anchor_row("cities_pdf_communities_data"),
                anchor_row("cities_pdf_gans"),
                anchor_row("cities_pdf_dp_365_1"),
            ],
        )

        summary = {row["metric"]: row["value"] for row in review.build_summary(rows)}

        self.assertEqual(summary["extractable_rows_reviewed"], "3")
        self.assertEqual(summary["status_data_bearing_candidate"], "1")
        self.assertEqual(summary["data_candidates_with_existing_source_shape_audit"], "0")
        self.assertEqual(summary["status_method_context_candidate"], "1")
        self.assertEqual(summary["status_commentary_or_perspective"], "1")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            queue = root / "queue.csv"
            text = root / "text.csv"
            anchors = root / "anchors.csv"
            gans_summary = root / "gans_summary.csv"
            out = root / "review.csv"
            summary = root / "summary.csv"
            markdown = root / "review.md"
            manifest = root / "manifest.json"
            write_csv(queue, [queue_row("cities_pdf_communities_data", "review_extractable_text")])
            write_csv(text, [text_row("cities_pdf_communities_data")])
            write_csv(anchors, [anchor_row("cities_pdf_communities_data")])
            write_csv(gans_summary, [gans_summary_row()])

            rc = review.main(
                [
                    "--queue",
                    str(queue),
                    "--text-audit",
                    str(text),
                    "--anchors",
                    str(anchors),
                    "--gans-summary",
                    str(gans_summary),
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
            self.assertEqual(rows[0]["source_role"], "communities_data_table")
            self.assertEqual(rows[0]["existing_records"], "66")
            markdown_text = markdown.read_text(encoding="utf-8")
            self.assertIn("source-role review only", markdown_text)
            self.assertIn("Gans source-shape records: 66", markdown_text)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)


def queue_row(label: str, lane: str) -> dict[str, str]:
    return {
        "label": label,
        "lane": lane,
        "family": "gans_communities",
        "pdf_pages": "8",
        "normalized_text_chars": "100",
        "selected_path": f"/tmp/{label}.pdf",
        "url": f"https://example.test/{label}.pdf",
    }


def text_row(label: str) -> dict[str, str]:
    return {
        "label": label,
        "normalized_text_chars": "100",
    }


def anchor_row(label: str) -> dict[str, str]:
    return {
        "label": label,
        "anchor": f"{label}_anchor",
        "status": "found",
    }


def gans_summary_row() -> dict[str, str]:
    return {
        "data_records": "66",
        "total_community_rows": "210",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
