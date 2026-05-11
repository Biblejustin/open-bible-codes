#!/usr/bin/env python3
"""Summarize broad ELS count sweeps."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.term_display import display_term


COUNTS_DIR = Path("reports/broad_search")
BASELINE_DIR = Path("reports/protocols/public_baseline")
SUMMARY_OUT = Path("reports/broad_search/broad_search_summary.csv")
TOP_OUT = Path("reports/broad_search/broad_search_top_counts.csv")
FOCUS_OUT = Path("reports/broad_search/broad_search_focus.csv")
DELTA_OUT = Path("reports/broad_search/broad_search_delta_vs_baseline.csv")
MD_OUT = Path("reports/broad_search/broad_search.md")
DOCS_OUT = Path("docs/BROAD_SEARCH_FINDINGS.md")
MANIFEST_OUT = Path("reports/broad_search/broad_search_summary.manifest.json")

FOCUS_CONCEPTS = {
    "Trump",
    "Donald Trump",
    "Vance",
    "Netanyahu",
    "Iran",
    "Russia",
    "Europe",
    "Germany",
    "Turkey",
    "United States",
    "USA",
    "United Nations",
    "European Union",
    "Gog",
    "Magog",
    "Beast",
    "Dragon",
    "Cowboy",
    "Catering",
    "Cowboy Catering",
    "Simsberry",
    "Simscorner",
}

SUMMARY_FIELDNAMES = [
    "term_set",
    "corpus",
    "rows",
    "counted_rows",
    "zero_rows",
    "total_hits",
    "max_hit_count",
    "max_term_id",
    "max_concept",
    "max_normalized_term",
]

TOP_FIELDNAMES = [
    "rank",
    "term_set",
    "corpus",
    "term_id",
    "concept",
    "category",
    "normalized_term",
    "normalized_length",
    "hit_count",
    "read",
]

FOCUS_FIELDNAMES = [
    "term_set",
    "corpus",
    "term_id",
    "concept",
    "category",
    "term_language",
    "term",
    "normalized_term",
    "normalized_length",
    "hit_count",
    "read",
]

DELTA_FIELDNAMES = [
    "term_set",
    "corpus",
    "term_id",
    "concept",
    "category",
    "normalized_term",
    "normalized_length",
    "baseline_hits_2_50",
    "run_hits",
    "delta_hits",
    "ratio",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = read_count_rows(args.counts_dir)
    baseline_rows = read_count_rows(args.baseline_dir) if args.baseline_dir.exists() else []
    summary_rows = summarize(rows)
    top_rows = top_counts(rows, limit=args.top, min_length=args.min_top_length)
    focus_rows = focus_counts(rows)
    delta_rows = delta_vs_baseline(rows, baseline_rows, limit=args.delta_top)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(args.top_out, TOP_FIELDNAMES, top_rows)
    write_rows(args.focus_out, FOCUS_FIELDNAMES, focus_rows)
    write_rows(args.delta_out, DELTA_FIELDNAMES, delta_rows)
    write_markdown(args.markdown_out, summary_rows, top_rows, focus_rows, delta_rows, args)
    if args.docs_out is not None:
        write_markdown(args.docs_out, summary_rows, top_rows, focus_rows, delta_rows, args)
    write_manifest(args, len(rows), len(baseline_rows), started)
    print(args.summary_out)
    print(args.top_out)
    print(args.focus_out)
    print(args.delta_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--counts-dir", type=Path, default=COUNTS_DIR)
    parser.add_argument("--baseline-dir", type=Path, default=BASELINE_DIR)
    parser.add_argument("--top", type=int, default=80)
    parser.add_argument("--delta-top", type=int, default=80)
    parser.add_argument("--min-top-length", type=int, default=4)
    parser.add_argument("--title", default="Broad Search Summary")
    parser.add_argument("--scope-line", default="Broader ELS count sweep across every declared term list.")
    parser.add_argument(
        "--main-read",
        action="append",
        help="Main-read bullet. May be repeated. Defaults to broad-screening interpretation bullets.",
    )
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--top-out", type=Path, default=TOP_OUT)
    parser.add_argument("--focus-out", type=Path, default=FOCUS_OUT)
    parser.add_argument("--delta-out", type=Path, default=DELTA_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--docs-out", type=Path)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_count_rows(counts_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(counts_dir.glob("*_counts.csv")):
        if not is_term_set_counts_file(path):
            continue
        term_set = path.name.removesuffix("_counts.csv")
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                copied = dict(row)
                copied["term_set"] = term_set
                rows.append(copied)
    return rows


def is_term_set_counts_file(path: Path) -> bool:
    if path.name.startswith("broad_search_"):
        return False
    return (path.parent / f"{path.stem}.manifest.json").exists()


def summarize(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    output = []
    for (term_set, corpus), group in grouped(rows, "term_set", "corpus").items():
        counted = [row for row in group if row.get("status") == "counted"]
        max_row = max(counted, key=hit_count, default={})
        output.append(
            {
                "term_set": term_set,
                "corpus": corpus,
                "rows": len(group),
                "counted_rows": len(counted),
                "zero_rows": sum(1 for row in counted if hit_count(row) == 0),
                "total_hits": sum(hit_count(row) for row in counted),
                "max_hit_count": hit_count(max_row),
                "max_term_id": max_row.get("term_id", ""),
                "max_concept": max_row.get("concept", ""),
                "max_normalized_term": max_row.get("normalized_term", ""),
            }
        )
    return sorted(output, key=lambda row: (str(row["term_set"]), str(row["corpus"])))


def top_counts(
    rows: list[dict[str, str]],
    *,
    limit: int,
    min_length: int,
) -> list[dict[str, object]]:
    counted = [
        row
        for row in rows
        if row.get("status") == "counted" and int_or_zero(row.get("normalized_length")) >= min_length
    ]
    output = []
    for rank, row in enumerate(sorted(counted, key=hit_count, reverse=True)[:limit], start=1):
        output.append(top_row(rank, row))
    return output


def focus_counts(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    output = []
    for row in rows:
        if row.get("status") != "counted":
            continue
        if row.get("concept", "") not in FOCUS_CONCEPTS:
            continue
        output.append(focus_row(row))
    return sorted(
        output,
        key=lambda row: (str(row["concept"]), str(row["corpus"]), str(row["term_id"])),
    )


def delta_vs_baseline(
    broad_rows: list[dict[str, str]],
    baseline_rows: list[dict[str, str]],
    *,
    limit: int,
) -> list[dict[str, object]]:
    baseline = {row_key(row): row for row in baseline_rows if row.get("status") == "counted"}
    deltas = []
    for row in broad_rows:
        if row.get("status") != "counted":
            continue
        old = baseline.get(row_key(row))
        if old is None:
            continue
        old_hits = hit_count(old)
        new_hits = hit_count(row)
        deltas.append(
            {
                "term_set": row["term_set"],
                "corpus": row["corpus"],
                "term_id": row["term_id"],
                "concept": row["concept"],
                "category": row["category"],
                "normalized_term": row["normalized_term"],
                "normalized_length": int_or_zero(row.get("normalized_length")),
                "baseline_hits_2_50": old_hits,
                "run_hits": new_hits,
                "delta_hits": new_hits - old_hits,
                "ratio": ratio_cell(new_hits, old_hits),
            }
        )
    return sorted(deltas, key=lambda row: int(row["delta_hits"]), reverse=True)[:limit]


def top_row(rank: int, row: dict[str, str]) -> dict[str, object]:
    return {
        "rank": rank,
        "term_set": row["term_set"],
        "corpus": row["corpus"],
        "term_id": row["term_id"],
        "concept": row["concept"],
        "category": row["category"],
        "normalized_term": row["normalized_term"],
        "normalized_length": int_or_zero(row.get("normalized_length")),
        "hit_count": hit_count(row),
        "read": read_label(row),
    }


def focus_row(row: dict[str, str]) -> dict[str, object]:
    return {
        "term_set": row["term_set"],
        "corpus": row["corpus"],
        "term_id": row["term_id"],
        "concept": row["concept"],
        "category": row["category"],
        "term_language": row.get("term_language", ""),
        "term": row.get("term", ""),
        "normalized_term": row["normalized_term"],
        "normalized_length": int_or_zero(row.get("normalized_length")),
        "hit_count": hit_count(row),
        "read": read_label(row),
    }


def display_count_term(row: dict[str, object]) -> str:
    term_id = str(row.get("term_id") or row.get("max_term_id") or "")
    normalized = str(row.get("normalized_term") or row.get("max_normalized_term") or "")
    concept = str(row.get("concept") or row.get("max_concept") or "")
    displayed = display_term(normalized, english=concept)
    if term_id and displayed:
        return f"`{term_id}` {displayed}"
    if term_id:
        return f"`{term_id}`"
    return displayed


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, object]],
    top_rows: list[dict[str, object]],
    focus_rows: list[dict[str, object]],
    delta_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    manifest = read_manifest(args.counts_dir / "broad_search.manifest.json")
    max_skip = manifest.get("max_skip", 100)
    main_read = getattr(args, "main_read", None) or [
        f"Widening to skip {max_skip} mostly scales up already-dense short terms.",
        "Length 4+ leaders still come from short Greek or Hebrew forms and acronyms.",
        "Full modern phrases remain weak or absent; abbreviations dominate.",
        "Frequency anchors and null controls are useful calibration rows because they also produce high counts.",
    ]
    lines = [
        f"# {getattr(args, 'title', 'Broad Search Summary')}",
        "",
        getattr(args, "scope_line", "Broader ELS count sweep across every declared term list."),
        "",
        "## Scope",
        "",
        f"- Skip range: `{manifest.get('min_skip', 2)}..{manifest.get('max_skip', 100)}`",
        f"- Direction: `{manifest.get('direction', 'both')}`",
        f"- Term sets: {len(manifest.get('term_sets', []))}",
        f"- Rows: {len(read_count_rows(args.counts_dir))}",
        f"- Manifest: `{args.counts_dir / 'broad_search.manifest.json'}`",
        "",
        "## Main Read",
        "",
        *[f"- {item}" for item in main_read],
        "",
        "## Term Set Summary",
        "",
        "| Term set | Corpus | Counted | Zero | Total hits | Max row |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in summary_rows:
        max_cell = f"{display_count_term(row)} ({row['max_hit_count']})"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["term_set"]),
                    str(row["corpus"]),
                    str(row["counted_rows"]),
                    str(row["zero_rows"]),
                    str(row["total_hits"]),
                    max_cell,
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            f"## Top Length {args.min_top_length}+ Counts",
            "",
            "| Rank | Set | Corpus | Term | Length | Hits | Read |",
            "| ---: | --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in top_rows[:30]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["rank"]),
                    str(row["term_set"]),
                    str(row["corpus"]),
                    display_count_term(row),
                    str(row["normalized_length"]),
                    str(row["hit_count"]),
                    str(row["read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Focus Terms",
            "",
            "| Concept | Corpus | Term | Length | Hits | Read |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in sorted(focus_rows, key=lambda item: int(item["hit_count"]), reverse=True)[:60]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["concept"]),
                    str(row["corpus"]),
                    display_count_term(row),
                    str(row["normalized_length"]),
                    str(row["hit_count"]),
                    str(row["read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Largest Increases Vs Skip 2..50",
            "",
            f"| Set | Corpus | Term | 2..50 | 2..{max_skip} | Delta | Ratio |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in delta_rows[:30]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["term_set"]),
                    str(row["corpus"]),
                    display_count_term(row),
                    str(row["baseline_hits_2_50"]),
                    str(row["run_hits"]),
                    str(row["delta_hits"]),
                    str(row["ratio"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Caution",
            "",
            "This is a broad screening run. It is not a control-backed claim report. Treat high counts as queue-building only.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    rows: int,
    baseline_rows: int,
    started: float,
) -> None:
    outputs = [
        str(args.summary_out),
        str(args.top_out),
        str(args.focus_out),
        str(args.delta_out),
        str(args.markdown_out),
        str(args.manifest_out),
    ]
    if args.docs_out is not None:
        outputs.append(str(args.docs_out))
    payload = {
        "tool": "analyze_broad_search",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "counts_dir": str(args.counts_dir),
        "baseline_dir": str(args.baseline_dir),
        "rows": rows,
        "baseline_rows": baseline_rows,
        "outputs": outputs,
        "seconds": round(time.perf_counter() - started, 3),
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def grouped(
    rows: list[dict[str, str]],
    *fields: str,
) -> dict[tuple[str, ...], list[dict[str, str]]]:
    output: dict[tuple[str, ...], list[dict[str, str]]] = {}
    for row in rows:
        output.setdefault(tuple(row.get(field, "") for field in fields), []).append(row)
    return output


def row_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (row.get("term_set", ""), row.get("corpus", ""), row.get("term_id", ""))


def hit_count(row: dict[str, str]) -> int:
    return int_or_zero(row.get("hit_count"))


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


def ratio_cell(new_hits: int, old_hits: int) -> str:
    if old_hits == 0:
        return ""
    return str(round(new_hits / old_hits, 3))


def read_label(row: dict[str, str]) -> str:
    length = int_or_zero(row.get("normalized_length"))
    hits = hit_count(row)
    if hits == 0:
        return "absent at this range"
    if length <= 3:
        return "high-noise short form"
    if length == 4 and hits >= 1000:
        return "dense short form"
    if hits >= 10000:
        return "very high count; needs controls"
    if hits >= 1000:
        return "high count; needs controls"
    if hits <= 10:
        return "low count"
    return "present; screen only"


def read_manifest(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
