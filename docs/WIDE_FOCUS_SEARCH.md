# Broad Search Summary

Broader ELS count sweep across every declared term list.

## Scope

- Skip range: `2..250`
- Direction: `both`
- Term sets: 2
- Rows: 3080
- Manifest: `reports/wide_focus_search/broad_search.manifest.json`

## Main Read

- Widening to skip 250 mostly scales up already-dense short terms.
- Length 4+ leaders still come from short Greek or Hebrew forms and acronyms.
- Full modern phrases remain weak or absent; abbreviations dominate.
- Frequency anchors and null controls are useful calibration rows because they also produce high counts.

## Term Set Summary

| Term set | Corpus | Counted | Zero | Total hits | Max row |
| --- | --- | ---: | ---: | ---: | --- |
| modern_names_dates | BYZ_NT | 60 | 38 | 224269 | `united_nations_acronym_g` `οηε` (oee; English: United Nations) (129582) |
| modern_names_dates | EBIBLE_WLC | 96 | 30 | 902558 | `united_nations_acronym_h` `אומ` (wm; English: United Nations) (421163) |
| modern_names_dates | LXX | 60 | 35 | 890607 | `united_nations_acronym_g` `οηε` (oee; English: United Nations) (478782) |
| modern_names_dates | MAM | 96 | 29 | 905881 | `united_nations_acronym_h` `אומ` (wm; English: United Nations) (421699) |
| modern_names_dates | MT_WLC | 96 | 30 | 902537 | `united_nations_acronym_h` `אומ` (wm; English: United Nations) (421133) |
| modern_names_dates | SBLGNT | 60 | 39 | 221005 | `united_nations_acronym_g` `οηε` (oee; English: United Nations) (127532) |
| modern_names_dates | TCG_NT | 60 | 39 | 224548 | `united_nations_acronym_g` `οηε` (oee; English: United Nations) (130689) |
| modern_names_dates | TR_NT | 60 | 37 | 225605 | `united_nations_acronym_g` `οηε` (oee; English: United Nations) (131208) |
| modern_names_dates | UHB | 96 | 30 | 902382 | `united_nations_acronym_h` `אומ` (wm; English: United Nations) (420971) |
| modern_names_dates | UXLC | 96 | 30 | 902509 | `united_nations_acronym_h` `אומ` (wm; English: United Nations) (421106) |
| prophetic_terms | BYZ_NT | 229 | 134 | 133042 | `ur_g` `ουρ` (our; English: Ur) (66457) |
| prophetic_terms | EBIBLE_WLC | 222 | 70 | 3596530 | `greece_h` `יונ` (ywn; English: Greece) (341669) |
| prophetic_terms | LXX | 229 | 117 | 574406 | `ur_g` `ουρ` (our; English: Ur) (294528) |
| prophetic_terms | MAM | 222 | 71 | 3611016 | `greece_h` `יונ` (ywn; English: Greece) (343126) |
| prophetic_terms | MT_WLC | 222 | 70 | 3596714 | `greece_h` `יונ` (ywn; English: Greece) (341633) |
| prophetic_terms | SBLGNT | 229 | 137 | 130868 | `ur_g` `ουρ` (our; English: Ur) (65298) |
| prophetic_terms | TCG_NT | 229 | 135 | 133435 | `ur_g` `ουρ` (our; English: Ur) (67054) |
| prophetic_terms | TR_NT | 229 | 133 | 134453 | `ur_g` `ουρ` (our; English: Ur) (67379) |
| prophetic_terms | UHB | 222 | 70 | 3591196 | `greece_h` `יונ` (ywn; English: Greece) (341626) |
| prophetic_terms | UXLC | 222 | 70 | 3596679 | `greece_h` `יונ` (ywn; English: Greece) (341645) |

## Top Length 4+ Counts

