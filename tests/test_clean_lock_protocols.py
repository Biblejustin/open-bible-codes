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


def test_greek_surface_context_review_tracks_manual_read() -> None:
    text = Path("docs/GREEK_SURFACE_NEW_TERMS_CONTEXT_REVIEW.md").read_text(encoding="utf-8")

    assert "# Greek Surface New Terms Context Review" in text
    assert "direct surface/self-lexeme hit" in text
    assert "ordinary \"name\" passages" in text
    assert "review-material" in text
    assert "category" in text
