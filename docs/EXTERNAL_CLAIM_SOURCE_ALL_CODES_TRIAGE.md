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
| 1 | multi_source | `cc_evil_fire_h` `אשרע` (shr; English: Evil Fire) | Evil Fire | -2 | 7 | 2Chr 3:15 | `אשרעלראשו` (shrlrshw) | not_run |
| 2 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Chr 26:27 | `יהוה` (YHWH; English: YHWH) | not_run |
| 3 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 26:27 | `יהוה` (YHWH; English: YHWH) | not_run |
| 4 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 26:27 | `יהוה` (YHWH; English: YHWH) | not_run |
| 5 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Chr 28:20 | `יהוה` (YHWH; English: YHWH) | not_run |
| 6 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 28:20 | `יהוה` (YHWH; English: YHWH) | not_run |
| 7 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 28:20 | `יהוה` (YHWH; English: YHWH) | not_run |
| 8 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Kgs 10:5 | `יהוה` (YHWH; English: YHWH) | not_run |
| 9 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 10:5 | `יהוה` (YHWH; English: YHWH) | not_run |
| 10 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 10:5 | `יהוה` (YHWH; English: YHWH) | not_run |
| 11 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Sam 26:11 | `יהוה` (YHWH; English: YHWH) | not_run |
| 12 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:11 | `יהוה` (YHWH; English: YHWH) | not_run |
| 13 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:11 | `יהוה` (YHWH; English: YHWH) | not_run |
| 14 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Sam 26:16 | `יהוה` (YHWH; English: YHWH) | not_run |
| 15 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:16 | `יהוה` (YHWH; English: YHWH) | not_run |
| 16 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:16 | `יהוה` (YHWH; English: YHWH) | not_run |
| 17 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Sam 26:23 | `יהוה` (YHWH; English: YHWH) | not_run |
| 18 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:23 | `יהוה` (YHWH; English: YHWH) | not_run |
| 19 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:23 | `יהוה` (YHWH; English: YHWH) | not_run |
| 20 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Sam 26:9 | `יהוה` (YHWH; English: YHWH) | not_run |

### center_word_same_concept

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -4 | 13 | 2Sam 2:30 | `מעבדי` (mbdy) | not_run |
| 2 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -14 | 43 | Num 4:47 | `עבדת` (bdt) | not_run |
| 3 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -19 | 58 | Josh 22:5 | `ולעבדו` (wlbdw) | not_run |
| 4 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -22 | 67 | Num 4:23 | `לעבד` (lbd) | not_run |
| 5 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 53 | 160 | 1Kgs 20:12 | `אלעבדיו` (lbdyw) | not_run |
| 6 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 54 | 163 | 2Kgs 10:21 | `כלעבדי` (klbdy) | not_run |
| 7 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 8 | 25 | Gen 32:17 | `בידעבדיו` (bydbdyw) | not_run |
| 8 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 77 | 232 | 2Chr 29:12 | `עבדי` (bdy) | not_run |
| 9 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -67 | 202 | 1Kgs 22:50 | `עבדי` (bdy) | not_run |
| 10 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -2 | 7 | PBY Brenner | `עבדותעולמ` (bdwtwlm) | not_run |
| 11 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -3 | 10 | PBY Brenner | `לעבדו` (lbdw) | not_run |
| 12 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -4 | 13 | PBY Bialik | `ועבדו` (wbdw) | not_run |
| 13 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 6 | 19 | PBY Bialik | `ולמשועבדו` (wlmshwbdw) | not_run |
| 14 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 8 | 25 | Gen 32:16 | `בידעבדיו` (bydbdyw) | not_run |
| 15 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 8 | 25 | PBY Bialik | `לאתעבד` (ltbd) | not_run |
| 16 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -12 | 37 | PBY Brenner | `עבדותעולמ` (bdwtwlm) | not_run |
| 17 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 38 | 115 | PBY Bialik | `ותעבדהו` (wtbdhw) | not_run |
| 18 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 55 | 166 | PBY Brenner | `עבד` (bd) | not_run |
| 19 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 62 | 187 | PBY Bialik | `משתעבדות` (mshtbdwt) | not_run |
| 20 | source_specific | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -65 | 196 | PBY Brenner | `המשועבד` (hmshwbd) | not_run |

