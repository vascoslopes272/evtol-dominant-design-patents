"""P1 weight results for condition 3 (disparity): test 1 (main text, three levels, two bases) and test 2 (family F, exploratory).

Design of 2026-11-18: the 15 dimension weights of Table A.11 are ONE flat list (architecture is one of the 15; no system
structure). A random draw multiplies each of the 15 weights by its own factor exp(N(0, 0.35^2)). The 1 000 draws are made once,
seed logged, and saved to ``weight_draws_1000.csv`` (in the results folder) (15 factors per row); both tests read that file.

Everything that computes is imported from ``ws_core`` (the shared code): the per-dimension matrices read with the
thesis code, the weighted Gower distance, Rao's Q, dQ, the permutation band (10 000 shuffles, seed 42, the same in every run),
the parallel / GPU runner, saving every 50 draws and resuming. This file only says which designs, which weights, and how the
results are summarised.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

import ws_core as ws

HERE = Path(__file__).resolve().parent
RESULTS_P1 = ws.RESULTS                         # eVTOL_dataset/07_results/72_weight_sensitivity (or WS_RESULTS)
INPUTS = RESULTS_P1 / "_inputs"                 # one version folder per dataset x level (or F x cohort), written by ws.build_inputs
DRAWS_FILE = RESULTS_P1 / "weight_draws_1000.csv"
DRAW_SEED = 42                                  # logged in weight_draws_1000.json
DRAW_SIGMA = 0.35
N_DRAWS = 1000
LEVELS = {"L1": "A0", "L2": "A1t", "L3": "A0c"}   # L1 = A (architecture), L2 = A·W·T, L3 = A·U (thesis code ids)
LEVEL_WORDS = {"L1": "L1, A: architecture", "L2": "L2, A·W·T: architecture, wings, tilt", "L3": "L3, A·U: architecture, propulsor units"}
F_COHORTS = ("2016-19", "2020-23")
F_MIN_EARLY = 20                                # stop test 2 if F's two earliest cohorts hold fewer designs together
DATASETS = ("v1", "thesis")

#: the 15 weights as one flat list, in the order of Table A.11. Values exactly as the thesis code holds them (1/45 and 1/3,
#: printed 0.022 and 0.333 in the table), so the baseline reproduces the thesis.
W0 = ws.weights()
WEIGHTS15 = dict(zip(ws.DIMS, W0))
EQUAL = np.ones(len(ws.DIMS))
W0_NO_ARCH = W0.copy()
W0_NO_ARCH[ws.DIMS.index("Architecture")] = 0.0


# ------------------------------------------------------------------------------------------------ the 1 000 draws, once
def weight_draws() -> pd.DataFrame:
    """The 1 000 x 15 factors exp(N(0, 0.35^2)), made once with seed 42 and saved; read back afterwards. A file that exists is
    never overwritten; its log must name the same seed, sigma and count."""
    log = DRAWS_FILE.with_suffix(".json")
    if DRAWS_FILE.exists():
        meta = json.loads(log.read_text(encoding="utf-8"))
        assert (meta["seed"], meta["sigma"], meta["draws"]) == (DRAW_SEED, DRAW_SIGMA, N_DRAWS), f"{DRAWS_FILE} was made with {meta}"
        return pd.read_csv(DRAWS_FILE, index_col="draw")
    RESULTS_P1.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(DRAW_SEED)
    f = np.exp(rng.normal(0.0, DRAW_SIGMA, size=(N_DRAWS, len(ws.DIMS))))
    t = pd.DataFrame(f, columns=ws.DIMS, index=pd.RangeIndex(N_DRAWS, name="draw"))
    t.to_csv(DRAWS_FILE, float_format="%.10f")
    log.write_text(json.dumps({"seed": DRAW_SEED, "sigma": DRAW_SIGMA, "draws": N_DRAWS, "generator": "numpy default_rng(seed).normal(0, sigma, (draws, 15)), exp",
                               "numpy": np.__version__, "made": time.strftime("%Y-%m-%d %H:%M:%S"), "columns": ws.DIMS}, indent=1), encoding="utf-8")
    return pd.read_csv(DRAWS_FILE, index_col="draw")


def _write_weights(folder: Path, test: str, base_w: np.ndarray) -> None:
    """weights_<test>.csv in an input folder: the weights of each draw = base_w x factors (ws_core reads it in every worker)."""
    p = Path(folder) / f"weights_{test}.csv"
    w = weight_draws() * base_w
    if p.exists():
        assert np.allclose(pd.read_csv(p, index_col="draw")[ws.DIMS].to_numpy(), w.to_numpy()), f"{p} holds other weights"
        return
    w.to_csv(p, float_format="%.12f")


# ------------------------------------------------------------------------------------------------ inputs
def prepare(dataset: str) -> dict:
    """Read the dataset with the thesis code (ws.build_inputs) for the three levels (cohort 2020-23) and for family F alone
    (cohorts 2016-19 and 2020-23). Returns the folders and the output folder of this data version."""
    folders = {lvl: ws.build_inputs(dataset, level=code, root=INPUTS, verbose=False) for lvl, code in LEVELS.items()}
    for c in F_COHORTS:
        folders[f"F {c}"] = ws.build_inputs(dataset, only="F", cohort=c, root=INPUTS, verbose=False)
    fp = hashlib.sha256("".join(p.name for p in folders.values()).encode()).hexdigest()[:8]
    n = json.loads((folders["L1"] / "inputs.json").read_text(encoding="utf-8"))["designs"]
    out = RESULTS_P1 / f"{dataset}_{n}designs_{fp}"
    out.mkdir(parents=True, exist_ok=True)
    (RESULTS_P1 / f"LATEST_{dataset}.txt").write_text(out.name, encoding="utf-8")
    for lvl in LEVELS:
        _write_weights(folders[lvl], "test1", W0)
    for c in F_COHORTS:
        _write_weights(folders[f"F {c}"], "test2", W0_NO_ARCH)        # architecture kept at 0, its factor ignored
    (out / "input_folders.json").write_text(json.dumps({k: str(v.relative_to(RESULTS_P1)) for k, v in folders.items()}, indent=1), encoding="utf-8")
    print(f"[{dataset}] {n} designs at L1 -> {out.name}")
    return {"folders": folders, "out": out, "dataset": dataset}


def designs_per_cohort(p: dict) -> pd.DataFrame:
    """Designs per cohort at each level (and actively protected), and in family F (the designs of each input folder)."""
    rows = {}
    for k, f in p["folders"].items():
        if k == "F 2016-19":
            continue
        z = np.load(f / "inputs.npz")
        win, ap, names = z["window"], z["ap"], [str(w) for w in z["win_names"]]
        key = "F" if k.startswith("F") else k
        rows[key] = {w: int((win == w).sum()) for w in names}
        if not k.startswith("F"):
            rows[f"{k} actively protected"] = {w: int(((win == w) & ap).sum()) for w in names}
    return pd.DataFrame(rows).T


def baseline_checks(p: dict) -> pd.DataFrame:
    """ws.baseline_check on every input folder: the thesis code and this code on the same 1 000 shuffles (stops if they differ),
    and this code on the 10 000 shuffles of the tests. Baseline = the 15 weights of Table A.11 (architecture included)."""
    parts = []
    for k, f in p["folders"].items():
        t = ws.baseline_check(f)
        t.columns = ["base", "designs in the cohort", *t.columns[2:]]
        parts.append(t.assign(inputs=k))
    t = pd.concat(parts, ignore_index=True)
    return t[["inputs", *t.columns[:-1]]]


def timing(p: dict) -> pd.DataFrame:
    """20 draws timed on all CPU cores and on the GPU, for the largest input (L1) and for F; the estimate of both tests."""
    b1, b2 = ws.benchmark(p["folders"]["L1"]), ws.benchmark(p["folders"]["F 2020-23"])
    runs1, runs2 = len(LEVELS) * (N_DRAWS + 2), len(F_COHORTS) * (N_DRAWS + 1)
    rows = []
    for test, b, runs in (("test 1", b1, runs1), ("test 2", b2, runs2)):
        per = b["GPU, s per draw"] if b["backend"] == "gpu" else b["CPU parallel, s per draw"]
        rows.append({"test": test, "cores": b["cores"], "RAM GB": b["RAM GB"], "GPU": b["GPU"], "CPU parallel, s per run": b["CPU parallel, s per draw"],
                     "GPU, s per run": b["GPU, s per draw"], "used": b["backend"], "runs": runs, "estimated minutes": round(per * runs / 60, 1),
                     "shuffles per band": ws.PERMS})
    t = pd.DataFrame(rows)
    print(f"estimated total: {t['estimated minutes'].sum():.1f} minutes (limit for keeping {ws.PERMS} shuffles: 48 h)")
    return t


# ------------------------------------------------------------------------------------------------ test 1
def run_test1(p: dict, backend: str = "cpu") -> None:
    """Per level: the baseline and the equal-weights run (fixed), then the 1 000 draws, band rebuilt in each run; saved every 50
    draws, resumable. Both bases in every run."""
    for lvl in LEVELS:
        f = p["folders"][lvl]
        print(f"\n-- test 1, {LEVEL_WORDS[lvl]}")
        ws.run_fixed(f, [("baseline", "test1", "Table A.11", W0), ("equal weights", "test1", "all 15 weights equal", EQUAL)])
        ws.run_random(f, "test1", N_DRAWS, backend=backend)


def _fixed(f: Path, run: str) -> pd.DataFrame:
    t = pd.read_csv(f / "results_fixed.csv")
    return t[t["run"].eq(run)].set_index("base")


def _random(f: Path, test: str) -> pd.DataFrame:
    t = pd.read_csv(f / f"results_random_{test}.csv")
    return t[t["draw"] < N_DRAWS].drop_duplicates(["draw", "base"]).sort_values(["draw", "base"])


def _share(g: pd.DataFrame) -> dict:
    k, n = int(g["holds"].sum()), len(g)
    lo, hi = ws.wilson(k, n)
    return {"draws": n, "share that holds": k / n, "Wilson 95 % low": lo, "Wilson 95 % high": hi, "median margin": g["margin"].median(),
            "margin 5th percentile": g["margin"].quantile(0.05), "margin 95th percentile": g["margin"].quantile(0.95)}


def summary_test1(p: dict) -> pd.DataFrame:
    """test1_draws.csv (one row per draw, level and base) and test1_summary.csv (per level and base: the draws, the equal-weights
    run, and the baseline beside them)."""
    draws, rows = [], []
    for lvl in LEVELS:
        f = p["folders"][lvl]
        r = _random(f, "test1")
        draws.append(r.assign(level=lvl)[["level", "draw", "base", "dQ", "band edge", "margin", "holds", *[c for c in r if c.startswith("w: ")]]])
        eq, b0 = _fixed(f, "equal weights"), _fixed(f, "baseline")
        z = np.load(f / "inputs.npz")
        for base in ws.BASES:
            n = int(((z["window"] == ws.COHORT) & (z["ap"] if base == "actively protected" else True)).sum())
            rows.append({"level": lvl, "level in words": LEVEL_WORDS[lvl], "base": base, "designs in 2020-23": n,
                         **_share(r[r["base"].eq(base)]),
                         "equal weights: dQ": eq.loc[base, "dQ"], "equal weights: band edge": eq.loc[base, "band edge"],
                         "equal weights: margin": eq.loc[base, "margin"], "equal weights: holds": bool(eq.loc[base, "holds"]),
                         "baseline: dQ": b0.loc[base, "dQ"], "baseline: band edge": b0.loc[base, "band edge"],
                         "baseline: margin": b0.loc[base, "margin"], "baseline: holds": bool(b0.loc[base, "holds"])})
    pd.concat(draws, ignore_index=True).to_csv(p["out"] / "test1_draws.csv", index=False)
    t = pd.DataFrame(rows)
    t.to_csv(p["out"] / "test1_summary.csv", index=False)
    return t


def figure_test1(p: dict, save: bool = True):
    """One panel per base; per level the margin of the 1 000 draws as a 5th-95th percentile bar with a median dot, the
    equal-weights run as a diamond, the baseline as an open circle; vertical line at zero (the band edge)."""
    import matplotlib.pyplot as plt
    ink, muted, grid, bar, point = "#1f2328", "#6b7280", "#e5e7eb", "#9db7d5", "#1f4e79"
    t = pd.read_csv(p["out"] / "test1_summary.csv")
    fig, axes = plt.subplots(1, len(ws.BASES), figsize=(10.5, 3.0), sharey=True, sharex=True)
    for ax, base in zip(axes, ws.BASES):
        s = t[t["base"].eq(base)].reset_index(drop=True)
        ax.axvline(0, color=ink, lw=1.0, zorder=1)
        for y, r in s.iterrows():
            ax.plot([r["margin 5th percentile"], r["margin 95th percentile"]], [y, y], color=bar, lw=7, solid_capstyle="round", zorder=2)
            ax.plot(r["median margin"], y, "o", color=point, ms=7, mec="white", mew=1.2, zorder=4)
            ax.plot(r["equal weights: margin"], y - 0.28, "D", color=point, ms=6, mec="white", mew=1.0, zorder=4)
            ax.plot(r["baseline: margin"], y + 0.28, "o", mfc="white", mec=point, mew=1.4, ms=6, zorder=4)
        ax.set_title(base, loc="left", fontsize=10, color=ink)
        ax.set_xlabel("margin = band edge − ΔQ (2020–23)", fontsize=9, color=ink)
        ax.grid(axis="x", color=grid, lw=0.6)
        ax.set_axisbelow(True)
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.tick_params(axis="y", length=0, labelsize=9, colors=ink)
        ax.tick_params(axis="x", labelsize=8, colors=muted)
        ax.annotate("band edge", (0, -0.55), xytext=(-3, 0), textcoords="offset points", ha="right", va="center", fontsize=8, color=ink)
    lab = t[t["base"].eq(ws.BASES[0])]["level in words"].str.replace(": ", "\n", n=1).tolist()
    axes[0].set_yticks(range(len(lab)), lab)
    axes[0].set_ylim(len(lab) - 0.4, -0.8)
    handles = [plt.Line2D([], [], color=bar, lw=7, solid_capstyle="round", label="1 000 draws: 5th to 95th percentile"),
               plt.Line2D([], [], color=point, marker="o", ls="", ms=7, mec="white", label="1 000 draws: median"),
               plt.Line2D([], [], color=point, marker="D", ls="", ms=6, mec="white", label="all 15 weights equal"),
               plt.Line2D([], [], color=point, marker="o", ls="", ms=6, mfc="white", mew=1.4, label="Table A.11 weights")]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=8.5)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    if save:
        fig.savefig(p["out"] / "test1_figure.png", dpi=200)
        fig.savefig(p["out"] / "test1_figure.pdf", metadata={"CreationDate": None, "ModDate": None})
    return fig


# ------------------------------------------------------------------------------------------------ test 2 (family F)
def f_counts(p: dict) -> pd.DataFrame:
    """F designs per cohort; raises (stops test 2) when the two earliest cohorts hold fewer than F_MIN_EARLY together."""
    t = designs_per_cohort(p).loc[["F"]]
    early = int(t[list(ws.BASE_COHORTS)].sum(axis=1).iloc[0])
    t["two earliest together"] = early
    if early < F_MIN_EARLY:
        raise SystemExit(f"STOP: family F holds {early} designs in {ws.BASE_COHORTS} together, fewer than {F_MIN_EARLY}.\n{t.to_string()}")
    return t


def run_test2(p: dict, backend: str = "cpu") -> None:
    """Per cohort (2016-19, 2020-23): the baseline with architecture 0 (fixed), then the 1 000 draws with architecture kept at 0.
    Designs = F only; the shuffles move the cohort labels among the F designs; dQ and F's baseline are recomputed in each shuffle."""
    f_counts(p)
    for c in F_COHORTS:
        f = p["folders"][f"F {c}"]
        print(f"\n-- test 2, family F, cohort {c}")
        ws.run_fixed(f, [("baseline, architecture 0", "test2", "Table A.11, architecture 0", W0_NO_ARCH)])
        ws.run_random(f, "test2", N_DRAWS, backend=backend)


