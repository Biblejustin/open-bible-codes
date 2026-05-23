import csv
import unittest
from pathlib import Path

from els.ebible_usfm import UsfmVerse
from scripts.download_openbible_english_controls import (
    sort_verses_canonically,
    verse_sort_key,
)


OPENBIBLE_CONTROLS = Path("configs/openbible_english_controls.csv")


class OpenBibleEnglishControlTests(unittest.TestCase):
    def test_openbible_controls_have_source_and_license_metadata(self) -> None:
        rows = {row["label"]: row for row in read_rows(OPENBIBLE_CONTROLS)}

        self.assertEqual(
            sorted(rows),
            ["AFINT-EXP-AE", "AFINT-EXP-BE", "AFINT-LIT-AE", "AFINT-LIT-BE"],
        )
        self.assertEqual(
            rows["AFINT-LIT-AE"]["details_url"],
            "https://www.open.bible/bibles/69a307e995245b14e244c7b0",
        )
        self.assertEqual(
            rows["AFINT-LIT-BE"]["details_url"],
            "https://www.open.bible/bibles/69a307e695245b14e244c7a8",
        )
        for label, row in rows.items():
            with self.subTest(label=label):
                self.assertTrue(row["source_id"].startswith("afint-"))
                self.assertTrue(row["source_url"].startswith("https://openbible-api-1.biblica.com/artifactContent/"))
                self.assertTrue(row["details_url"].startswith("https://www.open.bible/bibles/"))
                self.assertIn("CC BY-SA", row["license_label"])
                self.assertEqual(row["basis_status"], "broad_tradition")
                self.assertEqual(row["coverage"], "nt")
                self.assertIn("New Testament only", row["ot_basis"])
                self.assertIn("does not state", row["nt_basis"])
                self.assertTrue(row["local_csv"].startswith("data/processed/openbible/"))
                self.assertEqual(row["source_path_prefix"], "release/text_1/")

    def test_verse_sort_key_keeps_nt_canonical_order(self) -> None:
        verses = [
            UsfmVerse("REV", "22", "21", "Amen."),
            UsfmVerse("1CO", "1", "1", "Paul."),
            UsfmVerse("MAT", "1", "1", "Record."),
        ]

        self.assertEqual(
            [verse.ref for verse in sort_verses_canonically(verses)],
            ["MAT 1:1", "1CO 1:1", "REV 22:21"],
        )
        self.assertLess(verse_sort_key(UsfmVerse("1JN", "2", "1", "")), verse_sort_key(UsfmVerse("REV", "1", "1", "")))


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
