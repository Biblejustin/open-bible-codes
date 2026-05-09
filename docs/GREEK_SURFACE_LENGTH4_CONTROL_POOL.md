# Greek Surface Length-4 Control Pool

Status: real-word control-pool construction; no ELS control statistic yet.

This report prepares fair controls for the tighter expanded Greek surface
triage. It counts normalized surface-substring verse frequency for every
term in the expanded Greek prospective list, then selects same-length real
Greek terms with the closest surface-frequency vectors across TR_NT,
BYZ_NT, TCG_NT, and SBLGNT.
Selected target terms are excluded from the control candidate pool.

## Inputs

- Terms: `terms/greek_surface_prospective_terms.csv`
- Selected triage rows: `reports/greek_surface_length4_followup/selected_patterns.csv`

## Surface-Frequency Scope

- terms measured: 288
- all-source surface-present terms: 162
- selected targets: 7
- matched controls per target requested: 999

## Selected Targets

| Term | Concept | Length | Surface verse vector | Sum | Controls found |
| --- | --- | ---: | --- | ---: | ---: |
| `αμην` | Amen | 4 | 155/155/155/130 | 595 | 14 |
| `χουσ` | Cush | 4 | 107/107/106/106 | 426 | 14 |
| `σιων` | Zion | 4 | 31/30/30/28 | 119 | 14 |
| `δασα` | Lasha | 4 | 28/28/28/26 | 110 | 14 |
| `αραμ` | Aram | 4 | 21/22/22/19 | 84 | 14 |
| `σαβα` | Seba | 4 | 10/9/9/7 | 35 | 14 |
| `ασηρ` | Asher | 4 | 7/7/7/7 | 28 | 14 |

## Closest Controls

