from pathlib import Path

from els.protocol_runner import load_protocol


PROTOCOL = Path("protocols/greek_expanded_prospective_exact_center.toml")
PREREG = Path("docs/GREEK_EXPANDED_PROSPECTIVE_PREREGISTRATION.md")


def test_expanded_prospective_protocol_uses_frozen_term_file_and_four_sources() -> None:
    protocol = load_protocol(PROTOCOL)
    surface = protocol["steps"][0]
    argv = surface["argv"]

    assert "terms/greek_expanded_prospective_terms.csv" in argv
    assert "TR_NT=configs/example_ebible_grctr.toml" in argv
    assert "BYZ_NT=configs/example_ebible_grcmt.toml" in argv
    assert "TCG_NT=configs/example_ebible_grctcgnt.toml" in argv
    assert "SBLGNT=configs/example_sblgnt.toml" in argv
    assert argv[argv.index("--max-skip") + 1] == "50"


def test_expanded_prospective_protocol_stops_before_controls() -> None:
    protocol = load_protocol(PROTOCOL)
    step_ids = [step["id"] for step in protocol["steps"]]

    assert step_ids[-1] == "pattern_presence"
    assert "paired_controls" not in step_ids
    assert "context_review" not in step_ids


def test_preregistration_declares_review_queue_boundary() -> None:
    text = PREREG.read_text(encoding="utf-8")

    assert "prospective candidate-discovery screen" in text
    assert "exclude every normalized form" in text
    assert "`prospective_review_queue_candidate`" in text
    assert "`confirmed_code`" in text