### center_word_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `cc_poplar_h` `לבנה` (lbnh; English: Poplar) | Poplar | -2 | 7 | 1Chr 16:14 | `אלהינו` (lhynw) | not_run |
| 2 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 2 | 7 | 1Sam 25:4 | `דוד` (dwd; English: David) | not_run |
| 3 | multi_source | `cc_fig_h` `תאנה` (tnh; English: Fig) | Fig | -2 | 7 | 1Sam 2:2 | `כאלהינו` (klhynw) | not_run |
| 4 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 34:19 | `התורה` (htwrh) | not_run |
| 5 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 34:19 | `התורה` (htwrh) | not_run |
| 6 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | 2 | 7 | 2Chr 9:11 | `האלגומימ` (hlgwmym) | not_run |
| 7 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | 2 | 7 | 2Chr 9:11 | `האלגומימ` (hlgwmym) | not_run |
| 8 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | 2 | 7 | 2Chr 9:11 | `האלגומימ` (hlgwmym) | not_run |
| 9 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Kgs 22:11 | `התורה` (htwrh) | not_run |
| 10 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Kgs 22:11 | `התורה` (htwrh) | not_run |
| 11 | multi_source | `cc_fig_h` `תאנה` (tnh; English: Fig) | Fig | -2 | 7 | Dan 9:17 | `אלהינו` (lhynw) | not_run |
| 12 | multi_source | `cc_matthew_h` `מתתי` (mtty; English: Matthew) | Matthew | -2 | 7 | Deut 11:11 | `תשתהמימ` (tshthmym) | not_run |
| 13 | multi_source | `mt_matthew_h` `מתתי` (mtty; English: Matthew) | Matthew | -2 | 7 | Deut 11:11 | `תשתהמימ` (tshthmym) | not_run |
| 14 | multi_source | `twn_matthew_h` `מתתי` (mtty; English: Matthew) | Matthew | -2 | 7 | Deut 11:11 | `תשתהמימ` (tshthmym) | not_run |
| 15 | multi_source | `cc_poplar_h` `לבנה` (lbnh; English: Poplar) | Poplar | -2 | 7 | Deut 4:7 | `אלהינו` (lhynw) | not_run |
| 16 | multi_source | `cc_moriah_h` `מריה` (mryh; English: Moriah) | Moriah | -2 | 7 | Exod 15:23 | `מרימ` (mrym) | not_run |
| 17 | multi_source | `mt_moriah_h` `מריה` (mryh; English: Moriah) | Moriah | -2 | 7 | Exod 15:23 | `מרימ` (mrym) | not_run |
| 18 | multi_source | `twn_moriah_h` `מריה` (mryh; English: Moriah) | Moriah | -2 | 7 | Exod 15:23 | `מרימ` (mrym) | not_run |
| 19 | multi_source | `cc_oak_h` `אלונ` (lwn; English: Oak) | Oak | -2 | 7 | Exod 21:6 | `אלהאלהימ` (lhlhym) | not_run |
| 20 | multi_source | `cc_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | 2 | 7 | Exod 24:10 | `השמימ` (hshmym) | not_run |

### center_verse_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 15:11 | `שמעיה` (shmyh) | not_run |
| 2 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 15:11 | `שמעיה` (shmyh) | not_run |
| 3 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 15:11 | `שמעיה` (shmyh) | not_run |
| 4 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 2 | 7 | 1Kgs 2:42 | `הלוא` (hlw) | not_run |
| 5 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Kgs 2:42 | `הלוא` (hlw) | not_run |
| 6 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Kgs 2:42 | `הלוא` (hlw) | not_run |
| 7 | multi_source | `bcd_saul_h` `שאול` (shwl; English: Saul) | Saul | 2 | 7 | 1Sam 14:47 | `ישראל` (Yisrael; English: Israel) | not_run |
| 8 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 2 | 7 | 1Sam 17:46 | `היומ` (hywm) | not_run |
| 9 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Sam 17:46 | `היומ` (hywm) | not_run |
| 10 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Sam 17:46 | `היומ` (hywm) | not_run |
| 11 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | -2 | 7 | 2Chr 13:10 | `וכהנימ` (wkhnym) | not_run |
| 12 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 13:10 | `וכהנימ` (wkhnym) | not_run |
| 13 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 13:10 | `וכהנימ` (wkhnym) | not_run |
| 14 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 2Chr 19:8 | `בירושלמ` (byrwshlm) | not_run |
| 15 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 2Chr 19:8 | `בירושלמ` (byrwshlm) | not_run |
| 16 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 2Chr 19:8 | `בירושלמ` (byrwshlm) | not_run |
| 17 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 2 | 7 | 2Chr 20:15 | `ההמונ` (hhmwn) | not_run |
| 18 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 2Chr 20:15 | `ההמונ` (hhmwn) | not_run |
| 19 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 2Chr 20:15 | `ההמונ` (hhmwn) | not_run |
| 20 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | -2 | 7 | 2Chr 24:8 | `חוצה` (chwtsh) | not_run |

### center_verse_same_concept

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -2 | 7 | 1Kgs 18:6 | `לבדו` (lbdw) | not_run |
| 2 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -2 | 7 | 1Kgs 3:8 | `בתוכ` (betokh; English: in the midst) | not_run |
| 3 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -3 | 10 | 1Sam 12:10 | `איבינו` (ybynw) | not_run |
| 4 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 3 | 10 | Lam 1:3 | `ומרב` (wmrb) | not_run |
| 5 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 4 | 13 | 2Sam 13:36 | `בכו` (bkw; English: Gregorian 2026 compact) | not_run |
| 6 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -5 | 16 | Ps 90:16 | `עלבניהמ` (lbnyhm) | not_run |
| 7 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 6 | 19 | 1Chr 19:2 | `ויבאו` (wybw) | not_run |
| 8 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -6 | 19 | 2Sam 7:20 | `אליכ` (lyk) | not_run |
| 9 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -6 | 19 | Gen 29:20 | `אתה` (th) | not_run |
| 10 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 7 | 22 | 1Chr 13:13 | `ויטהו` (wythw) | not_run |
| 11 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 7 | 22 | 2Sam 15:34 | `ואמרת` (wmrt) | not_run |
| 12 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -8 | 25 | 2Kgs 24:1 | `ויהילו` (wyhylw) | not_run |
| 13 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -8 | 25 | Jer 2:20 | `כי` (ky) | not_run |
| 14 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -9 | 28 | Deut 26:6 | `וירעו` (wyrw) | not_run |
| 15 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 9 | 28 | Isa 60:12 | `והגוימ` (whgwym) | not_run |
| 16 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -10 | 31 | Dan 2:49 | `מלכא` (mlk) | not_run |
| 17 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 10 | 31 | Jer 37:2 | `הארצ` (hrts) | not_run |
| 18 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 10 | 31 | Ps 134:1 | `אתיהוה` (tyhwh) | not_run |
| 19 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -12 | 37 | 2Chr 24:25 | `המלכימ` (hmlkym) | not_run |
| 20 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -12 | 37 | 2Chr 35:24 | `יאשיהו` (yshyhw; English: Josiah) | not_run |

### center_verse_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `cc_mary_h` `מרימ` (mrym; English: Mary) | Mary | 2 | 7 | 1Chr 13:2 | `מגרשיהמ` (mgrshyhm) | not_run |
| 2 | multi_source | `mt_mary_h` `מרימ` (mrym; English: Mary) | Mary | 2 | 7 | 1Chr 13:2 | `מגרשיהמ` (mgrshyhm) | not_run |
| 3 | multi_source | `twn_mary_h` `מרימ` (mrym; English: Mary) | Mary | 2 | 7 | 1Chr 13:2 | `מגרשיהמ` (mgrshyhm) | not_run |
| 4 | multi_source | `cc_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 15:12 | `אלהי` (lhy) | not_run |
| 5 | multi_source | `mt_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 15:12 | `אלהי` (lhy) | not_run |
| 6 | multi_source | `cc_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 15:14 | `אלהי` (lhy) | not_run |
| 7 | multi_source | `mt_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 15:14 | `אלהי` (lhy) | not_run |
| 8 | multi_source | `cc_thomas_h` `תומא` (twm; English: Thomas) | Thomas | 2 | 7 | 1Chr 16:17 | `עולמ` (wlm) | not_run |
| 9 | multi_source | `mt_thomas_h` `תומא` (twm; English: Thomas) | Thomas | 2 | 7 | 1Chr 16:17 | `עולמ` (wlm) | not_run |
| 10 | multi_source | `twn_thomas_h` `תומא` (twm; English: Thomas) | Thomas | 2 | 7 | 1Chr 16:17 | `עולמ` (wlm) | not_run |
| 11 | multi_source | `cc_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 16:4 | `אלהי` (lhy) | not_run |
| 12 | multi_source | `mt_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 16:4 | `אלהי` (lhy) | not_run |
| 13 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 17:4 | `יהוה` (YHWH; English: YHWH) | not_run |
| 14 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 17:4 | `יהוה` (YHWH; English: YHWH) | not_run |
| 15 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 17:4 | `יהוה` (YHWH; English: YHWH) | not_run |
| 16 | multi_source | `cc_torah_h` `תורה` (twrh; English: Torah) | Torah | 2 | 7 | 1Chr 21:17 | `והרע` (whr) | not_run |
| 17 | multi_source | `twn_torah_h` `תורה` (twrh; English: Torah) | Torah | 2 | 7 | 1Chr 21:17 | `והרע` (whr) | not_run |
| 18 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 21:27 | `יהוה` (YHWH; English: YHWH) | not_run |
| 19 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 21:27 | `יהוה` (YHWH; English: YHWH) | not_run |
| 20 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 21:27 | `יהוה` (YHWH; English: YHWH) | not_run |

### span_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 2Chr 19:9 | `ויצו` (wytsw) | not_run |
| 2 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 2Chr 19:9 | `ויצו` (wytsw) | not_run |
| 3 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 2Chr 19:9 | `ויצו` (wytsw) | not_run |
| 4 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | -2 | 7 | Neh 8:13 | `התורה` (htwrh) | not_run |
| 5 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | Num 1:46 | `וחמשימ` (wchmshym) | not_run |
| 6 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | Num 1:46 | `וחמשימ` (wchmshym) | not_run |
| 7 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | Num 1:46 | `וחמשימ` (wchmshym) | not_run |
| 8 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | Num 2:32 | `וחמשימ` (wchmshym) | not_run |
| 9 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | Num 2:32 | `וחמשימ` (wchmshym) | not_run |
| 10 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | Num 2:32 | `וחמשימ` (wchmshym) | not_run |
| 11 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Chr 28:7 | `הזה` (hzh) | not_run |
| 12 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 28:7 | `הזה` (hzh) | not_run |
| 13 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 28:7 | `הזה` (hzh) | not_run |
| 14 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Kgs 3:6 | `הזה` (hzh) | not_run |
| 15 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 3:6 | `הזה` (hzh) | not_run |
| 16 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 3:6 | `הזה` (hzh) | not_run |
| 17 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 1Kgs 8:24 | `הזה` (hzh) | not_run |
| 18 | multi_source | `cc_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 8:24 | `הזה` (hzh) | not_run |
| 19 | multi_source | `twn_yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 8:24 | `הזה` (hzh) | not_run |
| 20 | multi_source | `bns_esther_yhwh_h` `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 3 | 10 | 2Chr 6:15 | `הזה` (hzh) | not_run |

