#!/usr/bin/env python3
"""Audit English row anchors for WRR 1994 primary-PDF Table 2."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from pypdf import PdfReader

from els import __version__


DEFAULT_SOURCE = Path("reports/wrr_1994/wrr_1994_paper.pdf")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_primary_table2_anchors.csv")
DEFAULT_MD = Path("reports/wrr_1994/wrr_primary_table2_anchors.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_primary_table2_anchors.manifest.json")

FIELDNAMES = [
    "anchor_id",
    "row_number",
    "english_name",
    "status",
    "page",
    "search_fragments",
    "current_read",
]

TABLE2_READ = (
    "Primary Table 2 English row-label anchor found; Hebrew name/date cells "
    "remain extraction-garbled and require a verified transcription before "
    "term-level reproduction claims."
)


@dataclass(frozen=True)
class Table2Personality:
    row_number: int
    english_name: str
    search_fragments: tuple[str, ...]

    @property
    def anchor_id(self) -> str:
        return f"table2_{self.row_number:02d}_{slug(self.english_name)}"


TABLE2_PERSONALITIES = (
    Table2Personality(1, "Rabbi Avraham Av-Beit-Din of Narbonne", ("Av-Beit-Din of Narbonne",)),
    Table2Personality(2, "Rabbi Avraham Yizhaki", ("Rabbi Avraham", "Yizhaki")),
    Table2Personality(3, "Rabbi Avraham Ha-Malakh", ("Rabbi Avraham", "Ha-Malak")),
    Table2Personality(4, "Rabbi Avraham Saba", ("Rabbi Avraham Saba",)),
    Table2Personality(5, "Rabbi Aaron of Karlin", ("Rabbi Aaron of Karlin",)),
    Table2Personality(6, "Rabbi Eliezer Ashkenazi", ("Rabbi Eliezer Ashkenazi",)),
    Table2Personality(7, "Rabbi David Oppenheim", ("Rabbi David Oppenheim",)),
    Table2Personality(8, "Rabbi David Ha-Nagid", ("Rabbi David Ha-Nagid",)),
    Table2Personality(9, "Rabbi David Nieto", ("Rabbi David Nieto",)),
    Table2Personality(10, "Rabbi Haim Abulafia", ("Rabbi Haim Abulafia",)),
    Table2Personality(11, "Rabbi Haim Benbenest", ("Rabbi Haim Benbenest",)),
    Table2Personality(12, "Rabbi Haim Capusi", ("Rabbi Haim", "Capusi")),
    Table2Personality(13, "Rabbi Haim Shabetai", ("Rabbi Haim", "Shabetai")),
    Table2Personality(14, "Rabbi Yair Haim Bacharach", ("Rabbi Yair Haim Bacharach",)),
    Table2Personality(15, "Rabbi Yehudah Hasid", ("Rabbi Yehudah Hasid",)),
    Table2Personality(16, "Rabbi Yehudah Ayash", ("Rabbi Yehudah Ayash",)),
    Table2Personality(17, "Rabbi Yehosef Ha-Nagid", ("Rabbi Yehosef Ha-Nagid",)),
    Table2Personality(18, "Rabbi Yehoshua of Cracow", ("Rabbi Yehoshua of Cracow",)),
    Table2Personality(19, "The Maharit", ("The Maharit",)),
    Table2Personality(20, "Rabbi Yosef Teomim", ("Rabbi Yosef Teomim",)),
    Table2Personality(21, "Rabbi Yakov Beirav", ("Rabbi Yakov", "Beirav")),
    Table2Personality(22, "Rabbi Israel Yaakov Hagiz", ("Rabbi Israel Yaakov Hagiz",)),
    Table2Personality(23, "The Maharil", ("The Maharil",)),
    Table2Personality(24, "The Yaabez", ("The Yaabez",)),
    Table2Personality(25, "Rabbi Yizhak Ha-Levi Horowitz", ("Rabbi Yizhak", "Ha-Levi Horowitz")),
    Table2Personality(26, "Rabbi Menahem Mendel Krochmal", ("Rabbi Menahem", "Mendel Krochmal")),
    Table2Personality(27, "Rabbi Moshe Zacuto", ("Rabbi Moshe", "Zacuto")),
    Table2Personality(28, "Rabbi Moshe Margalith", ("Rabbi Moshe Margalith",)),
    Table2Personality(29, "Rabbi Azariah Figo", ("Rabbi Azariah Figo",)),
    Table2Personality(30, "Rabbi Immanuel Hai Ricchi", ("Rabbi Immanuel Hai Ricchi",)),
    Table2Personality(31, "Rabbi Shalom Sharabi", ("Rabbi Shalom", "Sharabi")),
    Table2Personality(32, "Rabbi Shelomo of Cheim", ("Rabbi Shelomo of Cheim",)),
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    pages = extract_pages(args.source)
    rows = build_anchor_rows(pages, TABLE2_PERSONALITIES)
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


def build_anchor_rows(
    pages: list[str],
    personalities: tuple[Table2Personality, ...],
) -> list[dict[str, str]]:
    table2_page = find_table2_page(pages)
    table2_text = "" if table2_page is None else pages[table2_page - 1]
    return [
        row_for_personality(personality, table2_text, table2_page)
        for personality in personalities
    ]


def find_table2_page(pages: list[str]) -> int | None:
    for index, page in enumerate(pages, start=1):
        normalized = normalize_space(page).casefold()
        if "table 2" in normalized and "second list of personalities" in normalized:
            return index
    return None


def row_for_personality(
    personality: Table2Personality,
    table2_text: str,
    table2_page: int | None,
) -> dict[str, str]:
    found = table2_page is not None and fragments_found(table2_text, personality.search_fragments)
    return {
        "anchor_id": personality.anchor_id,
        "row_number": str(personality.row_number),
        "english_name": personality.english_name,
        "status": "found" if found else "missing",
        "page": str(table2_page or "") if found else "",
        "search_fragments": "; ".join(personality.search_fragments),
        "current_read": TABLE2_READ if found else "Table 2 English row-label anchor not found in extracted PDF text.",
    }


def fragments_found(text: str, fragments: tuple[str, ...]) -> bool:
    normalized_text = normalize_space(text).casefold()
    return all(normalize_space(fragment).casefold() in normalized_text for fragment in fragments)


def normalize_space(value: str) -> str:
    return " ".join(value.split())


def slug(value: str) -> str:
    chars = []
    for char in value.lower():
        if char.isalnum():
            chars.append(char)
        elif chars and chars[-1] != "_":
            chars.append("_")
    return "".join(chars).strip("_")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    lines = [
        "# WRR Primary Table 2 Anchors",
        "",
        "Status: source-row-label audit from the local WRR 1994 PDF; not Hebrew term extraction.",
        "",
        "This checks that the English row labels for the second-list personalities",
        "are visible in extracted PDF text. It does not treat the Hebrew table",
        "cells as machine-ready term/date data.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.analyze_wrr_primary_table2_anchors "
            f"--source {args.source} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Row Anchors",
        "",
        "| Row | English name | Status | Page | Search fragments |",
        "| ---: | --- | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["row_number"]),
                    markdown_cell(row["english_name"]),
                    f"`{markdown_cell(row['status'])}`",
                    markdown_cell(row["page"]),
                    markdown_cell(row["search_fragments"]),
                ]
            )
            + " |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def write_manifest(args: argparse.Namespace, rows: list[dict[str, str]], started: float) -> None:
    found = sum(1 for row in rows if row["status"] == "found")
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "source": str(args.source),
        "source_sha256": sha256_file(args.source),
        "rows": len(rows),
        "found": found,
        "missing": len(rows) - found,
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