def summary_test2(p: dict) -> pd.DataFrame:
    """test2_draws.csv (one row per draw and cohort) and test2_summary.csv (per cohort). All-designs base only: the engine also
    computes an 'actively protected' row on F, which is not part of test 2 and is left out here (it stays in the raw files)."""
    draws, rows = [], []
    cnt = designs_per_cohort(p).loc["F"]
    for c in F_COHORTS:
        f = p["folders"][f"F {c}"]
        r = _random(f, "test2")
        r = r[r["base"].eq("all designs")]
        draws.append(r.assign(cohort=c)[["cohort", "draw", "dQ", "band edge", "margin", "holds", *[x for x in r if x.startswith("w: ")]]])
        b = _fixed(f, "baseline, architecture 0").loc["all designs"]
        eng = ws.engine(f)
        r1 = eng.one(W0_NO_ARCH, ws.THESIS_PERMS)["all designs"]
        rows.append({"cohort": c, "F designs in the cohort": int(cnt[c]), "F designs in the two earliest cohorts": int(cnt[list(ws.BASE_COHORTS)].sum()),
                     "baseline (architecture 0): dQ": b["dQ"], "baseline: band edge": b["band edge"], "baseline: margin": b["margin"],
                     "baseline: dQ below band": bool(b["holds"]), f"baseline: band edge with {ws.THESIS_PERMS} shuffles": r1[1],
                     **_share(r)})
    pd.concat(draws, ignore_index=True).to_csv(p["out"] / "test2_draws.csv", index=False)
    t = pd.DataFrame(rows).rename(columns={"share that holds": "share of draws with dQ below band"})
    t.to_csv(p["out"] / "test2_summary.csv", index=False)
    return t


