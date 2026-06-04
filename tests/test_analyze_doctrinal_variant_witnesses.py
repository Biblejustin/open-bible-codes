"""Tests for the doctrinal-variant witness analysis helpers."""

from __future__ import annotations

from scripts.analyze_doctrinal_variant_witnesses import (
    chi2_2x2,
    classify_tradition_pattern,
    has_atonement,
    has_divine,
    wording_divine_direction,
    wording_token_direction,
)


def test_classify_tradition_pattern() -> None:
    # TR + Byzantine have it, Alexandrian omits -> genuine Byz-vs-Alex omission
    assert classify_tradition_pattern(True, True, False, False) == "alex_omits_byz_keeps"
    # TR has it, Byzantine AND Alexandrian omit -> TR-only (e.g. the Comma)
    assert classify_tradition_pattern(True, False, False, False) == "tr_only"
    # all four present -> wording-level variant
    assert classify_tradition_pattern(True, True, True, True) == "wording_variant"
    # not in TR at all
    assert classify_tradition_pattern(False, True, True, True) == "not_in_tr"


def test_chi2_2x2_independence_and_association() -> None:
    # perfectly independent table -> chi-square 0
    assert chi2_2x2(25, 25, 25, 25) == 0.0
    # strong association -> positive
    assert chi2_2x2(40, 10, 10, 40) > 0
    # empty table is defined as 0
    assert chi2_2x2(0, 0, 0, 0) == 0.0


def test_has_divine_folds_final_sigma() -> None:
    # nominative ends in final sigma; normalizer folds it so the token matches
    assert has_divine("θεὸς ἐφανερώθη ἐν σαρκί") is True
    assert has_divine("καὶ ἐπορεύθη ἕκαστος εἰς τὸν οἶκον") is False


def test_has_atonement_matches_blood_stem() -> None:
    assert has_atonement("τὴν ἀπολύτρωσιν διὰ τοῦ αἵματος αὐτοῦ") is True
    assert has_atonement("μέγα ἐστὶν τὸ τῆς εὐσεβείας μυστήριον") is False


def test_wording_divine_direction_tracks_each_side() -> None:
    # TR reads "God", WH reads "who": the deity token is a TR-side loss
    tr_drop, wh_gain = wording_divine_direction("Θεὸς ἐφανερώθη", "Ὃς ἐφανερώθη")
    assert "θεοσ" in tr_drop and wh_gain == []
    # John 1:18: WH gains the deity token (Son -> God)
    tr_drop2, wh_gain2 = wording_divine_direction(
        "ὁ μονογενὴς υἱός ὁ ὢν", "μονογενὴς θεὸς ὁ ὢν"
    )
    assert "θεοσ" in wh_gain2


def test_wording_token_direction_counts_total_and_divine() -> None:
    # TR has three extra words including one divine token; WH gains none
    counts = wording_token_direction("ἐκκλησίαν τοῦ θεοῦ ἁγίου", "ἐκκλησίαν")
    assert counts["tr_total"] == 3 and counts["wh_total"] == 0
    assert counts["tr_divine"] == 1 and counts["wh_divine"] == 0
