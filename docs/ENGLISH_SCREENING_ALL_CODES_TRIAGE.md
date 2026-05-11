# English KJV Screening All-Codes Triage

This is a compact review queue built from the relaxed all-codes export.
It ranks same center-word rows first, then related center-word rows,
center-verse rows, span rows, and finally hidden-path-only rows.

It is a triage aid, not a claim-grade filter.

## Inputs

- Hits: `reports/english_screening_all_codes/surface_all_codes.csv`
- Summary: `reports/english_screening_all_codes/surface_all_codes_summary.csv`
- Report DB: `reports/db/open_bible_codes.duckdb`
- Queue CSV: `reports/english_screening_all_codes/triage_queue.csv`
- Corpora: `KJV`

## Counts

| Metric | Count |
| --- | ---: |
| Raw rows scanned | 1,374,596 |
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
| 1 | all_source | `eng_baal` `baal` | Baal | 2 | 7 | 2Kgs 10:19 | `baal` |  |
| 2 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Acts 25:20 | `whether` |  |
| 3 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Deut 24:14 | `whether` |  |
| 4 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Eccl 2:19 | `whether` |  |
| 5 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Eccl 5:12 | `whether` |  |
| 6 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Eph 6:8 | `whether` |  |
| 7 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Exod 12:19 | `whether` |  |
| 8 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Exod 21:31 | `whether` |  |
| 9 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Exod 22:8 | `whether` |  |
| 10 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | John 9:25 | `whether` |  |
| 11 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Lev 15:3 | `whether` |  |
| 12 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Lev 5:1 | `whether` |  |
| 13 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Luke 14:28 | `whether` |  |
| 14 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Luke 14:31 | `whether` |  |
| 15 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Luke 3:15 | `whether` |  |
| 16 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Luke 6:7 | `whether` |  |
| 17 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Mark 15:44 | `whether` |  |
| 18 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Mark 3:2 | `whether` |  |
| 19 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Num 15:30 | `whether` |  |
| 20 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Prov 20:11 | `whether` |  |

### center_word_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `eng_obed` `obed` | Obed | 2 | 7 | 1Chr 16:3 | `bread` |  |
| 2 | all_source | `eng_obed_2` `obed` | Obed | 2 | 7 | 1Chr 16:3 | `bread` |  |
| 3 | all_source | `eng_edom` `edom` | Edom | -2 | 7 | 1Chr 19:1 | `ammon` |  |
| 4 | all_source | `eng_shem` `shem` | Shem | -2 | 7 | 1Chr 4:26 | `hamuel` |  |
| 5 | all_source | `eng_seba_2` `seba` | Seba | -2 | 7 | 1Chr 4:28 | `beersheba` |  |
| 6 | all_source | `eng_obed` `obed` | Obed | 2 | 7 | 1Cor 11:23 | `bread` |  |
| 7 | all_source | `eng_obed_2` `obed` | Obed | 2 | 7 | 1Cor 11:23 | `bread` |  |
| 8 | all_source | `eng_obed` `obed` | Obed | 2 | 7 | 1Kgs 17:11 | `bread` |  |
| 9 | all_source | `eng_obed_2` `obed` | Obed | 2 | 7 | 1Kgs 17:11 | `bread` |  |
| 10 | all_source | `eng_noah_2` `noah` | Noah | 2 | 7 | 1Kgs 1:11 | `bathsheba` |  |
| 11 | all_source | `eng_obed` `obed` | Obed | 2 | 7 | 1Sam 10:3 | `bread` |  |
| 12 | all_source | `eng_obed_2` `obed` | Obed | 2 | 7 | 1Sam 10:3 | `bread` |  |
| 13 | all_source | `eng_obed` `obed` | Obed | 2 | 7 | 1Sam 10:4 | `bread` |  |
| 14 | all_source | `eng_obed_2` `obed` | Obed | 2 | 7 | 1Sam 10:4 | `bread` |  |
| 15 | all_source | `eng_obed` `obed` | Obed | 2 | 7 | 1Sam 21:3 | `bread` |  |
| 16 | all_source | `eng_obed_2` `obed` | Obed | 2 | 7 | 1Sam 21:3 | `bread` |  |
| 17 | all_source | `eng_obed` `obed` | Obed | 2 | 7 | 1Sam 21:4 | `bread` |  |
| 18 | all_source | `eng_obed_2` `obed` | Obed | 2 | 7 | 1Sam 21:4 | `bread` |  |
| 19 | all_source | `eng_obed` `obed` | Obed | 2 | 7 | 1Sam 21:6 | `bread` |  |
| 20 | all_source | `eng_obed_2` `obed` | Obed | 2 | 7 | 1Sam 21:6 | `bread` |  |

