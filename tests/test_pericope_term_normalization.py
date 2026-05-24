import csv
import unittest
from pathlib import Path

from els.normalization import normalize_greek


class PericopeTermNormalizationTests(unittest.TestCase):
    def test_all_pericope_terms_normalize_non_empty(self) -> None:
        with Path("terms/pericope_adulterae_terms.csv").open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                self.assertTrue(normalize_greek(row["term"]), row["term_id"])


if __name__ == "__main__":
    unittest.main()
