"""Tests for the wording-divine chronology analysis helpers."""

from __future__ import annotations

from scripts.analyze_wording_divine_chronology import (
    byzantine_share,
    century_bucket,
    chi2_2x2,
    divine_counts,
    extra_divine_tokens,
    fmt_ref,
    token_direction,
    witness_side,
)


def test_divine_counts_folds_final_sigma() -> None:
    counts = divine_counts("θεὸς καὶ ὁ υἱός καὶ θεὸς")
    assert counts["θεοσ"] == 2  # nominative final sigma folded
    assert counts["υιοσ"] == 1


def test_token_direction_splits_total_and_divine() -> None:
    # TR adds "τοῦ θεοῦ" (a divine token + an article); WH adds nothing here
    counts = token_direction("ἐκκλησίαν τοῦ θεοῦ", "ἐκκλησίαν")
    assert counts["tr_total"] == 2 and counts["wh_total"] == 0
    assert counts["tr_divine"] == 1 and counts["wh_divine"] == 0


def test_extra_divine_tokens_finds_tr_extra() -> None:
    # TR reads "God manifest"; WH reads "who manifest" -> theos is TR-extra
    extra = extra_divine_tokens("θεὸς ἐφανερώθη", "ὃς ἐφανερώθη")
    assert ("θεοσ", 1, 0) in extra


def test_witness_side_agrees_by_count() -> None:
    assert witness_side(1, 1, 0) == "have"   # has the token -> longer reading
    assert witness_side(0, 1, 0) == "lack"   # lacks it -> shorter reading
    assert witness_side(1, 2, 0) == "ambiguous"  # between have(2) and lack(0)


def test_century_bucket_boundaries() -> None:
    assert century_bucket(200).startswith("II-III")
    assert century_bucket(250).startswith("II-III")
    assert century_bucket(350).startswith("III-IV")
    assert century_bucket(450).startswith("IV-V")


def test_chi2_2x2_zero_and_positive() -> None:
    assert chi2_2x2(25, 25, 25, 25) == 0.0
    assert chi2_2x2(320, 150, 9749, 7115) > 0


def test_byzantine_share() -> None:
    # Byzantine reading carries the divine token as fully as the TR -> shared
    assert byzantine_share("ποιμαίνειν τὴν ἐκκλησίαν τοῦ κυρίου καὶ θεοῦ", "θεου", 1) is True
    # Byzantine lacks it -> TR-only divine name
    assert byzantine_share("ποιμαίνειν τὴν ἐκκλησίαν", "θεου", 1) is False


def test_fmt_ref() -> None:
    assert fmt_ref("54003016") == "1Tim 3:16"
    assert fmt_ref("43001018") == "John 1:18"
