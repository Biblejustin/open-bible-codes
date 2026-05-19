# Strong Full-Span Exact-Center Synthesis

This page summarizes the exact-center follow-up chain for the strongest
full-span dynamic-skip rows. It is a navigation and interpretation aid; the
supporting reports remain the audit trail.

## Inputs

- Exact-center row export:
  `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_ROWS.md`
- Bible/control comparison:
  `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_COMPARISON.md`
- Review queue:
  `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_REVIEW_QUEUE.md`
- Context excerpts:
  `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_CONTEXT.md`
- Bible extensions:
  `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_EXTENSIONS.md`
- Control extensions:
  `docs/DYNAMIC_SKIP_STRONG_CONTROL_FULL_SPAN_EXACT_CENTER_EXTENSIONS.md`
- Matrix exports:
  `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_MATRIX.md`
- Review bundle:
  `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_REVIEW_BUNDLE.md`

## Run Chain

| Stage | Result |
| --- | ---: |
| Hit rows scanned for exact-center export | 356,494,786 |
| Exact-center paths exported | 9,794 |
| Bible exact-center paths | 1,582 |
| Control exact-center paths | 8,212 |
| Surface-word review units | 537 |
| Bible review units | 453 |
| Control review units | 84 |
| Context rows generated | 537 |
| Matrix letter rows | 39,806 |
| Review bundle rows | 537 |
| Bundle rows with strong extension flags | 43 |

## Extension Comparison

| Cohort | Exact-center paths | Raw extension rows | Phrase summary groups | Strong phrase rows |
| --- | ---: | ---: | ---: | ---: |
| Bible exact-center paths | 1,582 | 2,093 | 38 | 5 |
| Control exact-center paths | 8,212 | 37,878 | 3,274 | 50 |

The Bible strong phrase rows are all KJV `Jesus` rows. The control strong phrase
rows are all HEB_PBY_BIALIK rows, mostly Hebrew `Messiah`/`Yeshua` rows. The
Shakespeare control had only two exact-center `Jesus` paths and no
phrase-summary groups.

## Current Read

The exact-center flag is real and useful: hidden paths can center on the same
surface word, and the tooling now preserves the surface word, context, same-skip
extensions, and matrix path for review.

It is not yet a promotion rule. The strongest Bible exact-center clusters are
mostly cases where the term is also ordinary surface vocabulary in that corpus:
UHB `Yeshua` in Ezra/Nehemiah, EBIBLE_WLC `Messiah`, KJV `Jesus`, LXX `Jesus`,
and TCG_NT `Gog`. The control extension run shows why that matters: a non-Bible
Hebrew corpus produced more exact-center extension pressure than the Bible
cohort in this post-screen set.

The useful interpretation is comparative, not binary. A pattern can be worth
review if it survives language-matched controls, version comparison, ordinary
surface-frequency checks, and manual context reading. The current exact-center
chain gives us that review queue without hiding the control evidence.

## Review Priority

1. Original-language Bible rows where the center word is the same surface term:
   UHB `Yeshua`, EBIBLE_WLC `Messiah`, LXX `Jesus`, and TCG_NT `Gog`.
2. KJV `Jesus` rows with strong same-skip phrase extensions, treated as
   translation-side evidence rather than original-language conclusive evidence.
3. HEB_PBY_BIALIK control rows with strong same-skip phrase extensions, because
   they show the background rate problem most directly.
4. Matrix rows for any candidate promoted to manual table inspection.

## Next Decision Point

Before any claim-grade report, each promoted row should carry:

- exact-center path data;
- center/start/end context;
- same-skip extension status;
- matrix letter path;
- language-matched control comparison;
- version/source presence where applicable.

The current artifacts now provide those fields for the exact-center cohort.
The review bundle is the shortest entry point for manual row-by-row inspection.
