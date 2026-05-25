import csv
import json
from pathlib import Path

from scripts import filter_prospective_terms as filt


def test_filter_removes_block_and_review_rows_by_default(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate.csv"
    audit = tmp_path / "audit.csv"
    out = tmp_path / "filtered.csv"
    write_csv(
        candidate,
        ["term_id", "concept", "category", "language", "term"],
        [
            ["keep", "Keep", "screen", "greek", "αληθεια"],
            ["drop_block", "Block", "screen", "greek", "δοξα"],
            ["drop_review", "Review", "screen", "greek", "δοξανωσ"],
        ],
    )
    write_csv(
        audit,
        ["severity", "candidate_file", "candidate_term_id"],
        [
            ["block", str(candidate), "drop_block"],
            ["review", str(candidate), "drop_review"],
        ],
    )

    code = filt.main(
        [
            "--candidate",
            str(candidate),
            "--audit",
            str(audit),
            "--out",
            str(out),
        ]
    )

    assert code == 0
    rows = read_rows(out)
    assert [row["term_id"] for row in rows] == ["keep"]
    summary = json.loads((tmp_path / "filtered.csv.summary.json").read_text(encoding="utf-8"))
    assert summary["dropped_term_ids"] == ["drop_block", "drop_review"]


def test_filter_can_drop_only_block_rows(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate.csv"
    audit = tmp_path / "audit.csv"
    out = tmp_path / "filtered.csv"
    write_csv(
        candidate,
        ["term_id", "concept", "category", "language", "term"],
        [
            ["drop_block", "Block", "screen", "greek", "δοξα"],
            ["keep_review", "Review", "screen", "greek", "δοξανωσ"],
        ],
    )
    write_csv(
        audit,
        ["severity", "candidate_file", "candidate_term_id"],
        [
            ["block", str(candidate), "drop_block"],
            ["review", str(candidate), "keep_review"],
        ],
    )

    code = filt.main(
        [
            "--candidate",
            str(candidate),
            "--audit",
            str(audit),
            "--drop-severity",
            "block",
            "--out",
            str(out),
        ]
    )

    assert code == 0
    assert [row["term_id"] for row in read_rows(out)] == ["keep_review"]


def test_filter_can_drop_rows_below_min_normalized_length(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate.csv"
    audit = tmp_path / "audit.csv"
    out = tmp_path / "filtered.csv"
    write_csv(
        candidate,
        ["term_id", "concept", "category", "language", "term"],
        [
            ["short", "Short", "screen", "greek", "σιων"],
            ["long", "Long", "screen", "greek", "αληθεια"],
        ],
    )
    write_csv(audit, ["severity", "candidate_file", "candidate_term_id"], [])

    code = filt.main(
        [
            "--candidate",
            str(candidate),
            "--audit",
            str(audit),
            "--out",
            str(out),
            "--min-normalized-length",
            "5",
        ]
    )

    assert code == 0
    assert [row["term_id"] for row in read_rows(out)] == ["long"]
    payload = json.loads((tmp_path / "filtered.csv.summary.json").read_text(encoding="utf-8"))
    assert payload["short_dropped_term_ids"] == ["short"]


def test_filter_can_drop_language_stopwords(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate.csv"
    audit = tmp_path / "audit.csv"
    out = tmp_path / "filtered.csv"
    write_csv(
        candidate,
        ["term_id", "concept", "category", "language", "term"],
        [
            ["drop_stopword", "Common Pronoun", "screen", "greek", "αὐτοῦ"],
            ["keep_content", "Truth", "screen", "greek", "ἀλήθεια"],
        ],
    )
    write_csv(audit, ["severity", "candidate_file", "candidate_term_id"], [])

    code = filt.main(
        [
            "--candidate",
            str(candidate),
            "--audit",
            str(audit),
            "--out",
            str(out),
            "--drop-language-stopwords",
            "greek",
        ]
    )

    assert code == 0
    assert [row["term_id"] for row in read_rows(out)] == ["keep_content"]
    payload = json.loads((tmp_path / "filtered.csv.summary.json").read_text(encoding="utf-8"))
    assert payload["stopword_dropped_term_ids"] == ["drop_stopword"]
    assert payload["drop_language_stopwords"] == ["greek"]


def test_filter_ignores_audit_rows_for_other_candidate_file(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate.csv"
    other = tmp_path / "other.csv"
    audit = tmp_path / "audit.csv"
    out = tmp_path / "filtered.csv"
    write_csv(
        candidate,
        ["term_id", "concept", "category", "language", "term"],
        [["keep", "Keep", "screen", "greek", "δοξα"]],
    )
    write_csv(
        audit,
        ["severity", "candidate_file", "candidate_term_id"],
        [["block", str(other), "keep"]],
    )

    code = filt.main(
        [
            "--candidate",
            str(candidate),
            "--audit",
            str(audit),
            "--out",
            str(out),
        ]
    )

    assert code == 0
    assert [row["term_id"] for row in read_rows(out)] == ["keep"]


def test_filter_fails_when_min_remaining_not_met(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate.csv"
    audit = tmp_path / "audit.csv"
    out = tmp_path / "filtered.csv"
    write_csv(
        candidate,
        ["term_id", "concept", "category", "language", "term"],
        [["drop", "Drop", "screen", "greek", "δοξα"]],
    )
    write_csv(
        audit,
        ["severity", "candidate_file", "candidate_term_id"],
        [["block", str(candidate), "drop"]],
    )

    code = filt.main(
        [
            "--candidate",
            str(candidate),
            "--audit",
            str(audit),
            "--out",
            str(out),
            "--min-remaining",
            "1",
        ]
    )

    assert code == 1
    payload = json.loads((tmp_path / "filtered.csv.summary.json").read_text(encoding="utf-8"))
    assert payload["status"] == "failed"
    assert payload["output_rows"] == 0


def write_csv(path: Path, fieldnames: list[str], rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(fieldnames)
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))
