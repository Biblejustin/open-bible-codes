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
| 1 | `center_word_same_category` | `μαρια` (Maria; English: Mary) | 29 | `canonical_to_apocrypha` | MAL 4:6 | `ισραηλ` (israel; English: Israel) | MAL 4:6;TOB 1:1 |
| 2 | `center_verse_exact` | `αμην` (amen; English: Amen) | 191 | `canonical_to_apocrypha` | MAL 4:6 | `δικαιωματα` (dikaiomata; English: ordinances) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 3 | `center_verse_same_category` | `σιων` (Sion; English: Zion) | -154 | `apocrypha_to_canonical` | MAL 4:6 | `δικαιωματα` (dikaiomata; English: ordinances) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 4 | `center_verse_same_category` | `αμμων` (ammon; English: Ammon) | -248 | `apocrypha_to_canonical` | TOB 1:3 | `εμου` (emou; English: of me) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4;TOB 1:5;TOB 1:6 |
| 5 | `span_exact` | `αμην` (amen; English: Amen) | 217 | `canonical_to_apocrypha` | MAL 4:5 | `καρδιαν` (kardian; English: heart) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 6 | `span_exact` | `αμην` (amen; English: Amen) | -231 | `apocrypha_to_canonical` | TOB 1:2 | `υπερανω` (uperano; English: above) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 7 | `span_exact` | `ναοσ` (naos; English: temple) | 242 | `canonical_to_apocrypha` | TOB 1:2 | `θισβησ` (thisbes; English: Thisbe) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 8 | `span_exact` | `αμην` (amen; English: Amen) | 247 | `canonical_to_apocrypha` | TOB 1:1 | `τωβιηλ` (tobiel; English: Tobiel) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 9 | `span_same_category` | `ελαμ` (Elam; English: Elam) | 120 | `canonical_to_apocrypha` | TOB 1:2 | `βασιλεωσ` (basileos; English: king) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 10 | `span_same_category` | `ελαμ` (Elam; English: Elam) | -136 | `apocrypha_to_canonical` | TOB 1:2 | `ενεμεσσαρου` (enemessarou; English: Enemessar) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 11 | `span_same_category` | `σιων` (Sion; English: Zion) | -176 | `apocrypha_to_canonical` | TOB 1:2 | `επορευομην` (eporeuomen; English: I walked) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 12 | `span_same_category` | `σιων` (Sion; English: Zion) | 187 | `canonical_to_apocrypha` | MAL 4:5 | `προσ` (pros; English: toward) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 13 | `span_same_category` | `αδαμ` (adam; English: Adam) | 195 | `canonical_to_apocrypha` | TOB 1:1 | `νεφθαλιμ` (nephthalim; English: Naphtali) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 14 | `span_same_category` | `αδαμ` (adam; English: Adam) | -195 | `apocrypha_to_canonical` | TOB 1:2 | `τωβιτ` (tobit; English: Tobit) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 15 | `span_same_category` | `σιων` (Sion; English: Zion) | -198 | `apocrypha_to_canonical` | MAL 4:5 | `υιον` (uion; English: son) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 16 | `span_same_category` | `θεοσ` (theos; English: God) | -204 | `apocrypha_to_canonical` | TOB 1:1 | `τωβιτ` (tobit; English: Tobit) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 17 | `span_same_category` | `σιων` (Sion; English: Zion) | -204 | `apocrypha_to_canonical` | TOB 1:1 | `γαβαηλ` (gabael; English: Gabael) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 18 | `span_same_category` | `ελαμ` (Elam; English: Elam) | -209 | `apocrypha_to_canonical` | MAL 4:6 | `δικαιωματα` (dikaiomata; English: ordinances) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 19 | `span_same_category` | `αιμα` (haima; English: blood) | -210 | `apocrypha_to_canonical` | TOB 1:2 | `οδοισ` (odois; English: ways) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 20 | `span_same_category` | `σιων` (Sion; English: Zion) | -218 | `apocrypha_to_canonical` | TOB 1:2 | `βασιλεωσ` (basileos; English: king) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 21 | `span_same_category` | `ρωμη` (rome; English: Rome) | -221 | `apocrypha_to_canonical` | TOB 1:1 | `τωβιηλ` (tobiel; English: Tobiel) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 22 | `span_same_category` | `βασαν` (basan; English: Bashan) | -222 | `apocrypha_to_canonical` | TOB 1:2 | `οδοισ` (odois; English: ways) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4;TOB 1:5 |
| 23 | `span_same_category` | `θεοσ` (theos; English: God) | 223 | `canonical_to_apocrypha` | MAL 4:4 | `επιφανη` (epiphane; English: manifest/glorious) | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 24 | `span_same_category` | `αιμα` (haima; English: blood) | -223 | `apocrypha_to_canonical` | TOB 1:1 | `του` (tou; English: of the) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 25 | `span_same_category` | `αιμα` (haima; English: blood) | 224 | `canonical_to_apocrypha` | TOB 1:3 | `τοισ` (tois; English: to the) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4;TOB 1:5 |
| 26 | `span_same_category` | `αιμα` (haima; English: blood) | 226 | `canonical_to_apocrypha` | TOB 1:3 | `τοισ` (tois; English: to the) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4;TOB 1:5 |
| 27 | `span_same_category` | `αιμα` (haima; English: blood) | -238 | `apocrypha_to_canonical` | TOB 1:2 | `ηχμαλωτευθη` (echmaloteuthe; English: was taken captive) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 28 | `span_same_category` | `αιμα` (haima; English: blood) | -246 | `apocrypha_to_canonical` | TOB 1:2 | `αληθειασ` (aletheias; English: truth) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 29 | `span_same_category` | `σιων` (Sion; English: Zion) | 250 | `canonical_to_apocrypha` | MAL 4:4 | `εγω` (ego; English: I) | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 30 | `hidden_path_only` | `ναοσ` (naos; English: temple) | 40 | `canonical_to_apocrypha` | TOB 1:1 | `λογων` (logon; English: words) | MAL 4:6;TOB 1:1 |
| 31 | `hidden_path_only` | `αδησ` (ades; English: Hades) | 43 | `canonical_to_apocrypha` | TOB 1:1 | `τωβιτ` (tobit; English: Tobit) | MAL 4:6;TOB 1:1 |
| 32 | `hidden_path_only` | `υιοσ` (huios; English: son) | 71 | `canonical_to_apocrypha` | TOB 1:1 | `ανανιηλ` (ananiel; English: Ananiel) | MAL 4:6;TOB 1:1;TOB 1:2 |
| 33 | `hidden_path_only` | `λεων` (leon; English: Lion) | -83 | `apocrypha_to_canonical` | TOB 1:1 | `σπερματοσ` (spermatos; English: seed/descendant) | MAL 4:6;TOB 1:1;TOB 1:2 |
| 34 | `hidden_path_only` | `ελαμ` (Elam; English: Elam) | -85 | `apocrypha_to_canonical` | TOB 1:1 | `ανανιηλ` (ananiel; English: Ananiel) | MAL 4:6;TOB 1:1;TOB 1:2 |
| 35 | `hidden_path_only` | `αιμα` (haima; English: blood) | -99 | `apocrypha_to_canonical` | TOB 1:2 | `ημεραισ` (hemerais; English: days) | MAL 4:6;TOB 1:1;TOB 1:2 |
| 36 | `hidden_path_only` | `υιοσ` (huios; English: son) | -103 | `apocrypha_to_canonical` | MAL 4:6 | `ισραηλ` (israel; English: Israel) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 37 | `hidden_path_only` | `ναοσ` (naos; English: temple) | 130 | `canonical_to_apocrypha` | MAL 4:5 | `αποκαταστησει` (apokatastesei; English: will restore) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 38 | `hidden_path_only` | `ναοσ` (naos; English: temple) | 131 | `canonical_to_apocrypha` | TOB 1:2 | `δεξιων` (dexion; English: right side) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 39 | `hidden_path_only` | `οφισ` (ophis; English: Serpent) | -136 | `apocrypha_to_canonical` | TOB 1:1 | `λογων` (logon; English: words) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 40 | `hidden_path_only` | `ναοσ` (naos; English: temple) | 138 | `canonical_to_apocrypha` | MAL 4:5 | `προσ` (pros; English: toward) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 41 | `hidden_path_only` | `δοξα` (doxa; English: glory) | 140 | `canonical_to_apocrypha` | MAL 4:5 | `αποκαταστησει` (apokatastesei; English: will restore) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 42 | `hidden_path_only` | `ναοσ` (naos; English: temple) | 140 | `canonical_to_apocrypha` | TOB 1:2 | `εκ` (ek; English: from) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 43 | `hidden_path_only` | `ελκη` (elke; English: boils/sores) | 147 | `canonical_to_apocrypha` | TOB 1:2 | `δεξιων` (dexion; English: right side) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 44 | `hidden_path_only` | `οθων` (othon; English: Otho) | -156 | `apocrypha_to_canonical` | TOB 1:2 | `ηχμαλωτευθη` (echmaloteuthe; English: was taken captive) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 45 | `hidden_path_only` | `ναοσ` (naos; English: temple) | 161 | `canonical_to_apocrypha` | TOB 1:1 | `αδουηλ` (adouel; English: Aduel) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 46 | `hidden_path_only` | `υιοσ` (huios; English: son) | 165 | `canonical_to_apocrypha` | MAL 4:6 | `δουλου` (doulou; English: servant) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 47 | `hidden_path_only` | `αιμα` (haima; English: blood) | -168 | `apocrypha_to_canonical` | MAL 4:5 | `ανθρωπου` (anthropou; English: man/human) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 48 | `hidden_path_only` | `οργη` (orge; English: Wrath) | 175 | `canonical_to_apocrypha` | MAL 4:6 | `του` (tou; English: of the) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 49 | `hidden_path_only` | `ακρισ` (akris; English: Locust) | 176 | `canonical_to_apocrypha` | MAL 4:4 | `πριν` (prin; English: before) | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 50 | `hidden_path_only` | `αδησ` (ades; English: Hades) | 177 | `canonical_to_apocrypha` | MAL 4:6 | `προσταγματα` (prostagmata; English: commandments) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 51 | `hidden_path_only` | `θεοσ` (theos; English: God) | 184 | `canonical_to_apocrypha` | TOB 1:2 | `τωβιτ` (tobit; English: Tobit) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 52 | `hidden_path_only` | `αιμα` (haima; English: blood) | 190 | `canonical_to_apocrypha` | MAL 4:5 | `καρδιαν` (kardian; English: heart) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 53 | `hidden_path_only` | `υιοσ` (huios; English: son) | -195 | `apocrypha_to_canonical` | TOB 1:2 | `του` (tou; English: of the) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 54 | `hidden_path_only` | `λεων` (leon; English: Lion) | -195 | `apocrypha_to_canonical` | TOB 1:2 | `υπερανω` (uperano; English: above) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 55 | `hidden_path_only` | `ελκη` (elke; English: boils/sores) | 196 | `canonical_to_apocrypha` | MAL 4:5 | `παταξω` (pataxo; English: I will strike) | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 56 | `hidden_path_only` | `υιοσ` (huios; English: son) | 203 | `canonical_to_apocrypha` | TOB 1:2 | `επορευομην` (eporeuomen; English: I walked) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 57 | `hidden_path_only` | `υιοσ` (huios; English: son) | 212 | `canonical_to_apocrypha` | TOB 1:2 | `υπερανω` (uperano; English: above) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 58 | `hidden_path_only` | `υιοσ` (huios; English: son) | -213 | `apocrypha_to_canonical` | MAL 4:6 | `παντα` (panta; English: all) | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 59 | `hidden_path_only` | `ελκη` (elke; English: boils/sores) | 215 | `canonical_to_apocrypha` | TOB 1:1 | `γαβαηλ` (gabael; English: Gabael) | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 60 | `hidden_path_only` | `τιτοσ` (titos; English: Titus) | 225 | `canonical_to_apocrypha` | MAL 4:3 | `καταπατησετε` (katapatesete; English: you will trample) | MAL 3:18;MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 61 | `hidden_path_only` | `λεων` (leon; English: Lion) | 232 | `canonical_to_apocrypha` | TOB 1:3 | `και` (kai; English: and) | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 62 | `hidden_path_only` | `λεων` (leon; English: Lion) | 248 | `canonical_to_apocrypha` | TOB 1:2 | `δικαιοσυνησ` (dikaiosunes; English: righteousness) | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |

## Read

- `center_word_exact` is the rare direct case: hidden term text is also
  present in the surface word containing the ELS center.
- same-concept and same-category rows are broader review queues, not
  interpretation claims.
- `hidden_path_only` means the bridge exists, but this pass did not find
  declared surface-term support at the center or span level.
