from scripts import build_real_report_run_summary as summary


def test_report_summary_cells_escape_markdown_and_ranges() -> None:
    assert summary.md_cell("a|b\nc") == "a\\|b c"
    assert summary.range_text(None, 10) == "none"
    assert summary.range_text(7, 7) == "7"
    assert summary.range_text(7, 12) == "7..12"


def test_kjva_no_input_handoff_status_section_keeps_result_closed() -> None:
    lines = summary.kjva_no_input_handoff_status_section(
        [
            {
                "status_rows": "9",
                "handoff_ready_rows": "9",
                "manual_input_needed_rows": "8",
                "gate_rows": "11",
                "blocked_gate_rows": "10",
                "source_policy_blocker_rows": "7",
                "source_use_ready_pages": "0",
                "source_lock_ready": "False",
                "result_allowed": "False",
                "completed_lane_terms": "7",
                "completed_lane_observed_bridge_rows": "1",
                "nonbible_controls_at_or_above_observed": "1",
                "gutenberg_manasseh_source_markers": "0",
                "gutenberg_manasseh_local_markers": "15",
                "hakkaac_exact_normalized_verse_matches": "5719",
                "hakkaac_total_verses": "5720",
                "split_source_blocker_rows": "6",
                "claim_status": "kjva_no_input_handoff_blocks_new_result",
                "gutenberg_sirach_gap_refs": "SIR 44:23",
            }
        ],
        {
            "claim_boundary": "KJVA no-input handoff only; no new result",
            "text_retention": "no Bible text written to tracked outputs",
        },
    )
    text = "\n".join(lines)
    assert "## KJVA No-Input Handoff Status" in text
    assert "| Result allowed | 0 |" in text
    assert "`kjva_no_input_handoff_blocks_new_result`" in text
    assert "- Current read: this is a work map, not a statistical result." in text
