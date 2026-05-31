from scripts.import_partition_worker_bundle import is_partition_artifact


def test_is_partition_artifact_accepts_only_safe_partition_members() -> None:
    assert is_partition_artifact("reports/dynamic_skip_focus/partitions/p1.csv.gz")
    assert is_partition_artifact("reports/dynamic_skip_focus/partitions/p1.manifest.json")
    assert not is_partition_artifact("../reports/dynamic_skip_focus/partitions/p1.csv")
    assert not is_partition_artifact("/reports/dynamic_skip_focus/partitions/p1.csv")
    assert not is_partition_artifact("reports/dynamic_skip_focus/worker_bundle_manifest.json")

