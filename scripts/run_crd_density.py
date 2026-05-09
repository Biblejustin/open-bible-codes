#!/usr/bin/env python3
"""Run Centered-Relevance Density over centered ELS hits."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import time
import tomllib
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els.corpus import Corpus, load_corpus
from els.search import ELSHit, find_els, normalize_for_corpus
from scripts.classify_centered_relevance import (
    CRDBudgetExceeded,
    CRDConfigurationError,
    Classifier,
    DeterministicClassifier,
    LLMClassifier,
    LLMClient,
    ClassificationResult,
    sha256_file,
    verify_hash,
)


DENSITY_FIELDNAMES = [
    "term_id",
    "term",
    "concept",
    "category",
    "language",
    "corpus",
    "corpus_class",
    "classifier_mode",
    "total_centered_hits",
    "relevant_centered_hits",
    "corpus_normalized_letters",
    "density_per_million",
    "relevance_rate",
    "agreement_rate",
    "agreement_kappa",
    "deterministic_only_relevant_count",
    "llm_only_relevant_count",
]

CLASSIFIED_HIT_FIELDNAMES = [
    "hit_id",
    "term_id",
    "term",
    "concept",
    "category",
    "language",
    "corpus",
    "corpus_class",
    "classifier_mode",
    "is_relevant",
    "relevance_type",
    "confidence",
    "skip",
    "direction",
    "start_ref",
    "center_ref",
    "end_ref",
    "center_word",
    "center_normalized_word",
    "center_verse_text",
    "span_text",
]

MAX_CONTEXT_TEXT_CHARS = 4000
SPAN_CONTEXT_RADIUS = 200


@dataclass(frozen=True)
class TermRow:
    term_id: str
    concept: str
    category: str
    language: str
    term: str
    notes: str = ""


@dataclass(frozen=True)
class CorpusSpec:
    label: str
    config: Path
    corpus_class: str
    language: str = ""


@dataclass(frozen=True)
class CRDOutputs:
    output_dir: Path
    density_matrix: Path
    classified_hits: Path
    manifest: Path
    audit_log: Path
    cache_dir: Path


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = run_crd_density(
            args.protocol,
            classifier_mode_override=args.classifier_mode,
            resume=args.resume,
            force_reset=args.force_reset,
        )
    except CRDBudgetExceeded as exc:
        print(f"CRD budget exceeded: {exc}")
        return 2
    print(result["outputs"]["density_matrix"])
    print(result["outputs"]["classified_hits"])
    print(result["outputs"]["manifest"])
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("protocol", type=Path)
    parser.add_argument("--classifier-mode", choices=["deterministic", "llm", "parallel"])
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--force-reset", action="store_true")
    return parser


def run_crd_density(
    protocol_path: str | Path,
    *,
    classifier_mode_override: str | None = None,
    resume: bool = False,
    force_reset: bool = False,
    api_client: LLMClient | None = None,
) -> dict[str, Any]:
    started = time.perf_counter()
    protocol_path = Path(protocol_path)
    protocol = tomllib.loads(protocol_path.read_text(encoding="utf-8"))
    mode = classifier_mode_override or str(protocol.get("classifier_mode", "deterministic"))
    outputs = output_paths(Path(str(protocol.get("output_dir", "reports/crd"))))
    outputs.output_dir.mkdir(parents=True, exist_ok=True)
    verify_protocol_locks(protocol, mode)
    prior_manifest = reusable_completed_manifest(
        outputs.manifest,
        protocol,
        mode,
        resume=resume,
        force_reset=force_reset,
    )
    if prior_manifest is not None:
        return prior_manifest
    terms = read_terms(resolve_term_files(protocol))
    corpora = parse_corpus_list(protocol.get("corpus_list", []))
    classifiers = build_classifiers(protocol, mode, outputs, api_client=api_client)

    density_rows: list[dict[str, Any]] = []
    hit_rows: list[dict[str, Any]] = []
    corpus_letters: dict[str, int] = {}
    status = "completed"
    budget_error = ""
    try:
        term_languages = {term.language for term in terms}
        for corpus_spec in corpora:
            if corpus_spec.language and corpus_spec.language not in term_languages:
                continue
            corpus = load_corpus(corpus_spec.config)
            corpus_letters[corpus_spec.label] = len(corpus.text)
            language = corpus_spec.language or corpus.language
            active_terms = language_matched_terms(terms, language, corpus, protocol)
            if not active_terms:
                continue
            for term in active_terms:
                grouped_results = classify_term_hits(
                    corpus_spec,
                    corpus,
                    term,
                    classifiers,
                    protocol,
                )
                hit_rows.extend(grouped_results["hit_rows"])
                density_rows.extend(
                    density_rows_for_term(
                        term,
                        corpus_spec,
                        corpus,
                        classifiers,
                        grouped_results["by_mode"],
                        grouped_results["agreements"],
                    )
                )
    except CRDBudgetExceeded as exc:
        status = "partial_budget_exceeded"
        budget_error = str(exc)

    write_rows(outputs.density_matrix, DENSITY_FIELDNAMES, density_rows)
    write_rows(outputs.classified_hits, CLASSIFIED_HIT_FIELDNAMES, hit_rows)
    manifest = build_manifest(
        protocol_path,
        protocol,
        mode,
        outputs,
        corpus_letters,
        classifiers,
        started,
        status=status,
        budget_error=budget_error,
        force_reset=force_reset,
    )
    outputs.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def output_paths(output_dir: Path) -> CRDOutputs:
    return CRDOutputs(
        output_dir=output_dir,
        density_matrix=output_dir / "density_matrix.csv",
        classified_hits=output_dir / "classified_hits.csv",
        manifest=output_dir / "manifest.json",
        audit_log=output_dir / "llm_audit.jsonl",
        cache_dir=output_dir / "llm_cache",
    )


def reusable_completed_manifest(
    manifest_path: Path,
    protocol: dict[str, Any],
    mode: str,
    *,
    resume: bool,
    force_reset: bool,
) -> dict[str, Any] | None:
    if not manifest_path.exists():
        return None
    prior = json.loads(manifest_path.read_text(encoding="utf-8"))
    if prior.get("status") != "completed":
        return None
    prereg_hash = str(protocol.get("preregistration_sha256", ""))
    if force_reset:
        return None
    mismatches = []
    if prior.get("preregistration_sha256") != prereg_hash:
        mismatches.append("preregistration hash")
    if prior.get("dictionary_hash") != protocol.get("relevance_dictionary_sha256"):
        mismatches.append("dictionary hash")
    if prior.get("classifier_mode") != mode:
        mismatches.append("classifier mode")
    if mismatches:
        raise CRDConfigurationError(f"completed CRD run has different {', '.join(mismatches)}; use --force-reset")
    if resume:
        return prior
    raise CRDConfigurationError("completed CRD run exists; use --resume or --force-reset")


def verify_protocol_locks(protocol: dict[str, Any], mode: str) -> None:
    verify_hash(Path(str(protocol["relevance_dictionary"])), str(protocol["relevance_dictionary_sha256"]), "relevance dictionary")
    prereg_path = Path(str(protocol["preregistration_doc"]))
    verify_hash(prereg_path, str(protocol["preregistration_sha256"]), "preregistration")
    validate_preregistration(prereg_path)
    if mode in {"llm", "parallel"}:
        verify_hash(Path(str(protocol["system_prompt_path"])), str(protocol["system_prompt_sha256"]), "system prompt")
        verify_hash(
            Path(str(protocol["user_prompt_template_path"])),
            str(protocol["user_prompt_template_sha256"]),
            "user prompt template",
        )
        if float(protocol.get("llm_temperature", 1)) != 0:
            raise CRDConfigurationError("llm_temperature must be 0")


def validate_preregistration(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    required_sections = [
        "## Hypothesis",
        "## Term List Path",
        "## Relevance Dictionary Path And Hash",
        "## Classifier Mode And Locked Parameters",
        "## Corpora",
        "## Skip Range",
        "## Direction",
        "## Decision Rule",
        "## Multiple Comparisons Correction",
        "## Lock Date",
        "## Locked By",
        "## Reviewers",
        "## Locked Hash",
        "## Sample Audit Log Review",
    ]
    missing = [section for section in required_sections if section not in text]
    if missing:
        raise CRDConfigurationError(f"preregistration missing sections: {', '.join(missing)}")
    for section in required_sections:
        body = section_body(text, section)
        if not body.strip():
            raise CRDConfigurationError(f"preregistration section is empty: {section}")


def section_body(text: str, section: str) -> str:
    start = text.index(section) + len(section)
    next_header = text.find("\n## ", start)
    if next_header == -1:
        return text[start:]
    return text[start:next_header]


def resolve_term_files(protocol: dict[str, Any]) -> list[Path]:
    raw = protocol.get("term_file", [])
    if isinstance(raw, str):
        return [Path(raw)]
    return [Path(str(value)) for value in raw]


def read_terms(paths: list[Path]) -> list[TermRow]:
    terms: list[TermRow] = []
    seen: set[str] = set()
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                term_id = row.get("term_id", "")
                if not term_id:
                    continue
                if term_id in seen:
                    raise CRDConfigurationError(f"duplicate term_id in CRD term files: {term_id}")
                seen.add(term_id)
                terms.append(
                    TermRow(
                        term_id=term_id,
                        concept=row.get("concept", ""),
                        category=row.get("category", ""),
                        language=row.get("language", ""),
                        term=row.get("term", ""),
                        notes=row.get("notes", ""),
                    )
                )
    return terms


def parse_corpus_list(raw: Any) -> list[CorpusSpec]:
    corpora: list[CorpusSpec] = []
    for item in raw:
        if isinstance(item, str):
            label, path = item.split("=", 1) if "=" in item else (Path(item).stem, item)
            corpora.append(CorpusSpec(label=label, config=Path(path), corpus_class="unknown"))
        else:
            corpora.append(
                CorpusSpec(
                    label=str(item["label"]),
                    config=Path(str(item["config"])),
                    corpus_class=str(item.get("corpus_class", item.get("class", "unknown"))),
                    language=str(item.get("language", "")),
                )
            )
    return corpora


def build_classifiers(
    protocol: dict[str, Any],
    mode: str,
    outputs: CRDOutputs,
    *,
    api_client: LLMClient | None,
) -> dict[str, Classifier]:
    classifiers: dict[str, Classifier] = {}
    if mode in {"deterministic", "parallel"}:
        classifiers["deterministic"] = DeterministicClassifier(protocol["relevance_dictionary"])
    if mode in {"llm", "parallel"}:
        classifiers["llm"] = LLMClassifier(
            model_id=str(protocol["llm_model"]),
            model_version=str(protocol.get("llm_model_version", protocol["llm_model"])),
            system_prompt_path=protocol["system_prompt_path"],
            user_prompt_template_path=protocol["user_prompt_template_path"],
            expected_system_prompt_sha256=str(protocol["system_prompt_sha256"]),
            expected_user_prompt_template_sha256=str(protocol["user_prompt_template_sha256"]),
            temperature=float(protocol["llm_temperature"]),
            max_tokens=int(protocol["llm_max_tokens"]),
            provider=str(protocol["llm_provider"]),
            cache_dir=outputs.cache_dir,
            audit_log_path=outputs.audit_log,
            max_api_calls=int(protocol.get("max_api_calls", 0)),
            max_estimated_cost_usd=float(protocol.get("max_estimated_cost_usd", 0)),
            estimated_cost_per_call_usd=float(protocol.get("estimated_cost_per_call_usd", 0)),
            api_client=api_client,
        )
    if not classifiers:
        raise CRDConfigurationError(f"unsupported classifier_mode: {mode}")
    return classifiers


def language_matched_terms(
    terms: list[TermRow],
    language: str,
    corpus: Corpus,
    protocol: dict[str, Any],
) -> list[TermRow]:
    min_length = int(protocol.get("min_term_length", 3))
    active: list[TermRow] = []
    for term in terms:
        if term.language != language:
            continue
        if len(normalize_for_corpus(corpus, term.term)) < min_length:
            continue
        active.append(term)
    return active


def classify_term_hits(
    corpus_spec: CorpusSpec,
    corpus: Corpus,
    term: TermRow,
    classifiers: dict[str, Classifier],
    protocol: dict[str, Any],
) -> dict[str, Any]:
    by_mode: dict[str, list[ClassificationResult]] = {mode: [] for mode in classifiers}
    hit_rows: list[dict[str, Any]] = []
    decisions_by_hit: dict[str, dict[str, bool]] = defaultdict(dict)
    max_hits = int(protocol.get("max_hits_per_term", 200))
    for hit in find_els(
        corpus,
        term.term,
        min_skip=int(protocol.get("min_skip", skip_bounds(str(protocol.get("skip_range", "2..100")))[0])),
        max_skip=int(protocol.get("max_skip", skip_bounds(str(protocol.get("skip_range", "2..100")))[1])),
        direction=str(protocol.get("direction", "both")),
        max_hits=max_hits if max_hits > 0 else None,
    ):
        base_row = hit_row(corpus_spec, corpus, term, hit)
        for mode, classifier in classifiers.items():
            result = classifier.classify(base_row, term_metadata(term))
            by_mode[mode].append(result)
            decisions_by_hit[str(base_row["hit_id"])][mode] = result.is_relevant
            hit_rows.append(classified_hit_row(base_row, mode, result))
    return {
        "by_mode": by_mode,
        "hit_rows": hit_rows,
        "agreements": agreement_metrics(decisions_by_hit),
    }


def skip_bounds(value: str) -> tuple[int, int]:
    if ".." not in value:
        raise CRDConfigurationError(f"skip_range must use MIN..MAX: {value}")
    left, right = value.split("..", 1)
    return int(left), int(right)


def term_metadata(term: TermRow) -> dict[str, str]:
    return {
        "term_id": term.term_id,
        "concept": term.concept,
        "category": term.category,
        "language": term.language,
        "term": term.term,
        "notes": term.notes,
    }


def hit_row(corpus_spec: CorpusSpec, corpus: Corpus, term: TermRow, hit: ELSHit) -> dict[str, Any]:
    # Center fields come from the existing ELSHit/corpus offset mapping path.
    row = dict(hit.as_row())
    row.update(term_metadata(term))
    row["corpus"] = corpus_spec.label
    row["corpus_class"] = corpus_spec.corpus_class
    row["language"] = term.language
    row["center_verse_text"] = center_verse_text(corpus, hit)
    row["span_text"] = span_text(corpus, hit)
    row["hit_id"] = stable_hit_id(row)
    return row


def center_verse_text(corpus: Corpus, hit: ELSHit) -> str:
    if not corpus.verses:
        return ""
    verse_index = corpus.position_to_verse[hit.center_offset]
    raw_text = corpus.verses[verse_index].raw_text
    if len(raw_text) <= MAX_CONTEXT_TEXT_CHARS:
        return raw_text
    return normalized_window(corpus.text, hit.center_offset, MAX_CONTEXT_TEXT_CHARS // 2)


def span_text(corpus: Corpus, hit: ELSHit) -> str:
    if not corpus.verses:
        return ""
    low = min(hit.start_offset, hit.end_offset)
    high = max(hit.start_offset, hit.end_offset)
    start_verse = corpus.position_to_verse[low]
    end_verse = corpus.position_to_verse[high]
    raw_text = " ".join(verse.raw_text for verse in corpus.verses[start_verse : end_verse + 1])
    if len(raw_text) <= MAX_CONTEXT_TEXT_CHARS:
        return raw_text
    start = max(0, low - SPAN_CONTEXT_RADIUS)
    end = min(len(corpus.text), high + SPAN_CONTEXT_RADIUS + 1)
    return corpus.text[start:end]


def normalized_window(text: str, center: int, radius: int) -> str:
    start = max(0, center - radius)
    end = min(len(text), center + radius + 1)
    return text[start:end]


def stable_hit_id(row: dict[str, Any]) -> str:
    payload = {
        "term_id": row.get("term_id"),
        "corpus": row.get("corpus"),
        "skip": row.get("skip"),
        "start_offset": row.get("start_offset"),
        "end_offset": row.get("end_offset"),
        "center_offset": row.get("center_offset"),
    }
    return json_hash(payload)[:16]


def json_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def classified_hit_row(base_row: dict[str, Any], mode: str, result: ClassificationResult) -> dict[str, Any]:
    row = {field: base_row.get(field, "") for field in CLASSIFIED_HIT_FIELDNAMES}
    row.update(
        {
            "classifier_mode": mode,
            "is_relevant": str(result.is_relevant).lower(),
            "relevance_type": result.relevance_type,
            "confidence": "" if result.confidence is None else result.confidence,
        }
    )
    return row


def density_rows_for_term(
    term: TermRow,
    corpus_spec: CorpusSpec,
    corpus: Corpus,
    classifiers: dict[str, Classifier],
    by_mode: dict[str, list[ClassificationResult]],
    agreements: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for mode in classifiers:
        results = by_mode.get(mode, [])
        total_hits = len(results)
        relevant_hits = sum(1 for result in results if result.is_relevant)
        letters = len(corpus.text)
        rows.append(
            {
                "term_id": term.term_id,
                "term": term.term,
                "concept": term.concept,
                "category": term.category,
                "language": term.language,
                "corpus": corpus_spec.label,
                "corpus_class": corpus_spec.corpus_class,
                "classifier_mode": mode,
                "total_centered_hits": total_hits,
                "relevant_centered_hits": relevant_hits,
                "corpus_normalized_letters": letters,
                "density_per_million": ratio(relevant_hits * 1_000_000, letters),
                "relevance_rate": ratio(relevant_hits, total_hits),
                "agreement_rate": agreements.get("agreement_rate", ""),
                "agreement_kappa": agreements.get("agreement_kappa", ""),
                "deterministic_only_relevant_count": agreements.get("deterministic_only_relevant_count", ""),
                "llm_only_relevant_count": agreements.get("llm_only_relevant_count", ""),
            }
        )
    return rows


def ratio(numerator: float, denominator: float) -> str:
    if not denominator:
        return "0"
    return f"{numerator / denominator:.9g}"


def agreement_metrics(decisions_by_hit: dict[str, dict[str, bool]]) -> dict[str, Any]:
    pairs = [
        (values["deterministic"], values["llm"])
        for values in decisions_by_hit.values()
        if "deterministic" in values and "llm" in values
    ]
    if not pairs:
        return {}
    total = len(pairs)
    agree = sum(1 for left, right in pairs if left == right)
    det_true = sum(1 for left, _ in pairs if left)
    det_false = total - det_true
    llm_true = sum(1 for _, right in pairs if right)
    llm_false = total - llm_true
    expected = ((det_true / total) * (llm_true / total)) + ((det_false / total) * (llm_false / total))
    observed = agree / total
    kappa = 1.0 if expected == 1 else (observed - expected) / (1 - expected)
    return {
        "agreement_rate": f"{observed:.9g}",
        "agreement_kappa": f"{kappa:.9g}",
        "deterministic_only_relevant_count": sum(1 for left, right in pairs if left and not right),
        "llm_only_relevant_count": sum(1 for left, right in pairs if right and not left),
    }


def build_manifest(
    protocol_path: Path,
    protocol: dict[str, Any],
    mode: str,
    outputs: CRDOutputs,
    corpus_letters: dict[str, int],
    classifiers: dict[str, Classifier],
    started: float,
    *,
    status: str,
    budget_error: str,
    force_reset: bool,
) -> dict[str, Any]:
    llm = classifiers.get("llm")
    api_calls = getattr(llm, "api_calls_made", 0)
    estimated_cost = getattr(llm, "estimated_cost_usd", 0.0)
    max_cost = float(protocol.get("max_estimated_cost_usd", 0))
    return {
        "status": status,
        "budget_error": budget_error,
        "protocol_path": str(protocol_path),
        "classifier_mode": mode,
        "relevance_dictionary": protocol.get("relevance_dictionary", ""),
        "dictionary_hash": protocol.get("relevance_dictionary_sha256", ""),
        "prompt_hashes": {
            "system": protocol.get("system_prompt_sha256", ""),
            "user_template": protocol.get("user_prompt_template_sha256", ""),
        },
        "model_version": protocol.get("llm_model_version", protocol.get("llm_model", "")),
        "run_timestamp": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "preregistration_doc": protocol.get("preregistration_doc", ""),
        "preregistration_sha256": protocol.get("preregistration_sha256", ""),
        "corpus_normalized_letters": corpus_letters,
        "total_api_calls_made": api_calls,
        "estimated_cost_usd": estimated_cost,
        "budget_remaining_usd": max(0.0, max_cost - estimated_cost),
        "force_reset": force_reset,
        "outputs": {
            "density_matrix": str(outputs.density_matrix),
            "classified_hits": str(outputs.classified_hits),
            "manifest": str(outputs.manifest),
            "audit_log": str(outputs.audit_log),
            "llm_cache": str(outputs.cache_dir),
        },
        "duration_seconds": round(time.perf_counter() - started, 3),
    }


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
