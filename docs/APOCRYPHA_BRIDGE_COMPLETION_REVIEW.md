# Apocrypha Bridge Completion Review

Status: derived review packet. This is not a claim report.

This report restates existing bridge candidates as completion rows:
the expanded stream supplies a full ELS, while the canonical-only
letters would leave a partial path under the same skip and direction.

## Inputs

- LXX: `reports/apocrypha_bridge_candidates/bridge_candidates.csv`
- KJVA: `reports/kjv_apocrypha_bridge_candidates/bridge_candidates.csv`

## Summary

- input_files: 2
- completion_rows: 597
- terms_with_completion_rows: 135
- source:KJVA:completion_rows: 535
- source:KJVA:terms_with_completion_rows: 114
- source:LXX:completion_rows: 62
- source:LXX:terms_with_completion_rows: 21
- source:KJVA:bridge_type:apocrypha_to_canonical: 270
- source:KJVA:bridge_type:canonical_to_apocrypha: 265
- source:LXX:bridge_type:apocrypha_to_canonical: 27
- source:LXX:bridge_type:canonical_to_apocrypha: 35
- source:KJVA:apocrypha_completion_letters:1: 186
- source:KJVA:apocrypha_completion_letters:2: 168
- source:KJVA:apocrypha_completion_letters:3: 159
- source:KJVA:apocrypha_completion_letters:4: 21
- source:KJVA:apocrypha_completion_letters:5: 1
- source:LXX:apocrypha_completion_letters:1: 13
- source:LXX:apocrypha_completion_letters:2: 23
- source:LXX:apocrypha_completion_letters:3: 25
- source:LXX:apocrypha_completion_letters:4: 1

## Shortest Completion Rows By Source


### LXX

