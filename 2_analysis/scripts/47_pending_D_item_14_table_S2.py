"""Pending part D, item 14 (Table S2): configurations, singletons, effective number (Hill order 2, 1 / sum p_i^2) and share of the
largest configuration for every level of description the thesis code can form (L1 = A0, L2 = A1t, L3 = A0c, and the six finer or
different sets A1, A1c, A1b, A1tc, A2, A2c that frames.ARCHETYPE_SETS holds and archetype_levels_table tests), plus the family level F.

    EVTOL_DATASET=<eVTOL_dataset> PYTHONPATH=2_analysis/src python3 2_analysis/scripts/47_pending_D_item_14_table_S2.py
Thesis functions unchanged: frames.archetype_levels_table (key = frames.level_key), frames.archetype_screens, lib.concentration.inverse_hhi,
lib.diversity.effective_number, frames.dd_level_keys (for F).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
import core  # noqa: E402

OUT = Path("/mnt/storage_11tb/Drive_files_to_syncronize/paper_figures_for_other_pc/numbers/pending_csv")
NAME = {"A0": "L1 (A)", "A1t": "L2 (A.W.T)", "A0c": "L3 (A.U)", "A1": "A.W.B", "A1c": "A.W.B.U", "A1b": "A.W.B# (booms binned)",
        "A1tc": "A.W.T.U", "A2": "A.W.B.E", "A2c": "A.W.B.E.U", "family_b": "F (family as one archetype)"}


def main():
    base = core.load()
    ctx = core.context(base, base.master)
    m, ds, v, cfg = base.m, ctx.ds, ctx.v, base.cfg
    fr = m.frames
    from lib import concentration as conc, diversity as div
    lv = fr.archetype_levels_table(ds, v, cfg)
    sc = fr.archetype_screens(lv, cfg)
    rows = []
    for _, r in lv.iterrows():
        rows.append({"level id": r["level"], "level": NAME[r["level"]], "thesis code": fr.SET_CODES[r["level"]][0], "fields in the key": " + ".join(fr.ARCHETYPE_SETS[r["level"]]),
                     "designs keyed": r["aircraft"], "designs left out (no key)": r["left out"], "configurations": r["archetypes"], "singletons": r["singletons"],
                     "singleton share": r["singleton share"], "effective number, order 1 (exp Shannon)": r["effective number ¹D"],
                     "effective number, order 2 (1 / sum p^2)": r["effective number ²D"], "largest configuration": r["largest archetype"],
                     "share of the largest configuration": r["largest share"], "screens passed (config.yaml archetype_screens)": sc.loc[sc["level"].eq(r["level"]), "screens passed"].iloc[0]})
    # family F, same recipe on the frame's own key (frames.dd_level_keys['family_b'])
    k = fr.dd_level_keys(ds, v)["family_b"].dropna()
    c = k.value_counts()
    rows.append({"level id": "family_b", "level": NAME["family_b"], "thesis code": "F", "fields in the key": "topType with the Lift + Cruise + CVT* family as one option",
                 "designs keyed": int(len(k)), "designs left out (no key)": int(len(v) - len(k)), "configurations": int(len(c)), "singletons": int((c == 1).sum()),
                 "singleton share": float((c == 1).sum() / len(k)), "effective number, order 1 (exp Shannon)": float(div.effective_number(k)),
                 "effective number, order 2 (1 / sum p^2)": float(conc.inverse_hhi(c)), "largest configuration": str(c.index[0]),
                 "share of the largest configuration": float(c.iloc[0] / len(k)), "screens passed (config.yaml archetype_screens)": "not computed (not in ARCHETYPE_SETS)"})
    t = pd.DataFrame(rows)
    # unrounded values of order 2 and shares for the three main levels, from the key itself
    un = []
    for lid in t["level id"][t["level id"] != "family_b"]:
        w = fr.with_boom_bin(v[v["topType"].notna()])
        key = fr.level_key(w, lid, ds.data_dictionary)
        key = key[key.notna()]
        cc = key.value_counts()
        un.append({"level id": lid, "order 2 unrounded": float(conc.inverse_hhi(cc)), "order 1 unrounded": float(div.effective_number(key)),
                   "largest share unrounded": float(cc.iloc[0] / len(key)), "designs keyed": int(len(key))})
    un = pd.DataFrame(un).set_index("level id")
    t["effective number, order 2 (unrounded)"] = t["level id"].map(un["order 2 unrounded"])
    t["share of the largest configuration (unrounded)"] = t["level id"].map(un["largest share unrounded"])
    t.loc[t["level id"].eq("family_b"), "effective number, order 2 (unrounded)"] = t.loc[t["level id"].eq("family_b"), "effective number, order 2 (1 / sum p^2)"]
    t.loc[t["level id"].eq("family_b"), "share of the largest configuration (unrounded)"] = t.loc[t["level id"].eq("family_b"), "share of the largest configuration"]
    t.to_csv(OUT / "D14a_table_S2_levels.csv", index=False)
    sc.to_csv(OUT / "D14b_table_S2_screens.csv", index=False)
    # for the record: the same three levels keyed with frames.archetype_key (used by dd_level_keys and B6c)
    rows = []
    for lid in ("A0", "A1t", "A0c"):
        kk = fr.archetype_key(v, lid).dropna()
        cc = kk.value_counts()
        rows.append({"level id": lid, "key function": "frames.archetype_key (dd_level_keys, B6c)", "designs keyed": int(len(kk)), "configurations": int(len(cc)),
                     "singletons": int((cc == 1).sum()), "order 2 (1 / sum p^2)": float(conc.inverse_hhi(cc)), "share of the largest configuration": float(cc.iloc[0] / len(kk))})
    pd.DataFrame(rows).to_csv(OUT / "D14c_table_S2_three_levels_archetype_key_basis.csv", index=False)
    pd.set_option("display.width", 250)
    print(t.drop(columns=["fields in the key"]).to_string())
    print(pd.DataFrame(rows).to_string())
    print(sc[["level", "screens passed"]].to_string())


if __name__ == "__main__":
    main()
