#!/usr/bin/env python3
"""Classify centered ELS hits for Centered-Relevance Density studies."""

from __future__ import annotations

import hashlib
import json
import os
import time
import tomllib
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from string import Formatter
from typing import Any, Protocol

from els.normalization import normalize_text
from scripts.json_utils import read_json_object


RELEVANCE_TYPES = {
    "surface_keyword_match",
    "verse_ref_match",
    "concept_match",
    "llm_judged_relevant",
    "llm_judged_not_relevant",
    "none",
}


class CRDConfigurationError(ValueError):
    """Raised when locked CRD configuration is invalid."""


class CRDBudgetExceeded(RuntimeError):
    """Raised when an LLM run exceeds its locked budget."""


@dataclass(frozen=True)
class ClassificationResult:
    is_relevant: bool
    relevance_type: str
    confidence: float | None = None
    audit_payload: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.relevance_type not in RELEVANCE_TYPES:
            raise ValueError(f"unsupported relevance_type: {self.relevance_type}")


class Classifier(ABC):
    @abstractmethod
    def classify(
        self,
        hit_row: dict[str, Any],
        term_metadata: dict[str, Any],
    ) -> ClassificationResult:
        """Classify one centered ELS hit."""


@dataclass(frozen=True)
class RelevanceEntry:
    term_id: str
    surface_keywords: tuple[str, ...]
    concept_codes: tuple[str, ...]
    verse_refs: tuple[str, ...]
    book_scope: tuple[str, ...]
    provenance: dict[str, Any]


@dataclass(frozen=True)
class SurfaceKeywordMatch:
    scope: str
    keyword: str
    normalized_keyword: str


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def load_relevance_dictionary(path: str | Path) -> dict[str, RelevanceEntry]:
    try:
        data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise CRDConfigurationError(f"dictionary invalid TOML: {exc}") from exc
    entries: dict[str, RelevanceEntry] = {}
    raw_entries = data.get("entries", [])
    if not isinstance(raw_entries, list):
        raise CRDConfigurationError("relevance dictionary entries must be a list")
    for index, raw in enumerate(raw_entries, start=1):
        if not isinstance(raw, dict):
            raise CRDConfigurationError(f"relevance dictionary entry {index} must be a table")
        entry = parse_relevance_entry(raw)
        if entry.term_id in entries:
            raise CRDConfigurationError(f"duplicate relevance dictionary term_id: {entry.term_id}")
        entries[entry.term_id] = entry
    return entries


def parse_relevance_entry(raw: dict[str, Any]) -> RelevanceEntry:
    required = ("term_id", "surface_keywords", "concept_codes", "verse_refs", "provenance")
    missing = [field for field in required if field not in raw]
    if missing:
        raise CRDConfigurationError(f"relevance entry missing required fields: {', '.join(missing)}")
    provenance = raw.get("provenance")
    if not isinstance(provenance, dict):
        raise CRDConfigurationError("relevance entry provenance must be a table")
    for field in ("author", "lock_date", "reviewer", "notes"):
        if field not in provenance or str(provenance.get(field, "")).strip() == "":
            raise CRDConfigurationError(f"relevance entry provenance missing {field}")
    for field in ("surface_keywords", "concept_codes", "verse_refs", "book_scope"):
        if field in raw and not isinstance(raw[field], list):
            raise CRDConfigurationError(f"relevance entry {field} must be a list")
    return RelevanceEntry(
        term_id=str(raw["term_id"]),
        surface_keywords=tuple(str(value) for value in raw["surface_keywords"]),
        concept_codes=tuple(str(value) for value in raw["concept_codes"]),
        verse_refs=tuple(str(value) for value in raw["verse_refs"]),
        book_scope=tuple(str(value) for value in raw.get("book_scope", [])),
        provenance=dict(provenance),
    )


