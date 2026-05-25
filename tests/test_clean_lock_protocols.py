from pathlib import Path

from els.protocol_runner import load_protocol
from scripts.check_preregistration_placeholders import find_placeholders


PROFILES = [
    (
        Path("protocols/greek_surface_new_terms.toml"),
        Path("docs/GREEK_SURFACE_NEW_TERMS_PREREGISTRATION.md"),
        "terms/greek_surface_new_terms_clean_lock.csv",
        "greek_surface_new_terms",
    ),
    (
        Path("protocols/compound_extension_prospective.toml"),
        Path("docs/COMPOUND_EXTENSION_PROSPECTIVE_PREREGISTRATION.md"),
        "terms/compound_extension_prospective_terms_clean_lock.csv",
        "compound_extension_prospective",
    ),
    (
        Path("protocols/hebrew_concordance_words_prospective.toml"),
        Path("docs/HEBREW_CONCORDANCE_WORDS_PROSPECTIVE_PREREGISTRATION.md"),
        "terms/hebrew_concordance_prospective_terms_clean_lock.csv",
        "hebrew_concordance_words_prospective",
    ),
]


def test_clean_lock_protocols_use_clean_term_files() -> None:
    for protocol_path, _prereg, term_file, name in PROFILES:
        protocol = load_protocol(protocol_path)
        argv_values = [value for step in protocol["steps"] for value in step["argv"]]
        input_values = [value for step in protocol["steps"] for value in step.get("inputs", [])]

        assert protocol["name"] == name
        assert term_file in argv_values
        assert term_file in input_values


def test_clean_lock_preregistrations_have_no_placeholders() -> None:
    for _protocol_path, prereg, _term_file, _name in PROFILES:
        assert list(find_placeholders(prereg, allowed=set())) == []


def test_clean_lock_protocols_have_expected_first_steps() -> None:
    assert load_protocol("protocols/greek_surface_new_terms.toml")["steps"][0]["id"] == "surface_context"
    assert load_protocol("protocols/compound_extension_prospective.toml")["steps"][0]["id"] == "version_presence"
    assert (
        load_protocol("protocols/hebrew_concordance_words_prospective.toml")["steps"][0]["id"]
        == "version_presence"
    )


def test_wrr_claim_blocker_step_mentions_visual_triage() -> None:
    protocol = load_protocol("protocols/wrr_audit_counts.toml")
    step = next(
        step for step in protocol["steps"] if step["id"] == "build_wrr_claim_blocker_packet"
    )

    assert "visual triage notes" in step["description"]
    assert "--residual-term-summary" in step["argv"]
    assert "--residual-term-queue" in step["argv"]
    assert "--source-transcription-row-summary" in step["argv"]
    assert "--method-pair-universe-summary" in step["argv"]
    assert "--remaining-lane-summary" in step["argv"]
    assert "--remaining-lane-packet" in step["argv"]
    assert "reports/wrr_1994/wrr_residual_term_reconciliation_summary.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_residual_term_reconciliation_queue.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_source_transcription_evidence_row_summary.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_method_pair_universe_evidence_summary.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_remaining_lane_evidence_summary.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_remaining_lane_evidence_packet.csv" in step["inputs"]


def test_greek_new_terms_report_step_uses_specific_title() -> None:
    protocol = load_protocol("protocols/greek_surface_new_terms.toml")
    step = next(step for step in protocol["steps"] if step["id"] == "prospective_report")
    argv = step["argv"]

    assert argv[argv.index("--title") + 1] == "Greek Surface New Terms Prospective Report"


