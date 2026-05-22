import unittest

from scripts.analyze_wrr_cross_pair_permutations import (
    analyze_permutations,
    build_pair_index,
    row_concepts,
    rows_for_mapping,
    source_concepts,
    statistic_row,
    summarize_samples,
)


class WrrCrossPairPermutationsTests(unittest.TestCase):
    def test_row_concepts_parses_same_and_cross_labels(self) -> None:
        self.assertEqual(row_concepts({"concept": "WRR2 01"}), ("WRR2 01", "WRR2 01"))
        self.assertEqual(
            row_concepts({"concept": "WRR2 01->WRR2 02"}),
            ("WRR2 01", "WRR2 02"),
        )

    def test_rows_for_mapping_selects_concept_cross_pairs(self) -> None:
        rows = [
            row("a_a", "WRR2 01", "0.1"),
            row("a_b", "WRR2 01->WRR2 02", "0.4"),
            row("b_a", "WRR2 02->WRR2 01", "0.2"),
            row("b_b", "WRR2 02", "0.3"),
        ]

        selected = rows_for_mapping(
            build_pair_index(rows),
            {"WRR2 01": "WRR2 02", "WRR2 02": "WRR2 01"},
        )

        self.assertEqual([item["pair_id"] for item in selected], ["a_b", "b_a"])

    def test_analyze_permutations_emits_observed_and_seeded_samples(self) -> None:
        rows = [
            row("a_a", "WRR2 01", "0.1"),
            row("a_b", "WRR2 01->WRR2 02", "0.4"),
            row("b_a", "WRR2 02->WRR2 01", "0.2"),
            row("b_b", "WRR2 02", "0.3"),
        ]

        samples, summary = analyze_permutations(
            rows,
            source="input.csv",
            permutations=3,
            seed=7,
            p1_threshold=0.2,
        )

        self.assertEqual(source_concepts(rows), ["WRR2 01", "WRR2 02"])
        self.assertEqual(len(samples), 4)
        self.assertEqual(samples[0]["sample_type"], "observed")
        self.assertEqual(samples[0]["rows"], 2)
        self.assertEqual(summary["permutations"], 3)
        self.assertEqual(summary["concepts"], 2)
        self.assertEqual(summary["status"], "diagnostic_only_not_wrr_reproduction")

    def test_summarize_samples_computes_metric_rhos_and_rho0(self) -> None:
        concepts = ["WRR2 01", "WRR2 02"]
        samples = [
            sample("observed", -1, "0.1", "0.2", "0.3", "0.4"),
            sample("permutation", 0, "0.2", "0.3", "0.4", "0.5"),
            sample("permutation", 1, "0.05", "0.1", "0.2", "0.3"),
        ]

        summary = summarize_samples(
            samples,
            source="input.csv",
            permutations=2,
            seed=1,
            concepts=concepts,
        )

        self.assertEqual(summary["rho_p1"], "0.666666666667")
        self.assertEqual(summary["rho_p2"], "0.666666666667")
        self.assertEqual(summary["rho0_bonferroni"], "2.66666666667")

    def test_statistic_row_records_p3_p4_non_rabbi_subset(self) -> None:
        rows = [
            row("rabbi", "WRR2 01", "0.1", rabbi_title="True"),
            row("plain", "WRR2 02", "0.3", rabbi_title="False"),
        ]

        stats = statistic_row(
            rows,
            sample_type="observed",
            permutation_index=-1,
            seed=1,
            concepts=["WRR2 01", "WRR2 02"],
            date_order=("WRR2 01", "WRR2 02"),
            p1_threshold=0.2,
        )

        self.assertEqual(stats["rows"], 2)
        self.assertEqual(stats["defined_corrected_distances"], 2)
        self.assertEqual(stats["p3_p4_sample_rows"], 1)
        self.assertEqual(stats["p3_p4_sample_defined_corrected_distances"], 1)


def row(
    pair_id: str,
    concept: str,
    corrected_distance: str,
    *,
    rabbi_title: str = "False",
) -> dict[str, str]:
    return {
        "pair_id": pair_id,
        "concept": concept,
        "corrected_distance": corrected_distance,
        "corrected_distance_status": "defined",
        "appellation_starts_with_rabbi_title": rabbi_title,
    }


def sample(
    sample_type: str,
    permutation_index: int,
    p1: str,
    p2: str,
    p3: str,
    p4: str,
) -> dict[str, object]:
    return {
        "sample_type": sample_type,
        "permutation_index": permutation_index,
        "rows": 2,
        "defined_corrected_distances": 2,
        "identity_mapping": "false",
        "p1": p1,
        "p2": p2,
        "p3": p3,
        "p4": p4,
    }


if __name__ == "__main__":
    unittest.main()