### center_verse_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `eng_hand` `hand` | Hand | -2 | 7 | 1Chr 2:2 | `and` |  |
| 2 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | 1Cor 10:20 | `ye` |  |
| 3 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | 1Cor 5:2 | `he` |  |
| 4 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | 1Cor 9:10 | `he` |  |
| 5 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | 1John 2:11 | `whither` |  |
| 6 | all_source | `eng_heal` `heal` | Heal | -2 | 7 | 1Kgs 1:6 | `displeased` |  |
| 7 | all_source | `eng_hand` `hand` | Hand | -2 | 7 | 1Kgs 3:6 | `according` |  |
| 8 | all_source | `eng_seal` `seal` | Seal | 2 | 7 | 1Kgs 6:22 | `finished` |  |
| 9 | all_source | `eng_seal_2` `seal` | Seal | 2 | 7 | 1Kgs 6:22 | `finished` |  |
| 10 | all_source | `eng_seal_3` `seal` | Seal | 2 | 7 | 1Kgs 6:22 | `finished` |  |
| 11 | all_source | `eng_seal_4` `seal` | Seal | 2 | 7 | 1Kgs 6:22 | `finished` |  |
| 12 | all_source | `eng_seal_5` `seal` | Seal | 2 | 7 | 1Kgs 6:22 | `finished` |  |
| 13 | all_source | `eng_lord` `lord` | Lord | 2 | 7 | 1Sam 10:19 | `your` |  |
| 14 | all_source | `eng_lord_2` `lord` | Lord | 2 | 7 | 1Sam 10:19 | `your` |  |
| 15 | all_source | `eng_saul` `saul` | Saul | 2 | 7 | 1Sam 15:35 | `samuel` |  |
| 16 | all_source | `eng_saul` `saul` | Saul | 2 | 7 | 1Sam 28:14 | `samuel` |  |
| 17 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | 2Chr 23:4 | `ye` |  |
| 18 | all_source | `eng_rent` `rent` | Rent | -2 | 7 | 2Chr 29:34 | `heart` |  |
| 19 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | 2Kgs 11:5 | `ye` |  |
| 20 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | 2Kgs 6:14 | `thither` |  |

### center_verse_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `eng_sign_2` `sign` | Sign | -2 | 7 | 1Chr 10:13 | `against` |  |
| 2 | all_source | `eng_adar` `adar` | Adar | -2 | 7 | 1Chr 11:19 | `and` |  |
| 3 | all_source | `eng_adam` `adam` | Adam | -2 | 7 | 1Chr 12:31 | `and` |  |
| 4 | all_source | `eng_tree_2` `tree` | Tree | -2 | 7 | 1Chr 12:38 | `heart` |  |
| 5 | all_source | `eng_adar` `adar` | Adar | -2 | 7 | 1Chr 13:8 | `and` |  |
| 6 | all_source | `eng_soul_2` `soul` | Soul | 2 | 7 | 1Chr 14:1 | `build` |  |
| 7 | all_source | `eng_adar` `adar` | Adar | -2 | 7 | 1Chr 15:16 | `and` |  |
| 8 | all_source | `eng_adam` `adam` | Adam | -2 | 7 | 1Chr 15:27 | `and` |  |
| 9 | all_source | `eng_otho` `otho` | Otho | -2 | 7 | 1Chr 17:1 | `prophet` |  |
| 10 | all_source | `eng_adam` `adam` | Adam | -2 | 7 | 1Chr 17:16 | `and` |  |
| 11 | all_source | `eng_adar` `adar` | Adar | -2 | 7 | 1Chr 17:16 | `and` |  |
| 12 | all_source | `eng_adam` `adam` | Adam | -2 | 7 | 1Chr 19:2 | `and` |  |
| 13 | all_source | `eng_adar` `adar` | Adar | 2 | 7 | 1Chr 19:5 | `tarry` |  |
| 14 | all_source | `eng_tree_2` `tree` | Tree | -2 | 7 | 1Chr 1:43 | `are` |  |
| 15 | all_source | `eng_adam` `adam` | Adam | -2 | 7 | 1Chr 20:1 | `and` |  |
| 16 | all_source | `eng_tree_2` `tree` | Tree | 2 | 7 | 1Chr 21:12 | `three` |  |
| 17 | all_source | `eng_adam` `adam` | Adam | -2 | 7 | 1Chr 21:13 | `and` |  |
| 18 | all_source | `eng_hand` `hand` | Hand | -2 | 7 | 1Chr 21:5 | `and` |  |
| 19 | all_source | `eng_hand` `hand` | Hand | -2 | 7 | 1Chr 22:14 | `and` |  |
| 20 | all_source | `eng_soul_2` `soul` | Soul | 2 | 7 | 1Chr 22:2 | `build` |  |

