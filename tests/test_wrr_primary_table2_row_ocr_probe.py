import csv
import tempfile
import unittest
from pathlib import Path

from scripts.analyze_wrr_primary_table2_row_ocr_probe import (
    TsvWord,
    build_row_centers,
    build_row_probe_rows,
    main,
    summarize_row_probe,
)


class WrrPrimaryTable2RowOcrProbeTests(unittest.TestCase):
    def test_build_row_centers_interpolates_missing_marker(self) -> None:
        centers, detected = build_row_centers(
            [
                marker(".1", 450),
                marker(".2", 490),
                marker(".4", 570),
            ],
            row_count=4,
        )

        self.assertEqual(detected, {1, 2, 4})
        self.assertEqual(centers[3], 540)

    def test_build_row_centers_reassigns_duplicate_to_missing_previous_row(self) -> None:
        centers, detected = build_row_centers(
            [
                marker(".12", 940),
                marker(".14", 1000),
                marker(".14", 1060),
                marker(".15", 1100),
            ],
            row_count=15,
        )

        self.assertEqual(centers[13], 1010)
        self.assertEqual(centers[14], 1070)
        self.assertIn(13, detected)
        self.assertIn(14, detected)

    def test_build_row_probe_rows_matches_expected_row_and_column(self) -> None:
        words = [
            marker(".1", 450),
            marker(".2", 510),
            word("רבי", 1200, 450),
            word("אברהם", 1120, 450),
            word("כ", 1800, 450),
            word("חשון", 1700, 450),
            word("רבי", 1200, 510),
            word("יצחק", 1120, 510),
        ]
        centers, _ = build_row_centers(words, row_count=2)

        rows = build_row_probe_rows(
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
                {
                    "term_id": "wrr2_02_app_01",
                    "concept": "WRR2 02",
                    "category": "wrr_appellation",
                    "term": "RBYABRHM",
                },
            ],
            words,
            centers,
        )

        self.assertEqual(rows[0]["row_ocr_status"], "matched")
        self.assertEqual(rows[1]["row_ocr_status"], "matched")
        self.assertEqual(rows[2]["row_ocr_status"], "not_matched")
        self.assertEqual(rows[1]["column"], "date")

    def test_summarize_row_probe_counts_matches_and_markers(self) -> None:
        summary = summarize_row_probe(
            [
                {"row_number": "01", "category": "wrr_appellation", "row_ocr_status": "matched"},
                {"row_number": "01", "category": "wrr_date", "row_ocr_status": "not_matched"},
                {"row_number": "02", "category": "wrr_appellation", "row_ocr_status": "matched"},
            ],
            [word("רבי", 1200, 100)],
            {1},
            "existing_tsv",
        )

        self.assertEqual(summary["matched_terms"], "2")
        self.assertEqual(summary["detected_row_markers"], "1")
        self.assertEqual(summary["inferred_row_markers"], "31")
        self.assertEqual(summary["status"], "row_ocr_probe_not_verification")

    def test_main_writes_outputs_from_existing_tsv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            terms = root / "terms.csv"
            tsv = root / "ocr.tsv"
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
            write_tsv(tsv, [marker(".1", 450), word("רבי", 1200, 450), word("אברהם", 1120, 450)])

            rc = main(
                [
                    "--source",
                    str(root / "paper.pdf"),
                    "--terms",
                    str(terms),
                    "--tsv",
                    str(tsv),
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
            self.assertEqual(rows[0]["row_ocr_status"], "matched")
            self.assertEqual(summary_rows[0]["matched_terms"], "1")
            self.assertTrue(markdown.exists())
            self.assertTrue(manifest.exists())


def marker(text: str, top: int) -> TsvWord:
    return TsvWord(text=text, left=551, top=top, width=20, height=20, conf=90.0)


def word(text: str, left: int, top: int) -> TsvWord:
    return TsvWord(text=text, left=left, top=top, width=40, height=20, conf=90.0)


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_tsv(path: Path, words: list[TsvWord]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "level",
                "page_num",
                "block_num",
                "par_num",
                "line_num",
                "word_num",
                "left",
                "top",
                "width",
                "height",
                "conf",
                "text",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        for index, item in enumerate(words, start=1):
            writer.writerow(
                {
                    "level": "5",
                    "page_num": "1",
                    "block_num": "1",
                    "par_num": "1",
                    "line_num": "1",
                    "word_num": str(index),
                    "left": str(item.left),
                    "top": str(item.top),
                    "width": str(item.width),
                    "height": str(item.height),
                    "conf": str(item.conf),
                    "text": item.text,
                }
            )


if __name__ == "__main__":
    unittest.main()
