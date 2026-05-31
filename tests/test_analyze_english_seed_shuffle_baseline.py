from scripts.analyze_english_seed_shuffle_baseline import read_label, stable_seed_offset


def test_seed_offset_is_stable_and_read_label_explains_outcome() -> None:
    assert stable_seed_offset("alpha") == stable_seed_offset("alpha")
    assert read_label(0, 0.9, None) == "absent in observed corpus"
    assert read_label(3, 0.04, None) == "observed above shuffled baseline floor"
    assert read_label(3, 0.9, 2.5) == "observed elevated vs shuffled mean"

