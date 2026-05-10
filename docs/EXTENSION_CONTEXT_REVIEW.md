# Extension Context Review

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `extension_context_review`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_context_review`
- Generated summary: `reports/extension_context_review_summary.csv`
- Generated markdown: `reports/extension_context_review.md`
- Generated letter paths: `reports/extension_letter_paths.md`
- Generated manifest: `reports/extension_context_review.manifest.json`
- Output size: 6 summary rows
- Runtime observed: 0.831s through the protocol runner

This tracked document summarizes manual context checks for the 3 strict TR_NT/SBLGNT extension overlaps. The generated `reports/` files keep the detailed verse text.

## Method

For each strict overlap row, the script checks:

- center verse
- ELS hit span verses
- ELS extension span verses
- whether the base term appears as normal surface text
- whether the matched phrase appears as normal surface text in the extension span
- promotion gate from the original surface-context row
- letter path for the hidden extension sequence

## Main Read

The overlap-control signal becomes more modest after surface-context review.

| Context read | Rows |
| --- | ---: |
| ELS-only at hit span; matched phrase appears elsewhere in corpus | 4 |
| base normalized string appears in center verse surface text | 2 |

No strict overlap row has the full matched phrase as ordinary surface text in the hit/extension passage.

Promotion gates:

| Gate | Rows |
| --- | ---: |
| `hold_same_category_only` | 4 |
| `promote_exact_center` | 2 |

## Row Reads

| Overlap | Rows | Context read |
| --- | ---: | --- |
| `υιοσ` (huios; English: son) / `υιοστησ` (huiostes; English: hidden extension form from huios) | 2 | ELS-only in John 5:13; matched phrase occurs elsewhere |
| `αδαμ` (Adam; English: Adam) / `αδαμεισ` (adameis; English: hidden extension form from Adam) | 2 | ELS-only in Hebrews 13:15-16; matched phrase occurs elsewhere |
| `δοξα` (doxa; English: glory) / `δοξανωσ` (doxanos; English: hidden extension form from doxa) | 2 | base normalized string appears in 2 Thessalonians 3:1; full matched phrase does not |

## Interpretation

- The overlap controls still identify these rows as worth review.
- Context review does not support saying the hit passages plainly discuss the full extension phrases.
- The `δοξα` (doxa; English: glory) overlap is the only promotion-gate pass because the original surface-context row is exact-center.
- The `υιος` (huios; English: son) and `αδαμ` (Adam; English: Adam) overlaps are weaker because their matched phrases are ELS-only at the hit span and their surface context is same-category only.

## Letter Paths

The generated `reports/extension_letter_paths.md` file now gives one compact table per corpus row:

- letter index
- role (`term`, `before`, or `after`)
- normalized hidden letter
- normalized corpus offset
- verse reference
- surface word containing that letter

This is the human review sheet for the 3 strict overlaps.

## Next Stronger Review

- use `docs/EXTENSION_EXACT_CENTER_CONTROLS.md` as the deeper exact-center follow-up
- use `docs/EXTENSION_EXACT_CENTER_COHORT_CONTROLS.md` to compare `δοξα` (doxa; English: glory) with the broader exact-center top-row cohort

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_context_review
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
