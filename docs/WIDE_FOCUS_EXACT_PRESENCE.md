# Wide Focus Exact-Hit Presence

Source run:

- Protocol: `protocols/wide_focus_exact_presence.toml`
- Command: `python3 -m scripts.run_protocol protocols/wide_focus_exact_presence.toml --resume`
- Status: success
- Hebrew step runtime observed: 56.239s
- Greek step runtime observed: 127.188s
- Hebrew patterns: `reports/wide_focus_exact_presence/hebrew_hit_patterns.csv`
- Hebrew summary: `reports/wide_focus_exact_presence/hebrew_term_summary.csv`
- Hebrew markdown: `reports/wide_focus_exact_presence/hebrew_exact_presence.md`
- Greek patterns: `reports/wide_focus_exact_presence/greek_hit_patterns.csv`
- Greek summary: `reports/wide_focus_exact_presence/greek_term_summary.csv`
- Greek markdown: `reports/wide_focus_exact_presence/greek_exact_presence.md`
- Protocol manifest: `reports/wide_focus_exact_presence/protocol_run.manifest.json`

## Scope

This is a capped exact-hit follow-up to the skip `2..250` wide focus count run.

- Skip range: `2..250`
- Direction: `both`
- Minimum normalized term length: `4`
- Max hits per term per corpus: `200`
- Hebrew corpora: MT_WLC, UXLC, MAM, EBIBLE_WLC, UHB
- Greek corpora: LXX, TR_NT, BYZ_NT, TCG_NT, SBLGNT
- Term files: `terms/modern_names_dates.csv`, `terms/prophetic_terms.csv`

The minimum length filter intentionally excludes 3-letter high-noise rows such
as Gog, Beast, United Nations acronym, and Greek/Hebrew USA acronym variants
unless the normalized spelling has length 4 or more.

## Hebrew Read

Pattern scope counts:

| Scope | Patterns |
| --- | ---: |
| present in every observed Hebrew source | 1,349 |
| present in all Leningrad-family streams | 558 |
| present in multiple Hebrew sources | 49 |
| source-specific | 707 |

Main Hebrew read:

- Many length 4+ forms have exact ref-key patterns stable across all five
  Hebrew streams. This mostly reflects shared MT-family consonantal density,
  not significance.
- Long phrases remain absent: United States, United States of America, United
  Nations, European Union, Cowboy Catering, Catering, Simscorner, Donald Trump,
  and Confederacy.
- `Simsberry` has exactly one exact row, and it is MAM-only.
- Short-to-medium transliterations such as Trump, Netanyahu, Germany, Turkey,
  Cowboy, Europe, Russia, Iran, Vance, France, NATO, Magog, and Dragon have
  exact rows, but they still need controls before interpretation.

Selected Hebrew examples:

| Term | Example skip | Example refs | Present | Read |
| --- | ---: | --- | --- | --- |
| `trump_h` `טראמפ` (Tramp; English: Trump) | 73 | Exod 23:30 / Exod 23:33 / Exod 24:3 | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | all observed Hebrew sources |
| `netanyahu_h` `נתניהו` (Netanyahu; English: Netanyahu) | 126 | 1Sam 13:22 / 1Sam 14:4 / 1Sam 14:10 | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | all observed Hebrew sources |
| `germany_h` `גרמניה` (Germanyah; English: Germany) | -25 | 1Kgs 7:12 / 1Kgs 7:10 / 1Kgs 7:9 | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | all observed Hebrew sources |
| `turkey_h` `טורקיה` (Turkiyah; English: Turkey) | 3 | Jer 42:6 / Jer 42:6 / Jer 42:6 | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | all observed Hebrew sources |
| `cowboy_h` `קאובוי` (kauboy; English: Cowboy) | 40 | 2Chr 24:16 / 2Chr 24:18 / 2Chr 24:19 | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | all observed Hebrew sources |
| `simsberry_h` `סימסברי` (Simsberry; English: Simsberry) | -109 | Jer 4:13 / Jer 4:7 / Jer 4:2 | MAM | source-specific only |

## Greek Read

Pattern scope counts:

| Scope | Patterns |
| --- | ---: |
| present in every observed Greek source | 0 |
| present in multiple Greek sources | 1,096 |
| source-specific | 2,214 |

The zero all-observed count is expected for this mixed Greek source set because
LXX and NT corpora do not share the same canonical reference space. Multi-source
rows mainly mean the same NT ref-key pattern appears across two or more Greek
NT streams.

Main Greek read:

- Full phrases remain absent: United States, United States of America, United
  Nations, European Union, Cowboy Catering, Catering, Simsberry, Simscorner,
  Germany, Netanyahu, and Confederacy.
- Multi-source Greek NT rows appear for shorter transliterations and biblical
  motifs such as Trump, Vance, Iran, Russia, China, NATO, Magog, Beast, Dragon,
  Europe, France, and Turkey.
- Those rows remain review queues only. They are not control-backed claims.

Selected Greek examples:

| Term | Example skip | Example refs | Present | Read |
| --- | ---: | --- | --- | --- |
| `trump_g` `τραμπ` (tramp; English: Trump) | 10 | 2Cor 1:9 / 2Cor 1:9 / 2Cor 1:9 | BYZ_NT, SBLGNT, TCG_NT, TR_NT | NT-family multi-source |
| `iran_g` `ιραν` (iran; English: Iran) | -4 | Luke 1:80 / Luke 1:80 / Luke 1:80 | BYZ_NT, SBLGNT, TCG_NT, TR_NT | NT-family multi-source |
| `russia_g` `ρωσια` (rosia; English: Russia) | -3 | 1Cor 15:18 / 1Cor 15:17 / 1Cor 15:17 | BYZ_NT, SBLGNT, TCG_NT, TR_NT | NT-family multi-source |
| `beast_g` `θηριον` (therion; English: beast) | -31 | Rom 12:21 / Rom 12:20 / Rom 12:19 | BYZ_NT, TCG_NT, TR_NT | NT-family multi-source |
| `dragon_g` `δρακων` (drakon; English: dragon) | -196 | 2Cor 11:16 / 2Cor 11:9 / 2Cor 11:4 | TCG_NT, TR_NT | NT-family multi-source |
| `turkey_g` `τουρκια` (tourkia; English: Turkey) | 77 | Acts 6:1 / Acts 6:3 / Acts 6:5 | BYZ_NT, TCG_NT | NT-family multi-source |

## Caution

This report is capped at 200 hits per term per corpus. It can establish absence
for terms with zero hits under the configured search, but for dense terms it
only gives representative exact-hit distribution. Statistical interpretation
still requires matched controls.

Representative matched controls for the nonzero wide-focus count rows are
tracked in `docs/WIDE_FOCUS_PAIRED_CONTROLS.md`.
