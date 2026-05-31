import unittest

from scripts.analyze_extension_final_gate import final_gate


class ExtensionFinalGateTests(unittest.TestCase):
    def test_final_gate_requires_exact_center(self) -> None:
        self.assertEqual(
            final_gate(
                context_gate="hold_same_category_only",
                cross_text_status="cross_text_match",
                combined_q="0.001",
                phrase_surface="no",
            ),
            "hold_no_exact_center",
        )

    def test_final_gate_requires_cross_text(self) -> None:
        self.assertEqual(
            final_gate(
                context_gate="promote_exact_center",
                cross_text_status="source_only",
                combined_q="0.001",
                phrase_surface="no",
            ),
            "hold_source_only",
        )

    def test_final_gate_allows_hidden_phrase_review(self) -> None:
        self.assertEqual(
            final_gate(
                context_gate="promote_exact_center",
                cross_text_status="cross_text_match",
                combined_q="0.004",
                phrase_surface="no",
            ),
            "review_cross_text_exact_center_hidden_phrase",
        )


if __name__ == "__main__":
    unittest.main()
