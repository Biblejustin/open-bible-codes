import csv
import tempfile
import unittest
from pathlib import Path

from scripts.compare_wrr_corrected_distance_variants import (
    parse_variant,
    read_variant_rows,
    write_markdown,
)


class WrrCorrectedDistanceVariantTests(unittest.TestCase):
    def test_parse_variant_requires_label_and_path(self) -> None:
        self.assertEqual(parse_variant("printed=summary.csv"), ("printed", Path("summary.csv")))
        with self.assertRaises(ValueError):
            parse_variant("summary.csv")
        with self.assertRaises(ValueError):
            parse_variant("=summary.csv")

    def test_read_variant_rows_adds_label_and_source_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "summary.csv"
            write_summary(path, defined="1", max_valid="12")

            rows = read_variant_rows([f"printed={path}"])

        self.assertEqual(rows[0]["variant"], "printed")
        self.assertEqual(rows[0]["defined_corrected_distances"], "1")
        self.assertEqual(rows[0]["max_pair_valid_perturbations"], "12")

    def test_write_markdown_lists_variant_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.md"
            write_markdown(
                path,
                [
                    {
                        "variant": "printed",
                        "pairs": "86",
                        "defined_corrected_distances": "0",
                        "ordinary_not_valid_pairs": "56",
                        "under_minimum_valid_pairs": "30",
                        "max_pair_valid_perturbations": "3",
                        "status": "diagnostic_only_not_wrr_reproduction",
                    }
                ],
            )

            text = path.read_text(encoding="utf-8")

        self.assertIn("`printed`", text)
        self.assertIn("| `printed` | 86 | 0 | 56 | 30 | 3 |", text)


def write_summary(path: Path, *, defined: str, max_valid: str) -> None:
    fieldnames = [
        "pairs",
        "candidate_lane",
        "search_max_skip",
        "skip_cap_mode",
        "skip_cap_formula",
        "minimum_valid",
        "defined_corrected_distances",
        "ordinary_not_valid_pairs",
        "under_minimum_valid_pairs",
        "min_corrected_distance",
        "min_corrected_pair_id",
        "max_pair_valid_perturbations",
        "status",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "pairs": "86",
                "candidate_lane": "length_5_8_smoke_candidate",
                "search_max_skip": "250",
                "skip_cap_mode": "term",
                "skip_cap_formula": "printed",
                "minimum_valid": "10",
                "defined_corrected_distances": defined,
                "ordinary_not_valid_pairs": "56",
                "under_minimum_valid_pairs": "30",
                "min_corrected_distance": "",
                "min_corrected_pair_id": "",
                "max_pair_valid_perturbations": max_valid,
                "status": "diagnostic_only_not_wrr_reproduction",
            }
        )


if __name__ == "__main__":
    unittest.main()
