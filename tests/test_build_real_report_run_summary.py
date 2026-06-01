import json

from scripts import build_real_report_run_summary as summary


def test_report_summary_cells_escape_markdown_and_ranges() -> None:
    assert summary.md_cell("a|b\nc") == "a\\|b c"
    assert summary.range_text(None, 10) == "none"
    assert summary.range_text(7, 7) == "7"
    assert summary.range_text(7, 12) == "7..12"


def test_current_report_manifest_exposes_cities_no_input_boundary() -> None:
    manifest = json.loads(summary.MANIFEST_OUT.read_text(encoding="utf-8"))

    assert manifest["cities_no_input_handoff_status_rows"] == 8
    assert manifest["cities_no_input_handoff_manual_input_needed_rows"] == 6
    assert manifest["cities_no_input_handoff_ocr_packet_pages"] == 61
    assert manifest["cities_no_input_handoff_reviewed_ocr_packet_pages"] == 41
    assert manifest["cities_no_input_handoff_unreviewed_ocr_packet_pages"] == 20
    assert manifest["cities_no_input_handoff_source_row_imports"] == 0
    assert manifest["cities_no_input_handoff_result_allowed"] == "0"
    assert (
        manifest["cities_no_input_handoff_claim_status"]
        == "cities_no_input_handoff_blocks_source_import_and_results"
    )


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
                "candidate_source_audit_rows": "4",
                "candidate_source_verse_import_ready_pages": "0",
                "candidate_source_result_ready_pages": "0",
                "crosswire_possible_independent_kjva_candidates": "1",
                "gutenberg_split_kjv_apocrypha_metadata_candidates": "1",
                "wikisource_source_candidate_pages": "1",
                "open_bibles_kjv_paths": "1",
                "open_bibles_apocrypha_paths": "0",
                "open_bibles_deuterocanon_paths": "0",
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
    assert "| Candidate source audits | 4 |" in text
    assert "| Candidate result-ready pages | 0 |" in text
    assert "| Result allowed | 0 |" in text
    assert "`kjva_no_input_handoff_blocks_new_result`" in text
    assert "- Current read: this is a work map, not a statistical result." in text


def test_wrr_no_input_handoff_status_section_keeps_result_closed() -> None:
    lines = summary.wrr_no_input_handoff_status_section(
        [
            {
                "status_rows": "9",
                "handoff_ready_rows": "9",
                "manual_input_needed_rows": "8",
                "claim_readiness_rows": "4",
                "claim_readiness_ready_rows": "4",
                "claim_blocker_rows": "0",
                "source_cited_defined_distances": "163",
                "current_defined_distances": "72",
                "remaining_gap": "91",
                "review_lanes": "4",
                "residual_action_terms": "58",
                "residual_pairs": "59",
                "frontier_pairs": "40",
                "manual_decision_rows": "37",
                "source_transcription_row_clusters": "22",
                "source_transcription_action_terms": "43",
                "page_image_terms": "3",
                "method_pair_universe_terms": "11",
                "wide_skip_max": "5000",
                "wide_skip_total_hits": "0",
                "new_result_allowed": "False",
                "exact_reproduction_ready": "False",
                "claim_boundary": "local_locked_method_ready_exact_published_open",
            }
        ],
        {
            "claim_boundary": "WRR no-input handoff only; no new result",
            "text_retention": "no Bible text written to tracked outputs",
        },
    )
    text = "\n".join(lines)
    assert "## WRR No-Input Handoff Status" in text
    assert "| New WRR result allowed | 0 |" in text
    assert "| Exact reproduction ready | 0 |" in text
    assert "`local_locked_method_ready_exact_published_open`" in text