| Target | Control | Control concept | Surface vector | Sum delta | Vector delta |
| --- | --- | --- | --- | ---: | ---: |
| `αμην` | `ψυχη` | Soul | 69/69/69/67 | 321 | 321 |
| `αμην` | `οργη` | Wrath | 34/34/34/34 | 459 | 459 |
| `αμην` | `σαρξ` | Flesh | 27/27/27/26 | 488 | 488 |
| `αμην` | `λεων` | Lion | 23/23/23/25 | 501 | 501 |
| `αμην` | `ρωμη` | Rome | 18/12/12/11 | 542 | 542 |
| `αμην` | `λευι` | Levi | 12/12/12/12 | 547 | 547 |
| `αμην` | `σαλα` | Shelah | 12/12/12/12 | 547 | 547 |
| `αμην` | `λουδ` | Lud | 10/10/10/15 | 550 | 550 |
| `αμην` | `ελαμ` | Elam | 11/10/11/10 | 553 | 553 |
| `αμην` | `αδαμ` | Adam | 7/7/7/8 | 566 | 566 |
| `αμην` | `οφισ` | Serpent | 6/6/6/7 | 570 | 570 |
| `αμην` | `εβερ` | Eber | 2/2/2/2 | 587 | 587 |
| `αμην` | `δαση` | Resen | 1/1/1/2 | 590 | 590 |
| `αμην` | `ελκη` | Boils | 1/1/1/1 | 591 | 591 |
| `αραμ` | `λεων` | Lion | 23/23/23/25 | 10 | 10 |
| `αραμ` | `σαρξ` | Flesh | 27/27/27/26 | 23 | 23 |
| `αραμ` | `ρωμη` | Rome | 18/12/12/11 | 31 | 31 |
| `αραμ` | `λευι` | Levi | 12/12/12/12 | 36 | 36 |
| `αραμ` | `σαλα` | Shelah | 12/12/12/12 | 36 | 36 |
| `αραμ` | `λουδ` | Lud | 10/10/10/15 | 39 | 39 |
| `αραμ` | `ελαμ` | Elam | 11/10/11/10 | 42 | 42 |
| `αραμ` | `οργη` | Wrath | 34/34/34/34 | 52 | 52 |
| `αραμ` | `αδαμ` | Adam | 7/7/7/8 | 55 | 55 |
| `αραμ` | `οφισ` | Serpent | 6/6/6/7 | 59 | 59 |
| `αραμ` | `εβερ` | Eber | 2/2/2/2 | 76 | 76 |
| `αραμ` | `δαση` | Resen | 1/1/1/2 | 79 | 79 |
| `αραμ` | `ελκη` | Boils | 1/1/1/1 | 80 | 80 |
| `αραμ` | `ψυχη` | Soul | 69/69/69/67 | 190 | 190 |
| `ασηρ` | `αδαμ` | Adam | 7/7/7/8 | 1 | 1 |
| `ασηρ` | `οφισ` | Serpent | 6/6/6/7 | 3 | 3 |
| `ασηρ` | `ελαμ` | Elam | 11/10/11/10 | 14 | 14 |
| `ασηρ` | `λουδ` | Lud | 10/10/10/15 | 17 | 17 |
| `ασηρ` | `εβερ` | Eber | 2/2/2/2 | 20 | 20 |
| `ασηρ` | `λευι` | Levi | 12/12/12/12 | 20 | 20 |
| `ασηρ` | `σαλα` | Shelah | 12/12/12/12 | 20 | 20 |
| `ασηρ` | `δαση` | Resen | 1/1/1/2 | 23 | 23 |
| `ασηρ` | `ελκη` | Boils | 1/1/1/1 | 24 | 24 |
| `ασηρ` | `ρωμη` | Rome | 18/12/12/11 | 25 | 25 |
| `ασηρ` | `λεων` | Lion | 23/23/23/25 | 66 | 66 |
| `ασηρ` | `σαρξ` | Flesh | 27/27/27/26 | 79 | 79 |
| `ασηρ` | `οργη` | Wrath | 34/34/34/34 | 108 | 108 |
| `ασηρ` | `ψυχη` | Soul | 69/69/69/67 | 246 | 246 |
| `χουσ` | `ψυχη` | Soul | 69/69/69/67 | 152 | 152 |
| `χουσ` | `οργη` | Wrath | 34/34/34/34 | 290 | 290 |
| `χουσ` | `σαρξ` | Flesh | 27/27/27/26 | 319 | 319 |
| `χουσ` | `λεων` | Lion | 23/23/23/25 | 332 | 332 |
| `χουσ` | `ρωμη` | Rome | 18/12/12/11 | 373 | 373 |
| `χουσ` | `λευι` | Levi | 12/12/12/12 | 378 | 378 |
| `χουσ` | `σαλα` | Shelah | 12/12/12/12 | 378 | 378 |
| `χουσ` | `λουδ` | Lud | 10/10/10/15 | 381 | 381 |
| `χουσ` | `ελαμ` | Elam | 11/10/11/10 | 384 | 384 |
| `χουσ` | `αδαμ` | Adam | 7/7/7/8 | 397 | 397 |
| `χουσ` | `οφισ` | Serpent | 6/6/6/7 | 401 | 401 |
| `χουσ` | `εβερ` | Eber | 2/2/2/2 | 418 | 418 |
| `χουσ` | `δαση` | Resen | 1/1/1/2 | 421 | 421 |
| `χουσ` | `ελκη` | Boils | 1/1/1/1 | 422 | 422 |
| `δασα` | `σαρξ` | Flesh | 27/27/27/26 | 3 | 3 |
| `δασα` | `λεων` | Lion | 23/23/23/25 | 16 | 16 |
| `δασα` | `οργη` | Wrath | 34/34/34/34 | 26 | 26 |
| `δασα` | `ρωμη` | Rome | 18/12/12/11 | 57 | 57 |
| `δασα` | `λευι` | Levi | 12/12/12/12 | 62 | 62 |
| `δασα` | `σαλα` | Shelah | 12/12/12/12 | 62 | 62 |
| `δασα` | `λουδ` | Lud | 10/10/10/15 | 65 | 65 |
| `δασα` | `ελαμ` | Elam | 11/10/11/10 | 68 | 68 |
| `δασα` | `αδαμ` | Adam | 7/7/7/8 | 81 | 81 |
| `δασα` | `οφισ` | Serpent | 6/6/6/7 | 85 | 85 |
| `δασα` | `εβερ` | Eber | 2/2/2/2 | 102 | 102 |
| `δασα` | `δαση` | Resen | 1/1/1/2 | 105 | 105 |
| `δασα` | `ελκη` | Boils | 1/1/1/1 | 106 | 106 |
| `δασα` | `ψυχη` | Soul | 69/69/69/67 | 164 | 164 |
| `σαβα` | `ελαμ` | Elam | 11/10/11/10 | 7 | 7 |
| `σαβα` | `αδαμ` | Adam | 7/7/7/8 | 6 | 8 |
| `σαβα` | `λουδ` | Lud | 10/10/10/15 | 10 | 10 |
| `σαβα` | `οφισ` | Serpent | 6/6/6/7 | 10 | 10 |
| `σαβα` | `λευι` | Levi | 12/12/12/12 | 13 | 13 |
| `σαβα` | `σαλα` | Shelah | 12/12/12/12 | 13 | 13 |
| `σαβα` | `ρωμη` | Rome | 18/12/12/11 | 18 | 18 |
| `σαβα` | `εβερ` | Eber | 2/2/2/2 | 27 | 27 |
| `σαβα` | `δαση` | Resen | 1/1/1/2 | 30 | 30 |
| `σαβα` | `ελκη` | Boils | 1/1/1/1 | 31 | 31 |
| `σαβα` | `λεων` | Lion | 23/23/23/25 | 59 | 59 |
| `σαβα` | `σαρξ` | Flesh | 27/27/27/26 | 72 | 72 |
| `σαβα` | `οργη` | Wrath | 34/34/34/34 | 101 | 101 |
| `σαβα` | `ψυχη` | Soul | 69/69/69/67 | 239 | 239 |
| `σιων` | `σαρξ` | Flesh | 27/27/27/26 | 12 | 12 |
| `σιων` | `οργη` | Wrath | 34/34/34/34 | 17 | 17 |
| `σιων` | `λεων` | Lion | 23/23/23/25 | 25 | 25 |
| `σιων` | `ρωμη` | Rome | 18/12/12/11 | 66 | 66 |
| `σιων` | `λευι` | Levi | 12/12/12/12 | 71 | 71 |
| `σιων` | `σαλα` | Shelah | 12/12/12/12 | 71 | 71 |
| `σιων` | `λουδ` | Lud | 10/10/10/15 | 74 | 74 |
| `σιων` | `ελαμ` | Elam | 11/10/11/10 | 77 | 77 |
| `σιων` | `αδαμ` | Adam | 7/7/7/8 | 90 | 90 |
| `σιων` | `οφισ` | Serpent | 6/6/6/7 | 94 | 94 |
| `σιων` | `εβερ` | Eber | 2/2/2/2 | 111 | 111 |
| `σιων` | `δαση` | Resen | 1/1/1/2 | 114 | 114 |
| `σιων` | `ελκη` | Boils | 1/1/1/1 | 115 | 115 |
| `σιων` | `ψυχη` | Soul | 69/69/69/67 | 155 | 155 |

## Read

This is a control-pool report, not a significance test. It uses the same
normalized substring rule as the current surface-context path and avoids
the bad control design of comparing surface-context rows against random
strings. The next step can freeze one matched-control set per target and
then run the ELS exact-center surface statistic against those real-word
controls.
