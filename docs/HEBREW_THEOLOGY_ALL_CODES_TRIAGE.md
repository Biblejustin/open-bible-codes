# Hebrew Theology All-Codes Triage

This is a compact review queue built from the relaxed all-codes export.
It ranks same center-word rows first, then related center-word rows,
center-verse rows, span rows, and finally hidden-path-only rows.

It is a triage aid, not a claim-grade filter.

## Inputs

- Hits: `reports/hebrew_theology_all_codes/surface_all_codes.csv`
- Summary: `reports/hebrew_theology_all_codes/surface_all_codes_summary.csv`
- Report DB: `reports/db/open_bible_codes.duckdb`
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
| 1 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 26:27 | `יהוה` (YHWH; English: YHWH) | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 28:20 | `יהוה` (YHWH; English: YHWH) | paired_uncorrected_p_le_0.05 |
| 3 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 10:5 | `יהוה` (YHWH; English: YHWH) | paired_uncorrected_p_le_0.05 |
| 4 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:11 | `יהוה` (YHWH; English: YHWH) | paired_uncorrected_p_le_0.05 |
| 5 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:16 | `יהוה` (YHWH; English: YHWH) | paired_uncorrected_p_le_0.05 |
| 6 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:23 | `יהוה` (YHWH; English: YHWH) | paired_uncorrected_p_le_0.05 |
| 7 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:9 | `יהוה` (YHWH; English: YHWH) | paired_uncorrected_p_le_0.05 |
| 8 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -3 | 10 | 2Chr 21:7 | `יהוה` (YHWH; English: YHWH) | paired_uncorrected_p_le_0.05 |
| 9 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 2Chr 33:15 | `יהוה` (YHWH; English: YHWH) | paired_uncorrected_p_le_0.05 |
| 10 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 2Chr 9:4 | `יהוה` (YHWH; English: YHWH) | paired_uncorrected_p_le_0.05 |
| 11 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 2Kgs 23:24 | `יהוה` (YHWH; English: YHWH) | paired_uncorrected_p_le_0.05 |
| 12 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 2Kgs 25:13 | `ביתיהוה` (beit YHWH; English: house of YHWH) | paired_uncorrected_p_le_0.05 |
| 13 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -3 | 10 | 2Kgs 8:19 | `יהוה` (YHWH; English: YHWH) | paired_uncorrected_p_le_0.05 |
| 14 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -3 | 10 | 2Sam 10:12 | `ויהוה` (ve-YHWH; English: and YHWH) | paired_uncorrected_p_le_0.05 |
| 15 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -3 | 10 | Isa 48:14 | `יהוה` (YHWH; English: YHWH) | paired_uncorrected_p_le_0.05 |
| 16 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Isa 51:22 | `יהוה` (YHWH; English: YHWH) | paired_uncorrected_p_le_0.05 |
| 17 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Jer 28:6 | `ביתיהוה` (beit YHWH; English: house of YHWH) | paired_uncorrected_p_le_0.05 |
| 18 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Jer 52:17 | `לביתיהוה` (le-beit YHWH; English: to the house of YHWH) | paired_uncorrected_p_le_0.05 |
| 19 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Num 14:44 | `בריתיהוה` (berit YHWH; English: covenant of YHWH) | paired_uncorrected_p_le_0.05 |
| 20 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Ps 32:5 | `ליהוה` (le-YHWH; English: to/for YHWH) | paired_uncorrected_p_le_0.05 |