def test_clean_lock_results_summary_tracks_completed_lanes() -> None:
    text = Path("docs/CLEAN_LOCK_RESULTS_SUMMARY.md").read_text(encoding="utf-8")

    assert "| Greek surface new terms | 236 |" in text
    assert "| Hebrew Gospel/genealogy | 27 |" in text
    assert "| Hebrew concordance words | 3,577 |" in text
    assert "0 adjusted-support terms" in text
    assert "38 ordinary lexical prompts" in text
    assert "10" in text
    assert "high-volume short-string/common-letter prompts" in text
    assert "ordinary" in text
    assert "local surface-context/self-lexeme effects" in text
    assert "KJVA apocrypha bridge prospective lane used a committed" in text
    assert "current manifest/preflight workflow" in text


def test_greek_lexicon_preregistration_is_historical_not_future_run() -> None:
    text = Path("docs/GREEK_LEXICON_EXTENSION_PROSPECTIVE_PREREGISTRATION.md").read_text(
        encoding="utf-8"
    )

    assert "historical preregistration for a completed lane" in text
    assert "completed context-cautioned review material" in text
    assert "## Completed Result Run" in text
    assert "## Future Result Run" not in text
    assert "result run not started" not in text
    assert "ready for lock manifest and preflight" not in text


def test_greek_surface_context_review_tracks_manual_read() -> None:
    text = Path("docs/GREEK_SURFACE_NEW_TERMS_CONTEXT_REVIEW.md").read_text(encoding="utf-8")

    assert "# Greek Surface New Terms Context Review" in text
    assert "direct surface/self-lexeme hit" in text
    assert "ordinary \"name\" passages" in text
    assert "review-material" in text
    assert "category" in text


def test_strict_followup_gate_summary_has_zero_claim_ready_rows() -> None:
    text = Path("docs/STRICT_FOLLOWUP_GATE_SUMMARY.md").read_text(encoding="utf-8")

    assert "| Hebrew concordance uncorrected queue | 87 | 0 |" in text
    assert "| Greek surface new terms controlled rows | 5 | 0 |" in text
    assert "All rows fail adjusted support" in text
    assert "They do not pass a context-distance gate" in text


def test_final_report_includes_clean_lock_closeout() -> None:
    text = Path("docs/FINAL_REPORT.md").read_text(encoding="utf-8")

    assert "## Clean-Lock Close-Out" in text
    assert "0 Hebrew concordance rows and 0 Greek surface rows" in text
    assert "0 all-source extension keys" in text
    assert "`docs/GREEK_LEXICON_EXTENSION_PROSPECTIVE_REPORT.md`" in text
    assert "`docs/STRICT_FOLLOWUP_GATE_SUMMARY.md`" in text

    draft = Path("docs/FINAL_REPORT_DRAFT.md").read_text(encoding="utf-8")
    outline = Path("docs/FINAL_REPORT_OUTLINE.md").read_text(encoding="utf-8")
    assert "0 Hebrew concordance" in draft
    assert "0 all-source extension keys" in draft
    assert "`docs/STRICT_FOLLOWUP_GATE_SUMMARY.md`" in outline


def test_final_report_includes_critical_omission_null_read() -> None:
    text = Path("docs/FINAL_REPORT.md").read_text(encoding="utf-8")
    normalized_text = " ".join(text.split())

    assert "### Critical Omission Breakage" in text
    assert "558 broken TR hits" in normalized_text
    assert "null distribution has median 657" in normalized_text
    assert "`p_ge=0.9910`" in text
    assert "do not break more TR ELS hits than matched random verse blocks" in normalized_text
    assert "`docs/CRITICAL_OMISSION_BREAKS_NULL.md`" in text

    draft = Path("docs/FINAL_REPORT_DRAFT.md").read_text(encoding="utf-8")
    outline = Path("docs/FINAL_REPORT_OUTLINE.md").read_text(encoding="utf-8")
    assert "critical-omission breakage" in draft
    assert "`p_ge=0.9910`" in draft
    assert "TR-vs-SBLGNT omission breakage" in outline


