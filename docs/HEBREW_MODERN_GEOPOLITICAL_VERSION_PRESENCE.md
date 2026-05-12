# Hebrew Modern Geopolitical Version Presence

This report compares exact ELS hit ref-key patterns across configured
corpora. A pattern key is term + normalized term + signed skip + direction
+ canonical start/center/end refs. Offsets are reported separately because
source streams can differ in length.

## Scope

- Skip range: `2..100`
- Direction: `both`
- Minimum normalized term length: `4`
- Max hits per term per corpus: `200`
- Language: `hebrew`
- Term files: `terms/modern_names_dates.csv`

## Current Read

This run found 7,589 exact ref-key pattern rows across 87 normalized terms that met the length gate.
All-observed-source rows: 4,625; Leningrad-family-only rows: 1,264; source-specific rows: 1,581.
Highest all-source buckets are: `india_h`, `usa_abbrev_h`, `haifa_h`, `5786_jewish_h`, `alliance_h`, `bibi_h`, `jordan_country_h`, `yemen_h`.
No exact patterns in the capped scan for: `ariel_sharon_pm_h`, `benjamin_netanyahu_pm_h`, `catering_h`, `coalition_h`, `confederacy_h`, `cowboy_catering_h`, `david_ben_gurion_h`, `donald_trump_h`, `ehud_barak_pm_h`, `ehud_olmert_pm_h`, `european_union_h`, `golda_meir_h`, `levi_eshkol_h`, `menachem_begin_h`, `naftali_bennett_h`, `oct_7_text_h`, `palestine_h`, `pope_h`, plus 13 more.

Interpretation: this is a source-version distribution report, not a
significance report. Version stability is common for short strings across
related MT-family streams, so stable rows should be treated as review
queue material until separate controls and context review are applied.

## Pattern Scope Counts

| Scope | Patterns |
| --- | ---: |
| `present_all_observed_sources` | 4625 |
| `present_all_leningrad_streams` | 1264 |
| `present_multiple_sources` | 119 |
| `source_specific` | 1581 |

## Term Summary

