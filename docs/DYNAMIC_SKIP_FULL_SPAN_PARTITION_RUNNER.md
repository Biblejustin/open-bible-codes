# Dynamic Full-Span Partition Runner

This runner executes selected rows from the dynamic full-span partition
plan. It is intentionally selective: it does not launch all dense
partitions unless the caller asks for that.

## Reproduce

Dry-run a few planned dense shards:

```bash
python3 -m scripts.run_dynamic_span_partitions --term-id dyn_beast_h --corpus-label UHB --limit 3 --dry-run
```

Run one bounded shard:

```bash
python3 -m scripts.run_dynamic_span_partitions --term-id dyn_christ_e --corpus-label KJV --limit 1
```

Run all one-partition Bible dense rows below the current 700k shard
ceiling:

```bash
python3 -m scripts.run_dynamic_span_partitions --bible-only --partition-count 1 --max-estimated-hits 700000
```

Run all one-partition non-Bible control dense rows below the current
1M shard ceiling:

```bash
python3 -m scripts.run_dynamic_span_partitions --controls-only --partition-count 1 --max-estimated-hits 1000000
```

## Current Smoke Run

- selected shard: `KJV__dyn_christ_e__full_span__p00001_of_00001__skip_2_644644`
- status: `executed`
- elapsed seconds: 7.578
- exported rows: 56,561 hits plus header
- output size: about 12 MB
- output CSV: `reports/dynamic_skip_focus/partitions/KJV__dyn_christ_e__full_span__p00001_of_00001__skip_2_644644.csv`

## One-Partition Bible Batch

- selected rows: 30
- executed rows: 26
- skipped existing rows: 4
- newly executed estimated hits: 9,368,862
- skipped existing estimated hits: 378,176
- remaining one-partition Bible dense rows: 0

## One-Partition Control Batch

- planned command: `python3 -m scripts.run_dynamic_span_partitions --controls-only --partition-count 1 --max-estimated-hits 1000000`
- intended scope: non-Bible control corpora only
- intended use: complete the bounded dense control side before comparing completed Bible and non-Bible dense exports

## Two-Through-Four Partition Batch

- `--partition-count 2 --max-estimated-hits 1000000`: 22 partitions executed, 15,632,462 estimated hits, 217.169 elapsed command seconds
- `--partition-count 3 --max-estimated-hits 1000000`: 18 partitions executed, 13,693,062 estimated hits, 232.494 elapsed command seconds
- `--partition-count 4 --max-estimated-hits 1000000`: 12 partitions executed, 10,077,504 estimated hits, 155.105 elapsed command seconds
- remaining dense rows with fewer than five planned partitions: 0

## Five-Partition Batch

- `--partition-count 5 --max-estimated-hits 1000000`: 20 partitions executed, 18,572,109 estimated hits, 237.617 elapsed command seconds
- scope: Greek Bible `dyn_iran_g` rows in BYZ_NT, SBLGNT, TCG_NT, and TR_NT
- cached report regeneration after this tier: 106 cache hits, 20 misses, 104.22 wall-clock seconds
- remaining dense rows with fewer than six planned partitions: 0

## Six-Partition Batch

- `--partition-count 6 --max-estimated-hits 1000000`: 66 partitions executed, 59,147,640 estimated hits, 801.522 elapsed command seconds
- scope: Hebrew Bible `dyn_gog_h` and `dyn_messiah_h` rows, plus HEB_PBY_BIALIK `dyn_russia_h`
- cached report regeneration after this tier: 126 cache hits, 66 misses, 328.06 wall-clock seconds
- remaining dense rows with fewer than seven planned partitions: 0

## Seven-Partition Batch

- `--partition-count 7 --max-estimated-hits 1000000`: 49 partitions executed, 43,418,861 estimated hits, 615.273 elapsed command seconds
- scope: Hebrew Bible `dyn_dragon_h` rows, plus ENG_PG_MOBY_DICK `dyn_iran_e` and HEB_PBY_BRENNER `dyn_russia_h`
- cached report regeneration after this tier: 192 cache hits, 49 misses, 248.60 wall-clock seconds
- remaining dense rows with fewer than ten planned partitions: 0

## Ten-Through-Twelve Partition Batch

- `--partition-count 10 --max-estimated-hits 1000000`: 10 partitions executed, 9,046,404 estimated hits, 124.555 elapsed command seconds
- `--partition-count 11 --max-estimated-hits 1000000`: 55 partitions executed, 53,266,655 estimated hits, 811.390 elapsed command seconds
- `--partition-count 12 --max-estimated-hits 1000000`: 36 partitions executed, 33,657,312 estimated hits, 547.041 elapsed command seconds
- scope: Herodotus `dyn_iran_g`; Hebrew controls `dyn_vance_h`/`dyn_iran_h`; MT-family `dyn_yeshua_h`
- cached report regeneration after `partition_count=12`: 306 cache hits, 36 misses, 193.99 wall-clock seconds
- remaining dense rows with fewer than fourteen planned partitions: 0

