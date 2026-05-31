from argparse import Namespace

from scripts.triage_english_version_controls import (
    merged_presence_scope,
    parse_hit_counts,
    read_label,
    triage_flag,
)


def test_triage_helpers_parse_counts_and_label_flags() -> None:
    args = Namespace(min_length=4, rare_control_count=1, rare_control_rate=0.05)

    assert parse_hit_counts("KJV:2; BSB:0") == {"KJV": 2, "BSB": 0}
    assert merged_presence_scope(2, 3) == "source_specific"
    flag = triage_flag(
        length=5,
        target_present_count=2,
        target_observed_count=10,
        control_present_count=0,
        control_present_rate=0,
        delta=0.5,
        args=args,
    )
    assert flag == "target_multi_control_absent"
    assert read_label(flag, 5, 2, 0) == "target multi-source hit; absent in controls"
