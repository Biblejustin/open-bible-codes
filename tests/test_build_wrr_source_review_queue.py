import csv
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_source_review_queue as queue


class WrrSourceReviewQueueTests(unittest.TestCase):
    def test_review_bucket_uses_ocr_and_variant_lead(self) -> None:
        self.assertEqual(
            queue.review_bucket("not_matched", 5),
            "ocr_not_matched_with_variant_lead",
        )
        self.assertEqual(
            queue.review_bucket("matched", 0),
            "ocr_matched_no_variant_lead",
        )
        self.assertEqual(
            queue.review_bucket("unknown", 3),
            "ocr_unknown_with_variant_lead",
        )

    def test_build_queue_rows_groups_blocking_terms_for_best_run(self) -> None:
        blocked = [
            {
                "run_label": "all_lanes_cap1000",
                "pair_id": "p1",
                "concept": "WRR2 01",
                "reason": "ordinary_missing_both_terms",
                "appellation_term_id": "app1",
                "appellation_term": "APP",
                "appellation_normalized": "APP",
                "date_term_id": "date1",
                "date_term": "DATE",
                "date_normalized": "DATE",
            },
            {
                "run_label": "all_lanes_cap1000",
                "pair_id": "p2",
                "concept": "WRR2 01",
                "reason": "ordinary_missing_appellation_hits",
                "appellation_term_id": "app1",
                "appellation_term": "APP",
                "appellation_normalized": "APP",
                "date_term_id": "date1",
                "date_term": "DATE",
                "date_normalized": "DATE",
            },
            {
                "run_label": "all_lanes_cap250",
                "pair_id": "ignored",
                "concept": "WRR2 02",
                "reason": "ordinary_missing_appellation_hits",
                "appellation_term_id": "app2",
                "appellation_term": "APP2",
                "appellation_normalized": "APP2",
                "date_term_id": "date2",
                "date_term": "DATE2",
                "date_normalized": "DATE2",
            },
        ]
        variants = queue.best_variants_by_term(
            [
                {
                    "term_id": "app1",
                    "variant_rule": "delete_one@1",
                    "variant_normalized": "PP",
                    "variant_hit_count": "8",
                }
            ]
        )
        row_ocr = {
            "app1": {
                "row_number": "01",
                "row_ocr_status": "not_matched",
                "column": "name",
                "match_basis": "probe",
                "row_ocr_text_normalized": "APP OCR",
            },
            "date1": {
                "row_number": "01",
                "row_ocr_status": "matched",
                "column": "date",
                "match_basis": "probe",
                "row_ocr_text_normalized": "DATE OCR",
            },
        }

        rows = queue.build_queue_rows(blocked, variants, row_ocr, "all_lanes_cap1000")
        by_term = {row["term_id"]: row for row in rows}

        self.assertEqual(by_term["app1"]["blocking_pairs"], 2)
        self.assertEqual(by_term["app1"]["best_variant_hit_count"], 8)
        self.assertEqual(by_term["app1"]["row_ocr_text_normalized"], "APP OCR")
        self.assertEqual(
            by_term["app1"]["review_bucket"],
            "ocr_not_matched_with_variant_lead",
        )
        self.assertEqual(by_term["app1"]["pair_ids"], "p1;p2")
        self.assertEqual(by_term["date1"]["blocking_pairs"], 1)
        self.assertNotIn("app2", by_term)

    def test_main_writes_queue_summary_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            blocked = root / "blocked.csv"
            variants = root / "variants.csv"
            row_ocr = root / "row_ocr.csv"
            out = root / "queue.csv"
            summary = root / "summary.csv"
            markdown = root / "queue.md"
            manifest = root / "manifest.json"
            write_csv(
                blocked,
                [
                    {
                        "run_label": "all_lanes_cap1000",
                        "pair_id": "p1",
                        "concept": "WRR2 01",
                        "reason": "ordinary_missing_appellation_hits",
                        "appellation_term_id": "app1",
                        "appellation_term": "APP",
                        "appellation_normalized": "APP",
                        "date_term_id": "date1",
                        "date_term": "DATE",
                        "date_normalized": "DATE",
                    }
                ],
            )
            write_csv(
                variants,
                [
                    {
                        "term_id": "app1",
                        "variant_rule": "delete_one@1",
                        "variant_normalized": "PP",
                        "variant_hit_count": "8",
                    }
                ],
            )
            write_csv(
                row_ocr,
                [
                    {
                        "term_id": "app1",
                        "row_number": "01",
                        "row_ocr_status": "not_matched",
                        "column": "name",
                        "match_basis": "probe",
                        "row_ocr_text_normalized": "APP OCR",
                    }
                ],
            )

            rc = queue.main(
                [
                    "--blocked-pairs",
                    str(blocked),
                    "--variants",
                    str(variants),
                    "--row-ocr",
                    str(row_ocr),
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
            self.assertEqual(rows[0]["review_bucket"], "ocr_not_matched_with_variant_lead")
            summary_rows = list(csv.DictReader(summary.open(encoding="utf-8")))
            self.assertEqual(summary_rows[0]["terms"], "1")
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("WRR Source Review Queue", text)
            self.assertIn("not a source correction", text)
            self.assertIn("OCR Context For Top Targets", text)
            self.assertIn("APP OCR", text)
            self.assertTrue(manifest.exists())


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
