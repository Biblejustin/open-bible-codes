import json
from pathlib import Path

from scripts import check_strongest_candidate_deep_dive_doc as check
from scripts import build_strongest_candidate_deep_dive as builder


def test_current_strongest_candidate_deep_dive_doc_passes() -> None:
    assert check.validate_strongest_candidate_deep_dive_doc() == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    markdown = tmp_path / "missing.md"
    args = check.build_parser().parse_args(["--markdown-out", str(markdown)])

    failures = check.validate_strongest_candidate_deep_dive_doc(args)

    assert failures == [f"{markdown} is missing"]


def test_stale_doc_fails(tmp_path: Path) -> None:
    args = make_args(tmp_path)
    markdown = args.markdown_out
    markdown.write_text("stale", encoding="utf-8")

    failures = check.validate_strongest_candidate_deep_dive_doc(args)

    assert failures == [
        f"{markdown} is stale; rerun python3 -m scripts.build_strongest_candidate_deep_dive"
    ]


def test_matching_generated_outputs_pass(tmp_path: Path) -> None:
    assert check.validate_strongest_candidate_deep_dive_doc(make_args(tmp_path)) == []


def test_stale_candidates_csv_fails(tmp_path: Path) -> None:
    args = make_args(tmp_path)
    args.out.write_text("rank\n999\n", encoding="utf-8")

    failures = check.validate_strongest_candidate_deep_dive_doc(args)

    assert any("candidate rows drifted" in failure for failure in failures)


def test_stale_manifest_fails(tmp_path: Path) -> None:
    args = make_args(tmp_path)
    payload = json.loads(args.manifest_out.read_text(encoding="utf-8"))
    payload["candidate_rows"] = 99
    args.manifest_out.write_text(json.dumps(payload) + "\n", encoding="utf-8")

    failures = check.validate_strongest_candidate_deep_dive_doc(args)

    assert any("candidate_rows drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    code = check.main(["--markdown-out", str(tmp_path / "missing.md")])

    assert code == 1
    assert "strongest-candidate deep-dive doc failure" in capsys.readouterr().err


def make_args(tmp_path: Path):
    markdown = tmp_path / "deep_dive.md"
    out = tmp_path / "candidates.csv"
    manifest = tmp_path / "manifest.json"
    args = check.build_parser().parse_args(
        [
            "--out",
            str(out),
            "--markdown-out",
            str(markdown),
            "--manifest-out",
            str(manifest),
        ]
    )
    candidates = builder.build_candidates(args)
    builder.write_csv(out, candidates)
    builder.write_markdown(markdown, candidates, args)
    builder.write_manifest(manifest, candidates, args, 0.0)
    return args
