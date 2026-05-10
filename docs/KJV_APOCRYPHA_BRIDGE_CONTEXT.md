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

- candidate rows: 350
- context rows: 350
- terms with context rows: 81
- center_word_exact: 0 rows / 0 terms
- center_word_same_concept: 0 rows / 0 terms
- center_word_same_category: 1 rows / 1 terms
- center_verse_exact: 4 rows / 4 terms
- center_verse_same_concept: 0 rows / 0 terms
- center_verse_same_category: 28 rows / 22 terms
- span_exact: 17 rows / 8 terms
- span_same_concept: 0 rows / 0 terms
- span_same_category: 72 rows / 37 terms
- hidden_path_only: 228 rows / 59 terms

## Highest-Priority Rows

| Rank | Bucket | Term | Skip | Bridge | Center | Center word | Span refs |
| ---: | --- | --- | ---: | --- | --- | --- | --- |
| 1 | `center_word_same_category` | `aids` | -121 | `canonical_to_apocrypha` | 2ES 16:77 | `bushes` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2 |
| 2 | `center_verse_exact` | `isaac` | 86 | `apocrypha_to_canonical` | MAT 1:2 | `judas` | 2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5 |
| 3 | `center_verse_exact` | `aram` | -148 | `canonical_to_apocrypha` | MAT 1:4 | `begat` | 2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7 |
| 4 | `center_verse_exact` | `bush` | 203 | `apocrypha_to_canonical` | 2ES 16:77 | `a` | 2ES 16:74;2ES 16:75;2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3 |
| 5 | `center_verse_exact` | `hand` | -243 | `canonical_to_apocrypha` | MAT 1:5 | `begat` | 2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7;MAT 1:8;MAT... |
| 6 | `center_verse_same_category` | `hand` | 40 | `canonical_to_apocrypha` | MAL 4:6 | `their` | MAL 4:6;TOB 1:1 |
| 7 | `center_verse_same_category` | `star` | -84 | `canonical_to_apocrypha` | 2ES 16:77 | `man` | 2ES 16:77;2ES 16:78;MAT 1:1 |
| 8 | `center_verse_same_category` | `light` | -127 | `apocrypha_to_canonical` | TOB 1:2 | `galilee` | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 9 | `center_verse_same_category` | `admah` | -131 | `canonical_to_apocrypha` | MAT 1:4 | `salmon` | 2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7;MAT 1:8;MAT... |
| 10 | `center_verse_same_category` | `tomb` | 134 | `apocrypha_to_canonical` | 2ES 16:77 | `field` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1 |
| 11 | `center_verse_same_category` | `eyes` | -143 | `canonical_to_apocrypha` | 2ES 16:77 | `field` | 2ES 16:75;2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2 |
| 12 | `center_verse_same_category` | `iran` | 145 | `canonical_to_apocrypha` | TOB 1:2 | `city` | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 13 | `center_verse_same_category` | `ahab` | 145 | `apocrypha_to_canonical` | MAT 1:1 | `generation` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4 |
| 14 | `center_verse_same_category` | `seba` | 169 | `apocrypha_to_canonical` | MAT 1:4 | `begat` | 2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7 |
| 15 | `center_verse_same_category` | `isaac` | 174 | `canonical_to_apocrypha` | MAL 4:5 | `day` | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 16 | `center_verse_same_category` | `seba` | 179 | `apocrypha_to_canonical` | MAT 1:4 | `aminadab` | 2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7;MAT 1:8 |
| 17 | `center_verse_same_category` | `rome` | 184 | `canonical_to_apocrypha` | TOB 1:2 | `nephthali` | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 18 | `center_verse_same_category` | `hail` | 185 | `apocrypha_to_canonical` | 2ES 16:78 | `be` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4 |
| 19 | `center_verse_same_category` | `nato` | -186 | `apocrypha_to_canonical` | TOB 1:2 | `was` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 20 | `center_verse_same_category` | `king` | -192 | `apocrypha_to_canonical` | MAL 4:5 | `the` | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 21 | `center_verse_same_category` | `house` | 196 | `canonical_to_apocrypha` | TOB 1:3 | `justice` | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4;TOB 1:5 |
| 22 | `center_verse_same_category` | `tyre` | 198 | `canonical_to_apocrypha` | TOB 1:2 | `galilee` | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 23 | `center_verse_same_category` | `seba` | 203 | `apocrypha_to_canonical` | MAT 1:3 | `and` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7 |
| 24 | `center_verse_same_category` | `noah` | -204 | `canonical_to_apocrypha` | MAT 1:4 | `and` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7;M... |
| 25 | `center_verse_same_category` | `hand` | 205 | `canonical_to_apocrypha` | MAL 4:6 | `lest` | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 26 | `center_verse_same_category` | `obal` | -210 | `canonical_to_apocrypha` | MAT 1:3 | `begat` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7;M... |
| 27 | `center_verse_same_category` | `love` | 222 | `canonical_to_apocrypha` | TOB 1:2 | `of` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 28 | `center_verse_same_category` | `elam` | 222 | `canonical_to_apocrypha` | TOB 1:2 | `at` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 29 | `center_verse_same_category` | `lion` | 226 | `apocrypha_to_canonical` | 2ES 16:77 | `may` | 2ES 16:74;2ES 16:75;2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT... |
| 30 | `center_verse_same_category` | `nato` | -245 | `apocrypha_to_canonical` | MAL 4:4 | `statutes` | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 31 | `center_verse_same_category` | `nato` | 246 | `canonical_to_apocrypha` | MAL 4:4 | `the` | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 32 | `center_verse_same_category` | `sign` | 248 | `canonical_to_apocrypha` | TOB 1:1 | `of` | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 33 | `center_verse_same_category` | `rome` | 250 | `canonical_to_apocrypha` | TOB 1:2 | `properly` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 34 | `span_exact` | `horn` | 126 | `apocrypha_to_canonical` | MAT 1:2 | `isaac` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5 |
| 35 | `span_exact` | `horn` | -127 | `canonical_to_apocrypha` | 2ES 16:78 | `fire` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3 |
| 36 | `span_exact` | `heart` | -130 | `apocrypha_to_canonical` | MAL 4:5 | `great` | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 37 | `span_exact` | `lord` | -145 | `apocrypha_to_canonical` | TOB 1:1 | `tobit` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 38 | `span_exact` | `life` | -159 | `apocrypha_to_canonical` | TOB 1:1 | `the` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 39 | `span_exact` | `heart` | -165 | `apocrypha_to_canonical` | TOB 1:2 | `assyrians` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 40 | `span_exact` | `fire` | 176 | `apocrypha_to_canonical` | 2ES 16:77 | `may` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3 |
| 41 | `span_exact` | `heart` | -178 | `apocrypha_to_canonical` | MAL 4:4 | `commanded` | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 42 | `span_exact` | `hand` | -188 | `canonical_to_apocrypha` | 2ES 16:77 | `their` | 2ES 16:74;2ES 16:75;2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2 |
| 43 | `span_exact` | `earth` | 191 | `apocrypha_to_canonical` | 2ES 16:75 | `afraid` | 2ES 16:70;2ES 16:71;2ES 16:72;2ES 16:73;2ES 16:74;2ES 16:75;2ES 16:76;2ES 16:... |
| 44 | `span_exact` | `heart` | 194 | `canonical_to_apocrypha` | MAL 4:5 | `elijah` | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 45 | `span_exact` | `hand` | -206 | `apocrypha_to_canonical` | TOB 1:1 | `son` | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 46 | `span_exact` | `horn` | 208 | `apocrypha_to_canonical` | MAT 1:2 | `isaac` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6 |
| 47 | `span_exact` | `heal` | 214 | `canonical_to_apocrypha` | MAL 4:4 | `law` | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 48 | `span_exact` | `life` | -234 | `apocrypha_to_canonical` | TOB 1:2 | `the` | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 49 | `span_exact` | `life` | -236 | `apocrypha_to_canonical` | TOB 1:2 | `that` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 50 | `span_exact` | `life` | 250 | `canonical_to_apocrypha` | MAL 4:6 | `i` | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 51 | `span_same_category` | `eber` | -75 | `canonical_to_apocrypha` | MAT 1:1 | `jesus` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3 |
| 52 | `span_same_category` | `torah` | -81 | `apocrypha_to_canonical` | MAL 4:6 | `heart` | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 53 | `span_same_category` | `torah` | -85 | `apocrypha_to_canonical` | MAL 4:5 | `great` | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 54 | `span_same_category` | `mash` | -90 | `canonical_to_apocrypha` | MAT 1:2 | `begat` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4 |
| 55 | `span_same_category` | `eber` | 110 | `apocrypha_to_canonical` | MAT 1:2 | `his` | 2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5 |
| 56 | `span_same_category` | `obal` | -111 | `canonical_to_apocrypha` | MAT 1:1 | `generation` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3 |
| 57 | `span_same_category` | `haifa` | -121 | `apocrypha_to_canonical` | MAL 4:6 | `i` | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 58 | `span_same_category` | `sign` | -121 | `apocrypha_to_canonical` | TOB 1:2 | `enemessar` | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 59 | `span_same_category` | `eber` | -136 | `canonical_to_apocrypha` | MAT 1:2 | `begat` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5 |
| 60 | `span_same_category` | `hand` | -141 | `apocrypha_to_canonical` | MAL 4:5 | `behold` | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 61 | `span_same_category` | `house` | -142 | `canonical_to_apocrypha` | 2ES 16:77 | `iniquities` | 2ES 16:74;2ES 16:75;2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2 |
| 62 | `span_same_category` | `hail` | -149 | `canonical_to_apocrypha` | 2ES 16:76 | `themselves` | 2ES 16:74;2ES 16:75;2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1 |
| 63 | `span_same_category` | `seba` | 157 | `apocrypha_to_canonical` | 2ES 16:77 | `man` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3 |
| 64 | `span_same_category` | `eber` | 160 | `apocrypha_to_canonical` | 2ES 16:78 | `undressed` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3 |
| 65 | `span_same_category` | `ahab` | -161 | `apocrypha_to_canonical` | TOB 1:1 | `son` | MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 66 | `span_same_category` | `heth` | 163 | `canonical_to_apocrypha` | MAL 4:4 | `judgments` | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 67 | `span_same_category` | `sheba` | 166 | `apocrypha_to_canonical` | MAT 1:2 | `begat` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6... |
| 68 | `span_same_category` | `ahab` | -169 | `apocrypha_to_canonical` | TOB 1:1 | `the` | MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3 |
| 69 | `span_same_category` | `dedan` | -170 | `apocrypha_to_canonical` | MAL 4:6 | `and` | MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 70 | `span_same_category` | `heth` | -172 | `canonical_to_apocrypha` | MAT 1:1 | `son` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5 |
| 71 | `span_same_category` | `heth` | -177 | `canonical_to_apocrypha` | MAT 1:2 | `jacob` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6 |
| 72 | `span_same_category` | `heth` | 179 | `canonical_to_apocrypha` | MAL 4:4 | `which` | MAL 4:1;MAL 4:2;MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1 |
| 73 | `span_same_category` | `bear` | -180 | `canonical_to_apocrypha` | MAT 1:3 | `and` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7 |
| 74 | `span_same_category` | `holy` | 183 | `canonical_to_apocrypha` | TOB 1:2 | `is` | MAL 4:6;TOB 1:1;TOB 1:2;TOB 1:3;TOB 1:4 |
| 75 | `span_same_category` | `heth` | 187 | `apocrypha_to_canonical` | MAT 1:5 | `booz` | 2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7;MAT 1:8;MAT... |
| 76 | `span_same_category` | `hail` | 189 | `canonical_to_apocrypha` | MAL 4:5 | `the` | MAL 4:3;MAL 4:4;MAL 4:5;MAL 4:6;TOB 1:1;TOB 1:2 |
| 77 | `span_same_category` | `ahab` | 192 | `apocrypha_to_canonical` | 2ES 16:78 | `consumed` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5 |
| 78 | `span_same_category` | `resen` | 193 | `apocrypha_to_canonical` | 2ES 16:76 | `iniquities` | 2ES 16:71;2ES 16:72;2ES 16:73;2ES 16:74;2ES 16:75;2ES 16:76;2ES 16:77;2ES 16:... |
| 79 | `span_same_category` | `star` | 194 | `apocrypha_to_canonical` | MAT 1:1 | `generation` | 2ES 16:76;2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5 |
| 80 | `span_same_category` | `image` | 195 | `apocrypha_to_canonical` | MAT 1:5 | `and` | 2ES 16:77;2ES 16:78;MAT 1:1;MAT 1:2;MAT 1:3;MAT 1:4;MAT 1:5;MAT 1:6;MAT 1:7;M... |
| ... | ... | ... | ... | ... | ... | ... | 270 more rows in CSV |

## Read

- `center_word_exact` is the rare direct case: hidden term text is also
  present in the surface word containing the ELS center.
- same-concept and same-category rows are broader review queues, not
  interpretation claims.
- `hidden_path_only` means the bridge exists, but this pass did not find
  declared surface-term support at the center or span level.
