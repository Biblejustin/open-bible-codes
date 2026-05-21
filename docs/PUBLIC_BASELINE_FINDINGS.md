# Public Baseline Findings

Run:

- Protocol: `protocols/public_baseline.toml`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume`
- Status: success
- Wall time: 141.413s
- Generated index: `reports/INDEX.md`
- Run manifest: `reports/protocols/public_baseline/protocol_run.manifest.json`

## What Ran

| Step | Time | Note |
| --- | ---: | --- |
| `els_controls` | 38.239s | shuffled-letter and shuffled-term controls |
| `gog_magog_pairs` | 22.635s | Gog/Magog proximity controls |
| `surface_context_nt` | 18.909s | NT hit center/span context screen |
| `gog_magog_strict_pairs` | 12.281s | same-chapter and same-signed-skip Gog/Magog controls |
| `batch_term_sets` | 11.161s | one scan per corpus for declared term sets |
| `targeted_paired_controls` | 10.806s | focused modern/geopolitical paired controls |
| `critical_omission_breaks` | 9.751s | TR hits affected by SBLGNT omitted verses |
| `pair_baselines` | 9.708s | strict observed unrelated pair baselines |
| `related_name_pairs` | 9.000s | related modern-name proximity |
| `extension_paired_controls` | 8.464s | filtered extension paired controls |
| `synthetic_pair_baselines` | 5.460s | length-matched synthetic Hebrew pair baselines |
| `surface_extensions_tr_nt` | 5.087s | same-skip extension scan |
| `surface_extensions_sblgnt` | 5.051s | same-skip extension scan |
| `report_index` | 4.901s | report index rebuild |
| `beast_dragon_strict_controls` | 4.477s | full controls for Hebrew Beast/Dragon baseline |
| `synthetic_extension_baselines` | 4.217s | same-length synthetic Greek extension baselines |
| `extension_exact_center_cohort_controls` | 4.088s | broader exact-center extension cohort controls |
| `extension_overlap_controls` | 3.987s | strict TR/SBLGNT overlap extension controls |
| `extension_exact_center_controls` | 3.583s | deeper exact-center extension controls |
| `extension_exact_center_cohort_review` | 0.831s | exact-center cohort context and letter-path review |
| `extension_context_review` | 0.798s | manual context review for strict extension overlaps |
| `extension_exact_center_cross_text` | 0.556s | exact-center cross-text key check |
| `synthetic_extension_match_review` | 0.471s | context review for synthetic extension match rows |
| `targeted_terms_report` | 0.384s | compact target-term join report |
| `surface_extension_summary_tr_nt` | 0.292s | filtered TR extension summary |
| `surface_extension_summary_sblgnt` | 0.292s | filtered SBLGNT extension summary |
| `word_counts` | 0.079s | cached lexical/morphology-style count reports |
| `extension_exact_center_final_gate` | 0.047s | final exact-center promotion gate |
| `bootstrap_public_sources` | 0.018s | cached source bootstrap and corpus stats |
| `critical_surface_variants` | 0.005s | cached critical-text surface variant rows |

Key output sizes:

| Output | Rows |
| --- | ---: |
| `reports/protocols/public_baseline/surface_context_hits.csv` | 56,654 |
| `reports/protocols/public_baseline/surface_context_summary.csv` | 766 |
| `reports/protocols/public_baseline/surface_context_extensions_tr_nt_top.csv` | 11 |
| `reports/protocols/public_baseline/surface_context_extensions_sblgnt_top.csv` | 21 |
| `reports/els_controls_summary.csv` | 1,560 |
| `reports/critical_omission_breaks_summary.csv` | 383 |
| `reports/related_name_pairs_summary.csv` | 85 |
| `reports/targeted_terms_summary.csv` | 41 |
| `reports/targeted_paired_controls_summary.csv` | 41 |
| `reports/gog_magog_pairs_summary.csv` | 4 |
| `reports/gog_magog_strict_pairs_summary.csv` | 4 |
| `reports/pair_baselines_summary.csv` | 20 |
| `reports/synthetic_pair_baselines_summary.csv` | 25 |
| `reports/synthetic_pair_baselines_comparison.csv` | 2 |
| `reports/beast_dragon_strict_controls_summary.csv` | 1 |
| `reports/extension_paired_controls_summary.csv` | 32 |
| `reports/extension_overlap_controls_summary.csv` | 6 |
| `reports/extension_context_review_summary.csv` | 6 |
| `reports/extension_exact_center_controls_summary.csv` | 2 |
| `reports/extension_exact_center_cohort_controls_summary.csv` | 4 |
| `reports/extension_exact_center_cohort_review_summary.csv` | 4 |
| `reports/extension_exact_center_cross_text_summary.csv` | 4 |
| `reports/extension_exact_center_final_gate_summary.csv` | 4 |
| `reports/synthetic_extension_baselines_summary.csv` | 4 |
| `reports/synthetic_extension_baselines_matches.csv` | 3 |
| `reports/synthetic_extension_match_review_summary.csv` | 3 |

## Main Read

The toolkit is now ready for actual searches. Raw ELS counts are abundant, especially for short strings and abbreviations. The controls do not support treating the raw leaders as meaningful by themselves.

Practical interpretation:

- High counts mostly track short normalized strings, common letter patterns, and search-space size.
- Abbreviations such as United Nations acronym forms produce very large counts.
- Longer phrases mostly produce zero hits at the current skip range.
- Filtered extension tops are manageable and readable; the `δοξα` (doxa; English: glory) exact-center overlap remains one strong review row, and the broader exact-center cohort adds `αιμα` (haima; English: blood) and `υιος` (huios; English: son) screens.
- No current result should be promoted as a claim without a stronger null test.

## Modern And Geopolitical Terms

Selected counts from `reports/protocols/public_baseline/modern_names_dates_counts.csv`.

| Concept | Term | MT_WLC | LXX | TR_NT | SBLGNT | Read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Trump | `טראמפ` (Tramp; English: Trump) / `τραμπ` (tramp; English: Trump) | 4 | 71 | 18 | 12 | present, low to modest |
| Donald Trump | `דונלדטראמפ` (Donald Tramp; English: Donald Trump) | 0 | - | - | - | absent in Hebrew combined form |
| Vance | `ואנס` (Vance; English: Vance) / `βανς` (vans; English: Vance) | 331 | 1,532 | 241 | 259 | high because short form |
| Vance alt | `ווענס` (Vance; English: Vance) | 12 | - | - | - | present, low |
| Netanyahu | `נתניהו` (Netanyahu; English: Netanyahu) / `νετανιαχου` (netaniachou; English: Netanyahu) | 8 | 0 | 0 | 0 | Hebrew only, low |
| Iran | `איראן` (Iran; English: Iran) / `ιραν` (iran; English: Iran) | 210 | 8,375 | 1,876 | 1,983 | high in Greek because short form |
| Russia | `רוסיה` (Russia; English: Russia) / `Ρωσία` (rosia; English: Russia) | 50 | 268 | 52 | 57 | present |
| Europe | `אירופה` (Europe; English: Europe) / `Ευρώπη` (Europe; English: Europe) | 17 | 1 | 0 | 1 | low |
| Germany | `גרמניה` (Germanyah; English: Germany) / `Γερμανία` (Germania; English: Germany) | 2 | 0 | 0 | 0 | near absent |
| Turkey | `טורקיה` (Turkiyah; English: Turkey) / `Τουρκία` (Tourkia; English: Turkey) | 1 | 0 | 1 | 0 | near absent |
| Turkey alt | `תורכיה` (Turkiyah; English: Turkey) | 14 | - | - | - | present, low |
| United States | phrase forms | 0 | 0 | 0 | 0 | absent as full phrase |
| USA abbreviation | `ארה״ב` (ARHB; English: USA abbreviation) / `ΗΠΑ` (HPA; English: USA abbreviation) | 2,410 | 42,727 | 9,567 | 9,201 | high abbreviation effect |
| United Nations | full phrase | 0 | 0 | 0 | 0 | absent as full phrase |
| United Nations acronym | `או״ם` (UM; English: United Nations abbreviation) / `ΟΗΕ` (OHE; English: United Nations abbreviation) | 81,373 | 95,280 | 25,587 | 24,918 | very high abbreviation effect |
| European Union | full phrase | 0 | 0 | 0 | 0 | absent |

Read:

- Full modern phrases usually disappear.
- Short acronyms and 3-4 letter transliterations dominate.
- `Iran`, `Vance`, `USA`, and United Nations acronym counts should be treated mainly as density/length effects until controls get stronger.

## Gog And Magog

From `reports/protocols/public_baseline/prophetic_terms_counts.csv`.

| Concept | Term | MT_WLC | LXX | TR_NT | SBLGNT |
| --- | --- | ---: | ---: | ---: | ---: |
| Gog | `גוג` (Gog; English: Gog) / `γωγ` (Gog; English: Gog) | 1,364 | 1,800 | 594 | 572 |
| Magog | `מגוג` (Magog; English: Magog) / `μαγωγ` (Magog; English: Magog) | 104 | 9 | 3 | 3 |

Read:

- `Gog` is short and dense.
- `Magog` is longer and much less frequent.
- Same-chapter plus same-signed-skip controls reduce raw pair counts sharply.
- MT_WLC becomes not unusual under the stricter pair screen; LXX/TR_NT/SBLGNT remain q <= 0.10 review rows.
- Unrelated Hebrew Beast/Dragon has more strict close pairs than Gog/Magog, so Hebrew raw proximity is not unique.
- Full Beast/Dragon controls are not unusual, showing raw strict density can be explained by controls.
- Synthetic 3+4 Hebrew baselines often match or exceed Gog/Magog: close-pair `p_ge = 0.807692`, overlap `p_ge = 0.230769`.

## Local Terms

From `modern_names_dates_counts.csv`.

| Concept | Hebrew | Greek | Counts |
| --- | --- | --- | --- |
| Cowboy | `קאובוי` (kauboy; English: Cowboy) | `καουμποϊ` (kaoumpoi; English: Cowboy) | MT_WLC 7; Greek corpora 0 |
| Catering | `קייטרינג` (keytering; English: Catering) | `κετερινγκ` (keteringk; English: Catering) | all 0 |
| Cowboy Catering | `קאובוי קייטרינג` (kauboy keytering; English: Cowboy Catering) | `καουμποϊ κετερινγκ` (kaoumpoi keteringk; English: Cowboy Catering) | all 0 |
| Simsberry | `סימסברי` (Simsberry; English: Simsberry) | `σιμσμπερι` (simsberi; English: Simsberry) | all 0 |
| Simscorner | `סימסקורנר` (Simscorner; English: Simscorner) | `σιμσκορνερ` (simskorner; English: Simscorner) | all 0 |

Read:

- Local phrase/name terms are effectively absent at current settings.
- `Cowboy` has 7 Hebrew hits, but no Greek hits and no phrase support.

## Count Leaders

Length-at-least-4 leaders are more informative than raw 3-letter leaders, but still not claims.

| File | Leaders |
| --- | --- |
| `modern_names_dates_counts.csv` | LXX `nato_g` 15,410; LXX `china_g` 10,915; LXX `iran_g` 8,375; MT `bibi_h` 5,088 |
| `prophetic_terms_counts.csv` | LXX `blood_g` 11,030; MT `rome_h` 6,954; MT `mary_h` 5,303; MT `lion_h` 5,155 |
| `theological_terms_counts.csv` | LXX `temple_g` 17,198; LXX `son_g` 12,919; LXX `blood_g` 11,030; MT `yhwh_h` 10,674 |
| `table_of_nations_counts.csv` | LXX `shelah_g` 9,611; LXX `lasha_g` 5,266; MT `amorite_h` 4,934; LXX `obal_g` 4,753 |

Read:

- This confirms the scanner is finding abundant ELS hits.
- It also confirms raw counts are not enough. Common short forms win.

## Surface Context

Top surface-context rows by `context_hit_count`:

| Corpus | Term | Hits | Context hits | Note |
| --- | --- | ---: | ---: | --- |
| SBLGNT | `eve_g` | 42,023 | 6,989 | dense short Greek form |
| TR_NT | `eve_g` | 43,331 | 6,664 | dense short Greek form |
| SBLGNT | `noah_g` | 17,189 | 4,022 | dense short Greek form |
| TR_NT | `noah_g` | 16,891 | 3,917 | dense short Greek form |
| TR_NT | `hul_g` | 10,456 | 2,906 | high-noise short form |
| SBLGNT | `hul_g` | 10,395 | 2,845 | high-noise short form |
| TR_NT | United Nations acronym | 25,587 | 2,748 | abbreviation effect |
| SBLGNT | United Nations acronym | 24,918 | 2,666 | abbreviation effect |

Read:

- Surface-context still favors short terms.
- Exact center/span hits exist, but short-term density dominates the top.

## Filtered Extension Tops

Current protocol uses stricter extension filters:

- `--min-extension-length 3`
- `--min-term-length 4`
- `--match-kind-prefix phrase_`
- `--exclude-term ουλ` (Oul; English: Hul)

Filtered top counts:

| Corpus | Top rows | Summary rows | Kept rows |
| --- | ---: | ---: | ---: |
| TR_NT | 11 | 422 | 485 |
| SBLGNT | 21 | 397 | 452 |

Strict TR_NT/SBLGNT top overlap:

| Term | Skip | Direction | Extension | Phrase | TR_NT span | SBLGNT span |
| --- | ---: | --- | --- | --- | --- | --- |
| `αδαμ` (Adam; English: Adam) | 11 | forward | `αδαμεισ` (adameis; English: hidden extension form from Adam) | `Ἀδὰμ εἰς` (Adam eis; English: Adam into) | HEB 13:15-HEB 13:16 | Heb 13:15-Heb 13:16 |
| `δοξα` (doxa; English: glory) | 21 | forward | `δοξανωσ` (doxanos; English: hidden extension form from doxa) | `δόξαν ὡς` (doxan hos; English: glory as) | 2TH 3:1 | 2Thess 3:1 |
| `υιος` (huios; English: son) | -4 | backward | `υιοστησ` (huiostes; English: hidden extension form from huios) | `υἱὸς τῆς` (huios tes; English: son of the) | JHN 5:13 | John 5:13 |

Read:

- The stricter filter produces a reviewable list.
- These overlaps survive TR/SBLGNT comparison because those passages are textually similar.
- Extension analysis now has a coarse all-row control screen, a stricter overlap-only screen, and a context review. Four overlap rows are ELS-only at the hit span; two `δοξα` (doxa; English: glory) rows have the base normalized string in the center verse surface text.

## Controls Verdict

From `reports/els_controls_summary.csv`:

| Band | Rows |
| --- | ---: |
| `not_unusual` | 1,526 |
| `not_tested` | 20 |
| `uncorrected_p_le_0.05` | 14 |

Important flags on the lowest-p rows:

- `few_letter_controls`
- `few_term_controls`
- `huge_search_space`
- `screening_min_p_adjusted`
- `uncorrected_only`

Read:

- No row should be treated as robustly significant from the current controls.
- The best p-values are screening artifacts from small control counts and large search space.
- Increase controls before making any external claim.

## Best Next Targets

Focused target results from the `targeted_terms_report` step are tracked in
`docs/TARGETED_TERMS_FINDINGS.md`. Focused paired controls are tracked in
`docs/TARGETED_PAIRED_CONTROLS.md`. Gog/Magog proximity controls are tracked in
`docs/GOG_MAGOG_PAIR_CONTROLS.md` and
`docs/GOG_MAGOG_STRICT_PAIR_CONTROLS.md`; unrelated pair baselines are tracked
in `docs/PAIR_BASELINES.md`, synthetic short-Hebrew pair baselines in
`docs/SYNTHETIC_PAIR_BASELINES.md`, with Beast/Dragon follow-up in
`docs/BEAST_DRAGON_STRICT_CONTROLS.md`. Filtered extension controls are tracked in
`docs/EXTENSION_PAIRED_CONTROLS.md`, `docs/EXTENSION_OVERLAP_CONTROLS.md`, and
`docs/EXTENSION_CONTEXT_REVIEW.md`. Exact-center cohort review is tracked in
`docs/EXTENSION_EXACT_CENTER_COHORT_REVIEW.md`, with cross-text filtering in
`docs/EXTENSION_EXACT_CENTER_CROSS_TEXT.md` and final gating in
`docs/EXTENSION_EXACT_CENTER_FINAL_GATE.md`. Synthetic extension baselines are
tracked in `docs/SYNTHETIC_EXTENSION_BASELINES.md`, with synthetic match context
review in `docs/SYNTHETIC_EXTENSION_MATCH_REVIEW.md`.

Targeted next round:

1. `Iran`
   - High enough to inspect, especially across Greek corpora.
   - Paired controls now read not unusual; short Greek form remains the main explanation.
2. `Trump`, `Vance`, `Netanyahu`
   - User-requested modern names.
   - Hebrew results are low to moderate; Greek `Vance` is high because short.
3. `Gog` / `Magog`
   - Theologically relevant pair.
   - Pair controls now show an exploratory q <= 0.10 screen, not a claim.
   - Strict same-chapter/same-skip controls make MT_WLC not unusual, while Greek rows remain exploratory q <= 0.10.
   - Pair baselines show Hebrew Beast/Dragon exceeds Gog/Magog strict close-pair counts.
   - Beast/Dragon controls are not unusual, reinforcing that high Hebrew raw pair counts need controls before interpretation.
   - Synthetic 3+4 Hebrew baselines often match or exceed Gog/Magog, so raw Hebrew proximity is now a low-priority claim path.
4. `Europe`, `Russia`, `Turkey`, `Germany`
   - Good geopolitical set.
   - Most are low except Russia and Europe Hebrew.
5. Filtered NT extension overlaps
   - Only 3 strict overlaps after filtering.
   - Overlap-only controls now put all 6 corpus rows at q = 0.019608.
   - Context review: `δοξα` (doxa; English: glory) passes the exact-center gate; `υιος` (huios; English: son) and `αδαμ` (Adam; English: Adam) are same-category only and ELS-only at the hit span.
   - Deeper `δοξα` (doxa; English: glory) controls: q = 0.004975 in both TR_NT and SBLGNT, still exploratory.
   - Broader exact-center cohort: 4 rows at q = 0.019608 with 50/50 controls; this prevents treating `δοξα` (doxa; English: glory) as the only exact-center example.
   - Cohort context review: all 4 rows have base-term surface context, but none has the full extension phrase as surface text.
   - Cross-text check: only `δοξα` (doxa; English: glory) appears in both Greek NT texts by exact extension key; SBLGNT `αιμα` (haima; English: blood) and `υιος` (huios; English: son) are source-only.
   - Final gate: only `δοξα` (doxa; English: glory) remains a review row, and it is still explicitly `review_only_not_claim`.
   - Synthetic extension baselines: same-type synthetic controls do not match target scores, but any-type synthetic controls can match/exceed 2 of 4 rows with 3 detailed synthetic match rows.
   - Synthetic match review: all 3 synthetic match rows are ELS-only at the hit span; matched phrases appear elsewhere.

## Current Follow-Up Map

- Focused-term baseline: tracked `targeted_paired_controls` report.
- Gog/Magog baseline comparison: `docs/SYNTHETIC_PAIR_BASELINES.md` and
  `docs/PAIR_BASELINES.md`.
- Filtered extension review baseline: `docs/EXTENSION_EXACT_CENTER_FINAL_GATE.md`,
  `docs/SYNTHETIC_EXTENSION_BASELINES.md`, and
  `docs/SYNTHETIC_EXTENSION_MATCH_REVIEW.md`.
- Formal extension claims require newly locked larger/deeper controls before any
  promotion language.
