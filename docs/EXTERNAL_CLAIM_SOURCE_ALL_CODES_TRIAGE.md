# External Claim Source All-Codes Triage

This is a compact review queue built from the relaxed all-codes export.
It ranks same center-word rows first, then related center-word rows,
center-verse rows, span rows, and finally hidden-path-only rows.

It is a triage aid, not a claim-grade filter.

## Inputs

- Hits: `reports/external_claim_source_all_codes/surface_all_codes.csv`
- Summary: `reports/external_claim_source_all_codes/surface_all_codes_summary.csv`
- Report DB: `reports/db/open_bible_codes.duckdb`
- Queue CSV: `reports/external_claim_source_all_codes/triage_queue.csv`
- Corpora: `BYZ_NT, EBIBLE_WLC, ENG_MOBY_DICK, ENG_SHAKESPEARE, ENG_WAR_AND_PEACE, GRK_HERODOTUS, GRK_ILIAD, GRK_ODYSSEY, HEB_AHAD_HAAM, HEB_BIALIK, HEB_BRENNER, KJV, KJVA, LXX, MAM, MT_WLC, SBLGNT, TCG_NT, TR_NT, UHB, UXLC`

## Counts

| Metric | Count |
| --- | ---: |
| Raw rows scanned | 8,443,775 |
| Queue rows | 926 |
| `center_word_exact` queue rows | 100 |
| `center_word_same_concept` queue rows | 26 |
| `center_word_same_category` queue rows | 100 |
| `center_verse_exact` queue rows | 100 |
| `center_verse_same_concept` queue rows | 100 |
| `center_verse_same_category` queue rows | 100 |
| `span_exact` queue rows | 100 |
| `span_same_concept` queue rows | 100 |
| `span_same_category` queue rows | 100 |
| `hidden_path_only` queue rows | 100 |

## Top Queue Rows

### center_word_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `cc_evil_fire_h` `אשרע` (shr; English: Evil Fire) | Evil Fire | -2 | 7 | 2Chr 3:15 | `אשרעלראשו` (shrlrshw) |  |
| 2 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Chr 26:27 | `יהוה` (YHWH; English: YHWH) |  |
| 3 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 26:27 | `יהוה` (YHWH; English: YHWH) |  |
| 4 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 26:27 | `יהוה` (YHWH; English: YHWH) |  |
| 5 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Chr 28:20 | `יהוה` (YHWH; English: YHWH) |  |
| 6 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 28:20 | `יהוה` (YHWH; English: YHWH) |  |
| 7 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 28:20 | `יהוה` (YHWH; English: YHWH) |  |
| 8 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Kgs 10:5 | `יהוה` (YHWH; English: YHWH) |  |
| 9 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 10:5 | `יהוה` (YHWH; English: YHWH) |  |
| 10 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 10:5 | `יהוה` (YHWH; English: YHWH) |  |
| 11 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Sam 26:11 | `יהוה` (YHWH; English: YHWH) |  |
| 12 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:11 | `יהוה` (YHWH; English: YHWH) |  |
| 13 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:11 | `יהוה` (YHWH; English: YHWH) |  |
| 14 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Sam 26:16 | `יהוה` (YHWH; English: YHWH) |  |
| 15 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:16 | `יהוה` (YHWH; English: YHWH) |  |
| 16 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:16 | `יהוה` (YHWH; English: YHWH) |  |
| 17 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Sam 26:23 | `יהוה` (YHWH; English: YHWH) |  |
| 18 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:23 | `יהוה` (YHWH; English: YHWH) |  |
| 19 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:23 | `יהוה` (YHWH; English: YHWH) |  |
| 20 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Sam 26:9 | `יהוה` (YHWH; English: YHWH) |  |

