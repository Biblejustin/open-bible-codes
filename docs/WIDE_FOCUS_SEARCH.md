# Wide Focus Search

Source run:

- Protocol: `protocols/wide_focus_search.toml`
- Command: `python3 -m scripts.run_protocol protocols/wide_focus_search.toml --resume`
- Status: success
- Count-step runtime observed: 40.327s
- Generated summary: `reports/wide_focus_search/wide_focus_summary.csv`
- Generated top counts: `reports/wide_focus_search/wide_focus_top_counts.csv`
- Generated focus rows: `reports/wide_focus_search/wide_focus_focus.csv`
- Generated delta report: `reports/wide_focus_search/wide_focus_delta_vs_baseline.csv`
- Generated version-presence report: `reports/wide_focus_search/wide_focus_version_presence.csv`
- Generated markdown: `reports/wide_focus_search/wide_focus.md`
- Generated version-presence markdown: `reports/wide_focus_search/wide_focus_version_presence.md`
- Protocol manifest: `reports/wide_focus_search/protocol_run.manifest.json`

## Scope

This is a focused wide-skip screening run, not a control-backed claim report.

- Skip range: `2..250`
- Direction: `both`
- Corpora: MT_WLC, UXLC, MAM, EBIBLE_WLC, UHB, LXX, TR_NT, BYZ_NT, TCG_NT, SBLGNT
- Term sets: `modern_names_dates`, `prophetic_terms`
- Output rows: 2,365
- Baseline comparison: skip `2..50` rows from `reports/protocols/public_baseline`

## Main Read

Widening the focused search to skip `2..250` did not change the broader
conclusion.

- Short forms and abbreviations dominate.
- Count increases versus skip `2..50` are mostly about 5x, which is expected
  from the wider search space.
- Full modern geopolitical phrases remain absent.
- Local phrases remain absent.
- Source-specific one-off rows should be treated as review noise unless they
  survive controls and exact-hit review.

## Top Length 4+ Rows

The length 4+ leaders are still dense short forms:

| Rank | Set | Corpus | Term | Hits | Read |
| ---: | --- | --- | --- | ---: | --- |
| 1 | modern_names_dates | LXX | `nato_g` `νατο` | 80,308 | dense short form |
| 2 | prophetic_terms | LXX | `blood_g` `αιμα` | 55,267 | dense short form |
| 3 | modern_names_dates | LXX | `china_g` `κινα` | 55,120 | dense short form |
| 4 | modern_names_dates | LXX | `iran_g` `ιραν` | 43,838 | dense short form |
| 5 | prophetic_terms | MAM | `rome_h` `רומי` | 35,090 | dense short form |
| 6 | prophetic_terms | UXLC | `rome_h` `רומי` | 35,006 | dense short form |
| 7 | prophetic_terms | EBIBLE_WLC | `rome_h` `רומי` | 35,005 | dense short form |
| 8 | prophetic_terms | MT_WLC | `rome_h` `רומי` | 35,004 | dense short form |
| 9 | prophetic_terms | UHB | `rome_h` `רומי` | 34,949 | dense short form |

## Focus Terms

Selected user-requested rows from the wide run:

