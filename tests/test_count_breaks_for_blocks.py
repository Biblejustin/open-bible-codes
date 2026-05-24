import unittest
from array import array

from els.corpus import Corpus, VerseSpan
from els.critical import OmittedBlock, TermBreakStats, count_breaks_for_blocks


class CountBreaksForBlocksTests(unittest.TestCase):
    def test_counts_removed_letter_and_spacing_breaks(self) -> None:
        corpus = _corpus("abcdef")
        stats_by_query = {
            "bdf": [TermBreakStats(0, {"term": "bdf"}, "bdf")],
            "ace": [TermBreakStats(1, {"term": "ace"}, "ace")],
        }
        blocks = [OmittedBlock("v1", 1, 1, 1, "deleted_block", True)]

        total, per_block, broken = count_breaks_for_blocks(
            corpus,
            stats_by_query,
            blocks,
            min_skip=2,
            max_skip=2,
            direction="forward",
        )

        self.assertEqual(total, 2)
        self.assertEqual(per_block, [2])
        self.assertEqual(
            sorted(record.break_type for record in broken),
            ["broken_removed_letter", "broken_spacing"],
        )
        self.assertEqual(stats_by_query["bdf"][0].broken_removed_letter_hits, 1)
        self.assertEqual(stats_by_query["ace"][0].broken_spacing_hits, 1)

    def test_ignores_hits_outside_block_span(self) -> None:
        corpus = _corpus("abcdef")
        stats_by_query = {"ace": [TermBreakStats(0, {"term": "ace"}, "ace")]}
        blocks = [OmittedBlock("v1", 5, 5, 1, "deleted_block", True)]

        total, per_block, broken = count_breaks_for_blocks(
            corpus,
            stats_by_query,
            blocks,
            min_skip=2,
            max_skip=2,
            direction="forward",
        )

        self.assertEqual(total, 0)
        self.assertEqual(per_block, [0])
        self.assertEqual(broken, [])


def _corpus(text: str) -> Corpus:
    verses = (
        VerseSpan("S", "v1", "X", "1", "1", text, 0, len(text) - 1, len(text)),
    )
    return Corpus(
        name="toy",
        language="greek",
        keep_hebrew_final_forms=False,
        text=text,
        verses=verses,
        position_to_verse=array("i", [0] * len(text)),
    )


if __name__ == "__main__":
    unittest.main()
