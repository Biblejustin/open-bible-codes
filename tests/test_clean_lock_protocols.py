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


def test_clean_lock_preregistrations_are_registered_docs() -> None:
    stale_template_phrases = (
        "Status: template",
        "copy before use",
        "pending current preregistration commit",
        "State the exact question",
        "Example shape:",
        "State whether the sources",
    )
    for _protocol_path, prereg, _term_file, name in PROFILES:
        text = prereg.read_text(encoding="utf-8")

        assert "Status: registered clean-lock candidate-discovery screen." in text
        assert (
            f"recorded by `reports/study_locks/{name}.manifest.json`"
            in text
        )
        for phrase in stale_template_phrases:
            assert phrase not in text


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
    assert "--method-lane-wide-skip-summary" in step["argv"]
    assert "--remaining-lane-summary" in step["argv"]
    assert "--remaining-lane-packet" in step["argv"]
    assert "reports/wrr_1994/wrr_residual_term_reconciliation_summary.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_residual_term_reconciliation_queue.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_source_transcription_evidence_row_summary.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_method_pair_universe_evidence_summary.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_method_lane_wide_skip_probe_summary.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_remaining_lane_evidence_summary.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_remaining_lane_evidence_packet.csv" in step["inputs"]


def test_wrr_source_row_coverage_step_is_no_input_packet() -> None:
    protocol = load_protocol("protocols/wrr_audit_counts.toml")
    step = next(
        step for step in protocol["steps"] if step["id"] == "build_wrr_source_row_coverage_packet"
    )

    assert "visual-triage coverage packet" in step["description"]
    assert "--row-checklist" in step["argv"]
    assert "--source-queue" in step["argv"]
    assert "scripts/build_wrr_source_row_coverage_packet.py" in step["inputs"]
    assert "reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_source_review_queue.csv" in step["inputs"]
    assert "docs/WRR_SOURCE_ROW_COVERAGE_PACKET.md" in step["outputs"]


def test_wrr_source_row_crop_step_is_no_input_packet() -> None:
    protocol = load_protocol("protocols/wrr_audit_counts.toml")
    step = next(
        step for step in protocol["steps"] if step["id"] == "build_wrr_source_row_crop_packet"
    )

    assert "row-crop packet" in step["description"]
    assert "--row-checklist" in step["argv"]
    assert "--crop-dir" in step["argv"]
    assert "--contact-sheet-out" in step["argv"]
    assert "scripts/build_wrr_source_row_crop_packet.py" in step["inputs"]
    assert "reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_primary_table2_row_ocr.tsv" in step["inputs"]
    assert "docs/WRR_SOURCE_ROW_CROP_PACKET.md" in step["outputs"]
    assert "docs/WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md" in step["outputs"]


def test_wrr_source_row_ocr_word_step_is_no_input_packet() -> None:
    protocol = load_protocol("protocols/wrr_audit_counts.toml")
    step = next(
        step for step in protocol["steps"] if step["id"] == "build_wrr_source_row_ocr_word_packet"
    )

    assert "OCR-word packet" in step["description"]
    assert "--crop-packet" in step["argv"]
    assert "--tsv" in step["argv"]
    assert "scripts/build_wrr_source_row_ocr_word_packet.py" in step["inputs"]
    assert "reports/wrr_1994/wrr_source_row_crop_packet.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_primary_table2_row_ocr.tsv" in step["inputs"]
    assert "docs/WRR_SOURCE_ROW_OCR_WORD_PACKET.md" in step["outputs"]


def test_wrr_source_row_review_bundle_step_is_no_input_packet() -> None:
    protocol = load_protocol("protocols/wrr_audit_counts.toml")
    step = next(
        step for step in protocol["steps"] if step["id"] == "build_wrr_source_row_review_bundle"
    )

    assert "row-review bundle" in step["description"]
    assert "--row-checklist" in step["argv"]
    assert "--crop-packet" in step["argv"]
    assert "--ocr-word-packet" in step["argv"]
    assert "scripts/build_wrr_source_row_review_bundle.py" in step["inputs"]
    assert "reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_source_row_crop_packet.csv" in step["inputs"]
    assert "reports/wrr_1994/wrr_source_row_ocr_word_packet.csv" in step["inputs"]
    assert "docs/WRR_SOURCE_ROW_REVIEW_BUNDLE.md" in step["outputs"]


def test_cities_source_row_lock_worksheet_tracks_decision_records_input() -> None:
    protocol = load_protocol("protocols/cities_source_row_lock_worksheet.toml")
    step = next(
        step
        for step in protocol["steps"]
        if step["id"] == "build_cities_source_row_lock_worksheet"
    )

    assert "data/study/mappings/cities_source_row_lock_decisions.csv" in step["inputs"]


def test_greek_new_terms_report_step_uses_specific_title() -> None:
    protocol = load_protocol("protocols/greek_surface_new_terms.toml")
    step = next(step for step in protocol["steps"] if step["id"] == "prospective_report")
    argv = step["argv"]

    assert argv[argv.index("--title") + 1] == "Greek Surface New Terms Prospective Report"


