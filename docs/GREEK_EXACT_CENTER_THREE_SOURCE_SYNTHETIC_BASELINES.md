# Greek Three-Source Synthetic Extension Baselines

Status: follow-up density control for the locked three-source review queue.

This is not a new claim protocol. It is a pressure test against 1000
same-length synthetic Greek strings for the five controlled rows from
`docs/GREEK_EXACT_CENTER_THREE_SOURCE_REPORT.md`.

## Run

Commands:

```bash
python3 -m scripts.analyze_synthetic_extension_baselines \
  --top-file reports/greek_exact_center_three_source/extensions_tr_nt_top.csv \
  --top-file reports/greek_exact_center_three_source/extensions_byz_nt_top.csv \
  --top-file reports/greek_exact_center_three_source/extensions_sblgnt_top.csv \
  --surface-context-hits reports/greek_exact_center_three_source/surface_context_hits.csv \
  --require-cross-corpus-overlap \
  --require-overlap-corpus BYZ_NT \
  --synthetic-samples 1000 \
  --summary-out reports/greek_exact_center_three_source/synthetic_extension_baselines_summary.csv \
  --examples-out reports/greek_exact_center_three_source/synthetic_extension_baselines_examples.csv \
  --matches-out reports/greek_exact_center_three_source/synthetic_extension_baselines_matches.csv \
  --markdown-out reports/greek_exact_center_three_source/synthetic_extension_baselines.md \
  --manifest-out reports/greek_exact_center_three_source/synthetic_extension_baselines.manifest.json

python3 -m scripts.analyze_synthetic_extension_match_review \
  --matches reports/greek_exact_center_three_source/synthetic_extension_baselines_matches.csv \
  --summary-out reports/greek_exact_center_three_source/synthetic_extension_match_review_summary.csv \
  --markdown-out reports/greek_exact_center_three_source/synthetic_extension_match_review.md \
  --manifest-out reports/greek_exact_center_three_source/synthetic_extension_match_review.manifest.json
```

Runtime:

- synthetic baseline scoring: 526.458s
- synthetic match context review: 0.571s

## Result

| Corpus | Target | Score | Synthetic same-type >= target | Same-type p | Synthetic any >= target | Any p |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| BYZ_NT | `υιος` 25 before_plus_term `ουουιοσ` | 3214 | 1 / 1000 | 0.001998 | 5 / 1000 | 0.005994 |
| BYZ_NT | `δοξα` 21 term_plus_after `δοξανωσ` | 3211 | 0 / 1000 | 0.000999 | 2 / 1000 | 0.002997 |
| SBLGNT | `υιος` 25 before_plus_term `ουουιοσ` | 3214 | 0 / 1000 | 0.000999 | 2 / 1000 | 0.002997 |
| SBLGNT | `δοξα` 21 term_plus_after `δοξανωσ` | 3211 | 3 / 1000 | 0.003996 | 3 / 1000 | 0.003996 |
| TR_NT | `δοξα` 21 term_plus_after `δοξανωσ` | 3211 | 0 / 1000 | 0.000999 | 5 / 1000 | 0.005994 |

Read:

- Every target row had at least one any-type synthetic row match or exceed its
  score.
- Two target rows also had same-type synthetic rows match or exceed their score:
  BYZ_NT `υιος` and SBLGNT `δοξα`.
- The p-value floor for this 1000-sample run is `0.000999`.

## Synthetic Match

The 1000-sample run produced 17 synthetic match rows.

Context review:

| Context read | Rows |
| --- | ---: |
| synthetic ELS-only at hit span; matched phrase appears elsewhere | 14 |
| synthetic query appears in center verse surface text | 1 |
| synthetic query appears in hit-span surface text | 2 |

No synthetic matched phrase appeared as surface text in its own extension span.
Most synthetic matches are therefore the same kind of hidden-path phenomenon as
the real review rows: the surface phrase appears elsewhere in the corpus, not in
the hit passage.

Examples:

| Corpus | Target | Synthetic query | Synthetic extension | Score | Matched phrase refs | Context read |
| --- | --- | --- | --- | ---: | --- | --- |
| BYZ_NT | `υιος` / `ουουιοσ` | `αικα` | `εσταικαι` | 4319 | MAT 6:21; MAT 12:45; MAT 24:3; MAT 24:27; MAT 24:37 | hit-span query surface |
| BYZ_NT | `υιος` / `ουουιοσ` | `αντι` | `εαντινα` | 3311 | JHN 13:20 | center-query surface |
| SBLGNT | `δοξα` / `δοξανωσ` | `τισυ` | `τισυμασ` | 3219 | Matt 24:4; Mark 13:5; Luke 19:31; 2Cor 11:20; Gal 1:9 | hidden-path only |
| TR_NT | `δοξα` / `δοξανωσ` | `τινα` | `απαρτιναι` | 5311 | REV 14:13 | hidden-path only |

## Interpretation

This follow-up strengthens the caution:

- the real rows still pass the registered 1000/1000 shuffled-term and random
  controls;
- however, broad same-length synthetic strings can also produce equal-or-higher
  hidden-path extension scores at the same skip and direction;
- therefore the correct status remains controlled review candidate, not claim;
- any future promotion standard should require stronger surface-context rules or
  stricter extension-type constraints, not just high hidden-path extension score.

This density control does not replace the 1000/1000 shuffled-term and
same-length random controls in the main three-source report. It explains why
manual context review and visible-passage relevance remain necessary.
