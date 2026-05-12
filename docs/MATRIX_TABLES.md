# Matrix Tables

Command:

```bash
python3 -m els matrix \
  --config configs/example_oshb_wlc.toml \
  --hits reports/search_hits.csv \
  --out reports/search_hit_matrix_letters.csv \
  --summary-out reports/search_hit_matrix_summary.csv
```

Purpose:

- turn an ELS hit CSV into table row/column coordinates;
- save a letter path for audit;
- support WRR-style and popular Bible-code table review without manual copying.

## Row Width

By default, row width is `abs(skip)` for each hit. That lays the ELS letters in
one column when the table is wrapped by the same interval.

Override it with:

```bash
--row-width 50
```

Use an explicit width when comparing multiple hits in the same table layout.

## Cluster Candidates

To extract multi-term matrix-neighborhood candidates from an existing hit CSV,
use:

```bash
python3 -m scripts.build_matrix_cluster_candidates \
  --hits reports/search_hits.csv \
  --row-width 50 \
  --max-cell-distance 1 \
  --out reports/matrix_clusters/candidates.csv
```

This reports pairs of different terms whose ELS letter paths touch the same
matrix cell or fall within the declared Chebyshev cell distance. The script is
parameterized on row width and distance; it does not choose a geometry for a
claim.

## Outputs

The letter output has one row per ELS letter:

- hit index;
- term and normalized term;
- skip and direction;
- letter index;
- normalized letter;
- absolute stream offset;
- row and column;
- verse reference;
- word fields when the corpus has word spans.

The summary output has one row per hit:

- row width;
- min/max row and column;
- row/column span;
- first/last offset;
- start, end, and center refs.

The cluster-candidate output has one row per neighboring hit pair:

- row width and maximum allowed cell distance;
- observed nearest cell distance;
- nearest left/right cells;
- corpus label;
- left/right hit indexes, term ids, skips, directions, center refs, and center
  words.

Older hit CSVs without center fields are accepted. In that case `center_offset`
is recomputed from the span and center ref/word fields are filled from the
configured corpus.

## Cautions

Matrix coordinates are an audit aid. They do not create statistical support by
themselves. Use them after the term, source, skip range, direction, and controls
are already declared.