### span_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `eng_thin` `thin` | Thin | -2 | 7 | 1John 2:5 | `him` |  |
| 2 | all_source | `eng_rent` `rent` | Rent | -2 | 7 | Gen 31:55 | `and` |  |
| 3 | all_source | `eng_wine` `wine` | Wine | -2 | 7 | Isa 22:14 | `and` |  |
| 4 | all_source | `eng_wine_2` `wine` | Wine | -2 | 7 | Isa 22:14 | `and` |  |
| 5 | all_source | `eng_wine_3` `wine` | Wine | -2 | 7 | Isa 22:14 | `and` |  |
| 6 | all_source | `eng_tree` `tree` | Tree | -2 | 7 | Luke 13:25 | `are` |  |
| 7 | all_source | `eng_tree_2` `tree` | Tree | -2 | 7 | Luke 13:25 | `are` |  |
| 8 | all_source | `eng_heth` `heth` | Heth | -2 | 7 | Matt 13:21 | `yet` |  |
| 9 | all_source | `eng_hand` `hand` | Hand | -3 | 10 | 1Chr 8:23 | `hanan` |  |
| 10 | all_source | `eng_lord` `lord` | Lord | -3 | 10 | 1Sam 30:24 | `who` |  |
| 11 | all_source | `eng_lord_2` `lord` | Lord | -3 | 10 | 1Sam 30:24 | `who` |  |
| 12 | all_source | `eng_ruth` `ruth` | Ruth | -3 | 10 | 2Tim 2:16 | `shun` |  |
| 13 | all_source | `eng_isis` `isis` | ISIS | -3 | 10 | Josh 15:19 | `springs` |  |
| 14 | all_source | `eng_hand` `hand` | Hand | -3 | 10 | Prov 6:12 | `a` |  |
| 15 | all_source | `eng_rent` `rent` | Rent | -4 | 13 | 1Chr 25:1 | `moreover` |  |
| 16 | all_source | `eng_thin` `thin` | Thin | -4 | 13 | 1John 2:25 | `life` |  |
| 17 | all_source | `eng_thin` `thin` | Thin | -4 | 13 | 1John 5:12 | `life` |  |
| 18 | all_source | `eng_heal` `heal` | Heal | -4 | 13 | 2Chr 15:9 | `and` |  |
| 19 | all_source | `eng_fire` `fire` | Fire | 4 | 13 | Ezek 22:22 | `silver` |  |
| 20 | all_source | `eng_hand` `hand` | Hand | 4 | 13 | Gal 6:12 | `many` |  |

