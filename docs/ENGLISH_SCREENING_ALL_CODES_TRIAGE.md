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
| Raw rows scanned | 666,378 |
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
| 1 | all_source | `eng_heth` | Heth | -2 | 7 | Acts 25:20 | `whether` |  |
| 2 | all_source | `eng_heth` | Heth | -2 | 7 | Deut 24:14 | `whether` |  |
| 3 | all_source | `eng_heth` | Heth | -2 | 7 | Eccl 2:19 | `whether` |  |
| 4 | all_source | `eng_heth` | Heth | -2 | 7 | Eccl 5:12 | `whether` |  |
| 5 | all_source | `eng_heth` | Heth | -2 | 7 | Eph 6:8 | `whether` |  |
| 6 | all_source | `eng_heth` | Heth | -2 | 7 | Exod 12:19 | `whether` |  |
| 7 | all_source | `eng_heth` | Heth | -2 | 7 | Exod 21:31 | `whether` |  |
| 8 | all_source | `eng_heth` | Heth | -2 | 7 | Exod 22:8 | `whether` |  |
| 9 | all_source | `eng_heth` | Heth | -2 | 7 | John 9:25 | `whether` |  |
| 10 | all_source | `eng_heth` | Heth | -2 | 7 | Lev 15:3 | `whether` |  |
| 11 | all_source | `eng_heth` | Heth | -2 | 7 | Lev 5:1 | `whether` |  |
| 12 | all_source | `eng_heth` | Heth | -2 | 7 | Luke 14:28 | `whether` |  |
| 13 | all_source | `eng_heth` | Heth | -2 | 7 | Luke 14:31 | `whether` |  |
| 14 | all_source | `eng_heth` | Heth | -2 | 7 | Luke 3:15 | `whether` |  |
| 15 | all_source | `eng_heth` | Heth | -2 | 7 | Luke 6:7 | `whether` |  |
| 16 | all_source | `eng_heth` | Heth | -2 | 7 | Mark 15:44 | `whether` |  |
| 17 | all_source | `eng_heth` | Heth | -2 | 7 | Mark 3:2 | `whether` |  |
| 18 | all_source | `eng_heth` | Heth | -2 | 7 | Num 15:30 | `whether` |  |
| 19 | all_source | `eng_heth` | Heth | -2 | 7 | Prov 20:11 | `whether` |  |
| 20 | all_source | `eng_heth` | Heth | -2 | 7 | Prov 29:9 | `whether` |  |

### center_word_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `eng_edom` | Edom | -2 | 7 | 1Chr 19:1 | `ammon` |  |
| 2 | all_source | `eng_shem` | Shem | -2 | 7 | 1Chr 4:26 | `hamuel` |  |
| 3 | all_source | `eng_seba` | Seba | -2 | 7 | 1Chr 4:28 | `beersheba` |  |
| 4 | all_source | `eng_noah` | Noah | 2 | 7 | 1Kgs 1:11 | `bathsheba` |  |
| 5 | all_source | `eng_heth` | Heth | -2 | 7 | 2Chr 25:21 | `bethshemesh` |  |
| 6 | all_source | `eng_heth` | Heth | -2 | 7 | 2Kgs 14:13 | `bethshemesh` |  |
| 7 | all_source | `eng_edom` | Edom | -2 | 7 | 2Sam 10:1 | `ammon` |  |
| 8 | all_source | `eng_eyes` | Eyes | 2 | 7 | Deut 14:6 | `beast` |  |
| 9 | all_source | `eng_eyes` | Eyes | 2 | 7 | Ezek 34:8 | `beast` |  |
| 10 | all_source | `eng_eyes` | Eyes | 2 | 7 | Ezek 39:17 | `beast` |  |
| 11 | all_source | `eng_noah` | Noah | 2 | 7 | Gen 10:19 | `lasha` |  |
| 12 | all_source | `eng_eyes` | Eyes | 2 | 7 | Gen 1:30 | `beast` |  |
| 13 | all_source | `eng_seba` | Seba | -2 | 7 | Gen 21:32 | `beersheba` |  |
| 14 | all_source | `eng_seba` | Seba | -2 | 7 | Gen 22:19 | `beersheba` |  |
| 15 | all_source | `eng_eyes` | Eyes | 2 | 7 | Gen 2:19 | `beast` |  |
| 16 | all_source | `eng_eyes` | Eyes | 2 | 7 | Gen 2:20 | `beast` |  |
| 17 | all_source | `eng_eyes` | Eyes | 2 | 7 | Gen 34:23 | `beast` |  |
| 18 | all_source | `eng_eyes` | Eyes | 2 | 7 | Gen 3:14 | `beast` |  |
| 19 | all_source | `eng_eyes` | Eyes | 2 | 7 | Gen 7:14 | `beast` |  |
| 20 | all_source | `eng_eyes` | Eyes | 2 | 7 | Gen 8:19 | `beast` |  |

