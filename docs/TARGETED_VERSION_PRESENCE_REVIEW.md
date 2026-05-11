# Targeted Version Presence Review

Source run:

```bash
python3 -m scripts.run_protocol protocols/targeted_version_presence.toml --resume
```

Generated local outputs:

- `reports/targeted_version_presence_summary.csv`
- `reports/targeted_version_presence_examples.csv`
- `reports/targeted_version_presence_control_targets.csv`
- `reports/targeted_version_presence.md`
- `reports/targeted_version_presence.manifest.json`
- `reports/targeted_version_presence_paired_controls_summary.csv`
- `reports/targeted_version_presence_paired_controls_examples.csv`
- `reports/targeted_version_presence_paired_controls.md`
- `reports/targeted_version_presence_paired_controls.manifest.json`
- `reports/targeted_version_presence_controlled_summary.csv`
- `reports/targeted_version_presence_controlled_examples.csv`
- `reports/targeted_version_presence_controlled.md`
- `reports/targeted_version_presence_controlled.manifest.json`

Latest observed runtimes:

| Step | Runtime |
| --- | ---: |
| `targeted_version_presence` | `0.182s` |
| `targeted_version_presence_paired_controls` | `10.809s` |
| `targeted_version_presence_controlled_review` | `0.177s` |

## Scope

This joins three already-generated report families for the requested
modern/geopolitical/local target rows:

- exact Hebrew MT-family version presence from
  `reports/hebrew_screening_version_presence/term_summary.csv`;
- exact Greek NT version presence from
  `reports/greek_screening_version_presence/term_summary.csv`;
- available paired controls from `reports/targeted_paired_controls_summary.csv`;
- bounded same-skip extension summaries from
  `reports/version_presence_extensions/*_summary.csv`.

The exact-version screens use skip `2..100`, direction `both`, minimum
normalized term length `4`, and capped hits per term per corpus. The older
paired controls use the focused skip `2..50` target set, so controls are present
for only part of this expanded target list.

This protocol also emits representative `2..100` paired controls for nonzero
target rows in:

- Hebrew: `MT_WLC` and `UHB`;
- Greek: `TR_NT` and `SBLGNT`.

Those representative controls use 100 shuffled-term samples and 100 same-length
random samples per row. They control the capped hit counts from the version
presence screen, not uncapped full-corpus counts.

The final controlled table is
`reports/targeted_version_presence_controlled_summary.csv`; it joins those
representative control rows back onto the exact-version summary.

## Summary

| Metric | Count |
| --- | ---: |
| Target rows | 59 |
| Hebrew rows | 31 |
| Greek rows | 28 |
| Rows with all-source exact patterns | 25 |
| Rows absent or unsummarized | 31 |
| Rows below exact-version minimum length | 5 |
| Rows with paired controls available | 21 |
| Rows with representative controls joined | 28 |
| Representative control target rows | 54 |
| Representative control rows reading `not_unusual` | 53 |
| Representative control rows reading uncorrected only | 1 |
| Rows with any strict phrase-extension summary row | 2 |
| Rows with strong plus-term extension top rows | 0 |

## Main Read

The version-distribution view is useful, but it does not change the claim
status of the modern/geopolitical/local targets.

- Some short forms are exact-pattern stable across all observed sources.
- The wider representative controls still do not support a claim.
- Many longer phrases remain absent in both Hebrew and Greek exact-version
  screens.
- The same-skip extension bridge found no strong plus-term extension row for
  this target set.

## Stronger Exact-Version Rows

These rows had the largest all-source exact-pattern counts in the targeted
join. Several are capped short forms, so the counts are screening counts, not
full corpus counts.

