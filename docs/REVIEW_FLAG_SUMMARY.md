# Review Flag Summary

Status: post-search review aid, not claim promotion.

This report unpivots meaningful-skip, gematria-skip, bigram-surprise,
and letter-frequency anomaly flags from the match-strata index. It does
not run a new ELS search.

## Settings

- Strata input: `reports/match_strata_index/occurrence_strata.csv`
- Input rows: `923`
- Flag rows: `59`

## Overall Counts

| Flag type | Rows |
| --- | ---: |
| `skip_equals_meaningful_constant` | 10 |
| `skip_equals_term_gematria` | 0 |
| `skip_equals_center_word_gematria` | 0 |
| `bigram_surprise` | 49 |
| `letter_frequency_anomaly` | 0 |

## Source / Corpus Summary

| Source family | Corpus class | Corpus | Flag type | Rows | Distinct terms | Share |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `all_codes_followup` | `bible` | `` | `skip_equals_meaningful_constant` | 5 | 4 | 0.067568 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `bigram_surprise` | 1 | 1 | 0.034483 |
| `gog_source_review` | `bible` | `SBLGNT` | `skip_equals_meaningful_constant` | 1 | 1 | 1.000000 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `bigram_surprise` | 48 | 16 | 0.236453 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `skip_equals_meaningful_constant` | 4 | 4 | 0.019704 |

## Flag Rows

