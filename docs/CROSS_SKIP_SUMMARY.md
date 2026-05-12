# Cross-Skip Summary

Status: post-search review aid, not claim promotion.

This report summarizes centered rows where another declared term appears
at the same center word, at a shared hidden-letter position, or within
the configured endpoint-letter distance at a different skip. It depends
on the already-built match-strata index and does not perform a new ELS
search.

## Settings

- Strata input: `reports/match_strata_index/occurrence_strata.csv`
- Input rows: `923`
- Candidate rows: `231`

## Overall Counts

Buckets may overlap. Candidate rows are the union of rows with any
cross-skip pair flag.

| Bucket | Rows |
| --- | ---: |
| `cross_skip_pair_at_word` | 122 |
| `cross_skip_pair_at_letter` | 171 |
| `cross_skip_pair_within_N_letters` | 228 |
| `no_cross_skip_pair_data` | 692 |

## Source / Corpus Summary

| Source family | Corpus class | Corpus | Bucket | Rows | Distinct terms | Share |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `all_codes_followup` | `bible` | `` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `all_codes_followup` | `bible` | `` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `all_codes_followup` | `bible` | `` | `cross_skip_pair_within_N_letters` | 2 | 2 | 0.027027 |
| `all_codes_followup` | `bible` | `` | `no_cross_skip_pair_data` | 72 | 52 | 0.972973 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `cross_skip_pair_at_word` | 9 | 6 | 0.310345 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `cross_skip_pair_at_letter` | 10 | 8 | 0.344828 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `cross_skip_pair_within_N_letters` | 25 | 11 | 0.862069 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `no_cross_skip_pair_data` | 2 | 2 | 0.068966 |
| `gog_source_review` | `bible` | `BYZ_NT` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `cross_skip_pair_within_N_letters` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `no_cross_skip_pair_data` | 1 | 1 | 1.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `cross_skip_pair_within_N_letters` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `no_cross_skip_pair_data` | 1 | 1 | 1.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `cross_skip_pair_within_N_letters` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `no_cross_skip_pair_data` | 1 | 1 | 1.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `cross_skip_pair_within_N_letters` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `no_cross_skip_pair_data` | 1 | 1 | 1.000000 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `cross_skip_pair_at_word` | 113 | 51 | 0.556650 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `cross_skip_pair_at_letter` | 161 | 65 | 0.793103 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `cross_skip_pair_within_N_letters` | 201 | 71 | 0.990148 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `no_cross_skip_pair_data` | 1 | 1 | 0.004926 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `cross_skip_pair_within_N_letters` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `no_cross_skip_pair_data` | 4 | 1 | 1.000000 |
| `original_language_findings` | `bible` | `LXX` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `LXX` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `LXX` | `cross_skip_pair_within_N_letters` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `LXX` | `no_cross_skip_pair_data` | 57 | 1 | 1.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `cross_skip_pair_within_N_letters` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `no_cross_skip_pair_data` | 1 | 1 | 1.000000 |
| `original_language_findings` | `bible` | `UHB` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `UHB` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `UHB` | `cross_skip_pair_within_N_letters` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `UHB` | `no_cross_skip_pair_data` | 14 | 1 | 1.000000 |
| `strong_full_span_exact_center` | `bible` | `EBIBLE_WLC` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `EBIBLE_WLC` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `EBIBLE_WLC` | `cross_skip_pair_within_N_letters` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `EBIBLE_WLC` | `no_cross_skip_pair_data` | 4 | 1 | 1.000000 |
| `strong_full_span_exact_center` | `bible` | `KJV` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `KJV` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `KJV` | `cross_skip_pair_within_N_letters` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `KJV` | `no_cross_skip_pair_data` | 377 | 1 | 1.000000 |
| `strong_full_span_exact_center` | `bible` | `LXX` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `LXX` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `LXX` | `cross_skip_pair_within_N_letters` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `LXX` | `no_cross_skip_pair_data` | 57 | 1 | 1.000000 |
| `strong_full_span_exact_center` | `bible` | `TCG_NT` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `TCG_NT` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `TCG_NT` | `cross_skip_pair_within_N_letters` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `TCG_NT` | `no_cross_skip_pair_data` | 1 | 1 | 1.000000 |
| `strong_full_span_exact_center` | `bible` | `UHB` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `UHB` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `UHB` | `cross_skip_pair_within_N_letters` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `UHB` | `no_cross_skip_pair_data` | 14 | 1 | 1.000000 |
| `strong_full_span_exact_center` | `control` | `ENG_PG_SHAKESPEARE` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `control` | `ENG_PG_SHAKESPEARE` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `control` | `ENG_PG_SHAKESPEARE` | `cross_skip_pair_within_N_letters` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `control` | `ENG_PG_SHAKESPEARE` | `no_cross_skip_pair_data` | 1 | 1 | 1.000000 |
| `strong_full_span_exact_center` | `control` | `HEB_PBY_BIALIK` | `cross_skip_pair_at_word` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `control` | `HEB_PBY_BIALIK` | `cross_skip_pair_at_letter` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `control` | `HEB_PBY_BIALIK` | `cross_skip_pair_within_N_letters` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `control` | `HEB_PBY_BIALIK` | `no_cross_skip_pair_data` | 83 | 2 | 1.000000 |

