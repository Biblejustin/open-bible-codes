from pathlib import Path

from els.protocol_runner import load_protocol


PROTOCOL = Path("protocols/doxa_four_source_claim_followup.toml")
PREREG = Path("docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_PREREGISTRATION.md")
TARGET_KEY = "δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ"


def test_doxa_followup_protocol_locks_registered_key_and_controls() -> None:
    protocol = load_protocol(PROTOCOL)
    paired = protocol["steps"][0]
    argv = paired["argv"]

    assert paired["id"] == "paired_controls"
    assert "--include-overlap-key" in argv
    assert TARGET_KEY in argv
    assert argv[argv.index("--term-control-samples") + 1] == "5000"
    assert argv[argv.index("--random-control-samples") + 1] == "5000"
    assert "reports/greek_exact_center_four_source/extensions_tcg_nt_top.csv" in argv
    assert "reports/greek_exact_center_four_source/extensions_sblgnt_top.csv" in argv


def test_doxa_followup_preregistration_states_boundary() -> None:
    text = PREREG.read_text(encoding="utf-8")

    assert TARGET_KEY in text
    assert "post-discovery locked follow-up" in text
    assert "hidden-path-only is meaningful review material" in text
    assert "`claim_followup_review_candidate`" in text
    assert "`confirmed_code`" in text