### center_verse_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `eng_hand` | Hand | -2 | 7 | 1Chr 2:2 | `and` |  |
| 2 | all_source | `eng_heth` | Heth | -2 | 7 | 1Cor 10:20 | `ye` |  |
| 3 | all_source | `eng_heth` | Heth | -2 | 7 | 1Cor 5:2 | `he` |  |
| 4 | all_source | `eng_heth` | Heth | -2 | 7 | 1Cor 9:10 | `he` |  |
| 5 | all_source | `eng_heth` | Heth | -2 | 7 | 1John 2:11 | `whither` |  |
| 6 | all_source | `eng_heal` | Heal | -2 | 7 | 1Kgs 1:6 | `displeased` |  |
| 7 | all_source | `eng_hand` | Hand | -2 | 7 | 1Kgs 3:6 | `according` |  |
| 8 | all_source | `eng_seal` | Seal | 2 | 7 | 1Kgs 6:22 | `finished` |  |
| 9 | all_source | `eng_seal_2` | Seal | 2 | 7 | 1Kgs 6:22 | `finished` |  |
| 10 | all_source | `eng_seal_3` | Seal | 2 | 7 | 1Kgs 6:22 | `finished` |  |
| 11 | all_source | `eng_lord` | Lord | 2 | 7 | 1Sam 10:19 | `your` |  |
| 12 | all_source | `eng_lord_2` | Lord | 2 | 7 | 1Sam 10:19 | `your` |  |
| 13 | all_source | `eng_heth` | Heth | -2 | 7 | 2Chr 23:4 | `ye` |  |
| 14 | all_source | `eng_heth` | Heth | -2 | 7 | 2Kgs 11:5 | `ye` |  |
| 15 | all_source | `eng_heth` | Heth | -2 | 7 | 2Kgs 6:14 | `thither` |  |
| 16 | all_source | `eng_heth` | Heth | -2 | 7 | 2Sam 19:18 | `he` |  |
| 17 | all_source | `eng_moab` | Moab | -2 | 7 | 2Sam 19:4 | `absalom` |  |
| 18 | all_source | `eng_heth` | Heth | -2 | 7 | 2Sam 24:24 | `the` |  |
| 19 | all_source | `eng_heth` | Heth | -2 | 7 | Acts 1:2 | `he` |  |
| 20 | all_source | `eng_heth` | Heth | -2 | 7 | Dan 5:29 | `he` |  |

### center_verse_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `eng_sign` | Sign | -2 | 7 | 1Chr 10:13 | `against` |  |
| 2 | all_source | `eng_adar` | Adar | -2 | 7 | 1Chr 11:19 | `and` |  |
| 3 | all_source | `eng_adam` | Adam | -2 | 7 | 1Chr 12:31 | `and` |  |
| 4 | all_source | `eng_adar` | Adar | -2 | 7 | 1Chr 13:8 | `and` |  |
| 5 | all_source | `eng_soul_2` | Soul | 2 | 7 | 1Chr 14:1 | `build` |  |
| 6 | all_source | `eng_adar` | Adar | -2 | 7 | 1Chr 15:16 | `and` |  |
| 7 | all_source | `eng_adam` | Adam | -2 | 7 | 1Chr 15:27 | `and` |  |
| 8 | all_source | `eng_adam` | Adam | -2 | 7 | 1Chr 17:16 | `and` |  |
| 9 | all_source | `eng_adar` | Adar | -2 | 7 | 1Chr 17:16 | `and` |  |
| 10 | all_source | `eng_adam` | Adam | -2 | 7 | 1Chr 19:2 | `and` |  |
| 11 | all_source | `eng_adar` | Adar | 2 | 7 | 1Chr 19:5 | `tarry` |  |
| 12 | all_source | `eng_adam` | Adam | -2 | 7 | 1Chr 20:1 | `and` |  |
| 13 | all_source | `eng_adam` | Adam | -2 | 7 | 1Chr 21:13 | `and` |  |
| 14 | all_source | `eng_hand` | Hand | -2 | 7 | 1Chr 21:5 | `and` |  |
| 15 | all_source | `eng_hand` | Hand | -2 | 7 | 1Chr 22:14 | `and` |  |
| 16 | all_source | `eng_soul_2` | Soul | 2 | 7 | 1Chr 22:2 | `build` |  |
| 17 | all_source | `eng_nero_2` | Nero | -2 | 7 | 1Chr 28:1 | `course` |  |
| 18 | all_source | `eng_adam` | Adam | 2 | 7 | 1Chr 28:2 | `had` |  |
| 19 | all_source | `eng_adar` | Adar | -2 | 7 | 1Chr 28:20 | `and` |  |
| 20 | all_source | `eng_adar` | Adar | -2 | 7 | 1Chr 29:17 | `and` |  |