### center_word_same_concept

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -4 | 13 | 2Sam 2:30 | `מעבדי` (mbdy) |  |
| 2 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -14 | 43 | Num 4:47 | `עבדת` (bdt) |  |
| 3 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -19 | 58 | Josh 22:5 | `ולעבדו` (wlbdw) |  |
| 4 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -22 | 67 | Num 4:23 | `לעבד` (lbd) |  |
| 5 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 53 | 160 | 1Kgs 20:12 | `אלעבדיו` (lbdyw) |  |
| 6 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 54 | 163 | 2Kgs 10:21 | `כלעבדי` (klbdy) |  |
| 7 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 8 | 25 | Gen 32:17 | `בידעבדיו` (bydbdyw) |  |
| 8 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 77 | 232 | 2Chr 29:12 | `עבדי` (bdy) |  |
| 9 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -67 | 202 | 1Kgs 22:50 | `עבדי` (bdy) |  |
| 10 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -2 | 7 | PBY Brenner | `עבדותעולמ` (bdwtwlm) |  |
| 11 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -3 | 10 | PBY Brenner | `לעבדו` (lbdw) |  |
| 12 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -4 | 13 | PBY Bialik | `ועבדו` (wbdw) |  |
| 13 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 6 | 19 | PBY Bialik | `ולמשועבדו` (wlmshwbdw) |  |
| 14 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 8 | 25 | Gen 32:16 | `בידעבדיו` (bydbdyw) |  |
| 15 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 8 | 25 | PBY Bialik | `לאתעבד` (ltbd) |  |
| 16 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -12 | 37 | PBY Brenner | `עבדותעולמ` (bdwtwlm) |  |
| 17 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 38 | 115 | PBY Bialik | `ותעבדהו` (wtbdhw) |  |
| 18 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 55 | 166 | PBY Brenner | `עבד` (bd) |  |
| 19 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 62 | 187 | PBY Bialik | `משתעבדות` (mshtbdwt) |  |
| 20 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -65 | 196 | PBY Brenner | `המשועבד` (hmshwbd) |  |