## Fourteen-Fifteen Partition Batch

- `--partition-count 14 --max-estimated-hits 1000000`: 14 partitions executed, 13,906,683 estimated hits, 218.255 elapsed command seconds
- `--partition-count 15 --max-estimated-hits 1000000`: 30 partitions executed, 29,423,456 estimated hits, 437.783 elapsed command seconds
- scope: Hebrew controls `dyn_magog_h`; LXX `dyn_vance_g`
- cached report regeneration after `partition_count=15`: 356 cache hits, 30 misses, 173.78 wall-clock seconds
- remaining dense rows with fewer than sixteen planned partitions: 0

## Sixteen-Partition Batch

- `--partition-count 16 --max-estimated-hits 1000000`: 16 partitions executed, 15,815,427 estimated hits, 204.813 elapsed command seconds
- scope: English control `ENG_PG_MOBY_DICK` `dyn_gog_e`
- cached report regeneration after `partition_count=16`: 386 cache hits, 16 misses, 88.98 wall-clock seconds
- remaining dense rows with fewer than twenty-three planned partitions: 0

## Twenty-Three Partition Batch

- `--partition-count 23 --max-estimated-hits 1000000`: 46 partitions executed, 45,015,070 estimated hits, 644.519 elapsed command seconds
- scope: Hebrew control `HEB_PBY_AHAD_HAAM` `dyn_messiah_h`; LXX `dyn_gog_g`
- cached report regeneration after `partition_count=23`: 402 cache hits, 46 misses, 266.84 wall-clock seconds
- remaining dense rows with fewer than thirty-four planned partitions: 0

## Thirty-Four Partition Batch

- `--partition-count 34 --max-estimated-hits 1000000`: 34 partitions executed, 33,004,002 estimated hits, 504.922 elapsed command seconds
- scope: Hebrew control `HEB_PBY_AHAD_HAAM` `dyn_dragon_h`
- cached report regeneration after `partition_count=34`: 448 cache hits, 34 misses, 204.59 wall-clock seconds
- remaining dense rows with fewer than forty-three planned partitions: 0

## Forty-Three Partition Batch

- `--partition-count 43 --max-estimated-hits 1000000`: 86 partitions executed, 85,537,885 estimated hits, 1126.950 elapsed command seconds
- scope: Bible `EBIBLE_WLC` and `UHB` `dyn_yhwh_h`
- cached report regeneration after `partition_count=43`: 482 cache hits, 86 misses, 477.14 wall-clock seconds
- remaining dense rows with fewer than forty-four planned partitions: 0

## Forty-Four Partition Batch

- `--partition-count 44 --max-estimated-hits 1000000`: 132 partitions executed, 130,186,442 estimated hits, 1696.893 elapsed command seconds
- scope: Bible `MAM`, `MT_WLC`, and `UXLC` `dyn_yhwh_h`
- cached report regeneration after `partition_count=44`: 568 cache hits, 132 misses, 701.25 wall-clock seconds
- remaining dense rows with fewer than forty-seven planned partitions: 0

## Forty-Seven Partition Batch

- `--partition-count 47 --max-estimated-hits 1000000`: 47 partitions executed, 46,208,269 estimated hits, 691.727 elapsed command seconds
- scope: Hebrew control `HEB_PBY_AHAD_HAAM` `dyn_yeshua_h`
- cached report regeneration after `partition_count=47`: 700 cache hits, 47 misses, 285.48 wall-clock seconds
- remaining dense rows with fewer than fifty-one planned partitions: 0

## Fifty-One Partition Batch

- `--partition-count 51 --max-estimated-hits 1000000`: 51 partitions executed, 50,720,130 estimated hits, 750.496 elapsed command seconds
- scope: English control `ENG_PG_WAR_PEACE` `dyn_iran_e`
- cached report regeneration after `partition_count=51`: 747 cache hits, 51 misses, 302.01 wall-clock seconds
- remaining dense rows with fewer than fifty-two planned partitions: 0
- pause point: partition artifacts reached about 187 GiB, with about 71 GiB free on the local volume

## Compression Checkpoint

- compressed completed partition CSVs: 798
- partition artifact directory after compression: about 26 GiB
- compressed payload: 181.30 GiB raw CSV to 26.08 GiB `.csv.gz`
- local free space after compression: about 232 GiB
- cached report regeneration after compression: 798 cache hits, 0 misses, 0.88 wall-clock seconds

## Fifty-Two Partition Batch

- `--partition-count 52 --max-estimated-hits 1000000`: 52 partitions executed, 51,012,025 estimated hits, 809.656 elapsed command seconds
- scope: Hebrew control `HEB_PBY_BIALIK` `dyn_vance_h`
- cached report regeneration after `partition_count=52`: 798 cache hits, 52 misses, 306.51 wall-clock seconds
- post-run compression: 52 CSVs compressed, 12.84 GiB saved, 850 cache hits, 0 misses after recompression
- remaining dense rows with fewer than fifty-three planned partitions: 0