## Candidate Rows

| Source family | Corpus | Term | Center ref | Center word | Skip | Pair types | Pair terms |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| `all_codes_followup` | `` | `javan_g` | `1Pet 5:13` | `Βαβυλῶνι` | `-2` | cross_skip_pair_within_N_letters | ελκη |
| `apocrypha_bridge_context` | `LXX` | `mary_g;maria_gnt` | `MAL 4:6` | `Ἰσραὴλ` | `29` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | αδαμ;ελαμ |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_torah;eng_torah_2;eng_torah_3` | `MAT 1:1` | `Abraham.` | `145` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | gate |
| `all_codes_followup` | `` | `boils_g` | `1Pet 5:13` | `συνεκλεκτή` | `2` | cross_skip_pair_within_N_letters | ιωυαν |
| `apocrypha_bridge_context` | `LXX` | `amen_g` | `MAL 4:6` | `δικαιώματα.` | `191` | cross_skip_pair_at_word;cross_skip_pair_within_N_letters | ελαμ;σιων |
| `apocrypha_bridge_context` | `LXX` | `ammon_g` | `TOB 1:3` | `ἐμοῦ` | `-248` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | αμην |
| `apocrypha_bridge_context` | `LXX` | `zion_g` | `MAL 4:6` | `δικαιώματα.` | `-154` | cross_skip_pair_at_word;cross_skip_pair_within_N_letters | αμην;ελαμ |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_admah` | `MAT 1:4` | `Salmon;` | `-131` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | heth |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_ahab` | `MAT 1:1` | `generation` | `145` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | gate;obal;star |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_altar` | `TOB 1:4` | `country,` | `-234` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | rent |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_aram` | `MAT 1:4` | `begat` | `-148` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | adam |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_bush` | `2ES 16:77` | `a` | `203` | cross_skip_pair_within_N_letters | hail;hand;hits;horn;house;mash;otho;resen |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_eden` | `MAL 4:4` | `judgments.` | `233` | cross_skip_pair_at_word;cross_skip_pair_within_N_letters | heth |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_ehyeh` | `2ES 16:76` | `you` | `-145` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | teeth |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_elam;eng_elam_2` | `TOB 1:2` | `at` | `222` | cross_skip_pair_within_N_letters | eden;hits;lane;life;rent;rome;water |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_eyes` | `2ES 16:77` | `field` | `-143` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | tomb |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_gate` | `MAL 4:6` | `children` | `-85` | cross_skip_pair_within_N_letters | heart;heth;holy;lane;leah;love;noah;ruth;torah |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_gate` | `MAT 1:2` | `his` | `-168` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | torah |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_hail` | `2ES 16:78` | `be` | `185` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | soot;thin |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_hand` | `MAL 4:6` | `their` | `40` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | seed |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_hand` | `MAL 4:6` | `lest` | `205` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | lane |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_hannah` | `MAT 1:6` | `Jesse` | `176` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | obal |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_hannah` | `MAT 1:6` | `Jesse` | `-176` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | obal |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_hits` | `MAL 4:6` | `heart` | `-85` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | lane;soot;torah |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_hits` | `MAL 4:6` | `fathers` | `-141` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | soot;wine |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_house;eng_house_2` | `TOB 1:3` | `justice,` | `196` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | hits |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_isaac;eng_isaac_2` | `MAT 1:2` | `Judas` | `86` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | tomb |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_king;eng_king_2` | `MAL 4:5` | `the` | `-192` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | hail;yhwh |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_lane` | `MAL 4:6` | `children,` | `106` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | hand;leah;rent;wine |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_lane` | `MAL 4:6` | `fathers,` | `192` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | seed;soot |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_lane` | `MAL 4:6` | `heart` | `226` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | hits;soot;torah |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_lane` | `MAL 4:6` | `and` | `-232` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | eden;seed |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_lane` | `MAT 1:2` | `Isaac` | `-124` | cross_skip_pair_at_word;cross_skip_pair_within_N_letters | horn |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_light;eng_light_2` | `TOB 1:2` | `Galilee` | `-127` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | tyre |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_lion` | `2ES 16:77` | `may` | `226` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | fire |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_love;eng_love_2;eng_love_3` | `TOB 1:2` | `of` | `222` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | holy |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_obal` | `MAT 1:3` | `begat` | `-210` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | seed |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_rome` | `TOB 1:2` | `Nephthali` | `184` | cross_skip_pair_within_N_letters | altar;eber;eden;lane;rent;tyre |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_rome` | `TOB 1:2` | `properly` | `250` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | eden;seed |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_seed;eng_seed_2;eng_seed_3` | `TOB 1:1` | `the` | `54` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | ahab;fire;gate;life;rent;tyre |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_seed;eng_seed_2;eng_seed_3` | `TOB 1:1` | `tribe` | `67` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | hits |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_seed;eng_seed_2;eng_seed_3` | `TOB 1:1` | `son` | `-73` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | ahab;hand |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_seed;eng_seed_2;eng_seed_3` | `TOB 1:1` | `Tobiel,` | `-102` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | sidon |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_seed;eng_seed_2;eng_seed_3` | `TOB 1:1` | `of` | `-178` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | hits;nato;sign;soot |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_seed;eng_seed_2;eng_seed_3` | `TOB 1:2` | `captive` | `125` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | hits |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_seed;eng_seed_2;eng_seed_3` | `TOB 1:2` | `properly` | `-238` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | eden;rome |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_soot` | `MAL 4:6` | `fathers,` | `-123` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | lane;seed |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_soot` | `MAL 4:6` | `fathers` | `124` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | hits;wine |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_soot` | `MAL 4:6` | `heart` | `240` | cross_skip_pair_at_word;cross_skip_pair_within_N_letters | hits;lane;torah |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_star` | `2ES 16:77` | `man` | `-84` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | heth;hits |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_tomb;eng_tomb_2;eng_tomb_3` | `2ES 16:77` | `field` | `134` | cross_skip_pair_at_word;cross_skip_pair_within_N_letters | eyes |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_tyre` | `TOB 1:2` | `Galilee` | `198` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | light |
| `apocrypha_bridge_context` | `LXX` | `adam_g` | `TOB 1:1` | `Νεφθαλίμ,` | `195` | cross_skip_pair_within_N_letters | αιμα;ναοσ;σιων |
| `apocrypha_bridge_context` | `LXX` | `adam_g` | `TOB 1:2` | `Τωβὶτ` | `-195` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | ελαμ;μαρια |
| `apocrypha_bridge_context` | `LXX` | `blood_g;haima_gnt` | `TOB 1:1` | `τοῦ` | `-223` | cross_skip_pair_within_N_letters | αδαμ;αμην |
| `apocrypha_bridge_context` | `LXX` | `blood_g;haima_gnt` | `TOB 1:2` | `ὁδοῖς` | `-210` | cross_skip_pair_at_word;cross_skip_pair_at_letter | βασαν |
| `apocrypha_bridge_context` | `LXX` | `blood_g;haima_gnt` | `TOB 1:2` | `ᾐχμαλωτεύθη` | `-238` | cross_skip_pair_within_N_letters | σιων |
| `apocrypha_bridge_context` | `LXX` | `blood_g;haima_gnt` | `TOB 1:2` | `ἀληθείας` | `-246` | cross_skip_pair_within_N_letters | αμην;αμμων |
| `apocrypha_bridge_context` | `LXX` | `blood_g;haima_gnt` | `TOB 1:3` | `τοῖς` | `224` | cross_skip_pair_within_N_letters | σιων |
| `apocrypha_bridge_context` | `LXX` | `blood_g;haima_gnt` | `TOB 1:3` | `τοῖς` | `226` | cross_skip_pair_within_N_letters | βασαν |
| `apocrypha_bridge_context` | `LXX` | `amen_g` | `TOB 1:1` | `Τωβιήλ,` | `247` | cross_skip_pair_at_word;cross_skip_pair_within_N_letters | ρωμη |
| `apocrypha_bridge_context` | `LXX` | `amen_g` | `TOB 1:2` | `ὑπεράνω` | `-231` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | αμμων;ελαμ |
| `apocrypha_bridge_context` | `LXX` | `bashan_g` | `TOB 1:2` | `ὁδοῖς` | `-222` | cross_skip_pair_at_word;cross_skip_pair_within_N_letters | αιμα |
| `apocrypha_bridge_context` | `LXX` | `elam_g` | `MAL 4:6` | `δικαιώματα.` | `-209` | cross_skip_pair_at_word | αμην;σιων |
| `apocrypha_bridge_context` | `LXX` | `elam_g` | `TOB 1:2` | `βασιλέως` | `120` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | σιων |
| `apocrypha_bridge_context` | `LXX` | `elam_g` | `TOB 1:2` | `Ἐνεμεσσάρου` | `-136` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | αδαμ;μαρια |
| `apocrypha_bridge_context` | `LXX` | `god_g` | `MAL 4:4` | `ἐπιφανῆ,` | `223` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | σιων |
| `apocrypha_bridge_context` | `LXX` | `god_g` | `TOB 1:1` | `Τωβίτ,` | `-204` | cross_skip_pair_within_N_letters | αμην;ελαμ |
| `apocrypha_bridge_context` | `LXX` | `temple_g` | `TOB 1:2` | `Θίσβης,` | `242` | cross_skip_pair_within_N_letters | αδαμ |
| `apocrypha_bridge_context` | `LXX` | `rome_g` | `TOB 1:1` | `Τωβιήλ,` | `-221` | cross_skip_pair_at_word;cross_skip_pair_within_N_letters | αμην |
| `apocrypha_bridge_context` | `LXX` | `zion_g` | `MAL 4:5` | `πρὸς` | `187` | cross_skip_pair_within_N_letters | θεοσ |
| `apocrypha_bridge_context` | `LXX` | `zion_g` | `MAL 4:5` | `υἱὸν` | `-198` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | θεοσ |
| `apocrypha_bridge_context` | `LXX` | `zion_g` | `TOB 1:1` | `Γαβαήλ,` | `-204` | cross_skip_pair_within_N_letters | αιμα;ρωμη |
| `apocrypha_bridge_context` | `LXX` | `zion_g` | `TOB 1:2` | `ἐπορευόμην` | `-176` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | αιμα |
| `apocrypha_bridge_context` | `LXX` | `zion_g` | `TOB 1:2` | `βασιλέως` | `-218` | cross_skip_pair_at_word;cross_skip_pair_within_N_letters | ελαμ |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_aaron;eng_aaron_2` | `2ES 16:78` | `undressed,` | `-243` | cross_skip_pair_at_word;cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | obed |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_aaron;eng_aaron_2` | `MAT 1:3` | `Esrom` | `-184` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | adam;horn |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_adam` | `MAT 1:3` | `Aram;` | `230` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | hail |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_adam` | `MAT 1:4` | `Naasson;` | `-210` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | aaron;aram |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_ahab` | `2ES 16:78` | `consumed` | `192` | cross_skip_pair_at_letter;cross_skip_pair_within_N_letters | horn;obal |
| ... | ... | ... | ... | ... | ... | ... | 151 more rows in CSV |

## Read

- Cross-skip rows are useful for pair review and audit packets.
- They are not stronger by default; paired controls define whether
  a cross-skip relationship is unusual.
- Claim-grade use needs the pair metric and correction family locked
  before looking at candidate rows.
