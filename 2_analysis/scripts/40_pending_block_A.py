"""Block A of the pending numbers of paper P1: the coding-noise run (15 % per value, locks) and the weight draws, result by result.

    EVTOL_DATASET=<path to eVTOL_dataset> python 2_analysis/scripts/40_pending_block_A.py

Reads (whatever is in the files when it runs)
  results/31_label_reliability/r15_p10000/replicas.jsonl   15 % per value, 10 000 permutations per band (31B_run_replicas.py, EVTOL_RATE=0.15)
  results/31_label_reliability/r20_p10000/replicas.jsonl   20 % per value, 10 000 permutations (same runner), if it exists
  eVTOL_dataset/07_results/71_label_reliability/reliability_replicas.csv   1 000 replicas, 15 %, 1 000 permutations (reference)
  eVTOL_dataset/07_results/72_weight_sensitivity/test1_summary.csv, test2_summary.csv   1 000 weight draws (both bases, L1-L3; within F)
Writes numbers/pending_csv/A*.csv and numbers/pending_part_A.md. Nothing is interpreted.
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
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
DS = Path(os.environ.get("EVTOL_DATASET", _DS))
NUM = Path(os.environ.get("SUPP_OUT", _SUPP))
CSV = NUM / "pending_csv"
CSV.mkdir(parents=True, exist_ok=True)
SCRIPT = "2_analysis/scripts/40_pending_block_A.py"
RUNS = {"allowed-values rule, 15 %, 10 000 perms": REPO / "results/31_label_reliability/allowed_r15_p10000/replicas.jsonl",
        "allowed-values rule, 20 %, 10 000 perms": REPO / "results/31_label_reliability/allowed_r20_p10000/replicas.jsonl",
        "first version (redraw whole design), 15 %, 10 000 perms": REPO / "results/31_label_reliability/r15_p10000/replicas.jsonl"}
REFJ = REPO / "results/31_label_reliability/allowed_r15_p1000_n1000/replicas.jsonl"      # 1 000 replicas, allowed-values rule, 1 000 permutations
W1 = DS / "07_results/72_weight_sensitivity/test1_summary.csv"
W2 = DS / "07_results/72_weight_sensitivity/test2_summary.csv"
REF = DS / "07_results/71_label_reliability/reliability_replicas.csv"
LV = {"A": "L1", "A·W·T": "L2", "A·U": "L3", "F": "L1"}          # F is read on the distance of level A (the distance has the architecture weight)


def wilson(k, n, z=1.959964):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def load(path):
    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    base = next(r["results"] for r in rows if r["log"]["replica"] == -1)
    reps = pd.DataFrame([{**r["log"], **r["results"]} for r in rows if r["log"]["replica"] >= 0]).sort_values("replica")
    return base, reps


def ready(path):
    """A replica file is read only when it holds the baseline row and at least ten replicas."""
    if not path.exists():
        return False
    rows = [json.loads(l)["log"]["replica"] for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    return -1 in rows and sum(1 for x in rows if x >= 0) >= 10


def keep_table(base, reps):
    """Every boolean result: original value and the share of replicas that keep it."""
    out = []
    for key, b in base.items():
        if isinstance(b, (bool, np.bool_)) and key in reps.columns:
            x = reps[key].dropna().astype(bool)
            k = int((x == bool(b)).sum())
            lo, hi = wilson(k, len(reps))
            out.append({"key": key, "original": bool(b), "replicas": len(reps), "kept": k, "share kept": k / len(reps), "Wilson low": lo,
                        "Wilson high": hi, "share true": float(x.mean())})
    return pd.DataFrame(out)


def weights_for(key):
    """Share of the 1 000 weight draws that keep the original value of a result; None when the result does not use the distance."""
    p = [s.strip() for s in key.split("|")]
    if p[0] in ("3", "4") and len(p) == 4 and p[2] == "3 disparity":
        t = pd.read_csv(W1)
        r = t[(t["level"] == LV[p[3]]) & (t["base"] == p[1])]
        if len(r):
            r = r.iloc[0]
            return float(r["share that holds"]), "disparity: draws with dQ below band (test1_summary.csv" + (", F read on level L1)" if p[3] == "F" else ")")
    if p[0] in ("3", "4") and len(p) == 4 and p[2] in ("1 share", "2 balance"):
        return 1.0, "not affected: the condition does not use the distance"
    if p[0] in ("5", "6", "7", "8", "1") or (len(p) == 3 and p[0] == "4" and "F above" in p[2]):
        return 1.0, "not affected: the result does not use the distance"
    return None, "not computed (weights change dQ only; combination of conditions not recomputed under draws)"


def main():
    md = ["# Pending numbers, block A (coding-noise run and weight draws)", "",
          "Paper P1, dataset eVTOL_dataset (621 designs, 619 with an architecture), seed 42. Script `" + SCRIPT + "`; replica files as listed in the script docstring. Nothing is interpreted.", ""]
    vals = []

    # A1 -------------------------------------------------------------------------------------------------------------------------
    rows = []
    for name, path in RUNS.items():
        if ready(path):
            b, r = load(path)
            rows.append({"run": name, "replicas finished": len(r), "file": str(path.relative_to(REPO)), "permutations per band": 10000,
                         "replica seed": 20261118, "designs changed in architecture label, mean share": float((r["architecture labels changed"] / r["designs"]).mean()),
                         "min changed": int(r["architecture labels changed"].min()), "max changed": int(r["architecture labels changed"].max())})
    if ready(REFJ):
        ref = load(REFJ)[1]
        reflab, reffile = "allowed-values rule, 15 %, 1 000 perms (reference)", str(REFJ.relative_to(REPO))
    else:
        ref, reflab, reffile = pd.read_csv(REF), "first version, 15 %, 1 000 perms (reference)", str(REF)
    refrow = {"run": reflab, "replicas finished": len(ref), "file": reffile, "permutations per band": 1000, "replica seed": 20261118}
    if "architecture labels changed" in ref and "designs" in ref:
        refrow.update({"designs changed in architecture label, mean share": float((ref["architecture labels changed"] / ref["designs"]).mean()),
                       "min changed": int(ref["architecture labels changed"].min()), "max changed": int(ref["architecture labels changed"].max())})
    rows.append(refrow)
    a1 = pd.DataFrame(rows)
    a1.to_csv(CSV / "A1_replica_counts.csv", index=False)
    md += ["## A1. Replica counts", "", "1 000 replicas at 10 000 permutations do not exist: a replica takes about 38 minutes on one core; 1 000 of them need about 42 hours on 15 workers. "
           "The 1 000-replica run at 1 000 permutations is reported next to the 10 000-permutation runs and is labelled.", "", a1.to_markdown(index=False), ""]

    # A2 / A4 --------------------------------------------------------------------------------------------------------------------
    summaries = {}
    for name, path in RUNS.items():
        if ready(path):
            b, r = load(path)
            summaries[name] = (b, r, keep_table(b, r))
    first = next(iter(summaries.values()))
    s7 = first[2][["key", "original"]].copy()
    s7["share kept, weight draws"], s7["weights: how read"] = zip(*[weights_for(k) for k in s7["key"]])
    for name, (b, r, t) in summaries.items():
        m = t.set_index("key")
        s7[f"share kept, coding {name} (n={len(r)})"] = s7["key"].map(m["share kept"])
        s7[f"Wilson low {name}"] = s7["key"].map(m["Wilson low"])
        s7[f"Wilson high {name}"] = s7["key"].map(m["Wilson high"])
    if True:
        # reference run: boolean columns keyed as in the jsonl where present
        refcols = {c: c for c in ref.columns}
        share_ref = {}
        for k, o in zip(s7["key"], s7["original"]):
            if k in refcols:
                x = ref[k].dropna()
                share_ref[k] = float((x.astype(bool) == bool(o)).mean())
        s7[f"share kept, coding {reflab}, n={len(ref)}"] = s7["key"].map(share_ref)
    s7.to_csv(CSV / "A2_S7_every_result.csv", index=False)
    md += ["## A2. Table S7: every tested result, original value, share kept under weight draws and under coding replicas", "",
           "Rows are the boolean results of `31B_run_replicas.py` (keys as in the replica file: 1 = variety of dimensions, 3/4 = conditions at A, A·W·T, A·U and F, 5 = trends of architecture shares, "
           "6 = trends inside architectures, 7 = entrants, 8 = regions). `share kept` = share of replicas whose value equals the original. Weight draws change only the distance (condition 3); "
           "for the other results the weights column says 'not affected'.", "", s7.to_markdown(index=False, floatfmt=".3f"), ""]

    # A3 -------------------------------------------------------------------------------------------------------------------------
    for name, (b, r, t) in summaries.items():
        rows = []
        for base in ("all designs", "actively protected"):
            for L in ("A", "A·W·T", "A·U", "F"):
                g = "4" if L == "F" else "3"
                k = f"{g} | {base} | 3 disparity | {L}"
                dq = f"{g} | {base} | dQ 2020-23 | {L}"
                edge = f"{g} | {base} | dQ band low 2020-23 | {L}"
                rows.append({"base": base, "level": L, "share of replicas with dQ below band in 2020-23": float(r[k].astype(bool).mean()),
                             "median dQ under noise": float(r[dq].median()), "original dQ": float(b[dq]), "median band low edge under noise": float(r[edge].median()),
                             "original band low edge": float(b[edge]), "replicas": len(r)})
        a3a = pd.DataFrame(rows)
        a3a.to_csv(CSV / f"A3a_disparity_{name.replace(' ', '_').replace('%', 'pc').replace(',', '')}.csv", index=False)
        k3 = "4 | actively protected | all three | F"
        k1 = "4 | all designs | 1 share | F"
        tp = "5 | falls (rho < 0, Holm p < 0.05) | TP"
        wc = "1 | top share | wing configuration"
        hc = "1 | top share | fuselage motion hover to cruise"
        du = "1 | top share | propulsor enclosure (any ducted)"
        spec = [("F meets all three conditions, protected designs: share of replicas", float(r[k3].astype(bool).mean()), k3),
                ("F fails the share condition, all designs: share of replicas", float((~r[k1].astype(bool)).mean()), k1),
                ("F share in 2020, protected designs: median over replicas", float(r["4 | actively protected | F share 2020"].median()), "4 | actively protected | F share 2020"),
                ("F share above 50 % in 2020, protected designs: share of replicas", float(r["4 | actively protected | F above 50 % in 2020"].astype(bool).mean()), "4 | actively protected | F above 50 % in 2020"),
                ("Tilt Propulsor share falls with Holm p < 0.05: share of replicas", float(r[tp].astype(bool).mean()), tp),
                ("Tilt Propulsor share falls: original value", bool(b[tp]), tp)]
        for lab, key in (("standard wings (wing configuration), leading share", wc), ("hover-to-cruise motion, leading share", hc), ("ducted, leading share", du)):
            if key in r.columns:
                spec += [(lab + ": original", float(b[key]), key), (lab + ": median under noise", float(r[key].median()), key),
                         (lab + ": 5th to 95th percentile under noise", f"{r[key].quantile(.05):.2f} to {r[key].quantile(.95):.2f}", key)]
        a3b = pd.DataFrame([{"quantity": a, "value": v, "replica-file key": c, "replicas": len(r)} for a, v, c in spec])
        a3b.to_csv(CSV / f"A3b_named_numbers_{name.replace(' ', '_').replace('%', 'pc').replace(',', '')}.csv", index=False)
        md += [f"## A3. Numbers for S5 and 4.4, coding noise {name}, {len(r)} replicas", "", "Disparity (condition 3) per level and base:", "", a3a.to_markdown(index=False, floatfmt=".4f"), "",
               a3b.to_markdown(index=False), ""]

    # A4 -------------------------------------------------------------------------------------------------------------------------
    for name, (b, r, t) in summaries.items():
        m = t.set_index("key")
        rows = []
        for base in ("all designs", "actively protected"):
            for cond in ("1 share", "2 balance", "3 disparity", "all three"):
                k = f"4 | {base} | {cond} | F"
                rows.append({"base": base, "condition": cond, "original": bool(b[k]), "share of replicas where it is met": float(r[k].astype(bool).mean()),
                             "share keeping the original": float(m.loc[k, "share kept"]), "Wilson low": float(m.loc[k, "Wilson low"]), "Wilson high": float(m.loc[k, "Wilson high"]),
                             "replicas": len(r)})
        a4 = pd.DataFrame(rows)
        a4.to_csv(CSV / f"A4_F_verdict_{name.replace(' ', '_').replace('%', 'pc').replace(',', '')}.csv", index=False)
        md += [f"## A4. Verdict for family F under coding replicas ({name}, {len(r)} replicas)", "", a4.to_markdown(index=False, floatfmt=".3f"), ""]

    (NUM / "pending_part_A.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md)[:4000])


if __name__ == "__main__":
    main()
