# Dynamic Full-Span Partition Findings

This report summarizes completed dense full-span partition outputs.
It is additive to the manageable-row export: a dense row becomes
complete when all planned partition outputs exist and summarize.

## Reproduce

```bash
python3 -m scripts.summarize_dynamic_span_partition_outputs --plan reports/dynamic_skip_focus/full_span_partition_plan.csv --manifest-only
```

## Scope

- planned partitions: 13,646
- completed partition outputs summarized: 13,646
- completed dense rows: 147
- partial dense rows: 0
- exported partition hit rows summarized: 13,556,483,793
- exact center-word hits in completed partitions: not_computed
- partition summary CSV: `reports/dynamic_skip_focus/full_span_partition_output_summary.csv`
- term summary CSV: `reports/dynamic_skip_focus/full_span_partition_term_summary.csv`
- examples CSV: `reports/dynamic_skip_focus/full_span_partition_examples.csv`

## Completed Dense Rows

| Corpus | Term | Hits | Exact center-word hits |
| --- | --- | ---: | ---: |
| BYZ_NT | `γωγ` (Gog; English: Gog)<br>`dyn_gog_g` | 1,990,638 | not_computed |
| BYZ_NT | `ιραν` (iran; English: Iran)<br>`dyn_iran_g` | 4,749,326 | not_computed |
| BYZ_NT | `ρωσια` (rosia; English: Russia)<br>`dyn_russia_g` | 102,577 | not_computed |
| BYZ_NT | `βανς` (bans; English: Vance)<br>`dyn_vance_g` | 573,495 | not_computed |
| EBIBLE_WLC | `חיה` (chayah; English: Beast)<br>`dyn_beast_h` | 165,249,617 | not_computed |
| EBIBLE_WLC | `תנין` (tannin; English: Dragon)<br>`dyn_dragon_h` | 6,204,591 | not_computed |
| EBIBLE_WLC | `גוג` (Gog; English: Gog)<br>`dyn_gog_h` | 5,606,606 | not_computed |
| EBIBLE_WLC | `איראן` (yrn; English: Iran)<br>`dyn_iran_h` | 667,552 | not_computed |
| EBIBLE_WLC | `מגוג` (Magog; English: Magog)<br>`dyn_magog_h` | 307,083 | not_computed |
| EBIBLE_WLC | `משיח` (Mashiach; English: Messiah)<br>`dyn_messiah_h` | 5,252,863 | not_computed |
| EBIBLE_WLC | `רוסיה` (rwsyh; English: Russia)<br>`dyn_russia_h` | 142,783 | not_computed |
| EBIBLE_WLC | `ואנס` (wns; English: Vance)<br>`dyn_vance_h` | 1,173,157 | not_computed |
| EBIBLE_WLC | `ישוע` (Yeshua; English: Yeshua)<br>`dyn_yeshua_h` | 11,156,131 | not_computed |
| EBIBLE_WLC | `יהוה` (YHWH; English: YHWH)<br>`dyn_yhwh_h` | 42,745,545 | not_computed |
| ENG_PG_MOBY_DICK | `Beast`<br>`dyn_beast_e` | 253,351 | not_computed |
| ENG_PG_MOBY_DICK | `Gog`<br>`dyn_gog_e` | 15,815,416 | not_computed |
| ENG_PG_MOBY_DICK | `Iran`<br>`dyn_iran_e` | 6,458,074 | not_computed |
| ENG_PG_SHAKESPEARE | `Beast`<br>`dyn_beast_e` | 3,418,141 | not_computed |
| ENG_PG_SHAKESPEARE | `Christ`<br>`dyn_christ_e` | 111,185 | not_computed |
| ENG_PG_SHAKESPEARE | `Dragon`<br>`dyn_dragon_e` | 60,588 | not_computed |
| ENG_PG_SHAKESPEARE | `Gog`<br>`dyn_gog_e` | 217,556,768 | not_computed |
| ENG_PG_SHAKESPEARE | `Iran`<br>`dyn_iran_e` | 113,877,707 | not_computed |
| ENG_PG_SHAKESPEARE | `Jesus`<br>`dyn_jesus_e` | 87,353 | not_computed |
| ENG_PG_SHAKESPEARE | `Magog`<br>`dyn_magog_e` | 248,036 | not_computed |
| ENG_PG_SHAKESPEARE | `Russia`<br>`dyn_russia_e` | 151,995 | not_computed |
| ENG_PG_SHAKESPEARE | `Trump`<br>`dyn_trump_e` | 335,790 | not_computed |
| ENG_PG_SHAKESPEARE | `Vance`<br>`dyn_vance_e` | 560,612 | not_computed |
| ENG_PG_WAR_PEACE | `Beast`<br>`dyn_beast_e` | 1,264,733 | not_computed |
| ENG_PG_WAR_PEACE | `Gog`<br>`dyn_gog_e` | 98,950,428 | not_computed |
| ENG_PG_WAR_PEACE | `Iran`<br>`dyn_iran_e` | 50,720,110 | not_computed |
| ENG_PG_WAR_PEACE | `Magog`<br>`dyn_magog_e` | 99,239 | not_computed |
| ENG_PG_WAR_PEACE | `Trump`<br>`dyn_trump_e` | 93,018 | not_computed |
| ENG_PG_WAR_PEACE | `Vance`<br>`dyn_vance_e` | 299,257 | not_computed |
| GRC_PERSEUS_HERODOTUS | `γωγ` (Gog; English: Gog)<br>`dyn_gog_g` | 3,079,794 | not_computed |
| GRC_PERSEUS_HERODOTUS | `ιραν` (iran; English: Iran)<br>`dyn_iran_g` | 9,046,396 | not_computed |
| GRC_PERSEUS_HERODOTUS | `ρωσια` (rosia; English: Russia)<br>`dyn_russia_g` | 184,242 | not_computed |
| GRC_PERSEUS_HERODOTUS | `τραμπ` (tramp; English: Trump)<br>`dyn_trump_g` | 68,470 | not_computed |
| GRC_PERSEUS_HERODOTUS | `βανς` (bans; English: Vance)<br>`dyn_vance_g` | 1,235,733 | not_computed |
| GRC_PERSEUS_ILIAD | `γωγ` (Gog; English: Gog)<br>`dyn_gog_g` | 895,700 | not_computed |
| GRC_PERSEUS_ILIAD | `ιραν` (iran; English: Iran)<br>`dyn_iran_g` | 3,579,561 | not_computed |
| GRC_PERSEUS_ILIAD | `ρωσια` (rosia; English: Russia)<br>`dyn_russia_g` | 67,477 | not_computed |
| GRC_PERSEUS_ILIAD | `βανς` (bans; English: Vance)<br>`dyn_vance_g` | 325,999 | not_computed |
| GRC_PERSEUS_ODYSSEY | `γωγ` (Gog; English: Gog)<br>`dyn_gog_g` | 501,302 | not_computed |
| GRC_PERSEUS_ODYSSEY | `ιραν` (iran; English: Iran)<br>`dyn_iran_g` | 1,997,138 | not_computed |
| GRC_PERSEUS_ODYSSEY | `βανς` (bans; English: Vance)<br>`dyn_vance_g` | 185,209 | not_computed |
| HEB_PBY_AHAD_HAAM | `חיה` (chayah; English: Beast)<br>`dyn_beast_h` | 816,402,749 | not_computed |
| HEB_PBY_AHAD_HAAM | `תנין` (tannin; English: Dragon)<br>`dyn_dragon_h` | 33,003,976 | not_computed |
| HEB_PBY_AHAD_HAAM | `גוג` (Gog; English: Gog)<br>`dyn_gog_h` | 52,524,066 | not_computed |
| HEB_PBY_AHAD_HAAM | `איראן` (yrn; English: Iran)<br>`dyn_iran_h` | 2,117,348 | not_computed |
| HEB_PBY_AHAD_HAAM | `מגוג` (Magog; English: Magog)<br>`dyn_magog_h` | 2,911,852 | not_computed |
| HEB_PBY_AHAD_HAAM | `משיח` (Mashiach; English: Messiah)<br>`dyn_messiah_h` | 22,587,059 | not_computed |
| HEB_PBY_AHAD_HAAM | `נתניהו` (ntnyhw; English: Netanyahu)<br>`dyn_netanyahu_h` | 195,658 | not_computed |
| HEB_PBY_AHAD_HAAM | `רוסיה` (rwsyh; English: Russia)<br>`dyn_russia_h` | 1,260,045 | not_computed |
| HEB_PBY_AHAD_HAAM | `טראמפ` (trmp; English: Trump)<br>`dyn_trump_h` | 92,451 | not_computed |
| HEB_PBY_AHAD_HAAM | `ואנס` (wns; English: Vance)<br>`dyn_vance_h` | 10,884,247 | not_computed |
| HEB_PBY_AHAD_HAAM | `ישוע` (Yeshua; English: Yeshua)<br>`dyn_yeshua_h` | 46,208,240 | not_computed |
| HEB_PBY_AHAD_HAAM | `יהוה` (YHWH; English: YHWH)<br>`dyn_yhwh_h` | 230,979,253 | not_computed |
| HEB_PBY_BIALIK | `חיה` (chayah; English: Beast)<br>`dyn_beast_h` | 3,152,690,416 | not_computed |
| HEB_PBY_BIALIK | `תנין` (tannin; English: Dragon)<br>`dyn_dragon_h` | 143,129,945 | not_computed |
| HEB_PBY_BIALIK | `גוג` (Gog; English: Gog)<br>`dyn_gog_h` | 259,364,876 | not_computed |
| HEB_PBY_BIALIK | `איראן` (yrn; English: Iran)<br>`dyn_iran_h` | 11,349,335 | not_computed |
| HEB_PBY_BIALIK | `מגוג` (Magog; English: Magog)<br>`dyn_magog_h` | 14,781,780 | not_computed |
| HEB_PBY_BIALIK | `משיח` (Mashiach; English: Messiah)<br>`dyn_messiah_h` | 110,129,394 | not_computed |
| HEB_PBY_BIALIK | `נתניהו` (ntnyhw; English: Netanyahu)<br>`dyn_netanyahu_h` | 763,870 | not_computed |
| HEB_PBY_BIALIK | `רוסיה` (rwsyh; English: Russia)<br>`dyn_russia_h` | 5,590,218 | not_computed |
| HEB_PBY_BIALIK | `טראמפ` (trmp; English: Trump)<br>`dyn_trump_h` | 526,134 | not_computed |
| HEB_PBY_BIALIK | `ואנס` (wns; English: Vance)<br>`dyn_vance_h` | 51,012,008 | not_computed |
| HEB_PBY_BIALIK | `ישוע` (Yeshua; English: Yeshua)<br>`dyn_yeshua_h` | 206,897,417 | not_computed |
| HEB_PBY_BIALIK | `יהוה` (YHWH; English: YHWH)<br>`dyn_yhwh_h` | 803,341,146 | not_computed |
| HEB_PBY_BRENNER | `חיה` (chayah; English: Beast)<br>`dyn_beast_h` | 3,663,683,890 | not_computed |
| HEB_PBY_BRENNER | `תנין` (tannin; English: Dragon)<br>`dyn_dragon_h` | 145,655,795 | not_computed |
| HEB_PBY_BRENNER | `גוג` (Gog; English: Gog)<br>`dyn_gog_h` | 266,462,544 | not_computed |
| HEB_PBY_BRENNER | `איראן` (yrn; English: Iran)<br>`dyn_iran_h` | 10,108,513 | not_computed |
| HEB_PBY_BRENNER | `מגוג` (Magog; English: Magog)<br>`dyn_magog_h` | 13,906,679 | not_computed |
| HEB_PBY_BRENNER | `משיח` (Mashiach; English: Messiah)<br>`dyn_messiah_h` | 90,027,862 | not_computed |
| HEB_PBY_BRENNER | `נתניהו` (ntnyhw; English: Netanyahu)<br>`dyn_netanyahu_h` | 920,932 | not_computed |
| HEB_PBY_BRENNER | `רוסיה` (rwsyh; English: Russia)<br>`dyn_russia_h` | 6,304,561 | not_computed |
| HEB_PBY_BRENNER | `טראמפ` (trmp; English: Trump)<br>`dyn_trump_h` | 461,367 | not_computed |
| HEB_PBY_BRENNER | `ואנס` (wns; English: Vance)<br>`dyn_vance_h` | 52,306,899 | not_computed |
| HEB_PBY_BRENNER | `ישוע` (Yeshua; English: Yeshua)<br>`dyn_yeshua_h` | 188,603,935 | not_computed |
| HEB_PBY_BRENNER | `יהוה` (YHWH; English: YHWH)<br>`dyn_yhwh_h` | 1,090,879,372 | not_computed |
| KJV | `Beast`<br>`dyn_beast_e` | 2,427,966 | not_computed |
| KJV | `Christ`<br>`dyn_christ_e` | 56,561 | not_computed |
| KJV | `Gog`<br>`dyn_gog_e` | 112,614,748 | not_computed |
| KJV | `Iran`<br>`dyn_iran_e` | 64,362,163 | not_computed |
| KJV | `Jesus`<br>`dyn_jesus_e` | 79,657 | not_computed |
| KJV | `Magog`<br>`dyn_magog_e` | 118,259 | not_computed |
| KJV | `Trump`<br>`dyn_trump_e` | 111,371 | not_computed |
| KJV | `Vance`<br>`dyn_vance_e` | 294,941 | not_computed |
| LXX | `γωγ` (Gog; English: Gog)<br>`dyn_gog_g` | 22,427,984 | not_computed |
| LXX | `ιραν` (iran; English: Iran)<br>`dyn_iran_g` | 81,141,888 | not_computed |
| LXX | `ιησους` (Iesous; English: Jesus)<br>`dyn_jesus_g` | 243,700 | not_computed |
| LXX | `ρωσια` (rosia; English: Russia)<br>`dyn_russia_g` | 2,218,044 | not_computed |
| LXX | `τραμπ` (tramp; English: Trump)<br>`dyn_trump_g` | 487,148 | not_computed |
| LXX | `βανς` (bans; English: Vance)<br>`dyn_vance_g` | 14,641,657 | not_computed |
| MAM | `חיה` (chayah; English: Beast)<br>`dyn_beast_h` | 164,260,192 | not_computed |
| MAM | `תנין` (tannin; English: Dragon)<br>`dyn_dragon_h` | 6,135,698 | not_computed |
| MAM | `גוג` (Gog; English: Gog)<br>`dyn_gog_h` | 5,593,814 | not_computed |
| MAM | `איראן` (yrn; English: Iran)<br>`dyn_iran_h` | 696,330 | not_computed |
| MAM | `מגוג` (Magog; English: Magog)<br>`dyn_magog_h` | 322,697 | not_computed |
| MAM | `משיח` (Mashiach; English: Messiah)<br>`dyn_messiah_h` | 5,093,697 | not_computed |
| MAM | `רוסיה` (rwsyh; English: Russia)<br>`dyn_russia_h` | 142,463 | not_computed |
| MAM | `ואנס` (wns; English: Vance)<br>`dyn_vance_h` | 1,224,569 | not_computed |
| MAM | `ישוע` (Yeshua; English: Yeshua)<br>`dyn_yeshua_h` | 10,824,700 | not_computed |
| MAM | `יהוה` (YHWH; English: YHWH)<br>`dyn_yhwh_h` | 43,619,325 | not_computed |
| MT_WLC | `חיה` (chayah; English: Beast)<br>`dyn_beast_h` | 163,013,648 | not_computed |
| MT_WLC | `תנין` (tannin; English: Dragon)<br>`dyn_dragon_h` | 6,066,657 | not_computed |
| MT_WLC | `גוג` (Gog; English: Gog)<br>`dyn_gog_h` | 5,532,568 | not_computed |
| MT_WLC | `איראן` (yrn; English: Iran)<br>`dyn_iran_h` | 691,579 | not_computed |
| MT_WLC | `מגוג` (Magog; English: Magog)<br>`dyn_magog_h` | 320,111 | not_computed |
| MT_WLC | `משיח` (Mashiach; English: Messiah)<br>`dyn_messiah_h` | 5,057,448 | not_computed |
| MT_WLC | `רוסיה` (rwsyh; English: Russia)<br>`dyn_russia_h` | 137,828 | not_computed |
| MT_WLC | `ואנס` (wns; English: Vance)<br>`dyn_vance_h` | 1,191,206 | not_computed |
| MT_WLC | `ישוע` (Yeshua; English: Yeshua)<br>`dyn_yeshua_h` | 10,724,464 | not_computed |
| MT_WLC | `יהוה` (YHWH; English: YHWH)<br>`dyn_yhwh_h` | 43,283,141 | not_computed |
| SBLGNT | `γωγ` (Gog; English: Gog)<br>`dyn_gog_g` | 1,935,106 | not_computed |
| SBLGNT | `ιραν` (iran; English: Iran)<br>`dyn_iran_g` | 4,615,073 | not_computed |
| SBLGNT | `ρωσια` (rosia; English: Russia)<br>`dyn_russia_g` | 99,245 | not_computed |
| SBLGNT | `βανς` (bans; English: Vance)<br>`dyn_vance_g` | 557,336 | not_computed |
| TCG_NT | `γωγ` (Gog; English: Gog)<br>`dyn_gog_g` | 2,000,884 | not_computed |
| TCG_NT | `ιραν` (iran; English: Iran)<br>`dyn_iran_g` | 4,582,262 | not_computed |
| TCG_NT | `ρωσια` (rosia; English: Russia)<br>`dyn_russia_g` | 103,404 | not_computed |
| TCG_NT | `βανς` (bans; English: Vance)<br>`dyn_vance_g` | 551,791 | not_computed |
| TR_NT | `γωγ` (Gog; English: Gog)<br>`dyn_gog_g` | 2,016,958 | not_computed |
| TR_NT | `ιραν` (iran; English: Iran)<br>`dyn_iran_g` | 4,625,438 | not_computed |
| TR_NT | `ρωσια` (rosia; English: Russia)<br>`dyn_russia_g` | 103,855 | not_computed |
| TR_NT | `βανς` (bans; English: Vance)<br>`dyn_vance_g` | 568,362 | not_computed |
| UHB | `חיה` (chayah; English: Beast)<br>`dyn_beast_h` | 164,784,929 | not_computed |
| UHB | `תנין` (tannin; English: Dragon)<br>`dyn_dragon_h` | 6,186,847 | not_computed |
| UHB | `גוג` (Gog; English: Gog)<br>`dyn_gog_h` | 5,587,606 | not_computed |
| UHB | `איראן` (yrn; English: Iran)<br>`dyn_iran_h` | 668,069 | not_computed |
| UHB | `מגוג` (Magog; English: Magog)<br>`dyn_magog_h` | 306,006 | not_computed |
| UHB | `משיח` (Mashiach; English: Messiah)<br>`dyn_messiah_h` | 5,240,076 | not_computed |
| UHB | `רוסיה` (rwsyh; English: Russia)<br>`dyn_russia_h` | 142,713 | not_computed |
| UHB | `ואנס` (wns; English: Vance)<br>`dyn_vance_h` | 1,170,235 | not_computed |
| UHB | `ישוע` (Yeshua; English: Yeshua)<br>`dyn_yeshua_h` | 11,151,829 | not_computed |
| UHB | `יהוה` (YHWH; English: YHWH)<br>`dyn_yhwh_h` | 42,792,278 | not_computed |
| UXLC | `חיה` (chayah; English: Beast)<br>`dyn_beast_h` | 163,014,892 | not_computed |
| UXLC | `תנין` (tannin; English: Dragon)<br>`dyn_dragon_h` | 6,062,411 | not_computed |
| UXLC | `גוג` (Gog; English: Gog)<br>`dyn_gog_h` | 5,536,796 | not_computed |
| UXLC | `איראן` (yrn; English: Iran)<br>`dyn_iran_h` | 692,152 | not_computed |
| UXLC | `מגוג` (Magog; English: Magog)<br>`dyn_magog_h` | 320,231 | not_computed |
| UXLC | `משיח` (Mashiach; English: Messiah)<br>`dyn_messiah_h` | 5,055,913 | not_computed |
| UXLC | `רוסיה` (rwsyh; English: Russia)<br>`dyn_russia_h` | 137,739 | not_computed |
| UXLC | `ואנס` (wns; English: Vance)<br>`dyn_vance_h` | 1,189,894 | not_computed |
| UXLC | `ישוע` (Yeshua; English: Yeshua)<br>`dyn_yeshua_h` | 10,724,706 | not_computed |
| UXLC | `יהוה` (YHWH; English: YHWH)<br>`dyn_yhwh_h` | 43,283,917 | not_computed |

