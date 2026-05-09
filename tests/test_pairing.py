import unittest

from els.pairing import (
    center_chapter,
    cylindrical_hit_distance,
    cylindrical_point_distance,
    pair_metrics,
    span_gap,
)
from els.search import ELSHit


def hit(
    start: int,
    end: int,
    *,
    skip: int = 2,
    center_ref: str = "Gen 1:1",
) -> ELSHit:
    return ELSHit(
        term="x",
        normalized_term="x",
        skip=skip,
        start_offset=start,
        end_offset=end,
        span_letters=abs(end - start) + 1,
        sequence="x",
        start_ref=center_ref,
        end_ref=center_ref,
        start_source="test",
        end_source="test",
        center_offset=(min(start, end) + max(start, end)) // 2,
        center_ref=center_ref,
        center_source="test",
        center_word_index="",
        center_word="",
        center_normalized_word="",
    )


class PairingTests(unittest.TestCase):
    def test_span_gap_zero_for_overlap(self) -> None:
        self.assertEqual(span_gap(hit(10, 20), hit(15, 25)), 0)
        self.assertEqual(span_gap(hit(10, 20), hit(25, 30)), 5)

    def test_pair_metrics_report_compactness_flags(self) -> None:
        metrics = pair_metrics(
            hit(10, 20, skip=7, center_ref="Gen 1:2"),
            hit(25, 35, skip=-7, center_ref="Gen 1:9"),
        )

        self.assertEqual(metrics.span_gap, 5)
        self.assertEqual(metrics.center_distance, 15)
        self.assertEqual(metrics.compactness_score, 20)
        self.assertFalse(metrics.overlap)
        self.assertTrue(metrics.same_center_chapter)
        self.assertFalse(metrics.same_signed_skip)
        self.assertTrue(metrics.same_abs_skip)

    def test_center_chapter_handles_multitoken_books(self) -> None:
        self.assertEqual(center_chapter("Song 2:4"), "Song 2")
        self.assertEqual(center_chapter("2 Thess 3:1"), "2 Thess 3")

    def test_cylindrical_distance_wraps_columns(self) -> None:
        self.assertEqual(cylindrical_point_distance(1, 9, 10), 2.0)
        self.assertEqual(cylindrical_hit_distance(hit(1, 1), hit(9, 9), 10), 2.0)


if __name__ == "__main__":
    unittest.main()
