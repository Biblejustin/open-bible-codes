import csv
import os
import subprocess
import sys

import pytest


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(os.environ.get("EDLS_RUN_INTEGRATION") != "1", reason="integration smoke"),
]


def test_critical_omission_null_smoke(tmp_path):
    out_dir = tmp_path / "null"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.analyze_critical_omission_breaks_null",
            "--shuffles",
            "1",
            "--seed",
            "1",
            "--out-dir",
            str(out_dir),
            "--max-terms",
            "1",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "observed=" in result.stdout
    with (out_dir / "null_per_block.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows
    assert {"ref", "observed_breaks", "p_ge", "bh_q"} <= set(rows[0])
