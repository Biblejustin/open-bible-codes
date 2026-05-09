# Hebrew Theology All-Codes Triage

This is a compact review queue built from the relaxed all-codes export.
It ranks same center-word rows first, then related center-word rows,
center-verse rows, span rows, and finally hidden-path-only rows.

It is a triage aid, not a claim-grade filter.

## Inputs

- Hits: `reports/hebrew_theology_all_codes/surface_all_codes.csv`
- Summary: `reports/hebrew_theology_all_codes/surface_all_codes_summary.csv`
- Queue CSV: `reports/hebrew_theology_all_codes/triage_queue.csv`
- Corpora: `EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC`

## Counts

| Metric | Count |
| --- | ---: |
| Raw rows scanned | 305,353 |
| Queue rows | 700 |
| `center_word_exact` queue rows | 100 |
| `center_word_same_concept` queue rows | 0 |
| `center_word_same_category` queue rows | 100 |
| `center_verse_exact` queue rows | 100 |
| `center_verse_same_concept` queue rows | 0 |
| `center_verse_same_category` queue rows | 100 |
| `span_exact` queue rows | 100 |
| `span_same_concept` queue rows | 0 |
| `span_same_category` queue rows | 100 |
| `hidden_path_only` queue rows | 100 |

## Top Queue Rows

### center_word_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 1Chr 26:27 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 1Chr 28:20 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 3 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 1Kgs 10:5 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 4 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 1Sam 26:11 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 5 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 1Sam 26:16 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 6 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 1Sam 26:23 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 7 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 1Sam 26:9 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 8 | all_source | `htp_yhwh_h` | YHWH | -3 | 10 | 2Chr 21:7 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 9 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 2Chr 33:15 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 10 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 2Chr 9:4 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 11 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 2Kgs 23:24 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 12 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 2Kgs 25:13 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 13 | all_source | `htp_yhwh_h` | YHWH | -3 | 10 | 2Kgs 8:19 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 14 | all_source | `htp_yhwh_h` | YHWH | -3 | 10 | 2Sam 10:12 | `ויהוה` | paired_uncorrected_p_le_0.05 |
| 15 | all_source | `htp_yhwh_h` | YHWH | -3 | 10 | Isa 48:14 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 16 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | Isa 51:22 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 17 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | Jer 28:6 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 18 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | Jer 52:17 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 19 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | Num 14:44 | `יהוה` | paired_uncorrected_p_le_0.05 |
| 20 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | Ps 32:5 | `ליהוה` | paired_uncorrected_p_le_0.05 |

### center_word_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `htp_torah_h` | Torah | 7 | 22 | 1Chr 5:1 | `בנישראל` | not_unusual |
| 2 | all_source | `htp_torah_h` | Torah | -7 | 22 | 2Kgs 17:20 | `ישראל` | not_unusual |
| 3 | all_source | `htp_covenant_h` | Covenant | 8 | 25 | Deut 34:9 | `חכמה` | not_unusual |
| 4 | all_source | `htp_torah_h` | Torah | 9 | 28 | 1Sam 17:45 | `ישראל` | not_unusual |
| 5 | all_source | `htp_torah_h` | Torah | 13 | 40 | Ezek 48:11 | `ישראל` | not_unusual |
| 6 | all_source | `htp_covenant_h` | Covenant | -13 | 40 | Prov 1:7 | `חכמה` | not_unusual |
| 7 | all_source | `htp_torah_h` | Torah | 14 | 43 | 1Sam 2:22 | `ישראל` | not_unusual |
| 8 | all_source | `htp_torah_h` | Torah | 14 | 43 | Exod 7:5 | `אתבניישראל` | not_unusual |
| 9 | all_source | `htp_love_h` | Love | -15 | 46 | 2Sam 14:30 | `אבשלומ` | not_unusual |
| 10 | all_source | `htp_torah_h` | Torah | -15 | 46 | Isa 45:17 | `ישראל` | not_unusual |
| 11 | all_source | `htp_peace_h` | Peace | -15 | 46 | Song 8:7 | `האהבה` | not_unusual |
| 12 | all_source | `htp_torah_h` | Torah | 16 | 49 | Deut 27:14 | `ישראל` | not_unusual |
| 13 | all_source | `htp_torah_h` | Torah | 16 | 49 | Lev 7:38 | `ישראל` | not_unusual |
| 14 | all_source | `htp_torah_h` | Torah | -16 | 49 | Num 3:40 | `ישראל` | not_unusual |
| 15 | all_source | `htp_torah_h` | Torah | 17 | 52 | 1Kgs 12:20 | `ישראל` | not_unusual |
| 16 | all_source | `htp_torah_h` | Torah | 18 | 55 | Jer 7:3 | `ישראל` | not_unusual |
| 17 | all_source | `htp_glory_h` | Glory | -18 | 55 | Lev 13:57 | `ואמתראה` | not_unusual |
| 18 | all_source | `htp_torah_h` | Torah | 20 | 61 | 1Chr 7:29 | `ישראל` | not_unusual |
| 19 | all_source | `htp_love_h` | Love | -20 | 61 | 2Sam 15:34 | `לאבשלומ` | not_unusual |
| 20 | all_source | `htp_torah_h` | Torah | 22 | 67 | Num 15:32 | `בניישראל` | not_unusual |

