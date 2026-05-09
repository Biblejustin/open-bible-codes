# Strong Control Manageable Full-Span Hit Export

This targeted control follow-up exports the low-hit language-matched control
row corresponding to a strong Bible full-span row with exact center-word hits.

This report exports full hit metadata for dynamic-span count rows whose
observed count is below the configured threshold. High-density rows are
not discarded; they are deferred for partitioned export because they can
contain millions or billions of paths.

## Reproduce

```bash
python3 -m scripts.export_dynamic_span_hits --max-count-row-hits 50000
```

## Run Counts

- selected count rows: 1
- skipped count rows: 0
- exported hit rows: 16,741
- max count row hits: 50,000
- max export hits per term/corpus/mode: 0
- min abs skip override: 
- max abs skip override: 
- hit CSV: `reports/dynamic_skip_focus/strong_control_manageable_exact_center_full_span_hits.csv`

## Status Counts

| Status | Rows |
| --- | ---: |
| `exported_all_hits` | 1 |

## Exported Rows

| Corpus | Term | Mode | Count row hits | Exported hits | Status |
| --- | --- | --- | ---: | ---: | --- |
| GRC_PERSEUS_HERODOTUS | `dyn_jesus_g` | `full-span` | 16741 | 16741 | `exported_all_hits` |

## Deferred Rows

| Corpus | Term | Mode | Count row hits | Status |
| --- | --- | --- | ---: | --- |
