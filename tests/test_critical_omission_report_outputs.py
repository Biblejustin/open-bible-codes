import unittest
from array import array
from pathlib import Path
from types import SimpleNamespace

from els.corpus import Corpus, VerseSpan
from els.critical import OmittedBlock, TermBreakStats
from scripts.analyze_critical_omission_breaks import TERM_PATHS, passage_summary_rows_for_blocks, term_paths_for_args


class PassageSummaryRowsTests(unittest.TestCase):
    def test_scopes_summary_to_requested_blocks(self) -> None:
        corpus = _corpus("abcdef")
        stats_by_query = {
            "bdf": [
                TermBreakStats(
                    0,
                    {"term": "bdf", "term_id": "removed", "term_source": "terms/a.csv"},
                    "bdf",
                )
            ],
            "ace": [
                TermBreakStats(
                    1,
                    {"term": "ace", "term_id": "spacing", "term_source": "terms/a.csv"},
                    "ace",
                )
            ],
            "zzz": [
                TermBreakStats(
                    2,
                    {"term": "zzz", "term_id": "global_only", "term_source": "terms/a.csv"},
                    "zzz",
                    broken_removed_letter_hits=99,
                )
            ],
        }
        matches = [("bdf", 2, 1, 5), ("ace", 2, 0, 4)]
        blocks = [OmittedBlock("v1", 1, 1, 1, "deleted_block", True)]

        rows = passage_summary_rows_for_blocks(corpus, stats_by_query, blocks, matches)

        self.assertEqual([row["term_id"] for row in rows], ["removed", "spacing"])
        self.assertEqual(rows[0]["broken_removed_letter_hits"], 1)
        self.assertEqual(rows[0]["broken_spacing_hits"], 0)
        self.assertEqual(rows[0]["broken_total_hits"], 1)
        self.assertEqual(rows[1]["broken_removed_letter_hits"], 0)
        self.assertEqual(rows[1]["broken_spacing_hits"], 1)
        self.assertEqual(rows[1]["broken_total_hits"], 1)
        self.assertNotIn("global_only", {row["term_id"] for row in rows})

    def test_empty_passage_has_empty_summary(self) -> None:
        corpus = _corpus("abcdef")
        stats_by_query = {"ace": [TermBreakStats(0, {"term": "ace", "term_id": "ace"}, "ace")]}
        matches = [("ace", 2, 0, 4)]
        blocks = [OmittedBlock("v2", 5, 5, 1, "deleted_block", True)]

        rows = passage_summary_rows_for_blocks(corpus, stats_by_query, blocks, matches)

        self.assertEqual(rows, [])


class TermPathSelectionTests(unittest.TestCase):
    def test_default_terms_are_used_unless_disabled(self) -> None:
        args = SimpleNamespace(no_default_terms=False, extra_terms=[Path("terms/extra.csv")])

        paths = term_paths_for_args(args)

        self.assertEqual(paths, TERM_PATHS + [Path("terms/extra.csv")])

    def test_no_default_terms_uses_only_extra_terms(self) -> None:
        args = SimpleNamespace(no_default_terms=True, extra_terms=[Path("terms/extra.csv")])

        paths = term_paths_for_args(args)

        self.assertEqual(paths, [Path("terms/extra.csv")])


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
