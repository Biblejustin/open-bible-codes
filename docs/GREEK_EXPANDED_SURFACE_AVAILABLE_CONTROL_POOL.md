# Greek Expanded Surface Available Control Pool

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
- matched controls per target requested: 999

## Selected Targets

| Term | Concept | Length | Surface verse vector | Sum | Controls found |
| --- | --- | ---: | --- | ---: | ---: |
| `τερασ` | Wonder | 5 | 46/43/43/42 | 174 | 32 |
| `ισαακ` | Isaac | 5 | 18/18/18/18 | 72 | 32 |
| `ανομια` | Lawlessness | 6 | 12/12/12/13 | 49 | 30 |

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
| `ισαακ` | `ελισα` | Elishah | 27/28/28/28 | 39 | 39 |
| `ισαακ` | `νυμφη` | Bride | 7/7/7/7 | 44 | 44 |
| `ισαακ` | `λιμοσ` | Famine | 7/7/7/7 | 44 | 44 |
| `ισαακ` | `εικων` | Image | 6/6/6/6 | 48 | 48 |
| `ισαακ` | `πληγη` | Plague | 6/6/6/6 | 48 | 48 |
| `ισαακ` | `αστηρ` | Star | 30/30/30/30 | 48 | 48 |
| `ισαακ` | `κερασ` | Horn | 4/4/4/5 | 55 | 55 |
| `ισαακ` | `φρεαρ` | Pit | 4/4/4/4 | 56 | 56 |
| `ισαακ` | `σαρρα` | Sarah | 4/4/4/4 | 56 | 56 |
| `ισαακ` | `ληνοσ` | Winepress | 4/4/4/4 | 56 | 56 |
| `ισαακ` | `ιωσηφ` | Joseph | 34/34/34/34 | 64 | 64 |
| `ισαακ` | `γαζαν` | Gaza | 1/1/1/1 | 68 | 68 |
| `ισαακ` | `ιαφεθ` | Japheth | 1/1/1/1 | 68 | 68 |
| `ισαακ` | `ιαραχ` | Jerah | 1/1/1/1 | 68 | 68 |
| `ισαακ` | `μαγωγ` | Magog | 1/1/1/1 | 68 | 68 |
| `ισαακ` | `ταφοσ` | Tomb | 1/1/1/1 | 68 | 68 |
| `ισαακ` | `τυροσ` | Tyre | 1/1/1/1 | 68 | 68 |
| `ισαακ` | `αζυμα` | Unleavened Bread | 1/1/1/1 | 68 | 68 |
| `ισαακ` | `νομοσ` | Law | 45/45/45/45 | 108 | 108 |
| `ισαακ` | `μαρια` | Mary | 46/46/46/46 | 112 | 112 |
| `ισαακ` | `ιακωβ` | Jacob | 63/63/63/63 | 180 | 180 |
| `ισαακ` | `ιουδα` | Judah | 277/277/277/274 | 1033 | 1033 |
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
| `ανομια` | `ωσαννα` | Hosanna | 5/6/6/6 | 26 | 26 |
| `ανομια` | `καπνοσ` | Smoke | 5/5/5/5 | 29 | 29 |
| `ανομια` | `βεροια` | Berea | 3/3/3/3 | 37 | 37 |
| `ανομια` | `χαλαζα` | Hail | 3/3/3/3 | 37 | 37 |
| `ανομια` | `νινευι` | Nineveh | 3/3/3/3 | 37 | 37 |
| `ανομια` | `σοδομα` | Sodom | 3/3/3/3 | 37 | 37 |
| `ανομια` | `χανααν` | Canaan | 2/2/2/2 | 41 | 41 |
| `ανομια` | `δανιηλ` | Daniel | 2/2/2/1 | 42 | 42 |
| `ανομια` | `μωυσησ` | Moses | 2/13/15/42 | 23 | 43 |
| `ανομια` | `εφραιμ` | Ephraim | 1/1/1/1 | 45 | 45 |
| `ανομια` | `ιωσιασ` | Josiah | 1/1/1/1 | 45 | 45 |
| `ανομια` | `ανεστη` | He Is Risen | 24/24/24/23 | 46 | 46 |
| `ανομια` | `ιουδασ` | Judas | 24/24/24/24 | 47 | 47 |
| `ανομια` | `ηρωδησ` | Herod | 25/25/25/24 | 50 | 50 |
| `ανομια` | `απαρχη` | Firstfruits | 27/27/27/27 | 59 | 59 |
| `ανομια` | `αβρααμ` | Abraham | 69/69/69/69 | 227 | 227 |
| `ανομια` | `ισραηλ` | Israel | 77/76/76/75 | 255 | 255 |
| `ανομια` | `παυλοσ` | Paul | 81/80/80/79 | 271 | 271 |
| `ανομια` | `πετροσ` | Peter | 104/103/103/100 | 361 | 361 |
| `ανομια` | `καρδια` | Heart | 151/150/150/148 | 550 | 550 |
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
| `τερασ` | `ηλιασ` | Elijah | 17/17/17/16 | 107 | 107 |
| `τερασ` | `χαραν` | Haran | 14/13/13/14 | 120 | 120 |
| `τερασ` | `γατερ` | Gether | 13/13/13/10 | 125 | 125 |
| `τερασ` | `τιτοσ` | Titus | 14/8/14/8 | 130 | 130 |
| `τερασ` | `ακρισ` | Locust | 11/11/11/10 | 131 | 131 |
| `τερασ` | `μηδια` | Media | 9/9/9/9 | 138 | 138 |
| `τερασ` | `νυμφη` | Bride | 7/7/7/7 | 146 | 146 |
| `τερασ` | `λιμοσ` | Famine | 7/7/7/7 | 146 | 146 |
| `τερασ` | `εικων` | Image | 6/6/6/6 | 150 | 150 |
| `τερασ` | `πληγη` | Plague | 6/6/6/6 | 150 | 150 |
| `τερασ` | `κερασ` | Horn | 4/4/4/5 | 157 | 157 |
| `τερασ` | `φρεαρ` | Pit | 4/4/4/4 | 158 | 158 |
| `τερασ` | `σαρρα` | Sarah | 4/4/4/4 | 158 | 158 |
| `τερασ` | `ληνοσ` | Winepress | 4/4/4/4 | 158 | 158 |
| `τερασ` | `γαζαν` | Gaza | 1/1/1/1 | 170 | 170 |
| `τερασ` | `ιαφεθ` | Japheth | 1/1/1/1 | 170 | 170 |
| `τερασ` | `ιαραχ` | Jerah | 1/1/1/1 | 170 | 170 |
| `τερασ` | `μαγωγ` | Magog | 1/1/1/1 | 170 | 170 |
| `τερασ` | `ταφοσ` | Tomb | 1/1/1/1 | 170 | 170 |
| `τερασ` | `τυροσ` | Tyre | 1/1/1/1 | 170 | 170 |
| `τερασ` | `αζυμα` | Unleavened Bread | 1/1/1/1 | 170 | 170 |
| `τερασ` | `ιουδα` | Judah | 277/277/277/274 | 931 | 931 |

## Read

This is a control-pool report, not a significance test. It uses the same
normalized substring rule as the current surface-context path and avoids
the bad control design of comparing surface-context rows against random
strings. The next step can freeze one matched-control set per target and
then run the ELS exact-center surface statistic against those real-word
controls.
