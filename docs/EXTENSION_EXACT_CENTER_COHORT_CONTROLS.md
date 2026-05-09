# Extension Exact-Center Cohort Controls

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `extension_exact_center_cohort_controls`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_exact_center_cohort_controls`
- Generated summary: `reports/extension_exact_center_cohort_controls_summary.csv`
- Generated examples: `reports/extension_exact_center_cohort_controls_examples.csv`
- Generated markdown: `reports/extension_exact_center_cohort_controls.md`
- Generated manifest: `reports/extension_exact_center_cohort_controls.manifest.json`
- Output size: 4 summary rows; 4 example rows
- Runtime observed: 45.787s through the protocol runner

This broadens the exact-center check beyond the hand-picked `δοξα` overlap. It keeps every NT extension-top row whose center verse has the base term as exact surface context, then dedupes repeated rows by corpus and overlap key.

## Scope

Included rows:

| Corpus | Term | Skip | Extension | Center | Note |
| --- | --- | ---: | --- | --- | --- |
| TR_NT | `δοξα` | 21 | `δοξανωσ` | 2TH 3:1 | exact center; strict overlap |
| SBLGNT | `δοξα` | 21 | `δοξανωσ` | 2Thess 3:1 | exact center; strict overlap |
| SBLGNT | `αιμα` | 14 | `ναιμανο` | Rev 17:6 | exact center; top-row only |
| SBLGNT | `υιος` | 25 | `ουουιοσ` | Luke 19:9 | exact center; top-row only |

Controls:

- 50 shuffled-term controls preserving the target's normalized letters
- 50 random same-length strings drawn from same-corpus letter frequencies
- same corpus, same skip, same direction, same extension settings

## Main Read

All 4 exact-center cohort rows crossed the exploratory q <= 0.05 screen.

Band counts:

| Band | Rows |
| --- | ---: |
| `extension_q_le_0.05` | 4 |

Rows:

| Corpus | Term | Extension | Combined p | Combined q | Term-any p | Random-any p | Band |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| SBLGNT | `αιμα` | `ναιμανο` | 0.019608 | 0.019608 | 0.098039 | 0.019608 | `extension_q_le_0.05` |
| SBLGNT | `υιος` | `ουουιοσ` | 0.019608 | 0.019608 | 0.058824 | 0.019608 | `extension_q_le_0.05` |
| SBLGNT | `δοξα` | `δοξανωσ` | 0.019608 | 0.019608 | 0.078431 | 0.019608 | `extension_q_le_0.05` |
| TR_NT | `δοξα` | `δοξανωσ` | 0.019608 | 0.019608 | 0.039216 | 0.019608 | `extension_q_le_0.05` |

Read:

- `δοξα` no longer stands alone as the only exact-center extension row.
- The broader exact-center cohort still screens above local controls.
- With 50 controls, the p-value floor is `1 / 51 = 0.019608`; these rows should not be over-read.
- All rows still involve short Greek base terms.

## Caution

This is a screening queue. Exact-center context means the base term appears in the center verse as surface text; it does not mean the full extended phrase appears as surface text in the hit or extension span.

The SBLGNT-only `αιμα` and `υιος` rows need separate cross-text checks before they can be compared with the TR/SBLGNT `δοξα` overlap.

## Next Check

- inspect the `αιμα` and `υιος` letter paths and surface passages
- run cross-text overlap checks for exact-center cohort rows
- raise controls to 200/200 only for rows that survive manual context review

Manual context and letter-path review is now tracked in
`docs/EXTENSION_EXACT_CENTER_COHORT_REVIEW.md`.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_exact_center_cohort_controls
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