## Fifty-Three Partition Batch

- `--partition-count 53 --max-estimated-hits 1000000`: 106 partitions executed, 104,830,986 estimated hits, 1577.709 elapsed command seconds
- scope: Hebrew controls `HEB_PBY_AHAD_HAAM` `dyn_gog_h`; `HEB_PBY_BRENNER` `dyn_vance_h`
- cached report regeneration after `partition_count=53`: 850 cache hits, 106 misses, 637.51 wall-clock seconds
- post-run compression: 106 CSVs compressed, 27.87 GiB saved, 956 cache hits, 0 misses after recompression
- remaining dense rows with fewer than sixty-five planned partitions: 0

## Sixty-Five Partition Batch

- `--partition-count 65 --max-estimated-hits 1000000`: 65 partitions executed, 64,362,175 estimated hits, 1009.585 elapsed command seconds
- scope: English Bible `KJV` `dyn_iran_e`
- cached report regeneration after `partition_count=65`: 956 cache hits, 65 misses, 338.98 wall-clock seconds
- post-run compression: 65 CSVs compressed, 11.48 GiB saved, 1021 cache hits, 0 misses after recompression
- remaining dense rows with fewer than eighty-two planned partitions: 0

## Eighty-Two Partition Batch

- `--partition-count 82 --max-estimated-hits 1000000`: 82 partitions executed, 81,141,952 estimated hits, 1166.140 elapsed command seconds
- scope: Greek Bible `LXX` `dyn_iran_g`
- cached report regeneration after `partition_count=82`: 1021 cache hits, 82 misses, 479.43 wall-clock seconds
- post-run compression: 82 CSVs compressed, 15.85 GiB saved, 1103 cache hits, 0 misses after recompression
- remaining dense rows with fewer than ninety-one planned partitions: 0

## Ninety-One Partition Batch

- `--partition-count 91 --max-estimated-hits 1000000`: 91 partitions executed, 90,027,911 estimated hits, 1410.974 elapsed command seconds
- scope: Hebrew control `HEB_PBY_BRENNER` `dyn_messiah_h`
- cached report regeneration after `partition_count=91`: 1103 cache hits, 91 misses, 598.45 wall-clock seconds
- post-run compression: 91 CSVs compressed, 23.90 GiB saved, 1194 cache hits, 0 misses after recompression
- remaining dense rows with fewer than ninety-nine planned partitions: 0

## Ninety-Nine Partition Batch

- `--partition-count 99 --max-estimated-hits 1000000`: 99 partitions executed, 98,950,467 estimated hits, 1485.670 elapsed command seconds
- scope: English control `ENG_PG_WAR_PEACE` `dyn_gog_e`
- cached report regeneration after `partition_count=99`: 1194 cache hits, 99 misses, 609.39 wall-clock seconds
- post-run compression: 99 CSVs compressed, 26.54 GiB saved, 1293 cache hits, 0 misses after recompression
- remaining dense rows with fewer than one hundred eleven planned partitions: 0

The generated partition hit CSVs remain ignored artifacts. The runner
and partition plan make them reproducible.

## Controls

- `--partition-id` runs exact partition IDs.
- `--term-id` filters by dynamic focus term.
- `--corpus-label` filters by corpus.
- `--min-partition-index` and `--max-partition-index` select a range within a term/corpus queue.
- `--partition-count` filters to rows with exactly that planned partition count.
- `--max-estimated-hits` avoids unexpectedly large shards.
- `--bible-only` excludes non-Bible control corpora.
- `--controls-only` excludes Bible corpora.
- `--limit` caps selected rows after filtering.
- `--dry-run` writes commands to the status CSV without executing them.
- `--rerun` overrides the default skip-existing behavior.

## Report Regeneration Cache

`scripts.summarize_dynamic_span_partition_outputs` writes an ignored
per-partition summary cache at
`reports/dynamic_skip_focus/full_span_partition_summary_cache.json`.

Observed on the current 106 completed partition outputs:

- cold scan, no cache: 325.36 seconds
- warm cache: 0.35 seconds
- warm-cache manifest: 106 hits, 0 misses

The cache key includes partition CSV and manifest path, size, mtime, and
example limit. Use `--no-cache` to force a full rescan.

## Compressed Partition Artifacts

Completed partition hit CSVs can be compressed in place:

```bash
python3 -m scripts.compress_dynamic_span_partition_outputs
```

The runner and summarizer treat either `partition.csv` or
`partition.csv.gz` as a completed partition when the matching manifest
exists. The compressor updates the summary cache fingerprints after
compression, so later report regeneration should continue using cached
per-partition summaries instead of rescanning older compressed hit files.

## Read

- This makes dense all-hit export operational, but it should still be
  run in batches.
- Start with `--dry-run`, then run small `--limit` batches.
- For very dense Hebrew and English rows, use lower `--max-estimated-hits`
  or regenerate the partition plan with a smaller target.
