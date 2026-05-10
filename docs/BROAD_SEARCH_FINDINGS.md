# Broad Search Summary

Broader ELS count sweep across every declared term list.

## Scope

- Skip range: `2..100`
- Direction: `both`
- Term sets: 12
- Rows: 6778
- Manifest: `reports/broad_search/broad_search.manifest.json`

## Main Read

- Widening to skip 100 mostly scales up already-dense short terms.
- Length 4+ leaders still come from short Greek or Hebrew forms and acronyms.
- Full modern phrases remain weak or absent; abbreviations dominate.
- Frequency anchors and null controls are useful calibration rows because they also produce high counts.

## Term Set Summary

| Term set | Corpus | Counted | Zero | Total hits | Max row |
| --- | --- | ---: | ---: | ---: | --- |
| biblical_calendar | EBIBLE_WLC | 14 | 0 | 178680 | `bul_h` `בול` (bwl; English: Bul) (102371) |
| biblical_calendar | MAM | 14 | 0 | 179280 | `bul_h` `בול` (bwl; English: Bul) (102680) |
| biblical_calendar | MT_WLC | 14 | 0 | 178704 | `bul_h` `בול` (bwl; English: Bul) (102399) |
| biblical_calendar | UHB | 14 | 0 | 178731 | `bul_h` `בול` (bwl; English: Bul) (102361) |
| biblical_calendar | UXLC | 14 | 0 | 178697 | `bul_h` `בול` (bwl; English: Bul) (102387) |
| biblical_festivals | BYZ_NT | 6 | 4 | 42 | `pesach_g` `πασχα` (pascha; English: Passover) (35) |
| biblical_festivals | EBIBLE_WLC | 13 | 4 | 47062 | `shabbat_h` `שבת` (shbt; English: Shabbat) (33067) |
| biblical_festivals | LXX | 6 | 3 | 176 | `pesach_g` `πασχα` (pascha; English: Passover) (150) |
| biblical_festivals | MAM | 13 | 3 | 47212 | `shabbat_h` `שבת` (shbt; English: Shabbat) (33273) |
| biblical_festivals | MT_WLC | 13 | 4 | 47051 | `shabbat_h` `שבת` (shbt; English: Shabbat) (33059) |
| biblical_festivals | SBLGNT | 6 | 3 | 43 | `pesach_g` `πασχα` (pascha; English: Passover) (35) |
| biblical_festivals | TCG_NT | 6 | 4 | 42 | `pesach_g` `πασχα` (pascha; English: Passover) (33) |
| biblical_festivals | TR_NT | 6 | 3 | 47 | `pesach_g` `πασχα` (pascha; English: Passover) (37) |
| biblical_festivals | UHB | 13 | 4 | 47023 | `shabbat_h` `שבת` (shbt; English: Shabbat) (33090) |
| biblical_festivals | UXLC | 13 | 4 | 47043 | `shabbat_h` `שבת` (shbt; English: Shabbat) (33053) |
| biblical_tribes | BYZ_NT | 14 | 5 | 32253 | `dan_g` `δαν` (dan; English: Dan) (23816) |
| biblical_tribes | EBIBLE_WLC | 12 | 0 | 275668 | `levi_h` `לוי` (lwy; English: Levi) (218876) |
| biblical_tribes | LXX | 14 | 3 | 111415 | `dan_g` `δαν` (dan; English: Dan) (80217) |
| biblical_tribes | MAM | 12 | 0 | 276784 | `levi_h` `לוי` (lwy; English: Levi) (219721) |
| biblical_tribes | MT_WLC | 12 | 0 | 275662 | `levi_h` `לוי` (lwy; English: Levi) (218858) |
| biblical_tribes | SBLGNT | 14 | 8 | 31767 | `dan_g` `δαν` (dan; English: Dan) (23407) |
| biblical_tribes | TCG_NT | 14 | 5 | 31313 | `dan_g` `δαν` (dan; English: Dan) (22835) |
| biblical_tribes | TR_NT | 14 | 4 | 31413 | `dan_g` `δαν` (dan; English: Dan) (22829) |
| biblical_tribes | UHB | 12 | 0 | 275567 | `levi_h` `לוי` (lwy; English: Levi) (218750) |
| biblical_tribes | UXLC | 12 | 0 | 275671 | `levi_h` `לוי` (lwy; English: Levi) (218875) |
| english_search_terms | KJV | 689 | 309 | 2229701 | `eng_dan` `dan` (195200) |
| frequency_anchors | BYZ_NT | 8 | 1 | 3790 | `laos_g` `λαοσ` (laos; English: People) (2971) |
| frequency_anchors | EBIBLE_WLC | 7 | 0 | 411043 | `yom_h` `יומ` (ywm; English: Day) (244302) |
| frequency_anchors | LXX | 8 | 1 | 15920 | `laos_g` `λαοσ` (laos; English: People) (12608) |
| frequency_anchors | MAM | 7 | 0 | 413163 | `yom_h` `יומ` (ywm; English: Day) (245539) |
| frequency_anchors | MT_WLC | 7 | 0 | 411006 | `yom_h` `יומ` (ywm; English: Day) (244260) |
| frequency_anchors | SBLGNT | 8 | 2 | 3699 | `laos_g` `λαοσ` (laos; English: People) (2975) |
| frequency_anchors | TCG_NT | 8 | 1 | 3833 | `laos_g` `λαοσ` (laos; English: People) (3068) |
| frequency_anchors | TR_NT | 8 | 1 | 3869 | `laos_g` `λαοσ` (laos; English: People) (3104) |
| frequency_anchors | UHB | 7 | 0 | 410772 | `yom_h` `יומ` (ywm; English: Day) (244067) |
| frequency_anchors | UXLC | 7 | 0 | 411009 | `yom_h` `יומ` (ywm; English: Day) (244273) |
| greek_nt_claim_terms | BYZ_NT | 32 | 17 | 4948 | `haima_gnt` `αιμα` (haima; English: Blood) (4621) |
| greek_nt_claim_terms | LXX | 32 | 12 | 23579 | `haima_gnt` `αιμα` (haima; English: Blood) (22054) |
| greek_nt_claim_terms | SBLGNT | 32 | 17 | 4855 | `haima_gnt` `αιμα` (haima; English: Blood) (4527) |
| greek_nt_claim_terms | TCG_NT | 32 | 15 | 4887 | `haima_gnt` `αιμα` (haima; English: Blood) (4575) |
| greek_nt_claim_terms | TR_NT | 32 | 16 | 4975 | `haima_gnt` `αιμα` (haima; English: Blood) (4652) |
| hebrew_claim_terms | EBIBLE_WLC | 140 | 55 | 685431 | `light_h` `אור` (or; English: Light) (115243) |
| hebrew_claim_terms | MAM | 140 | 51 | 687949 | `light_h` `אור` (or; English: Light) (115587) |
| hebrew_claim_terms | MT_WLC | 140 | 55 | 685458 | `light_h` `אור` (or; English: Light) (115238) |
| hebrew_claim_terms | UHB | 140 | 54 | 684726 | `light_h` `אור` (or; English: Light) (115249) |
| hebrew_claim_terms | UXLC | 140 | 55 | 685458 | `light_h` `אור` (or; English: Light) (115230) |
| modern_names_dates | BYZ_NT | 60 | 40 | 88708 | `united_nations_acronym_g` `οηε` (oee; English: United Nations) (51298) |
| modern_names_dates | EBIBLE_WLC | 96 | 32 | 356541 | `united_nations_acronym_h` `אומ` (wm; English: United Nations) (165755) |
| modern_names_dates | LXX | 60 | 37 | 354220 | `united_nations_acronym_g` `οηε` (oee; English: United Nations) (191280) |
| modern_names_dates | MAM | 96 | 33 | 358184 | `united_nations_acronym_h` `אומ` (wm; English: United Nations) (166493) |
| modern_names_dates | MT_WLC | 96 | 32 | 356566 | `united_nations_acronym_h` `אומ` (wm; English: United Nations) (165765) |
| modern_names_dates | SBLGNT | 60 | 40 | 87367 | `united_nations_acronym_g` `οηε` (oee; English: United Nations) (50442) |
| modern_names_dates | TCG_NT | 60 | 40 | 88703 | `united_nations_acronym_g` `οηε` (oee; English: United Nations) (51660) |
| modern_names_dates | TR_NT | 60 | 39 | 89117 | `united_nations_acronym_g` `οηε` (oee; English: United Nations) (51733) |
| modern_names_dates | UHB | 96 | 32 | 356357 | `united_nations_acronym_h` `אומ` (wm; English: United Nations) (165694) |
| modern_names_dates | UXLC | 96 | 32 | 356565 | `united_nations_acronym_h` `אומ` (wm; English: United Nations) (165766) |
| null_controls | BYZ_NT | 11 | 5 | 1614 | `scrambled_theos_g` `σθεο` (stheo; English: Scrambled God) (1586) |
| null_controls | EBIBLE_WLC | 13 | 2 | 134610 | `scrambled_moses_h` `השמ` (hshm; English: Scrambled Moses) (81477) |
| null_controls | LXX | 11 | 5 | 5486 | `scrambled_theos_g` `σθεο` (stheo; English: Scrambled God) (5362) |
| null_controls | MAM | 13 | 2 | 134957 | `scrambled_moses_h` `השמ` (hshm; English: Scrambled Moses) (81733) |
| null_controls | MT_WLC | 13 | 2 | 134600 | `scrambled_moses_h` `השמ` (hshm; English: Scrambled Moses) (81467) |
| null_controls | SBLGNT | 11 | 4 | 1549 | `scrambled_theos_g` `σθεο` (stheo; English: Scrambled God) (1520) |
| null_controls | TCG_NT | 11 | 5 | 1592 | `scrambled_theos_g` `σθεο` (stheo; English: Scrambled God) (1563) |
| null_controls | TR_NT | 11 | 5 | 1581 | `scrambled_theos_g` `σθεο` (stheo; English: Scrambled God) (1549) |
| null_controls | UHB | 13 | 2 | 134433 | `scrambled_moses_h` `השמ` (hshm; English: Scrambled Moses) (81481) |
| null_controls | UXLC | 13 | 2 | 134600 | `scrambled_moses_h` `השמ` (hshm; English: Scrambled Moses) (81466) |
| prophetic_terms | BYZ_NT | 229 | 143 | 52867 | `ur_g` `ουρ` (our; English: Ur) (26527) |
| prophetic_terms | EBIBLE_WLC | 221 | 75 | 1427243 | `greece_h` `יונ` (ywn; English: Greece) (136086) |
| prophetic_terms | LXX | 229 | 126 | 228575 | `ur_g` `ουρ` (our; English: Ur) (117550) |
| prophetic_terms | MAM | 221 | 76 | 1433092 | `greece_h` `יונ` (ywn; English: Greece) (137065) |
| prophetic_terms | MT_WLC | 221 | 75 | 1427290 | `greece_h` `יונ` (ywn; English: Greece) (136081) |
| prophetic_terms | SBLGNT | 229 | 145 | 52029 | `ur_g` `ουρ` (our; English: Ur) (25964) |
| prophetic_terms | TCG_NT | 229 | 142 | 53010 | `ur_g` `ουρ` (our; English: Ur) (26634) |
| prophetic_terms | TR_NT | 229 | 142 | 53319 | `ur_g` `ουρ` (our; English: Ur) (26737) |
| prophetic_terms | UHB | 221 | 77 | 1425083 | `greece_h` `יונ` (ywn; English: Greece) (136105) |
| prophetic_terms | UXLC | 221 | 75 | 1427254 | `greece_h` `יונ` (ywn; English: Greece) (136087) |
| table_of_nations | BYZ_NT | 91 | 32 | 89470 | `noah_g` `νωε` (Noe; English: Noah) (35247) |
| table_of_nations | EBIBLE_WLC | 86 | 2 | 1131362 | `javan_h` `יונ` (ywn; English: Javan) (136086) |
| table_of_nations | LXX | 91 | 25 | 338044 | `noah_g` `νωε` (Noe; English: Noah) (116736) |
| table_of_nations | MAM | 86 | 3 | 1135658 | `javan_h` `יונ` (ywn; English: Javan) (137065) |
| table_of_nations | MT_WLC | 86 | 2 | 1131360 | `javan_h` `יונ` (ywn; English: Javan) (136081) |
| table_of_nations | SBLGNT | 91 | 30 | 87948 | `noah_g` `νωε` (Noe; English: Noah) (34385) |
| table_of_nations | TCG_NT | 91 | 30 | 88538 | `noah_g` `νωε` (Noe; English: Noah) (34128) |
| table_of_nations | TR_NT | 91 | 29 | 88399 | `noah_g` `νωε` (Noe; English: Noah) (34092) |
| table_of_nations | UHB | 86 | 2 | 1129891 | `javan_h` `יונ` (ywn; English: Javan) (136105) |
| table_of_nations | UXLC | 86 | 2 | 1131366 | `javan_h` `יונ` (ywn; English: Javan) (136087) |
| theological_terms | BYZ_NT | 74 | 22 | 117729 | `eve_g` `ευα` (eua; English: Eve) (86765) |
| theological_terms | EBIBLE_WLC | 59 | 0 | 1015395 | `light_h` `אור` (or; English: Light) (115243) |
| theological_terms | LXX | 74 | 15 | 509870 | `eve_g` `ευα` (eua; English: Eve) (378085) |
| theological_terms | MAM | 59 | 0 | 1019006 | `light_h` `אור` (or; English: Light) (115587) |
| theological_terms | MT_WLC | 59 | 0 | 1015373 | `light_h` `אור` (or; English: Light) (115238) |
| theological_terms | SBLGNT | 74 | 21 | 116006 | `eve_g` `ευα` (eua; English: Eve) (85401) |
| theological_terms | TCG_NT | 74 | 19 | 117985 | `eve_g` `ευα` (eua; English: Eve) (87390) |
| theological_terms | TR_NT | 74 | 22 | 118581 | `eve_g` `ευα` (eua; English: Eve) (87671) |
| theological_terms | UHB | 59 | 0 | 1014467 | `light_h` `אור` (or; English: Light) (115249) |
| theological_terms | UXLC | 59 | 0 | 1015352 | `light_h` `אור` (or; English: Light) (115230) |

