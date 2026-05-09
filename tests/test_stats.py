import random
import unittest

from els.corpus import Corpus, VerseSpan
from els.stats import (
    shuffled_letter_control,
    shuffled_letter_controls,
    shuffled_term_samples,
    summarize_null_counts,
)


def sample_corpus() -> Corpus:
    text = "αβγαβγδε"
    return Corpus(
        name="test",
        language="greek",
        keep_hebrew_final_forms=False,
        text=text,
        verses=(
            VerseSpan(
                "test",
                "Test 1:1",
                "Test",
                "1",
                "1",
                text,
                0,
                len(text) - 1,
                len(text),
            ),
        ),
        position_to_verse=tuple(0 for _ in text),
    )


class StatsTests(unittest.TestCase):
    def test_multi_term_shuffle_matches_single_term_result(self) -> None:
        corpus = sample_corpus()

        single = shuffled_letter_control(
            corpus,
            "αβ",
            min_skip=1,
            max_skip=3,
            direction="both",
            shuffles=5,
            seed=7,
        )
        multi = dict(
            shuffled_letter_controls(
                corpus,
                ["αβ", "γδ"],
                min_skip=1,
                max_skip=3,
                direction="both",
                shuffles=5,
                seed=7,
            )
        )

        self.assertEqual(multi["αβ"], single)
        self.assertEqual(len(multi["γδ"].shuffled_counts), 5)

    def test_empty_normalized_shuffle_has_full_null_series(self) -> None:
        result = shuffled_letter_control(
            sample_corpus(),
            "123",
            min_skip=1,
            max_skip=3,
            direction="both",
            shuffles=4,
            seed=7,
        )

        self.assertEqual(result.observed, 0)
        self.assertEqual(result.shuffled_counts, (0, 0, 0, 0))
        self.assertEqual(result.p_greater_equal, 1.0)

    def test_summarize_null_counts_reports_z_and_percentile(self) -> None:
        summary = summarize_null_counts(10, [4, 8, 10, 12])

        self.assertEqual(summary.samples, 4)
        self.assertAlmostEqual(summary.mean or 0.0, 8.5)
        self.assertIsNotNone(summary.z_score)
        self.assertEqual(summary.p_greater_equal, 3 / 5)
        self.assertEqual(summary.percentile, 75.0)
        self.assertEqual(summary.min_count, 4)
        self.assertEqual(summary.max_count, 12)

    def test_shuffled_term_samples_are_deterministic(self) -> None:
        samples = shuffled_term_samples("abcd", shuffles=3, rng=random.Random(2))

        self.assertEqual(samples, ("bcda", "dbac", "badc"))


if __name__ == "__main__":
    unittest.main()
