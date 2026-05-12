# KJVA Apocrypha Bridge Context

Status: surface-context review aid for bridge candidates. This is not a claim report.

This report keeps all bridge rows and tags whether the hidden term is
centered on the same surface word, a same-concept word, a same-category
word, the center verse, or the start-to-end span.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_context --corpus-label KJVA --config configs/example_ebible_engkjv_apocrypha.toml --candidates reports/kjv_apocrypha_bridge_candidates/bridge_candidates.csv --terms terms/english_search_terms.csv --min-term-length 4 --out reports/kjv_apocrypha_bridge_context/context.csv --summary-out reports/kjv_apocrypha_bridge_context/summary.csv --markdown-out docs/KJV_APOCRYPHA_BRIDGE_CONTEXT.md --manifest-out reports/kjv_apocrypha_bridge_context/manifest.json
```

## Summary

- candidate rows: 535
- context rows: 535
- terms with context rows: 114
- center_word_exact: 0 rows / 0 terms
- center_word_same_concept: 0 rows / 0 terms
- center_word_same_category: 1 rows / 1 terms
- center_verse_exact: 9 rows / 5 terms
- center_verse_same_concept: 0 rows / 0 terms
- center_verse_same_category: 37 rows / 25 terms
- span_exact: 34 rows / 13 terms
- span_same_concept: 0 rows / 0 terms
- span_same_category: 122 rows / 52 terms
- hidden_path_only: 332 rows / 81 terms

## Highest-Priority Rows

| Rank | Bucket | Term | Skip | Bridge | Center | Center word | Span refs |
| ---: | --- | --- | ---: | --- | --- | --- | --- |
| 1 | `center_word_same_category` | `torah` | 145 | `apocrypha_to_canonical` | MAT 1:1 | `abraham` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6 |
| 2 | `center_verse_exact` | `seed` | 54 | `canonical_to_apocrypha` | TOB 1:1 | `the` | MAL 4:6;TOB 1:1;TOB 1:2 |
| 3 | `center_verse_exact` | `seed` | 67 | `canonical_to_apocrypha` | TOB 1:1 | `tribe` | MAL 4:6;TOB 1:1;TOB 1:2 |
| 4 | `center_verse_exact` | `seed` | -73 | `apocrypha_to_canonical` | TOB 1:1 | `son` | MAL 4:6;TOB 1:1;TOB 1:2 |
| 5 | `center_verse_exact` | `isaac` | 86 | `apocrypha_to_canonical` | MAT 1:2 | `judas` | 2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5 |
| 6 | `center_verse_exact` | `seed` | -102 | `apocrypha_to_canonical` | TOB 1:1 | `tobiel` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 7 | `center_verse_exact` | `aram` | -148 | `canonical_to_apocrypha` | MAT 1:4 | `begat` | 2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7 |
| 8 | `center_verse_exact` | `seed` | -178 | `apocrypha_to_canonical` | TOB 1:1 | `of` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 9 | `center_verse_exact` | `bush` | 203 | `apocrypha_to_canonical` | 2ES 16:77 | `a` | 2ES 16:74;2ES 16:75;2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3 |
| 10 | `center_verse_exact` | `hand` | -243 | `canonical_to_apocrypha` | MAT 1:5 | `begat` | 2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7;MAT 1:8;MAT... |
| 11 | `center_verse_same_category` | `hand` | 40 | `canonical_to_apocrypha` | MAL 4:6 | `their` | MAL 4:6;TOB 1:1 |
| 12 | `center_verse_same_category` | `star` | -84 | `canonical_to_apocrypha` | 2ES 16:77 | `man` | 2ES 16:77;2ES 16:78;MAT 1:1 |
| 13 | `center_verse_same_category` | `hits` | -85 | `apocrypha_to_canonical` | MAL 4:6 | `heart` | MAL 4:5;MAL 4:6;TOB 1:1 |
| 14 | `center_verse_same_category` | `gate` | -85 | `apocrypha_to_canonical` | MAL 4:6 | `children` | MAL 4:5;MAL 4:6;TOB 1:1 |
| 15 | `center_verse_same_category` | `lane` | 106 | `canonical_to_apocrypha` | MAL 4:6 | `children` | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 16 | `center_verse_same_category` | `soot` | -123 | `apocrypha_to_canonical` | MAL 4:6 | `fathers` | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 17 | `center_verse_same_category` | `soot` | 124 | `canonical_to_apocrypha` | MAL 4:6 | `fathers` | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 18 | `center_verse_same_category` | `lane` | -124 | `canonical_to_apocrypha` | MAT 1:2 | `isaac` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5 |
| 19 | `center_verse_same_category` | `seed` | 125 | `canonical_to_apocrypha` | TOB 1:2 | `captive` | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 20 | `center_verse_same_category` | `light` | -127 | `apocrypha_to_canonical` | TOB 1:2 | `galilee` | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 21 | `center_verse_same_category` | `admah` | -131 | `canonical_to_apocrypha` | MAT 1:4 | `salmon` | 2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7;MAT 1:8;MAT... |
| 22 | `center_verse_same_category` | `tomb` | 134 | `apocrypha_to_canonical` | 2ES 16:77 | `field` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1 |
| 23 | `center_verse_same_category` | `hits` | -141 | `apocrypha_to_canonical` | MAL 4:6 | `fathers` | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 24 | `center_verse_same_category` | `eyes` | -143 | `canonical_to_apocrypha` | 2ES 16:77 | `field` | 2ES 16:75;2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2 |
| 25 | `center_verse_same_category` | `ahab` | 145 | `apocrypha_to_canonical` | MAT 1:1 | `generation` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4 |
| 26 | `center_verse_same_category` | `ehyeh` | -145 | `canonical_to_apocrypha` | 2ES 16:76 | `you` | 2ES 16:72;2ES 16:73;2ES 16:74;2ES 16:75;2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1 |
| 27 | `center_verse_same_category` | `gate` | -168 | `canonical_to_apocrypha` | MAT 1:2 | `his` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6 |
| 28 | `center_verse_same_category` | `hannah` | 176 | `apocrypha_to_canonical` | MAT 1:6 | `jesse` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7;M... |
| 29 | `center_verse_same_category` | `hannah` | -176 | `canonical_to_apocrypha` | MAT 1:6 | `jesse` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7;M... |
| 30 | `center_verse_same_category` | `rome` | 184 | `canonical_to_apocrypha` | TOB 1:2 | `nephthali` | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 31 | `center_verse_same_category` | `hail` | 185 | `apocrypha_to_canonical` | 2ES 16:78 | `be` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4 |
| 32 | `center_verse_same_category` | `lane` | 192 | `canonical_to_apocrypha` | MAL 4:6 | `fathers` | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 33 | `center_verse_same_category` | `king` | -192 | `apocrypha_to_canonical` | MAL 4:5 | `the` | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 34 | `center_verse_same_category` | `house` | 196 | `canonical_to_apocrypha` | TOB 1:3 | `justice` | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4;TOB 1:5 |
| 35 | `center_verse_same_category` | `tyre` | 198 | `canonical_to_apocrypha` | TOB 1:2 | `galilee` | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 36 | `center_verse_same_category` | `hand` | 205 | `canonical_to_apocrypha` | MAL 4:6 | `lest` | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 37 | `center_verse_same_category` | `obal` | -210 | `canonical_to_apocrypha` | MAT 1:3 | `begat` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7;M... |
| 38 | `center_verse_same_category` | `love` | 222 | `canonical_to_apocrypha` | TOB 1:2 | `of` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 39 | `center_verse_same_category` | `elam` | 222 | `canonical_to_apocrypha` | TOB 1:2 | `at` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 40 | `center_verse_same_category` | `lane` | 226 | `canonical_to_apocrypha` | MAL 4:6 | `heart` | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 41 | `center_verse_same_category` | `lion` | 226 | `apocrypha_to_canonical` | 2ES 16:77 | `may` | 2ES 16:74;2ES 16:75;2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT... |
| 42 | `center_verse_same_category` | `lane` | -232 | `apocrypha_to_canonical` | MAL 4:6 | `and` | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 43 | `center_verse_same_category` | `eden` | 233 | `canonical_to_apocrypha` | MAL 4:4 | `judgments` | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 44 | `center_verse_same_category` | `altar` | -234 | `apocrypha_to_canonical` | TOB 1:4 | `country` | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4;TOB 1:5;TOB 1:6 |
| 45 | `center_verse_same_category` | `seed` | -238 | `apocrypha_to_canonical` | TOB 1:2 | `properly` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 46 | `center_verse_same_category` | `soot` | 240 | `canonical_to_apocrypha` | MAL 4:6 | `heart` | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 47 | `center_verse_same_category` | `rome` | 250 | `canonical_to_apocrypha` | TOB 1:2 | `properly` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 48 | `span_exact` | `seed` | -53 | `apocrypha_to_canonical` | MAL 4:6 | `fathers` | MAL 4:5;MAL 4:6;TOB 1:1 |
| 49 | `span_exact` | `rent` | 73 | `canonical_to_apocrypha` | TOB 1:1 | `the` | MAL 4:6;TOB 1:1;TOB 1:2 |
| 50 | `span_exact` | `gate` | -84 | `canonical_to_apocrypha` | MAT 1:1 | `generation` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3 |
| 51 | `span_exact` | `gate` | -98 | `canonical_to_apocrypha` | MAT 1:1 | `jesus` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3 |
| 52 | `span_exact` | `seed` | -115 | `apocrypha_to_canonical` | MAL 4:6 | `and` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 53 | `span_exact` | `gate` | -116 | `canonical_to_apocrypha` | MAT 1:1 | `the` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3 |
| 54 | `span_exact` | `horn` | 126 | `apocrypha_to_canonical` | MAT 1:2 | `isaac` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5 |
| 55 | `span_exact` | `horn` | -127 | `canonical_to_apocrypha` | 2ES 16:78 | `fire` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3 |
| 56 | `span_exact` | `heart` | -130 | `apocrypha_to_canonical` | MAL 4:5 | `great` | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 57 | `span_exact` | `lord` | -145 | `apocrypha_to_canonical` | TOB 1:1 | `tobit` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 58 | `span_exact` | `life` | -159 | `apocrypha_to_canonical` | TOB 1:1 | `the` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 59 | `span_exact` | `rent` | 165 | `canonical_to_apocrypha` | TOB 1:2 | `which` | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 60 | `span_exact` | `heart` | -165 | `apocrypha_to_canonical` | TOB 1:2 | `assyrians` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 61 | `span_exact` | `fire` | 176 | `apocrypha_to_canonical` | 2ES 16:77 | `may` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3 |
| 62 | `span_exact` | `heart` | -178 | `apocrypha_to_canonical` | MAL 4:4 | `commanded` | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 63 | `span_exact` | `seed` | -178 | `apocrypha_to_canonical` | MAL 4:5 | `dreadful` | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 64 | `span_exact` | `hand` | -188 | `canonical_to_apocrypha` | 2ES 16:77 | `their` | 2ES 16:74;2ES 16:75;2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2 |
| 65 | `span_exact` | `seed` | 189 | `canonical_to_apocrypha` | MAL 4:5 | `behold` | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 66 | `span_exact` | `earth` | 191 | `apocrypha_to_canonical` | 2ES 16:75 | `afraid` | 2ES 16:70;2ES 16:71;2ES 16:72;2ES 16:73;2ES 16:74;2ES 16:75;2ES 16:76;2ES 16:... |
| 67 | `span_exact` | `heart` | 194 | `canonical_to_apocrypha` | MAL 4:5 | `elijah` | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 68 | `span_exact` | `hand` | -206 | `apocrypha_to_canonical` | TOB 1:1 | `son` | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 69 | `span_exact` | `obed` | -207 | `canonical_to_apocrypha` | 2ES 16:78 | `and` | 2ES 16:75;2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5 |
| 70 | `span_exact` | `horn` | 208 | `apocrypha_to_canonical` | MAT 1:2 | `isaac` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6 |
| 71 | `span_exact` | `gate` | -212 | `canonical_to_apocrypha` | MAT 1:1 | `the` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6 |
| 72 | `span_exact` | `heal` | 214 | `canonical_to_apocrypha` | MAL 4:4 | `law` | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 73 | `span_exact` | `gate` | -218 | `canonical_to_apocrypha` | MAT 1:1 | `david` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6 |
| 74 | `span_exact` | `obed` | -224 | `canonical_to_apocrypha` | 2ES 16:78 | `undressed` | 2ES 16:75;2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5 |
| 75 | `span_exact` | `rent` | 228 | `canonical_to_apocrypha` | TOB 1:2 | `right` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 76 | `span_exact` | `life` | -234 | `apocrypha_to_canonical` | TOB 1:2 | `the` | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 77 | `span_exact` | `life` | -236 | `apocrypha_to_canonical` | TOB 1:2 | `that` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 78 | `span_exact` | `seed` | -238 | `apocrypha_to_canonical` | MAL 4:6 | `their` | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 79 | `span_exact` | `ruth` | -242 | `apocrypha_to_canonical` | TOB 1:2 | `is` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 80 | `span_exact` | `obed` | -245 | `canonical_to_apocrypha` | 2ES 16:78 | `left` | 2ES 16:74;2ES 16:75;2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT... |
| ... | ... | ... | ... | ... | ... | ... | 455 more rows in CSV |

## Read

- `center_word_exact` is the rare direct case: hidden term text is also
  present in the surface word containing the ELS center.
- same-concept and same-category rows are broader review queues, not
  interpretation claims.
- `hidden_path_only` means the bridge exists, but this pass did not find
  declared surface-term support at the center or span level.
