import tempfile
import unittest
from pathlib import Path

from scripts.analyze_wrr_source_shapes import source_shape, summarize


class WrrSourceShapesTests(unittest.TestCase):
    def test_source_shape_counts_raw_pairs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "source.txt"
            path.write_text("2 1 APPA APPB /A/NYSN 1 2 APPC /B/AYR /C/SYWN", encoding="utf-8")

            row = source_shape("sample", path)

        self.assertEqual(row["records"], 2)
        self.assertEqual(row["appellations"], 3)
        self.assertEqual(row["dates"], 3)
        self.assertEqual(row["same_record_pairs"], 4)
        self.assertEqual(row["records_with_multiple_dates"], 1)
        self.assertEqual(row["status"], "parsed")

    def test_summarize_reports_expected_pair_match_gap(self) -> None:
        rows = [
            {"label": "a", "status": "parsed", "same_record_pairs": 10},
            {"label": "b", "status": "parsed", "same_record_pairs": 15},
            {"label": "bad", "status": "parse_error", "same_record_pairs": 0},
        ]

        summary = summarize(rows, expected_pairs=12)

        self.assertEqual(summary["source_files"], 3)
        self.assertEqual(summary["parsed_files"], 2)
        self.assertEqual(summary["files_matching_expected_pairs"], 0)
        self.assertEqual(summary["max_same_record_pairs"], 15)
        self.assertEqual(summary["closest_label"], "a")
        self.assertEqual(summary["closest_pair_gap"], 2)


if __name__ == "__main__":
    unittest.main()
