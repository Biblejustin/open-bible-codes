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
| 1 | `center_word_same_category` | `μαρια` | 29 | `canonical_to_apocrypha` | MAL 4:6 | ισραηλ | MAL 4:6;TOB 1:1 |
| 2 | `center_verse_exact` | `αμην` | 191 | `canonical_to_apocrypha` | MAL 4:6 | δικαιωματα | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 3 | `center_verse_same_category` | `σιων` | -154 | `apocrypha_to_canonical` | MAL 4:6 | δικαιωματα | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 4 | `center_verse_same_category` | `αμμων` | -248 | `apocrypha_to_canonical` | TOB 1:3 | εμου | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4;TOB 1:5;TOB 1:6 |
| 5 | `span_exact` | `αμην` | 217 | `canonical_to_apocrypha` | MAL 4:5 | καρδιαν | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 6 | `span_exact` | `αμην` | -231 | `apocrypha_to_canonical` | TOB 1:2 | υπερανω | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 7 | `span_exact` | `ναοσ` | 242 | `canonical_to_apocrypha` | TOB 1:2 | θισβησ | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 8 | `span_exact` | `αμην` | 247 | `canonical_to_apocrypha` | TOB 1:1 | τωβιηλ | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 9 | `span_same_category` | `ελαμ` | 120 | `canonical_to_apocrypha` | TOB 1:2 | βασιλεωσ | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 10 | `span_same_category` | `ελαμ` | -136 | `apocrypha_to_canonical` | TOB 1:2 | ενεμεσσαρου | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 11 | `span_same_category` | `σιων` | -176 | `apocrypha_to_canonical` | TOB 1:2 | επορευομην | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 12 | `span_same_category` | `σιων` | 187 | `canonical_to_apocrypha` | MAL 4:5 | προσ | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 13 | `span_same_category` | `αδαμ` | 195 | `canonical_to_apocrypha` | TOB 1:1 | νεφθαλιμ | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 14 | `span_same_category` | `αδαμ` | -195 | `apocrypha_to_canonical` | TOB 1:2 | τωβιτ | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 15 | `span_same_category` | `σιων` | -198 | `apocrypha_to_canonical` | MAL 4:5 | υιον | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 16 | `span_same_category` | `θεοσ` | -204 | `apocrypha_to_canonical` | TOB 1:1 | τωβιτ | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 17 | `span_same_category` | `σιων` | -204 | `apocrypha_to_canonical` | TOB 1:1 | γαβαηλ | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 18 | `span_same_category` | `ελαμ` | -209 | `apocrypha_to_canonical` | MAL 4:6 | δικαιωματα | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 19 | `span_same_category` | `αιμα` | -210 | `apocrypha_to_canonical` | TOB 1:2 | οδοισ | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 20 | `span_same_category` | `σιων` | -218 | `apocrypha_to_canonical` | TOB 1:2 | βασιλεωσ | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 21 | `span_same_category` | `ρωμη` | -221 | `apocrypha_to_canonical` | TOB 1:1 | τωβιηλ | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 22 | `span_same_category` | `βασαν` | -222 | `apocrypha_to_canonical` | TOB 1:2 | οδοισ | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4;TOB 1:5 |
| 23 | `span_same_category` | `θεοσ` | 223 | `canonical_to_apocrypha` | MAL 4:4 | επιφανη | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 24 | `span_same_category` | `αιμα` | -223 | `apocrypha_to_canonical` | TOB 1:1 | του | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 25 | `span_same_category` | `αιμα` | 224 | `canonical_to_apocrypha` | TOB 1:3 | τοισ | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4;TOB 1:5 |
| 26 | `span_same_category` | `αιμα` | 226 | `canonical_to_apocrypha` | TOB 1:3 | τοισ | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4;TOB 1:5 |
| 27 | `span_same_category` | `αιμα` | -238 | `apocrypha_to_canonical` | TOB 1:2 | ηχμαλωτευθη | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 28 | `span_same_category` | `αιμα` | -246 | `apocrypha_to_canonical` | TOB 1:2 | αληθειασ | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 29 | `span_same_category` | `σιων` | 250 | `canonical_to_apocrypha` | MAL 4:4 | εγω | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 30 | `hidden_path_only` | `ναοσ` | 40 | `canonical_to_apocrypha` | TOB 1:1 | λογων | MAL 4:6;TOB 1:1 |
| 31 | `hidden_path_only` | `αδησ` | 43 | `canonical_to_apocrypha` | TOB 1:1 | τωβιτ | MAL 4:6;TOB 1:1 |
| 32 | `hidden_path_only` | `υιοσ` | 71 | `canonical_to_apocrypha` | TOB 1:1 | ανανιηλ | MAL 4:6;TOB 1:1;TOB 1:2 |
| 33 | `hidden_path_only` | `λεων` | -83 | `apocrypha_to_canonical` | TOB 1:1 | σπερματοσ | MAL 4:6;TOB 1:1;TOB 1:2 |
| 34 | `hidden_path_only` | `ελαμ` | -85 | `apocrypha_to_canonical` | TOB 1:1 | ανανιηλ | MAL 4:6;TOB 1:1;TOB 1:2 |
| 35 | `hidden_path_only` | `αιμα` | -99 | `apocrypha_to_canonical` | TOB 1:2 | ημεραισ | MAL 4:6;TOB 1:1;TOB 1:2 |
| 36 | `hidden_path_only` | `υιοσ` | -103 | `apocrypha_to_canonical` | MAL 4:6 | ισραηλ | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 37 | `hidden_path_only` | `ναοσ` | 130 | `canonical_to_apocrypha` | MAL 4:5 | αποκαταστησει | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 38 | `hidden_path_only` | `ναοσ` | 131 | `canonical_to_apocrypha` | TOB 1:2 | δεξιων | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 39 | `hidden_path_only` | `οφισ` | -136 | `apocrypha_to_canonical` | TOB 1:1 | λογων | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 40 | `hidden_path_only` | `ναοσ` | 138 | `canonical_to_apocrypha` | MAL 4:5 | προσ | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 41 | `hidden_path_only` | `δοξα` | 140 | `canonical_to_apocrypha` | MAL 4:5 | αποκαταστησει | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 42 | `hidden_path_only` | `ναοσ` | 140 | `canonical_to_apocrypha` | TOB 1:2 | εκ | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 43 | `hidden_path_only` | `ελκη` | 147 | `canonical_to_apocrypha` | TOB 1:2 | δεξιων | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 44 | `hidden_path_only` | `οθων` | -156 | `apocrypha_to_canonical` | TOB 1:2 | ηχμαλωτευθη | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 45 | `hidden_path_only` | `ναοσ` | 161 | `canonical_to_apocrypha` | TOB 1:1 | αδουηλ | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 46 | `hidden_path_only` | `υιοσ` | 165 | `canonical_to_apocrypha` | MAL 4:6 | δουλου | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 47 | `hidden_path_only` | `αιμα` | -168 | `apocrypha_to_canonical` | MAL 4:5 | ανθρωπου | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 48 | `hidden_path_only` | `οργη` | 175 | `canonical_to_apocrypha` | MAL 4:6 | του | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 49 | `hidden_path_only` | `ακρισ` | 176 | `canonical_to_apocrypha` | MAL 4:4 | πριν | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 50 | `hidden_path_only` | `αδησ` | 177 | `canonical_to_apocrypha` | MAL 4:6 | προσταγματα | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 51 | `hidden_path_only` | `θεοσ` | 184 | `canonical_to_apocrypha` | TOB 1:2 | τωβιτ | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 52 | `hidden_path_only` | `αιμα` | 190 | `canonical_to_apocrypha` | MAL 4:5 | καρδιαν | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 53 | `hidden_path_only` | `υιοσ` | -195 | `apocrypha_to_canonical` | TOB 1:2 | του | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 54 | `hidden_path_only` | `λεων` | -195 | `apocrypha_to_canonical` | TOB 1:2 | υπερανω | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 55 | `hidden_path_only` | `ελκη` | 196 | `canonical_to_apocrypha` | MAL 4:5 | παταξω | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 56 | `hidden_path_only` | `υιοσ` | 203 | `canonical_to_apocrypha` | TOB 1:2 | επορευομην | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 57 | `hidden_path_only` | `υιοσ` | 212 | `canonical_to_apocrypha` | TOB 1:2 | υπερανω | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 58 | `hidden_path_only` | `υιοσ` | -213 | `apocrypha_to_canonical` | MAL 4:6 | παντα | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 59 | `hidden_path_only` | `ελκη` | 215 | `canonical_to_apocrypha` | TOB 1:1 | γαβαηλ | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 60 | `hidden_path_only` | `τιτοσ` | 225 | `canonical_to_apocrypha` | MAL 4:3 | καταπατησετε | MAL 3:18;MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 61 | `hidden_path_only` | `λεων` | 232 | `canonical_to_apocrypha` | TOB 1:3 | και | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 62 | `hidden_path_only` | `λεων` | 248 | `canonical_to_apocrypha` | TOB 1:2 | δικαιοσυνησ | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |

## Read

- `center_word_exact` is the rare direct case: hidden term text is also
  present in the surface word containing the ELS center.
- same-concept and same-category rows are broader review queues, not
  interpretation claims.
- `hidden_path_only` means the bridge exists, but this pass did not find
  declared surface-term support at the center or span level.
