import csv
import tempfile
import unittest
from pathlib import Path

from els.cli import main
from els.skip_plan import (
    expected_hits_for_skip,
    letters_per_term_skip,
    max_possible_skip,
    plan_skip_cap,
    query_probability,
)


class SkipPlanTests(unittest.TestCase):
    def test_expected_hits_use_corpus_letter_frequency(self) -> None:
        self.assertEqual(query_probability("aaaa", "aa"), 1.0)
        self.assertEqual(expected_hits_for_skip(4, 2, 1.0, 1, "forward"), 3.0)
        self.assertEqual(expected_hits_for_skip(4, 2, 1.0, 1, "both"), 6.0)

    def test_full_span_and_letters_per_term_skip_caps(self) -> None:
        self.assertEqual(max_possible_skip(44, 5), 10)
        self.assertEqual(letters_per_term_skip(44, 5), 8)

    def test_plan_selects_largest_skip_under_target(self) -> None:
        plan = plan_skip_cap(
            "aaaa",
            "aa",
            "aa",
            min_skip=1,
            max_skip_limit=3,
            direction="forward",
            target_expected_hits=5,
        )

        self.assertEqual(plan.selected_max_skip, 2)
        self.assertEqual(plan.expected_hits, 5.0)
        self.assertEqual(plan.status, "capped_by_target")

    def test_cli_skip_plan_writes_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.txt"
            config = root / "source.toml"
            out = root / "skip_plan.csv"
            source.write_text("αααα", encoding="utf-8")
            config.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        'language = "greek"',
                        "",
                        "[[sources]]",
                        'name = "sample"',
                        'format = "text"',
                        'path = "source.txt"',
                        'ref = "Sample 1:1"',
                    ]
                ),
                encoding="utf-8",
            )

            exit_code = main(
                [
                    "skip-plan",
                    "--config",
                    str(config),
                    "--term",
                    "αα",
                    "--min-skip",
                    "1",
                    "--max-skip-limit",
                    "3",
                    "--direction",
                    "forward",
                    "--target-expected-hits",
                    "5",
                    "--out",
                    str(out),
                ]
            )
            with out.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))

        self.assertEqual(exit_code, 0)
        self.assertEqual(rows[0]["selected_max_skip"], "2")
        self.assertEqual(rows[0]["status"], "capped_by_target")


if __name__ == "__main__":
    unittest.main()
