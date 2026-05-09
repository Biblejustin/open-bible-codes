import csv
import tempfile
import unittest
from pathlib import Path

from scripts.build_dynamic_span_exact_center_review_queue import build_queue


class BuildDynamicSpanExactCenterReviewQueueTests(unittest.TestCase):
    def test_groups_exact_rows_by_center_word_and_sorts_bible_first(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "exact.csv"
            write_rows(
                path,
                [
                    row("HEB_PBY_BIALIK", "dyn_yeshua_h", "PBY Bialik", "7", "forward", "20"),
                    row("UHB", "dyn_yeshua_h", "EZR 2:2", "3", "forward", "12"),
                    row("UHB", "dyn_yeshua_h", "EZR 2:2", "3", "backward", "-5"),
                    row("UHB", "dyn_yeshua_h", "NEH 8:17", "11", "forward", "100"),
                ],
            )

            result = build_queue(path)

        rows = result["rows"]
        self.assertEqual(result["total_exact_rows"], 4)
        self.assertEqual(result["review_units"], 3)
        self.assertEqual([row["corpus"] for row in rows], ["UHB", "UHB", "HEB_PBY_BIALIK"])
        first = rows[0]
        self.assertEqual(first["center_ref"], "EZR 2:2")
        self.assertEqual(first["exact_center_paths"], "2")
        self.assertEqual(first["forward_paths"], "1")
        self.assertEqual(first["backward_paths"], "1")
        self.assertEqual(first["min_abs_skip"], "5")
        self.assertEqual(first["max_abs_skip"], "12")
        self.assertEqual(first["example_skip"], "-5")
        self.assertEqual(first["review_bucket"], "bible low-count review")


FIELDNAMES = [
    "source_kind",
    "source_path",
    "partition_id",
    "corpus",
    "term_id",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "span_letters",
    "start_ref",
    "center_ref",
    "end_ref",
    "center_source",
    "center_word_index",
    "center_word",
    "center_normalized_word",
    "start_offset",
    "center_offset",
    "end_offset",
]


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def row(
    corpus: str,
    term_id: str,
    center_ref: str,
    center_word_index: str,
    direction: str,
    skip: str,
) -> dict[str, str]:
    return {
        "source_kind": "partition",
        "source_path": "part.csv.gz",
        "partition_id": "p1",
        "corpus": corpus,
        "term_id": term_id,
        "term": "ישוע",
        "normalized_term": "ישוע",
        "skip": skip,
        "direction": direction,
        "span_letters": "30",
        "start_ref": "START 1:1",
        "center_ref": center_ref,
        "end_ref": "END 1:1",
        "center_source": corpus,
        "center_word_index": center_word_index,
        "center_word": "יֵשׁוּעַ",
        "center_normalized_word": "ישוע",
        "start_offset": "1",
        "center_offset": "2",
        "end_offset": "3",
    }


if __name__ == "__main__":
    unittest.main()