### center_word_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `cc_poplar_h` `לבנה` (lbnh; English: Poplar) | Poplar | -2 | 7 | 1Chr 16:14 | `אלהינו` (lhynw) |  |
| 2 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 2 | 7 | 1Sam 25:4 | `דוד` (dwd; English: David) |  |
| 3 | multi_source | `cc_fig_h` `תאנה` (tnh; English: Fig) | Fig | -2 | 7 | 1Sam 2:2 | `כאלהינו` (klhynw) |  |
| 4 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 34:19 | `התורה` (htwrh) |  |
| 5 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 34:19 | `התורה` (htwrh) |  |
| 6 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | 2 | 7 | 2Chr 9:11 | `האלגומימ` (hlgwmym) |  |
| 7 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | 2 | 7 | 2Chr 9:11 | `האלגומימ` (hlgwmym) |  |
| 8 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | 2 | 7 | 2Chr 9:11 | `האלגומימ` (hlgwmym) |  |
| 9 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Kgs 22:11 | `התורה` (htwrh) |  |
| 10 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Kgs 22:11 | `התורה` (htwrh) |  |
| 11 | multi_source | `cc_fig_h` `תאנה` (tnh; English: Fig) | Fig | -2 | 7 | Dan 9:17 | `אלהינו` (lhynw) |  |
| 12 | multi_source | `cc_matthew_h` `מתתי` (mtty; English: Matthew) | Matthew | -2 | 7 | Deut 11:11 | `תשתהמימ` (tshthmym) |  |
| 13 | multi_source | `mt_matthew_h` `מתתי` (mtty; English: Matthew) | Matthew | -2 | 7 | Deut 11:11 | `תשתהמימ` (tshthmym) |  |
| 14 | multi_source | `twn_matthew_h` `מתתי` (mtty; English: Matthew) | Matthew | -2 | 7 | Deut 11:11 | `תשתהמימ` (tshthmym) |  |
| 15 | multi_source | `cc_poplar_h` `לבנה` (lbnh; English: Poplar) | Poplar | -2 | 7 | Deut 4:7 | `אלהינו` (lhynw) |  |
| 16 | multi_source | `cc_moriah_h` `מריה` (mryh; English: Moriah) | Moriah | -2 | 7 | Exod 15:23 | `מרימ` (mrym) |  |
| 17 | multi_source | `mt_moriah_h` `מריה` (mryh; English: Moriah) | Moriah | -2 | 7 | Exod 15:23 | `מרימ` (mrym) |  |
| 18 | multi_source | `twn_moriah_h` `מריה` (mryh; English: Moriah) | Moriah | -2 | 7 | Exod 15:23 | `מרימ` (mrym) |  |
| 19 | multi_source | `cc_oak_h` `אלונ` (lwn; English: Oak) | Oak | -2 | 7 | Exod 21:6 | `אלהאלהימ` (lhlhym) |  |
| 20 | multi_source | `cc_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | 2 | 7 | Exod 24:10 | `השמימ` (hshmym) |  |

### center_verse_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 15:11 | `שמעיה` (shmyh) |  |
| 2 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 15:11 | `שמעיה` (shmyh) |  |
| 3 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 15:11 | `שמעיה` (shmyh) |  |
| 4 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 2 | 7 | 1Kgs 2:42 | `הלוא` (hlw) |  |
| 5 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Kgs 2:42 | `הלוא` (hlw) |  |
| 6 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Kgs 2:42 | `הלוא` (hlw) |  |
| 7 | multi_source | `bcd_saul_h` `שאול` (shwl; English: Saul) | Saul | 2 | 7 | 1Sam 14:47 | `ישראל` (Yisrael; English: Israel) |  |
| 8 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 2 | 7 | 1Sam 17:46 | `היומ` (hywm) |  |
| 9 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Sam 17:46 | `היומ` (hywm) |  |
| 10 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Sam 17:46 | `היומ` (hywm) |  |
| 11 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | -2 | 7 | 2Chr 13:10 | `וכהנימ` (wkhnym) |  |
| 12 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 13:10 | `וכהנימ` (wkhnym) |  |
| 13 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 13:10 | `וכהנימ` (wkhnym) |  |
| 14 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 2Chr 19:8 | `בירושלמ` (byrwshlm) |  |
| 15 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 2Chr 19:8 | `בירושלמ` (byrwshlm) |  |
| 16 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 2Chr 19:8 | `בירושלמ` (byrwshlm) |  |
| 17 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 2 | 7 | 2Chr 20:15 | `ההמונ` (hhmwn) |  |
| 18 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 2Chr 20:15 | `ההמונ` (hhmwn) |  |
| 19 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 2Chr 20:15 | `ההמונ` (hhmwn) |  |
| 20 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | -2 | 7 | 2Chr 24:8 | `חוצה` (chwtsh) |  |

### center_verse_same_concept

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -2 | 7 | 1Kgs 18:6 | `לבדו` (lbdw) |  |
| 2 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -2 | 7 | 1Kgs 3:8 | `בתוכ` (betokh; English: in the midst) |  |
| 3 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -3 | 10 | 1Sam 12:10 | `איבינו` (ybynw) |  |
| 4 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 3 | 10 | Lam 1:3 | `ומרב` (wmrb) |  |
| 5 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 4 | 13 | 2Sam 13:36 | `בכו` (bkw; English: Gregorian 2026 compact) |  |
| 6 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -5 | 16 | Ps 90:16 | `עלבניהמ` (lbnyhm) |  |
| 7 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 6 | 19 | 1Chr 19:2 | `ויבאו` (wybw) |  |
| 8 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -6 | 19 | 2Sam 7:20 | `אליכ` (lyk) |  |
| 9 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -6 | 19 | Gen 29:20 | `אתה` (th) |  |
| 10 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 7 | 22 | 1Chr 13:13 | `ויטהו` (wythw) |  |
| 11 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 7 | 22 | 2Sam 15:34 | `ואמרת` (wmrt) |  |
| 12 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -8 | 25 | 2Kgs 24:1 | `ויהילו` (wyhylw) |  |
| 13 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -8 | 25 | Jer 2:20 | `כי` (ky) |  |
| 14 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -9 | 28 | Deut 26:6 | `וירעו` (wyrw) |  |
| 15 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 9 | 28 | Isa 60:12 | `והגוימ` (whgwym) |  |
| 16 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -10 | 31 | Dan 2:49 | `מלכא` (mlk) |  |
| 17 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 10 | 31 | Jer 37:2 | `הארצ` (hrts) |  |
| 18 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 10 | 31 | Ps 134:1 | `אתיהוה` (tyhwh) |  |
| 19 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -12 | 37 | 2Chr 24:25 | `המלכימ` (hmlkym) |  |
| 20 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -12 | 37 | 2Chr 35:24 | `יאשיהו` (yshyhw; English: Josiah) |  |

### center_verse_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `cc_mary_h` `מרימ` (mrym; English: Mary) | Mary | 2 | 7 | 1Chr 13:2 | `מגרשיהמ` (mgrshyhm) |  |
| 2 | multi_source | `mt_mary_h` `מרימ` (mrym; English: Mary) | Mary | 2 | 7 | 1Chr 13:2 | `מגרשיהמ` (mgrshyhm) |  |
| 3 | multi_source | `twn_mary_h` `מרימ` (mrym; English: Mary) | Mary | 2 | 7 | 1Chr 13:2 | `מגרשיהמ` (mgrshyhm) |  |
| 4 | multi_source | `cc_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 15:12 | `אלהי` (lhy) |  |
| 5 | multi_source | `mt_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 15:12 | `אלהי` (lhy) |  |
| 6 | multi_source | `cc_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 15:14 | `אלהי` (lhy) |  |
| 7 | multi_source | `mt_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 15:14 | `אלהי` (lhy) |  |
| 8 | multi_source | `cc_thomas_h` `תומא` (twm; English: Thomas) | Thomas | 2 | 7 | 1Chr 16:17 | `עולמ` (wlm) |  |
| 9 | multi_source | `mt_thomas_h` `תומא` (twm; English: Thomas) | Thomas | 2 | 7 | 1Chr 16:17 | `עולמ` (wlm) |  |
| 10 | multi_source | `twn_thomas_h` `תומא` (twm; English: Thomas) | Thomas | 2 | 7 | 1Chr 16:17 | `עולמ` (wlm) |  |
| 11 | multi_source | `cc_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 16:4 | `אלהי` (lhy) |  |
| 12 | multi_source | `mt_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 16:4 | `אלהי` (lhy) |  |
| 13 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 17:4 | `יהוה` (YHWH; English: YHWH) |  |
| 14 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 17:4 | `יהוה` (YHWH; English: YHWH) |  |
| 15 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 17:4 | `יהוה` (YHWH; English: YHWH) |  |
| 16 | multi_source | `cc_torah_h` `תורה` (twrh; English: Torah) | Torah | 2 | 7 | 1Chr 21:17 | `והרע` (whr) |  |
| 17 | multi_source | `twn_torah_h` `תורה` (twrh; English: Torah) | Torah | 2 | 7 | 1Chr 21:17 | `והרע` (whr) |  |
| 18 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 21:27 | `יהוה` (YHWH; English: YHWH) |  |
| 19 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 21:27 | `יהוה` (YHWH; English: YHWH) |  |
| 20 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 21:27 | `יהוה` (YHWH; English: YHWH) |  |

### span_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 2Chr 19:9 | `ויצו` (wytsw) |  |
| 2 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 2Chr 19:9 | `ויצו` (wytsw) |  |
| 3 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 2Chr 19:9 | `ויצו` (wytsw) |  |
| 4 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | -2 | 7 | Neh 8:13 | `התורה` (htwrh) |  |
| 5 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | Num 1:46 | `וחמשימ` (wchmshym) |  |
| 6 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | Num 1:46 | `וחמשימ` (wchmshym) |  |
| 7 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | Num 1:46 | `וחמשימ` (wchmshym) |  |
| 8 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | Num 2:32 | `וחמשימ` (wchmshym) |  |
| 9 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | Num 2:32 | `וחמשימ` (wchmshym) |  |
| 10 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | Num 2:32 | `וחמשימ` (wchmshym) |  |
| 11 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Chr 28:7 | `הזה` (hzh) |  |
| 12 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 28:7 | `הזה` (hzh) |  |
| 13 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 28:7 | `הזה` (hzh) |  |
| 14 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Kgs 3:6 | `הזה` (hzh) |  |
| 15 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 3:6 | `הזה` (hzh) |  |
| 16 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 3:6 | `הזה` (hzh) |  |
| 17 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Kgs 8:24 | `הזה` (hzh) |  |
| 18 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 8:24 | `הזה` (hzh) |  |
| 19 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 8:24 | `הזה` (hzh) |  |
| 20 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 2Chr 6:15 | `הזה` (hzh) |  |

### span_same_concept

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -2 | 7 | Dan 3:27 | `בהונ` (bhwn) |  |
| 2 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -7 | 22 | Ps 90:12 | `חכמה` (chkmh; English: Wisdom) |  |
| 3 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -10 | 31 | Josh 5:15 | `יהוה` (YHWH; English: YHWH) |  |
| 4 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 12 | 37 | 2Chr 25:25 | `אמציהו` (mtsyhw) |  |
| 5 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 16 | 49 | Lev 23:20 | `לכהנ` (lkhn) |  |
| 6 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 27 | 82 | Ezra 7:25 | `תהודעונ` (thwdwn) |  |
| 7 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -30 | 91 | Gen 15:15 | `תקבר` (tqbr) |  |
| 8 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 34 | 103 | Num 3:9 | `בני` (bny) |  |
| 9 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 35 | 106 | 1Chr 8:32 | `ואפ` (wp) |  |
| 10 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -37 | 112 | Gen 29:21 | `אללבנ` (llbn) |  |
| 11 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -37 | 112 | Num 9:1 | `לצאתמ` (ltstm) |  |
| 12 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -38 | 115 | Isa 53:12 | `שלל` (shalal; English: spoil/plunder) |  |
| 13 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -38 | 115 | Judg 2:9 | `מצפונ` (mtspwn) |  |
| 14 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 39 | 118 | 1Kgs 2:42 | `ויאמר` (wymr) |  |
| 15 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -39 | 118 | Isa 48:21 | `בחרבות` (bchrbwt) |  |
| 16 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 39 | 118 | Josh 11:13 | `יהושע` (yhwsh) |  |
| 17 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 42 | 127 | 1Chr 16:14 | `משפטיו` (mshptyw) |  |
| 18 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -42 | 127 | 1Kgs 15:30 | `אתישראל` (tyshrl) |  |
| 19 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -45 | 136 | 2Kgs 9:27 | `מגדו` (mgdw) |  |
| 20 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -45 | 136 | Exod 12:33 | `עלהעמ` (lhm) |  |

### span_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `bcd_saul_h` `שאול` (shwl; English: Saul) | Saul | 2 | 7 | 1Chr 11:10 | `עלישראל` (lyshrl) |  |
| 2 | multi_source | `cc_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | 2 | 7 | 1Chr 16:6 | `ובניהו` (wbnyhw) |  |
| 3 | multi_source | `mt_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | 2 | 7 | 1Chr 16:6 | `ובניהו` (wbnyhw) |  |
| 4 | multi_source | `cc_thomas_h` `תומא` (twm; English: Thomas) | Thomas | 2 | 7 | 1Chr 24:4 | `וימצאו` (wymtsw) |  |
| 5 | multi_source | `mt_thomas_h` `תומא` (twm; English: Thomas) | Thomas | 2 | 7 | 1Chr 24:4 | `וימצאו` (wymtsw) |  |
| 6 | multi_source | `twn_thomas_h` `תומא` (twm; English: Thomas) | Thomas | 2 | 7 | 1Chr 24:4 | `וימצאו` (wymtsw) |  |
| 7 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 26:7 | `וסמכיהו` (wsmkyhw) |  |
| 8 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 26:7 | `וסמכיהו` (wsmkyhw) |  |
| 9 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 26:7 | `וסמכיהו` (wsmkyhw) |  |
| 10 | multi_source | `cc_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 27:17 | `ללוי` (llwy) |  |
| 11 | multi_source | `mt_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 27:17 | `ללוי` (llwy) |  |
| 12 | multi_source | `bcd_saul_h` `שאול` (shwl; English: Saul) | Saul | 2 | 7 | 1Chr 4:35 | `עשיאל` (shyl) |  |
| 13 | multi_source | `cc_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | 2 | 7 | 1Kgs 4:4 | `ובניהו` (wbnyhw) |  |
| 14 | multi_source | `mt_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | 2 | 7 | 1Kgs 4:4 | `ובניהו` (wbnyhw) |  |
| 15 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | 2 | 7 | 1Sam 15:1 | `ויאמר` (wymr) |  |
| 16 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | 2 | 7 | 1Sam 15:1 | `ויאמר` (wymr) |  |
| 17 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | 2 | 7 | 1Sam 15:1 | `ויאמר` (wymr) |  |
| 18 | multi_source | `cc_pomegranate_h` `רמונ` (rmwn; English: Pomegranate) | Pomegranate | 2 | 7 | 1Sam 1:6 | `רחמה` (rchmh) |  |
| 19 | multi_source | `cc_mary_h` `מרימ` (mrym; English: Mary) | Mary | 2 | 7 | Deut 7:5 | `כיאמכה` (kymkh) |  |
| 20 | multi_source | `mt_mary_h` `מרימ` (mrym; English: Mary) | Mary | 2 | 7 | Deut 7:5 | `כיאמכה` (kymkh) |  |

### hidden_path_only

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `cc_shoah_h` `שואה` (shwh; English: Holocaust) | Holocaust | 2 | 7 | 1Chr 10:4 | `שאול` (shwl) |  |
| 2 | multi_source | `cri_holocaust_h` `שואה` (shwh; English: Holocaust) | Holocaust | 2 | 7 | 1Chr 10:4 | `שאול` (shwl) |  |
| 3 | multi_source | `bcd_saul_h` `שאול` (shwl; English: Saul) | Saul | 2 | 7 | 1Chr 11:10 | `ישראל` (Yisrael; English: Israel) |  |
| 4 | multi_source | `cc_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | 2 | 7 | 1Chr 11:24 | `בנ` (bn) |  |
| 5 | multi_source | `mt_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | 2 | 7 | 1Chr 11:24 | `בנ` (bn) |  |
| 6 | multi_source | `cc_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | -2 | 7 | 1Chr 11:28 | `הענתותי` (hntwty) |  |
| 7 | multi_source | `mt_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | -2 | 7 | 1Chr 11:28 | `הענתותי` (hntwty) |  |
| 8 | multi_source | `bcd_chile_h` `צילה` (tsylh; English: Chile) | Chile | -2 | 7 | 1Chr 11:36 | `הפלני` (hplny) |  |
| 9 | multi_source | `cc_evil_fire_h` `אשרע` (shr; English: Evil Fire) | Evil Fire | 2 | 7 | 1Chr 11:8 | `שאר` (shr) |  |
| 10 | multi_source | `cc_aaron_h` `אהרנ` (hrn; English: Aaron) | Aaron | 2 | 7 | 1Chr 13:13 | `הארונ` (hrwn) |  |
| 11 | multi_source | `twn_aaron_h` `אהרנ` (hrn; English: Aaron) | Aaron | 2 | 7 | 1Chr 13:13 | `הארונ` (hrwn) |  |
| 12 | multi_source | `cc_aaron_h` `אהרנ` (hrn; English: Aaron) | Aaron | 2 | 7 | 1Chr 13:9 | `הארונ` (hrwn) |  |
| 13 | multi_source | `twn_aaron_h` `אהרנ` (hrn; English: Aaron) | Aaron | 2 | 7 | 1Chr 13:9 | `הארונ` (hrwn) |  |
| 14 | multi_source | `cc_yeshua_h` `ישוע` (Yeshua; English: Yeshua) | Yeshua | 2 | 7 | 1Chr 14:13 | `ויפשטו` (wypshtw) |  |
| 15 | multi_source | `twn_yeshua_h` `ישוע` (Yeshua; English: Yeshua) | Yeshua | 2 | 7 | 1Chr 14:13 | `ויפשטו` (wypshtw) |  |
| 16 | multi_source | `bns_rabin_h` `רבינ` (rbyn; English: Rabin) | Rabin | -2 | 7 | 1Chr 14:3 | `נשימ` (nshym) |  |
| 17 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 14:3 | `בירושלמ` (byrwshlm) |  |
| 18 | multi_source | `cc_rabin_h` `רבינ` (rbyn; English: Rabin) | Rabin | -2 | 7 | 1Chr 14:3 | `נשימ` (nshym) |  |
| 19 | multi_source | `cri_rabin_h` `רבינ` (rbyn; English: Rabin) | Rabin | -2 | 7 | 1Chr 14:3 | `נשימ` (nshym) |  |
| 20 | multi_source | `cri_robin_h` `רבינ` (rbyn; English: Robin) | Robin | -2 | 7 | 1Chr 14:3 | `נשימ` (nshym) |  |

## Read

Rows at the top are good manual-review candidates because their hidden ELS
path center is located on, or near, surface language from the same declared
term set. The `presence_scope` column reports whether the selected exact
ref-key pattern appears in every configured source, multiple sources, or
only one source among the selected candidate keys.
