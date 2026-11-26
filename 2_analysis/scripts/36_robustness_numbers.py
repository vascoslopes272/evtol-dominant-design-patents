"""Coding-noise robustness numbers for paper P1 (items E11-E14): reads the replicas that exist, computes nothing new except the
architecture-label change share (which needs only the perturbation, not the permutations).

    EVTOL_DATASET=<path> PYTHONPATH=2_analysis/src python 2_analysis/scripts/36_robustness_numbers.py

Inputs
  results/31_label_reliability/r15_p10000/replicas.jsonl   15 % per value, 10 000 permutations per band, replicas written by
                                                           3_robustness/31_label_reliability/src/31B_run_replicas.py (EVTOL_RATE=0.15
                                                           EVTOL_TAG=r15_p10000, --n 120). Whatever is in the file when this runs.
  eVTOL_dataset/07_results/71_label_reliability/reliability_replicas.csv
                                                           the 1 000-replica run at 1 000 permutations (reference only)
Outputs (numbers/supplementary_csv)
  E11_verdict_table_10000perms.csv, E11_verdict_table_1000reps_1000perms.csv, E11b_band_dependent_numbers_*.csv,
  E11c_direction_vs_significance_*.csv, E12_label_change_per_replica.csv, E13_family_F_verdict_*.csv, _robustness_values.csv
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
DS_ROOT = Path(os.environ.get("EVTOL_DATASET", "/mnt/storage_11tb/Drive_files_to_syncronize/eVTOL_dataset"))
OUT = Path(os.environ.get("SUPP_OUT", "/mnt/storage_11tb/Drive_files_to_syncronize/paper_figures_for_other_pc/numbers")) / "supplementary_csv"
JSONL = REPO / "results" / "31_label_reliability" / os.environ.get("RUN_TAG", "allowed_r15_p10000") / "replicas.jsonl"
REF = DS_ROOT / "07_results" / "71_label_reliability" / "reliability_replicas.csv"
SEED = 20261118
LEVELS = ["A", "A·W·T", "A·U", "F"]
VALUES = []


def wilson(k, n, z=1.959964):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def load_jsonl():
    rows = [json.loads(l) for l in JSONL.read_text(encoding="utf-8").splitlines() if l.strip()]
    base = next(r["results"] for r in rows if r["log"]["replica"] == -1)
    reps = pd.DataFrame([{**r["log"], **r["results"]} for r in rows if r["log"]["replica"] >= 0]).sort_values("replica")
    return base, reps


def summarise_bool(reps, key, orig):
    x = reps[key].dropna()
    n = len(reps)
    k_same = int((x.astype(bool) == bool(orig)).sum())
    k_true = int(x.astype(bool).sum())
    lo, hi = wilson(k_same, n)
    return {"original": bool(orig), "replicas": n, "replicas computed": int(len(x)), "replicas keeping the original value": k_same,
            "share keeping the original value": k_same / n, "Wilson 95 % low": lo, "Wilson 95 % high": hi,
            "replicas where it is true": k_true, "share where it is true": k_true / n}


def verdict_tables(base_res, reps, tag):
    vt, bd, dr = [], [], []
    for key, b in base_res.items():
        p = [s.strip() for s in key.split("|")]
        if p[0] in ("3", "4") and isinstance(b, (bool, np.bool_)) and len(p) == 4:      # 3 | base | condition | level
            vt.append({"key": key, "result group": "F (4)" if p[0] == "4" else "A, A·W·T, A·U (3)", "base": p[1], "condition": p[2], "level": p[3],
                       **summarise_bool(reps, key, b)})
        if p[0] in ("3", "4") and isinstance(b, (bool, np.bool_)) and len(p) == 3 and "F above 50" in p[2]:
            vt.append({"key": key, "result group": "F (4)", "base": p[1], "condition": p[2], "level": "F", **summarise_bool(reps, key, b)})
    vt = pd.DataFrame(vt)
    # numbers that depend on the band
    for base in ("all designs", "actively protected"):
        for L in LEVELS:
            k = lambda s: f"{'4' if L == 'F' else '3'} | {base} | {s} | {L}"          # noqa: E731
            if k("2D 2020-23") not in reps.columns:
                continue
            d2, e2, dq, eq = (reps[k(s)] for s in ("2D 2020-23", "2D band low 2020-23", "dQ 2020-23", "dQ band low 2020-23"))
            o = {s: base_res[k(s)] for s in ("2D 2020-23", "2D band low 2020-23", "dQ 2020-23", "dQ band low 2020-23")}
            n = len(reps)
            bd.append({"base": base, "level": L, "replicas": n,
                       "2D original": o["2D 2020-23"], "2D median": d2.median(), "2D p5": d2.quantile(.05), "2D p95": d2.quantile(.95),
                       "2D band low original": o["2D band low 2020-23"], "2D band low median": e2.median(), "2D band low p5": e2.quantile(.05), "2D band low p95": e2.quantile(.95),
                       "share with 2D below its own band low": float((d2 < e2).mean()), "original: 2D below band": bool(o["2D 2020-23"] < o["2D band low 2020-23"]),
                       "dQ original": o["dQ 2020-23"], "dQ median": dq.median(), "dQ p5": dq.quantile(.05), "dQ p95": dq.quantile(.95),
                       "dQ band low original": o["dQ band low 2020-23"], "dQ band low median": eq.median(), "dQ band low p5": eq.quantile(.05), "dQ band low p95": eq.quantile(.95),
                       "share with dQ below 0": float((dq < 0).mean()), "share with dQ below its own band low": float((dq < eq).mean()),
                       "original: dQ below band": bool(o["dQ 2020-23"] < o["dQ band low 2020-23"]),
                       "share with leading share unchanged in verdict (> 50 %)": np.nan})
    bd = pd.DataFrame(bd)
    return vt, bd


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    out = {}
    base_res, reps = load_jsonl()
    n10 = len(reps)
    vt10, bd10 = verdict_tables(base_res, reps, "10000")
    vt10.to_csv(OUT / "E11_verdict_table_10000perms.csv", index=False)
    bd10.to_csv(OUT / "E11b_band_dependent_numbers_10000perms.csv", index=False)
    VALUES.append({"id": "E11.n_replicas_10000perms", "value": n10, "script": "36_robustness_numbers.py",
                   "file": str(JSONL), "definition": "replicas in replicas.jsonl when the script ran (15 % per value, 10 000 permutations per band, seed 20261118); the job asked for 120"})
    # reference: 1 000 replicas, 1 000 permutations
    ref = pd.read_csv(REF, low_memory=False)
    refsum = pd.read_csv(REF.with_name("reliability_summary.csv"))
    base_ref = dict(zip(refsum["key"], refsum["original value"]))
    for c in ref.columns:
        pass
    refb = {k: (str(v).lower() == "true" if str(v).lower() in ("true", "false") else v) for k, v in base_ref.items()}
    for c in ref.columns:
        if ref[c].dtype == object and ref[c].dropna().astype(str).isin(["True", "False"]).all():
            ref[c] = ref[c].map({"True": True, "False": False})
    vt1, bd1 = verdict_tables(refb, ref, "1000")
    vt1.to_csv(OUT / "E11_verdict_table_1000reps_1000perms.csv", index=False)
    bd1.to_csv(OUT / "E11b_band_dependent_numbers_1000reps_1000perms.csv", index=False)
    VALUES.append({"id": "E11.n_replicas_reference", "value": len(ref), "script": "3_robustness/31_label_reliability/src/31B_run_replicas.py (run of 2026-11-22/23)",
                   "file": str(REF), "definition": "reference run: 15 % per value, 1 000 permutations per band; not the 10 000-permutation run"})

    # direction vs significance for the three trend results and the disparity (keys in core.py)
    rows = []
    for tag, R, bR in (("10000 perms", reps, base_res), ("1000 reps, 1000 perms", ref, refb)):
        n = len(R)
        for key in [k for k in R.columns if k.startswith(("5 | rises", "5 | falls", "6 | significant", "6 | sign |"))]:
            if key not in bR:
                continue
            x = R[key].dropna()
            rows.append({"run": tag, "key": key, "original": bR[key], "replicas": n,
                         "share where it is true / equals": float((x.astype(float) == (1.0 if not isinstance(bR[key], (bool, np.bool_)) else float(bR[key]))).mean()) if len(x) else np.nan})
    pd.DataFrame(rows).to_csv(OUT / "E11c_trend_keys.csv", index=False)

    # E13 the verdict for family F
    f10 = vt10[vt10["level"].eq("F")]
    f10.to_csv(OUT / "E13_family_F_verdict_10000perms.csv", index=False)
    vt1[vt1["level"].eq("F")].to_csv(OUT / "E13_family_F_verdict_1000reps_1000perms.csv", index=False)

    # E12 label change with the perturbation only, replicas 0..99 (same seed and stream as the runs)
    import core
    import perturb
    base = core.load()
    perturb.R = 0.15
    P = perturb.Perturber(base, r=0.15)
    rows_ = list(P.rows)
    a0 = base.master.loc[rows_, "topType"].astype(str).to_numpy()
    has_arch = base.master.loc[rows_, "topType"].notna().to_numpy()
    lc = []
    for i in range(100):
        m, log = P.replica(SEED, i)
        a1 = m.loc[rows_, "topType"].astype(str).to_numpy()
        ch = a0 != a1
        lc.append({"replica": i, "architecture labels changed": int(ch.sum()), "designs perturbed (rows)": len(rows_),
                   "designs with an architecture": int(has_arch.sum()), "share of 621 designs": ch.sum() / len(rows_),
                   "share of the 619 with an architecture": ch[has_arch].sum() / has_arch.sum(), "codes changed": log["codes changed"],
                   "designs changed (any code)": log["designs changed"], "designs redrawn at least once": log["designs redrawn"],
                   "designs kept after 20 redraws": log["designs kept after 20 redraws"]})
    lc = pd.DataFrame(lc)
    lc.to_csv(OUT / "E12_label_change_per_replica.csv", index=False)
    # cross-check with the jsonl logs
    j = reps.set_index("replica")["architecture labels changed"]
    chk = lc.set_index("replica")["architecture labels changed"].reindex(j.index)
    VALUES.extend([
        {"id": "E12.mean_share_621", "value": lc["share of 621 designs"].mean(), "script": "36_robustness_numbers.py (perturb.Perturber.replica, seed 20261118, rate 0.15)",
         "file": "E12_label_change_per_replica.csv", "definition": "mean over replicas 0-99 of (designs whose architecture code topType differs from the original) / 621"},
        {"id": "E12.mean_share_619", "value": lc["share of the 619 with an architecture"].mean(), "script": "36_robustness_numbers.py",
         "file": "E12_label_change_per_replica.csv", "definition": "same, over the 619 designs that have an architecture"},
        {"id": "E12.median_changed", "value": float(lc["architecture labels changed"].median()), "script": "36_robustness_numbers.py", "file": "E12_label_change_per_replica.csv",
         "definition": "median number of changed architecture labels per replica"},
        {"id": "E12.min_max_changed", "value": f"{lc['architecture labels changed'].min()} - {lc['architecture labels changed'].max()}", "script": "36_robustness_numbers.py",
         "file": "E12_label_change_per_replica.csv", "definition": "range over 100 replicas"},
        {"id": "E12.crosscheck_with_jsonl", "value": f"{int((chk.values == j.values).sum())} of {len(j)} replicas equal", "script": "36_robustness_numbers.py",
         "file": str(JSONL), "definition": "architecture labels changed in the 10 000-permutation replicas against the perturbation rerun here"}])
    if "architecture labels changed" in ref.columns:
        VALUES.append({"id": "E12.reference_1000_replicas_mean_share_621", "value": float((ref["architecture labels changed"] / ref["designs"]).mean()) if "designs" in ref.columns else float(ref["architecture labels changed"].mean() / 621),
                       "script": "31B_run_replicas.py (reference run)", "file": str(REF), "definition": "mean over the 1 000 replicas of architecture labels changed / designs"})
    # E14 definition of entrants inside the replicas
    pd.DataFrame(VALUES).to_csv(OUT / "_robustness_values.csv", index=False)
    print(pd.DataFrame(VALUES).to_string())


if __name__ == "__main__":
    main()
