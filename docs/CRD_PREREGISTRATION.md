# CRD Preregistration

Status: locked deterministic Gog/Magog cohort CRD run.

## Hypothesis

For the Hebrew Gog/Magog prospective cohort, centered ELS hits in Bible
editions may show a higher rate of deterministic contextual relevance than
language-matched Hebrew secular controls. This is a screening hypothesis only;
it does not promote any row to a claim without downstream controls and context
review.

## Term List Path

`terms/gog_magog_pair_prospective_terms.csv`

## Relevance Dictionary Path And Hash

- path: `terms/relevance_dictionary.toml`
- sha256: `a6406048b9953ca50715d99100994b9065394d9db31b35867666d365a3bd0f99`

## Classifier Mode And Locked Parameters

- classifier_mode: `deterministic`
- llm_provider: `openai`
- llm_model: `gpt-5`
- llm_model_version: `gpt-5`
- system_prompt_path: `prompts/crd_classifier_v1/system.md`
- system_prompt_sha256: `403bd5c4a48e45824bd895c15f43753f7a83f16c82fa89ea5e67d60e67297619`
- user_prompt_template_path: `prompts/crd_classifier_v1/user_template.md`
- user_prompt_template_sha256: `6af9bc5cca43ee6688e4f83b332ed3488d77db309968a848dabcedde95865309`
- llm_temperature: `0`
- llm_max_tokens: `200`
- max_api_calls: `0`
- max_estimated_cost_usd: `0`

## Corpora

Bible editions:

- `MT_WLC`
- `UXLC`
- `MAM`
- `EBIBLE_WLC`
- `UHB`
- `LXX`
- `TR_NT`
- `BYZ_NT`
- `TCG_NT`
- `SBLGNT`
- `KJV`

Language-matched secular controls:

- `HEB_PBY_BIALIK`
- `HEB_PBY_BRENNER`
- `HEB_PBY_AHAD_HAAM`
- `GRC_PERSEUS_ILIAD`
- `GRC_PERSEUS_ODYSSEY`
- `GRC_PERSEUS_HERODOTUS`
- `ENG_PG_SHAKESPEARE`
- `ENG_PG_WAR_PEACE`
- `ENG_PG_MOBY_DICK`

## Skip Range

`2..100`

## Direction

`both`

## Decision Rule

Compute deterministic relevant centered hits per million normalized corpus
letters for each `(term, corpus)`. Compare Bible maximum density against
language-matched secular-control maximum density per term. Treat
`exceeds_secular_max = true` as a review-priority flag, not as significance.

## Multiple Comparisons Correction

Benjamini-Hochberg q <= 0.05 if downstream p-values are computed. This initial
CRD run reports deterministic density only and does not itself compute p-values.

## Lock Date

2026-05-09

## Locked By

gpt-5-assisted-draft

## Reviewers

gpt-5-assisted-draft

## Locked Hash

Recorded in `protocols/centered_relevance_density.toml` after this document is locked.

## Required Preflight Checklist

- [x] Hypothesis is non-empty.
- [x] Term list path is final.
- [x] Relevance dictionary path and hash are final.
- [x] Classifier mode and all locked parameters are final.
- [x] Corpora are final.
- [x] Skip range is final.
- [x] Direction is final.
- [x] Decision rule is final.
- [x] Multiple-comparisons method and threshold are final.
- [x] Lock date, locked by, reviewers, and locked hash are final.

## Sample Audit Log Review

This locked run uses deterministic mode only. No LLM classification API calls
are made and no LLM audit-log sample is required for execution. If parallel or
LLM mode is later enabled, paste at least 50 representative classifications here
and record reviewer sign-off before interpreting those results.

Reviewer sign-off: gpt-5-assisted-draft for lexical/context dictionary draft.