### span_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `eng_heth` | Heth | -2 | 7 | Matt 13:21 | `yet` |  |
| 2 | all_source | `eng_hand` | Hand | -3 | 10 | 1Chr 8:23 | `hanan` |  |
| 3 | all_source | `eng_lord` | Lord | -3 | 10 | 1Sam 30:24 | `who` |  |
| 4 | all_source | `eng_lord_2` | Lord | -3 | 10 | 1Sam 30:24 | `who` |  |
| 5 | all_source | `eng_isis` | ISIS | -3 | 10 | Josh 15:19 | `springs` |  |
| 6 | all_source | `eng_hand` | Hand | -3 | 10 | Prov 6:12 | `a` |  |
| 7 | all_source | `eng_heal` | Heal | -4 | 13 | 2Chr 15:9 | `and` |  |
| 8 | all_source | `eng_fire` | Fire | 4 | 13 | Ezek 22:22 | `silver` |  |
| 9 | all_source | `eng_hand` | Hand | 4 | 13 | Gal 6:12 | `many` |  |
| 10 | all_source | `eng_word` | Word | -4 | 13 | John 3:33 | `true` |  |
| 11 | all_source | `eng_heth` | Heth | 4 | 13 | Lev 15:28 | `but` |  |
| 12 | all_source | `eng_hand` | Hand | -4 | 13 | Neh 12:33 | `azariah` |  |
| 13 | all_source | `eng_hail` | Hail | -4 | 13 | Ps 105:31 | `coasts` |  |
| 14 | all_source | `eng_soul` | Soul | -4 | 13 | Ps 109:30 | `multitude` |  |
| 15 | all_source | `eng_soul_2` | Soul | -4 | 13 | Ps 109:30 | `multitude` |  |
| 16 | all_source | `eng_truth` | Truth | 4 | 17 | 3John 1:9 | `unto` |  |
| 17 | all_source | `eng_truth_3` | Truth | 4 | 17 | 3John 1:9 | `unto` |  |
| 18 | all_source | `eng_heth` | Heth | -5 | 16 | 1Kgs 18:2 | `and` |  |
| 19 | all_source | `eng_heth` | Heth | -5 | 16 | 1Kgs 1:26 | `called` |  |
| 20 | all_source | `eng_amen` | Amen | -5 | 16 | 2Chr 18:24 | `and` |  |

