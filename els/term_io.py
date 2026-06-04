"""Term-list and corpus-argument parsing helpers.

Pure helpers extracted from els.cli so analysis scripts can parse term CSVs and
--corpus/--terms arguments without importing the whole CLI. cli.py re-imports
these for its own use and for backward-compatible `from els.cli import ...`.
"""

from __future__ import annotations

import csv
from pathlib import Path

from els.search import normalize_for_corpus
from els.surface import SurfaceTerm


def collect_terms(raw_terms: list[str], terms_file: str | None) -> list[str]:
    terms = [term.strip() for term in raw_terms if term.strip()]
    if terms_file:
        path = Path(terms_file).expanduser()
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                terms.append(line)
    return terms

def read_term_rows(path: str) -> list[dict[str, str]]:
    with Path(path).expanduser().open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))

def read_term_rows_many(paths: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for raw_path in paths:
        path = Path(raw_path).expanduser()
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                row = dict(row)
                row["term_source"] = str(path)
                rows.append(row)
    return rows

def build_surface_terms(corpus, term_rows: list[dict[str, str]]) -> list[SurfaceTerm]:
    terms = []
    for row in term_rows:
        term = row.get("term", "").strip()
        normalized = normalize_for_corpus(corpus, term)
        terms.append(
            SurfaceTerm(
                term_source=row.get("term_source", ""),
                term_id=row.get("term_id", ""),
                concept=row.get("concept", ""),
                category=row.get("category", ""),
                term=term,
                normalized_term=normalized,
            )
        )
    return terms

def parse_corpus_args(raw_corpora: list[str]) -> list[tuple[str, str]]:
    parsed = []
    for raw in raw_corpora:
        if "=" not in raw:
            raise SystemExit(f"--corpus must be label=config_path: {raw}")
        label, config = raw.split("=", 1)
        label = label.strip()
        config = config.strip()
        if not label or not config:
            raise SystemExit(f"--corpus must be label=config_path: {raw}")
        parsed.append((label, config))
    return parsed

def accepted_term_languages(corpus_language: str) -> set[str]:
    if corpus_language in {"michigan", "michigan_claremont", "hebrew"}:
        return {"hebrew", "michigan"}
    if corpus_language == "greek":
        return {"greek"}
    if corpus_language == "english":
        return {"english"}
    return {corpus_language}

def is_safe_report_label(label: str) -> bool:
    return all(char.isalnum() or char in {"_", "-"} for char in label)
