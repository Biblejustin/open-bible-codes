import unittest

from scripts.analyze_synthetic_extension_match_review import context_read


class SyntheticExtensionMatchReviewTests(unittest.TestCase):
    def test_context_read_prioritizes_surface_phrase(self) -> None:
        self.assertEqual(
            context_read(False, False, True),
            "synthetic phrase appears as surface text in extension span",
        )
        self.assertEqual(
            context_read(False, False, False),
            "synthetic ELS-only at hit span; matched phrase appears elsewhere",
        )


if __name__ == "__main__":
    unittest.main()
