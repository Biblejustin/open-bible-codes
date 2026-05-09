# Version-Presence Extension Screen

This is a bounded same-skip extension screen built from all-source
version-presence rows:

```bash
python3 -m scripts.run_protocol protocols/version_presence_extensions.toml --resume
```

## Scope

Input queues:

- Hebrew: `reports/hebrew_screening_version_presence/hit_patterns.csv`
- Greek: `reports/greek_screening_version_presence/hit_patterns.csv`

Selection:

- presence scope: `present_all_observed_sources`
- max patterns per term: `2`
- max selected patterns per language: `120`

Exported hit rows:

| Queue | Corpora | Hit rows |
| --- | --- | ---: |
| Hebrew | `MT_WLC`, `UHB` | 240 |
| Greek | `TR_NT`, `SBLGNT` | 240 |

Extension settings:

- max letters before: `12`
- max letters after: `12`
- phrase lexicon: surface words and phrases up to 4 words
- both-sided extensions: enabled
- max extension rows per hit: `20`
- summary filter: extension length at least 3, normalized term length at least
  4, phrase matches only

First observed uncached timings:

| Step | Runtime |
| --- | ---: |
| export Hebrew hits | 0.939s |
| export Greek hits | 0.492s |
| MT_WLC extensions | 2.868s |
| UHB extensions | 2.555s |
| TR_NT extensions | 1.371s |
| SBLGNT extensions | 1.373s |

Resume check after the run was cached.

## Output Counts

| Output | Rows |
| --- | ---: |
| `extensions_hebrew_mt_wlc.csv` | 298 |
| `extensions_hebrew_uhb.csv` | 263 |
| `extensions_greek_tr_nt.csv` | 153 |
| `extensions_greek_sblgnt.csv` | 152 |

Phrase-summary rows after the strict filter:

| Corpus | Phrase rows |
| --- | ---: |
| `MT_WLC` | 6 |
| `UHB` | 4 |
| `TR_NT` | 15 |
| `SBLGNT` | 10 |

Strict top rows:

| Corpus | Strong plus-term top rows |
| --- | ---: |
| `MT_WLC` | 0 |
| `UHB` | 0 |
| `TR_NT` | 0 |
| `SBLGNT` | 0 |

## Example Phrase Rows

These are same-skip neighboring-letter phrase matches. They are not surface
phrases in the ELS hit span unless separately reviewed.

| Corpus | Term | Skip | Type | Matched normalized | Surface phrase examples | Phrase refs |
| --- | --- | ---: | --- | --- | --- | --- |
| `MT_WLC` | `איידס` | -70 | before only | `אוילי` | `אוי לי` variants | Isa 6:5; Isa 24:16; Jer 10:19 |
| `MT_WLC` | `מלאך` | 2 | after only | `לואכ` | `לו אך` | 1Sam 18:8 |
| `MT_WLC` | `קאובוי` | 40 | after only | `אומה` | `או מה` | 1Sam 20:10; Job 16:3 |
| `UHB` | `איידס` | -70 | before only | `אוילי` | `אוי לי` variants | ISA 6:5; JER 15:10 |
| `TR_NT` | `αμμων` | -8 | before only | `οεαν` | `ὃ ἐὰν` variants | MAT 12:36; MAT 14:7 |
| `TR_NT` | `βασαν` | 54 | after only | `εισο` | `εἷς ὁ`; `εἰς ὃ` | MAT 19:17; MRK 2:7 |
| `SBLGNT` | `χανααν` | 16 | after only | `οτασ` | `ὁ τὰς` | Heb 11:17 |
| `SBLGNT` | `ιακωβ` | 4 | before only | `οσοι` | `ὅσοι` variants | Matt 14:36; Mark 3:10 |

## Current Read

This confirms the extension bridge works on exact version-presence rows:

- all-source version-presence hits can be exported into normal hit rows;
- same-skip letters before and after those hits can be checked against any
  corpus-derived Hebrew or Greek surface word/phrase;
- the bounded sample produced some before-only and after-only phrase matches;
- it produced no strong `before_plus_term`, `term_plus_after`, or
  `before_plus_term_plus_after` top rows under the strict phrase filter.

Current read: extension scanning is useful for finding review queues, but this
bounded all-source sample does not produce a stronger compound-word or phrase
finding.

The targeted modern/geopolitical/local join that reuses these extension
summaries is tracked in `docs/TARGETED_VERSION_PRESENCE_REVIEW.md`.
