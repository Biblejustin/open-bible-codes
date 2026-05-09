# Dynamic Full-Span Partition Plan

This plan splits high-density dynamic full-span rows into bounded
absolute-skip ranges. It does not drop those rows; it creates a
reproducible path to export them in shards.

## Reproduce

```bash
python3 -m scripts.plan_dynamic_span_partitions
```

## Scope

- dense threshold: 50,000 hits
- target hits per partition: 1,000,000
- dense count rows planned: 147
- planned partitions: 13,646
- total dense row hits represented: 13,556,483,793
- plan CSV: `reports/dynamic_skip_focus/full_span_partition_plan.csv`

## Dense Rows By Language

| Language | Rows |
| --- | ---: |
| english | 27 |
| greek | 34 |
| hebrew | 86 |

## Largest Dense Rows

| Corpus | Term | Hits | Max skip | Partitions |
| --- | --- | ---: | ---: | ---: |
| HEB_PBY_BRENNER | `dyn_beast_h` | 3,663,683,890 | 2,785,650 | 3,664 |
| HEB_PBY_BIALIK | `dyn_beast_h` | 3,152,690,416 | 2,857,999 | 3,153 |
| HEB_PBY_BRENNER | `dyn_yhwh_h` | 1,090,879,372 | 1,857,100 | 1,091 |
| HEB_PBY_AHAD_HAAM | `dyn_beast_h` | 816,402,749 | 1,379,092 | 817 |
| HEB_PBY_BIALIK | `dyn_yhwh_h` | 803,341,146 | 1,905,332 | 804 |
| HEB_PBY_BRENNER | `dyn_gog_h` | 266,462,544 | 2,785,650 | 267 |
| HEB_PBY_BIALIK | `dyn_gog_h` | 259,364,876 | 2,857,999 | 260 |
| HEB_PBY_AHAD_HAAM | `dyn_yhwh_h` | 230,979,253 | 919,394 | 231 |
| ENG_PG_SHAKESPEARE | `dyn_gog_e` | 217,556,768 | 2,028,610 | 218 |
| HEB_PBY_BIALIK | `dyn_yeshua_h` | 206,897,417 | 1,905,332 | 207 |
| HEB_PBY_BRENNER | `dyn_yeshua_h` | 188,603,935 | 1,857,100 | 189 |
| EBIBLE_WLC | `dyn_beast_h` | 165,249,617 | 598,520 | 166 |
| UHB | `dyn_beast_h` | 164,784,929 | 597,811 | 165 |
| MAM | `dyn_beast_h` | 164,260,192 | 600,987 | 165 |
| UXLC | `dyn_beast_h` | 163,014,892 | 598,521 | 164 |
| MT_WLC | `dyn_beast_h` | 163,013,648 | 598,520 | 164 |
| HEB_PBY_BRENNER | `dyn_dragon_h` | 145,655,795 | 1,857,100 | 146 |
| HEB_PBY_BIALIK | `dyn_dragon_h` | 143,129,945 | 1,905,332 | 144 |
| ENG_PG_SHAKESPEARE | `dyn_iran_e` | 113,877,707 | 1,352,406 | 114 |
| KJV | `dyn_gog_e` | 112,614,748 | 1,611,612 | 113 |
| HEB_PBY_BIALIK | `dyn_messiah_h` | 110,129,394 | 1,905,332 | 111 |
| ENG_PG_WAR_PEACE | `dyn_gog_e` | 98,950,428 | 1,258,456 | 99 |
| HEB_PBY_BRENNER | `dyn_messiah_h` | 90,027,862 | 1,857,100 | 91 |
| LXX | `dyn_iran_g` | 81,141,888 | 930,619 | 82 |
| KJV | `dyn_iran_e` | 64,362,163 | 1,074,408 | 65 |

## First Export Commands

These commands are examples from the plan CSV. They use `--max-export-hits 0`,
which means no cap inside the bounded skip shard.

