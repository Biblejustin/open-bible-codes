# Wide Focus Paired Controls

Source run:

- Protocol: `protocols/wide_focus_paired_controls.toml`
- Command: `python3 -m scripts.run_protocol protocols/wide_focus_paired_controls.toml --resume`
- Status: success
- Runtime observed: 32.089s
- Generated summary: `reports/wide_focus_paired_controls_summary.csv`
- Generated examples: `reports/wide_focus_paired_controls_examples.csv`
- Generated markdown: `reports/wide_focus_paired_controls.md`
- Generated manifest: `reports/wide_focus_paired_controls.manifest.json`

## Scope

This controls nonzero rows from `reports/wide_focus_search/wide_focus_focus.csv`
in representative corpora:

- Hebrew: MT_WLC, UHB
- Greek: LXX, TR_NT, SBLGNT

Settings:

- Skip range: `2..250`
- Direction: `both`
- Term-shuffle controls: 100 per row
- Same-length corpus-letter random controls: 100 per row
- Rows controlled: 66

## Main Read

No wide-focus row has adjusted paired-control support.

Band counts:

| Band | Rows |
| --- | ---: |
| `not_unusual` | 63 |
| `paired_uncorrected_p_le_0.05` | 3 |

The three uncorrected-only rows were:

| Concept | Corpus | Term | Hits | Combined p | Combined q | Read |
| --- | --- | --- | ---: | ---: | ---: | --- |
| Trump | TR_NT | `trump_g` | 113 | 0.019802 | 0.780529 | uncorrected only |
| Trump | LXX | `trump_g` | 380 | 0.029703 | 0.780529 | uncorrected only |
| Turkey | UHB | `turkey_h` | 6 | 0.039604 | 0.780529 | uncorrected only |

Because the corrected q-values are high, these rows are not claim-ready.

## Concept Read

| Concept | Best representative row | Best band | Read |
| --- | --- | --- | --- |
| Iran | TR_NT `iran_g` hits=10,002 | `not_unusual` | short-form density remains likely |
| Trump | TR_NT `trump_g` hits=113 | `paired_uncorrected_p_le_0.05` | uncorrected only |
| Vance | SBLGNT `vance_g` hits=1,268 | `not_unusual` | short-form density remains likely |
| Netanyahu | UHB `netanyahu_h` hits=68 | `not_unusual` | not unusual |
| Gog | LXX `gog_g` hits=8,656 | `not_unusual` | short-form density remains likely |
| Magog | LXX `magog_g` hits=33 | `not_unusual` | not unusual |
| Russia | TR_NT `russia_g` hits=333 | `not_unusual` | not unusual |
| Europe | SBLGNT `europe_g` hits=5 | `not_unusual` | not unusual |
| Turkey | UHB `turkey_h` hits=6 | `paired_uncorrected_p_le_0.05` | uncorrected only |
| Germany | UHB `germany_h` hits=15 | `not_unusual` | not unusual |
| USA | UHB `usa_abbrev_h` hits=12,627 | `not_unusual` | short-form density remains likely |
| United Nations | MT_WLC `united_nations_acronym_h` hits=421,133 | `not_unusual` | short-form density remains likely |
| Dragon | TR_NT `dragon_g` hits=3 | `not_unusual` | not unusual |
| Cowboy | UHB `cowboy_h` hits=43 | `not_unusual` | not unusual |
| Beast | LXX `beast_g` hits=22 | `not_unusual` | not unusual |

## Caution

This is a representative paired-control screen, not a full all-corpus control
suite. It is enough to explain the broad modern/local/geopolitical rows as
ordinary under matched controls, but any future public claim still needs its
own pre-registered control protocol.
