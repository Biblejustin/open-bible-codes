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
| `τερασ` (teras; English: Wonder) | Wonder | 5 | 46/43/43/42 | 174 | 32 |
| `ισαακ` (Isaak; English: Isaac) | Isaac | 5 | 18/18/18/18 | 72 | 32 |
| `ανομια` (anomia; English: Lawlessness) | Lawlessness | 6 | 12/12/12/13 | 49 | 30 |

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
| `ισαακ` (Isaak; English: Isaac) | `ελισα` (Elisa; English: Elishah) | Elishah | 27/28/28/28 | 39 | 39 |
| `ισαακ` (Isaak; English: Isaac) | `νυμφη` (numphe; English: Bride) | Bride | 7/7/7/7 | 44 | 44 |
| `ισαακ` (Isaak; English: Isaac) | `λιμοσ` (limos; English: Famine) | Famine | 7/7/7/7 | 44 | 44 |
| `ισαακ` (Isaak; English: Isaac) | `εικων` (eikon; English: Image) | Image | 6/6/6/6 | 48 | 48 |
| `ισαακ` (Isaak; English: Isaac) | `πληγη` (plege; English: Plague) | Plague | 6/6/6/6 | 48 | 48 |
| `ισαακ` (Isaak; English: Isaac) | `αστηρ` (aster; English: Star) | Star | 30/30/30/30 | 48 | 48 |
| `ισαακ` (Isaak; English: Isaac) | `κερασ` (keras; English: Horn) | Horn | 4/4/4/5 | 55 | 55 |
| `ισαακ` (Isaak; English: Isaac) | `φρεαρ` (phrear; English: Pit) | Pit | 4/4/4/4 | 56 | 56 |
| `ισαακ` (Isaak; English: Isaac) | `σαρρα` (sarra; English: Sarah) | Sarah | 4/4/4/4 | 56 | 56 |
| `ισαακ` (Isaak; English: Isaac) | `ληνοσ` (lenos; English: Winepress) | Winepress | 4/4/4/4 | 56 | 56 |
| `ισαακ` (Isaak; English: Isaac) | `ιωσηφ` (ioseph; English: Joseph) | Joseph | 34/34/34/34 | 64 | 64 |
| `ισαακ` (Isaak; English: Isaac) | `γαζαν` (gazan; English: Gaza) | Gaza | 1/1/1/1 | 68 | 68 |
| `ισαακ` (Isaak; English: Isaac) | `ιαφεθ` (iapheth; English: Japheth) | Japheth | 1/1/1/1 | 68 | 68 |
| `ισαακ` (Isaak; English: Isaac) | `ιαραχ` (iarach; English: Jerah) | Jerah | 1/1/1/1 | 68 | 68 |
| `ισαακ` (Isaak; English: Isaac) | `μαγωγ` (magog; English: Magog) | Magog | 1/1/1/1 | 68 | 68 |
| `ισαακ` (Isaak; English: Isaac) | `ταφοσ` (taphos; English: Tomb) | Tomb | 1/1/1/1 | 68 | 68 |
| `ισαακ` (Isaak; English: Isaac) | `τυροσ` (turos; English: Tyre) | Tyre | 1/1/1/1 | 68 | 68 |
| `ισαακ` (Isaak; English: Isaac) | `αζυμα` (azuma; English: Unleavened Bread) | Unleavened Bread | 1/1/1/1 | 68 | 68 |
| `ισαακ` (Isaak; English: Isaac) | `νομοσ` (nomos; English: Law) | Law | 45/45/45/45 | 108 | 108 |
| `ισαακ` (Isaak; English: Isaac) | `μαρια` (Maria; English: Mary) | Mary | 46/46/46/46 | 112 | 112 |
| `ισαακ` (Isaak; English: Isaac) | `ιακωβ` (iakob; English: Jacob) | Jacob | 63/63/63/63 | 180 | 180 |
| `ισαακ` (Isaak; English: Isaac) | `ιουδα` (iouda; English: Judah) | Judah | 277/277/277/274 | 1033 | 1033 |
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
| `ανομια` (anomia; English: Lawlessness) | `ωσαννα` (osanna; English: Hosanna) | Hosanna | 5/6/6/6 | 26 | 26 |
| `ανομια` (anomia; English: Lawlessness) | `καπνοσ` (kapnos; English: Smoke) | Smoke | 5/5/5/5 | 29 | 29 |
| `ανομια` (anomia; English: Lawlessness) | `βεροια` (beroia; English: Berea) | Berea | 3/3/3/3 | 37 | 37 |
| `ανομια` (anomia; English: Lawlessness) | `χαλαζα` (chalaza; English: Hail) | Hail | 3/3/3/3 | 37 | 37 |
| `ανομια` (anomia; English: Lawlessness) | `νινευι` (nineui; English: Nineveh) | Nineveh | 3/3/3/3 | 37 | 37 |
| `ανομια` (anomia; English: Lawlessness) | `σοδομα` (sodoma; English: Sodom) | Sodom | 3/3/3/3 | 37 | 37 |
| `ανομια` (anomia; English: Lawlessness) | `χανααν` (chanaan; English: Canaan) | Canaan | 2/2/2/2 | 41 | 41 |
| `ανομια` (anomia; English: Lawlessness) | `δανιηλ` (daniel; English: Daniel) | Daniel | 2/2/2/1 | 42 | 42 |
| `ανομια` (anomia; English: Lawlessness) | `μωυσησ` (mouses; English: Moses) | Moses | 2/13/15/42 | 23 | 43 |
| `ανομια` (anomia; English: Lawlessness) | `εφραιμ` (ephraim; English: Ephraim) | Ephraim | 1/1/1/1 | 45 | 45 |
| `ανομια` (anomia; English: Lawlessness) | `ιωσιασ` (iosias; English: Josiah) | Josiah | 1/1/1/1 | 45 | 45 |
| `ανομια` (anomia; English: Lawlessness) | `ανεστη` (aneste; English: He Is Risen) | He Is Risen | 24/24/24/23 | 46 | 46 |
| `ανομια` (anomia; English: Lawlessness) | `ιουδασ` (Ioudas; English: Judas) | Judas | 24/24/24/24 | 47 | 47 |
| `ανομια` (anomia; English: Lawlessness) | `ηρωδησ` (erodes; English: Herod) | Herod | 25/25/25/24 | 50 | 50 |
| `ανομια` (anomia; English: Lawlessness) | `απαρχη` (aparche; English: Firstfruits) | Firstfruits | 27/27/27/27 | 59 | 59 |
| `ανομια` (anomia; English: Lawlessness) | `αβρααμ` (abraam; English: Abraham) | Abraham | 69/69/69/69 | 227 | 227 |
| `ανομια` (anomia; English: Lawlessness) | `ισραηλ` (israel; English: Israel) | Israel | 77/76/76/75 | 255 | 255 |
| `ανομια` (anomia; English: Lawlessness) | `παυλοσ` (paulos; English: Paul) | Paul | 81/80/80/79 | 271 | 271 |
| `ανομια` (anomia; English: Lawlessness) | `πετροσ` (Petros; English: Peter) | Peter | 104/103/103/100 | 361 | 361 |
| `ανομια` (anomia; English: Lawlessness) | `καρδια` (kardia; English: Heart) | Heart | 151/150/150/148 | 550 | 550 |
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
| `τερασ` (teras; English: Wonder) | `ηλιασ` (elias; English: Elijah) | Elijah | 17/17/17/16 | 107 | 107 |
| `τερασ` (teras; English: Wonder) | `χαραν` (charan; English: Haran) | Haran | 14/13/13/14 | 120 | 120 |
| `τερασ` (teras; English: Wonder) | `γατερ` (gater; English: Gether) | Gether | 13/13/13/10 | 125 | 125 |
| `τερασ` (teras; English: Wonder) | `τιτοσ` (titos; English: Titus) | Titus | 14/8/14/8 | 130 | 130 |
| `τερασ` (teras; English: Wonder) | `ακρισ` (akris; English: Locust) | Locust | 11/11/11/10 | 131 | 131 |
| `τερασ` (teras; English: Wonder) | `μηδια` (media; English: Media) | Media | 9/9/9/9 | 138 | 138 |
| `τερασ` (teras; English: Wonder) | `νυμφη` (numphe; English: Bride) | Bride | 7/7/7/7 | 146 | 146 |
| `τερασ` (teras; English: Wonder) | `λιμοσ` (limos; English: Famine) | Famine | 7/7/7/7 | 146 | 146 |
| `τερασ` (teras; English: Wonder) | `εικων` (eikon; English: Image) | Image | 6/6/6/6 | 150 | 150 |
| `τερασ` (teras; English: Wonder) | `πληγη` (plege; English: Plague) | Plague | 6/6/6/6 | 150 | 150 |
| `τερασ` (teras; English: Wonder) | `κερασ` (keras; English: Horn) | Horn | 4/4/4/5 | 157 | 157 |
| `τερασ` (teras; English: Wonder) | `φρεαρ` (phrear; English: Pit) | Pit | 4/4/4/4 | 158 | 158 |
| `τερασ` (teras; English: Wonder) | `σαρρα` (sarra; English: Sarah) | Sarah | 4/4/4/4 | 158 | 158 |
| `τερασ` (teras; English: Wonder) | `ληνοσ` (lenos; English: Winepress) | Winepress | 4/4/4/4 | 158 | 158 |
| `τερασ` (teras; English: Wonder) | `γαζαν` (gazan; English: Gaza) | Gaza | 1/1/1/1 | 170 | 170 |
| `τερασ` (teras; English: Wonder) | `ιαφεθ` (iapheth; English: Japheth) | Japheth | 1/1/1/1 | 170 | 170 |
| `τερασ` (teras; English: Wonder) | `ιαραχ` (iarach; English: Jerah) | Jerah | 1/1/1/1 | 170 | 170 |
| `τερασ` (teras; English: Wonder) | `μαγωγ` (magog; English: Magog) | Magog | 1/1/1/1 | 170 | 170 |
| `τερασ` (teras; English: Wonder) | `ταφοσ` (taphos; English: Tomb) | Tomb | 1/1/1/1 | 170 | 170 |
| `τερασ` (teras; English: Wonder) | `τυροσ` (turos; English: Tyre) | Tyre | 1/1/1/1 | 170 | 170 |
| `τερασ` (teras; English: Wonder) | `αζυμα` (azuma; English: Unleavened Bread) | Unleavened Bread | 1/1/1/1 | 170 | 170 |
| `τερασ` (teras; English: Wonder) | `ιουδα` (iouda; English: Judah) | Judah | 277/277/277/274 | 931 | 931 |

## Read

This is a control-pool report, not a significance test. It uses the same
normalized substring rule as the current surface-context path and avoids
the bad control design of comparing surface-context rows against random
strings. The next step can freeze one matched-control set per target and
then run the ELS exact-center surface statistic against those real-word
controls.