### center_verse_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `htp_yhwh_h` | YHWH | 2 | 7 | 1Kgs 2:42 | `הלוא` | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `htp_yhwh_h` | YHWH | 2 | 7 | 1Sam 17:46 | `היומ` | paired_uncorrected_p_le_0.05 |
| 3 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | 2Chr 13:10 | `וכהנימ` | paired_uncorrected_p_le_0.05 |
| 4 | all_source | `htp_yhwh_h` | YHWH | 2 | 7 | 2Chr 20:15 | `ההמונ` | paired_uncorrected_p_le_0.05 |
| 5 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | 2Chr 24:8 | `חוצה` | paired_uncorrected_p_le_0.05 |
| 6 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | 2Kgs 5:11 | `והניפ` | paired_uncorrected_p_le_0.05 |
| 7 | all_source | `htp_yhwh_h` | YHWH | 2 | 7 | Exod 12:14 | `היומ` | paired_uncorrected_p_le_0.05 |
| 8 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | Ezek 45:23 | `עולה` | paired_uncorrected_p_le_0.05 |
| 9 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | Ezek 46:13 | `עולה` | paired_uncorrected_p_le_0.05 |
| 10 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | Ezek 4:3 | `אותה` | paired_uncorrected_p_le_0.05 |
| 11 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | Gen 39:21 | `ויהי` | paired_uncorrected_p_le_0.05 |
| 12 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | Isa 40:2 | `עונה` | paired_uncorrected_p_le_0.05 |
| 13 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | Jer 3:23 | `המונ` | paired_uncorrected_p_le_0.05 |
| 14 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | Lev 10:19 | `היומ` | paired_uncorrected_p_le_0.05 |
| 15 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | Mal 1:13 | `אותה` | paired_uncorrected_p_le_0.05 |
| 16 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | Neh 8:9 | `התורה` | paired_uncorrected_p_le_0.05 |
| 17 | all_source | `htp_yhwh_h` | YHWH | 2 | 7 | Num 10:32 | `הטוב` | paired_uncorrected_p_le_0.05 |
| 18 | all_source | `htp_yhwh_h` | YHWH | 2 | 7 | Zech 1:6 | `הלוא` | paired_uncorrected_p_le_0.05 |
| 19 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | Zech 1:6 | `הלוא` | paired_uncorrected_p_le_0.05 |
| 20 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 1Chr 19:13 | `אלהינו` | paired_uncorrected_p_le_0.05 |

### center_verse_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `htp_torah_h` | Torah | -2 | 7 | 1Sam 6:5 | `הארצ` | not_unusual |
| 2 | all_source | `htp_love_h` | Love | 2 | 7 | 2Sam 14:21 | `הדבר` | not_unusual |
| 3 | all_source | `htp_love_h` | Love | 2 | 7 | 2Sam 15:27 | `שבה` | not_unusual |
| 4 | all_source | `htp_love_h` | Love | 2 | 7 | Exod 18:23 | `הדבר` | not_unusual |
| 5 | all_source | `htp_torah_h` | Torah | -2 | 7 | Ezek 36:10 | `והחרבות` | not_unusual |
| 6 | all_source | `htp_torah_h` | Torah | -2 | 7 | Ezra 10:2 | `הארצ` | not_unusual |
| 7 | all_source | `htp_torah_h` | Torah | -2 | 7 | Jer 7:12 | `וראו` | not_unusual |
| 8 | all_source | `htp_torah_h` | Torah | 3 | 10 | 1Sam 28:19 | `ומחר` | not_unusual |
| 9 | all_source | `htp_torah_h` | Torah | -3 | 10 | 2Chr 31:1 | `האשרימ` | not_unusual |
| 10 | all_source | `htp_torah_h` | Torah | -3 | 10 | 2Kgs 17:23 | `יהוה` | not_unusual |
| 11 | all_source | `htp_torah_h` | Torah | -3 | 10 | 2Kgs 8:12 | `תרטש` | not_unusual |
| 12 | all_source | `htp_torah_h` | Torah | -3 | 10 | Deut 9:1 | `היומ` | not_unusual |
| 13 | all_source | `htp_torah_h` | Torah | -3 | 10 | Exod 10:23 | `במושבתמ` | not_unusual |
| 14 | all_source | `htp_torah_h` | Torah | -3 | 10 | Ezra 7:7 | `והשערימ` | not_unusual |
| 15 | all_source | `htp_wisdom_h` | Wisdom | 3 | 10 | Isa 49:8 | `כה` | not_unusual |
| 16 | all_source | `htp_torah_h` | Torah | 4 | 13 | 1Chr 11:10 | `ואלה` | not_unusual |
| 17 | all_source | `htp_torah_h` | Torah | 4 | 13 | 1Sam 14:45 | `אשר` | not_unusual |
| 18 | all_source | `htp_glory_h` | Glory | -4 | 13 | Ezek 27:16 | `בעזבוניכ` | not_unusual |
| 19 | all_source | `htp_torah_h` | Torah | 4 | 13 | Ezek 7:2 | `הארצ` | not_unusual |
| 20 | all_source | `htp_torah_h` | Torah | 4 | 13 | Ezek 8:12 | `ויאמר` | not_unusual |

