import tempfile
import unittest
from pathlib import Path

from scripts import analyze_american_presidents_source as presidents


DATA_TEXT = """No   President's Name          Last Name Hebrew     Last Name and First
                                    Spellings     Initial Hebrew Spellings
1    George Washington     pehbpiye               pehbpiye b
                           phbpiye                phbpiye b
2    John Adam             qnc`                   qnc` b
                                                  qnc` w b
"""

RULES_TEXT = """Transliteration of English Names Into Hebrew
The table below shows the letter to letter correspondence.
The vowels are the place where there is some variability.
If the last sound of a name is a vowel, that vowel sound is always explicit in the Hebrew.
We form spelling variations with the basic name and add variations preceded by the first initial.
If a name has a double consonant, we form spelling variations with the consonant doubled and singular.
"""


class AmericanPresidentsSourceTests(unittest.TestCase):
    def test_parse_records_counts_spelling_columns(self) -> None:
        records = presidents.parse_records(DATA_TEXT)
        spelling_rows = presidents.spelling_rows_from_records(records)

        self.assertEqual([record.record_index for record in records], [1, 2])
        self.assertEqual(records[0].last_name_spellings, 2)
        self.assertEqual(records[0].with_initial_spellings, 2)
        self.assertEqual(records[1].last_name_spellings, 1)
        self.assertEqual(records[1].with_initial_spellings, 2)
        self.assertTrue(records[1].has_continuation_only_initial_spellings)
        self.assertEqual(len(spelling_rows), 7)
        self.assertEqual(spelling_rows[0]["spelling_type"], "last_name")
        self.assertEqual(spelling_rows[0]["hebrew_spelling"], "pehbpiye")
        self.assertEqual(spelling_rows[1]["spelling_type"], "last_name_with_initial")
        self.assertEqual(spelling_rows[-1]["hebrew_spelling"], "qnc` w b")

    def test_protocol_anchors_find_data_and_rule_sources(self) -> None:
        anchors = presidents.protocol_anchors(DATA_TEXT, RULES_TEXT)

        self.assertEqual({row["status"] for row in anchors}, {"found"})

    def test_main_writes_source_shape_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data.pdf"
            rules = root / "rules.pdf"
            data.write_bytes(DATA_TEXT.encode("utf-8"))
            rules.write_bytes(RULES_TEXT.encode("utf-8"))

            original_extract = presidents.extract_pdf_text
            try:
                presidents.extract_pdf_text = (  # type: ignore[assignment]
                    lambda path: DATA_TEXT if Path(path) == data else RULES_TEXT
                )
                rc = presidents.main(
                    [
                        "--data-source",
                        str(data),
                        "--rules-source",
                        str(rules),
                        "--out",
                        str(root / "records.csv"),
                        "--spellings-out",
                        str(root / "spellings.csv"),
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
                presidents.extract_pdf_text = original_extract  # type: ignore[assignment]

            self.assertEqual(rc, 0)
            markdown = (root / "audit.md").read_text(encoding="utf-8")
            self.assertIn("source-shape audit only", markdown)
            self.assertIn("data records | 2", markdown)
            self.assertIn("machine spelling rows extracted | 7", markdown)
            self.assertIn("not a claim-ready replication", markdown)
            self.assertTrue((root / "spellings.csv").exists())
            self.assertTrue((root / "manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