# ------------------------------------------------------------------------------------------------ test 2, exploratory additions (2026-11-22)
#: The author's choice of 2026-11-22, made after test 2 was run: three exploratory readings of family F, reported as such.
PEAK, LATE = "2016-19", "2020-23"


def _f_engine(p: dict):
    """The F inputs (all F designs; cohort labels in engine.window) and their architecture (SLC / CVT, from design_frame.csv)."""
    f = p["folders"][f"F {LATE}"]
    eng = ws.engine(f)
    arch = pd.read_csv(f / "design_frame.csv")["Architecture"].astype(str).to_numpy()
    return eng, arch


def _shuffled_blocks(pool: np.ndarray, n_first: int, perms: int, n: int):
    """10 000 shuffles (seed 42) of the designs in ``pool``: indicator matrices of the first n_first and of the rest."""
    rng = np.random.default_rng(ws.BAND_SEED)
    P = np.stack([rng.permutation(pool) for _ in range(perms)])
    Za, Zb = np.zeros((perms, n)), np.zeros((perms, n))
    np.put_along_axis(Za, P[:, :n_first], 1.0, axis=1)
    np.put_along_axis(Zb, P[:, n_first:], 1.0, axis=1)
    return Za, Zb


def _q_rows(D, V, Z):
    s = ((Z @ D) * Z).sum(axis=1)
    return s / (Z.sum(axis=1) ** 2 if V is None else ((Z @ V) * Z).sum(axis=1))