class DeterministicClassifier(Classifier):
    def __init__(self, dictionary_path: str | Path | None = None, *, entries: dict[str, RelevanceEntry] | None = None):
        if entries is None:
            if dictionary_path is None:
                raise CRDConfigurationError("dictionary_path or entries is required")
            entries = load_relevance_dictionary(dictionary_path)
        self.entries = entries

    def classify(
        self,
        hit_row: dict[str, Any],
        term_metadata: dict[str, Any],
    ) -> ClassificationResult:
        term_id = str(term_metadata.get("term_id") or hit_row.get("term_id") or "")
        entry = self.entries.get(term_id)
        if entry is None:
            return ClassificationResult(False, "none", audit_payload={"reason": "missing_dictionary_entry"})

        ref_values = {
            str(hit_row.get("center_ref", "")),
            str(hit_row.get("start_ref", "")),
            str(hit_row.get("end_ref", "")),
        }
        if any(ref and ref in ref_values for ref in entry.verse_refs):
            return ClassificationResult(
                True,
                "verse_ref_match",
                audit_payload={"matched_refs": sorted(set(entry.verse_refs) & ref_values)},
            )

        language = str(hit_row.get("language") or term_metadata.get("language") or "")
        surface_match = surface_keyword_match(entry, hit_row, language)
        if surface_match is not None:
            return ClassificationResult(
                True,
                "surface_keyword_match",
                audit_payload={
                    "language": language,
                    "surface_match_scope": surface_match.scope,
                    "matched_surface_keyword": surface_match.keyword,
                    "matched_normalized_surface_keyword": surface_match.normalized_keyword,
                },
            )

        concept_values = {
            normalize_code(hit_row.get("concept_code", "")),
            normalize_code(hit_row.get("center_concept_code", "")),
            normalize_code(hit_row.get("surface_concept_code", "")),
        }
        concept_values.update(
            normalize_code(value)
            for value in split_codes(str(hit_row.get("concept_codes", "")))
        )
        concept_values.update(
            normalize_code(value)
            for value in split_codes(str(hit_row.get("center_concept_codes", "")))
        )
        concept_values.update(
            normalize_code(value)
            for value in split_codes(str(hit_row.get("surface_concept_codes", "")))
        )
        wanted_codes = {normalize_code(value) for value in entry.concept_codes}
        if "" not in wanted_codes and wanted_codes & concept_values:
            return ClassificationResult(
                True,
                "concept_match",
                audit_payload={"matched_codes": sorted(wanted_codes & concept_values)},
            )

        reason = "no_deterministic_match"
        if entry.book_scope and center_book(hit_row) not in set(entry.book_scope):
            reason = "outside_book_scope_no_match"
        return ClassificationResult(False, "none", audit_payload={"reason": reason})


def center_book(hit_row: dict[str, Any]) -> str:
    ref = str(hit_row.get("center_ref", ""))
    if not ref:
        return ""
    return ref.split()[0]


def normalize_code(value: Any) -> str:
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


def split_codes(value: str) -> list[str]:
    return [part.strip() for part in value.replace(";", ",").split(",") if part.strip()]


def normalize_surface(value: str, language: str) -> str:
    if not language:
        return value.strip().lower()
    return normalize_text(value, language)


def surface_keyword_match(entry: RelevanceEntry, hit_row: dict[str, Any], language: str) -> SurfaceKeywordMatch | None:
    center_word = normalize_surface(str(hit_row.get("center_word", "")), language)
    center_normalized_word = str(hit_row.get("center_normalized_word", "")).strip()
    center_verse_text = str(hit_row.get("center_verse_text", ""))
    span_text = str(hit_row.get("span_text", ""))
    for keyword in entry.surface_keywords:
        normalized_keyword = normalize_surface(keyword, language)
        if not normalized_keyword:
            continue
        if normalized_keyword == center_word or normalized_keyword == center_normalized_word:
            return SurfaceKeywordMatch("center_word", keyword, normalized_keyword)
        if normalized_phrase_in_text(keyword, center_verse_text, language) or normalized_phrase_in_text(
            keyword,
            span_text,
            language,
        ):
            scope = "center_verse" if normalized_phrase_in_text(keyword, center_verse_text, language) else "span"
            return SurfaceKeywordMatch(scope, keyword, normalized_keyword)
    return None


def normalized_phrase_in_text(keyword: str, text: str, language: str) -> bool:
    keyword_tokens = normalized_tokens(keyword, language)
    if not keyword_tokens:
        return False
    text_tokens = normalized_tokens(text, language)
    if len(keyword_tokens) == 1:
        return keyword_tokens[0] in set(text_tokens)
    width = len(keyword_tokens)
    return any(text_tokens[index : index + width] == keyword_tokens for index in range(len(text_tokens) - width + 1))