| Rank | Set | Corpus | Term | Length | Hits | Read |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 1 | modern_names_dates | LXX | `nato_g` `νατο` (nato; English: NATO) | 4 | 80308 | dense short form |
| 2 | prophetic_terms | LXX | `blood_g` `αιμα` (haima; English: Blood) | 4 | 55267 | dense short form |
| 3 | modern_names_dates | LXX | `china_g` `κινα` (kina; English: China) | 4 | 55120 | dense short form |
| 4 | modern_names_dates | LXX | `iran_g` `ιραν` (iran; English: Iran) | 4 | 43838 | dense short form |
| 5 | prophetic_terms | MAM | `rome_h` `רומי` (rwmy; English: Rome) | 4 | 35090 | dense short form |
| 6 | prophetic_terms | UXLC | `rome_h` `רומי` (rwmy; English: Rome) | 4 | 35006 | dense short form |
| 7 | prophetic_terms | EBIBLE_WLC | `rome_h` `רומי` (rwmy; English: Rome) | 4 | 35005 | dense short form |
| 8 | prophetic_terms | MT_WLC | `rome_h` `רומי` (rwmy; English: Rome) | 4 | 35004 | dense short form |
| 9 | prophetic_terms | UHB | `rome_h` `רומי` (rwmy; English: Rome) | 4 | 34949 | dense short form |
| 10 | prophetic_terms | MAM | `otho_h` `אותו` (wtw; English: Otho) | 4 | 29445 | dense short form |
| 11 | prophetic_terms | UXLC | `otho_h` `אותו` (wtw; English: Otho) | 4 | 29289 | dense short form |
| 12 | prophetic_terms | MT_WLC | `otho_h` `אותו` (wtw; English: Otho) | 4 | 29280 | dense short form |
| 13 | prophetic_terms | EBIBLE_WLC | `otho_h` `אותו` (wtw; English: Otho) | 4 | 29265 | dense short form |
| 14 | prophetic_terms | UHB | `otho_h` `אותו` (wtw; English: Otho) | 4 | 29181 | dense short form |
| 15 | prophetic_terms | MAM | `mary_h` `מרימ` (mrym; English: Mary) | 4 | 27120 | dense short form |
| 16 | prophetic_terms | UHB | `mary_h` `מרימ` (mrym; English: Mary) | 4 | 27086 | dense short form |
| 17 | prophetic_terms | EBIBLE_WLC | `mary_h` `מרימ` (mrym; English: Mary) | 4 | 27036 | dense short form |
| 18 | prophetic_terms | MT_WLC | `mary_h` `מרימ` (mrym; English: Mary) | 4 | 27025 | dense short form |
| 19 | prophetic_terms | UXLC | `mary_h` `מרימ` (mrym; English: Mary) | 4 | 27022 | dense short form |
| 20 | prophetic_terms | EBIBLE_WLC | `lion_h` `אריה` (ryh; English: Lion) | 4 | 26492 | dense short form |
| 21 | prophetic_terms | MT_WLC | `lion_h` `אריה` (ryh; English: Lion) | 4 | 26477 | dense short form |
| 22 | prophetic_terms | UHB | `lion_h` `אריה` (ryh; English: Lion) | 4 | 26476 | dense short form |
| 23 | prophetic_terms | UXLC | `lion_h` `אריה` (ryh; English: Lion) | 4 | 26463 | dense short form |
| 24 | prophetic_terms | MAM | `lion_h` `אריה` (ryh; English: Lion) | 4 | 26450 | dense short form |
| 25 | prophetic_terms | LXX | `zion_g` `σιων` (Sion; English: Zion) | 4 | 25442 | dense short form |
| 26 | modern_names_dates | MAM | `bibi_h` `ביבי` (byby; English: Bibi) | 4 | 24771 | dense short form |
| 27 | modern_names_dates | MT_WLC | `bibi_h` `ביבי` (byby; English: Bibi) | 4 | 24549 | dense short form |
| 28 | modern_names_dates | EBIBLE_WLC | `bibi_h` `ביבי` (byby; English: Bibi) | 4 | 24542 | dense short form |
| 29 | modern_names_dates | UXLC | `bibi_h` `ביבי` (byby; English: Bibi) | 4 | 24537 | dense short form |
| 30 | modern_names_dates | UHB | `bibi_h` `ביבי` (byby; English: Bibi) | 4 | 24529 | dense short form |

## Focus Terms

