import unittest

from els.corpus import Corpus, VerseSpan, WordSpan
from els.word_counts import count_content_words, content_key_for_word, multiple_flags, multiples_for_count


def sample_corpus() -> Corpus:
    verses = (
        VerseSpan("test", "Test 1:1", "Test", "1", "1", "και λογος αγαθος", 0, 16, 17),
        VerseSpan("test", "Test 1:2", "Test", "1", "2", "λογος λογος", 17, 27, 11),
    )
    words = (
        WordSpan("test", "Test 1:1", "Test", "1", "1", 1, "και", "και", 0, 2, 3),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 2, "λογος", "λογοσ", 3, 7, 5),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 3, "αγαθος", "αγαθοσ", 8, 13, 6),
        WordSpan("test", "Test 1:2", "Test", "1", "2", 1, "λογος", "λογοσ", 14, 18, 5),
        WordSpan("test", "Test 1:2", "Test", "1", "2", 2, "λογος", "λογοσ", 19, 23, 5),
    )
    return Corpus(
        name="test",
        language="greek",
        keep_hebrew_final_forms=False,
        text="καιλογοσαγαθοσλογοσλογοσ",
        verses=verses,
        position_to_verse=tuple(0 for _ in range(14)) + tuple(1 for _ in range(10)),
        words=words,
        position_to_word=(0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4),
    )


class WordCountTests(unittest.TestCase):
    def test_counts_content_words_and_filters_stopwords(self) -> None:
        bundle = count_content_words(sample_corpus())
        self.assertNotIn("και", bundle.by_word)
        self.assertEqual(bundle.by_word["λογοσ"], 3)
        self.assertEqual(bundle.by_word["αγαθοσ"], 1)
        self.assertEqual(bundle.by_verse[("Test 1:2", "λογοσ", "λογος")], 2)

    def test_multiples(self) -> None:
        self.assertEqual(multiples_for_count(21), (3, 7))
        self.assertTrue(multiple_flags(40)["multiple_40"])
        self.assertFalse(multiple_flags(41)["multiple_40"])

    def test_hebrew_slash_prefix_uses_lexical_segment(self) -> None:
        corpus = Corpus(
            name="hebrew",
            language="hebrew",
            keep_hebrew_final_forms=False,
            text="ויאמרולא",
            verses=(VerseSpan("test", "Gen 1:1", "Gen", "1", "1", "", 0, 7, 8),),
            position_to_verse=tuple(0 for _ in range(8)),
            words=(
                WordSpan("test", "Gen 1:1", "Gen", "1", "1", 1, "וַ/יֹּאמֶר", "ויאמר", 0, 4, 5),
                WordSpan("test", "Gen 1:1", "Gen", "1", "1", 2, "וְ/לֹא", "ולא", 5, 7, 3),
            ),
            position_to_word=(0, 0, 0, 0, 0, 1, 1, 1),
        )

        self.assertEqual(content_key_for_word(corpus, corpus.words[0]), "יאמר")
        bundle = count_content_words(corpus)
        self.assertEqual(bundle.by_word["יאמר"], 1)
        self.assertNotIn("לא", bundle.by_word)


if __name__ == "__main__":
    unittest.main()
