import unittest
from types import SimpleNamespace

from els.corpus import Corpus, VerseSpan
from els.search import count_els_terms_by_lanes
from scripts.analyze_els_controls import (
    ProgressTicker,
    benjamini_hochberg_q_values,
    direction_count,
    estimated_search_space,
    observed_and_shuffled_term_counts,
    significance_band,
)


class ELSControlsTests(unittest.TestCase):
    def test_benjamini_hochberg_q_values_are_monotone(self) -> None:
        self.assertEqual(
            benjamini_hochberg_q_values([0.01, 0.04, 0.03, None]),
            [0.03, 0.04, 0.04, None],
        )

    def test_significance_band_uses_adjusted_values_first(self) -> None:
        self.assertEqual(
            significance_band(
                {
                    "status": "counted",
                    "combined_min_p_ge": 0.001,
                    "combined_min_q_value": 0.04,
                }
            ),
            "screen_q_le_0.05",
        )

    def test_significance_band_marks_uncorrected_only(self) -> None:
        self.assertEqual(
            significance_band(
                {
                    "status": "counted",
                    "combined_min_p_ge": 0.04,
                    "combined_min_q_value": 0.50,
                }
            ),
            "uncorrected_p_le_0.05",
        )

    def test_search_space_counts_valid_start_positions(self) -> None:
        self.assertEqual(
            estimated_search_space(
                text_length=10,
                query_length=3,
                min_skip=2,
                max_skip=3,
                direction="both",
            ),
            20,
        )

    def test_direction_count(self) -> None:
        self.assertEqual(direction_count("both"), 2)
        self.assertEqual(direction_count("forward"), 1)

    def test_observed_counts_share_shuffled_term_scan(self) -> None:
        corpus = Corpus(
            name="test",
            language="greek",
            keep_hebrew_final_forms=False,
            text="αβγδαβγδ",
            verses=(
                VerseSpan("test", "Test 1:1", "Test", "1", "1", "αβγδαβγδ", 0, 7, 8),
            ),
            position_to_verse=tuple(0 for _index in range(8)),
        )
        args = SimpleNamespace(
            min_skip=1,
            max_skip=3,
            direction="both",
            jobs=1,
            term_shuffles=3,
        )
        progress = ProgressTicker(False, 1.0, 0.0, 0.0)
        queries = ["αβ", "γδ"]

        observed, term_counts, term_samples = observed_and_shuffled_term_counts(
            corpus,
            "test",
            queries,
            args,
            progress,
            seed=2,
        )

        self.assertEqual(
            observed,
            count_els_terms_by_lanes(
                corpus.text,
                queries,
                min_skip=1,
                max_skip=3,
                direction="both",
                jobs=1,
            ),
        )
        self.assertEqual(set(term_counts), set(queries))
        self.assertEqual(len(term_samples["αβ"]), 3)


if __name__ == "__main__":
    unittest.main()
