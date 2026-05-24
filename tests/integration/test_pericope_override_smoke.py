import csv
import os
import subprocess
import sys

import pytest


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(os.environ.get("EDLS_RUN_INTEGRATION") != "1", reason="integration smoke"),
]


def test_pericope_override_smoke(tmp_path):
    suffix = "_integration_pericope"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.analyze_critical_omission_breaks",
            "--treat-as-deleted",
            "protocols/treat_as_deleted/critical_consensus.csv",
            "--extra-terms",
            "terms/pericope_adulterae_terms.csv",
            "--out-suffix",
            suffix,
            "--max-terms",
            "1",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    with open(f"reports/critical_omission_missing_verses{suffix}.csv", newline="") as handle:
        rows = list(csv.DictReader(handle))
    pericope_rows = [row for row in rows if row["ref"].startswith("JHN 7:") or row["ref"].startswith("JHN 8:")]
    assert len(pericope_rows) == 12
