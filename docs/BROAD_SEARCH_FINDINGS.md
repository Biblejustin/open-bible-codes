# Broad Search Findings

Source run:

- Protocol: `protocols/broad_search.toml`
- Command: `python3 -m scripts.run_protocol protocols/broad_search.toml --resume`
- Status: success
- Runtime observed: 20.650s through the protocol runner
- Generated summary: `reports/broad_search/broad_search_summary.csv`
- Generated top counts: `reports/broad_search/broad_search_top_counts.csv`
- Generated focus rows: `reports/broad_search/broad_search_focus.csv`
- Generated delta report: `reports/broad_search/broad_search_delta_vs_baseline.csv`
- Generated version-presence report: `reports/broad_search/broad_version_presence.csv`
- Generated markdown: `reports/broad_search/broad_search.md`
- Protocol manifest: `reports/broad_search/protocol_run.manifest.json`

## Scope

This is a broader screening run, not a replacement for the fixed public baseline.

- Skip range: `2..100`
- Direction: `both`
- Corpora: MT_WLC, UXLC, MAM, EBIBLE_WLC, UHB, LXX, TR_NT, BYZ_NT, TCG_NT, SBLGNT
- Term sets: 11 declared term lists
- Output rows: 5,375
- Baseline comparison: skip `2..50` rows from `reports/protocols/public_baseline`

Source note:

- `MT_WLC` now uses only direct OSHB word tokens. Apparatus notes, alternate
  accent readings, and qere readings nested in notes are excluded from the ELS
  stream.
- `UXLC` is included as a second Hebrew MT stream, defaulting to ketiv. Its
  normalized length is 1,197,043 letters vs. MT_WLC 1,197,042.
- `MAM` is included as a third Hebrew MT stream. It is a CC BY-SA
  Masorah-reader edition based chiefly on the Aleppo Codex tradition, with
  1,201,975 normalized letters across 23,202 parsed verses.
- `EBIBLE_WLC` is included as an eBible WLC packaging check. Standalone Hebrew
  paragraph markers are stripped before ELS normalization; the result has
  1,197,042 normalized letters across 23,213 verses.
- `UHB` is included as a derived MT-family comparison stream. USFM markers,
  word attributes, notes, crossrefs, and Hebrew paragraph markers are stripped
  before ELS normalization; the result has 1,195,624 normalized letters across
  23,145 parsed verses.

## Main Read

The wider skip range mostly scales up already-dense short terms.

Practical read:

- Most high-count rows are 3-4 letter terms.
- Full modern phrases remain weak or absent.
- Abbreviations dominate modern/geopolitical rows.
- Null controls and frequency anchors also produce high counts, so raw count size alone is not evidential.
- Moving from skip `2..50` to `2..100` roughly doubles many dense rows, which is expected because the search space roughly doubles.

## Top Length 4+ Rows

The length 4+ leaders still read as density effects, not claims.

| Rank | Set | Corpus | Term | Hits | Read |
| ---: | --- | --- | --- | ---: | --- |
| 1 | theological_terms | LXX | `temple_g` `ναοσ` | 35,302 | dense short form |
| 2 | modern_names_dates | LXX | `nato_g` `νατο` | 31,674 | dense short form |
| 3 | theological_terms | LXX | `son_g` `υιοσ` | 25,745 | dense short form |
| 4 | null_controls | MAM | `scrambled_yhwh_h` `וההי` | 22,293 | dense short control form |
| 5 | null_controls | MT_WLC | `scrambled_yhwh_h` `וההי` | 22,277 | dense short control form |
| 6 | null_controls | EBIBLE_WLC | `scrambled_yhwh_h` `וההי` | 22,271 | dense short control form |
| 7 | null_controls | UXLC | `scrambled_yhwh_h` `וההי` | 22,269 | dense short control form |
| 8 | null_controls | UHB | `scrambled_yhwh_h` `וההי` | 22,204 | dense short control form |
| 9 | greek_nt_claim_terms | LXX | `haima_gnt` `αιμα` | 22,054 | dense short form |
| 12 | hebrew_claim_terms | MAM | `yhwh_h` `יהוה` | 21,812 | dense short form |
| 15 | hebrew_claim_terms | UHB | `yhwh_h` `יהוה` | 21,640 | dense short form |
| 17 | hebrew_claim_terms | MT_WLC | `yhwh_h` `יהוה` | 21,626 | dense short form |
| 19 | hebrew_claim_terms | UXLC | `yhwh_h` `יהוה` | 21,622 | dense short form |
| 21 | hebrew_claim_terms | EBIBLE_WLC | `yhwh_h` `יהוה` | 21,620 | dense short form |

