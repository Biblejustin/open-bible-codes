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
| `boundary_alignment` | implemented as a distribution summary over start/end boundary flags | `scripts/build_boundary_alignment.py` |
| `chapter_position_bias` | implemented as a distribution summary over center-position flags | `scripts/build_chapter_position_bias.py` |
| `forward_only` / `backward_only` / `bidirectional_present` | implemented by grouped direction counts | `scripts/build_match_strata_index.py` |
| `direction_imbalance_score` | summarized as term/corpus direction asymmetry review metadata | `scripts/build_direction_asymmetry.py` |
| `canonical_first_occurrence` | implemented within the current centered occurrence family | `scripts/build_match_strata_index.py` |
| `canonical_first_summary` | implemented as a distribution and first-row review export | `scripts/build_canonical_first_summary.py` |
| `cross_skip_pair_at_word` | implemented for same center word/reference with different skips | `scripts/build_match_strata_index.py` |
| `cross_skip_pair_at_letter` | implemented when retained/reconstructed letter paths share a letter position | `scripts/build_match_strata_index.py` |
| `cross_skip_pair_within_N_letters` | implemented for endpoint proximity under a configured distance | `scripts/build_match_strata_index.py` |
| `cross_skip_summary` | implemented as a distribution and candidate-row review export | `scripts/build_cross_skip_summary.py` |
| `canonical_first_in_thematic_chapter` | implemented against locked term-to-chapter mappings | `data/study/mappings/thematic_chapters.csv` |
| `author_in_own_book` | implemented against locked author-to-book mappings | `data/study/mappings/author_book_mapping.csv` |
| `protagonist_in_own_narrative` | implemented against locked protagonist-range mappings | `data/study/mappings/protagonist_narrative_mapping.csv` |
| `nt_quotation_anchor` / `nt_quotation_span` | implemented against locked OT-in-NT quotation mappings | `data/study/mappings/ot_in_nt_quotations.csv` |
| `lxx_vs_mt_semantic_divergence` | implemented as center-locus annotation against locked MT/LXX divergence mappings | `data/study/mappings/mt_lxx_semantic_divergence.csv` |
| `root_only_match` | implemented as exact matching against a locked Hebrew root policy | `data/study/mappings/hebrew_root_policy.csv` |
| `skip_equals_meaningful_constant` | implemented against locked constants | `terms/meaningful_constants.csv` |
| `skip_equals_term_gematria` | implemented for standard Hebrew/Greek values | `scripts/build_match_strata_index.py` |
| `skip_equals_center_word_gematria` | implemented for standard Hebrew/Greek values | `scripts/build_match_strata_index.py` |
| `low_bigram_surprise` / `high_bigram_surprise` | implemented as corpus-local review metadata | `els/letter_stats.py` |
| `letter_frequency_anomaly` | implemented as corpus-local review metadata | `els/letter_stats.py` |
| `review_flag_summary` | implemented as a meaningful-skip and rarity review export | `scripts/build_review_flag_summary.py` |
| `cohort_cluster_density_window_N` | implemented as declared-cohort word-window post-processing | `scripts/build_cohort_cluster_density.py` |
| `cohort_full_house` | implemented when every declared cohort term appears in the same word window | `scripts/build_cohort_cluster_density.py` |
| `term_absence_at_thematic_chapter` | implemented as optional thematic-chapter targets in the notable-passage gap analyzer | `scripts/analyze_notable_passage_gaps.py` |

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
| word-edge `word_skip_ELS` | first/last letter every `K`th word | `scripts/search_word_edge_patterns.py` |
| full word-token `word_skip_ELS` | full normalized surface-word tokens every `K`th word | `protocols/word_skip_term_audit.toml` |
| `cipher_layered_pair` | pairs ordinary and transformed hits at a declared same-anchor key | `scripts/build_cipher_layered_pairs.py` |

These families widen the search surface. Their reports include control
warnings and capped-row flags.

## Partial / Primitive Support

| Stratum | Current support | Missing for claim-grade use |
| --- | --- | --- |
| `matrix_cluster_at_width_W` | locked width-50 candidate protocol over CRD Bible/control hit rows exists, with relation-level Bible/control and opportunity-normalized summary | locked correction family and promotion threshold |
| `matrix_orthogonal` / `matrix_diagonal` / `matrix_adjacent_row` | candidate extraction labels nearest-cell relation over Bible/control rows and summarizes relation counts plus possible-pair denominators against controls | locked relation-specific promotion metric and correction family |
| WRR-style pair geometry | cylindrical distance primitives exist | full corrected WRR distance, domain weights, permutation driver |

## Deferred Pending Declared Data

No declared-data-only strata are currently waiting on schema support. Some
implemented mapping files contain conservative seed rows; others remain
header-only templates until populated and locked for a specific study.

Mapping-dependent rows use the locked CSV files in `data/study/mappings/`.
Some mapping files now contain conservative seed rows; others remain header-only
templates. Before any populated mapping can drive promotion, run:

```bash
make study-mapping-schemas
```

## Current Caution

Every added stratum widens either the metadata surface or the search surface.
Post-search metadata can prioritize review, but claim promotion still requires
a narrower locked protocol, language-matched controls, and correction for the
tested family.
