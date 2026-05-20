import csv
import tempfile
import unittest
from pathlib import Path

from scripts.build_wrr_table2_source_bridge import (
    FIELDNAMES,
    build_bridge_rows,
    int_or_zero,
    main,
    markdown_cell,
    summarize,
)
from scripts.import_wrr_terms import WrrRecord


class WrrTable2SourceBridgeTests(unittest.TestCase):
    def test_build_bridge_rows_joins_primary_anchor_to_secondary_record(self) -> None:
        rows = build_bridge_rows(
            [
                {
                    "row_number": "1",
                    "english_name": "Rabbi One",
                    "status": "found",
                    "page": "6",
                }
            ],
            [WrrRecord(1, ("AAA", "BBB"), ("DATE",))],
        )

        self.assertEqual(rows[0]["primary_anchor_status"], "found")
        self.assertEqual(rows[0]["secondary_record_status"], "found")
        self.assertEqual(rows[0]["secondary_appellations"], "2")
        self.assertEqual(rows[0]["secondary_dates"], "1")
        self.assertEqual(rows[0]["secondary_same_record_pairs"], "2")
        self.assertEqual(rows[0]["primary_hebrew_cells_status"], "not_verified")

    def test_build_bridge_rows_marks_missing_secondary_record(self) -> None:
        rows = build_bridge_rows(
            [
                {
                    "row_number": "2",
                    "english_name": "Rabbi Two",
                    "status": "found",
                    "page": "6",
                }
            ],
            [],
        )

        self.assertEqual(rows[0]["secondary_record_status"], "missing")
        self.assertEqual(rows[0]["secondary_same_record_pairs"], "")

    def test_summarize_counts_bridge_shape(self) -> None:
        summary = summarize(
            [
                {
                    "primary_anchor_status": "found",
                    "secondary_record_status": "found",
                    "secondary_appellations": "2",
                    "secondary_dates": "1",
                    "secondary_same_record_pairs": "2",
                    "primary_hebrew_cells_status": "not_verified",
                },
                {
                    "primary_anchor_status": "found",
                    "secondary_record_status": "found",
                    "secondary_appellations": "4",
                    "secondary_dates": "0",
                    "secondary_same_record_pairs": "0",
                    "primary_hebrew_cells_status": "not_verified",
                },
            ]
        )

        self.assertEqual(summary["primary_rows"], "2")
        self.assertEqual(summary["rows_with_primary_and_secondary"], "2")
        self.assertEqual(summary["secondary_appellations"], "6")
        self.assertEqual(summary["secondary_dates"], "1")
        self.assertEqual(summary["secondary_same_record_pairs"], "2")
        self.assertEqual(summary["undated_secondary_records"], "1")
        self.assertEqual(summary["status"], "bridge_only_not_transcription")

    def test_main_writes_outputs_from_fixture_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            anchors = root / "anchors.csv"
            source = root / "WRR2.txt"
            out = root / "bridge.csv"
            summary = root / "summary.csv"
            markdown = root / "bridge.md"
            manifest = root / "manifest.json"
            write_rows(
                anchors,
                ["row_number", "english_name", "status", "page"],
                [
                    {
                        "row_number": "1",
                        "english_name": "Rabbi One",
                        "status": "found",
                        "page": "6",
                    }
                ],
            )
            source.write_text("2 1 AAA BBB DATE\n", encoding="utf-8")

            rc = main(
                [
                    "--anchors",
                    str(anchors),
                    "--source",
                    str(source),
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

            self.assertEqual(rc, 0)
            self.assertEqual(rows[0]["secondary_same_record_pairs"], "2")
            self.assertTrue(summary.exists())
            self.assertTrue(markdown.exists())
            self.assertTrue(manifest.exists())

    def test_markdown_cell_escapes_pipes(self) -> None:
        self.assertEqual(markdown_cell("a|b\nc"), "a\\|b c")

    def test_int_or_zero_handles_bad_values(self) -> None:
        self.assertEqual(int_or_zero("7"), 7)
        self.assertEqual(int_or_zero(""), 0)


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
