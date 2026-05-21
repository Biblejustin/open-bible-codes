# WRR Claim Readiness

Status: blocked for claim-grade WRR reproduction language.

This gate does not decide disputed WRR method questions. It only records
whether the method-status matrix has the required locked statuses.

## Reproduce

```bash
python3 -m scripts.check_wrr_claim_readiness --status reports/wrr_1994/wrr_method_status.csv --out reports/wrr_1994/wrr_claim_readiness.csv --markdown-out docs/WRR_CLAIM_READINESS.md --manifest-out reports/wrr_1994/wrr_claim_readiness.manifest.json
```

## Gate

| Area | Current status | Required status | Ready | Blocker |
| --- | --- | --- | --- | --- |
| Pair universe | `open` | `locked,source_locked` | `false` | Pair universe: status open is not claim-ready; requires one of locked,source_locked |
| D(w) skip-cap formula | `open` | `locked,source_locked` | `false` | D(w) skip-cap formula: status open is not claim-ready; requires one of locked,source_locked |
| Corrected distance c(w,w') | `smoke_only` | `defined_full_run,full_run_locked` | `false` | Corrected distance c(w,w'): status smoke_only is not claim-ready; requires one of defined_full_run,full_run_locked |
| Aggregate statistic and permutation | `source_locked_not_built` | `claim_grade_ready,permutation_locked` | `false` | Aggregate statistic and permutation: status source_locked_not_built is not claim-ready; requires one of claim_grade_ready,permutation_locked |
