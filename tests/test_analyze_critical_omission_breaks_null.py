import csv
from pathlib import Path
from types import SimpleNamespace

from scripts.analyze_critical_omission_breaks_null import (
    write_distribution_csv,
    write_per_block_csv,
    write_summary_csv,
)


def test_null_writers_emit_distribution_summary_and_blocks(tmp_path: Path) -> None:
    distribution = tmp_path / "distribution.csv"
    summary = tmp_path / "summary.csv"
    blocks = tmp_path / "blocks.csv"

    write_distribution_csv(distribution, [2, 4])
    write_summary_csv(summary, 3, [2, 4], 0.5, 0.25, 7, 8)
    write_per_block_csv(
        blocks,
        [SimpleNamespace(ref="John 1:1", length=9)],
        [3],
        [[2], [4]],
        [0.5],
        [0.6],
    )

    with distribution.open(encoding="utf-8", newline="") as handle:
        assert list(csv.DictReader(handle))[1]["broken_total_hits"] == "4"
    with summary.open(encoding="utf-8", newline="") as handle:
        assert list(csv.DictReader(handle))[0]["observed_total"] == "3"
    with blocks.open(encoding="utf-8", newline="") as handle:
        assert list(csv.DictReader(handle))[0]["ref"] == "John 1:1"

