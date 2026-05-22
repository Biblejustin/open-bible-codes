import csv
import tempfile
import unittest
from pathlib import Path

from scripts import analyze_wrr_dw_formula_sensitivity as sensitivity


class WrrDwFormulaSensitivityTests(unittest.TestCase):
    def test_changed_pair_rows_detects_formula_differences(self) -> None:
        changed = sensitivity.changed_pair_rows(
            [
                row("p1", "defined", "0.1", "10"),
                row("p2", "ordinary_not_valid", "", "0"),
            ],
            [
                row("p1", "defined", "0.1", "10"),
                row("p2", "defined", "0.2", "11"),
                row("p3", "defined", "0.3", "12"),
            ],
        )

        self.assertEqual([item["pair_id"] for item in changed], ["p2", "p3"])
        self.assertIn("corrected_distance_status", changed[0]["changed_fields"])
        self.assertIn("missing_from_printed", changed[1]["changed_fields"])

    def test_build_summary_rows_keeps_formula_unselected(self) -> None:
        summary = sensitivity.build_summary_rows(
            skip_row={
                "rows": "120",
                "skip_cap_formula": "printed",
                "program_cap_lt_printed": "13",
                "program_cap_eq_printed": "107",
                "program_cap_gt_printed": "0",
                "target_unreached_rows": "55",
                "program_target_unreached_rows": "55",
            },
            variant_rows=[
                variant("term_printed", "86", "printed", "28", "56", "2"),
                variant("term_program", "86", "program", "28", "56", "2"),
                variant("fixed_250", "86", "printed", "28", "56", "2"),
            ],
            direct_printed_summary=direct_summary("printed", "72", "110", "0"),
            direct_program_summary=direct_summary("program", "72", "110", "0"),
            changed_rows=[],
        )

        by_scope = {row["scope"]: row for row in summary}
        self.assertEqual(by_scope["skip_cap_profile"]["program_cap_lt_printed"], "13")
        self.assertEqual(
            by_scope["smoke_length_5_8_cap250"]["program_defined_corrected_distances"],
            "28",
        )
        self.assertEqual(by_scope["all_lanes_cap1000"]["changed_pairs"], 0)
        self.assertIn("no D(w) formula selected", by_scope["all_lanes_cap1000"]["diagnostic_read"])

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skip = root / "skip.csv"
            variants = root / "variants.csv"
            printed_summary = root / "printed_summary.csv"
            program_summary = root / "program_summary.csv"
            printed = root / "printed.csv"
            program = root / "program.csv"
            out = root / "out.csv"
            changed = root / "changed.csv"
            markdown = root / "out.md"
            manifest = root / "manifest.json"
            write_csv(
                skip,
                [
                    {
                        "rows": "120",
                        "skip_cap_formula": "printed",
                        "program_cap_lt_printed": "13",
                        "program_cap_eq_printed": "107",
                        "program_cap_gt_printed": "0",
                        "target_unreached_rows": "55",
                        "program_target_unreached_rows": "55",
                    }
                ],
            )
            write_csv(
                variants,
                [
                    variant("term_printed", "86", "printed", "28", "56", "2"),
                    variant("term_program", "86", "program", "28", "56", "2"),
                    variant("fixed_250", "86", "printed", "28", "56", "2"),
                ],
            )
            write_csv(printed_summary, [direct_summary("printed", "72", "110", "0")])
            write_csv(program_summary, [direct_summary("program", "72", "110", "0")])
            write_csv(printed, [row("p1", "defined", "0.1", "10")])
            write_csv(program, [row("p1", "defined", "0.1", "10")])

            rc = sensitivity.main(
                [
                    "--skip-summary",
                    str(skip),
                    "--variants",
                    str(variants),
                    "--direct-printed-summary",
                    str(printed_summary),
                    "--direct-program-summary",
                    str(program_summary),
                    "--direct-printed",
                    str(printed),
                    "--direct-program",
                    str(program),
                    "--out",
                    str(out),
                    "--changed-out",
                    str(changed),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 3)
            self.assertEqual(len(list(csv.DictReader(changed.open(encoding="utf-8")))), 0)
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("WRR D(w) Formula Sensitivity", text)
            self.assertIn("No pair rows changed", text)
            self.assertTrue(manifest.exists())


def variant(
    name: str,
    pairs: str,
    formula: str,
    defined: str,
    ordinary_invalid: str,
    under_minimum: str,
) -> dict[str, str]:
    return {
        "variant": name,
        "pairs": pairs,
        "skip_cap_formula": formula,
        "defined_corrected_distances": defined,
        "ordinary_not_valid_pairs": ordinary_invalid,
        "under_minimum_valid_pairs": under_minimum,
    }


def direct_summary(formula: str, defined: str, ordinary_invalid: str, under_minimum: str) -> dict[str, str]:
    return {
        "pairs": "182",
        "skip_cap_formula": formula,
        "defined_corrected_distances": defined,
        "ordinary_not_valid_pairs": ordinary_invalid,
        "under_minimum_valid_pairs": under_minimum,
    }


def row(pair_id: str, status: str, distance: str, valid: str) -> dict[str, str]:
    return {
        "pair_id": pair_id,
        "concept": "WRR2 01",
        "corrected_distance_status": status,
        "corrected_distance": distance,
        "pair_valid_perturbations": valid,
        "ordinary_q": distance,
        "appellation_defined_perturbed_rows": valid,
        "date_defined_perturbed_rows": valid,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
