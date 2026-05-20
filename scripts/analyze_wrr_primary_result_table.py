#!/usr/bin/env python3
"""Audit WRR 1994 primary-PDF Table 3 published rank results."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from pypdf import PdfReader

from els import __version__
from els.wrr import bonferroni_rho0


DEFAULT_SOURCE = Path("reports/wrr_1994/wrr_1994_paper.pdf")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_primary_result_table.csv")
DEFAULT_MD = Path("reports/wrr_1994/wrr_primary_result_table.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_primary_result_table.manifest.json")

RANK_DENOMINATOR = 1_000_000
STATISTICS = ("P1", "P2", "P3", "P4")

FIELDNAMES = [
    "label",
    "source_text",
    "status",
    "page",
    "p1_rank",
    "p2_rank",
    "p3_rank",
    "p4_rank",
    "min_rank",
    "min_statistic",
    "min_rank_proportion",
    "bonferroni_p0",
    "bonferroni_p0_capped",
]

TABLE3_ROW_RE = re.compile(
    r"^\s*(?P<label>[GRTIWUV])\s+"
    r"(?P<p1>[0-9,]+)\s+"
    r"(?P<p2>[0-9,]+)\s+"
    r"(?P<p3>[0-9,]+)\s+"
    r"(?P<p4>[0-9,]+)\s*$"
)


@dataclass(frozen=True)
class ResultSource:
    label: str
    source_text: str


EXPECTED_SOURCES = (
    ResultSource("G", "Genesis text"),
    ResultSource("R", "letter-permuted Genesis control"),
    ResultSource("T", "Hebrew War and Peace control"),
    ResultSource("I", "Isaiah control"),
    ResultSource("W", "word-permuted Genesis control"),
    ResultSource("U", "within-verse word-permuted Genesis control"),
    ResultSource("V", "verse-permuted Genesis control"),
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    pages = extract_pages(args.source)
    rows = build_result_rows(pages)
    write_csv(args.out, rows)
    write_markdown(args.markdown_out, rows, args)
    write_manifest(args, rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def extract_pages(path: Path) -> list[str]:
    reader = PdfReader(str(path))
    return [page.extract_text() or "" for page in reader.pages]


def build_result_rows(pages: list[str]) -> list[dict[str, str]]:
    parsed = parse_table3_rows(pages)
    rows = []
    for source in EXPECTED_SOURCES:
        parsed_row = parsed.get(source.label)
        if parsed_row is None:
            rows.append(missing_row(source))
        else:
            rows.append(result_row(source, parsed_row))
    return rows


def parse_table3_rows(pages: list[str]) -> dict[str, dict[str, object]]:
    rows: dict[str, dict[str, object]] = {}
    for page_index, page_text in enumerate(pages, start=1):
        if "TABLE 3" not in page_text or "Rank order of Pi" not in page_text:
            continue
        for line in page_text.splitlines():
            match = TABLE3_ROW_RE.match(line)
            if not match:
                continue
            ranks = tuple(
                parse_rank(match.group(group))
                for group in ("p1", "p2", "p3", "p4")
            )
            rows[match.group("label")] = {
                "page": page_index,
                "ranks": ranks,
            }
    return rows


def result_row(source: ResultSource, parsed_row: dict[str, object]) -> dict[str, str]:
    ranks = tuple(parsed_row["ranks"])
    rank_summary = summarize_ranks(ranks)
    return {
        "label": source.label,
        "source_text": source.source_text,
        "status": "found",
        "page": str(parsed_row["page"]),
        "p1_rank": str(ranks[0]),
        "p2_rank": str(ranks[1]),
        "p3_rank": str(ranks[2]),
        "p4_rank": str(ranks[3]),
        **rank_summary,
    }


def missing_row(source: ResultSource) -> dict[str, str]:
    return {
        "label": source.label,
        "source_text": source.source_text,
        "status": "missing",
        "page": "",
        "p1_rank": "",
        "p2_rank": "",
        "p3_rank": "",
        "p4_rank": "",
        "min_rank": "",
        "min_statistic": "",
        "min_rank_proportion": "",
        "bonferroni_p0": "",
        "bonferroni_p0_capped": "",
    }


def parse_rank(value: str) -> int:
    return int(value.replace(",", ""))


def summarize_ranks(ranks: tuple[int, ...]) -> dict[str, str]:
    if len(ranks) != len(STATISTICS):
        raise ValueError("rank tuple must contain P1..P4")
    min_index, min_rank = min(enumerate(ranks), key=lambda item: item[1])
    rank_proportions = [rank / RANK_DENOMINATOR for rank in ranks]
    p0 = bonferroni_rho0(rank_proportions, statistic_count=len(STATISTICS))
    return {
        "min_rank": str(min_rank),
        "min_statistic": STATISTICS[min_index],
        "min_rank_proportion": format_float(min_rank / RANK_DENOMINATOR),
        "bonferroni_p0": format_float(p0),
        "bonferroni_p0_capped": format_float(min(1.0, p0)),
    }


def format_float(value: float) -> str:
    return f"{value:.6f}"


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    lines = [
        "# WRR Primary Result Table",
        "",
        "Status: source-result audit from the local WRR 1994 PDF; not a recomputation.",
        "",
        "This extracts the published Table 3 rank orders and derives the paper's",
        "Bonferroni-style `p0 = 4 * min(pi)` value from the source ranks.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.analyze_wrr_primary_result_table "
            f"--source {args.source} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Table 3 Rows",
        "",
        "| Label | Source text | Status | Page | P1 | P2 | P3 | P4 | Min | p0 | capped p0 |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{markdown_cell(row['label'])}`",
                    markdown_cell(row["source_text"]),
                    f"`{markdown_cell(row['status'])}`",
                    markdown_cell(row["page"]),
                    markdown_cell(row["p1_rank"]),
                    markdown_cell(row["p2_rank"]),
                    markdown_cell(row["p3_rank"]),
                    markdown_cell(row["p4_rank"]),
                    markdown_cell(
                        f"{row['min_statistic']}={row['min_rank']}"
                        if row["min_rank"]
                        else ""
                    ),
                    markdown_cell(row["bonferroni_p0"]),
                    markdown_cell(row["bonferroni_p0_capped"]),
                ]
            )
            + " |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def write_manifest(args: argparse.Namespace, rows: list[dict[str, str]], started: float) -> None:
    found_rows = [row for row in rows if row["status"] == "found"]
    genesis = next((row for row in rows if row["label"] == "G"), {})
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "source": str(args.source),
        "source_sha256": sha256_file(args.source),
        "rows": len(rows),
        "found": len(found_rows),
        "missing": len(rows) - len(found_rows),
        "rank_denominator": RANK_DENOMINATOR,
        "genesis_bonferroni_p0": genesis.get("bonferroni_p0", ""),
        "outputs": {
            "csv": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
