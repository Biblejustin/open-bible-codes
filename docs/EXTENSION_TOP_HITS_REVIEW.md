# Extension Top Hits Review

Scope:

- Source hit file: `reports/protocols/public_baseline/surface_context_hits.csv`
- Extension files:
  - `reports/protocols/public_baseline/surface_context_extensions_tr_nt_top.csv`
  - `reports/protocols/public_baseline/surface_context_extensions_sblgnt_top.csv`
- Settings: same-skip before/after scan, `max_before=12`, `max_after=12`, `phrase_words=4`, `include_both_sided=true`, `max_extensions_per_hit=20`
- Summary filter: `min_extension_length=3`, `min_term_length=4`, `match_kind_prefix=phrase_`, `exclude_term=ουλ`

This is a screening review only. It reports what the tool surfaced; it does not treat any row as statistically meaningful.

## Run Totals

| Corpus | Input surface-context hits | Raw extension rows | Kept after filters | Summary groups | Top rows |
| --- | ---: | ---: | ---: | ---: | ---: |
| TR_NT | 28,123 | 37,190 | 485 | 422 | 11 |
| SBLGNT | 28,531 | 36,946 | 452 | 397 | 21 |

Protocol timings on this run:

| Step | Time |
| --- | ---: |
| `surface_extensions_tr_nt` | 3.376s |
| `surface_extensions_sblgnt` | 3.358s |
| `surface_extension_summary_tr_nt` | 0.213s |
| `surface_extension_summary_sblgnt` | 0.213s |

## Shape Of The Top Rows

The top files are now filtered to phrase matches with base terms of at least four normalized letters and extension lengths of at least three. This removes the worst short-term noise.

| Corpus | Top-row term leaders | Extension length shape | Match kind shape |
| --- | --- | --- | --- |
| TR_NT | `υιος` 4, `θεος` 3, `ναος` 1, `αιμα` 1, `αδαμ` 1, `δοξα` 1 | 10/11 rows have extension length 3 | all 11 rows match phrases |
| SBLGNT | `υιος` 8, `αιμα` 5, `σαλα` 2, plus single rows for `ΝΑΤΟ`, `ισαακ`, `θεος`, `αδαμ`, `ναος`, `δοξα` | 20/21 rows have extension length 3 | all 21 rows match phrases |

Interpretation:

- `ουλ` was excluded because it dominated the previous top file and mostly extended into ordinary servant/people/Saul surface forms.
- Phrase matches are surface-lexicon matches elsewhere in the same corpus, not proof that the hit location itself reads as that phrase.
- Remaining rows are more readable. The first paired-control pass is tracked in
  `docs/EXTENSION_PAIRED_CONTROLS.md`.

## Stronger TR_NT Candidates

Rows below use a rough stricter screen: normalized base term length at least 4 and extension length at least 3.

| Term | Skip | Type | Extended sequence | Surface match | Hit span | Center/context |
| --- | ---: | --- | --- | --- | --- | --- |
| `θεος` | -40 | term plus after | `θεοσοτιο` | Θεός ὅτι ὁ | MAT 24:48-MAT 24:46 | center MAT 24:48 `δὲ`; same category center `lord_g` |
| `ναος` | -38 | both-sided | `ηοναοσο` | ἢ ὁ ναὸς ὁ | MAT 27:9-MAT 27:8 | center MAT 27:9 `Καὶ`; same category span |
| `υιος` | -4 | term plus after | `υιοστησ` | υἱὸς τῆς | JHN 5:13-JHN 5:13 | center JHN 5:13 `γὰρ`; same category center `jesus_g` |
| `υιος` | 25 | before plus term | `οδευιοσ` | ὁ δὲ υἱὸς | MAT 16:19-MAT 16:20 | center MAT 16:20 `τοῖς`; same category center `jesus_g`, `christ_g` |
| `αιμα` | -2 | before plus term | `εισαιμα` | εἰς αἷμα | 2CO 6:16-2CO 6:16 | center 2CO 6:16 `μοι`; same category center `temple_g` |
| `αδαμ` | 11 | term plus after | `αδαμεισ` | Ἀδὰμ εἰς | HEB 13:15-HEB 13:16 | center HEB 13:16 `εὐποιΐας` |
| `δοξα` | 21 | term plus after | `δοξανωσ` | δόξαν ὡς | 2TH 3:1-2TH 3:1 | center 2TH 3:1 `Κυρίου`; exact center |

