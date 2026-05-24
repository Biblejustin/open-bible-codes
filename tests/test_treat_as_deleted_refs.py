import csv
import unittest
from pathlib import Path

from els.corpus import load_corpus
from scripts.analyze_critical_omission_breaks import TR_CONFIG, normalize_ref_label


class TreatAsDeletedRefsTests(unittest.TestCase):
    def test_non_partial_override_refs_exist_in_tr(self) -> None:
        tr = load_corpus(TR_CONFIG)
        refs = {verse.ref for verse in tr.verses}
        with Path("protocols/treat_as_deleted/critical_consensus.csv").open(
            "r",
            encoding="utf-8",
            newline="",
        ) as handle:
            for row in csv.DictReader(handle):
                ref = row["ref"].strip()
                if ref.endswith("a"):
                    continue
                self.assertIn(normalize_ref_label(ref), refs, ref)


if __name__ == "__main__":
    unittest.main()