### center_word_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 7 | 22 | 1Chr 5:1 | `בנישראל` (bnei Yisrael; English: children of Israel) | not_unusual |
| 2 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -7 | 22 | 2Kgs 17:20 | `ישראל` (Yisrael; English: Israel) | not_unusual |
| 3 | all_source | `htp_covenant_h` `ברית` (bryt; English: Covenant) | Covenant | 8 | 25 | Deut 34:9 | `חכמה` (chkmh) | not_unusual |
| 4 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 9 | 28 | 1Sam 17:45 | `ישראל` (Yisrael; English: Israel) | not_unusual |
| 5 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 13 | 40 | Ezek 48:11 | `ישראל` (Yisrael; English: Israel) | not_unusual |
| 6 | all_source | `htp_covenant_h` `ברית` (bryt; English: Covenant) | Covenant | -13 | 40 | Prov 1:7 | `חכמה` (chkmh) | not_unusual |
| 7 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 14 | 43 | 1Sam 2:22 | `ישראל` (Yisrael; English: Israel) | not_unusual |
| 8 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 14 | 43 | Exod 7:5 | `אתבניישראל` (tbnyyshrl) | not_unusual |
| 9 | all_source | `htp_love_h` `אהבה` (hbh; English: Love) | Love | -15 | 46 | 2Sam 14:30 | `אבשלומ` (bshlwm) | not_unusual |
| 10 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -15 | 46 | Isa 45:17 | `ישראל` (Yisrael; English: Israel) | not_unusual |
| 11 | all_source | `htp_peace_h` `שלומ` (shlwm; English: Peace) | Peace | -15 | 46 | Song 8:7 | `אתהאהבה` (thhbh) | not_unusual |
| 12 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 16 | 49 | Deut 27:14 | `ישראל` (Yisrael; English: Israel) | not_unusual |
| 13 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 16 | 49 | Lev 7:38 | `ישראל` (Yisrael; English: Israel) | not_unusual |
| 14 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -16 | 49 | Num 3:40 | `ישראל` (Yisrael; English: Israel) | not_unusual |
| 15 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 17 | 52 | 1Kgs 12:20 | `עלכלישראל` (lklyshrl) | not_unusual |
| 16 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 18 | 55 | Jer 7:3 | `ישראל` (Yisrael; English: Israel) | not_unusual |
| 17 | all_source | `htp_glory_h` `כבוד` (kbwd; English: Glory) | Glory | -18 | 55 | Lev 13:57 | `ואמתראה` (wmtrh) | not_unusual |
| 18 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 20 | 61 | 1Chr 7:29 | `ישראל` (Yisrael; English: Israel) | not_unusual |
| 19 | all_source | `htp_love_h` `אהבה` (hbh; English: Love) | Love | -20 | 61 | 2Sam 15:34 | `לאבשלומ` (lbshlwm) | not_unusual |
| 20 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 22 | 67 | Num 15:32 | `בניישראל` (bnyyshrl; English: Children Israel) | not_unusual |

### center_verse_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Kgs 2:42 | `הלוא` (hlw) | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Sam 17:46 | `היומ` (hywm) | paired_uncorrected_p_le_0.05 |
| 3 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 13:10 | `וכהנימ` (wkhnym) | paired_uncorrected_p_le_0.05 |
| 4 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 2Chr 20:15 | `ההמונ` (hhmwn) | paired_uncorrected_p_le_0.05 |
| 5 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 24:8 | `חוצה` (chwtsh) | paired_uncorrected_p_le_0.05 |
| 6 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Kgs 5:11 | `והניפ` (whnyp) | paired_uncorrected_p_le_0.05 |
| 7 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | Exod 12:14 | `היומ` (hywm) | paired_uncorrected_p_le_0.05 |
| 8 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | Ezek 45:23 | `עולה` (wlh) | paired_uncorrected_p_le_0.05 |
| 9 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | Ezek 46:13 | `עולה` (wlh) | paired_uncorrected_p_le_0.05 |
| 10 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | Ezek 4:3 | `אותה` (wth) | paired_uncorrected_p_le_0.05 |
| 11 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | Gen 39:21 | `ויהי` (wyhy) | paired_uncorrected_p_le_0.05 |
| 12 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | Isa 40:2 | `עונה` (wnh; English: 1) cohabitation, conjugal rights) | paired_uncorrected_p_le_0.05 |
| 13 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | Jer 3:23 | `המונ` (hmwn) | paired_uncorrected_p_le_0.05 |
| 14 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | Lev 10:19 | `היומ` (hywm) | paired_uncorrected_p_le_0.05 |
| 15 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | Mal 1:13 | `אותה` (wth) | paired_uncorrected_p_le_0.05 |
| 16 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | Neh 8:9 | `התורה` (htwrh) | paired_uncorrected_p_le_0.05 |
| 17 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | Num 10:32 | `הטוב` (htwb) | paired_uncorrected_p_le_0.05 |
| 18 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | Zech 1:6 | `הלוא` (hlw) | paired_uncorrected_p_le_0.05 |
| 19 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | Zech 1:6 | `הלוא` (hlw) | paired_uncorrected_p_le_0.05 |
| 20 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 19:13 | `אלהינו` (lhynw) | paired_uncorrected_p_le_0.05 |

