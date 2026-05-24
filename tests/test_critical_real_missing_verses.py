import unittest

from els.corpus import load_corpus
from els.critical import classify_missing_verses


class CriticalRealMissingVersesTests(unittest.TestCase):
    def test_real_tr_sblgnt_missing_refs_downgrade_merges(self) -> None:
        tr = load_corpus("configs/example_ebible_grctr.toml")
        sblgnt = load_corpus("configs/example_sblgnt.toml")

        blocks = classify_missing_verses(tr, sblgnt)
        by_ref = {block.ref: block for block in blocks}

        self.assertEqual(len(blocks), 20)
        self.assertEqual(sum(block.used_as_deletion for block in blocks), 18)
        self.assertEqual(sum(block.length for block in blocks if block.used_as_deletion), 1290)
        self.assertEqual(by_ref["ACT 19:41"].status, "adjacent_merge")
        self.assertFalse(by_ref["ACT 19:41"].used_as_deletion)
        self.assertEqual(by_ref["2CO 13:14"].status, "renumbered_minus_amen_subscription")
        self.assertFalse(by_ref["2CO 13:14"].used_as_deletion)


if __name__ == "__main__":
    unittest.main()
