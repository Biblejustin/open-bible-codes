# LXX Apocrypha Bridge Controls

Status: non-Bible boundary controls for the initial LXX apocrypha bridge scan.
This is not a claim report.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_controls --canonical-label LXX --canonical-config configs/example_ebible_grclxx.toml --control ILIAD=configs/nonbible_greek_perseus_iliad.toml --control ODYSSEY=configs/nonbible_greek_perseus_odyssey.toml --control HERODOTUS=configs/nonbible_greek_perseus_herodotus.toml --terms terms/theological_terms.csv --terms terms/prophetic_terms.csv --terms terms/greek_nt_claim_terms.csv --observed reports/apocrypha_bridge_candidates/bridge_candidates.csv --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --out reports/apocrypha_bridge_controls/control_summary.csv --term-out reports/apocrypha_bridge_controls/term_summary.csv --markdown-out docs/APOCRYPHA_BRIDGE_CONTROLS.md --manifest-out reports/apocrypha_bridge_controls/manifest.json
```

## Observed Bridge Baseline

- observed bridge rows: 62
- observed terms with bridge rows: 21
- observed apocrypha_to_canonical: 27
- observed canonical_to_apocrypha: 35
- non-Bible controls >= observed total: 0 of 3

## Control Summary

| Control | Bridge rows | Terms | C→A | A→C | Multi |
| --- | ---: | ---: | ---: | ---: | ---: |
| `ILIAD` | 59 | 24 | 28 | 31 | 0 |
| `ODYSSEY` | 39 | 15 | 18 | 21 | 0 |
| `HERODOTUS` | 61 | 27 | 27 | 34 | 0 |

## Top Control Terms

| Control | Term | Bridge rows | C→A | A→C | Multi |
| --- | --- | ---: | ---: | ---: | ---: |
| `ODYSSEY` | `ναοσ` (naos; English: temple) | 13 | 5 | 8 | 0 |
| `ILIAD` | `αιμα` (haima; English: blood) | 12 | 4 | 8 | 0 |
| `HERODOTUS` | `αιμα` (haima; English: blood) | 11 | 4 | 7 | 0 |
| `ILIAD` | `ναοσ` (naos; English: temple) | 9 | 6 | 3 | 0 |
| `HERODOTUS` | `ναοσ` (naos; English: temple) | 8 | 4 | 4 | 0 |
| `HERODOTUS` | `αμην` (amen; English: Amen) | 6 | 3 | 3 | 0 |
| `ILIAD` | `αμην` (amen; English: Amen) | 5 | 2 | 3 | 0 |
| `ILIAD` | `υιοσ` (huios; English: son) | 4 | 2 | 2 | 0 |
| `ODYSSEY` | `αιμα` (haima; English: blood) | 4 | 2 | 2 | 0 |
| `ODYSSEY` | `υιοσ` (huios; English: son) | 4 | 4 | 0 | 0 |
| `HERODOTUS` | `αδησ` (ades; English: Hades) | 3 | 3 | 0 | 0 |
| `HERODOTUS` | `θεοσ` (theos; English: God) | 3 | 2 | 1 | 0 |
| `HERODOTUS` | `λεων` (leon; English: Lion) | 3 | 0 | 3 | 0 |
| `ILIAD` | `αδαμ` (adam; English: Adam) | 3 | 3 | 0 | 0 |
| `ILIAD` | `αδησ` (ades; English: Hades) | 3 | 2 | 1 | 0 |
| `ILIAD` | `ρωμη` (rome; English: Rome) | 3 | 1 | 2 | 0 |
| `ILIAD` | `σιων` (Sion; English: Zion) | 3 | 2 | 1 | 0 |
| `ODYSSEY` | `ελαμ` (Elam; English: Elam) | 3 | 1 | 2 | 0 |
| `HERODOTUS` | `δοξα` (doxa; English: glory) | 2 | 0 | 2 | 0 |
| `HERODOTUS` | `ελαμ` (Elam; English: Elam) | 2 | 0 | 2 | 0 |
| `HERODOTUS` | `ισαακ` (Isaak; English: Isaac) | 2 | 1 | 1 | 0 |
| `HERODOTUS` | `οργη` (orge; English: Wrath) | 2 | 1 | 1 | 0 |
| `HERODOTUS` | `σαρρα` (sarra) | 2 | 1 | 1 | 0 |
| `HERODOTUS` | `τυροσ` (turos) | 2 | 1 | 1 | 0 |
| `ILIAD` | `χαραν` (charan; English: Haran) | 2 | 1 | 1 | 0 |
| `ODYSSEY` | `αδαμ` (adam; English: Adam) | 2 | 0 | 2 | 0 |
| `ODYSSEY` | `αμην` (amen; English: Amen) | 2 | 1 | 1 | 0 |
| `ODYSSEY` | `αμνοσ` (amnos; English: lamb) | 2 | 1 | 1 | 0 |
| `ODYSSEY` | `θεοσ` (theos; English: God) | 2 | 1 | 1 | 0 |
| `HERODOTUS` | `αδαμ` (adam; English: Adam) | 1 | 1 | 0 | 0 |
| `HERODOTUS` | `βασαν` (basan; English: Bashan) | 1 | 1 | 0 | 0 |
| `HERODOTUS` | `δαυιδ` (dauid; English: David) | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `ελκη` (elke; English: boils/sores) | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `ηλιασ` (elias) | 1 | 1 | 0 | 0 |
| `HERODOTUS` | `καροσ` (karos; English: Carus) | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `κερασ` (keras) | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `μαρια` (Maria; English: Mary) | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `νικαω` (nikao) | 1 | 0 | 1 | 0 |
| `HERODOTUS` | `νομοσ` (nomos; English: law) | 1 | 1 | 0 | 0 |
| `HERODOTUS` | `ρωμη` (rome; English: Rome) | 1 | 0 | 1 | 0 |

## Read

- These controls preserve the LXX canonical prefix
  length and replace the apocrypha block with same-length non-Bible
  control text.
- A control match means the tested canonical/block boundary can generate
  comparable cross-boundary ELS rows.
- This does not answer manuscript-specific insertion order; it only tests
  whether the first boundary scan is unusual against comparable
  boundary opportunities.
