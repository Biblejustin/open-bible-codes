# CRD Center-Word Self Vs Concept Findings

Status: local comparison generated from ignored outputs under `reports/crd_self_surface/` and `reports/crd_concept_surface/`.

## Scope

This comparison checks whether the broader concept-surface CRD dictionary changes the strict exact center-word result relative to the self-surface dictionary.

Self-surface means hidden `X` is centered on visible `X`.

Concept-surface means hidden `X` is centered on a visible spelling from the same committed `(language, concept)` group.

The exact `center_word` subset is stricter than both verse-level and span-level relevance, because the matched surface keyword must be the centered visible word.

## Result

The Bible exact center-word hit set is identical in the self-surface and concept-surface runs.

- self-surface Bible exact center-word rows: 1,153
- concept-surface Bible exact center-word rows: 1,153
- matching row key set: true
- self-only Bible rows: 0
- concept-only Bible rows: 0

The center-word density summaries are also effectively stable:

- term rows compared: 3,503
- rows with changed summary values: 2
- rows with changed Bible max density or Bible max corpus: 0
- rows with changed `exceeds_secular_max`: 0
- rows with changed secular max density or corpus: 2

The changed rows are secular-control changes only:

| Term | Language | Self secular max | Self secular corpus | Concept secular max | Concept secular corpus |
| --- | --- | ---: | --- | ---: | --- |
| `שטה` (shittah; English: acacia)<br>`cc_acacia_h` | hebrew | 0 | HEB_PBY_BIALIK | 1.45022905 | HEB_PBY_AHAD_HAAM |
| `חוכמה` (chokhmah; English: wisdom)<br>`wisdom_h` | hebrew | 0 | HEB_PBY_BIALIK | 0.362557261 | HEB_PBY_AHAD_HAAM |

The exact center-word version-presence view contains:

- exact center-word term rows: 154
- distinct normalized surface forms: 87
- exact center-word hit rows: 1,153
- distinct normalized surface hit paths: 496
- language distribution: Hebrew 78, Greek 40, English 36
- corpus-count distribution: 63 terms in 5 corpus labels, 1 term in 4 corpus labels, 5 terms in 3 corpus labels, 25 terms in 2 corpus labels, 60 terms in 1 corpus label

## Interpretation

For the strict exact center-word question, concept-surface expansion did not add Bible hits and did not change any exceedance decisions. That means the current exact center-word Bible signal can be reviewed from the self-surface output without losing any concept-surface Bible rows.

Concept-surface remains useful for broader center-verse and span review, but exact center-word reporting should stay separated from those wider scopes.
