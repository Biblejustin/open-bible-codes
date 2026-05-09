# CRD Preregistration

Status: template only. This document must be locked before any Centered-Relevance Density run is interpreted.

## Hypothesis

TEMPLATE: state the hypothesis before inspecting density output.

## Term List Path

`terms/theological_terms.csv`

## Relevance Dictionary Path And Hash

- path: `terms/relevance_dictionary.toml`
- sha256: `TEMPLATE_REPLACE_WITH_LOCKED_DICTIONARY_SHA256`

## Classifier Mode And Locked Parameters

- classifier_mode: `deterministic`
- llm_provider: `TEMPLATE`
- llm_model: `TEMPLATE`
- llm_model_version: `TEMPLATE`
- system_prompt_path: `prompts/crd_classifier_v1/system.md`
- system_prompt_sha256: `TEMPLATE_REPLACE_WITH_SYSTEM_PROMPT_SHA256`
- user_prompt_template_path: `prompts/crd_classifier_v1/user_template.md`
- user_prompt_template_sha256: `TEMPLATE_REPLACE_WITH_USER_PROMPT_SHA256`
- llm_temperature: `0`
- llm_max_tokens: `TEMPLATE`
- max_api_calls: `0`
- max_estimated_cost_usd: `0`

## Corpora

TEMPLATE: list Bible editions and language-matched secular controls.

## Skip Range

`2..100`

## Direction

`both`

## Decision Rule

TEMPLATE: define the density comparison rule before running.

## Multiple Comparisons Correction

TEMPLATE: choose Bonferroni or Benjamini-Hochberg and state the threshold before running.

## Lock Date

TEMPLATE

## Locked By

TEMPLATE

## Reviewers

TEMPLATE

## Locked Hash

TEMPLATE_REPLACE_WITH_THIS_DOCUMENT_SHA256

## Required Preflight Checklist

- [ ] Hypothesis is non-empty.
- [ ] Term list path is final.
- [ ] Relevance dictionary path and hash are final.
- [ ] Classifier mode and all locked parameters are final.
- [ ] Corpora are final.
- [ ] Skip range is final.
- [ ] Direction is final.
- [ ] Decision rule is final.
- [ ] Multiple-comparisons method and threshold are final.
- [ ] Lock date, locked by, reviewers, and locked hash are final.

## Sample Audit Log Review

Before an LLM-mode or parallel-mode run is permitted for interpretation, paste at least 50 representative classifications here and record reviewer sign-off. The sample must include relevant, non-relevant, and borderline rows when available.

Reviewer sign-off: TEMPLATE
