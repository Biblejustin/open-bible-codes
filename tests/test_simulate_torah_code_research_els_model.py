import random
import tempfile
import unittest
from pathlib import Path

from scripts import simulate_torah_code_research_els_model as model


class TorahCodeResearchElsModelTests(unittest.TestCase):
    def test_random_els_offsets_fit_text(self) -> None:
        rng = random.Random(1)

        occurrence = model.random_els(rng, word_length=5, text_length=100, max_skip=20)

        offsets = occurrence.offsets()
        self.assertEqual(len(offsets), 5)
        self.assertGreaterEqual(min(offsets), 0)
        self.assertLess(max(offsets), 100)

    def test_resonant_widths_intersect_wrr_widths(self) -> None:
        self.assertEqual(
            model.resonant_row_widths(10, 20, row_width_count=2),
            (10,),
        )

    def test_combined_width_mode_uses_both_wrr_series(self) -> None:
        self.assertEqual(
            model.resonant_row_widths(
                10,
                20,
                row_width_count=2,
                row_width_mode="combined_wrr_series",
            ),
            (5, 10, 20),
        )

    def test_pair_distance_zero_for_identical_occurrences(self) -> None:
        occurrence = model.ElsOccurrence(start=10, skip=5, word_length=3)

        self.assertEqual(
            model.els_pair_distance(occurrence, occurrence, row_width_count=5),
            0,
        )

    def test_move_els_toward_target_reduces_start_gap(self) -> None:
        occurrence = model.ElsOccurrence(start=80, skip=2, word_length=4)
        target = model.ElsOccurrence(start=20, skip=2, word_length=4)

        moved = model.move_els_toward(
            occurrence,
            target,
            compactness_factor=0.25,
            text_length=100,
        )

        self.assertEqual(moved.start, 35)
        self.assertEqual(moved.skip, occurrence.skip)

    def test_projected_start_on_cylinder_wraps_shortest_column_path(self) -> None:
        self.assertEqual(
            model.projected_start_on_cylinder(
                9,
                0,
                row_width=10,
                compactness_factor=0.0,
            ),
            0,
        )
        self.assertEqual(
            model.projected_start_on_cylinder(
                9,
                0,
                row_width=10,
                compactness_factor=1.0,
            ),
            9,
        )

    def test_move_els_toward_meeting_reduces_cylinder_distance(self) -> None:
        occurrence = model.ElsOccurrence(start=90, skip=10, word_length=3)
        target = model.ElsOccurrence(start=10, skip=10, word_length=3)
        meeting = model.MeetingChoice(target=target, distance=8, row_width=10)

        moved = model.move_els_toward_meeting(
            occurrence,
            meeting,
            compactness_factor=0.25,
            text_length=200,
        )

        before = model.els_pair_distance_at_row_width(occurrence.offsets(), target.offsets(), 10)
        after = model.els_pair_distance_at_row_width(moved.offsets(), target.offsets(), 10)
        self.assertLess(after, before)
        self.assertEqual(moved.skip, occurrence.skip)

    def test_meeting_statistics_compare_mean_families(self) -> None:
        left = (model.ElsOccurrence(start=10, skip=5, word_length=3),)
        right = (model.ElsOccurrence(start=20, skip=5, word_length=3),)

        stats = model.meeting_statistics(left, right, row_width_count=5)

        self.assertEqual(stats["comparable_distances"], 2)
        self.assertEqual(stats["order_vector"], (2.0,))
        self.assertGreater(stats["arithmetic_mean"], 0)
        self.assertGreater(stats["geometric_mean"], 0)
        self.assertGreater(stats["harmonic_mean"], 0)
        self.assertEqual(stats["order_trimmed_mean"], stats["arithmetic_mean"])

    def test_order_statistic_vector_omits_smallest_distance(self) -> None:
        self.assertEqual(model.order_statistic_vector([3.0, 1.0, 2.0]), (2.0, 3.0))

    def test_fisher_order_weights_score_compact_vectors_lower(self) -> None:
        null_vectors = [(10.0, 12.0), (11.0, 13.0), (12.0, 14.0)]
        alternative_vectors = [(4.0, 6.0), (5.0, 7.0), (6.0, 8.0)]

        weights = model.fisher_order_weights(null_vectors, alternative_vectors)

        self.assertGreater(weights[0], 0)
        self.assertLess(
            model.dot(weights, alternative_vectors[0]),
            model.dot(weights, null_vectors[0]),
        )

    def test_summarize_setting_detects_strong_compactness_shift(self) -> None:
        rows = model.summarize_setting(
            els_count=6,
            left_word_length=3,
            right_word_length=3,
            text_length=300,
            max_skip=1,
            row_width_count=1,
            moved_fraction=1.0,
            compactness_factor=0.0,
            replicates=24,
            alpha=0.05,
            seed=7,
        )

        arithmetic = next(row for row in rows if row["statistic"] == "arithmetic_mean")
        fisher = next(row for row in rows if row["statistic"] == "fisher_order_split")
        self.assertEqual(arithmetic["row_width_mode"], "shared_intersection")
        self.assertGreater(float(arithmetic["null_mean"]), float(arithmetic["alternative_mean"]))
        self.assertGreater(float(arithmetic["power_p_le_alpha"]), 0.7)
        self.assertGreater(float(fisher["null_mean"]), float(fisher["alternative_mean"]))
        self.assertIn(
            arithmetic["interpretation"],
            {"moderate_power_for_declared_model", "high_power_for_declared_model"},
        )

    def test_main_writes_csv_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rc = model.main(
                [
                    "--els-count",
                    "4",
                    "--left-word-length",
                    "3",
                    "--right-word-length",
                    "3",
                    "--text-length",
                    "300",
                    "--max-skip",
                    "12",
                    "--row-width-count",
                    "4",
                    "--moved-fraction",
                    "0.5",
                    "--compactness-factor",
                    "0.25",
                    "--replicates",
                    "5",
                    "--out",
                    str(root / "out.csv"),
                    "--markdown-out",
                    str(root / "out.md"),
                    "--manifest-out",
                    str(root / "manifest.json"),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertTrue((root / "out.csv").exists())
            self.assertIn("row_width_mode", (root / "out.csv").read_text(encoding="utf-8"))
            self.assertIn("combined_wrr_series", (root / "out.csv").read_text(encoding="utf-8"))
            self.assertIn("level-1 ELS analogue", (root / "out.md").read_text(encoding="utf-8"))
            self.assertIn(
                "simulate_torah_code_research_els_model.py",
                (root / "manifest.json").read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