### span_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | Neh 8:13 | `התורה` | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 1Chr 28:7 | `הזה` | paired_uncorrected_p_le_0.05 |
| 3 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 1Kgs 3:6 | `הזה` | paired_uncorrected_p_le_0.05 |
| 4 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 1Kgs 8:24 | `הזה` | paired_uncorrected_p_le_0.05 |
| 5 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | 2Chr 6:15 | `הזה` | paired_uncorrected_p_le_0.05 |
| 6 | all_source | `htp_yhwh_h` | YHWH | -3 | 10 | Exod 32:10 | `ועתה` | paired_uncorrected_p_le_0.05 |
| 7 | all_source | `htp_yhwh_h` | YHWH | -3 | 10 | Ezek 22:13 | `והנה` | paired_uncorrected_p_le_0.05 |
| 8 | all_source | `htp_yhwh_h` | YHWH | -3 | 10 | Ezek 2:5 | `והמה` | paired_uncorrected_p_le_0.05 |
| 9 | all_source | `htp_yhwh_h` | YHWH | -3 | 10 | Ezek 30:9 | `ביומ` | paired_uncorrected_p_le_0.05 |
| 10 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | Ezek 44:14 | `בו` | paired_uncorrected_p_le_0.05 |
| 11 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | Ezra 9:7 | `הזה` | paired_uncorrected_p_le_0.05 |
| 12 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | Gen 24:53 | `ויוצא` | paired_uncorrected_p_le_0.05 |
| 13 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | Isa 1:3 | `התבוננ` | paired_uncorrected_p_le_0.05 |
| 14 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | Isa 3:18 | `ביומ` | paired_uncorrected_p_le_0.05 |
| 15 | all_source | `htp_yhwh_h` | YHWH | -3 | 10 | Isa 3:18 | `ביומ` | paired_uncorrected_p_le_0.05 |
| 16 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | Isa 58:6 | `הלוא` | paired_uncorrected_p_le_0.05 |
| 17 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | Jer 44:6 | `הזה` | paired_uncorrected_p_le_0.05 |
| 18 | all_source | `htp_yhwh_h` | YHWH | 3 | 10 | Josh 4:9 | `הזה` | paired_uncorrected_p_le_0.05 |
| 19 | all_source | `htp_yhwh_h` | YHWH | -4 | 13 | Deut 15:3 | `את` | paired_uncorrected_p_le_0.05 |
| 20 | all_source | `htp_yhwh_h` | YHWH | -4 | 13 | Deut 1:44 | `ויצא` | paired_uncorrected_p_le_0.05 |

