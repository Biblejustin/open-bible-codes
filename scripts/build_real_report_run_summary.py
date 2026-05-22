#!/usr/bin/env python3
"""Build a compact summary for the formal report assembly run."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.term_display import display_term
from scripts.download_wrr_sources import REQUIRED_MANIFEST_LABELS as WRR_REQUIRED_SOURCE_LABELS


STEP_TAHOT_MANIFEST = Path("reports/step_tahot_final_gate/manifest.json")
GREEK_GATE_SUMMARY = Path("reports/greek_exact_center_final_gate/summary.csv")
GREEK_PATTERN_SUMMARY = Path("reports/greek_pattern_versions/summary.csv")
DOXA_SUMMARY = Path("reports/doxa_four_source_claim_followup/paired_controls_summary.csv")
DOXA_PROTOCOL_MANIFEST = Path("reports/doxa_four_source_claim_followup/protocol_run.manifest.json")
DOXA_CONFIRMATORY_SUMMARY = Path(
    "reports/doxa_four_source_confirmatory_followup/paired_controls_summary.csv"
)
DOXA_CONFIRMATORY_PROTOCOL_MANIFEST = Path(
    "reports/doxa_four_source_confirmatory_followup/protocol_run.manifest.json"
)
SURFACE_QUEUE_SUMMARY = Path("reports/greek_expanded_surface_queue/term_summary.csv")
SURFACE_QUEUE_PATTERNS = Path("reports/greek_expanded_surface_queue/surface_patterns.csv")
SURFACE_QUEUE_PROTOCOL_MANIFEST = Path("reports/greek_expanded_surface_queue/protocol_run.manifest.json")
SURFACE_TRIAGE_SELECTED = Path("reports/greek_expanded_surface_triage/selected_patterns.csv")
SURFACE_TRIAGE_COHORT = Path("reports/greek_expanded_surface_triage/term_cohort.csv")
SURFACE_TRIAGE_PROTOCOL_MANIFEST = Path("reports/greek_expanded_surface_triage/protocol_run.manifest.json")
SURFACE_LETTER_PATHS_SUMMARY = Path("reports/greek_expanded_surface_letter_paths/path_summary.csv")
SURFACE_LETTER_PATHS_PROTOCOL_MANIFEST = Path("reports/greek_expanded_surface_letter_paths/protocol_run.manifest.json")
SURFACE_CONTROL_FREQUENCIES = Path("reports/greek_expanded_surface_control_pool/term_surface_frequencies.csv")
SURFACE_CONTROL_MATCHED = Path("reports/greek_expanded_surface_control_pool/matched_controls.csv")
SURFACE_CONTROL_PROTOCOL_MANIFEST = Path("reports/greek_expanded_surface_control_pool/protocol_run.manifest.json")
SURFACE_CONTROL_EVALUATION = Path("reports/greek_expanded_surface_control_evaluation/summary.csv")
SURFACE_CONTROL_EVALUATION_MANIFEST = Path("reports/greek_expanded_surface_control_evaluation/protocol_run.manifest.json")
SURFACE_AVAILABLE_CONTROL_EVALUATION = Path("reports/greek_expanded_surface_available_control_evaluation/summary.csv")
SURFACE_AVAILABLE_CONTROL_EVALUATION_MANIFEST = Path("reports/greek_expanded_surface_available_control_evaluation/protocol_run.manifest.json")
SURFACE_FOLLOWUP_REPORT_MANIFEST = Path("reports/greek_expanded_surface_followup/report.manifest.json")
SURFACE_FOLLOWUP_PROTOCOL_MANIFEST = Path("reports/greek_expanded_surface_followup/protocol_run.manifest.json")
LENGTH4_SELECTED = Path("reports/greek_surface_length4_followup/selected_patterns.csv")
LENGTH4_COHORT = Path("reports/greek_surface_length4_followup/term_cohort.csv")
LENGTH4_CONTROL_EVALUATION = Path("reports/greek_surface_length4_followup/control_summary.csv")
LENGTH4_LETTER_PATHS = Path("reports/greek_surface_length4_followup/path_summary.csv")
LENGTH4_PROTOCOL_MANIFEST = Path("reports/greek_surface_length4_followup/protocol_run.manifest.json")
LENGTH4_VOCAB_TERMS_MANIFEST = Path("reports/greek_surface_length4_vocab_controls/terms.manifest.json")
LENGTH4_VOCAB_CONTROL_EVALUATION = Path("reports/greek_surface_length4_vocab_controls/control_summary.csv")
LENGTH4_VOCAB_PROTOCOL_MANIFEST = Path("reports/greek_surface_length4_vocab_controls/protocol_run.manifest.json")
WRR_PROTOCOL_MANIFEST = Path("reports/wrr_1994/audit_counts_protocol.manifest.json")
WRR_SOURCE_MANIFEST = Path("reports/wrr_1994/sources.manifest.json")
WRR_TEXT_SOURCE_SUMMARY = Path("reports/wrr_1994/koren_genesis_text_source.csv")
WRR_SOURCE_SHAPES_SUMMARY = Path("reports/wrr_1994/wrr_source_shapes_summary.csv")
WRR_COUNT_SUMMARY = Path("reports/wrr_1994/wrr2_genesis_count_summary.csv")
WRR_PAIR_AUDIT_LEN_5_8 = Path("reports/wrr_1994/wrr2_genesis_pair_audit_len_5_8_concepts.csv")
WRR_PAIR_CONTROLS_LEN_5_8 = Path("reports/wrr_1994/wrr2_genesis_pair_controls_len_5_8.csv")
WRR_SKIP_CAPS_SUMMARY = Path("reports/wrr_1994/wrr2_skip_caps_summary.csv")
WRR_PAIR_TABLE_RECONCILIATION = Path("reports/wrr_1994/wrr2_pair_table_reconciliation_summary.csv")
WRR_PERTURBATION_SUMMARY = Path("reports/wrr_1994/wrr2_perturbation_diagnostics_summary.csv")
WRR_CROSS_PAIR_RECOMMENDED_PERMUTATION_SUMMARY = Path(
    "reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_permutations_no_wnp_999999_summary.csv"
)
HEBREW_THEOLOGY_ALL_CODES_TRIAGE_MANIFEST = Path(
    "reports/hebrew_theology_all_codes/triage.manifest.json"
)
HEBREW_SCREENING_ALL_CODES_TRIAGE_MANIFEST = Path(
    "reports/hebrew_screening_all_codes/triage.manifest.json"
)
GREEK_SCREENING_ALL_CODES_TRIAGE_MANIFEST = Path(
    "reports/greek_screening_all_codes/triage.manifest.json"
)
ALL_CODES_FOLLOWUP_SELECTION_MANIFEST = Path("reports/all_codes_followup_selection/manifest.json")
ALL_CODES_FOLLOWUP_LETTER_PATHS_SUMMARY = Path(
    "reports/all_codes_followup_letter_paths/path_summary.csv"
)
ALL_CODES_FOLLOWUP_LETTER_PATHS_MANIFEST = Path(
    "reports/all_codes_followup_letter_paths/manifest.json"
)
ALL_CODES_FOLLOWUP_CONTEXT_EXCERPTS = Path(
    "reports/all_codes_followup_context/context_excerpts.csv"
)
ALL_CODES_FOLLOWUP_CONTEXT_MANIFEST = Path("reports/all_codes_followup_context/manifest.json")
ALL_CODES_FOLLOWUP_EXTENSIONS_SUMMARY = Path("reports/all_codes_followup_extensions/summary.csv")
ALL_CODES_FOLLOWUP_EXTENSIONS_MANIFEST = Path("reports/all_codes_followup_extensions/manifest.json")
ALL_CODES_COMPOUND_EXTENSION_CONTROLS_SUMMARY = Path(
    "reports/all_codes_compound_extension_controls/summary.csv"
)
ALL_CODES_COMPOUND_EXTENSION_CONTROLS_MANIFEST = Path(
    "reports/all_codes_compound_extension_controls/manifest.json"
)
ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_SUMMARY = Path(
    "reports/all_codes_compound_extension_confirmatory/summary.csv"
)
ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_MANIFEST = Path(
    "reports/all_codes_compound_extension_confirmatory/manifest.json"
)
ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_PROTOCOL_MANIFEST = Path(
    "reports/all_codes_compound_extension_confirmatory/protocol_run.manifest.json"
)
ALL_CODES_FOLLOWUP_REVIEW_SUMMARY = Path("reports/all_codes_followup_review/review_summary.csv")
ALL_CODES_FOLLOWUP_REVIEW_MANIFEST = Path("reports/all_codes_followup_review/manifest.json")
CENTERED_OCCURRENCE_PRESENCE = Path("reports/centered_occurrence_index/presence_summary.csv")
CENTERED_OCCURRENCE_MANIFEST = Path("reports/centered_occurrence_index/manifest.json")
KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_TERM_SUMMARY = Path(
    "reports/kjv_apocrypha_bridge_confirmatory_controls_5000/term_summary.csv"
)
KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_MANIFEST = Path(
    "reports/kjv_apocrypha_bridge_confirmatory_controls_5000/manifest.json"
)
KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_TERM_SUMMARY = Path(
    "reports/kjv_apocrypha_bridge_prospective/term_summary.csv"
)
KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_MANIFEST = Path(
    "reports/kjv_apocrypha_bridge_prospective/manifest.json"
)
KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_SUMMARY = Path(
    "reports/kjv_apocrypha_bridge_prospective_nonbible_controls/control_summary.csv"
)
KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_MANIFEST = Path(
    "reports/kjv_apocrypha_bridge_prospective_nonbible_controls/manifest.json"
)
EXTERNAL_CLAIM_COUNTS_SUMMARY = Path("reports/external_claim_source_counts/summary.csv")
EXTERNAL_CLAIM_COUNTS_MANIFEST = Path(
    "reports/external_claim_source_counts/summary.manifest.json"
)
EXTERNAL_CLAIM_ALL_CODES_SUMMARY = Path(
    "reports/external_claim_source_all_codes/surface_all_codes_summary.csv"
)
EXTERNAL_CLAIM_ALL_CODES_SUMMARY_MANIFEST = Path(
    "reports/external_claim_source_all_codes/summary.manifest.json"
)
EXTERNAL_CLAIM_ALL_CODES_TRIAGE = Path(
    "reports/external_claim_source_all_codes/triage_queue.csv"
)
EXTERNAL_CLAIM_ALL_CODES_TRIAGE_MANIFEST = Path(
    "reports/external_claim_source_all_codes/triage.manifest.json"
)
MATRIX_CLUSTER_RELATION_CONTROL_SUMMARY = Path(
    "reports/matrix_clusters/relation_control_summary.csv"
)
MATRIX_CLUSTER_TERM_PAIR_CONTROL_SUMMARY = Path(
    "reports/matrix_clusters/term_pair_control_summary.csv"
)
NOTABLE_PASSAGE_GAP_PASSAGE_SUMMARY = Path("reports/notable_passage_gaps/passage_summary.csv")
NOTABLE_PASSAGE_GAP_CROSS_SOURCE_SUMMARY = Path(
    "reports/notable_passage_gaps/cross_source_gap_summary.csv"
)
THEMATIC_CHAPTER_ABSENCE_PASSAGE_SUMMARY = Path(
    "reports/thematic_chapter_absence/passage_summary.csv"
)
THEMATIC_CHAPTER_ABSENCE_CROSS_SOURCE_SUMMARY = Path(
    "reports/thematic_chapter_absence/cross_source_gap_summary.csv"
)
MATCH_STRATA_SUMMARY = Path("reports/match_strata_index/strata_summary.csv")
BOUNDARY_ALIGNMENT_SUMMARY = Path("reports/boundary_alignment/summary.csv")
CHAPTER_POSITION_BIAS_SUMMARY = Path("reports/chapter_position_bias/summary.csv")
DIRECTION_ASYMMETRY_SUMMARY = Path("reports/direction_asymmetry/summary.csv")
CANONICAL_FIRST_SUMMARY = Path("reports/canonical_first_summary/summary.csv")
CROSS_SKIP_SUMMARY = Path("reports/cross_skip_summary/summary.csv")
REVIEW_FLAG_SUMMARY = Path("reports/review_flag_summary/summary.csv")
COHORT_CLUSTER_DENSITY_SUMMARY = Path("reports/cohort_cluster_density/summary.csv")
REPORT_INDEX = Path("reports/INDEX.md")
OUT_DIR = Path("reports/real_report_run")
SUMMARY_OUT = OUT_DIR / "summary.md"
MANIFEST_OUT = OUT_DIR / "manifest.json"


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    step_manifest = read_json(args.step_tahot_manifest)
    greek_gate_rows = read_rows(args.greek_gate_summary)
    greek_pattern_rows = read_rows(args.greek_pattern_summary)
    doxa_rows = read_rows(args.doxa_summary)
    doxa_manifest = read_json(args.doxa_protocol_manifest)
    doxa_confirmatory_rows = read_rows(args.doxa_confirmatory_summary)
    doxa_confirmatory_manifest = read_json(args.doxa_confirmatory_protocol_manifest)
    surface_queue_summary_rows = read_rows(args.surface_queue_summary)
    surface_queue_pattern_rows = read_rows(args.surface_queue_patterns)
    surface_queue_manifest = read_json(args.surface_queue_protocol_manifest)
    surface_triage_selected_rows = read_rows(args.surface_triage_selected)
    surface_triage_cohort_rows = read_rows(args.surface_triage_cohort)
    surface_triage_manifest = read_json(args.surface_triage_protocol_manifest)
    surface_letter_path_rows = read_rows(args.surface_letter_paths_summary)
    surface_letter_paths_manifest = read_json(args.surface_letter_paths_protocol_manifest)
    surface_control_frequency_rows = read_rows(args.surface_control_frequencies)
    surface_control_matched_rows = read_rows(args.surface_control_matched)
    surface_control_manifest = read_json(args.surface_control_protocol_manifest)
    surface_control_evaluation_rows = read_rows(args.surface_control_evaluation)
    surface_control_evaluation_manifest = read_json(args.surface_control_evaluation_manifest)
    surface_available_control_evaluation_rows = read_rows(args.surface_available_control_evaluation)
    surface_available_control_evaluation_manifest = read_json(
        args.surface_available_control_evaluation_manifest
    )
    surface_followup_report_manifest = read_json(args.surface_followup_report_manifest)
    surface_followup_protocol_manifest = read_json(args.surface_followup_protocol_manifest)
    length4_selected_rows = read_rows(args.length4_selected)
    length4_cohort_rows = read_rows(args.length4_cohort)
    length4_control_evaluation_rows = read_rows(args.length4_control_evaluation)
    length4_letter_path_rows = read_rows(args.length4_letter_paths)
    length4_protocol_manifest = read_json(args.length4_protocol_manifest)
    length4_vocab_terms_manifest = read_json(args.length4_vocab_terms_manifest)
    length4_vocab_control_evaluation_rows = read_rows(args.length4_vocab_control_evaluation)
    length4_vocab_protocol_manifest = read_json(args.length4_vocab_protocol_manifest)
    wrr_protocol_manifest = read_json(args.wrr_protocol_manifest)
    wrr_source_manifest = read_json(args.wrr_source_manifest)
    wrr_text_source_rows = read_rows(args.wrr_text_source)
    wrr_source_shapes_summary_rows = read_rows(args.wrr_source_shapes_summary)
    wrr_count_summary_rows = read_rows(args.wrr_count_summary)
    wrr_pair_audit_len_5_8_rows = read_rows(args.wrr_pair_audit_len_5_8)
    wrr_pair_controls_len_5_8_rows = read_rows(args.wrr_pair_controls_len_5_8)
    wrr_skip_caps_summary_rows = read_rows(args.wrr_skip_caps_summary)
    wrr_pair_table_reconciliation_rows = read_rows(args.wrr_pair_table_reconciliation)
    wrr_perturbation_summary_rows = read_rows(args.wrr_perturbation_summary)
    wrr_cross_pair_recommended_permutation_rows = read_rows(
        args.wrr_cross_pair_recommended_permutation_summary
    )
    hebrew_theology_all_codes_triage_manifest = read_json(
        args.hebrew_theology_all_codes_triage_manifest
    )
    hebrew_screening_all_codes_triage_manifest = read_json(
        args.hebrew_screening_all_codes_triage_manifest
    )
    greek_screening_all_codes_triage_manifest = read_json(
        args.greek_screening_all_codes_triage_manifest
    )
    all_codes_followup_selection_manifest = read_json(args.all_codes_followup_selection_manifest)
    all_codes_followup_letter_path_rows = read_rows(args.all_codes_followup_letter_paths_summary)
    all_codes_followup_letter_paths_manifest = read_json(
        args.all_codes_followup_letter_paths_manifest
    )
    all_codes_followup_context_rows = read_rows(args.all_codes_followup_context_excerpts)
    all_codes_followup_context_manifest = read_json(args.all_codes_followup_context_manifest)
    all_codes_followup_extension_rows = read_rows(args.all_codes_followup_extensions_summary)
    all_codes_followup_extensions_manifest = read_json(args.all_codes_followup_extensions_manifest)
    all_codes_compound_extension_control_rows = read_rows(
        args.all_codes_compound_extension_controls_summary
    )
    all_codes_compound_extension_controls_manifest = read_json(
        args.all_codes_compound_extension_controls_manifest
    )
    all_codes_compound_extension_confirmatory_rows = read_rows(
        args.all_codes_compound_extension_confirmatory_summary
    )
    all_codes_compound_extension_confirmatory_manifest = read_json(
        args.all_codes_compound_extension_confirmatory_manifest
    )
    all_codes_compound_extension_confirmatory_protocol_manifest = read_json(
        args.all_codes_compound_extension_confirmatory_protocol_manifest
    )
    all_codes_followup_review_rows = read_rows(args.all_codes_followup_review_summary)
    all_codes_followup_review_manifest = read_json(args.all_codes_followup_review_manifest)
    centered_occurrence_presence_rows = read_rows(args.centered_occurrence_presence)
    centered_occurrence_manifest = read_json(args.centered_occurrence_manifest)
    kjva_apocrypha_bridge_confirmatory_rows = read_rows(
        args.kjva_apocrypha_bridge_confirmatory_term_summary
    )
    kjva_apocrypha_bridge_confirmatory_manifest = read_json(
        args.kjva_apocrypha_bridge_confirmatory_manifest
    )
    kjva_apocrypha_bridge_prospective_rows = read_rows(
        args.kjva_apocrypha_bridge_prospective_term_summary
    )
    kjva_apocrypha_bridge_prospective_manifest = read_json(
        args.kjva_apocrypha_bridge_prospective_manifest
    )
    kjva_apocrypha_bridge_prospective_nonbible_rows = read_rows(
        args.kjva_apocrypha_bridge_prospective_nonbible_summary
    )
    kjva_apocrypha_bridge_prospective_nonbible_manifest = read_json(
        args.kjva_apocrypha_bridge_prospective_nonbible_manifest
    )
    external_claim_counts_rows = read_rows(args.external_claim_counts_summary)
    external_claim_counts_manifest = read_json(args.external_claim_counts_manifest)
    external_claim_all_codes_rows = read_rows(args.external_claim_all_codes_summary)
    external_claim_all_codes_summary_manifest = read_json(
        args.external_claim_all_codes_summary_manifest
    )
    external_claim_all_codes_triage_rows = read_rows(args.external_claim_all_codes_triage)
    external_claim_all_codes_triage_manifest = read_json(
        args.external_claim_all_codes_triage_manifest
    )
    matrix_cluster_relation_control_rows = read_rows(
        args.matrix_cluster_relation_control_summary
    )
    matrix_cluster_term_pair_control_rows = read_rows(
        args.matrix_cluster_term_pair_control_summary
    )
    notable_passage_gap_passage_rows = read_rows(args.notable_passage_gap_passage_summary)
    notable_passage_gap_cross_source_rows = read_rows(
        args.notable_passage_gap_cross_source_summary
    )
    thematic_chapter_absence_passage_rows = read_rows(
        args.thematic_chapter_absence_passage_summary
    )
    thematic_chapter_absence_cross_source_rows = read_rows(
        args.thematic_chapter_absence_cross_source_summary
    )
    match_strata_summary_rows = read_rows(args.match_strata_summary)
    boundary_alignment_summary_rows = read_rows(args.boundary_alignment_summary)
    chapter_position_bias_summary_rows = read_rows(args.chapter_position_bias_summary)
    direction_asymmetry_summary_rows = read_rows(args.direction_asymmetry_summary)
    canonical_first_summary_rows = read_rows(args.canonical_first_summary)
    cross_skip_summary_rows = read_rows(args.cross_skip_summary)
    review_flag_summary_rows = read_rows(args.review_flag_summary)
    cohort_cluster_density_summary_rows = read_rows(args.cohort_cluster_density_summary)
    commit = git_commit()

    write_summary(
        args.summary_out,
        commit=commit,
        step_manifest=step_manifest,
        greek_gate_rows=greek_gate_rows,
        greek_pattern_rows=greek_pattern_rows,
        doxa_rows=doxa_rows,
        doxa_manifest=doxa_manifest,
        doxa_confirmatory_rows=doxa_confirmatory_rows,
        doxa_confirmatory_manifest=doxa_confirmatory_manifest,
        surface_queue_summary_rows=surface_queue_summary_rows,
        surface_queue_pattern_rows=surface_queue_pattern_rows,
        surface_queue_manifest=surface_queue_manifest,
        surface_triage_selected_rows=surface_triage_selected_rows,
        surface_triage_cohort_rows=surface_triage_cohort_rows,
        surface_triage_manifest=surface_triage_manifest,
        surface_letter_path_rows=surface_letter_path_rows,
        surface_letter_paths_manifest=surface_letter_paths_manifest,
        surface_control_frequency_rows=surface_control_frequency_rows,
        surface_control_matched_rows=surface_control_matched_rows,
        surface_control_manifest=surface_control_manifest,
        surface_control_evaluation_rows=surface_control_evaluation_rows,
        surface_control_evaluation_manifest=surface_control_evaluation_manifest,
        surface_available_control_evaluation_rows=surface_available_control_evaluation_rows,
        surface_available_control_evaluation_manifest=surface_available_control_evaluation_manifest,
        surface_followup_report_manifest=surface_followup_report_manifest,
        surface_followup_protocol_manifest=surface_followup_protocol_manifest,
        length4_selected_rows=length4_selected_rows,
        length4_cohort_rows=length4_cohort_rows,
        length4_control_evaluation_rows=length4_control_evaluation_rows,
        length4_letter_path_rows=length4_letter_path_rows,
        length4_protocol_manifest=length4_protocol_manifest,
        length4_vocab_terms_manifest=length4_vocab_terms_manifest,
        length4_vocab_control_evaluation_rows=length4_vocab_control_evaluation_rows,
        length4_vocab_protocol_manifest=length4_vocab_protocol_manifest,
        wrr_protocol_manifest=wrr_protocol_manifest,
        wrr_source_manifest=wrr_source_manifest,
        wrr_text_source_rows=wrr_text_source_rows,
        wrr_source_shapes_summary_rows=wrr_source_shapes_summary_rows,
        wrr_count_summary_rows=wrr_count_summary_rows,
        wrr_pair_audit_len_5_8_rows=wrr_pair_audit_len_5_8_rows,
        wrr_pair_controls_len_5_8_rows=wrr_pair_controls_len_5_8_rows,
        wrr_skip_caps_summary_rows=wrr_skip_caps_summary_rows,
        wrr_pair_table_reconciliation_rows=wrr_pair_table_reconciliation_rows,
        wrr_perturbation_summary_rows=wrr_perturbation_summary_rows,
        wrr_cross_pair_recommended_permutation_rows=(
            wrr_cross_pair_recommended_permutation_rows
        ),
        hebrew_theology_all_codes_triage_manifest=hebrew_theology_all_codes_triage_manifest,
        hebrew_screening_all_codes_triage_manifest=hebrew_screening_all_codes_triage_manifest,
        greek_screening_all_codes_triage_manifest=greek_screening_all_codes_triage_manifest,
        all_codes_followup_selection_manifest=all_codes_followup_selection_manifest,
        all_codes_followup_letter_path_rows=all_codes_followup_letter_path_rows,
        all_codes_followup_letter_paths_manifest=all_codes_followup_letter_paths_manifest,
        all_codes_followup_context_rows=all_codes_followup_context_rows,
        all_codes_followup_context_manifest=all_codes_followup_context_manifest,
        all_codes_followup_extension_rows=all_codes_followup_extension_rows,
        all_codes_followup_extensions_manifest=all_codes_followup_extensions_manifest,
        all_codes_compound_extension_control_rows=all_codes_compound_extension_control_rows,
        all_codes_compound_extension_controls_manifest=all_codes_compound_extension_controls_manifest,
        all_codes_compound_extension_confirmatory_rows=all_codes_compound_extension_confirmatory_rows,
        all_codes_compound_extension_confirmatory_manifest=all_codes_compound_extension_confirmatory_manifest,
        all_codes_compound_extension_confirmatory_protocol_manifest=all_codes_compound_extension_confirmatory_protocol_manifest,
        all_codes_followup_review_rows=all_codes_followup_review_rows,
        all_codes_followup_review_manifest=all_codes_followup_review_manifest,
        centered_occurrence_presence_rows=centered_occurrence_presence_rows,
        centered_occurrence_manifest=centered_occurrence_manifest,
        kjva_apocrypha_bridge_confirmatory_rows=kjva_apocrypha_bridge_confirmatory_rows,
        kjva_apocrypha_bridge_confirmatory_manifest=kjva_apocrypha_bridge_confirmatory_manifest,
        kjva_apocrypha_bridge_prospective_rows=kjva_apocrypha_bridge_prospective_rows,
        kjva_apocrypha_bridge_prospective_manifest=kjva_apocrypha_bridge_prospective_manifest,
        kjva_apocrypha_bridge_prospective_nonbible_rows=kjva_apocrypha_bridge_prospective_nonbible_rows,
        kjva_apocrypha_bridge_prospective_nonbible_manifest=kjva_apocrypha_bridge_prospective_nonbible_manifest,
        external_claim_counts_rows=external_claim_counts_rows,
        external_claim_counts_manifest=external_claim_counts_manifest,
        external_claim_all_codes_rows=external_claim_all_codes_rows,
        external_claim_all_codes_summary_manifest=external_claim_all_codes_summary_manifest,
        external_claim_all_codes_triage_rows=external_claim_all_codes_triage_rows,
        external_claim_all_codes_triage_manifest=external_claim_all_codes_triage_manifest,
        matrix_cluster_relation_control_rows=matrix_cluster_relation_control_rows,
        matrix_cluster_term_pair_control_rows=matrix_cluster_term_pair_control_rows,
        notable_passage_gap_passage_rows=notable_passage_gap_passage_rows,
        notable_passage_gap_cross_source_rows=notable_passage_gap_cross_source_rows,
        thematic_chapter_absence_passage_rows=thematic_chapter_absence_passage_rows,
        thematic_chapter_absence_cross_source_rows=thematic_chapter_absence_cross_source_rows,
        match_strata_summary_rows=match_strata_summary_rows,
        boundary_alignment_summary_rows=boundary_alignment_summary_rows,
        chapter_position_bias_summary_rows=chapter_position_bias_summary_rows,
        direction_asymmetry_summary_rows=direction_asymmetry_summary_rows,
        canonical_first_summary_rows=canonical_first_summary_rows,
        cross_skip_summary_rows=cross_skip_summary_rows,
        review_flag_summary_rows=review_flag_summary_rows,
        cohort_cluster_density_summary_rows=cohort_cluster_density_summary_rows,
        report_index=args.report_index,
    )
    write_manifest(
        args,
        commit=commit,
        step_manifest=step_manifest,
        greek_gate_rows=greek_gate_rows,
        greek_pattern_rows=greek_pattern_rows,
        doxa_rows=doxa_rows,
        doxa_manifest=doxa_manifest,
        doxa_confirmatory_rows=doxa_confirmatory_rows,
        doxa_confirmatory_manifest=doxa_confirmatory_manifest,
        surface_queue_summary_rows=surface_queue_summary_rows,
        surface_queue_pattern_rows=surface_queue_pattern_rows,
        surface_queue_manifest=surface_queue_manifest,
        surface_triage_selected_rows=surface_triage_selected_rows,
        surface_triage_cohort_rows=surface_triage_cohort_rows,
        surface_triage_manifest=surface_triage_manifest,
        surface_letter_path_rows=surface_letter_path_rows,
        surface_letter_paths_manifest=surface_letter_paths_manifest,
        surface_control_frequency_rows=surface_control_frequency_rows,
        surface_control_matched_rows=surface_control_matched_rows,
        surface_control_manifest=surface_control_manifest,
        surface_control_evaluation_rows=surface_control_evaluation_rows,
        surface_control_evaluation_manifest=surface_control_evaluation_manifest,
        surface_available_control_evaluation_rows=surface_available_control_evaluation_rows,
        surface_available_control_evaluation_manifest=surface_available_control_evaluation_manifest,
        surface_followup_report_manifest=surface_followup_report_manifest,
        surface_followup_protocol_manifest=surface_followup_protocol_manifest,
        length4_selected_rows=length4_selected_rows,
        length4_cohort_rows=length4_cohort_rows,
        length4_control_evaluation_rows=length4_control_evaluation_rows,
        length4_letter_path_rows=length4_letter_path_rows,
        length4_protocol_manifest=length4_protocol_manifest,
        length4_vocab_terms_manifest=length4_vocab_terms_manifest,
        length4_vocab_control_evaluation_rows=length4_vocab_control_evaluation_rows,
        length4_vocab_protocol_manifest=length4_vocab_protocol_manifest,
        wrr_protocol_manifest=wrr_protocol_manifest,
        wrr_source_manifest=wrr_source_manifest,
        wrr_text_source_rows=wrr_text_source_rows,
        wrr_source_shapes_summary_rows=wrr_source_shapes_summary_rows,
        wrr_count_summary_rows=wrr_count_summary_rows,
        wrr_pair_audit_len_5_8_rows=wrr_pair_audit_len_5_8_rows,
        wrr_pair_controls_len_5_8_rows=wrr_pair_controls_len_5_8_rows,
        wrr_skip_caps_summary_rows=wrr_skip_caps_summary_rows,
        wrr_pair_table_reconciliation_rows=wrr_pair_table_reconciliation_rows,
        wrr_perturbation_summary_rows=wrr_perturbation_summary_rows,
        wrr_cross_pair_recommended_permutation_rows=(
            wrr_cross_pair_recommended_permutation_rows
        ),
        hebrew_theology_all_codes_triage_manifest=hebrew_theology_all_codes_triage_manifest,
        hebrew_screening_all_codes_triage_manifest=hebrew_screening_all_codes_triage_manifest,
        greek_screening_all_codes_triage_manifest=greek_screening_all_codes_triage_manifest,
        all_codes_followup_selection_manifest=all_codes_followup_selection_manifest,
        all_codes_followup_letter_path_rows=all_codes_followup_letter_path_rows,
        all_codes_followup_letter_paths_manifest=all_codes_followup_letter_paths_manifest,
        all_codes_followup_context_rows=all_codes_followup_context_rows,
        all_codes_followup_context_manifest=all_codes_followup_context_manifest,
        all_codes_followup_extension_rows=all_codes_followup_extension_rows,
        all_codes_followup_extensions_manifest=all_codes_followup_extensions_manifest,
        all_codes_compound_extension_control_rows=all_codes_compound_extension_control_rows,
        all_codes_compound_extension_controls_manifest=all_codes_compound_extension_controls_manifest,
        all_codes_compound_extension_confirmatory_rows=all_codes_compound_extension_confirmatory_rows,
        all_codes_compound_extension_confirmatory_manifest=all_codes_compound_extension_confirmatory_manifest,
        all_codes_compound_extension_confirmatory_protocol_manifest=all_codes_compound_extension_confirmatory_protocol_manifest,
        all_codes_followup_review_rows=all_codes_followup_review_rows,
        all_codes_followup_review_manifest=all_codes_followup_review_manifest,
        centered_occurrence_presence_rows=centered_occurrence_presence_rows,
        centered_occurrence_manifest=centered_occurrence_manifest,
        kjva_apocrypha_bridge_confirmatory_rows=kjva_apocrypha_bridge_confirmatory_rows,
        kjva_apocrypha_bridge_confirmatory_manifest=kjva_apocrypha_bridge_confirmatory_manifest,
        kjva_apocrypha_bridge_prospective_rows=kjva_apocrypha_bridge_prospective_rows,
        kjva_apocrypha_bridge_prospective_manifest=kjva_apocrypha_bridge_prospective_manifest,
        kjva_apocrypha_bridge_prospective_nonbible_rows=kjva_apocrypha_bridge_prospective_nonbible_rows,
        kjva_apocrypha_bridge_prospective_nonbible_manifest=kjva_apocrypha_bridge_prospective_nonbible_manifest,
        external_claim_counts_rows=external_claim_counts_rows,
        external_claim_counts_manifest=external_claim_counts_manifest,
        external_claim_all_codes_rows=external_claim_all_codes_rows,
        external_claim_all_codes_summary_manifest=external_claim_all_codes_summary_manifest,
        external_claim_all_codes_triage_rows=external_claim_all_codes_triage_rows,
        external_claim_all_codes_triage_manifest=external_claim_all_codes_triage_manifest,
        matrix_cluster_relation_control_rows=matrix_cluster_relation_control_rows,
        matrix_cluster_term_pair_control_rows=matrix_cluster_term_pair_control_rows,
        notable_passage_gap_passage_rows=notable_passage_gap_passage_rows,
        notable_passage_gap_cross_source_rows=notable_passage_gap_cross_source_rows,
        thematic_chapter_absence_passage_rows=thematic_chapter_absence_passage_rows,
        thematic_chapter_absence_cross_source_rows=thematic_chapter_absence_cross_source_rows,
        match_strata_summary_rows=match_strata_summary_rows,
        boundary_alignment_summary_rows=boundary_alignment_summary_rows,
        chapter_position_bias_summary_rows=chapter_position_bias_summary_rows,
        direction_asymmetry_summary_rows=direction_asymmetry_summary_rows,
        canonical_first_summary_rows=canonical_first_summary_rows,
        cross_skip_summary_rows=cross_skip_summary_rows,
        review_flag_summary_rows=review_flag_summary_rows,
        cohort_cluster_density_summary_rows=cohort_cluster_density_summary_rows,
        started=started,
    )
    print(args.summary_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-tahot-manifest", type=Path, default=STEP_TAHOT_MANIFEST)
    parser.add_argument("--greek-gate-summary", type=Path, default=GREEK_GATE_SUMMARY)
    parser.add_argument("--greek-pattern-summary", type=Path, default=GREEK_PATTERN_SUMMARY)
    parser.add_argument("--doxa-summary", type=Path, default=DOXA_SUMMARY)
    parser.add_argument("--doxa-protocol-manifest", type=Path, default=DOXA_PROTOCOL_MANIFEST)
    parser.add_argument(
        "--doxa-confirmatory-summary",
        type=Path,
        default=DOXA_CONFIRMATORY_SUMMARY,
    )
    parser.add_argument(
        "--doxa-confirmatory-protocol-manifest",
        type=Path,
        default=DOXA_CONFIRMATORY_PROTOCOL_MANIFEST,
    )
    parser.add_argument("--surface-queue-summary", type=Path, default=SURFACE_QUEUE_SUMMARY)
    parser.add_argument("--surface-queue-patterns", type=Path, default=SURFACE_QUEUE_PATTERNS)
    parser.add_argument(
        "--surface-queue-protocol-manifest",
        type=Path,
        default=SURFACE_QUEUE_PROTOCOL_MANIFEST,
    )
    parser.add_argument("--surface-triage-selected", type=Path, default=SURFACE_TRIAGE_SELECTED)
    parser.add_argument("--surface-triage-cohort", type=Path, default=SURFACE_TRIAGE_COHORT)
    parser.add_argument(
        "--surface-triage-protocol-manifest",
        type=Path,
        default=SURFACE_TRIAGE_PROTOCOL_MANIFEST,
    )
    parser.add_argument(
        "--surface-letter-paths-summary",
        type=Path,
        default=SURFACE_LETTER_PATHS_SUMMARY,
    )
    parser.add_argument(
        "--surface-letter-paths-protocol-manifest",
        type=Path,
        default=SURFACE_LETTER_PATHS_PROTOCOL_MANIFEST,
    )
    parser.add_argument("--surface-control-frequencies", type=Path, default=SURFACE_CONTROL_FREQUENCIES)
    parser.add_argument("--surface-control-matched", type=Path, default=SURFACE_CONTROL_MATCHED)
    parser.add_argument(
        "--surface-control-protocol-manifest",
        type=Path,
        default=SURFACE_CONTROL_PROTOCOL_MANIFEST,
    )
    parser.add_argument("--surface-control-evaluation", type=Path, default=SURFACE_CONTROL_EVALUATION)
    parser.add_argument(
        "--surface-control-evaluation-manifest",
        type=Path,
        default=SURFACE_CONTROL_EVALUATION_MANIFEST,
    )
    parser.add_argument(
        "--surface-available-control-evaluation",
        type=Path,
        default=SURFACE_AVAILABLE_CONTROL_EVALUATION,
    )
    parser.add_argument(
        "--surface-available-control-evaluation-manifest",
        type=Path,
        default=SURFACE_AVAILABLE_CONTROL_EVALUATION_MANIFEST,
    )
    parser.add_argument(
        "--surface-followup-report-manifest",
        type=Path,
        default=SURFACE_FOLLOWUP_REPORT_MANIFEST,
    )
    parser.add_argument(
        "--surface-followup-protocol-manifest",
        type=Path,
        default=SURFACE_FOLLOWUP_PROTOCOL_MANIFEST,
    )
    parser.add_argument("--length4-selected", type=Path, default=LENGTH4_SELECTED)
    parser.add_argument("--length4-cohort", type=Path, default=LENGTH4_COHORT)
    parser.add_argument(
        "--length4-control-evaluation",
        type=Path,
        default=LENGTH4_CONTROL_EVALUATION,
    )
    parser.add_argument("--length4-letter-paths", type=Path, default=LENGTH4_LETTER_PATHS)
    parser.add_argument(
        "--length4-protocol-manifest",
        type=Path,
        default=LENGTH4_PROTOCOL_MANIFEST,
    )
    parser.add_argument(
        "--length4-vocab-terms-manifest",
        type=Path,
        default=LENGTH4_VOCAB_TERMS_MANIFEST,
    )
    parser.add_argument(
        "--length4-vocab-control-evaluation",
        type=Path,
        default=LENGTH4_VOCAB_CONTROL_EVALUATION,
    )
    parser.add_argument(
        "--length4-vocab-protocol-manifest",
        type=Path,
        default=LENGTH4_VOCAB_PROTOCOL_MANIFEST,
    )
    parser.add_argument("--wrr-protocol-manifest", type=Path, default=WRR_PROTOCOL_MANIFEST)
    parser.add_argument("--wrr-source-manifest", type=Path, default=WRR_SOURCE_MANIFEST)
    parser.add_argument("--wrr-text-source", type=Path, default=WRR_TEXT_SOURCE_SUMMARY)
    parser.add_argument(
        "--wrr-source-shapes-summary",
        type=Path,
        default=WRR_SOURCE_SHAPES_SUMMARY,
    )
    parser.add_argument("--wrr-count-summary", type=Path, default=WRR_COUNT_SUMMARY)
    parser.add_argument(
        "--wrr-pair-audit-len-5-8",
        type=Path,
        default=WRR_PAIR_AUDIT_LEN_5_8,
    )
    parser.add_argument(
        "--wrr-pair-controls-len-5-8",
        type=Path,
        default=WRR_PAIR_CONTROLS_LEN_5_8,
    )
    parser.add_argument("--wrr-skip-caps-summary", type=Path, default=WRR_SKIP_CAPS_SUMMARY)
    parser.add_argument(
        "--wrr-pair-table-reconciliation",
        type=Path,
        default=WRR_PAIR_TABLE_RECONCILIATION,
    )
    parser.add_argument(
        "--wrr-perturbation-summary",
        type=Path,
        default=WRR_PERTURBATION_SUMMARY,
    )
    parser.add_argument(
        "--wrr-cross-pair-recommended-permutation-summary",
        type=Path,
        default=WRR_CROSS_PAIR_RECOMMENDED_PERMUTATION_SUMMARY,
    )
    parser.add_argument(
        "--hebrew-theology-all-codes-triage-manifest",
        type=Path,
        default=HEBREW_THEOLOGY_ALL_CODES_TRIAGE_MANIFEST,
    )
    parser.add_argument(
        "--hebrew-screening-all-codes-triage-manifest",
        type=Path,
        default=HEBREW_SCREENING_ALL_CODES_TRIAGE_MANIFEST,
    )
    parser.add_argument(
        "--greek-screening-all-codes-triage-manifest",
        type=Path,
        default=GREEK_SCREENING_ALL_CODES_TRIAGE_MANIFEST,
    )
    parser.add_argument(
        "--all-codes-followup-selection-manifest",
        type=Path,
        default=ALL_CODES_FOLLOWUP_SELECTION_MANIFEST,
    )
    parser.add_argument(
        "--all-codes-followup-letter-paths-summary",
        type=Path,
        default=ALL_CODES_FOLLOWUP_LETTER_PATHS_SUMMARY,
    )
    parser.add_argument(
        "--all-codes-followup-letter-paths-manifest",
        type=Path,
        default=ALL_CODES_FOLLOWUP_LETTER_PATHS_MANIFEST,
    )
    parser.add_argument(
        "--all-codes-followup-context-excerpts",
        type=Path,
        default=ALL_CODES_FOLLOWUP_CONTEXT_EXCERPTS,
    )
    parser.add_argument(
        "--all-codes-followup-context-manifest",
        type=Path,
        default=ALL_CODES_FOLLOWUP_CONTEXT_MANIFEST,
    )
    parser.add_argument(
        "--all-codes-followup-extensions-summary",
        type=Path,
        default=ALL_CODES_FOLLOWUP_EXTENSIONS_SUMMARY,
    )
    parser.add_argument(
        "--all-codes-followup-extensions-manifest",
        type=Path,
        default=ALL_CODES_FOLLOWUP_EXTENSIONS_MANIFEST,
    )
    parser.add_argument(
        "--all-codes-compound-extension-controls-summary",
        type=Path,
        default=ALL_CODES_COMPOUND_EXTENSION_CONTROLS_SUMMARY,
    )
    parser.add_argument(
        "--all-codes-compound-extension-controls-manifest",
        type=Path,
        default=ALL_CODES_COMPOUND_EXTENSION_CONTROLS_MANIFEST,
    )
    parser.add_argument(
        "--all-codes-compound-extension-confirmatory-summary",
        type=Path,
        default=ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_SUMMARY,
    )
    parser.add_argument(
        "--all-codes-compound-extension-confirmatory-manifest",
        type=Path,
        default=ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_MANIFEST,
    )
    parser.add_argument(
        "--all-codes-compound-extension-confirmatory-protocol-manifest",
        type=Path,
        default=ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_PROTOCOL_MANIFEST,
    )
    parser.add_argument(
        "--all-codes-followup-review-summary",
        type=Path,
        default=ALL_CODES_FOLLOWUP_REVIEW_SUMMARY,
    )
    parser.add_argument(
        "--all-codes-followup-review-manifest",
        type=Path,
        default=ALL_CODES_FOLLOWUP_REVIEW_MANIFEST,
    )
    parser.add_argument(
        "--centered-occurrence-presence",
        type=Path,
        default=CENTERED_OCCURRENCE_PRESENCE,
    )
    parser.add_argument(
        "--centered-occurrence-manifest",
        type=Path,
        default=CENTERED_OCCURRENCE_MANIFEST,
    )
    parser.add_argument(
        "--kjva-apocrypha-bridge-confirmatory-term-summary",
        type=Path,
        default=KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_TERM_SUMMARY,
    )
    parser.add_argument(
        "--kjva-apocrypha-bridge-confirmatory-manifest",
        type=Path,
        default=KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_MANIFEST,
    )
    parser.add_argument(
        "--kjva-apocrypha-bridge-prospective-term-summary",
        type=Path,
        default=KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_TERM_SUMMARY,
    )
    parser.add_argument(
        "--kjva-apocrypha-bridge-prospective-manifest",
        type=Path,
        default=KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_MANIFEST,
    )
    parser.add_argument(
        "--kjva-apocrypha-bridge-prospective-nonbible-summary",
        type=Path,
        default=KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_SUMMARY,
    )
    parser.add_argument(
        "--kjva-apocrypha-bridge-prospective-nonbible-manifest",
        type=Path,
        default=KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_MANIFEST,
    )
    parser.add_argument(
        "--external-claim-counts-summary",
        type=Path,
        default=EXTERNAL_CLAIM_COUNTS_SUMMARY,
    )
    parser.add_argument(
        "--external-claim-counts-manifest",
        type=Path,
        default=EXTERNAL_CLAIM_COUNTS_MANIFEST,
    )
    parser.add_argument(
        "--external-claim-all-codes-summary",
        type=Path,
        default=EXTERNAL_CLAIM_ALL_CODES_SUMMARY,
    )
    parser.add_argument(
        "--external-claim-all-codes-summary-manifest",
        type=Path,
        default=EXTERNAL_CLAIM_ALL_CODES_SUMMARY_MANIFEST,
    )
    parser.add_argument(
        "--external-claim-all-codes-triage",
        type=Path,
        default=EXTERNAL_CLAIM_ALL_CODES_TRIAGE,
    )
    parser.add_argument(
        "--external-claim-all-codes-triage-manifest",
        type=Path,
        default=EXTERNAL_CLAIM_ALL_CODES_TRIAGE_MANIFEST,
    )
    parser.add_argument(
        "--matrix-cluster-relation-control-summary",
        type=Path,
        default=MATRIX_CLUSTER_RELATION_CONTROL_SUMMARY,
    )
    parser.add_argument(
        "--matrix-cluster-term-pair-control-summary",
        type=Path,
        default=MATRIX_CLUSTER_TERM_PAIR_CONTROL_SUMMARY,
    )
    parser.add_argument(
        "--notable-passage-gap-passage-summary",
        type=Path,
        default=NOTABLE_PASSAGE_GAP_PASSAGE_SUMMARY,
    )
    parser.add_argument(
        "--notable-passage-gap-cross-source-summary",
        type=Path,
        default=NOTABLE_PASSAGE_GAP_CROSS_SOURCE_SUMMARY,
    )
    parser.add_argument(
        "--thematic-chapter-absence-passage-summary",
        type=Path,
        default=THEMATIC_CHAPTER_ABSENCE_PASSAGE_SUMMARY,
    )
    parser.add_argument(
        "--thematic-chapter-absence-cross-source-summary",
        type=Path,
        default=THEMATIC_CHAPTER_ABSENCE_CROSS_SOURCE_SUMMARY,
    )
    parser.add_argument("--match-strata-summary", type=Path, default=MATCH_STRATA_SUMMARY)
    parser.add_argument(
        "--boundary-alignment-summary",
        type=Path,
        default=BOUNDARY_ALIGNMENT_SUMMARY,
    )
    parser.add_argument(
        "--chapter-position-bias-summary",
        type=Path,
        default=CHAPTER_POSITION_BIAS_SUMMARY,
    )
    parser.add_argument(
        "--direction-asymmetry-summary",
        type=Path,
        default=DIRECTION_ASYMMETRY_SUMMARY,
    )
    parser.add_argument(
        "--canonical-first-summary",
        type=Path,
        default=CANONICAL_FIRST_SUMMARY,
    )
    parser.add_argument("--cross-skip-summary", type=Path, default=CROSS_SKIP_SUMMARY)
    parser.add_argument("--review-flag-summary", type=Path, default=REVIEW_FLAG_SUMMARY)
    parser.add_argument(
        "--cohort-cluster-density-summary",
        type=Path,
        default=COHORT_CLUSTER_DENSITY_SUMMARY,
    )
    parser.add_argument("--report-index", type=Path, default=REPORT_INDEX)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def write_summary(
    path: Path,
    *,
    commit: str,
    step_manifest: dict[str, Any],
    greek_gate_rows: list[dict[str, str]],
    greek_pattern_rows: list[dict[str, str]],
    doxa_rows: list[dict[str, str]],
    doxa_manifest: dict[str, Any],
    doxa_confirmatory_rows: list[dict[str, str]],
    doxa_confirmatory_manifest: dict[str, Any],
    surface_queue_summary_rows: list[dict[str, str]],
    surface_queue_pattern_rows: list[dict[str, str]],
    surface_queue_manifest: dict[str, Any],
    surface_triage_selected_rows: list[dict[str, str]],
    surface_triage_cohort_rows: list[dict[str, str]],
    surface_triage_manifest: dict[str, Any],
    surface_letter_path_rows: list[dict[str, str]],
    surface_letter_paths_manifest: dict[str, Any],
    surface_control_frequency_rows: list[dict[str, str]],
    surface_control_matched_rows: list[dict[str, str]],
    surface_control_manifest: dict[str, Any],
    surface_control_evaluation_rows: list[dict[str, str]],
    surface_control_evaluation_manifest: dict[str, Any],
    surface_available_control_evaluation_rows: list[dict[str, str]],
    surface_available_control_evaluation_manifest: dict[str, Any],
    surface_followup_report_manifest: dict[str, Any],
    surface_followup_protocol_manifest: dict[str, Any],
    length4_selected_rows: list[dict[str, str]],
    length4_cohort_rows: list[dict[str, str]],
    length4_control_evaluation_rows: list[dict[str, str]],
    length4_letter_path_rows: list[dict[str, str]],
    length4_protocol_manifest: dict[str, Any],
    length4_vocab_terms_manifest: dict[str, Any],
    length4_vocab_control_evaluation_rows: list[dict[str, str]],
    length4_vocab_protocol_manifest: dict[str, Any],
    wrr_protocol_manifest: dict[str, Any],
    wrr_source_manifest: dict[str, Any],
    wrr_text_source_rows: list[dict[str, str]],
    wrr_source_shapes_summary_rows: list[dict[str, str]],
    wrr_count_summary_rows: list[dict[str, str]],
    wrr_pair_audit_len_5_8_rows: list[dict[str, str]],
    wrr_pair_controls_len_5_8_rows: list[dict[str, str]],
    wrr_skip_caps_summary_rows: list[dict[str, str]],
    wrr_pair_table_reconciliation_rows: list[dict[str, str]],
    wrr_perturbation_summary_rows: list[dict[str, str]],
    wrr_cross_pair_recommended_permutation_rows: list[dict[str, str]],
    hebrew_theology_all_codes_triage_manifest: dict[str, Any],
    hebrew_screening_all_codes_triage_manifest: dict[str, Any],
    greek_screening_all_codes_triage_manifest: dict[str, Any],
    all_codes_followup_selection_manifest: dict[str, Any],
    all_codes_followup_letter_path_rows: list[dict[str, str]],
    all_codes_followup_letter_paths_manifest: dict[str, Any],
    all_codes_followup_context_rows: list[dict[str, str]],
    all_codes_followup_context_manifest: dict[str, Any],
    all_codes_followup_extension_rows: list[dict[str, str]],
    all_codes_followup_extensions_manifest: dict[str, Any],
    all_codes_compound_extension_control_rows: list[dict[str, str]],
    all_codes_compound_extension_controls_manifest: dict[str, Any],
    all_codes_compound_extension_confirmatory_rows: list[dict[str, str]],
    all_codes_compound_extension_confirmatory_manifest: dict[str, Any],
    all_codes_compound_extension_confirmatory_protocol_manifest: dict[str, Any],
    all_codes_followup_review_rows: list[dict[str, str]],
    all_codes_followup_review_manifest: dict[str, Any],
    centered_occurrence_presence_rows: list[dict[str, str]],
    centered_occurrence_manifest: dict[str, Any],
    kjva_apocrypha_bridge_confirmatory_rows: list[dict[str, str]],
    kjva_apocrypha_bridge_confirmatory_manifest: dict[str, Any],
    kjva_apocrypha_bridge_prospective_rows: list[dict[str, str]],
    kjva_apocrypha_bridge_prospective_manifest: dict[str, Any],
    kjva_apocrypha_bridge_prospective_nonbible_rows: list[dict[str, str]],
    kjva_apocrypha_bridge_prospective_nonbible_manifest: dict[str, Any],
    external_claim_counts_rows: list[dict[str, str]],
    external_claim_counts_manifest: dict[str, Any],
    external_claim_all_codes_rows: list[dict[str, str]],
    external_claim_all_codes_summary_manifest: dict[str, Any],
    external_claim_all_codes_triage_rows: list[dict[str, str]],
    external_claim_all_codes_triage_manifest: dict[str, Any],
    matrix_cluster_relation_control_rows: list[dict[str, str]],
    matrix_cluster_term_pair_control_rows: list[dict[str, str]],
    notable_passage_gap_passage_rows: list[dict[str, str]],
    notable_passage_gap_cross_source_rows: list[dict[str, str]],
    thematic_chapter_absence_passage_rows: list[dict[str, str]],
    thematic_chapter_absence_cross_source_rows: list[dict[str, str]],
    match_strata_summary_rows: list[dict[str, str]],
    boundary_alignment_summary_rows: list[dict[str, str]],
    chapter_position_bias_summary_rows: list[dict[str, str]],
    direction_asymmetry_summary_rows: list[dict[str, str]],
    canonical_first_summary_rows: list[dict[str, str]],
    cross_skip_summary_rows: list[dict[str, str]],
    review_flag_summary_rows: list[dict[str, str]],
    cohort_cluster_density_summary_rows: list[dict[str, str]],
    report_index: Path,
) -> None:
    real_counts = step_manifest.get("real_counts", {})
    control_counts = step_manifest.get("control_counts", {})
    real_policy = step_manifest.get("real_policy_counts", {})
    control_policy = step_manifest.get("control_policy_counts", {})
    strongest = next(
        (
            row
            for row in greek_gate_rows
            if row["final_gate"] == "cross_version_controlled_surface_anchored_hidden_candidate"
        ),
        {},
    )
    lines = [
        "# Real Report Run Summary",
        "",
        f"Generated UTC: {datetime.now(UTC).isoformat()}",
        f"Commit: `{commit}`",
        "",
        "## Scope",
        "",
        "This is an assembly report over locked outputs, not a new exploratory term expansion.",
        "",
        "Included tracks:",
        "",
        "- STEP_TAHOT Hebrew source-family final gate",
        "- Greek exact-center pattern version summary",
        "- Greek exact-center final gate",
        "- Doxa four-source claim follow-up",
        "- Doxa four-source confirmatory follow-up",
        "- expanded Greek exact-center surface queue",
        "- expanded Greek exact-center surface triage",
        "- expanded Greek exact-center surface letter-path audit",
        "- expanded Greek exact-center surface real-word control pool",
        "- expanded Greek exact-center surface matched-control evaluation",
        "- expanded Greek exact-center surface all-available control evaluation",
        "- expanded Greek exact-center surface compact follow-up report",
        "- Greek surface length-4 post-discovery follow-up",
        "- Greek surface length-4 generated vocabulary-control follow-up",
        "- WRR 1994 source/import audit and repo-defined diagnostic status",
        "- broad Hebrew modern/geopolitical representative-control review",
        "- locked Hebrew modern/geopolitical prospective source-distribution report",
        "- broader Hebrew screening representative-control review",
        "- relaxed all-codes Hebrew theology triage",
        "- relaxed all-codes Hebrew screening triage",
        "- relaxed all-codes Greek screening triage",
        "- compact all-codes follow-up selection",
        "- all-codes follow-up letter-path audit",
        "- all-codes follow-up context excerpts",
        "- all-codes follow-up same-skip extension audit",
        "- all-codes compound-extension paired controls",
        "- all-codes compound-extension confirmatory controls",
        "- all-codes follow-up manual-review packet",
        "- centered occurrence index",
        "- apocrypha/deuterocanon bridge study with expanded shuffled controls",
        "- KJVA apocrypha/deuterocanon bridge term-level review",
        "- KJVA apocrypha/deuterocanon bridge term-level shuffled controls",
        "- KJVA apocrypha/deuterocanon bridge 5000-sample confirmatory controls",
        "- external claim/source count baseline across Bible and secular controls",
        "- external claim/source relaxed all-codes collection, triage queue, and findings layer",
        "- expanded post-search strata summaries",
        "- matrix-cluster relation control summary",
        "- notable-passage cross-source gap ledger",
        "- thematic-chapter absence ledger",
        "- completed Gog/Magog prospective pair-control report",
        "- prospective-study lock/readiness documents",
        "- Bible Code Digest source audit and term-list expansion",
        "- CRI ELS critique audit and control-design guardrails",
        "- TheWordNotes ELS PDF source audit and term-list expansion",
        "- Cosmic Codes source audit and term-list expansion",
        "- Mark Tabata Isaiah 53 source audit and term-list expansion",
        "- Felcjo Ringo ELS algorithm/control-source audit",
        "- Amandasaurus/Rory Biblecode implementation prior-art audit",
        "- Bible-codes.org pictogram/source audit and term-list expansion",
        "- Bible and Science ELS critique/source audit",
        "- Religions Wiki scriptural-codes critique/source audit",
        "- Torah-code WRR-adjacent source-shape audits for Gans communities, American presidents, Witztum birth dates, Israeli prime ministers, Cities source-chain files, event/object experiment pages, under-construction placeholders, and missing research model pages",
        "- report file index",
        "",
        "## Current Read",
        "",
        "No row is labeled as a claim in this report run. Rows are classified as",
        "review candidates, source-specific candidates, or controls-informed holds.",
        "",
        "Hidden-path-only phrases are treated as normal ELS candidate types. A",
        "same-span surface echo is treated as a rarer stronger subtype, but is not",
        "required for candidate status.",
        "",
        "For centered-self and relevant-center rows, this report treats occurrence",
        "as the primary review fact: the row should be listed if it happens. Counts",
        "and controls describe frequency strength, but they do not remove the",
        "occurrence from the findings list.",
        "The centered occurrence index is the dedicated occurrence-first artifact",
        "for that final-report layer.",
        "",
        f"The current {display_term('δοξα', english='glory')} four-source follow-ups remain review candidates,",
        "not claims, even though the 5000/5000 and 20000/20000 locked runs",
        "passed their registered q <= 0.01 gates.",
        "",
        "The completed Hebrew Gog/Magog prospective pair-control lane produced",
        "target occurrences in MT_WLC and UHB, but no",
        "`prospective_controlled_review_candidate`: both rows were",
        "`not_unusual` under pair controls and synthetic 3+4 Hebrew pairs often",
        "matched or exceeded target density.",
        "",
        "## STEP_TAHOT Hebrew Gate",
        "",
        "| Metric | Real terms | Controls |",
        "| --- | ---: | ---: |",
        f"| Pattern rows | {int_value(real_counts, 'pattern_rows'):,} | {int_value(control_counts, 'pattern_rows'):,} |",
        f"| Patterns with STEP_TAHOT | {int_value(real_counts, 'with_source'):,} | {int_value(control_counts, 'with_source'):,} |",
        f"| STEP_TAHOT-only rows | {int_value(real_counts, 'source_only'):,} | {int_value(control_counts, 'source_only'):,} |",
        f"| Source-only rate | {percent(real_counts.get('source_only_rate'))} | {percent(control_counts.get('source_only_rate'))} |",
        f"| Policy-touch rows | {int_value(real_policy, 'policy_touch'):,} | {int_value(control_policy, 'policy_touch'):,} |",
        "",
        "STEP_TAHOT-only behavior appears at nearly the same rate in real screening",
        "rows and null/frequency controls, so STEP_TAHOT-only rows remain",
        "source-family review material rather than claim evidence.",
        "",
        "## Greek Exact-Center Gate",
        "",
        "| Pattern | Gate | Claim status | Present | Missing |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in greek_gate_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    display_overlap_key(row["overlap_key"]),
                    f"`{row['final_gate']}`",
                    f"`{row['claim_status']}`",
                    row["current_present_corpora"],
                    row["current_absent_corpora"] or "none",
                ]
            )
            + " |"
        )
    if strongest:
        lines.extend(
            [
                "",
                "Strongest current Greek row:",
                "",
                f"- {display_overlap_key(strongest['overlap_key'])}",
                f"- gate: `{strongest['final_gate']}`",
                f"- claim status: `{strongest['claim_status']}`",
            ]
    )
    lines.extend(doxa_section("Doxa Four-Source Claim Follow-Up", doxa_rows, doxa_manifest))
    lines.extend(
        doxa_section(
            "Doxa Four-Source Confirmatory Follow-Up",
            doxa_confirmatory_rows,
            doxa_confirmatory_manifest,
        )
    )
    lines.extend(
        surface_queue_section(
            surface_queue_summary_rows,
            surface_queue_pattern_rows,
            surface_queue_manifest,
        )
    )
    lines.extend(
        surface_triage_section(
            surface_triage_selected_rows,
            surface_triage_cohort_rows,
            surface_triage_manifest,
        )
    )
    lines.extend(
        surface_letter_paths_section(
            surface_letter_path_rows,
            surface_letter_paths_manifest,
        )
    )
    lines.extend(
        surface_control_pool_section(
            surface_control_frequency_rows,
            surface_control_matched_rows,
            surface_control_manifest,
        )
    )
    lines.extend(
        surface_control_evaluation_section(
            surface_control_evaluation_rows,
            surface_control_evaluation_manifest,
            title="Expanded Greek Surface Control Evaluation",
            lead=(
                "Exploratory result: selected rows beat their 10 matched real-word controls "
                "on all-source exact-center surface-pattern count, but the control pool is "
                "too small for p <= 0.05."
            ),
            read=(
                "Current read: useful triage evidence, not statistical support. A larger "
                "real-word matched-control pool must be frozen before a stronger "
                "evaluation."
            ),
        )
    )
    lines.extend(
        surface_control_evaluation_section(
            surface_available_control_evaluation_rows,
            surface_available_control_evaluation_manifest,
            title="Expanded Greek Surface All-Available Control Evaluation",
            lead=(
                "The all-available follow-up excludes selected targets from the control "
                "pool. Against the remaining same-length all-source controls, all three "
                "selected rows exceed that pool with study-level q = 0.032258."
            ),
            read=(
                "Current read: this is stronger triage evidence after excluding selected "
                "targets from controls, but it is still post-screen and not claim-grade."
            ),
        )
    )
    lines.extend(
        surface_followup_section(
            surface_followup_report_manifest,
            surface_followup_protocol_manifest,
        )
    )
    lines.extend(
        surface_length4_followup_section(
            length4_selected_rows,
            length4_cohort_rows,
            length4_control_evaluation_rows,
            length4_letter_path_rows,
            length4_protocol_manifest,
        )
    )
    lines.extend(
        surface_length4_vocabulary_controls_section(
            length4_vocab_terms_manifest,
            length4_vocab_control_evaluation_rows,
            length4_vocab_protocol_manifest,
        )
    )
    lines.extend(
        wrr_audit_section(
            wrr_protocol_manifest,
            wrr_source_manifest,
            wrr_text_source_rows,
            wrr_source_shapes_summary_rows,
            wrr_count_summary_rows,
            wrr_pair_audit_len_5_8_rows,
            wrr_pair_controls_len_5_8_rows,
            wrr_skip_caps_summary_rows,
            wrr_pair_table_reconciliation_rows,
            wrr_perturbation_summary_rows,
            wrr_cross_pair_recommended_permutation_rows,
        )
    )
    lines.extend(
        all_codes_triage_section(
            hebrew_theology_all_codes_triage_manifest,
            hebrew_screening_all_codes_triage_manifest,
            greek_screening_all_codes_triage_manifest,
            all_codes_followup_selection_manifest,
            all_codes_followup_letter_path_rows,
            all_codes_followup_letter_paths_manifest,
            all_codes_followup_context_rows,
            all_codes_followup_context_manifest,
            all_codes_followup_extension_rows,
            all_codes_followup_extensions_manifest,
            all_codes_compound_extension_control_rows,
            all_codes_compound_extension_controls_manifest,
            all_codes_compound_extension_confirmatory_rows,
            all_codes_compound_extension_confirmatory_manifest,
            all_codes_compound_extension_confirmatory_protocol_manifest,
            all_codes_followup_review_rows,
            all_codes_followup_review_manifest,
        )
    )
    lines.extend(
        centered_occurrence_section(
            centered_occurrence_presence_rows,
            centered_occurrence_manifest,
        )
    )
    lines.extend(
        expanded_strata_summary_section(
            match_strata_summary_rows,
            boundary_alignment_summary_rows,
            chapter_position_bias_summary_rows,
            direction_asymmetry_summary_rows,
            canonical_first_summary_rows,
            cross_skip_summary_rows,
            review_flag_summary_rows,
            cohort_cluster_density_summary_rows,
        )
    )
    lines.extend(
        kjva_apocrypha_bridge_confirmatory_section(
            kjva_apocrypha_bridge_confirmatory_rows,
            kjva_apocrypha_bridge_confirmatory_manifest,
        )
    )
    lines.extend(
        kjva_apocrypha_bridge_prospective_section(
            kjva_apocrypha_bridge_prospective_rows,
            kjva_apocrypha_bridge_prospective_manifest,
            kjva_apocrypha_bridge_prospective_nonbible_rows,
        )
    )
    lines.extend(
        external_claim_source_section(
            external_claim_counts_rows,
            external_claim_counts_manifest,
            external_claim_all_codes_rows,
            external_claim_all_codes_summary_manifest,
            external_claim_all_codes_triage_rows,
            external_claim_all_codes_triage_manifest,
        )
    )
    lines.extend(
        matrix_cluster_control_section(
            matrix_cluster_relation_control_rows,
            matrix_cluster_term_pair_control_rows,
        )
    )
    lines.extend(
        notable_passage_gap_section(
            notable_passage_gap_passage_rows,
            notable_passage_gap_cross_source_rows,
        )
    )
    lines.extend(
        thematic_chapter_absence_section(
            thematic_chapter_absence_passage_rows,
            thematic_chapter_absence_cross_source_rows,
        )
    )
    lines.extend(
        [
            "",
            "## Report Index",
            "",
            f"Generated index: `{report_index}`",
            "",
            "## Tracked Summary Docs",
            "",
            "- `docs/STEP_TAHOT_FINAL_GATE.md`",
            "- `docs/CLAIM_CATALOG.md`",
            "- `docs/BIBLE_CODE_DIGEST_AUDIT.md`",
            "- `docs/CRI_ELS_CRITIQUE_AUDIT.md`",
            "- `docs/THEWORDNOTES_ELS_AUDIT.md`",
            "- `docs/COSMIC_CODES_AUDIT.md`",
            "- `docs/MARK_TABATA_ISAIAH53_AUDIT.md`",
            "- `docs/FELCJO_RINGO_ALGORITHM_AUDIT.md`",
            "- `docs/AMANDASAURUS_BIBLECODE_PRIOR_ART_AUDIT.md`",
            "- `docs/BIBLE_CODES_ORG_AUDIT.md`",
            "- `docs/BIBLE_AND_SCIENCE_CODES_AUDIT.md`",
            "- `docs/RELIGIONS_WIKI_SCRIPTURAL_CODES_AUDIT.md`",
            "- `docs/GREEK_PATTERN_VERSION_SUMMARY.md`",
            "- `docs/GREEK_EXACT_CENTER_FINAL_GATE.md`",
            "- `docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_REPORT.md`",
            "- `docs/GREEK_EXPANDED_SURFACE_QUEUE.md`",
            "- `docs/GREEK_EXPANDED_SURFACE_TRIAGE.md`",
            "- `docs/GREEK_EXPANDED_SURFACE_LETTER_PATHS.md`",
            "- `docs/GREEK_EXPANDED_SURFACE_CONTROL_POOL.md`",
            "- `docs/GREEK_EXPANDED_SURFACE_CONTROL_EVALUATION.md`",
            "- `docs/GREEK_EXPANDED_SURFACE_AVAILABLE_CONTROL_POOL.md`",
            "- `docs/GREEK_EXPANDED_SURFACE_AVAILABLE_CONTROL_EVALUATION.md`",
            "- `docs/GREEK_EXPANDED_SURFACE_FOLLOWUP_REPORT.md`",
            "- `docs/GREEK_SURFACE_PROSPECTIVE_PREREGISTRATION.md`",
            "- `docs/GREEK_SURFACE_PROSPECTIVE_REPORT.md`",
            "- `docs/GREEK_SURFACE_PROSPECTIVE_QUEUE.md`",
            "- `docs/GREEK_SURFACE_PROSPECTIVE_TRIAGE.md`",
            "- `docs/GREEK_SURFACE_PROSPECTIVE_CONTROL_EVALUATION.md`",
            "- `docs/GREEK_SURFACE_PROSPECTIVE_LETTER_PATHS.md`",
            "- `docs/GREEK_SURFACE_LENGTH4_FOLLOWUP_TRIAGE.md`",
            "- `docs/GREEK_SURFACE_LENGTH4_CONTROL_POOL.md`",
            "- `docs/GREEK_SURFACE_LENGTH4_CONTROL_EVALUATION.md`",
            "- `docs/GREEK_SURFACE_LENGTH4_LETTER_PATHS.md`",
            "- `docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROLS.md`",
            "- `docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROL_POOL.md`",
            "- `docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROL_EVALUATION.md`",
            "- `docs/WRR_SOURCE_AUDIT.md`",
            "- `docs/WRR_REPLICATION_PLAN.md`",
            "- `docs/WRR_METHODOLOGY_GAPS.md`",
            "- `docs/WRR_CORRECTED_DISTANCE_NOTES.md`",
            "- `docs/WRR_CROSS_PAIR_GRID.md`",
            "- `docs/WRR_METHOD_STATUS.md`",
            "- `docs/WRR_LOCK_OPTIONS.md`",
            "- `docs/GREEK_SURFACE_PROSPECTIVE_CLAIM_STANDARD.md`",
            "- `docs/STUDY_LOCK_MANIFESTS.md`",
            "- `docs/PROSPECTIVE_STUDY_PREREGISTRATION_TEMPLATE.md`",
            "- `docs/PROSPECTIVE_TERM_AUDITS.md`",
            "- `docs/BROADER_SEARCH_FINDINGS.md`",
            "- `docs/HEBREW_MODERN_GEOPOLITICAL_VERSION_PRESENCE.md`",
            "- `docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_REVIEW.md`",
            "- `docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_FINDINGS.md`",
            "- `docs/HEBREW_MODERN_GEOPOLITICAL_PRESENCE_PREREGISTRATION.md`",
            "- `docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_REPORT.md`",
            "- `docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_FINDINGS.md`",
            "- `docs/HEBREW_SCREENING_CONTROLLED_REVIEW.md`",
            "- `docs/HEBREW_SCREENING_CONTROLLED_FINDINGS.md`",
            "- `docs/HEBREW_THEOLOGY_PROSPECTIVE_PREREGISTRATION.md`",
            "- `docs/HEBREW_THEOLOGY_PROSPECTIVE_REPORT.md`",
            "- `docs/HEBREW_THEOLOGY_PROSPECTIVE_FINDINGS.md`",
            "- `docs/HEBREW_THEOLOGY_ALL_CODES_COLLECTION.md`",
            "- `docs/HEBREW_THEOLOGY_ALL_CODES_TRIAGE.md`",
            "- `docs/HEBREW_SCREENING_ALL_CODES_COLLECTION.md`",
            "- `docs/HEBREW_SCREENING_ALL_CODES_TRIAGE.md`",
            "- `docs/GREEK_SCREENING_ALL_CODES_COLLECTION.md`",
            "- `docs/GREEK_SCREENING_ALL_CODES_TRIAGE.md`",
            "- `docs/ALL_CODES_FOLLOWUP_SELECTION.md`",
            "- `docs/ALL_CODES_FOLLOWUP_LETTER_PATHS.md`",
            "- `docs/ALL_CODES_FOLLOWUP_CONTEXT.md`",
            "- `docs/ALL_CODES_FOLLOWUP_EXTENSIONS.md`",
            "- `docs/ALL_CODES_COMPOUND_EXTENSION_CONTROLS.md`",
            "- `docs/ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_CONTROLS.md`",
            "- `docs/ALL_CODES_FOLLOWUP_REVIEW.md`",
            "- `docs/GOG_MAGOG_PAIR_PROSPECTIVE_PREREGISTRATION.md`",
            "- `docs/GOG_MAGOG_PAIR_PROSPECTIVE_REPORT.md`",
            "- `docs/CENTERED_OCCURRENCE_INDEX.md`",
            "- `docs/FINAL_REPORT_HIGHLIGHTS.md`",
            "- `docs/PROSPECTIVE_STUDY_READINESS.md`",
            "- `docs/PROSPECTIVE_STUDY_NEXT_LOCK.md`",
            "- `docs/CONSOLIDATED_FINDINGS.md`",
            "- `docs/FINAL_REPORT_OUTLINE.md`",
            "- `docs/FINAL_REPORT_DRAFT.md`",
            "- `docs/FINAL_REPORT.md`",
            "- `docs/APOCRYPHA_BRIDGE_STUDY.md`",
            "- `docs/APOCRYPHA_SOURCE_COVERAGE.md`",
            "- `docs/APOCRYPHA_BRIDGE_CANDIDATES.md`",
            "- `docs/APOCRYPHA_BRIDGE_CONTEXT.md`",
            "- `docs/APOCRYPHA_BRIDGE_CONTROLS.md`",
            "- `docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS.md`",
            "- `docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_50.md`",
            "- `docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_100.md`",
            "- `docs/APOCRYPHA_ONLY_COUNTS.md`",
            "- `docs/KJV_APOCRYPHA_ONLY_COUNTS.md`",
            "- `docs/KJV_APOCRYPHA_BRIDGE_CANDIDATES.md`",
            "- `docs/KJV_APOCRYPHA_BRIDGE_CONTEXT.md`",
            "- `docs/KJV_APOCRYPHA_BRIDGE_CONTROLS.md`",
            "- `docs/KJV_APOCRYPHA_BRIDGE_TERM_REVIEW.md`",
            "- `docs/KJV_APOCRYPHA_BRIDGE_TERM_SHUFFLED_CONTROLS_1000.md`",
            "- `docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_PREREGISTRATION.md`",
            "- `docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_CONTROLS_5000.md`",
            "- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_PREREGISTRATION.md`",
            "- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CANDIDATES.md`",
            "- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md`",
            "- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_CONTROLS.md`",
            "- `docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS.md`",
            "- `docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_50.md`",
            "- `docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_100.md`",
            "- `docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_250.md`",
            "- `protocols/kjv_apocrypha_bridge_term_review.toml`",
            "- `protocols/kjv_apocrypha_bridge_term_shuffled_controls_1000.toml`",
            "- `protocols/kjv_apocrypha_bridge_confirmatory_controls_5000.toml`",
            "- `protocols/kjv_apocrypha_bridge_prospective_controls_5000.toml`",
            "- `protocols/kjv_apocrypha_bridge_prospective_nonbible_controls.toml`",
            "- `docs/VERSION_DISTRIBUTION_INDEX.md`",
            "- `claims/claim_catalog.csv`",
            "",
            "## Next Formal Step",
            "",
            "Before moving from review candidates to claims, require independent",
            "replication or a new locked prospective design that survives both",
            "shuffled and non-Bible insertion controls. The fresh KJVA prospective",
            "bridge run is negative under both control families.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    *,
    commit: str,
    step_manifest: dict[str, Any],
    greek_gate_rows: list[dict[str, str]],
    greek_pattern_rows: list[dict[str, str]],
    doxa_rows: list[dict[str, str]],
    doxa_manifest: dict[str, Any],
    doxa_confirmatory_rows: list[dict[str, str]],
    doxa_confirmatory_manifest: dict[str, Any],
    surface_queue_summary_rows: list[dict[str, str]],
    surface_queue_pattern_rows: list[dict[str, str]],
    surface_queue_manifest: dict[str, Any],
    surface_triage_selected_rows: list[dict[str, str]],
    surface_triage_cohort_rows: list[dict[str, str]],
    surface_triage_manifest: dict[str, Any],
    surface_letter_path_rows: list[dict[str, str]],
    surface_letter_paths_manifest: dict[str, Any],
    surface_control_frequency_rows: list[dict[str, str]],
    surface_control_matched_rows: list[dict[str, str]],
    surface_control_manifest: dict[str, Any],
    surface_control_evaluation_rows: list[dict[str, str]],
    surface_control_evaluation_manifest: dict[str, Any],
    surface_available_control_evaluation_rows: list[dict[str, str]],
    surface_available_control_evaluation_manifest: dict[str, Any],
    surface_followup_report_manifest: dict[str, Any],
    surface_followup_protocol_manifest: dict[str, Any],
    length4_selected_rows: list[dict[str, str]],
    length4_cohort_rows: list[dict[str, str]],
    length4_control_evaluation_rows: list[dict[str, str]],
    length4_letter_path_rows: list[dict[str, str]],
    length4_protocol_manifest: dict[str, Any],
    length4_vocab_terms_manifest: dict[str, Any],
    length4_vocab_control_evaluation_rows: list[dict[str, str]],
    length4_vocab_protocol_manifest: dict[str, Any],
    wrr_protocol_manifest: dict[str, Any],
    wrr_source_manifest: dict[str, Any],
    wrr_text_source_rows: list[dict[str, str]],
    wrr_source_shapes_summary_rows: list[dict[str, str]],
    wrr_count_summary_rows: list[dict[str, str]],
    wrr_pair_audit_len_5_8_rows: list[dict[str, str]],
    wrr_pair_controls_len_5_8_rows: list[dict[str, str]],
    wrr_skip_caps_summary_rows: list[dict[str, str]],
    wrr_pair_table_reconciliation_rows: list[dict[str, str]],
    wrr_perturbation_summary_rows: list[dict[str, str]],
    wrr_cross_pair_recommended_permutation_rows: list[dict[str, str]],
    hebrew_theology_all_codes_triage_manifest: dict[str, Any],
    hebrew_screening_all_codes_triage_manifest: dict[str, Any],
    greek_screening_all_codes_triage_manifest: dict[str, Any],
    all_codes_followup_selection_manifest: dict[str, Any],
    all_codes_followup_letter_path_rows: list[dict[str, str]],
    all_codes_followup_letter_paths_manifest: dict[str, Any],
    all_codes_followup_context_rows: list[dict[str, str]],
    all_codes_followup_context_manifest: dict[str, Any],
    all_codes_followup_extension_rows: list[dict[str, str]],
    all_codes_followup_extensions_manifest: dict[str, Any],
    all_codes_compound_extension_control_rows: list[dict[str, str]],
    all_codes_compound_extension_controls_manifest: dict[str, Any],
    all_codes_compound_extension_confirmatory_rows: list[dict[str, str]],
    all_codes_compound_extension_confirmatory_manifest: dict[str, Any],
    all_codes_compound_extension_confirmatory_protocol_manifest: dict[str, Any],
    all_codes_followup_review_rows: list[dict[str, str]],
    all_codes_followup_review_manifest: dict[str, Any],
    centered_occurrence_presence_rows: list[dict[str, str]],
    centered_occurrence_manifest: dict[str, Any],
    kjva_apocrypha_bridge_confirmatory_rows: list[dict[str, str]],
    kjva_apocrypha_bridge_confirmatory_manifest: dict[str, Any],
    kjva_apocrypha_bridge_prospective_rows: list[dict[str, str]],
    kjva_apocrypha_bridge_prospective_manifest: dict[str, Any],
    kjva_apocrypha_bridge_prospective_nonbible_rows: list[dict[str, str]],
    kjva_apocrypha_bridge_prospective_nonbible_manifest: dict[str, Any],
    external_claim_counts_rows: list[dict[str, str]],
    external_claim_counts_manifest: dict[str, Any],
    external_claim_all_codes_rows: list[dict[str, str]],
    external_claim_all_codes_summary_manifest: dict[str, Any],
    external_claim_all_codes_triage_rows: list[dict[str, str]],
    external_claim_all_codes_triage_manifest: dict[str, Any],
    matrix_cluster_relation_control_rows: list[dict[str, str]],
    matrix_cluster_term_pair_control_rows: list[dict[str, str]],
    notable_passage_gap_passage_rows: list[dict[str, str]],
    notable_passage_gap_cross_source_rows: list[dict[str, str]],
    thematic_chapter_absence_passage_rows: list[dict[str, str]],
    thematic_chapter_absence_cross_source_rows: list[dict[str, str]],
    match_strata_summary_rows: list[dict[str, str]],
    boundary_alignment_summary_rows: list[dict[str, str]],
    chapter_position_bias_summary_rows: list[dict[str, str]],
    direction_asymmetry_summary_rows: list[dict[str, str]],
    canonical_first_summary_rows: list[dict[str, str]],
    cross_skip_summary_rows: list[dict[str, str]],
    review_flag_summary_rows: list[dict[str, str]],
    cohort_cluster_density_summary_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "build_real_report_run_summary",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "commit": commit,
        "inputs": {
            "step_tahot_manifest": str(args.step_tahot_manifest),
            "greek_gate_summary": str(args.greek_gate_summary),
            "greek_pattern_summary": str(args.greek_pattern_summary),
            "doxa_summary": str(args.doxa_summary),
            "doxa_protocol_manifest": str(args.doxa_protocol_manifest),
            "doxa_confirmatory_summary": str(args.doxa_confirmatory_summary),
            "doxa_confirmatory_protocol_manifest": str(
                args.doxa_confirmatory_protocol_manifest
            ),
            "surface_queue_summary": str(args.surface_queue_summary),
            "surface_queue_patterns": str(args.surface_queue_patterns),
            "surface_queue_protocol_manifest": str(args.surface_queue_protocol_manifest),
            "surface_triage_selected": str(args.surface_triage_selected),
            "surface_triage_cohort": str(args.surface_triage_cohort),
            "surface_triage_protocol_manifest": str(args.surface_triage_protocol_manifest),
            "surface_letter_paths_summary": str(args.surface_letter_paths_summary),
            "surface_letter_paths_protocol_manifest": str(args.surface_letter_paths_protocol_manifest),
            "surface_control_frequencies": str(args.surface_control_frequencies),
            "surface_control_matched": str(args.surface_control_matched),
            "surface_control_protocol_manifest": str(args.surface_control_protocol_manifest),
            "surface_control_evaluation": str(args.surface_control_evaluation),
            "surface_control_evaluation_manifest": str(args.surface_control_evaluation_manifest),
            "surface_available_control_evaluation": str(args.surface_available_control_evaluation),
            "surface_available_control_evaluation_manifest": str(args.surface_available_control_evaluation_manifest),
            "surface_followup_report_manifest": str(args.surface_followup_report_manifest),
            "surface_followup_protocol_manifest": str(args.surface_followup_protocol_manifest),
            "length4_selected": str(args.length4_selected),
            "length4_cohort": str(args.length4_cohort),
            "length4_control_evaluation": str(args.length4_control_evaluation),
            "length4_letter_paths": str(args.length4_letter_paths),
            "length4_protocol_manifest": str(args.length4_protocol_manifest),
            "length4_vocab_terms_manifest": str(args.length4_vocab_terms_manifest),
            "length4_vocab_control_evaluation": str(args.length4_vocab_control_evaluation),
            "length4_vocab_protocol_manifest": str(args.length4_vocab_protocol_manifest),
            "wrr_protocol_manifest": str(args.wrr_protocol_manifest),
            "wrr_source_manifest": str(args.wrr_source_manifest),
            "wrr_text_source": str(args.wrr_text_source),
            "wrr_source_shapes_summary": str(args.wrr_source_shapes_summary),
            "wrr_count_summary": str(args.wrr_count_summary),
            "wrr_pair_audit_len_5_8": str(args.wrr_pair_audit_len_5_8),
            "wrr_pair_controls_len_5_8": str(args.wrr_pair_controls_len_5_8),
            "wrr_skip_caps_summary": str(args.wrr_skip_caps_summary),
            "wrr_pair_table_reconciliation": str(args.wrr_pair_table_reconciliation),
            "wrr_perturbation_summary": str(args.wrr_perturbation_summary),
            "wrr_cross_pair_recommended_permutation_summary": str(
                args.wrr_cross_pair_recommended_permutation_summary
            ),
            "hebrew_theology_all_codes_triage_manifest": str(
                args.hebrew_theology_all_codes_triage_manifest
            ),
            "hebrew_screening_all_codes_triage_manifest": str(
                args.hebrew_screening_all_codes_triage_manifest
            ),
            "greek_screening_all_codes_triage_manifest": str(
                args.greek_screening_all_codes_triage_manifest
            ),
            "all_codes_followup_selection_manifest": str(
                args.all_codes_followup_selection_manifest
            ),
            "all_codes_followup_letter_paths_summary": str(
                args.all_codes_followup_letter_paths_summary
            ),
            "all_codes_followup_letter_paths_manifest": str(
                args.all_codes_followup_letter_paths_manifest
            ),
            "all_codes_followup_context_excerpts": str(
                args.all_codes_followup_context_excerpts
            ),
            "all_codes_followup_context_manifest": str(
                args.all_codes_followup_context_manifest
            ),
            "all_codes_followup_extensions_summary": str(
                args.all_codes_followup_extensions_summary
            ),
            "all_codes_followup_extensions_manifest": str(
                args.all_codes_followup_extensions_manifest
            ),
            "all_codes_compound_extension_controls_summary": str(
                args.all_codes_compound_extension_controls_summary
            ),
            "all_codes_compound_extension_controls_manifest": str(
                args.all_codes_compound_extension_controls_manifest
            ),
            "all_codes_compound_extension_confirmatory_summary": str(
                args.all_codes_compound_extension_confirmatory_summary
            ),
            "all_codes_compound_extension_confirmatory_manifest": str(
                args.all_codes_compound_extension_confirmatory_manifest
            ),
            "all_codes_compound_extension_confirmatory_protocol_manifest": str(
                args.all_codes_compound_extension_confirmatory_protocol_manifest
            ),
            "all_codes_followup_review_summary": str(
                args.all_codes_followup_review_summary
            ),
            "all_codes_followup_review_manifest": str(
                args.all_codes_followup_review_manifest
            ),
            "centered_occurrence_presence": str(args.centered_occurrence_presence),
            "centered_occurrence_manifest": str(args.centered_occurrence_manifest),
            "kjva_apocrypha_bridge_confirmatory_term_summary": str(
                args.kjva_apocrypha_bridge_confirmatory_term_summary
            ),
            "kjva_apocrypha_bridge_confirmatory_manifest": str(
                args.kjva_apocrypha_bridge_confirmatory_manifest
            ),
            "kjva_apocrypha_bridge_prospective_term_summary": str(
                args.kjva_apocrypha_bridge_prospective_term_summary
            ),
            "kjva_apocrypha_bridge_prospective_manifest": str(
                args.kjva_apocrypha_bridge_prospective_manifest
            ),
            "kjva_apocrypha_bridge_prospective_nonbible_summary": str(
                args.kjva_apocrypha_bridge_prospective_nonbible_summary
            ),
            "kjva_apocrypha_bridge_prospective_nonbible_manifest": str(
                args.kjva_apocrypha_bridge_prospective_nonbible_manifest
            ),
            "external_claim_counts_summary": str(args.external_claim_counts_summary),
            "external_claim_counts_manifest": str(args.external_claim_counts_manifest),
            "external_claim_all_codes_summary": str(args.external_claim_all_codes_summary),
            "external_claim_all_codes_summary_manifest": str(
                args.external_claim_all_codes_summary_manifest
            ),
            "external_claim_all_codes_triage": str(args.external_claim_all_codes_triage),
            "external_claim_all_codes_triage_manifest": str(
                args.external_claim_all_codes_triage_manifest
            ),
            "matrix_cluster_relation_control_summary": str(
                args.matrix_cluster_relation_control_summary
            ),
            "matrix_cluster_term_pair_control_summary": str(
                args.matrix_cluster_term_pair_control_summary
            ),
            "notable_passage_gap_passage_summary": str(
                args.notable_passage_gap_passage_summary
            ),
            "notable_passage_gap_cross_source_summary": str(
                args.notable_passage_gap_cross_source_summary
            ),
            "thematic_chapter_absence_passage_summary": str(
                args.thematic_chapter_absence_passage_summary
            ),
            "thematic_chapter_absence_cross_source_summary": str(
                args.thematic_chapter_absence_cross_source_summary
            ),
            "match_strata_summary": str(args.match_strata_summary),
            "boundary_alignment_summary": str(args.boundary_alignment_summary),
            "chapter_position_bias_summary": str(args.chapter_position_bias_summary),
            "direction_asymmetry_summary": str(args.direction_asymmetry_summary),
            "canonical_first_summary": str(args.canonical_first_summary),
            "cross_skip_summary": str(args.cross_skip_summary),
            "review_flag_summary": str(args.review_flag_summary),
            "cohort_cluster_density_summary": str(args.cohort_cluster_density_summary),
            "report_index": str(args.report_index),
        },
        "step_tahot": {
            "real_counts": step_manifest.get("real_counts", {}),
            "control_counts": step_manifest.get("control_counts", {}),
            "real_policy_counts": step_manifest.get("real_policy_counts", {}),
            "control_policy_counts": step_manifest.get("control_policy_counts", {}),
        },
        "greek_gate_rows": len(greek_gate_rows),
        "greek_pattern_rows": len(greek_pattern_rows),
        "doxa_rows": len(doxa_rows),
        "doxa_protocol_status": doxa_manifest.get("status", ""),
        "doxa_confirmatory_rows": len(doxa_confirmatory_rows),
        "doxa_confirmatory_protocol_status": doxa_confirmatory_manifest.get("status", ""),
        "surface_queue_summary_rows": len(surface_queue_summary_rows),
        "surface_queue_pattern_rows": len(surface_queue_pattern_rows),
        "surface_queue_protocol_status": surface_queue_manifest.get("status", ""),
        "surface_triage_selected_rows": len(surface_triage_selected_rows),
        "surface_triage_cohort_rows": len(surface_triage_cohort_rows),
        "surface_triage_protocol_status": surface_triage_manifest.get("status", ""),
        "surface_letter_path_rows": len(surface_letter_path_rows),
        "surface_letter_paths_protocol_status": surface_letter_paths_manifest.get("status", ""),
        "surface_control_frequency_rows": len(surface_control_frequency_rows),
        "surface_control_matched_rows": len(surface_control_matched_rows),
        "surface_control_protocol_status": surface_control_manifest.get("status", ""),
        "surface_control_evaluation_rows": len(surface_control_evaluation_rows),
        "surface_control_evaluation_protocol_status": surface_control_evaluation_manifest.get("status", ""),
        "surface_available_control_evaluation_rows": len(surface_available_control_evaluation_rows),
        "surface_available_control_evaluation_protocol_status": surface_available_control_evaluation_manifest.get("status", ""),
        "surface_followup_status": surface_followup_report_manifest.get("status", ""),
        "surface_followup_selected_rows": surface_followup_report_manifest.get("selected_rows", 0),
        "surface_followup_path_rows": surface_followup_report_manifest.get("path_rows", 0),
        "surface_followup_control_rows": surface_followup_report_manifest.get("control_rows", 0),
        "surface_followup_protocol_status": surface_followup_protocol_manifest.get("status", ""),
        "length4_selected_rows": len(length4_selected_rows),
        "length4_selected_terms": len({row["term_id"] for row in length4_selected_rows}),
        "length4_cohort_rows": len(length4_cohort_rows),
        "length4_control_evaluation_rows": len(length4_control_evaluation_rows),
        "length4_letter_path_rows": len(length4_letter_path_rows),
        "length4_protocol_status": length4_protocol_manifest.get("status", ""),
        "length4_vocab_generated_controls": length4_vocab_terms_manifest.get("control_rows", 0),
        "length4_vocab_control_evaluation_rows": len(length4_vocab_control_evaluation_rows),
        "length4_vocab_protocol_status": length4_vocab_protocol_manifest.get("status", ""),
        "wrr_protocol_status": wrr_protocol_manifest.get("status", ""),
        "wrr_downloads": len(wrr_source_manifest.get("downloads", [])),
        "wrr_text_source_rows": len(wrr_text_source_rows),
        "wrr_source_shapes_summary_rows": len(wrr_source_shapes_summary_rows),
        "wrr_count_summary_rows": len(wrr_count_summary_rows),
        "wrr_pair_audit_len_5_8_rows": len(wrr_pair_audit_len_5_8_rows),
        "wrr_pair_controls_len_5_8_rows": len(wrr_pair_controls_len_5_8_rows),
        "wrr_skip_caps_summary_rows": len(wrr_skip_caps_summary_rows),
        "wrr_pair_table_reconciliation_rows": len(wrr_pair_table_reconciliation_rows),
        "wrr_perturbation_summary_rows": len(wrr_perturbation_summary_rows),
        "wrr_cross_pair_recommended_permutation_rows": len(
            wrr_cross_pair_recommended_permutation_rows
        ),
        "hebrew_theology_all_codes_triage_rows": hebrew_theology_all_codes_triage_manifest.get(
            "queue_rows", 0
        ),
        "hebrew_screening_all_codes_triage_rows": hebrew_screening_all_codes_triage_manifest.get(
            "queue_rows", 0
        ),
        "greek_screening_all_codes_triage_rows": greek_screening_all_codes_triage_manifest.get(
            "queue_rows", 0
        ),
        "all_codes_followup_selection_rows": all_codes_followup_selection_manifest.get(
            "selected_rows", 0
        ),
        "all_codes_followup_letter_path_rows": len(all_codes_followup_letter_path_rows),
        "all_codes_followup_letter_paths_manifest_rows": all_codes_followup_letter_paths_manifest.get(
            "summary_rows", 0
        ),
        "all_codes_followup_letter_rows": all_codes_followup_letter_paths_manifest.get(
            "letter_rows", 0
        ),
        "all_codes_followup_letter_path_mismatches": all_codes_followup_letter_paths_manifest.get(
            "mismatches", 0
        ),
        "all_codes_followup_context_rows": len(all_codes_followup_context_rows),
        "all_codes_followup_context_excerpt_rows": all_codes_followup_context_manifest.get(
            "excerpt_rows", 0
        ),
        "all_codes_followup_context_center_contains_rows": all_codes_followup_context_manifest.get(
            "center_contains_normalized_term_rows", 0
        ),
        "all_codes_followup_context_span_contains_rows": all_codes_followup_context_manifest.get(
            "span_contains_normalized_term_rows", 0
        ),
        "all_codes_followup_extension_summary_rows": len(all_codes_followup_extension_rows),
        "all_codes_followup_extension_rows": all_codes_followup_extensions_manifest.get(
            "extension_rows", 0
        ),
        "all_codes_followup_compound_extension_rows": all_codes_followup_extensions_manifest.get(
            "compound_extension_rows", 0
        ),
        "all_codes_followup_extension_selected_rows": all_codes_followup_extensions_manifest.get(
            "selected_rows_with_extensions", 0
        ),
        "all_codes_followup_selected_rows_with_compound_extensions": all_codes_followup_extensions_manifest.get(
            "selected_rows_with_compound_extensions", 0
        ),
        "all_codes_followup_extension_max_length": all_codes_followup_extensions_manifest.get(
            "max_extension_length", 0
        ),
        "all_codes_compound_extension_control_rows": len(
            all_codes_compound_extension_control_rows
        ),
        "all_codes_compound_extension_control_targets": all_codes_compound_extension_controls_manifest.get(
            "targets", 0
        ),
        "all_codes_compound_extension_control_term_samples": all_codes_compound_extension_controls_manifest.get(
            "term_control_samples", 0
        ),
        "all_codes_compound_extension_control_random_samples": all_codes_compound_extension_controls_manifest.get(
            "random_control_samples", 0
        ),
        "all_codes_compound_extension_confirmatory_rows": len(
            all_codes_compound_extension_confirmatory_rows
        ),
        "all_codes_compound_extension_confirmatory_targets": all_codes_compound_extension_confirmatory_manifest.get(
            "targets", 0
        ),
        "all_codes_compound_extension_confirmatory_term_samples": all_codes_compound_extension_confirmatory_manifest.get(
            "term_control_samples", 0
        ),
        "all_codes_compound_extension_confirmatory_random_samples": all_codes_compound_extension_confirmatory_manifest.get(
            "random_control_samples", 0
        ),
        "all_codes_compound_extension_confirmatory_protocol_status": all_codes_compound_extension_confirmatory_protocol_manifest.get(
            "status", ""
        ),
        "all_codes_followup_review_rows": len(all_codes_followup_review_rows),
        "all_codes_followup_review_summary_rows": all_codes_followup_review_manifest.get(
            "summary_rows", 0
        ),
        "all_codes_followup_review_status_counts": all_codes_followup_review_manifest.get(
            "review_status_counts", {}
        ),
        "centered_occurrence_presence_rows": len(centered_occurrence_presence_rows),
        "centered_occurrence_occurrence_rows": centered_occurrence_manifest.get("rows", 0),
        "centered_occurrence_bible_presence_rows": sum(
            row.get("corpus_class") == "bible" for row in centered_occurrence_presence_rows
        ),
        "centered_occurrence_control_presence_rows": sum(
            row.get("corpus_class") == "control" for row in centered_occurrence_presence_rows
        ),
        "centered_occurrence_type_counts": centered_occurrence_manifest.get(
            "summary_type_counts", {}
        ),
        "kjva_apocrypha_bridge_confirmatory_rows": len(
            kjva_apocrypha_bridge_confirmatory_rows
        ),
        "kjva_apocrypha_bridge_confirmatory_samples": kjva_apocrypha_bridge_confirmatory_manifest.get(
            "samples", 0
        ),
        "kjva_apocrypha_bridge_confirmatory_terms_above_all_samples": kjva_apocrypha_bridge_confirmatory_manifest.get(
            "terms_observed_gt_sample_max", 0
        ),
        "kjva_apocrypha_bridge_confirmatory_terms_q_le_0_05": kjva_apocrypha_bridge_confirmatory_manifest.get(
            "terms_q_le_0_05", 0
        ),
        "kjva_apocrypha_bridge_prospective_rows": len(
            kjva_apocrypha_bridge_prospective_rows
        ),
        "kjva_apocrypha_bridge_prospective_samples": kjva_apocrypha_bridge_prospective_manifest.get(
            "samples", 0
        ),
        "kjva_apocrypha_bridge_prospective_terms_above_all_samples": kjva_apocrypha_bridge_prospective_manifest.get(
            "terms_observed_gt_sample_max", 0
        ),
        "kjva_apocrypha_bridge_prospective_terms_q_le_0_05": kjva_apocrypha_bridge_prospective_manifest.get(
            "terms_q_le_0_05", 0
        ),
        "kjva_apocrypha_bridge_prospective_nonbible_controls": len(
            kjva_apocrypha_bridge_prospective_nonbible_rows
        ),
        "kjva_apocrypha_bridge_prospective_nonbible_controls_ge_observed": sum(
            int_value(row, "bridge_rows") >= 1
            for row in kjva_apocrypha_bridge_prospective_nonbible_rows
        ),
        "external_claim_count_summary_rows": len(external_claim_counts_rows),
        "external_claim_count_term_sets": len(
            {row.get("term_set", "") for row in external_claim_counts_rows}
        ),
        "external_claim_count_corpora": len(
            {row.get("corpus", "") for row in external_claim_counts_rows}
        ),
        "external_claim_count_total_hits": sum(
            int_value(row, "total_hits") for row in external_claim_counts_rows
        ),
        "external_claim_count_manifest_rows": external_claim_counts_manifest.get("rows", 0),
        "external_claim_all_codes_summary_rows": len(external_claim_all_codes_rows),
        "external_claim_all_codes_hit_rows": external_claim_all_codes_summary_manifest.get(
            "aggregates", {}
        ).get("hit_rows", 0),
        "external_claim_all_codes_context_hits": external_claim_all_codes_summary_manifest.get(
            "aggregates", {}
        ).get("context_hits", 0),
        "external_claim_all_codes_triage_rows": len(external_claim_all_codes_triage_rows),
        "external_claim_all_codes_triage_bucket_counts": external_claim_all_codes_triage_manifest.get(
            "bucket_counts", {}
        ),
        "matrix_cluster_relation_control_rows": len(matrix_cluster_relation_control_rows),
        "matrix_cluster_term_pair_control_rows": len(matrix_cluster_term_pair_control_rows),
        "notable_passage_gap_passage_rows": len(notable_passage_gap_passage_rows),
        "notable_passage_gap_cross_source_rows": len(notable_passage_gap_cross_source_rows),
        "thematic_chapter_absence_passage_rows": len(thematic_chapter_absence_passage_rows),
        "thematic_chapter_absence_cross_source_rows": len(
            thematic_chapter_absence_cross_source_rows
        ),
        "match_strata_summary_rows": len(match_strata_summary_rows),
        "boundary_alignment_summary_rows": len(boundary_alignment_summary_rows),
        "chapter_position_bias_summary_rows": len(chapter_position_bias_summary_rows),
        "direction_asymmetry_summary_rows": len(direction_asymmetry_summary_rows),
        "canonical_first_summary_rows": len(canonical_first_summary_rows),
        "cross_skip_summary_rows": len(cross_skip_summary_rows),
        "review_flag_summary_rows": len(review_flag_summary_rows),
        "cohort_cluster_density_summary_rows": len(cohort_cluster_density_summary_rows),
        "outputs": {
            "summary": str(args.summary_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def all_codes_triage_section(
    hebrew_theology_manifest: dict[str, Any],
    hebrew_screening_manifest: dict[str, Any],
    greek_screening_manifest: dict[str, Any],
    selection_manifest: dict[str, Any],
    letter_path_rows: list[dict[str, str]],
    letter_paths_manifest: dict[str, Any],
    context_rows: list[dict[str, str]],
    context_manifest: dict[str, Any],
    extension_rows: list[dict[str, str]],
    extensions_manifest: dict[str, Any],
    compound_control_rows: list[dict[str, str]],
    compound_controls_manifest: dict[str, Any],
    compound_confirmatory_rows: list[dict[str, str]],
    compound_confirmatory_manifest: dict[str, Any],
    compound_confirmatory_protocol_manifest: dict[str, Any],
    review_rows: list[dict[str, str]],
    review_manifest: dict[str, Any],
) -> list[str]:
    term_control_samples = int_value(compound_controls_manifest, "term_control_samples")
    random_control_samples = int_value(compound_controls_manifest, "random_control_samples")
    confirmatory_term_samples = int_value(
        compound_confirmatory_manifest,
        "term_control_samples",
    )
    confirmatory_random_samples = int_value(
        compound_confirmatory_manifest,
        "random_control_samples",
    )
    rows = [
        ("Hebrew theology", hebrew_theology_manifest),
        ("Hebrew screening", hebrew_screening_manifest),
        ("Greek screening", greek_screening_manifest),
    ]
    lines = [
        "",
        "## Relaxed All-Codes Triage",
        "",
        "These queues keep hidden-path-only rows visible while ranking same-center-word",
        "and related surface-context rows first for manual review.",
        "",
        "| Queue | Raw rows scanned | Queue rows | Selected keys | Bucket counts |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for label, manifest in rows:
        bucket_counts = manifest.get("bucket_counts", {})
        bucket_summary = ", ".join(
            f"{bucket}:{count}" for bucket, count in sorted(bucket_counts.items())
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    label,
                    f"{int_value(manifest, 'scanned_rows'):,}",
                    f"{int_value(manifest, 'queue_rows'):,}",
                    f"{int_value(manifest, 'selected_keys'):,}",
                    bucket_summary,
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Follow-up selection:",
            "",
            f"- selected rows: {int_value(selection_manifest, 'selected_rows'):,}",
            f"- source queue rows considered: {int_value(selection_manifest, 'queue_rows'):,}",
            f"- selected by queue: `{selection_manifest.get('selected_by_queue', {})}`",
            "",
            "Letter-path audit:",
            "",
            f"- path summary rows: {len(letter_path_rows):,}",
            f"- letter rows: {int_value(letter_paths_manifest, 'letter_rows'):,}",
            f"- sequence mismatches: {int_value(letter_paths_manifest, 'mismatches'):,}",
            f"- path rows by corpus: `{letter_paths_manifest.get('summary_by_corpus', {})}`",
            "",
            "Context excerpts:",
            "",
            f"- excerpt rows: {len(context_rows):,}",
            f"- center rows containing normalized hidden term: {int_value(context_manifest, 'center_contains_normalized_term_rows'):,}",
            f"- span rows containing normalized hidden term: {int_value(context_manifest, 'span_contains_normalized_term_rows'):,}",
            "",
            "Same-skip extension audit:",
            "",
            f"- selected rows with extensions: {int_value(extensions_manifest, 'selected_rows_with_extensions'):,}",
            f"- extension rows: {int_value(extensions_manifest, 'extension_rows'):,}",
            f"- selected rows with compound extensions: {int_value(extensions_manifest, 'selected_rows_with_compound_extensions'):,}",
            f"- compound extension rows containing hidden term: {int_value(extensions_manifest, 'compound_extension_rows'):,}",
            f"- max extension length: {int_value(extensions_manifest, 'max_extension_length'):,}",
            f"- extension rows by type: `{extensions_manifest.get('extension_rows_by_type', {})}`",
            f"- summary rows: {len(extension_rows):,}",
            "",
            "Compound-extension paired controls:",
            "",
            f"- target rows: {len(compound_control_rows):,}",
            f"- deduped targets: {int_value(compound_controls_manifest, 'targets'):,}",
            f"- term controls per target: {int_value(compound_controls_manifest, 'term_control_samples'):,}",
            f"- random controls per target: {int_value(compound_controls_manifest, 'random_control_samples'):,}",
            f"- q band counts: `{dict(Counter(row['extension_band'] for row in compound_control_rows))}`",
            f"- all-control q band counts: `{dict(Counter(row.get('all_controls_band', '') for row in compound_control_rows))}`",
            f"- read: post-screen flags only; empirical p-values still have a {term_control_samples}/{random_control_samples} control-sample floor.",
            "",
            "Compound-extension confirmatory controls:",
            "",
            f"- target rows: {len(compound_confirmatory_rows):,}",
            f"- deduped targets: {int_value(compound_confirmatory_manifest, 'targets'):,}",
            f"- term controls per target: {confirmatory_term_samples:,}",
            f"- random controls per target: {confirmatory_random_samples:,}",
            f"- protocol status: `{compound_confirmatory_protocol_manifest.get('status', '')}`",
            f"- all-control q band counts: `{dict(Counter(row.get('all_controls_band', '') for row in compound_confirmatory_rows))}`",
            f"- conservative all-control q range: {q_range(compound_confirmatory_rows, 'all_controls_max_q')}.",
            "- read: locked post-discovery confirmatory review candidate, not a claim.",
            "",
            "Manual-review packet:",
            "",
            f"- review rows: {len(review_rows):,}",
            f"- strongest same-surface-word rows: {review_status_count(review_manifest, 'strongest_manual_review'):,}",
            f"- hidden-path-only review rows: {review_status_count(review_manifest, 'hidden_path_review'):,}",
            f"- review status counts: `{review_manifest.get('review_status_counts', {})}`",
            "",
            "Current read: these are review queues. They choose manual follow-up",
            "rows; the compact selection, letter-path/context/extension audits, and review packet are",
            "work queues and do not promote rows into claims.",
        ]
    )
    return lines


def review_status_count(manifest: dict[str, Any], status: str) -> int:
    counts = manifest.get("review_status_counts", {})
    try:
        return int(counts.get(status, 0))
    except (TypeError, ValueError):
        return 0


def display_overlap_key(value: str) -> str:
    parts = value.split("|")
    if len(parts) < 6:
        return md_cell(display_term(value))
    term, skip, direction, extension_type, extended, sequence = parts[:6]
    return md_cell(
        "; ".join(
            [
                f"term {display_term(term)}",
                f"skip `{skip}`",
                f"direction `{direction}`",
                f"extension `{extension_type}`",
                f"extended {display_term(extended)}",
                f"sequence {display_term(sequence)}",
            ]
        )
    )


def centered_occurrence_section(
    presence_rows: list[dict[str, str]],
    manifest: dict[str, Any],
) -> list[str]:
    bible_rows = [row for row in presence_rows if row.get("corpus_class") == "bible"]
    control_rows = [row for row in presence_rows if row.get("corpus_class") == "control"]
    source_counts = Counter(row.get("source_family", "") for row in presence_rows)
    type_counts = Counter(row.get("occurrence_type", "") for row in presence_rows)
    top_rows = sorted(
        bible_rows,
        key=lambda row: (
            int_value(row, "summary_rank"),
            row.get("normalized_term", ""),
            row.get("center_ref", ""),
        ),
    )
    lines = [
        "",
        "## Centered Occurrence Index",
        "",
        "This is the occurrence-first layer. It answers whether a hidden word or",
        "phrase is centered on itself, centered on a related surface word, or tied",
        "to related surface context. Frequency and controls are reported beside the",
        "occurrence, but they do not erase the fact that the occurrence exists.",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Presence rows | {len(presence_rows):,} |",
        f"| Bible presence rows | {len(bible_rows):,} |",
        f"| Control presence rows | {len(control_rows):,} |",
        f"| Raw occurrence rows | {int_value(manifest, 'rows'):,} |",
        "",
        "| Occurrence type | Presence rows |",
        "| --- | ---: |",
    ]
    for label, count in sorted(type_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{label}` | {count:,} |")
    lines.extend(["", "| Source family | Presence rows |", "| --- | ---: |"])
    for label, count in sorted(source_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{label}` | {count:,} |")
    lines.extend(
        [
            "",
            "Top Bible presence rows:",
            "",
            "| Rank | Type | Source | Corpora | Term | Center | Occurrence rows | Total paths | Frequency read |",
            "| ---: | --- | --- | --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in top_rows[:12]:
        lines.append(
            "| "
            + " | ".join(
                [
                    row.get("summary_rank", ""),
                    f"`{row.get('occurrence_type', '')}`",
                    f"`{row.get('source_family', '')}`",
                    md_cell(row.get("corpora", "")),
                    display_term(
                        row.get("normalized_term", ""),
                        english=row.get("concept", ""),
                    ),
                    md_cell(
                        f"{row.get('center_ref', '')} "
                        f"{display_term(row.get('center_word', ''))}"
                    ),
                    f"{int_value(row, 'occurrence_rows'):,}",
                    f"{int_value(row, 'total_paths'):,}",
                    md_cell(row.get("frequency_reads", "")),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Current read: this section lists occurrences, not claims. The `Gog` row",
            "at Rev 20:8 is present across the compared Greek NT source labels as a",
            "centered-self occurrence in the Gog/Magog verse. Its short length still",
            "requires frequency caution, so the final report should state both facts.",
        ]
    )
    return lines


def kjva_apocrypha_bridge_confirmatory_section(
    rows: list[dict[str, str]],
    manifest: dict[str, Any],
) -> list[str]:
    rows_above_all = [row for row in rows if row.get("observed_gt_sample_max") == "True"]
    rows_q_le_01 = [
        row for row in rows if row.get("q_ge") and float(row.get("q_ge", "1")) <= 0.01
    ]
    top_rows = sorted(
        rows,
        key=lambda row: (
            float(row.get("q_ge", "1")),
            -int_value(row, "observed_minus_sample_max"),
            row.get("normalized_term", ""),
        ),
    )
    lines = [
        "",
        "## KJVA Apocrypha Bridge Confirmatory Controls",
        "",
        "This is a locked post-screen follow-up over the 15 KJVA bridge terms",
        "selected from the 1000-sample term-level shuffled-control pass. It is",
        "confirmatory calibration of a screened candidate set, not original",
        "prospective discovery.",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Terms reviewed | {len(rows):,} |",
        f"| Shuffled samples | {int_value(manifest, 'samples'):,} |",
        f"| Terms with q_ge <= 0.01 | {len(rows_q_le_01):,} |",
        f"| Terms above every shuffled sample | {len(rows_above_all):,} |",
        f"| Corpus letters | {int_value(manifest, 'corpus_letters'):,} |",
        "",
        "| Rank | Term | Observed | Shuffled max | p_ge | q_ge | Delta |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for index, row in enumerate(top_rows[:10], start=1):
        lines.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    display_term(row.get("normalized_term", "")),
                    f"{int_value(row, 'observed_bridge_rows'):,}",
                    f"{int_value(row, 'sample_max'):,}",
                    row.get("p_ge", ""),
                    row.get("q_ge", ""),
                    f"{int_value(row, 'observed_minus_sample_max'):,}",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Current read: all registered confirmatory terms pass BH `q_ge <= 0.01`,",
            "and three terms exceed every shuffled sample. This raises follow-up",
            "priority for KJVA bridge rows, but the row family remains post-screen",
            "and should not be promoted as a claim without successful prospective",
            "replication and non-Bible insertion controls.",
        ]
    )
    return lines


def kjva_apocrypha_bridge_prospective_section(
    rows: list[dict[str, str]],
    manifest: dict[str, Any],
    nonbible_rows: list[dict[str, str]],
) -> list[str]:
    rows_above_all = [row for row in rows if row.get("observed_gt_sample_max") == "True"]
    rows_q_le_01 = [
        row for row in rows if row.get("q_ge") and float(row.get("q_ge", "1")) <= 0.01
    ]
    rows_q_le_05 = [
        row for row in rows if row.get("q_ge") and float(row.get("q_ge", "1")) <= 0.05
    ]
    top_rows = sorted(
        rows,
        key=lambda row: (
            float(row.get("q_ge", "1")),
            -int_value(row, "observed_bridge_rows"),
            row.get("normalized_term", ""),
        ),
    )
    observed_total = max((int_value(row, "observed_bridge_rows") for row in rows), default=0)
    nonbible_max = max((int_value(row, "bridge_rows") for row in nonbible_rows), default=0)
    nonbible_max_labels = [
        row.get("control_label", "")
        for row in nonbible_rows
        if int_value(row, "bridge_rows") == nonbible_max
    ]
    nonbible_ge_observed = sum(
        int_value(row, "bridge_rows") >= observed_total for row in nonbible_rows
    )
    nonbible_max_display = (
        f"{nonbible_max:,} ({', '.join(label for label in nonbible_max_labels if label)})"
        if nonbible_rows
        else "0"
    )
    lines = [
        "",
        "## KJVA Apocrypha Bridge Prospective Controls",
        "",
        "This is the fresh prospective KJVA bridge run over 7 fixed",
        "apocrypha/deuterocanon proper names. The observed scan found one bridge",
        "row, for `tobit`, and the 5000-sample shuffled-insertion control did not",
        "produce a prospective review candidate. Secondary non-Bible insertion",
        "controls also do not support claim language: one same-length replacement",
        "block matched the observed total with one `tobit` bridge row.",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Registered terms reviewed | {len(rows):,} |",
        f"| Observed bridge rows | {observed_total:,} |",
        f"| Shuffled samples | {int_value(manifest, 'samples'):,} |",
        f"| Terms with q_ge <= 0.01 | {len(rows_q_le_01):,} |",
        f"| Terms with q_ge <= 0.05 | {len(rows_q_le_05):,} |",
        f"| Terms above every shuffled sample | {len(rows_above_all):,} |",
        f"| Non-Bible controls >= observed total | {nonbible_ge_observed:,} / {len(nonbible_rows):,} |",
        f"| Max non-Bible control rows | {nonbible_max_display} |",
        f"| Corpus letters | {int_value(manifest, 'corpus_letters'):,} |",
        "",
        "| Rank | Term | Observed | Shuffled max | p_ge | q_ge | Delta |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for index, row in enumerate(top_rows[:10], start=1):
        lines.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    display_term(row.get("normalized_term", "")),
                    f"{int_value(row, 'observed_bridge_rows'):,}",
                    f"{int_value(row, 'sample_max'):,}",
                    row.get("p_ge", ""),
                    row.get("q_ge", ""),
                    f"{int_value(row, 'observed_minus_sample_max'):,}",
                ]
            )
            + " |"
        )
    return lines


def external_claim_source_section(
    count_rows: list[dict[str, str]],
    count_manifest: dict[str, Any],
    all_codes_rows: list[dict[str, str]],
    all_codes_summary_manifest: dict[str, Any],
    triage_rows: list[dict[str, str]],
    triage_manifest: dict[str, Any],
) -> list[str]:
    term_sets = {row.get("term_set", "") for row in count_rows if row.get("term_set")}
    corpora = {row.get("corpus", "") for row in count_rows if row.get("corpus")}
    total_hits = sum(int_value(row, "total_hits") for row in count_rows)
    zero_rows = sum(int_value(row, "zero_rows") for row in count_rows)
    top_count_rows = sorted(
        count_rows,
        key=lambda row: (-int_value(row, "total_hits"), row.get("term_set", "")),
    )
    aggregates = all_codes_summary_manifest.get("aggregates", {})
    context_counts = aggregates.get("context_counts", {})
    bucket_counts = triage_manifest.get("bucket_counts", {})
    top_triage_rows = sorted(
        triage_rows,
        key=lambda row: (
            int_value(row, "overall_rank"),
            int_value(row, "bucket_rank"),
            row.get("term_id", ""),
        ),
    )
    lines = [
        "",
        "## External Claim Source Runs",
        "",
        "These runs bring the audited external-source term lists into the same",
        "count and relaxed all-codes pipeline used elsewhere in the project. They",
        "are source-derived screening and collection outputs; reproducing any",
        "external claim still requires that source's exact spelling, skip",
        "geometry, matrix width, proximity metric, and controls.",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Term-set/corpus summary rows | {len(count_rows):,} |",
        f"| Term sets | {len(term_sets):,} |",
        f"| Corpora | {len(corpora):,} |",
        f"| Skip 2..100 count hits | {total_hits:,} |",
        f"| Zero corpus-term rows | {zero_rows:,} |",
        f"| All-codes summary rows | {len(all_codes_rows):,} |",
        f"| Hidden-path rows retained | {int_value(aggregates, 'hit_rows'):,} |",
        f"| Any surface-context hits | {int_value(aggregates, 'context_hits'):,} |",
        f"| Center word contains same term | {int_value(aggregates, 'center_word_exact_hits'):,} |",
        f"| Center word contains related term | {int_value(aggregates, 'center_word_related_hits'):,} |",
        f"| Triage queue rows | {len(triage_rows):,} |",
        "",
        "Top count-summary rows:",
        "",
        "| Term set | Corpus | Counted | Zero | Hits | Max row |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in top_count_rows[:8]:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(row.get("term_set", "")),
                    md_cell(row.get("corpus", "")),
                    f"{int_value(row, 'counted_rows'):,}",
                    f"{int_value(row, 'zero_rows'):,}",
                    f"{int_value(row, 'total_hits'):,}",
                    md_cell(
                        f"{row.get('max_term_id', '')} "
                        f"{display_term(row.get('max_normalized_term', ''), english=row.get('max_concept', ''))} "
                        f"({int_value(row, 'max_hit_count'):,})"
                    ),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "All-codes context labels:",
            "",
            "| Label | Rows |",
            "| --- | ---: |",
        ]
    )
    for label, count in sorted(context_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{label}` | {count:,} |")
    lines.extend(
        [
            "",
            "Triage bucket counts:",
            "",
            "| Bucket | Queue rows |",
            "| --- | ---: |",
        ]
    )
    for label, count in sorted(bucket_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{label}` | {count:,} |")
    lines.extend(
        [
            "",
            "Top triage rows:",
            "",
            "| Rank | Bucket | Scope | Term | Center | Best context |",
            "| ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for row in top_triage_rows[:10]:
        lines.append(
            "| "
            + " | ".join(
                [
                    row.get("overall_rank", ""),
                    f"`{row.get('bucket', '')}`",
                    f"`{row.get('presence_scope', '')}`",
                    md_cell(
                        f"{row.get('term_id', '')} "
                        f"{display_term(row.get('normalized_term', ''), english=row.get('concept', ''))}"
                    ),
                    md_cell(
                        f"{row.get('center_ref', '')} "
                        f"{display_term(row.get('center_normalized_word', ''))}"
                    ),
                    f"`{row.get('best_context', '')}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            f"Count manifest raw rows: {int_value(count_manifest, 'rows'):,}.",
            "Current read: this broad source-audit lane is useful for discovering",
            "what is present in which editions and controls. It should not be read",
            "as claim reproduction without the source's original geometry and a",
            "locked control design.",
            "",
            "Source artifacts: `docs/EXTERNAL_CLAIM_SOURCE_COUNTS.md`,",
            "`docs/EXTERNAL_CLAIM_SOURCE_ALL_CODES_COLLECTION.md`,",
            "`docs/EXTERNAL_CLAIM_SOURCE_ALL_CODES_TRIAGE.md`, and",
            "`docs/EXTERNAL_CLAIM_SOURCE_FINDINGS.md`.",
        ]
    )
    return lines


def expanded_strata_summary_section(
    match_strata_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    chapter_rows: list[dict[str, str]],
    direction_rows: list[dict[str, str]],
    canonical_rows: list[dict[str, str]],
    cross_skip_rows: list[dict[str, str]],
    review_flag_rows: list[dict[str, str]],
    cohort_cluster_rows: list[dict[str, str]],
) -> list[str]:
    top_strata = sorted(
        match_strata_rows,
        key=lambda row: (-int_value(row, "rows"), row.get("stratum", "")),
    )
    lines = [
        "",
        "## Expanded Post-Search Strata",
        "",
        "These summaries annotate already retained occurrence rows. They do not run",
        "new ELS searches and do not promote rows into claims. Their purpose is to",
        "preserve extra review dimensions: boundary alignment, direction asymmetry,",
        "canonical-first status, cross-skip overlap, meaningful skips, and rarity",
        "flags.",
        "",
        "Top strata from the match-strata index:",
        "",
        "| Stratum | Rows |",
        "| --- | ---: |",
    ]
    for row in top_strata[:12]:
        lines.append(
            f"| `{row.get('stratum', '')}` | {int_value(row, 'rows'):,} |"
        )

    lines.extend(
        [
            "",
            "Post-search summary counts:",
            "",
            "| Summary | Key read |",
            "| --- | --- |",
            f"| Boundary alignment | {bucket_count_text(boundary_rows, 'bucket', 'rows')} |",
            f"| Chapter position | {bucket_count_text(chapter_rows, 'bucket', 'rows')} |",
            f"| Direction asymmetry | {bucket_count_text(direction_rows, 'bucket', 'term_groups')} |",
            f"| Canonical first | {bucket_count_text(canonical_rows, 'bucket', 'rows')} |",
            f"| Cross-skip pairs | {bucket_count_text(cross_skip_rows, 'bucket', 'rows')} |",
            f"| Review flags | {bucket_count_text(review_flag_rows, 'flag_type', 'flag_rows')} |",
            f"| Cohort windows | {cohort_window_text(cohort_cluster_rows)} |",
            "",
            "Current read: these are review-prioritization fields. A boundary hit,",
            "canonical-first hit, meaningful skip, or cross-skip pair is worth",
            "recording, but claim language still requires a narrower locked study and",
            "matched controls for that exact family.",
            "",
            "Source artifacts: `docs/MATCH_STRATA_INDEX.md`,",
            "`docs/BOUNDARY_ALIGNMENT.md`, `docs/CHAPTER_POSITION_BIAS.md`,",
            "`docs/DIRECTION_ASYMMETRY.md`, `docs/CANONICAL_FIRST_SUMMARY.md`,",
            "`docs/CROSS_SKIP_SUMMARY.md`, `docs/REVIEW_FLAG_SUMMARY.md`, and",
            "`docs/COHORT_CLUSTER_DENSITY_AUDIT.md`.",
        ]
    )
    return lines


def matrix_cluster_control_section(
    relation_rows: list[dict[str, str]],
    term_pair_rows: list[dict[str, str]],
) -> list[str]:
    top_pairs = sorted(
        term_pair_rows,
        key=lambda row: (
            -int_value(row, "bible_pairs"),
            row.get("cell_relation", ""),
            row.get("term_a_id", ""),
            row.get("term_b_id", ""),
        ),
    )
    lines = [
        "",
        "## Matrix Cluster Control Summary",
        "",
        "This opt-in geometry layer wraps centered-hit positions to width 50 and",
        "counts declared term-pair neighborhoods by nearest relation. It compares",
        "Bible corpora against language-matched secular controls, normalized both",
        "per observed corpus and per possible centered-hit pair opportunity.",
        "",
        "| Relation | Bible pairs | Control pairs | Corpus ratio | Opportunity ratio | Exceeds control max |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in relation_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row.get('cell_relation', '')}`",
                    f"{int_value(row, 'bible_pairs'):,}",
                    f"{int_value(row, 'secular_control_pairs'):,}",
                    numeric_cell(row.get("bible_to_control_rate_ratio", "")),
                    numeric_cell(row.get("bible_to_control_opportunity_ratio", "")),
                    f"`{row.get('exceeds_secular_max', '')}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Top term-pair rows:",
            "",
            "| Relation | Term A | Term B | Bible pairs | Control pairs | Corpus ratio | Opportunity ratio |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in top_pairs[:10]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row.get('cell_relation', '')}`",
                    display_term(
                        row.get("term_a_normalized", ""),
                        english=row.get("term_a_concept", ""),
                    ),
                    display_term(
                        row.get("term_b_normalized", ""),
                        english=row.get("term_b_concept", ""),
                    ),
                    f"{int_value(row, 'bible_pairs'):,}",
                    f"{int_value(row, 'secular_control_pairs'):,}",
                    numeric_cell(row.get("bible_to_control_rate_ratio", "")),
                    numeric_cell(row.get("bible_to_control_opportunity_ratio", "")),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Current read: this is a relation-specific screening summary, not a",
            "matrix-code claim. Claim-grade matrix work still needs locked row-width",
            "families, relation metrics, matched controls, and multiple-comparison",
            "correction.",
            "",
            "Source artifacts: `docs/MATRIX_CLUSTER_CANDIDATES.md` and",
            "`docs/MATRIX_CLUSTER_CONTROL_SUMMARY.md`.",
        ]
    )
    return lines


def notable_passage_gap_section(
    passage_rows: list[dict[str, str]],
    cross_source_rows: list[dict[str, str]],
) -> list[str]:
    declared_rows = [
        row
        for row in passage_rows
        if row.get("passage_id") == "lev24_blasphemy_law"
    ]
    lev24_cross_rows = [
        row
        for row in cross_source_rows
        if row.get("passage_id") in {
            "lev24_blasphemy_law",
            "lev24_blasphemy_law_lxx",
            "lev24_blasphemy_law_kjva",
        }
        and int_value(row, "gap_corpus_count") > 0
    ]
    top_cross_rows = sorted(
        lev24_cross_rows,
        key=lambda row: (
            -int_value(row, "gap_corpus_count"),
            row.get("passage_id", ""),
            row.get("term_id", ""),
        ),
    )
    min_present = min_int(declared_rows, "terms_present_in_passage")
    max_present = max_int(declared_rows, "terms_present_in_passage")
    min_absent = min_int(declared_rows, "terms_absent_in_passage_common_elsewhere")
    max_absent = max_int(declared_rows, "terms_absent_in_passage_common_elsewhere")
    min_low = min_int(declared_rows, "terms_low_vs_uniform")
    max_low = max_int(declared_rows, "terms_low_vs_uniform")
    lines = [
        "",
        "## Notable Passage Gap Ledger",
        "",
        "This absence layer records declared passages where selected centered ELS",
        "terms are absent or sparse inside the passage while appearing elsewhere",
        "in the same corpus. It is a screening ledger, not a negative conclusion.",
        "",
        "The current declared Leviticus 24 blasphemy-law target uses skip 2..500.",
        (
            "Across the five MT-family witnesses, present terms range "
            f"{range_text(min_present, max_present)}, absent-common-elsewhere terms "
            f"range {range_text(min_absent, max_absent)}, and low-vs-uniform terms "
            f"range {range_text(min_low, max_low)}."
            if declared_rows
            else "No Leviticus 24 MT-family passage-summary rows were available."
        ),
        "",
        "| Passage | Term | Gap class | Gap corpora | Present corpora |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    for row in top_cross_rows[:12]:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(row.get("passage_concept", "")),
                    display_term(
                        row.get("normalized_term", ""),
                        english=row.get("concept", ""),
                    ),
                    f"`{row.get('strongest_gap_class', '')}`",
                    f"{int_value(row, 'gap_corpus_count'):,}",
                    f"{int_value(row, 'present_corpus_count'):,}",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Current read: the cross-source file groups absence and low-density rows",
            "by term across editions, so repeated gaps can be reviewed separately",
            "from one-source curiosities.",
            "",
            "Source artifact: `docs/NOTABLE_PASSAGE_GAPS.md`.",
        ]
    )
    return lines


def thematic_chapter_absence_section(
    passage_rows: list[dict[str, str]],
    cross_source_rows: list[dict[str, str]],
) -> list[str]:
    gap_rows = [
        row
        for row in cross_source_rows
        if int_value(row, "gap_corpus_count") > 0
    ]
    present_rows = [
        row
        for row in cross_source_rows
        if int_value(row, "present_corpus_count") > 0
        and int_value(row, "gap_corpus_count") == 0
    ]
    top_gap_rows = sorted(
        gap_rows,
        key=lambda row: (
            -int_value(row, "gap_corpus_count"),
            row.get("passage_id", ""),
            row.get("term_id", ""),
        ),
    )
    top_present_rows = sorted(
        present_rows,
        key=lambda row: (
            -int_value(row, "present_corpus_count"),
            row.get("passage_id", ""),
            row.get("term_id", ""),
        ),
    )
    lines = [
        "",
        "## Thematic Chapter Absence Ledger",
        "",
        "This narrower ledger checks locked term-to-chapter mappings. It keeps",
        "positive thematic presence and thematic absence in the same view, because",
        "both are review facts.",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Passage summary rows | {len(passage_rows):,} |",
        f"| Cross-source rows | {len(cross_source_rows):,} |",
        f"| Rows with any gap corpus | {len(gap_rows):,} |",
        f"| Rows present without gap | {len(present_rows):,} |",
        "",
        "Top gap rows:",
        "",
        "| Passage | Term | Gap class | Gap corpora | Present corpora |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    for row in top_gap_rows[:10]:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(row.get("passage_concept", "")),
                    display_term(
                        row.get("normalized_term", ""),
                        english=row.get("concept", ""),
                    ),
                    f"`{row.get('strongest_gap_class', '')}`",
                    f"{int_value(row, 'gap_corpus_count'):,}",
                    f"{int_value(row, 'present_corpus_count'):,}",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Top present rows:",
            "",
            "| Passage | Term | Present corpora |",
            "| --- | --- | ---: |",
        ]
    )
    for row in top_present_rows[:8]:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(row.get("passage_concept", "")),
                    display_term(
                        row.get("normalized_term", ""),
                        english=row.get("concept", ""),
                    ),
                    f"{int_value(row, 'present_corpus_count'):,}",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Current read: Gog, Magog, and Beast thematic chapters have positive",
            "MT-family presence rows, while Isaiah 53 wound/Greek servant-term rows",
            "remain absence-review material at the registered settings.",
            "",
            "Source artifact: `docs/THEMATIC_CHAPTER_ABSENCE.md`.",
        ]
    )
    return lines


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def bucket_count_text(rows: list[dict[str, str]], label_key: str, count_key: str) -> str:
    totals: Counter[str] = Counter()
    for row in rows:
        label = row.get(label_key, "")
        if label:
            totals[label] += int_value(row, count_key)
    if not totals:
        return "none"
    top = sorted(totals.items(), key=lambda item: (-item[1], item[0]))[:4]
    return md_cell(", ".join(f"`{label}`={count:,}" for label, count in top))


def cohort_window_text(rows: list[dict[str, str]]) -> str:
    windows = sum(int_values(rows, "windows"))
    if windows == 0:
        return "no cohort windows met the declared threshold"
    max_distinct = max_int(rows, "max_distinct_term_count")
    return f"{windows:,} windows; max distinct term count {max_distinct or 0:,}"


def numeric_cell(value: object) -> str:
    text = str(value)
    return text if text else "--"


def range_text(low: int | None, high: int | None) -> str:
    if low is None or high is None:
        return "none"
    if low == high:
        return f"{low:,}"
    return f"{low:,}..{high:,}"


def doxa_section(
    title: str,
    rows: list[dict[str, str]],
    manifest: dict[str, Any],
) -> list[str]:
    lines = [
        "",
        f"## {title}",
        "",
        f"Protocol status: `{manifest.get('status', '')}`; runtime {manifest.get('duration_seconds', '')}s.",
        "",
        "| Corpus | Combined p | Combined q | All-control q | Term-any p | Random-any p | Flags |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in sorted(rows, key=lambda item: item["corpus"]):
        lines.append(
            "| "
            + " | ".join(
                [
                    row["corpus"],
                    row["combined_min_p"],
                    row["combined_min_q"],
                    row.get("all_controls_max_q", ""),
                    row["term_any_p_ge"],
                    row["random_any_p_ge"],
                    f"`{row['flags']}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            f"Current read: all four rows have q <= 0.01; q range {q_range(rows)}.",
            f"Conservative all-control q range: {q_range(rows, 'all_controls_max_q')}.",
            "Status remains `claim_followup_review_candidate`, not claim.",
        ]
    )
    return lines


def surface_queue_section(
    summary_rows: list[dict[str, str]],
    pattern_rows: list[dict[str, str]],
    manifest: dict[str, Any],
) -> list[str]:
    scope_counts = Counter(row["presence_scope"] for row in pattern_rows)
    top_rows = sorted(
        summary_rows,
        key=lambda row: (
            -int_value(row, "all_source_patterns"),
            -int_value(row, "multi_source_patterns"),
            -int_value(row, "total_exact_center_hits"),
            row["term_id"],
        ),
    )
    lines = [
        "",
        "## Expanded Greek Surface Queue",
        "",
        f"Protocol status: `{manifest.get('status', '')}`; runtime {manifest.get('duration_seconds', '')}s.",
        "",
        "`exact-center surface` means the ELS center lands in a verse where the",
        "term appears as ordinary surface text. It does not mean the center word",
        "itself is the searched term.",
        "",
        "| Scope | Patterns |",
        "| --- | ---: |",
        f"| All-source | {scope_counts.get('all_sources', 0):,} |",
        f"| Multi-source | {scope_counts.get('multi_source', 0):,} |",
        f"| Source-only | {scope_counts.get('source_only', 0):,} |",
        "",
        "Top queued terms:",
        "",
        "| Term | Concept | Exact-center hits | Unique patterns | All-source | Multi-source |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in top_rows[:10]:
        lines.append(
            "| "
            + " | ".join(
                [
                    display_term(row["normalized_term"], english=row["concept"]),
                    row["concept"],
                    row["total_exact_center_hits"],
                    row["unique_patterns"],
                    row["all_source_patterns"],
                    row["multi_source_patterns"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Current read: this queue is broader and weaker than the phrase-extension",
            "gate. It is useful for selecting future matched-control targets, not for",
            "claim promotion.",
        ]
    )
    return lines


def surface_triage_section(
    selected_rows: list[dict[str, str]],
    cohort_rows: list[dict[str, str]],
    manifest: dict[str, Any],
) -> list[str]:
    selected_terms = {row["term_id"] for row in selected_rows}
    short_all_source_patterns = sum(
        int_value(row, "all_source_patterns")
        for row in cohort_rows
        if row.get("read") == "all-source but below length threshold"
    )
    lines = [
        "",
        "## Expanded Greek Surface Triage",
        "",
        f"Protocol status: `{manifest.get('status', '')}`; runtime {manifest.get('duration_seconds', '')}s.",
        "",
        "Mechanical filter: all-source exact-center surface rows with normalized",
        "term length >= 5. This excludes the dense length-4 bucket without making",
        "term-specific judgments.",
        "",
        f"Selected patterns: {len(selected_rows):,}; selected terms: {len(selected_terms):,};",
        f"all-source patterns below length threshold: {short_all_source_patterns:,}.",
        "",
        "| Term | Concept | Center | Skip | Direction | Length rank |",
        "| --- | --- | --- | ---: | --- | ---: |",
    ]
    for row in selected_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    display_term(row["normalized_term"], english=row["concept"]),
                    row["concept"],
                    row["center_ref"],
                    row["skip"],
                    row["direction"],
                    row["length_cohort_all_source_rank"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Current read: these are review rows only. Surface-context controls should",
            "use real Greek terms matched by length and surface frequency, not random",
            "strings that cannot appear openly in the text.",
        ]
    )
    return lines


def surface_letter_paths_section(
    rows: list[dict[str, str]],
    manifest: dict[str, Any],
) -> list[str]:
    lines = [
        "",
        "## Expanded Greek Surface Letter Paths",
        "",
        f"Protocol status: `{manifest.get('status', '')}`; runtime {manifest.get('duration_seconds', '')}s.",
        "",
        "The audit sheet reconstructs the actual ELS letters for each selected",
        "surface-triage row in each compared Greek NT source.",
        "",
        "| Term | Corpus | Sequence | Skip | Center | Center word |",
        "| --- | --- | --- | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    display_term(row["normalized_term"]),
                    row["corpus"],
                    display_term(row["sequence"]),
                    row["skip"],
                    row["center_ref"],
                    display_term(row["center_word"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Current read: all selected paths should spell the normalized term exactly.",
            "This is an audit layer, not a new statistical test.",
        ]
    )
    return lines


def surface_control_pool_section(
    frequency_rows: list[dict[str, str]],
    matched_rows: list[dict[str, str]],
    manifest: dict[str, Any],
) -> list[str]:
    selected = [row for row in frequency_rows if row.get("selected_target") == "True"]
    all_source_terms = sum(
        row.get("all_source_surface_present") == "True" for row in frequency_rows
    )
    lines = [
        "",
        "## Expanded Greek Surface Control Pool",
        "",
        f"Protocol status: `{manifest.get('status', '')}`; runtime {manifest.get('duration_seconds', '')}s.",
        "",
        "This is a real-word normalized surface-substring frequency control pool,",
        "not an ELS significance test. Selected target terms are excluded from",
        "the control candidates.",
        "",
        f"Terms measured: {len(frequency_rows):,}; all-source surface-present terms: {all_source_terms:,};",
        f"matched controls: {len(matched_rows):,}.",
        "",
        "| Target | Surface vector | Sum | Closest controls |",
        "| --- | --- | ---: | --- |",
    ]
    for row in selected:
        controls = [
            control
            for control in matched_rows
            if control["target_term_id"] == row["term_id"]
        ][:3]
        control_text = ", ".join(
            f"{display_term(control['control_normalized_term'])} ({control['surface_vector_l1_delta']})"
            for control in controls
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    display_term(row["normalized_term"]),
                    "/".join(
                        [
                            row["surface_verses_tr_nt"],
                            row["surface_verses_byz_nt"],
                            row["surface_verses_tcg_nt"],
                            row["surface_verses_sblgnt"],
                        ]
                    ),
                    row["surface_verse_sum"],
                    control_text,
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Current read: the fair next control should be run against these frozen",
            "real-word pools, because random strings cannot meet a surface-context",
            "condition.",
        ]
    )
    return lines


def surface_control_evaluation_section(
    rows: list[dict[str, str]],
    manifest: dict[str, Any],
    *,
    title: str = "Expanded Greek Surface Control Evaluation",
    lead: str = (
        "Exploratory result: selected rows beat their 10 matched real-word controls "
        "on all-source exact-center surface-pattern count, but the control pool is "
        "too small for p <= 0.05."
    ),
    read: str = (
        "Current read: useful triage evidence, not statistical support. A larger "
        "real-word matched-control pool must be frozen before a stronger "
        "evaluation."
    ),
) -> list[str]:
    lines = [
        "",
        f"## {title}",
        "",
        f"Protocol status: `{manifest.get('status', '')}`; runtime {manifest.get('duration_seconds', '')}s.",
        "",
        lead,
        "",
        "| Term | Observed all-source | Controls >= observed | p_ge | q |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    display_term(row["target_normalized_term"]),
                    row["observed_all_source_patterns"],
                    row["controls_ge_observed_all_source"],
                    row["all_source_p_ge"],
                    row["all_source_q_value"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            read,
        ]
    )
    return lines


def surface_followup_section(
    report_manifest: dict[str, Any],
    protocol_manifest: dict[str, Any],
) -> list[str]:
    status = report_manifest.get("status", "")
    selected_rows = report_manifest.get("selected_rows", "")
    path_rows = report_manifest.get("path_rows", "")
    control_rows = report_manifest.get("control_rows", "")
    return [
        "",
        "## Expanded Greek Surface Follow-Up Report",
        "",
        f"Protocol status: `{protocol_manifest.get('status', '')}`; runtime {protocol_manifest.get('duration_seconds', '')}s.",
        "",
        f"Report status: `{status}`.",
        "",
        "| Input | Rows |",
        "| --- | ---: |",
        f"| Selected surface rows | {selected_rows} |",
        f"| Letter-path audit rows | {path_rows} |",
        f"| All-available control rows | {control_rows} |",
        "",
        "Current read: this compact report joins selected rows, reconstructed letter",
        "paths, and all-available real-word controls into one post-screen review",
        "sheet. It remains a review candidate report, not a claim.",
    ]


def surface_length4_followup_section(
    selected_rows: list[dict[str, str]],
    cohort_rows: list[dict[str, str]],
    control_rows: list[dict[str, str]],
    path_rows: list[dict[str, str]],
    protocol_manifest: dict[str, Any],
) -> list[str]:
    selected_terms = sorted({row["normalized_term"] for row in selected_rows})
    short_rows = [
        row for row in cohort_rows if row.get("read") == "all-source but below length threshold"
    ]
    min_q = min_float(control_rows, "all_source_q_value")
    max_q = max_float(control_rows, "all_source_q_value")
    q_range_text = "none" if min_q is None or max_q is None else f"{min_q:.6f}..{max_q:.6f}"
    lines = [
        "",
        "## Greek Surface Length-4 Follow-Up",
        "",
        f"Protocol status: `{protocol_manifest.get('status', '')}`; runtime {protocol_manifest.get('duration_seconds', '')}s.",
        "",
        "This is a post-discovery follow-up on the length-4 all-source bucket exposed",
        "by the locked Greek surface prospective run. It is not prospective discovery.",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Selected length-4 surface rows | {len(selected_rows):,} |",
        f"| Selected terms | {len(selected_terms):,} |",
        f"| Cohort rows still below threshold | {len(short_rows):,} |",
        f"| Control-evaluation rows | {len(control_rows):,} |",
        f"| Letter-path audit rows | {len(path_rows):,} |",
        "",
        f"Selected terms: {', '.join(display_term(term) for term in selected_terms)}.",
        f"Matched-control q range: {q_range_text}.",
        "",
        "| Term | Observed all-source | Controls >= observed | q |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in control_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    display_term(row["target_normalized_term"]),
                    row["observed_all_source_patterns"],
                    row["controls_ge_observed_all_source"],
                    row["all_source_q_value"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Current read: each selected length-4 target exceeds every available",
            "same-length real-word control on all-source exact-center surface-pattern",
            "count, but only 14 controls were available per target. The add-one",
            "empirical floor is p/q = 0.066667, so this remains triage evidence and",
            "not a claim-grade result.",
        ]
    )
    return lines


def surface_length4_vocabulary_controls_section(
    terms_manifest: dict[str, Any],
    control_rows: list[dict[str, str]],
    protocol_manifest: dict[str, Any],
) -> list[str]:
    generated_controls = int(terms_manifest.get("control_rows", 0))
    target_rows = int(terms_manifest.get("target_rows", 0))
    q_values = float_values(control_rows, "all_source_q_value")
    q_range_text = "none" if not q_values else f"{min(q_values):.6f}..{max(q_values):.6f}"
    min_matched = min_int(control_rows, "matched_controls")
    max_matched = max_int(control_rows, "matched_controls")
    matched_text = "none" if min_matched is None or max_matched is None else f"{min_matched}..{max_matched}"
    lines = [
        "",
        "## Greek Surface Length-4 Vocabulary Controls",
        "",
        f"Protocol status: `{protocol_manifest.get('status', '')}`; runtime {protocol_manifest.get('duration_seconds', '')}s.",
        "",
        "This post-discovery follow-up replaces the sparse declared-term control",
        "pool with generated length-4 real Greek surface vocabulary controls.",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Selected targets retained | {target_rows:,} |",
        f"| Generated vocabulary controls | {generated_controls:,} |",
        f"| Evaluation rows | {len(control_rows):,} |",
        f"| Matched controls per target | {matched_text} |",
        "",
        f"Vocabulary-control q range: {q_range_text}.",
        "",
        "| Term | Observed all-source | Controls >= observed | p_ge | q |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in control_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    display_term(row["target_normalized_term"]),
                    row["observed_all_source_patterns"],
                    row["controls_ge_observed_all_source"],
                    row["all_source_p_ge"],
                    row["all_source_q_value"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Current read: the larger vocabulary-control pool overlaps every length-4",
            "target, and no target survives study-level q <= 0.05. This weakens the",
            "length-4 follow-up rather than strengthening it.",
        ]
    )
    return lines


def wrr_audit_section(
    protocol_manifest: dict[str, Any],
    source_manifest: dict[str, Any],
    text_source_rows: list[dict[str, str]],
    source_shape_rows: list[dict[str, str]],
    count_rows: list[dict[str, str]],
    pair_rows: list[dict[str, str]],
    control_rows: list[dict[str, str]],
    skip_cap_rows: list[dict[str, str]],
    reconciliation_rows: list[dict[str, str]],
    perturbation_rows: list[dict[str, str]],
    cross_pair_recommended_permutation_rows: list[dict[str, str]],
) -> list[str]:
    source_hashes = {
        download["label"]: download.get("sha256", "")
        for download in source_manifest.get("downloads", [])
        if isinstance(download, dict)
    }
    missing_source_labels = [
        label for label in WRR_REQUIRED_SOURCE_LABELS if not source_hashes.get(label)
    ]
    if missing_source_labels:
        raise ValueError(
            "WRR source manifest missing hashes for: " + ", ".join(missing_source_labels)
        )
    count_totals = {
        "concepts": len(count_rows),
        "appellation_rows": sum(int_values(count_rows, "appellation_rows")),
        "date_rows": sum(int_values(count_rows, "date_rows")),
        "appellation_hits": sum(int_values(count_rows, "appellation_hits")),
        "date_hits": sum(int_values(count_rows, "date_hits")),
    }
    pair_totals = {
        "concepts": len(pair_rows),
        "pair_rows": sum(int_values(pair_rows, "pair_rows")),
        "close_pairs": sum(int_values(pair_rows, "all_pairs_within_gap")),
        "overlap_pairs": sum(int_values(pair_rows, "all_overlap_pairs")),
        "strict_pairs": sum(int_values(pair_rows, "strict_pairs_within_gap")),
        "best_wrr_alpha": max_float(pair_rows, "best_wrr_alpha"),
    }
    skip_caps = skip_cap_rows[0] if skip_cap_rows else {}
    source_shapes = source_shape_rows[0] if source_shape_rows else {}
    text_source = text_source_rows[0] if text_source_rows else {}
    reconciliation = reconciliation_rows[0] if reconciliation_rows else {}
    perturbations = perturbation_rows[0] if perturbation_rows else {}
    cross_pair_permutation = (
        cross_pair_recommended_permutation_rows[0]
        if cross_pair_recommended_permutation_rows
        else {}
    )
    adjusted_signal_rows = sum(
        1
        for row in control_rows
        if row.get("band") not in {"not_unusual", ""}
        and (min_float([row], "combined_min_q") or 1.0) <= 0.05
    )
    lines = [
        "",
        "## WRR 1994 Source Audit",
        "",
        f"Protocol status: `{protocol_manifest.get('status', '')}`; runtime {protocol_manifest.get('duration_seconds', '')}s.",
        "",
        "This track imports the secondary ANU/McKay `WRR2.txt` source into an",
        "ignored local term file, counts the rows in Koren Genesis, runs smoke",
        "controls, and records the current repo-defined WRR diagnostic status.",
        "It is not an exact WRR reproduction.",
        "",
        "| Source | SHA-256 |",
        "| --- | --- |",
        f"| WRR 1994 paper PDF | `{source_hashes.get('wrr_1994_paper', '')}` |",
        f"| MBBK 1999 response PDF | `{source_hashes.get('mmbbk_1999_paper', '')}` |",
        f"| MBBK data page | `{source_hashes.get('mmbbk_data_page', '')}` |",
        f"| Chance article PDF | `{source_hashes.get('chance_article', '')}` |",
        f"| Torah-code papers page | `{source_hashes.get('torah_code_papers_page', '')}` |",
        f"| Torah-code co-linear paper | `{source_hashes.get('torah_code_colinear_paper', '')}` |",
        f"| Torah-code co-linear attachments | `{source_hashes.get('torah_code_colinear_attachments', '')}` |",
        f"| Gans/Inbal/Bombach Genesis pairs paper | `{source_hashes.get('gans_communities_paper', '')}` |",
        f"| Gans/Inbal/Bombach Genesis pairs data | `{source_hashes.get('gans_communities_data', '')}` |",
        f"| Haralick new protocols paper | `{source_hashes.get('haralick_new_protocols', '')}` |",
        f"| Haralick controversy paper | `{source_hashes.get('haralick_controversy', '')}` |",
        f"| Haralick Skeptical Inquirer response | `{source_hashes.get('haralick_skeptical_response', '')}` |",
        f"| Haralick basic concepts paper | `{source_hashes.get('haralick_basic_concepts', '')}` |",
        f"| Haralick experimental protocol paper | `{source_hashes.get('haralick_experimental_protocol', '')}` |",
        f"| Levitt component-analysis paper | `{source_hashes.get('levitt_component_analysis', '')}` |",
        f"| Levitt component-analysis data | `{source_hashes.get('levitt_component_data', '')}` |",
        f"| Levitt long-phrases paper | `{source_hashes.get('levitt_long_phrases', '')}` |",
        f"| Levitt linguistic-connections paper | `{source_hashes.get('levitt_linguistic_connections', '')}` |",
        f"| Rips/Levitt Twin Towers paper | `{source_hashes.get('rips_twin_towers', '')}` |",
        f"| Schwartzman dialog-mode paper | `{source_hashes.get('schwartzman_dialog_mode', '')}` |",
        f"| Witztum Genesis birth-dates paper | `{source_hashes.get('witztum_birth_dates', '')}` |",
        f"| Witztum Genesis birth-dates data | `{source_hashes.get('witztum_birth_dates_data', '')}` |",
        f"| Torah-code experiments page | `{source_hashes.get('torah_code_experiments_page', '')}` |",
        f"| Torah-code experiment personal statement | `{source_hashes.get('torah_code_experiment_personal_statement', '')}` |",
        f"| American-presidents experiment paper | `{source_hashes.get('torah_code_experiment_american_presidents_paper', '')}` |",
        f"| American-presidents input data | `{source_hashes.get('torah_code_experiment_american_presidents_data', '')}` |",
        f"| American-presidents transliteration rules | `{source_hashes.get('torah_code_experiment_english_hebrew_transliteration_rules', '')}` |",
        f"| Israeli-prime-ministers experiment paper | `{source_hashes.get('torah_code_experiment_israeli_prime_ministers_paper', '')}` |",
        f"| Israeli-prime-ministers first keyword page | `{source_hashes.get('torah_code_experiment_israeli_prime_ministers_1', '')}` |",
        f"| Israeli-prime-ministers eighth keyword page | `{source_hashes.get('torah_code_experiment_israeli_prime_ministers_8', '')}` |",
        f"| Cities experiment page | `{source_hashes.get('torah_code_experiment_cities_page', '')}` |",
        f"| Gans original cities report | `{source_hashes.get('torah_code_experiment_cities_gans_original_report', '')}` |",
        f"| Aumann cities committee report | `{source_hashes.get('torah_code_experiment_cities_aumann_report', '')}` |",
        f"| Aumann cities expert city names | `{source_hashes.get('torah_code_experiment_cities_aumann_city_names', '')}` |",
        f"| Simon-McKay cities page | `{source_hashes.get('torah_code_experiment_cities_simon_mckay_page', '')}` |",
        f"| Margolioth cities data | `{source_hashes.get('torah_code_experiment_cities_margolioth_data', '')}` |",
        f"| Sons of Haman data page | `{source_hashes.get('torah_code_experiment_sons_of_haman_data', '')}` |",
        f"| Pumbedita data PDF | `{source_hashes.get('torah_code_experiment_pumbedita_data', '')}` |",
        f"| Auschwitz data PDF | `{source_hashes.get('torah_code_experiment_auschwitz_data', '')}` |",
        f"| Ark Code tutorial PDF | `{source_hashes.get('torah_code_experiment_ark_code', '')}` |",
        f"| Torah-code research program page 1 | `{source_hashes.get('torah_code_research_program_1', '')}` |",
        f"| Torah-code research program page 2 | `{source_hashes.get('torah_code_research_program_2', '')}` |",
        f"| Torah-code research model overview | `{source_hashes.get('torah_code_research_model_overview', '')}` |",
        f"| Torah-code research geometric model level 1 | `{source_hashes.get('torah_code_research_geometric_model_level_1', '')}` |",
        f"| Torah-code research geometric model level 2 | `{source_hashes.get('torah_code_research_geometric_model_level_2', '')}` |",
        f"| Torah-code research geometric model level 3 | `{source_hashes.get('torah_code_research_geometric_model_level_3', '')}` |",
        f"| Torah-code research ELS model level 1 | `{source_hashes.get('torah_code_research_els_model_level_1', '')}` |",
        f"| Torah-code research ELS model level 2 | `{source_hashes.get('torah_code_research_els_model_level_2', '')}` |",
        f"| Torah-code research ELS model level 3 | `{source_hashes.get('torah_code_research_els_model_level_3', '')}` |",
        f"| WRR2.txt | `{source_hashes.get('wrr2', '')}` |",
        f"| WRR1.txt | `{source_hashes.get('wrr1', '')}` |",
        f"| SE2a.txt | `{source_hashes.get('se2a', '')}` |",
        f"| SE2b.txt | `{source_hashes.get('se2b', '')}` |",
        f"| SE3.txt | `{source_hashes.get('se3', '')}` |",
        f"| MC key | `{source_hashes.get('mc_key', '')}` |",
        f"| WRR/Nations MC page | `{source_hashes.get('wrr_nations_mc', '')}` |",
        f"| WRR/Nations Hebrew page | `{source_hashes.get('wrr_nations_gir', '')}` |",
        f"| WNP source critique MC page | `{source_hashes.get('wnp_mc', '')}` |",
        f"| WNP source critique English page | `{source_hashes.get('wnp_en', '')}` |",
        "",
        "| Koren Genesis Text | Value |",
        "| --- | --- |",
        f"| Raw source SHA-256 | `{text_source.get('source_raw_sha256', '')}` |",
        f"| Decompressed source SHA-256 | `{text_source.get('source_text_sha256', '')}` |",
        f"| Normalized text SHA-256 | `{text_source.get('normalized_text_sha256', '')}` |",
        f"| Normalized letters | {int_value(text_source, 'normalized_letters'):,} |",
        f"| Parsed verses | {int_value(text_source, 'verse_count'):,} |",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Counted concepts | {count_totals['concepts']:,} |",
        f"| Appellation rows | {count_totals['appellation_rows']:,} |",
        f"| Date rows | {count_totals['date_rows']:,} |",
        f"| Appellation hits | {count_totals['appellation_hits']:,} |",
        f"| Date hits | {count_totals['date_hits']:,} |",
        "| WRR paper second-list candidate word pairs | 298 |",
        "| WRR/Nations cited second-list defined distances | 163 |",
        f"| ANU famous-rabbi source files parsed | {int_value(source_shapes, 'parsed_files'):,} |",
        f"| ANU source files matching 163 raw pairs | {int_value(source_shapes, 'files_matching_expected_pairs'):,} |",
        f"| Max raw pairs in ANU source shape audit | {int_value(source_shapes, 'max_same_record_pairs'):,} |",
        f"| Length 5..8 pair-audited concepts | {pair_totals['concepts']:,} |",
        f"| Length 5..8 pair rows | {pair_totals['pair_rows']:,} |",
        f"| Length 5..8 close pairs | {pair_totals['close_pairs']:,} |",
        f"| Length 5..8 overlap pairs | {pair_totals['overlap_pairs']:,} |",
        f"| Length 5..8 strict pairs | {pair_totals['strict_pairs']:,} |",
        f"| Length 5..8 best diagnostic WRR alpha | {format_optional_float(pair_totals['best_wrr_alpha'])} |",
        f"| Length 5..8 adjusted control-signal rows | {adjusted_signal_rows:,} |",
        f"| Imported source-record pairs | {int_value(reconciliation, 'imported_same_record_pairs'):,} |",
        f"| Appellation length >= 5 source-record pairs | {int_value(reconciliation, 'appellation_min_length_same_record_pairs'):,} |",
        f"| WNP-disputed Zacut appellation rows | {int_value(reconciliation, 'wnp_disputed_zacut_appellation_rows'):,} |",
        f"| Pair delta if all WNP-disputed Zacut rows are excluded | {int_value(reconciliation, 'wnp_disputed_zacut_appellation_min_length_pair_delta'):,} |",
        f"| Appellation length >= 5 pairs after one Zacut appellation exclusion | {int_value(reconciliation, 'appellation_min_length_pairs_after_one_zacut_appellation_excluded'):,} |",
        f"| Gap after one Zacut appellation exclusion | {int_value(reconciliation, 'appellation_min_length_gap_after_one_zacut_appellation_excluded'):,} |",
        f"| Length 5..8 reconciled pair rows | {int_value(reconciliation, 'length_filtered_same_record_pairs'):,} |",
        f"| Gap to source-cited 163 distances after import | {int_value(reconciliation, 'imported_pair_gap_to_expected'):,} |",
        f"| Gap after appellation length >= 5 filter | {int_value(reconciliation, 'appellation_min_length_gap_to_expected'):,} |",
        f"| Gap to source-cited 163 distances after length filter | {int_value(reconciliation, 'length_filtered_gap_to_expected'):,} |",
        f"| Skip-cap rows with D(w) <= 250 | {int_value(skip_caps, 'cap_le_observed_max_skip'):,} |",
        f"| Skip-cap rows not reaching target by word-max skip | {int_value(skip_caps, 'target_unreached_rows'):,} |",
        f"| Perturbation diagnostic rows | {int_value(perturbations, 'rows'):,} |",
        f"| Perturbation rows with checked hits | {int_value(perturbations, 'rows_with_hits'):,} |",
        f"| Perturbation rows with checked-hit < 10 valid | {int_value(perturbations, 'rows_with_checked_under_10_valid'):,} |",
        f"| Perturbation ordinary boundary failures | {int_value(perturbations, 'ordinary_in_bounds_failures'):,} |",
        f"| Repo-defined date-label permutations | {int_value(cross_pair_permutation, 'permutations'):,} |",
        f"| Repo-defined observed rows | {int_value(cross_pair_permutation, 'observed_rows'):,} |",
        f"| Repo-defined observed c-values | {int_value(cross_pair_permutation, 'observed_defined_corrected_distances'):,} |",
        f"| Repo-defined rho P1 | {cross_pair_permutation.get('rho_p1', '')} |",
        f"| Repo-defined rho P2 | {cross_pair_permutation.get('rho_p2', '')} |",
        f"| Repo-defined rho P3 | {cross_pair_permutation.get('rho_p3', '')} |",
        f"| Repo-defined rho P4 | {cross_pair_permutation.get('rho_p4', '')} |",
        f"| Repo-defined Bonferroni rho0 | {cross_pair_permutation.get('rho0_bonferroni', '')} |",
        "",
        "The WRR 1994 paper's 298 second-list word pairs and the later WRR/Nations",
        "163-distance statement are treated here as distinct quantities. Current",
        "source review treats `163` as a defined corrected-distance output count,",
        "not a raw pair table.",
        "",
        "Current read: WRR has repo-defined diagnostic evidence, but exact WRR",
        "reproduction remains `under_specified`. Exact reproduction still needs a",
        "source-locked pair set and source-locked `D(w)` before claim-grade WRR",
        "language is possible.",
    ]
    return lines


def q_range(rows: list[dict[str, str]], key: str = "combined_min_q") -> str:
    values = []
    for row in rows:
        try:
            values.append(float(row[key]))
        except (KeyError, ValueError):
            continue
    if not values:
        return "none"
    return f"{min(values):.4g}..{max(values):.4g}"


def min_float(rows: list[dict[str, str]], key: str) -> float | None:
    values = float_values(rows, key)
    if not values:
        return None
    return min(values)


def max_float(rows: list[dict[str, str]], key: str) -> float | None:
    values = float_values(rows, key)
    if not values:
        return None
    return max(values)


def format_optional_float(value: object) -> str:
    if value in ("", None):
        return ""
    return f"{float(value):.1f}"


def float_values(rows: list[dict[str, str]], key: str) -> list[float]:
    values = []
    for row in rows:
        try:
            values.append(float(row[key]))
        except (KeyError, ValueError):
            continue
    return values


def min_int(rows: list[dict[str, str]], key: str) -> int | None:
    values = int_values(rows, key)
    if not values:
        return None
    return min(values)


def max_int(rows: list[dict[str, str]], key: str) -> int | None:
    values = int_values(rows, key)
    if not values:
        return None
    return max(values)


def int_values(rows: list[dict[str, str]], key: str) -> list[int]:
    values = []
    for row in rows:
        try:
            values.append(int(row[key]))
        except (KeyError, ValueError):
            continue
    return values


def git_commit() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def int_value(mapping: dict[str, Any], key: str) -> int:
    value = mapping.get(key, 0)
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def percent(value: Any) -> str:
    try:
        return f"{float(value) * 100:.3f}%"
    except (TypeError, ValueError):
        return "0.000%"


if __name__ == "__main__":
    raise SystemExit(main())
