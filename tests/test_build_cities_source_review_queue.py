import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_source_review_queue as queue


class CitiesSourceReviewQueueTests(unittest.TestCase):
    def test_classify_lane_uses_recovery_and_text_status(self) -> None:
        self.assertEqual(
            queue.classify_lane({"usable_status": "no_pdf_recovered"}, {}),
            "recover_missing_pdf",
        )
        self.assertEqual(
            queue.classify_lane(
                {"usable_status": "usable_archived_pdf"},
                {"text_status": "extractable_text"},
            ),
            "review_extractable_text",
        )
        self.assertEqual(
            queue.classify_lane(
                {"usable_status": "usable_archived_pdf"},
                {"text_status": "zero_extractable_text"},
            ),
            "ocr_image_only_pdf",
        )
        self.assertEqual(
            queue.classify_lane(
                {"usable_status": "usable_archived_pdf"},
                {"text_status": "extractable_but_garbled_or_nonlatin"},
            ),
            "encoding_or_ocr_candidate",
        )

    def test_build_queue_orders_lanes_and_merges_text_rows(self) -> None:
        recovery = [
            recovery_row("missing", "no_pdf_recovered", "torah_code_experiment_cities_simon_mckay"),
            recovery_row("good", "usable_archived_pdf", "torah_code_experiment_cities_gans"),
            recovery_row("zero", "usable_archived_pdf", "torah_code_experiment_cities_aumann"),
            recovery_row("garbled", "usable_archived_pdf", "torah_code_experiment_cities_aumann"),
        ]
        text = {
            "good": text_row("good", "extractable_text", "gans_communities", "100"),
            "zero": text_row("zero", "zero_extractable_text", "aumann_committee", "0"),
            "garbled": text_row(
                "garbled",
                "extractable_but_garbled_or_nonlatin",
                "aumann_committee",
                "25",
            ),
        }

        rows = queue.build_queue(recovery, text)

        self.assertEqual(
            [row["lane"] for row in rows],
            [
                "review_extractable_text",
                "ocr_image_only_pdf",
                "encoding_or_ocr_candidate",
                "recover_missing_pdf",
            ],
        )
        self.assertEqual(rows[0]["normalized_text_chars"], "100")
        self.assertEqual(rows[-1]["family"], "simon_mckay")
        self.assertIn("no usable PDF", rows[-1]["blocker"])

    def test_build_summary_counts_families_and_source_pages(self) -> None:
        rows = queue.build_queue(
            [
                recovery_row("good", "usable_archived_pdf", "torah_code_experiment_cities_gans"),
                recovery_row("good2", "usable_archived_pdf", "torah_code_experiment_cities_gans"),
            ],
            {
                "good": text_row("good", "extractable_text", "gans_communities", "10"),
                "good2": text_row("good2", "extractable_text", "gans_communities", "20"),
            },
        )

        summary = queue.build_summary(rows)

        self.assertEqual(summary[0]["lane"], "review_extractable_text")
        self.assertEqual(summary[0]["rows"], "2")
        self.assertEqual(summary[0]["families"], "gans_communities:2")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            recovery = root / "recovery.csv"
            text = root / "text.csv"
            out = root / "queue.csv"
            summary = root / "summary.csv"
            markdown = root / "queue.md"
            manifest = root / "manifest.json"
            write_csv(recovery, [recovery_row("good", "usable_archived_pdf", "torah_code_experiment_cities_gans")])
            write_csv(text, [text_row("good", "extractable_text", "gans_communities", "100")])

            rc = queue.main(
                [
                    "--recovery",
                    str(recovery),
                    "--text-audit",
                    str(text),
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
            self.assertEqual(rows[0]["lane"], "review_extractable_text")
            self.assertIn("source-review triage only", markdown.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"]["queue"], 1)


def recovery_row(label: str, usable_status: str, source_pages: str) -> dict[str, str]:
    return {
        "label": label,
        "source_pages": source_pages,
        "url": f"https://example.test/{label}.pdf",
        "usable_status": usable_status,
        "archive_status": "archive_downloaded",
        "archive_cdx_candidate_count": "0",
        "selected_source": "archive" if usable_status != "no_pdf_recovered" else "",
        "selected_path": f"/tmp/{label}.pdf" if usable_status != "no_pdf_recovered" else "",
        "pdf_pages": "1" if usable_status != "no_pdf_recovered" else "",
        "archive_sha256": f"{label}-sha",
    }


def text_row(
    label: str,
    text_status: str,
    family: str,
    normalized_text_chars: str,
) -> dict[str, str]:
    return {
        "label": label,
        "family": family,
        "pdf_pages": "1",
        "text_status": text_status,
        "normalized_text_chars": normalized_text_chars,
        "sha256": f"{label}-text-sha",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
