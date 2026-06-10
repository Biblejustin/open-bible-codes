"""Tests for the Esther YHWH-acrostic scanner."""

from __future__ import annotations

from scripts.analyze_esther_yhwh_acrostics import (
    TRADITIONAL_REFS,
    word_stream,
    yhwh_windows,
)


def stream_of(words: list[str]):
    return [("ESTH", "5", "4", w) for w in words]


def test_yhwh_windows_initials_forward() -> None:
    # the Esther 5:4 shape: initials yod-he-vav-he across four words
    hits = yhwh_windows(stream_of(["יבוא", "המלך", "והמן", "היום"]))
    assert len(hits) == 1
    assert hits[0]["kind"] == "initials" and hits[0]["direction"] == "forward"


def test_yhwh_windows_initials_backward() -> None:
    # the Esther 1:20 shape: initials he-vav-he-yod read backward
    hits = yhwh_windows(stream_of(["היא", "וכל", "הנשים", "יתנו"]))
    assert len(hits) == 1
    assert hits[0]["kind"] == "initials" and hits[0]["direction"] == "backward"


def test_yhwh_windows_finals_both_directions() -> None:
    # finals forward (7:7 shape) and finals backward (5:13 shape)
    fwd = yhwh_windows(stream_of(["כי", "כלתה", "אליו", "הרעה"]))
    assert fwd and fwd[0]["kind"] == "finals" and fwd[0]["direction"] == "forward"
    bwd = yhwh_windows(stream_of(["זה", "איננו", "שוה", "לי"]))
    assert bwd and bwd[0]["kind"] == "finals" and bwd[0]["direction"] == "backward"


def test_yhwh_windows_no_false_hit() -> None:
    assert yhwh_windows(stream_of(["אבג", "דגב", "גבא", "באג"])) == []


def test_word_stream_filters_book_and_strips_points() -> None:
    vmap = {("ESTH", "1", "1"): "וַיְהִי בִּימֵי", ("GEN", "1", "1"): "בְּרֵאשִׁית"}
    esther = word_stream(vmap, book="ESTH")
    assert [w[3] for w in esther] == ["ויהי", "בימי"]
    everything = word_stream(vmap)
    assert len(everything) == 3


def test_traditional_refs_are_the_four_classical_spots() -> None:
    assert TRADITIONAL_REFS == {("ESTH", "1", "20"), ("ESTH", "5", "4"),
                                ("ESTH", "5", "13"), ("ESTH", "7", "7")}
