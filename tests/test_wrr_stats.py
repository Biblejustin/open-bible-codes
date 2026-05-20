import math
import unittest

from els.wrr import (
    binomial_upper_tail,
    bonferroni_rho0,
    corrected_distance_rank,
    corrected_distance_strict_rank,
    corrected_distance_wrr_rank,
    cylindrical_letter_distance_squared,
    els_window_count,
    expected_els_count,
    is_perturbed_els_match,
    iter_perturbed_els_matches,
    nearest_integer_half_up,
    ordinary_els_offsets,
    p1_binomial_tail,
    p2_product_statistic,
    perturbation_triples,
    perturbed_offsets,
    permutation_rank_rho,
    product_uniform_cdf_from_log,
    relative_letter_frequencies,
    skip_cap_for_expected_count,
    WrrElsOccurrence,
    wrr_domain_intersection_length,
    wrr_domain_weight,
    wrr_els_els_alpha,
    wrr_els_els_distance_at_row_width,
    wrr_els_els_proximity_at_row_width,
    wrr_label_minimality_domains,
    wrr_minimality_domain,
    wrr_minimality_domain_candidates,
    wrr_offsets_span,
    wrr_ordinary_els_els_alpha,
    wrr_corrected_distance_from_perturbation_sets,
    wrr_weighted_els_pair_proximity,
    wrr_word_pair_proximity,
    wrr2_els_sl_distance_at_row_width,
    wrr2_els_sl_proximity,
    wrr2_els_sl_proximity_at_row_width,
    wrr2_ordinary_els_sl_proximity,
    wrr_row_widths,
)


