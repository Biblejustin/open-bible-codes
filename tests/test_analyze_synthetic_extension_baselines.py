import unittest
from types import SimpleNamespace

from els.corpus import Corpus, VerseSpan, WordSpan
from els.extensions import build_extension_lexicon
from scripts.analyze_extension_paired_controls import ExtensionTarget
from scripts.analyze_synthetic_extension_baselines import (
    ge_count,
    score_synthetic_controls,
    synthetic_read,
)


class SyntheticExtensionBaselinesTests(unittest.TestCase):
    def test_ge_count_counts_scores_at_or_above_observed(self) -> None:
        self.assertEqual(ge_count(10, (0, 10, 11, 9)), 2)

    def test_synthetic_read_flags_sampled_exceedance(self) -> None:
        self.assertEqual(
            synthetic_read(1, 0),
            "synthetic samples can match or exceed target extension score",
        )
        self.assertEqual(
            synthetic_read(0, 0),
            "target exceeds sampled synthetic extension score",
        )

    def test_score_synthetic_controls_batches_and_preserves_duplicates(self) -> None:
        corpus = extension_corpus()
        scores, matches = score_synthetic_controls(
            corpus,
            build_extension_lexicon(corpus, max_phrase_words=2),
            extension_target(),
            ("αβ", "αβ", "βγ"),
            SimpleNamespace(
                max_before=2,
                max_after=2,
                include_both_sided=True,
                max_extensions_per_hit=20,
                min_extension_length=1,
                match_kind_prefix="phrase_",
            ),
        )

        self.assertEqual(scores.same_type_scores, (2211, 2211, 0))
        self.assertEqual(scores.any_scores[:2], (2211, 2211))
        self.assertEqual(len(matches), 3)
        self.assertEqual([row["synthetic_query"] for row in matches], ["αβ", "αβ", "βγ"])


def extension_target() -> ExtensionTarget:
    return ExtensionTarget(
        target_id="target",
        source_file="test.csv",
        row={
            "corpus": "TR_NT",
            "term": "αβ",
            "normalized_term": "αβ",
            "skip": "1",
            "direction": "forward",
            "extension_type": "term_plus_after",
            "extended_sequence": "αβγδ",
            "matched_normalized": "αβγδ",
            "extension_score": "2211",
        },
    )


def extension_corpus() -> Corpus:
    return Corpus(
        name="extension",
        language="greek",
        keep_hebrew_final_forms=False,
        text="αβγδ",
        verses=(
            VerseSpan("test", "Test 1:1", "Test", "1", "1", "αβ γδ", 0, 3, 4),
        ),
        position_to_verse=(0, 0, 0, 0),
        words=(
            WordSpan("test", "Test 1:1", "Test", "1", "1", 1, "αβ", "αβ", 0, 1, 2),
            WordSpan("test", "Test 1:1", "Test", "1", "1", 2, "γδ", "γδ", 2, 3, 2),
        ),
        position_to_word=(0, 0, 1, 1),
    )


if __name__ == "__main__":
    unittest.main()
