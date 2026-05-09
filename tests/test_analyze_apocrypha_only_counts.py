import unittest
from array import array

from els.corpus import Corpus, VerseSpan
from scripts.analyze_apocrypha_only_counts import text_for_class


class ApocryphaOnlyCountsTests(unittest.TestCase):
    def test_text_for_class_splits_apocrypha_books(self) -> None:
        corpus = Corpus(
            name="demo",
            language="greek",
            keep_hebrew_final_forms=False,
            text="abcdef",
            verses=(
                VerseSpan("demo", "MAL 1:1", "MAL", "1", "1", "", 0, 2, 3),
                VerseSpan("demo", "TOB 1:1", "TOB", "1", "1", "", 3, 5, 3),
            ),
            position_to_verse=array("i", [0, 0, 0, 1, 1, 1]),
        )

        self.assertEqual(text_for_class(corpus, apocrypha=False), "abc")
        self.assertEqual(text_for_class(corpus, apocrypha=True), "def")
