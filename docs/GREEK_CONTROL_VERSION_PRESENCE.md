# Greek Control Version Presence

This is the tracked summary for the Greek null/frequency control exact-hit
version-presence run:

```bash
python3 -m scripts.run_protocol protocols/greek_control_version_presence.toml --resume
```

## Scope

- Term sources: `terms/null_controls.csv`, `terms/frequency_anchors.csv`
- Corpora: `TR_NT`, `BYZ_NT`, `TCG_NT`, `SBLGNT`
- Skip range: `2..100`
- Direction: `both`
- Minimum normalized term length: `4`
- Max hits: `100` per term per corpus

## Output

Ignored local outputs:

- `reports/greek_control_version_presence/hit_patterns.csv`
- `reports/greek_control_version_presence/term_summary.csv`
- `reports/greek_control_version_presence/greek_control_version_presence.md`
- `reports/greek_control_version_presence/manifest.json`

Latest run:

- Runtime: `12.366s`
- Declared Greek control rows: `20`
- Summary rows: `19`
- Hit records: `2,003`
- Exact pattern rows: `826`

Pattern scope counts:

| Scope | Pattern rows |
| --- | ---: |
| `present_all_observed_sources` | 270 |
| `present_multiple_sources` | 237 |
| `source_specific` | 319 |

Source-specific rows:

| Source | Rows |
| --- | ---: |
| `SBLGNT` | 160 |
| `TR_NT` | 64 |
| `BYZ_NT` | 63 |
| `TCG_NT` | 32 |

## Current Read

Greek controls also produce many exact all-source rows:

- `λαοσ` (laos; English: people): 72 all-source exact patterns.
- scrambled Theos / `σθεο` (stheo; English: scrambled Theos control): 72 all-source exact patterns.
- `χειρ` (cheir; English: hand): 53 all-source exact patterns.
- `οικοσ` (oikos; English: house): 52 all-source exact patterns.
- `ημερα` (hemera; English: day): 16 all-source exact patterns.

This matters because the control all-source rate is higher than the claim-term
all-source rate in this capped run.

## Caution

Version stability remains a reproducibility filter. Controls are version-stable
too, so all-source presence cannot be used as evidence without controls and
context review.
