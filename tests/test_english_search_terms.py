import csv
import tempfile
import unittest
from pathlib import Path

from els.normalization import normalize_text
from scripts.build_english_search_terms import build_english_rows, main


class EnglishSearchTermTests(unittest.TestCase):
    def test_generated_english_terms_include_requested_examples(self) -> None:
        path = Path("terms/english_search_terms.csv")
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        by_concept = {row["concept"]: row for row in rows}

        self.assertEqual(by_concept["Jesus"]["language"], "english")
        self.assertEqual(normalize_text(by_concept["Jesus"]["term"], "english"), "jesus")
        self.assertIn("Donald Trump", by_concept)
        self.assertIn("United States Of America", by_concept)
        self.assertIn("Cowboy Catering", by_concept)
        self.assertIn("Constantine I", by_concept)

    def test_build_english_rows_skips_digit_only_or_digit_mixed_concepts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "terms.csv"
            source.write_text(
                "\n".join(
                    [
                        "term_id,concept,category,language,term,notes",
                        "ok_h,Jesus,core,hebrew,ישוע,",
                        "year_h,1948,dates,hebrew,1948,digits are removed",
                        "date_h,October 7,dates,hebrew,שבעה באוקטובר,",
                    ]
                ),
                encoding="utf-8",
            )
            rows, skipped = build_english_rows([source])

        self.assertEqual(skipped, 2)
        self.assertEqual([row["concept"] for row in rows], ["Jesus"])

    def test_script_can_write_english_terms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "terms.csv"
            out = Path(tmp) / "english.csv"
            source.write_text(
                "\n".join(
                    [
                        "term_id,concept,category,language,term,notes",
                        "law_h,Law,revelation,hebrew,תורה,",
                    ]
                ),
                encoding="utf-8",
            )

            code = main(["--source", str(source), "--out", str(out)])

            self.assertEqual(code, 0)
            with out.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual(rows[0]["term_id"], "eng_law")
        self.assertEqual(rows[0]["language"], "english")


if __name__ == "__main__":
    unittest.main()
