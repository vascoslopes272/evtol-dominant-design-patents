"""Pending numbers, part D2 (items 16 to 19): funnel check, relevance and completeness intervals, directory mix, drawing mismatches,
worked Gower example.

    EVTOL_DATASET=<path to eVTOL_dataset> PYTHONPATH=2_analysis/src python3 2_analysis/scripts/55_pending_part_D2.py

Writes one CSV per table to numbers/pending_csv/ (names start with D2_). Nothing is interpreted. Light: one pass over the dataset, one
619 x 619 Gower matrix. Seed 42 (no random draw is made).
"""
from __future__ import annotations

import os as _os
from pathlib import Path as _Path
_REPO = _Path(__file__).resolve().parents[2]
_SUPP = _os.environ.get("SUPP_OUT", str(_REPO / "results" / "2_analysis" / "numbers"))
_DS = _os.environ.get("EVTOL_DATASET", str(_REPO.parent / "eVTOL_dataset"))
for _d in ("pending_csv", "supplementary_csv"):
    _os.makedirs(_os.path.join(_SUPP, _d), exist_ok=True)
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
import core  # noqa: E402

DS = Path(os.environ.get("EVTOL_DATASET", _DS))
NUM = Path(_SUPP)
OUT = NUM / "pending_csv"
OUT.mkdir(parents=True, exist_ok=True)


def save(name, df):
    df.to_csv(OUT / name, index=False)
    print(f"\n=== {name}\n{df.to_string(index=False)}")
    return df


