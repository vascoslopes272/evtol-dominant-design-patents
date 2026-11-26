"""Pending part D, item 13 (Table S1): for every dimension of the design-space table (11) and of the 15-dimension distance (15):
answer rate, share of the most common option, whether it varies (80 % rule: leading option under 80 %), whether it enters the
15-dimension distance, and the reason for an exclusion as written in the code.

    EVTOL_DATASET=<eVTOL_dataset> PYTHONPATH=2_analysis/src python3 2_analysis/scripts/46_pending_D_item_13_table_S1.py
Thesis functions unchanged (viz.frames.selected_fields, form_frame15). 80 % rule: lib/ SHARE_RULE as in 3_robustness/31_label_reliability/src/core.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
import core  # noqa: E402

OUT = Path("/mnt/storage_11tb/Drive_files_to_syncronize/paper_figures_for_other_pc/numbers/pending_csv")
RULE = 0.80
NS = "not stated in the code"

# table dimension -> (distance dimension it enters through, or None, note on how)
LINK = {
    "tail type": ("Empennage Type", "same field empType"),
    "fuselage motion hover to cruise": ("Fuselage Kinematics", "same field fusKin"),
    "wing configuration": ("Wing Architecture", "same field wingConf"),
    "number of wings (winged designs)": ("Wing count", "same field wCount (0 kept in the distance, dropped in the table)"),
    "fuselage shape": ("Fuselage Shape", "same field fusShape"),
    "booms present": ("Boom count", "enters only through Boom count (rank 0 when boomsPresent is not True, else the number of booms)"),
    "propulsor units per aircraft (band)": ("Propulsor band", "same quantity, propulsor_units in ROTOR_BINS"),
    "propulsor enclosure (any ducted)": ("Propulsor Enclosure", "not the same variable: the table row is 'any unit ducted', the distance reads the enclosure of the set with the most propulsors"),
    "places carrying propulsor units per aircraft": ("Mount locations", "not the same variable: the table row counts stations (4 or more pooled), the distance compares the set of stations by Jaccard distance"),
    "landing-gear type": (None, ""),
    "left-right symmetry": (None, ""),
}
REASON_EXCLUDED = {
    "landing-gear type": "frames.py FORM15 (w15, 'the dissertation's declaration, 2026-10-15') does not list it; it is in the 34-dimension w34 weighting as 'Ground Contact Interface' (FORM_GROUPS, M1 structure). No reason for leaving it out of w15 is written. " + NS + ". Separate note in core.py:r1_design_space: 68 % of its answers are 'Unknown' (thesis II.1) and the thesis count of varying dimensions leaves it out.",
    "left-right symmetry": "frames.py FORM15 does not list it; it is in w34 as 'Airframe Lateral Symmetry'. " + NS + ".",
}


def main():
    base = core.load()
    ctx = core.context(base, base.master)
    m, ds, v = base.m, ctx.ds, ctx.v
    fr = m.frames
    N = len(v)
    N_arch = int(v["topType"].notna().sum())
    t6 = fr.selected_fields(ds)
    rows = []
    for _, r in t6.iterrows():
        ent, how = LINK[r["name"]]
        rows.append({"list": "design-space table (11)", "dimension": r["name"], "field": r["field"],
                     "designs answering": int(r["answered"]), "answer rate (of 621 designs)": r["answered"] / N,
                     "answer rate (of 619 designs with an architecture)": r["answered"] / N_arch if True else np.nan,
                     "options": int(r["answers"]), "share of the most common option (unrounded, among answering)": None,
                     "share as printed (2 dp, selected_fields)": r["top_share"],
                     "most common options": r["most common answers"],
                     "varies (leading option under 80 %)": bool(r["top_share"] < RULE),
                     "enters the 15-dimension distance": ent is not None,
                     "distance dimension it enters through": ent or "", "how": how,
                     "reason for exclusion from the distance": "" if ent else REASON_EXCLUDED[r["name"]]})
    # unrounded top shares from the series behind each row
    ser = fr.selected_field_series(ds)
    for r in rows:
        s = ser[r["dimension"]].dropna()
        r["share of the most common option (unrounded, among answering)"] = float(s.value_counts().iloc[0] / len(s))
        r["varies (leading option under 80 %)"] = bool(r["share of the most common option (unrounded, among answering)"] < RULE)
    tab = pd.DataFrame(rows)
    tab.to_csv(OUT / "D13a_table_S1_design_space_table_dimensions.csv", index=False)

    f15 = fr.form_frame15(ds)
    inv = {d: (system, field, how, kind, w) for system, d, field, how, kind, w in fr.FORM15}
    back = {v_[0]: k for k, v_ in LINK.items() if v_[0]}
    rows = []
    for d in fr.FORM15_FIELDS:
        s = f15[d].dropna()
        vc = s.astype(str).value_counts()
        system, field, how, kind, w = inv[d]
        rows.append({"list": "15-dimension distance", "dimension": d, "system": system, "codebook field": field, "compared as": how,
                     "weight in the distance (FORM15)": w, "designs answering (of the 619 with an architecture)": int(len(s)),
                     "answer rate (of 621 designs)": len(s) / N, "answer rate (of 619 designs with an architecture)": len(s) / len(f15),
                     "distinct values": int(vc.size), "most common value": vc.index[0],
                     "share of the most common value (among answering)": float(vc.iloc[0] / len(s)),
                     "varies (leading value under 80 %)": bool(vc.iloc[0] / len(s) < RULE),
                     "enters the 15-dimension distance": True,
                     "table row it corresponds to": back.get(d, "none (distance only)")})
    tab2 = pd.DataFrame(rows)
    tab2.to_csv(OUT / "D13b_table_S1_distance_dimensions.csv", index=False)
    print(tab.drop(columns=["reason for exclusion from the distance", "how", "most common options"]).to_string())
    print(tab2.to_string())
    # the w34 dimensions that are not in w15 (the codebook's own dimensions left out of the distance)
    left = [d for d in fr.FORM_FIELDS if d not in fr.FORM15_FIELDS]
    pd.DataFrame({"w34 dimension not in the 15": left}).to_csv(OUT / "D13c_w34_dimensions_not_in_w15.csv", index=False)
    print(len(left), left)


if __name__ == "__main__":
    main()
