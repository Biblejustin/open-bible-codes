# STEP TAHOT Policy Hit Audit

Last run: 2026-05-05.

## Scope

This audit classifies `STEP_TAHOT`-only exact-hit rows from the broader Hebrew
screening run by the TAHOT source-type path touched by the ELS letters.

The question is narrow: when a pattern appears only in `STEP_TAHOT`, is the
hidden-letter path itself touching selected qere (`Q`), restored (`R`), or
LXX-based Hebrew addition (`X`) rows?

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/step_tahot_policy_hits.toml --resume
```

Outputs:

- `reports/step_tahot_policy_hits/step_tahot_only_policy_hits.csv`
- `reports/step_tahot_policy_hits/summary.csv`
- `reports/step_tahot_policy_hits/step_tahot_policy_hits.md`
- `reports/step_tahot_policy_hits/manifest.json`

## Summary

| Metric | Rows |
| --- | ---: |
| `STEP_TAHOT`-only rows audited | 379 |
| Rows touching `Q` qere-selected words | 65 |
| Rows touching `R` restored words | 2 |
| Rows touching `X` LXX-based Hebrew additions | 13 |
| Rows touching other non-L prefixes | 0 |
| Rows whose letter path is only L-prefixed words | 299 |

## Read

Eighty `STEP_TAHOT`-only rows touch at least one `Q`, `R`, or `X` word on the
letter path. Those rows are likely source-policy artifacts unless they survive a
different source-family test.

The remaining 299 rows are `L_ONLY_PATH`, which means the letters themselves
fall in L-prefixed TAHOT words. They can still be `STEP_TAHOT`-only because
earlier qere/restoration/addition decisions, versification, or word division
shifted the global ELS stream before the hit.

Current rule: do not promote `STEP_TAHOT`-only rows. Keep them as source-policy
review rows.
