import csv
import json
from pathlib import Path

from scripts import build_wrr_locked_method_report as report


def test_build_report_rows_summarizes_locks_and_boundaries(tmp_path: Path) -> None:
    args = report.build_parser().parse_args(
        [
            "--method-status",
            str(tmp_path / "method.csv"),
            "--readiness",
            str(tmp_path / "readiness.csv"),
            "--lock-options",
            str(tmp_path / "locks.csv"),
            "--manual-worksheet",
            str(tmp_path / "manual.csv"),
            "--corrected-distance-summary",
            str(tmp_path / "corrected_summary.csv"),
            "--corrected-distance-aggregate",
            str(tmp_path / "aggregate.csv"),
            "--permutation-summary",
            str(tmp_path / "permutation.csv"),
            "--primary-result-table",
            str(tmp_path / "primary.csv"),
            "--defined-pair-summary",
            str(tmp_path / "defined.csv"),
        ]
    )
    inputs = _inputs()

    rows = report.build_report_rows(inputs, args)

    by_key = {(row["section"], row["item"]): row for row in rows}
    assert by_key[("lock", "Pair universe")]["value"] == "keep_all_working_source"
    assert by_key[("lock", "Manual decisions")]["value"] == (
        "37 locked rows: 26 no_source_change; 11 method_lock"
    )
    assert by_key[("local_result", "defined_c_values")]["value"] == "72"
    assert by_key[("local_result", "rho_values")]["value"].endswith("rho0=0.000404")
    assert by_key[("boundary", "source_defined_gap")]["value"] == (
        "defined 72 of 163; gap 91"
    )


def test_main_writes_csv_markdown_and_manifest(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)
    out = tmp_path / "report.csv"
    markdown = tmp_path / "report.md"
    manifest = tmp_path / "manifest.json"

    code = report.main(
        [
            "--method-status",
            str(paths["method"]),
            "--readiness",
            str(paths["readiness"]),
            "--lock-options",
            str(paths["locks"]),
            "--manual-worksheet",
            str(paths["manual"]),
            "--corrected-distance-summary",
            str(paths["corrected_summary"]),
            "--corrected-distance-aggregate",
            str(paths["aggregate"]),
            "--permutation-summary",
            str(paths["permutation"]),
            "--primary-result-table",
            str(paths["primary"]),
            "--defined-pair-summary",
            str(paths["defined"]),
            "--out",
            str(out),
            "--markdown-out",
            str(markdown),
            "--manifest-out",
            str(manifest),
        ]
    )

    assert code == 0
    assert out.exists()
    text = markdown.read_text(encoding="utf-8")
    assert "Status: locked local WRR method report; not an exact published WRR reproduction." in text
    assert "Pair universe: keep_all_working_source" in text
    assert "Manual decisions: 37 locked rows: 26 no_source_change; 11 method_lock" in text
    assert "rho0 | 0.000404" in text
    assert "Do not describe this as an exact published WRR reproduction." in text
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["tool"] == "build_wrr_locked_method_report"
    assert payload["manual_decision_rows"] == 37


def _inputs() -> report.LoadedInputs:
    return report.LoadedInputs(
        method_status=[
            {
                "decision_area": "Pair universe",
                "status": "source_locked",
                "evidence": "source policy selected: keep_all_working_source",
            },
            {
                "decision_area": "D(w) skip-cap formula",
                "status": "source_locked",
                "evidence": "printed formula selected as main",
            },
            {
                "decision_area": "Corrected distance c(w,w')",
                "status": "defined_full_run",
                "evidence": "full all-lane cap 1000 run",
            },
            {
                "decision_area": "Aggregate statistic and permutation",
                "status": "permutation_locked",
                "evidence": "locked keep-all cap1000 999999 date-label permutation",
            },
        ],
        readiness=[
            {
                "decision_area": "Pair universe",
                "status": "source_locked",
                "ready": "true",
                "current_read": "selected source policy",
            },
            {
                "decision_area": "D(w) skip-cap formula",
                "status": "source_locked",
                "ready": "true",
                "current_read": "selected formula",
            },
            {
                "decision_area": "Corrected distance c(w,w')",
                "status": "defined_full_run",
                "ready": "true",
                "current_read": "full run exists",
            },
            {
                "decision_area": "Aggregate statistic and permutation",
                "status": "permutation_locked",
                "ready": "true",
                "current_read": "permutation locked",
            },
        ],
        lock_options=[
            {
                "area": "Pair universe",
                "status": "selected_working_source_policy",
                "evidence": "182 imported same-record pairs",
            },
            {
                "area": "D(w) skip-cap formula",
                "status": "source_locked_primary_formula",
                "evidence": "printed formula selected",
            },
            {
                "area": "Permutation",
                "status": "locked_local_permutation",
                "evidence": "999999 permutations",
            },
        ],
        manual_worksheet=[
            {"record_selected_action": "no_source_change"} for _ in range(26)
        ]
        + [{"record_selected_action": "method_lock"} for _ in range(11)],
        corrected_distance_summary=[
            {
                "pairs": "182",
                "defined_corrected_distances": "72",
                "ordinary_not_valid_pairs": "110",
                "status": "diagnostic_only_not_wrr_reproduction",
            }
        ],
        corrected_distance_aggregate=[
            {
                "rows": "182",
                "defined_corrected_distances": "72",
                "undefined_rows": "110",
                "p1": "0.00252257011468",
                "p2": "1.16472976875e-05",
                "p3": "0.0184584022574",
                "p4": "0.000274264355592",
                "status": "diagnostic_only_not_wrr_reproduction",
            }
        ],
        permutation_summary=[
            {
                "observed_rows": "182",
                "observed_defined_corrected_distances": "72",
                "rho_p1": "0.019722",
                "rho_p2": "0.000101",
                "rho_p3": "0.0506065",
                "rho_p4": "0.000535",
                "rho0_bonferroni": "0.000404",
                "status": "diagnostic_only_not_wrr_reproduction",
            }
        ],
        primary_result_table=[
            {
                "label": "G",
                "status": "found",
                "min_statistic": "P4",
                "min_rank": "4",
                "bonferroni_p0": "0.000016",
            }
        ],
        defined_pair_summary=[
            {
                "run_label": "all_lanes_cap1000",
                "defined": "72",
                "source_cited_defined_distances": "163",
                "defined_gap_to_source_cited": "91",
                "status": "diagnostic_only_not_wrr_reproduction",
            }
        ],
    )


def _write_inputs(tmp_path: Path) -> dict[str, Path]:
    inputs = _inputs()
    paths = {
        "method": tmp_path / "method.csv",
        "readiness": tmp_path / "readiness.csv",
        "locks": tmp_path / "locks.csv",
        "manual": tmp_path / "manual.csv",
        "corrected_summary": tmp_path / "corrected_summary.csv",
        "aggregate": tmp_path / "aggregate.csv",
        "permutation": tmp_path / "permutation.csv",
        "primary": tmp_path / "primary.csv",
        "defined": tmp_path / "defined.csv",
    }
    _write_csv(paths["method"], inputs.method_status)
    _write_csv(paths["readiness"], inputs.readiness)
    _write_csv(paths["locks"], inputs.lock_options)
    _write_csv(paths["manual"], inputs.manual_worksheet)
    _write_csv(paths["corrected_summary"], inputs.corrected_distance_summary)
    _write_csv(paths["aggregate"], inputs.corrected_distance_aggregate)
    _write_csv(paths["permutation"], inputs.permutation_summary)
    _write_csv(paths["primary"], inputs.primary_result_table)
    _write_csv(paths["defined"], inputs.defined_pair_summary)
    return paths


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
