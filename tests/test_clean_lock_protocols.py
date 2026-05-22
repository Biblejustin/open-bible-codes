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
    assert "`docs/STRICT_FOLLOWUP_GATE_SUMMARY.md`" in text

    draft = Path("docs/FINAL_REPORT_DRAFT.md").read_text(encoding="utf-8")
    outline = Path("docs/FINAL_REPORT_OUTLINE.md").read_text(encoding="utf-8")
    assert "0 Hebrew concordance" in draft
    assert "`docs/STRICT_FOLLOWUP_GATE_SUMMARY.md`" in outline


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


def test_next_lock_tracks_completed_clean_lock_expansion() -> None:
    text = Path("docs/PROSPECTIVE_STUDY_NEXT_LOCK.md").read_text(encoding="utf-8")

    assert "## Track 4: Completed Clean-Lock Expansion" in text
    assert "0 Greek surface rows and 0 Hebrew concordance rows" in text
    assert "`prospective_controlled_review_candidate`" in text


def test_prospective_readiness_marks_current_profiles_closed() -> None:
    readiness = Path("docs/PROSPECTIVE_STUDY_READINESS.md").read_text(encoding="utf-8")
    manifests = Path("docs/STUDY_LOCK_MANIFESTS.md").read_text(encoding="utf-8")

    assert "There is no remaining `ready_for_preflight`" in readiness
    assert "lane" in readiness
    assert "Do not rerun a completed profile as a claim lane" in readiness
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
