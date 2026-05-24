import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from scripts import analyze_pair_baselines as pair_baselines
from scripts.analyze_pair_baselines import BASELINE_PAIRS, run_corpus_analyses, selected_corpora


class PairBaselinesTests(unittest.TestCase):
    def test_baseline_pairs_have_unique_ids_and_gog_target(self) -> None:
        pair_ids = [pair.pair_id for pair in BASELINE_PAIRS]

        self.assertEqual(len(pair_ids), len(set(pair_ids)))
        self.assertIn("gog_magog", pair_ids)

    def test_baseline_pairs_have_language_specific_terms(self) -> None:
        for pair in BASELINE_PAIRS:
            with self.subTest(pair=pair.pair_id):
                self.assertTrue(pair.left_hebrew.endswith("_h"))
                self.assertTrue(pair.right_hebrew.endswith("_h"))
                self.assertTrue(pair.left_greek.endswith("_g"))
                self.assertTrue(pair.right_greek.endswith("_g"))

    def test_selected_corpora_accepts_explicit_subset(self) -> None:
        selected = selected_corpora(
            SimpleNamespace(corpus=[("UHB", "configs/example_uhb.toml")])
        )

        self.assertEqual(selected, [("UHB", "configs/example_uhb.toml")])

    def test_run_corpus_analyses_falls_back_when_process_pool_denied(self) -> None:
        tasks = [
            ("FIRST", Path("first.toml"), {}, SimpleNamespace()),
            ("SECOND", Path("second.toml"), {}, SimpleNamespace()),
        ]

        with (
            patch.object(pair_baselines, "ProcessPoolExecutor", side_effect=PermissionError("denied")),
            patch.object(pair_baselines, "analyze_corpus_task", side_effect=lambda task: task[0]),
        ):
            self.assertEqual(run_corpus_analyses(tasks, jobs=2), ["FIRST", "SECOND"])


if __name__ == "__main__":
    unittest.main()
