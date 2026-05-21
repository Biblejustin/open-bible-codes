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

- `υιος` (huios; English: son), skip `-4`, backward, `term_plus_after`, `υιοστησ` (huiostes; English: hidden extension form from huios)
- `αδαμ` (Adam; English: Adam), skip `11`, forward, `term_plus_after`, `αδαμεισ` (adameis; English: hidden extension form from Adam)
- `δοξα` (doxa; English: glory), skip `21`, forward, `term_plus_after`, `δοξανωσ` (doxanos; English: hidden extension form from doxa)

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
| SBLGNT | `υιος` (huios; English: son) | -4 | `υιοστησ` (huiostes; English: hidden extension form from huios) | 0.019608 | 0.019608 | `extension_q_le_0.05` | John 5:13 overlap |
| TR_NT | `υιος` (huios; English: son) | -4 | `υιοστησ` (huiostes; English: hidden extension form from huios) | 0.019608 | 0.019608 | `extension_q_le_0.05` | JHN 5:13 overlap |
| SBLGNT | `αδαμ` (Adam; English: Adam) | 11 | `αδαμεισ` (adameis; English: hidden extension form from Adam) | 0.019608 | 0.019608 | `extension_q_le_0.05` | Heb 13:16 overlap |
| TR_NT | `αδαμ` (Adam; English: Adam) | 11 | `αδαμεισ` (adameis; English: hidden extension form from Adam) | 0.019608 | 0.019608 | `extension_q_le_0.05` | HEB 13:16 overlap |
| SBLGNT | `δοξα` (doxa; English: glory) | 21 | `δοξανωσ` (doxanos; English: hidden extension form from doxa) | 0.019608 | 0.019608 | `extension_q_le_0.05` | 2Thess 3:1 overlap |
| TR_NT | `δοξα` (doxa; English: glory) | 21 | `δοξανωσ` (doxanos; English: hidden extension form from doxa) | 0.019608 | 0.019608 | `extension_q_le_0.05` | 2TH 3:1 overlap |

## Read

- These rows survive a stricter text-form overlap filter.
- The extension strings are ordinary Greek phrase completions: `υἱὸς τῆς` (huios tes; English: son of the), `Ἀδὰμ εἰς` (Adam eis; English: Adam into), and `δόξαν ὡς` (doxan hos; English: glory as).
- The rows are now worth manual review in context.
- The result still mainly says "these overlap rows beat sampled local controls", not "these are encoded messages."
- Manual context review is tracked in `docs/EXTENSION_CONTEXT_REVIEW.md`.

## Cautions

- This is stronger than the 10/10 full extension screen but still exploratory.
- The p-value floor is `1 / 51 = 0.019608`.
- Rows remain short Greek theological terms.
- TR/SBLGNT overlap reduces text-form noise, but does not remove search-space effects.

## Follow-Up Status

- Exact-center surface-context filtering is tracked in
  `docs/EXTENSION_EXACT_CENTER_COHORT_REVIEW.md`.
- 200/200 controls for the surviving exact-center overlap row are tracked in
  `docs/EXTENSION_EXACT_CENTER_CONTROLS.md`.
- The final exact-center gate is tracked in
  `docs/EXTENSION_EXACT_CENTER_FINAL_GATE.md`.
- Four-source and confirmatory doxa follow-ups are tracked in
  `docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_REPORT.md` and
  `docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md`.

Any stronger run should now be a newly locked prospective design, not a rerun
of this post-screen overlap queue.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_overlap_controls
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
