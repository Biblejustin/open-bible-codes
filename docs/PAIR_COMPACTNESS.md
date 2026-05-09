# Pair Compactness

Command:

```bash
python3 -m els pairs \
  --terms terms/modern_names_dates.csv \
  --corpus MT_WLC=configs/example_oshb_wlc.toml \
  --left-category modern_names \
  --right-category dates \
  --min-skip 2 \
  --max-skip 50 \
  --max-gap 500 \
  --row-width 50 \
  --out reports/modern_name_date_pairs.csv
```

Pair rows include:

- one-dimensional `span_gap`;
- one-dimensional `center_distance`;
- `compactness_score = span_gap + center_distance`;
- overlap and same-center-ref/chapter flags;
- same signed/absolute skip flags;
- span-union width;
- optional cylindrical distance when `--row-width` is supplied.

## Cylindrical Distance

`--row-width` treats the continuous stream as a wrapped table. The cylindrical
distance is the minimum Euclidean row/column distance between any letter in the
left ELS and any letter in the right ELS, with columns wrapping around the row.

This is a WRR-style building block, not a full WRR statistic. Full WRR
replication still needs a locked term/date list, row-width rule, and
permutation test.

## Cautions

Compactness scores rank review queues. They are not p-values and do not account
for term length, spelling choice, source selection, or multiple testing.
