"""Family F as a LEVEL in 2020-23: is F alike inside on five dimensions, and how does it compare with the designs not in F?

Separate from the within-F disparity test (notebooks/06_weight_sensitivity, test 2), which measures a fall over time.

Nothing of the measures is rewritten. The design table, F, the cohorts, the actively protected flag and the dimension values come
from the thesis code (eVTOL-Visual-Evaluation/labeling_evaluation, imported, never edited) through the reliability code of P1
(eVTOL-dataset-v1/reliability: core.load / core.context build the thesis context from a design table; perturb.Perturber makes a
coding-error replica). Outputs: eVTOL_dataset_v1/results/family_F_level/ on the Drive.

Designs: the 619 of the main test (an architecture recorded, a cohort, in the form distance), cohorts 2016-19 and 2020-23.
F = frames.dd_level_keys(...)["family_b"] == FAMILY_LABEL (every Lift + Cruise design and every CVT* design).

The five dimensions, read as the main test reads them (frames.form_frame15) except booms present:
  Number of wings         form_frame15 "Wing count" (wCount, 0 when no wing, blank under an M2 override); ordered 0..3, range 3
  Propulsor band          form_frame15 "Propulsor band" (frames.ROTOR_BINS: 1-3, 4, 5-6, 7-8, 9+); ordered rank 0..4, range 4
  Wing configuration      form_frame15 "Wing Architecture" (wingConf); categorical
  Tractor/pusher          form_frame15 "Tractor/Pusher Arrangement" (the set with the most propulsors); categorical
  Booms present           boomsPresent of the design (True / False; blank under an M1 override); categorical. Not one of the 15
                          dimensions of the main test (Boom count is); compared as a categorical dimension.
Blank = not answered: left out of n, of the shares and of Q.

Tests (2020-23, each base):
  top-option share of F and of the non-F designs (each group's own most common option), difference F - non-F,
  Newcombe hybrid score 95 % interval of the difference (built from the two Wilson intervals, Newcombe 1998, method 10),
  permutation test: the F label shuffled among the 2020-23 designs of the base, 10 000 shuffles, seed 42, the same shuffles for
  every dimension; band = 2.5th and 97.5th percentiles of the shuffled difference; p two-sided = (1 + #|d*| >= |d|) / (1 + 10 000);
  Holm over the five dimensions, per base.
  Rao's Q of each dimension alone (the Gower distance is then that dimension, so the weights of the main test cancel): Q of F, Q of
  the non-F designs, their difference, with the band and p of the same shuffles. Q is the mean distance over all ordered pairs,
  diagonal included, as the thesis computes it (lib.dominant_design.mean_pairwise_distance); for a categorical dimension that is
  1 - sum of squared shares.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REL = HERE.parents[1] / "reliability"
if str(REL) not in sys.path:
    sys.path.insert(0, str(REL))
import core       # noqa: E402
import perturb    # noqa: E402

OUT = core.DRIVE / "results" / "family_F_level"
COHORTS = ("2016-19", "2020-23")
TEST_COHORT = "2020-23"
BASES = ("all designs", "actively protected")
PERMS = 10_000
PERM_SEED = 42
SIM_SEED = 20261118            # the seed of the coding simulation (reliability/31B_run_replicas.py)
SIM_N = 1000
SAVE_EVERY = 50
#: dimension -> (column of form_frame15 or None, kind, range). kind "ordered" keeps a rank; "categorical" an option.
DIMS = {
    "Number of wings": ("Wing count", "ordered", 3.0),
    "Propulsor band": ("Propulsor band", "ordered", 4.0),
    "Wing configuration": ("Wing Architecture", "categorical", None),
    "Tractor/pusher arrangement": ("Tractor/Pusher Arrangement", "categorical", None),
    "Booms present": (None, "categorical", None),
}


# ------------------------------------------------------------------------------------------------------------- the design frame
def design_frame(base, master: pd.DataFrame | None = None) -> pd.DataFrame:
    """One row per design of the main test: aircraft_id, cohort, F, actively protected, and the five dimensions (option labels;
    ordered dimensions also as '<name> rank'). ``master`` = a design table (default the original)."""
    m = base.m
    fr = m.frames
    ctx = core.context(base, base.master if master is None else master)
    ds, v = ctx.ds, ctx.v
    ff = fr.form_frame15(ds)
    sub = v[fr.archetype_key(v, "A0").notna()].dropna(subset=["window"])
    sub = sub[sub["aircraft_id"].isin(set(ff["aircraft_id"]))]
    fam = fr.dd_level_keys(ds, v)["family_b"].eq(fr.FAMILY_LABEL)
    live = v["aircraft_id"].map(fr.patent_state(ds, v)["in_force"]).astype(bool)
    out = pd.DataFrame({"aircraft_id": sub["aircraft_id"].to_numpy(), "cohort": sub["window"].astype(str).to_numpy(),
                        "F": fam.loc[sub.index].to_numpy(), "actively protected": live.loc[sub.index].to_numpy()})
    f15 = ff.set_index("aircraft_id").loc[out["aircraft_id"]]
    var = ds.variants.set_index("aircraft_id").loc[out["aircraft_id"]]
    m1 = fr.override_sets(ds.variants).set_axis(ds.variants["aircraft_id"]).loc[out["aircraft_id"]].map(lambda o: "M1" in o).to_numpy()
    labels = fr.ROTOR_BINS[1]
    for name, (col, kind, _) in DIMS.items():
        if name == "Booms present":
            b = var["boomsPresent"].map(lambda x: {"True": "yes", "False": "no"}.get(str(x).strip(), np.nan)).to_numpy(dtype=object)
            b[m1] = np.nan
            out[name] = b
        elif kind == "ordered":
            x = pd.to_numeric(f15[col], errors="coerce").to_numpy()
            out[f"{name} rank"] = x
            lab = (lambda r: labels[int(r)]) if name == "Propulsor band" else (lambda r: str(int(r)))
            out[name] = [lab(r) if not np.isnan(r) else np.nan for r in x]
        else:
            out[name] = f15[col].to_numpy(dtype=object)
    return out


# ------------------------------------------------------------------------------------------------------------- task 1 and 2
def top_table(df: pd.DataFrame) -> pd.DataFrame:
    """Per cohort (2016-19, 2020-23), base, group (F / not F) and dimension: designs, n answered, the most common option and its
    share, whether another option ties with it, and every option with its count."""
    rows = []
    for c in COHORTS:
        for b in BASES:
            d = df[df["cohort"].eq(c) & (df["actively protected"] if b == "actively protected" else True)]
            for g, gm in (("F", d["F"]), ("not F", ~d["F"])):
                x = d[gm]
                for name in DIMS:
                    vc = x[name].dropna().astype(str).value_counts()
                    n = int(vc.sum())
                    rows.append({"cohort": c, "base": b, "group": g, "dimension": name, "designs": len(x), "n answered": n,
                                 "top option": vc.index[0] if n else "", "top-option share": vc.iloc[0] / n if n else np.nan,
                                 "tied top": bool(n and (vc == vc.iloc[0]).sum() > 1),
                                 "options (count)": "; ".join(f"{k} {v}" for k, v in vc.items())})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------------------- task 3 and 4
def wilson(k: int, n: int, z: float = 1.959964) -> tuple:
    return core_wilson(k, n, z)


def core_wilson(k, n, z=1.959964):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def newcombe(k1, n1, k2, n2) -> tuple:
    """Newcombe (1998) hybrid score interval of p1 - p2, from the Wilson intervals of p1 and p2 (method 10)."""
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = core_wilson(k1, n1)
    l2, u2 = core_wilson(k2, n2)
    d = p1 - p2
    return (d - np.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + np.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2))


def holm(p) -> np.ndarray:
    p = np.asarray(p, dtype=float)
    o = np.argsort(p)
    adj = np.empty_like(p)
    run = 0.0
    for i, j in enumerate(o):
        run = max(run, (len(p) - i) * p[j])
        adj[j] = min(1.0, run)
    return adj


def shuffles(n_designs: int, n_f: int) -> np.ndarray:
    """PERMS rows of the F label shuffled among the designs (seed 42): boolean matrix PERMS x n_designs."""
    rng = np.random.default_rng(PERM_SEED)
    lab = np.zeros(n_designs, dtype=bool)
    lab[:n_f] = True
    return np.stack([rng.permutation(lab) for _ in range(PERMS)])


def _stats(C: np.ndarray, A: np.ndarray | None, rng_: float | None):
    """From counts per option C (rows = shuffles or one row): top-option share and Rao's Q (diagonal included)."""
    n = C.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        top = C.max(axis=1) / n
        if A is None:
            q = 1.0 - ((C / n[:, None]) ** 2).sum(axis=1)
        else:
            q = np.einsum("pi,ij,pj->p", C, A, C) / (n ** 2) / rng_
    return top, q