The null-control leader is important: a scrambled YHWH control lands in the same broad count band as real 4-letter theological terms. That reinforces the need for controls before interpretation.

## Focus Terms

Selected user-requested terms from the broad run:

| Concept | Corpus | Term | Hits | Read |
| --- | --- | --- | ---: | --- |
| United Nations acronym | LXX | `οηε` | 191,280 | high-noise short form |
| United Nations acronym | MAM | `אומ` | 166,493 | high-noise short form |
| United Nations acronym | UXLC | `אומ` | 165,766 | high-noise short form |
| United Nations acronym | MT_WLC | `אומ` | 165,765 | high-noise short form |
| United Nations acronym | EBIBLE_WLC | `אומ` | 165,755 | high-noise short form |
| United Nations acronym | UHB | `אומ` | 165,694 | high-noise short form |
| USA abbreviation | LXX | `ηπα` | 85,735 | high-noise short form |
| Beast | MAM | `חיה` | 51,404 | high-noise short form |
| Beast | MT_WLC | `חיה` | 51,305 | high-noise short form |
| Beast | EBIBLE_WLC | `חיה` | 51,302 | high-noise short form |
| Beast | UXLC | `חיה` | 51,295 | high-noise short form |
| Beast | UHB | `חיה` | 51,252 | high-noise short form |
| United Nations acronym | TR_NT | `οηε` | 51,733 | high-noise short form |
| United Nations acronym | TCG_NT | `οηε` | 51,660 | high-noise short form |
| United Nations acronym | BYZ_NT | `οηε` | 51,298 | high-noise short form |
| United Nations acronym | SBLGNT | `οηε` | 50,442 | high-noise short form |
| USA abbreviation | TR_NT | `ηπα` | 19,220 | high-noise short form |
| USA abbreviation | TCG_NT | `ηπα` | 18,955 | high-noise short form |
| USA abbreviation | BYZ_NT | `ηπα` | 18,720 | high-noise short form |
| USA abbreviation | SBLGNT | `ηπα` | 18,649 | high-noise short form |
| Iran | LXX | `ιραν` | 17,335 | dense short form |
| USA abbreviation | UHB | `ארהב` | 5,044 | dense short form |
| USA abbreviation | EBIBLE_WLC | `ארהב` | 5,035 | dense short form |
| USA abbreviation | MT_WLC | `ארהב` | 5,029 | dense short form |
| USA abbreviation | UXLC | `ארהב` | 5,028 | dense short form |
| USA abbreviation | MAM | `ארהב` | 4,984 | dense short form |
| Iran | BYZ_NT | `ιραν` | 4,048 | dense short form |
| Iran | SBLGNT | `ιραν` | 3,958 | dense short form |
| Iran | TR_NT | `ιραν` | 3,892 | dense short form |
| Iran | TCG_NT | `ιραν` | 3,847 | dense short form |
| Vance | LXX | `βανσ` | 3,156 | dense short form |
| Dragon | MAM | `תנינ` | 3,107 | dense short form |
| Dragon | MT_WLC | `תנינ` | 3,055 | dense short form |
| Dragon | EBIBLE_WLC | `תנינ` | 3,054 | dense short form |
| Dragon | UXLC | `תנינ` | 3,053 | dense short form |
| Gog | EBIBLE_WLC | `גוג` | 2,482 | high-noise short form |
| Gog | MT_WLC | `גוג` | 2,480 | high-noise short form |
| Gog | UXLC | `גוג` | 2,480 | high-noise short form |
| Gog | MAM | `גוג` | 2,460 | high-noise short form |
| Gog | TR_NT | `γωγ` | 1,244 | high-noise short form |
| Gog | TCG_NT | `γωγ` | 1,212 | high-noise short form |
| Gog | SBLGNT | `γωγ` | 1,178 | high-noise short form |
| Gog | BYZ_NT | `γωγ` | 1,166 | high-noise short form |
| Russia | LXX | `ρωσια` | 534 | present; screen only |
| Vance | SBLGNT | `βανσ` | 512 | present; screen only |
| Vance | BYZ_NT | `βανσ` | 501 | present; screen only |
| Vance | TR_NT | `βανσ` | 485 | present; screen only |
| Vance | TCG_NT | `βανσ` | 473 | present; screen only |
| Iran | UHB | `איראנ` | 477 | present; screen only |
| Iran | UXLC | `איראנ` | 473 | present; screen only |
| Iran | MT_WLC | `איראנ` | 472 | present; screen only |
| Magog | MAM | `מגוג` | 201 | present; screen only |
| Magog | MT_WLC | `מגוג` | 185 | present; screen only |
| Magog | UXLC | `מגוג` | 185 | present; screen only |
| Trump | LXX | `τραμπ` | 162 | present; screen only |
| Russia | TR_NT | `ρωσια` | 121 | present; screen only |
| Russia | SBLGNT | `ρωσια` | 111 | present; screen only |
| Russia | MT_WLC | `רוסיה` | 91 | present; screen only |
| Russia | UXLC | `רוסיה` | 91 | present; screen only |
| Russia | TCG_NT | `ρωσια` | 105 | present; screen only |
| Russia | BYZ_NT | `ρωσια` | 100 | present; screen only |
| Trump | BYZ_NT | `τραμπ` | 41 | present; screen only |
| Trump | TCG_NT | `τραμπ` | 38 | present; screen only |
| Trump | TR_NT | `τραμπ` | 38 | present; screen only |
| Trump | SBLGNT | `τραμπ` | 26 | present; screen only |
| Turkey | MAM/UHB/EBIBLE_WLC/MT_WLC/UXLC | `תורכיה` | 33 / 32 / 30 / 29 / 29 | present; screen only |
| Netanyahu | EBIBLE_WLC/MT_WLC/UXLC/MAM/UHB | `נתניהו` | 27 / 27 / 27 / 25 / 25 | present; screen only |
| Europe | EBIBLE_WLC/MT_WLC/UXLC/UHB/MAM | `אירופה` | 22 / 22 / 22 / 20 / 19 | present; screen only |
| Cowboy | MAM/EBIBLE_WLC/MT_WLC/UXLC/UHB | `קאובוי` | 15 / 12 / 12 / 12 / 11 | present; screen only |
| Germany | EBIBLE_WLC/MT_WLC/UHB/UXLC/MAM | `גרמניה` | 8 / 8 / 8 / 8 / 6 | low count |
| Trump | MAM/EBIBLE_WLC/MT_WLC/UHB/UXLC | `טראמפ` | 7 / 6 / 6 / 6 / 6 | low count |
| Donald Trump | MAM/EBIBLE_WLC/MT_WLC/UHB/UXLC | `דונלדטראמפ` | 0 | absent |
| European Union | MAM/EBIBLE_WLC/MT_WLC/UHB/UXLC/LXX/TR_NT/BYZ_NT/TCG_NT/SBLGNT | full phrase forms | 0 | absent |
| Cowboy Catering | MAM/EBIBLE_WLC/MT_WLC/UHB/UXLC/LXX/TR_NT/BYZ_NT/TCG_NT/SBLGNT | full phrase forms | 0 | absent |
| Catering | all corpora | transliterated forms | 0 | absent |
| Simsberry / Simscorner | all corpora | transliterated forms | 0 | absent |