def main():
    base = core.load()
    ctx = core.context(base, base.master)
    m, ds, v = base.m, ctx.ds, ctx.v
    from lib import intervals, association, distance as dist
    fr = m.frames
    q4 = __import__("viz.thesis_q4", fromlist=["x"])

    # ---------------------------------------------------------------- item 16: funnel, recomputed from the files
    p = pd.read_csv(DS / "03_patents" / "33_patents.csv")
    a42 = pd.read_csv(DS / "04_aircraft" / "42_aircraft.csv")
    d45 = pd.read_csv(DS / "04_aircraft" / "45_designs.csv")
    rows = [("families in the PatSeer export / file 33", len(p), "03_patents/33_patents.csv rows"),
            ("disapproved at T1", int((~p["is_approved"].astype(bool)).sum()), "33_patents.is_approved == False"),
            ("approved at T1", int(p["is_approved"].astype(bool).sum()), "33_patents.is_approved == True"),
            ("aircraft rows on approved patents", len(a42), "04_aircraft/42_aircraft.csv rows"),
            ("non-primary rows (duplicates)", int((~a42["is_primary"].astype(bool)).sum()), "42_aircraft.is_primary == False"),
            ("primary rows", int(a42["is_primary"].astype(bool).sum()), "42_aircraft.is_primary == True"),
            ("designs (is_design)", int(a42["is_design"].astype(bool).sum()), "42_aircraft.is_design == True"),
            ("designs in file 45", len(d45), "04_aircraft/45_designs.csv rows"),
            ("designs with an architecture (analysis frame)", int(v["topType"].notna().sum()), "ctx.v.topType notna")]
    reasons = p.loc[~p["is_approved"].astype(bool), "reason"].value_counts(dropna=False)
    save("D2_16_funnel_recomputed.csv", pd.DataFrame(rows, columns=["step", "value", "source"]))
    save("D2_16_disapproval_reasons.csv", reasons.rename_axis("reason").reset_index(name="families"))
    x = pd.read_excel(DS / "01_query" / "patseer_1639_2026-06-08.xlsx", nrows=3)
    print("export columns:", list(x.columns))

    # ---------------------------------------------------------------- item 17: relevance and completeness
    n_all, n_app = len(p), int(p["is_approved"].astype(bool).sum())
    gs = pd.read_csv(DS / "02_gold_standard" / "29_gold_standard.csv")
    rr = []

    def add(label, k, n, source, definition):
        lo, hi = intervals.wilson_interval(k, n)
        rr.append({"quantity": label, "k": k, "n": n, "share_pct": round(100 * k / n, 2), "wilson95_low_pct": round(100 * lo, 2),
                   "wilson95_high_pct": round(100 * hi, 2), "source": source, "definition": definition})
    add("relevance: families approved at T1 of all families judged", n_app, n_all, "03_patents/33_patents.csv",
        "is_approved == True over all 1 639 families (every family judged by the author; no sample)")
    nd = int(v["topType"].notna().sum())
    add("families that carry an approved aircraft, share of designs-bearing patents", int(v["patent_id"].nunique()), n_all,
        "ctx.v", "unique primary patents behind the 621 designs over 1 639 families")
    ac = gs["aircraft_outcome"].value_counts()
    cap_a, out_a = int(ac.get("captured", 0)), int(ac.get("outside, patent found", 0))
    pg = gs.drop_duplicates("programme")[["programme", "programme_outcome"]]
    pc = pg["programme_outcome"].value_counts()
    cap_p, out_p, nop_p = int(pc.get("captured", 0)), int(pc.get("outside, patent found", 0)), int(pc.get("no patent found", 0))
    add("completeness, aircraft with a patent found: captured of (captured + outside)", cap_a, cap_a + out_a,
        "02_gold_standard/29_gold_standard.csv", "aircraft_outcome == captured over captured + 'outside, patent found'")
    add("completeness, programmes with a patent found: captured of (captured + outside)", cap_p, cap_p + out_p,
        "02_gold_standard/29_gold_standard.csv", "programme_outcome, one row per programme")
    add("completeness, all census aircraft: captured of all", cap_a, len(gs), "02_gold_standard/29_gold_standard.csv",
        "aircraft_outcome == captured over all rows (includes no patent found and search pending)")
    add("completeness, all programmes: captured of all", cap_p, len(pg), "02_gold_standard/29_gold_standard.csv",
        "programme_outcome == captured over all programmes")
    save("D2_17_relevance_completeness_wilson.csv", pd.DataFrame(rr))
    save("D2_17_gold_standard_counts.csv", pd.concat([
        ac.rename_axis("aircraft_outcome").reset_index(name="aircraft").rename(columns={"aircraft_outcome": "category"}).assign(level="aircraft"),
        pc.rename_axis("programme_outcome").reset_index(name="programmes").rename(columns={"programme_outcome": "category", "programmes": "aircraft"}).assign(level="programme")]))
    for col in ("entered_by", "tier"):
        save(f"D2_17_gold_standard_by_{col}.csv", gs.groupby([col, "aircraft_outcome"]).size().reset_index(name="aircraft"))
    dacc = pd.read_csv(DS / "06_external" / "61_evtol_news_directory" / "directory_accuracy.csv")
    save("D2_17_directory_accuracy_copy.csv", dacc)

    # ---------------------------------------------------------------- item 18
    dm = q4.directory_mix(ctx)
    n_set, n_dir = dm["n_set"], dm["n_dir"]
    t = pd.DataFrame({"code": n_set.index, "dataset_designs": n_set.to_numpy(), "dataset_share_pct": (100 * n_set / n_set.sum()).round(2).to_numpy(),
                      "directory_aircraft_in_domain": n_dir.to_numpy(), "directory_share_pct": (100 * n_dir / n_dir.sum()).round(2).to_numpy(),
                      "adjusted_residual": np.round(dm["resid"], 2)})
    t.loc[len(t)] = ["total", int(n_set.sum()), 100.0, int(n_dir.sum()), 100.0, np.nan]
    save("D2_18_dataset_vs_directory.csv", t)
    print("chi2 test:", dm["test"])
    pub = q4.public_frame(ctx)
    mm = pub[pub["match"].isin(["no", "image"])]
    tab = pd.DataFrame({"design": mm["aircraft_id"].to_numpy(), "aircraft_name": mm["aircraft_name"].to_numpy(),
                        "match": mm["match"].to_numpy(), "label_from_drawing": mm["topType"].to_numpy(),
                        "label_from_text": mm["arch_gt"].to_numpy(), "public_aircraft": mm["public_arch"].to_numpy()})
    save("D2_18_ten_mismatches.csv", tab)
    save("D2_18_match_values.csv", pub["match"].value_counts().rename_axis("match").reset_index(name="designs"))

    # ---------------------------------------------------------------- item 19
    fi = fr.gower_inputs(ds, "w15")
    F = fi.frame.reset_index(drop=True)
    fields, w = fi.fields, fi.weights
    others = [f for f in fields if f not in ("Wing count", "Propulsor band")]

    def tok(x):
        return "NA" if (not isinstance(x, (set, frozenset)) and pd.isna(x)) else (tuple(sorted(x)) if isinstance(x, (set, frozenset)) else x)
    key = F[others].apply(lambda r: tuple(tok(x) for x in r), axis=1)
    cands = []
    for k, idx in key.groupby(key).groups.items():
        idx = list(idx)
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                i, j = idx[a], idx[b]
                dw = abs(F.loc[i, "Wing count"] - F.loc[j, "Wing count"])
                db = abs(F.loc[i, "Propulsor band"] - F.loc[j, "Propulsor band"])
                if dw > 0 and db > 0:
                    cands.append((int(F.loc[[i, j], others].isna().sum().sum()), dw + db, F.loc[i, "aircraft_id"], F.loc[j, "aircraft_id"], i, j, dw, db))
    cands.sort(key=lambda c: (c[0], c[1], c[2], c[3]))
    print("candidate pairs differing only in wing count and propulsor band:", len(cands))
    save("D2_19_candidate_pairs.csv", pd.DataFrame(cands, columns=["blank_cells_in_other_dims", "rank_diffs_sum", "id_i", "id_j", "row_i", "row_j", "wing_diff", "band_diff"]))
    best = cands[0]
    i, j = best[4], best[5]
    ri, rj = F.loc[i], F.loc[j]
    rec = []
    for f in fields:
        both = not any(isinstance(x, (set, frozenset)) is False and pd.isna(x) for x in (ri[f], rj[f]))
        if f in fi.sets:
            delta = float(dist.jaccard_distance(pd.Series([ri[f], rj[f]]))[0, 1]) if both else 0.0
        elif f in fi.numeric:
            delta = abs(float(ri[f]) - float(rj[f])) / fi.ranges[f] if both else 0.0
        else:
            delta = float(ri[f] != rj[f]) if both else 0.0
        rec.append({"dimension": f, "value_i": ri[f] if not isinstance(ri[f], frozenset) else "{" + ", ".join(sorted(ri[f])) + "}",
                    "value_j": rj[f] if not isinstance(rj[f], frozenset) else "{" + ", ".join(sorted(rj[f])) + "}",
                    "weight": w[f], "both_present": int(both), "delta": delta, "w_times_delta": w[f] * delta, "w_times_present": w[f] * both})
    R = pd.DataFrame(rec)
    num, den = R["w_times_delta"].sum(), R["w_times_present"].sum()
    D_pair = dist.gower_distance(F.loc[[i, j]].reset_index(drop=True), fields, fi.numeric, w, ranges=fi.ranges, sets=fi.sets)[0, 1]
    D_full = dist.gower_distance(F, fields, fi.numeric, w, ranges=fi.ranges, sets=fi.sets)
    R.loc[len(R)] = ["sum", "", "", R["weight"].sum(), "", np.nan, num, den]
    save("D2_19_worked_gower_example.csv", R)
    chk = pd.DataFrame([{"design_i": ri["aircraft_id"], "design_j": rj["aircraft_id"], "numerator": num, "denominator": den,
                         "d_hand": num / den, "d_library_two_row_frame": D_pair, "d_library_full_matrix": D_full[i, j],
                         "abs_diff_hand_vs_full": abs(num / den - D_full[i, j]), "frame_rows": len(F)}])
    save("D2_19_check.csv", chk)
    # context of the two designs
    ctxcols = [c for c in ("aircraft_id", "patent_id", "aircraft_name", "firm", "window", "year") if c in v.columns]
    print(v[v["aircraft_id"].isin([ri["aircraft_id"], rj["aircraft_id"]])][ctxcols].to_string(index=False))


if __name__ == "__main__":
    main()
