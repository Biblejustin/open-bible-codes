import unittest

from scripts.analyze_apocrypha_bridge_controls import position_classes, repeated_prefix


class ApocryphaBridgeControlsTests(unittest.TestCase):
    def test_position_classes_split_on_boundary(self) -> None:
        self.assertEqual(
            position_classes([0, 9, 10, 11], 10),
            ["canonical", "canonical", "apocrypha", "apocrypha"],
        )

    def test_repeated_prefix_fills_requested_length(self) -> None:
        self.assertEqual(repeated_prefix("abc", 8), "abcabcab")
        self.assertEqual(repeated_prefix("abc", 0), "")
