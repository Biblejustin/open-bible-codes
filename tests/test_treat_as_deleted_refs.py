import csv
import unittest
from pathlib import Path

from els.corpus import load_corpus
from scripts.analyze_critical_omission_breaks import (
    TR_CONFIG,
    build_partial_deleted_blocks,
    normalize_ref_label,
    partial_ref_base,
    read_treat_as_deleted_refs,
)


class TreatAsDeletedRefsTests(unittest.TestCase):
    def test_override_refs_exist_in_tr(self) -> None:
        tr = load_corpus(TR_CONFIG)
        refs = {verse.ref for verse in tr.verses}
        with Path("protocols/treat_as_deleted/critical_consensus.csv").open(
            "r",
            encoding="utf-8",
            newline="",
        ) as handle:
            for row in csv.DictReader(handle):
                ref = row["ref"].strip()
                lookup_ref = partial_ref_base(ref) if row.get("normalized_subspan", "").strip() else ref
                self.assertIn(normalize_ref_label(lookup_ref), refs, ref)

    def test_partial_override_subspan_resolves_in_tr(self) -> None:
        tr = load_corpus(TR_CONFIG)
        _extra_refs, _passage_refs, partial_refs = read_treat_as_deleted_refs(
            Path("protocols/treat_as_deleted/critical_consensus.csv")
        )

        blocks = build_partial_deleted_blocks(tr, partial_refs)

        self.assertEqual([block.ref for block in blocks], ["LUK 23:34a"])
        self.assertEqual(blocks[0].status, "explicit_deleted_partial_ref")
        self.assertGreater(blocks[0].length, 0)


if __name__ == "__main__":
    unittest.main()