def normalized_tokens(text: str, language: str) -> list[str]:
    tokens: list[str] = []
    for raw_token in text.split():
        normalized = normalize_surface(raw_token, language)
        if normalized:
            tokens.append(normalized)
    return tokens


class LLMClient(Protocol):
    def classify(
        self,
        *,
        provider: str,
        model_id: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
    ) -> dict[str, Any]:
        """Return provider payload with response text and model version."""


class OpenAICompatibleClient:
    """Minimal OpenAI-compatible chat client used only when a real API key is configured."""

    def classify(
        self,
        *,
        provider: str,
        model_id: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
    ) -> dict[str, Any]:
        if provider.lower() != "openai":
            raise CRDConfigurationError(f"unsupported provider without custom client: {provider}")
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise CRDConfigurationError("OPENAI_API_KEY is required for provider=openai")
        payload = {
            "model": model_id,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        request = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(f"LLM API call failed: {exc}") from exc
        if not isinstance(data, dict):
            raise RuntimeError("LLM API response JSON root must be an object")
        choices = data.get("choices")
        if (
            not isinstance(choices, list)
            or not choices
            or not isinstance(choices[0], dict)
        ):
            raise RuntimeError("LLM API response choices must be a non-empty object list")
        message = choices[0].get("message")
        if not isinstance(message, dict):
            raise RuntimeError("LLM API response choice message must be an object")
        content = message.get("content", "")
        if not isinstance(content, str):
            raise RuntimeError("LLM API response message content must be a string")
        return {
            "raw_response": content,
            "model_version": str(data.get("model", model_id)),
            "response_json": data,
        }


class LLMClassifier(Classifier):
    def __init__(
        self,
        *,
        model_id: str,
        model_version: str,
        system_prompt_path: str | Path,
        user_prompt_template_path: str | Path,
        expected_system_prompt_sha256: str,
        expected_user_prompt_template_sha256: str,
        temperature: float,
        max_tokens: int,
        provider: str,
        cache_dir: str | Path,
        audit_log_path: str | Path,
        max_api_calls: int,
        max_estimated_cost_usd: float,
        estimated_cost_per_call_usd: float = 0.0,
        api_client: LLMClient | None = None,
    ):
        if temperature != 0:
            raise CRDConfigurationError("LLM temperature must be 0")
        self.model_id = model_id
        self.model_version = model_version
        self.system_prompt_path = Path(system_prompt_path)
        self.user_prompt_template_path = Path(user_prompt_template_path)
        verify_hash(self.system_prompt_path, expected_system_prompt_sha256, "system prompt")
        verify_hash(self.user_prompt_template_path, expected_user_prompt_template_sha256, "user prompt template")
        self.system_prompt = self.system_prompt_path.read_text(encoding="utf-8")
        self.user_prompt_template = self.user_prompt_template_path.read_text(encoding="utf-8")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.provider = provider
        self.cache_dir = Path(cache_dir)
        self.audit_log_path = Path(audit_log_path)
        self.max_api_calls = max_api_calls
        self.max_estimated_cost_usd = max_estimated_cost_usd
        self.estimated_cost_per_call_usd = estimated_cost_per_call_usd
        self.api_client = api_client or OpenAICompatibleClient()
        self.api_calls_made = 0
        self.estimated_cost_usd = 0.0
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)

    def classify(
        self,
        hit_row: dict[str, Any],
        term_metadata: dict[str, Any],
    ) -> ClassificationResult:
        prompt_payload = self.prompt_payload(hit_row, term_metadata)
        input_hash = normalized_hash(prompt_payload)
        cache_path = self.cache_path(input_hash)
        if cache_path.exists():
            cached = read_json_object(cache_path)
            cached_audit = dict(cached.get("audit_payload", {}))
            cached_audit["cache_hit"] = True
            cached_audit["timestamp"] = datetime.now(UTC).isoformat()
            append_jsonl(self.audit_log_path, cached_audit)
            return self.result_from_payload(cached, cache_hit=True)

        self.enforce_budget()
        user_prompt = render_template(self.user_prompt_template, prompt_payload)
        response = self.api_client.classify(
            provider=self.provider,
            model_id=self.model_id,
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        self.api_calls_made += 1
        self.estimated_cost_usd += self.estimated_cost_per_call_usd
        raw_response = str(response.get("raw_response", ""))
        parsed = parse_llm_response(raw_response)
        audit_payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "hit_row": hit_row,
            "term_metadata": term_metadata,
            "system_prompt": self.system_prompt,
            "user_prompt": user_prompt,
            "raw_response": raw_response,
            "parsed_decision": parsed,
            "model_version_returned": response.get("model_version", ""),
            "provider": self.provider,
            "cache_hit": False,
        }
        cache_payload = {
            "parsed_decision": parsed,
            "audit_payload": audit_payload,
            "model_version": response.get("model_version", self.model_version),
        }
        cache_path.write_text(json.dumps(cache_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        append_jsonl(self.audit_log_path, audit_payload)
        return self.result_from_payload(cache_payload, cache_hit=False)

    def prompt_payload(self, hit_row: dict[str, Any], term_metadata: dict[str, Any]) -> dict[str, Any]:
        return {
            "term": term_metadata.get("term") or hit_row.get("term") or "",
            "language": hit_row.get("language") or term_metadata.get("language") or "",
            "center_verse_ref": hit_row.get("center_ref", ""),
            "center_verse_text": hit_row.get("center_verse_text", ""),
            "span_text": hit_row.get("span_text", ""),
        }

    def cache_path(self, input_hash: str) -> Path:
        cache_key = normalized_hash(
            {
                "prompt_template_sha256": sha256_file(self.user_prompt_template_path),
                "model_version": self.model_version,
                "normalized_input_hash": input_hash,
            }
        )
        return self.cache_dir / f"{cache_key}.json"

    def enforce_budget(self) -> None:
        if self.max_api_calls >= 0 and self.api_calls_made >= self.max_api_calls:
            raise CRDBudgetExceeded("max_api_calls exceeded")
        if (
            self.max_estimated_cost_usd >= 0
            and self.estimated_cost_usd + self.estimated_cost_per_call_usd > self.max_estimated_cost_usd
        ):
            raise CRDBudgetExceeded("max_estimated_cost_usd exceeded")

    def result_from_payload(self, payload: dict[str, Any], *, cache_hit: bool) -> ClassificationResult:
        parsed = payload.get("parsed_decision", {})
        is_relevant = bool(parsed.get("is_relevant"))
        relevance_type = str(parsed.get("relevance_type", ""))
        expected_type = "llm_judged_relevant" if is_relevant else "llm_judged_not_relevant"
        if relevance_type not in {"llm_judged_relevant", "llm_judged_not_relevant"}:
            relevance_type = expected_type
        audit_payload = dict(payload.get("audit_payload", {}))
        audit_payload["cache_hit"] = cache_hit
        return ClassificationResult(
            is_relevant,
            relevance_type,
            confidence=parsed.get("confidence"),
            audit_payload=audit_payload,
        )


def verify_hash(path: Path, expected: str, label: str) -> None:
    actual = sha256_file(path)
    if actual != expected:
        raise CRDConfigurationError(f"{label} hash mismatch for {path}: expected {expected}, got {actual}")


def render_template(template: str, values: dict[str, Any]) -> str:
    names = {field_name for _, field_name, _, _ in Formatter().parse(template) if field_name}
    return template.format(**{name: values.get(name, "") for name in names})


def parse_llm_response(raw_response: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise ValueError("LLM response was not valid JSON") from exc
    if set(parsed) < {"is_relevant", "relevance_type", "rationale"}:
        raise ValueError("LLM response missing required fields")
    if not isinstance(parsed["is_relevant"], bool):
        raise ValueError("LLM is_relevant must be boolean")
    if parsed["relevance_type"] not in {"llm_judged_relevant", "llm_judged_not_relevant"}:
        raise ValueError("LLM relevance_type is outside locked taxonomy")
    return parsed


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def sleep_for_rate_limit(seconds: float) -> None:
    if seconds > 0:
        time.sleep(seconds)


if __name__ == "__main__":
    raise SystemExit("classify_centered_relevance is a library module")
