"""Pending part D, item 20 (S3.4): every quantity tested with a Spearman correlation and its Holm correction.
One row per test: block, quantity, rho, raw p, Holm p, family of the Holm correction, number of comparisons in the family.

    EVTOL_DATASET=<eVTOL_dataset> PYTHONPATH=2_analysis/src python3 2_analysis/scripts/48_pending_D_item_20_spearman_holm.py

Sources (read, not recomputed, because the notebooks wrote them): results/2_analysis/freeze/csv/q6_share_trend_spearman.csv (III.1),
q6_driver_trends.csv (IV, family = trace over SLC, TR, CVT, thesis_q6.HOLM_ARCH), q3_region_mix_change.csv (V, one family over every trend test of
the table). Block A is also recomputed with viz.analysis_iii.rho_table (thesis function, unchanged) as a check. Family sizes are the count of finite
raw p in the family (lib.multiple.holm leaves a NaN out of the family).
"""
from __future__ import annotations

import os as _os
from pathlib import Path as _Path
_REPO = _Path(__file__).resolve().parents[2]
_SUPP = _os.environ.get("SUPP_OUT", str(_REPO / "results" / "2_analysis" / "numbers"))
_DS = _os.environ.get("EVTOL_DATASET", str(_REPO.parent / "eVTOL_dataset"))
for _d in ("pending_csv", "supplementary_csv"):
    _os.makedirs(_os.path.join(_SUPP, _d), exist_ok=True)
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
import core  # noqa: E402

CSV = REPO / "results" / "2_analysis" / "freeze" / "csv"
OUT = Path((_SUPP + "/pending_csv"))


def main():
    rows = []
    # A. share of the architecture x priority year (analysis_iii.rho_table), two spans, one Holm family per span
    a = pd.read_csv(CSV / "q6_share_trend_spearman.csv")
    for span, (rc, pc, hc, lab) in {"2008-2023": ("rho", "p", "p (Holm)", "A1"), "2016-2023": ("rho, 2016-23", "p, 2016-23", "p, 2016-23 (Holm)", "A2")}.items():
        for _, r in a.iterrows():
            rows.append({"block": "III.1 share of the architecture in the year's designs against priority year", "quantity": f"{r['architecture']} ({r['architecture code']}), {span}",
                         "n": f"{int(r['designs'])} designs, {int(r['years'])} years" if span == "2008-2023" else f"{int(r['designs'])} designs (2016-23 yearly shares)",
                         "rho": r[rc], "raw p": r[pc], "Holm p": r[hc],
                         "family of the Holm correction": f"the architectures tested over {span} (analysis_iii.rho_table, one family per span)",
                         "comparisons in the family": int(a[pc].notna().sum()), "source file": "freeze/csv/q6_share_trend_spearman.csv"})
    # B. driver traces inside architectures (thesis_q6.HOLM_ARCH families)
    d = pd.read_csv(CSV / "q6_driver_trends.csv")
    d = d[d["p"].notna()]
    fam_n = d[d["code"].isin(["SLC", "TR", "CVT"])].groupby("trace")["p"].apply(lambda s: int(s.notna().sum()))
    for _, r in d.iterrows():
        inn = r["code"] in ("SLC", "TR", "CVT")
        rows.append({"block": "IV trend of a trace inside an architecture, over the cohorts (Spearman)", "quantity": f"{r['trace']} in {r['architecture']} ({r['code']})",
                     "n": f"{int(r['aircraft'])} aircraft", "rho": r["rho"], "raw p": r["p"], "Holm p": r["p_holm"] if inn else np.nan,
                     "family of the Holm correction": f"trace '{r['trace']}' over the three largest architectures SLC, TR, CVT (thesis_q6.HOLM_ARCH)" if inn else "none: outside the Holm family (TW, MR and the pooled rows carry the raw p only)",
                     "comparisons in the family": int(fam_n[r["trace"]]) if inn else np.nan, "source file": "freeze/csv/q6_driver_trends.csv"})
    # C. regional trends, one family over every test of the table
    m = pd.read_csv(CSV / "q3_region_mix_change.csv")
    m = m[m["p"].notna()]
    for _, r in m.iterrows():
        rows.append({"block": "V trend 2012-2023 of a regional answer (Spearman on the cohort shares)", "quantity": f"{r['region']} · {r['variable']} · {r['label']}",
                     "n": f"{int(r['aircraft 2012-23'])} designs", "rho": r["rho"], "raw p": r["p"], "Holm p": r["p (Holm)"],
                     "family of the Holm correction": "every trend test of the table (viz/latex_part5.regional_test_csvs: 'Holm over every trend test of the table')",
                     "comparisons in the family": int(m["p"].notna().sum()), "source file": "freeze/csv/q3_region_mix_change.csv"})
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "D20_spearman_holm_tests.csv", index=False)
    # check block A against the thesis function
    base = core.load()
    ctx = core.context(base, base.master)
    rt = base.m.analysis_iii.rho_table(ctx)
    rt.to_csv(OUT / "D20_check_rho_table_recomputed.csv", index=False)
    print(rt[["code", "aircraft", "years", "rho", "p", "p (Holm)", "rho, 2016-23", "p, 2016-23", "p, 2016-23 (Holm)"]].round(4).to_string())
    print(t.groupby("block").agg(tests=("raw p", "size")))
    print(t.groupby(["block", "family of the Holm correction"])["comparisons in the family"].agg(["min", "max", "size"]).to_string())


if __name__ == "__main__":
    main()