## Top Length 4+ Counts

| Rank | Set | Corpus | Term | Length | Hits | Read |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 1 | english_search_terms | KJV | `eng_heth` `heth` | 4 | 62273 | dense short form |
| 2 | theological_terms | LXX | `temple_g` `ναοσ` (naos; English: Temple) | 4 | 35302 | dense short form |
| 3 | modern_names_dates | LXX | `nato_g` `νατο` (nato; English: NATO) | 4 | 31674 | dense short form |
| 4 | english_search_terms | KJV | `eng_otho` `otho` | 4 | 30851 | dense short form |
| 5 | english_search_terms | KJV | `eng_nato` `nato` | 4 | 27042 | dense short form |
| 6 | theological_terms | LXX | `son_g` `υιοσ` (huios; English: Son) | 4 | 25745 | dense short form |
| 7 | english_search_terms | KJV | `eng_noah` `noah` | 4 | 24538 | dense short form |
| 8 | english_search_terms | KJV | `eng_heal` `heal` | 4 | 23995 | dense short form |
| 9 | english_search_terms | KJV | `eng_nero` `nero` | 4 | 22308 | dense short form |
| 10 | english_search_terms | KJV | `eng_nero_2` `nero` | 4 | 22308 | dense short form |
| 11 | null_controls | MAM | `scrambled_yhwh_h` `וההי` (whhy; English: Scrambled YHWH) | 4 | 22293 | dense short form |
| 12 | null_controls | MT_WLC | `scrambled_yhwh_h` `וההי` (whhy; English: Scrambled YHWH) | 4 | 22277 | dense short form |
| 13 | null_controls | EBIBLE_WLC | `scrambled_yhwh_h` `וההי` (whhy; English: Scrambled YHWH) | 4 | 22271 | dense short form |
| 14 | null_controls | UXLC | `scrambled_yhwh_h` `וההי` (whhy; English: Scrambled YHWH) | 4 | 22269 | dense short form |
| 15 | null_controls | UHB | `scrambled_yhwh_h` `וההי` (whhy; English: Scrambled YHWH) | 4 | 22204 | dense short form |
| 16 | greek_nt_claim_terms | LXX | `haima_gnt` `αιμα` (haima; English: Blood) | 4 | 22054 | dense short form |
| 17 | prophetic_terms | LXX | `blood_g` `αιμα` (haima; English: Blood) | 4 | 22054 | dense short form |
| 18 | theological_terms | LXX | `blood_g` `αιμα` (haima; English: Blood) | 4 | 22054 | dense short form |
| 19 | hebrew_claim_terms | MAM | `yhwh_h` `יהוה` (yhwh; English: YHWH) | 4 | 21812 | dense short form |
| 20 | theological_terms | MAM | `yhwh_h` `יהוה` (yhwh; English: YHWH) | 4 | 21812 | dense short form |
| 21 | modern_names_dates | LXX | `china_g` `κινα` (kina; English: China) | 4 | 21772 | dense short form |
| 22 | hebrew_claim_terms | UHB | `yhwh_h` `יהוה` (yhwh; English: YHWH) | 4 | 21640 | dense short form |
| 23 | theological_terms | UHB | `yhwh_h` `יהוה` (yhwh; English: YHWH) | 4 | 21640 | dense short form |
| 24 | hebrew_claim_terms | MT_WLC | `yhwh_h` `יהוה` (yhwh; English: YHWH) | 4 | 21626 | dense short form |
| 25 | theological_terms | MT_WLC | `yhwh_h` `יהוה` (yhwh; English: YHWH) | 4 | 21626 | dense short form |
| 26 | hebrew_claim_terms | UXLC | `yhwh_h` `יהוה` (yhwh; English: YHWH) | 4 | 21622 | dense short form |
| 27 | theological_terms | UXLC | `yhwh_h` `יהוה` (yhwh; English: YHWH) | 4 | 21622 | dense short form |
| 28 | hebrew_claim_terms | EBIBLE_WLC | `yhwh_h` `יהוה` (yhwh; English: YHWH) | 4 | 21620 | dense short form |
| 29 | theological_terms | EBIBLE_WLC | `yhwh_h` `יהוה` (yhwh; English: YHWH) | 4 | 21620 | dense short form |
| 30 | table_of_nations | LXX | `shelah_g` `σαλα` (Sala; English: Shelah) | 4 | 18310 | dense short form |

