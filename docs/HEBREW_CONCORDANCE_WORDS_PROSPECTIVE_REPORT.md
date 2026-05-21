# Hebrew Concordance Words Prospective Report

Status: initial exact-version screen complete; representative controls pending.

This tracked report summarizes the locked Hebrew concordance clean-lock run after
the exact-version matrix and representative-control target list were generated.
It is review material, not a significance claim.

## Scope

| Field | Value |
| --- | --- |
| Term lock | `terms/hebrew_concordance_prospective_terms_clean_lock.csv` |
| Protocol | `protocols/hebrew_concordance_words_prospective.toml` |
| Corpora | `MT_WLC`, `UXLC`, `EBIBLE_WLC`, `MAM`, `UHB` |
| Exact-version skip range | `2..100`, both directions |
| Representative-control corpora | `MT_WLC`, `UHB` |

## Current Results

| Metric | Rows |
| --- | ---: |
| Target rows | 3,577 |
| Rows with all-source exact patterns | 3,372 |
| Rows absent or unsummarized | 163 |
| Representative control target rows | 6,790 |
| Rows with paired controls | 0 |
| Rows with representative controls | 0 |
| Rows with strong plus-term extension tops | 0 |

## Read

The exact-version screen found many all-source exact rows, but those rows are not
interpretable as unusual until representative paired controls are run.

The generated control-target list contains 6,790 rows: 3,398 for `MT_WLC` and
3,392 for `UHB`. The protocol currently registers 1,000 term-shuffle plus 1,000
random controls per target row, so the full control pass is a large run and
should not be started casually.

## Local Generated Files

These generated files are ignored by git and can be regenerated from the
protocol:

| File | Purpose |
| --- | --- |
| `reports/hebrew_concordance_words_prospective/version_presence.md` | Exact-version matrix report |
| `reports/hebrew_concordance_words_prospective/initial.md` | Initial joined report before controls |
| `reports/hebrew_concordance_words_prospective/control_targets.csv` | Representative-control target rows |
| `reports/hebrew_concordance_words_prospective/initial_summary.csv` | Full per-term initial summary |

## Next Decision

Next work should choose one of these before launching controls:

1. Full registered controls over all 6,790 target rows.
2. A smaller registered pilot control run over a fixed top-risk subset.
3. A stratified sample control run across term length, corpus, and hit-count bands.
