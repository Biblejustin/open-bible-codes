# CRD Review Workflow

Status: workflow notes for preparing a locked Centered-Relevance Density dictionary.

## Draft Queue

```bash
make crd-review-scaffold
```

For a non-interpretive starting point that checks only whether a hidden term is
centered on its own visible surface form, use:

```bash
make crd-review-scaffold-self
```

This writes ignored local files:

- `reports/crd/relevance_review_queue.csv`
- `reports/crd/relevance_dictionary_draft.toml`

The CSV is the intended review surface. Each row maps to one `term_id`.
Fill these fields:

- `surface_keywords_reviewed`: semicolon-separated normalized surface words or phrases.
- `concept_codes_reviewed`: semicolon-separated short tags.
- `verse_refs_reviewed`: semicolon-separated exact canonical refs.
- `book_scope_reviewed`: optional semicolon-separated book codes.
- `reviewer`: required for locked provenance. This may be a person, an LLM-assisted drafting label, or a combined workflow label.
- `review_notes`: short rationale or boundary note.

Leaving all relevance fields empty means the term has no deterministic relevance
criteria and will fail locked review.

The `crd-review-scaffold-self` target pre-fills `surface_keywords_reviewed`
from the term's own surface spelling. It does not add broader related terms.
For a conservative related-variant scaffold, pass `--seed-concept-terms` to
`scripts.scaffold_crd_relevance_dictionary`; that pre-fills all surface forms
sharing the same normalized `(language, concept)` in the committed term lists.

For a broad self-surface screening run across all committed term CSVs, use:

```bash
make crd-self-surface-prepare
make crd-self-surface-run
make crd-self-surface-report
```

This writes ignored local artifacts under `reports/crd_self_surface/`.

For the same broad run with same-concept surface variants, use:

```bash
make crd-concept-surface-prepare
make crd-concept-surface-run
make crd-concept-surface-report
```

This writes ignored local artifacts under `reports/crd_concept_surface/`.

LLM-assisted drafting is allowed for lexical/context related-term proposals when
the provenance names that assistance. The key rule is not "human-only"; the key
rule is that the dictionary is locked before density output is interpreted.

## Convert Queue To TOML

```bash
make crd-review-apply
```

This converts the CSV into:

- `reports/crd/relevance_dictionary_reviewed.toml`

This is still ignored output. It can be regenerated while review is in progress.

## Locked Check

```bash
make crd-review-check
```

This fails until every reviewed or drafted term has:

- a dictionary entry,
- at least one relevance criterion,
- locked metadata,
- reviewer or drafting provenance.

When the check passes, copy the reviewed TOML into `terms/relevance_dictionary.toml`,
replace template metadata, update hashes in `protocols/centered_relevance_density.toml`
and `docs/CRD_PREREGISTRATION.md`, then run:

```bash
shasum -a 256 terms/relevance_dictionary.toml \
  prompts/crd_classifier_v1/system.md \
  prompts/crd_classifier_v1/user_template.md \
  docs/CRD_PREREGISTRATION.md
make crd-deterministic
```

Do not interpret CRD output if the dictionary or preregistration changed after
density output was inspected.
