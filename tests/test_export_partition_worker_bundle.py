from pathlib import Path

from scripts.export_partition_worker_bundle import collect_artifacts


def test_collect_artifacts_requires_compressed_hits(tmp_path: Path) -> None:
    raw = tmp_path / "hits.csv"
    compressed = tmp_path / "hits.csv.gz"
    manifest = tmp_path / "hits.manifest.json"
    summary = tmp_path / "hits.md"
    raw.write_text("raw\n", encoding="utf-8")
    compressed.write_text("compressed\n", encoding="utf-8")
    manifest.write_text("{}\n", encoding="utf-8")
    summary.write_text("# summary\n", encoding="utf-8")
    row = {
        "partition_id": "p1",
        "out": str(raw),
        "manifest_out": str(manifest),
        "summary_out": str(summary),
    }

    manifest_payload, files = collect_artifacts([row], require_compressed=True)

    assert manifest_payload["completed"] == ["p1"]
    assert manifest_payload["missing"] == []
    assert compressed in files
    assert raw not in files

