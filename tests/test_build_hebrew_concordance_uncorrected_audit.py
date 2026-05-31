from scripts import build_hebrew_concordance_uncorrected_audit as audit


def test_uncorrected_audit_flags_short_high_volume_names() -> None:
    row = {
        "category": "strong_proper_names",
        "normalized_length": "4",
        "exact_all_source_patterns": "2000",
        "exact_total_hits": "50000",
    }

    flags = audit.classify_row(row)

    assert flags == [
        "no_adjusted_support",
        "short_string",
        "high_pattern_volume",
        "proper_name_gloss",
    ]
    assert audit.primary_read(row, flags).startswith("high-volume short-string")

