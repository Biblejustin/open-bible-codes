# Greek Surface Length-4 Vocabulary Control Pool

Status: real-word control-pool construction; no ELS control statistic yet.

This report prepares fair controls for the tighter expanded Greek surface
triage. It counts normalized surface-substring verse frequency for every
term in the expanded Greek prospective list, then selects same-length real
Greek terms with the closest surface-frequency vectors across TR_NT,
BYZ_NT, TCG_NT, and SBLGNT.
Selected target terms are excluded from the control candidate pool.

## Inputs

- Terms: `reports/greek_surface_length4_vocab_controls/terms.csv`
- Selected triage rows: `reports/greek_surface_length4_followup/selected_patterns.csv`

## Surface-Frequency Scope

- terms measured: 579
- all-source surface-present terms: 579
- selected targets: 7
- matched controls per target requested: 200

## Selected Targets

| Term | Concept | Length | Surface verse vector | Sum | Controls found |
| --- | --- | ---: | --- | ---: | ---: |
| `αμην` | Amen | 4 | 155/155/155/130 | 595 | 200 |
| `χουσ` | Cush | 4 | 107/107/106/106 | 426 | 200 |
| `σιων` | Zion | 4 | 31/30/30/28 | 119 | 200 |
| `δασα` | Lasha | 4 | 28/28/28/26 | 110 | 200 |
| `αραμ` | Aram | 4 | 21/22/22/19 | 84 | 200 |
| `σαβα` | Seba | 4 | 10/9/9/7 | 35 | 200 |
| `ασηρ` | Asher | 4 | 7/7/7/7 | 28 | 200 |

## Closest Controls

