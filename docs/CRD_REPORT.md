# CRD Report

Status: generated from the Centered-Relevance Density matrix.

## Reproduce

```bash
python3 -m scripts.run_crd_density protocols/centered_relevance_density.toml --resume
python3 -m scripts.build_crd_comparison
```

## Summary

- density rows: 80
- term/control comparison rows: 10
- edition summary rows: 8
- classifier agreement rows: 0
- rows with secular max density = 0: 9
- manifest status: completed

## Bible vs Secular Controls

| Classifier | Term | Bible max | Secular max | Ratio | Exceeds secular max |
| --- | --- | ---: | ---: | ---: | --- |
| deterministic | `חזון` (chazon; English: vision)<br>`vision_h` | 11.6954961 | 0.179491289 | 65.1591293 | true |
| deterministic | `דריוש` (Daryavesh; English: Darius)<br>`darius_h` | 42.6050214 | 0 |  | true |
| deterministic | `מגוג` (Magog; English: Magog)<br>`magog_h` | 20.0494218 | 0 |  | true |
| deterministic | `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | 19.2140292 | 0 |  | true |
| deterministic | `גוג` (Gog; English: Gog)<br>`gog_h` | 10.0247109 | 0 |  | true |
| deterministic | `קרן` (qeren; English: horn)<br>`horn_h` | 5.84774803 | 0 |  | true |
| deterministic | `נביא` (navi; English: prophet)<br>`prophet_h` | 3.3415703 | 0 |  | true |
| deterministic | `חותם` (chotam; English: seal)<br>`seal_h` | 2.50617773 | 0 |  | true |
| deterministic | `חיה` (chayah; English: beast/living creature)<br>`beast_h` | 0 | 0 |  | false |
| deterministic | `תנין` (tannin; English: dragon/sea monster)<br>`dragon_h` | 0 | 0 |  | false |

## Top Finite Bible-Vs-Control Ratios

| Classifier | Term | Bible max | Bible corpus | Secular max | Secular corpus | Ratio |
| --- | --- | ---: | --- | ---: | --- | ---: |
| deterministic | `חזון` (chazon; English: vision)<br>`vision_h` | 11.6954961 | MT_WLC | 0.179491289 | HEB_PBY_BRENNER | 65.1591293 |

## Top Bible Hits With Secular Max Zero

| Classifier | Term | Bible max | Bible corpus |
| --- | --- | ---: | --- |
| deterministic | `דריוש` (Daryavesh; English: Darius)<br>`darius_h` | 42.6050214 | MT_WLC |
| deterministic | `מגוג` (Magog; English: Magog)<br>`magog_h` | 20.0494218 | MT_WLC |
| deterministic | `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | 19.2140292 | MT_WLC |
| deterministic | `גוג` (Gog; English: Gog)<br>`gog_h` | 10.0247109 | MT_WLC |
| deterministic | `קרן` (qeren; English: horn)<br>`horn_h` | 5.84774803 | MT_WLC |
| deterministic | `נביא` (navi; English: prophet)<br>`prophet_h` | 3.3415703 | MT_WLC |
| deterministic | `חותם` (chotam; English: seal)<br>`seal_h` | 2.50617773 | MT_WLC |

## Relevance Scope Summary

