# Strong Control Full-Span Exact-Center Findings

This targeted control follow-up scans archived dense hit payloads for the
language-matched control-max rows corresponding to strong Bible full-span rows
with exact center-word hits.

This report summarizes completed dense full-span partition outputs.
It is additive to the manageable-row export: a dense row becomes
complete when all planned partition outputs exist and summarize.

## Reproduce

```bash
python3 -m scripts.summarize_dynamic_span_partition_outputs --plan reports/dynamic_skip_focus/strong_control_exact_center_full_span_plan.csv --examples-per-partition 5
```

## Scope

- planned partitions: 323
- completed partition outputs summarized: 323
- completed dense rows: 4
- partial dense rows: 0
- exported partition hit rows summarized: 320,193,958
- exact center-word hits in completed partitions: 8,212
- partition summary CSV: `reports/dynamic_skip_focus/strong_control_exact_center_full_span_partition_summary.csv`
- term summary CSV: `reports/dynamic_skip_focus/strong_control_exact_center_full_span_term_summary.csv`
- examples CSV: `reports/dynamic_skip_focus/strong_control_exact_center_full_span_examples.csv`

## Completed Dense Rows

| Corpus | Term | Hits | Exact center-word hits |
| --- | --- | ---: | ---: |
| ENG_PG_SHAKESPEARE | `dyn_jesus_e` | 87,353 | 2 |
| GRC_PERSEUS_HERODOTUS | `dyn_gog_g` | 3,079,794 | 0 |
| HEB_PBY_BIALIK | `dyn_messiah_h` | 110,129,394 | 7,059 |
| HEB_PBY_BIALIK | `dyn_yeshua_h` | 206,897,417 | 1,151 |

## Partial Dense Rows

| Corpus | Term | Completed partitions | Hits so far | Skip ranges |
| --- | --- | ---: | ---: | --- |

## Completed Partitions

