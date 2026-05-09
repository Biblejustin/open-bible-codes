# Targeted Terms Findings

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `targeted_terms_report`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only targeted_terms_report`
- Generated summary: `reports/targeted_terms_summary.csv`
- Generated examples: `reports/targeted_terms_examples.csv`
- Generated markdown: `reports/targeted_terms.md`
- Generated manifest: `reports/targeted_terms.manifest.json`
- Output size: 41 summary rows; 26 example rows

This tracked document summarizes the generated report so the current read is visible in git. The generated `reports/` files remain local run artifacts.

## Scope

Focused targets:

- Iran
- Trump
- Vance
- Netanyahu
- Gog
- Magog
- Russia
- Europe
- Turkey
- Germany

The report joins raw ELS counts, shuffled-letter and shuffled-term controls, NT surface-context rows, and filtered NT extension-top rows. It is a screening artifact, not a significance claim.

## Main Read

No targeted concept currently has a robust control-backed signal.

Practical read:

- Short Greek forms dominate raw counts.
- Surface-context rows exist for some NT Greek hits, but mostly track short-form density.
- No focused target produced a filtered NT extension-top row.
- Europe Hebrew is the only focused row with a low uncorrected p-value, but it remains an uncorrected screening result with weak-control flags.
- Gog and Magog should be reviewed as a pair/proximity question, not by raw counts.

## Concept Summary

| Concept | Best raw count | Best control band | Surface context rows | Extension top rows | Read |
| --- | ---: | --- | ---: | ---: | --- |
| Iran | LXX `iran_g` 8,375 | `not_unusual` | 508 | 0 | Greek form is short; high count is expected noise candidate |
| Trump | LXX `trump_g` 71 | `not_unusual` | 2 | 0 | present, low/modest; controls first |
| Vance | LXX `vance_g` 1,532 | `not_unusual` | 13 | 0 | high because short Greek form |
| Netanyahu | MT_WLC `netanyahu_h` 8 | `not_unusual` | 0 | 0 | Hebrew only, low |
| Gog | LXX `gog_g` 1,800 | `not_unusual` | 124 | 0 | very short form; use pair/proximity review |
| Magog | MT_WLC `magog_h` 104 | `not_unusual` | 0 | 0 | present; better reviewed with Gog proximity |
| Russia | LXX `russia_g` 268 | `not_unusual` | 16 | 0 | present, no robust signal |
| Europe | MT_WLC `europe_h` 17 | `not_unusual`, `uncorrected_p_le_0.05` | 0 | 0 | uncorrected screen only |
| Turkey | MT_WLC `turkey_alt_h` 14 | `not_unusual` | 0 | 0 | low |
| Germany | MT_WLC `germany_h` 2 | `not_unusual` | 0 | 0 | near absent |

## Term Details

### Iran

| Corpus | Term ID | Term | Hits | Control | Surface | Read |
| --- | --- | --- | ---: | --- | ---: | --- |
| LXX | `iran_g` | `ιραν` | 8,375 | `not_unusual` | 0 | high count, likely short-form density |
| TR_NT | `iran_g` | `ιραν` | 1,876 | `not_unusual` | 250 | high count, likely short-form density |
| SBLGNT | `iran_g` | `ιραν` | 1,983 | `not_unusual` | 258 | high count, likely short-form density |
| MT_WLC | `iran_h` | `איראן` | 210 | `not_unusual` | 0 | counted, not unusual |

### Trump, Vance, Netanyahu

| Concept | Corpus | Term ID | Term | Hits | Control | Surface | Read |
| --- | --- | --- | --- | ---: | --- | ---: | --- |
| Trump | MT_WLC | `trump_h` | `טראמפ` | 4 | `not_unusual` | 0 | low |
| Trump | LXX | `trump_g` | `τραμπ` | 71 | `not_unusual` | 0 | modest |
| Trump | TR_NT | `trump_g` | `τραμπ` | 18 | `not_unusual` | 1 | has NT surface context |
| Trump | SBLGNT | `trump_g` | `τραμπ` | 12 | `not_unusual` | 1 | has NT surface context |
| Vance | MT_WLC | `vance_h` | `ואנס` | 331 | `not_unusual` | 0 | counted, not unusual |
| Vance | LXX | `vance_g` | `βανς` | 1,532 | `not_unusual` | 0 | high, likely short-form density |
| Vance | TR_NT | `vance_g` | `βανς` | 241 | `not_unusual` | 5 | has NT surface context |
| Vance | SBLGNT | `vance_g` | `βανς` | 259 | `not_unusual` | 8 | has NT surface context |
| Netanyahu | MT_WLC | `netanyahu_h` | `נתניהו` | 8 | `not_unusual` | 0 | counted, not unusual |
| Netanyahu | LXX/TR_NT/SBLGNT | `netanyahu_g` | `νετανιαχου` | 0 | `not_unusual` | 0 | absent |

### Gog And Magog

| Concept | Corpus | Term ID | Term | Hits | Control | Surface | Read |
| --- | --- | --- | --- | ---: | --- | ---: | --- |
| Gog | MT_WLC | `gog_h` | `גוג` | 1,364 | `not_unusual` | 0 | very short form |
| Gog | LXX | `gog_g` | `γωγ` | 1,800 | `not_unusual` | 0 | very short form |
| Gog | TR_NT | `gog_g` | `γωγ` | 594 | `not_unusual` | 62 | has NT surface context |
| Gog | SBLGNT | `gog_g` | `γωγ` | 572 | `not_unusual` | 62 | has NT surface context |
| Magog | MT_WLC | `magog_h` | `מגוג` | 104 | `not_unusual` | 0 | counted, not unusual |
| Magog | LXX | `magog_g` | `μαγωγ` | 9 | `not_unusual` | 0 | counted, not unusual |
| Magog | TR_NT | `magog_g` | `μαγωγ` | 3 | `not_unusual` | 0 | counted, not unusual |
| Magog | SBLGNT | `magog_g` | `μαγωγ` | 3 | `not_unusual` | 0 | counted, not unusual |

Read: `Gog` is too short for raw count claims. `Magog` is less dense. The next useful test is same-passage, same-span, or same-skip proximity between the pair with paired controls.

### Russia, Europe, Turkey, Germany

| Concept | Corpus | Term ID | Term | Hits | Control | Surface | Read |
| --- | --- | --- | --- | ---: | --- | ---: | --- |
| Russia | MT_WLC | `russia_h` | `רוסיה` | 50 | `not_unusual` | 0 | present |
| Russia | LXX | `russia_g` | `Ρωσία` | 268 | `not_unusual` | 0 | present |
| Russia | TR_NT | `russia_g` | `Ρωσία` | 52 | `not_unusual` | 7 | has NT surface context |
| Russia | SBLGNT | `russia_g` | `Ρωσία` | 57 | `not_unusual` | 9 | has NT surface context |
| Europe | MT_WLC | `europe_h` | `אירופה` | 17 | `uncorrected_p_le_0.05` | 0 | uncorrected only |
| Europe | LXX | `europe_g` | `Ευρώπη` | 1 | `not_unusual` | 0 | low |
| Europe | TR_NT | `europe_g` | `Ευρώπη` | 0 | `not_unusual` | 0 | absent |
| Europe | SBLGNT | `europe_g` | `Ευρώπη` | 1 | `not_unusual` | 0 | low |
| Turkey | MT_WLC | `turkey_alt_h` | `תורכיה` | 14 | `not_unusual` | 0 | low |
| Turkey | MT_WLC | `turkey_h` | `טורקיה` | 1 | `not_unusual` | 0 | near absent |
| Turkey | LXX/TR_NT/SBLGNT | `turkey_g` | `Τουρκία` | 0/1/0 | `not_unusual` | 0 | near absent |
| Germany | MT_WLC | `germany_h` | `גרמניה` | 2 | `not_unusual` | 0 | near absent |
| Germany | LXX/TR_NT/SBLGNT | `germany_g` | `Γερμανία` | 0 | `not_unusual` | 0 | absent |

## Example Rows

The generated examples file has 26 rows:

- Iran: exact-center NT Greek examples exist, but the term is short.
- Trump: two same-category center examples.
- Vance: several same-category examples.
- Gog: exact-center examples in TR_NT and SBLGNT.
- Russia: same-category examples.
- Magog, Netanyahu, Europe, Turkey, Germany: no focused example rows in the generated targeted report.

No focused target had a filtered extension-top row.

## Controls Verdict

Current controls do not support an external claim:

- `not_unusual` dominates focused rows.
- Europe Hebrew has `uncorrected_p_le_0.05`, but this is not adjusted enough to matter by itself.
- Existing low-p rows in the broader baseline carry flags such as `few_letter_controls`, `few_term_controls`, `huge_search_space`, and `uncorrected_only`.

The follow-up paired-control run is tracked in `docs/TARGETED_PAIRED_CONTROLS.md`.
It found 40 of 41 focused rows `not_unusual`; only `MT_WLC europe_h` crossed
the uncorrected screen, and its adjusted focused-row q-value is `1.0`.

The Gog/Magog pair/proximity follow-up is tracked in
`docs/GOG_MAGOG_PAIR_CONTROLS.md`. It produced an exploratory q <= 0.10 screen,
not a claim.

Next meaningful move:

- strengthen Gog/Magog with same-chapter and same-skip controls
- Europe Hebrew rerun with more controls and adjusted reporting

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only targeted_terms_report
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
