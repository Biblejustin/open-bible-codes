# English Seed Shuffle Follow-Up Report

Command:

```bash
python3 -m scripts.run_protocol protocols/english_seed_shuffle_followup_100.toml
```

## Scope

- BibleGateway-overlap corpus set: 34 available English versions; 30 missing versions skipped.
- Source rows: `reports/english_seed_shuffle_baseline/summary.csv`
- Candidate rule: `read = observed above shuffled baseline floor`
- Candidates: 1 term/corpus row
- Samples: 100 full-corpus letter shuffles
- Skip range: `2..100`
- Direction: `both`
- Runtime: `733.639s`

## Results

| Corpus | Term | Observed | Null mean | Null min-max | p_ge | z | Read |
| --- | --- | ---: | ---: | --- | ---: | ---: | --- |
| ERV | `eng_hamathite` Hamathite | 1 | 0.06 | 0-1 | 0.0693069 | 3.95811 | observed elevated vs shuffled mean |

## Read

No English seed row survived the 100-sample corpus-letter shuffle at p_ge <= 0.05
after the 34-version BibleGateway refresh.

`eng_hamathite` remained elevated against the shuffled mean, but the empirical
tail was not below 0.05. The survivor list is therefore intentionally empty:

```text
terms/english_seed_followup_survivors.csv
```

Downstream same-letter term shuffle, survivor audit, and paired-control survivor
reports should not be treated as current until a new row clears this gate.