| Classifier | Corpus class | Term | Scope | Relevant hits |
| --- | --- | --- | --- | ---: |
| deterministic | bible | `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | center_word | 10 |
| deterministic | bible | `דריוש` (Daryavesh; English: Darius)<br>`darius_h` | center_word | 9 |
| deterministic | secular_control | `חזון` (chazon; English: vision)<br>`vision_h` | center_word | 1 |
| deterministic | bible | `דריוש` (Daryavesh; English: Darius)<br>`darius_h` | center_verse | 79 |
| deterministic | bible | `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | center_verse | 71 |
| deterministic | bible | `מגוג` (Magog; English: Magog)<br>`magog_h` | center_verse | 35 |
| deterministic | bible | `גוג` (Gog; English: Gog)<br>`gog_h` | center_verse | 30 |
| deterministic | bible | `קרן` (qeren; English: horn)<br>`horn_h` | center_verse | 27 |
| deterministic | bible | `חזון` (chazon; English: vision)<br>`vision_h` | center_verse | 12 |
| deterministic | bible | `נביא` (navi; English: prophet)<br>`prophet_h` | center_verse | 10 |
| deterministic | bible | `חותם` (chotam; English: seal)<br>`seal_h` | center_verse | 5 |
| deterministic | bible | `דריוש` (Daryavesh; English: Darius)<br>`darius_h` | span | 130 |
| deterministic | bible | `מגוג` (Magog; English: Magog)<br>`magog_h` | span | 67 |
| deterministic | bible | `חזון` (chazon; English: vision)<br>`vision_h` | span | 25 |
| deterministic | bible | `גוג` (Gog; English: Gog)<br>`gog_h` | span | 20 |
| deterministic | bible | `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | span | 15 |
| deterministic | bible | `חותם` (chotam; English: seal)<br>`seal_h` | span | 2 |
| deterministic | bible | `מגוג` (Magog; English: Magog)<br>`magog_h` | verse_ref_match | 9 |
| deterministic | bible | `דריוש` (Daryavesh; English: Darius)<br>`darius_h` | verse_ref_match | 6 |
| deterministic | bible | `חזון` (chazon; English: vision)<br>`vision_h` | verse_ref_match | 5 |
| deterministic | bible | `קרן` (qeren; English: horn)<br>`horn_h` | verse_ref_match | 3 |
| deterministic | bible | `חותם` (chotam; English: seal)<br>`seal_h` | verse_ref_match | 3 |

## Representative Relevant Centers

| Term | Corpus | Center ref | Center word | Type | Scope | Matched keyword | Skip |
| --- | --- | --- | --- | --- | --- | --- | ---: |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | 1KI 9:15 | `וְזֶ֨ה` (wzh) | surface_keyword_match | center_verse | `ירושלם` (Yerushalem; English: Jerusalem) | 5 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | 2CH 12:11 | `בָּ֤אוּ` (bw) | surface_keyword_match | center_verse | `בית יהוה` (beit YHWH; English: house of YHWH) | 6 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | 2CH 32:9 | `יְר֣וּשָׁלַ֔יְמָה` (yrwshlymh) | surface_keyword_match | center_verse | `מלך` (melekh; English: king) | -9 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | 2CH 35:24 | `יְר֣וּשָׁלִַ֔ם` (Yerushalem; English: Jerusalem) | surface_keyword_match | center_word | `ירושלם` (Yerushalem; English: Jerusalem) | 2 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | 2CH 36:2 | `שָׁנָ֖ה` (shnh) | surface_keyword_match | center_verse | `מלך` (melekh; English: king) | -7 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | 2KI 16:3 | `וַיֵּ֕לֶךְ` (wylk) | surface_keyword_match | span | `מלך` (melekh; English: king) | 7 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | 2KI 17:2 | `בְּעֵינֵ֣י` (byny) | surface_keyword_match | span | `מלך` (melekh; English: king) | -9 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | 2KI 18:31 | `וּצְא֣וּ` (wtsw) | surface_keyword_match | center_verse | `מלך` (melekh; English: king) | -6 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | 2KI 23:12 | `בֵּית־יְהוָ֖ה` (beit YHWH; English: house of YHWH) | surface_keyword_match | center_word | `בית יהוה` (beit YHWH; English: house of YHWH) | -8 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | 2SA 20:22 | `אֶת־רֹ֨אשׁ` (trsh) | surface_keyword_match | center_verse | `ירושלם` (Yerushalem; English: Jerusalem) | 3 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | 2SA 20:3 | `בֵּית־מִשְׁמֶ֨רֶת֙` (bytmshmrt) | surface_keyword_match | center_verse | `ירושלם` (Yerushalem; English: Jerusalem) | -2 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | 2SA 6:20 | `אֶת־בֵּית֑וֹ` (tbytw) | surface_keyword_match | center_verse | `מלך` (melekh; English: king) | -7 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | EZR 4:7 | `עַל־ארתחששתא` (lrtchshsht) | surface_keyword_match | center_verse | `פרס` (Paras; English: Persia) | 4 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | JER 25:3 | `דְבַר־יְהוָ֖ה` (dbryhwh) | surface_keyword_match | center_verse | `מלך` (melekh; English: king) | -8 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | JER 50:17 | `עִצְּמ֔וֹ` (tsmw) | surface_keyword_match | center_verse | `מלך` (melekh; English: king) | -9 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | JOS 10:1 | `לִֽירִיחוֹ֙` (lyrychw) | surface_keyword_match | center_verse | `מלך` (melekh; English: king) | -4 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | EBIBLE_WLC | JOS 2:2 | `אֶת־הָאָֽרֶץ׃` (thrts) | surface_keyword_match | span | `מלך` (melekh; English: king) | -7 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | MAM | 1 Kgs 9:15 | `וְזֶ֨ה` (wzh) | surface_keyword_match | center_verse | `ירושלם` (Yerushalem; English: Jerusalem) | 5 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | MAM | 2 Chr 12:11 | `בָּ֤אוּ` (bw) | surface_keyword_match | center_verse | `בית יהוה` (beit YHWH; English: house of YHWH) | 6 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | MAM | 2 Chr 32:9 | `יְר֣וּשָׁלַ֔יְמָה` (yrwshlymh) | surface_keyword_match | center_verse | `מלך` (melekh; English: king) | -9 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | MAM | 2 Chr 35:24 | `יְר֣וּשָׁלַ֔͏ִם` (Yerushalem; English: Jerusalem) | surface_keyword_match | center_word | `ירושלם` (Yerushalem; English: Jerusalem) | 2 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | MAM | 2 Chr 36:2 | `שָׁנָ֖ה` (shnh) | surface_keyword_match | center_verse | `מלך` (melekh; English: king) | -7 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | MAM | 2 Kgs 16:3 | `וַיֵּ֕לֶךְ` (wylk) | surface_keyword_match | span | `מלך` (melekh; English: king) | 7 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | MAM | 2 Kgs 17:2 | `בְּעֵינֵ֣י` (byny) | surface_keyword_match | span | `מלך` (melekh; English: king) | -9 |
| `כורש` (Koresh; English: Cyrus)<br>`cyrus_h` | MAM | 2 Kgs 18:31 | `וּצְא֣וּ` (wtsw) | surface_keyword_match | center_verse | `מלך` (melekh; English: king) | -6 |

## Read

- CRD is a density screen, not a claim promotion engine.
- Deterministic mode only reports locked exact dictionary matches.
- Concept-code matches require explicit surface/context concept fields; hidden-term metadata alone is not counted.
- Secular-control zeroes can reflect dictionary vocabulary and context coverage, not only signal strength.
- LLM and parallel modes require audit-log review before interpretation.
- Interpret results only against the dictionary and preregistration hashes recorded in the manifest.
