import unittest
from array import array

from els.corpus import Corpus, VerseSpan
from scripts import analyze_wrr_method_lane_wide_skip as probe


class WrrMethodLaneWideSkipTests(unittest.TestCase):
    def test_probe_rows_count_profiles_and_first_hit(self) -> None:
        corpus = toy_corpus("BXXGXXD")
        rows = probe.build_probe_rows(
            [packet_row("wrr2_x", "BGD")],
            corpus,
            profiles=[2, 3, 5],
            max_skip=5,
            direction="both",
            jobs=1,
        )
        summary = probe.build_summary_rows(
            rows,
            profiles=[2, 3, 5],
            max_skip=5,
            direction="both",
        )

        self.assertEqual(rows[0]["hits_le_2"], 0)
        self.assertEqual(rows[0]["hits_le_3"], 1)
        self.assertEqual(rows[0]["hits_le_5"], 1)
        self.assertEqual(rows[0]["total_hits_through_max"], 1)
        self.assertEqual(rows[0]["found_within_max_skip"], "true")
        self.assertEqual(rows[0]["first_hit_skip"], 3)
        self.assertEqual(summary[0]["terms_with_any_hit"], 1)

    def test_probe_rows_record_no_hit_boundary(self) -> None:
        corpus = toy_corpus("BBBBBBBB")
        rows = probe.build_probe_rows(
            [packet_row("wrr2_x", "BGD")],
            corpus,
            profiles=[2, 3, 5],
            max_skip=5,
            direction="both",
            jobs=1,
        )
        summary = probe.build_summary_rows(
            rows,
            profiles=[2, 3, 5],
            max_skip=5,
            direction="both",
        )

        self.assertEqual(rows[0]["found_within_max_skip"], "false")
        self.assertEqual(rows[0]["total_hits_through_max"], 0)
        self.assertIn("No ordinary Genesis ELS hit", rows[0]["read"])
        self.assertEqual(summary[0]["terms_zero_through_max"], 1)


def packet_row(term_id: str, term: str) -> dict[str, str]:
    return {
        "term_id": term_id,
        "term": term,
        "concept": "WRR2 X",
        "row_number": "99",
        "pair_id": "pair_x",
        "date_term_id": "date_x",
    }


def toy_corpus(text: str) -> Corpus:
    verse = VerseSpan(
        source="toy",
        ref="Genesis 1:1",
        book="Genesis",
        chapter="1",
        verse="1",
        raw_text=text,
        norm_start=0,
        norm_end=len(text) - 1,
        norm_length=len(text),
    )
    return Corpus(
        name="toy",
        language="michigan",
        keep_hebrew_final_forms=False,
        text=text,
        verses=(verse,),
        position_to_verse=array("i", [0] * len(text)),
    )


if __name__ == "__main__":
    unittest.main()
