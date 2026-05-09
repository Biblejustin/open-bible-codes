# KJVA Apocrypha Bridge Controls

Status: non-Bible boundary controls for the initial KJVA apocrypha bridge scan.
This is not a claim report.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_controls --canonical-label KJVA --canonical-config configs/example_ebible_engkjv_apocrypha.toml --control SHAKESPEARE=configs/nonbible_english_pg_shakespeare.toml --control WAR_PEACE=configs/nonbible_english_pg_war_and_peace.toml --control MOBY_DICK=configs/nonbible_english_pg_moby_dick.toml --terms terms/english_search_terms.csv --observed reports/kjv_apocrypha_bridge_candidates/bridge_candidates.csv --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --out reports/kjv_apocrypha_bridge_controls/control_summary.csv --term-out reports/kjv_apocrypha_bridge_controls/term_summary.csv --markdown-out docs/KJV_APOCRYPHA_BRIDGE_CONTROLS.md --manifest-out reports/kjv_apocrypha_bridge_controls/manifest.json
```

## Observed Bridge Baseline

- observed bridge rows: 350
- observed terms with bridge rows: 81
- observed apocrypha_to_canonical: 178
- observed canonical_to_apocrypha: 172
- non-Bible controls >= observed total: 0 of 3

## Control Summary

| Control | Bridge rows | Terms | C→A | A→C | Multi |
| --- | ---: | ---: | ---: | ---: | ---: |
| `SHAKESPEARE` | 182 | 60 | 98 | 84 | 0 |
| `WAR_PEACE` | 140 | 50 | 72 | 68 | 0 |
| `MOBY_DICK` | 168 | 59 | 90 | 78 | 0 |

## Top Control Terms

| Control | Term | Bridge rows | C→A | A→C | Multi |
| --- | --- | ---: | ---: | ---: | ---: |
| `WAR_PEACE` | `heth` | 29 | 15 | 14 | 0 |
| `MOBY_DICK` | `heth` | 24 | 15 | 9 | 0 |
| `SHAKESPEARE` | `heth` | 23 | 13 | 10 | 0 |
| `SHAKESPEARE` | `otho` | 12 | 8 | 4 | 0 |
| `SHAKESPEARE` | `heal` | 11 | 4 | 7 | 0 |
| `SHAKESPEARE` | `seal` | 10 | 6 | 4 | 0 |
| `MOBY_DICK` | `nero` | 9 | 5 | 4 | 0 |
| `SHAKESPEARE` | `noah` | 9 | 6 | 3 | 0 |
| `MOBY_DICK` | `otho` | 8 | 5 | 3 | 0 |
| `MOBY_DICK` | `heal` | 7 | 4 | 3 | 0 |
| `SHAKESPEARE` | `shem` | 7 | 3 | 4 | 0 |
| `MOBY_DICK` | `aram` | 6 | 1 | 5 | 0 |
| `SHAKESPEARE` | `nero` | 6 | 3 | 3 | 0 |
| `SHAKESPEARE` | `star` | 6 | 5 | 1 | 0 |
| `WAR_PEACE` | `heal` | 6 | 0 | 6 | 0 |
| `MOBY_DICK` | `elam` | 5 | 3 | 2 | 0 |
| `MOBY_DICK` | `eyes` | 5 | 2 | 3 | 0 |
| `MOBY_DICK` | `rome` | 5 | 2 | 3 | 0 |
| `SHAKESPEARE` | `heart` | 5 | 3 | 2 | 0 |
| `SHAKESPEARE` | `isis` | 5 | 1 | 4 | 0 |
| `SHAKESPEARE` | `life` | 5 | 5 | 0 | 0 |
| `SHAKESPEARE` | `lord` | 5 | 2 | 3 | 0 |
| `WAR_PEACE` | `city` | 5 | 0 | 5 | 0 |
| `WAR_PEACE` | `hand` | 5 | 0 | 5 | 0 |
| `WAR_PEACE` | `star` | 5 | 5 | 0 | 0 |
| `WAR_PEACE` | `teeth` | 5 | 2 | 3 | 0 |
| `MOBY_DICK` | `heart` | 4 | 3 | 1 | 0 |
| `MOBY_DICK` | `nato` | 4 | 2 | 2 | 0 |
| `MOBY_DICK` | `noah` | 4 | 4 | 0 | 0 |
| `MOBY_DICK` | `seal` | 4 | 4 | 0 | 0 |
| `MOBY_DICK` | `star` | 4 | 3 | 1 | 0 |
| `MOBY_DICK` | `torah` | 4 | 3 | 1 | 0 |
| `SHAKESPEARE` | `fire` | 4 | 3 | 1 | 0 |
| `SHAKESPEARE` | `horn` | 4 | 4 | 0 | 0 |
| `SHAKESPEARE` | `iran` | 4 | 1 | 3 | 0 |
| `SHAKESPEARE` | `nato` | 4 | 3 | 1 | 0 |
| `WAR_PEACE` | `adar` | 4 | 3 | 1 | 0 |
| `WAR_PEACE` | `aids` | 4 | 1 | 3 | 0 |
| `WAR_PEACE` | `face` | 4 | 4 | 0 | 0 |
| `WAR_PEACE` | `nero` | 4 | 3 | 1 | 0 |

## Read

- These controls preserve the KJVA canonical prefix
  length and replace the apocrypha block with same-length non-Bible
  control text.
- A control match means the tested canonical/block boundary can generate
  comparable cross-boundary ELS rows.
- This does not answer manuscript-specific insertion order; it only tests
  whether the first boundary scan is unusual against comparable
  boundary opportunities.
