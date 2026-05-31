import unittest

from scripts.merge_wrr_corrected_distance_shards import (
    merge_rows,
    summarize_merged_rows,
    validate_merge_inputs,
)


class WrrCorrectedDistanceShardMergeTests(unittest.TestCase):
    def test_merge_rows_sorts_and_rejects_duplicates(self) -> None:
        rows = merge_rows(
            [[row("p2", "defined", "0.4", 10)], [row("p1", "ordinary_not_valid", "", 0)]]
        )

        self.assertEqual([item["pair_id"] for item in rows], ["p1", "p2"])
        with self.assertRaises(ValueError):
            merge_rows(
                [[row("p1", "defined", "0.2", 10)], [row("p1", "defined", "0.3", 10)]]
            )

    def test_summarize_merged_rows_uses_shard_summary_parameters(self) -> None:
        rows = [
            row("p1", "ordinary_not_valid", "", 0),
            row("p2", "under_minimum_valid_perturbations", "", 4),
            row("p3", "defined", "0.2", 10),
        ]
        summaries = [
            summary("0", "2"),
            summary("1", "2"),
        ]

        result = summarize_merged_rows(rows, summaries)

        self.assertEqual(result["selected_pairs"], "3")
        self.assertEqual(result["shard_index"], "merged")
        self.assertEqual(result["shard_count"], "2")
        self.assertEqual(result["pairs"], 3)
        self.assertEqual(result["defined_corrected_distances"], 1)
        self.assertEqual(result["ordinary_not_valid_pairs"], 1)
        self.assertEqual(result["under_minimum_valid_pairs"], 1)
        self.assertEqual(result["min_corrected_pair_id"], "p3")
        self.assertEqual(result["max_pair_valid_perturbations"], 10)

    def test_validate_merge_inputs_requires_complete_shard_set(self) -> None:
        rows = [
            row("p1", "ordinary_not_valid", "", 0),
            row("p2", "under_minimum_valid_perturbations", "", 4),
        ]

        with self.assertRaisesRegex(ValueError, "expected \\[0, 1\\]"):
            validate_merge_inputs(rows, [summary("0", "2", pairs="2")], expected_shard_count=2)

    def test_validate_merge_inputs_checks_row_counts(self) -> None:
        rows = [row("p1", "ordinary_not_valid", "", 0)]

        with self.assertRaisesRegex(ValueError, "shard summaries report 2 rows"):
            validate_merge_inputs(
                rows,
                [summary("0", "2", pairs="1"), summary("1", "2", pairs="1")],
            )


def row(
    pair_id: str,
    status: str,
    corrected_distance: str,
    valid_perturbations: int,
) -> dict[str, str]:
    return {
        "pair_id": pair_id,
        "corrected_distance_status": status,
        "corrected_distance": corrected_distance,
        "pair_valid_perturbations": str(valid_perturbations),
    }


def summary(shard_index: str, shard_count: str, *, pairs: str = "0") -> dict[str, str]:
    return {
        "selected_pairs": "3",
        "shard_index": shard_index,
        "shard_count": shard_count,
        "pairs": pairs,
        "candidate_lane": "length_5_8_smoke_candidate",
        "search_max_skip": "250",
        "skip_cap_mode": "term",
        "skip_cap_formula": "printed",
        "minimum_valid": "10",
    }


if __name__ == "__main__":
    unittest.main()
