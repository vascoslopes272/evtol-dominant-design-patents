"""Numbers for the supplementary material of paper P1 (S1-S4 and the pending main-text numbers), recomputed on the 621 designs.

    EVTOL_DATASET=<path to eVTOL_dataset> PYTHONPATH=2_analysis/src python 2_analysis/scripts/34_supplementary_numbers.py

Computes sections B (S2), C (S1), E15-E17 from the design table with the thesis functions (nothing is rewritten) and reads the
10 000-permutation tables of 31_family_F_numbers.py for section D. Writes one CSV per table to numbers/supplementary_csv/ and the
value register numbers/supplementary_csv/_values.csv (value, script, file, definition). The markdown file is assembled by
35_supplementary_markdown.py from these CSVs, the robustness summaries (36_robustness_numbers.py) and the code reading.
No rounding beyond what each table says. Nothing is interpreted.
"""
from __future__ import annotations

import os as _os
from pathlib import Path as _Path
_REPO = _Path(__file__).resolve().parents[2]
_SUPP = _os.environ.get("SUPP_OUT", str(_REPO / "results" / "2_analysis" / "numbers"))
_DS = _os.environ.get("EVTOL_DATASET", str(_REPO.parent / "eVTOL_dataset"))
for _d in ("pending_csv", "supplementary_csv"):
    _os.makedirs(_os.path.join(_SUPP, _d), exist_ok=True)
import json
import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
import core  # noqa: E402

DS_ROOT = Path(os.environ.get("EVTOL_DATASET", _DS))
OUT = Path(os.environ.get("SUPP_OUT", _SUPP)) / "supplementary_csv"
FF = REPO / "results" / "2_analysis" / "family_F"
SCRIPT = "2_analysis/scripts/34_supplementary_numbers.py"
VALUES = []


def reg(vid, value, source, definition, file=""):
    VALUES.append({"id": vid, "value": value, "script": source, "file": file, "definition": definition})


def save(name, df, note=""):
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / name, index=False)
    return df