### span_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `htp_torah_h` | Torah | -2 | 7 | Exod 19:5 | `הארצ` | not_unusual |
| 2 | all_source | `htp_torah_h` | Torah | -2 | 7 | Ezek 39:16 | `הארצ` | not_unusual |
| 3 | all_source | `htp_torah_h` | Torah | -2 | 7 | Josh 13:21 | `הארצ` | not_unusual |
| 4 | all_source | `htp_torah_h` | Torah | 2 | 7 | Lev 17:6 | `וזרק` | not_unusual |
| 5 | all_source | `htp_torah_h` | Torah | 4 | 13 | 1Kgs 8:51 | `הברזל` | not_unusual |
| 6 | all_source | `htp_torah_h` | Torah | 4 | 13 | Exod 30:17 | `וידבר` | not_unusual |
| 7 | all_source | `htp_torah_h` | Torah | 4 | 13 | Exod 34:31 | `ויקרא` | not_unusual |
| 8 | all_source | `htp_torah_h` | Torah | 4 | 13 | Exod 9:8 | `ויאמר` | not_unusual |
| 9 | all_source | `htp_torah_h` | Torah | 4 | 13 | Ezek 9:4 | `ויאמר` | not_unusual |
| 10 | all_source | `htp_love_h` | Love | -4 | 13 | Jer 4:11 | `בעת` | not_unusual |
| 11 | all_source | `htp_torah_h` | Torah | 4 | 13 | Lev 17:1 | `וידבר` | not_unusual |
| 12 | all_source | `htp_torah_h` | Torah | 4 | 13 | Lev 25:1 | `וידבר` | not_unusual |
| 13 | all_source | `htp_torah_h` | Torah | -5 | 16 | 1Sam 8:5 | `אליו` | not_unusual |
| 14 | all_source | `htp_torah_h` | Torah | -6 | 19 | 2Sam 12:6 | `חמל` | not_unusual |
| 15 | all_source | `htp_messiah_h` | Messiah | 6 | 19 | Ezra 2:5 | `ושבעימ` | not_unusual |
| 16 | all_source | `htp_love_h` | Love | -6 | 19 | Jer 34:6 | `ירמיהו` | not_unusual |
| 17 | all_source | `htp_torah_h` | Torah | 6 | 19 | Jer 3:7 | `ואמר` | not_unusual |
| 18 | all_source | `htp_messiah_h` | Messiah | 6 | 19 | Neh 7:10 | `ושנימ` | not_unusual |
| 19 | all_source | `htp_torah_h` | Torah | -7 | 22 | 2Kgs 14:18 | `אמציהו` | not_unusual |
| 20 | all_source | `htp_torah_h` | Torah | 9 | 28 | 2Chr 11:15 | `ולעגלימ` | not_unusual |

### hidden_path_only

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `htp_yhwh_h` | YHWH | 2 | 7 | 1Chr 24:10 | `להקוצ` | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `htp_yhwh_h` | YHWH | 2 | 7 | 1Chr 29:28 | `טובה` | paired_uncorrected_p_le_0.05 |
| 3 | all_source | `htp_yhwh_h` | YHWH | 2 | 7 | 1Kgs 13:24 | `וימיתהו` | paired_uncorrected_p_le_0.05 |
| 4 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | 1Kgs 8:8 | `החוצה` | paired_uncorrected_p_le_0.05 |
| 5 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | 1Sam 25:16 | `חומה` | paired_uncorrected_p_le_0.05 |
| 6 | all_source | `htp_yhwh_h` | YHWH | 2 | 7 | 1Sam 26:21 | `היומ` | paired_uncorrected_p_le_0.05 |
| 7 | all_source | `htp_yhwh_h` | YHWH | 2 | 7 | 1Sam 30:25 | `מהיומ` | paired_uncorrected_p_le_0.05 |
| 8 | all_source | `htp_yhwh_h` | YHWH | 2 | 7 | 2Chr 20:12 | `ההמונ` | paired_uncorrected_p_le_0.05 |
| 9 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | 2Chr 24:16 | `טובה` | paired_uncorrected_p_le_0.05 |
| 10 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | 2Chr 31:18 | `ולהתיחש` | paired_uncorrected_p_le_0.05 |
| 11 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | 2Chr 32:18 | `החומה` | paired_uncorrected_p_le_0.05 |
| 12 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | 2Chr 33:14 | `חומה` | paired_uncorrected_p_le_0.05 |
| 13 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | 2Chr 34:19 | `התורה` | paired_uncorrected_p_le_0.05 |
| 14 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | 2Chr 5:9 | `החוצה` | paired_uncorrected_p_le_0.05 |
| 15 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | 2Kgs 22:11 | `התורה` | paired_uncorrected_p_le_0.05 |
| 16 | all_source | `htp_yhwh_h` | YHWH | 2 | 7 | 2Kgs 6:5 | `הקורה` | paired_uncorrected_p_le_0.05 |
| 17 | all_source | `htp_yhwh_h` | YHWH | 2 | 7 | 2Kgs 7:9 | `היומ` | paired_uncorrected_p_le_0.05 |
| 18 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | 2Sam 11:20 | `החומה` | paired_uncorrected_p_le_0.05 |
| 19 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | 2Sam 11:21 | `החומה` | paired_uncorrected_p_le_0.05 |
| 20 | all_source | `htp_yhwh_h` | YHWH | -2 | 7 | 2Sam 11:24 | `החומה` | paired_uncorrected_p_le_0.05 |

## Read

Rows at the top are good manual-review candidates because their hidden ELS
path center is located on, or near, surface language from the same declared
term set. The `presence_scope` column reports whether the selected exact
ref-key pattern appears in every configured source, multiple sources, or
only one source among the selected candidate keys.
