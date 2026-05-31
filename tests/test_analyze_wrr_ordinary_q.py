import csv
import tempfile
import unittest
from pathlib import Path

from els.wrr import WrrElsOccurrence
from scripts.analyze_wrr_ordinary_q import (
    DomainSummary,
    build_q_rows,
    read_defined_occurrences,
    summarize_lane_rows,
    summarize_q_rows,
)


class WrrOrdinaryQTests(unittest.TestCase):
    def test_read_defined_occurrences_reconstructs_signed_offsets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "domains.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "term_id",
                        "normalized_length",
                        "skip",
                        "start_offset",
                        "domain_status",
                        "domain_start",
                        "domain_end",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "term_id": "app",
                        "normalized_length": "4",
                        "skip": "-3",
                        "start_offset": "20",
                        "domain_status": "defined",
                        "domain_start": "0",
                        "domain_end": "30",
                    }
                )
                writer.writerow(
                    {
                        "term_id": "app",
                        "normalized_length": "4",
                        "skip": "3",
                        "start_offset": "1",
                        "domain_status": "undefined",
                        "domain_start": "",
                        "domain_end": "",
                    }
                )

            occurrences = read_defined_occurrences(path)

        self.assertEqual(
            occurrences["app"],
            (WrrElsOccurrence((20, 17, 14, 11), -3, 0, 30),),
        )

    def test_build_q_rows_reports_complete_and_incomplete_pairs(self) -> None:
        pair_rows = [
            pair_row("p1", "app", "date"),
            pair_row("p2", "empty", "date"),
        ]
        summaries = {
            "app": DomainSummary(hit_count=1, defined_domains=1, undefined_domains=0),
            "date": DomainSummary(hit_count=2, defined_domains=1, undefined_domains=1),
            "empty": DomainSummary(hit_count=0, defined_domains=0, undefined_domains=0),
        }
        occurrences = {
            "app": (WrrElsOccurrence((0, 10, 20), 10, 0, 50),),
            "date": (WrrElsOccurrence((11, 21, 31), 10, 10, 40),),
        }

        rows = build_q_rows(
            pair_rows,
            summaries,
            occurrences,
            text_length=100,
            row_width_count=1,
        )
        summary = summarize_q_rows(rows)

        self.assertEqual(rows[0]["ordinary_q_defined_only"], "0.2")
        self.assertEqual(rows[0]["q_status"], "defined_domain_only_incomplete")
        self.assertEqual(rows[1]["ordinary_q_defined_only"], "")
        self.assertEqual(rows[1]["q_status"], "no_defined_domain_pair")
        self.assertEqual(summary["pairs"], 2)
        self.assertEqual(summary["pairs_with_defined_domain_pair"], 1)
        self.assertEqual(summary["defined_only_incomplete_pairs"], 1)
        self.assertEqual(summary["no_defined_domain_pair_pairs"], 1)
        self.assertEqual(summary["max_q_pair_id"], "p1")

    def test_summarize_lane_rows_splits_candidate_lanes(self) -> None:
        pair_rows = [
            pair_row("p1", "app", "date", lane="length_5_8_smoke_candidate"),
            pair_row("p2", "empty", "date", lane="excluded_by_appellation_min_length"),
        ]
        summaries = {
            "app": DomainSummary(hit_count=1, defined_domains=1, undefined_domains=0),
            "date": DomainSummary(hit_count=1, defined_domains=1, undefined_domains=0),
            "empty": DomainSummary(hit_count=0, defined_domains=0, undefined_domains=0),
        }
        occurrences = {
            "app": (WrrElsOccurrence((0, 10, 20), 10, 0, 50),),
            "date": (WrrElsOccurrence((11, 21, 31), 10, 10, 40),),
        }

        rows = build_q_rows(
            pair_rows,
            summaries,
            occurrences,
            text_length=100,
            row_width_count=1,
        )
        lane_rows = summarize_lane_rows(rows)

        lanes = {row["candidate_lane"]: row for row in lane_rows}
        self.assertEqual(lanes["length_5_8_smoke_candidate"]["pairs"], 1)
        self.assertEqual(
            lanes["length_5_8_smoke_candidate"]["all_observed_domains_defined_pairs"],
            1,
        )
        self.assertEqual(
            lanes["excluded_by_appellation_min_length"]["no_defined_domain_pair_pairs"],
            1,
        )


def pair_row(
    pair_id: str,
    app_id: str,
    date_id: str,
    *,
    lane: str = "length_5_8_smoke_candidate",
) -> dict[str, str]:
    return {
        "pair_id": pair_id,
        "concept": "WRR2 01",
        "candidate_lane": lane,
        "pair_review_status": "needs_primary_source_pair_rule",
        "appellation_term_id": app_id,
        "date_term_id": date_id,
    }


if __name__ == "__main__":
    unittest.main()
