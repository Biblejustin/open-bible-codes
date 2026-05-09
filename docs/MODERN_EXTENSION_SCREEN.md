# Modern Extension Screen

This is the first capped run of same-skip extension checks for the modern
names, geopolitical terms, and local terms list.

Command:

```bash
python3 -m scripts.run_protocol protocols/modern_focus_extensions.toml --resume
```

Generated local reports:

- `reports/modern_extension_screen/surface_context_hits.csv`
- `reports/modern_extension_screen/surface_context_summary.csv`
- `reports/modern_extension_screen/extensions_*_top.csv`
- `reports/modern_extension_screen/protocol_run.manifest.json`

## Scope

- Term file: `terms/modern_names_dates.csv`
- Corpora: MT_WLC, UHB, LXX, TR_NT, SBLGNT
- Skip range: `2..100`
- Direction: both
- Minimum normalized term length: 4
- Hit cap: 25 hits per term per corpus
- Extension window: 12 letters before and 12 letters after on the same signed
  skip lane
- Phrase lexicon: surface words and surface phrases up to 4 words in the same
  corpus
- Runtime observed: 32.910s

## Hit Counts

| Corpus | Terms | Capped hits | Context hits | Zero-hit rows |
| --- | ---: | ---: | ---: | ---: |
| MT_WLC | 82 | 1,136 | 193 | 28 |
| UHB | 82 | 1,133 | 191 | 28 |
| LXX | 46 | 410 | 49 | 25 |
| TR_NT | 46 | 343 | 36 | 27 |
| SBLGNT | 46 | 338 | 29 | 28 |

## Top Phrase Extensions

The strict summary filter kept phrase-like extension rows only:
`--min-extension-length 3 --min-term-length 4 --match-kind-prefix phrase_`.

| Corpus | Base term | Skip | Extension type | Extended sequence | Surface phrase match | Read |
| --- | --- | ---: | --- | --- | --- | --- |
| UHB | `ישראל` | -2 | before_plus_term | `אישישראל` | `איש ישראל` | biblical Israel phrase |
| UHB | `ישראל` | -5 | term_plus_after | `ישראלוקח` | `ישראל וקח` | biblical Israel phrase |
| MT_WLC | `מצרימ` | 15 | before_plus_term | `והנמצרימ` | `והנם צרים` | surface phrase is not Egypt |
| MT_WLC | `ישראל` | -5 | term_plus_after | `ישראלוקח` | `ישראל וקח` | biblical Israel phrase |
| LXX | `ισραηλ` | 15 | term_plus_after | `ισραηλανα` | `Ισραηλ ανα` | biblical Israel phrase |
| SBLGNT | `χαρισ` | 10 | before_plus_term | `ιναηχαρισ` | `ινα η χαρις` | Harris transliteration collides with Greek grace |
| TR_NT | none | - | - | - | - | no filtered top rows |

## Read

This confirms the extension tool works for the user-requested question: it can
look before and after an ELS hit at the same interval and test those adjacent
letters against any surface word or short phrase in the same Hebrew or Greek
corpus.

The first modern-term screen did not strengthen the modern-name rows. The best
extension rows are explained by ordinary surface text:

- `Israel` is a biblical surface term, so phrase extensions around `ישראל` and
  `ισραηλ` are expected.
- `Egypt` / `מצרימ` can be matched by unrelated Hebrew surface wording after
  normalization and space removal.
- `Harris` / `χαρις` collides with ordinary Greek `χαρις` / grace.
- Local terms such as Cowboy Catering, Simsberry, and Simscorner had no
  meaningful phrase-extension row in this capped screen.

Current read: use extension rows as review queues only. They are valuable for
finding possible same-skip compounds, but they need surface-context review and
controls before any interpretation.
