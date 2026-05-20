import csv
import tempfile
import unittest
from pathlib import Path

from scripts.analyze_wrr_primary_table2_ocr_probe import (
    build_probe_rows,
    main,
    michigan_to_hebrew_normalized,
    normalize_hebrew_for_match,
    summarize,
    terms_from_records,
)
from scripts.import_wrr_terms import WrrRecord


class WrrPrimaryTable2OcrProbeTests(unittest.TestCase):
    def test_michigan_to_hebrew_normalizes_final_forms(self) -> None:
        self.assertEqual(michigan_to_hebrew_normalized("RBYABRHM"), "רביאברהמ")
        self.assertEqual(normalize_hebrew_for_match("רבי אברהם"), "רביאברהמ")

    def test_build_probe_rows_matches_normalized_ocr_text(self) -> None:
        rows = build_probe_rows(
            [
                {
                    "term_id": "wrr2_01_app_01",
                    "concept": "WRR2 01",
                    "category": "wrr_appellation",
                    "term": "RBYABRHM",
                },
                {
                    "term_id": "wrr2_01_date_01",
                    "concept": "WRR2 01",
                    "category": "wrr_date",
                    "term": "/K/X$WN",
                },
            ],
            "רבי אברהם, כ חשון",
        )

        self.assertEqual(rows[0]["row_number"], "01")
        self.assertEqual(rows[0]["ocr_status"], "matched")
        self.assertEqual(rows[1]["ocr_status"], "matched")

    def test_terms_from_records_keeps_undated_appellations(self) -> None:
        rows = terms_from_records([WrrRecord(4, ("RBYABRHM", "ABRHMSB@"), ())])

        self.assertEqual([row["term_id"] for row in rows], ["wrr2_04_app_01", "wrr2_04_app_02"])
        self.assertEqual(rows[0]["concept"], "WRR2 04")

    def test_summarize_counts_matches_and_rows(self) -> None:
        rows = [
            {
                "row_number": "01",
                "category": "wrr_appellation",
                "ocr_status": "matched",
            },
            {
                "row_number": "01",
                "category": "wrr_date",
                "ocr_status": "not_matched",
            },
            {
                "row_number": "02",
                "category": "wrr_appellation",
                "ocr_status": "matched",
            },
        ]

        summary = summarize(rows, "רבי", "existing_ocr_text")

        self.assertEqual(summary["total_terms"], "3")
        self.assertEqual(summary["matched_terms"], "2")
        self.assertEqual(summary["source_rows_with_any_match"], "2")
        self.assertEqual(summary["source_rows_with_all_terms_matched"], "1")
        self.assertEqual(summary["status"], "ocr_probe_not_verification")

    def test_main_writes_outputs_from_existing_ocr_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            terms = root / "terms.csv"
            ocr = root / "ocr.txt"
            out = root / "probe.csv"
            summary = root / "summary.csv"
            markdown = root / "probe.md"
            manifest = root / "manifest.json"
            write_rows(
                terms,
                ["term_id", "concept", "category", "term"],
                [
                    {
                        "term_id": "wrr2_01_app_01",
                        "concept": "WRR2 01",
                        "category": "wrr_appellation",
                        "term": "RBYABRHM",
                    }
                ],
            )
            ocr.write_text("רבי אברהם", encoding="utf-8")

            rc = main(
                [
                    "--source",
                    str(root / "paper.pdf"),
                    "--terms",
                    str(terms),
                    "--ocr-text",
                    str(ocr),
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

            with out.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            with summary.open(encoding="utf-8", newline="") as handle:
                summary_rows = list(csv.DictReader(handle))

            self.assertEqual(rc, 0)
            self.assertEqual(rows[0]["ocr_status"], "matched")
            self.assertEqual(summary_rows[0]["matched_terms"], "1")
            self.assertTrue(markdown.exists())
            self.assertTrue(manifest.exists())


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
