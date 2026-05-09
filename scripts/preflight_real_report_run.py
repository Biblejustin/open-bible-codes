#!/usr/bin/env python3
"""Preflight checks for a formal report assembly run."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


OUT = Path("reports/real_report_run/preflight.json")
FORBIDDEN_ACCOUNT_PART = "sp" + "lunk"
FORBIDDEN_ACCOUNT_TERMS = ("justin-" + FORBIDDEN_ACCOUNT_PART, FORBIDDEN_ACCOUNT_PART)
DEFAULT_REQUIRED_PATHS = [
    "scripts/preflight_real_report_run.py",
    "protocols/real_report_run.toml",
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
    "protocols/wrr_audit_counts.toml",
    "docs/STEP_TAHOT_FINAL_GATE.md",
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
    "docs/WRR_REPLICATION_PLAN.md",
    "docs/WRR_METHODOLOGY_GAPS.md",
    "docs/WRR_CORRECTED_DISTANCE_NOTES.md",
    "docs/GREEK_SURFACE_PROSPECTIVE_CLAIM_STANDARD.md",
    "docs/STUDY_LOCK_MANIFESTS.md",
    "docs/PROSPECTIVE_STUDY_PREREGISTRATION_TEMPLATE.md",
    "docs/PROSPECTIVE_TERM_AUDITS.md",
    "docs/BROADER_SEARCH_FINDINGS.md",
    "docs/HEBREW_MODERN_GEOPOLITICAL_VERSION_PRESENCE.md",
    "docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_REVIEW.md",
    "docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_FINDINGS.md",
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
    "docs/FINAL_REPORT_HIGHLIGHTS.md",
    "docs/PROSPECTIVE_STUDY_READINESS.md",
    "docs/PROSPECTIVE_STUDY_NEXT_LOCK.md",
    "docs/CONSOLIDATED_FINDINGS.md",
    "docs/FINAL_REPORT_OUTLINE.md",
    "docs/FINAL_REPORT_DRAFT.md",
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
    "docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS.md",
    "docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_50.md",
    "docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_100.md",
    "docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_250.md",
    "docs/VERSION_DISTRIBUTION_INDEX.md",
    "claims/claim_catalog.csv",
    "terms/bible_code_digest_claim_terms.csv",
    "terms/cri_els_critique_terms.csv",
    "terms/thewordnotes_els_claim_terms.csv",
    "terms/cosmic_codes_claim_terms.csv",
    "terms/mark_tabata_isaiah53_claim_terms.csv",
    "terms/bible_and_science_codes_terms.csv",
    "terms/religions_wiki_scriptural_codes_terms.csv",
    "configs/example_ebible_engkjv_apocrypha.toml",
    "configs/prospective_study_lanes.json",
    "protocols/apocrypha_bridge_study.toml",
    "protocols/kjv_apocrypha_bridge_shuffled_controls_250.toml",
    "protocols/kjv_apocrypha_bridge_term_review.toml",
    "protocols/kjv_apocrypha_bridge_term_shuffled_controls_1000.toml",
    "protocols/kjv_apocrypha_bridge_confirmatory_controls_5000.toml",
    "scripts/audit_apocrypha_coverage.py",
    "scripts/analyze_apocrypha_bridge_shuffled_controls.py",
    "scripts/analyze_apocrypha_bridge_term_shuffled_controls.py",
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
    "scripts/build_final_report_highlights.py",
    "scripts/download_wrr_sources.py",
    "scripts/import_wrr_terms.py",
    "scripts/analyze_wrr_source_shapes.py",
    "scripts/analyze_wrr_audit_counts.py",
    "scripts/analyze_wrr_text_source.py",
    "scripts/analyze_wrr_pair_audit.py",
    "scripts/analyze_wrr_pair_controls.py",
    "scripts/analyze_wrr_skip_caps.py",
    "scripts/analyze_wrr_pair_table_reconciliation.py",
    "scripts/analyze_wrr_perturbation_diagnostics.py",
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
    forbidden_remote_hits = forbidden_hits("\n".join(remotes))
    if forbidden_remote_hits:
        failures.append(
            "forbidden account text found in git remotes: "
            + ", ".join(sorted(forbidden_remote_hits))
        )

    forbidden_repo_hits = scan_forbidden_terms(root)
    if forbidden_repo_hits:
        failures.append(
            "forbidden account text found in repository files: "
            + ", ".join(forbidden_repo_hits[:5])
        )

    missing_paths = [path for path in required_paths(args) if not (root / path).exists()]
    if missing_paths:
        failures.append("missing required paths: " + ", ".join(missing_paths))

    payload = {
        "tool": "preflight_real_report_run",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "status": "failed" if failures else "passed",
        "output_path": str(args.out),
        "allow_dirty": args.allow_dirty,
        "git_status_lines": git_status,
        "git_remotes": remotes,
        "required_paths": required_paths(args),
        "missing_paths": missing_paths,
        "forbidden_account_terms": FORBIDDEN_ACCOUNT_TERMS,
        "forbidden_repo_hits": forbidden_repo_hits,
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


def git_status_short(root: Path) -> list[str]:
    return run_git(root, "status", "--short")


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


def forbidden_hits(text: str) -> set[str]:
    lowered = text.lower()
    return {term for term in FORBIDDEN_ACCOUNT_TERMS if term in lowered}


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