| Source rank | Term | Skip | Type | Start | Center | End | Canonical partial | Apocrypha completion | Completion indexes | Center word |
| ---: | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | `ναοσ` (naos; English: Temple) | 130 | `canonical_to_apocrypha` | MAL 4:2 | MAL 4:5 | TOB 1:1 | `ναο.` | `...σ` | 4 | ἀποκαταστήσει |
| 14 | `ναοσ` (naos; English: Temple) | 138 | `canonical_to_apocrypha` | MAL 4:3 | MAL 4:5 | TOB 1:1 | `ναο.` | `...σ` | 4 | πρὸς |
| 15 | `δοξα` (doxa; English: Glory) | 140 | `canonical_to_apocrypha` | MAL 4:2 | MAL 4:5 | TOB 1:1 | `δοξ.` | `...α` | 4 | ἀποκαταστήσει |
| 22 | `αιμα` (haima; English: Blood) | -168 | `apocrypha_to_canonical` | TOB 1:2 | MAL 4:5 | MAL 4:2 | `.ιμα` | `α...` | 1 | ἀνθρώπου |
| 24 | `ακρισ` (akris; English: Locust) | 176 | `canonical_to_apocrypha` | MAL 4:1 | MAL 4:4 | TOB 1:2 | `ακρι.` | `....σ` | 5 | πρὶν |
| 28 | `σιων` (Sion; English: Zion) | 187 | `canonical_to_apocrypha` | MAL 4:2 | MAL 4:5 | TOB 1:2 | `σιω.` | `...ν` | 4 | πρὸς |
| 29 | `αιμα` (haima; English: Blood) | 190 | `canonical_to_apocrypha` | MAL 4:2 | MAL 4:5 | TOB 1:2 | `αιμ.` | `...α` | 4 | καρδίαν |
| 35 | `ελκη` (elke; English: Boils) | 196 | `canonical_to_apocrypha` | MAL 4:2 | MAL 4:5 | TOB 1:2 | `ελκ.` | `...η` | 4 | πατάξω |
| 36 | `σιων` (Sion; English: Zion) | -198 | `apocrypha_to_canonical` | TOB 1:2 | MAL 4:5 | MAL 4:2 | `.ιων` | `σ...` | 1 | υἱὸν |
| 45 | `αμην` (amen; English: Amen) | 217 | `canonical_to_apocrypha` | MAL 4:2 | MAL 4:5 | TOB 1:2 | `αμη.` | `...ν` | 4 | καρδίαν |
| 49 | `θεοσ` (theos; English: God) | 223 | `canonical_to_apocrypha` | MAL 4:1 | MAL 4:4 | TOB 1:2 | `θεο.` | `...σ` | 4 | ἐπιφανῆ, |
| 52 | `τιτοσ` (titos; English: Titus) | 225 | `canonical_to_apocrypha` | MAL 3:18 | MAL 4:3 | TOB 1:1 | `τιτο.` | `....σ` | 5 | καταπατήσετε |
| 62 | `σιων` (Sion; English: Zion) | 250 | `canonical_to_apocrypha` | MAL 4:1 | MAL 4:4 | TOB 1:2 | `σιω.` | `...ν` | 4 | ἐγὼ |
| 1 | `μαρια` (Maria; English: Mary) | 29 | `canonical_to_apocrypha` | MAL 4:6 | MAL 4:6 | TOB 1:1 | `μαρ..` | `...ια` | 4;5 | Ἰσραὴλ |
| 2 | `ναοσ` (naos; English: Temple) | 40 | `canonical_to_apocrypha` | MAL 4:6 | TOB 1:1 | TOB 1:1 | `να..` | `..οσ` | 3;4 | λόγων |
| 3 | `αδησ` (ades; English: Hades) | 43 | `canonical_to_apocrypha` | MAL 4:6 | TOB 1:1 | TOB 1:1 | `αδ..` | `..ησ` | 3;4 | Τωβίτ, |
| 4 | `υιοσ` (huios; English: Son) | 71 | `canonical_to_apocrypha` | MAL 4:6 | TOB 1:1 | TOB 1:2 | `υι..` | `..οσ` | 3;4 | Ἀνανιήλ, |
| 6 | `ελαμ` (Elam; English: Elam) | -85 | `apocrypha_to_canonical` | TOB 1:2 | TOB 1:1 | MAL 4:6 | `..αμ` | `ελ..` | 1;2 | Ἀνανιήλ, |
| 8 | `υιοσ` (huios; English: Son) | -103 | `apocrypha_to_canonical` | TOB 1:2 | MAL 4:6 | MAL 4:5 | `..οσ` | `υι..` | 1;2 | Ἰσραὴλ |
| 12 | `οφισ` (ophis; English: Serpent) | -136 | `apocrypha_to_canonical` | TOB 1:2 | TOB 1:1 | MAL 4:5 | `..ισ` | `οφ..` | 1;2 | λόγων |
| 18 | `σιων` (Sion; English: Zion) | -154 | `apocrypha_to_canonical` | TOB 1:2 | MAL 4:6 | MAL 4:4 | `..ων` | `σι..` | 1;2 | δικαιώματα. |
| 20 | `ναοσ` (naos; English: Temple) | 161 | `canonical_to_apocrypha` | MAL 4:4 | TOB 1:1 | TOB 1:3 | `να..` | `..οσ` | 3;4 | Ἀδουήλ, |
| 21 | `υιοσ` (huios; English: Son) | 165 | `canonical_to_apocrypha` | MAL 4:3 | MAL 4:6 | TOB 1:2 | `υι..` | `..οσ` | 3;4 | δούλου |
| 23 | `οργη` (orge; English: Wrath) | 175 | `canonical_to_apocrypha` | MAL 4:3 | MAL 4:6 | TOB 1:2 | `ορ..` | `..γη` | 3;4 | τοῦ |
| 26 | `αδησ` (ades; English: Hades) | 177 | `canonical_to_apocrypha` | MAL 4:4 | MAL 4:6 | TOB 1:2 | `αδ..` | `..ησ` | 3;4 | προστάγματα |
| 30 | `αμην` (amen; English: Amen) | 191 | `canonical_to_apocrypha` | MAL 4:3 | MAL 4:6 | TOB 1:3 | `αμ..` | `..ην` | 3;4 | δικαιώματα. |
| 31 | `αδαμ` (adam; English: Adam) | 195 | `canonical_to_apocrypha` | MAL 4:4 | TOB 1:1 | TOB 1:4 | `αδ..` | `..αμ` | 3;4 | Νεφθαλίμ, |
| 38 | `θεοσ` (theos; English: God) | -204 | `apocrypha_to_canonical` | TOB 1:3 | TOB 1:1 | MAL 4:3 | `..οσ` | `θε..` | 1;2 | Τωβίτ, |
| 39 | `σιων` (Sion; English: Zion) | -204 | `apocrypha_to_canonical` | TOB 1:3 | TOB 1:1 | MAL 4:4 | `..ων` | `σι..` | 1;2 | Γαβαήλ, |
| 40 | `ελαμ` (Elam; English: Elam) | -209 | `apocrypha_to_canonical` | TOB 1:3 | MAL 4:6 | MAL 4:3 | `..αμ` | `ελ..` | 1;2 | δικαιώματα. |
| 43 | `υιοσ` (huios; English: Son) | -213 | `apocrypha_to_canonical` | TOB 1:3 | MAL 4:6 | MAL 4:3 | `..οσ` | `υι..` | 1;2 | πάντα |
| 44 | `ελκη` (elke; English: Boils) | 215 | `canonical_to_apocrypha` | MAL 4:4 | TOB 1:1 | TOB 1:3 | `ελ..` | `..κη` | 3;4 | Γαβαήλ, |
| 47 | `ρωμη` (rome; English: Rome) | -221 | `apocrypha_to_canonical` | TOB 1:3 | TOB 1:1 | MAL 4:3 | `..μη` | `ρω..` | 1;2 | Τωβιήλ, |
| 50 | `αιμα` (haima; English: Blood) | -223 | `apocrypha_to_canonical` | TOB 1:4 | TOB 1:1 | MAL 4:4 | `..μα` | `αι..` | 1;2 | τοῦ |
| 56 | `αιμα` (haima; English: Blood) | -238 | `apocrypha_to_canonical` | TOB 1:4 | TOB 1:2 | MAL 4:4 | `..μα` | `αι..` | 1;2 | ᾐχμαλωτεύθη |
| 59 | `αμην` (amen; English: Amen) | 247 | `canonical_to_apocrypha` | MAL 4:3 | TOB 1:1 | TOB 1:4 | `αμ..` | `..ην` | 3;4 | Τωβιήλ, |
| 5 | `λεων` (leon; English: Lion) | -83 | `apocrypha_to_canonical` | TOB 1:2 | TOB 1:1 | MAL 4:6 | `...ν` | `λεω.` | 1;2;3 | σπέρματος |
| 7 | `αιμα` (haima; English: Blood) | -99 | `apocrypha_to_canonical` | TOB 1:2 | TOB 1:2 | MAL 4:6 | `...α` | `αιμ.` | 1;2;3 | ἡμέραις |
| 9 | `ελαμ` (Elam; English: Elam) | 120 | `canonical_to_apocrypha` | MAL 4:6 | TOB 1:2 | TOB 1:3 | `ε...` | `.λαμ` | 2;3;4 | βασιλέως |
| 11 | `ναοσ` (naos; English: Temple) | 131 | `canonical_to_apocrypha` | MAL 4:6 | TOB 1:2 | TOB 1:3 | `ν...` | `.αοσ` | 2;3;4 | δεξιῶν |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | 22 more rows in CSV |

