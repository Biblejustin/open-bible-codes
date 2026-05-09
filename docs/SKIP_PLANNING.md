# Skip Planning

Command:

```bash
python3 -m els skip-plan \
  --config configs/example_oshb_wlc.toml \
  --term משיח \
  --min-skip 2 \
  --max-skip-limit 1000 \
  --target-expected-hits 100 \
  --out reports/skip_plan.csv
```

Purpose:

- choose a declared skip cap before a run;
- scale skip ranges by term length and corpus letter frequency;
- avoid widening searches only after seeing interesting rows.

## Model

The planner uses a simple independent-letter estimate:

- compute each query letter frequency from the normalized corpus stream;
- multiply those frequencies to estimate one placement probability;
- sum valid placements from `min_skip` through candidate max skip;
- multiply by direction count (`1` for forward/backward, `2` for both).

This is not a statistical test. It is a conservative planning aid for choosing
search bounds before running a screen.

## Full-Corpus Skip Caps

The CLI can also compute a per-term upper skip bound at search time:

```bash
python3 -m els search \
  --config configs/example_oshb_wlc.toml \
  --term משיח \
  --min-skip 2 \
  --max-skip-mode full-span \
  --out reports/full_span_messiah.csv
```

Supported modes:

| Mode | Meaning |
| --- | --- |
| `fixed` | Use the literal `--max-skip` value. This remains the default for reproducible locked runs. |
| `full-span` | Use `floor((corpus_letters - 1) / (term_letters - 1))`, the exact largest skip where a term can still fit from the start to the end of the corpus. |
| `letters-per-term` | Use `floor(corpus_letters / term_letters)`, matching the rough axis formula sometimes used in simple ELS scatter-plot explanations. |

Use `--max-skip-limit N` with either dynamic mode when you want a safety cap.
The effective max skip is recorded in manifests and in batch output rows.

`full-span` is usually much larger than traditional caps such as `50`, `100`,
or `2000`. It is appropriate for declared exhaustive screens, but it can produce
very large runs. Treat widened skip ranges as a new preregistered study setting,
not as a quiet change to an existing report.

## Output

The CSV includes:

- original and normalized term;
- normalized length;
- selected max skip;
- target expected hits;
- expected hits through the selected cap;
- expected hits at the minimum skip;
- status.

Statuses:

| Status | Meaning |
| --- | --- |
| `capped_by_target` | Next skip would exceed target expected hits. |
| `reached_limit` | Planner reached the hard max skip or corpus-imposed maximum. |
| `target_below_min_skip_expectation` | Even the minimum skip exceeds the target. |
| `skipped_empty_term` | Term normalized to no searchable letters. |

## Cautions

The model assumes independent letters. Real biblical text is not independent.
Use this only to preregister a reasonable search range; use matched controls for
interpretation.
