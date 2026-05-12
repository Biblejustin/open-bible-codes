import csv
from pathlib import Path

from scripts.build_matrix_cluster_candidates import (
    matrix_cluster_rows,
    matrix_hit_from_row,
    read_hits,
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