### span_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `eng_adar` | Adar | -2 | 7 | 1Sam 15:14 | `and` |  |
| 2 | all_source | `eng_mash` | Mash | -2 | 7 | 1Sam 28:18 | `day` |  |
| 3 | all_source | `eng_adar` | Adar | -2 | 7 | 1Sam 2:1 | `and` |  |
| 4 | all_source | `eng_adar` | Adar | -2 | 7 | 1Sam 30:2 | `and` |  |
| 5 | all_source | `eng_adam` | Adam | -2 | 7 | 1Sam 9:22 | `and` |  |
| 6 | all_source | `eng_nero_2` | Nero | 2 | 7 | 2Sam 15:36 | `hear` |  |
| 7 | all_source | `eng_moab` | Moab | -2 | 7 | 2Sam 16:23 | `absalom` |  |
| 8 | all_source | `eng_seba` | Seba | -2 | 7 | Deut 33:11 | `bless` |  |
| 9 | all_source | `eng_adam` | Adam | -2 | 7 | Eph 1:22 | `and` |  |
| 10 | all_source | `eng_adam` | Adam | -2 | 7 | Gen 22:16 | `and` |  |
| 11 | all_source | `eng_aids` | AIDS | -2 | 7 | Gen 26:12 | `him` |  |
| 12 | all_source | `eng_adam` | Adam | -2 | 7 | Gen 30:34 | `and` |  |
| 13 | all_source | `eng_adar` | Adar | -2 | 7 | Gen 31:28 | `and` |  |
| 14 | all_source | `eng_hand` | Hand | -2 | 7 | Gen 32:31 | `and` |  |
| 15 | all_source | `eng_fire` | Fire | -2 | 7 | Heb 4:2 | `heard` |  |
| 16 | all_source | `eng_bear` | Bear | 2 | 7 | Jer 50:37 | `robbed` |  |
| 17 | all_source | `eng_shem` | Shem | -2 | 7 | Job 19:11 | `enemies` |  |
| 18 | all_source | `eng_aids` | AIDS | -2 | 7 | Luke 23:10 | `him` |  |
| 19 | all_source | `eng_heth` | Heth | 2 | 7 | Matt 11:25 | `at` |  |
| 20 | all_source | `eng_ahab` | Ahab | 2 | 7 | Matt 12:2 | `day` |  |

### hidden_path_only

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `eng_heal` | Heal | -2 | 7 | 1Chr 10:11 | `jabeshgilead` |  |
| 2 | all_source | `eng_cush` | Cush | -2 | 7 | 1Chr 10:4 | `these` |  |
| 3 | all_source | `eng_heth` | Heth | 2 | 7 | 1Chr 10:4 | `lest` |  |
| 4 | all_source | `eng_bear` | Bear | 2 | 7 | 1Chr 11:8 | `repaired` |  |
| 5 | all_source | `eng_noah` | Noah | 2 | 7 | 1Chr 12:36 | `of` |  |
| 6 | all_source | `eng_horn` | Horn | 2 | 7 | 1Chr 13:5 | `bring` |  |
| 7 | all_source | `eng_horn` | Horn | 2 | 7 | 1Chr 13:6 | `bring` |  |
| 8 | all_source | `eng_soul` | Soul | 2 | 7 | 1Chr 14:1 | `build` |  |
| 9 | all_source | `eng_shem` | Shem | -2 | 7 | 1Chr 16:12 | `remember` |  |
| 10 | all_source | `eng_geta` | Geta | 2 | 7 | 1Chr 16:14 | `judgments` |  |
| 11 | all_source | `eng_adar` | Adar | -2 | 7 | 1Chr 16:39 | `and` |  |
| 12 | all_source | `eng_hail` | Hail | -2 | 7 | 1Chr 17:1 | `in` |  |
| 13 | all_source | `eng_otho` | Otho | -2 | 7 | 1Chr 17:1 | `prophet` |  |
| 14 | all_source | `eng_hail` | Hail | 2 | 7 | 1Chr 17:16 | `am` |  |
| 15 | all_source | `eng_adam` | Adam | -2 | 7 | 1Chr 17:17 | `and` |  |
| 16 | all_source | `eng_star` | Star | -2 | 7 | 1Chr 17:19 | `servants` |  |
| 17 | all_source | `eng_heal` | Heal | -2 | 7 | 1Chr 17:27 | `please` |  |
| 18 | all_source | `eng_hail` | Hail | -2 | 7 | 1Chr 17:5 | `in` |  |
| 19 | all_source | `eng_hand` | Hand | 2 | 7 | 1Chr 1:30 | `and` |  |
| 20 | all_source | `eng_adam` | Adam | -2 | 7 | 1Chr 1:46 | `was` |  |

## Read

Rows at the top are good manual-review candidates because their hidden ELS
path center is located on, or near, surface language from the same declared
term set. The `presence_scope` column reports whether the selected exact
ref-key pattern appears in every configured source, multiple sources, or
only one source among the selected candidate keys.
