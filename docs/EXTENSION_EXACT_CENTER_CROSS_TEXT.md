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

Only `δοξα` survives the cross-text requirement.

| Source | Term | Extension | Opposite text | Matches | Status |
| --- | --- | --- | --- | ---: | --- |
| SBLGNT | `αιμα` | `ναιμανο` | TR_NT | 0 | `source_only` |
| SBLGNT | `δοξα` | `δοξανωσ` | TR_NT | 1 | `cross_text_match` |
| TR_NT | `δοξα` | `δοξανωσ` | SBLGNT | 1 | `cross_text_match` |
| SBLGNT | `υιος` | `ουουιοσ` | TR_NT | 0 | `source_only` |

Read:

- `δοξα` remains the only exact-center cohort key with TR_NT/SBLGNT support.
- SBLGNT `αιμα` and `υιος` should be demoted unless a looser cross-text rule is intentionally declared.
- Exact key matching is strict; it does not count related terms or nearby but non-identical extension phrases.

## Caution

Cross-text support is a filter, not proof. `δοξα` still has a hidden full extension phrase, not a surface phrase in the passage.

## Next Check

- keep `δοξα` as the only exact-center cross-text extension review row
- apply 200/200 controls only to cross-text rows
- if testing SBLGNT-only rows, mark them as source-specific screens

Final gate report is now tracked in `docs/EXTENSION_EXACT_CENTER_FINAL_GATE.md`.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_exact_center_cross_text
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
