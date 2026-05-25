#!/usr/bin/env python3
"""Download external WRR audit/source files into ignored reports output."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.request import Request, urlopen

from els import __version__


DEFAULT_OUT_DIR = Path("reports/wrr_1994")
DEFAULT_SOURCES = {
    "wrr_1994_paper": "https://academicweb.nd.edu/~rwilliam/ndonly/readings/Methods/06-ContentAnalysis/Equidistant%20Letter%20Sequences%20in%20the%20Book%20of%20Genesis%201994.pdf",
    "mmbbk_1999_paper": "https://users.cecs.anu.edu.au/~bdm/codes/StatSci/StatSci.pdf",
    "mmbbk_data_page": "https://users.cecs.anu.edu.au/~bdm/codes/StatSci/data.html",
    "chance_article": "https://users.cecs.anu.edu.au/~bdm/codes/Chance.pdf",
    "torah_code_papers_page": "https://www.torah-code.org/papers.html",
    "torah_code_colinear_paper": "https://www.torah-code.org/papers/bombach.pdf",
    "torah_code_colinear_attachments": "https://www.torah-code.org/papers/attachments.html",
    "torah_code_colinear_attachment_pls": "http://www.torahcodes.org/patterns/pls.pdf",
    "torah_code_colinear_attachment_roots": "http://www.torahcodes.org/patterns/roots.pdf",
    "torah_code_colinear_attachment_all_1698": "http://www.torahcodes.org/patterns/all_1698.pdf",
    "torah_code_colinear_attachment_res_113": "http://www.torahcodes.org/patterns/res_113.pdf",
    "torah_code_colinear_attachment_consul_138": "http://www.torahcodes.org/patterns/consul_138.pdf",
    "torah_code_colinear_attachment_intersec_108": "http://www.torahcodes.org/patterns/intersec_108.pdf",
    "torah_code_colinear_attachment_comb_143": "http://www.torahcodes.org/patterns/comb_143.pdf",
    "torah_code_colinear_attachment_att_heb": "http://www.torahcodes.org/patterns/att_heb.pdf",
    "gans_communities_paper": "https://www.torah-code.org/papers/gans.pdf",
    "gans_communities_data": "https://www.torah-code.org/papers/communities_data.pdf",
    "haralick_new_protocols": "https://www.torah-code.org/papers/sspr98.pdf",
    "haralick_controversy": "https://www.torah-code.org/papers/icpr98.pdf",
    "haralick_skeptical_response": "https://www.torah-code.org/papers/skeptical_inquirer_02_15_07.pdf",
    "haralick_basic_concepts": "https://www.torah-code.org/papers/wdp.pdf",
    "haralick_experimental_protocol": "https://www.torah-code.org/papers/wdp2.pdf",
    "levitt_component_analysis": "https://www.torah-code.org/papers/levitt.pdf",
    "levitt_component_data": "https://www.torah-code.org/papers/caweb.pdf",
    "levitt_long_phrases": "https://www.torah-code.org/papers/belgpdf.pdf",
    "levitt_linguistic_connections": "https://www.torah-code.org/papers/belj.pdf",
    "rips_twin_towers": "https://www.torah-code.org/papers/rips.pdf",
    "schwartzman_dialog_mode": "https://www.torah-code.org/papers/mode_1.pdf",
    "witztum_birth_dates": "https://www.torah-code.org/papers/witztum.pdf",
    "witztum_birth_dates_data": "https://www.torah-code.org/papers/personaldata.pdf",
    "torah_code_experiments_page": "https://www.torah-code.org/experiments.html",
    "torah_code_experiment_personal_statement": "https://www.torah-code.org/experiments/personal_statement.shtml",
    "torah_code_experiment_american_presidents_page": "https://www.torah-code.org/experiments/american_presidents.shtml",
    "torah_code_experiment_american_presidents_paper": "https://www.torah-code.org/experiments/american_presidents.pdf",
    "torah_code_experiment_american_presidents_data": "https://www.torah-code.org/experiments/americanpresidents_nasi_data.pdf",
    "torah_code_experiment_english_hebrew_transliteration_rules": "https://www.torah-code.org/experiments/english_hebrew_transliteration_rule.pdf",
    "torah_code_experiment_israeli_prime_ministers_page": "https://www.torah-code.org/experiments/israeli_prime_ministers.shtml",
    "torah_code_experiment_israeli_prime_ministers_paper": "https://www.torah-code.org/experiments/Israeli_prime_ministers.pdf",
    "torah_code_experiment_israeli_prime_ministers_1": "https://www.torah-code.org/experiments/israeli_prime_ministers_1.html",
    "torah_code_experiment_israeli_prime_ministers_2": "https://www.torah-code.org/experiments/israeli_prime_ministers_2.html",
    "torah_code_experiment_israeli_prime_ministers_3": "https://www.torah-code.org/experiments/israeli_prime_ministers_3.html",
    "torah_code_experiment_israeli_prime_ministers_4": "https://www.torah-code.org/experiments/israeli_prime_ministers_4.html",
    "torah_code_experiment_israeli_prime_ministers_5": "https://www.torah-code.org/experiments/israeli_prime_ministers_5.html",
    "torah_code_experiment_israeli_prime_ministers_6": "https://www.torah-code.org/experiments/israeli_prime_ministers_6.html",
    "torah_code_experiment_israeli_prime_ministers_7": "https://www.torah-code.org/experiments/israeli_prime_ministers_7.html",
    "torah_code_experiment_israeli_prime_ministers_8": "https://www.torah-code.org/experiments/israeli_prime_ministers_8.html",
    "torah_code_experiment_cities_page": "https://www.torah-code.org/experiments/cities_experiment.shtml",
    "torah_code_experiment_cities_gans_original_report": "https://www.torah-code.org/papers/gans_original_report.pdf",
    "torah_code_experiment_cities_gans_page": "https://www.torah-code.org/experiments/gans_cities.html",
    "torah_code_experiment_cities_aumann_page": "https://www.torah-code.org/experiments/aumann_experiment.html",
    "torah_code_experiment_cities_aumann_report": "https://www.torah-code.org/experiments/dp364_short.pdf",
    "torah_code_experiment_cities_aumann_expert_instructions": "https://www.torah-code.org/experiments/dp364_appendix_3.pdf",
    "torah_code_experiment_cities_aumann_city_names": "https://www.torah-code.org/experiments/dp364_appendix_4.pdf",
    "torah_code_experiment_cities_aumann_minority_reports": "https://www.torah-code.org/experiments/dp364_appendix_5.pdf",
    "torah_code_experiment_cities_simon_mckay_page": "https://www.torah-code.org/experiments/simon_mckay_experiment.html",
    "torah_code_experiment_cities_margolioth_report": "https://www.torah-code.org/experiments/Margcities.pdf",
    "torah_code_experiment_cities_margolioth_data": "https://www.torah-code.org/experiments/Margoliot_Cities_Data.pdf",
    "torah_code_experiment_cities_comparison": "https://www.torah-code.org/experiments/cities_comparison.pdf",
    "torah_code_experiment_cities_haralick_page": "https://www.torah-code.org/experiments/haralick_cities_experiment.html",
    "torah_code_experiment_chumash_page": "https://www.torah-code.org/experiments/chumash_experiment.shtml",
    "torah_code_experiment_sons_of_haman_page": "https://www.torah-code.org/experiments/sons_of_haman_experiment.shtml",
    "torah_code_experiment_sons_of_haman_data": "https://www.torah-code.org/experiments/sons_of_haman_experiment_1.html",
    "torah_code_experiment_twin_towers_page": "https://www.torah-code.org/experiments/twin_towers_experiment.shtml",
    "torah_code_experiment_tsunami_page": "https://www.torah-code.org/experiments/tsunami_experiment.shtml",
    "torah_code_experiment_katrina_page": "https://www.torah-code.org/experiments/katrina_experiment.shtml",
    "torah_code_experiment_great_rabbis_page": "https://www.torah-code.org/experiments/great_rabbis_experiment.shtml",
    "torah_code_experiment_son_rabbis_page": "https://www.torah-code.org/experiments/son_rabbis_experiment.shtml",
    "torah_code_experiment_pumbedita_page": "https://www.torah-code.org/experiments/pumbedita_experiment.shtml",
    "torah_code_experiment_pumbedita_data": "https://www.torah-code.org/experiments/pumbedita.pdf",
    "torah_code_experiment_auschwitz_page": "https://www.torah-code.org/experiments/auschwitz_experiment.shtml",
    "torah_code_experiment_auschwitz_data": "https://www.torah-code.org/experiments/auschwitz.pdf",
    "torah_code_experiment_witztum_statement": "https://www.torah-code.org/controversy/witztum_statement.pdf",
    "torah_code_experiment_ark_page": "https://www.torah-code.org/experiments/ark_experiment.shtml",
    "torah_code_experiment_ark_code": "https://www.torah-code.org/experiments/ark_code_1.pdf",
    "torah_code_hypothesis_testing_overview": "https://www.torah-code.org/hypothesis_testing/hypothesis_1.html",
    "torah_code_hypothesis_testing_errors": "https://www.torah-code.org/hypothesis_testing/hypothesis_2.html",
    "torah_code_hypothesis_testing_hypotheses": "https://www.torah-code.org/hypothesis_testing/hypotheses.html",
    "torah_code_hypothesis_testing_simulated_experiments": "https://www.torah-code.org/hypothesis_testing/simulated_experiments.html",
    "torah_code_research_program_1": "https://www.torah-code.org/research/research_1.html",
    "torah_code_research_program_1_shtml": "https://www.torah-code.org/research/research_1.shtml",
    "torah_code_research_program_2": "https://www.torah-code.org/research/research_2.html",
    "torah_code_research_program_2_shtml": "https://www.torah-code.org/research/research_2.shtml",
    "torah_code_research_model_overview": "https://www.torah-code.org/research/research_2a.html",
    "torah_code_research_model_overview_shtml": "https://www.torah-code.org/research/research_2a.shtml",
    "torah_code_research_geometric_model_level_1": "https://www.torah-code.org/research/research_3.html",
    "torah_code_research_geometric_model_level_1_shtml": "https://www.torah-code.org/research/research_3.shtml",
    "torah_code_research_geometric_model_level_2": "https://www.torah-code.org/research/research_3a.html",
    "torah_code_research_geometric_model_level_2_shtml": "https://www.torah-code.org/research/research_3a.shtml",
    "torah_code_research_geometric_model_level_3": "https://www.torah-code.org/research/research_3b.html",
    "torah_code_research_geometric_model_level_3_shtml": "https://www.torah-code.org/research/research_3b.shtml",
    "torah_code_research_els_model_level_1": "https://www.torah-code.org/research/research_3c.html",
    "torah_code_research_els_model_level_1_shtml": "https://www.torah-code.org/research/research_3c.shtml",
    "torah_code_research_els_model_level_2": "https://www.torah-code.org/research/research_3d.html",
    "torah_code_research_els_model_level_2_shtml": "https://www.torah-code.org/research/research_3d.shtml",
    "torah_code_research_els_model_level_3": "https://www.torah-code.org/research/research_3e.html",
    "torah_code_research_els_model_level_3_shtml": "https://www.torah-code.org/research/research_3e.shtml",
    "wrr1": "https://users.cecs.anu.edu.au/~bdm/codes/statsci/WRR1.txt",
    "wrr2": "https://users.cecs.anu.edu.au/~bdm/codes/statsci/WRR2.txt",
    "se2a": "https://users.cecs.anu.edu.au/~bdm/codes/statsci/SE2a.txt",
    "se2b": "https://users.cecs.anu.edu.au/~bdm/codes/statsci/SE2b.txt",
    "se3": "https://users.cecs.anu.edu.au/~bdm/codes/statsci/SE3.txt",
    "mc_key": "https://users.cecs.anu.edu.au/~bdm/codes/MC.html",
    "wrr_nations_mc": "https://www.math.utoronto.ca/drorbn/Codes/Nations/main_mc.html",
    "wrr_nations_gir": "https://www.math.utoronto.ca/drorbn/Codes/Nations/main_gir.html",
    "wnp_mc": "https://users.cecs.anu.edu.au/~bdm/codes/WNP/main_mc.html",
    "wnp_en": "https://users.cecs.anu.edu.au/~bdm/codes/WNP/main_en.html",
}
REQUIRED_MANIFEST_LABELS = tuple(DEFAULT_SOURCES)


@dataclass(frozen=True)
class FetchResult:
    data: bytes
    final_url: str
    http_status: int | None


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    downloads = []
    source_items = selected_sources(args.label)
    for label, url in source_items:
        target = args.out_dir / source_filename(label, url)
        if target.exists() and not args.refresh:
            status = "cached"
            final_url = ""
            http_status = None
        else:
            result = fetch_url(url)
            target.write_bytes(result.data)
            status = "downloaded"
            final_url = result.final_url
            http_status = result.http_status
        downloads.append(
            {
                "label": label,
                "url": url,
                "final_url": final_url,
                "redirected": bool(final_url and final_url != url),
                "http_status": http_status,
                "path": str(target),
                "status": status,
                "bytes": target.stat().st_size,
                "sha256": sha256_file(target),
            }
        )
        print(target)
    if args.manifest_out:
        write_manifest(args.manifest_out, downloads, started)
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_OUT_DIR / "sources.manifest.json")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument(
        "--label",
        action="append",
        default=[],
        help="Download only a specific source label. May be repeated.",
    )
    return parser


def selected_sources(labels: list[str]) -> list[tuple[str, str]]:
    if not labels:
        return list(DEFAULT_SOURCES.items())
    unknown = [label for label in labels if label not in DEFAULT_SOURCES]
    if unknown:
        raise SystemExit("unknown source labels: " + ", ".join(unknown))
    return [(label, DEFAULT_SOURCES[label]) for label in labels]


def source_filename(label: str, url: str) -> str:
    suffix = Path(url).suffix or ".txt"
    canonical_names = {
        "wrr_1994_paper": "wrr_1994_paper.pdf",
        "mmbbk_1999_paper": "mmbbk_1999_paper.pdf",
        "mmbbk_data_page": "mmbbk_data_page.html",
        "chance_article": "chance_torah_codes_puzzle_solution.pdf",
        "torah_code_papers_page": "torah_code_papers.html",
        "torah_code_colinear_paper": "torah_code_colinear_paper.pdf",
        "torah_code_colinear_attachments": "torah_code_colinear_attachments.html",
        "torah_code_colinear_attachment_pls": "torah_code_colinear_attachment_pls.pdf",
        "torah_code_colinear_attachment_roots": "torah_code_colinear_attachment_roots.pdf",
        "torah_code_colinear_attachment_all_1698": "torah_code_colinear_attachment_all_1698.pdf",
        "torah_code_colinear_attachment_res_113": "torah_code_colinear_attachment_res_113.pdf",
        "torah_code_colinear_attachment_consul_138": "torah_code_colinear_attachment_consul_138.pdf",
        "torah_code_colinear_attachment_intersec_108": "torah_code_colinear_attachment_intersec_108.pdf",
        "torah_code_colinear_attachment_comb_143": "torah_code_colinear_attachment_comb_143.pdf",
        "torah_code_colinear_attachment_att_heb": "torah_code_colinear_attachment_att_heb.pdf",
        "gans_communities_paper": "gans_communities_paper.pdf",
        "gans_communities_data": "gans_communities_data.pdf",
        "haralick_new_protocols": "haralick_new_protocols.pdf",
        "haralick_controversy": "haralick_controversy.pdf",
        "haralick_skeptical_response": "haralick_skeptical_response.pdf",
        "haralick_basic_concepts": "haralick_basic_concepts.pdf",
        "haralick_experimental_protocol": "haralick_experimental_protocol.pdf",
        "levitt_component_analysis": "levitt_component_analysis.pdf",
        "levitt_component_data": "levitt_component_data.pdf",
        "levitt_long_phrases": "levitt_long_phrases.pdf",
        "levitt_linguistic_connections": "levitt_linguistic_connections.pdf",
        "rips_twin_towers": "rips_twin_towers.pdf",
        "schwartzman_dialog_mode": "schwartzman_dialog_mode.pdf",
        "witztum_birth_dates": "witztum_birth_dates.pdf",
        "witztum_birth_dates_data": "witztum_birth_dates_data.pdf",
        "torah_code_experiments_page": "torah_code_experiments.html",
        "torah_code_experiment_personal_statement": "torah_code_experiment_personal_statement.html",
        "torah_code_experiment_american_presidents_page": "torah_code_experiment_american_presidents.html",
        "torah_code_experiment_american_presidents_paper": "torah_code_experiment_american_presidents.pdf",
        "torah_code_experiment_american_presidents_data": "torah_code_experiment_american_presidents_data.pdf",
        "torah_code_experiment_english_hebrew_transliteration_rules": "torah_code_experiment_english_hebrew_transliteration_rules.pdf",
        "torah_code_experiment_israeli_prime_ministers_page": "torah_code_experiment_israeli_prime_ministers.html",
        "torah_code_experiment_israeli_prime_ministers_paper": "torah_code_experiment_israeli_prime_ministers.pdf",
        "torah_code_experiment_israeli_prime_ministers_1": "torah_code_experiment_israeli_prime_ministers_1.html",
        "torah_code_experiment_israeli_prime_ministers_2": "torah_code_experiment_israeli_prime_ministers_2.html",
        "torah_code_experiment_israeli_prime_ministers_3": "torah_code_experiment_israeli_prime_ministers_3.html",
        "torah_code_experiment_israeli_prime_ministers_4": "torah_code_experiment_israeli_prime_ministers_4.html",
        "torah_code_experiment_israeli_prime_ministers_5": "torah_code_experiment_israeli_prime_ministers_5.html",
        "torah_code_experiment_israeli_prime_ministers_6": "torah_code_experiment_israeli_prime_ministers_6.html",
        "torah_code_experiment_israeli_prime_ministers_7": "torah_code_experiment_israeli_prime_ministers_7.html",
        "torah_code_experiment_israeli_prime_ministers_8": "torah_code_experiment_israeli_prime_ministers_8.html",
        "torah_code_experiment_cities_page": "torah_code_experiment_cities.html",
        "torah_code_experiment_cities_gans_original_report": "torah_code_experiment_cities_gans_original_report.pdf",
        "torah_code_experiment_cities_gans_page": "torah_code_experiment_cities_gans.html",
        "torah_code_experiment_cities_aumann_page": "torah_code_experiment_cities_aumann.html",
        "torah_code_experiment_cities_aumann_report": "torah_code_experiment_cities_aumann_report.pdf",
        "torah_code_experiment_cities_aumann_expert_instructions": "torah_code_experiment_cities_aumann_expert_instructions.pdf",
        "torah_code_experiment_cities_aumann_city_names": "torah_code_experiment_cities_aumann_city_names.pdf",
        "torah_code_experiment_cities_aumann_minority_reports": "torah_code_experiment_cities_aumann_minority_reports.pdf",
        "torah_code_experiment_cities_simon_mckay_page": "torah_code_experiment_cities_simon_mckay.html",
        "torah_code_experiment_cities_margolioth_report": "torah_code_experiment_cities_margolioth_report.pdf",
        "torah_code_experiment_cities_margolioth_data": "torah_code_experiment_cities_margolioth_data.pdf",
        "torah_code_experiment_cities_comparison": "torah_code_experiment_cities_comparison.pdf",
        "torah_code_experiment_cities_haralick_page": "torah_code_experiment_cities_haralick.html",
        "torah_code_experiment_chumash_page": "torah_code_experiment_chumash.html",
        "torah_code_experiment_sons_of_haman_page": "torah_code_experiment_sons_of_haman.html",
        "torah_code_experiment_sons_of_haman_data": "torah_code_experiment_sons_of_haman_data.html",
        "torah_code_experiment_twin_towers_page": "torah_code_experiment_twin_towers.html",
        "torah_code_experiment_tsunami_page": "torah_code_experiment_tsunami.html",
        "torah_code_experiment_katrina_page": "torah_code_experiment_katrina.html",
        "torah_code_experiment_great_rabbis_page": "torah_code_experiment_great_rabbis.html",
        "torah_code_experiment_son_rabbis_page": "torah_code_experiment_son_rabbis.html",
        "torah_code_experiment_pumbedita_page": "torah_code_experiment_pumbedita.html",
        "torah_code_experiment_pumbedita_data": "torah_code_experiment_pumbedita_data.pdf",
        "torah_code_experiment_auschwitz_page": "torah_code_experiment_auschwitz.html",
        "torah_code_experiment_auschwitz_data": "torah_code_experiment_auschwitz_data.pdf",
        "torah_code_experiment_witztum_statement": "torah_code_experiment_witztum_statement.pdf",
        "torah_code_experiment_ark_page": "torah_code_experiment_ark.html",
        "torah_code_experiment_ark_code": "torah_code_experiment_ark_code.pdf",
        "torah_code_hypothesis_testing_overview": "torah_code_hypothesis_testing_overview.html",
        "torah_code_hypothesis_testing_errors": "torah_code_hypothesis_testing_errors.html",
        "torah_code_hypothesis_testing_hypotheses": "torah_code_hypothesis_testing_hypotheses.html",
        "torah_code_hypothesis_testing_simulated_experiments": "torah_code_hypothesis_testing_simulated_experiments.html",
        "torah_code_research_program_1": "torah_code_research_program_1.html",
        "torah_code_research_program_1_shtml": "torah_code_research_program_1_shtml.html",
        "torah_code_research_program_2": "torah_code_research_program_2.html",
        "torah_code_research_program_2_shtml": "torah_code_research_program_2_shtml.html",
        "torah_code_research_model_overview": "torah_code_research_model_overview.html",
        "torah_code_research_model_overview_shtml": "torah_code_research_model_overview_shtml.html",
        "torah_code_research_geometric_model_level_1": "torah_code_research_geometric_model_level_1.html",
        "torah_code_research_geometric_model_level_1_shtml": "torah_code_research_geometric_model_level_1_shtml.html",
        "torah_code_research_geometric_model_level_2": "torah_code_research_geometric_model_level_2.html",
        "torah_code_research_geometric_model_level_2_shtml": "torah_code_research_geometric_model_level_2_shtml.html",
        "torah_code_research_geometric_model_level_3": "torah_code_research_geometric_model_level_3.html",
        "torah_code_research_geometric_model_level_3_shtml": "torah_code_research_geometric_model_level_3_shtml.html",
        "torah_code_research_els_model_level_1": "torah_code_research_els_model_level_1.html",
        "torah_code_research_els_model_level_1_shtml": "torah_code_research_els_model_level_1_shtml.html",
        "torah_code_research_els_model_level_2": "torah_code_research_els_model_level_2.html",
        "torah_code_research_els_model_level_2_shtml": "torah_code_research_els_model_level_2_shtml.html",
        "torah_code_research_els_model_level_3": "torah_code_research_els_model_level_3.html",
        "torah_code_research_els_model_level_3_shtml": "torah_code_research_els_model_level_3_shtml.html",
        "wrr1": "WRR1.txt",
        "wrr2": "WRR2.txt",
        "se2a": "SE2a.txt",
        "se2b": "SE2b.txt",
        "se3": "SE3.txt",
        "wrr_nations_mc": "wrr_nations_main_mc.html",
        "wrr_nations_gir": "wrr_nations_main_gir.html",
    }
    if label in canonical_names:
        return canonical_names[label]
    return f"{label}{suffix}"


def fetch_url(url: str) -> FetchResult:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 EDLS source audit"})
    with urlopen(request, timeout=30) as response:
        return FetchResult(
            data=response.read(),
            final_url=response.geturl(),
            http_status=getattr(response, "status", None),
        )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(path: Path, downloads: list[dict[str, object]], started: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "downloads": downloads,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
