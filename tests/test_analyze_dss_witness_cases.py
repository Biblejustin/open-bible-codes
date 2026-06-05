"""Tests for the DSS witness-cases helpers."""

from __future__ import annotations

from scripts.analyze_dss_witness_cases import CASES, lookup


def test_lookup_uppercases_book_and_handles_none() -> None:
    vmap = {("ISA", "7", "14"): "text"}
    assert lookup(vmap, ("Isa", "7", "14")) == "text"
    assert lookup(vmap, ("ISA", "7", "14")) == "text"
    assert lookup(vmap, ("Isa", "7", "15")) == ""
    assert lookup(vmap, None) == ""


def test_cases_are_well_formed() -> None:
    # every case carries the fields the analysis needs and a recorded side
    for case in CASES:
        assert case["dss_sides_with"] in {"MT", "LXX", "both_differ"}
        assert isinstance(case["mt"], tuple) and len(case["mt"]) == 3
        assert isinstance(case["lxx"], tuple) and len(case["lxx"]) == 3
        assert case["note"]
