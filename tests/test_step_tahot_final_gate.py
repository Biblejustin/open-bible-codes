import unittest

from scripts import analyze_step_tahot_final_gate as final_gate


class StepTahotFinalGateTests(unittest.TestCase):
    def test_pattern_counts_distinguish_step_only(self) -> None:
        rows = [
            {"present_corpora": "MT_WLC,STEP_TAHOT"},
            {"present_corpora": "STEP_TAHOT"},
            {"present_corpora": "MAM"},
        ]
        self.assertEqual(
            final_gate.pattern_counts(rows, "STEP_TAHOT"),
            {
                "pattern_rows": 3,
                "with_source": 2,
                "source_only": 1,
                "source_only_rate": 1 / 3,
            },
        )

    def test_policy_counts_classify_source_paths(self) -> None:
        rows = [
            {"policy_flags": "L_ONLY_PATH"},
            {"policy_flags": "Q"},
            {"policy_flags": "R X"},
        ]
        self.assertEqual(final_gate.policy_counts(rows)["policy_touch"], 2)
        self.assertEqual(final_gate.policy_counts(rows)["l_only"], 1)
        self.assertEqual(final_gate.policy_counts(rows)["q_rows"], 1)
        self.assertEqual(final_gate.policy_counts(rows)["r_rows"], 1)
        self.assertEqual(final_gate.policy_counts(rows)["x_rows"], 1)

    def test_gate_holds_all_step_only_rows(self) -> None:
        self.assertEqual(
            final_gate.gate_for_flags("L_ONLY_PATH"),
            "hold_l_only_step_tahot_specific",
        )
        self.assertEqual(
            final_gate.gate_for_flags("Q"),
            "hold_selected_reading_policy_path",
        )

    def test_validate_policy_rows_catches_stale_inputs(self) -> None:
        final_gate.validate_policy_rows("real", 1, [{"policy_flags": "L_ONLY_PATH"}])
        with self.assertRaises(ValueError):
            final_gate.validate_policy_rows("real", 2, [{"policy_flags": "L_ONLY_PATH"}])


if __name__ == "__main__":
    unittest.main()
