# Critical Omission Breaks Reverse

## Setup

Run:

```bash
python3 -m scripts.analyze_critical_omission_breaks_reverse
```

Outputs:

- `reports/critical_omission_breaks_reverse_summary.csv`
- `reports/critical_omission_breaks_reverse_examples.csv`
- `reports/critical_omission_breaks_reverse_by_verse.csv`
- `reports/critical_omission_breaks_reverse.manifest.json`

## Method

The script builds an augmented SBLGNT corpus by splicing TR-only verses into
SBLGNT in TR canonical order. It then sends those inserted blocks through the
same shared break engine used by the forward omission analysis.

This asks which hits in the augmented text depend on those spliced blocks and
would break when those blocks are removed again.

## Results

Current run:

- Spliced blocks: 20.
- Broken example rows: 636.

## Cautions

- Raw break counts are not significance tests.
- This shared-engine reverse read is comparable to the forward deletion engine, but it is not a full insertion-coordinate survival model.
- SBLGNT and TR wording can differ outside the inserted verses.