| Concept | Corpus | Term | Length | Hits | Read |
| --- | --- | --- | ---: | ---: | --- |
| United Nations | LXX | `united_nations_acronym_g` `οηε` (oee; English: United Nations) | 3 | 478782 | high-noise short form |
| United Nations | MAM | `united_nations_acronym_h` `אומ` (wm; English: United Nations) | 3 | 421699 | high-noise short form |
| United Nations | EBIBLE_WLC | `united_nations_acronym_h` `אומ` (wm; English: United Nations) | 3 | 421163 | high-noise short form |
| United Nations | MT_WLC | `united_nations_acronym_h` `אומ` (wm; English: United Nations) | 3 | 421133 | high-noise short form |
| United Nations | UXLC | `united_nations_acronym_h` `אומ` (wm; English: United Nations) | 3 | 421106 | high-noise short form |
| United Nations | UHB | `united_nations_acronym_h` `אומ` (wm; English: United Nations) | 3 | 420971 | high-noise short form |
| USA | LXX | `usa_abbrev_g` `ηπα` (epa; English: USA) | 3 | 216290 | high-noise short form |
| United Nations | TR_NT | `united_nations_acronym_g` `οηε` (oee; English: United Nations) | 3 | 131208 | high-noise short form |
| United Nations | TCG_NT | `united_nations_acronym_g` `οηε` (oee; English: United Nations) | 3 | 130689 | high-noise short form |
| Beast | MT_WLC | `beast_h` `חיה` (chayah; English: Beast) | 3 | 130361 | high-noise short form |
| Beast | UXLC | `beast_h` `חיה` (chayah; English: Beast) | 3 | 130342 | high-noise short form |
| Beast | EBIBLE_WLC | `beast_h` `חיה` (chayah; English: Beast) | 3 | 130323 | high-noise short form |
| Beast | MAM | `beast_h` `חיה` (chayah; English: Beast) | 3 | 130136 | high-noise short form |
| Beast | UHB | `beast_h` `חיה` (chayah; English: Beast) | 3 | 130058 | high-noise short form |
| United Nations | BYZ_NT | `united_nations_acronym_g` `οηε` (oee; English: United Nations) | 3 | 129582 | high-noise short form |
| United Nations | SBLGNT | `united_nations_acronym_g` `οηε` (oee; English: United Nations) | 3 | 127532 | high-noise short form |
| USA | TR_NT | `usa_abbrev_g` `ηπα` (epa; English: USA) | 3 | 48141 | high-noise short form |
| USA | TCG_NT | `usa_abbrev_g` `ηπα` (epa; English: USA) | 3 | 47901 | high-noise short form |
| USA | BYZ_NT | `usa_abbrev_g` `ηπα` (epa; English: USA) | 3 | 47270 | high-noise short form |
| USA | SBLGNT | `usa_abbrev_g` `ηπα` (epa; English: USA) | 3 | 47047 | high-noise short form |
| Iran | LXX | `iran_g` `ιραν` (iran; English: Iran) | 4 | 43838 | dense short form |
| USA | UHB | `usa_abbrev_h` `ארהב` (rhb; English: USA) | 4 | 12627 | dense short form |
| USA | EBIBLE_WLC | `usa_abbrev_h` `ארהב` (rhb; English: USA) | 4 | 12600 | dense short form |
| USA | MT_WLC | `usa_abbrev_h` `ארהב` (rhb; English: USA) | 4 | 12580 | dense short form |
| USA | UXLC | `usa_abbrev_h` `ארהב` (rhb; English: USA) | 4 | 12572 | dense short form |
| USA | MAM | `usa_abbrev_h` `ארהב` (rhb; English: USA) | 4 | 12549 | dense short form |
| Iran | BYZ_NT | `iran_g` `ιραν` (iran; English: Iran) | 4 | 10405 | dense short form |
| Iran | SBLGNT | `iran_g` `ιραν` (iran; English: Iran) | 4 | 10019 | dense short form |
| Iran | TR_NT | `iran_g` `ιραν` (iran; English: Iran) | 4 | 10002 | dense short form |
| Iran | TCG_NT | `iran_g` `ιραν` (iran; English: Iran) | 4 | 9860 | dense short form |
| Gog | LXX | `gog_g` `γωγ` (Gog; English: Gog) | 3 | 8656 | high-noise short form |
| Dragon | MAM | `dragon_h` `תנינ` (tnyn; English: Dragon) | 4 | 7869 | dense short form |
| Dragon | UHB | `dragon_h` `תנינ` (tnyn; English: Dragon) | 4 | 7847 | dense short form |
| Dragon | UXLC | `dragon_h` `תנינ` (tnyn; English: Dragon) | 4 | 7842 | dense short form |
| Vance | LXX | `vance_g` `βανσ` (bans; English: Vance) | 4 | 7841 | dense short form |
| Dragon | MT_WLC | `dragon_h` `תנינ` (tnyn; English: Dragon) | 4 | 7839 | dense short form |
| Dragon | EBIBLE_WLC | `dragon_h` `תנינ` (tnyn; English: Dragon) | 4 | 7835 | dense short form |
| Gog | MAM | `gog_h` `גוג` (Gog; English: Gog) | 3 | 5876 | high-noise short form |
| Gog | UHB | `gog_h` `גוג` (Gog; English: Gog) | 3 | 5824 | high-noise short form |
| Gog | EBIBLE_WLC | `gog_h` `גוג` (Gog; English: Gog) | 3 | 5804 | high-noise short form |
| Gog | MT_WLC | `gog_h` `גוג` (Gog; English: Gog) | 3 | 5800 | high-noise short form |
| Gog | UXLC | `gog_h` `גוג` (Gog; English: Gog) | 3 | 5798 | high-noise short form |
| Gog | TR_NT | `gog_g` `γωγ` (Gog; English: Gog) | 3 | 2940 | high-noise short form |
| Gog | SBLGNT | `gog_g` `γωγ` (Gog; English: Gog) | 3 | 2908 | high-noise short form |
| Gog | TCG_NT | `gog_g` `γωγ` (Gog; English: Gog) | 3 | 2874 | high-noise short form |
| Gog | BYZ_NT | `gog_g` `γωγ` (Gog; English: Gog) | 3 | 2870 | high-noise short form |
| Russia | LXX | `russia_g` `ρωσια` (rosia; English: Russia) | 5 | 1499 | high count; needs controls |
| Vance | MAM | `vance_h` `ואנס` (wns; English: Vance) | 4 | 1461 | dense short form |
| Vance | MT_WLC | `vance_h` `ואנס` (wns; English: Vance) | 4 | 1461 | dense short form |
| Vance | UXLC | `vance_h` `ואנס` (wns; English: Vance) | 4 | 1459 | dense short form |
| Vance | EBIBLE_WLC | `vance_h` `ואנס` (wns; English: Vance) | 4 | 1457 | dense short form |
| Vance | UHB | `vance_h` `ואנס` (wns; English: Vance) | 4 | 1437 | dense short form |
| Vance | SBLGNT | `vance_g` `βανσ` (bans; English: Vance) | 4 | 1268 | dense short form |
| Vance | TR_NT | `vance_g` `βανσ` (bans; English: Vance) | 4 | 1251 | dense short form |
| Vance | BYZ_NT | `vance_g` `βανσ` (bans; English: Vance) | 4 | 1243 | dense short form |
| Vance | TCG_NT | `vance_g` `βανσ` (bans; English: Vance) | 4 | 1229 | dense short form |
| Iran | UXLC | `iran_h` `איראנ` (yrn; English: Iran) | 5 | 1181 | high count; needs controls |
| Iran | MT_WLC | `iran_h` `איראנ` (yrn; English: Iran) | 5 | 1180 | high count; needs controls |
| Iran | EBIBLE_WLC | `iran_h` `איראנ` (yrn; English: Iran) | 5 | 1173 | high count; needs controls |
| Iran | UHB | `iran_h` `איראנ` (yrn; English: Iran) | 5 | 1169 | high count; needs controls |

