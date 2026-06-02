import csv
import json
from pathlib import Path

from scripts import build_no_input_blocker_summary as summary


def test_build_summary_counts_all_no_input_blockers() -> None:
    inputs = _inputs()
    rows = summary.build_lane_rows(inputs, summary.build_parser().parse_args([]))
    row = summary.build_summary(rows, inputs)

    assert row["lane_rows"] == 3
    assert row["total_status_rows"] == 26
    assert row["total_manual_input_needed_rows"] == 22
    assert row["result_allowed_lanes"] == 0
    assert row["blocked_result_lanes"] == 3
    assert row["wrr_remaining_gap"] == "91"
    assert row["cities_pending_transcription_rows"] == "14"
    assert row["kjva_blocked_gate_rows"] == "10"


def test_main_writes_csv_markdown_and_manifest(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)
    out = tmp_path / "status.csv"
    summary_out = tmp_path / "summary.csv"
    markdown = tmp_path / "summary.md"
    manifest = tmp_path / "manifest.json"

    code = summary.main(
        [
            "--wrr-status",
            str(paths["wrr_status"]),
            "--wrr-summary",
            str(paths["wrr_summary"]),
            "--cities-status",
            str(paths["cities_status"]),
            "--cities-summary",
            str(paths["cities_summary"]),
            "--kjva-status",
            str(paths["kjva_status"]),
            "--kjva-summary",
            str(paths["kjva_summary"]),
            "--out",
            str(out),
            "--summary-out",
            str(summary_out),
            "--markdown-out",
            str(markdown),
            "--manifest-out",
            str(manifest),
        ]
    )

    assert code == 0
    rows = list(csv.DictReader(out.open(encoding="utf-8", newline="")))
    assert [row["lane_id"] for row in rows] == ["wrr", "cities", "kjva"]
    assert all(row["result_allowed"] == "0" for row in rows)
    text = markdown.read_text(encoding="utf-8")
    assert "Status: consolidated blocker map." in text
    assert "Result-allowed lanes: 0." in text
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["tool"] == "scripts.build_no_input_blocker_summary"
    assert payload["summary"]["claim_boundary"] == summary.CLAIM_BOUNDARY


def _inputs() -> summary.LoadedInputs:
    return summary.LoadedInputs(
        wrr_status=[{"status_id": f"w{index}"} for index in range(9)],
        wrr_summary={
            "manual_input_needed_rows": "8",
            "new_result_allowed": "False",
            "remaining_gap": "91",
            "claim_boundary": "local_locked_method_ready_exact_published_open",
        },
        cities_status=[{"status_id": f"c{index}"} for index in range(8)],
        cities_summary={
            "manual_input_needed_rows": "6",
            "result_allowed": "False",
            "pending_transcription_rows": "14",
            "claim_status": "cities_no_input_handoff_blocks_source_import_and_results",
        },
        kjva_status=[{"status_id": f"k{index}"} for index in range(9)],
        kjva_summary={
            "manual_input_needed_rows": "8",
            "result_allowed": "False",
            "blocked_gate_rows": "10",
            "claim_status": "kjva_no_input_handoff_blocks_new_result",
        },
    )


def _write_inputs(tmp_path: Path) -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for name, rows in {
        "wrr_status": _inputs().wrr_status,
        "cities_status": _inputs().cities_status,
        "kjva_status": _inputs().kjva_status,
    }.items():
        path = tmp_path / f"{name}.csv"
        _write_csv(path, sorted(rows[0]), rows)
        paths[name] = path
    for name, row in {
        "wrr_summary": _inputs().wrr_summary,
        "cities_summary": _inputs().cities_summary,
        "kjva_summary": _inputs().kjva_summary,
    }.items():
        path = tmp_path / f"{name}.csv"
        _write_csv(path, sorted(row), [row])
        paths[name] = path
    return paths


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
