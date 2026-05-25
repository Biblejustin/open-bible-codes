from pathlib import Path

from scripts import check_strongest_candidate_deep_dive_doc as check


def test_current_strongest_candidate_deep_dive_doc_passes() -> None:
    assert check.validate_strongest_candidate_deep_dive_doc() == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    markdown = tmp_path / "missing.md"
    args = check.build_parser().parse_args(["--markdown-out", str(markdown)])

    failures = check.validate_strongest_candidate_deep_dive_doc(args)

    assert failures == [f"{markdown} is missing"]


def test_stale_doc_fails(tmp_path: Path) -> None:
    markdown = tmp_path / "deep_dive.md"
    markdown.write_text("stale", encoding="utf-8")
    args = check.build_parser().parse_args(["--markdown-out", str(markdown)])

    failures = check.validate_strongest_candidate_deep_dive_doc(args)

    assert failures == [
        f"{markdown} is stale; rerun python3 -m scripts.build_strongest_candidate_deep_dive"
    ]


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    code = check.main(["--markdown-out", str(tmp_path / "missing.md")])

    assert code == 1
    assert "strongest-candidate deep-dive doc failure" in capsys.readouterr().err
