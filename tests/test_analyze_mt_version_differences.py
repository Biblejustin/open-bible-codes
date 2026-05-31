import unittest

from scripts.analyze_mt_version_differences import (
    VerseRecord,
    compare_pair,
    first_difference_index,
    normalize_book,
)


class MTVersionDifferenceTests(unittest.TestCase):
    def test_book_aliases_normalize_across_sources(self) -> None:
        self.assertEqual(normalize_book("Exod"), "Exod")
        self.assertEqual(normalize_book("Exodus"), "Exod")
        self.assertEqual(normalize_book("1 Samuel"), "1Sam")
        self.assertEqual(normalize_book("1Samuel"), "1Sam")
        self.assertEqual(normalize_book("1SA"), "1Sam")
        self.assertEqual(normalize_book("2 Chr"), "2Chr")
        self.assertEqual(normalize_book("2CH"), "2Chr")
        self.assertEqual(normalize_book("2Chronicles"), "2Chr")
        self.assertEqual(normalize_book("SNG"), "Song")
        self.assertEqual(normalize_book("GEN"), "Gen")

    def test_first_difference_index_handles_prefix_and_equal(self) -> None:
        self.assertIsNone(first_difference_index("בראשית", "בראשית"))
        self.assertEqual(first_difference_index("בראשית", "בראשיתא"), 6)
        self.assertEqual(first_difference_index("בראשית", "בראשימ"), 5)

    def test_compare_pair_counts_equal_different_and_missing_refs(self) -> None:
        left_map = {
            ("Gen", 1, 1): record("L", ("Gen", 1, 1), "בראשית"),
            ("Gen", 1, 2): record("L", ("Gen", 1, 2), "ארץ"),
            ("Gen", 1, 3): record("L", ("Gen", 1, 3), "אור"),
        }
        right_map = {
            ("Gen", 1, 1): record("R", ("Gen", 1, 1), "בראשית"),
            ("Gen", 1, 2): record("R", ("Gen", 1, 2), "ארצ"),
            ("Gen", 1, 4): record("R", ("Gen", 1, 4), "יום"),
        }

        summary, diffs = compare_pair(
            "L",
            left_map,
            "R",
            right_map,
            dummy_corpus(3, 12),
            dummy_corpus(3, 13),
        )

        self.assertEqual(summary["shared_refs"], 2)
        self.assertEqual(summary["equal_refs"], 1)
        self.assertEqual(summary["different_refs"], 1)
        self.assertEqual(summary["left_only_refs"], 1)
        self.assertEqual(summary["right_only_refs"], 1)
        self.assertEqual([row["status"] for row in diffs], ["different", "left_only", "right_only"])


def record(label: str, key: tuple[str, int, int], normalized: str) -> VerseRecord:
    book, chapter, verse = key
    return VerseRecord(
        label=label,
        ref=f"{book} {chapter}:{verse}",
        key=key,
        normalized=normalized,
    )


class dummy_corpus:
    def __init__(self, verses: int, letters: int) -> None:
        self.verses = [None] * verses
        self.text = "x" * letters


if __name__ == "__main__":
    unittest.main()