def test_clean_lock_results_summary_tracks_completed_lanes() -> None:
    text = Path("docs/CLEAN_LOCK_RESULTS_SUMMARY.md").read_text(encoding="utf-8")
    user_terms = Path("docs/USER_REQUESTED_PROSPECTIVE_TERMS.md").read_text(
        encoding="utf-8"
    )
    concordance_terms = Path("docs/HEBREW_CONCORDANCE_PROSPECTIVE_TERMS.md").read_text(
        encoding="utf-8"
    )

    assert "| Greek surface new terms | 236 |" in text
    assert "| Greek lexicon extension | 5,009 |" in text
    assert "2 all-source common-pronoun extension keys" in text
    assert "strict function-word rerun left 0 all-source keys" in text
    assert "| Hebrew Gospel/genealogy | 27 |" in text
    assert "| Hebrew concordance words | 3,577 |" in text
    assert "0 adjusted-support terms" in text
    assert "38 ordinary lexical prompts" in text
    assert "10" in text
    assert "high-volume short-string/common-letter prompts" in text
    assert "ordinary" in text
    assert "local surface-context/self-lexeme effects" in text
    assert "common-pronoun" in text
    assert "rows with surface-context support" in text
    assert "KJVA apocrypha bridge prospective lane used a committed" in text
    assert "current manifest/preflight workflow" in text
    assert "completed prospective protocols" in user_terms
    assert "completed negative controlled result" in concordance_terms
    assert "future prospective work" not in user_terms
    assert "future prospective work" not in concordance_terms


def test_greek_lexicon_preregistration_is_historical_not_future_run() -> None:
    text = Path("docs/GREEK_LEXICON_EXTENSION_PROSPECTIVE_PREREGISTRATION.md").read_text(
        encoding="utf-8"
    )
    source = Path("docs/GREEK_LEXICON_PROSPECTIVE_SOURCE.md").read_text(encoding="utf-8")
    protocol = load_protocol("protocols/greek_lexicon_extension_prospective_lock.toml")
    lock_step = next(step for step in protocol["steps"] if step["id"] == "lock_manifest")

    assert "historical preregistration for a completed lane" in text
    assert "completed context-cautioned review material" in text
    assert "## Completed Result Run" in text
    assert "## Future Result Run" not in text
    assert "result run not started" not in text
    assert "ready for lock manifest and preflight" not in text
    assert "historical source packet for the completed Greek lexicon extension" in source
    assert "completed result report" in source
    assert "future result-producing study" not in source
    assert "completed Strong's Greek lexicon extension study" in protocol["description"]
    assert "completed result run" in lock_step["description"]
    assert "future result-producing run" not in lock_step["description"]


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
    normalized_text = " ".join(text.split())

    assert "## Clean-Lock Close-Out" in text
    assert "0 Hebrew concordance rows and 0 Greek surface rows" in text
    assert "0 all-source extension keys" in text
    assert "`docs/GREEK_LEXICON_EXTENSION_PROSPECTIVE_REPORT.md`" in text
    assert "`docs/STRICT_FOLLOWUP_GATE_SUMMARY.md`" in text
    assert "genuinely new clean source or source-family question" in normalized_text
    assert "exclusion gates, and controls frozen" in normalized_text
    assert "proper next step is a narrower locked prospective study" not in normalized_text

    draft = Path("docs/FINAL_REPORT_DRAFT.md").read_text(encoding="utf-8")
    outline = Path("docs/FINAL_REPORT_OUTLINE.md").read_text(encoding="utf-8")
    normalized_draft = " ".join(draft.split())
    normalized_outline = " ".join(outline.split())
    assert "0 Hebrew concordance" in draft
    assert "0 all-source extension keys" in draft
    assert "`docs/STRICT_FOLLOWUP_GATE_SUMMARY.md`" in outline
    assert "apocrypha/deuterocanon bridge comparison is now present" in normalized_draft
    assert "apocrypha/deuterocanon bridge study and KJVA bridge controls are now completed" in normalized_outline
    assert "After the current report baseline is frozen" not in normalized_draft
    assert "finish any remaining locked reports" not in normalized_outline


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


def test_apocrypha_bridge_study_is_current_review_layer() -> None:
    text = Path("docs/APOCRYPHA_BRIDGE_STUDY.md").read_text(encoding="utf-8")
    normalized_text = " ".join(text.split())

    assert "completed bridge-completion review layer" in normalized_text
    assert "already-declared corpora" in normalized_text
    assert "The bridge study records these output classes" in normalized_text
    assert "planned follow-on study" not in normalized_text
    assert "After that baseline is frozen" not in normalized_text
    assert "The bridge study should produce" not in normalized_text


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
    normalized_readme = " ".join(readme.split())

    assert "fast-validate: test indexes" in makefile
    assert "git diff --check" in makefile
    assert "scripts.check_public_release_hygiene --allow-dirty" in makefile
    assert "scripts.check_expanded_strata_tooling" in makefile
    assert "scripts.check_project_findings_overview_doc" in makefile
    assert "scripts.check_public_claim_language" in makefile
    assert "$(MAKE) protocol-files" in makefile
    assert "$(MAKE) corpus-configs" in makefile
    assert "$(MAKE) term-files" in makefile
    assert "$(MAKE) study-mapping-schemas" in makefile
    assert "$(MAKE) local-data-doc-check" in makefile
    assert "make fast-validate" in readme
    assert "expanded-strata operator tooling" in readme
    assert "general-reader findings overview" in readme
    assert "checks public claim language" in readme
    assert "protocol TOML files" in readme
    assert "corpus config schemas" in normalized_readme
    assert "term-file schema/normalization" in normalized_readme
    assert "study-mapping guard suite" in readme