### KJVA

| Source rank | Term | Skip | Type | Start | Center | End | Canonical partial | Apocrypha completion | Completion indexes | Center word |
| ---: | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | `otho` | 11 | `canonical_to_apocrypha` | MAL 4:6 | MAL 4:6 | TOB 1:1 | `oth.` | `...o` | 4 | earth |
| 4 | `tree` | -12 | `apocrypha_to_canonical` | TOB 1:1 | MAL 4:6 | MAL 4:6 | `.ree` | `t...` | 1 | with |
| 7 | `heth` | 22 | `canonical_to_apocrypha` | MAL 4:6 | MAL 4:6 | TOB 1:1 | `het.` | `...h` | 4 | smite |
| 11 | `tree` | 27 | `canonical_to_apocrypha` | MAL 4:6 | MAL 4:6 | TOB 1:1 | `tre.` | `...e` | 4 | come |
| 13 | `nato` | 33 | `canonical_to_apocrypha` | MAL 4:6 | MAL 4:6 | TOB 1:1 | `nat.` | `...o` | 4 | and |
| 17 | `hand` | 40 | `canonical_to_apocrypha` | MAL 4:6 | MAL 4:6 | TOB 1:1 | `han.` | `...d` | 4 | their |
| 22 | `seed` | -53 | `apocrypha_to_canonical` | TOB 1:1 | MAL 4:6 | MAL 4:5 | `.eed` | `s...` | 1 | fathers, |
| 23 | `nato` | 54 | `canonical_to_apocrypha` | MAL 4:5 | MAL 4:6 | TOB 1:1 | `nat.` | `...o` | 4 | children, |
| 27 | `noah` | 56 | `apocrypha_to_canonical` | 2ES 16:78 | MAT 1:1 | MAT 1:2 | `.oah` | `n...` | 1 | the |
| 28 | `heth` | 57 | `canonical_to_apocrypha` | MAL 4:5 | MAL 4:6 | TOB 1:1 | `het.` | `...h` | 4 | children, |
| 31 | `house` | 60 | `apocrypha_to_canonical` | 2ES 16:78 | MAT 1:2 | MAT 1:4 | `.ouse` | `h....` | 1 | Judas |
| 38 | `star` | 68 | `apocrypha_to_canonical` | 2ES 16:78 | MAT 1:2 | MAT 1:3 | `.tar` | `s...` | 1 | Abraham |
| 39 | `nato` | -68 | `canonical_to_apocrypha` | MAT 1:3 | MAT 1:2 | 2ES 16:78 | `nat.` | `...o` | 4 | and |
| 42 | `nero` | 73 | `canonical_to_apocrypha` | MAL 4:5 | MAL 4:6 | TOB 1:1 | `ner.` | `...o` | 4 | children, |
| 44 | `nero` | -73 | `apocrypha_to_canonical` | TOB 1:1 | MAL 4:6 | MAL 4:5 | `.ero` | `n...` | 1 | heart |
| 47 | `iron` | 74 | `canonical_to_apocrypha` | MAL 4:5 | MAL 4:6 | TOB 1:1 | `iro.` | `...n` | 4 | to |
| 48 | `seal` | 75 | `canonical_to_apocrypha` | MAL 4:5 | MAL 4:6 | TOB 1:1 | `sea.` | `...l` | 4 | children, |
| 49 | `otho` | -75 | `apocrypha_to_canonical` | TOB 1:1 | MAL 4:6 | MAL 4:5 | `.tho` | `o...` | 1 | their |
| 51 | `sign` | 76 | `apocrypha_to_canonical` | 2ES 16:78 | MAT 1:2 | MAT 1:3 | `.ign` | `s...` | 1 | begat |
| 56 | `fire` | -79 | `apocrypha_to_canonical` | TOB 1:1 | MAL 4:6 | MAL 4:5 | `.ire` | `f...` | 1 | to |
| 62 | `torah` | -85 | `apocrypha_to_canonical` | TOB 1:1 | MAL 4:5 | MAL 4:3 | `.orah` | `t....` | 1 | great |
| 63 | `hits` | -85 | `apocrypha_to_canonical` | TOB 1:1 | MAL 4:6 | MAL 4:5 | `.its` | `h...` | 1 | heart |
| 64 | `gate` | -85 | `apocrypha_to_canonical` | TOB 1:1 | MAL 4:6 | MAL 4:5 | `.ate` | `g...` | 1 | children |
| 69 | `isaac` | 86 | `apocrypha_to_canonical` | 2ES 16:78 | MAT 1:2 | MAT 1:5 | `.saac` | `i....` | 1 | Judas |
| 70 | `aaron` | -86 | `apocrypha_to_canonical` | TOB 1:1 | MAL 4:6 | MAL 4:4 | `.aron` | `a....` | 1 | heart |
| 72 | `tree` | 88 | `canonical_to_apocrypha` | MAL 4:4 | MAL 4:6 | TOB 1:1 | `tre.` | `...e` | 4 | the |
| 76 | `otho` | -90 | `apocrypha_to_canonical` | TOB 1:1 | MAL 4:6 | MAL 4:4 | `.tho` | `o...` | 1 | the |
| 77 | `mash` | -90 | `canonical_to_apocrypha` | MAT 1:4 | MAT 1:2 | 2ES 16:77 | `mas.` | `...h` | 4 | begat |
| 80 | `sadat` | -92 | `canonical_to_apocrypha` | MAT 1:6 | MAT 1:3 | 2ES 16:78 | `sada.` | `....t` | 5 | and |
| 82 | `otho` | 94 | `apocrypha_to_canonical` | 2ES 16:78 | MAT 1:2 | MAT 1:4 | `.tho` | `o...` | 1 | his |
| 85 | `nato` | -96 | `canonical_to_apocrypha` | MAT 1:4 | MAT 1:2 | 2ES 16:77 | `nat.` | `...o` | 4 | and |
| 91 | `tree` | 103 | `canonical_to_apocrypha` | MAL 4:4 | MAL 4:6 | TOB 1:1 | `tre.` | `...e` | 4 | and |
| 93 | `seal` | 105 | `apocrypha_to_canonical` | 2ES 16:78 | MAT 1:2 | MAT 1:4 | `.eal` | `s...` | 1 | Jacob |
| 95 | `lane` | 106 | `canonical_to_apocrypha` | MAL 4:4 | MAL 4:6 | TOB 1:1 | `lan.` | `...e` | 4 | children, |
| 99 | `isis` | -109 | `apocrypha_to_canonical` | TOB 1:1 | MAL 4:5 | MAL 4:3 | `.sis` | `i...` | 1 | and |
| 100 | `eber` | 110 | `apocrypha_to_canonical` | 2ES 16:78 | MAT 1:2 | MAT 1:5 | `.ber` | `e...` | 1 | his |
| 120 | `shot` | 123 | `canonical_to_apocrypha` | MAL 4:3 | MAL 4:5 | TOB 1:1 | `sho.` | `...t` | 4 | you |
| 121 | `india` | 123 | `apocrypha_to_canonical` | 2ES 16:78 | MAT 1:4 | MAT 1:8 | `.ndia` | `i....` | 1 | and |
| 123 | `soot` | 124 | `canonical_to_apocrypha` | MAL 4:4 | MAL 4:6 | TOB 1:1 | `soo.` | `...t` | 4 | fathers |
| 125 | `aram` | -124 | `apocrypha_to_canonical` | TOB 1:1 | MAL 4:6 | MAL 4:4 | `.ram` | `a...` | 1 | children, |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | 495 more rows in CSV |

## Read

- `canonical_partial_pattern` preserves canonical-text letters and marks apocrypha-supplied letters with `.`.
- `apocrypha_completion_pattern` preserves the apocrypha/deuterocanon letters that complete the ELS and marks canonical letters with `.`.
- Every row here is complete in the expanded stream and incomplete in canonical-only text under the same path.
- This report records that the bridge-completion event exists; significance still depends on the paired non-Bible and shuffled-insertion controls.
