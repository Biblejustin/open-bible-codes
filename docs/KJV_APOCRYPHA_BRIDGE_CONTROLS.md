# KJVA Apocrypha Bridge Controls

Status: non-Bible boundary controls for the initial KJVA apocrypha bridge scan.
This is not a claim report.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_controls --canonical-label KJVA --canonical-config configs/example_ebible_engkjv_apocrypha.toml --control SHAKESPEARE=configs/nonbible_english_pg_shakespeare.toml --control WAR_PEACE=configs/nonbible_english_pg_war_and_peace.toml --control MOBY_DICK=configs/nonbible_english_pg_moby_dick.toml --terms terms/english_search_terms.csv --observed reports/kjv_apocrypha_bridge_candidates/bridge_candidates.csv --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --out reports/kjv_apocrypha_bridge_controls/control_summary.csv --term-out reports/kjv_apocrypha_bridge_controls/term_summary.csv --markdown-out docs/KJV_APOCRYPHA_BRIDGE_CONTROLS.md --manifest-out reports/kjv_apocrypha_bridge_controls/manifest.json
```

## Observed Bridge Baseline

- observed bridge rows: 535
- observed terms with bridge rows: 114
- observed apocrypha_to_canonical: 270
- observed canonical_to_apocrypha: 265
- non-Bible controls >= observed total: 0 of 3

## Control Summary

| Control | Bridge rows | Terms | C→A | A→C | Multi |
| --- | ---: | ---: | ---: | ---: | ---: |
| `SHAKESPEARE` | 289 | 85 | 157 | 132 | 0 |
| `WAR_PEACE` | 207 | 69 | 105 | 102 | 0 |
| `MOBY_DICK` | 262 | 81 | 133 | 129 | 0 |

## Top Control Terms

| Control | Term | Bridge rows | C→A | A→C | Multi |
| --- | --- | ---: | ---: | ---: | ---: |
| `WAR_PEACE` | `heth` | 29 | 15 | 14 | 0 |
| `MOBY_DICK` | `heth` | 24 | 15 | 9 | 0 |
| `MOBY_DICK` | `tree` | 24 | 14 | 10 | 0 |
| `SHAKESPEARE` | `heth` | 23 | 13 | 10 | 0 |
| `SHAKESPEARE` | `tree` | 22 | 12 | 10 | 0 |
| `WAR_PEACE` | `tree` | 16 | 8 | 8 | 0 |
| `MOBY_DICK` | `rent` | 13 | 6 | 7 | 0 |
| `SHAKESPEARE` | `otho` | 12 | 8 | 4 | 0 |
| `SHAKESPEARE` | `heal` | 11 | 4 | 7 | 0 |
| `SHAKESPEARE` | `leah` | 11 | 7 | 4 | 0 |
| `SHAKESPEARE` | `seal` | 10 | 6 | 4 | 0 |
| `MOBY_DICK` | `leah` | 9 | 7 | 2 | 0 |
| `MOBY_DICK` | `nero` | 9 | 5 | 4 | 0 |
| `SHAKESPEARE` | `noah` | 9 | 6 | 3 | 0 |
| `MOBY_DICK` | `otho` | 8 | 5 | 3 | 0 |
| `SHAKESPEARE` | `hits` | 8 | 6 | 2 | 0 |
| `SHAKESPEARE` | `seed` | 8 | 4 | 4 | 0 |
| `SHAKESPEARE` | `shot` | 8 | 6 | 2 | 0 |
| `MOBY_DICK` | `heal` | 7 | 4 | 3 | 0 |
| `MOBY_DICK` | `seed` | 7 | 1 | 6 | 0 |
| `SHAKESPEARE` | `shem` | 7 | 3 | 4 | 0 |
| `WAR_PEACE` | `haiti` | 7 | 5 | 2 | 0 |
| `WAR_PEACE` | `leah` | 7 | 5 | 2 | 0 |
| `MOBY_DICK` | `aram` | 6 | 1 | 5 | 0 |
| `MOBY_DICK` | `eden` | 6 | 2 | 4 | 0 |
| `SHAKESPEARE` | `eden` | 6 | 1 | 5 | 0 |
| `SHAKESPEARE` | `lane` | 6 | 3 | 3 | 0 |
| `SHAKESPEARE` | `nero` | 6 | 3 | 3 | 0 |
| `SHAKESPEARE` | `soot` | 6 | 2 | 4 | 0 |
| `SHAKESPEARE` | `star` | 6 | 5 | 1 | 0 |
| `WAR_PEACE` | `heal` | 6 | 0 | 6 | 0 |
| `WAR_PEACE` | `rent` | 6 | 4 | 2 | 0 |
| `WAR_PEACE` | `thin` | 6 | 0 | 6 | 0 |
| `MOBY_DICK` | `elam` | 5 | 3 | 2 | 0 |
| `MOBY_DICK` | `eyes` | 5 | 2 | 3 | 0 |
| `MOBY_DICK` | `hits` | 5 | 1 | 4 | 0 |
| `MOBY_DICK` | `rome` | 5 | 2 | 3 | 0 |
| `MOBY_DICK` | `ruth` | 5 | 3 | 2 | 0 |
| `SHAKESPEARE` | `gate` | 5 | 2 | 3 | 0 |
| `SHAKESPEARE` | `heart` | 5 | 3 | 2 | 0 |

## Read

- These controls preserve the KJVA canonical prefix
  length and replace the apocrypha block with same-length non-Bible
  control text.
- A control match means the tested canonical/block boundary can generate
  comparable cross-boundary ELS rows.
- This does not answer manuscript-specific insertion order; it only tests
  whether the first boundary scan is unusual against comparable
  boundary opportunities.