## Focus Terms

| Concept | Corpus | Term | Length | Hits | Read |
| --- | --- | --- | ---: | ---: | --- |
| United Nations | LXX | `united_nations_acronym_g` `οηε` (oee; English: United Nations) | 3 | 191280 | high-noise short form |
| United Nations | MAM | `united_nations_acronym_h` `אומ` (wm; English: United Nations) | 3 | 166493 | high-noise short form |
| United Nations | UXLC | `united_nations_acronym_h` `אומ` (wm; English: United Nations) | 3 | 165766 | high-noise short form |
| United Nations | MT_WLC | `united_nations_acronym_h` `אומ` (wm; English: United Nations) | 3 | 165765 | high-noise short form |
| United Nations | EBIBLE_WLC | `united_nations_acronym_h` `אומ` (wm; English: United Nations) | 3 | 165755 | high-noise short form |
| United Nations | UHB | `united_nations_acronym_h` `אומ` (wm; English: United Nations) | 3 | 165694 | high-noise short form |
| USA | LXX | `usa_abbrev_g` `ηπα` (epa; English: USA) | 3 | 85735 | high-noise short form |
| USA | KJV | `eng_usa` `usa` | 3 | 80819 | high-noise short form |
| United Nations | TR_NT | `united_nations_acronym_g` `οηε` (oee; English: United Nations) | 3 | 51733 | high-noise short form |
| United Nations | TCG_NT | `united_nations_acronym_g` `οηε` (oee; English: United Nations) | 3 | 51660 | high-noise short form |
| Beast | MAM | `beast_h` `חיה` (chayah; English: Beast) | 3 | 51404 | high-noise short form |
| Beast | MT_WLC | `beast_h` `חיה` (chayah; English: Beast) | 3 | 51305 | high-noise short form |
| Beast | EBIBLE_WLC | `beast_h` `חיה` (chayah; English: Beast) | 3 | 51302 | high-noise short form |
| United Nations | BYZ_NT | `united_nations_acronym_g` `οηε` (oee; English: United Nations) | 3 | 51298 | high-noise short form |
| Beast | UXLC | `beast_h` `חיה` (chayah; English: Beast) | 3 | 51295 | high-noise short form |
| Beast | UHB | `beast_h` `חיה` (chayah; English: Beast) | 3 | 51252 | high-noise short form |
| United Nations | SBLGNT | `united_nations_acronym_g` `οηε` (oee; English: United Nations) | 3 | 50442 | high-noise short form |
| USA | TR_NT | `usa_abbrev_g` `ηπα` (epa; English: USA) | 3 | 19220 | high-noise short form |
| USA | TCG_NT | `usa_abbrev_g` `ηπα` (epa; English: USA) | 3 | 18955 | high-noise short form |
| USA | BYZ_NT | `usa_abbrev_g` `ηπα` (epa; English: USA) | 3 | 18720 | high-noise short form |
| USA | SBLGNT | `usa_abbrev_g` `ηπα` (epa; English: USA) | 3 | 18649 | high-noise short form |
| Iran | LXX | `iran_g` `ιραν` (iran; English: Iran) | 4 | 17335 | dense short form |
| Gog | KJV | `eng_gog` `gog` | 3 | 15290 | high-noise short form |
| Iran | KJV | `eng_iran` `iran` | 4 | 11859 | dense short form |
| USA | UHB | `usa_abbrev_h` `ארהב` (rhb; English: USA) | 4 | 5044 | dense short form |
| USA | EBIBLE_WLC | `usa_abbrev_h` `ארהב` (rhb; English: USA) | 4 | 5035 | dense short form |
| USA | MT_WLC | `usa_abbrev_h` `ארהב` (rhb; English: USA) | 4 | 5029 | dense short form |
| USA | UXLC | `usa_abbrev_h` `ארהב` (rhb; English: USA) | 4 | 5028 | dense short form |
| USA | MAM | `usa_abbrev_h` `ארהב` (rhb; English: USA) | 4 | 4984 | dense short form |
| Iran | BYZ_NT | `iran_g` `ιραν` (iran; English: Iran) | 4 | 4048 | dense short form |
| Iran | SBLGNT | `iran_g` `ιραν` (iran; English: Iran) | 4 | 3958 | dense short form |
| Iran | TR_NT | `iran_g` `ιραν` (iran; English: Iran) | 4 | 3892 | dense short form |
| Iran | TCG_NT | `iran_g` `ιραν` (iran; English: Iran) | 4 | 3847 | dense short form |
| Gog | LXX | `gog_g` `γωγ` (Gog; English: Gog) | 3 | 3476 | high-noise short form |
| Vance | LXX | `vance_g` `βανσ` (bans; English: Vance) | 4 | 3156 | dense short form |
| Dragon | MAM | `dragon_h` `תנינ` (tnyn; English: Dragon) | 4 | 3107 | dense short form |
| Dragon | UHB | `dragon_h` `תנינ` (tnyn; English: Dragon) | 4 | 3067 | dense short form |
| Dragon | MT_WLC | `dragon_h` `תנינ` (tnyn; English: Dragon) | 4 | 3055 | dense short form |
| Dragon | EBIBLE_WLC | `dragon_h` `תנינ` (tnyn; English: Dragon) | 4 | 3054 | dense short form |
| Dragon | UXLC | `dragon_h` `תנינ` (tnyn; English: Dragon) | 4 | 3053 | dense short form |
| Gog | EBIBLE_WLC | `gog_h` `גוג` (gwg; English: Gog) | 3 | 2482 | high-noise short form |
| Gog | UHB | `gog_h` `גוג` (gwg; English: Gog) | 3 | 2482 | high-noise short form |
| Gog | MT_WLC | `gog_h` `גוג` (gwg; English: Gog) | 3 | 2480 | high-noise short form |
| Gog | UXLC | `gog_h` `גוג` (gwg; English: Gog) | 3 | 2480 | high-noise short form |
| Gog | MAM | `gog_h` `גוג` (gwg; English: Gog) | 3 | 2460 | high-noise short form |
| Gog | TR_NT | `gog_g` `γωγ` (Gog; English: Gog) | 3 | 1244 | high-noise short form |
| Gog | TCG_NT | `gog_g` `γωγ` (Gog; English: Gog) | 3 | 1212 | high-noise short form |
| Gog | SBLGNT | `gog_g` `γωγ` (Gog; English: Gog) | 3 | 1178 | high-noise short form |
| Gog | BYZ_NT | `gog_g` `γωγ` (Gog; English: Gog) | 3 | 1166 | high-noise short form |
| Beast | KJV | `eng_beast` `beast` | 5 | 584 | present; screen only |
| Beast | KJV | `eng_beast_2` `beast` | 5 | 584 | present; screen only |
| Beast | KJV | `eng_beast_3` `beast` | 5 | 584 | present; screen only |
| Vance | EBIBLE_WLC | `vance_h` `ואנס` (wns; English: Vance) | 4 | 556 | present; screen only |
| Vance | MAM | `vance_h` `ואנס` (wns; English: Vance) | 4 | 556 | present; screen only |
| Vance | MT_WLC | `vance_h` `ואנס` (wns; English: Vance) | 4 | 556 | present; screen only |
| Vance | UXLC | `vance_h` `ואנס` (wns; English: Vance) | 4 | 555 | present; screen only |
| Vance | UHB | `vance_h` `ואנס` (wns; English: Vance) | 4 | 546 | present; screen only |
| Russia | LXX | `russia_g` `ρωσια` (rosia; English: Russia) | 5 | 534 | present; screen only |
| Vance | SBLGNT | `vance_g` `βανσ` (bans; English: Vance) | 4 | 512 | present; screen only |
| Vance | BYZ_NT | `vance_g` `βανσ` (bans; English: Vance) | 4 | 501 | present; screen only |