class WrrStatsTests(unittest.TestCase):
    def test_perturbation_triples_default_to_wrr_radius_two(self) -> None:
        triples = perturbation_triples()

        self.assertEqual(len(triples), 125)
        self.assertIn((-2, -2, -2), triples)
        self.assertIn((0, 0, 0), triples)
        self.assertIn((2, 2, 2), triples)

    def test_perturbed_offsets_preserve_unperturbed_prefix(self) -> None:
        offsets = perturbed_offsets(
            start=10,
            skip=4,
            word_length=5,
            perturbation=(1, -2, 3),
        )

        self.assertEqual(offsets, (10, 14, 19, 21, 28))

    def test_zero_perturbation_offsets_match_ordinary_els(self) -> None:
        offsets = perturbed_offsets(
            start=7,
            skip=3,
            word_length=6,
            perturbation=(0, 0, 0),
        )

        self.assertEqual(offsets, (7, 10, 13, 16, 19, 22))

    def test_perturbed_offsets_support_negative_skips(self) -> None:
        offsets = perturbed_offsets(
            start=20,
            skip=-3,
            word_length=4,
            perturbation=(1, 1, -2),
        )

        self.assertEqual(offsets, (20, 18, 16, 11))

    def test_perturbed_els_match_checks_actual_letters(self) -> None:
        text = "AXXBXCXD"

        self.assertTrue(is_perturbed_els_match(text, "ABCD", 0, 2, (1, 0, 0)))
        self.assertFalse(is_perturbed_els_match(text, "ABCD", 0, 2, (0, 0, 0)))

    def test_perturbed_els_match_returns_false_outside_text(self) -> None:
        self.assertFalse(is_perturbed_els_match("ABC", "ABCD", 0, 1, (0, 0, 0)))

    def test_iter_perturbed_els_matches_finds_forward_hits(self) -> None:
        matches = list(
            iter_perturbed_els_matches(
                "AXXBXCXD",
                "ABCD",
                min_skip=2,
                max_skip=2,
                direction="forward",
                perturbation=(1, 0, 0),
            )
        )

        self.assertEqual(matches, [(0, 2, (0, 3, 5, 7))])

    def test_iter_perturbed_els_matches_finds_backward_hits(self) -> None:
        matches = list(
            iter_perturbed_els_matches(
                "DXCXBXXA",
                "ABCD",
                min_skip=2,
                max_skip=2,
                direction="backward",
                perturbation=(-1, 0, 0),
            )
        )

        self.assertEqual(matches, [(7, -2, (7, 4, 2, 0))])

    def test_nearest_integer_half_up_rounds_halves_upward(self) -> None:
        self.assertEqual(nearest_integer_half_up(10, 3), 3)
        self.assertEqual(nearest_integer_half_up(10, 4), 3)
        self.assertEqual(nearest_integer_half_up(9, 2), 5)

    def test_wrr_row_widths_preserve_ordered_first_widths(self) -> None:
        self.assertEqual(wrr_row_widths(10, count=5), (10, 5, 3, 3, 2))
        self.assertEqual(wrr_row_widths(-9, count=4), (9, 5, 3, 2))

    def test_wrr_row_widths_stay_positive_for_small_skips(self) -> None:
        self.assertEqual(wrr_row_widths(2, count=5), (2, 1, 1, 1, 1))

    def test_ordinary_els_offsets_follow_signed_skip(self) -> None:
        self.assertEqual(ordinary_els_offsets(20, -3, 4), (20, 17, 14, 11))

    def test_cylindrical_letter_distance_wraps_columns(self) -> None:
        self.assertEqual(cylindrical_letter_distance_squared(0, 9, 10), 1)
        self.assertEqual(cylindrical_letter_distance_squared(0, 10, 10), 1)
        self.assertEqual(cylindrical_letter_distance_squared(0, 11, 10), 2)

    def test_wrr2_els_sl_distance_uses_source_formula(self) -> None:
        distance = wrr2_els_sl_distance_at_row_width(
            (0, 10, 20),
            sl_start=1,
            sl_length=3,
            row_width=10,
        )

        self.assertEqual(distance, 4)

    def test_wrr2_els_sl_proximity_is_inverse_distance(self) -> None:
        proximity = wrr2_els_sl_proximity_at_row_width(
            (0, 10, 20),
            sl_start=1,
            sl_length=3,
            row_width=10,
        )

        self.assertEqual(proximity, 0.25)

    def test_wrr2_els_sl_proximity_sums_candidate_row_widths(self) -> None:
        proximity = wrr2_els_sl_proximity(
            (0, 10, 20),
            sl_start=1,
            sl_length=3,
            row_widths=(9, 10),
        )

        self.assertAlmostEqual(proximity, 0.45)

    def test_wrr2_ordinary_els_sl_proximity_uses_first_row_widths(self) -> None:
        proximity = wrr2_ordinary_els_sl_proximity(
            start=0,
            skip=10,
            word_length=3,
            sl_start=1,
            sl_length=3,
            row_width_count=1,
        )

        self.assertEqual(proximity, 0.25)

    def test_wrr_els_els_distance_uses_1994_source_formula(self) -> None:
        distance = wrr_els_els_distance_at_row_width(
            (0, 10, 20),
            (1, 11, 21),
            row_width=10,
        )

        self.assertEqual(distance, 3)

    def test_wrr_els_els_proximity_is_inverse_distance(self) -> None:
        proximity = wrr_els_els_proximity_at_row_width(
            (0, 10, 20),
            (1, 11, 21),
            row_width=10,
        )

        self.assertEqual(proximity, 1 / 3)

    def test_wrr_els_els_alpha_sums_both_row_width_series(self) -> None:
        alpha = wrr_els_els_alpha(
            (0, 10, 20),
            (1, 11, 21),
            left_skip=10,
            right_skip=10,
            row_width_count=1,
        )

        self.assertEqual(alpha, 2 / 3)

    def test_wrr_ordinary_els_els_alpha_builds_offsets(self) -> None:
        alpha = wrr_ordinary_els_els_alpha(
            left_start=0,
            left_skip=10,
            left_word_length=3,
            right_start=1,
            right_skip=10,
            right_word_length=3,
            row_width_count=1,
        )

        self.assertEqual(alpha, 2 / 3)

    def test_wrr_offsets_span_returns_half_open_bounds(self) -> None:
        self.assertEqual(wrr_offsets_span((20, 10, 30), text_length=100), (10, 31))

    def test_wrr_minimality_domain_bounds_shorter_skip_competitors(self) -> None:
        domain = wrr_minimality_domain(
            (20, 30, 40),
            target_skip=10,
            competing_occurrences=(
                ((5, 15), 5),
                ((70, 75), 5),
                ((0, 50), 12),
            ),
            text_length=100,
        )

        self.assertEqual(domain, (6, 75))

    def test_wrr_minimality_domain_is_undefined_for_inner_shorter_els(self) -> None:
        domain = wrr_minimality_domain(
            (20, 30, 40),
            target_skip=10,
            competing_occurrences=(((25, 35), 5),),
            text_length=100,
        )

        self.assertIsNone(domain)

    def test_wrr_minimality_domain_is_undefined_for_enclosing_shorter_els(self) -> None:
        domain = wrr_minimality_domain(
            (20, 30, 40),
            target_skip=10,
            competing_occurrences=(((10, 50), 5),),
            text_length=100,
        )

        self.assertIsNone(domain)

    def test_wrr_minimality_domain_candidates_expose_enclosing_ambiguity(self) -> None:
        domains = wrr_minimality_domain_candidates(
            (20, 30, 40),
            target_skip=10,
            competing_occurrences=(((10, 50), 5),),
            text_length=100,
        )

        self.assertEqual(domains, ((0, 50), (11, 100)))

    def test_wrr_label_minimality_domains_marks_defined_and_undefined_rows(self) -> None:
        assignments = wrr_label_minimality_domains(
            (
                ((20, 30, 40), 10),
                ((25, 35), 5),
                ((70, 80), 12),
            ),
            text_length=100,
        )

        self.assertEqual(
            [row.status for row in assignments],
            ["undefined", "defined", "defined"],
        )
        self.assertEqual(assignments[0].reason, "blocked_by_inner_shorter_skip")
        self.assertEqual(
            assignments[1].to_occurrence(),
            WrrElsOccurrence((25, 35), 5, 0, 100),
        )
        self.assertEqual(assignments[2].domain_start, 26)
        self.assertEqual(assignments[2].domain_end, 100)

    def test_wrr_domain_assignment_rejects_undefined_occurrence_conversion(self) -> None:
        assignment = wrr_label_minimality_domains(
            (((20, 30, 40), 10), ((25, 35), 5)),
            text_length=100,
        )[0]

        with self.assertRaises(ValueError):
            assignment.to_occurrence()

    def test_wrr_domain_weight_uses_overlap_relative_to_text_length(self) -> None:
        left = WrrElsOccurrence((0, 10, 20), 10, 0, 50)
        right = WrrElsOccurrence((11, 21, 31), 10, 10, 40)

        self.assertEqual(wrr_domain_intersection_length(left, right, text_length=100), 30)
        self.assertEqual(wrr_domain_weight(left, right, text_length=100), 0.3)

    def test_wrr_weighted_pair_proximity_multiplies_alpha_by_domain_weight(self) -> None:
        left = WrrElsOccurrence((0, 10, 20), 10, 0, 50)
        right = WrrElsOccurrence((11, 21, 31), 10, 10, 40)

        proximity = wrr_weighted_els_pair_proximity(
            left,
            right,
            text_length=100,
            row_width_count=1,
        )

        self.assertAlmostEqual(proximity, 0.2)

    def test_wrr_word_pair_proximity_sums_all_domain_weighted_pairs(self) -> None:
        left = (
            WrrElsOccurrence((0, 10, 20), 10, 0, 50),
            WrrElsOccurrence((50, 60, 70), 10, 50, 90),
        )
        right = (WrrElsOccurrence((11, 21, 31), 10, 10, 40),)

        proximity = wrr_word_pair_proximity(left, right, text_length=100, row_width_count=1)

        self.assertAlmostEqual(proximity, 0.2)

    def test_wrr_corrected_distance_computes_rank_from_perturbed_q_values(self) -> None:
        perturbations = tuple((index, 0, 0) for index in range(10))
        right_starts = {
            (0, 0, 0): 2,
            (1, 0, 0): 1,
            (2, 0, 0): 40,
            (3, 0, 0): 3,
            (4, 0, 0): 5,
            (5, 0, 0): 15,
            (6, 0, 0): 25,
            (7, 0, 0): 35,
            (8, 0, 0): 45,
            (9, 0, 0): 55,
        }
        left_by_perturbation = {triple: (wrr_occurrence(0),) for triple in perturbations}
        right_by_perturbation = {
            triple: (wrr_occurrence(right_starts[triple]),) for triple in perturbations
        }

        result = wrr_corrected_distance_from_perturbation_sets(
            left_by_perturbation,
            right_by_perturbation,
            text_length=100,
            row_width_count=1,
        )

        self.assertEqual(result.valid_perturbations, 10)
        self.assertAlmostEqual(result.ordinary_proximity, 1 / 3)
        self.assertEqual(result.corrected_distance, 3 / 10)

    def test_wrr_corrected_distance_requires_ordinary_perturbation(self) -> None:
        with self.assertRaises(ValueError):
            wrr_corrected_distance_from_perturbation_sets(
                {(1, 0, 0): (wrr_occurrence(0),)},
                {(1, 0, 0): (wrr_occurrence(1),)},
                text_length=100,
                row_width_count=1,
                minimum_valid=1,
            )

    def test_wrr_corrected_distance_enforces_minimum_valid_perturbations(self) -> None:
        left_by_perturbation = {
            (0, 0, 0): (wrr_occurrence(0),),
            (1, 0, 0): (wrr_occurrence(0),),
        }
        right_by_perturbation = {
            (0, 0, 0): (wrr_occurrence(1),),
            (1, 0, 0): (wrr_occurrence(2),),
        }

        with self.assertRaises(ValueError):
            wrr_corrected_distance_from_perturbation_sets(
                left_by_perturbation,
                right_by_perturbation,
                text_length=100,
                row_width_count=1,
                minimum_valid=3,
            )

    def test_wrr_helper_argument_validation(self) -> None:
        with self.assertRaises(ValueError):
            perturbation_triples(-1)
        with self.assertRaises(ValueError):
            perturbed_offsets(0, 0, 4, (0, 0, 0))
        with self.assertRaises(ValueError):
            perturbed_offsets(0, 1, 3, (0, 0, 0))
        with self.assertRaises(ValueError):
            perturbed_offsets(0, 1, 4, (0, 0))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            is_perturbed_els_match("", "ABCD", 0, 1, (0, 0, 0))
        with self.assertRaises(ValueError):
            is_perturbed_els_match("ABCD", "", 0, 1, (0, 0, 0))
        with self.assertRaises(ValueError):
            list(
                iter_perturbed_els_matches(
                    "ABCD",
                    "ABCD",
                    min_skip=0,
                    max_skip=1,
                )
            )
        with self.assertRaises(ValueError):
            list(
                iter_perturbed_els_matches(
                    "ABCD",
                    "ABCD",
                    min_skip=1,
                    max_skip=1,
                    direction="sideways",
                )
            )
        with self.assertRaises(ValueError):
            nearest_integer_half_up(-1, 1)
        with self.assertRaises(ValueError):
            nearest_integer_half_up(1, 0)
        with self.assertRaises(ValueError):
            wrr_row_widths(0)
        with self.assertRaises(ValueError):
            wrr_row_widths(1, count=0)
        with self.assertRaises(ValueError):
            ordinary_els_offsets(0, 0, 1)
        with self.assertRaises(ValueError):
            ordinary_els_offsets(0, 1, 0)
        with self.assertRaises(ValueError):
            cylindrical_letter_distance_squared(0, 1, 0)
        with self.assertRaises(ValueError):
            cylindrical_letter_distance_squared(-1, 1, 10)
        with self.assertRaises(ValueError):
            wrr2_els_sl_distance_at_row_width((0,), sl_start=0, sl_length=1, row_width=10)
        with self.assertRaises(ValueError):
            wrr2_els_sl_distance_at_row_width((0, 1), sl_start=-1, sl_length=1, row_width=10)
        with self.assertRaises(ValueError):
            wrr2_els_sl_distance_at_row_width((0, 1), sl_start=0, sl_length=0, row_width=10)
        with self.assertRaises(ValueError):
            wrr2_els_sl_proximity((0, 1), sl_start=0, sl_length=1, row_widths=())
        with self.assertRaises(ValueError):
            wrr_els_els_distance_at_row_width((0,), (1, 2), row_width=10)
        with self.assertRaises(ValueError):
            wrr_els_els_distance_at_row_width((0, 1), (2,), row_width=10)
        with self.assertRaises(ValueError):
            wrr_offsets_span((), text_length=1)
        with self.assertRaises(ValueError):
            wrr_minimality_domain((0, 1), target_skip=0, competing_occurrences=(), text_length=2)
        with self.assertRaises(ValueError):
            wrr_minimality_domain(
                (0, 1),
                target_skip=1,
                competing_occurrences=(((0, 1), 0),),
                text_length=2,
            )
        with self.assertRaises(ValueError):
            wrr_domain_weight(
                WrrElsOccurrence((0,), 1, 0, 1),
                WrrElsOccurrence((0, 1), 1, 0, 2),
                text_length=2,
            )
        with self.assertRaises(ValueError):
            wrr_domain_weight(
                WrrElsOccurrence((0, 1), 1, 1, 2),
                WrrElsOccurrence((0, 1), 1, 0, 2),
                text_length=2,
            )

    def test_corrected_distance_rank_is_small_for_large_proximity(self) -> None:
        rank = corrected_distance_rank(9.0, [9.0, 7.0, 5.0, 3.0, 1.0], minimum_valid=1)

        self.assertEqual(rank, 0)

    def test_corrected_distance_rank_is_nearly_one_for_smallest_proximity(self) -> None:
        rank = corrected_distance_rank(1.0, [9.0, 7.0, 5.0, 3.0, 1.0], minimum_valid=1)

        self.assertEqual(rank, 4 / 5)

    def test_corrected_distance_rank_half_weights_tied_ordinary_values(self) -> None:
        rank = corrected_distance_rank(8.0, [10.0, 8.0, 8.0, 8.0, 2.0], minimum_valid=1)

        self.assertEqual(rank, 2 / 5)

    def test_corrected_distance_wrr_rank_uses_1994_greater_or_equal_count(self) -> None:
        rank = corrected_distance_wrr_rank(
            8.0,
            [10.0, 8.0, 8.0, 8.0, 2.0],
            minimum_valid=1,
        )

        self.assertEqual(rank, 4 / 5)

    def test_corrected_distance_wrr_rank_counts_ordinary_value(self) -> None:
        rank = corrected_distance_wrr_rank(9.0, [9.0, 7.0, 5.0, 3.0, 1.0], minimum_valid=1)

        self.assertEqual(rank, 1 / 5)

    def test_corrected_distance_strict_rank_is_legacy_alias(self) -> None:
        rank = corrected_distance_strict_rank(
            8.0,
            [10.0, 8.0, 8.0, 8.0, 2.0],
            minimum_valid=1,
        )

        self.assertEqual(rank, 4 / 5)

    def test_corrected_distance_rank_validates_source_conditions(self) -> None:
        with self.assertRaises(ValueError):
            corrected_distance_rank(1.0, [1.0] * 9)
        with self.assertRaises(ValueError):
            corrected_distance_rank(1.0, [2.0] * 10)
        with self.assertRaises(ValueError):
            corrected_distance_rank(float("nan"), [1.0] * 10)
        with self.assertRaises(ValueError):
            corrected_distance_rank(1.0, [float("inf")] * 10)
        with self.assertRaises(ValueError):
            corrected_distance_rank(1.0, [1.0], minimum_valid=0)
        with self.assertRaises(ValueError):
            corrected_distance_wrr_rank(1.0, [1.0] * 9)

    def test_els_window_count_matches_appendix_formula(self) -> None:
        self.assertEqual(
            els_window_count(text_length=100, word_length=5, max_skip=10),
            9 * (200 - 4 * 12),
        )

    def test_els_window_count_supports_reported_program_formula(self) -> None:
        self.assertEqual(
            els_window_count(text_length=100, word_length=5, max_skip=10, formula="program"),
            9 * (200 - 4 * 10),
        )

    def test_expected_count_uses_letter_frequencies(self) -> None:
        frequencies = {"A": 0.5, "B": 0.25}

        count = expected_els_count(100, "AB", 4, frequencies)

        self.assertEqual(count, 0.125 * els_window_count(100, 2, 4))

    def test_expected_count_accepts_program_formula(self) -> None:
        frequencies = {"A": 0.5, "B": 0.25}

        count = expected_els_count(100, "AB", 4, frequencies, formula="program")

        self.assertEqual(
            count,
            0.125 * els_window_count(100, 2, 4, formula="program"),
        )

    def test_skip_cap_returns_first_cap_reaching_target(self) -> None:
        cap = skip_cap_for_expected_count(
            "AAAAABBBBB",
            "AB",
            target_expected=5,
            max_skip_limit=10,
        )

        self.assertEqual(cap, 3)

    def test_skip_cap_can_use_reported_program_formula(self) -> None:
        printed = skip_cap_for_expected_count(
            "AAAAABBBBB",
            "AB",
            target_expected=8,
            max_skip_limit=10,
        )
        program = skip_cap_for_expected_count(
            "AAAAABBBBB",
            "AB",
            target_expected=8,
            max_skip_limit=10,
            formula="program",
        )

        self.assertEqual(printed, 4)
        self.assertEqual(program, 3)

    def test_skip_cap_limit_is_capped_to_possible_word_span(self) -> None:
        cap = skip_cap_for_expected_count(
            "AAAAABBBBB",
            "AB",
            target_expected=10_000,
            max_skip_limit=999,
        )

        self.assertEqual(cap, 9)

    def test_skip_cap_rejects_unknown_formula(self) -> None:
        with self.assertRaises(ValueError):
            skip_cap_for_expected_count("AAAAABBBBB", "AB", formula="other")

    def test_relative_letter_frequencies_sum_to_one(self) -> None:
        frequencies = relative_letter_frequencies("AAB")

        self.assertAlmostEqual(sum(frequencies.values()), 1.0)
        self.assertAlmostEqual(frequencies["A"], 2 / 3)

    def test_p1_binomial_tail_counts_values_under_threshold(self) -> None:
        values = [0.1, 0.2, 0.4]

        self.assertAlmostEqual(p1_binomial_tail(values), binomial_upper_tail(3, 2, 0.2))

    def test_product_uniform_cdf_matches_singleton_product(self) -> None:
        self.assertAlmostEqual(product_uniform_cdf_from_log(math.log(0.25), 1), 0.25)

    def test_p2_product_statistic_matches_product_formula(self) -> None:
        values = [0.5, 0.5]
        expected = product_uniform_cdf_from_log(math.log(0.25), 2)

        self.assertAlmostEqual(p2_product_statistic(values), expected)

    def test_p2_product_statistic_returns_zero_for_zero_c_value(self) -> None:
        self.assertEqual(p2_product_statistic([0.0, 0.5]), 0.0)

    def test_permutation_rank_rho_half_weights_ties(self) -> None:
        rho = permutation_rank_rho(5, [1, 5, 5, 9])

        self.assertEqual(rho, (1 + 1 + 0.5 * 2) / 5)

    def test_bonferroni_rho0_does_not_cap_above_one(self) -> None:
        self.assertEqual(bonferroni_rho0([0.3, 0.4]), 1.2)


def wrr_occurrence(start: int) -> WrrElsOccurrence:
    return WrrElsOccurrence((start, start + 10, start + 20), 10, 0, 100)


if __name__ == "__main__":
    unittest.main()