## Largest Increases Vs Skip 2..50

| Set | Corpus | Term | 2..50 | 2..250 | Delta | Ratio |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| modern_names_dates | LXX | `united_nations_acronym_g` `οηε` (oee; English: United Nations) | 95280 | 478782 | 383502 | 5.025 |
| modern_names_dates | MT_WLC | `united_nations_acronym_h` `אומ` (wm; English: United Nations) | 81340 | 421133 | 339793 | 5.177 |
| prophetic_terms | MT_WLC | `greece_h` `יונ` (ywn; English: Greece) | 67460 | 341633 | 274173 | 5.064 |
| prophetic_terms | LXX | `ur_g` `ουρ` (our; English: Ur) | 57970 | 294528 | 236558 | 5.081 |
| prophetic_terms | MT_WLC | `ur_h` `אור` (or; English: Ur) | 57065 | 290922 | 233857 | 5.098 |
| prophetic_terms | MT_WLC | `lawlessness_h` `אונ` (wn; English: Lawlessness) | 45095 | 233282 | 188187 | 5.173 |
| modern_names_dates | LXX | `usa_abbrev_g` `ηπα` (epa; English: USA) | 42727 | 216290 | 173563 | 5.062 |
| prophetic_terms | MT_WLC | `pit_h` `בור` (bwr; English: Pit) | 40037 | 200223 | 160186 | 5.001 |
| prophetic_terms | MT_WLC | `amen_h` `אמנ` (mn; English: Amen) | 34330 | 176602 | 142272 | 5.144 |
| prophetic_terms | MT_WLC | `media_h` `מדי` (Madai; English: Media) | 30131 | 152767 | 122636 | 5.07 |
| prophetic_terms | MT_WLC | `bride_h` `כלה` (klh; English: Bride) | 29217 | 148813 | 119596 | 5.093 |
| modern_names_dates | MT_WLC | `2026_compact_h` `בכו` (bkw; English: Gregorian 2026 compact) | 26284 | 136350 | 110066 | 5.188 |
| prophetic_terms | MT_WLC | `babylon_h` `בבל` (Bavel; English: Babylon) | 26900 | 135150 | 108250 | 5.024 |
| prophetic_terms | MT_WLC | `babylon_alt_h` `בבל` (Bavel; English: Babylon) | 26900 | 135150 | 108250 | 5.024 |
| modern_names_dates | TR_NT | `united_nations_acronym_g` `οηε` (oee; English: United Nations) | 25587 | 131208 | 105621 | 5.128 |
| prophetic_terms | MT_WLC | `beast_h` `חיה` (chayah; English: Beast) | 25397 | 130361 | 104964 | 5.133 |
| modern_names_dates | SBLGNT | `united_nations_acronym_g` `οηε` (oee; English: United Nations) | 24918 | 127532 | 102614 | 5.118 |
| prophetic_terms | MT_WLC | `leopard_h` `נמר` (nmr; English: Leopard) | 24749 | 126750 | 102001 | 5.121 |
| prophetic_terms | MT_WLC | `oil_h` `שמנ` (shmn; English: Oil) | 21917 | 110131 | 88214 | 5.025 |
| modern_names_dates | MT_WLC | `2025_compact_h` `בכה` (bkh; English: Gregorian 2025 compact) | 20922 | 107059 | 86137 | 5.117 |
| prophetic_terms | LXX | `fire_g` `πυρ` (pur; English: Fire) | 18516 | 95983 | 77467 | 5.184 |
| modern_names_dates | LXX | `nato_g` `νατο` (nato; English: NATO) | 15410 | 80308 | 64898 | 5.211 |
| prophetic_terms | MT_WLC | `bashan_h` `בשנ` (bshn; English: Bashan) | 14201 | 72822 | 58621 | 5.128 |
| prophetic_terms | MT_WLC | `flies_plague_h` `ערב` (rb; English: Flies Plague) | 13754 | 69503 | 55749 | 5.053 |
| prophetic_terms | MT_WLC | `famine_h` `רעב` (rb; English: Famine) | 13722 | 69377 | 55655 | 5.056 |
| prophetic_terms | TR_NT | `ur_g` `ουρ` (our; English: Ur) | 13276 | 67379 | 54103 | 5.075 |
| prophetic_terms | SBLGNT | `ur_g` `ουρ` (our; English: Ur) | 12846 | 65298 | 52452 | 5.083 |
| prophetic_terms | MT_WLC | `earthquake_h` `רעש` (rsh; English: Earthquake) | 12158 | 62149 | 49991 | 5.112 |
| prophetic_terms | LXX | `blood_g` `αιμα` (haima; English: Blood) | 11030 | 55267 | 44237 | 5.011 |
| modern_names_dates | LXX | `china_g` `κινα` (kina; English: China) | 10915 | 55120 | 44205 | 5.05 |

## Caution

This is a broad screening run. It is not a control-backed claim report. Treat high counts as queue-building only.
