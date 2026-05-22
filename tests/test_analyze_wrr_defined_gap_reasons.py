import csv
import tempfile
import unittest
from pathlib import Path

from scripts import analyze_wrr_defined_gap_reasons as audit


class WrrDefinedGapReasonTests(unittest.TestCase):
    def test_reason_for_row_classifies_ordinary_missing_sides(self) -> None:
        self.assertEqual(
            audit.reason_for_row(
                {
                    "corrected_distance_status": "ordinary_not_valid",
                    "appellation_ordinary_hits": "0",
                    "date_ordinary_hits": "4",
                    "pair_valid_perturbations": "0",
                }
            ),
            audit.REASON_ORDINARY_NO_APPELLATION,
        )
        self.assertEqual(
            audit.reason_for_row(
                {
                    "corrected_distance_status": "ordinary_not_valid",
                    "appellation_ordinary_hits": "3",
                    "date_ordinary_hits": "0",
                    "pair_valid_perturbations": "0",
                }
            ),
            audit.REASON_ORDINARY_NO_DATE,
        )
        self.assertEqual(
            audit.reason_for_row(
                {
                    "corrected_distance_status": "ordinary_not_valid",
                    "appellation_ordinary_hits": "2",
                    "date_ordinary_hits": "5",
                    "pair_valid_perturbations": "0",
                }
            ),
            audit.REASON_ORDINARY_NO_SHARED_DEFINED,
        )

    def test_summarize_run_reports_defined_gap(self) -> None:
        run = audit.RunSpec("sample", Path("sample.csv"))
        rows = [
            {"corrected_distance_status": "defined"},
            {
                "corrected_distance_status": "ordinary_not_valid",
                "appellation_ordinary_hits": "0",
                "date_ordinary_hits": "7",
                "pair_valid_perturbations": "0",
            },
            {
                "corrected_distance_status": "under_minimum_valid_perturbations",
                "appellation_ordinary_hits": "2",
                "date_ordinary_hits": "7",
                "pair_valid_perturbations": "4",
            },
        ]

        summary = audit.summarize_run(run, rows, expected_defined=5)
        by_reason = {row["reason"]: row for row in summary}

        self.assertEqual(by_reason[audit.REASON_DEFINED]["run_defined"], 1)
        self.assertEqual(by_reason[audit.REASON_DEFINED]["run_gap_to_source_cited"], 4)
        self.assertEqual(by_reason[audit.REASON_ORDINARY_NO_APPELLATION]["pairs"], 1)
        self.assertEqual(by_reason[audit.REASON_UNDER_MINIMUM]["pairs"], 1)

    def test_main_writes_reason_term_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pair_summary = root / "pair_summary.csv"
            pair_table = root / "pair_table.csv"
            corrected = root / "corrected.csv"
            out = root / "out.csv"
            term_out = root / "terms.csv"
            markdown = root / "out.md"
            manifest = root / "manifest.json"
            write_csv(pair_summary, [{"expected_published_pairs": "3"}])
            write_csv(
                pair_table,
                [
                    {
                        "pair_id": "p1",
                        "concept": "WRR2 01",
                        "candidate_lane": "sample_lane",
                        "appellation_term_id": "app1",
                        "appellation_term": "APP",
                        "appellation_normalized": "APP",
                        "date_term_id": "date1",
                        "date_term": "DATE",
                        "date_normalized": "DATE",
                    },
                    {
                        "pair_id": "p2",
                        "concept": "WRR2 02",
                        "candidate_lane": "sample_lane",
                        "appellation_term_id": "app2",
                        "appellation_term": "APP2",
                        "appellation_normalized": "APP2",
                        "date_term_id": "date2",
                        "date_term": "DATE2",
                        "date_normalized": "DATE2",
                    },
                ],
            )
            write_csv(
                corrected,
                [
                    {
                        "pair_id": "p1",
                        "corrected_distance_status": "defined",
                        "appellation_ordinary_hits": "2",
                        "date_ordinary_hits": "3",
                        "pair_valid_perturbations": "10",
                        "appellation_defined_perturbed_rows": "4",
                        "date_defined_perturbed_rows": "5",
                        "appellation_triples_with_defined_rows": "4",
                        "date_triples_with_defined_rows": "5",
                    },
                    {
                        "pair_id": "p2",
                        "corrected_distance_status": "ordinary_not_valid",
                        "appellation_ordinary_hits": "0",
                        "date_ordinary_hits": "3",
                        "pair_valid_perturbations": "0",
                        "appellation_defined_perturbed_rows": "0",
                        "date_defined_perturbed_rows": "5",
                        "appellation_triples_with_defined_rows": "0",
                        "date_triples_with_defined_rows": "5",
                    },
                ],
            )

            rc = audit.main(
                [
                    "--pair-summary",
                    str(pair_summary),
                    "--pair-table",
                    str(pair_table),
                    "--run",
                    f"sample={corrected}",
                    "--out",
                    str(out),
                    "--term-out",
                    str(term_out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            rows = list(csv.DictReader(out.open(encoding="utf-8")))
            by_reason = {row["reason"]: row for row in rows}
            self.assertEqual(by_reason[audit.REASON_DEFINED]["run_defined"], "1")
            self.assertEqual(by_reason[audit.REASON_ORDINARY_NO_APPELLATION]["pairs"], "1")
            term_rows = list(csv.DictReader(term_out.open(encoding="utf-8")))
            self.assertEqual(term_rows[0]["term_id"], "app2")
            self.assertEqual(term_rows[0]["concepts"], "WRR2 02")
            self.assertEqual(term_rows[0]["candidate_lanes"], "sample_lane")
            self.assertEqual(term_rows[0]["pair_ids"], "p2")
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("WRR Defined Gap Reason Audit", text)
            self.assertIn("Gap to the source-cited count remains 2", text)
            self.assertTrue(manifest.exists())


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