### center_verse_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -2 | 7 | 1Sam 6:5 | `הארצ` (hrts) | not_unusual |
| 2 | all_source | `htp_love_h` `אהבה` (hbh; English: Love) | Love | 2 | 7 | 2Sam 14:21 | `הדבר` (ha-davar; English: the word/matter) | not_unusual |
| 3 | all_source | `htp_love_h` `אהבה` (hbh; English: Love) | Love | 2 | 7 | 2Sam 15:27 | `שבה` (shuvah; English: return) | not_unusual |
| 4 | all_source | `htp_love_h` `אהבה` (hbh; English: Love) | Love | 2 | 7 | Exod 18:23 | `אתהדבר` (thdbr) | not_unusual |
| 5 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -2 | 7 | Ezek 36:10 | `והחרבות` (whchrbwt) | not_unusual |
| 6 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -2 | 7 | Ezra 10:2 | `הארצ` (hrts) | not_unusual |
| 7 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -2 | 7 | Jer 7:12 | `וראו` (wrw) | not_unusual |
| 8 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 3 | 10 | 1Sam 28:19 | `ומחר` (wmchr) | not_unusual |
| 9 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -3 | 10 | 2Chr 31:1 | `האשרימ` (hshrym) | not_unusual |
| 10 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -3 | 10 | 2Kgs 17:23 | `יהוה` (YHWH; English: YHWH) | not_unusual |
| 11 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -3 | 10 | 2Kgs 8:12 | `תרטש` (trtsh) | not_unusual |
| 12 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -3 | 10 | Deut 9:1 | `היומ` (hywm) | not_unusual |
| 13 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -3 | 10 | Exod 10:23 | `במושבתמ` (bmwshbtm) | not_unusual |
| 14 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -3 | 10 | Ezra 7:7 | `והשערימ` (whshrym) | not_unusual |
| 15 | all_source | `htp_wisdom_h` `חכמה` (chkmh; English: Wisdom) | Wisdom | 3 | 10 | Isa 49:8 | `כה` (koh; English: thus) | not_unusual |
| 16 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 4 | 13 | 1Chr 11:10 | `ואלה` (wlh) | not_unusual |
| 17 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 4 | 13 | 1Sam 14:45 | `אשר` (shr; English: Asher) | not_unusual |
| 18 | all_source | `htp_glory_h` `כבוד` (kbwd; English: Glory) | Glory | -4 | 13 | Ezek 27:16 | `בעזבוניכ` (bzbwnyk) | not_unusual |
| 19 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 4 | 13 | Ezek 7:2 | `הארצ` (hrts) | not_unusual |
| 20 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 4 | 13 | Ezek 8:12 | `ויאמר` (wymr) | not_unusual |

### span_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | Neh 8:13 | `התורה` (htwrh) | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 28:7 | `הזה` (hzh) | paired_uncorrected_p_le_0.05 |
| 3 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 3:6 | `הזה` (hzh) | paired_uncorrected_p_le_0.05 |
| 4 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 8:24 | `הזה` (hzh) | paired_uncorrected_p_le_0.05 |
| 5 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 2Chr 6:15 | `הזה` (hzh) | paired_uncorrected_p_le_0.05 |
| 6 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -3 | 10 | Exod 32:10 | `ועתה` (wth) | paired_uncorrected_p_le_0.05 |
| 7 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -3 | 10 | Ezek 22:13 | `והנה` (whnh) | paired_uncorrected_p_le_0.05 |
| 8 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -3 | 10 | Ezek 2:5 | `והמה` (whmh) | paired_uncorrected_p_le_0.05 |
| 9 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -3 | 10 | Ezek 30:9 | `ביומ` (bywm) | paired_uncorrected_p_le_0.05 |
| 10 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Ezek 44:14 | `בו` (bw) | paired_uncorrected_p_le_0.05 |
| 11 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Ezra 9:7 | `הזה` (hzh) | paired_uncorrected_p_le_0.05 |
| 12 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Gen 24:53 | `ויוצא` (wywts) | paired_uncorrected_p_le_0.05 |
| 13 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Isa 1:3 | `התבוננ` (htbwnn) | paired_uncorrected_p_le_0.05 |
| 14 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Isa 3:18 | `ביומ` (bywm) | paired_uncorrected_p_le_0.05 |
| 15 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -3 | 10 | Isa 3:18 | `ביומ` (bywm) | paired_uncorrected_p_le_0.05 |
| 16 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Isa 58:6 | `הלוא` (hlw) | paired_uncorrected_p_le_0.05 |
| 17 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Jer 44:6 | `הזה` (hzh) | paired_uncorrected_p_le_0.05 |
| 18 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Josh 4:9 | `הזה` (hzh) | paired_uncorrected_p_le_0.05 |
| 19 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -4 | 13 | Deut 15:3 | `אתהנכרי` (thnkry) | paired_uncorrected_p_le_0.05 |
| 20 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -4 | 13 | Deut 1:44 | `ויצא` (wyts) | paired_uncorrected_p_le_0.05 |