def test_critical_omission_root_doc_keeps_null_interpretation_visible() -> None:
    text = Path("docs/CRITICAL_OMISSION_BREAKS.md").read_text(encoding="utf-8")
    normalized_text = " ".join(text.split())

    assert "`p_ge=0.9910`" in text
    assert "null median 657" in normalized_text
    assert "do not break more TR ELS hits than matched random verse blocks" in normalized_text
    assert "below the null median" in normalized_text
    assert "Raw break counts are not significance tests" in text


def test_readme_tracks_public_final_report_read() -> None:
    text = Path("README.md").read_text(encoding="utf-8")
    normalized_text = " ".join(text.split())

    assert "Current public read:" in text
    assert "no current row should be presented as a public claim" in normalized_text
    assert "TR-vs-SBLGNT critical-omission breakage is a source-variation screen" in normalized_text
    assert "observed broken TR hits are 558" in normalized_text
    assert "1000-shuffle null median is 657" in normalized_text
    assert "`p_ge=0.9910`" in text
    assert "protocols/critical_omission_followups.toml" in text


def test_public_baseline_tracks_critical_omission_null_read() -> None:
    text = Path("docs/PUBLIC_BASELINE_FINDINGS.md").read_text(encoding="utf-8")
    normalized_text = " ".join(text.split())

    assert "## Critical Omission Follow-Up Read" in text
    assert "558 observed broken TR hits" in normalized_text
    assert "1000-shuffle null median 657" in normalized_text
    assert "`p_ge=0.9910`" in text
    assert "not break more TR ELS hits than matched random verse blocks" in normalized_text
    assert "`docs/CRITICAL_OMISSION_BREAKS_PERICOPE_OVERRIDE.md`" in text


def test_local_data_doc_check_make_target_is_documented() -> None:
    makefile = Path("Makefile").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "local-data-doc-check:" in makefile
    assert "scripts.check_doc_command_references --check-local-data" in makefile
    assert "make local-data-doc-check" in readme
    assert "separate from `make public-release-check`" in readme


def test_fast_validate_make_target_tracks_current_handoff_checks() -> None:
    makefile = Path("Makefile").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "fast-validate: test indexes" in makefile
    assert "git diff --check" in makefile
    assert "scripts.check_public_release_hygiene --allow-dirty" in makefile
    assert "scripts.check_expanded_strata_tooling" in makefile
    assert "scripts.check_public_claim_language" in makefile
    assert "$(MAKE) local-data-doc-check" in makefile
    assert "make fast-validate" in readme
    assert "expanded-strata operator tooling" in readme
    assert "checks public claim language" in readme


def test_release_ready_make_target_wraps_handoff_and_release_checks() -> None:
    makefile = Path("Makefile").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    normalized_readme = " ".join(readme.split())

    assert "release-ready: fast-validate public-release-check" in makefile
    assert "scripts.check_doc_command_references" in makefile
    assert "make release-ready" in readme
    assert "validates documented script/source-path references" in normalized_readme
    assert "after committing" in readme
    assert "clean public-release gate" in readme
    assert "intentionally fails while tracked files are dirty" in normalized_readme


def test_remaining_work_register_tracks_latest_validation_snapshot() -> None:
    text = Path("docs/REMAINING_WORK_REGISTER.md").read_text(encoding="utf-8")

    assert "Latest validation snapshot after the release-ready make target" in text
    assert "1473 tests" in text
    assert "2 skipped, and 29195 subtests" in text
    assert "make release-ready" in text
    assert "committed tree" in text
    assert "make fast-validate" in text
    assert "scripts.check_expanded_strata_tooling" in text
    assert "scripts.check_public_claim_language" in text
    assert "scripts.check_doc_command_references" in text
    assert "real-report" in text
    assert "make local-data-doc-check" in text
    assert "`make public-release-check` passed" in text
    assert "Earlier WRR/source-recovery validation snapshot" in text
    assert "Historical validation after the fallback work" in text
    assert "Historical `python3 -m pytest -q` result after the lock-status" in text