| Target | Control | Control concept | Surface vector | Sum delta | Vector delta |
| --- | --- | --- | --- | ---: | ---: |
| `αμην` | `ερει` | Surface vocabulary ερει | 155/155/155/152 | 22 | 22 |
| `αμην` | `υιοσ` | Surface vocabulary υιοσ | 155/156/156/151 | 23 | 23 |
| `αμην` | `ολου` | Surface vocabulary ολου | 154/152/152/149 | 12 | 26 |
| `αμην` | `εμοι` | Surface vocabulary εμοι | 161/141/161/134 | 2 | 30 |
| `αμην` | `δοξα` | Surface vocabulary δοξα | 150/150/150/147 | 2 | 32 |
| `αμην` | `ερισ` | Surface vocabulary ερισ | 152/152/152/153 | 14 | 32 |
| `αμην` | `μενω` | Surface vocabulary μενω | 150/149/149/147 | 0 | 34 |
| `αμην` | `θεον` | Surface vocabulary θεον | 151/149/149/148 | 2 | 34 |
| `αμην` | `ειτα` | Surface vocabulary ειτα | 150/147/145/143 | 10 | 36 |
| `αμην` | `φωνη` | Surface vocabulary φωνη | 159/157/157/159 | 37 | 37 |
| `αμην` | `εργα` | Surface vocabulary εργα | 147/146/146/142 | 14 | 38 |
| `αμην` | `εμου` | Surface vocabulary εμου | 146/144/150/144 | 11 | 39 |
| `αμην` | `ονον` | Surface vocabulary ονον | 158/160/160/158 | 41 | 41 |
| `αμην` | `εχον` | Surface vocabulary εχον | 143/144/144/138 | 26 | 42 |
| `αμην` | `μηδε` | Surface vocabulary μηδε | 142/144/144/142 | 23 | 47 |
| `αμην` | `σωμα` | Surface vocabulary σωμα | 142/142/142/139 | 30 | 48 |
| `αμην` | `αλλη` | Surface vocabulary αλλη | 143/137/137/128 | 50 | 50 |
| `αμην` | `ελθω` | Surface vocabulary ελθω | 163/162/163/158 | 51 | 51 |
| `αμην` | `επει` | Surface vocabulary επει | 137/136/137/133 | 52 | 58 |
| `αμην` | `ελθε` | Surface vocabulary ελθε | 137/135/136/124 | 63 | 63 |
| `αμην` | `ειμι` | Surface vocabulary ειμι | 139/133/133/135 | 55 | 65 |
| `αμην` | `απαν` | Surface vocabulary απαν | 173/165/165/157 | 65 | 65 |
| `αμην` | `ημιν` | Surface vocabulary ημιν | 168/168/168/161 | 70 | 70 |
| `αμην` | `γενη` | Surface vocabulary γενη | 131/133/134/134 | 63 | 71 |
| `αμην` | `ιωνα` | Surface vocabulary ιωνα | 134/133/132/124 | 72 | 72 |
| `αμην` | `πασα` | Surface vocabulary πασα | 166/168/167/166 | 72 | 72 |
| `αμην` | `ισαι` | Surface vocabulary ισαι | 168/168/169/164 | 74 | 74 |
| `αμην` | `καιν` | Surface vocabulary καιν | 131/131/131/128 | 74 | 74 |
| `αμην` | `οιδα` | Surface vocabulary οιδα | 171/171/171/169 | 87 | 87 |
| `αμην` | `λαλη` | Surface vocabulary λαλη | 129/126/126/125 | 89 | 89 |
| `αμην` | `καθα` | Surface vocabulary καθα | 127/127/127/124 | 90 | 90 |
| `αμην` | `ρακα` | Surface vocabulary ρακα | 173/172/172/177 | 99 | 99 |
| `αμην` | `εκτω` | Surface vocabulary εκτω | 118/122/122/124 | 109 | 109 |
| `αμην` | `οταν` | Surface vocabulary οταν | 119/119/118/120 | 119 | 119 |
| `αμην` | `πολυ` | Surface vocabulary πολυ | 119/120/120/117 | 119 | 119 |
| `αμην` | `εχει` | Surface vocabulary εχει | 180/179/180/179 | 123 | 123 |
| `αμην` | `ημασ` | Surface vocabulary ημασ | 187/180/181/175 | 128 | 128 |
| `αμην` | `ουση` | Surface vocabulary ουση | 117/118/118/113 | 129 | 129 |
| `αμην` | `τινα` | Surface vocabulary τινα | 180/180/180/185 | 130 | 130 |
| `αμην` | `αιμα` | Surface vocabulary αιμα | 184/181/181/180 | 131 | 131 |
| `αμην` | `εστη` | Surface vocabulary εστη | 187/181/184/182 | 139 | 139 |
| `αμην` | `ρημα` | Surface vocabulary ρημα | 116/114/114/112 | 139 | 139 |
| `αμην` | `εκτη` | Surface vocabulary εκτη | 115/114/115/111 | 140 | 140 |
| `αμην` | `καθη` | Surface vocabulary καθη | 113/111/111/114 | 146 | 146 |
| `αμην` | `οντι` | Surface vocabulary οντι | 115/114/114/105 | 147 | 147 |
| `αμην` | `ωσει` | Surface vocabulary ωσει | 189/188/190/175 | 147 | 147 |
| `αμην` | `λαβε` | Surface vocabulary λαβε | 111/110/110/110 | 154 | 154 |
| `αμην` | `αλασ` | Surface vocabulary αλασ | 110/109/109/110 | 157 | 157 |
| `αμην` | `εστω` | Surface vocabulary εστω | 111/108/108/104 | 164 | 164 |
| `αμην` | `ατερ` | Surface vocabulary ατερ | 192/192/192/184 | 165 | 165 |
| `αμην` | `ταδε` | Surface vocabulary ταδε | 108/108/108/102 | 169 | 169 |
| `αμην` | `ουτε` | Surface vocabulary ουτε | 107/107/108/99 | 174 | 174 |
| `αμην` | `ποτε` | Surface vocabulary ποτε | 104/104/104/104 | 179 | 179 |
| `αμην` | `οπου` | Surface vocabulary οπου | 104/103/103/102 | 183 | 183 |
| `αμην` | `εγνω` | Surface vocabulary εγνω | 104/102/103/101 | 185 | 185 |
| `αμην` | `χειρ` | Surface vocabulary χειρ | 198/194/194/194 | 185 | 185 |
| `αμην` | `ωστε` | Surface vocabulary ωστε | 103/102/102/103 | 185 | 185 |
| `αμην` | `θελη` | Surface vocabulary θελη | 102/100/100/98 | 195 | 195 |
| `αμην` | `εστε` | Surface vocabulary εστε | 201/200/200/200 | 206 | 206 |
| `αμην` | `μιαν` | Surface vocabulary μιαν | 97/98/98/96 | 206 | 206 |
| `αμην` | `ησαυ` | Surface vocabulary ησαυ | 96/96/96/97 | 210 | 210 |
| `αμην` | `μεγα` | Surface vocabulary μεγα | 203/201/201/203 | 213 | 213 |
| `αμην` | `ολην` | Surface vocabulary ολην | 95/96/96/93 | 215 | 215 |
| `αμην` | `ητοι` | Surface vocabulary ητοι | 94/94/94/93 | 220 | 220 |
| `αμην` | `επαν` | Surface vocabulary επαν | 100/88/98/88 | 221 | 221 |
| `αμην` | `κενα` | Surface vocabulary κενα | 91/93/93/96 | 222 | 222 |
| `αμην` | `αρασ` | Surface vocabulary αρασ | 94/93/93/92 | 223 | 223 |
| `αμην` | `ητισ` | Surface vocabulary ητισ | 91/89/89/86 | 240 | 240 |
| `αμην` | `αββα` | Surface vocabulary αββα | 88/90/90/80 | 247 | 247 |
| `αμην` | `ουαι` | Surface vocabulary ουαι | 86/88/88/85 | 248 | 248 |
| `αμην` | `ομου` | Surface vocabulary ομου | 86/86/86/85 | 252 | 252 |
| `αμην` | `οιοι` | Surface vocabulary οιοι | 85/86/86/84 | 254 | 254 |
| `αμην` | `παση` | Surface vocabulary παση | 84/85/86/86 | 254 | 254 |
| `αμην` | `αγει` | Surface vocabulary αγει | 85/84/84/85 | 257 | 257 |
| `αμην` | `αρτι` | Surface vocabulary αρτι | 214/214/214/211 | 258 | 258 |
| `αμην` | `εχων` | Surface vocabulary εχων | 80/83/83/88 | 261 | 261 |
| `αμην` | `πουσ` | Surface vocabulary πουσ | 83/83/83/82 | 264 | 264 |
| `αμην` | `ιδων` | Surface vocabulary ιδων | 82/84/84/80 | 265 | 265 |
| `αμην` | `αιρε` | Surface vocabulary αιρε | 82/81/81/79 | 272 | 272 |
| `αμην` | `ειτε` | Surface vocabulary ειτε | 218/218/218/216 | 275 | 275 |
| `αμην` | `υιον` | Surface vocabulary υιον | 79/78/80/80 | 278 | 278 |
| `αμην` | `ημεν` | Surface vocabulary ημεν | 220/221/220/213 | 279 | 279 |
| `αμην` | `ανερ` | Surface vocabulary ανερ | 81/79/79/76 | 280 | 280 |
| `αμην` | `οτου` | Surface vocabulary οτου | 224/222/221/209 | 281 | 281 |
| `αμην` | `ειπα` | Surface vocabulary ειπα | 73/74/73/174 | 201 | 289 |
| `αμην` | `αρτω` | Surface vocabulary αρτω | 75/76/76/76 | 292 | 292 |
| `αμην` | `ετων` | Surface vocabulary ετων | 76/74/74/76 | 295 | 295 |
| `αμην` | `επτα` | Surface vocabulary επτα | 73/75/75/73 | 299 | 299 |
| `αμην` | `καλω` | Surface vocabulary καλω | 74/74/74/74 | 299 | 299 |
| `αμην` | `μενε` | Surface vocabulary μενε | 227/227/225/221 | 305 | 305 |
| `αμην` | `μενη` | Surface vocabulary μενη | 226/225/225/225 | 306 | 306 |
| `αμην` | `γυνη` | Surface vocabulary γυνη | 73/72/72/71 | 307 | 307 |
| `αμην` | `αρχη` | Surface vocabulary αρχη | 69/70/70/75 | 311 | 311 |
| `αμην` | `δοθη` | Surface vocabulary δοθη | 70/71/71/71 | 312 | 312 |
| `αμην` | `δοξη` | Surface vocabulary δοξη | 69/69/69/69 | 319 | 319 |
| `αμην` | `ελθη` | Surface vocabulary ελθη | 68/68/68/72 | 319 | 319 |
| `αμην` | `τιμη` | Surface vocabulary τιμη | 73/66/71/65 | 320 | 320 |
| `αμην` | `δουσ` | Surface vocabulary δουσ | 69/70/70/65 | 321 | 321 |
| `αμην` | `ψυχη` | Surface vocabulary ψυχη | 69/69/69/67 | 321 | 321 |
| `αμην` | `οδον` | Surface vocabulary οδον | 68/68/68/68 | 323 | 323 |

Markdown preview capped at 100 controls; full matched-control rows: 1,400.

## Read

This is a control-pool report, not a significance test. It uses the same
normalized substring rule as the current surface-context path and avoids
the bad control design of comparing surface-context rows against random
strings. The next step can freeze one matched-control set per target and
then run the ELS exact-center surface statistic against those real-word
controls.