### span_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -2 | 7 | Exod 19:5 | `כלהארצ` (klhrts) | not_unusual |
| 2 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -2 | 7 | Ezek 39:16 | `הארצ` (hrts) | not_unusual |
| 3 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -2 | 7 | Josh 13:21 | `הארצ` (hrts) | not_unusual |
| 4 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 2 | 7 | Lev 17:6 | `וזרק` (wzrq) | not_unusual |
| 5 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 4 | 13 | 1Kgs 8:51 | `הברזל` (hbrzl) | not_unusual |
| 6 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 4 | 13 | Exod 30:17 | `וידבר` (wydbr) | not_unusual |
| 7 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 4 | 13 | Exod 34:31 | `ויקרא` (wyqr) | not_unusual |
| 8 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 4 | 13 | Exod 9:8 | `ויאמר` (wymr) | not_unusual |
| 9 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 4 | 13 | Ezek 9:4 | `ויאמר` (wymr) | not_unusual |
| 10 | all_source | `htp_love_h` `אהבה` (hbh; English: Love) | Love | -4 | 13 | Jer 4:11 | `בעת` (bt) | not_unusual |
| 11 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 4 | 13 | Lev 17:1 | `וידבר` (wydbr) | not_unusual |
| 12 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 4 | 13 | Lev 25:1 | `וידבר` (wydbr) | not_unusual |
| 13 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -5 | 16 | 1Sam 8:5 | `אליו` (lyw) | not_unusual |
| 14 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -6 | 19 | 2Sam 12:6 | `חמל` (chml) | not_unusual |
| 15 | all_source | `htp_messiah_h` `משיח` (Mashiach; English: Messiah) | Messiah | 6 | 19 | Ezra 2:5 | `ושבעימ` (ve-shivim; English: and seventy) | not_unusual |
| 16 | all_source | `htp_love_h` `אהבה` (hbh; English: Love) | Love | -6 | 19 | Jer 34:6 | `ירמיהו` (yrmyhw; English: Jeremiah) | not_unusual |
| 17 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 6 | 19 | Jer 3:7 | `ואמר` (wmr) | not_unusual |
| 18 | all_source | `htp_messiah_h` `משיח` (Mashiach; English: Messiah) | Messiah | 6 | 19 | Neh 7:10 | `ושנימ` (ve-shenayim; English: and two) | not_unusual |
| 19 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | -7 | 22 | 2Kgs 14:18 | `אמציהו` (mtsyhw) | not_unusual |
| 20 | all_source | `htp_torah_h` `תורה` (twrh; English: Torah) | Torah | 9 | 28 | 2Chr 11:15 | `ולעגלימ` (wlglym) | not_unusual |

### hidden_path_only

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Chr 24:10 | `להקוצ` (lhqwts) | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Chr 29:28 | `טובה` (twbh) | paired_uncorrected_p_le_0.05 |
| 3 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Kgs 13:24 | `וימיתהו` (wymythw) | paired_uncorrected_p_le_0.05 |
| 4 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 1Kgs 8:8 | `החוצה` (hchwtsh) | paired_uncorrected_p_le_0.05 |
| 5 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 1Sam 25:16 | `חומה` (chwmh; English: 1) wall) | paired_uncorrected_p_le_0.05 |
| 6 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Sam 26:21 | `היומ` (hywm) | paired_uncorrected_p_le_0.05 |
| 7 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Sam 30:25 | `מהיומ` (mhywm) | paired_uncorrected_p_le_0.05 |
| 8 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 2Chr 20:12 | `ההמונ` (hhmwn) | paired_uncorrected_p_le_0.05 |
| 9 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 24:16 | `טובה` (twbh) | paired_uncorrected_p_le_0.05 |
| 10 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 31:18 | `ולהתיחש` (wlhtychsh) | paired_uncorrected_p_le_0.05 |
| 11 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 32:18 | `החומה` (hchwmh) | paired_uncorrected_p_le_0.05 |
| 12 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 33:14 | `חומה` (chwmh; English: 1) wall) | paired_uncorrected_p_le_0.05 |
| 13 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 34:19 | `התורה` (htwrh) | paired_uncorrected_p_le_0.05 |
| 14 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 5:9 | `החוצה` (hchwtsh) | paired_uncorrected_p_le_0.05 |
| 15 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Kgs 22:11 | `התורה` (htwrh) | paired_uncorrected_p_le_0.05 |
| 16 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 2Kgs 6:5 | `הקורה` (hqwrh) | paired_uncorrected_p_le_0.05 |
| 17 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 2Kgs 7:9 | `היומ` (hywm) | paired_uncorrected_p_le_0.05 |
| 18 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Sam 11:20 | `החומה` (hchwmh) | paired_uncorrected_p_le_0.05 |
| 19 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Sam 11:21 | `החומה` (hchwmh) | paired_uncorrected_p_le_0.05 |
| 20 | all_source | `htp_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Sam 11:24 | `החומה` (hchwmh) | paired_uncorrected_p_le_0.05 |

## Read

Rows at the top are good manual-review candidates because their hidden ELS
path center is located on, or near, surface language from the same declared
term set. The `presence_scope` column reports whether the selected exact
ref-key pattern appears in every configured source, multiple sources, or
only one source among the selected candidate keys.