### span_same_concept

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -2 | 7 | Dan 3:27 | `בהונ` (bhwn) | not_run |
| 2 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -7 | 22 | Ps 90:12 | `חכמה` (chkmh; English: Wisdom) | not_run |
| 3 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -10 | 31 | Josh 5:15 | `יהוה` (YHWH; English: YHWH) | not_run |
| 4 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 12 | 37 | 2Chr 25:25 | `אמציהו` (mtsyhw) | not_run |
| 5 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 16 | 49 | Lev 23:20 | `לכהנ` (lkhn) | not_run |
| 6 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 27 | 82 | Ezra 7:25 | `תהודעונ` (thwdwn) | not_run |
| 7 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -30 | 91 | Gen 15:15 | `תקבר` (tqbr) | not_run |
| 8 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 34 | 103 | Num 3:9 | `בני` (bny) | not_run |
| 9 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 35 | 106 | 1Chr 8:32 | `ואפ` (wp) | not_run |
| 10 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -37 | 112 | Gen 29:21 | `אללבנ` (llbn) | not_run |
| 11 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -37 | 112 | Num 9:1 | `לצאתמ` (ltstm) | not_run |
| 12 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -38 | 115 | Isa 53:12 | `שלל` (shalal; English: spoil/plunder) | not_run |
| 13 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -38 | 115 | Judg 2:9 | `מצפונ` (mtspwn) | not_run |
| 14 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 39 | 118 | 1Kgs 2:42 | `ויאמר` (wymr) | not_run |
| 15 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -39 | 118 | Isa 48:21 | `בחרבות` (bchrbwt) | not_run |
| 16 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 39 | 118 | Josh 11:13 | `יהושע` (yhwsh; English: Joshua) | not_run |
| 17 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | 42 | 127 | 1Chr 16:14 | `משפטיו` (mshptyw) | not_run |
| 18 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -42 | 127 | 1Kgs 15:30 | `אתישראל` (tyshrl) | not_run |
| 19 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -45 | 136 | 2Kgs 9:27 | `מגדו` (mgdw) | not_run |
| 20 | multi_source | `twn_obed_h` `עובד` (wbd; English: Obed) | Obed | -45 | 136 | Exod 12:33 | `עלהעמ` (lhm) | not_run |