def main():
    base = core.load()
    ctx = core.context(base, base.master)
    m, ds, v = base.m, ctx.ds, ctx.v
    fr = m.frames
    q4 = m.q1 if False else __import__("viz.thesis_q4", fromlist=["x"])
    WIN = ctx.WIN_NAMES
    live = v["aircraft_id"].map(fr.patent_state(ds, v)["in_force"]).astype(bool)
    v = v.assign(protected=live.to_numpy())

    # ------------------------------------------------------------------ B4, B5: agreement with public aircraft
    pub = q4.public_frame(ctx)
    pw = q4.pairwise(ctx)
    lab = q4.public_labels(ctx)
    lab = lab[lab["text"].ne("")]
    named = v["name_is_real"].fillna(False).astype(bool)
    linked = fr.linked_aircraft_ids(v, ctx.cfg)
    nc = q4.name_coverage(ctx)
    save("B4_named_and_compared.csv", nc)
    reg("B4.named", int(named.sum()), SCRIPT, "designs with a real product name (name_is_real)", "B4_named_and_compared.csv")
    reg("B4.compared", int(len(pub)), SCRIPT + " via viz.thesis_q4.public_frame -> frames.public_arch_frame",
        "designs compared with the public aircraft in the agreement table (every row of public_frame)", "B4_named_and_compared.csv")
    reg("B4.linked_to_page", int(v["aircraft_id"].isin(linked).sum()), SCRIPT, "designs linked to an evtol.news page (frames.linked_aircraft_ids)")
    from lib import association
    rows = []
    kap = {"drawing label against the public aircraft": ("drawing", "public vs drawing"),
           "patent text against the public aircraft": ("text", "public vs text"),
           "drawing label against the patent text": ("drawing", "text")}
    for _, r in pw.iterrows():
        a_, b_ = kap[r["comparison"]]
        n_, share = association.raw_agreement(lab[a_], lab[b_])
        rows.append({"comparison": r["comparison"], "designs compared": int(r["of"]), "designs that agree": int(r["agree"]),
                     "raw agreement (agree / compared)": int(r["agree"]) / int(r["of"]),
                     "Cohen's kappa (unrounded)": association.cohen_kappa(lab[a_], lab[b_]),
                     "Wilson 95 % interval with finite-population correction": r["95 % interval"]})
    ag = save("B5_agreement_kappa.csv", pd.DataFrame(rows))
    for _, r in ag.iterrows():
        reg(f"B5.{r['comparison']}", f"{r['designs that agree']} of {r['designs compared']}; kappa {r['Cohen\'s kappa (unrounded)']}",
            SCRIPT + " via viz.thesis_q4.pairwise / public_labels", "agreements, raw agreement and Cohen's kappa on the architecture label", "B5_agreement_kappa.csv")
    # match column breakdown
    mc = pub["match"].astype(str).value_counts().rename_axis("match value in public_frame").reset_index(name="designs")
    save("B5b_public_match_values.csv", mc)

    # ------------------------------------------------------------------ B6: designs per cohort, base, level, configuration
    keys = fr.dd_level_keys(ds, v)
    LV = {"A0": "L1 (A, architecture)", "A1t": "L2 (A.W.T)", "A0c": "L3 (A.U)", "family_b": "F (family, yes/no)"}
    rows = []
    for w in WIN:
        s = v[v["window"].eq(w)]
        rows.append({"cohort": w, "all designs": int(len(s)), "protected designs (active patent)": int(s["protected"].sum()),
                     "designs with an architecture": int(s["topType"].notna().sum()),
                     "protected with an architecture": int((s["protected"] & s["topType"].notna()).sum())})
    rows.append({"cohort": "all cohorts", "all designs": int(len(v)), "protected designs (active patent)": int(v["protected"].sum()),
                 "designs with an architecture": int(v["topType"].notna().sum()), "protected with an architecture": int((v["protected"] & v["topType"].notna()).sum())})
    co = save("B6a_designs_per_cohort_and_base.csv", pd.DataFrame(rows))
    reg("B6.cohorts", "; ".join(f"{r['cohort']}: {r['all designs']} all / {r['protected designs (active patent)']} protected" for _, r in co.iterrows()),
        SCRIPT, "designs per priority-year cohort; protected = at least one linked patent whose status is known and not inactive (frames.patent_state in_force)", "B6a_designs_per_cohort_and_base.csv")
    rows = []
    for lvl in ("A0", "A1t", "A0c", "family_b"):
        k = keys[lvl].loc[v.index]
        for cfgv in sorted(k.dropna().unique(), key=lambda x: str(x)):
            sel = k.eq(cfgv)
            name = fr._key_words(cfgv, lvl) if hasattr(fr, "_key_words") else str(cfgv)
            row = {"level": LV[lvl], "level id": lvl, "configuration key": str(cfgv), "configuration": name,
                   "designs, all": int(sel.sum()), "designs, protected": int((sel & v["protected"]).sum())}
            for w in WIN:
                row[f"all {w}"] = int((sel & v["window"].eq(w)).sum())
                row[f"protected {w}"] = int((sel & v["window"].eq(w) & v["protected"]).sum())
            rows.append(row)
    cf = save("B6b_designs_per_configuration_level_base_cohort.csv", pd.DataFrame(rows))
    sumry = cf.groupby("level").agg(configurations=("configuration key", "count"), designs=("designs, all", "sum")).reset_index()
    save("B6c_configurations_per_level.csv", sumry)
    reg("B6.levels", "; ".join(f"{r['level']}: {r['configurations']} configurations, {r['designs']} designs" for _, r in sumry.iterrows()),
        SCRIPT + " via frames.dd_level_keys", "distinct configurations present and designs keyed at each level (designs without a key are left out)", "B6c_configurations_per_level.csv")

    # ------------------------------------------------------------------ B7: dimensions answered
    sel_f = fr.selected_fields(ds)[["name", "answered"]].rename(columns={"name": "dimension"})
    f15 = fr.form_frame15(ds)
    dist = pd.DataFrame({"dimension": [c for c in f15.columns if c != "aircraft_id"],
                         "answered": [int(f15[c].notna().sum()) for c in f15.columns if c != "aircraft_id"]})
    save("B7a_design_space_table_dimensions_answered.csv", sel_f.assign(**{"answered for at least 500 designs": sel_f["answered"] >= 500}))
    save("B7b_distance_dimensions_answered.csv", dist.assign(**{"answered for at least 500 designs": dist["answered"] >= 500}))
    reg("B7.design_space_table", f"{int((sel_f['answered'] >= 500).sum())} of {len(sel_f)}", SCRIPT + " via frames.selected_fields",
        "dimensions of the design-space table answered for at least 500 designs", "B7a_design_space_table_dimensions_answered.csv")
    reg("B7.distance", f"{int((dist['answered'] >= 500).sum())} of {len(dist)}", SCRIPT + " via frames.form_frame15",
        "dimensions of the 15-dimension distance answered for at least 500 designs (non-null cells)", "B7b_distance_dimensions_answered.csv")

    # ------------------------------------------------------------------ C8: the funnel and the counts
    pat = pd.read_csv(DS_ROOT / "03_patents" / "33_patents.csv", low_memory=False)
    air = pd.read_csv(DS_ROOT / "04_aircraft" / "42_aircraft.csv", low_memory=False)
    des = pd.read_csv(DS_ROOT / "04_aircraft" / "45_designs.csv", low_memory=False)
    exp = pd.read_excel(DS_ROOT / "01_query" / "patseer_1639_2026-06-08.xlsx")
    exp.columns = [str(c).strip() for c in exp.columns]
    cnt = ds.counts
    fun = [("records (rows) in the PatSeer export", len(exp), "01_query/patseer_1639_2026-06-08.xlsx: number of rows"),
           ("distinct Simple Family ID in the export", int(exp["Simple Family ID"].nunique()), "column Simple Family ID"),
           ("distinct Record Number in the export", int(exp["Record Number"].nunique()), "column Record Number"),
           ("patent families in file 33 (one row per family)", len(pat), "03_patents/33_patents.csv rows"),
           ("patents acquired (ds.counts)", cnt["patents_acquired"], "viz.data counts"),
           ("disapproved at labelling (T1)", int((~pat["is_approved"].astype(bool)).sum()), "33_patents.is_approved == False"),
           ("approved at labelling", int(pat["is_approved"].astype(bool).sum()), "33_patents.is_approved == True"),
           ("approved patents whose every aircraft is 'but similar', set aside (gate)", cnt["patents_gated_out"], "ds.counts patents_gated_out"),
           ("representative patents after the gate (ds.counts patents_approved)", cnt["patents_approved"], "ds.counts patents_approved"),
           ("aircraft observations on approved patents", cnt["approved_variants"], "ds.counts approved_variants"),
           ("aircraft observations after the gate, primary (unique designs)", cnt["primary_approved_variants"], "ds.counts primary_approved_variants"),
           ("designs in the analysis table (len(ctx.v))", len(v), "frames.base"),
           ("designs in 45_designs.csv", len(des), "04_aircraft/45_designs.csv rows"),
           ("patents behind the designs (primary patents)", int(v["patent_id"].nunique()), "unique patent_id in ctx.v"),
           ("whole-aircraft figures approved (T2)", cnt["approved_figures"], "ds.counts approved_figures")]
    # reasons for disapproval, duplicates
    reasons = pat.loc[~pat["is_approved"].astype(bool), "reason"].fillna("(blank)").value_counts().rename_axis("reason").reset_index(name="patents")
    save("C8b_disapproval_reasons.csv", reasons)
    dup = pat["dup_type_name"].fillna("(not a duplicate)").value_counts().rename_axis("duplicate type (file 33)").reset_index(name="patents")
    save("C8c_duplicate_types_file33.csv", dup)
    prim = air["is_primary"].astype(bool)
    dup_nm = air["dup_type_name"].fillna("")
    dd = pd.DataFrame([{"approved aircraft rows (file 42, on the 1 108 approved patents)": len(air),
                        "non-primary rows removed as duplicates (types D1 + D2)": int((~prim).sum()),
                        "  of which D1": int(dup_nm[~prim].eq("D1").sum()), "  of which D2": int(dup_nm[~prim].eq("D2").sum()),
                        "primary rows (is_primary)": int(prim.sum()),
                        "  primary rows that carry a D3 flag (kept as designs of their own)": int((prim & dup_nm.eq("D3")).sum()),
                        "primary rows set aside by the gate (every aircraft 'but similar')": int((prim & ~air["is_design"].astype(bool)).sum()),
                        "designs (is_design)": int(air["is_design"].astype(bool).sum())}])
    save("C8d_aircraft_rows_duplicates.csv", dd.T.reset_index().set_axis(["step", "count"], axis=1))
    fun += [("aircraft rows on the 1 108 approved patents (file 42)", len(air), "42_aircraft.csv rows (all is_approved)"),
            ("duplicates removed (non-primary rows, D1 41 + D2 381)", int((~prim).sum()), "42_aircraft.is_primary == False; dup_type_name D1/D2"),
            ("primary aircraft rows", int(prim.sum()), "42_aircraft.is_primary == True (797 = rows of file 43)"),
            ("primary rows set aside by the gate", int((prim & ~air["is_design"].astype(bool)).sum()), "is_primary and not is_design"),
            ("designs (is_design)", int(air["is_design"].astype(bool).sum()), "42_aircraft.is_design == True")]
    # assignees and inventors
    per = v.groupby("assignee")["aircraft_id"].nunique().sort_values(ascending=False)
    nm = v[v["named"]].groupby("firm").size()
    fun += [("assignees = organisations (companies and universities) with at least one design", int(len(nm)), "ctx.v.firm over ctx.v.named; the 198 of the paper (thesis_q2.py org_n)"),
            ("organisations with one design", int((nm == 1).sum()), "same; the 130 of the paper (thesis_q2.py single_n)"),
            ("designs of named organisations (companies + universities)", int(v["named"].sum()), "ctx.v.named; 397 company + 43 university designs in thesis_q2.py"),
            ("largest organisation and its designs", f"{nm.sort_values(ascending=False).index[0]}: {int(nm.max())}", "same"),
            ("distinct raw 'assignee' strings over all 621 designs (not the paper's count)", int(len(per)), "ctx.v.assignee, includes individuals and spelling variants of one firm")]
    pid = set(v["patent_id"].astype(str))
    key = "Record Number"
    ex2 = exp.copy()
    ex2["_pid"] = ex2[key].astype(str)

    def inv_set(frame):
        s = set()
        for x in frame["Inventors"].dropna().astype(str):
            for p in re.split(r"[;|]", x):
                p = re.sub(r"\s+", " ", p).strip().lower()
                if p:
                    s.add(p)
        return s
    inv_all = inv_set(ex2)
    inv_des = inv_set(ex2[ex2["_pid"].isin(pid)])
    fun += [("distinct inventor names, all 1 639 export rows", len(inv_all), "export column Inventors split on ';' or '|', lower-cased, whitespace collapsed; no disambiguation of people"),
            ("distinct inventor names, rows of the primary patents of the 621 designs", len(inv_des), "same, rows whose Record Number is a primary patent of ctx.v"),
            ("export rows matched to primary patents of the designs", int(ex2["_pid"].isin(pid).sum()), "Record Number in ctx.v.patent_id")]
    fu = save("C8a_funnel.csv", pd.DataFrame(fun, columns=["step or count", "value", "definition / source"]))
    for _, r in fu.iterrows():
        reg("C8." + r["step or count"], r["value"], SCRIPT, r["definition / source"], "C8a_funnel.csv")

    # ------------------------------------------------------------------ E15: entrants (company and university designs)
    ent = fr.named_entries(v, WIN)
    rows = []
    for wn in WIN:
        s = ent[ent["window"].eq(wn)]
        rows.append({"cohort": wn, "designs of named organisations (companies and universities)": int(len(s)),
                     "of first-time filers (entrants, definition b)": int(s["first_time"].sum()),
                     "returning": int((~s["first_time"]).sum()),
                     "share of entrants (unrounded)": float(s["first_time"].mean()) if len(s) else np.nan,
                     "organisations active": int(s["firm"].nunique()),
                     "organisations whose first design falls in the cohort": int(s.loc[s["first_time"], "firm"].nunique())})
    e15 = save("E15_entrant_design_shares.csv", pd.DataFrame(rows))
    for wn in ("2016-19", "2020-23"):
        r = e15[e15["cohort"].eq(wn)].iloc[0]
        reg(f"E15.{wn}", f"{r['of first-time filers (entrants, definition b)']} of {r['designs of named organisations (companies and universities)']} = {r['share of entrants (unrounded)']}",
            SCRIPT + " via frames.named_entries (file: viz/frames.py:2969); the paper text value comes from viz/thesis_q2.py:398-401",
            "share of designs of named organisations (v.named) whose organisation's earliest cohort with a design is this cohort", "E15_entrant_design_shares.csv")
    # firms level: definition b of 30_entrants_two_definitions.py
    try:
        e30 = pd.read_csv(REPO / "results" / "2_analysis" / "entrants" / "entrants_two_definitions.csv")
        save("E15b_entrant_firms_two_definitions_copy.csv", e30)
    except Exception:
        pass
    # does the 'named' flag cover companies and universities?
    ft = v.groupby("filer_type").size().rename("designs").reset_index() if "filer_type" in v.columns else pd.DataFrame()
    if len(ft):
        save("E15c_filer_types.csv", ft)

    # ------------------------------------------------------------------ E16: dropping the largest assignee
    lev = fr.firm_leverage_table(v, WIN)
    levc = fr.firm_leverage_classes(v, WIN, top=8, lev=lev)
    save("E16a_firm_leverage_ranking.csv", lev)
    save("E16b_share_shift_when_firm_dropped.csv", levc)
    l1, l2 = lev.iloc[0], lev.iloc[1]
    reg("E16.first", f"{l1['firm']}: {l1['shift magnitude (pp)']:.2f} pp ({l1['class most moved']}); unrounded shift {l1['shift if the firm is dropped (pp)']}",
        SCRIPT + " via frames.firm_leverage_table (viz/frames.py:2858); text value thesis_q2.py lev1_pp", "largest all-years class-share change in points when one firm with >= 3 designs is dropped; firm and class are those of the ranking's first row", "E16a_firm_leverage_ranking.csv")
    reg("E16.second", f"{l2['firm']}: {l2['shift magnitude (pp)']:.2f} pp ({l2['class most moved']}); unrounded shift {l2['shift if the firm is dropped (pp)']}",
        SCRIPT + " via frames.firm_leverage_table; text value thesis_q2.py lev2_pp", "same for the second row of the ranking", "E16a_firm_leverage_ranking.csv")
    bell = levc[levc["firm"].eq(l1["firm"])]
    save("E16c_first_firm_all_classes.csv", bell)
    # numerator / denominator for the first two rows
    rows = []
    for _, r in lev.head(2).iterrows():
        f, c = r["firm"], r["class most moved"]
        with_ = v["topType"].eq(c)
        wo = v[v["company_canonical"].ne(f)]
        rows.append({"firm dropped": f, "class most moved": c, "designs of the firm": int(v["company_canonical"].eq(f).sum()),
                     "class designs, all": int(with_.sum()), "analysis set": int(v["topType"].notna().sum()),
                     "class share with the firm": float(with_.sum() / v["topType"].notna().sum()),
                     "class designs without the firm": int(wo["topType"].eq(c).sum()), "analysis set without the firm": int(wo["topType"].notna().sum()),
                     "class share without the firm": float(wo["topType"].eq(c).sum() / wo["topType"].notna().sum()),
                     "shift in points (without minus with)": float((wo["topType"].eq(c).sum() / wo["topType"].notna().sum() - with_.sum() / v["topType"].notna().sum()) * 100)})
    save("E16d_numerators_denominators.csv", pd.DataFrame(rows))
    # Bell without: per cohort and architecture, every shift (grid), to find any value in the paper
    grid = []
    big = l1["firm"]
    for wn in WIN:
        s = v[v["window"].eq(wn) & v["topType"].notna()]
        s2 = s[s["company_canonical"].ne(big)]
        for c in sorted(s["topType"].unique()):
            a, b = s["topType"].eq(c).mean(), s2["topType"].eq(c).mean()
            grid.append({"cohort": wn, "architecture": c, "designs in cohort": len(s), "with": int(s["topType"].eq(c).sum()),
                         "designs without the firm": len(s2), "without": int(s2["topType"].eq(c).sum()),
                         "share with (%)": a * 100, "share without (%)": b * 100, "change (points)": (b - a) * 100})
    save("E16e_first_firm_grid_cohort_architecture.csv", pd.DataFrame(grid))

    # ------------------------------------------------------------------ E17: regions
    w = fr.regional_frame(ds, v)
    ln = fr.region_lean(w)
    save("E17a_region_F_share.csv", ln[["region"] + [c for c in ln.columns if c.startswith("F ")]])
    tot = int(v["window"].eq("2020-23").sum())
    rows = []
    for reg_ in fr.REGIONS:
        s = w[w["region3"].eq(reg_) & w["window"].eq("2020-23")]
        rows.append({"region": reg_, "designs in 2020-23 (region3)": int(len(s)), "of all designs in 2020-23": tot,
                     "share of the cohort": len(s) / tot, "F base 2020-23 (designs with F defined)": int(s["F"].notna().sum()),
                     "F aircraft 2020-23": int(s["F"].dropna().sum())})
    r17 = pd.DataFrame(rows)
    r17.loc[len(r17)] = {"region": "three regions together", "designs in 2020-23 (region3)": int(r17["designs in 2020-23 (region3)"].sum()),
                         "of all designs in 2020-23": tot, "share of the cohort": r17["designs in 2020-23 (region3)"].sum() / tot,
                         "F base 2020-23 (designs with F defined)": int(r17["F base 2020-23 (designs with F defined)"].sum()),
                         "F aircraft 2020-23": int(r17["F aircraft 2020-23"].sum())}
    r17.loc[len(r17)] = {"region": "outside the three regions or without region", "designs in 2020-23 (region3)": tot - int(r17.iloc[:3]["designs in 2020-23 (region3)"].sum()),
                         "of all designs in 2020-23": tot, "share of the cohort": 1 - r17.iloc[:3]["designs in 2020-23 (region3)"].sum() / tot,
                         "F base 2020-23 (designs with F defined)": np.nan, "F aircraft 2020-23": np.nan}
    save("E17b_region_denominators_2020_23.csv", r17)
    ap = r17[r17["region"].eq("Asia-Pacific")].iloc[0]
    reg("E17.asia_pacific", f"{ap['designs in 2020-23 (region3)']} of {ap['of all designs in 2020-23']}", SCRIPT + " via frames.regional_frame (viz/frames.py), frames.region_lean (frames.py:3270)",
        "designs of 2020-23 whose applicant region3 is Asia-Pacific, over all designs of 2020-23", "E17b_region_denominators_2020_23.csv")
    reg("E17.three_regions", int(r17.iloc[3]["designs in 2020-23 (region3)"]), SCRIPT, "designs of 2020-23 in North America, Europe or Asia-Pacific", "E17b_region_denominators_2020_23.csv")

    # ------------------------------------------------------------------ D9: long and wide tables from the 10 000-permutation run
    note = (FF / "run_note.txt").read_text()
    reg("D9.run_note", note.replace("\n", "; "), "2_analysis/scripts/31_family_F_numbers.py --perms 10000", "permutations, seed and designs behind percentiles_*.csv", "family_F/run_note.txt")
    pb = pd.read_csv(FF / "percentiles_balance.csv")
    pdq = pd.read_csv(FF / "percentiles_disparity.csv")
    pav = pd.read_csv(FF / "percentiles_disparity_protected_vs_all.csv")
    LVN = {"A0": "L1", "A1t": "L2", "A0c": "L3", "family_b": "F"}
    pb["L"] = pb["level"].map(LVN)
    pdq["L"] = pdq["level"].map(LVN)
    bal = pb[["L", "level", "level name", "base", "window", "aircraft", "top archetype", "top share", "D2", "percentile of the observed D2 (share of shuffles at or below)",
              "D2 permutation low", "D2 permutation high", "below band", "partial"]].rename(columns={
        "top share": "share of the leading configuration", "D2": "Hill 2D rarefied to 40 (raw, mean of 1000 draws)",
        "percentile of the observed D2 (share of shuffles at or below)": "percentile of the observed 2D in its permutation distribution",
        "D2 permutation low": "2D band low (2.5th pct)", "D2 permutation high": "2D band high (97.5th pct)", "below band": "2D below band"})
    dq = pdq[pdq["weighting"].eq("w15")][["L", "level", "base", "window", "aircraft", "Q", "Q of the earliest windows", "ΔQ",
                                         "percentile of the observed dQ (share of shuffles at or below)", "ΔQ permutation low", "ΔQ permutation high", "below band"]].rename(columns={
        "Q of the earliest windows": "Q0 (mean of Q of the two earliest cohorts)", "percentile of the observed dQ (share of shuffles at or below)": "percentile of the observed dQ",
        "ΔQ permutation low": "dQ band low (2.5th pct)", "ΔQ permutation high": "dQ band high (97.5th pct)", "below band": "dQ below band", "ΔQ": "dQ"})
    # F row of dQ is C's row (frames.dd_form_table), mark it
    dq["note"] = np.where(dq["L"].eq("F"), "F is C's row: Q uses no archetype (frames.py:2375)", "")
    long = bal.merge(dq.drop(columns=["level", "aircraft"]), on=["L", "base", "window"], how="left", suffixes=("", " (dQ)"))
    save("D9_long_all_levels_all_bases.csv", long)
    for base_name in ("all designs", "actively protected"):
        for L in ("L1", "L2", "L3", "F"):
            sub = long[(long["L"] == L) & (long["base"] == base_name)]
            save(f"D9_{L}_{'all' if base_name.startswith('all') else 'protected'}.csv", sub)
    save("D9_dq_weighting_w34_for_the_record.csv", pdq[pdq["weighting"].eq("w34")])
    save("D9_protected_2020_23_against_all_designs_baseline.csv", pav)
    # wide table ready for LaTeX: one row per level and base, columns per cohort (share, 2D [lo, hi] pct, dQ [lo, hi] pct)
    def cell(r, cols):
        return r
    wide_rows = []
    for L in ("L1", "L2", "L3", "F"):
        for base_name in ("all designs", "actively protected"):
            sub = long[(long["L"] == L) & (long["base"] == base_name)].set_index("window")
            row = {"level": L, "base": base_name}
            for wn in WIN:
                if wn in sub.index:
                    r = sub.loc[wn]
                    row[f"{wn} n"] = int(r["aircraft"])
                    row[f"{wn} share"] = f"{r['share of the leading configuration']:.3f}"
                    row[f"{wn} 2D"] = f"{r['Hill 2D rarefied to 40 (raw, mean of 1000 draws)']:.2f}"
                    row[f"{wn} 2D band"] = f"{r['2D band low (2.5th pct)']:.2f}--{r['2D band high (97.5th pct)']:.2f}"
                    row[f"{wn} 2D pct"] = f"{r['percentile of the observed 2D in its permutation distribution']:.1f}"
                    row[f"{wn} dQ"] = f"{r['dQ']:+.4f}" if pd.notna(r["dQ"]) else ""
                    row[f"{wn} dQ band"] = f"{r['dQ band low (2.5th pct)']:+.4f}..{r['dQ band high (97.5th pct)']:+.4f}" if pd.notna(r["dQ"]) else ""
                    row[f"{wn} dQ pct"] = f"{r['percentile of the observed dQ']:.1f}" if pd.notna(r["dQ"]) else ""
                else:
                    for k in ("n", "share", "2D", "2D band", "2D pct", "dQ", "dQ band", "dQ pct"):
                        row[f"{wn} {k}"] = "not computed (< 10 designs)"
            wide_rows.append(row)
    wide = save("D9_wide.csv", pd.DataFrame(wide_rows))
    # LaTeX
    tex = ["% generated by 34_supplementary_numbers.py; columns per cohort: n, leading share, 2D [band] pct, dQ [band] pct",
           "\\begin{tabular}{llr" + "rrrr" * 0 + "}"]
    tex = ["% generated by 34_supplementary_numbers.py from D9_long_all_levels_all_bases.csv",
           "% one block per cohort row; cells: leading share | 2D (band low--high, percentile) | dQ (band low..high, percentile)",
           "\\begin{tabular}{lllrrrrr}", "Level & Base & Cohort & $n$ & Share & $^2D$ & $^2D$ band (pct) & $\\Delta Q$ [band] (pct) \\\\", "\\hline"]
    for _, r in long.sort_values(["L", "base"]).iterrows():
        dqs = "" if pd.isna(r["dQ"]) else f"{r['dQ']:+.4f} [{r['dQ band low (2.5th pct)']:+.4f}, {r['dQ band high (97.5th pct)']:+.4f}] ({r['percentile of the observed dQ']:.1f})"
        tex.append(f"{r['L']} & {r['base']} & {r['window']} & {int(r['aircraft'])} & {r['share of the leading configuration']:.3f} & "
                   f"{r['Hill 2D rarefied to 40 (raw, mean of 1000 draws)']:.2f} & [{r['2D band low (2.5th pct)']:.2f}, {r['2D band high (97.5th pct)']:.2f}] ({r['percentile of the observed 2D in its permutation distribution']:.1f}) & {dqs} \\\\")
    tex.append("\\end{tabular}")
    (OUT / "D9_wide_latex.tex").write_text("\n".join(tex) + "\n", encoding="utf-8")

    # ------------------------------------------------------------------ E: what the replicas use for entrants (named_entries is on ctx.v, which the replicas do not touch)
    pd.DataFrame(VALUES).to_csv(OUT / "_values.csv", index=False)
    print(json.dumps({"values": len(VALUES)}))


if __name__ == "__main__":
    main()