```bash
python3 -m scripts.export_dynamic_span_hits --include-dense --max-export-hits 0 --corpus-label HEB_PBY_BRENNER --term-id dyn_beast_h --mode full-span --min-abs-skip 2 --max-abs-skip 761 --out reports/dynamic_skip_focus/partitions/HEB_PBY_BRENNER__dyn_beast_h__full_span__p00001_of_03664__skip_2_761.csv --summary-out reports/dynamic_skip_focus/partitions/HEB_PBY_BRENNER__dyn_beast_h__full_span__p00001_of_03664__skip_2_761.md --manifest-out reports/dynamic_skip_focus/partitions/HEB_PBY_BRENNER__dyn_beast_h__full_span__p00001_of_03664__skip_2_761.manifest.json --counts reports/dynamic_skip_focus/nonbible_hebrew_full_span_pair_counts.csv
python3 -m scripts.export_dynamic_span_hits --include-dense --max-export-hits 0 --corpus-label HEB_PBY_BRENNER --term-id dyn_beast_h --mode full-span --min-abs-skip 762 --max-abs-skip 1521 --out reports/dynamic_skip_focus/partitions/HEB_PBY_BRENNER__dyn_beast_h__full_span__p00002_of_03664__skip_762_1521.csv --summary-out reports/dynamic_skip_focus/partitions/HEB_PBY_BRENNER__dyn_beast_h__full_span__p00002_of_03664__skip_762_1521.md --manifest-out reports/dynamic_skip_focus/partitions/HEB_PBY_BRENNER__dyn_beast_h__full_span__p00002_of_03664__skip_762_1521.manifest.json --counts reports/dynamic_skip_focus/nonbible_hebrew_full_span_pair_counts.csv
python3 -m scripts.export_dynamic_span_hits --include-dense --max-export-hits 0 --corpus-label HEB_PBY_BRENNER --term-id dyn_beast_h --mode full-span --min-abs-skip 1522 --max-abs-skip 2281 --out reports/dynamic_skip_focus/partitions/HEB_PBY_BRENNER__dyn_beast_h__full_span__p00003_of_03664__skip_1522_2281.csv --summary-out reports/dynamic_skip_focus/partitions/HEB_PBY_BRENNER__dyn_beast_h__full_span__p00003_of_03664__skip_1522_2281.md --manifest-out reports/dynamic_skip_focus/partitions/HEB_PBY_BRENNER__dyn_beast_h__full_span__p00003_of_03664__skip_1522_2281.manifest.json --counts reports/dynamic_skip_focus/nonbible_hebrew_full_span_pair_counts.csv
python3 -m scripts.export_dynamic_span_hits --include-dense --max-export-hits 0 --corpus-label HEB_PBY_BRENNER --term-id dyn_beast_h --mode full-span --min-abs-skip 2282 --max-abs-skip 3042 --out reports/dynamic_skip_focus/partitions/HEB_PBY_BRENNER__dyn_beast_h__full_span__p00004_of_03664__skip_2282_3042.csv --summary-out reports/dynamic_skip_focus/partitions/HEB_PBY_BRENNER__dyn_beast_h__full_span__p00004_of_03664__skip_2282_3042.md --manifest-out reports/dynamic_skip_focus/partitions/HEB_PBY_BRENNER__dyn_beast_h__full_span__p00004_of_03664__skip_2282_3042.manifest.json --counts reports/dynamic_skip_focus/nonbible_hebrew_full_span_pair_counts.csv
python3 -m scripts.export_dynamic_span_hits --include-dense --max-export-hits 0 --corpus-label HEB_PBY_BRENNER --term-id dyn_beast_h --mode full-span --min-abs-skip 3043 --max-abs-skip 3802 --out reports/dynamic_skip_focus/partitions/HEB_PBY_BRENNER__dyn_beast_h__full_span__p00005_of_03664__skip_3043_3802.csv --summary-out reports/dynamic_skip_focus/partitions/HEB_PBY_BRENNER__dyn_beast_h__full_span__p00005_of_03664__skip_3043_3802.md --manifest-out reports/dynamic_skip_focus/partitions/HEB_PBY_BRENNER__dyn_beast_h__full_span__p00005_of_03664__skip_3043_3802.manifest.json --counts reports/dynamic_skip_focus/nonbible_hebrew_full_span_pair_counts.csv
```

## Read

- Partition estimates are based on proportional skip-range width, not a pre-count of each shard.
- A shard may still be heavier than estimated; rerun that shard with narrower skip bounds if needed.
- The full-span count rows remain the source of truth for version presence.
- The partition CSV is the execution queue for dense all-hit export.
