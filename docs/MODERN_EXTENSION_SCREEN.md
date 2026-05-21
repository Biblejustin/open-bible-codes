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
- Runtime observed: 38.262s

## Hit Counts

| Corpus | Terms | Capped hits | Context hits | Zero-hit rows |
| --- | ---: | ---: | ---: | ---: |
| MT_WLC | 96 | 1,153 | 193 | 41 |
| UHB | 96 | 1,149 | 191 | 41 |
| LXX | 60 | 410 | 49 | 39 |
| TR_NT | 60 | 343 | 36 | 41 |
| SBLGNT | 60 | 338 | 29 | 42 |

## Top Phrase Extensions

The strict summary filter kept phrase-like extension rows only:
`--min-extension-length 3 --min-term-length 4 --match-kind-prefix phrase_`.

| Corpus | Base term | Skip | Extension type | Extended sequence | Surface phrase match | Read |
| --- | --- | ---: | --- | --- | --- | --- |
| UHB | `ישראל` (Yisrael; English: Israel) | -2 | before_plus_term | `אישישראל` (ish Yisrael; English: man of Israel) | `איש ישראל` (ish Yisrael; English: man of Israel) | biblical Israel phrase |
| UHB | `ישראל` (Yisrael; English: Israel) | -5 | term_plus_after | `ישראלוקח` (Yisrael u-qach; English: Israel and take) | `ישראל וקח` (Yisrael u-qach; English: Israel and take) | biblical Israel phrase |
| MT_WLC | `מצרימ` (Mitzrayim; English: Egypt/Egyptians) | 15 | before_plus_term | `והנמצרימ` (ve-hen metzarim; English: and behold, distressing/enemies) | `והנם צרים` (ve-hinnam tzarim; English: and behold, enemies) | surface phrase is not Egypt |
| MT_WLC | `ישראל` (Yisrael; English: Israel) | -5 | term_plus_after | `ישראלוקח` (Yisrael u-qach; English: Israel and take) | `ישראל וקח` (Yisrael u-qach; English: Israel and take) | biblical Israel phrase |
| LXX | `ισραηλ` (Israel; English: Israel) | 15 | term_plus_after | `ισραηλανα` (Israel ana; English: Israel up/again) | `Ισραηλ ανα` (Israel ana; English: Israel up/again) | biblical Israel phrase |
| SBLGNT | `χαρισ` (charis; English: grace) | 10 | before_plus_term | `ιναηχαρισ` (hina he charis; English: so that the grace) | `ινα η χαρις` (hina he charis; English: so that the grace) | Harris transliteration collides with Greek grace |
| TR_NT | none | - | - | - | - | no filtered top rows |

Phrase-summary rows after the strict filter:

| Corpus | Phrase rows | Strict top rows | Plus-term top rows |
| --- | ---: | ---: | ---: |
| MT_WLC | 51 | 2 | 2 |
| UHB | 24 | 2 | 2 |
| LXX | 35 | 1 | 1 |
| TR_NT | 24 | 0 | 0 |
| SBLGNT | 27 | 1 | 1 |

## Read

This confirms the extension tool works for the user-requested question: it can
look before and after an ELS hit at the same interval and test those adjacent
letters against any surface word or short phrase in the same Hebrew or Greek
corpus.

The first modern-term screen did not strengthen the modern-name rows. The best
extension rows are explained by ordinary surface text:

- `Israel` is a biblical surface term, so phrase extensions around `ישראל` (Yisrael; English: Israel) and
  `ισραηλ` (Israel; English: Israel) are expected.
- `Egypt` / `מצרימ` (Mitzrayim; English: Egypt/Egyptians) can be matched by unrelated Hebrew surface wording after
  normalization and space removal.
- `Harris` / `χαρις` (charis; English: grace) collides with ordinary Greek `χαρις` (charis; English: grace).
- Local terms such as Cowboy Catering, Simsberry, and Simscorner had no
  meaningful phrase-extension row in this capped screen.

Current read: use extension rows as review queues only. They are valuable for
finding possible same-skip compounds, but they need surface-context review and
controls before any interpretation.
