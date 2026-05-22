#!/usr/bin/env python3
"""Preflight checks for a formal report assembly run."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
import time
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
    check_expanded_strata_tooling,
    check_preregistration_placeholders,
    check_prospective_study_lanes,
    check_source_basis_audit_queue,
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
    "els/project_index.py",
    "Makefile",
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
    "docs/RESEARCH_MISSING_MODEL_PAGES_AUDIT.md",
    "docs/WRR_REPLICATION_PLAN.md",
    "docs/WRR_METHOD_STATUS.md",
    "docs/WRR_LOCK_OPTIONS.md",
    "docs/WRR_DEFINED_PAIR_SET_AUDIT.md",
    "docs/WRR_DEFINED_GAP_REASON_AUDIT.md",
    "docs/WRR_METHODOLOGY_GAPS.md",
    "docs/WRR_CORRECTED_DISTANCE_NOTES.md",
    "docs/WRR_CROSS_PAIR_GRID.md",
    "docs/WRR_CLAIM_READINESS.md",
    "docs/WRR_CLAIM_BLOCKER_PACKET.md",
    "docs/WRR_SOURCE_POLICY_SCENARIOS.md",
    "docs/WRR_DW_FORMULA_SENSITIVITY.md",
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
    "protocols/biblegateway_english_versions.toml",
    "protocols/ebible_english_controls.toml",
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
    "scripts/check_expanded_strata_tooling.py",
    "scripts/validate_study_mapping_schemas.py",
    "els/match_strata.py",
    "els/gematria.py",
    "els/letter_stats.py",
    "els/term_display.py",
    "terms/meaningful_constants.csv",
    "scripts/build_final_report_highlights.py",
    "scripts/build_gog_magog_pair_prospective_report.py",
    "scripts/download_wrr_sources.py",
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
    "scripts/analyze_wrr_defined_pair_set.py",
    "scripts/analyze_wrr_defined_gap_reasons.py",
    "scripts/analyze_wrr_variant_gap_impact.py",
    "scripts/build_wrr_source_review_queue.py",
    "scripts/analyze_wrr_source_policy_scenarios.py",
    "scripts/analyze_wrr_dw_formula_sensitivity.py",
    "scripts/build_wrr_method_status.py",
    "scripts/check_wrr_claim_readiness.py",
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
        audit_queue=root / check_source_basis_audit_queue.DEFAULT_AUDIT_QUEUE,
    )
    if source_basis_failures:
        failures.append(
            "source-basis validation failures: "
            + "; ".join(source_basis_failures)
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
        "expanded_strata_tooling_failures": expanded_strata_tooling_failures,
        "study_mapping_schema_failures": study_mapping_schema_failures,
        "preregistration_placeholder_paths": [
            str(path) for path in preregistration_placeholder_paths
        ],
        "preregistration_placeholder_failures": preregistration_placeholder_failures,
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
