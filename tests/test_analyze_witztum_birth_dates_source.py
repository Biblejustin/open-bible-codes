import tempfile
import unittest
from pathlib import Path

from scripts import analyze_witztum_birth_dates_source as witztum


DATA_TEXT = """List L consists of these 14 personalities.
Sample S1 is a set of word pairs.
The conventions use three fixed forms.
Each expression is restricted in length to the range 5-8.
These have been indicated in the table with an asterisk and are not included in the sample.
Table 1

Personality       Name                                  Date
Adam           )DM            ) T$RY, B) T$RY, ) BT$RY.
Asher          )$R            *K $B+, BK $B+, K B$B+.

This table presents sample S1 in a concise form.
This yields the Sample S2.
Table 2

Personality      Name                                  Date
Adam          )DM            ) T$RY, B) T$RY, ) BT$RY.
Asher         )$R            *K $B+, BK $B+, K B$B+.

(Note that S2 differs in the omission of variants.)
"""

PAPER_TEXT = """Pattern of type B.
We chose 999, 999 random permutations and obtained 1, 000, 000 numbers.
The p-levels were 0.00051 and 0.000046.
"""


class WitztumBirthDatesSourceTests(unittest.TestCase):
    def test_parse_birth_date_rows_counts_tables(self) -> None:
        rows = witztum.parse_birth_date_rows(DATA_TEXT)
        by_key = {(row.sample, row.personality): row for row in rows}

        self.assertEqual(len(rows), 4)
        self.assertEqual(by_key[("S1", "Adam")].date_forms, 3)
        self.assertEqual(by_key[("S1", "Asher")].starred_date_forms, 1)
        self.assertEqual(by_key[("S1", "Asher")].pair_forms_after_star_filter, 2)

    def test_protocol_anchors_find_paper_and_data_rules(self) -> None:
        anchors = witztum.protocol_anchors(PAPER_TEXT, DATA_TEXT)

        self.assertEqual({row["status"] for row in anchors}, {"found"})

    def test_main_writes_source_shape_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paper = root / "paper.pdf"
            data = root / "data.pdf"
            paper.write_bytes(PAPER_TEXT.encode("utf-8"))
            data.write_bytes(DATA_TEXT.encode("utf-8"))

            original_extract = witztum.extract_pdf_text
            try:
                witztum.extract_pdf_text = (  # type: ignore[assignment]
                    lambda path: PAPER_TEXT if Path(path) == paper else DATA_TEXT
                )
                rc = witztum.main(
                    [
                        "--paper-source",
                        str(paper),
                        "--data-source",
                        str(data),
                        "--out",
                        str(root / "rows.csv"),
                        "--summary-out",
                        str(root / "summary.csv"),
                        "--anchors-out",
                        str(root / "anchors.csv"),
                        "--markdown-out",
                        str(root / "audit.md"),
                        "--manifest-out",
                        str(root / "manifest.json"),
                    ]
                )
            finally:
                witztum.extract_pdf_text = original_extract  # type: ignore[assignment]

            self.assertEqual(rc, 0)
            markdown = (root / "audit.md").read_text(encoding="utf-8")
            self.assertIn("source-shape audit only", markdown)
            self.assertIn("total table rows | 4", markdown)
            self.assertIn("not a claim-ready replication", markdown)
            self.assertTrue((root / "manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