| Source family | Corpus | Term | Center ref | Center word | Skip | Flag type | Value | Evidence |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| `gog_source_review` | `SBLGNT` | `dyn_gog_g` | `Rev 20:8=4` | `Gog` | `-7;7;-4423;4423` | `skip_equals_meaningful_constant` | 7 | Sabbath / completeness |
| `all_codes_followup` | `` | `isa53_servant_g` | `Luke 22:64` | `παίσας` | `-7` | `skip_equals_meaningful_constant` | 7 | Sabbath / completeness |
| `all_codes_followup` | `` | `htp_torah_h` | `1Chr 5:1` | `בֶּן־יִשְׂרָאֵ֑ל` | `7` | `skip_equals_meaningful_constant` | 7 | Sabbath / completeness |
| `all_codes_followup` | `` | `htp_torah_h` | `2Kgs 17:20` | `יִשְׂרָאֵל֙` | `-7` | `skip_equals_meaningful_constant` | 7 | Sabbath / completeness |
| `apocrypha_bridge_context` | `LXX` | `mary_g;maria_gnt` | `MAL 4:6` | `Ἰσραὴλ` | `29` | `bigram_surprise` | low_bigram_surprise | μα:16196;αρ:17084;ρι:20410;ια:32513 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_eden` | `MAL 4:4` | `judgments.` | `233` | `bigram_surprise` | low_bigram_surprise | ed:33489;de:17773;en:40399 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_hand` | `MAL 4:6` | `their` | `40` | `skip_equals_meaningful_constant` | 40 | Wilderness / testing |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_hand` | `MAL 4:6` | `their` | `40` | `bigram_surprise` | low_bigram_surprise | ha:58723;an:90242;nd:76718 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_hand` | `MAL 4:6` | `lest` | `205` | `bigram_surprise` | low_bigram_surprise | ha:58723;an:90242;nd:76718 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_hand` | `MAT 1:5` | `begat` | `-243` | `bigram_surprise` | low_bigram_surprise | ha:58723;an:90242;nd:76718 |
| `all_codes_followup` | `` | `am_5708_full_h` | `Lev 22:27` | `וָהָ֔לְאָה` | `40` | `skip_equals_meaningful_constant` | 40 | Wilderness / testing |
| `all_codes_followup` | `` | `nato_g` | `1Cor 1:27` | `μωρὰ` | `7` | `skip_equals_meaningful_constant` | 7 | Sabbath / completeness |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_bear` | `MAT 1:3` | `and` | `-180` | `bigram_surprise` | low_bigram_surprise | be:22507;ea:43577;ar:25373 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_death;eng_death_2` | `TOB 1:2` | `Assyrians` | `228` | `bigram_surprise` | low_bigram_surprise | de:17773;ea:43577;at:39393;th:195529 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_dedan` | `MAL 4:6` | `And` | `-170` | `bigram_surprise` | low_bigram_surprise | de:17773;ed:33489;da:24821;an:90242 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_earth` | `2ES 16:75` | `afraid` | `191` | `bigram_surprise` | low_bigram_surprise | ea:43577;ar:25373;rt:18883;th:195529 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_eden` | `MAL 4:5` | `you` | `-230` | `bigram_surprise` | low_bigram_surprise | ed:33489;de:17773;en:40399 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_eden` | `MAL 4:6` | `and` | `140` | `bigram_surprise` | low_bigram_surprise | ed:33489;de:17773;en:40399 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_eden` | `TOB 1:1` | `The` | `239` | `bigram_surprise` | low_bigram_surprise | ed:33489;de:17773;en:40399 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_eden` | `TOB 1:2` | `properly` | `-197` | `bigram_surprise` | low_bigram_surprise | ed:33489;de:17773;en:40399 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_gate` | `MAL 4:5` | `great` | `-144` | `skip_equals_meaningful_constant` | 144 | Revelation square of twelve |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_hand` | `2ES 16:77` | `their` | `-188` | `bigram_surprise` | low_bigram_surprise | ha:58723;an:90242;nd:76718 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_hand` | `MAL 4:5` | `Behold,` | `-141` | `bigram_surprise` | low_bigram_surprise | ha:58723;an:90242;nd:76718 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_hand` | `TOB 1:1` | `son` | `-206` | `bigram_surprise` | low_bigram_surprise | ha:58723;an:90242;nd:76718 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_heal` | `MAL 4:4` | `law` | `214` | `bigram_surprise` | low_bigram_surprise | he:153400;ea:43577;al:32047 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_heart;eng_heart_2` | `MAL 4:4` | `commanded` | `-178` | `bigram_surprise` | low_bigram_surprise | he:153400;ea:43577;ar:25373;rt:18883 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_heart;eng_heart_2` | `MAL 4:5` | `great` | `-130` | `bigram_surprise` | low_bigram_surprise | he:153400;ea:43577;ar:25373;rt:18883 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_heart;eng_heart_2` | `MAL 4:5` | `Elijah` | `194` | `bigram_surprise` | low_bigram_surprise | he:153400;ea:43577;ar:25373;rt:18883 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_heart;eng_heart_2` | `TOB 1:2` | `Assyrians` | `-165` | `bigram_surprise` | low_bigram_surprise | he:153400;ea:43577;ar:25373;rt:18883 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_heth` | `MAL 4:4` | `judgments.` | `163` | `bigram_surprise` | low_bigram_surprise | he:153400;et:40713;th:195529 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_heth` | `MAL 4:4` | `which` | `179` | `bigram_surprise` | low_bigram_surprise | he:153400;et:40713;th:195529 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_heth` | `MAL 4:4` | `servant,` | `-224` | `bigram_surprise` | low_bigram_surprise | he:153400;et:40713;th:195529 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_heth` | `MAL 4:5` | `will` | `244` | `bigram_surprise` | low_bigram_surprise | he:153400;et:40713;th:195529 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_heth` | `MAT 1:1` | `son` | `-172` | `bigram_surprise` | low_bigram_surprise | he:153400;et:40713;th:195529 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_heth` | `MAT 1:2` | `Jacob;` | `-177` | `bigram_surprise` | low_bigram_surprise | he:153400;et:40713;th:195529 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_heth` | `MAT 1:5` | `Booz` | `187` | `bigram_surprise` | low_bigram_surprise | he:153400;et:40713;th:195529 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_heth` | `TOB 1:3` | `nation,` | `249` | `bigram_surprise` | low_bigram_surprise | he:153400;et:40713;th:195529 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_hits` | `MAL 4:5` | `before` | `144` | `skip_equals_meaningful_constant` | 144 | Revelation square of twelve |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_mash` | `2ES 16:77` | `like` | `213` | `bigram_surprise` | low_bigram_surprise | ma:20579;as:23084;sh:27021 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_mash` | `MAT 1:2` | `begat` | `-90` | `bigram_surprise` | low_bigram_surprise | ma:20579;as:23084;sh:27021 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_otho;eng_otho_2` | `2ES 16:76` | `weigh` | `-206` | `bigram_surprise` | low_bigram_surprise | ot:25564;th:195529;ho:25372 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_otho;eng_otho_2` | `2ES 16:77` | `unto` | `-245` | `bigram_surprise` | low_bigram_surprise | ot:25564;th:195529;ho:25372 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_rent` | `TOB 1:1` | `the` | `73` | `bigram_surprise` | low_bigram_surprise | re:50330;en:40399;nt:46361 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_rent` | `TOB 1:2` | `which` | `165` | `bigram_surprise` | low_bigram_surprise | re:50330;en:40399;nt:46361 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_rent` | `TOB 1:2` | `right` | `228` | `bigram_surprise` | low_bigram_surprise | re:50330;en:40399;nt:46361 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_resen` | `2ES 16:76` | `iniquities` | `193` | `bigram_surprise` | low_bigram_surprise | re:50330;es:47860;se:28717;en:40399 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_shem` | `MAL 4:4` | `Israel,` | `-215` | `bigram_surprise` | low_bigram_surprise | sh:27021;he:153400;em:21585 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_soot` | `TOB 1:1` | `of` | `-70` | `skip_equals_meaningful_constant` | 70 | Nations / exile years |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_thin` | `2ES 16:77` | `travel` | `-118` | `bigram_surprise` | low_bigram_surprise | th:195529;hi:41738;in:55949 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_thin` | `2ES 16:77` | `travel` | `-141` | `bigram_surprise` | low_bigram_surprise | th:195529;hi:41738;in:55949 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_thin` | `2ES 16:78` | `be` | `188` | `bigram_surprise` | low_bigram_surprise | th:195529;hi:41738;in:55949 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_thin` | `MAL 4:5` | `prophet` | `-132` | `bigram_surprise` | low_bigram_surprise | th:195529;hi:41738;in:55949 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_thin` | `MAT 1:5` | `Salmon` | `198` | `bigram_surprise` | low_bigram_surprise | th:195529;hi:41738;in:55949 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_thin` | `TOB 1:1` | `Nephthali;` | `-245` | `bigram_surprise` | low_bigram_surprise | th:195529;hi:41738;in:55949 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_thin` | `TOB 1:2` | `king` | `148` | `bigram_surprise` | low_bigram_surprise | th:195529;hi:41738;in:55949 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_wine;eng_wine_2;eng_wine_3` | `MAL 4:5` | `coming` | `163` | `bigram_surprise` | low_bigram_surprise | wi:17895;in:55949;ne:20523 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_wine;eng_wine_2;eng_wine_3` | `MAL 4:6` | `fathers` | `131` | `bigram_surprise` | low_bigram_surprise | wi:17895;in:55949;ne:20523 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_wine;eng_wine_2;eng_wine_3` | `MAT 1:2` | `and` | `168` | `bigram_surprise` | low_bigram_surprise | wi:17895;in:55949;ne:20523 |
| `kjv_apocrypha_bridge_context` | `KJVA` | `eng_wine;eng_wine_2;eng_wine_3` | `TOB 1:3` | `have` | `185` | `bigram_surprise` | low_bigram_surprise | wi:17895;in:55949;ne:20523 |

## Read

- These flags help prioritize review; they do not change hit counts.
- Meaningful constants and gematria schemes must be locked before
  claim-grade use.
- Bigram and letter-frequency flags are corpus-local metadata; controls
  still decide whether a flagged row is unusual.
