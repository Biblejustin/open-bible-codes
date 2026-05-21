# WRR Windows Split Run

Status: operational handoff for splitting corrected-distance runs across Mac and
Windows. This is diagnostic only, not claim-grade reproduction.

Use the same git commit and source files on both machines.

For a Mac-only verification of the same split/merge flow:

```bash
python3 -m scripts.run_protocol protocols/wrr_corrected_distance_split_2.toml --resume
```

## Mac Shard

```bash
python3 -m scripts.analyze_wrr_corrected_distance \
  --pair-table reports/wrr_1994/wrr2_pair_eligibility_table.csv \
  --config configs/example_koren_genesis.toml \
  --candidate-lane length_5_8_smoke_candidate \
  --min-skip 2 \
  --search-max-skip 250 \
  --direction both \
  --jobs 0 \
  --row-width-count 10 \
  --minimum-valid 10 \
  --skip-cap-mode term \
  --skip-cap-formula printed \
  --shard-index 0 \
  --shard-count 2 \
  --out reports/wrr_1994/shards/wrr2_corrected_distance_s00of02.csv \
  --summary-out reports/wrr_1994/shards/wrr2_corrected_distance_s00of02_summary.csv \
  --markdown-out reports/wrr_1994/shards/wrr2_corrected_distance_s00of02.md \
  --manifest-out reports/wrr_1994/shards/wrr2_corrected_distance_s00of02.manifest.json
```

## Windows Shard

```bash
python3 -m scripts.analyze_wrr_corrected_distance \
  --pair-table reports/wrr_1994/wrr2_pair_eligibility_table.csv \
  --config configs/example_koren_genesis.toml \
  --candidate-lane length_5_8_smoke_candidate \
  --min-skip 2 \
  --search-max-skip 250 \
  --direction both \
  --jobs 0 \
  --row-width-count 10 \
  --minimum-valid 10 \
  --skip-cap-mode term \
  --skip-cap-formula printed \
  --shard-index 1 \
  --shard-count 2 \
  --out reports/wrr_1994/shards/wrr2_corrected_distance_s01of02.csv \
  --summary-out reports/wrr_1994/shards/wrr2_corrected_distance_s01of02_summary.csv \
  --markdown-out reports/wrr_1994/shards/wrr2_corrected_distance_s01of02.md \
  --manifest-out reports/wrr_1994/shards/wrr2_corrected_distance_s01of02.manifest.json
```

Copy the Windows shard CSV, summary CSV, Markdown, and manifest back to the Mac
under `reports/wrr_1994/shards/`.

## Merge

```bash
python3 -m scripts.merge_wrr_corrected_distance_shards \
  --expected-shard-count 2 \
  --shard reports/wrr_1994/shards/wrr2_corrected_distance_s00of02.csv \
  --shard reports/wrr_1994/shards/wrr2_corrected_distance_s01of02.csv \
  --shard-summary reports/wrr_1994/shards/wrr2_corrected_distance_s00of02_summary.csv \
  --shard-summary reports/wrr_1994/shards/wrr2_corrected_distance_s01of02_summary.csv \
  --out reports/wrr_1994/wrr2_corrected_distance_smoke_merged.csv \
  --summary-out reports/wrr_1994/wrr2_corrected_distance_smoke_merged_summary.csv \
  --markdown-out reports/wrr_1994/wrr2_corrected_distance_smoke_merged.md \
  --manifest-out reports/wrr_1994/wrr2_corrected_distance_smoke_merged.manifest.json
```

Then aggregate the merged CSV:

```bash
python3 -m scripts.analyze_wrr_corrected_distance_aggregate \
  --input reports/wrr_1994/wrr2_corrected_distance_smoke_merged.csv \
  --p1-threshold 0.2 \
  --out reports/wrr_1994/wrr2_corrected_distance_aggregate.csv \
  --markdown-out reports/wrr_1994/wrr2_corrected_distance_aggregate.md \
  --manifest-out reports/wrr_1994/wrr2_corrected_distance_aggregate.manifest.json
```

Keep shard artifacts ignored and local. Commit only code, docs, and small final
status documents.