def f_since_peak(p: dict, draws: bool = True) -> tuple:
    """Exploratory: contraction of family F since its peak cohort. dQ = Q(F, 2020-23) - Q(F, 2016-19); band = the cohort labels of
    the F designs of those two cohorts shuffled 10 000 times (seed 42), edge = 2.5th percentile; holds = dQ below the edge.
    Rows: Table A.11 with architecture 0 and with architecture 1, then each dimension alone; with ``draws``, the 1 000 draws of
    weight_draws_1000.csv with architecture 0 (as in test 2). Writes test2_explore_since_peak.csv and _draws.csv."""
    eng, _ = _f_engine(p)
    a, b = np.flatnonzero(eng.window == PEAK), np.flatnonzero(eng.window == LATE)
    Za, Zb = _shuffled_blocks(np.r_[a, b], len(a), ws.PERMS, eng.n)

    def run(w):
        D, V = eng.distance(np.asarray(w, dtype=float))
        q = lambda i: float(D[np.ix_(i, i)].mean()) if V is None else float(D[np.ix_(i, i)].sum() / V[np.ix_(i, i)].sum())   # noqa: E731
        dq = q(b) - q(a)
        edge = float(np.percentile(_q_rows(D, V, Zb) - _q_rows(D, V, Za), 2.5))
        return {"Q 2016-19": q(a), "Q 2020-23": q(b), "dQ": dq, "band edge": edge, "margin": edge - dq, "holds": edge - dq > 0}

    rows = [{"weights": "Table A.11, architecture 0", **run(W0_NO_ARCH)}, {"weights": "Table A.11", **run(W0)}]
    rows += [{"weights": f"{d} alone", **run(np.eye(len(ws.DIMS))[k])} for k, d in enumerate(ws.DIMS) if d != "Architecture"]
    t = pd.DataFrame(rows)
    t.insert(1, "F designs 2016-19", len(a))
    t.insert(2, "F designs 2020-23", len(b))
    t.to_csv(p["out"] / "test2_explore_since_peak.csv", index=False)
    s = None
    if draws:
        path = p["out"] / "test2_explore_since_peak_draws.csv"
        if path.exists():
            dr = pd.read_csv(path)
        else:
            W = weight_draws().to_numpy() * W0_NO_ARCH
            dr = pd.DataFrame([{"draw": i, **run(w)} for i, w in enumerate(W)])
            dr.to_csv(path, index=False)
        s = pd.DataFrame([{"weights": "1 000 draws, architecture 0", **_share(dr)}])
    return t, s


