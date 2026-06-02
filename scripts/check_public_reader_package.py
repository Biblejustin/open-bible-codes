#!/usr/bin/env python3
"""Validate a generated public-reader package against its manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tomllib
from pathlib import Path
from typing import Any

from scripts import build_public_reader_package as builder


DEFAULT_PACKAGE_DIR = builder.DEFAULT_OUT_DIR
REQUIRED_GENERATED_FILES = (
    Path("README.md"),
    Path("package_manifest.json"),
    Path("reader_package.md"),
)
REAL_REPORT_SUMMARY_SOURCE = Path("reports/real_report_run/summary.md")
REAL_REPORT_MANIFEST_SOURCE = Path("reports/real_report_run/manifest.json")
REAL_REPORT_PREFLIGHT_SOURCE = Path("reports/real_report_run/preflight.json")
REAL_REPORT_PROTOCOL_MANIFEST_SOURCE = Path(
    "reports/real_report_run/protocol_run.manifest.json"
)
REAL_REPORT_PROTOCOL_SOURCE = Path("protocols/real_report_run.toml")
REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH = {
    Path("docs/START_HERE.md"): (
        "8. `docs/WRR_NO_INPUT_HANDOFF_STATUS.md` for exact WRR source/method status.",
        "9. `docs/KJVA_NO_INPUT_HANDOFF_STATUS.md` for KJVA source-lock status.",
        "10. `docs/CITIES_NO_INPUT_HANDOFF_STATUS.md` for Cities source-chain status.",
    ),
    Path("docs/PROJECT_FINDINGS_OVERVIEW.md"): (
        "`docs/REMAINING_WORK_REGISTER.md`",
        "`docs/WRR_NO_INPUT_HANDOFF_STATUS.md`",
        "`docs/KJVA_NO_INPUT_HANDOFF_STATUS.md`",
        "`docs/CITIES_NO_INPUT_HANDOFF_STATUS.md`",
        "The KJV with Apocrypha work found bridge patterns that stood above several",
        "comparison checks. This area deserves more review, but it came from earlier",
        "candidate-source audit rows, but 0 candidate pages ready to import verses and",
        "0 candidate pages ready for a result.",
    ),
    Path("docs/FINAL_REPORT.md"): (
        "`docs/REMAINING_WORK_REGISTER.md`",
        "`docs/WRR_NO_INPUT_HANDOFF_STATUS.md`",
        "`docs/KJVA_NO_INPUT_HANDOFF_STATUS.md`",
        "`docs/CITIES_NO_INPUT_HANDOFF_STATUS.md`",
        "812 unique term-center presence rows.",
        "809 Bible presence rows and 3 control presence rows.",
        "The bridge pass found 350 boundary-spanning rows.",
        "expanded 250-sample shuffled-insertion control produced 149 to 236 bridge rows",
        "with no shuffled sample at or above the observed 350 (`p_ge=0.003984`).",
        "confirmatory follow-up over those 15 terms found all 15 with `q_ge <= 0.01`",
        "and 3 terms stood above every shuffled sample.",
    ),
    Path("docs/REAL_REPORT_RUN.md"): (
        "Git remotes pointing at `Biblejustin/open-bible-codes`;",
        "WRR no-input handoff status consolidates 9 handoff rows, 8 manual-input-needed rows, the 163 vs 72 defined-distance gap, 37 manual-decision rows, and the no-new-result boundary;",
        "KJVA no-input handoff status consolidates 9 handoff rows, 8 manual-input-needed rows, 11 next-result gates, 7 source-policy blocker rows, the `SIR 44:23` Gutenberg gap, 0/15 Gutenberg Prayer of Manasseh markers, 5719/5720 Hakkaac exact normalized verse matches, 4 candidate-source audit rows, 0 result-ready candidate pages, and the no-new-KJVA-result boundary;",
        "Cities source-row lock handoff stays source-review only: 14 source-row lock candidate pages, 14 populated lock rows, 14 pending transcription-review rows, no source rows imported, and no city-name normalization, ELS searches, compactness runs, or p-levels;",
    ),
    Path("docs/FINAL_REPORT_HIGHLIGHTS.md"): (
        "actual omitted blocks do not break more TR ELS hits than matched random verse blocks",
    ),
    Path("docs/CLAIM_CATALOG.md"): (
        "the consolidated no-input handoff keeps 8 handoff rows, 6 manual-input-needed rows, 14 transcription review rows, 61 OCR packet pages, 41 reviewed OCR packet pages, 20 unreviewed OCR packet pages, 203 priority line-crop review rows, and no Cities result allowed.",
        "Apocrypha bridge-completion study | `mixed` | 2",
        "KJVA bridge rows stand above same-length controls at total and term-review layers plus 250-sample total shuffled controls",
        "locked 5000-sample post-screen controls kept all 15 at q <= 0.01 with 3 above every shuffled sample.",
    ),
    Path("docs/CONSOLIDATED_FINDINGS.md"): (
        "Neither result is public-claim evidence.",
        "4 candidate-source audit rows, 0 candidate verse-import-ready pages, 0 candidate result-ready pages, and result allowed 0.",
        "812 unique term-center presence rows.",
        "839 Bible occurrence rows and 84 control occurrence rows.",
        "83 selected follow-up rows from English screening, Greek screening, Hebrew screening, and Hebrew theology queues",
        "46 deduped compound-extension rows with 250/250 row-local paired controls",
        "149 to 236 shuffled rows against 350 observed rows (`p_ge=0.003984`).",
        "The KJVA term-level bridge review found 48 of 81 bridge terms above all three",
        "15 terms with Benjamini-Hochberg `q_ge <= 0.05`.",
    ),
    Path("docs/STRONGEST_CANDIDATE_DEEP_DIVE.md"): (
        "This page does not make any row a public claim.",
        "main caution: these are review candidates, not settled findings",
        "Post-screen confirmatory: 15/15 terms at q <= 0.01, 3 above every shuffled sample. Prospective lock: 1 bridge row, 0/7 terms at q <= 0.05.",
    ),
    Path("docs/REMAINING_WORK_REGISTER.md"): (
        "Current overview wording now keeps the same no-result boundary visible: 14 source-row lock candidate pages, 14 populated source-row lock rows, 8 handoff rows, 6 manual-input-needed rows, 14 transcription review rows, 61 OCR packet pages, 41 reviewed OCR packet pages, 20 unreviewed OCR packet pages, 203 priority line-crop review rows, and no Cities result allowed.",
    ),
    Path("docs/REPOSITORY_README.md"): (
        "reads 4 candidate-source audit rows with 0 verse-import-ready candidate pages and 0 result-ready candidate pages, records result allowed 0",
    ),
    Path("docs/WRR_NO_INPUT_HANDOFF_STATUS.md"): (
        "Manual-input-needed rows: 8.",
        "Source-cited defined distances: 163.",
        "Current defined distances: 72.",
        "Manual decision rows: 37.",
        "New WRR result allowed: 0.",
    ),
    Path("docs/KJVA_NO_INPUT_HANDOFF_STATUS.md"): (
        "Candidate source audits: 4.",
        "Candidate result-ready pages: 0.",
        "Source-lock ready: 0.",
        "Result allowed: 0.",
        "Claim status: `kjva_no_input_handoff_blocks_new_result`.",
    ),
    Path("docs/CITIES_NO_INPUT_HANDOFF_STATUS.md"): (
        "OCR packet pages: 61.",
        "Reviewed OCR packet pages: 41.",
        "Unreviewed OCR packet pages: 20.",
        "Line crop rows: 203.",
        "Result allowed: 0.",
    ),
    Path("docs/PROSPECTIVE_STUDY_READINESS.md"): (
        "There is no remaining `ready_for_preflight` lane in `configs/prospective_study_lanes.json`.",
        "A new result-producing study now needs a fresh term/source target set and a new clean prospective lock.",
        "Do not call a row a claim because it is hidden, version-stable, or visually interesting.",
    ),
    Path("docs/WRR_LOCKED_METHOD_REPORT.md"): (
        "Status: locked local WRR method report; not an exact published WRR reproduction.",
        "Current source-defined gap: defined 72 of 163; gap 91.",
        "Do not describe this as an exact published WRR reproduction.",
    ),
    Path("docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md"): (
        "Status: exact published WRR reproduction is not closed.",
        "It does not select source corrections, pair exclusions, replacement spellings, or method changes.",
        "Remaining 163-distance gap | 91",
        "This dashboard is a review map, not a reproduction result.",
    ),
    Path("docs/WRR_METHOD_LANE_WIDE_SKIP_PROBE.md"): (
        "It does not choose source corrections, method changes, or pair exclusions.",
        "terms still zero through max skip: 11.",
        "total hits through max skip: 0.",
        "Exact published reproduction remains caveated by the documented 163-distance gap.",
    ),
    Path("docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md"): (
        "It does not transcribe rows, import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.",
        "Evidence rows: 14.",
        "Source-row imports: 0.",
        "No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.",
    ),
    Path("docs/CRITICAL_OMISSION_BREAKS_NULL.md"): (
        "Observed breaks: 558.",
        "Null min/median/max: 525 / 657 / 807.",
        "Greater-or-equal tail: 0.9910.",
        "Raw break counts are not significance tests.",
    ),
    Path("reports/real_report_run/summary.md"): (
        "No row is labeled as a claim in this report run.",
        "It is not an exact WRR reproduction.",
        "Exact published WRR reproduction | forbidden | 72 of 163 defined; gap 91",
        "Claim boundary: KJVA no-input handoff only; no new result.",
        "Current read: Cities source-row pages remain a source-review lane only.",
        "Presence rows | 812",
        "Bible presence rows | 809",
        "Control presence rows | 3",
        "Raw occurrence rows | 923",
        "Skip 2..100 count hits | 58,715,011",
        "Hidden-path rows retained | 8,443,775",
        "Triage queue rows | 926",
        "reproducing any external claim still requires that source's exact spelling",
    ),
}

REQUIRED_REAL_REPORT_MANIFEST_FIELDS: dict[str, Any] = {
    "tool": "build_real_report_run_summary",
    "step_tahot": {
        "real_counts": {
            "pattern_rows": 18855,
            "with_source": 14701,
            "source_only": 465,
            "source_only_rate": 0.024661893396976928,
        },
        "control_counts": {
            "pattern_rows": 1005,
            "with_source": 749,
            "source_only": 24,
            "source_only_rate": 0.023880597014925373,
        },
        "real_policy_counts": {
            "policy_rows": 465,
            "policy_touch": 97,
            "l_only": 368,
            "q_rows": 77,
            "r_rows": 2,
            "x_rows": 18,
            "policy_touch_rate": 0.2086021505376344,
        },
        "control_policy_counts": {
            "policy_rows": 24,
            "policy_touch": 3,
            "l_only": 21,
            "q_rows": 3,
            "r_rows": 0,
            "x_rows": 0,
            "policy_touch_rate": 0.125,
        },
    },
    "greek_gate_rows": 4,
    "greek_pattern_rows": 4,
    "doxa_rows": 4,
    "doxa_protocol_status": "success",
    "doxa_confirmatory_rows": 4,
    "doxa_confirmatory_protocol_status": "success",
    "surface_queue_summary_rows": 26,
    "surface_queue_pattern_rows": 161,
    "surface_queue_protocol_status": "success",
    "surface_triage_selected_rows": 3,
    "surface_triage_cohort_rows": 291,
    "surface_triage_protocol_status": "success",
    "surface_letter_path_rows": 12,
    "surface_letter_paths_protocol_status": "success",
    "surface_control_frequency_rows": 291,
    "surface_control_matched_rows": 30,
    "surface_control_protocol_status": "success",
    "surface_control_evaluation_rows": 3,
    "surface_control_evaluation_protocol_status": "success",
    "surface_available_control_evaluation_rows": 3,
    "surface_available_control_evaluation_protocol_status": "success",
    "surface_followup_status": "post_screen_surface_followup_review_candidate",
    "surface_followup_selected_rows": 3,
    "surface_followup_path_rows": 12,
    "surface_followup_control_rows": 3,
    "surface_followup_protocol_status": "success",
    "length4_selected_rows": 24,
    "length4_selected_terms": 7,
    "length4_cohort_rows": 288,
    "length4_control_evaluation_rows": 7,
    "length4_letter_path_rows": 96,
    "length4_protocol_status": "success",
    "length4_vocab_generated_controls": 572,
    "length4_vocab_control_evaluation_rows": 7,
    "length4_vocab_protocol_status": "success",
    "wrr_protocol_status": "success",
    "wrr_downloads": 106,
    "wrr_text_source_rows": 1,
    "wrr_source_shapes_summary_rows": 1,
    "wrr_count_summary_rows": 30,
    "wrr_pair_audit_len_5_8_rows": 22,
    "wrr_pair_controls_len_5_8_rows": 18,
    "wrr_skip_caps_summary_rows": 1,
    "wrr_pair_table_reconciliation_rows": 1,
    "wrr_perturbation_summary_rows": 1,
    "wrr_cross_pair_recommended_permutation_rows": 1,
    "wrr_source_policy_scenario_rows": 5,
    "wrr_source_policy_term_impact_rows": 7,
    "wrr_source_policy_evidence_summary_rows": 1,
    "wrr_source_transcription_evidence_row_summary_rows": 22,
    "wrr_source_row_review_bundle_summary_rows": 9,
    "wrr_source_row_crop_review_html_summary_rows": 17,
    "wrr_post_lock_reporting_boundary_rows": 10,
    "wrr_remaining_lane_evidence_summary_rows": 2,
    "wrr_method_pair_universe_evidence_summary_rows": 1,
    "wrr_dw_formula_sensitivity_rows": 3,
    "wrr_no_input_handoff_status_rows": 9,
    "wrr_no_input_handoff_manual_input_needed_rows": 8,
    "wrr_no_input_handoff_new_result_allowed": "0",
    "wrr_no_input_handoff_exact_reproduction_ready": "0",
    "wrr_no_input_handoff_claim_status": "local_locked_method_ready_exact_published_open",
    "kjva_no_input_handoff_status_rows": 9,
    "kjva_no_input_handoff_manual_input_needed_rows": 8,
    "kjva_no_input_handoff_source_policy_blocker_rows": 7,
    "kjva_no_input_handoff_result_allowed": "0",
    "kjva_no_input_handoff_claim_status": "kjva_no_input_handoff_blocks_new_result",
    "cities_no_input_handoff_status_rows": 8,
    "cities_no_input_handoff_manual_input_needed_rows": 6,
    "cities_no_input_handoff_ocr_packet_pages": 61,
    "cities_no_input_handoff_reviewed_ocr_packet_pages": 41,
    "cities_no_input_handoff_unreviewed_ocr_packet_pages": 20,
    "cities_no_input_handoff_source_row_imports": 0,
    "cities_no_input_handoff_result_allowed": "0",
    "cities_no_input_handoff_claim_status": (
        "cities_no_input_handoff_blocks_source_import_and_results"
    ),
    "external_claim_count_summary_rows": 97,
    "external_claim_count_term_sets": 8,
    "external_claim_count_corpora": 21,
    "external_claim_count_total_hits": 58715011,
    "external_claim_count_manifest_rows": 3708,
    "external_claim_all_codes_summary_rows": 3708,
    "external_claim_all_codes_hit_rows": 8443775,
    "external_claim_all_codes_context_hits": 7114738,
    "external_claim_all_codes_triage_rows": 926,
    "external_claim_all_codes_triage_bucket_counts": {
        "center_word_exact": 100,
        "center_word_same_concept": 26,
        "center_word_same_category": 100,
        "center_verse_exact": 100,
        "center_verse_same_concept": 100,
        "center_verse_same_category": 100,
        "span_exact": 100,
        "span_same_concept": 100,
        "span_same_category": 100,
        "hidden_path_only": 100,
    },
    "hebrew_theology_all_codes_triage_rows": 700,
    "hebrew_screening_all_codes_triage_rows": 909,
    "greek_screening_all_codes_triage_rows": 700,
    "all_codes_followup_selection_rows": 83,
    "all_codes_followup_letter_path_rows": 310,
    "all_codes_followup_letter_paths_manifest_rows": 310,
    "all_codes_followup_letter_rows": 1394,
    "all_codes_followup_letter_path_mismatches": 0,
    "all_codes_followup_context_rows": 310,
    "all_codes_followup_context_excerpt_rows": 310,
    "all_codes_followup_context_center_contains_rows": 73,
    "all_codes_followup_context_span_contains_rows": 100,
    "all_codes_followup_extension_summary_rows": 83,
    "all_codes_followup_extension_rows": 692,
    "all_codes_followup_compound_extension_rows": 55,
    "all_codes_followup_extension_selected_rows": 69,
    "all_codes_followup_selected_rows_with_compound_extensions": 13,
    "all_codes_followup_extension_max_length": 5,
    "all_codes_compound_extension_control_rows": 46,
    "all_codes_compound_extension_control_targets": 46,
    "all_codes_compound_extension_control_term_samples": 250,
    "all_codes_compound_extension_control_random_samples": 250,
    "all_codes_compound_extension_confirmatory_rows": 5,
    "all_codes_compound_extension_confirmatory_targets": 5,
    "all_codes_compound_extension_confirmatory_term_samples": 5000,
    "all_codes_compound_extension_confirmatory_random_samples": 5000,
    "all_codes_compound_extension_confirmatory_protocol_status": "success",
    "all_codes_followup_review_rows": 83,
    "all_codes_followup_review_summary_rows": 83,
    "all_codes_followup_review_status_counts": {
        "center_verse_context_review": 24,
        "hidden_path_review": 9,
        "related_center_word_review": 15,
        "span_context_review": 24,
        "strongest_manual_review": 11,
    },
    "centered_occurrence_presence_rows": 812,
    "centered_occurrence_occurrence_rows": 923,
    "centered_occurrence_bible_presence_rows": 809,
    "centered_occurrence_control_presence_rows": 3,
    "centered_occurrence_type_counts": {
        "centered_self_exact_word": 526,
        "centered_self_surface_form": 4,
        "relevant_center_same_concept": 3,
        "relevant_center_same_category": 13,
        "center_verse_relevant": 70,
        "span_relevant": 196,
    },
    "matrix_cluster_relation_control_rows": 4,
    "matrix_cluster_term_pair_control_rows": 95,
    "notable_passage_gap_passage_rows": 122,
    "notable_passage_gap_cross_source_rows": 1390,
    "thematic_chapter_absence_passage_rows": 63,
    "thematic_chapter_absence_cross_source_rows": 19,
    "match_strata_summary_rows": 28,
    "boundary_alignment_summary_rows": 144,
    "chapter_position_bias_summary_rows": 90,
    "direction_asymmetry_summary_rows": 72,
    "canonical_first_summary_rows": 54,
    "cross_skip_summary_rows": 72,
    "review_flag_summary_rows": 5,
    "cohort_cluster_density_summary_rows": 0,
    "kjva_apocrypha_bridge_confirmatory_rows": 15,
    "kjva_apocrypha_bridge_confirmatory_samples": 5000,
    "kjva_apocrypha_bridge_confirmatory_terms_above_all_samples": 3,
    "kjva_apocrypha_bridge_confirmatory_terms_q_le_0_05": 15,
    "kjva_apocrypha_bridge_prospective_rows": 7,
    "kjva_apocrypha_bridge_prospective_samples": 5000,
    "kjva_apocrypha_bridge_prospective_terms_above_all_samples": 0,
    "kjva_apocrypha_bridge_prospective_terms_q_le_0_05": 0,
    "kjva_apocrypha_bridge_prospective_nonbible_controls": 3,
    "kjva_apocrypha_bridge_prospective_nonbible_controls_ge_observed": 1,
}
ALLOWED_REAL_REPORT_MANIFEST_METADATA_FIELDS = {
    "commit",
    "duration_seconds",
    "edls_version",
    "generated_at",
    "inputs",
    "outputs",
}


def _load_real_report_protocol_requirements(
    path: Path = REAL_REPORT_PROTOCOL_SOURCE,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if not path.exists():
        return (), (f"{path} is missing",)
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        return (), (f"{path} is invalid TOML: {exc}",)
    steps = data.get("steps", [])
    if not isinstance(steps, list):
        return (), (f"{path} steps must be a list",)
    step_ids = tuple(
        str(step.get("id", ""))
        for step in steps
        if isinstance(step, dict) and step.get("id")
    )
    if not step_ids:
        return (), (f"{path} has no step ids",)
    return step_ids, ()


(
    REQUIRED_REAL_REPORT_PROTOCOL_STEP_IDS,
    REAL_REPORT_PROTOCOL_SOURCE_FAILURES,
) = _load_real_report_protocol_requirements()


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_public_reader_package(args.package_dir)
    if failures:
        for failure in failures:
            print(f"public-reader package failure: {failure}", file=sys.stderr)
        return 1
    print(f"public-reader package ok: {args.package_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", type=Path, default=DEFAULT_PACKAGE_DIR)
    return parser


def validate_public_reader_package(
    package_dir: Path = DEFAULT_PACKAGE_DIR,
) -> list[str]:
    failures: list[str] = []
    if not package_dir.exists():
        return [f"{package_dir} is missing"]
    if package_dir.is_symlink():
        failures.append(f"{package_dir} is a symlink")
    if not package_dir.is_dir():
        failures.append(f"{package_dir} is not a directory")
        return failures

    for generated in REQUIRED_GENERATED_FILES:
        path = package_dir / generated
        if not path.exists():
            failures.append(f"{path} is missing")
        elif path.is_symlink():
            failures.append(f"{path} is a symlink")
        elif not path.is_file():
            failures.append(f"{path} is not a file")

    manifest_path = package_dir / "package_manifest.json"
    if not manifest_path.exists() or not manifest_path.is_file():
        return failures

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"{manifest_path} is invalid JSON: {exc}")
        return failures

    failures.extend(validate_manifest_metadata(manifest, package_dir))
    failures.extend(validate_manifest_files(manifest, package_dir))
    failures.extend(validate_required_packaged_phrase_guard_coverage())
    failures.extend(validate_required_packaged_phrase_guard_targets(manifest))
    failures.extend(validate_required_packaged_phrases(package_dir))
    failures.extend(validate_packaged_real_report_summary(manifest, package_dir))
    failures.extend(validate_packaged_real_report_manifest(manifest, package_dir))
    failures.extend(validate_packaged_real_report_preflight(manifest, package_dir))
    failures.extend(validate_packaged_real_report_protocol_manifest(manifest, package_dir))
    failures.extend(validate_generated_package_readme(manifest, package_dir))
    failures.extend(validate_generated_reader_package(manifest, package_dir))
    failures.extend(validate_no_unmanifested_files(manifest, package_dir))
    return failures


def validate_required_packaged_phrase_guard_targets(
    manifest: dict[str, Any],
) -> list[str]:
    files = manifest.get("files")
    if not isinstance(files, list):
        return []
    package_paths = {
        str(item.get("package_path", ""))
        for item in files
        if isinstance(item, dict)
    }
    failures: list[str] = []
    for path in REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH:
        if path.as_posix() not in package_paths:
            failures.append(
                f"required packaged phrase guard path not in manifest: {path}"
            )
    return failures


def validate_required_packaged_phrase_guard_coverage() -> list[str]:
    failures: list[str] = []
    guarded_package_paths = set(REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH)
    for source_path in builder.DEFAULT_DOC_PATHS:
        package_path = builder.SOURCE_PACKAGE_PATH_OVERRIDES.get(
            source_path,
            source_path,
        )
        if package_path not in guarded_package_paths:
            failures.append(
                f"default package doc lacks required phrase guard: {package_path}"
            )
    return failures


def validate_required_packaged_phrases(package_dir: Path) -> list[str]:
    failures: list[str] = []
    for relative_path, required_phrases in REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH.items():
        path = package_dir / relative_path
        if not path.exists() or path.is_symlink() or not path.is_file():
            continue
        text = normalize_space(path.read_text(encoding="utf-8"))
        for phrase in required_phrases:
            if normalize_space(phrase) not in text:
                failures.append(f"{path} missing packaged phrase: {phrase}")
    return failures


def validate_manifest_metadata(
    manifest: dict[str, Any],
    package_dir: Path,
) -> list[str]:
    failures: list[str] = []
    current_git_head = builder.git_head()
    if manifest.get("git_head") != current_git_head:
        failures.append(
            f"{package_dir}/package_manifest.json git_head drifted: "
            f"{manifest.get('git_head')} != {current_git_head}"
        )
    if "no raw source texts" not in str(manifest.get("package_boundary", "")):
        failures.append(f"{package_dir}/package_manifest.json missing package boundary")
    if "validated before packaging" not in str(manifest.get("reader_path_guard", "")):
        failures.append(f"{package_dir}/package_manifest.json missing reader guard")
    if manifest.get("package_start_paths") != [
        path.as_posix() for path in builder.PACKAGE_START_PATHS
    ]:
        failures.append(f"{package_dir}/package_manifest.json package start paths drifted")
    expected_reader_sources = {
        "full_doc": [path.as_posix() for path in builder.READER_LINK_SOURCE_PATHS],
        "marked_sections": {
            path.as_posix(): marker
            for path, marker in builder.READER_LINK_SECTION_MARKERS.items()
        },
    }
    if manifest.get("reader_link_sources") != expected_reader_sources:
        failures.append(f"{package_dir}/package_manifest.json reader-link sources drifted")
    files = manifest.get("files")
    if not isinstance(files, list):
        failures.append(f"{package_dir}/package_manifest.json files must be a list")
    elif manifest.get("file_count") != len(files):
        failures.append(
            f"{package_dir}/package_manifest.json file_count drifted: "
            f"{manifest.get('file_count')} != {len(files)}"
        )
    return failures


def validate_manifest_files(
    manifest: dict[str, Any],
    package_dir: Path,
) -> list[str]:
    failures: list[str] = []
    files = manifest.get("files")
    if not isinstance(files, list):
        return failures
    seen_sources: set[str] = set()
    seen_package_paths: set[str] = set()
    for index, item in enumerate(files):
        if not isinstance(item, dict):
            failures.append(f"manifest file row {index} is not an object")
            continue
        source = str(item.get("source", ""))
        package_path_text = str(item.get("package_path", ""))
        failures.extend(validate_manifest_file_row_shape(index, item))
        failures.extend(validate_manifest_source_path(source))
        if source in seen_sources:
            failures.append(f"duplicate manifest source: {source}")
        seen_sources.add(source)
        if package_path_text in seen_package_paths:
            failures.append(f"duplicate manifest package path: {package_path_text}")
        seen_package_paths.add(package_path_text)
        if not package_path_text:
            continue
        package_path = Path(package_path_text)
        if package_path.is_absolute() or ".." in package_path.parts:
            failures.append(f"unsafe manifest package path: {package_path_text}")
            continue
        failures.extend(validate_manifest_package_mapping(source, package_path_text))
        path = package_dir / package_path
        failures.extend(validate_packaged_file(path, item))
    source_set = {str(item.get("source", "")) for item in files if isinstance(item, dict)}
    for path in builder.PACKAGE_START_PATHS:
        if path.as_posix() not in source_set:
            failures.append(f"package start source missing from manifest: {path}")
    for source in required_manifest_sources():
        if source not in source_set:
            failures.append(f"required package source missing from manifest: {source}")
    return failures


def required_manifest_sources() -> list[str]:
    paths = [*builder.DEFAULT_DOC_PATHS]
    paths.extend(path for path in builder.DEFAULT_REPORT_PATHS if path.exists())
    return sorted(path.as_posix() for path in paths)


def validate_manifest_package_mapping(
    source: str,
    package_path_text: str,
) -> list[str]:
    source_path = Path(source)
    if source_path.is_absolute() or ".." in source_path.parts:
        return []
    expected = builder.SOURCE_PACKAGE_PATH_OVERRIDES.get(source_path, source_path)
    if package_path_text != expected.as_posix():
        return [
            "manifest package path does not match source mapping: "
            f"{source} -> {package_path_text} (expected {expected.as_posix()})"
        ]
    return []


def validate_no_unmanifested_files(
    manifest: dict[str, Any],
    package_dir: Path,
) -> list[str]:
    files = manifest.get("files")
    if not isinstance(files, list):
        return []
    expected = {path.as_posix() for path in REQUIRED_GENERATED_FILES}
    for item in files:
        if isinstance(item, dict):
            package_path = item.get("package_path")
            if isinstance(package_path, str):
                expected.add(package_path)
    failures: list[str] = []
    for path in package_dir.rglob("*"):
        if path.is_dir() and not path.is_symlink():
            continue
        relative = path.relative_to(package_dir).as_posix()
        if relative not in expected:
            failures.append(f"unexpected package file: {relative}")
    return failures


def validate_packaged_real_report_summary(
    manifest: dict[str, Any],
    package_dir: Path,
) -> list[str]:
    git_head = manifest.get("git_head")
    if not isinstance(git_head, str) or not git_head:
        return []
    files = manifest.get("files")
    if not isinstance(files, list):
        return []
    for item in files:
        if not isinstance(item, dict):
            continue
        if item.get("source") != REAL_REPORT_SUMMARY_SOURCE.as_posix():
            continue
        package_path_text = item.get("package_path")
        if not isinstance(package_path_text, str):
            return []
        package_path = Path(package_path_text)
        if package_path.is_absolute() or ".." in package_path.parts:
            return []
        path = package_dir / package_path
        if not path.exists() or path.is_symlink() or not path.is_file():
            return []
        expected = f"Commit: `{git_head[:7]}`"
        if expected not in path.read_text(encoding="utf-8"):
            return [f"{path} commit stamp drifted: expected {expected}"]
        return []
    return []


def validate_packaged_real_report_manifest(
    manifest: dict[str, Any],
    package_dir: Path,
) -> list[str]:
    git_head = manifest.get("git_head")
    files = manifest.get("files")
    if not isinstance(files, list):
        return []
    for item in files:
        if not isinstance(item, dict):
            continue
        if item.get("source") != REAL_REPORT_MANIFEST_SOURCE.as_posix():
            continue
        package_path_text = item.get("package_path")
        if not isinstance(package_path_text, str):
            return []
        package_path = Path(package_path_text)
        if package_path.is_absolute() or ".." in package_path.parts:
            return []
        path = package_dir / package_path
        if not path.exists() or path.is_symlink() or not path.is_file():
            return []
        try:
            report_manifest = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return [f"{path} is invalid JSON: {exc}"]
        failures: list[str] = []
        if isinstance(git_head, str) and git_head:
            expected = git_head[:7]
            if report_manifest.get("commit") != expected:
                failures.append(
                    f"{path} commit stamp drifted: "
                    f"{report_manifest.get('commit')} != {expected}"
                )
        for key, expected_value in REQUIRED_REAL_REPORT_MANIFEST_FIELDS.items():
            if report_manifest.get(key) != expected_value:
                failures.append(
                    f"{path} {key} drifted: "
                    f"{report_manifest.get(key)} != {expected_value}"
                )
        allowed_keys = (
            set(REQUIRED_REAL_REPORT_MANIFEST_FIELDS)
            | ALLOWED_REAL_REPORT_MANIFEST_METADATA_FIELDS
        )
        for key in sorted(set(report_manifest) - allowed_keys):
            failures.append(f"{path} has unguarded real-report manifest key: {key}")
        return failures
    return []


def validate_packaged_real_report_preflight(
    manifest: dict[str, Any],
    package_dir: Path,
) -> list[str]:
    path = packaged_path_for_source(manifest, package_dir, REAL_REPORT_PREFLIGHT_SOURCE)
    if path is None:
        return []
    data = read_packaged_json(path)
    if isinstance(data, str):
        return [data]
    failures: list[str] = []
    checks: dict[str, Any] = {
        "status": "passed",
        "allow_dirty": False,
        "git_status_lines": [],
        "risky_tracked_paths": [],
    }
    for key, expected in checks.items():
        if data.get(key) != expected:
            failures.append(f"{path} {key} drifted: {data.get(key)} != {expected}")
    remotes = data.get("git_remotes")
    if not isinstance(remotes, list) or not any(
        "github.com/Biblejustin/open-bible-codes" in str(remote)
        for remote in remotes
    ):
        failures.append(f"{path} missing Biblejustin remote")
    git_head = manifest.get("git_head")
    if isinstance(git_head, str) and git_head:
        expected = git_head[:7]
        if data.get("git_commit") != expected:
            failures.append(
                f"{path} git_commit drifted: {data.get('git_commit')} != {expected}"
            )
    return failures


def validate_packaged_real_report_protocol_manifest(
    manifest: dict[str, Any],
    package_dir: Path,
) -> list[str]:
    failures = list(REAL_REPORT_PROTOCOL_SOURCE_FAILURES)
    path = packaged_path_for_source(
        manifest,
        package_dir,
        REAL_REPORT_PROTOCOL_MANIFEST_SOURCE,
    )
    if path is None:
        return failures
    data = read_packaged_json(path)
    if isinstance(data, str):
        failures.append(data)
        return failures
    checks: dict[str, Any] = {
        "tool": "run_protocol",
        "protocol": "real_report_run",
        "status": "success",
        "dry_run": False,
    }
    for key, expected in checks.items():
        if data.get(key) != expected:
            failures.append(f"{path} {key} drifted: {data.get(key)} != {expected}")
    steps = data.get("steps")
    if not isinstance(steps, list) or not steps:
        failures.append(f"{path} has no protocol steps")
        return failures
    step_id_list = [
        str(step.get("id", ""))
        for step in steps
        if isinstance(step, dict) and step.get("id")
    ]
    step_ids = set(step_id_list)
    required_step_ids = set(REQUIRED_REAL_REPORT_PROTOCOL_STEP_IDS)
    for step_id in sorted(
        step_id
        for step_id in step_ids
        if step_id_list.count(step_id) > 1
    ):
        failures.append(f"{path} has duplicate protocol step: {step_id}")
    for step_id in REQUIRED_REAL_REPORT_PROTOCOL_STEP_IDS:
        if step_id not in step_ids:
            failures.append(f"{path} missing protocol step: {step_id}")
    for step_id in sorted(step_ids - required_step_ids):
        failures.append(f"{path} has unexpected protocol step: {step_id}")
    preflight = protocol_step(steps, "preflight")
    if not isinstance(preflight, dict):
        failures.append(f"{path} missing preflight step")
    elif preflight.get("return_code") != 0 or preflight.get("skipped") is not False:
        failures.append(f"{path} preflight step did not run cleanly")
    cities_handoff = protocol_step(steps, "cities_no_input_handoff_status")
    if not isinstance(cities_handoff, dict):
        failures.append(f"{path} missing cities_no_input_handoff_status step")
    elif cities_handoff.get("return_code") != 0:
        failures.append(f"{path} cities_no_input_handoff_status step failed")
    for step_id in (
        "wrr_no_input_handoff_status",
        "kjva_no_input_handoff_status",
        "external_claim_source_counts",
        "external_claim_source_all_codes_collection",
    ):
        step = protocol_step(steps, step_id)
        if not isinstance(step, dict):
            failures.append(f"{path} missing {step_id} step")
        elif step.get("return_code") != 0:
            failures.append(f"{path} {step_id} step failed")
    summary = protocol_step(steps, "real_report_summary")
    if not isinstance(summary, dict):
        failures.append(f"{path} missing real_report_summary step")
    elif summary.get("return_code") != 0 or summary.get("skipped") is not False:
        failures.append(f"{path} real_report_summary step did not run cleanly")
    elif not protocol_step_contains_all(
        summary,
        key="inputs",
        required=(
            "reports/wrr_1994/wrr_no_input_handoff_status_summary.csv",
            "reports/wrr_1994/wrr_no_input_handoff_status.manifest.json",
            "reports/cities_no_input_handoff_status/summary.csv",
            "reports/cities_no_input_handoff_status/manifest.json",
            "reports/kjva_no_input_handoff_status/summary.csv",
            "reports/kjva_no_input_handoff_status/manifest.json",
        ),
    ):
        failures.append(f"{path} real_report_summary missing no-input handoff inputs")
    elif not protocol_step_contains_all(
        summary,
        key="inputs",
        required=(
            "reports/external_claim_source_counts/summary.csv",
            "reports/external_claim_source_counts/summary.manifest.json",
            "reports/external_claim_source_all_codes/surface_all_codes_summary.csv",
            "reports/external_claim_source_all_codes/summary.manifest.json",
            "reports/external_claim_source_all_codes/triage_queue.csv",
            "reports/external_claim_source_all_codes/triage.manifest.json",
            "reports/external_claim_source_all_codes/findings.manifest.json",
        ),
    ):
        failures.append(f"{path} real_report_summary missing external-claim inputs")
    elif not protocol_step_contains_all(
        summary,
        key="outputs",
        required=(
            "reports/real_report_run/summary.md",
            "reports/real_report_run/manifest.json",
        ),
    ):
        failures.append(f"{path} real_report_summary outputs drifted")
    return failures


def protocol_step(steps: list[Any], step_id: str) -> dict[str, Any] | None:
    return next(
        (
            step
            for step in steps
            if isinstance(step, dict) and step.get("id") == step_id
        ),
        None,
    )


def protocol_step_contains_all(
    step: dict[str, Any],
    *,
    key: str,
    required: tuple[str, ...],
) -> bool:
    values = step.get(key)
    if not isinstance(values, list):
        return False
    return set(required).issubset({str(value) for value in values})


def packaged_path_for_source(
    manifest: dict[str, Any],
    package_dir: Path,
    source: Path,
) -> Path | None:
    files = manifest.get("files")
    if not isinstance(files, list):
        return None
    for item in files:
        if not isinstance(item, dict) or item.get("source") != source.as_posix():
            continue
        package_path_text = item.get("package_path")
        if not isinstance(package_path_text, str):
            return None
        package_path = Path(package_path_text)
        if package_path.is_absolute() or ".." in package_path.parts:
            return None
        path = package_dir / package_path
        if not path.exists() or path.is_symlink() or not path.is_file():
            return None
        return path
    return None


def read_packaged_json(path: Path) -> dict[str, Any] | str:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return f"{path} is invalid JSON: {exc}"
    if not isinstance(data, dict):
        return f"{path} JSON root must be an object"
    return data


def validate_generated_package_readme(
    manifest: dict[str, Any],
    package_dir: Path,
) -> list[str]:
    readme = package_dir / "README.md"
    if not readme.exists() or readme.is_symlink() or not readme.is_file():
        return []
    actual = readme.read_text(encoding="utf-8")
    expected = expected_package_readme_text(manifest)
    if actual != expected:
        return [f"{readme} content drifted from manifest"]
    return []


def expected_package_readme_text(manifest: dict[str, Any]) -> str:
    lines = [
        "# Public Reader Package",
        "",
        "Status: generated package over whitelisted docs and formal report summary.",
        "Reader-path guard: project findings overview, package start paths, and configured reader-link sources validated before packaging.",
        "It contains no raw Bible source files and no local database artifacts.",
        "",
        "Start with:",
        "",
        *[
            f"{index}. `{path.as_posix()}`"
            for index, path in enumerate(builder.PACKAGE_START_PATHS, start=1)
        ],
        "",
        "Package files:",
        "",
        "| Source | Package path | Bytes | SHA-256 |",
        "| --- | --- | ---: | --- |",
    ]
    files = manifest.get("files")
    if isinstance(files, list):
        for item in files:
            if not isinstance(item, dict):
                continue
            lines.append(
                f"| `{item.get('source', '')}` | `{item.get('package_path', '')}` | "
                f"{item.get('bytes', '')} | `{item.get('sha256', '')}` |"
            )
    return "\n".join(lines).rstrip() + "\n"


def validate_generated_reader_package(
    manifest: dict[str, Any],
    package_dir: Path,
) -> list[str]:
    reader_package = package_dir / "reader_package.md"
    if (
        not reader_package.exists()
        or reader_package.is_symlink()
        or not reader_package.is_file()
    ):
        return []
    failures: list[str] = []
    expected = expected_reader_package_text(manifest, package_dir, failures)
    if failures:
        return failures
    actual = reader_package.read_text(encoding="utf-8")
    if actual != expected:
        failures.append(f"{reader_package} content drifted from package files")
    return failures


def expected_reader_package_text(
    manifest: dict[str, Any],
    package_dir: Path,
    failures: list[str],
) -> str:
    lines = [
        "# Public Reader Package",
        "",
        "This concatenates the reader-path docs and formal report summary.",
        "",
    ]
    files = manifest.get("files")
    if not isinstance(files, list):
        return "\n".join(lines).rstrip() + "\n"
    for item in files:
        if not isinstance(item, dict):
            continue
        source = str(item.get("source", ""))
        package_path_text = str(item.get("package_path", ""))
        if not package_path_text.endswith(".md"):
            continue
        package_path = Path(package_path_text)
        if package_path.is_absolute() or ".." in package_path.parts:
            continue
        path = package_dir / package_path
        if path.is_symlink() or not path.exists() or not path.is_file():
            failures.append(f"cannot validate reader package source section: {path}")
            continue
        lines.extend(
            [
                "",
                "---",
                "",
                f"Source: `{source}`",
                "",
                path.read_text(encoding="utf-8").rstrip(),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def validate_manifest_file_row_shape(
    index: int,
    item: dict[str, Any],
) -> list[str]:
    failures: list[str] = []
    for key in ("source", "package_path", "bytes", "sha256"):
        if key not in item:
            failures.append(f"manifest file row {index} missing {key}")
    if "sha256" in item and not is_hex_sha256(str(item["sha256"])):
        failures.append(f"manifest file row {index} has invalid sha256")
    if "bytes" in item and not isinstance(item["bytes"], int):
        failures.append(f"manifest file row {index} bytes must be an integer")
    return failures


def validate_manifest_source_path(source: str) -> list[str]:
    if not source:
        return ["manifest file row has empty source"]
    path = Path(source)
    failures: list[str] = []
    if path.is_absolute() or ".." in path.parts:
        failures.append(f"unsafe manifest source path: {source}")
    if path.suffix.lower() not in {".md", ".json"}:
        failures.append(f"unsupported manifest source suffix: {source}")
    if builder.is_forbidden_source(path):
        failures.append(f"forbidden manifest source path: {source}")
    return failures


def validate_packaged_file(path: Path, item: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"{path} is missing"]
    if path.is_symlink():
        failures.append(f"{path} is a symlink")
    if not path.is_file():
        failures.append(f"{path} is not a file")
        return failures
    data = path.read_bytes()
    if item.get("bytes") != len(data):
        failures.append(f"{path} byte count drifted")
    digest = hashlib.sha256(data).hexdigest()
    if item.get("sha256") != digest:
        failures.append(f"{path} sha256 drifted")
    return failures


def is_hex_sha256(value: str) -> bool:
    return len(value) == 64 and all(char in "0123456789abcdef" for char in value)


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
