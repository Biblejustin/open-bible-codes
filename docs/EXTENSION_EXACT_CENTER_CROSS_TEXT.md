# Extension Exact-Center Cross-Text Review

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `extension_exact_center_cross_text`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_exact_center_cross_text`
- Generated summary: `reports/extension_exact_center_cross_text_summary.csv`
- Generated markdown: `reports/extension_exact_center_cross_text.md`
- Generated manifest: `reports/extension_exact_center_cross_text.manifest.json`
- Output size: 4 summary rows
- Runtime observed: 0.577s through the protocol runner

This checks each exact-center extension cohort row against the opposite Greek NT text using the exact extension key:

- normalized term
- skip
- direction
- extension type
- extended sequence
- matched normalized phrase

## Main Read

Only `δοξα` (doxa; English: glory) survives the cross-text requirement.

| Source | Term | Extension | Opposite text | Matches | Status |
| --- | --- | --- | --- | ---: | --- |
| SBLGNT | `αιμα` (haima; English: blood) | `ναιμανο` (naimano; English: hidden extension form from haima) | TR_NT | 0 | `source_only` |
| SBLGNT | `δοξα` (doxa; English: glory) | `δοξανωσ` (doxanos; English: hidden extension form from doxa) | TR_NT | 1 | `cross_text_match` |
| TR_NT | `δοξα` (doxa; English: glory) | `δοξανωσ` (doxanos; English: hidden extension form from doxa) | SBLGNT | 1 | `cross_text_match` |
| SBLGNT | `υιος` (huios; English: son) | `ουουιοσ` (ouhuios; English: hidden extension form from huios) | TR_NT | 0 | `source_only` |

Read:

- `δοξα` (doxa; English: glory) remains the only exact-center cohort key with TR_NT/SBLGNT support.
- SBLGNT `αιμα` (haima; English: blood) and `υιος` (huios; English: son) should be demoted unless a looser cross-text rule is intentionally declared.
- Exact key matching is strict; it does not count related terms or nearby but non-identical extension phrases.

## Caution

Cross-text support is a filter, not conclusive evidence. `δοξα` (doxa; English: glory) still has a hidden full extension phrase, not a surface phrase in the passage.

## Follow-Up Status

- 200/200 controls for the surviving `δοξα` (doxa; English: glory) row are
  tracked in `docs/EXTENSION_EXACT_CENTER_CONTROLS.md`.
- The final exact-center gate is tracked in
  `docs/EXTENSION_EXACT_CENTER_FINAL_GATE.md`.
- Four-source and confirmatory doxa follow-ups are tracked in
  `docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_REPORT.md` and
  `docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md`.

The SBLGNT-only rows remain source-specific screens unless a new prospective
rule explicitly includes source-only rows.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_exact_center_cross_text
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
