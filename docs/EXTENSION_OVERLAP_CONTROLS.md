# Extension Overlap Controls

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `extension_overlap_controls`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_overlap_controls`
- Generated summary: `reports/extension_overlap_controls_summary.csv`
- Generated examples: `reports/extension_overlap_controls_examples.csv`
- Generated markdown: `reports/extension_overlap_controls.md`
- Generated manifest: `reports/extension_overlap_controls.manifest.json`
- Output size: 6 summary rows; 6 example rows
- Runtime observed: 66.021s through the protocol runner

This tracked document summarizes the stricter overlap-only extension-control report. The generated `reports/` files remain local run artifacts.

## Method

This step narrows `extension_paired_controls` to strict TR_NT/SBLGNT overlaps.

Overlap key:

- normalized base term
- skip
- direction
- extension type
- extended sequence
- matched normalized phrase

Expected overlap pairs:

- `υιος`, skip `-4`, backward, `term_plus_after`, `υιοστησ`
- `αδαμ`, skip `11`, forward, `term_plus_after`, `αδαμεισ`
- `δοξα`, skip `21`, forward, `term_plus_after`, `δοξανωσ`

The run keeps one row per corpus per overlap key, so the report should contain 6 rows.

Controls:

- 50 shuffled-term controls preserving the target's normalized letters
- 50 random same-length strings drawn from same-corpus letter frequencies
- same corpus, same skip, same direction, same extension settings

## Main Read

All 6 overlap rows crossed the current exploratory q <= 0.05 screen.

Band counts:

| Band | Rows |
| --- | ---: |
| `extension_q_le_0.05` | 6 |

Every row has `combined_min_p = 0.019608` and `combined_min_q = 0.019608`. With 50 controls, no sampled control matched or exceeded the observed score on at least one row-local comparison, so add-one smoothing sets the floor at `1 / 51`.

This is a stronger review queue than the 10/10 all-extension screen, but still not a claim.

## Rows

| Corpus | Term | Skip | Extension | Combined p | Combined q | Band | Notes |
| --- | --- | ---: | --- | ---: | ---: | --- | --- |
| SBLGNT | `υιος` | -4 | `υιοστησ` | 0.019608 | 0.019608 | `extension_q_le_0.05` | John 5:13 overlap |
| TR_NT | `υιος` | -4 | `υιοστησ` | 0.019608 | 0.019608 | `extension_q_le_0.05` | JHN 5:13 overlap |
| SBLGNT | `αδαμ` | 11 | `αδαμεισ` | 0.019608 | 0.019608 | `extension_q_le_0.05` | Heb 13:16 overlap |
| TR_NT | `αδαμ` | 11 | `αδαμεισ` | 0.019608 | 0.019608 | `extension_q_le_0.05` | HEB 13:16 overlap |
| SBLGNT | `δοξα` | 21 | `δοξανωσ` | 0.019608 | 0.019608 | `extension_q_le_0.05` | 2Thess 3:1 overlap |
| TR_NT | `δοξα` | 21 | `δοξανωσ` | 0.019608 | 0.019608 | `extension_q_le_0.05` | 2TH 3:1 overlap |

## Read

- These rows survive a stricter text-form overlap filter.
- The extension strings are ordinary Greek phrase completions: `υἱὸς τῆς`, `Ἀδὰμ εἰς`, and `δόξαν ὡς`.
- The rows are now worth manual review in context.
- The result still mainly says "these overlap rows beat sampled local controls", not "these are encoded messages."
- Manual context review is tracked in `docs/EXTENSION_CONTEXT_REVIEW.md`.

## Cautions

- This is stronger than the 10/10 full extension screen but still exploratory.
- The p-value floor is `1 / 51 = 0.019608`.
- Rows remain short Greek theological terms.
- TR/SBLGNT overlap reduces text-form noise, but does not remove search-space effects.

## Next Stronger Run

- raise controls to 200/200 for these 6 rows if runtime is acceptable
- score only exact extension type and exact extension length, not any strong extension type
- require exact center/span surface context in both TR_NT and SBLGNT
- use the letter-path diagrams in `reports/extension_letter_paths.md` for John 5:13, Hebrews 13:16, and 2 Thessalonians 3:1

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_overlap_controls
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
