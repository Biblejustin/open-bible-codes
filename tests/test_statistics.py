import unittest

from els.statistics import (
    benjamini_hochberg_q_values,
    direction_count,
    estimated_search_space,
    hits_per_million,
    numeric_value,
    round_float,
    tail_p_value_ge,
    tail_p_value_le,
)


class StatisticsTests(unittest.TestCase):
    def test_tail_p_values_use_add_one_smoothing(self) -> None:
        samples = (1, 5, 7)

        self.assertEqual(tail_p_value_ge(5, samples), 0.75)
        self.assertEqual(tail_p_value_le(5, samples), 0.75)

    def test_tail_p_values_return_none_without_samples_or_observation(self) -> None:
        self.assertIsNone(tail_p_value_ge(5, ()))
        self.assertIsNone(tail_p_value_le(None, (1, 2, 3)))

    def test_benjamini_hochberg_q_values_preserve_none_slots(self) -> None:
        self.assertEqual(
            benjamini_hochberg_q_values([0.01, 0.04, 0.03, None]),
            [0.03, 0.04, 0.04, None],
        )

    def test_search_space_counts_valid_start_positions(self) -> None:
        self.assertEqual(
            estimated_search_space(
                text_length=10,
                query_length=3,
                min_skip=2,
                max_skip=3,
                direction="both",
            ),
            20,
        )

    def test_direction_count(self) -> None:
        self.assertEqual(direction_count("both"), 2)
        self.assertEqual(direction_count("forward"), 1)

    def test_numeric_and_round_helpers(self) -> None:
        self.assertIsNone(numeric_value(""))
        self.assertEqual(numeric_value("0.25"), 0.25)
        self.assertEqual(round_float(0.1234567), 0.123457)
        self.assertEqual(round_float(None), "")

    def test_hits_per_million_handles_empty_space(self) -> None:
        self.assertEqual(hits_per_million(2, 1_000_000), 2.0)
        self.assertEqual(hits_per_million(2, 0), "")


if __name__ == "__main__":
    unittest.main()
