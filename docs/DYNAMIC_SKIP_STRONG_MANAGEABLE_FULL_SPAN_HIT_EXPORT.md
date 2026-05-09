# Strong Manageable Full-Span Hit Export

This targeted follow-up exports the low-hit full-span rows whose Bible max
normalized rate exceeded all observed language-matched controls but were not
part of the dense partition plan.

This report exports full hit metadata for dynamic-span count rows whose
observed count is below the configured threshold. High-density rows are
not discarded; they are deferred for partitioned export because they can
contain millions or billions of paths.

## Reproduce

```bash
python3 -m scripts.export_dynamic_span_hits --max-count-row-hits 50000
```

## Run Counts

- selected count rows: 4
- skipped count rows: 0
- exported hit rows: 3,301
- max count row hits: 50,000
- max export hits per term/corpus/mode: 0
- min abs skip override: 
- max abs skip override: 
- hit CSV: `reports/dynamic_skip_focus/strong_bible_over_control_manageable_full_span_hits.csv`

## Status Counts

| Status | Rows |
| --- | ---: |
| `exported_all_hits` | 4 |

## Exported Rows

| Corpus | Term | Mode | Count row hits | Exported hits | Status |
| --- | --- | --- | ---: | ---: | --- |
| KJV | `dyn_netanyahu_e` | `full-span` | 27 | 27 | `exported_all_hits` |
| KJV | `dyn_simsberry_e` | `full-span` | 2 | 2 | `exported_all_hits` |
| TCG_NT | `dyn_magog_g` | `full-span` | 3271 | 3271 | `exported_all_hits` |
| TR_NT | `dyn_netanyahu_g` | `full-span` | 1 | 1 | `exported_all_hits` |

## Deferred Rows

| Corpus | Term | Mode | Count row hits | Status |
| --- | --- | --- | ---: | --- |
