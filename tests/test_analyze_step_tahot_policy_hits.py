import unittest
from collections import Counter

from scripts import analyze_step_tahot_policy_hits as policy_hits


class StepTahotPolicyHitTests(unittest.TestCase):
    def test_source_only_filter_accepts_exact_step_label(self) -> None:
        self.assertTrue(
            policy_hits.is_source_only({"present_corpora": "STEP_TAHOT"}, "STEP_TAHOT")
        )
        self.assertFalse(
            policy_hits.is_source_only(
                {"present_corpora": "MT_WLC,STEP_TAHOT"},
                "STEP_TAHOT",
            )
        )

    def test_policy_flags_distinguish_selected_readings(self) -> None:
        self.assertEqual(policy_hits.policy_flags(Counter({"L": 4})), ["L_ONLY_PATH"])
        self.assertEqual(policy_hits.policy_flags(Counter({"Q": 1, "L": 3})), ["Q"])
        self.assertEqual(
            policy_hits.policy_flags(Counter({"R": 1, "X": 1, "L": 2})),
            ["R", "X"],
        )
        self.assertEqual(
            policy_hits.policy_flags(Counter({"B": 1, "L": 2})),
            ["OTHER_NON_L"],
        )

    def test_offsets_are_read_from_labeled_list(self) -> None:
        self.assertEqual(
            policy_hits.parse_source_offsets("MT_WLC:1-2; STEP_TAHOT:10-40", "STEP_TAHOT"),
            (10, 40),
        )

    def test_source_type_prefix_strips_variants(self) -> None:
        self.assertEqual(policy_hits.source_type_prefix("Q(K+B)"), "Q")
        self.assertEqual(policy_hits.source_type_prefix("LA(HC+b)"), "LA")


if __name__ == "__main__":
    unittest.main()
