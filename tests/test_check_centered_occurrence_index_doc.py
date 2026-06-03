import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import json
from pathlib import Path

from scripts import check_centered_occurrence_index_doc as check
from scripts import build_centered_occurrence_index as builder


def test_current_centered_occurrence_index_doc_passes() -> None:
    assert check.validate_centered_occurrence_index_doc() == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    args = make_args(tmp_path, markdown_exists=False)

    failures = check.validate_centered_occurrence_index_doc(args)

    assert failures == [f"{args.markdown_out} is missing"]


def test_stale_doc_fails(tmp_path: Path) -> None:
    args = make_args(tmp_path)
    args.markdown_out.write_text("stale", encoding="utf-8")

    failures = check.validate_centered_occurrence_index_doc(args)

    assert failures == [
        f"{args.markdown_out} is stale; rerun python3 -m scripts.build_centered_occurrence_index"
    ]


def test_stale_occurrences_csv_fails(tmp_path: Path) -> None:
    args = make_args(tmp_path)
    args.out.write_text("occurrence_rank\n999\n", encoding="utf-8")

    failures = check.validate_centered_occurrence_index_doc(args)

    assert any("centered occurrences rows drifted" in failure for failure in failures)


def test_stale_manifest_fails(tmp_path: Path) -> None:
    args = make_args(tmp_path)
    payload = json.loads(args.manifest_out.read_text(encoding="utf-8"))
    payload["rows"] = 999
    args.manifest_out.write_text(json.dumps(payload) + "\n", encoding="utf-8")

    failures = check.validate_centered_occurrence_index_doc(args)

    assert any("manifest.json rows drifted" in failure for failure in failures)


def test_invalid_manifest_json_fails(tmp_path: Path) -> None:
    args = make_args(tmp_path)
    args.manifest_out.write_text("{", encoding="utf-8")

    failures = check.validate_centered_occurrence_index_doc(args)

    assert len(failures) == 1
    assert failures[0].startswith(f"{args.manifest_out} is invalid JSON:")


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    args = make_args(tmp_path, markdown_exists=False)

    code = check.main(check_args_for(args))

    assert code == 1
    assert "centered-occurrence index doc failure" in capsys.readouterr().err


def make_args(tmp_path: Path, *, markdown_exists: bool = True):
    paths = {
        "all_codes_review": tmp_path / "all_codes_review.csv",
        "all_codes_selected": tmp_path / "all_codes_selected.csv",
        "all_codes_context": tmp_path / "all_codes_context.csv",
        "strong_queue": tmp_path / "strong_queue.csv",
        "strong_bundle": tmp_path / "strong_bundle.csv",
        "original_findings": tmp_path / "original_findings.csv",
        "gog_source_review": tmp_path / "gog_source_review.csv",
        "gog_control_review": tmp_path / "gog_control_review.csv",
        "apocrypha_bridge_context": tmp_path / "apocrypha_bridge_context.csv",
        "kjv_apocrypha_bridge_context": tmp_path / "kjv_apocrypha_bridge_context.csv",
    }
    for path in paths.values():
        path.write_text("", encoding="utf-8")
    markdown = tmp_path / "CENTERED_OCCURRENCE_INDEX.md"
    args = check.build_parser().parse_args(
        [
            "--all-codes-review",
            str(paths["all_codes_review"]),
            "--all-codes-selected",
            str(paths["all_codes_selected"]),
            "--all-codes-context",
            str(paths["all_codes_context"]),
            "--strong-queue",
            str(paths["strong_queue"]),
            "--strong-bundle",
            str(paths["strong_bundle"]),
            "--original-findings",
            str(paths["original_findings"]),
            "--gog-source-review",
            str(paths["gog_source_review"]),
            "--gog-control-review",
            str(paths["gog_control_review"]),
            "--apocrypha-bridge-context",
            str(paths["apocrypha_bridge_context"]),
            "--kjv-apocrypha-bridge-context",
            str(paths["kjv_apocrypha_bridge_context"]),
            "--out",
            str(tmp_path / "centered_occurrences.csv"),
            "--summary-out",
            str(tmp_path / "presence_summary.csv"),
            "--markdown-out",
            str(markdown),
            "--manifest-out",
            str(tmp_path / "manifest.json"),
        ]
    )
    rows = builder.build_occurrences(args)
    summary_rows = builder.build_presence_summary(rows)
    builder.write_csv(args.out, rows)
    builder.write_csv(args.summary_out, summary_rows, fieldnames=builder.SUMMARY_FIELDNAMES)
    builder.write_manifest(args.manifest_out, args, rows, summary_rows, 0.0)
    if markdown_exists:
        markdown.write_text(builder.render_markdown(rows, summary_rows, args), encoding="utf-8")
    return args


def check_args_for(args) -> list[str]:
    return [
        "--all-codes-review",
        str(args.all_codes_review),
        "--all-codes-selected",
        str(args.all_codes_selected),
        "--all-codes-context",
        str(args.all_codes_context),
        "--strong-queue",
        str(args.strong_queue),
        "--strong-bundle",
        str(args.strong_bundle),
        "--original-findings",
        str(args.original_findings),
        "--gog-source-review",
        str(args.gog_source_review),
        "--gog-control-review",
        str(args.gog_control_review),
        "--apocrypha-bridge-context",
        str(args.apocrypha_bridge_context),
        "--kjv-apocrypha-bridge-context",
        str(args.kjv_apocrypha_bridge_context),
        "--out",
        str(args.out),
        "--summary-out",
        str(args.summary_out),
        "--markdown-out",
        str(args.markdown_out),
        "--manifest-out",
        str(args.manifest_out),
    ]