## Largest Increases Vs Skip 2..50

| Set | Corpus | Term | 2..50 | 2..100 | Delta | Ratio |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| theological_terms | LXX | `eve_g` `ευα` (eua; English: Eve) | 185778 | 378085 | 192307 | 2.035 |
| modern_names_dates | LXX | `united_nations_acronym_g` `οηε` (oee; English: United Nations) | 95280 | 191280 | 96000 | 2.008 |
| modern_names_dates | MT_WLC | `united_nations_acronym_h` `אומ` (wm; English: United Nations) | 81340 | 165765 | 84425 | 2.038 |
| prophetic_terms | MT_WLC | `greece_h` `יונ` (ywn; English: Greece) | 67460 | 136081 | 68621 | 2.017 |
| table_of_nations | MT_WLC | `javan_h` `יונ` (ywn; English: Javan) | 67460 | 136081 | 68621 | 2.017 |
| prophetic_terms | LXX | `ur_g` `ουρ` (our; English: Ur) | 57970 | 117550 | 59580 | 2.028 |
| table_of_nations | LXX | `noah_g` `νωε` (Noe; English: Noah) | 58411 | 116736 | 58325 | 1.999 |
| prophetic_terms | MT_WLC | `ur_h` `אור` (or; English: Ur) | 57065 | 115238 | 58173 | 2.019 |
| theological_terms | MT_WLC | `light_h` `אור` (or; English: Light) | 57065 | 115238 | 58173 | 2.019 |
| theological_terms | MT_WLC | `death_h` `מות` (mavet; English: Death) | 53653 | 108729 | 55076 | 2.027 |
| theological_terms | MT_WLC | `sign_h` `אות` (wt; English: Sign) | 52905 | 107043 | 54138 | 2.023 |
| prophetic_terms | MT_WLC | `lawlessness_h` `אונ` (wn; English: Lawlessness) | 45095 | 92033 | 46938 | 2.041 |
| table_of_nations | MT_WLC | `aram_h` `ארמ` (rm; English: Aram) | 44303 | 89519 | 45216 | 2.021 |
| theological_terms | TR_NT | `eve_g` `ευα` (eua; English: Eve) | 43331 | 87671 | 44340 | 2.023 |
| theological_terms | SBLGNT | `eve_g` `ευα` (eua; English: Eve) | 42023 | 85401 | 43378 | 2.032 |
| modern_names_dates | LXX | `usa_abbrev_g` `ηπα` (epa; English: USA) | 42727 | 85735 | 43008 | 2.007 |
| table_of_nations | LXX | `hul_g` `ουλ` (Oul; English: Hul) | 40723 | 82692 | 41969 | 2.031 |
| theological_terms | MT_WLC | `truth_h` `אמת` (emet; English: Truth) | 40282 | 81693 | 41411 | 2.028 |
| theological_terms | MT_WLC | `moses_h` `משה` (Moshe; English: Moses) | 40205 | 81467 | 41262 | 2.026 |
| prophetic_terms | MT_WLC | `pit_h` `בור` (bwr; English: Pit) | 40037 | 80107 | 40070 | 2.001 |
| table_of_nations | MT_WLC | `mesha_h` `משא` (Mesha; English: Mesha) | 37261 | 75511 | 38250 | 2.027 |
| prophetic_terms | MT_WLC | `amen_h` `אמנ` (mn; English: Amen) | 34330 | 69649 | 35319 | 2.029 |
| table_of_nations | MT_WLC | `hivite_h` `חוי` (Chivvi; English: Hivite) | 33983 | 68129 | 34146 | 2.005 |
| prophetic_terms | MT_WLC | `media_h` `מדי` (Madai; English: Media) | 30131 | 60828 | 30697 | 2.019 |
| table_of_nations | MT_WLC | `madai_h` `מדי` (Madai; English: Madai) | 30131 | 60828 | 30697 | 2.019 |
| prophetic_terms | MT_WLC | `bride_h` `כלה` (klh; English: Bride) | 29217 | 59049 | 29832 | 2.021 |
| theological_terms | MT_WLC | `king_h` `מלכ` (mlk; English: King) | 28501 | 57666 | 29165 | 2.023 |
| theological_terms | MT_WLC | `sarah_h` `שרה` (shrh; English: Sarah) | 27925 | 56109 | 28184 | 2.009 |
| prophetic_terms | MT_WLC | `babylon_h` `בבל` (Bavel; English: Babylon) | 26900 | 54493 | 27593 | 2.026 |
| prophetic_terms | MT_WLC | `babylon_alt_h` `בבל` (Bavel; English: Babylon) | 26900 | 54493 | 27593 | 2.026 |

## Caution

This is a broad screening run. It is not a control-backed claim report. Treat high counts as queue-building only.