| Concept | Result | Read |
| --- | --- | --- |
| United States full phrase | 0 in observed Hebrew and Greek corpora | absent at this range |
| United States of America full phrase | 0 in observed Hebrew and Greek corpora | absent at this range |
| United Nations full phrase | 0 in observed Hebrew and Greek corpora | absent at this range |
| United Nations acronym | Hebrew totals around 421k per MT-family corpus; Greek LXX 478,782 and NT streams around 127k-131k | high-noise short form |
| European Union full phrase | 0 in observed Hebrew and Greek corpora | absent at this range |
| Cowboy Catering | 0 in observed Hebrew and Greek corpora | absent at this range |
| Catering | 0 in observed Hebrew and Greek corpora | absent at this range |
| Cowboy | Hebrew MT-family 36-49; Greek 0 | present but low, Hebrew only |
| Simsberry | Hebrew MAM 1; all other observed Hebrew and Greek corpora 0 | source-specific one-off |
| Simscorner | 0 in observed Hebrew and Greek corpora | absent at this range |
| Trump | Hebrew MT-family 11-13; Greek NT streams 91-113; LXX 380 | present, low/modest |
| Vance | Hebrew MT-family 1,437-1,461; Greek NT streams 1,229-1,268; LXX 7,841 | dense short form |
| Netanyahu | Hebrew MT-family 60-71; Greek 0 | Hebrew-only at this range |
| Iran | Hebrew MT-family 1,162-1,181; Greek NT streams 9,860-10,405; LXX 43,838 | dense short form |
| Russia | Hebrew MT-family 194-220; Greek NT streams 285-333; LXX 1,499 | present, screen only |
| Europe | Hebrew MT-family 36-43; Greek 1-7 | present but sparse |
| Germany | Hebrew MT-family 9-15; Greek 0 | Hebrew-only and low |
| Turkey | Hebrew alternate form 75-80; regular Hebrew 2-6; Greek 0-13 | spelling-sensitive and sparse |
| Gog | Hebrew MT-family 5,798-5,876; Greek NT streams 2,870-2,940; LXX 8,656 | high-noise short form |
| Magog | Hebrew MT-family 438-478; Greek 5-33 | present, screen only |
| Beast | Hebrew MT-family around 130k; Greek 1-22 | Hebrew short-form density |
| Dragon | Hebrew MT-family 7,835-7,869; Greek 0-10 | Hebrew short-form density |

## Skip Range Effect

Largest increases versus skip `2..50` scale roughly with the wider range:

| Term | 2..50 | 2..250 | Ratio |
| --- | ---: | ---: | ---: |
| LXX United Nations acronym `οηε` | 95,280 | 478,782 | 5.025 |
| MT_WLC United Nations acronym `אומ` | 81,340 | 421,133 | 5.177 |
| MT_WLC `greece_h` `יונ` | 67,460 | 341,633 | 5.064 |
| LXX `ur_g` `ουρ` | 57,970 | 294,528 | 5.081 |
| MT_WLC `ur_h` `אור` | 57,065 | 290,922 | 5.098 |
| LXX USA abbreviation `ηπα` | 42,727 | 216,290 | 5.062 |
| LXX `nato_g` `νατο` | 15,410 | 80,308 | 5.211 |

## Version Presence

The wide run also emits a term-level version-presence report:

- `reports/wide_focus_search/wide_focus_version_presence.csv`
- `reports/wide_focus_search/wide_focus_version_presence.md`

Presence summary:

| Scope | Terms |
| --- | ---: |
| present in every observed source | 290 |
| present in multiple observed sources | 23 |
| source-specific | 19 |
| absent in every observed source | 141 |

Important read: exact source distribution matters, but broad count presence is
not significance. The same run produces all-source stability for many short,
high-density forms and absence for most longer modern/local phrases.

## Exact-Hit Follow-Up

A capped exact-hit follow-up is tracked separately:

- Protocol: `protocols/wide_focus_exact_presence.toml`
- Summary: `docs/WIDE_FOCUS_EXACT_PRESENCE.md`

This follow-up exports representative exact ref-key patterns for length 4+
focused terms. It confirms the same practical read: long phrases remain absent,
the single `Simsberry` row is MAM-only, and Greek multi-source rows are mostly
NT-family review queues rather than all-source claims.

Representative paired controls are tracked in
`docs/WIDE_FOCUS_PAIRED_CONTROLS.md`. That control run found no adjusted
paired-control support for the nonzero wide-focus rows.

## Caution

This run is useful for queue-building and source-distribution review. It does
not replace paired controls, exact-hit review, or pre-registered claim tests.
