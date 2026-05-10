# Centered-Relevance Density Framework

Centered-Relevance Density (CRD) measures how often centered ELS hits land on contextually relevant surface text. The comparison unit is `(term, corpus, classifier_mode)`, and the normal comparison is Bible editions versus language-matched secular controls.

## Modes

- `deterministic`: exact normalized matching against the locked relevance dictionary. It uses `surface_keywords`, `verse_refs`, and `concept_codes`. It does not use fuzzy matching, embeddings, or an LLM.
- `llm`: locked-prompt classification with temperature `0`, hash-verified prompts, per-hit audit logs, cache keys, and budget caps.
- `parallel`: runs deterministic and LLM classifiers on the same centered hits and reports agreement, disagreement counts, and Cohen's kappa.

For deterministic `surface_keywords`, classified-hit output records
`surface_match_scope` so future reports can distinguish the strongest exact
case (`center_word`) from broader contextual cases (`center_verse` or `span`).
It also records the matched keyword and normalized matched keyword. This keeps
"hidden term centered on the same visible word" separate from "hidden term
centered in a verse or span that discusses the term."

## Lock Discipline

The run is invalid unless the preregistration document, relevance dictionary, and prompt files match the hashes declared by the protocol. If any prompt or dictionary changes after density output has been seen, the study needs a new preregistration. `run_crd_density.py` stores the preregistration hash in the manifest and refuses to overwrite completed runs unless `--force-reset` is supplied.

Long deterministic runs can be resumed. With `--resume`, completed `(term, corpus)`
pairs already present in the density matrix are skipped and new rows are appended.
Protocols may set `progress_interval_seconds` to print periodic stderr progress
without changing report artifacts.

## LLM Cost

LLM mode caches classifications under `reports/crd/llm_cache/`, keyed by prompt-template hash, model version, and normalized input hash. Re-runs against the same cache do not make new calls. Each protocol must declare `max_api_calls` and `max_estimated_cost_usd`; the runner aborts cleanly with partial outputs if either cap is reached.

## Recommended Workflow

1. Draft `terms/relevance_dictionary.toml` with locked provenance. LLM-assisted lexical/context drafting is allowed before lock.
2. Record reviewer, lock date, dictionary hash, prompt hashes, and decision rule in `docs/CRD_PREREGISTRATION.md`.
3. Run deterministic mode first.
4. Optionally run parallel mode to compare deterministic precision against LLM recall.
5. Review audit logs before interpreting any LLM-supported result.

See `docs/CRD_PREREGISTRATION.md` for the gating checklist.
