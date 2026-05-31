from scripts.analyze_word_counts import count_fields, multiple_flag_fields


def test_count_fields_records_default_multiple_flags() -> None:
    fields = count_fields(6)
    flags = multiple_flag_fields(fields)

    assert fields["multiples"] == "3"
    assert flags["multiple_3"] is True
    assert flags["multiple_7"] is False
