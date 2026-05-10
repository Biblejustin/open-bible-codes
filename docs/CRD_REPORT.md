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
| deterministic | `vision_h` | 11.6954961 | 0.179491289 | 65.1591293 | true |
| deterministic | `darius_h` | 42.6050214 | 0 |  | true |
| deterministic | `magog_h` | 20.0494218 | 0 |  | true |
| deterministic | `cyrus_h` | 19.2140292 | 0 |  | true |
| deterministic | `gog_h` | 10.0247109 | 0 |  | true |
| deterministic | `horn_h` | 5.84774803 | 0 |  | true |
| deterministic | `prophet_h` | 3.3415703 | 0 |  | true |
| deterministic | `seal_h` | 2.50617773 | 0 |  | true |
| deterministic | `beast_h` | 0 | 0 |  | false |
| deterministic | `dragon_h` | 0 | 0 |  | false |

## Top Finite Bible-Vs-Control Ratios

| Classifier | Term | Bible max | Bible corpus | Secular max | Secular corpus | Ratio |
| --- | --- | ---: | --- | ---: | --- | ---: |
| deterministic | `vision_h` | 11.6954961 | MT_WLC | 0.179491289 | HEB_PBY_BRENNER | 65.1591293 |

## Top Bible Hits With Secular Max Zero

| Classifier | Term | Bible max | Bible corpus |
| --- | --- | ---: | --- |
| deterministic | `darius_h` | 42.6050214 | MT_WLC |
| deterministic | `magog_h` | 20.0494218 | MT_WLC |
| deterministic | `cyrus_h` | 19.2140292 | MT_WLC |
| deterministic | `gog_h` | 10.0247109 | MT_WLC |
| deterministic | `horn_h` | 5.84774803 | MT_WLC |
| deterministic | `prophet_h` | 3.3415703 | MT_WLC |
| deterministic | `seal_h` | 2.50617773 | MT_WLC |

## Relevance Scope Summary

| Classifier | Corpus class | Term | Scope | Relevant hits |
| --- | --- | --- | --- | ---: |
| deterministic | bible | `cyrus_h` | center_word | 10 |
| deterministic | bible | `darius_h` | center_word | 9 |
| deterministic | secular_control | `vision_h` | center_word | 1 |
| deterministic | bible | `darius_h` | center_verse | 79 |
| deterministic | bible | `cyrus_h` | center_verse | 71 |
| deterministic | bible | `magog_h` | center_verse | 35 |
| deterministic | bible | `gog_h` | center_verse | 30 |
| deterministic | bible | `horn_h` | center_verse | 27 |
| deterministic | bible | `vision_h` | center_verse | 12 |
| deterministic | bible | `prophet_h` | center_verse | 10 |
| deterministic | bible | `seal_h` | center_verse | 5 |
| deterministic | bible | `darius_h` | span | 130 |
| deterministic | bible | `magog_h` | span | 67 |
| deterministic | bible | `vision_h` | span | 25 |
| deterministic | bible | `gog_h` | span | 20 |
| deterministic | bible | `cyrus_h` | span | 15 |
| deterministic | bible | `seal_h` | span | 2 |
| deterministic | bible | `magog_h` | verse_ref_match | 9 |
| deterministic | bible | `darius_h` | verse_ref_match | 6 |
| deterministic | bible | `vision_h` | verse_ref_match | 5 |
| deterministic | bible | `horn_h` | verse_ref_match | 3 |
| deterministic | bible | `seal_h` | verse_ref_match | 3 |

## Representative Relevant Centers