## Stronger SBLGNT Candidates

| Term | Skip | Type | Extended sequence | Surface match | Hit span | Center/context |
| --- | ---: | --- | --- | --- | --- | --- |
| `υιος` | 36 | both-sided | `ουιοσει` | ὁ υἱός, εἰ | John 16:33-John 17:1 | center John 16:33 `θαρσεῖτε`; exact span John 17:1 |
| `αιμα` | 14 | both-sided | `ναιμανο` | Ναιμὰν ὁ | Rev 17:5-Rev 17:6 | center Rev 17:6 `γυναῖκα`; exact center |
| `ΝΑΤΟ` | 19 | both-sided | `ενατομω` | ἐν ἀτόμῳ | John 5:35-John 5:36 | center John 5:36 `δὲ` |
| `υιος` | 33 | before plus term | `ειουιοσ` | εἶ ὁ υἱός | Matt 14:31-Matt 14:33 | center Matt 14:32 `ἀναβάντων`; exact span Matt 14:33 |
| `υιος` | -4 | term plus after | `υιοστησ` | υἱὸς τῆς | John 5:13-John 5:13 | center John 5:13 `γὰρ`; same category center `jesus_g` |
| `ισαακ` | 41 | before plus term | `καιισαακ` | καὶ Ἰσαὰκ | Luke 22:53-Luke 22:55 | center Luke 22:54 `ἀρχιερέως` |
| `υιος` | 25 | before plus term | `ουουιοσ` | οὗ ὁ υἱὸς | Luke 19:9-Luke 19:10 | center Luke 19:9 `ἐστιν`; exact center Luke 19:9-10 |
| `θεος` | 36 | before plus term | `εισθεοσ` | εἷς θεὸς | Jas 4:14-Jas 4:15 | center Jas 4:14 `φαινομένη`; same category span |
| `αιμα` | 41 | before plus term | `εισαιμα` | εἰς αἷμα | Acts 5:17-Acts 5:19 | center Acts 5:18 `ἔθεντο`; same category span |
| `αδαμ` | 11 | term plus after | `αδαμεισ` | Ἀδὰμ εἰς | Heb 13:15-Heb 13:16 | center Heb 13:16 `εὐποιΐας` |
| `δοξα` | 21 | term plus after | `δοξανωσ` | δόξαν ὡς | 2Thess 3:1-2Thess 3:1 | center 2Thess 3:1 `κυρίου`; exact center |

## TR_NT vs SBLGNT Overlap

Strict overlap means same term, skip, direction, extension type, extended sequence, and matched normalized form appeared in both filtered top files. There were 3 strict overlaps.

Representative overlaps:

| Term | Skip | Type | Extended sequence | Surface match | TR_NT span/context | SBLGNT span/context |
| --- | ---: | --- | --- | --- | --- | --- |
| `υιος` | -4 | term plus after | `υιοστησ` | υἱὸς τῆς | JHN 5:13; same category center | John 5:13; same category center |
| `αδαμ` | 11 | term plus after | `αδαμεισ` | Ἀδὰμ εἰς | HEB 13:15-HEB 13:16 | Heb 13:15-Heb 13:16 |
| `δοξα` | 21 | term plus after | `δοξανωσ` | δόξαν ὡς | 2TH 3:1; exact center | 2Thess 3:1; exact center |

## Review Notes

- The strongest-looking rows are mostly ordinary Greek article/preposition completions around theological terms.
- TR_NT and SBLGNT overlaps are useful because they survive text-form variation, but most overlaps occur where the underlying text is essentially the same.
- `ουλ` should remain excluded from top-rank review unless analyzed separately.
- Duplicate-looking rows can appear when separate term rows normalize to the same ELS term.
- The first paired null-control pass made these rows a review queue, not a claim.

## Next Analysis Choices

1. Review the stricter overlap-only controls in `docs/EXTENSION_OVERLAP_CONTROLS.md`.
2. Add a human review report generator that joins extension top rows back to surface context fields automatically.
3. Run broader declared term searches and use the stricter summary filters by default.