## Partial Dense Rows

| Corpus | Term | Completed partitions | Hits so far | Skip ranges |
| --- | --- | ---: | ---: | --- |

## Completed Partitions

| Partition | Exported hits | Estimated hits | Delta | Exact center-word hits |
| --- | ---: | ---: | ---: | ---: |
| `BYZ_NT__dyn_gog_g__full_span__p00001_of_00002__skip_2_172632` | 1,490,888 | 995,319 | 495,569 | not_computed |
| `BYZ_NT__dyn_gog_g__full_span__p00002_of_00002__skip_172633_345263` | 499,750 | 995,319 | -495,569 | not_computed |
| `BYZ_NT__dyn_iran_g__full_span__p00001_of_00005__skip_2_46035` | 1,716,415 | 949,849 | 766,566 | not_computed |
| `BYZ_NT__dyn_iran_g__full_span__p00002_of_00005__skip_46036_92070` | 1,336,881 | 949,870 | 387,011 | not_computed |
| `BYZ_NT__dyn_iran_g__full_span__p00003_of_00005__skip_92071_138105` | 944,255 | 949,870 | -5,615 | not_computed |
| `BYZ_NT__dyn_iran_g__full_span__p00004_of_00005__skip_138106_184140` | 564,017 | 949,870 | -385,853 | not_computed |
| `BYZ_NT__dyn_iran_g__full_span__p00005_of_00005__skip_184141_230175` | 187,758 | 949,870 | -762,112 | not_computed |
| `BYZ_NT__dyn_russia_g__full_span__p00001_of_00001__skip_2_172631` | 102,577 | 102,577 | 0 | not_computed |
| `BYZ_NT__dyn_vance_g__full_span__p00001_of_00001__skip_2_230175` | 573,495 | 573,495 | 0 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00001_of_00166__skip_2_3606` | 1,902,327 | 995,332 | 906,995 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00002_of_00166__skip_3607_7212` | 1,896,076 | 995,608 | 900,468 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00003_of_00166__skip_7213_10817` | 1,887,277 | 995,332 | 891,945 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00004_of_00166__skip_10818_14423` | 1,884,484 | 995,608 | 888,876 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00005_of_00166__skip_14424_18028` | 1,876,125 | 995,332 | 880,793 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00006_of_00166__skip_18029_21634` | 1,869,431 | 995,608 | 873,823 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00007_of_00166__skip_21635_25239` | 1,856,718 | 995,332 | 861,386 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00008_of_00166__skip_25240_28845` | 1,845,291 | 995,608 | 849,683 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00009_of_00166__skip_28846_32450` | 1,836,262 | 995,332 | 840,930 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00010_of_00166__skip_32451_36056` | 1,825,685 | 995,608 | 830,077 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00011_of_00166__skip_36057_39661` | 1,823,000 | 995,332 | 827,668 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00012_of_00166__skip_39662_43267` | 1,810,272 | 995,608 | 814,664 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00013_of_00166__skip_43268_46872` | 1,801,484 | 995,332 | 806,152 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00014_of_00166__skip_46873_50478` | 1,780,232 | 995,608 | 784,624 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00015_of_00166__skip_50479_54084` | 1,771,073 | 995,608 | 775,465 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00016_of_00166__skip_54085_57689` | 1,764,147 | 995,332 | 768,815 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00017_of_00166__skip_57690_61295` | 1,754,482 | 995,608 | 758,874 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00018_of_00166__skip_61296_64900` | 1,744,011 | 995,332 | 748,679 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00019_of_00166__skip_64901_68506` | 1,736,122 | 995,608 | 740,514 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00020_of_00166__skip_68507_72111` | 1,720,760 | 995,332 | 725,428 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00021_of_00166__skip_72112_75717` | 1,699,098 | 995,608 | 703,490 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00022_of_00166__skip_75718_79322` | 1,677,955 | 995,332 | 682,623 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00023_of_00166__skip_79323_82928` | 1,665,769 | 995,608 | 670,161 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00024_of_00166__skip_82929_86533` | 1,650,673 | 995,332 | 655,341 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00025_of_00166__skip_86534_90139` | 1,637,981 | 995,608 | 642,373 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00026_of_00166__skip_90140_93744` | 1,629,887 | 995,332 | 634,555 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00027_of_00166__skip_93745_97350` | 1,624,091 | 995,608 | 628,483 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00028_of_00166__skip_97351_100956` | 1,615,935 | 995,608 | 620,327 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00029_of_00166__skip_100957_104561` | 1,602,007 | 995,332 | 606,675 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00030_of_00166__skip_104562_108167` | 1,593,119 | 995,608 | 597,511 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00031_of_00166__skip_108168_111772` | 1,580,839 | 995,332 | 585,507 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00032_of_00166__skip_111773_115378` | 1,567,759 | 995,608 | 572,151 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00033_of_00166__skip_115379_118983` | 1,552,514 | 995,332 | 557,182 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00034_of_00166__skip_118984_122589` | 1,545,568 | 995,608 | 549,960 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00035_of_00166__skip_122590_126194` | 1,529,725 | 995,332 | 534,393 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00036_of_00166__skip_126195_129800` | 1,517,620 | 995,608 | 522,012 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00037_of_00166__skip_129801_133405` | 1,508,448 | 995,332 | 513,116 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00038_of_00166__skip_133406_137011` | 1,500,375 | 995,608 | 504,767 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00039_of_00166__skip_137012_140616` | 1,485,261 | 995,332 | 489,929 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00040_of_00166__skip_140617_144222` | 1,477,501 | 995,608 | 481,893 | not_computed |
| `EBIBLE_WLC__dyn_beast_h__full_span__p00041_of_00166__skip_144223_147827` | 1,465,318 | 995,332 | 469,986 | not_computed |

