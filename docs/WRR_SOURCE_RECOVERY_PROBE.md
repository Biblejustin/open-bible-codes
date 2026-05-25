# WRR Source Recovery Probe

Status: live-source recovery probe only. This does not run ELS searches,
does not update the cached `reports/wrr_1994/` bundle, and does not make
claim-ready source decisions.

## Summary

| Item | Count |
| --- | ---: |
| downloads probed | 18 |
| rows with expected labels configured | 18 |
| rows where expected label appeared | 0 |
| redirected rows | 18 |
| final URL is Torah-code root | 18 |
| canonical URL is Torah-code root | 18 |
| unrelated slot/gambling markers | 18 |
| usable current source rows | 0 |

Current recovery status: `no_live_sources_recovered`.

## Probe Rows

| Label | HTTP | Redirected | Final Root | Expected Text | Spam Marker | Bytes | SHA-256 | Status |
| --- | ---: | --- | --- | --- | --- | ---: | --- | --- |
| torah_code_research_program_1 | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_program_1_shtml | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_program_2 | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_program_2_shtml | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_model_overview | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_model_overview_shtml | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_geometric_model_level_1 | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_geometric_model_level_1_shtml | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_geometric_model_level_2 | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_geometric_model_level_2_shtml | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_geometric_model_level_3 | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_geometric_model_level_3_shtml | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_els_model_level_1 | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_els_model_level_1_shtml | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_els_model_level_2 | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_els_model_level_2_shtml | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_els_model_level_3 | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |
| torah_code_research_els_model_level_3_shtml | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unusable_current_download |

## Source Boundary

Probe manifest: `reports/wrr_source_recovery_probe/sources.manifest.json`.
Use this document to see whether previously missing Torah-code model pages
have become directly recoverable. A row is treated as usable only when the
download contains the expected page label, does not declare the site root as
canonical, does not end at the site root URL, and lacks unrelated spam markers.
