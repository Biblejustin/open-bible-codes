import unittest
from array import array

from els.corpus import Corpus, VerseSpan
from els.critical import OmittedBlock, shuffled_block_placement


def _toy_corpus(verses_with_lengths):
    verses, text, p2v = [], [], []
    for i, (ref, length) in enumerate(verses_with_lengths):
        start = len(text)
        text.extend("α" * length)
        p2v.extend([i] * length)
        verses.append(
            VerseSpan(
                "S",
                ref,
                "X",
                "1",
                str(i + 1),
                "α" * length,
                start,
                start + length - 1,
                length,
            )
        )
    return Corpus(
        name="t",
        language="greek",
        keep_hebrew_final_forms=False,
        text="".join(text),
        verses=tuple(verses),
        position_to_verse=array("i", p2v),
    )


class ShuffleTests(unittest.TestCase):
    def test_same_seed_reproducible(self):
        c = _toy_corpus([(f"v{i}", 30) for i in range(100)])
        b = [
            OmittedBlock("v10", 300, 329, 30, "d", True),
            OmittedBlock("v20", 600, 629, 30, "d", True),
        ]
        a = shuffled_block_placement(c, b, seed=42)
        z = shuffled_block_placement(c, b, seed=42)
        self.assertEqual([p.start for p in a], [p.start for p in z])

    def test_different_seed_different(self):
        c = _toy_corpus([(f"v{i}", 30) for i in range(100)])
        b = [OmittedBlock(f"v{i}", i * 30, i * 30 + 29, 30, "d", True) for i in range(3)]
        self.assertNotEqual(
            [p.start for p in shuffled_block_placement(c, b, seed=1)],
            [p.start for p in shuffled_block_placement(c, b, seed=2)],
        )

    def test_no_overlap(self):
        c = _toy_corpus([(f"v{i}", 30) for i in range(50)])
        b = [OmittedBlock(f"v{i}", i * 30, i * 30 + 29, 30, "d", True) for i in range(10)]
        ranges = [(p.start, p.end) for p in shuffled_block_placement(c, b, seed=7)]
        for i, (s1, e1) in enumerate(ranges):
            for s2, e2 in ranges[i + 1 :]:
                self.assertTrue(e1 < s2 or e2 < s1)

    def test_excludes_actual_blocks_by_default(self):
        c = _toy_corpus([(f"v{i}", 30) for i in range(20)])
        b = [OmittedBlock("v5", 150, 179, 30, "d", True)]
        self.assertNotEqual(shuffled_block_placement(c, b, seed=0)[0].start, 150)

    def test_empty_exclude_refs_allows_actual_blocks(self):
        c = _toy_corpus([(f"v{i}", 30) for i in range(2)])
        b = [OmittedBlock("v1", 30, 59, 30, "d", True)]

        placement = shuffled_block_placement(c, b, exclude_refs=set(), seed=0)

        self.assertEqual(placement[0].start, 30)

    def test_verse_boundary_alignment(self):
        c = _toy_corpus([(f"v{i}", 30) for i in range(20)])
        b = [OmittedBlock("v0", 0, 29, 30, "d", True)]
        starts = {v.norm_start for v in c.verses}
        for p in shuffled_block_placement(c, b, seed=0):
            self.assertIn(p.start, starts)

    def test_raises_when_eligibility_too_narrow(self):
        c = _toy_corpus([(f"v{i}", 30) for i in range(2)])
        b = [OmittedBlock("v0", 0, 29, 30, "d", True)] * 10
        with self.assertRaises(RuntimeError):
            shuffled_block_placement(c, b, seed=0)

    def test_raises_when_no_eligible_verses(self):
        c = _toy_corpus([(f"v{i}", 30) for i in range(2)])
        b = [OmittedBlock("v0", 0, 29, 30, "d", True)]
        with self.assertRaises(RuntimeError):
            shuffled_block_placement(c, b, exclude_refs={"v0", "v1"}, seed=0)


if __name__ == "__main__":
    unittest.main()
