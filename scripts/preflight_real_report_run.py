#!/usr/bin/env python3
"""Preflight checks for a formal report assembly run."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
import time
import tomllib
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.project_index import (
    scan_markdown_docs,
    scan_protocols,
    write_docs_index,
    write_protocol_index,
)
from scripts import (
    check_crd_relevance_dictionary,
    check_doc_command_references,
    check_english_corpus_policy_docs,
    check_expanded_strata_tooling,
    check_hypothesis_testing_source_audit_doc,
    check_manual_review_queue,
    check_preregistration_placeholders,
    check_prospective_study_lanes,
    check_public_claim_language,
    check_source_basis_audit_queue,
    check_wrr_claim_blocker_packet_doc,
    check_wrr_claim_readiness_doc,
    check_wrr_cross_pair_grid_doc,
    check_wrr_defined_diagnostic_docs,
    check_wrr_direct_all_lanes_doc,
    check_wrr_dw_formula_sensitivity_doc,
    check_wrr_lock_options_doc,
    check_wrr_locked_method_report_doc,
    check_wrr_exact_reproduction_gap_dashboard_doc,
    check_wrr_manual_decision_record_worksheet_doc,
    check_wrr_manual_decision_records,
    check_wrr_manual_decision_register_doc,
    check_wrr_method_status_doc,
    check_wrr_public_handoff_docs,
    check_wrr_residual_reconciliation_action_plan_doc,
    check_wrr_residual_term_reconciliation_queue_doc,
    check_wrr_source_recovery_probe_doc,
    check_wrr_wayback_source_recovery_probe_doc,
    check_wrr_method_pair_universe_evidence_packet_doc,
    check_wrr_source_policy_evidence_packet_doc,
    check_wrr_source_policy_review_checklist_doc,
    check_wrr_source_transcription_evidence_packet_doc,
    check_wrr_source_transcription_row_review_checklist_doc,
    check_wrr_remaining_lane_evidence_packets_doc,
    check_wrr_remaining_lane_review_checklist_doc,
    check_wrr_source_policy_scenarios_doc,
    check_wrr_source_review_queue_doc,
    check_wrr_source_visual_review_notes_doc,
    check_wrr_variant_gap_docs,
    validate_study_mapping_schemas,
)
from scripts.release_hygiene import (
    FORBIDDEN_ACCOUNT_TERMS,
    forbidden_hits,
    format_finding,
    git_tracked_paths,
    remote_owner_failures,
    risky_tracked_paths,
    scan_tracked_for_forbidden_account,
    scan_tracked_for_secret_patterns,
)


OUT = Path("reports/real_report_run/preflight.json")
DEFAULT_REQUIRED_PATHS = [
    "scripts/preflight_real_report_run.py",
    "scripts/release_hygiene.py",
    "scripts/check_public_release_hygiene.py",
    "scripts/check_public_claim_language.py",
    "scripts/check_doc_command_references.py",
    "els/project_index.py",
    "Makefile",
    "README.md",
    "docs/REAL_REPORT_RUN.md",
    "docs/REMAINING_WORK_REGISTER.md",
    "protocols/real_report_run.toml",
    "protocols/INDEX.md",
    "protocols/step_tahot_final_gate.toml",
    "protocols/greek_pattern_versions.toml",
    "protocols/greek_exact_center_final_gate.toml",
    "protocols/doxa_four_source_claim_followup.toml",
    "protocols/doxa_four_source_confirmatory_followup.toml",
    "protocols/greek_expanded_surface_queue.toml",
    "protocols/greek_expanded_surface_triage.toml",
    "protocols/greek_expanded_surface_letter_paths.toml",
    "protocols/greek_expanded_surface_control_pool.toml",
    "protocols/greek_expanded_surface_control_evaluation.toml",
    "protocols/greek_expanded_surface_available_control_evaluation.toml",
    "protocols/greek_expanded_surface_followup.toml",
    "protocols/greek_surface_length4_followup.toml",
    "protocols/greek_surface_length4_vocabulary_controls.toml",
    "protocols/hebrew_modern_geopolitical_version_presence.toml",
    "protocols/hebrew_modern_geopolitical_controlled_review.toml",
    "protocols/hebrew_modern_geopolitical_prospective.toml",
    "protocols/hebrew_screening_controlled_review.toml",
    "protocols/hebrew_theology_prospective.toml",
    "protocols/hebrew_theology_all_codes_collection.toml",
    "protocols/hebrew_screening_all_codes_collection.toml",
    "protocols/greek_screening_all_codes_collection.toml",
    "protocols/all_codes_followup_selection.toml",
    "protocols/all_codes_followup_letter_paths.toml",
    "protocols/all_codes_followup_context.toml",
    "protocols/all_codes_followup_extensions.toml",
    "protocols/all_codes_compound_extension_controls.toml",
    "protocols/all_codes_compound_extension_confirmatory.toml",
    "protocols/all_codes_followup_review.toml",
    "protocols/gog_magog_pair_prospective.toml",
    "protocols/wrr_audit_counts.toml",
    "protocols/wrr_cross_pair_grid.toml",
    "protocols/wrr_corrected_distance_direct_all_lanes.toml",
    "protocols/wrr_source_recovery_probe.toml",
    "protocols/wrr_wayback_source_recovery_probe.toml",
    "protocols/centered_relevance_density.toml",
    "protocols/matrix_cluster_candidates.toml",
    "protocols/matrix_cluster_control_summary.toml",
    "protocols/notable_passage_gaps.toml",
    "protocols/thematic_chapter_absence.toml",
    "protocols/boundary_alignment.toml",
    "protocols/chapter_position_bias.toml",
    "protocols/direction_asymmetry.toml",
    "protocols/canonical_first_summary.toml",
    "protocols/cross_skip_summary.toml",
    "protocols/review_flag_summary.toml",
    "protocols/cohort_cluster_density_audit.toml",
    "docs/STEP_TAHOT_FINAL_GATE.md",
    "docs/INDEX.md",
    "docs/CLAIM_CATALOG.md",
    "docs/BIBLE_CODE_DIGEST_AUDIT.md",
    "docs/CRI_ELS_CRITIQUE_AUDIT.md",
    "docs/THEWORDNOTES_ELS_AUDIT.md",
    "docs/COSMIC_CODES_AUDIT.md",
    "docs/MARK_TABATA_ISAIAH53_AUDIT.md",
    "docs/FELCJO_RINGO_ALGORITHM_AUDIT.md",
    "docs/AMANDASAURUS_BIBLECODE_PRIOR_ART_AUDIT.md",
    "docs/BIBLE_CODES_ORG_AUDIT.md",
    "docs/BIBLE_AND_SCIENCE_CODES_AUDIT.md",
    "docs/RELIGIONS_WIKI_SCRIPTURAL_CODES_AUDIT.md",
    "terms/bible_codes_org_claim_terms.csv",
    "docs/GREEK_PATTERN_VERSION_SUMMARY.md",
    "docs/GREEK_EXACT_CENTER_FINAL_GATE.md",
    "docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_PREREGISTRATION.md",
    "docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_REPORT.md",
    "docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_PREREGISTRATION.md",
    "docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md",
    "docs/GREEK_EXPANDED_SURFACE_QUEUE.md",
    "docs/GREEK_EXPANDED_SURFACE_TRIAGE.md",
    "docs/GREEK_EXPANDED_SURFACE_LETTER_PATHS.md",
    "docs/GREEK_EXPANDED_SURFACE_CONTROL_POOL.md",
    "docs/GREEK_EXPANDED_SURFACE_CONTROL_EVALUATION.md",
    "docs/GREEK_EXPANDED_SURFACE_AVAILABLE_CONTROL_POOL.md",
    "docs/GREEK_EXPANDED_SURFACE_AVAILABLE_CONTROL_EVALUATION.md",
    "docs/GREEK_EXPANDED_SURFACE_FOLLOWUP_REPORT.md",
    "docs/GREEK_SURFACE_PROSPECTIVE_PREREGISTRATION.md",
    "docs/GREEK_SURFACE_PROSPECTIVE_REPORT.md",
    "docs/GREEK_SURFACE_PROSPECTIVE_QUEUE.md",
    "docs/GREEK_SURFACE_PROSPECTIVE_TRIAGE.md",
    "docs/GREEK_SURFACE_PROSPECTIVE_CONTROL_EVALUATION.md",
    "docs/GREEK_SURFACE_PROSPECTIVE_LETTER_PATHS.md",
    "docs/CLEAN_LOCK_RESULTS_SUMMARY.md",
    "docs/STRICT_FOLLOWUP_GATE_SUMMARY.md",
    "docs/GREEK_LEXICON_EXTENSION_PROSPECTIVE_REPORT.md",
    "docs/GREEK_SURFACE_LENGTH4_FOLLOWUP_TRIAGE.md",
    "docs/GREEK_SURFACE_LENGTH4_CONTROL_POOL.md",
    "docs/GREEK_SURFACE_LENGTH4_CONTROL_EVALUATION.md",
    "docs/GREEK_SURFACE_LENGTH4_LETTER_PATHS.md",
    "docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROLS.md",
    "docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROL_POOL.md",
    "docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROL_EVALUATION.md",
    "docs/WRR_SOURCE_AUDIT.md",
    "docs/TORAH_CODE_RESEARCH_MODEL_SIMULATION.md",
    "docs/TORAH_CODE_RESEARCH_ELS_MODEL_SIMULATION.md",
    "docs/GANS_COMMUNITIES_SOURCE_AUDIT.md",
    "docs/AMERICAN_PRESIDENTS_SOURCE_AUDIT.md",
    "docs/WITZTUM_BIRTH_DATES_SOURCE_AUDIT.md",
    "docs/ISRAELI_PRIME_MINISTERS_SOURCE_AUDIT.md",
    "docs/COLINEAR_ELS_SOURCE_AUDIT.md",
    "docs/CITIES_SOURCE_CHAIN_AUDIT.md",
    "docs/EVENT_OBJECT_EXPERIMENT_SOURCE_AUDIT.md",
    "docs/UNDER_CONSTRUCTION_EXPERIMENT_SOURCE_AUDIT.md",
    "docs/HYPOTHESIS_TESTING_SOURCE_AUDIT.md",
    "docs/RESEARCH_MISSING_MODEL_PAGES_AUDIT.md",
    "docs/WRR_SOURCE_RECOVERY_PROBE.md",
    "docs/WRR_WAYBACK_SOURCE_RECOVERY_PROBE.md",
    "docs/WRR_REPLICATION_PLAN.md",
    "docs/WRR_METHOD_STATUS.md",
    "docs/WRR_LOCK_OPTIONS.md",
    "docs/WRR_DEFINED_PAIR_SET_AUDIT.md",
    "docs/WRR_DEFINED_GAP_REASON_AUDIT.md",
    "docs/WRR_ZERO_HIT_VARIANT_PROBE.md",
    "docs/WRR_VARIANT_GAP_IMPACT.md",
    "docs/WRR_VARIANT_GAP_UPPER_BOUND.md",
    "docs/WRR_VARIANT_RESIDUAL_REVIEW_PACKET.md",
    "docs/WRR_RESIDUAL_TERM_RECONCILIATION_QUEUE.md",
    "docs/WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md",
    "docs/WRR_SOURCE_REVIEW_QUEUE.md",
    "docs/WRR_SOURCE_VISUAL_REVIEW_NOTES.md",
    "docs/WRR_METHODOLOGY_GAPS.md",
    "docs/WRR_CORRECTED_DISTANCE_NOTES.md",
    "docs/WRR_CROSS_PAIR_GRID.md",
    "docs/WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md",
    "docs/WRR_CLAIM_READINESS.md",
    "docs/WRR_CLAIM_BLOCKER_PACKET.md",
    "docs/WRR_LOCKED_METHOD_REPORT.md",
    "docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md",
    "docs/WRR_SOURCE_POLICY_EVIDENCE_PACKET.md",
    "docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md",
    "docs/WRR_SOURCE_TRANSCRIPTION_EVIDENCE_PACKET.md",
    "docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md",
    "docs/WRR_REMAINING_LANE_EVIDENCE_PACKETS.md",
    "docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md",
    "docs/WRR_MANUAL_DECISION_REGISTER.md",
    "docs/WRR_MANUAL_DECISION_RECORD_WORKSHEET.md",
    "docs/WRR_METHOD_PAIR_UNIVERSE_EVIDENCE_PACKET.md",
    "docs/WRR_SOURCE_POLICY_SCENARIOS.md",
    "docs/WRR_DW_FORMULA_SENSITIVITY.md",
    "docs/CRD_FRAMEWORK.md",
    "docs/CRD_PREREGISTRATION.md",
    "docs/CRD_REPORT.md",
    "docs/CRD_CENTER_WORD_SELF_VS_CONCEPT_FINDINGS.md",
    "docs/CRD_CENTER_WORD_VERSION_PRESENCE_FINDINGS.md",
    "docs/GREEK_SURFACE_PROSPECTIVE_CLAIM_STANDARD.md",
    "docs/STUDY_LOCK_MANIFESTS.md",
    "docs/EXPANDED_STRATA_TOOLING.md",
    "docs/STUDY_MAPPING_SCHEMAS.md",
    "docs/PROSPECTIVE_STUDY_PREREGISTRATION_TEMPLATE.md",
    "docs/PROSPECTIVE_TERM_AUDITS.md",
    "docs/BROADER_SEARCH_FINDINGS.md",
    "docs/HEBREW_MODERN_GEOPOLITICAL_VERSION_PRESENCE.md",
    "docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_REVIEW.md",
    "docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_FINDINGS.md",
    "docs/HEBREW_MODERN_GEOPOLITICAL_PRESENCE_PREREGISTRATION.md",
    "docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_REPORT.md",
    "docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_FINDINGS.md",
    "docs/HEBREW_SCREENING_CONTROLLED_REVIEW.md",
    "docs/HEBREW_SCREENING_CONTROLLED_FINDINGS.md",
    "docs/HEBREW_THEOLOGY_PROSPECTIVE_PREREGISTRATION.md",
    "docs/HEBREW_THEOLOGY_PROSPECTIVE_REPORT.md",
    "docs/HEBREW_THEOLOGY_PROSPECTIVE_FINDINGS.md",
    "docs/HEBREW_THEOLOGY_ALL_CODES_COLLECTION.md",
    "docs/HEBREW_THEOLOGY_ALL_CODES_TRIAGE.md",
    "docs/HEBREW_SCREENING_ALL_CODES_COLLECTION.md",
    "docs/HEBREW_SCREENING_ALL_CODES_TRIAGE.md",
    "docs/GREEK_SCREENING_ALL_CODES_COLLECTION.md",
    "docs/GREEK_SCREENING_ALL_CODES_TRIAGE.md",
    "docs/ALL_CODES_FOLLOWUP_SELECTION.md",
    "docs/ALL_CODES_FOLLOWUP_LETTER_PATHS.md",
    "docs/ALL_CODES_FOLLOWUP_CONTEXT.md",
    "docs/ALL_CODES_FOLLOWUP_EXTENSIONS.md",
    "docs/ALL_CODES_COMPOUND_EXTENSION_CONTROLS.md",
    "docs/ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_PREREGISTRATION.md",
    "docs/ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_CONTROLS.md",
    "docs/ALL_CODES_FOLLOWUP_REVIEW.md",
    "docs/CENTERED_OCCURRENCE_INDEX.md",
    "docs/MANUAL_REVIEW_QUEUE.md",
    "docs/FINAL_REPORT_HIGHLIGHTS.md",
    "docs/PROSPECTIVE_STUDY_READINESS.md",
    "docs/PROSPECTIVE_STUDY_NEXT_LOCK.md",
    "docs/PROSPECTIVE_LANE_STATUS.md",
    "docs/GOG_MAGOG_PAIR_PROSPECTIVE_PREREGISTRATION.md",
    "docs/GOG_MAGOG_PAIR_PROSPECTIVE_REPORT.md",
    "docs/MATRIX_CLUSTER_CANDIDATES.md",
    "docs/MATRIX_CLUSTER_CONTROL_SUMMARY.md",
    "docs/NOTABLE_PASSAGE_GAPS.md",
    "docs/THEMATIC_CHAPTER_ABSENCE.md",
    "docs/MATCH_STRATA_INDEX.md",
    "docs/BOUNDARY_ALIGNMENT.md",
    "docs/CHAPTER_POSITION_BIAS.md",
    "docs/DIRECTION_ASYMMETRY.md",
    "docs/CANONICAL_FIRST_SUMMARY.md",
    "docs/CROSS_SKIP_SUMMARY.md",
    "docs/REVIEW_FLAG_SUMMARY.md",
    "docs/COHORT_CLUSTER_DENSITY_AUDIT.md",
    "docs/CONSOLIDATED_FINDINGS.md",
    "docs/FINAL_REPORT_OUTLINE.md",
    "docs/FINAL_REPORT_DRAFT.md",
    "docs/FINAL_REPORT.md",
    "docs/APOCRYPHA_BRIDGE_STUDY.md",
    "docs/APOCRYPHA_SOURCE_COVERAGE.md",
    "docs/APOCRYPHA_BRIDGE_CANDIDATES.md",
    "docs/APOCRYPHA_BRIDGE_CONTEXT.md",
    "docs/APOCRYPHA_BRIDGE_CONTROLS.md",
    "docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS.md",
    "docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_50.md",
    "docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_100.md",
    "docs/APOCRYPHA_ONLY_COUNTS.md",
    "docs/KJV_APOCRYPHA_ONLY_COUNTS.md",
    "docs/KJV_APOCRYPHA_BRIDGE_CANDIDATES.md",
    "docs/KJV_APOCRYPHA_BRIDGE_CONTEXT.md",
    "docs/KJV_APOCRYPHA_BRIDGE_CONTROLS.md",
    "docs/KJV_APOCRYPHA_BRIDGE_TERM_REVIEW.md",
    "docs/KJV_APOCRYPHA_BRIDGE_TERM_SHUFFLED_CONTROLS_1000.md",
    "docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_PREREGISTRATION.md",
    "docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_CONTROLS_5000.md",
    "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_PREREGISTRATION.md",
    "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CANDIDATES.md",
    "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md",
    "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_CONTROLS.md",
    "docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS.md",
    "docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_50.md",
    "docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_100.md",
    "docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_250.md",
    "docs/VERSION_DISTRIBUTION_INDEX.md",
    "docs/PRIVATE_ENGLISH_VERSIONS.md",
    "docs/SOURCE_BASIS_AUDIT_QUEUE.md",
    "configs/biblegateway_english_versions.csv",
    "configs/ebible_english_controls.csv",
    "configs/door43_english_controls.csv",
    "configs/oet_english_controls.csv",
    "configs/otb_english_controls.csv",
    "configs/openbible_english_controls.csv",
    "configs/odr_english_controls.csv",
    "configs/supplemental_english_controls.csv",
    "protocols/biblegateway_english_versions.toml",
    "protocols/ebible_english_controls.toml",
    "protocols/door43_english_controls.toml",
    "protocols/oet_english_controls.toml",
    "protocols/otb_english_controls.toml",
    "protocols/openbible_english_controls.toml",
    "protocols/odr_english_controls.toml",
    "protocols/supplemental_english_controls.toml",
    "claims/claim_catalog.csv",
    "terms/bible_code_digest_claim_terms.csv",
    "terms/cri_els_critique_terms.csv",
    "terms/thewordnotes_els_claim_terms.csv",
    "terms/cosmic_codes_claim_terms.csv",
    "terms/mark_tabata_isaiah53_claim_terms.csv",
    "terms/bible_and_science_codes_terms.csv",
    "terms/religions_wiki_scriptural_codes_terms.csv",
    "terms/gog_magog_pair_prospective_terms.csv",
    "terms/hebrew_modern_geopolitical_prospective_terms.csv",
    "terms/kjv_apocrypha_bridge_prospective_terms.csv",
    "configs/example_ebible_engkjv_apocrypha.toml",
    "configs/prospective_study_lanes.json",
    "data/study/mappings/README.md",
    "data/study/mappings/author_book_mapping.csv",
    "data/study/mappings/hebrew_root_policy.csv",
    "data/study/mappings/mt_lxx_semantic_divergence.csv",
    "data/study/mappings/ot_in_nt_quotations.csv",
    "data/study/mappings/protagonist_narrative_mapping.csv",
    "data/study/mappings/thematic_chapters.csv",
    "data/study/mappings/wrr_manual_decision_records.csv",
    "protocols/apocrypha_bridge_study.toml",
    "protocols/kjv_apocrypha_bridge_shuffled_controls_250.toml",
    "protocols/kjv_apocrypha_bridge_term_review.toml",
    "protocols/kjv_apocrypha_bridge_term_shuffled_controls_1000.toml",
    "protocols/kjv_apocrypha_bridge_confirmatory_controls_5000.toml",
    "protocols/kjv_apocrypha_bridge_prospective_controls_5000.toml",
    "protocols/kjv_apocrypha_bridge_prospective_nonbible_controls.toml",
    "protocols/external_claim_source_counts.toml",
    "protocols/external_claim_source_all_codes_collection.toml",
    "docs/EXTERNAL_CLAIM_SOURCE_COUNTS.md",
    "docs/EXTERNAL_CLAIM_SOURCE_ALL_CODES_COLLECTION.md",
    "docs/EXTERNAL_CLAIM_SOURCE_ALL_CODES_TRIAGE.md",
    "docs/EXTERNAL_CLAIM_SOURCE_FINDINGS.md",
    "scripts/audit_apocrypha_coverage.py",
    "scripts/analyze_apocrypha_bridge_shuffled_controls.py",
    "scripts/analyze_apocrypha_bridge_term_shuffled_controls.py",
    "scripts/analyze_broad_search.py",
    "scripts/build_external_claim_source_findings.py",
    "scripts/summarize_kjv_apocrypha_bridge_terms.py",
    "scripts/download_ebible_engkjv_apocrypha.py",
    "scripts/build_study_lock_manifest.py",
    "scripts/check_study_lock_manifest.py",
    "scripts/check_preregistration_placeholders.py",
    "scripts/audit_prospective_terms.py",
    "scripts/filter_prospective_terms.py",
    "scripts/preflight_prospective_study.py",
    "scripts/scaffold_prospective_study.py",
    "scripts/check_prospective_study_lanes.py",
    "scripts/check_english_corpus_policy_docs.py",
    "scripts/check_source_basis_audit_queue.py",
    "scripts/build_prospective_lane_status.py",
    "scripts/build_greek_surface_prospective_report.py",
    "scripts/build_greek_surface_vocabulary_controls.py",
    "scripts/summarize_surface_all_codes.py",
    "scripts/triage_surface_all_codes.py",
    "scripts/select_all_codes_followup.py",
    "scripts/analyze_all_codes_letter_paths.py",
    "scripts/build_all_codes_context_excerpts.py",
    "scripts/analyze_all_codes_extensions.py",
    "scripts/analyze_extension_paired_controls.py",
    "scripts/build_all_codes_followup_report.py",
    "scripts/build_centered_occurrence_index.py",
    "scripts/build_match_strata_index.py",
    "scripts/check_crd_relevance_dictionary.py",
    "scripts/check_expanded_strata_tooling.py",
    "scripts/check_manual_review_queue.py",
    "scripts/validate_study_mapping_schemas.py",
    "scripts/run_crd_density.py",
    "scripts/classify_centered_relevance.py",
    "scripts/build_crd_comparison.py",
    "els/match_strata.py",
    "els/gematria.py",
    "els/letter_stats.py",
    "els/term_display.py",
    "terms/meaningful_constants.csv",
    "scripts/build_final_report_highlights.py",
    "scripts/build_strongest_candidate_deep_dive.py",
    "protocols/strongest_candidate_deep_dive.toml",
    "scripts/build_gog_magog_pair_prospective_report.py",
    "scripts/download_wrr_sources.py",
    "scripts/build_wrr_source_recovery_probe.py",
    "scripts/import_wrr_terms.py",
    "scripts/analyze_wrr_source_shapes.py",
    "scripts/analyze_wrr_audit_counts.py",
    "scripts/analyze_wrr_zero_hit_variant_probe.py",
    "scripts/analyze_wrr_text_source.py",
    "scripts/analyze_wrr_pair_audit.py",
    "scripts/analyze_wrr_pair_controls.py",
    "scripts/analyze_wrr_skip_caps.py",
    "scripts/analyze_wrr_pair_table_reconciliation.py",
    "scripts/analyze_wrr_perturbation_diagnostics.py",
    "scripts/build_wrr_cross_pair_grid.py",
    "scripts/analyze_wrr_corrected_distance.py",
    "scripts/analyze_wrr_corrected_distance_aggregate.py",
    "scripts/analyze_wrr_cross_pair_permutations.py",
    "scripts/check_wrr_cross_pair_grid_doc.py",
    "scripts/check_wrr_direct_all_lanes_doc.py",
    "scripts/analyze_wrr_defined_pair_set.py",
    "scripts/analyze_wrr_defined_gap_reasons.py",
    "scripts/analyze_wrr_variant_gap_impact.py",
    "scripts/analyze_wrr_variant_gap_upper_bound.py",
    "scripts/build_wrr_variant_residual_review_packet.py",
    "scripts/build_wrr_residual_term_reconciliation_queue.py",
    "scripts/build_wrr_residual_reconciliation_action_plan.py",
    "scripts/build_wrr_source_review_queue.py",
    "scripts/check_wrr_source_review_queue_doc.py",
    "scripts/check_wrr_source_visual_review_notes_doc.py",
    "scripts/analyze_wrr_source_policy_scenarios.py",
    "scripts/build_wrr_source_policy_evidence_packet.py",
    "scripts/check_wrr_source_policy_evidence_packet_doc.py",
    "scripts/build_wrr_source_policy_review_checklist.py",
    "scripts/check_wrr_source_policy_review_checklist_doc.py",
    "scripts/build_wrr_source_transcription_evidence_packet.py",
    "scripts/check_wrr_source_transcription_evidence_packet_doc.py",
    "scripts/build_wrr_source_transcription_row_review_checklist.py",
    "scripts/check_wrr_source_transcription_row_review_checklist_doc.py",
    "scripts/build_wrr_remaining_lane_evidence_packets.py",
    "scripts/check_wrr_remaining_lane_evidence_packets_doc.py",
    "scripts/build_wrr_remaining_lane_review_checklist.py",
    "scripts/check_wrr_remaining_lane_review_checklist_doc.py",
    "scripts/build_wrr_manual_decision_register.py",
    "scripts/build_wrr_manual_decision_record_worksheet.py",
    "scripts/check_wrr_manual_decision_record_worksheet_doc.py",
    "scripts/check_wrr_manual_decision_records.py",
    "scripts/check_wrr_manual_decision_register_doc.py",
    "scripts/build_wrr_method_pair_universe_evidence_packet.py",
    "scripts/check_wrr_method_pair_universe_evidence_packet_doc.py",
    "scripts/check_wrr_source_policy_scenarios_doc.py",
    "scripts/analyze_wrr_dw_formula_sensitivity.py",
    "scripts/check_wrr_dw_formula_sensitivity_doc.py",
    "scripts/build_wrr_method_status.py",
    "scripts/check_wrr_claim_readiness.py",
    "scripts/check_wrr_claim_readiness_doc.py",
    "scripts/check_wrr_claim_blocker_packet_doc.py",
    "scripts/build_wrr_locked_method_report.py",
    "scripts/check_wrr_locked_method_report_doc.py",
    "scripts/build_wrr_exact_reproduction_gap_dashboard.py",
    "scripts/check_wrr_exact_reproduction_gap_dashboard_doc.py",
    "scripts/check_wrr_public_handoff_docs.py",
    "scripts/check_wrr_defined_diagnostic_docs.py",
    "scripts/check_wrr_lock_options_doc.py",
    "scripts/check_wrr_method_status_doc.py",
    "scripts/check_wrr_residual_term_reconciliation_queue_doc.py",
    "scripts/check_wrr_residual_reconciliation_action_plan_doc.py",
    "scripts/check_wrr_source_recovery_probe_doc.py",
    "scripts/build_wrr_wayback_source_recovery_probe.py",
    "scripts/check_wrr_wayback_source_recovery_probe_doc.py",
    "scripts/check_hypothesis_testing_source_audit_doc.py",
    "scripts/check_wrr_variant_gap_docs.py",
    "scripts/build_wrr_claim_blocker_packet.py",
    "scripts/build_matrix_cluster_candidates.py",
    "scripts/summarize_matrix_cluster_controls.py",
    "scripts/analyze_notable_passage_gaps.py",
    "scripts/build_boundary_alignment.py",
    "scripts/build_chapter_position_bias.py",
    "scripts/build_direction_asymmetry.py",
    "scripts/build_canonical_first_summary.py",
    "scripts/build_cross_skip_summary.py",
    "scripts/build_review_flag_summary.py",
    "scripts/build_cohort_cluster_density.py",
    "protocols/greek_surface_prospective.toml",
    "protocols/greek_surface_length4_followup.toml",
    "protocols/greek_surface_length4_vocabulary_controls.toml",
    "protocols/hebrew_theology_all_codes_collection.toml",
    "protocols/hebrew_screening_all_codes_collection.toml",
    "protocols/greek_screening_all_codes_collection.toml",
    "protocols/wrr_audit_counts.toml",
    "protocols/wrr_source_recovery_probe.toml",
    "protocols/wrr_wayback_source_recovery_probe.toml",
    "terms/relevance_dictionary.toml",
    "prompts/crd_classifier_v1/system.md",
    "prompts/crd_classifier_v1/user_template.md",
    "terms/theological_terms.csv",
    "terms/modern_names_dates.csv",
    "terms/greek_nt_claim_terms.csv",
    "terms/greek_expanded_prospective_terms.csv",
    "terms/greek_surface_prospective_terms.csv",
    "terms/null_controls.csv",
    "terms/frequency_anchors.csv",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    root = Path.cwd()
    failures: list[str] = []

    git_status = git_status_short(root)
    if git_status and not args.allow_dirty:
        failures.append("git working tree is not clean")

    remotes = git_remotes(root)
    failures.extend(remote_owner_failures(remotes))

    forbidden_repo_hits = scan_forbidden_terms(root)
    if forbidden_repo_hits:
        failures.append(
            "forbidden account text found in repository files: "
            + ", ".join(forbidden_repo_hits[:5])
        )

    tracked_paths = git_tracked_paths(root)
    risky_paths = risky_tracked_paths(tracked_paths)
    if risky_paths:
        failures.append("risky tracked paths: " + ", ".join(risky_paths[:10]))

    forbidden_tracked_hits = scan_tracked_for_forbidden_account(root, tracked_paths)
    if forbidden_tracked_hits:
        failures.append(
            "forbidden account text in tracked files: "
            + ", ".join(forbidden_tracked_hits[:10])
        )

    secret_hits = scan_tracked_for_secret_patterns(root, tracked_paths)
    if secret_hits:
        failures.append(
            "high-confidence secret patterns in tracked files: "
            + ", ".join(format_finding(hit) for hit in secret_hits[:10])
        )

    missing_paths = [path for path in required_paths(args) if not (root / path).exists()]
    if missing_paths:
        failures.append("missing required paths: " + ", ".join(missing_paths))

    prospective_lane_failures = check_prospective_study_lanes.validate_profiles(
        root / check_prospective_study_lanes.DEFAULT_PROFILE_FILE
    )
    if prospective_lane_failures:
        failures.append(
            "prospective lane validation failures: "
            + "; ".join(prospective_lane_failures)
        )

    source_basis_failures = check_source_basis_audit_queue.validate_source_basis_queue(
        biblegateway_manifest=root / check_source_basis_audit_queue.DEFAULT_BIBLEGATEWAY_MANIFEST,
        ebible_controls=root / check_source_basis_audit_queue.DEFAULT_EBIBLE_CONTROLS,
        door43_controls=root / check_source_basis_audit_queue.DEFAULT_DOOR43_CONTROLS,
        oet_controls=root / check_source_basis_audit_queue.DEFAULT_OET_CONTROLS,
        otb_controls=root / check_source_basis_audit_queue.DEFAULT_OTB_CONTROLS,
        openbible_controls=root / check_source_basis_audit_queue.DEFAULT_OPENBIBLE_CONTROLS,
        odr_controls=root / check_source_basis_audit_queue.DEFAULT_ODR_CONTROLS,
        supplemental_controls=root / check_source_basis_audit_queue.DEFAULT_SUPPLEMENTAL_CONTROLS,
        audit_queue=root / check_source_basis_audit_queue.DEFAULT_AUDIT_QUEUE,
    )
    if source_basis_failures:
        failures.append(
            "source-basis validation failures: "
            + "; ".join(source_basis_failures)
        )

    english_corpus_policy_failures = (
        check_english_corpus_policy_docs.validate_policy_docs(root)
    )
    if english_corpus_policy_failures:
        failures.append(
            "English corpus policy failures: "
            + "; ".join(english_corpus_policy_failures)
        )

    expanded_strata_tooling_result = check_expanded_strata_tooling.check_tooling(
        check_expanded_strata_tooling.DEFAULT_DOC,
        check_expanded_strata_tooling.DEFAULT_MAKEFILE,
    )
    expanded_strata_tooling_failures = [
        str(item)
        for item in expanded_strata_tooling_result.get("missing", [])
    ]
    if expanded_strata_tooling_failures:
        failures.append(
            "expanded-strata tooling failures: "
            + "; ".join(expanded_strata_tooling_failures)
        )

    public_claim_language_failures = (
        check_public_claim_language.validate_public_claim_language()
    )
    if public_claim_language_failures:
        failures.append(
            "public claim-language failures: "
            + "; ".join(public_claim_language_failures)
        )

    doc_command_reference_failures = (
        check_doc_command_references.validate_doc_command_references(root)
    )
    if doc_command_reference_failures:
        failures.append(
            "doc command-reference failures: "
            + "; ".join(doc_command_reference_failures)
        )

    study_mapping_schema_failures = validate_study_mapping_schemas.validate_mapping_dir(
        validate_study_mapping_schemas.MAPPINGS_DIR
    )
    if study_mapping_schema_failures:
        failures.append(
            "study mapping schema failures: "
            + "; ".join(study_mapping_schema_failures)
        )

    preregistration_placeholder_paths = concrete_preregistration_paths(root)
    preregistration_placeholder_failures = find_preregistration_placeholder_failures(
        preregistration_placeholder_paths
    )
    if preregistration_placeholder_failures:
        failures.append(
            "preregistration placeholder failures: "
            + "; ".join(preregistration_placeholder_failures)
        )

    crd_relevance_dictionary_failures = check_crd_relevance_dictionary_lock()
    if crd_relevance_dictionary_failures:
        failures.append(
            "CRD relevance dictionary failures: "
            + "; ".join(crd_relevance_dictionary_failures)
        )

    manual_review_queue_failures = check_manual_review_queue.validate_manual_review_queue(
        check_manual_review_queue.DEFAULT_DOC
    )
    if manual_review_queue_failures:
        failures.append(
            "manual review queue failures: "
            + "; ".join(manual_review_queue_failures)
        )

    wrr_claim_readiness_doc_failures = (
        check_wrr_claim_readiness_doc.validate_readiness_doc(
            check_wrr_claim_readiness_doc.DEFAULT_DOC
        )
    )
    if wrr_claim_readiness_doc_failures:
        failures.append(
            "WRR claim-readiness doc failures: "
            + "; ".join(wrr_claim_readiness_doc_failures)
        )

    wrr_claim_blocker_packet_doc_failures = (
        check_wrr_claim_blocker_packet_doc.validate_blocker_packet_doc(
            check_wrr_claim_blocker_packet_doc.DEFAULT_DOC
        )
    )
    if wrr_claim_blocker_packet_doc_failures:
        failures.append(
            "WRR claim-blocker packet failures: "
            + "; ".join(wrr_claim_blocker_packet_doc_failures)
        )

    wrr_locked_method_report_doc_failures = (
        check_wrr_locked_method_report_doc.validate_locked_method_report_doc(
            check_wrr_locked_method_report_doc.DEFAULT_DOC
        )
    )
    if wrr_locked_method_report_doc_failures:
        failures.append(
            "WRR locked-method report failures: "
            + "; ".join(wrr_locked_method_report_doc_failures)
        )

    wrr_exact_reproduction_gap_dashboard_doc_failures = (
        check_wrr_exact_reproduction_gap_dashboard_doc.validate_gap_dashboard_doc(
            check_wrr_exact_reproduction_gap_dashboard_doc.DEFAULT_DOC
        )
    )
    if wrr_exact_reproduction_gap_dashboard_doc_failures:
        failures.append(
            "WRR exact-reproduction gap dashboard failures: "
            + "; ".join(wrr_exact_reproduction_gap_dashboard_doc_failures)
        )

    wrr_public_handoff_doc_failures = (
        check_wrr_public_handoff_docs.validate_public_handoff_docs()
    )
    if wrr_public_handoff_doc_failures:
        failures.append(
            "WRR public handoff doc failures: "
            + "; ".join(wrr_public_handoff_doc_failures)
        )

    wrr_defined_diagnostic_doc_failures = (
        check_wrr_defined_diagnostic_docs.validate_defined_diagnostic_docs()
    )
    if wrr_defined_diagnostic_doc_failures:
        failures.append(
            "WRR defined diagnostic doc failures: "
            + "; ".join(wrr_defined_diagnostic_doc_failures)
        )

    wrr_variant_gap_doc_failures = check_wrr_variant_gap_docs.validate_variant_gap_docs()
    if wrr_variant_gap_doc_failures:
        failures.append(
            "WRR variant-gap doc failures: "
            + "; ".join(wrr_variant_gap_doc_failures)
        )

    wrr_residual_term_reconciliation_doc_failures = (
        check_wrr_residual_term_reconciliation_queue_doc.validate_residual_term_reconciliation_queue_doc(
            check_wrr_residual_term_reconciliation_queue_doc.DEFAULT_DOC
        )
    )
    if wrr_residual_term_reconciliation_doc_failures:
        failures.append(
            "WRR residual term reconciliation doc failures: "
            + "; ".join(wrr_residual_term_reconciliation_doc_failures)
        )

    wrr_residual_reconciliation_action_plan_doc_failures = (
        check_wrr_residual_reconciliation_action_plan_doc.validate_residual_reconciliation_action_plan_doc(
            check_wrr_residual_reconciliation_action_plan_doc.DEFAULT_DOC
        )
    )
    if wrr_residual_reconciliation_action_plan_doc_failures:
        failures.append(
            "WRR residual reconciliation action-plan failures: "
            + "; ".join(wrr_residual_reconciliation_action_plan_doc_failures)
        )

    wrr_source_review_queue_doc_failures = (
        check_wrr_source_review_queue_doc.validate_source_review_queue_doc(
            check_wrr_source_review_queue_doc.DEFAULT_DOC
        )
    )
    if wrr_source_review_queue_doc_failures:
        failures.append(
            "WRR source-review queue doc failures: "
            + "; ".join(wrr_source_review_queue_doc_failures)
        )

    wrr_source_visual_review_notes_doc_failures = (
        check_wrr_source_visual_review_notes_doc.validate_source_visual_review_notes_doc(
            check_wrr_source_visual_review_notes_doc.DEFAULT_DOC
        )
    )
    if wrr_source_visual_review_notes_doc_failures:
        failures.append(
            "WRR source visual-review notes doc failures: "
            + "; ".join(wrr_source_visual_review_notes_doc_failures)
        )

    wrr_source_policy_evidence_packet_doc_failures = (
        check_wrr_source_policy_evidence_packet_doc.validate_source_policy_evidence_packet_doc(
            check_wrr_source_policy_evidence_packet_doc.DEFAULT_DOC
        )
    )
    if wrr_source_policy_evidence_packet_doc_failures:
        failures.append(
            "WRR source-policy evidence packet failures: "
            + "; ".join(wrr_source_policy_evidence_packet_doc_failures)
        )

    wrr_source_policy_review_checklist_doc_failures = (
        check_wrr_source_policy_review_checklist_doc.validate_source_policy_review_checklist_doc(
            check_wrr_source_policy_review_checklist_doc.DEFAULT_DOC
        )
    )
    if wrr_source_policy_review_checklist_doc_failures:
        failures.append(
            "WRR source-policy checklist failures: "
            + "; ".join(wrr_source_policy_review_checklist_doc_failures)
        )

    wrr_source_transcription_evidence_packet_doc_failures = (
        check_wrr_source_transcription_evidence_packet_doc.validate_source_transcription_evidence_packet_doc(
            check_wrr_source_transcription_evidence_packet_doc.DEFAULT_DOC
        )
    )
    if wrr_source_transcription_evidence_packet_doc_failures:
        failures.append(
            "WRR source-transcription evidence packet failures: "
            + "; ".join(wrr_source_transcription_evidence_packet_doc_failures)
        )

    wrr_source_transcription_row_review_checklist_doc_failures = (
        check_wrr_source_transcription_row_review_checklist_doc.validate_row_review_checklist_doc(
            check_wrr_source_transcription_row_review_checklist_doc.DEFAULT_DOC
        )
    )
    if wrr_source_transcription_row_review_checklist_doc_failures:
        failures.append(
            "WRR source-transcription row checklist failures: "
            + "; ".join(wrr_source_transcription_row_review_checklist_doc_failures)
        )

    wrr_remaining_lane_evidence_packets_doc_failures = (
        check_wrr_remaining_lane_evidence_packets_doc.validate_remaining_lane_evidence_packets_doc(
            check_wrr_remaining_lane_evidence_packets_doc.DEFAULT_DOC
        )
    )
    if wrr_remaining_lane_evidence_packets_doc_failures:
        failures.append(
            "WRR remaining-lane evidence packet failures: "
            + "; ".join(wrr_remaining_lane_evidence_packets_doc_failures)
        )

    wrr_remaining_lane_review_checklist_doc_failures = (
        check_wrr_remaining_lane_review_checklist_doc.validate_remaining_lane_review_checklist_doc(
            check_wrr_remaining_lane_review_checklist_doc.DEFAULT_DOC
        )
    )
    if wrr_remaining_lane_review_checklist_doc_failures:
        failures.append(
            "WRR remaining-lane checklist failures: "
            + "; ".join(wrr_remaining_lane_review_checklist_doc_failures)
        )

    wrr_manual_decision_register_doc_failures = (
        check_wrr_manual_decision_register_doc.validate_manual_decision_register_doc(
            check_wrr_manual_decision_register_doc.DEFAULT_DOC
        )
    )
    if wrr_manual_decision_register_doc_failures:
        failures.append(
            "WRR manual decision register failures: "
            + "; ".join(wrr_manual_decision_register_doc_failures)
        )

    wrr_manual_decision_record_worksheet_doc_failures = (
        check_wrr_manual_decision_record_worksheet_doc.validate_worksheet_doc(
            check_wrr_manual_decision_record_worksheet_doc.DEFAULT_DOC
        )
    )
    if wrr_manual_decision_record_worksheet_doc_failures:
        failures.append(
            "WRR manual decision record worksheet failures: "
            + "; ".join(wrr_manual_decision_record_worksheet_doc_failures)
        )

    wrr_manual_decision_record_failures = (
        check_wrr_manual_decision_records.validate_decision_records(
            check_wrr_manual_decision_records.DEFAULT_RECORDS,
            check_wrr_manual_decision_records.DEFAULT_REGISTER_DOC,
        )
    )
    if wrr_manual_decision_record_failures:
        failures.append(
            "WRR manual decision record failures: "
            + "; ".join(wrr_manual_decision_record_failures)
        )

    wrr_method_pair_universe_evidence_packet_doc_failures = (
        check_wrr_method_pair_universe_evidence_packet_doc.validate_method_pair_universe_evidence_packet_doc(
            check_wrr_method_pair_universe_evidence_packet_doc.DEFAULT_DOC
        )
    )
    if wrr_method_pair_universe_evidence_packet_doc_failures:
        failures.append(
            "WRR method/pair-universe evidence packet failures: "
            + "; ".join(wrr_method_pair_universe_evidence_packet_doc_failures)
        )

    wrr_dw_formula_sensitivity_doc_failures = (
        check_wrr_dw_formula_sensitivity_doc.validate_dw_formula_sensitivity_doc(
            check_wrr_dw_formula_sensitivity_doc.DEFAULT_DOC
        )
    )
    if wrr_dw_formula_sensitivity_doc_failures:
        failures.append(
            "WRR D(w) formula sensitivity doc failures: "
            + "; ".join(wrr_dw_formula_sensitivity_doc_failures)
        )

    wrr_source_policy_scenarios_doc_failures = (
        check_wrr_source_policy_scenarios_doc.validate_source_policy_scenarios_doc(
            check_wrr_source_policy_scenarios_doc.DEFAULT_DOC
        )
    )
    if wrr_source_policy_scenarios_doc_failures:
        failures.append(
            "WRR source-policy scenarios doc failures: "
            + "; ".join(wrr_source_policy_scenarios_doc_failures)
        )

    wrr_cross_pair_grid_doc_failures = (
        check_wrr_cross_pair_grid_doc.validate_cross_pair_grid_doc(
            check_wrr_cross_pair_grid_doc.DEFAULT_DOC
        )
    )
    if wrr_cross_pair_grid_doc_failures:
        failures.append(
            "WRR cross-pair grid doc failures: "
            + "; ".join(wrr_cross_pair_grid_doc_failures)
        )

    wrr_direct_all_lanes_doc_failures = (
        check_wrr_direct_all_lanes_doc.validate_direct_all_lanes_doc(
            check_wrr_direct_all_lanes_doc.DEFAULT_DOC
        )
    )
    if wrr_direct_all_lanes_doc_failures:
        failures.append(
            "WRR direct all-lane doc failures: "
            + "; ".join(wrr_direct_all_lanes_doc_failures)
        )

    wrr_lock_options_doc_failures = (
        check_wrr_lock_options_doc.validate_lock_options_doc(
            check_wrr_lock_options_doc.DEFAULT_DOC
        )
    )
    if wrr_lock_options_doc_failures:
        failures.append(
            "WRR lock-options doc failures: "
            + "; ".join(wrr_lock_options_doc_failures)
        )

    wrr_method_status_doc_failures = (
        check_wrr_method_status_doc.validate_method_status_doc(
            check_wrr_method_status_doc.DEFAULT_DOC
        )
    )
    if wrr_method_status_doc_failures:
        failures.append(
            "WRR method-status doc failures: "
            + "; ".join(wrr_method_status_doc_failures)
        )

    wrr_source_recovery_probe_doc_failures = (
        check_wrr_source_recovery_probe_doc.validate_source_recovery_probe_doc(
            check_wrr_source_recovery_probe_doc.DEFAULT_DOC
        )
    )
    if wrr_source_recovery_probe_doc_failures:
        failures.append(
            "WRR source-recovery probe doc failures: "
            + "; ".join(wrr_source_recovery_probe_doc_failures)
        )

    wrr_wayback_source_recovery_probe_doc_failures = (
        check_wrr_wayback_source_recovery_probe_doc.validate_wayback_source_recovery_probe_doc(
            check_wrr_wayback_source_recovery_probe_doc.DEFAULT_DOC
        )
    )
    if wrr_wayback_source_recovery_probe_doc_failures:
        failures.append(
            "WRR Wayback source-recovery probe doc failures: "
            + "; ".join(wrr_wayback_source_recovery_probe_doc_failures)
        )

    hypothesis_testing_source_audit_doc_failures = (
        check_hypothesis_testing_source_audit_doc.validate_hypothesis_testing_source_audit_doc(
            check_hypothesis_testing_source_audit_doc.DEFAULT_DOC
        )
    )
    if hypothesis_testing_source_audit_doc_failures:
        failures.append(
            "hypothesis-testing source audit doc failures: "
            + "; ".join(hypothesis_testing_source_audit_doc_failures)
        )

    stale_indexes = stale_generated_indexes(root)
    if stale_indexes:
        failures.append("stale generated indexes: " + ", ".join(stale_indexes))

    payload = {
        "tool": "preflight_real_report_run",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "status": "failed" if failures else "passed",
        "output_path": str(args.out),
        "allow_dirty": args.allow_dirty,
        "git_commit": git_commit(root),
        "git_status_lines": git_status,
        "git_remotes": remotes,
        "tracked_path_count": len(tracked_paths),
        "risky_tracked_paths": risky_paths,
        "required_paths": required_paths(args),
        "missing_paths": missing_paths,
        "prospective_lane_failures": prospective_lane_failures,
        "source_basis_failures": source_basis_failures,
        "english_corpus_policy_failures": english_corpus_policy_failures,
        "expanded_strata_tooling_failures": expanded_strata_tooling_failures,
        "public_claim_language_failures": public_claim_language_failures,
        "doc_command_reference_failures": doc_command_reference_failures,
        "study_mapping_schema_failures": study_mapping_schema_failures,
        "preregistration_placeholder_paths": [
            str(path) for path in preregistration_placeholder_paths
        ],
        "preregistration_placeholder_failures": preregistration_placeholder_failures,
        "crd_relevance_dictionary_failures": crd_relevance_dictionary_failures,
        "manual_review_queue_failures": manual_review_queue_failures,
        "wrr_claim_readiness_doc_failures": wrr_claim_readiness_doc_failures,
        "wrr_claim_blocker_packet_doc_failures": (
            wrr_claim_blocker_packet_doc_failures
        ),
        "wrr_locked_method_report_doc_failures": (
            wrr_locked_method_report_doc_failures
        ),
        "wrr_exact_reproduction_gap_dashboard_doc_failures": (
            wrr_exact_reproduction_gap_dashboard_doc_failures
        ),
        "wrr_public_handoff_doc_failures": wrr_public_handoff_doc_failures,
        "wrr_defined_diagnostic_doc_failures": wrr_defined_diagnostic_doc_failures,
        "wrr_variant_gap_doc_failures": wrr_variant_gap_doc_failures,
        "wrr_residual_term_reconciliation_doc_failures": (
            wrr_residual_term_reconciliation_doc_failures
        ),
        "wrr_residual_reconciliation_action_plan_doc_failures": (
            wrr_residual_reconciliation_action_plan_doc_failures
        ),
        "wrr_source_review_queue_doc_failures": wrr_source_review_queue_doc_failures,
        "wrr_source_visual_review_notes_doc_failures": (
            wrr_source_visual_review_notes_doc_failures
        ),
        "wrr_source_policy_evidence_packet_doc_failures": (
            wrr_source_policy_evidence_packet_doc_failures
        ),
        "wrr_source_policy_review_checklist_doc_failures": (
            wrr_source_policy_review_checklist_doc_failures
        ),
        "wrr_source_transcription_evidence_packet_doc_failures": (
            wrr_source_transcription_evidence_packet_doc_failures
        ),
        "wrr_source_transcription_row_review_checklist_doc_failures": (
            wrr_source_transcription_row_review_checklist_doc_failures
        ),
        "wrr_remaining_lane_evidence_packets_doc_failures": (
            wrr_remaining_lane_evidence_packets_doc_failures
        ),
        "wrr_remaining_lane_review_checklist_doc_failures": (
            wrr_remaining_lane_review_checklist_doc_failures
        ),
        "wrr_manual_decision_register_doc_failures": (
            wrr_manual_decision_register_doc_failures
        ),
        "wrr_manual_decision_record_worksheet_doc_failures": (
            wrr_manual_decision_record_worksheet_doc_failures
        ),
        "wrr_manual_decision_record_failures": wrr_manual_decision_record_failures,
        "wrr_method_pair_universe_evidence_packet_doc_failures": (
            wrr_method_pair_universe_evidence_packet_doc_failures
        ),
        "wrr_dw_formula_sensitivity_doc_failures": (
            wrr_dw_formula_sensitivity_doc_failures
        ),
        "wrr_source_policy_scenarios_doc_failures": (
            wrr_source_policy_scenarios_doc_failures
        ),
        "wrr_cross_pair_grid_doc_failures": wrr_cross_pair_grid_doc_failures,
        "wrr_direct_all_lanes_doc_failures": wrr_direct_all_lanes_doc_failures,
        "wrr_lock_options_doc_failures": wrr_lock_options_doc_failures,
        "wrr_method_status_doc_failures": wrr_method_status_doc_failures,
        "wrr_source_recovery_probe_doc_failures": wrr_source_recovery_probe_doc_failures,
        "wrr_wayback_source_recovery_probe_doc_failures": (
            wrr_wayback_source_recovery_probe_doc_failures
        ),
        "hypothesis_testing_source_audit_doc_failures": hypothesis_testing_source_audit_doc_failures,
        "stale_generated_indexes": stale_indexes,
        "forbidden_account_terms": FORBIDDEN_ACCOUNT_TERMS,
        "forbidden_repo_hits": forbidden_repo_hits,
        "forbidden_tracked_hits": forbidden_tracked_hits,
        "secret_pattern_hits": [hit.as_dict() for hit in secret_hits],
        "failures": failures,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(args.out)
    if failures:
        for failure in failures:
            print(f"preflight failure: {failure}")
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--required-path", action="append", default=[])
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--out", type=Path, default=OUT)
    return parser


def required_paths(args: argparse.Namespace) -> list[str]:
    return [*DEFAULT_REQUIRED_PATHS, *args.required_path]


def stale_generated_indexes(root: Path) -> list[str]:
    stale: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        docs_out = tmp_root / "docs_INDEX.md"
        docs_root = root / "docs"
        docs_index = docs_root / "INDEX.md"
        if docs_root.exists() and docs_index.exists():
            write_docs_index(
                scan_markdown_docs(docs_root),
                docs_out,
                docs_root=Path("docs"),
            )
            if (
                docs_out.read_text(encoding="utf-8")
                != docs_index.read_text(encoding="utf-8")
            ):
                stale.append("docs/INDEX.md")

        protocols_out = tmp_root / "protocols_INDEX.md"
        protocols_root = root / "protocols"
        protocols_index = protocols_root / "INDEX.md"
        if protocols_root.exists() and protocols_index.exists():
            write_protocol_index(
                scan_protocols(protocols_root),
                protocols_out,
                protocols_root=Path("protocols"),
            )
            if (
                protocols_out.read_text(encoding="utf-8")
                != protocols_index.read_text(encoding="utf-8")
            ):
                stale.append("protocols/INDEX.md")
    return stale


def concrete_preregistration_paths(root: Path) -> list[Path]:
    template = Path("docs/PROSPECTIVE_STUDY_PREREGISTRATION_TEMPLATE.md")
    docs_root = root / "docs"
    return [
        Path("docs") / path.name
        for path in sorted(docs_root.glob("*PREREG*.md"))
        if Path("docs") / path.name != template
    ]


def find_preregistration_placeholder_failures(paths: list[Path]) -> list[str]:
    failures: list[str] = []
    for path in paths:
        for hit in check_preregistration_placeholders.find_placeholders(
            path,
            allowed=set(),
        ):
            failures.append(
                f"{hit.path}:{hit.line_number}:{hit.column_number}: {hit.placeholder}"
            )
    return failures


def check_crd_relevance_dictionary_lock(
    protocol_path: Path = Path("protocols/centered_relevance_density.toml"),
) -> list[str]:
    try:
        protocol = tomllib.loads(protocol_path.read_text(encoding="utf-8"))
        term_file = protocol.get("term_file")
        dictionary = protocol.get("relevance_dictionary")
        expected_sha256 = protocol.get("relevance_dictionary_sha256")
        if not isinstance(term_file, str) or not term_file.strip():
            return [f"{protocol_path}: missing term_file"]
        if not isinstance(dictionary, str) or not dictionary.strip():
            return [f"{protocol_path}: missing relevance_dictionary"]
        if not isinstance(expected_sha256, str) or not expected_sha256.strip():
            return [f"{protocol_path}: missing relevance_dictionary_sha256"]
        report = check_crd_relevance_dictionary.check_dictionary(
            dictionary=Path(dictionary),
            term_files=[Path(term_file)],
            require_reviewed=True,
            expected_sha256=expected_sha256,
        )
    except Exception as exc:
        return [str(exc)]
    if report["missing_entries"]:
        return [f"{dictionary}: missing entries: {report['missing_entries']}"]
    if report["extra_entries"]:
        return [f"{dictionary}: extra entries: {report['extra_entries']}"]
    return []


def git_status_short(root: Path) -> list[str]:
    return run_git(root, "status", "--short")


def git_commit(root: Path) -> str:
    rows = run_git(root, "rev-parse", "--short", "HEAD")
    return rows[0] if rows else ""


def git_remotes(root: Path) -> list[str]:
    return run_git(root, "remote", "-v")


def run_git(root: Path, *args: str) -> list[str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    output = completed.stdout.strip()
    if not output:
        return []
    return output.splitlines()


def scan_forbidden_terms(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob("*"):
        if should_skip(path, root):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue
        found = forbidden_hits(text)
        if found:
            hits.append(f"{path.relative_to(root)}:{','.join(sorted(found))}")
    return hits


def should_skip(path: Path, root: Path) -> bool:
    if not path.is_file():
        return True
    relative = path.relative_to(root)
    skip_parts = {
        ".git",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "data",
        "reports",
    }
    return any(part in skip_parts for part in relative.parts)


if __name__ == "__main__":
    raise SystemExit(main())
