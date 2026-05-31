import random
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from els.corpus import Corpus, VerseSpan
from scripts import analyze_gog_magog_pairs as gog_magog
from scripts.analyze_gog_magog_pairs import (
    ControlSample,
    HitLite,
    collect_hits_by_query,
    nearest_hits,
    paired_random_samples,
    paired_term_samples,
    parse_corpus_arg,
    p_value_ge,
    p_value_le,
    resolve_corpus_jobs,
    run_corpus_analyses,
    score_control_samples,
    score_pair,
    span_gap,
    term_ids_for_corpus,
)


class GogMagogPairsTests(unittest.TestCase):
    def test_span_gap_zero_for_overlaps(self) -> None:
        self.assertEqual(
            span_gap(
                HitLite("a", 2, 10, 20),
                HitLite("b", 2, 18, 30),
            ),
            0,
        )

    def test_span_gap_counts_between_spans(self) -> None:
        self.assertEqual(
            span_gap(
                HitLite("a", 2, 10, 20),
                HitLite("b", 2, 25, 30),
            ),
            5,
        )

    def test_nearest_hits_returns_center_window(self) -> None:
        hits = [
            HitLite("b", 1, 10, 10),
            HitLite("b", 1, 20, 20),
            HitLite("b", 1, 40, 40),
        ]
        centers = [hit.center for hit in hits]

        self.assertEqual(
            nearest_hits(HitLite("a", 1, 21, 21), hits, centers, radius=1),
            hits[:3],
        )

    def test_paired_term_samples_preserve_letter_multisets(self) -> None:
        samples = paired_term_samples("abc", "deef", samples=10, rng=random.Random(1))

        self.assertEqual(len(samples), 10)
        self.assertTrue(all(sorted(sample.left_query) == ["a", "b", "c"] for sample in samples))
        self.assertTrue(
            all(sorted(sample.right_query) == ["d", "e", "e", "f"] for sample in samples)
        )

    def test_paired_random_samples_preserve_lengths(self) -> None:
        samples = paired_random_samples(
            left_length=3,
            right_length=5,
            corpus_text="aabbcc",
            samples=10,
            rng=random.Random(1),
        )

        self.assertTrue(all(len(sample.left_query) == 3 for sample in samples))
        self.assertTrue(all(len(sample.right_query) == 5 for sample in samples))
        self.assertTrue(all(set(sample.left_query) <= {"a", "b", "c"} for sample in samples))

    def test_tail_p_values_use_add_one_smoothing(self) -> None:
        self.assertEqual(p_value_ge(5, (1, 5, 7)), 0.75)
        self.assertEqual(p_value_le(5, (1, 5, 7)), 0.75)

    def test_resolve_corpus_jobs_caps_to_available_tasks(self) -> None:
        self.assertEqual(resolve_corpus_jobs(99, 4), 4)
        self.assertEqual(resolve_corpus_jobs(1, 4), 1)
        self.assertGreaterEqual(resolve_corpus_jobs(0, 4), 1)
        with self.assertRaises(ValueError):
            resolve_corpus_jobs(-1, 4)

    def test_run_corpus_analyses_falls_back_when_process_pool_denied(self) -> None:
        tasks = [
            ("FIRST", Path("first.toml"), {}, SimpleNamespace()),
            ("SECOND", Path("second.toml"), {}, SimpleNamespace()),
        ]

        with (
            patch.object(gog_magog, "ProcessPoolExecutor", side_effect=PermissionError("denied")),
            patch.object(gog_magog, "analyze_corpus_task", side_effect=lambda task: task[0]),
        ):
            self.assertEqual(run_corpus_analyses(tasks, jobs=2), ["FIRST", "SECOND"])

    def test_collect_hits_by_query_parallel_matches_serial(self) -> None:
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

        serial = collect_hits_by_query(
            corpus,
            ("αβ", "γδ"),
            min_skip=1,
            max_skip=4,
            direction="both",
            jobs=1,
        )
        parallel = collect_hits_by_query(
            corpus,
            ("αβ", "γδ"),
            min_skip=1,
            max_skip=4,
            direction="both",
            jobs=2,
        )

        self.assertEqual(parallel, serial)

    def test_score_pair_can_require_same_signed_skip(self) -> None:
        hits_by_query = {
            "gog": [
                HitLite("gog", 7, 10, 24),
                HitLite("gog", -7, 100, 86),
            ],
            "magog": [
                HitLite("magog", 7, 12, 40),
                HitLite("magog", -5, 100, 80),
            ],
        }

        metrics, examples = score_pair(
            "TEST",
            None,
            "gog",
            "magog",
            hits_by_query,
            max_gap=100,
            require_same_skip=True,
            keep_examples=True,
        )

        self.assertEqual(metrics.pairs_within_gap, 1)
        self.assertEqual(metrics.overlap_pairs, 1)
        self.assertEqual(len(examples), 1)
        self.assertEqual(examples[0].left_hit.skip, 7)
        self.assertEqual(examples[0].right_hit.skip, 7)

    def test_score_control_samples_preserves_duplicate_sample_rows(self) -> None:
        hits_by_query = {
            "aa": [HitLite("aa", 1, 0, 1)],
            "bb": [HitLite("bb", 1, 3, 4)],
            "cc": [],
        }
        samples = (
            ControlSample("aa", "bb"),
            ControlSample("aa", "bb"),
            ControlSample("aa", "cc"),
        )

        metrics = score_control_samples(
            "TEST",
            None,
            samples,
            hits_by_query,
            max_gap=10,
        )

        self.assertEqual(len(metrics), 3)
        self.assertEqual(metrics[0], metrics[1])
        self.assertEqual(metrics[0].pairs_within_gap, 1)
        self.assertEqual(metrics[2].pairs_within_gap, 0)

    def test_term_ids_for_corpus_accepts_custom_pairs(self) -> None:
        args = SimpleNamespace(
            left_hebrew_term_id="cyrus_h",
            right_hebrew_term_id="darius_h",
            left_greek_term_id="cyrus_g",
            right_greek_term_id="darius_g",
        )

        self.assertEqual(
            term_ids_for_corpus(SimpleNamespace(language="hebrew"), args),
            ("cyrus_h", "darius_h"),
        )
        self.assertEqual(
            term_ids_for_corpus(SimpleNamespace(language="greek"), args),
            ("cyrus_g", "darius_g"),
        )

    def test_parse_corpus_arg_requires_label_and_config(self) -> None:
        label, config = parse_corpus_arg("UHB=configs/example_uhb.toml")

        self.assertEqual(label, "UHB")
        self.assertEqual(str(config), "configs/example_uhb.toml")


if __name__ == "__main__":
    unittest.main()
