# Targeted Paired Controls

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `targeted_paired_controls`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only targeted_paired_controls`
- Generated summary: `reports/targeted_paired_controls_summary.csv`
- Generated examples: `reports/targeted_paired_controls_examples.csv`
- Generated markdown: `reports/targeted_paired_controls.md`
- Generated manifest: `reports/targeted_paired_controls.manifest.json`
- Output size: 41 summary rows; 41 example rows
- Runtime observed: 11.964s through the protocol runner

This tracked document summarizes the generated paired-control report. The generated `reports/` files remain local run artifacts.

## Method

Each focused target row was compared against two row-local paired controls:

- term-shuffle controls: 200 samples preserving the target row's normalized letters
- random controls: 200 same-length strings drawn from same-corpus letter frequencies

The search settings match the focused baseline:

- skip range: `2..50`
- direction: `both`
- corpora: MT_WLC, LXX, TR_NT, SBLGNT

## Main Read

Paired controls do not support any robust focused-term claim.

Band counts:

| Band | Rows |
| --- | ---: |
| `not_unusual` | 40 |
| `paired_uncorrected_p_le_0.05` | 1 |

Only `MT_WLC europe_h` crossed the uncorrected p <= 0.05 screen. Its Benjamini-Hochberg adjusted focused-row q-value is `1.0`, so it remains an uncorrected screen only.

## Concept Summary

| Concept | Best paired row | Best band | Combined p | Combined q | Read |
| --- | --- | --- | ---: | ---: | --- |
| Iran | SBLGNT `iran_g` hits=1,983 | `not_unusual` | 0.248756 | 1.0 | short-form density remains likely |
| Trump | LXX `trump_g` hits=71 | `not_unusual` | 0.293532 | 1.0 | not unusual |
| Vance | SBLGNT `vance_g` hits=259 | `not_unusual` | 0.517413 | 1.0 | not unusual |
| Netanyahu | MT_WLC `netanyahu_h` hits=8 | `not_unusual` | 0.467662 | 1.0 | not unusual |
| Gog | MT_WLC `gog_h` hits=1,364 | `not_unusual` | 0.975124 | 1.0 | short-form density remains likely |
| Magog | LXX `magog_g` hits=9 | `not_unusual` | 0.303483 | 1.0 | not unusual |
| Russia | LXX `russia_g` hits=268 | `not_unusual` | 0.512438 | 1.0 | not unusual |
| Europe | MT_WLC `europe_h` hits=17 | `paired_uncorrected_p_le_0.05` | 0.024876 | 1.0 | uncorrected screen only |
| Turkey | MT_WLC `turkey_alt_h` hits=14 | `not_unusual` | 0.263682 | 1.0 | not unusual |
| Germany | MT_WLC `germany_h` hits=2 | `not_unusual` | 0.597015 | 1.0 | not unusual |

## Focused Rows

### Iran

| Corpus | Term | Hits | Term p | Random p | Combined q | Band |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| LXX | `iran_g` | 8,375 | 1.0 | 0.278607 | 1.0 | `not_unusual` |
| TR_NT | `iran_g` | 1,876 | 0.830846 | 0.338308 | 1.0 | `not_unusual` |
| SBLGNT | `iran_g` | 1,983 | 0.353234 | 0.248756 | 1.0 | `not_unusual` |
| MT_WLC | `iran_h` | 210 | 0.920398 | 0.328358 | 1.0 | `not_unusual` |

### Trump, Vance, Netanyahu

| Concept | Corpus | Term | Hits | Term p | Random p | Combined q | Band |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Trump | LXX | `trump_g` | 71 | 0.293532 | 0.791045 | 1.0 | `not_unusual` |
| Trump | TR_NT | `trump_g` | 18 | 0.716418 | 0.776119 | 1.0 | `not_unusual` |
| Trump | SBLGNT | `trump_g` | 12 | 1.0 | 0.870647 | 1.0 | `not_unusual` |
| Trump | MT_WLC | `trump_h` | 4 | 0.492537 | 0.970149 | 1.0 | `not_unusual` |
| Vance | LXX | `vance_g` | 1,532 | 0.830846 | 0.746269 | 1.0 | `not_unusual` |
| Vance | TR_NT | `vance_g` | 241 | 0.820896 | 0.820896 | 1.0 | `not_unusual` |
| Vance | SBLGNT | `vance_g` | 259 | 0.517413 | 0.850746 | 1.0 | `not_unusual` |
| Vance | MT_WLC | `vance_h` | 331 | 1.0 | 0.890547 | 1.0 | `not_unusual` |
| Netanyahu | MT_WLC | `netanyahu_h` | 8 | 0.970149 | 0.467662 | 1.0 | `not_unusual` |
| Netanyahu | LXX/TR_NT/SBLGNT | `netanyahu_g` | 0 | 1.0 | 1.0 | 1.0 | `not_unusual` |

### Gog And Magog

| Concept | Corpus | Term | Hits | Term p | Random p | Combined q | Band |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Gog | MT_WLC | `gog_h` | 1,364 | 1.0 | 0.975124 | 1.0 | `not_unusual` |
| Gog | LXX | `gog_g` | 1,800 | 1.0 | 0.995025 | 1.0 | `not_unusual` |
| Gog | TR_NT | `gog_g` | 594 | 1.0 | 0.995025 | 1.0 | `not_unusual` |
| Gog | SBLGNT | `gog_g` | 572 | 1.0 | 0.99005 | 1.0 | `not_unusual` |
| Magog | MT_WLC | `magog_h` | 104 | 0.681592 | 0.975124 | 1.0 | `not_unusual` |
| Magog | LXX | `magog_g` | 9 | 0.303483 | 0.935323 | 1.0 | `not_unusual` |
| Magog | TR_NT | `magog_g` | 3 | 0.348259 | 0.965174 | 1.0 | `not_unusual` |
| Magog | SBLGNT | `magog_g` | 3 | 0.348259 | 0.950249 | 1.0 | `not_unusual` |

Read: raw Gog counts do not survive as unusual under paired controls. The pair/proximity follow-up is tracked in `docs/GOG_MAGOG_PAIR_CONTROLS.md`.

### Russia, Europe, Turkey, Germany

| Concept | Corpus | Term | Hits | Term p | Random p | Combined q | Band |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Russia | LXX | `russia_g` | 268 | 0.945274 | 0.512438 | 1.0 | `not_unusual` |
| Russia | TR_NT | `russia_g` | 52 | 0.925373 | 0.557214 | 1.0 | `not_unusual` |
| Russia | SBLGNT | `russia_g` | 57 | 0.621891 | 0.572139 | 1.0 | `not_unusual` |
| Russia | MT_WLC | `russia_h` | 50 | 0.731343 | 0.706468 | 1.0 | `not_unusual` |
| Europe | MT_WLC | `europe_h` | 17 | 0.024876 | 0.248756 | 1.0 | `paired_uncorrected_p_le_0.05` |
| Europe | LXX | `europe_g` | 1 | 0.835821 | 0.935323 | 1.0 | `not_unusual` |
| Europe | TR_NT | `europe_g` | 0 | 1.0 | 1.0 | 1.0 | `not_unusual` |
| Europe | SBLGNT | `europe_g` | 1 | 0.358209 | 0.810945 | 1.0 | `not_unusual` |
| Turkey | MT_WLC | `turkey_alt_h` | 14 | 0.532338 | 0.263682 | 1.0 | `not_unusual` |
| Turkey | MT_WLC | `turkey_h` | 1 | 0.412935 | 0.875622 | 1.0 | `not_unusual` |
| Turkey | TR_NT | `turkey_g` | 1 | 0.288557 | 0.373134 | 1.0 | `not_unusual` |
| Germany | MT_WLC | `germany_h` | 2 | 0.597015 | 0.761194 | 1.0 | `not_unusual` |

## Verdict

The paired controls make the focused target read more conservative:

- Iran and Vance remain high-count because they are short strings, not because they are unusual against matched controls.
- Trump, Netanyahu, Russia, Turkey, and Germany remain ordinary or low.
- Gog is dense because it is very short; Magog is present but not unusual.
- Europe Hebrew remains the only row worth rechecking, but only as an uncorrected screen.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only targeted_paired_controls
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
