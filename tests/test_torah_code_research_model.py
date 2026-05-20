import random
import tempfile
import unittest
from pathlib import Path

from scripts import simulate_torah_code_research_model as model


class TorahCodeResearchModelTests(unittest.TestCase):
    def test_nearest_point_uses_euclidean_distance(self) -> None:
        point = model.Point(0.8, 0.8)
        candidates = (model.Point(0.0, 0.0), model.Point(0.7, 0.7))

        self.assertEqual(model.nearest_point(point, candidates), model.Point(0.7, 0.7))

    def test_move_toward_nearest_with_zero_factor_lands_on_target(self) -> None:
        fixed = (model.Point(0.0, 0.0),)
        moving = (model.Point(1.0, 0.0), model.Point(0.0, 1.0))

        moved = model.move_toward_nearest(
            fixed,
            moving,
            moved_fraction=1.0,
            closeness_factor=0.0,
            rng=random.Random(1),
        )

        self.assertEqual(moved, (model.Point(0.0, 0.0), model.Point(0.0, 0.0)))

    def test_left_tail_p_value_uses_add_one_smoothing(self) -> None:
        self.assertEqual(model.left_tail_p_value([0.2, 0.3, 0.4], 0.1), 0.25)
        self.assertEqual(model.left_tail_p_value([0.2, 0.3, 0.4], 0.3), 0.75)

    def test_summarize_setting_detects_strong_compactness_shift(self) -> None:
        row = model.summarize_setting(
            point_count=12,
            moved_fraction=1.0,
            closeness_factor=0.0,
            replicates=20,
            alpha=0.05,
            seed=7,
        )

        self.assertEqual(row["alternative_mean"], "0")
        self.assertGreater(float(row["null_mean"]), 0)
        self.assertGreater(float(row["power_p_le_alpha"]), 0.9)
        self.assertEqual(row["interpretation"], "high_power_for_declared_model")

    def test_main_writes_csv_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rc = model.main(
                [
                    "--point-count",
                    "8",
                    "--moved-fraction",
                    "0.5",
                    "--closeness-factor",
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
            self.assertIn("simulation harness", (root / "out.md").read_text(encoding="utf-8"))
            self.assertIn("simulate_torah_code_research_model.py", (root / "manifest.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
