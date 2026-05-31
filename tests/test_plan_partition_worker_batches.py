import pytest

from scripts.plan_partition_worker_batches import parse_worker_weights


def test_parse_worker_weights_defaults_and_rejects_unknown_labels() -> None:
    assert parse_worker_weights(2, "box", ["box_01=2.5"]) == {
        "box_01": 2.5,
        "box_02": 1.0,
    }
    with pytest.raises(ValueError, match="unknown worker label"):
        parse_worker_weights(2, "box", ["box_03=2"])