def level_tests(df: pd.DataFrame, cohort: str = TEST_COHORT, perms: np.ndarray | dict | None = None) -> pd.DataFrame:
    """Task 3 and 4 for one cohort, both bases: per dimension, F against the non-F designs."""
    rows = []
    for b in BASES:
        d = df[df["cohort"].eq(cohort) & (df["actively protected"] if b == "actively protected" else True)].reset_index(drop=True)
        L = d["F"].to_numpy()
        P = shuffles(len(d), int(L.sum())) if perms is None or b not in perms else perms[b]
        part = []
        for name, (_, kind, rng_) in DIMS.items():
            ans = d[name].notna().to_numpy()
            if kind == "ordered":
                vals = d.loc[ans, f"{name} rank"].to_numpy(dtype=float)
                opts = np.unique(vals)
                A = np.abs(opts[:, None] - opts[None, :])
                codes = np.searchsorted(opts, vals)
                names = [d.loc[ans, name].to_numpy()[np.flatnonzero(codes == i)[0]] for i in range(len(opts))]
            else:
                lab = d.loc[ans, name].astype(str).to_numpy()
                names, codes = np.unique(lab, return_inverse=True)
                A = None
            O = np.eye(len(names))[codes]                                      # answered designs x options
            total = O.sum(axis=0)
            cf = L[ans].astype(float) @ O
            tF, qF = _stats(cf[None, :], A, rng_)
            tN, qN = _stats((total - cf)[None, :], A, rng_)
            CF = P[:, ans].astype(float) @ O
            sF, sqF = _stats(CF, A, rng_)
            sN, sqN = _stats(total[None, :] - CF, A, rng_)
            dt, dq = tF[0] - tN[0], qF[0] - qN[0]
            dts, dqs = sF - sN, sqF - sqN
            nF, nN = int(cf.sum()), int((total - cf).sum())
            kF, kN = int(cf.max()), int((total - cf).max())
            lo, hi = newcombe(kF, nF, kN, nN)
            part.append({"base": b, "cohort": cohort, "dimension": name,
                         "F n answered": nF, "F top option": names[int(np.argmax(cf))], "F top-option share": tF[0],
                         "not F n answered": nN, "not F top option": names[int(np.argmax(total - cf))], "not F top-option share": tN[0],
                         "difference in top-option share (F - not F)": dt, "Newcombe 95 % low": lo, "Newcombe 95 % high": hi,
                         "permutation band 2.5 %": float(np.nanpercentile(dts, 2.5)), "permutation band 97.5 %": float(np.nanpercentile(dts, 97.5)),
                         "permutation p (two-sided)": (1 + int(np.sum(np.abs(dts) >= abs(dt) - 1e-12))) / (1 + len(dts)),
                         "Q of F": qF[0], "Q of not F": qN[0], "Q difference (F - not F)": dq,
                         "Q band 2.5 %": float(np.nanpercentile(dqs, 2.5)), "Q band 97.5 %": float(np.nanpercentile(dqs, 97.5)),
                         "Q permutation p (two-sided)": (1 + int(np.sum(np.abs(dqs) >= abs(dq) - 1e-12))) / (1 + len(dqs))})
        t = pd.DataFrame(part)
        t.insert(t.columns.get_loc("permutation p (two-sided)") + 1, "permutation p (Holm)", holm(t["permutation p (two-sided)"]))
        t["Q permutation p (Holm)"] = holm(t["Q permutation p (two-sided)"])
        t["F alike as a level"] = ((t["difference in top-option share (F - not F)"] > 0) & (t["Newcombe 95 % low"] > 0)
                                   & (t["difference in top-option share (F - not F)"] > t["permutation band 97.5 %"])
                                   & (t["permutation p (Holm)"] < 0.05))
        rows.append(t)
    return pd.concat(rows, ignore_index=True)


