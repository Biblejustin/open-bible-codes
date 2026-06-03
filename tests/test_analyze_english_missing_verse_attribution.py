from scripts.analyze_english_missing_verse_attribution import (
    hit_missing_verse_attribution,
    inserted_blocks_from_augmented,
    missing_baseline_verses,
    ref_gap_category,
    _toy_corpus,
)


def test_missing_baseline_verses_detects_ref_absent_from_target() -> None:
    baseline = _toy_corpus("KJV", [("GEN 1:1", 4), ("GEN 1:2", 3), ("GEN 1:3", 4)])
    target = _toy_corpus("NIV", [("GEN 1:1", 4), ("GEN 1:3", 4)])

    missing = missing_baseline_verses(baseline, target)

    assert [verse.ref for verse in missing] == ["GEN 1:2"]


def test_hit_crossing_inserted_ref_is_attributed() -> None:
    base = _toy_corpus("base", [("GEN 1:1", 4), ("GEN 1:3", 4)])
    augmented = _toy_corpus("augmented", [("GEN 1:1", 4), ("GEN 1:2", 2), ("GEN 1:3", 4)])
    blocks = inserted_blocks_from_augmented(augmented, ["GEN 1:2"])

    attribution, refs = hit_missing_verse_attribution(
        base,
        augmented,
        blocks,
        start=3,
        skip=1,
        normalized_length=2,
    )

    assert attribution == "missing_verse_attributed"
    assert refs == ["GEN 1:2"]


def test_hit_before_inserted_ref_is_not_attributed() -> None:
    base = _toy_corpus("base", [("GEN 1:1", 4), ("GEN 1:3", 4)])
    augmented = _toy_corpus("augmented", [("GEN 1:1", 4), ("GEN 1:2", 2), ("GEN 1:3", 4)])
    blocks = inserted_blocks_from_augmented(augmented, ["GEN 1:2"])

    attribution, refs = hit_missing_verse_attribution(
        base,
        augmented,
        blocks,
        start=0,
        skip=1,
        normalized_length=2,
    )

    assert attribution == "not_missing_verse_related"
    assert refs == []


def test_no_missing_refs_reports_no_missing_refs_for_version() -> None:
    base = _toy_corpus("base", [("GEN 1:1", 4)])
    augmented = _toy_corpus("augmented", [("GEN 1:1", 4)])

    attribution, refs = hit_missing_verse_attribution(
        base,
        augmented,
        [],
        start=0,
        skip=1,
        normalized_length=2,
    )

    assert attribution == "no_missing_kjv_refs_for_version"
    assert refs == []


def test_ref_gap_category_marks_known_nt_disputed_refs() -> None:
    assert ref_gap_category("ACT 8:37") == "known_nt_disputed_kjv_ref"
    assert ref_gap_category("NUM 1:21") == "other_reference_gap"
