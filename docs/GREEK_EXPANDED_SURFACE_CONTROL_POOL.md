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
| `τερασ` | Wonder | 5 | 46/43/43/42 | 174 | 10 |
| `ισαακ` | Isaac | 5 | 18/18/18/18 | 72 | 10 |
| `ανομια` | Lawlessness | 6 | 12/12/12/13 | 49 | 10 |

## Closest Controls

| Target | Control | Control concept | Surface vector | Sum delta | Vector delta |
| --- | --- | --- | --- | ---: | ---: |
| `ισαακ` | `ηλιασ` | Elijah | 17/17/17/16 | 5 | 5 |
| `ισαακ` | `χαραν` | Haran | 14/13/13/14 | 18 | 18 |
| `ισαακ` | `γατερ` | Gether | 13/13/13/10 | 23 | 23 |
| `ισαακ` | `σιδων` | Sidon | 25/25/25/21 | 24 | 24 |
| `ισαακ` | `βασαν` | Bashan | 25/25/25/24 | 27 | 27 |
| `ισαακ` | `κλεισ` | Key | 25/26/25/24 | 28 | 28 |
| `ισαακ` | `τιτοσ` | Titus | 14/8/14/8 | 28 | 28 |
| `ισαακ` | `ακρισ` | Locust | 11/11/11/10 | 29 | 29 |
| `ισαακ` | `μηδια` | Media | 9/9/9/9 | 36 | 36 |
| `ισαακ` | `πασχα` | Passover | 27/27/27/27 | 36 | 36 |
| `ανομια` | `σκοτοσ` | Darkness | 13/13/13/13 | 3 | 3 |
| `ανομια` | `μαρτυσ` | Witness | 11/11/11/11 | 5 | 5 |
| `ανομια` | `ησαιασ` | Isaiah | 10/10/10/10 | 9 | 9 |
| `ανομια` | `αθηναι` | Athens | 15/16/16/15 | 13 | 13 |
| `ανομια` | `λυχνια` | Lampstand | 9/9/9/9 | 13 | 13 |
| `ανομια` | `ελαιον` | Oil | 7/7/7/7 | 21 | 21 |
| `ανομια` | `συμεων` | Simeon | 7/7/7/7 | 21 | 21 |
| `ανομια` | `θλιψισ` | Tribulation | 7/7/7/7 | 21 | 21 |
| `ανομια` | `λυχνοσ` | Lamp | 6/6/6/6 | 25 | 25 |
| `ανομια` | `θρονοσ` | Throne | 6/6/6/6 | 25 | 25 |
| `τερασ` | `νομοσ` | Law | 45/45/45/45 | 6 | 8 |
| `τερασ` | `μαρια` | Mary | 46/46/46/46 | 10 | 10 |
| `τερασ` | `ιωσηφ` | Joseph | 34/34/34/34 | 38 | 38 |
| `τερασ` | `αστηρ` | Star | 30/30/30/30 | 54 | 54 |
| `τερασ` | `ελισα` | Elishah | 27/28/28/28 | 63 | 63 |
| `τερασ` | `πασχα` | Passover | 27/27/27/27 | 66 | 66 |
| `τερασ` | `κλεισ` | Key | 25/26/25/24 | 74 | 74 |
| `τερασ` | `βασαν` | Bashan | 25/25/25/24 | 75 | 75 |
| `τερασ` | `ιακωβ` | Jacob | 63/63/63/63 | 78 | 78 |
| `τερασ` | `σιδων` | Sidon | 25/25/25/21 | 78 | 78 |

## Read

This is a control-pool report, not a significance test. It uses the same
normalized substring rule as the current surface-context path and avoids
the bad control design of comparing surface-context rows against random
strings. The next step can freeze one matched-control set per target and
then run the ELS exact-center surface statistic against those real-word
controls.