def test_final_report_tracks_wrr_single_term_source_policy_impacts() -> None:
    report_paths = [
        Path("docs/FINAL_REPORT.md"),
        Path("docs/FINAL_REPORT_DRAFT.md"),
        Path("docs/FINAL_REPORT_OUTLINE.md"),
    ]

    for path in report_paths:
        text = path.read_text(encoding="utf-8")
        assert "Single-term Zacut" in text or "single-term Zacut" in text
        assert "`M$HZKWTW`" in text
        assert "163 >=5 pairs" in text
        assert "gap 0" in text
        assert "visual triage" in text.lower()
        assert "do not exclude pairs automatically" in text


def test_wrr_support_docs_track_single_term_source_policy_impacts() -> None:
    report_paths = [
        Path("docs/CONSOLIDATED_FINDINGS.md"),
        Path("docs/WRR_CORRECTED_DISTANCE_NOTES.md"),
        Path("docs/WRR_REPLICATION_PLAN.md"),
        Path("docs/WRR_METHODOLOGY_GAPS.md"),
    ]

    for path in report_paths:
        text = path.read_text(encoding="utf-8")
        assert "`M$HZKWTW`" in text
        assert "163 >=5 pairs" in text
        assert "gap 0" in text
        assert "Visual triage" in text
        assert "do not exclude pairs automatically" in text


def test_wrr_catalog_and_source_audit_track_visual_non_exclusion() -> None:
    report_paths = [
        Path("docs/WRR_SOURCE_AUDIT.md"),
        Path("docs/CLAIM_CATALOG.md"),
    ]

    for path in report_paths:
        text = path.read_text(encoding="utf-8")
        assert "Visual triage" in text
        assert "do not exclude pairs automatically" in text


def test_consolidated_findings_include_clean_lock_closeout() -> None:
    text = Path("docs/CONSOLIDATED_FINDINGS.md").read_text(encoding="utf-8")

    assert "Clean-lock follow-up lanes" in text
    assert "87" in text
    assert "uncorrected-only representative-control prompts" in text
    assert "0 Hebrew concordance rows and 0 Greek surface rows" in text
    assert "0 all-source extension keys" in text


def test_next_lock_tracks_completed_clean_lock_expansion() -> None:
    text = Path("docs/PROSPECTIVE_STUDY_NEXT_LOCK.md").read_text(encoding="utf-8")

    assert "## Track 4: Completed Clean-Lock Expansion" in text
    assert "0 Greek surface rows and 0 Hebrew concordance rows" in text
    assert "`prospective_controlled_review_candidate`" in text


def test_prospective_readiness_marks_current_profiles_closed() -> None:
    readiness = Path("docs/PROSPECTIVE_STUDY_READINESS.md").read_text(encoding="utf-8")
    second_cohort = Path("docs/GREEK_SURFACE_SECOND_COHORT_READINESS.md").read_text(
        encoding="utf-8"
    )
    manifests = Path("docs/STUDY_LOCK_MANIFESTS.md").read_text(encoding="utf-8")

    assert "There is no remaining `ready_for_preflight`" in readiness
    assert "lane" in readiness
    assert "Do not rerun a completed profile as a claim lane" in readiness
    assert "no tracked lane remains `ready_for_preflight`" in second_cohort
    assert "fresh term/source target set and a clean" in second_cohort
    assert "use another lane" not in second_cohort
    assert "historical/status records" in manifests


def test_term_source_notes_point_to_completed_outcomes() -> None:
    user_terms = Path("docs/USER_REQUESTED_PROSPECTIVE_TERMS.md").read_text(encoding="utf-8")
    concordance = Path("docs/HEBREW_CONCORDANCE_PROSPECTIVE_TERMS.md").read_text(
        encoding="utf-8"
    )

    assert "now marks the affected lanes completed" in user_terms
    assert "manual context review found local surface-context/self-lexeme effects" in user_terms
    assert "now marks this lane completed negative" in concordance
    assert "87 uncorrected-only review prompts" in concordance
