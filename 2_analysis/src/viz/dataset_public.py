"""Read the public eVTOL_dataset (numbered folders 01 to 07) with the thesis code, unchanged inside.

The public dataset publishes aircraft ids as ``<patent>_ad<N>`` and the thesis architecture codes TP and TF, with its own file
names (30 to 33, 41 to 45, 61 to 63). The thesis code was written for ``<patent>_ua<N>``, the codes TR and TB, and the file layout
of the working folder. ``ensure_compat(root, output)`` therefore builds, from the public files only, a mirror in the layout the
code reads (``<output>/_dataset_public_compat/``) and writes the four script lists the analysis reads from
``review/script_outputs/`` (DOMAIN, YEAR, TRL, COMPANY_MAP). Nothing is taken from outside ``root``. The values are not changed
except the ids (_ad to _ua) and the codes (TP to TR, TF to TB), which ``publish_ids`` and the style layer undo in the outputs.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import pandas as pd

PILLAR = Path(__file__).resolve().parents[2]
SCRIPT_OUT = PILLAR / "review" / "script_outputs"
AD = re.compile(r"(?<=[A-Z0-9])_ad(?=\d)")
CODE_IN = {"TP": "TR", "TF": "TB"}
CODE_COLUMNS = ("topType", "arch_gt", "image_label", "ml_topType")
V = "06_external/61_evtol_news_directory/"
A = "06_external/62_aam_index/"
C = "06_external/63_context_series/"


# NASA definitions of the nine levels (the table in 04_aircraft/README.md)
_NASA_TRL = {1: 'Basic principles observed and reported.', 2: 'Technology concept and/or application formulated.', 3: 'Analytical and experimental proof-of-concept of critical function and/or characteristics.', 4: 'Component and/or breadboard validation in a  laboratory environment.', 5: 'Component and/or brassboard validated in a relevant environment.', 6: 'System/sub-system model or prototype demonstration in a relevant environment.', 7: 'System prototype demonstration in an operational environment.', 8: 'Actual system completed and "flight qualified" through test and demonstration.', 9: 'Actual system flight proven through successful mission operations.'}

def is_public(root) -> bool:
    return root is not None and (Path(root) / "03_patents" / "32_master_labels.xlsx").exists() and (Path(root) / "04_aircraft" / "42_aircraft.csv").exists()


def _rd(root: Path, rel: str) -> pd.DataFrame:
    return pd.read_csv(root / rel, dtype=str, keep_default_na=False, low_memory=False)


def _ids(df: pd.DataFrame) -> pd.DataFrame:
    return df.apply(lambda c: c.str.replace(AD, "_ua", regex=True) if c.dtype == object else c)


def _codes(df: pd.DataFrame) -> pd.DataFrame:
    for c in CODE_COLUMNS:
        if c in df.columns:
            df[c] = df[c].replace(CODE_IN)
    return df


def _out(df: pd.DataFrame, path: Path, **kw):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, **kw)


def _tables(root: Path, dst: Path):
    # ---- 02_patents ----
    p = _rd(root, "03_patents/33_patents.csv")
    _out(_codes(_ids(p.rename(columns={"ad": "ua"}))), dst / "02_patents" / "patents_1639.csv")
    ident = pd.read_csv(root / "03_patents/31_patent_text_extraction.csv", dtype=str, keep_default_na=False, low_memory=False)
    (dst / "02_patents").mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(dst / "02_patents" / "aircraft_identity_ALL.xlsx") as w:
        ident.to_excel(w, sheet_name="Identity", index=False)
    shutil.copy2(root / "03_patents/32_master_labels.xlsx", dst / "02_patents" / "wizard_record_Batch_ALL.xlsx")
    d = _rd(root, "data_dictionary.csv")
    rank = {"04_aircraft/42_aircraft.csv": 0, "04_aircraft/41_figures.csv": 1}
    d = d.assign(description="", _r=d["file"].map(rank).fillna(9)).sort_values("_r", kind="stable").drop_duplicates("column")[["column", "section", "kind", "options", "non_empty", "description"]]
    d["thesis_names"] = ""
    _out(_codes_dict(d), dst / "02_patents" / "data_dictionary.csv")
    # ---- 03_aircraft ----
    a = _rd(root, "04_aircraft/42_aircraft.csv").drop(columns=["is_design"], errors="ignore")
    a = _ids(a.rename(columns={"ad": "ua", "points_to_ad": "points_to_ua"}))
    a = _codes(a)
    if "main_figure" in a.columns:
        a["main_figure"] = a["main_figure"].map(lambda x: str(root / x) if x else "")
    extra = _not_approved(p, a)
    _out(pd.concat([a, extra], ignore_index=True).fillna(""), dst / "03_aircraft" / "aircraft_table.csv")
    f = _rd(root, "04_aircraft/41_figures.csv")
    idx = _rd(root, "index.csv")
    crop = idx.drop_duplicates(["aircraft_id", "fig_key"]).set_index(["aircraft_id", "fig_key"])
    key = list(zip(f["aircraft_id"], f["fig_key"]))
    cp = pd.Series([crop["crop_path"].get(k, "") for k in key], index=f.index)
    ap = pd.Series([crop["approved_path"].get(k, "") for k in key], index=f.index)
    f["image_path"] = cp.map(lambda x: str(root / x) if x else "")
    f["file_exists"] = f["image_path"].map(lambda x: str(bool(x) and Path(x).exists()))
    f["approved_copy_path"] = ap.map(lambda x: str(root / x) if x else "")
    f = _ids(f.rename(columns={"ad": "ua"}))
    _out(_codes(f), dst / "03_aircraft" / "figure_table.csv")
    trl = _ids(_rd(root, "04_aircraft/44_trl.csv"))
    scale = pd.Series(_NASA_TRL)
    t = pd.DataFrame({"aircraft_id": trl.aircraft_id, "patent_id": trl.patent_id, "aircraft_name": trl.aircraft_name, "company": trl.company})
    t = t.merge(a[["aircraft_id", "topType", "app_year"]], on="aircraft_id", how="left")
    t["trl"] = trl.evidence_trl.values
    t["nasa_definition"] = t["trl"].map(scale).fillna("")
    for new, old in [("trl_basis", "evidence_basis"), ("confidence", "evidence_confidence"), ("evidence_quote", "evidence_quote"), ("source", "evidence_source"),
                     ("programme_trl", "programme_trl"), ("arch_match", "arch_match"), ("public_arch", "public_arch"), ("note", "evidence_note"), ("programme_status", "programme_status"),
                     ("status_since", "status_since"), ("status_confidence", "status_confidence"), ("status_evidence", "status_evidence"), ("status_source", "status_source"), ("status_note", "status_note")]:
        t[new] = trl[old].values
    _out(_codes(_ids(t.fillna(""))), dst / "03_aircraft" / "trl" / "aircraft_trl.csv")
    # ---- 05_secondary/vfs ----
    da = _rd(root, V + "directory_aircraft.csv")
    base_cols = ["slug_key", "slug", "url", "list_name", "list_status", "evtol_class", "list_pos", "title", "model", "status", "company", "location", "website", "spec_aircraft_type", "spec_piloting",
                 "spec_capacity", "spec_cruise_speed", "spec_range", "spec_flight_time", "spec_propellers", "spec_electric_motors", "spec_power_source", "spec_fuselage", "spec_wings", "spec_windows",
                 "spec_landing_gear", "spec_safety_features", "spec_tail", "n_images", "page_status", "n_classes", "evtol_class_main"]
    _out(da[base_cols], dst / "05_secondary" / "vfs" / "aircraft.csv")
    pl = _rd(root, V + "directory_patent_links.csv").rename(columns={"aircraft_id": "aircraft_uid"})
    _out(_codes(_ids(pl)), dst / "05_secondary" / "vfs" / "patent_links.csv")
    dy = pd.DataFrame({"slug_key": da.slug_key, "list_name": da.list_name, "company": da.company, "status": da.status, "evtol_class": da.evtol_class, "dev_year": da.year_final, "url": da.url})
    _out(dy, dst / "05_secondary" / "vfs" / "aircraft_dev_year.csv")
    shutil.copy2(root / (V + "directory_pages.jsonl"), dst / "05_secondary" / "vfs" / "pages.jsonl")
    (dst / "05_secondary" / "vfs" / "readers").mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / (V + "directory_year_sentences.csv"), dst / "05_secondary" / "vfs" / "readers" / "evidence_ids.csv")
    # ---- external series (the yaml points here) ----
    e = dst / "external"
    cur = _rd(root, A + "aam_index_current.csv")
    _out(cur, e / "aam_reality_index" / "ari_may2026.csv")
    _out(_rd(root, A + "aam_index_history.csv"), e / "aam_reality_index" / "ari_history.csv")
    fund = cur[pd.to_numeric(cur["funding_musd"], errors="coerce").notna()][["oem", "funding_musd"]]
    _out(fund, e / "aam_reality_index" / "ari_funding_may2026.csv")
    cm = _rd(root, A + "aam_index_company_map.csv")
    _out(cm[["oem", "company_canonical", "note"]], e / "aam_reality_index" / "ari_company_map.csv")
    bl = _rd(root, C + "aviation_patent_baselines.csv")
    _out(_rd(root, C + "aviation_b64_by_priority_year.csv"), e / "aviation_baseline" / "b64_by_priority_year.csv")
    pw = e / "aviation_baseline" / "patseer_worldwide"
    for col, name in [("patseer_b64", "patseer_B64_worldwide_by_priority_year.csv"), ("patseer_section_b", "patseer_sectionB_worldwide_by_priority_year.csv"),
                      ("patseer_b64_excl_b64c29", "patseer_B64_noB64C29_worldwide_by_priority_year.csv"), ("patseer_b64_excl_b64u", "patseer_B64_noB64U_worldwide_by_priority_year.csv")]:
        s = bl[bl[col] != ""][["year", col]].sort_values("year", ascending=False)
        s.columns = ["Earliest Priority Year", "Total"]
        _out(s, pw / name, quoting=1)
    w = bl[bl["wipo_world"] != ""].rename(columns={"year": "y", "wipo_world": "world", "wipo_china": "CN", "wipo_world_excl_china": "exCN", "patseer_b64": "b64", "patseer_section_b": "B",
                                                    "china_share_pct": "CNshare%", "b64_per_10k_world_families": "b64_per10k", "section_b_share_pct": "B_share%"})
    _out(w[["y", "world", "CN", "exCN", "b64", "B", "CNshare%", "b64_per10k", "B_share%"]], pw / "baselines_2000_2023.csv")
    _out(_rd(root, C + "grant_status_by_priority_year.csv"), e / "lapse_check" / "status_by_priority_year.csv")
    lag = pd.read_csv(root / (C + "grant_lag_summary.csv"), dtype=str, keep_default_na=False)
    _out(lag.rename(columns={lag.columns[0]: ""}), e / "lapse_check" / "grant_lag_summary.csv")
    if (root / (C + "funding_by_period.csv")).exists():   # not part of the public dataset (not used by the analysis)
        _out(_rd(root, C + "funding_by_period.csv"), e / "investment" / "aam_funding_by_period.csv")
    _out(_rd(root, C + "market_forecasts.csv"), e / "investment" / "evtol_market_forecasts.csv")
    _out(_rd(root, C + "sector_events.csv"), e / "sector_events" / "sector_events.csv")


def _codes_dict(d: pd.DataFrame) -> pd.DataFrame:
    m = d["column"].eq("topType")
    d.loc[m, "options"] = d.loc[m, "options"].str.replace(r"\bTP=", "TR=", regex=True).str.replace(r"\bTF=", "TB=", regex=True)
    return d


def _not_approved(p: pd.DataFrame, a: pd.DataFrame) -> pd.DataFrame:
    """The patents without an approved aircraft, as the analysis table lists them (one row, is_approved False)."""
    have = set(a["patent_id"])
    q = p[~p["patent_id"].isin(have)].copy()
    aid = q["patent_id"] + "_ua1"
    return pd.DataFrame({"patent_id": q["patent_id"], "aircraft_id": aid, "ua": "1", "n_variants": "0", "batch": q["batch"], "company": q["company"], "aircraft_name": aid,
                         "name_is_real": "False", "variant": "1", "variant_id": q["patent_id"], "reason_source": "human", "reason": q["reason"], "reason_human": q["reason"],
                         "is_approved": "False", "is_primary": "True", "dup_of_missing": "False", "n_figures": "0", "n_approved": "0", "n_approved_this_variant": "0", "n_fig_placeholders": "0"})


def script_outputs(root: Path, out: Path = SCRIPT_OUT):
    """The four lists notebook 60 wrote (DOMAIN, YEAR, TRL, COMPANY_MAP), made from the public tables."""
    out.mkdir(parents=True, exist_ok=True)
    da = _rd(root, V + "directory_aircraft.csv")
    yr = da[["slug_key", "evtol_class", "year_script", "year_sentence", "year_author", "year_final", "year_source"]]
    yr.columns = ["slug_key", "evtol_class", "script_year", "evidence_sentence", "author_year", "final_year", "source"]
    _out(yr, out / "YEAR.csv")
    dm = da[["slug_key", "domain_class5", "domain_status", "domain_status_group", "domain_not_combustion", "domain_crewed", "domain_in_domain", "domain_patented"]]
    dm.columns = ["slug_key", "class5", "status", "status_group", "not_combustion", "crewed", "in_domain", "patented"]
    _out(dm, out / "DOMAIN.csv")
    t = _rd(root, "04_aircraft/44_trl.csv")
    tt = t[["aircraft_id", "patent_id", "aircraft_name", "company", "directory_page", "directory_sentence", "script_trl", "author_trl", "trl", "trl_source"]]
    tt.columns = ["aircraft_id", "patent_id", "aircraft_name", "company", "script_page", "script_sentence", "script_trl", "author_trl", "final_trl", "source"]
    _out(_ids(tt), out / "TRL.csv")
    cm = _rd(root, A + "aam_index_company_map.csv")
    _out(cm[["oem", "script_match", "author", "company_canonical", "note"]], out / "COMPANY_MAP.csv")


def ensure_compat(root, output) -> Path:
    """The mirror of ``root`` this code reads; rebuilt when any public file is newer than it."""
    root, dst = Path(root), Path(output) / "_dataset_public_compat"
    stamp = dst / ".built"
    newest = max(p.stat().st_mtime for p in root.rglob("*") if p.is_file() and "05_images" not in p.parts)
    if stamp.exists() and stamp.stat().st_mtime >= newest:
        script_outputs(root)
        return dst
    if dst.exists():
        shutil.rmtree(dst)
    _tables(root, dst)
    script_outputs(root)
    stamp.write_text(f"mirror of {root}\n")
    return dst
