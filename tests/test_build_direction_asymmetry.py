import csv
import json
from pathlib import Path

from scripts.build_direction_asymmetry import build_term_direction_groups, main, summarize_direction_asymmetry


def row(
    *,
    term_id: str = "term",
    corpus: str = "MT",
    bucket: str = "forward_only",
    forward: str = "2",
    backward: str = "0",
    normalized_term: str = "abc",
) -> dict[str, str]:
    return {
        "source_family": "demo",
        "corpus_class": "bible",
        "corpus": corpus,
        "term_id": term_id,
        "normalized_term": normalized_term,
        "direction_stratum": bucket,
        "forward_direction_count": forward,
        "backward_direction_count": backward,
        "direction_imbalance_score": "1.000000",
    }


def test_summarize_direction_asymmetry_counts_term_groups_once() -> None:
    groups = build_term_direction_groups(
        [
            row(term_id="a", bucket="forward_only", forward="2", backward="0"),
            row(term_id="a", bucket="forward_only", forward="2", backward="0"),
            row(term_id="b", bucket="backward_only", forward="0", backward="3"),
            row(term_id="c", bucket="bidirectional_present", forward="1", backward="1"),
        ]
    )
    summary = summarize_direction_asymmetry(groups)
    keyed = {(item["bucket"], item["corpus"]): item for item in summary}

    assert keyed[("forward_only", "MT")]["term_groups"] == 1
    assert keyed[("forward_only", "MT")]["hit_rows"] == 2
    assert keyed[("forward_only", "MT")]["forward_hits"] == 2
    assert keyed[("backward_only", "MT")]["backward_hits"] == 3
    assert keyed[("bidirectional_present", "MT")]["share_of_term_groups"] == "0.333333"


def test_main_writes_outputs(tmp_path: Path) -> None:
    strata = tmp_path / "strata.csv"
    out = tmp_path / "summary.csv"
    term_out = tmp_path / "term_summary.csv"
    markdown = tmp_path / "report.md"
    manifest = tmp_path / "manifest.json"
    rows = [row(term_id="a", bucket="forward_only"), row(term_id="b", bucket="backward_only", backward="1")]
    with strata.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    assert (
        main(
            [
                "--strata",
                str(strata),
                "--out",
                str(out),
                "--term-out",
                str(term_out),
                "--markdown-out",
                str(markdown),
                "--manifest-out",
                str(manifest),
            ]
        )
        == 0
    )
    assert "forward_only" in out.read_text(encoding="utf-8")
    assert "backward_only" in term_out.read_text(encoding="utf-8")
    assert "Direction Asymmetry" in markdown.read_text(encoding="utf-8")
    assert json.loads(manifest.read_text(encoding="utf-8"))["term_groups"] == 2
