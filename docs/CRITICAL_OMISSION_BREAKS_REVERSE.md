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
SBLGNT in TR canonical order. It then maps SBLGNT ELS hits into the augmented
coordinate space and sends the inserted blocks through the same break-stat
recording path used by the forward omission analysis.

This asks which SBLGNT hits lose same-skip spacing when the TR-only verses are
inserted back into the text.

## Results

Current run:

- Spliced blocks: 20.
- Broken example rows: 276.
- Break type: spacing only, because insertion does not remove SBLGNT letters.

## Cautions

- Raw break counts are not significance tests.
- SBLGNT and TR wording can differ outside the inserted verses.
