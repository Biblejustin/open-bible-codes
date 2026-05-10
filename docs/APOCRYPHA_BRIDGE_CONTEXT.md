# LXX Apocrypha Bridge Context

Status: surface-context review aid for bridge candidates. This is not a claim report.

This report keeps all bridge rows and tags whether the hidden term is
centered on the same surface word, a same-concept word, a same-category
word, the center verse, or the start-to-end span.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_context --corpus-label LXX --config configs/example_ebible_grclxx.toml --candidates reports/apocrypha_bridge_candidates/bridge_candidates.csv --terms terms/theological_terms.csv --terms terms/prophetic_terms.csv --terms terms/greek_nt_claim_terms.csv --min-term-length 4 --out reports/apocrypha_bridge_context/context.csv --summary-out reports/apocrypha_bridge_context/summary.csv --markdown-out docs/APOCRYPHA_BRIDGE_CONTEXT.md --manifest-out reports/apocrypha_bridge_context/manifest.json
```

## Summary

- candidate rows: 62
- context rows: 62
- terms with context rows: 21
- center_word_exact: 0 rows / 0 terms
- center_word_same_concept: 0 rows / 0 terms
- center_word_same_category: 1 rows / 1 terms
- center_verse_exact: 1 rows / 1 terms
- center_verse_same_concept: 0 rows / 0 terms
- center_verse_same_category: 2 rows / 2 terms
- span_exact: 4 rows / 2 terms
- span_same_concept: 0 rows / 0 terms
- span_same_category: 21 rows / 7 terms
- hidden_path_only: 33 rows / 14 terms

## Highest-Priority Rows

| Rank | Bucket | Term | Skip | Bridge | Center | Center word | Span refs |
| ---: | --- | --- | ---: | --- | --- | --- | --- |
| 1 | `center_word_same_category` | `μαρια` (maria) | 29 | `canonical_to_apocrypha` | MAL 4:6 | `ισραηλ` (israel) | MAL 4:6;TOB 1:1 |
| 2 | `center_verse_exact` | `αμην` (amen) | 191 | `canonical_to_apocrypha` | MAL 4:6 | `δικαιωματα` (dikaiomata) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 3 | `center_verse_same_category` | `σιων` (sion) | -154 | `apocrypha_to_canonical` | MAL 4:6 | `δικαιωματα` (dikaiomata) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 4 | `center_verse_same_category` | `αμμων` (ammon) | -248 | `apocrypha_to_canonical` | TOB 1:3 | `εμου` (emou) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4;TOB 1:5;TOB 1:6 |
| 5 | `span_exact` | `αμην` (amen) | 217 | `canonical_to_apocrypha` | MAL 4:5 | `καρδιαν` (kardian) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 6 | `span_exact` | `αμην` (amen) | -231 | `apocrypha_to_canonical` | TOB 1:2 | `υπερανω` (uperano) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 7 | `span_exact` | `ναοσ` (naos) | 242 | `canonical_to_apocrypha` | TOB 1:2 | `θισβησ` (thisbes) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 8 | `span_exact` | `αμην` (amen) | 247 | `canonical_to_apocrypha` | TOB 1:1 | `τωβιηλ` (tobiel) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 9 | `span_same_category` | `ελαμ` (elam) | 120 | `canonical_to_apocrypha` | TOB 1:2 | `βασιλεωσ` (basileos) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 10 | `span_same_category` | `ελαμ` (elam) | -136 | `apocrypha_to_canonical` | TOB 1:2 | `ενεμεσσαρου` (enemessarou) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 11 | `span_same_category` | `σιων` (sion) | -176 | `apocrypha_to_canonical` | TOB 1:2 | `επορευομην` (eporeuomen) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 12 | `span_same_category` | `σιων` (sion) | 187 | `canonical_to_apocrypha` | MAL 4:5 | `προσ` (pros) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 13 | `span_same_category` | `αδαμ` (adam) | 195 | `canonical_to_apocrypha` | TOB 1:1 | `νεφθαλιμ` (nephthalim) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 14 | `span_same_category` | `αδαμ` (adam) | -195 | `apocrypha_to_canonical` | TOB 1:2 | `τωβιτ` (tobit) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 15 | `span_same_category` | `σιων` (sion) | -198 | `apocrypha_to_canonical` | MAL 4:5 | `υιον` (uion) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 16 | `span_same_category` | `θεοσ` (theos) | -204 | `apocrypha_to_canonical` | TOB 1:1 | `τωβιτ` (tobit) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 17 | `span_same_category` | `σιων` (sion) | -204 | `apocrypha_to_canonical` | TOB 1:1 | `γαβαηλ` (gabael) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 18 | `span_same_category` | `ελαμ` (elam) | -209 | `apocrypha_to_canonical` | MAL 4:6 | `δικαιωματα` (dikaiomata) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 19 | `span_same_category` | `αιμα` (aima) | -210 | `apocrypha_to_canonical` | TOB 1:2 | `οδοισ` (odois) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 20 | `span_same_category` | `σιων` (sion) | -218 | `apocrypha_to_canonical` | TOB 1:2 | `βασιλεωσ` (basileos) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 21 | `span_same_category` | `ρωμη` (rome) | -221 | `apocrypha_to_canonical` | TOB 1:1 | `τωβιηλ` (tobiel) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 22 | `span_same_category` | `βασαν` (basan) | -222 | `apocrypha_to_canonical` | TOB 1:2 | `οδοισ` (odois) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4;TOB 1:5 |
| 23 | `span_same_category` | `θεοσ` (theos) | 223 | `canonical_to_apocrypha` | MAL 4:4 | `επιφανη` (epiphane) | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 24 | `span_same_category` | `αιμα` (aima) | -223 | `apocrypha_to_canonical` | TOB 1:1 | `του` (tou) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 25 | `span_same_category` | `αιμα` (aima) | 224 | `canonical_to_apocrypha` | TOB 1:3 | `τοισ` (tois) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4;TOB 1:5 |
| 26 | `span_same_category` | `αιμα` (aima) | 226 | `canonical_to_apocrypha` | TOB 1:3 | `τοισ` (tois) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4;TOB 1:5 |
| 27 | `span_same_category` | `αιμα` (aima) | -238 | `apocrypha_to_canonical` | TOB 1:2 | `ηχμαλωτευθη` (echmaloteuthe) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 28 | `span_same_category` | `αιμα` (aima) | -246 | `apocrypha_to_canonical` | TOB 1:2 | `αληθειασ` (aletheias) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 29 | `span_same_category` | `σιων` (sion) | 250 | `canonical_to_apocrypha` | MAL 4:4 | `εγω` (ego) | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 30 | `hidden_path_only` | `ναοσ` (naos) | 40 | `canonical_to_apocrypha` | TOB 1:1 | `λογων` (logon) | MAL 4:6;TOB 1:1 |
| 31 | `hidden_path_only` | `αδησ` (ades) | 43 | `canonical_to_apocrypha` | TOB 1:1 | `τωβιτ` (tobit) | MAL 4:6;TOB 1:1 |
| 32 | `hidden_path_only` | `υιοσ` (uios) | 71 | `canonical_to_apocrypha` | TOB 1:1 | `ανανιηλ` (ananiel) | MAL 4:6;TOB 1:1;TOB 1:2 |
| 33 | `hidden_path_only` | `λεων` (leon) | -83 | `apocrypha_to_canonical` | TOB 1:1 | `σπερματοσ` (spermatos) | MAL 4:6;TOB 1:1;TOB 1:2 |
| 34 | `hidden_path_only` | `ελαμ` (elam) | -85 | `apocrypha_to_canonical` | TOB 1:1 | `ανανιηλ` (ananiel) | MAL 4:6;TOB 1:1;TOB 1:2 |
| 35 | `hidden_path_only` | `αιμα` (aima) | -99 | `apocrypha_to_canonical` | TOB 1:2 | `ημεραισ` (emerais) | MAL 4:6;TOB 1:1;TOB 1:2 |
| 36 | `hidden_path_only` | `υιοσ` (uios) | -103 | `apocrypha_to_canonical` | MAL 4:6 | `ισραηλ` (israel) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 37 | `hidden_path_only` | `ναοσ` (naos) | 130 | `canonical_to_apocrypha` | MAL 4:5 | `αποκαταστησει` (apokatastesei) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 38 | `hidden_path_only` | `ναοσ` (naos) | 131 | `canonical_to_apocrypha` | TOB 1:2 | `δεξιων` (dexion) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 39 | `hidden_path_only` | `οφισ` (ophis) | -136 | `apocrypha_to_canonical` | TOB 1:1 | `λογων` (logon) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 40 | `hidden_path_only` | `ναοσ` (naos) | 138 | `canonical_to_apocrypha` | MAL 4:5 | `προσ` (pros) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 41 | `hidden_path_only` | `δοξα` (doxa; English: glory) | 140 | `canonical_to_apocrypha` | MAL 4:5 | `αποκαταστησει` (apokatastesei) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 42 | `hidden_path_only` | `ναοσ` (naos) | 140 | `canonical_to_apocrypha` | TOB 1:2 | `εκ` (ek) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 43 | `hidden_path_only` | `ελκη` (elke) | 147 | `canonical_to_apocrypha` | TOB 1:2 | `δεξιων` (dexion) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 44 | `hidden_path_only` | `οθων` (othon) | -156 | `apocrypha_to_canonical` | TOB 1:2 | `ηχμαλωτευθη` (echmaloteuthe) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 45 | `hidden_path_only` | `ναοσ` (naos) | 161 | `canonical_to_apocrypha` | TOB 1:1 | `αδουηλ` (adouel) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 46 | `hidden_path_only` | `υιοσ` (uios) | 165 | `canonical_to_apocrypha` | MAL 4:6 | `δουλου` (doulou) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 47 | `hidden_path_only` | `αιμα` (aima) | -168 | `apocrypha_to_canonical` | MAL 4:5 | `ανθρωπου` (anthropou) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 48 | `hidden_path_only` | `οργη` (orge) | 175 | `canonical_to_apocrypha` | MAL 4:6 | `του` (tou) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 49 | `hidden_path_only` | `ακρισ` (akris) | 176 | `canonical_to_apocrypha` | MAL 4:4 | `πριν` (prin) | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 50 | `hidden_path_only` | `αδησ` (ades) | 177 | `canonical_to_apocrypha` | MAL 4:6 | `προσταγματα` (prostagmata) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 51 | `hidden_path_only` | `θεοσ` (theos) | 184 | `canonical_to_apocrypha` | TOB 1:2 | `τωβιτ` (tobit) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 52 | `hidden_path_only` | `αιμα` (aima) | 190 | `canonical_to_apocrypha` | MAL 4:5 | `καρδιαν` (kardian) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 53 | `hidden_path_only` | `υιοσ` (uios) | -195 | `apocrypha_to_canonical` | TOB 1:2 | `του` (tou) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 54 | `hidden_path_only` | `λεων` (leon) | -195 | `apocrypha_to_canonical` | TOB 1:2 | `υπερανω` (uperano) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 55 | `hidden_path_only` | `ελκη` (elke) | 196 | `canonical_to_apocrypha` | MAL 4:5 | `παταξω` (pataxo) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 56 | `hidden_path_only` | `υιοσ` (uios) | 203 | `canonical_to_apocrypha` | TOB 1:2 | `επορευομην` (eporeuomen) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 57 | `hidden_path_only` | `υιοσ` (uios) | 212 | `canonical_to_apocrypha` | TOB 1:2 | `υπερανω` (uperano) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 58 | `hidden_path_only` | `υιοσ` (uios) | -213 | `apocrypha_to_canonical` | MAL 4:6 | `παντα` (panta) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 59 | `hidden_path_only` | `ελκη` (elke) | 215 | `canonical_to_apocrypha` | TOB 1:1 | `γαβαηλ` (gabael) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 60 | `hidden_path_only` | `τιτοσ` (titos) | 225 | `canonical_to_apocrypha` | MAL 4:3 | `καταπατησετε` (katapatesete) | MAL 3:18;MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 61 | `hidden_path_only` | `λεων` (leon) | 232 | `canonical_to_apocrypha` | TOB 1:3 | `και` (kai) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 62 | `hidden_path_only` | `λεων` (leon) | 248 | `canonical_to_apocrypha` | TOB 1:2 | `δικαιοσυνησ` (dikaiosunes) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |

## Read

- `center_word_exact` is the rare direct case: hidden term text is also
  present in the surface word containing the ELS center.
- same-concept and same-category rows are broader review queues, not
  interpretation claims.
- `hidden_path_only` means the bridge exists, but this pass did not find
  declared surface-term support at the center or span level.