## Example Hits

| Type | Corpus | Term | Skip | Center | Center word |
| --- | --- | --- | ---: | --- | --- |

## Targeted Exact-Center Follow-Ups

This broad summary used manifest-only mode, so it preserves the full
partition completion and hit-count totals without rescanning archived dense
hit payloads for center-word metadata. `not_computed` in this report means
center-word metadata was not scanned here; it does not mean exact-center
hits are absent.

| Follow-up | Purpose |
| --- | --- |
| `docs/DYNAMIC_SKIP_FULL_SPAN_HIT_FINDINGS.md` | manageable full-span hit summary with exact-center examples |
| `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_FINDINGS.md` | Bible rows where strong full-span signals were rescanned for exact centers |
| `docs/DYNAMIC_SKIP_STRONG_CONTROL_FULL_SPAN_EXACT_CENTER_FINDINGS.md` | language-matched control rows corresponding to strong Bible exact-center rows |
| `docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_ORIGINAL_LANGUAGE_FINDINGS.md` | original-language synthesis of promoted, hold, and background exact-center rows |

## Read

- Completed partition rows are no longer deferred; their hit-level metadata exists.
- Exact center-word hits are flags, not the admission rule.
- `not_computed` means the manifest-only path was used; hit counts still come from export manifests.
- Partition estimates are planning estimates; exported hit rows are observed counts.
- The ignored partition CSVs are reproducible from the tracked plan and runner.