| Term | Normalized | Total capped hits | All-source | Leningrad-family | Source-specific | Control read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `france_h` | `צרפת` (Tzarfat; English: France) | 250 | 46 | 3 | 4 | no paired control in this run |
| `nato_h` | `נאטו` (NATO; English: NATO) | 250 | 43 | 7 | 5 | no paired control in this run |
| `iran_h` | `איראנ` (Iran; English: Iran) | 250 | 44 | 5 | 6 | `not_unusual` |
| `vance_h` | `ואנס` (Vance; English: Vance) | 250 | 43 | 6 | 9 | `not_unusual` |
| `alliance_h` | `ברית` (berit; English: alliance/covenant) | 250 | 36 | 13 | 15 | no paired control in this run |
| `usa_abbrev_h` | `ארהב` (ARHB; English: USA abbreviation) | 250 | 37 | 8 | 8 | no paired control in this run |
| `magog_h` | `מגוג` (Magog; English: Magog) | 250 | 39 | 11 | 11 | `not_unusual` |
| `iran_g` | `ιραν` (iran; English: Iran) | 200 | 38 | 0 | 12 | `not_unusual` |
| `nato_g` | `νατο` (nato; English: NATO) | 200 | 38 | 0 | 22 | no paired control in this run |
| `hamas_h` | `חמאס` (Hamas; English: Hamas) | 250 | 37 | 13 | 13 | no paired control in this run |

## Requested Phrase And Local Rows

| Term | Hebrew result | Greek result | Read |
| --- | --- | --- | --- |
| United States | absent | absent | no exact-version row in capped screen |
| United States of America | absent | absent | no exact-version row in capped screen |
| United Nations | absent; acronym below minimum length | absent; acronym below minimum length | phrase absent; acronyms too short for this matrix |
| European Union | absent | absent | no exact-version row in capped screen |
| Cowboy | 62 capped hits; 8 all-source patterns | absent | version-distribution row only |
| Catering | absent | absent | no exact-version row in capped screen |
| Cowboy Catering | absent | absent | no exact-version row in capped screen |
| Simsberry | absent | absent | no exact-version row in capped screen |
| Simscorner | absent | absent | no exact-version row in capped screen |

## Extension Read

Only two target rows appeared in the bounded strict phrase-extension summaries:

| Term | Extension summary rows | Best extension summary row |
| --- | ---: | --- |
| `cowboy_h` (Hebrew `קאובוי` (kauboy; English: Cowboy)) | 1 | `MT_WLC after_match skip=40 match=phrase_2 max_len=4` |
| `hamas_g` (Greek `χαμασ` (chamas; English: Hamas)) | 2 | `TR_NT after_match skip=16 match=phrase_2 max_len=4` |

Neither produced a strong `before_plus_term`, `term_plus_after`, or
`before_plus_term_plus_after` top row.

## Representative Paired Controls

The second protocol step produced 54 representative control rows across 28
nonzero terms:

| Corpus | Rows |
| --- | ---: |
| `MT_WLC` | 18 |
| `UHB` | 18 |
| `TR_NT` | 9 |
| `SBLGNT` | 9 |

Band counts:

| Band | Rows |
| --- | ---: |
| `not_unusual` | 53 |
| `paired_uncorrected_p_le_0.05` | 1 |

The one uncorrected row was `UHB germany_h`, with p = `0.049505` and adjusted
q = `1.0`. It remains an uncorrected screen only.

Current control read: the expanded representative controls reinforce the
earlier caution. Version stability does not become significance.

The controlled summary joins those controls back to the target rows:

| Final controlled read | Rows |
| --- | ---: |
| version-stable where present, but representative controls do not support a claim | 24 |
| absent or unsummarized in exact-version matrix | 26 |
| not comparable because normalized form is short | 5 |
| multi-source exact rows only; not all-source stable | 2 |
| source-specific exact rows only | 1 |
| uncorrected representative-control screen only; no adjusted support | 1 |

## Cautions

This report is a triage sheet. It answers which exact patterns appear in which
source streams. It does not establish meaning or significance.

Before promoting any row, require:

- a predeclared target list;
- row-local paired controls for the same skip range;
- correction across tested rows;
- surface/passage context review;
- letter-path audit.
