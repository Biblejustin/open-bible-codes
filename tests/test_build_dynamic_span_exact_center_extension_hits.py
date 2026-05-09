import csv
import tempfile
import unittest
from pathlib import Path

from scripts.build_dynamic_span_exact_center_extension_hits import convert


class BuildDynamicSpanExactCenterExtensionHitsTests(unittest.TestCase):
    def test_converts_exact_rows_to_hits_input_and_filters_corpus(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "exact.csv"
            out = tmp_path / "hits.csv"
            write_rows(
                source,
                [
                    row("UHB", "dyn_yeshua_h"),
                    row("KJV", "dyn_jesus_e"),
                ],
            )

            result = convert(source, out, corpus_filter={"UHB"})
            rows = list(csv.DictReader(out.open(encoding="utf-8", newline="")))

        self.assertEqual(result["input_rows"], 2)
        self.assertEqual(result["written_rows"], 1)
        self.assertEqual(result["written_by_corpus"], {"UHB": 1})
        self.assertEqual(rows[0]["corpus"], "UHB")
        self.assertEqual(rows[0]["sequence"], rows[0]["normalized_term"])
        self.assertEqual(rows[0]["start_source"], "UHB")
        self.assertEqual(rows[0]["end_source"], "UHB")


FIELDNAMES = [
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


def row(corpus: str, term_id: str) -> dict[str, str]:
    return {
        "corpus": corpus,
        "term_id": term_id,
        "term": "ישוע",
        "normalized_term": "ישוע",
        "skip": "3",
        "direction": "forward",
        "span_letters": "9",
        "start_ref": "START 1:1",
        "center_ref": "CENTER 1:1",
        "end_ref": "END 1:1",
        "center_source": corpus,
        "center_word_index": "2",
        "center_word": "יֵשׁוּעַ",
        "center_normalized_word": "ישוע",
        "start_offset": "1",
        "center_offset": "2",
        "end_offset": "3",
    }


if __name__ == "__main__":
    unittest.main()
