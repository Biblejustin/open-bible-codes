import unittest

from scripts import analyze_greek_exact_center_final_gate as final_gate


class GreekExactCenterFinalGateTests(unittest.TestCase):
    def test_final_gate_labels_source_specific_rows(self) -> None:
        self.assertEqual(
            final_gate.final_gate(
                current_scope="source_only",
                best_q="0.000999",
                extension_span_surface_phrase=True,
                synthetic_any_ge_target=0,
            ),
            "source_specific_hidden_path_candidate",
        )

    def test_final_gate_treats_hidden_path_as_candidate_type(self) -> None:
        self.assertEqual(
            final_gate.final_gate(
                current_scope="all_sources",
                best_q="0.000999",
                extension_span_surface_phrase=False,
                synthetic_any_ge_target=3,
            ),
            "cross_version_controlled_surface_anchored_hidden_candidate",
        )

    def test_final_gate_labels_surface_echo_candidate(self) -> None:
        self.assertEqual(
            final_gate.final_gate(
                current_scope="all_sources",
                best_q="0.000999",
                extension_span_surface_phrase=True,
                synthetic_any_ge_target=0,
            ),
            "cross_version_controlled_surface_echo_candidate",
        )

    def test_synthetic_rows_are_keyed_by_exact_extension(self) -> None:
        rows = [
            {
                "normalized_term": "δοξα",
                "skip": "21",
                "direction": "forward",
                "extension_type": "term_plus_after",
                "extended_sequence": "δοξανωσ",
                "synthetic_same_type_ge_target": "1",
                "synthetic_any_ge_target": "2",
            }
        ]
        grouped = final_gate.group_synthetic_rows(rows)
        key = "δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ"
        self.assertIn(key, grouped)


if __name__ == "__main__":
    unittest.main()