| Term | Corpus | Center ref | Center word | Type | Scope | Matched keyword | Skip |
| --- | --- | --- | --- | --- | --- | --- | ---: |
| `cyrus_h` | EBIBLE_WLC | 1KI 9:15 | וְזֶ֨ה | surface_keyword_match | center_verse | ירושלם | 5 |
| `cyrus_h` | EBIBLE_WLC | 2CH 12:11 | בָּ֤אוּ | surface_keyword_match | center_verse | בית יהוה | 6 |
| `cyrus_h` | EBIBLE_WLC | 2CH 32:9 | יְר֣וּשָׁלַ֔יְמָה | surface_keyword_match | center_verse | מלך | -9 |
| `cyrus_h` | EBIBLE_WLC | 2CH 35:24 | יְר֣וּשָׁלִַ֔ם | surface_keyword_match | center_word | ירושלם | 2 |
| `cyrus_h` | EBIBLE_WLC | 2CH 36:2 | שָׁנָ֖ה | surface_keyword_match | center_verse | מלך | -7 |
| `cyrus_h` | EBIBLE_WLC | 2KI 16:3 | וַיֵּ֕לֶךְ | surface_keyword_match | span | מלך | 7 |
| `cyrus_h` | EBIBLE_WLC | 2KI 17:2 | בְּעֵינֵ֣י | surface_keyword_match | span | מלך | -9 |
| `cyrus_h` | EBIBLE_WLC | 2KI 18:31 | וּצְא֣וּ | surface_keyword_match | center_verse | מלך | -6 |
| `cyrus_h` | EBIBLE_WLC | 2KI 23:12 | בֵּית־יְהוָ֖ה | surface_keyword_match | center_word | בית יהוה | -8 |
| `cyrus_h` | EBIBLE_WLC | 2SA 20:22 | אֶת־רֹ֨אשׁ | surface_keyword_match | center_verse | ירושלם | 3 |
| `cyrus_h` | EBIBLE_WLC | 2SA 20:3 | בֵּית־מִשְׁמֶ֨רֶת֙ | surface_keyword_match | center_verse | ירושלם | -2 |
| `cyrus_h` | EBIBLE_WLC | 2SA 6:20 | אֶת־בֵּית֑וֹ | surface_keyword_match | center_verse | מלך | -7 |
| `cyrus_h` | EBIBLE_WLC | EZR 4:7 | עַל־ארתחששתא | surface_keyword_match | center_verse | פרס | 4 |
| `cyrus_h` | EBIBLE_WLC | JER 25:3 | דְבַר־יְהוָ֖ה | surface_keyword_match | center_verse | מלך | -8 |
| `cyrus_h` | EBIBLE_WLC | JER 50:17 | עִצְּמ֔וֹ | surface_keyword_match | center_verse | מלך | -9 |
| `cyrus_h` | EBIBLE_WLC | JOS 10:1 | לִֽירִיחוֹ֙ | surface_keyword_match | center_verse | מלך | -4 |
| `cyrus_h` | EBIBLE_WLC | JOS 2:2 | אֶת־הָאָֽרֶץ׃ | surface_keyword_match | span | מלך | -7 |
| `cyrus_h` | MAM | 1 Kgs 9:15 | וְזֶ֨ה | surface_keyword_match | center_verse | ירושלם | 5 |
| `cyrus_h` | MAM | 2 Chr 12:11 | בָּ֤אוּ | surface_keyword_match | center_verse | בית יהוה | 6 |
| `cyrus_h` | MAM | 2 Chr 32:9 | יְר֣וּשָׁלַ֔יְמָה | surface_keyword_match | center_verse | מלך | -9 |
| `cyrus_h` | MAM | 2 Chr 35:24 | יְר֣וּשָׁלַ֔͏ִם | surface_keyword_match | center_word | ירושלם | 2 |
| `cyrus_h` | MAM | 2 Chr 36:2 | שָׁנָ֖ה | surface_keyword_match | center_verse | מלך | -7 |
| `cyrus_h` | MAM | 2 Kgs 16:3 | וַיֵּ֕לֶךְ | surface_keyword_match | span | מלך | 7 |
| `cyrus_h` | MAM | 2 Kgs 17:2 | בְּעֵינֵ֣י | surface_keyword_match | span | מלך | -9 |
| `cyrus_h` | MAM | 2 Kgs 18:31 | וּצְא֣וּ | surface_keyword_match | center_verse | מלך | -6 |

## Read

- CRD is a density screen, not a claim promotion engine.
- Deterministic mode only reports locked exact dictionary matches.
- Concept-code matches require explicit surface/context concept fields; hidden-term metadata alone is not counted.
- Secular-control zeroes can reflect dictionary vocabulary and context coverage, not only signal strength.
- LLM and parallel modes require audit-log review before interpretation.
- Interpret results only against the dictionary and preregistration hashes recorded in the manifest.