def check_q_against_thesis_code(base, df: pd.DataFrame) -> pd.DataFrame:
    """Q of F and of the non-F designs in 2020-23 (all designs) from the thesis functions (lib.distance.gower_distance on the one
    dimension, lib.dominant_design.mean_pairwise_distance), against this module's count formula. Raises if they differ."""
    sys.path.insert(0, str(core.THESIS_CODE))
    from lib import distance as _dist, dominant_design as dd          # noqa: E402
    d = df[df["cohort"].eq(TEST_COHORT)].reset_index(drop=True)
    t = level_tests(df).query("base == 'all designs'").set_index("dimension")
    rows = []
    for name, (_, kind, rng_) in DIMS.items():
        col = f"{name} rank" if kind == "ordered" else name
        fr = d[[col]].rename(columns={col: "x"})
        D = _dist.gower_distance(fr, ["x"], {"x"} if kind == "ordered" else set(), {"x": 1.0}, ranges={"x": rng_} if rng_ else None)
        for g, mask, key in (("F", d["F"], "Q of F"), ("not F", ~d["F"], "Q of not F")):
            idx = np.flatnonzero(mask.to_numpy() & d[col].notna().to_numpy())
            q = dd.mean_pairwise_distance(D, idx)
            rows.append({"dimension": name, "group": g, "Q, thesis code": q, "Q, this module": t.loc[name, key]})
    c = pd.DataFrame(rows)
    gap = float((c["Q, thesis code"] - c["Q, this module"]).abs().max())
    if gap > 1e-12:
        raise SystemExit(f"STOP: Q differs from the thesis code by {gap}")
    return c


