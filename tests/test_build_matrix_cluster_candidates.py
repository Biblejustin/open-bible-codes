import csv
from pathlib import Path

from scripts.build_matrix_cluster_candidates import (
    main,
    matrix_cluster_rows,
    matrix_hit_from_row,
    read_hits,
    read_hits_with_stats,
    summarize_rows,
)


def hit_row(
    *,
    term_id: str,
    start_offset: int,
    skip: int,
    sequence: str = "abc",
    corpus_label: str = "TINY",
) -> dict[str, str]:
    return {
        "corpus_label": corpus_label,
        "corpus_class": "bible",
        "term_id": term_id,
        "concept": term_id.upper(),
        "normalized_term": sequence,
        "skip": str(skip),
        "direction": "forward" if skip > 0 else "backward",
        "start_offset": str(start_offset),
        "sequence": sequence,
        "center_ref": "Test 1:1",
        "center_word": term_id,
    }


def test_matrix_hit_from_row_maps_offsets_to_cells() -> None:
    hit = matrix_hit_from_row(hit_row(term_id="left", start_offset=0, skip=3), hit_index=1, row_width=3)

    assert hit is not None
    assert hit.cells == ((0, 0), (1, 0), (2, 0))


def test_matrix_hit_from_row_accepts_extension_offset_columns() -> None:
    row = hit_row(term_id="left", start_offset=0, skip=3)
    row.pop("start_offset")
    row.pop("sequence")
    row["extension_start_offset"] = "1"
    row["extended_sequence"] = "abcd"

    hit = matrix_hit_from_row(row, hit_index=1, row_width=3)

    assert hit is not None
    assert hit.cells == ((0, 1), (1, 1), (2, 1), (3, 1))


def test_matrix_cluster_rows_finds_neighboring_terms() -> None:
    left = matrix_hit_from_row(hit_row(term_id="left", start_offset=0, skip=3), hit_index=1, row_width=3)
    right = matrix_hit_from_row(hit_row(term_id="right", start_offset=1, skip=3), hit_index=2, row_width=3)
    far = matrix_hit_from_row(hit_row(term_id="far", start_offset=30, skip=3), hit_index=3, row_width=3)

    rows = matrix_cluster_rows(
        [hit for hit in (left, right, far) if hit is not None],
        row_width=3,
        max_cell_distance=1,
    )

    assert len(rows) == 1
    assert rows[0]["left_term_id"] == "left"
    assert rows[0]["right_term_id"] == "right"
    assert rows[0]["cell_distance"] == 1
    assert rows[0]["cell_relation"] == "orthogonal"
    assert rows[0]["left_cell"] == "0:0"
    assert rows[0]["right_cell"] == "0:1"


def test_matrix_cluster_rows_skips_same_term_by_default() -> None:
    left = matrix_hit_from_row(hit_row(term_id="same", start_offset=0, skip=3), hit_index=1, row_width=3)
    right = matrix_hit_from_row(hit_row(term_id="same", start_offset=1, skip=3), hit_index=2, row_width=3)

    rows = matrix_cluster_rows(
        [hit for hit in (left, right) if hit is not None],
        row_width=3,
        max_cell_distance=1,
    )

    assert rows == []


def test_read_hits_and_main_shape(tmp_path: Path) -> None:
    hits = tmp_path / "hits.csv"
    out = tmp_path / "clusters.csv"
    with hits.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(hit_row(term_id="x", start_offset=0, skip=3)))
        writer.writeheader()
        writer.writerow(hit_row(term_id="left", start_offset=0, skip=3))
        writer.writerow(hit_row(term_id="right", start_offset=1, skip=3))

    parsed = read_hits([hits], row_width=3)
    rows = matrix_cluster_rows(parsed, row_width=3, max_cell_distance=1)

    assert len(rows) == 1
    assert rows[0]["corpus_label"] == "TINY"
    assert rows[0]["corpus_class"] == "bible"


def test_read_hits_with_stats_counts_unusable_rows(tmp_path: Path) -> None:
    hits = tmp_path / "hits.csv"
    usable = hit_row(term_id="left", start_offset=0, skip=3)
    unusable = dict(usable)
    unusable["sequence"] = ""
    unusable["normalized_term"] = ""
    with hits.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(usable))
        writer.writeheader()
        writer.writerow(usable)
        writer.writerow(unusable)

    parsed = read_hits_with_stats([hits], row_width=3)

    assert len(parsed.hits) == 1
    assert parsed.input_rows == 2
    assert parsed.skipped_rows == 1


def test_summarize_rows_counts_relations_corpora_and_distances() -> None:
    left = matrix_hit_from_row(hit_row(term_id="left", start_offset=0, skip=3), hit_index=1, row_width=3)
    right = matrix_hit_from_row(hit_row(term_id="right", start_offset=1, skip=3), hit_index=2, row_width=3)
    rows = matrix_cluster_rows(
        [hit for hit in (left, right) if hit is not None],
        row_width=3,
        max_cell_distance=1,
    )

    summary = summarize_rows(rows)

    assert {"bucket": "cell_relation", "value": "orthogonal", "pairs": 1} in summary
    assert {"bucket": "corpus_label", "value": "TINY", "pairs": 1} in summary
    assert {"bucket": "corpus_class", "value": "bible", "pairs": 1} in summary
    assert {"bucket": "cell_distance", "value": "1", "pairs": 1} in summary


def test_main_writes_candidates_summary_and_manifest(tmp_path: Path) -> None:
    hits = tmp_path / "hits.csv"
    out = tmp_path / "clusters.csv"
    summary = tmp_path / "summary.csv"
    markdown = tmp_path / "matrix.md"
    manifest = tmp_path / "manifest.json"
    with hits.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(hit_row(term_id="x", start_offset=0, skip=3)))
        writer.writeheader()
        writer.writerow(hit_row(term_id="left", start_offset=0, skip=3))
        writer.writerow(hit_row(term_id="right", start_offset=1, skip=3))

    assert (
        main(
            [
                "--hits",
                str(hits),
                "--row-width",
                "3",
                "--max-cell-distance",
                "1",
                "--out",
                str(out),
                "--summary-out",
                str(summary),
                "--markdown-out",
                str(markdown),
                "--manifest-out",
                str(manifest),
            ]
        )
        == 0
    )

    assert "orthogonal" in out.read_text(encoding="utf-8")
    assert "cell_relation" in summary.read_text(encoding="utf-8")
    assert "Matrix Cluster Candidates" in markdown.read_text(encoding="utf-8")
    assert '"candidate_pairs": 1' in manifest.read_text(encoding="utf-8")
    assert '"markdown_out":' in manifest.read_text(encoding="utf-8")
    assert '"skipped_input_rows": 0' in manifest.read_text(encoding="utf-8")


def test_main_can_require_parsed_hits(tmp_path: Path) -> None:
    hits = tmp_path / "hits.csv"
    out = tmp_path / "clusters.csv"
    summary = tmp_path / "summary.csv"
    manifest = tmp_path / "manifest.json"
    row = hit_row(term_id="left", start_offset=0, skip=3)
    row["sequence"] = ""
    row["normalized_term"] = ""
    with hits.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)

    try:
        main(
            [
                "--hits",
                str(hits),
                "--row-width",
                "3",
                "--require-parsed-hits",
                "--out",
                str(out),
                "--summary-out",
                str(summary),
                "--manifest-out",
                str(manifest),
            ]
        )
    except SystemExit as exc:
        assert "no matrix-usable hit rows parsed" in str(exc)
    else:
        raise AssertionError("expected SystemExit")
