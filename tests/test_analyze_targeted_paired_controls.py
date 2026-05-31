import random
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.analyze_targeted_paired_controls import (
    paired_band,
    read_targets,
    sample_random_controls,
    sample_term_controls,
    stable_seed,
    write_markdown,
)


class TargetedPairedControlsTests(unittest.TestCase):
    def test_term_controls_preserve_letter_multiset(self) -> None:
        rng = random.Random(1)
        samples = sample_term_controls("abcd", samples=20, rng=rng)

        self.assertEqual(len(samples), 20)
        self.assertTrue(all(sorted(sample) == ["a", "b", "c", "d"] for sample in samples))

    def test_random_controls_preserve_length_and_use_corpus_alphabet(self) -> None:
        rng = random.Random(1)
        samples = sample_random_controls(
            length=4,
            corpus_text="aabbcc",
            samples=20,
            rng=rng,
        )

        self.assertEqual(len(samples), 20)
        self.assertTrue(all(len(sample) == 4 for sample in samples))
        self.assertTrue(all(set(sample) <= {"a", "b", "c"} for sample in samples))

    def test_stable_seed_is_repeatable(self) -> None:
        self.assertEqual(stable_seed(1, "MT_WLC", "iran_h"), stable_seed(1, "MT_WLC", "iran_h"))
        self.assertNotEqual(stable_seed(1, "MT_WLC", "iran_h"), stable_seed(1, "LXX", "iran_g"))

    def test_paired_band_prefers_adjusted_values(self) -> None:
        self.assertEqual(
            paired_band({"combined_min_p_ge": 0.001, "combined_min_q_value": 0.04}),
            "paired_q_le_0.05",
        )
        self.assertEqual(
            paired_band({"combined_min_p_ge": 0.04, "combined_min_q_value": 0.50}),
            "paired_uncorrected_p_le_0.05",
        )

    def test_read_targets_filters_corpus_and_zero_hits(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "targets.csv"
            path.write_text(
                "concept,corpus,term_set,term_id,category,term_language,term,normalized_term,normalized_length,hit_count\n"
                "Trump,MT_WLC,wide,trump_h,modern,hebrew,טראמפ,טראמפ,5,11\n"
                "Trump,MAM,wide,trump_h,modern,hebrew,טראמפ,טראמפ,5,13\n"
                "Catering,MT_WLC,wide,catering_h,local,hebrew,קייטרינג,קייטרינג,7,0\n",
                encoding="utf-8",
            )

            rows = read_targets(path, corpora={"MT_WLC"}, min_observed_hits=1)

        self.assertEqual([row.row["term_id"] for row in rows], ["trump_h"])

    def test_write_markdown_handles_empty_targets(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "paired.md"

            write_markdown(path, [])

            text = path.read_text(encoding="utf-8")
        self.assertIn("Status: no target rows.", text)
        self.assertIn("target summary was empty", text)


if __name__ == "__main__":
    unittest.main()