| Term | Hits by corpus | Unique patterns | All observed | All Leningrad-family | Multi-source | Source-specific | Read |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `5786_jewish_h` `תשפו` (tshpw; English: Hebrew year 5786) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 227 | 176 | 24 | 0 | 27 | has exact patterns stable across all observed streams |
| `lebanon_h` `לבנונ` (lbnwn; English: Lebanon) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 279 | 139 | 60 | 1 | 79 | has exact patterns stable across all observed streams |
| `likud_h` `ליכוד` (lykwd; English: Likud) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 278 | 135 | 64 | 1 | 78 | has exact patterns stable across all observed streams |
| `alliance_h` `ברית` (bryt; English: Alliance) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 221 | 176 | 22 | 8 | 15 | has exact patterns stable across all observed streams |
| `haifa_h` `חיפה` (chyph; English: Haifa) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 225 | 177 | 21 | 2 | 25 | has exact patterns stable across all observed streams |
| `hamas_h` `חמאס` (chms; English: Hamas) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 266 | 136 | 62 | 8 | 60 | has exact patterns stable across all observed streams |
| `israel_h` `ישראל` (Yisrael; English: Israel) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 253 | 156 | 42 | 3 | 52 | has exact patterns stable across all observed streams |
| `pandemic_h` `מגפה` (mgph; English: Pandemic) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 257 | 151 | 47 | 2 | 57 | has exact patterns stable across all observed streams |
| `5784_jewish_h` `תשפד` (tshpd; English: Hebrew year 5784) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 261 | 150 | 47 | 4 | 60 | has exact patterns stable across all observed streams |
| `biden_h` `ביידנ` (byydn; English: Biden) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 272 | 136 | 61 | 4 | 71 | has exact patterns stable across all observed streams |
| `india_h` `הודו` (hwdw; English: India) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 222 | 180 | 17 | 3 | 22 | has exact patterns stable across all observed streams |
| `jordan_country_h` `ירדנ` (yrdn; English: Jordan) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 230 | 175 | 22 | 4 | 29 | has exact patterns stable across all observed streams |
| `nato_h` `נאטו` (ntw; English: NATO) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 242 | 165 | 32 | 4 | 41 | has exact patterns stable across all observed streams |
| `vance_h` `ואנס` (wns; English: Vance) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 248 | 160 | 37 | 5 | 46 | has exact patterns stable across all observed streams |
| `yemen_h` `תימנ` (tymn; English: Yemen) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 227 | 174 | 23 | 2 | 28 | has exact patterns stable across all observed streams |
| `iran_h` `איראנ` (yrn; English: Iran) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 251 | 159 | 37 | 4 | 51 | has exact patterns stable across all observed streams |
| `mossad_h` `מוסד` (mwsd; English: Mossad) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 275 | 135 | 61 | 6 | 73 | has exact patterns stable across all observed streams |
| `obama_h` `אובמה` (wbmh; English: Obama) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 234 | 167 | 29 | 7 | 31 | has exact patterns stable across all observed streams |
| `5785_jewish_h` `תשפה` (tshph; English: Hebrew year 5785) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 237 | 165 | 30 | 5 | 37 | has exact patterns stable across all observed streams |
| `isis_h` `דאעש` (dsh; English: ISIS) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 232 | 172 | 23 | 6 | 31 | has exact patterns stable across all observed streams |
| `usa_abbrev_h` `ארהב` (rhb; English: USA) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 227 | 178 | 17 | 9 | 23 | has exact patterns stable across all observed streams |
| `bibi_h` `ביבי` (byby; English: Bibi) | EBIBLE_WLC:200; MAM:200; MT_WLC:200; UHB:200; UXLC:200 | 241 | 175 | 17 | 4 | 45 | has exact patterns stable across all observed streams |
| `knesset_h` `כנסת` (knst; English: Knesset) | EBIBLE_WLC:158; MAM:176; MT_WLC:158; UHB:159; UXLC:158 | 223 | 115 | 41 | 4 | 63 | has exact patterns stable across all observed streams |
| `france_h` `צרפת` (tsrpt; English: France) | EBIBLE_WLC:156; MAM:161; MT_WLC:156; UHB:153; UXLC:156 | 192 | 127 | 28 | 1 | 36 | has exact patterns stable across all observed streams |
| `egypt_modern_h` `מצרימ` (Mitzrayim; English: Egypt Modern) | EBIBLE_WLC:153; MAM:152; MT_WLC:153; UHB:145; UXLC:152 | 207 | 103 | 46 | 5 | 53 | has exact patterns stable across all observed streams |
| `vatican_h` `ותיקנ` (wtyqn; English: Vatican) | EBIBLE_WLC:102; MAM:111; MT_WLC:102; UHB:101; UXLC:102 | 138 | 76 | 23 | 4 | 35 | has exact patterns stable across all observed streams |
| `syria_h` `סוריה` (swryh; English: Syria) | EBIBLE_WLC:94; MAM:103; MT_WLC:94; UHB:91; UXLC:94 | 128 | 71 | 22 | 1 | 34 | has exact patterns stable across all observed streams |
| `year_5786_jewish_h` `התשפו` (htshpw; English: Hebrew year 5786) | EBIBLE_WLC:95; MAM:96; MT_WLC:95; UHB:95; UXLC:94 | 129 | 66 | 27 | 2 | 34 | has exact patterns stable across all observed streams |
| `russia_h` `רוסיה` (rwsyh; English: Russia) | EBIBLE_WLC:91; MAM:94; MT_WLC:91; UHB:93; UXLC:91 | 132 | 58 | 32 | 1 | 41 | has exact patterns stable across all observed streams |
| `iraq_h` `עיראק` (yrq; English: Iraq) | EBIBLE_WLC:77; MAM:74; MT_WLC:77; UHB:80; UXLC:77 | 105 | 53 | 24 | 0 | 28 | has exact patterns stable across all observed streams |
| `jd_h` `גיידי` (gyydy; English: JD) | EBIBLE_WLC:76; MAM:82; MT_WLC:76; UHB:68; UXLC:76 | 117 | 40 | 36 | 0 | 41 | has exact patterns stable across all observed streams |
| `donald_h` `דונלד` (dwnld; English: Donald) | EBIBLE_WLC:75; MAM:76; MT_WLC:75; UHB:78; UXLC:75 | 106 | 51 | 23 | 1 | 31 | has exact patterns stable across all observed streams |
| `covid_h` `קוביד` (qwbyd; English: COVID) | EBIBLE_WLC:64; MAM:73; MT_WLC:64; UHB:65; UXLC:64 | 89 | 52 | 12 | 0 | 25 | has exact patterns stable across all observed streams |
| `5787_jewish_h` `תשפז` (tshpz; English: Hebrew year 5787) | EBIBLE_WLC:62; MAM:59; MT_WLC:63; UHB:57; UXLC:63 | 79 | 43 | 19 | 1 | 16 | has exact patterns stable across all observed streams |
| `harris_h` `האריס` (hrys; English: Harris) | EBIBLE_WLC:64; MAM:62; MT_WLC:64; UHB:62; UXLC:64 | 92 | 36 | 25 | 3 | 28 | has exact patterns stable across all observed streams |
| `vance_alt_h` `ווענס` (wwns; English: Vance alt) | EBIBLE_WLC:39; MAM:38; MT_WLC:39; UHB:41; UXLC:39 | 59 | 23 | 16 | 0 | 20 | has exact patterns stable across all observed streams |
| `benjamin_h` `בנימינ` (bnymyn; English: Benjamin) | EBIBLE_WLC:31; MAM:35; MT_WLC:31; UHB:33; UXLC:31 | 50 | 19 | 12 | 0 | 19 | has exact patterns stable across all observed streams |
| `tel_aviv_h` `תלאביב` (tlbyb; English: Tel Aviv) | EBIBLE_WLC:30; MAM:23; MT_WLC:29; UHB:29; UXLC:29 | 39 | 18 | 11 | 1 | 9 | has exact patterns stable across all observed streams |
| `turkey_alt_h` `תורכיה` (twrkyh; English: Turkey) | EBIBLE_WLC:30; MAM:33; MT_WLC:29; UHB:32; UXLC:29 | 43 | 24 | 5 | 0 | 14 | has exact patterns stable across all observed streams |
| `netanyahu_h` `נתניהו` (ntnyhw; English: Netanyahu) | EBIBLE_WLC:27; MAM:25; MT_WLC:27; UHB:25; UXLC:27 | 38 | 15 | 12 | 0 | 11 | has exact patterns stable across all observed streams |
| `year_5784_jewish_h` `התשפד` (htshpd; English: Hebrew year 5784) | EBIBLE_WLC:27; MAM:27; MT_WLC:27; UHB:28; UXLC:27 | 34 | 21 | 6 | 0 | 7 | has exact patterns stable across all observed streams |
| `europe_h` `אירופה` (yrwph; English: Europe) | EBIBLE_WLC:22; MAM:19; MT_WLC:22; UHB:20; UXLC:22 | 32 | 10 | 10 | 2 | 10 | has exact patterns stable across all observed streams |
| `korea_h` `קוריאה` (qwryh; English: Korea) | EBIBLE_WLC:17; MAM:17; MT_WLC:17; UHB:14; UXLC:17 | 23 | 9 | 8 | 0 | 6 | has exact patterns stable across all observed streams |
| `moshe_sharett_h` `משהשרת` (mshhshrt; English: Moshe Sharett) | EBIBLE_WLC:18; MAM:18; MT_WLC:17; UHB:16; UXLC:17 | 22 | 13 | 4 | 1 | 4 | has exact patterns stable across all observed streams |
| `vaccine_h` `חיסונ` (chyswn; English: Vaccine) | EBIBLE_WLC:17; MAM:18; MT_WLC:17; UHB:16; UXLC:17 | 25 | 11 | 6 | 0 | 8 | has exact patterns stable across all observed streams |
| `america_h` `אמריקה` (mryqh; English: America) | EBIBLE_WLC:12; MAM:11; MT_WLC:12; UHB:12; UXLC:12 | 17 | 6 | 6 | 0 | 5 | has exact patterns stable across all observed streams |
| `cowboy_h` `קאובוי` (qwbwy; English: Cowboy) | EBIBLE_WLC:12; MAM:15; MT_WLC:12; UHB:11; UXLC:12 | 19 | 8 | 4 | 0 | 7 | has exact patterns stable across all observed streams |
| `putin_h` `פוטינ` (pwtyn; English: Putin) | EBIBLE_WLC:11; MAM:10; MT_WLC:11; UHB:13; UXLC:11 | 16 | 7 | 4 | 0 | 5 | has exact patterns stable across all observed streams |
| `germany_h` `גרמניה` (grmnyh; English: Germany) | EBIBLE_WLC:8; MAM:6; MT_WLC:8; UHB:8; UXLC:8 | 12 | 3 | 5 | 0 | 4 | has exact patterns stable across all observed streams |
| `trump_h` `טראמפ` (trmp; English: Trump) | EBIBLE_WLC:6; MAM:7; MT_WLC:6; UHB:6; UXLC:6 | 7 | 6 | 0 | 0 | 1 | has exact patterns stable across all observed streams |
| `2027_additive_h` `תתתתתכז` (tttttkz; English: Gregorian 2027 additive) | EBIBLE_WLC:2; MAM:3; MT_WLC:2; UHB:2; UXLC:2 | 3 | 2 | 0 | 0 | 1 | has exact patterns stable across all observed streams |
| `2025_additive_h` `תתתתתכה` (tttttkh; English: Gregorian 2025 additive) | EBIBLE_WLC:1; MAM:0; MT_WLC:1; UHB:3; UXLC:1 | 3 | 0 | 1 | 0 | 2 | has exact patterns stable across Leningrad-family streams |
| `2026_additive_h` `תתתתתכו` (tttttkw; English: Gregorian 2026 additive) | EBIBLE_WLC:1; MAM:0; MT_WLC:1; UHB:1; UXLC:1 | 1 | 0 | 1 | 0 | 0 | has exact patterns stable across Leningrad-family streams |
| `moscow_h` `מוסקבה` (mwsqbh; English: Moscow) | EBIBLE_WLC:1; MAM:2; MT_WLC:1; UHB:1; UXLC:1 | 2 | 1 | 0 | 0 | 1 | has exact patterns stable across all observed streams |
| `turkey_h` `טורקיה` (twrqyh; English: Turkey) | EBIBLE_WLC:1; MAM:1; MT_WLC:1; UHB:1; UXLC:1 | 1 | 1 | 0 | 0 | 0 | has exact patterns stable across all observed streams |
| `2024_additive_h` `תתתתתכד` (tttttkd; English: Gregorian 2024 additive) | EBIBLE_WLC:0; MAM:1; MT_WLC:0; UHB:0; UXLC:0 | 1 | 0 | 0 | 0 | 1 | only source-specific exact patterns in capped scan |
| `ariel_sharon_pm_h` `אריאלשרונ` (rylshrwn; English: Ariel Sharon) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `benjamin_netanyahu_pm_h` `בנימיננתניהו` (bnymynntnyhw; English: Benjamin Netanyahu) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `catering_h` `קייטרינג` (qyytryng; English: Catering) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `coalition_h` `קואליציה` (qwlytsyh; English: Coalition) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `confederacy_h` `קונפדרציה` (qwnpdrtsyh; English: Confederacy) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `cowboy_catering_h` `קאובויקייטרינג` (qwbwyqyytryng; English: Cowboy Catering) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `david_ben_gurion_h` `דודבנגוריונ` (dwdbngwrywn; English: David Ben-Gurion) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `donald_trump_h` `דונלדטראמפ` (dwnldtrmp; English: Donald Trump) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `ehud_barak_pm_h` `אהודברק` (hwdbrq; English: Ehud Barak) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `ehud_olmert_pm_h` `אהודאולמרט` (hwdwlmrt; English: Ehud Olmert) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `european_union_h` `האיחודהאירופי` (hychwdhyrwpy; English: European Union) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `golda_meir_h` `גולדהמאיר` (gwldhmyr; English: Golda Meir) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `levi_eshkol_h` `לויאשכול` (lwyshkwl; English: Levi Eshkol) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `menachem_begin_h` `מנחמבגינ` (mnchmbgyn; English: Menachem Begin) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `naftali_bennett_h` `נפתליבנט` (nptlybnt; English: Naftali Bennett) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `oct_7_text_h` `שבעהבאוקטובר` (shbhbwqtwbr; English: October 7) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `palestine_h` `פלסטינ` (plstyn; English: Palestine) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `pope_h` `אפיפיור` (pypywr; English: Pope) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `saudi_arabia_h` `ערבהסעודית` (rbhswdyt; English: Saudi Arabia) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `shimon_peres_pm_h` `שמעונפרס` (shmwnprs; English: Shimon Peres) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `simsberry_h` `סימסברי` (symsbry; English: Simsberry) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `simscorner_h` `סימסקורנר` (symsqwrnr; English: Simscorner) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `ukraine_h` `אוקראינה` (wqrynh; English: Ukraine) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |
| `united_nations_h` `האומותהמאוחדות` (hwmwthmwchdwt; English: United Nations) | EBIBLE_WLC:0; MAM:0; MT_WLC:0; UHB:0; UXLC:0 | 0 | 0 | 0 | 0 | 0 | no exact patterns in capped scan |

