import unittest
from array import array

from els.corpus import Corpus, VerseSpan
from scripts.analyze_critical_omission_breaks_cross_tradition import (
    classify_cross,
    equivalent_status,
)


class CriticalOmissionCrossTraditionTests(unittest.TestCase):
    def test_equivalent_status_preserved_offsets(self) -> None:
        tr = _corpus("abcdef")
        other = _corpus("abcdef")
        row = _row("ace", skip=2, start=0, end=4)

        status = equivalent_status(row, tr, {"v1": tr.verses[0]}, other, {"v1": other.verses[0]})

        self.assertEqual(status, "preserved_equivalent_offsets")

    def test_equivalent_status_not_preserved_offsets(self) -> None:
        tr = _corpus("abcdef")
        other = _corpus("abxdef")
        row = _row("ace", skip=2, start=0, end=4)

        status = equivalent_status(row, tr, {"v1": tr.verses[0]}, other, {"v1": other.verses[0]})

        self.assertEqual(status, "not_preserved_equivalent_offsets")

    def test_equivalent_status_missing_ref(self) -> None:
        tr = _corpus("abcdef")
        other = _corpus("abcdef")
        row = _row("ace", skip=2, start=0, end=4)

        status = equivalent_status(row, tr, {"v1": tr.verses[0]}, other, {})

        self.assertEqual(status, "ref_missing")

    def test_classify_cross(self) -> None:
        self.assertEqual(
            classify_cross("preserved_equivalent_offsets", "preserved_equivalent_offsets"),
            "preserved_by_byz_and_tcg",
        )
        self.assertEqual(
            classify_cross("preserved_equivalent_offsets", "ref_missing"),
            "preserved_by_byz",
        )
        self.assertEqual(
            classify_cross("ref_missing", "preserved_equivalent_offsets"),
            "preserved_by_tcg",
        )
        self.assertEqual(
            classify_cross("ref_missing", "not_preserved_equivalent_offsets"),
            "tr_specific_under_equivalent_offsets",
        )


def _row(query: str, *, skip: int, start: int, end: int) -> dict[str, str]:
    return {
        "start_ref": "v1",
        "end_ref": "v1",
        "start_offset": str(start),
        "end_offset": str(end),
        "skip": str(skip),
        "normalized_term": query,
    }


def _corpus(text: str) -> Corpus:
    return Corpus(
        name="toy",
        language="greek",
        keep_hebrew_final_forms=False,
        text=text,
        verses=(VerseSpan("S", "v1", "X", "1", "1", text, 0, len(text) - 1, len(text)),),
        position_to_verse=array("i", [0] * len(text)),
    )


if __name__ == "__main__":
    unittest.main()