### span_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `eng_adar` `adar` | Adar | -2 | 7 | 1Sam 15:14 | `and` |  |
| 2 | all_source | `eng_mash` `mash` | Mash | -2 | 7 | 1Sam 28:18 | `day` |  |
| 3 | all_source | `eng_adar` `adar` | Adar | -2 | 7 | 1Sam 2:1 | `and` |  |
| 4 | all_source | `eng_adar` `adar` | Adar | -2 | 7 | 1Sam 30:2 | `and` |  |
| 5 | all_source | `eng_adam` `adam` | Adam | -2 | 7 | 1Sam 9:22 | `and` |  |
| 6 | all_source | `eng_nero_2` `nero` | Nero | 2 | 7 | 2Sam 15:36 | `hear` |  |
| 7 | all_source | `eng_moab` `moab` | Moab | -2 | 7 | 2Sam 16:23 | `absalom` |  |
| 8 | all_source | `eng_seed_3` `seed` | Seed | 2 | 7 | Deut 16:15 | `seven` |  |
| 9 | all_source | `eng_seba_2` `seba` | Seba | -2 | 7 | Deut 33:11 | `bless` |  |
| 10 | all_source | `eng_adam` `adam` | Adam | -2 | 7 | Eph 1:22 | `and` |  |
| 11 | all_source | `eng_adam` `adam` | Adam | -2 | 7 | Gen 22:16 | `and` |  |
| 12 | all_source | `eng_aids_3` `aids` | AIDS | -2 | 7 | Gen 26:12 | `him` |  |
| 13 | all_source | `eng_adam` `adam` | Adam | -2 | 7 | Gen 30:34 | `and` |  |
| 14 | all_source | `eng_adar` `adar` | Adar | -2 | 7 | Gen 31:28 | `and` |  |
| 15 | all_source | `eng_hand` `hand` | Hand | -2 | 7 | Gen 32:31 | `and` |  |
| 16 | all_source | `eng_rent` `rent` | Rent | 2 | 7 | Gen 46:16 | `and` |  |
| 17 | all_source | `eng_fire` `fire` | Fire | -2 | 7 | Heb 4:2 | `heard` |  |
| 18 | all_source | `eng_tree` `tree` | Tree | -2 | 7 | Jer 31:4 | `merry` |  |
| 19 | all_source | `eng_bear` `bear` | Bear | 2 | 7 | Jer 50:37 | `robbed` |  |
| 20 | all_source | `eng_shem` `shem` | Shem | -2 | 7 | Job 19:11 | `enemies` |  |

### hidden_path_only

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `eng_heal` `heal` | Heal | -2 | 7 | 1Chr 10:11 | `jabeshgilead` |  |
| 2 | all_source | `eng_sign` `sign` | Sign | -2 | 7 | 1Chr 10:13 | `against` |  |
| 3 | all_source | `eng_cush` `cush` | Cush | -2 | 7 | 1Chr 10:4 | `these` |  |
| 4 | all_source | `eng_heth` `heth` | Heth | 2 | 7 | 1Chr 10:4 | `lest` |  |
| 5 | all_source | `eng_shot` `shot` | Shot | -2 | 7 | 1Chr 10:9 | `took` |  |
| 6 | all_source | `eng_tree` `tree` | Tree | 2 | 7 | 1Chr 11:21 | `three` |  |
| 7 | all_source | `eng_tree` `tree` | Tree | 2 | 7 | 1Chr 11:21 | `three` |  |
| 8 | all_source | `eng_tree_2` `tree` | Tree | 2 | 7 | 1Chr 11:21 | `three` |  |
| 9 | all_source | `eng_tree_2` `tree` | Tree | 2 | 7 | 1Chr 11:21 | `three` |  |
| 10 | all_source | `eng_tree` `tree` | Tree | -2 | 7 | 1Chr 11:37 | `hezro` |  |
| 11 | all_source | `eng_tree_2` `tree` | Tree | -2 | 7 | 1Chr 11:37 | `hezro` |  |
| 12 | all_source | `eng_bear` `bear` | Bear | 2 | 7 | 1Chr 11:8 | `repaired` |  |
| 13 | all_source | `eng_tree` `tree` | Tree | -2 | 7 | 1Chr 12:1 | `are` |  |
| 14 | all_source | `eng_tree_2` `tree` | Tree | -2 | 7 | 1Chr 12:1 | `are` |  |
| 15 | all_source | `eng_tree` `tree` | Tree | -2 | 7 | 1Chr 12:15 | `are` |  |
| 16 | all_source | `eng_tree_2` `tree` | Tree | -2 | 7 | 1Chr 12:15 | `are` |  |
| 17 | all_source | `eng_tree` `tree` | Tree | -2 | 7 | 1Chr 12:23 | `are` |  |
| 18 | all_source | `eng_tree_2` `tree` | Tree | -2 | 7 | 1Chr 12:23 | `are` |  |
| 19 | all_source | `eng_noah` `noah` | Noah | 2 | 7 | 1Chr 12:36 | `of` |  |
| 20 | all_source | `eng_noah_2` `noah` | Noah | 2 | 7 | 1Chr 12:36 | `of` |  |

## Read

Rows at the top are good manual-review candidates because their hidden ELS
path center is located on, or near, surface language from the same declared
term set. The `presence_scope` column reports whether the selected exact
ref-key pattern appears in every configured source, multiple sources, or
only one source among the selected candidate keys.
