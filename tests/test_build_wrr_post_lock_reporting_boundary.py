import csv
import json
from pathlib import Path

from scripts import build_wrr_post_lock_reporting_boundary as boundary


def test_build_boundary_rows_separates_allowed_and_forbidden_language(tmp_path: Path) -> None:
    args = boundary.build_parser().parse_args(_argv(tmp_path))
    rows = boundary.build_boundary_rows(_inputs(), args)

    by_key = {(row["section"], row["item"]): row for row in rows}
    assert by_key[("allowed", "local_locked_method_language")]["status"] == "ready"
    assert "4 readiness gates ready" in by_key[
        ("allowed", "local_locked_method_language")
    ]["value"]
    assert by_key[("not_allowed", "exact_published_reproduction_language")][
        "status"
    ] == "forbidden"
    assert by_key[("not_allowed", "exact_published_reproduction_language")][
        "value"
    ] == "72 of 163 defined; gap 91"
    assert by_key[("source_boundary", "manual_decision_records")]["value"] == (
        "37 locked; 0 unlocked; method_lock=11; no_source_change=26"
    )
    assert by_key[("source_boundary", "source_changes")]["status"] == "none_selected"
    assert by_key[("method_boundary", "method_locks")]["value"] == "11 method_lock rows"
    assert by_key[("residual_gap", "remaining_163_distance_gap")]["value"] == "91"
    assert by_key[("next_action", "post_lock_reporting_boundary")][
        "status"
    ] == "complete"


def test_main_writes_csv_markdown_and_manifest(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)
    out = tmp_path / "boundary.csv"
    markdown = tmp_path / "boundary.md"
    manifest = tmp_path / "manifest.json"

    code = boundary.main(
        [
            "--claim-readiness",
            str(paths["readiness"]),
            "--locked-method-report",
            str(paths["locked"]),
            "--dashboard",
            str(paths["dashboard"]),
            "--priority-packet",
            str(paths["priority"]),
            "--manual-decision-records",
            str(paths["records"]),
            "--out",
            str(out),
            "--markdown-out",
            str(markdown),
            "--manifest-out",
            str(manifest),
        ]
    )

    assert code == 0
    rows = list(csv.DictReader(out.open("r", encoding="utf-8", newline="")))
    assert rows[0]["item"] == "local_locked_method_language"
    text = markdown.read_text(encoding="utf-8")
    assert "Status: post-lock reporting boundary locked." in text
    assert "Exact published WRR reproduction | `forbidden` | 72 of 163 defined; gap 91" in text
    assert "Do not say exact published WRR reproduced." in text
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["tool"] == "build_wrr_post_lock_reporting_boundary.py"
    assert payload["rows"] == len(rows)


def _argv(tmp_path: Path) -> list[str]:
    return [
        "--claim-readiness",
        str(tmp_path / "readiness.csv"),
        "--locked-method-report",
        str(tmp_path / "locked.csv"),
        "--dashboard",
        str(tmp_path / "dashboard.csv"),
        "--priority-packet",
        str(tmp_path / "priority.csv"),
        "--manual-decision-records",
        str(tmp_path / "records.csv"),
    ]


def _inputs() -> dict[str, list[dict[str, str]]]:
    return {
        "claim_readiness": [
            {"decision_area": str(i), "ready": "true"} for i in range(4)
        ],
        "locked_method_report": [
            {
                "section": "status",
                "item": "report_status",
                "value": "locked local WRR method report; not an exact published WRR reproduction",
            }
        ],
        "dashboard": [
            {
                "section": "gap",
                "item": "source_cited_defined_distances",
                "value": "163",
            },
            {
                "section": "gap",
                "item": "current_defined_distances",
                "value": "72",
            },
            {"section": "gap", "item": "remaining_gap", "value": "91"},
            {
                "section": "variant_upper_bound",
                "item": "residual_after_simple_variants",
                "value": "40",
            },
        ],
        "priority_packet": [
            {
                "section": "priority_lane",
                "item": "post-lock reporting boundary",
                "boundary": "describe the residual gap as exact-reproduction work, not pending source edits",
            }
        ],
        "manual_decision_records": [
            {"decision_status": "locked", "selected_action": "no_source_change"}
            for _ in range(26)
        ]
        + [
            {"decision_status": "locked", "selected_action": "method_lock"}
            for _ in range(11)
        ],
    }


def _write_inputs(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "readiness": tmp_path / "readiness.csv",
        "locked": tmp_path / "locked.csv",
        "dashboard": tmp_path / "dashboard.csv",
        "priority": tmp_path / "priority.csv",
        "records": tmp_path / "records.csv",
    }
    write_csv(paths["readiness"], ["decision_area", "ready"], _inputs()["claim_readiness"])
    write_csv(
        paths["locked"],
        ["section", "item", "value"],
        _inputs()["locked_method_report"],
    )
    write_csv(paths["dashboard"], ["section", "item", "value"], _inputs()["dashboard"])
    write_csv(
        paths["priority"],
        ["section", "item", "boundary"],
        _inputs()["priority_packet"],
    )
    write_csv(
        paths["records"],
        ["decision_status", "selected_action"],
        _inputs()["manual_decision_records"],
    )
    return paths


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
