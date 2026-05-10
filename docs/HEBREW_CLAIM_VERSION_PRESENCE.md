# Hebrew Claim Version Presence

This is the tracked summary for the compiled Hebrew claim-term exact-hit
version-presence run:

```bash
python3 -m scripts.run_protocol protocols/hebrew_claim_version_presence.toml --resume
```

## Scope

- Term source: `terms/hebrew_claim_terms.csv`
- Corpora: `MT_WLC`, `UXLC`, `EBIBLE_WLC`, `MAM`, `UHB`
- Skip range: `2..100`
- Direction: `both`
- Minimum normalized term length: `4`
- Max hits: `100` per term per corpus

The report groups hits by exact ref-key pattern:

`term_id + normalized_term + signed_skip + direction + canonical start/center/end refs`

## Output

Ignored local outputs:

- `reports/hebrew_claim_version_presence/hit_patterns.csv`
- `reports/hebrew_claim_version_presence/term_summary.csv`
- `reports/hebrew_claim_version_presence/hebrew_claim_version_presence.md`
- `reports/hebrew_claim_version_presence/manifest.json`

Latest run:

- Runtime: `23.037s`
- Declared terms: `143`
- Summary rows: `125`
- Hit records: `22,811`
- Exact pattern rows: `5,603`

Pattern scope counts:

| Scope | Pattern rows |
| --- | ---: |
| `present_all_observed_sources` | 3,635 |
| `present_all_leningrad_streams` | 798 |
| `present_multiple_sources` | 214 |
| `source_specific` | 956 |

## Current Read

Short Hebrew forms dominate the stable rows. Core and short claim terms such as
`משיח` (Mashiach; English: Messiah/anointed one), `ישוע` (Yeshua; English: Yeshua/Jeshua), `רמבמ` (Rambam; English: Maimonides), `יהוה` (YHWH; English: YHWH), `תורה` (Torah; English: Torah), `נביא` (navi; English: prophet), and `שלום` (shalom; English: peace) all hit the per-term
cap in every Hebrew stream and produce many exact ref-key patterns shared by all
five sources.

This is expected for dense 4-5 letter strings in a large consonantal corpus. It
is not evidence by itself.

Some longer or more phrase-like rows stay sparse or absent:

- `אני ישוע` (ani Yeshua; English: I am Yeshua) has 3 hits per source and 3 all-source exact patterns.
- `ישוע יתלה` (Yeshua yitlah; English: Yeshua will be hanged) has 1-2 hits per source and 1 all-source exact pattern.
- `ישוע ראוי` (Yeshua ra'ui; English: Yeshua is worthy) has 1 MAM-only hit and no all-source pattern.
- `ישוע נצלב` (Yeshua nitzlav; English: Yeshua was crucified), `ישוע המשיח` (Yeshua haMashiach; English: Yeshua the Messiah), `ישוע מושלם` (Yeshua mushlam; English: Yeshua perfect), `ישוע יחזור` (Yeshua yachzor; English: Yeshua will return), and `ישוע מושיע` (Yeshua moshia; English: Yeshua savior) have no hits in this capped scan.
- `גאון וילנא` (Gaon Vilna; English: Vilna Gaon) has no hits in this capped scan, while shorter rabbinic abbreviations such as `רמבמ` (Rambam; English: Maimonides), `רמבנ` (Ramban; English: Nachmanides), and `מהרל` (Maharal; English: Maharal) are dense.
- `היטלר` (Hitler; English: Hitler) has all-source patterns, but `היטלר רשע` (Hitler rasha; English: Hitler the wicked) has none.
- `טראמפ` (Tramp; English: Trump) has 6 all-source exact patterns; longer political phrases are mostly absent.

Zero-hit rows: `50` of the `125` summarized terms.

## Caution

This run is useful for version distribution, not significance. It answers:

Which exact hit patterns are shared, Leningrad-family only, multi-source, or
source-specific?

It does not answer:

Are these hits meaningful?

Use this report to choose stable review rows before running controls and context
checks.
