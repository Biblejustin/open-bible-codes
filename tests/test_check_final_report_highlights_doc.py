import csv
from pathlib import Path

from scripts import check_final_report_highlights_doc as check


def test_current_highlights_doc_passes() -> None:
    assert check.validate_highlights_doc() == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    args = check.build_parser().parse_args(["--markdown-out", str(tmp_path / "missing.md")])

    failures = check.validate_highlights_doc(args)

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_stale_doc_fails(tmp_path: Path) -> None:
    centered = tmp_path / "presence.csv"
    claims = tmp_path / "claims.csv"
    markdown = tmp_path / "highlights.md"
    write_centered(centered)
    write_claims(claims)
    markdown.write_text("stale", encoding="utf-8")
    args = check.build_parser().parse_args(
        [
            "--centered-summary",
            str(centered),
            "--claim-catalog",
            str(claims),
            "--markdown-out",
            str(markdown),
        ]
    )

    failures = check.validate_highlights_doc(args)

    assert failures == [
        f"{markdown} is stale; rerun python3 -m scripts.build_final_report_highlights"
    ]


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    code = check.main(["--markdown-out", str(tmp_path / "missing.md")])

    assert code == 1
    assert "final-report highlights doc failure" in capsys.readouterr().err


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
