import csv
import json
from pathlib import Path

from scripts import check_final_report_highlights_doc as check
from scripts import build_final_report_highlights as builder


def test_current_highlights_doc_passes() -> None:
    assert check.validate_highlights_doc() == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    args = check.build_parser().parse_args(["--markdown-out", str(tmp_path / "missing.md")])

    failures = check.validate_highlights_doc(args)

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_stale_doc_fails(tmp_path: Path) -> None:
    args = make_args(tmp_path)
    markdown = args.markdown_out
    markdown.write_text("stale", encoding="utf-8")

    failures = check.validate_highlights_doc(args)

    assert failures == [
        f"{markdown} is stale; rerun python3 -m scripts.build_final_report_highlights"
    ]


def test_matching_generated_outputs_pass(tmp_path: Path) -> None:
    assert check.validate_highlights_doc(make_args(tmp_path)) == []


def test_stale_highlights_csv_fails(tmp_path: Path) -> None:
    args = make_args(tmp_path)
    args.out.write_text("rank\n999\n", encoding="utf-8")

    failures = check.validate_highlights_doc(args)

    assert any("highlight rows drifted" in failure for failure in failures)


def test_stale_manifest_fails(tmp_path: Path) -> None:
    args = make_args(tmp_path)
    payload = json.loads(args.manifest_out.read_text(encoding="utf-8"))
    payload["highlight_rows"] = 99
    args.manifest_out.write_text(json.dumps(payload) + "\n", encoding="utf-8")

    failures = check.validate_highlights_doc(args)

    assert any("highlight_rows drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    code = check.main(["--markdown-out", str(tmp_path / "missing.md")])

    assert code == 1
    assert "final-report highlights doc failure" in capsys.readouterr().err


def make_args(tmp_path: Path):
    centered = tmp_path / "presence.csv"
    claims = tmp_path / "claims.csv"
    markdown = tmp_path / "highlights.md"
    out = tmp_path / "highlights.csv"
    manifest = tmp_path / "manifest.json"
    write_centered(centered)
    write_claims(claims)
    args = check.build_parser().parse_args(
        [
            "--centered-summary",
            str(centered),
            "--claim-catalog",
            str(claims),
            "--out",
            str(out),
            "--markdown-out",
            str(markdown),
            "--manifest-out",
            str(manifest),
        ]
    )
    highlights = builder.build_highlights(builder.read_rows(centered), limit=args.limit)
    claim_rows = builder.read_rows(claims)
    builder.write_csv(out, highlights)
    builder.write_markdown(markdown, highlights, claim_rows, args)
    builder.write_manifest(manifest, args, highlights, claim_rows, 0.0)
    return args


def write_centered(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "summary_rank",
                "occurrence_type",
                "source_family",
                "corpus_class",
                "normalized_term",
                "center_ref",
                "center_word",
                "corpora",
                "total_paths",
                "frequency_reads",
                "control_reads",
                "context_excerpt",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "summary_rank": "1",
                "occurrence_type": "centered_self_exact_word",
                "source_family": "gog_source_review",
                "corpus_class": "bible",
                "normalized_term": "γωγ",
                "center_ref": "REV 20:8",
                "center_word": "Gog",
                "corpora": "TR_NT",
                "total_paths": "4",
                "frequency_reads": "not frequency-promoted",
                "control_reads": "control read",
                "context_excerpt": "context",
            }
        )


def write_claims(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["claim_id", "status", "current_reproduction", "evidence"],
        )
        writer.writeheader()
        writer.writerow(
            {
                "claim_id": "gog",
                "status": "controlled_review_candidate",
                "current_reproduction": "review",
                "evidence": "docs/CENTERED_OCCURRENCE_INDEX.md",
            }
        )