def f_per_dimension(p: dict) -> pd.DataFrame:
    """Exploratory: each dimension alone (the Gower distance is then that dimension), F against its two earliest cohorts, for
    2016-19 and 2020-23, with the 10 000-shuffle band of test 2. Writes test2_explore_per_dimension.csv."""
    rows = []
    for c in F_COHORTS:
        eng = ws.engine(p["folders"][f"F {c}"])
        for k, d in enumerate(ws.DIMS):
            r = eng.one(np.eye(len(ws.DIMS))[k])["all designs"]
            rows.append({"dimension": d, "cohort": c, "dQ": r[0], "band edge": r[1], "margin": r[2], "dQ below band": r[3]})
    t = pd.DataFrame(rows).pivot(index="dimension", columns="cohort").reindex(ws.DIMS)
    t.columns = [f"{c}: {m}" for m, c in t.columns]
    t = t[[f"{c}: {m}" for c in F_COHORTS for m in ("dQ", "band edge", "margin", "dQ below band")]].reset_index()
    t.to_csv(p["out"] / "test2_explore_per_dimension.csv", index=False)
    return t


def f_slc_cvt(p: dict) -> pd.DataFrame:
    """Exploratory, descriptive (no band): per cohort, the mean distance between the Lift + Cruise and the CVT* designs of F, Q of
    each and of F, under Table A.11 with architecture 0. Writes test2_explore_slc_cvt.csv."""
    eng, arch = _f_engine(p)
    D, V = eng.distance(W0_NO_ARCH)
    m = lambda i, j: float(D[np.ix_(i, j)].mean()) if len(i) and len(j) else np.nan        # noqa: E731
    rows = []
    for c in eng.win_names:
        a = np.flatnonzero((eng.window == c) & (arch == "SLC"))
        b = np.flatnonzero((eng.window == c) & (arch == "CVT"))
        rows.append({"cohort": c, "Lift + Cruise designs": len(a), "CVT* designs": len(b), "CVT* share": len(b) / max(len(a) + len(b), 1),
                     "Q Lift + Cruise": m(a, a), "Q CVT*": m(b, b), "mean distance Lift + Cruise to CVT*": m(a, b), "Q of F": m(np.r_[a, b], np.r_[a, b])})
    t = pd.DataFrame(rows)
    t.to_csv(p["out"] / "test2_explore_slc_cvt.csv", index=False)
    return t
