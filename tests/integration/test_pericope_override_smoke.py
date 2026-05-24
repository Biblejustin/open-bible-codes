import csv
import glob
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
    partial_rows = [row for row in rows if row["ref"] == "LUK 23:34a"]
    assert len(partial_rows) == 1
    assert partial_rows[0]["status"] == "explicit_deleted_partial_ref"
    father_summary = f"reports/critical_omission_breaks_treat_as_deleted_father_forgive_them{suffix}_summary.csv"
    assert os.path.exists(father_summary)
    for summary_path in glob.glob(f"reports/critical_omission_breaks_treat_as_deleted_*{suffix}_summary.csv"):
        examples_path = summary_path.replace("_summary.csv", "_examples.csv")
        with open(summary_path, newline="") as handle:
            summary_rows = list(csv.DictReader(handle))
        with open(examples_path, newline="") as handle:
            example_rows = list(csv.DictReader(handle))
        summary_total = sum(int(row["broken_total_hits"]) for row in summary_rows)
        assert summary_total == len(example_rows)
