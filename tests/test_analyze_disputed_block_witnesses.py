"""Tests for the disputed-block witness analysis helpers."""

from __future__ import annotations

from scripts.analyze_disputed_block_witnesses import (
    block_codes,
    classify_block,
    fmt_ref,
    is_present,
)


def test_block_codes_range() -> None:
    assert block_codes(41, 16, 9, 20) == [f"41016{v:03d}" for v in range(9, 21)]
    assert block_codes(43, 5, 4, 4) == ["43005004"]


def test_is_present_distinguishes_absent_marker_and_lacuna() -> None:
    w = {"43008007": "ο αναμαρτητος", "43008008": "-", }
    assert is_present(w, "43008007") is True
    assert is_present(w, "43008008") is False   # marked absent
    assert is_present(w, "43008009") is False   # not covered at all


def test_classify_block_include_omit_lacuna() -> None:
    codes = ["43008003", "43008004", "43008005", "43008006"]
    have = dict.fromkeys(codes, "text")
    assert classify_block(have, codes) == ("include", 4, 4)
    absent = dict.fromkeys(codes, "-")
    assert classify_block(absent, codes) == ("omit", 0, 4)
    assert classify_block({}, codes) == ("lacuna", 0, 0)


def test_classify_block_half_threshold_counts_as_include() -> None:
    codes = ["a", "b", "c", "d"]
    half = {"a": "x", "b": "x", "c": "-", "d": "-"}
    # exactly half present -> include (present*2 >= covered)
    assert classify_block(half, codes) == ("include", 2, 4)


def test_fmt_ref() -> None:
    assert fmt_ref("43007053") == "43:7:53"
    assert fmt_ref("41016009") == "41:16:9"