| Partition | Exported hits | Estimated hits | Delta | Exact center-word hits |
| --- | ---: | ---: | ---: | ---: |
| `ENG_PG_SHAKESPEARE__dyn_jesus_e__full_span__p00001_of_00001__skip_2_1014305` | 87,353 | 87,353 | 0 | 2 |
| `GRC_PERSEUS_HERODOTUS__dyn_gog_g__full_span__p00001_of_00004__skip_2_120280` | 1,352,994 | 769,949 | 583,045 | 0 |
| `GRC_PERSEUS_HERODOTUS__dyn_gog_g__full_span__p00002_of_00004__skip_120281_240559` | 945,044 | 769,949 | 175,095 | 0 |
| `GRC_PERSEUS_HERODOTUS__dyn_gog_g__full_span__p00003_of_00004__skip_240560_360838` | 588,426 | 769,949 | -181,523 | 0 |
| `GRC_PERSEUS_HERODOTUS__dyn_gog_g__full_span__p00004_of_00004__skip_360839_481117` | 193,330 | 769,949 | -576,619 | 0 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00001_of_00111__skip_2_17166` | 1,935,577 | 992,149 | 943,428 | 109 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00002_of_00111__skip_17167_34331` | 1,914,568 | 992,149 | 922,419 | 126 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00003_of_00111__skip_34332_51496` | 1,900,048 | 992,149 | 907,899 | 108 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00004_of_00111__skip_51497_68661` | 1,891,318 | 992,149 | 899,169 | 127 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00005_of_00111__skip_68662_85826` | 1,873,845 | 992,149 | 881,696 | 118 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00006_of_00111__skip_85827_102991` | 1,861,060 | 992,149 | 868,911 | 96 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00007_of_00111__skip_102992_120157` | 1,847,819 | 992,207 | 855,612 | 112 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00008_of_00111__skip_120158_137322` | 1,832,603 | 992,149 | 840,454 | 103 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00009_of_00111__skip_137323_154487` | 1,814,670 | 992,149 | 822,521 | 109 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00010_of_00111__skip_154488_171652` | 1,793,015 | 992,149 | 800,866 | 99 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00011_of_00111__skip_171653_188817` | 1,772,021 | 992,149 | 779,872 | 109 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00012_of_00111__skip_188818_205982` | 1,758,768 | 992,149 | 766,619 | 128 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00013_of_00111__skip_205983_223147` | 1,739,813 | 992,149 | 747,664 | 116 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00014_of_00111__skip_223148_240313` | 1,725,994 | 992,207 | 733,787 | 127 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00015_of_00111__skip_240314_257478` | 1,707,505 | 992,149 | 715,356 | 114 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00016_of_00111__skip_257479_274643` | 1,688,844 | 992,149 | 696,695 | 111 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00017_of_00111__skip_274644_291808` | 1,669,929 | 992,149 | 677,780 | 103 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00018_of_00111__skip_291809_308973` | 1,654,314 | 992,149 | 662,165 | 110 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00019_of_00111__skip_308974_326138` | 1,642,988 | 992,149 | 650,839 | 108 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00020_of_00111__skip_326139_343303` | 1,625,645 | 992,149 | 633,496 | 138 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00021_of_00111__skip_343304_360469` | 1,608,316 | 992,207 | 616,109 | 122 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00022_of_00111__skip_360470_377634` | 1,588,498 | 992,149 | 596,349 | 101 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00023_of_00111__skip_377635_394799` | 1,570,732 | 992,149 | 578,583 | 114 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00024_of_00111__skip_394800_411964` | 1,554,605 | 992,149 | 562,456 | 117 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00025_of_00111__skip_411965_429129` | 1,540,097 | 992,149 | 547,948 | 107 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00026_of_00111__skip_429130_446294` | 1,520,140 | 992,149 | 527,991 | 115 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00027_of_00111__skip_446295_463459` | 1,500,635 | 992,149 | 508,486 | 113 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00028_of_00111__skip_463460_480625` | 1,482,347 | 992,207 | 490,140 | 108 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00029_of_00111__skip_480626_497790` | 1,467,297 | 992,149 | 475,148 | 115 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00030_of_00111__skip_497791_514955` | 1,448,549 | 992,149 | 456,400 | 102 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00031_of_00111__skip_514956_532120` | 1,434,483 | 992,149 | 442,334 | 99 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00032_of_00111__skip_532121_549285` | 1,417,939 | 992,149 | 425,790 | 113 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00033_of_00111__skip_549286_566450` | 1,402,372 | 992,149 | 410,223 | 122 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00034_of_00111__skip_566451_583615` | 1,383,319 | 992,149 | 391,170 | 101 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00035_of_00111__skip_583616_600781` | 1,368,226 | 992,207 | 376,019 | 99 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00036_of_00111__skip_600782_617946` | 1,351,909 | 992,149 | 359,760 | 103 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00037_of_00111__skip_617947_635111` | 1,336,551 | 992,149 | 344,402 | 93 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00038_of_00111__skip_635112_652276` | 1,318,466 | 992,149 | 326,317 | 97 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00039_of_00111__skip_652277_669441` | 1,304,933 | 992,149 | 312,784 | 91 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00040_of_00111__skip_669442_686606` | 1,287,652 | 992,149 | 295,503 | 100 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00041_of_00111__skip_686607_703771` | 1,266,260 | 992,149 | 274,111 | 98 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00042_of_00111__skip_703772_720937` | 1,247,704 | 992,207 | 255,497 | 106 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00043_of_00111__skip_720938_738102` | 1,230,403 | 992,149 | 238,254 | 90 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00044_of_00111__skip_738103_755267` | 1,209,737 | 992,149 | 217,588 | 94 |
| `HEB_PBY_BIALIK__dyn_messiah_h__full_span__p00045_of_00111__skip_755268_772432` | 1,193,336 | 992,149 | 201,187 | 94 |

## Example Hits

| Type | Corpus | Term | Skip | Center | Center word |
| --- | --- | --- | ---: | --- | --- |
| `exact_center_word` | ENG_PG_SHAKESPEARE | `dyn_jesus_e` | 212862 | PG Shakespeare | Jesus |
| `exact_center_word` | ENG_PG_SHAKESPEARE | `dyn_jesus_e` | 680396 | PG Shakespeare | Jesus |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -16278 | PBY Bialik | משיח, |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -15926 | PBY Bialik | משיח. |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -15613 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -15319 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -15264 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -34264 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -33849 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -33511 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -33113 | PBY Bialik | משיח1755 |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -32122 | PBY Bialik | משיח? |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -51468 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -51466 | PBY Bialik | משיח, |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -50948 | PBY Bialik | משיח, |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -50535 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -50284 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -68264 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -68087 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -68014 | PBY Bialik | משיח. |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -67260 | PBY Bialik | משיח&nbsp;— |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -67216 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -85184 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -84666 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -84657 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -84537 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -84340 | PBY Bialik | משיח? |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -102907 | PBY Bialik | משיח? |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -102320 | PBY Bialik | משיח |
| `exact_center_word` | HEB_PBY_BIALIK | `dyn_messiah_h` | -102011 | PBY Bialik | משיח |

## Read

- Completed partition rows are no longer deferred; their hit-level metadata exists.
- Exact center-word hits are flags, not the admission rule.
- `not_computed` means the manifest-only path was used; hit counts still come from export manifests.
- Partition estimates are planning estimates; exported hit rows are observed counts.
- The ignored partition CSVs are reproducible from the tracked plan and runner.
