import unittest
from types import SimpleNamespace

from scripts.analyze_related_name_pairs import hit_center, nearest_hits


class RelatedNamePairsTests(unittest.TestCase):
    def test_nearest_hits_matches_linear_tie_behavior(self) -> None:
        hits = [
            _hit(10),
            _hit(20),
            _hit(20, tag=2),
            _hit(40),
            _hit(60),
        ]
        centers = [hit_center(hit) for hit in hits]
        target = _hit(30)

        actual = nearest_hits(target, hits, centers, radius=1)

        self.assertEqual(actual, hits[0:3])


def _hit(center: int, *, tag: int = 0) -> SimpleNamespace:
    return SimpleNamespace(start_offset=center, end_offset=center, tag=tag)


if __name__ == "__main__":
    unittest.main()
