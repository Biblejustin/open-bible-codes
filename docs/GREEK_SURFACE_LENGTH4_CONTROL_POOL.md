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
| `αμην` (amen; English: Amen) | Amen | 4 | 155/155/155/130 | 595 | 14 |
| `χουσ` (chous; English: Cush) | Cush | 4 | 107/107/106/106 | 426 | 14 |
| `σιων` (Sion; English: Zion) | Zion | 4 | 31/30/30/28 | 119 | 14 |
| `δασα` (dasa; English: Lasha) | Lasha | 4 | 28/28/28/26 | 110 | 14 |
| `αραμ` (aram; English: Aram) | Aram | 4 | 21/22/22/19 | 84 | 14 |
| `σαβα` (saba; English: Seba) | Seba | 4 | 10/9/9/7 | 35 | 14 |
| `ασηρ` (aser; English: Asher) | Asher | 4 | 7/7/7/7 | 28 | 14 |

## Closest Controls

| Target | Control | Control concept | Surface vector | Sum delta | Vector delta |
| --- | --- | --- | --- | ---: | ---: |
| `αμην` (amen; English: Amen) | `ψυχη` (psuche; English: Soul) | Soul | 69/69/69/67 | 321 | 321 |
| `αμην` (amen; English: Amen) | `οργη` (orge; English: Wrath) | Wrath | 34/34/34/34 | 459 | 459 |
| `αμην` (amen; English: Amen) | `σαρξ` (sarx; English: Flesh) | Flesh | 27/27/27/26 | 488 | 488 |
| `αμην` (amen; English: Amen) | `λεων` (leon; English: Lion) | Lion | 23/23/23/25 | 501 | 501 |
| `αμην` (amen; English: Amen) | `ρωμη` (rome; English: Rome) | Rome | 18/12/12/11 | 542 | 542 |
| `αμην` (amen; English: Amen) | `λευι` (leui; English: Levi) | Levi | 12/12/12/12 | 547 | 547 |
| `αμην` (amen; English: Amen) | `σαλα` (Sala; English: Shelah) | Shelah | 12/12/12/12 | 547 | 547 |
| `αμην` (amen; English: Amen) | `λουδ` (loud; English: Lud) | Lud | 10/10/10/15 | 550 | 550 |
| `αμην` (amen; English: Amen) | `ελαμ` (Elam; English: Elam) | Elam | 11/10/11/10 | 553 | 553 |
| `αμην` (amen; English: Amen) | `αδαμ` (adam; English: Adam) | Adam | 7/7/7/8 | 566 | 566 |
| `αμην` (amen; English: Amen) | `οφισ` (ophis; English: Serpent) | Serpent | 6/6/6/7 | 570 | 570 |
| `αμην` (amen; English: Amen) | `εβερ` (eber; English: Eber) | Eber | 2/2/2/2 | 587 | 587 |
| `αμην` (amen; English: Amen) | `δαση` (dase; English: Resen) | Resen | 1/1/1/2 | 590 | 590 |
| `αμην` (amen; English: Amen) | `ελκη` (elke; English: Boils) | Boils | 1/1/1/1 | 591 | 591 |
| `αραμ` (aram; English: Aram) | `λεων` (leon; English: Lion) | Lion | 23/23/23/25 | 10 | 10 |
| `αραμ` (aram; English: Aram) | `σαρξ` (sarx; English: Flesh) | Flesh | 27/27/27/26 | 23 | 23 |
| `αραμ` (aram; English: Aram) | `ρωμη` (rome; English: Rome) | Rome | 18/12/12/11 | 31 | 31 |
| `αραμ` (aram; English: Aram) | `λευι` (leui; English: Levi) | Levi | 12/12/12/12 | 36 | 36 |
| `αραμ` (aram; English: Aram) | `σαλα` (Sala; English: Shelah) | Shelah | 12/12/12/12 | 36 | 36 |
| `αραμ` (aram; English: Aram) | `λουδ` (loud; English: Lud) | Lud | 10/10/10/15 | 39 | 39 |
| `αραμ` (aram; English: Aram) | `ελαμ` (Elam; English: Elam) | Elam | 11/10/11/10 | 42 | 42 |
| `αραμ` (aram; English: Aram) | `οργη` (orge; English: Wrath) | Wrath | 34/34/34/34 | 52 | 52 |
| `αραμ` (aram; English: Aram) | `αδαμ` (adam; English: Adam) | Adam | 7/7/7/8 | 55 | 55 |
| `αραμ` (aram; English: Aram) | `οφισ` (ophis; English: Serpent) | Serpent | 6/6/6/7 | 59 | 59 |
| `αραμ` (aram; English: Aram) | `εβερ` (eber; English: Eber) | Eber | 2/2/2/2 | 76 | 76 |
| `αραμ` (aram; English: Aram) | `δαση` (dase; English: Resen) | Resen | 1/1/1/2 | 79 | 79 |
| `αραμ` (aram; English: Aram) | `ελκη` (elke; English: Boils) | Boils | 1/1/1/1 | 80 | 80 |
| `αραμ` (aram; English: Aram) | `ψυχη` (psuche; English: Soul) | Soul | 69/69/69/67 | 190 | 190 |
| `ασηρ` (aser; English: Asher) | `αδαμ` (adam; English: Adam) | Adam | 7/7/7/8 | 1 | 1 |
| `ασηρ` (aser; English: Asher) | `οφισ` (ophis; English: Serpent) | Serpent | 6/6/6/7 | 3 | 3 |
| `ασηρ` (aser; English: Asher) | `ελαμ` (Elam; English: Elam) | Elam | 11/10/11/10 | 14 | 14 |
| `ασηρ` (aser; English: Asher) | `λουδ` (loud; English: Lud) | Lud | 10/10/10/15 | 17 | 17 |
| `ασηρ` (aser; English: Asher) | `εβερ` (eber; English: Eber) | Eber | 2/2/2/2 | 20 | 20 |
| `ασηρ` (aser; English: Asher) | `λευι` (leui; English: Levi) | Levi | 12/12/12/12 | 20 | 20 |
| `ασηρ` (aser; English: Asher) | `σαλα` (Sala; English: Shelah) | Shelah | 12/12/12/12 | 20 | 20 |
| `ασηρ` (aser; English: Asher) | `δαση` (dase; English: Resen) | Resen | 1/1/1/2 | 23 | 23 |
| `ασηρ` (aser; English: Asher) | `ελκη` (elke; English: Boils) | Boils | 1/1/1/1 | 24 | 24 |
| `ασηρ` (aser; English: Asher) | `ρωμη` (rome; English: Rome) | Rome | 18/12/12/11 | 25 | 25 |
| `ασηρ` (aser; English: Asher) | `λεων` (leon; English: Lion) | Lion | 23/23/23/25 | 66 | 66 |
| `ασηρ` (aser; English: Asher) | `σαρξ` (sarx; English: Flesh) | Flesh | 27/27/27/26 | 79 | 79 |
| `ασηρ` (aser; English: Asher) | `οργη` (orge; English: Wrath) | Wrath | 34/34/34/34 | 108 | 108 |
| `ασηρ` (aser; English: Asher) | `ψυχη` (psuche; English: Soul) | Soul | 69/69/69/67 | 246 | 246 |
| `χουσ` (chous; English: Cush) | `ψυχη` (psuche; English: Soul) | Soul | 69/69/69/67 | 152 | 152 |
| `χουσ` (chous; English: Cush) | `οργη` (orge; English: Wrath) | Wrath | 34/34/34/34 | 290 | 290 |
| `χουσ` (chous; English: Cush) | `σαρξ` (sarx; English: Flesh) | Flesh | 27/27/27/26 | 319 | 319 |
| `χουσ` (chous; English: Cush) | `λεων` (leon; English: Lion) | Lion | 23/23/23/25 | 332 | 332 |
| `χουσ` (chous; English: Cush) | `ρωμη` (rome; English: Rome) | Rome | 18/12/12/11 | 373 | 373 |
| `χουσ` (chous; English: Cush) | `λευι` (leui; English: Levi) | Levi | 12/12/12/12 | 378 | 378 |
| `χουσ` (chous; English: Cush) | `σαλα` (Sala; English: Shelah) | Shelah | 12/12/12/12 | 378 | 378 |
| `χουσ` (chous; English: Cush) | `λουδ` (loud; English: Lud) | Lud | 10/10/10/15 | 381 | 381 |
| `χουσ` (chous; English: Cush) | `ελαμ` (Elam; English: Elam) | Elam | 11/10/11/10 | 384 | 384 |
| `χουσ` (chous; English: Cush) | `αδαμ` (adam; English: Adam) | Adam | 7/7/7/8 | 397 | 397 |
| `χουσ` (chous; English: Cush) | `οφισ` (ophis; English: Serpent) | Serpent | 6/6/6/7 | 401 | 401 |
| `χουσ` (chous; English: Cush) | `εβερ` (eber; English: Eber) | Eber | 2/2/2/2 | 418 | 418 |
| `χουσ` (chous; English: Cush) | `δαση` (dase; English: Resen) | Resen | 1/1/1/2 | 421 | 421 |
| `χουσ` (chous; English: Cush) | `ελκη` (elke; English: Boils) | Boils | 1/1/1/1 | 422 | 422 |
| `δασα` (dasa; English: Lasha) | `σαρξ` (sarx; English: Flesh) | Flesh | 27/27/27/26 | 3 | 3 |
| `δασα` (dasa; English: Lasha) | `λεων` (leon; English: Lion) | Lion | 23/23/23/25 | 16 | 16 |
| `δασα` (dasa; English: Lasha) | `οργη` (orge; English: Wrath) | Wrath | 34/34/34/34 | 26 | 26 |
| `δασα` (dasa; English: Lasha) | `ρωμη` (rome; English: Rome) | Rome | 18/12/12/11 | 57 | 57 |
| `δασα` (dasa; English: Lasha) | `λευι` (leui; English: Levi) | Levi | 12/12/12/12 | 62 | 62 |
| `δασα` (dasa; English: Lasha) | `σαλα` (Sala; English: Shelah) | Shelah | 12/12/12/12 | 62 | 62 |
| `δασα` (dasa; English: Lasha) | `λουδ` (loud; English: Lud) | Lud | 10/10/10/15 | 65 | 65 |
| `δασα` (dasa; English: Lasha) | `ελαμ` (Elam; English: Elam) | Elam | 11/10/11/10 | 68 | 68 |
| `δασα` (dasa; English: Lasha) | `αδαμ` (adam; English: Adam) | Adam | 7/7/7/8 | 81 | 81 |
| `δασα` (dasa; English: Lasha) | `οφισ` (ophis; English: Serpent) | Serpent | 6/6/6/7 | 85 | 85 |
| `δασα` (dasa; English: Lasha) | `εβερ` (eber; English: Eber) | Eber | 2/2/2/2 | 102 | 102 |
| `δασα` (dasa; English: Lasha) | `δαση` (dase; English: Resen) | Resen | 1/1/1/2 | 105 | 105 |
| `δασα` (dasa; English: Lasha) | `ελκη` (elke; English: Boils) | Boils | 1/1/1/1 | 106 | 106 |
| `δασα` (dasa; English: Lasha) | `ψυχη` (psuche; English: Soul) | Soul | 69/69/69/67 | 164 | 164 |
| `σαβα` (saba; English: Seba) | `ελαμ` (Elam; English: Elam) | Elam | 11/10/11/10 | 7 | 7 |
| `σαβα` (saba; English: Seba) | `αδαμ` (adam; English: Adam) | Adam | 7/7/7/8 | 6 | 8 |
| `σαβα` (saba; English: Seba) | `λουδ` (loud; English: Lud) | Lud | 10/10/10/15 | 10 | 10 |
| `σαβα` (saba; English: Seba) | `οφισ` (ophis; English: Serpent) | Serpent | 6/6/6/7 | 10 | 10 |
| `σαβα` (saba; English: Seba) | `λευι` (leui; English: Levi) | Levi | 12/12/12/12 | 13 | 13 |
| `σαβα` (saba; English: Seba) | `σαλα` (Sala; English: Shelah) | Shelah | 12/12/12/12 | 13 | 13 |
| `σαβα` (saba; English: Seba) | `ρωμη` (rome; English: Rome) | Rome | 18/12/12/11 | 18 | 18 |
| `σαβα` (saba; English: Seba) | `εβερ` (eber; English: Eber) | Eber | 2/2/2/2 | 27 | 27 |
| `σαβα` (saba; English: Seba) | `δαση` (dase; English: Resen) | Resen | 1/1/1/2 | 30 | 30 |
| `σαβα` (saba; English: Seba) | `ελκη` (elke; English: Boils) | Boils | 1/1/1/1 | 31 | 31 |
| `σαβα` (saba; English: Seba) | `λεων` (leon; English: Lion) | Lion | 23/23/23/25 | 59 | 59 |
| `σαβα` (saba; English: Seba) | `σαρξ` (sarx; English: Flesh) | Flesh | 27/27/27/26 | 72 | 72 |
| `σαβα` (saba; English: Seba) | `οργη` (orge; English: Wrath) | Wrath | 34/34/34/34 | 101 | 101 |
| `σαβα` (saba; English: Seba) | `ψυχη` (psuche; English: Soul) | Soul | 69/69/69/67 | 239 | 239 |
| `σιων` (Sion; English: Zion) | `σαρξ` (sarx; English: Flesh) | Flesh | 27/27/27/26 | 12 | 12 |
| `σιων` (Sion; English: Zion) | `οργη` (orge; English: Wrath) | Wrath | 34/34/34/34 | 17 | 17 |
| `σιων` (Sion; English: Zion) | `λεων` (leon; English: Lion) | Lion | 23/23/23/25 | 25 | 25 |
| `σιων` (Sion; English: Zion) | `ρωμη` (rome; English: Rome) | Rome | 18/12/12/11 | 66 | 66 |
| `σιων` (Sion; English: Zion) | `λευι` (leui; English: Levi) | Levi | 12/12/12/12 | 71 | 71 |
| `σιων` (Sion; English: Zion) | `σαλα` (Sala; English: Shelah) | Shelah | 12/12/12/12 | 71 | 71 |
| `σιων` (Sion; English: Zion) | `λουδ` (loud; English: Lud) | Lud | 10/10/10/15 | 74 | 74 |
| `σιων` (Sion; English: Zion) | `ελαμ` (Elam; English: Elam) | Elam | 11/10/11/10 | 77 | 77 |
| `σιων` (Sion; English: Zion) | `αδαμ` (adam; English: Adam) | Adam | 7/7/7/8 | 90 | 90 |
| `σιων` (Sion; English: Zion) | `οφισ` (ophis; English: Serpent) | Serpent | 6/6/6/7 | 94 | 94 |
| `σιων` (Sion; English: Zion) | `εβερ` (eber; English: Eber) | Eber | 2/2/2/2 | 111 | 111 |
| `σιων` (Sion; English: Zion) | `δαση` (dase; English: Resen) | Resen | 1/1/1/2 | 114 | 114 |
| `σιων` (Sion; English: Zion) | `ελκη` (elke; English: Boils) | Boils | 1/1/1/1 | 115 | 115 |
| `σιων` (Sion; English: Zion) | `ψυχη` (psuche; English: Soul) | Soul | 69/69/69/67 | 155 | 155 |

## Read

This is a control-pool report, not a significance test. It uses the same
normalized substring rule as the current surface-context path and avoids
the bad control design of comparing surface-context rows against random
strings. The next step can freeze one matched-control set per target and
then run the ELS exact-center surface statistic against those real-word
controls.
