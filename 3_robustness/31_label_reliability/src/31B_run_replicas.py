"""Stage 3 of the coding-error check for P1: 1 000 replicas at 15 %, every result recomputed on each.

    python 31B_run_replicas.py                       # 1 000 replicas, seed 20261118, 14 workers; resumes where it stopped
    python 31B_run_replicas.py --n 1000 --workers 14
    python 31B_run_replicas.py --summary-only        # rebuild summary.csv / unstable.txt / replicas.csv from the saved replicas

Replica i is perturb.Perturber(base).replica(SEED, i): its random numbers depend only on (SEED, i), so the result does not depend
on the number of workers, on their order, or on a restart. The original table is evaluated in the same run (replica -1) and
compared with results/reliability/baseline.csv.

Progress: every replica is appended to replicas.jsonl as it finishes (flushed to disk every 50); a restart skips the replicas
already there. At the end: replicas.csv, summary.csv, unstable.txt, run_log.txt (all in results/reliability/).
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from multiprocessing import get_context

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np
import pandas as pd

import core
import perturb

SEED = 20261118
N = 1000
SAVE_EVERY = 50
UNSTABLE = 0.10
# Optional settings through the environment (defaults = the first run: 15 %, the thesis's 1 000 shuffles):
#   EVTOL_RATE   error rate per coded value (0.15)
#   EVTOL_PERMS  permutations per band (1000, the thesis value)
#   EVTOL_TAG    sub-folder of results/31_label_reliability for the outputs ("" = the folder itself)
RATE = float(os.environ.get("EVTOL_RATE", "0.15"))
PERMS = int(os.environ.get("EVTOL_PERMS", "1000"))
TAG = os.environ.get("EVTOL_TAG", "")
perturb.R = RATE
OUT = core.OUT / TAG if TAG else core.OUT
JSONL = OUT / "replicas.jsonl"

_W = {}


def _init():
    import warnings
    warnings.filterwarnings("ignore")
    _W["base"] = core.load()
    _W["P"] = perturb.Perturber(_W["base"], r=RATE)
    if PERMS != 1000:
        _W["base"].m.q7.PERMS = PERMS


def _one(i: int) -> dict:
    base, P = _W["base"], _W["P"]
    t0 = time.time()
    if i < 0:
        m, log = base.master, {"replica": -1, "codes changed": 0, "designs changed": 0, "redraws": 0, "designs redrawn": 0,
                               "designs kept after 20 redraws": 0}
    else:
        m, log = P.replica(SEED, i)
    res = core.evaluate(base, m)
    rows = list(P.rows)
    a0, a1 = base.master.loc[rows, "topType"].astype(str), m.loc[rows, "topType"].astype(str)
    log["architecture labels changed"] = int((a0.values != a1.values).sum())
    log["designs"] = len(rows)
    log["seconds"] = round(time.time() - t0, 1)
    return {"log": log, "results": {k: (v.item() if hasattr(v, "item") else v) for k, v in res.items()}}


def wilson(k: int, n: int, z: float = 1.959964) -> tuple:
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def _is_bool(v) -> bool:
    return isinstance(v, (bool, np.bool_))


def summarise(rows: list, base_res: dict) -> tuple:
    """summary.csv and unstable.txt from the replica rows (replica -1 = the original table)."""
    reps = [r for r in rows if r["log"]["replica"] >= 0]
    n = len(reps)
    out, unstable = [], []
    for key, b in base_res.items():
        vals = [r["results"].get(key) for r in reps]
        got = [v for v in vals if v is not None and not (isinstance(v, float) and np.isnan(v))]
        nt = len(got)
        row = {"result": key.split("|")[0].strip() if key[:1].isdigit() else "0", "key": key, "original value": b,
               "replicas": n, "replicas where it is computed": nt}
        if _is_bool(b):
            k_true = sum(bool(v) for v in got)
            k_same = sum(bool(v) == bool(b) for v in got)
            lo, hi = wilson(k_true, nt)
            slo, shi = wilson(k_same, nt)
            row.update({"kind": "yes/no", "share of replicas where it holds": k_true / nt if nt else np.nan,
                        "holds, Wilson 95 % low": lo, "holds, Wilson 95 % high": hi,
                        "share of replicas with the original verdict": k_same / nt if nt else np.nan,
                        "original verdict, Wilson 95 % low": slo, "original verdict, Wilson 95 % high": shi})
            changed = 1 - (k_same / n if n else np.nan)          # a replica where it cannot be computed counts as changed
        elif isinstance(b, (int, float, np.integer, np.floating)):
            x = np.array([float(v) for v in got], dtype=float)
            row.update({"kind": "number", "median": float(np.median(x)) if nt else np.nan,
                        "5th percentile": float(np.percentile(x, 5)) if nt else np.nan,
                        "95th percentile": float(np.percentile(x, 95)) if nt else np.nan})
            changed = np.nan                                     # a number moves in almost every replica: not listed as unstable
        else:
            k_same = sum(str(v) == str(b) for v in got)
            row.update({"kind": "category", "share of replicas with the original value": k_same / nt if nt else np.nan})
            changed = 1 - (k_same / n if n else np.nan)
        row["share of replicas where it changes"] = changed
        out.append(row)
        if not np.isnan(changed) and changed > UNSTABLE:
            unstable.append((key, b, changed, nt))
    return pd.DataFrame(out), unstable


def write_outputs(rows: list, base_res: dict, meta: dict) -> None:
    rows = sorted(rows, key=lambda r: r["log"]["replica"])
    keys = list(base_res) + sorted({k for r in rows for k in r["results"]} - set(base_res))
    flat = [{**r["log"], **{k: r["results"].get(k) for k in keys}} for r in rows if r["log"]["replica"] >= 0]
    pd.DataFrame(flat).to_csv(OUT / "replicas.csv", index=False)
    summ, unstable = summarise(rows, base_res)
    summ.to_csv(OUT / "summary.csv", index=False)
    n = sum(r["log"]["replica"] >= 0 for r in rows)
    lines = [f"Results that change in more than {UNSTABLE:.0%} of the {n} replicas (error rate {perturb.R:.0%} per coded value, "
             f"seed {SEED}). Yes/no and category results only: numbers move in almost every replica and are read in summary.csv "
             f"(median, 5th-95th percentile). A replica where a result cannot be computed (e.g. an architecture under 20 designs "
             f"has no trend test) counts as a change.", ""]
    for key, b, ch, nt in sorted(unstable, key=lambda t: -t[2]):
        lines.append(f"{ch:6.1%} changed | original {b} | computed in {nt} of {n} | {key}")
    (OUT / "unstable.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    logs = pd.DataFrame([r["log"] for r in rows if r["log"]["replica"] >= 0])
    meta = dict(meta)
    meta["replicas done"] = int(len(logs))
    if len(logs):
        for c in ("codes changed", "designs changed", "redraws", "designs redrawn", "designs kept after 20 redraws", "architecture labels changed", "values with no allowed alternative", "seconds"):
            if c not in logs: continue
            meta[f"{c}: total, median, min, max"] = [float(logs[c].sum()), float(logs[c].median()), float(logs[c].min()), float(logs[c].max())]
    (OUT / "run_log.txt").write_text(json.dumps(meta, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")


def _versions() -> dict:
    import matplotlib
    import scipy
    v = {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "scipy": scipy.__version__,
         "matplotlib": matplotlib.__version__, "machine": f"{platform.node()} {os.cpu_count()} cores"}
    for name, path in (("thesis code commit", core.THESIS_CODE), ("dataset repo commit", core.REPO)):
        try:
            h = subprocess.run(["git", "-C", str(path), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
            dirty = subprocess.run(["git", "-C", str(path), "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True).stdout.strip()
            v[name] = h + (" (with uncommitted changes)" if dirty else "")
        except Exception as e:                                   # noqa: BLE001
            v[name] = f"unknown ({e})"
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=N)
    ap.add_argument("--workers", type=int, default=14)
    ap.add_argument("--summary-only", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    done = []
    if JSONL.exists():
        done = [json.loads(l) for l in JSONL.read_text(encoding="utf-8").splitlines() if l.strip()]
    have = {r["log"]["replica"] for r in done}
    meta = {"task": "coding-error check for P1 (Stage 3)", "seed": SEED, "replica random numbers": "numpy default_rng([seed, i])",
            "replicas asked": a.n, "error rate per coded value": perturb.R, "max redraws per design": perturb.MAX_REDRAWS, "lock rule": perturb.LOCK_MODE,
            "rules": {"counts perturbed (observed frequencies)": perturb.COUNTS, "only values the wizard asks for": perturb.APPLICABLE_ONLY},
            "share rule of result 1": core.SHARE_RULE, "permutations per band": f"{PERMS} (seed 42)", "error rate": RATE,
            "yaml": str(core.YAML), "workers": a.workers, "versions": _versions()}
    t0 = time.time()
    if not a.summary_only:
        todo = ([-1] if -1 not in have else []) + [i for i in range(a.n) if i not in have]
        print(f"{len(have)} saved, {len(todo)} to run on {a.workers} workers", flush=True)
        if todo:
            with open(JSONL, "a", encoding="utf-8") as fh, get_context("fork").Pool(a.workers, initializer=_init) as pool:
                for k, r in enumerate(pool.imap_unordered(_one, todo), 1):
                    fh.write(json.dumps(r, default=str) + "\n")
                    done.append(r)
                    if k % SAVE_EVERY == 0 or k == len(todo):
                        fh.flush()
                        os.fsync(fh.fileno())
                        el = time.time() - t0
                        print(f"{k} / {len(todo)} done, {el / 60:.0f} min, about {el / k * (len(todo) - k) / 60:.0f} min left", flush=True)
        meta["runtime of this call (min)"] = round((time.time() - t0) / 60, 1)
    base_res = next(r["results"] for r in done if r["log"]["replica"] == -1)
    # the original table evaluated in this run must equal baseline.csv
    diff = []
    if PERMS == 1000 and (core.OUT / "baseline.csv").exists():
        bl = pd.read_csv(core.OUT / "baseline.csv")
        diff = [k for k, v in zip(bl["key"], bl["value"]) if str(base_res.get(k)) != str(v)]
        meta["original table in this run equals baseline.csv"] = not diff
    if diff:
        meta["keys that differ from baseline.csv"] = diff
    write_outputs(done, base_res, meta)
    print(json.dumps({k: meta[k] for k in meta if k != "versions"}, indent=1, default=str))


if __name__ == "__main__":
    sys.exit(main())