def test_study_mapping_make_target_runs_all_mapping_guards() -> None:
    makefile = Path("Makefile").read_text(encoding="utf-8")
    study_mapping_doc = Path("docs/STUDY_MAPPING_SCHEMAS.md").read_text(encoding="utf-8")
    mappings_readme = Path("data/study/mappings/README.md").read_text(encoding="utf-8")

    expected = [
        "scripts.validate_study_mapping_schemas",
        "scripts.check_study_mapping_term_ids",
        "scripts.check_wrr_manual_decision_records",
        "scripts.check_cities_ocr_page_review_decisions",
        "scripts.check_cities_source_row_lock_decision_records",
        "scripts.check_cities_source_transcription_decision_records",
    ]

    assert "study-mapping-schemas:" in makefile
    for command in expected:
        assert command in makefile
        assert command in study_mapping_doc
        assert command in mappings_readme


def test_mapping_status_docs_track_seed_rows_and_guard_suite() -> None:
    hypothesis = Path("docs/HYPOTHESIS_ANALYSIS_FRAMEWORK.md").read_text(encoding="utf-8")
    match_status = Path("docs/MATCH_TYPE_EXTENSION_STATUS.md").read_text(encoding="utf-8")
    real_report = Path("docs/REAL_REPORT_RUN.md").read_text(encoding="utf-8")

    assert "conservative seed rows" in hypothesis
    assert "make study-mapping-schemas" in hypothesis
    assert "Mapping files are header-only planning artifacts until populated" not in hypothesis

    assert "conservative seed rows" in match_status
    assert "make study-mapping-schemas" in match_status

    assert "study-mapping CSV schemas retain exact columns" in real_report
    assert "ISO\n  `locked_at` dates" in real_report
    assert "tracked term IDs" in real_report


def test_release_ready_make_target_wraps_handoff_and_release_checks() -> None:
    makefile = Path("Makefile").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    normalized_readme = " ".join(readme.split())

    assert "release-ready: fast-validate public-release-check" in makefile
    assert "scripts.check_doc_command_references" in makefile
    assert "scripts.check_project_findings_overview_doc" in makefile
    assert "$(MAKE) protocol-files" in makefile
    assert "$(MAKE) corpus-configs" in makefile
    assert "$(MAKE) term-files" in makefile
    assert "$(MAKE) study-mapping-schemas" in makefile
    assert "make release-ready" in readme
    assert "validates documented script/source-path references" in normalized_readme
    assert "guards the general-reader findings overview" in normalized_readme
    assert "validates protocol TOML files" in normalized_readme
    assert "corpus config schemas" in normalized_readme
    assert "term-file schema/normalization" in normalized_readme
    assert "study-mapping guard suite" in normalized_readme
    assert "after committing" in readme
    assert "clean public-release gate" in readme
    assert "intentionally fails while tracked files are dirty" in normalized_readme


def test_remaining_work_register_tracks_latest_validation_snapshot() -> None:
    text = Path("docs/REMAINING_WORK_REGISTER.md").read_text(encoding="utf-8")

    assert "Latest validation snapshot after the release-ready make target" in text
    assert "1577 tests" in text
    assert "2 skipped, and 29196 subtests" in text
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


def test_wrr_support_docs_track_locked_local_method_boundary() -> None:
    replication = Path("docs/WRR_REPLICATION_PLAN.md").read_text(encoding="utf-8")
    methodology = Path("docs/WRR_METHODOLOGY_GAPS.md").read_text(encoding="utf-8")
    corrected = Path("docs/WRR_CORRECTED_DISTANCE_NOTES.md").read_text(
        encoding="utf-8"
    )

    combined = "\n".join([replication, methodology, corrected])
    assert "full cap-1000 corrected distances over 182 observed rows" in replication
    assert "999,999 date-label permutation" in replication
    assert "72 defined, 110 ordinary-not-valid, 0 under-minimum" in methodology
    assert "printed `D(w)` as main" in corrected
    assert "locked local evidence, not exact published reproduction" in combined
    assert "final `D(w)` formula decision" not in combined
    assert "optimized full corrected-distance run over the final locked pair universe" not in combined
    assert "choose one before final `D(w)` runs" not in combined


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

    assert "historical planning lock and closeout map" in text
    assert "no tracked lane remains `ready_for_preflight`" in text
    assert "fresh term/source target set and a" in text
    assert "## Track 4: Completed Clean-Lock Expansion" in text
    assert "0 Greek surface rows and 0 Hebrew concordance rows" in text
    assert "`prospective_controlled_review_candidate`" in text
    assert "one future prospective lane" not in text


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
