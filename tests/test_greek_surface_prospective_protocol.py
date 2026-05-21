import csv
from pathlib import Path

from scripts.build_greek_surface_prospective_report import (
    PREFLIGHT_IN,
    display_report_term,
    interpretation_read,
    primary_filter_read,
    preflight_artifact,
    registered_outcome,
    report_status,
)
from els.protocol_runner import load_protocol
from scripts.analyze_greek_expanded_surface_triage import triage_read_lines
from scripts.analyze_greek_surface_control_evaluation import control_read_lines
from scripts.analyze_greek_surface_letter_paths import letter_path_read_lines
from scripts.check_preregistration_placeholders import find_placeholders


PROTOCOL = Path("protocols/greek_surface_prospective.toml")
LENGTH4_PROTOCOL = Path("protocols/greek_surface_length4_followup.toml")
LENGTH4_VOCAB_PROTOCOL = Path("protocols/greek_surface_length4_vocabulary_controls.toml")
PREREG = Path("docs/GREEK_SURFACE_PROSPECTIVE_PREREGISTRATION.md")
TERMS = Path("terms/greek_surface_prospective_terms.csv")


def test_surface_prospective_protocol_uses_filtered_term_file_and_four_sources() -> None:
    protocol = load_protocol(PROTOCOL)
    surface = protocol["steps"][0]
    argv = surface["argv"]

    assert protocol["name"] == "greek_surface_prospective"
    assert "terms/greek_surface_prospective_terms.csv" in argv
    assert "TR_NT=configs/example_ebible_grctr.toml" in argv
    assert "BYZ_NT=configs/example_ebible_grcmt.toml" in argv
    assert "TCG_NT=configs/example_ebible_grctcgnt.toml" in argv
    assert "SBLGNT=configs/example_sblgnt.toml" in argv
    assert argv[argv.index("--max-skip") + 1] == "50"
    assert argv[argv.index("--direction") + 1] == "both"


def test_surface_prospective_protocol_includes_registered_control_and_path_steps() -> None:
    protocol = load_protocol(PROTOCOL)
    step_ids = [step["id"] for step in protocol["steps"]]

    assert step_ids == [
        "surface_context",
        "surface_queue",
        "surface_triage",
        "available_control_pool",
        "available_control_evaluation",
        "letter_paths",
        "prospective_report",
    ]


def test_length4_followup_protocol_is_post_discovery_and_uses_length4_gate() -> None:
    protocol = load_protocol(LENGTH4_PROTOCOL)
    step_ids = [step["id"] for step in protocol["steps"]]
    triage = protocol["steps"][0]
    argv = triage["argv"]

    assert protocol["name"] == "greek_surface_length4_followup"
    assert step_ids == [
        "length4_triage",
        "available_control_pool",
        "available_control_evaluation",
        "letter_paths",
    ]
    assert argv[argv.index("--min-length") + 1] == "4"
    assert "reports/greek_surface_prospective/surface_patterns.csv" in argv
    assert "post-discovery" in argv[argv.index("--status") + 1]


def test_length4_vocabulary_control_protocol_uses_generated_reports_terms() -> None:
    protocol = load_protocol(LENGTH4_VOCAB_PROTOCOL)
    step_ids = [step["id"] for step in protocol["steps"]]
    surface_context = protocol["steps"][1]
    control_pool = protocol["steps"][4]

    assert protocol["name"] == "greek_surface_length4_vocabulary_controls"
    assert step_ids == [
        "vocabulary_terms",
        "surface_context",
        "surface_queue",
        "surface_cohort",
        "vocabulary_control_pool",
        "vocabulary_control_evaluation",
    ]
    assert "reports/greek_surface_length4_vocab_controls/terms.csv" in surface_context["argv"]
    assert control_pool["argv"][control_pool["argv"].index("--top-controls") + 1] == "200"
    assert "--max-markdown-controls" in control_pool["argv"]


def test_surface_prospective_terms_exclude_prior_selected_rows() -> None:
    with TERMS.open("r", encoding="utf-8", newline="") as handle:
        term_ids = {row["term_id"] for row in csv.DictReader(handle)}

    assert len(term_ids) == 288
    assert "gpx_isaac_g" not in term_ids
    assert "gpx_lawlessness_g" not in term_ids
    assert "gpx_wonder_g" not in term_ids


def test_surface_prospective_preregistration_has_no_placeholders() -> None:
    assert list(find_placeholders(PREREG, allowed=set())) == []


def test_zero_selected_report_reads_are_negative_not_stale_queue_text() -> None:
    assert "No row met the registered all-source" in triage_read_lines([], 24)[0]
    assert "No row reached the registered triage stage" in control_read_lines([])[0]
    assert "No selected rows were available" in letter_path_read_lines([])[0]
    assert report_status([], []) == "negative_primary_filter_result; no claim"
    assert "No row met the registered" in registered_outcome([], [])


def test_preflight_artifact_uses_payload_path_with_default_fallback() -> None:
    assert preflight_artifact(
        {"output_path": "reports/custom.preflight.json"}
    ) == "reports/custom.preflight.json"
    assert preflight_artifact({}) == str(PREFLIGHT_IN)


def test_surface_report_term_display_adds_transliteration_and_english() -> None:
    assert (
        display_report_term({"normalized_term": "σιων", "concept": "Zion"})
        == "`σιων` (Sion; English: Zion)"
    )
    assert (
        display_report_term({"normalized_term": "ονομα", "concept": "ὄνομα"})
        == "`ονομα` (onoma; English: Name)"
    )


def test_surface_report_interpretation_tracks_selected_rows() -> None:
    assert "no all-source rows" in primary_filter_read([])
    assert "1 selected review rows" in primary_filter_read([{"term_id": "demo"}])
    assert "negative result" in interpretation_read([], [])
    assert "controlled review material" in interpretation_read(
        [{"term_id": "demo"}],
        [{"all_source_q_value": "0.01"}],
    )


def test_report_steps_track_term_display_dependency() -> None:
    protocol = load_protocol(PROTOCOL)
    length4 = load_protocol(LENGTH4_PROTOCOL)
    vocab = load_protocol(LENGTH4_VOCAB_PROTOCOL)

    checked_steps = [
        (protocol, "surface_queue"),
        (protocol, "surface_triage"),
        (protocol, "available_control_pool"),
        (protocol, "available_control_evaluation"),
        (protocol, "letter_paths"),
        (protocol, "prospective_report"),
        (length4, "length4_triage"),
        (length4, "available_control_evaluation"),
        (vocab, "surface_queue"),
        (vocab, "surface_cohort"),
        (vocab, "vocabulary_control_evaluation"),
    ]

    for current_protocol, step_id in checked_steps:
        step = next(step for step in current_protocol["steps"] if step["id"] == step_id)
        assert "els/term_display.py" in step["inputs"], step_id