# ------------------------------------------------------------------------------------------------------------- task 5
_W: dict = {}


def _init():
    import warnings
    warnings.filterwarnings("ignore")
    _W["base"] = core.load()
    _W["P"] = perturb.Perturber(_W["base"], r=perturb.R)


def _replica(i: int) -> dict:
    base, P = _W["base"], _W["P"]
    t0 = time.time()
    m, log = P.replica(SIM_SEED, i)
    df = design_frame(base, m)
    top = top_table(df)
    lt = level_tests(df)
    return {"replica": i, "seconds": round(time.time() - t0, 1), "codes changed": log.get("codes changed"),
            "F designs 2020-23": int(df.loc[df["cohort"].eq(TEST_COHORT), "F"].sum()),
            "top": top[["cohort", "base", "group", "dimension", "n answered", "top option", "top-option share"]].to_dict("records"),
            "tests": lt.drop(columns=[c for c in lt.columns if c.startswith("Q ")]).to_dict("records")}


def run_simulation(n: int = SIM_N, workers: int = 14) -> None:
    """The 1 000 replicas of the coding simulation (15 % per value, seed 20261118), in parallel, saved every 50, resumable."""
    from multiprocessing import get_context
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "simulation_replicas.jsonl"
    have = set()
    if path.exists():
        have = {json.loads(l)["replica"] for l in path.read_text(encoding="utf-8").splitlines() if l.strip()}
    todo = [i for i in range(n) if i not in have]
    print(f"{len(have)} replicas on disk, {len(todo)} to run on {workers} workers", flush=True)
    if not todo:
        return
    t0 = time.time()
    with open(path, "a", encoding="utf-8") as fh, get_context("fork").Pool(workers, initializer=_init) as pool:
        for k, r in enumerate(pool.imap_unordered(_replica, todo), 1):
            fh.write(json.dumps(r, default=lambda o: o.item() if hasattr(o, "item") else str(o)) + "\n")
            if k % SAVE_EVERY == 0 or k == len(todo):
                fh.flush()
                os.fsync(fh.fileno())
                el = time.time() - t0
                print(f"{k} / {len(todo)} replicas, {el / 60:.1f} min, about {el / k * (len(todo) - k) / 60:.0f} min left", flush=True)


def time_replicas(k: int = 3) -> float:
    """Seconds per replica on one core (perturbation + rebuild + tests)."""
    _init()
    t = time.time()
    for i in range(k):
        _replica(i)
    return (time.time() - t) / k


def summary_simulation(original: pd.DataFrame) -> pd.DataFrame:
    """Per base and dimension (2020-23): the share of replicas in which F's top-option share stays above that of the non-F
    designs (Wilson 95 %), the share in which F is 'alike as a level' by the rule of task 3, the share in which F keeps its
    original top option, and the difference in top-option share (median, 5th and 95th percentile)."""
    recs = [json.loads(l) for l in (OUT / "simulation_replicas.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    recs = [r for r in recs if r["replica"] < SIM_N]
    t = pd.DataFrame([{**x, "replica": r["replica"]} for r in recs for x in r["tests"]])
    t.to_csv(OUT / "simulation_tests_per_replica.csv", index=False)
    pd.DataFrame([{**x, "replica": r["replica"]} for r in recs for x in r["top"]]).to_csv(OUT / "simulation_top_per_replica.csv", index=False)
    o = original.set_index(["base", "dimension"])
    rows = []
    for (b, dim), g in t.groupby(["base", "dimension"], sort=False):
        n = len(g)
        above = int((g["difference in top-option share (F - not F)"] > 0).sum())
        alike = int(g["F alike as a level"].astype(bool).sum())
        same = int(g["F top option"].astype(str).eq(str(o.loc[(b, dim), "F top option"])).sum())
        lo, hi = core_wilson(above, n)
        alo, ahi = core_wilson(alike, n)
        d = g["difference in top-option share (F - not F)"]
        rows.append({"base": b, "dimension": dim, "replicas": n, "original difference": o.loc[(b, dim), "difference in top-option share (F - not F)"],
                     "replicas with F top share above not F": above, "share": above / n, "Wilson 95 % low": lo, "Wilson 95 % high": hi,
                     "replicas with F alike as a level (task 3 rule)": alike, "share alike": alike / n, "alike, Wilson low": alo, "alike, Wilson high": ahi,
                     "replicas with F's original top option": same,
                     "difference: median": d.median(), "difference: 5th percentile": d.quantile(0.05), "difference: 95th percentile": d.quantile(0.95)})
    s = pd.DataFrame(rows)
    s.to_csv(OUT / "simulation_summary.csv", index=False)
    return s
