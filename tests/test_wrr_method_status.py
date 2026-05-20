import csv
import tempfile
import unittest
from pathlib import Path

from scripts.build_wrr_method_status import FIELDNAMES, build_status_rows, main, markdown_cell, write_markdown


class WrrMethodStatusTests(unittest.TestCase):
    def test_build_status_rows_summarizes_open_method_decisions(self) -> None:
        rows = build_status_rows(
            text_row={
                "normalized_letters": "78064",
                "verse_count": "2075",
                "normalized_text_sha256": "abc123",
            },
            pair_row={
                "source_records": "32",
                "source_appellations": "174",
                "source_dates": "31",
                "source_undated_records": "2",
                "source_same_record_pairs": "182",
                "appellation_min_length_same_record_pairs": "165",
                "appellation_min_length": "5",
                "length_filtered_same_record_pairs": "86",
                "length_filter_min": "5",
                "length_filter_max": "8",
                "expected_published_pairs": "163",
            },
            skip_row={
                "rows": "120",
                "program_cap_lt_printed": "13",
                "program_cap_eq_printed": "107",
                "target_unreached_rows": "55",
            },
            variant_rows=[
                {"variant": "term_printed", "defined_corrected_distances": "0", "max_pair_valid_perturbations": "3"},
                {"variant": "fixed_250", "defined_corrected_distances": "0", "max_pair_valid_perturbations": "4"},
            ],
        )

        by_area = {row["decision_area"]: row for row in rows}
        self.assertEqual(by_area["Pair universe"]["status"], "open")
        self.assertIn("182 raw same-record pairs", by_area["Pair universe"]["evidence"])
        self.assertIn("163 cited second-list distances", by_area["Pair universe"]["evidence"])
        self.assertEqual(by_area["D(w) skip-cap formula"]["status"], "open")
        self.assertIn("13 program caps below printed", by_area["D(w) skip-cap formula"]["evidence"])
        self.assertEqual(by_area["Corrected distance c(w,w')"]["status"], "smoke_only")
        self.assertIn("maximum valid perturbation count 4", by_area["Corrected distance c(w,w')"]["evidence"])

    def test_markdown_cell_escapes_pipes(self) -> None:
        self.assertEqual(markdown_cell("a|b\nc"), "a\\|b c")

    def test_write_markdown_emits_matrix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "status.md"
            args = type(
                "Args",
                (),
                {
                    "text_source": Path("text.csv"),
                    "pair_summary": Path("pairs.csv"),
                    "skip_summary": Path("skip.csv"),
                    "corrected_distance_variants": Path("variants.csv"),
                    "out": Path("out.csv"),
                    "markdown_out": path,
                    "manifest_out": Path("manifest.json"),
                },
            )()
            write_markdown(
                path,
                [
                    {
                        "decision_area": "Pair universe",
                        "status": "open",
                        "current_read": "current",
                        "evidence": "evidence",
                        "next_action": "next",
                    }
                ],
                args,
            )

            text = path.read_text(encoding="utf-8")

        self.assertIn("# WRR Method Status", text)
        self.assertIn("| Pair universe | `open` | current | evidence | next |", text)

    def test_main_writes_csv_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            text_source = root / "text.csv"
            pair_summary = root / "pairs.csv"
            skip_summary = root / "skip.csv"
            variants = root / "variants.csv"
            out = root / "status.csv"
            markdown = root / "status.md"
            manifest = root / "manifest.json"
            write_dict_rows(
                text_source,
                [
                    {
                        "normalized_letters": "78064",
                        "verse_count": "2075",
                        "normalized_text_sha256": "abc123",
                    }
                ],
            )
            write_dict_rows(
                pair_summary,
                [
                    {
                        "source_records": "32",
                        "source_appellations": "174",
                        "source_dates": "31",
                        "source_undated_records": "2",
                        "source_same_record_pairs": "182",
                        "appellation_min_length_same_record_pairs": "165",
                        "appellation_min_length": "5",
                        "length_filtered_same_record_pairs": "86",
                        "length_filter_min": "5",
                        "length_filter_max": "8",
                        "expected_published_pairs": "163",
                    }
                ],
            )
            write_dict_rows(
                skip_summary,
                [
                    {
                        "rows": "120",
                        "program_cap_lt_printed": "13",
                        "program_cap_eq_printed": "107",
                        "target_unreached_rows": "55",
                    }
                ],
            )
            write_dict_rows(
                variants,
                [
                    {
                        "variant": "term_printed",
                        "defined_corrected_distances": "0",
                        "max_pair_valid_perturbations": "3",
                    }
                ],
            )

            rc = main(
                [
                    "--text-source",
                    str(text_source),
                    "--pair-summary",
                    str(pair_summary),
                    "--skip-summary",
                    str(skip_summary),
                    "--corrected-distance-variants",
                    str(variants),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            with out.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))

            self.assertEqual(rc, 0)
            self.assertEqual(rows[0]["decision_area"], "Genesis text stream")
            self.assertTrue(markdown.exists())
            self.assertTrue(manifest.exists())


def write_dict_rows(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = sorted({field for row in rows for field in row}) if rows else FIELDNAMES
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
