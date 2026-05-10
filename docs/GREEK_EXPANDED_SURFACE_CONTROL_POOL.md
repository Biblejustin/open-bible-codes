# Greek Expanded Surface Control Pool

Status: real-word control-pool construction; no ELS control statistic yet.

This report prepares fair controls for the tighter expanded Greek surface
triage. It counts normalized surface-substring verse frequency for every
term in the expanded Greek prospective list, then selects same-length real
Greek terms with the closest surface-frequency vectors across TR_NT,
BYZ_NT, TCG_NT, and SBLGNT.
Selected target terms are excluded from the control candidate pool.

## Inputs

- Terms: `terms/greek_expanded_prospective_terms.csv`
- Selected triage rows: `reports/greek_expanded_surface_triage/selected_patterns.csv`

## Surface-Frequency Scope

- terms measured: 291
- all-source surface-present terms: 165
- selected targets: 3
- matched controls per target requested: 10

## Selected Targets

| Term | Concept | Length | Surface verse vector | Sum | Controls found |
| --- | --- | ---: | --- | ---: | ---: |
| `τερασ` (teras; English: Wonder) | Wonder | 5 | 46/43/43/42 | 174 | 10 |
| `ισαακ` (Isaak; English: Isaac) | Isaac | 5 | 18/18/18/18 | 72 | 10 |
| `ανομια` (anomia; English: Lawlessness) | Lawlessness | 6 | 12/12/12/13 | 49 | 10 |

## Closest Controls

| Target | Control | Control concept | Surface vector | Sum delta | Vector delta |
| --- | --- | --- | --- | ---: | ---: |
| `ισαακ` (Isaak; English: Isaac) | `ηλιασ` (elias; English: Elijah) | Elijah | 17/17/17/16 | 5 | 5 |
| `ισαακ` (Isaak; English: Isaac) | `χαραν` (charan; English: Haran) | Haran | 14/13/13/14 | 18 | 18 |
| `ισαακ` (Isaak; English: Isaac) | `γατερ` (gater; English: Gether) | Gether | 13/13/13/10 | 23 | 23 |
| `ισαακ` (Isaak; English: Isaac) | `σιδων` (sidon; English: Sidon) | Sidon | 25/25/25/21 | 24 | 24 |
| `ισαακ` (Isaak; English: Isaac) | `βασαν` (basan; English: Bashan) | Bashan | 25/25/25/24 | 27 | 27 |
| `ισαακ` (Isaak; English: Isaac) | `κλεισ` (kleis; English: Key) | Key | 25/26/25/24 | 28 | 28 |
| `ισαακ` (Isaak; English: Isaac) | `τιτοσ` (titos; English: Titus) | Titus | 14/8/14/8 | 28 | 28 |
| `ισαακ` (Isaak; English: Isaac) | `ακρισ` (akris; English: Locust) | Locust | 11/11/11/10 | 29 | 29 |
| `ισαακ` (Isaak; English: Isaac) | `μηδια` (media; English: Media) | Media | 9/9/9/9 | 36 | 36 |
| `ισαακ` (Isaak; English: Isaac) | `πασχα` (pascha; English: Passover) | Passover | 27/27/27/27 | 36 | 36 |
| `ανομια` (anomia; English: Lawlessness) | `σκοτοσ` (skotos; English: Darkness) | Darkness | 13/13/13/13 | 3 | 3 |
| `ανομια` (anomia; English: Lawlessness) | `μαρτυσ` (martus; English: Witness) | Witness | 11/11/11/11 | 5 | 5 |
| `ανομια` (anomia; English: Lawlessness) | `ησαιασ` (esaias; English: Isaiah) | Isaiah | 10/10/10/10 | 9 | 9 |
| `ανομια` (anomia; English: Lawlessness) | `αθηναι` (athenai; English: Athens) | Athens | 15/16/16/15 | 13 | 13 |
| `ανομια` (anomia; English: Lawlessness) | `λυχνια` (luchnia; English: Lampstand) | Lampstand | 9/9/9/9 | 13 | 13 |
| `ανομια` (anomia; English: Lawlessness) | `ελαιον` (elaion; English: Oil) | Oil | 7/7/7/7 | 21 | 21 |
| `ανομια` (anomia; English: Lawlessness) | `συμεων` (sumeon; English: Simeon) | Simeon | 7/7/7/7 | 21 | 21 |
| `ανομια` (anomia; English: Lawlessness) | `θλιψισ` (thlipsis; English: Tribulation) | Tribulation | 7/7/7/7 | 21 | 21 |
| `ανομια` (anomia; English: Lawlessness) | `λυχνοσ` (luchnos; English: Lamp) | Lamp | 6/6/6/6 | 25 | 25 |
| `ανομια` (anomia; English: Lawlessness) | `θρονοσ` (thronos; English: Throne) | Throne | 6/6/6/6 | 25 | 25 |
| `τερασ` (teras; English: Wonder) | `νομοσ` (nomos; English: Law) | Law | 45/45/45/45 | 6 | 8 |
| `τερασ` (teras; English: Wonder) | `μαρια` (Maria; English: Mary) | Mary | 46/46/46/46 | 10 | 10 |
| `τερασ` (teras; English: Wonder) | `ιωσηφ` (ioseph; English: Joseph) | Joseph | 34/34/34/34 | 38 | 38 |
| `τερασ` (teras; English: Wonder) | `αστηρ` (aster; English: Star) | Star | 30/30/30/30 | 54 | 54 |
| `τερασ` (teras; English: Wonder) | `ελισα` (Elisa; English: Elishah) | Elishah | 27/28/28/28 | 63 | 63 |
| `τερασ` (teras; English: Wonder) | `πασχα` (pascha; English: Passover) | Passover | 27/27/27/27 | 66 | 66 |
| `τερασ` (teras; English: Wonder) | `κλεισ` (kleis; English: Key) | Key | 25/26/25/24 | 74 | 74 |
| `τερασ` (teras; English: Wonder) | `βασαν` (basan; English: Bashan) | Bashan | 25/25/25/24 | 75 | 75 |
| `τερασ` (teras; English: Wonder) | `ιακωβ` (iakob; English: Jacob) | Jacob | 63/63/63/63 | 78 | 78 |
| `τερασ` (teras; English: Wonder) | `σιδων` (sidon; English: Sidon) | Sidon | 25/25/25/21 | 78 | 78 |

## Read

This is a control-pool report, not a significance test. It uses the same
normalized substring rule as the current surface-context path and avoids
the bad control design of comparing surface-context rows against random
strings. The next step can freeze one matched-control set per target and
then run the ELS exact-center surface statistic against those real-word
controls.