## Version Presence

The broad run now also emits:

- `reports/broad_search/broad_version_presence.csv`
- `reports/broad_search/broad_version_presence.md`

This groups raw broad-count rows by term and records which observed corpora have
at least one hit.

Presence summary:

| Scope | Terms |
| --- | ---: |
| present in every observed source | 700 |
| present in multiple observed sources | 43 |
| source-specific | 33 |
| absent in every observed source | 299 |

Selected reads from the version-presence report:

| Term | Present | Absent | Read |
| --- | --- | --- | --- |
| Greek United Nations acronym `οηε` | BYZ_NT, LXX, SBLGNT, TCG_NT, TR_NT | none | high-noise short form |
| Hebrew United Nations acronym `אומ` | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | none | high-noise short form |
| Greek USA abbreviation `ηπα` | BYZ_NT, LXX, SBLGNT, TCG_NT, TR_NT | none | high-noise short form |
| Greek Iran `ιραν` | BYZ_NT, LXX, SBLGNT, TCG_NT, TR_NT | none | dense short form |
| Greek Trump `τραμπ` | BYZ_NT, LXX, SBLGNT, TCG_NT, TR_NT | none | present in every compatible corpus |
| Hebrew Trump `טראמפ` | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | none | present in every compatible corpus |
| Hebrew Netanyahu `נתניהו` | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | none | present in every compatible corpus |
| Greek Beast `θηριον` | BYZ_NT, LXX, TCG_NT, TR_NT | SBLGNT | present in multiple observed corpora |
| Greek Europe `ευρωπη` | BYZ_NT, LXX, SBLGNT | TCG_NT, TR_NT | present in multiple observed corpora |
| Greek United Nations full phrase `ηνωμεναεθνη` | none | BYZ_NT, LXX, SBLGNT, TCG_NT, TR_NT | absent |
| Hebrew United Nations full phrase `האומותהמאוחדות` | none | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | absent |
| Greek United States full phrase `ηνωμενεσπολιτειεσ` | none | BYZ_NT, LXX, SBLGNT, TCG_NT, TR_NT | absent |
| Hebrew United States full phrase `ארצותהברית` | none | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | absent |
| Greek European Union `ευρωπαικηενωση` | none | BYZ_NT, LXX, SBLGNT, TCG_NT, TR_NT | absent |
| Cowboy Catering forms | none | observed Hebrew/Greek corpora | absent |
| Simsberry / Simscorner forms | none | observed Hebrew/Greek corpora | absent |

This is still raw count presence, not a control result. Its value is that it
keeps the source distribution visible instead of collapsing the broad run into
one hit count per term.

## Skip Range Effect

The largest increases from skip `2..50` to `2..100` mostly doubled.

Examples:

| Term | 2..50 | 2..100 | Ratio |
| --- | ---: | ---: | ---: |
| LXX `eve_g` `ευα` | 185,778 | 378,085 | 2.035 |
| LXX United Nations acronym `οηε` | 95,280 | 191,280 | 2.008 |
| MT_WLC United Nations acronym `אומ` | 81,373 | 165,765 | 2.037 |
| MT_WLC `greece_h` / `javan_h` `יונ` | 68,556 | 136,081 | 1.985 |
| LXX USA abbreviation `ηπα` | 42,727 | 85,735 | 2.007 |

This is expected behavior. It means a wider skip range raises the raw count ceiling without making the strongest rows more meaningful by itself.

## Verdict

The broader run is useful for queue-building, but it does not change the main conclusion:

- raw ELS counts are abundant;
- short terms dominate;
- broader skip ranges inflate counts predictably;
- full modern phrases remain mostly absent;
- any serious claim needs matched controls, surface/context review, and predeclared thresholds.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/broad_search.toml --resume
```