## Strongest Shared Pattern Rows

| Term | Skip | Refs | Present | Absent | Read |
| --- | ---: | --- | --- | --- | --- |
| `alliance_h` `ברית` (bryt; English: Alliance) | -5 | 1Chr 10:9 / 1Chr 10:9 / 1Chr 10:9 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 5 | 1Chr 14:17 / 1Chr 14:17 / 1Chr 14:17 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 2 | 1Chr 1:49 / 1Chr 1:50 / 1Chr 1:50 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | 1Chr 28:6 / 1Chr 28:6 / 1Chr 28:6 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | 1Chr 29:4 / 1Chr 29:4 / 1Chr 29:4 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | 1Chr 29:7 / 1Chr 29:7 / 1Chr 29:7 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 6 | 1Chr 4:40 / 1Chr 4:40 / 1Chr 4:40 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 2 | 1Kgs 11:34 / 1Kgs 11:34 / 1Kgs 11:34 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | 1Kgs 13:31 / 1Kgs 13:31 / 1Kgs 13:31 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -5 | 1Kgs 14:10 / 1Kgs 14:10 / 1Kgs 14:10 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -5 | 1Kgs 16:3 / 1Kgs 16:3 / 1Kgs 16:2 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 4 | 1Kgs 16:34 / 1Kgs 16:34 / 1Kgs 16:34 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | 1Kgs 16:34 / 1Kgs 16:34 / 1Kgs 16:34 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 4 | 1Kgs 19:21 / 1Kgs 19:21 / 1Kgs 19:21 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | 1Kgs 6:15 / 1Kgs 6:15 / 1Kgs 6:15 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 6 | 1Kgs 6:25 / 1Kgs 6:25 / 1Kgs 6:25 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 6 | 1Kgs 7:10 / 1Kgs 7:10 / 1Kgs 7:10 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 2 | 1Kgs 7:29 / 1Kgs 7:29 / 1Kgs 7:29 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 2 | 1Sam 11:7 / 1Sam 11:7 / 1Sam 11:7 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | 1Sam 15:17 / 1Sam 15:17 / 1Sam 15:17 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 2 | 1Sam 1:19 / 1Sam 1:19 / 1Sam 1:19 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | 1Sam 20:30 / 1Sam 20:30 / 1Sam 20:30 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 2 | 1Sam 3:15 / 1Sam 3:15 / 1Sam 3:15 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | 1Sam 7:6 / 1Sam 7:6 / 1Sam 7:6 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -2 | 2Chr 13:22 / 2Chr 13:22 / 2Chr 13:21 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 2 | 2Chr 17:12 / 2Chr 17:12 / 2Chr 17:12 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | 2Chr 24:16 / 2Chr 24:16 / 2Chr 24:15 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -2 | 2Chr 35:26 / 2Chr 35:26 / 2Chr 35:25 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 4 | 2Chr 3:16 / 2Chr 3:16 / 2Chr 3:17 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 5 | 2Chr 7:3 / 2Chr 7:3 / 2Chr 7:3 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | 2Kgs 14:1 / 2Kgs 13:25 / 2Kgs 13:25 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 6 | 2Kgs 14:21 / 2Kgs 14:21 / 2Kgs 14:21 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 4 | 2Kgs 17:24 / 2Kgs 17:24 / 2Kgs 17:25 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 2 | 2Kgs 23:27 / 2Kgs 23:27 / 2Kgs 23:27 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 2 | 2Sam 11:14 / 2Sam 11:14 / 2Sam 11:14 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -5 | 2Sam 18:8 / 2Sam 18:8 / 2Sam 18:8 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 2 | 2Sam 4:11 / 2Sam 4:11 / 2Sam 4:11 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -2 | 2Sam 7:29 / 2Sam 7:29 / 2Sam 7:29 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | Deut 11:3 / Deut 11:3 / Deut 11:3 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | Deut 12:29 / Deut 12:29 / Deut 12:29 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 2 | Deut 21:16 / Deut 21:17 / Deut 21:17 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 5 | Deut 32:51 / Deut 32:51 / Deut 32:51 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | Deut 3:4 / Deut 3:4 / Deut 3:4 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -5 | Deut 4:21 / Deut 4:21 / Deut 4:21 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 3 | Esth 9:12 / Esth 9:12 / Esth 9:12 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | Exod 15:9 / Exod 15:9 / Exod 15:8 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 5 | Exod 16:3 / Exod 16:3 / Exod 16:3 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 6 | Exod 16:30 / Exod 16:31 / Exod 16:31 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | Exod 1:13 / Exod 1:13 / Exod 1:13 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -2 | Exod 24:7 / Exod 24:7 / Exod 24:7 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | Exod 25:11 / Exod 25:11 / Exod 25:11 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | Exod 28:29 / Exod 28:29 / Exod 28:29 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 6 | Exod 36:15 / Exod 36:15 / Exod 36:15 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | Exod 38:31 / Exod 38:31 / Exod 38:31 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | Exod 3:9 / Exod 3:9 / Exod 3:9 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | Exod 4:14 / Exod 4:14 / Exod 4:14 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 5 | Exod 4:31 / Exod 4:31 / Exod 4:31 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 5 | Ezek 12:13 / Ezek 12:13 / Ezek 12:13 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | Ezek 16:24 / Ezek 16:24 / Ezek 16:24 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -5 | Ezek 20:1 / Ezek 20:1 / Ezek 20:1 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 3 | Ezek 32:2 / Ezek 32:2 / Ezek 32:2 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | Ezek 32:3 / Ezek 32:3 / Ezek 32:3 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 2 | Ezek 33:22 / Ezek 33:22 / Ezek 33:22 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 6 | Ezek 37:5 / Ezek 37:5 / Ezek 37:6 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -5 | Ezek 39:21 / Ezek 39:21 / Ezek 39:21 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | Ezek 43:23 / Ezek 43:23 / Ezek 43:23 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | Ezek 4:3 / Ezek 4:3 / Ezek 4:3 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | Ezek 7:21 / Ezek 7:21 / Ezek 7:21 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | Ezra 10:3 / Ezra 10:3 / Ezra 10:3 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | Ezra 2:16 / Ezra 2:15 / Ezra 2:15 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 6 | Ezra 7:28 / Ezra 7:28 / Ezra 7:28 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -2 | Gen 13:8 / Gen 13:8 / Gen 13:8 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | Gen 19:29 / Gen 19:29 / Gen 19:29 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | Gen 23:3 / Gen 23:3 / Gen 23:3 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 6 | Gen 24:38 / Gen 24:39 / Gen 24:39 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -3 | Gen 29:13 / Gen 29:13 / Gen 29:13 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -5 | Gen 31:36 / Gen 31:36 / Gen 31:35 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | -4 | Gen 35:2 / Gen 35:2 / Gen 35:2 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 2 | Gen 36:38 / Gen 36:39 / Gen 36:39 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |
| `alliance_h` `ברית` (bryt; English: Alliance) | 2 | Gen 41:18 / Gen 41:18 / Gen 41:18 | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |  | same ref-key pattern present in every compatible corpus |

## Caution

This is exact ref-key presence in a capped hit scan. It does not prove
textual identity, and it can miss later hits once the per-term cap is
reached. Use it to find stable review rows, not to score significance.
