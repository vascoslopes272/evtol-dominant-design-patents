"""The numbers of paper item 4, collected in one place from the results of notebooks 21-29 and the design table.

    EVTOL_DATASET=<path to eVTOL_dataset> python 32_paper_numbers.py

Reads results/2_analysis/freeze/csv (run 20_run_all.sh first) and the design table. Writes results/2_analysis/paper_numbers/paper_numbers.md
and the same tables as CSV. Nothing is recomputed that a notebook already computes; the few counts that are not in a table are
computed here from the design table.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
import core  # noqa: E402

CSV = REPO / "results" / "2_analysis" / "freeze" / "csv"
OUT = REPO / "results" / "2_analysis" / "paper_numbers"
WINDOWS = ["<= 2011", "2012-15", "2016-19", "2020-23", "2024-26 (partial)"]


def rd(name):
    return pd.read_csv(CSV / f"{name}.csv")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    base = core.load()
    ctx = core.context(base, base.master)
    fr = base.base if False else base.m.frames
    parts = []

    def add(title, df, note=""):
        df.to_csv(OUT / (re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_") + ".csv"), index=False)
        parts.append(f"## {title}\n\n{note}\n\n{df.to_markdown(index=False)}\n")

    # 1. the three largest architectures per cohort
    sh = rd("q6_architecture_shares_by_cohort")
    sh.insert(0, "cohort", WINDOWS[:len(sh)])
    rows = []
    for _, r in sh.iterrows():
        arch = r.drop(["cohort", "designs", "Other"], errors="ignore").astype(float).sort_values(ascending=False)
        top = arch.head(3)
        rows.append({"cohort": r["cohort"], "designs": int(r["designs"]), "largest three": ", ".join(f"{k} {v:.1%}" for k, v in top.items()),
                     "sum of the three": f"{top.sum():.1%}"})
    add("1. Three largest architectures per cohort", pd.DataFrame(rows), "Architecture codes as the dataset names them (TR = TP, TB = TF in the compat layer).")

    # 2. maximum share at architecture level per year
    d = base.m.q7._data(ctx)["dy"]
    a = d[d["level id"].eq("A0") & d["base"].eq("all")][["priority year", "aircraft", "its share", "read"]].copy()
    add("2. Largest architecture share per priority year (all designs)", a, f"Maximum over the years read: {a[a['read'].astype(bool)]['its share'].astype(float).max():.1%}.")

    # 3. balance of the earliest cohorts at architecture level, and dQ with band edges at the three levels
    bal = rd("q7_condition2_balance")
    add("3a. Balance (2D) per cohort and level", bal[["level", "cohort", "aircraft", "D2", "D2 permutation low", "D2 permutation high", "below band"]])
    det = rd("q7_verdict_detail")
    keep = [c for c in det.columns if c in ("base", "level") or c.startswith("ΔQ") or c.startswith("²D")]
    add("3b. dQ and band edges, 2020-23, three levels and F", det[keep])

    # 4. trends: rho and Holm p
    add("4a. Share trends by architecture (Spearman, Holm)", rd("q6_share_trend_spearman"))
    tr = rd("q6_driver_trends")
    pick = tr[tr["trace"].str.contains("boom|propulsor|tilt|duct", case=False, regex=True)]
    add("4b. Driver trends inside architectures (Spearman, Holm)", pick[["trace", "architecture", "code", "aircraft", "first cohort", "first value", "2020-23 value", "rho", "p", "p_holm", "movement"]])
    add("4c. Share of CVT designs with propulsors on booms", rd("q6_cvt_units_on_booms"))
    add("4d. Median propulsor units by cohort", rd("q6_propulsor_units_median_by_cohort"))

    # 5. assignees
    v = ctx.v
    per = v.drop_duplicates("aircraft_id").groupby("assignee").size().sort_values(ascending=False)
    top1 = rd("q2_largest_filers_share").head(1)
    asg = pd.DataFrame([{"assignees (designs)": int(len(per)), "with one design": int((per == 1).sum()),
                         "largest assignee": per.index[0], "its designs": int(per.iloc[0]), "its share of designs": round(float(per.iloc[0] / per.sum()), 3),
                         "designs": int(per.sum())}])
    add("5. Assignees", asg, "From the design table (aircraft_id, assignee as recorded). The patent-level view is in q2_largest_filers_share.csv.")
    wb = rd("q7_iii1_without_bell")
    add("5b. Without Bell / Textron", wb[wb["table"].notna() & wb["table"].astype(str).str.startswith(("2", "3", "4"))].dropna(axis=1, how="all"))

    # 6. F shares
    cf = rd("q7_condition1_family")
    add("6a. F share by priority year, all and protected", cf[cf["priority year"].isin([2019, 2020, 2021, 2022, 2023])][["priority year", "aircraft", "F aircraft", "F share", "aircraft in force", "F aircraft in force", "F share in force"]])
    add("6b. F share by region", rd("q7_region_family_share"))

    # 7. dimensions answered
    sel = fr.selected_fields(ctx.ds)[["name", "answered"]].rename(columns={"name": "dimension"})
    f15 = fr.form_frame15(ctx.ds)
    dist = pd.DataFrame({"dimension": [c for c in f15.columns if c != "aircraft_id"], "answered": [int(f15[c].notna().sum()) for c in f15.columns if c != "aircraft_id"]})
    add("7a. Distance dimensions (the 15 used for disparity) and designs answering", dist, f"Dimensions answered for at least 500 designs: {int((dist['answered'] >= 500).sum())} of {len(dist)}.")
    add("7b. Dimensions of the design-space table and designs answering", sel, f"Answered for at least 500 designs: {int((sel['answered'] >= 500).sum())} of {len(sel)}.")

    (OUT / "paper_numbers.md").write_text("# Numbers for paper item 4\n\nDataset: eVTOL_dataset (621 designs, 619 with an architecture), thesis seed 42.\n\n" + "\n".join(parts), encoding="utf-8")
    print((OUT / "paper_numbers.md").read_text()[:6000])


if __name__ == "__main__":
    main()