### span_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `bcd_saul_h` `שאול` (shwl; English: Saul) | Saul | 2 | 7 | 1Chr 11:10 | `עלישראל` (lyshrl) | not_run |
| 2 | multi_source | `cc_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | 2 | 7 | 1Chr 16:6 | `ובניהו` (wbnyhw) | not_run |
| 3 | multi_source | `mt_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | 2 | 7 | 1Chr 16:6 | `ובניהו` (wbnyhw) | not_run |
| 4 | multi_source | `cc_thomas_h` `תומא` (twm; English: Thomas) | Thomas | 2 | 7 | 1Chr 24:4 | `וימצאו` (wymtsw) | not_run |
| 5 | multi_source | `mt_thomas_h` `תומא` (twm; English: Thomas) | Thomas | 2 | 7 | 1Chr 24:4 | `וימצאו` (wymtsw) | not_run |
| 6 | multi_source | `twn_thomas_h` `תומא` (twm; English: Thomas) | Thomas | 2 | 7 | 1Chr 24:4 | `וימצאו` (wymtsw) | not_run |
| 7 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 26:7 | `וסמכיהו` (wsmkyhw) | not_run |
| 8 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 26:7 | `וסמכיהו` (wsmkyhw) | not_run |
| 9 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 26:7 | `וסמכיהו` (wsmkyhw) | not_run |
| 10 | multi_source | `cc_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 27:17 | `ללוי` (llwy) | not_run |
| 11 | multi_source | `mt_shiloh_h` `שילה` (shylh; English: Shiloh) | Shiloh | -2 | 7 | 1Chr 27:17 | `ללוי` (llwy) | not_run |
| 12 | multi_source | `bcd_saul_h` `שאול` (shwl; English: Saul) | Saul | 2 | 7 | 1Chr 4:35 | `עשיאל` (shyl) | not_run |
| 13 | multi_source | `cc_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | 2 | 7 | 1Kgs 4:4 | `ובניהו` (wbnyhw) | not_run |
| 14 | multi_source | `mt_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | 2 | 7 | 1Kgs 4:4 | `ובניהו` (wbnyhw) | not_run |
| 15 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | 2 | 7 | 1Sam 15:1 | `ויאמר` (wymr) | not_run |
| 16 | multi_source | `mt_levites_h` `לוימ` (lwym; English: Levites) | Levites | 2 | 7 | 1Sam 15:1 | `ויאמר` (wymr) | not_run |
| 17 | multi_source | `twn_levites_h` `לוימ` (lwym; English: Levites) | Levites | 2 | 7 | 1Sam 15:1 | `ויאמר` (wymr) | not_run |
| 18 | multi_source | `cc_pomegranate_h` `רמונ` (rmwn; English: Pomegranate) | Pomegranate | 2 | 7 | 1Sam 1:6 | `רחמה` (rchmh) | not_run |
| 19 | multi_source | `cc_mary_h` `מרימ` (mrym; English: Mary) | Mary | 2 | 7 | Deut 7:5 | `כיאמכה` (kymkh) | not_run |
| 20 | multi_source | `mt_mary_h` `מרימ` (mrym; English: Mary) | Mary | 2 | 7 | Deut 7:5 | `כיאמכה` (kymkh) | not_run |

### hidden_path_only

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | multi_source | `cc_shoah_h` `שואה` (shwh; English: Holocaust) | Holocaust | 2 | 7 | 1Chr 10:4 | `שאול` (shwl) | not_run |
| 2 | multi_source | `cri_holocaust_h` `שואה` (shwh; English: Holocaust) | Holocaust | 2 | 7 | 1Chr 10:4 | `שאול` (shwl) | not_run |
| 3 | multi_source | `bcd_saul_h` `שאול` (shwl; English: Saul) | Saul | 2 | 7 | 1Chr 11:10 | `ישראל` (Yisrael; English: Israel) | not_run |
| 4 | multi_source | `cc_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | 2 | 7 | 1Chr 11:24 | `בנ` (bn) | not_run |
| 5 | multi_source | `mt_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | 2 | 7 | 1Chr 11:24 | `בנ` (bn) | not_run |
| 6 | multi_source | `cc_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | -2 | 7 | 1Chr 11:28 | `הענתותי` (hntwty) | not_run |
| 7 | multi_source | `mt_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | -2 | 7 | 1Chr 11:28 | `הענתותי` (hntwty) | not_run |
| 8 | multi_source | `bcd_chile_h` `צילה` (tsylh; English: Chile) | Chile | -2 | 7 | 1Chr 11:36 | `הפלני` (hplny) | not_run |
| 9 | multi_source | `cc_evil_fire_h` `אשרע` (shr; English: Evil Fire) | Evil Fire | 2 | 7 | 1Chr 11:8 | `שאר` (shr) | not_run |
| 10 | multi_source | `cc_aaron_h` `אהרנ` (hrn; English: Aaron) | Aaron | 2 | 7 | 1Chr 13:13 | `הארונ` (hrwn) | not_run |
| 11 | multi_source | `twn_aaron_h` `אהרנ` (hrn; English: Aaron) | Aaron | 2 | 7 | 1Chr 13:13 | `הארונ` (hrwn) | not_run |
| 12 | multi_source | `cc_aaron_h` `אהרנ` (hrn; English: Aaron) | Aaron | 2 | 7 | 1Chr 13:9 | `הארונ` (hrwn) | not_run |
| 13 | multi_source | `twn_aaron_h` `אהרנ` (hrn; English: Aaron) | Aaron | 2 | 7 | 1Chr 13:9 | `הארונ` (hrwn) | not_run |
| 14 | multi_source | `cc_yeshua_h` `ישוע` (Yeshua; English: Yeshua) | Yeshua | 2 | 7 | 1Chr 14:13 | `ויפשטו` (wypshtw) | not_run |
| 15 | multi_source | `twn_yeshua_h` `ישוע` (Yeshua; English: Yeshua) | Yeshua | 2 | 7 | 1Chr 14:13 | `ויפשטו` (wypshtw) | not_run |
| 16 | multi_source | `bns_rabin_h` `רבינ` (rbyn; English: Rabin) | Rabin | -2 | 7 | 1Chr 14:3 | `נשימ` (nshym) | not_run |
| 17 | multi_source | `cc_levites_h` `לוימ` (lwym; English: Levites) | Levites | -2 | 7 | 1Chr 14:3 | `בירושלמ` (byrwshlm) | not_run |
| 18 | multi_source | `cc_rabin_h` `רבינ` (rbyn; English: Rabin) | Rabin | -2 | 7 | 1Chr 14:3 | `נשימ` (nshym) | not_run |
| 19 | multi_source | `cri_rabin_h` `רבינ` (rbyn; English: Rabin) | Rabin | -2 | 7 | 1Chr 14:3 | `נשימ` (nshym) | not_run |
| 20 | multi_source | `cri_robin_h` `רבינ` (rbyn; English: Robin) | Robin | -2 | 7 | 1Chr 14:3 | `נשימ` (nshym) | not_run |

## Read

Rows at the top are good manual-review candidates because their hidden ELS
path center is located on, or near, surface language from the same declared
term set. The `presence_scope` column reports whether the selected exact
ref-key pattern appears in every configured source, multiple sources, or
only one source among the selected candidate keys.
