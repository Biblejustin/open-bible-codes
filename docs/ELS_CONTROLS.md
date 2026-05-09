# ELS Statistical Controls

`scripts/analyze_els_controls.py` compares observed ELS counts against two
simple null models:

- letter-shuffled corpus controls: preserve corpus letter frequencies, break word/order structure
- shuffled-term controls: preserve term length and letter multiset, change letter order

Run:

```bash
python3 -m scripts.analyze_els_controls
```

Use `--progress` for corpus and shuffle milestones during longer reruns.

Outputs:

- `reports/els_controls_summary.csv`
- `reports/els_controls_examples.csv`
- `reports/els_controls.manifest.json`

Important fields:

- `observed_hits`: ELS hits in the real corpus
- `letter_p_ge`: smoothed empirical probability that a shuffled corpus count is at least observed
- `term_p_ge`: smoothed empirical probability that a shuffled-term count is at least observed
- `letter_q_value` / `term_q_value`: Benjamini-Hochberg adjusted values across emitted rows
- `combined_min_q_value`: adjusted screening value for the smaller of `letter_p_ge` and `term_p_ge`
- `significance_band`: coarse screening bucket based on adjusted values, not a proof claim
- `search_space_positions`: estimated valid ELS start positions searched for this term
- `hits_per_million_positions`: observed hits normalized by search space size
- `letter_z_score` / `term_z_score`: observed count vs null mean and standard deviation
- `warning_count` / `flags`: warnings such as few controls, zero variance, short terms, low observed hits, and huge search spaces

These are screening controls, not proof of significance. The default public
protocol uses a small sample (`3` letter shuffles, `25` term shuffles) so it can
run quickly. Strong-looking rows need larger reruns, preregistered term lists,
and review of the adjusted values and warning flags before making claims.

## Critique-Driven Guardrails

The CRI critique audit in `docs/CRI_ELS_CRITIQUE_AUDIT.md` adds a standing
control-design checklist:

- lock spellings, corpus, normalization, direction, skip range, row width, and
  cluster metric before any claim run;
- report legal search-space size and all tested rows;
- preserve hidden-path-only rows as data, but do not promote them without
  controls and context;
- separate post-screen follow-up from prospective discovery;
- require archived source timing for modern-event prediction claims;
- treat nonvoweled Hebrew ambiguity as a spelling-audit issue, not as a
  rhetorical afterthought.

Observed local timing on 2026-05-04:

- standalone controls with `--jobs 0` before prophetic-term expansion: 36.14s
- standalone controls with serial counting: 135.45s
- full protocol including prophetic terms and controls: 93.08s
- `els_controls` protocol step with prophetic terms: 70.34s
- summary rows with prophetic terms included: 824
- example rows: 200
