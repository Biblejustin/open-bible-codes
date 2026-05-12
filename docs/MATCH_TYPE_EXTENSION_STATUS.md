# Match Type Extension Status

This tracker maps proposed ELS match-type extensions to current repository
support. Status labels are engineering status only, not claim status.

## Implemented As Post-Search Metadata

| Stratum | Current support | Primary artifact |
| --- | --- | --- |
| `hidden_path_only` | existing centered occurrence type | `reports/centered_occurrence_index/centered_occurrences.csv` |
| `center_word_exact` / related center strata | existing centered occurrence and CRD pipeline | `scripts/build_centered_occurrence_index.py`, `scripts/run_crd_density.py` |
| `same_skip_extension` | existing extension audit | `els/extensions.py` |
| `boundary_*` endpoint flags | implemented from retained start/end offsets | `scripts/build_match_strata_index.py` |
| `center_verse_first_in_chapter` / `center_verse_last_in_chapter` | implemented from center verse refs | `scripts/build_match_strata_index.py` |
| `center_verse_first_in_book` / `center_verse_last_in_book` | implemented from center verse refs | `scripts/build_match_strata_index.py` |
| `chapter_position_bias` | implemented as a distribution summary over center-position flags | `scripts/build_chapter_position_bias.py` |
| `forward_only` / `backward_only` / `bidirectional_present` | implemented by grouped direction counts | `scripts/build_match_strata_index.py` |
| `canonical_first_occurrence` | implemented within the current centered occurrence family | `scripts/build_match_strata_index.py` |
| `cross_skip_pair_at_word` | implemented for same center word/reference with different skips | `scripts/build_match_strata_index.py` |
| `cross_skip_pair_at_letter` | implemented when retained/reconstructed letter paths share a letter position | `scripts/build_match_strata_index.py` |
| `cross_skip_pair_within_N_letters` | implemented for endpoint proximity under a configured distance | `scripts/build_match_strata_index.py` |
| `skip_equals_meaningful_constant` | implemented against locked constants | `terms/meaningful_constants.csv` |
| `skip_equals_term_gematria` | implemented for standard Hebrew/Greek values | `scripts/build_match_strata_index.py` |
| `skip_equals_center_word_gematria` | implemented for standard Hebrew/Greek values | `scripts/build_match_strata_index.py` |
| `low_bigram_surprise` / `high_bigram_surprise` | implemented as corpus-local review metadata | `els/letter_stats.py` |
| `letter_frequency_anomaly` | implemented as corpus-local review metadata | `els/letter_stats.py` |
| `cohort_cluster_density_window_N` | implemented as declared-cohort word-window post-processing | `scripts/build_cohort_cluster_density.py` |
| `cohort_full_house` | implemented when every declared cohort term appears in the same word window | `scripts/build_cohort_cluster_density.py` |

Current generated report:

```bash
python3 -m scripts.run_protocol protocols/match_strata_index.toml --resume
```

## Implemented As Opt-In Expanded Search Families

| Family | Current support | Primary artifact |
| --- | --- | --- |
| `atbash_path` | Hebrew Atbash transformed-corpus search | `protocols/hebrew_atbash_audit.toml` |
| `albam_path` | Hebrew ALBAM transformed-corpus search | `protocols/hebrew_albam_audit.toml` |
| `acrostic_pattern` | first-letter word-edge scanner with optional word skip | `protocols/word_edge_pattern_audit.toml` |
| `telestic_pattern` | last-letter word-edge scanner with optional word skip | `protocols/word_edge_pattern_audit.toml` |
| word-edge `word_skip_ELS` | first/last letter every `K`th word; full word-token variant remains deferred | `scripts/search_word_edge_patterns.py` |
| `cipher_layered_pair` | pairs ordinary and transformed hits at a declared same-anchor key | `scripts/build_cipher_layered_pairs.py` |

These families widen the search surface. Their reports include control
warnings and capped-row flags.

## Partial / Primitive Support

| Stratum | Current support | Missing for claim-grade use |
| --- | --- | --- |
| `matrix_cluster_at_width_W` | parameterized matrix-neighborhood candidate extraction exists | locked row-width protocol and matched controls |
| `matrix_orthogonal` / `matrix_diagonal` / `matrix_adjacent_row` | candidate extraction labels nearest-cell relation | locked relation-specific metric and correction family |
| WRR-style pair geometry | cylindrical distance primitives exist | full corrected WRR distance, domain weights, permutation driver |
| `term_absence_at_thematic_chapter` | notable-passage gap protocol exists | generalized term-to-chapter mapping |

## Deferred Pending Declared Data

| Stratum | Data dependency |
| --- | --- |
| `canonical_first_in_thematic_chapter` | locked term-to-thematic-chapter mapping |
| `author_in_own_book` | locked author-to-book mapping |
| `protagonist_in_own_narrative` | locked protagonist range mapping |
| `nt_quotation_anchor` / `nt_quotation_span` | OT-in-NT quotation catalog with anchors |
| `lxx_vs_mt_semantic_divergence` | locked MT/LXX divergence catalog |
| `root_only_match` | locked Hebrew root/lemma analyzer policy |
| full word-token `word_skip_ELS` | token-level word skip definition plus matched controls |

The mapping-dependent rows above now have header-only templates in
`data/study/mappings/`. Before any populated mapping can drive promotion, run:

```bash
python3 -m scripts.validate_study_mapping_schemas
```

## Current Caution

Every added stratum widens either the metadata surface or the search surface.
Post-search metadata can prioritize review, but claim promotion still requires
a narrower locked protocol, language-matched controls, and correction for the
tested family.
