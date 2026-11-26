"""Weight sensitivity of condition 3 (disparity): the shared code of the notebooks in this folder.

Specification: ``Weight sensitivity of condition 3 tests, sources and justifications.md`` (same folder).

The measure is NOT rewritten here. ``build_inputs`` calls the thesis code (eVTOL-Visual-Evaluation/labeling_evaluation:
``viz.frames.gower_inputs``, ``lib.distance.gower_distance``, ``lib.dominant_design.cohesion_band``,
``viz.analysis_iii.form_ap_vs_all``) once, to get, per dimension k, the pairwise distance matrix d_k and the "both answered"
matrix delta_k. Every run is then

    D(w) = sum_k w_k d_k delta_k / sum_k w_k delta_k          (Gower, thesis A.3.7)
    Q(S) = mean of D over all ordered pairs of S              (Rao's Q as the thesis computes it, diagonal included)
    dQ   = Q(2020-23) - mean(Q(<= 2011), Q(2012-15))
    band = 2.5th percentile of dQ* over shuffles of the designs across cohorts, cohort sizes kept
    margin = band edge - dQ ; holds = margin > 0

on two bases: all designs, and actively protected (Q of the actively protected designs of 2020-23 against the all-designs
baseline; band on all designs with the 2020-23 block cut at the actively protected size), as ``form_ap_vs_all`` does.

The shuffles are drawn once (seed 42, the thesis seed) and reused in every run, so two runs differ only by their weights.
The first 1 000 shuffles are exactly those of the thesis, which is how the baseline check reproduces its numbers.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]                                              # the root of this repository
ANALYSIS = REPO / "2_analysis"
DATASET_ROOT = Path(os.environ.get("EVTOL_DATASET", REPO.parent / "eVTOL_dataset"))   # the public dataset (or set EVTOL_DATASET)
RESULTS = Path(os.environ.get("WS_RESULTS", DATASET_ROOT / "07_results" / "72_weight_sensitivity"))   # where the tests write and read
THESIS_CODE = Path(os.environ.get("WS_THESIS_CODE", ANALYSIS / "src"))   # the packages viz and lib of the analysis
DATASETS = {
    # the public dataset: 2_analysis/20_config.yaml reads it from EVTOL_DATASET
    "v1": {"yaml": ANALYSIS / "20_config.yaml", "words": "the public dataset (621 designs)"},
    # the frozen thesis table is not part of the public dataset: point WS_THESIS_YAML at its config to run the baseline check
    "thesis": {"yaml": Path(os.environ.get("WS_THESIS_YAML", ANALYSIS / "20_config.yaml")), "words": "the frozen thesis table (baseline check)"},
}

# ------------------------------------------------------------------------------------------------ settings
COHORT = "2020-23"
BASE_COHORTS = ("<= 2011", "2012-15")
BASES = ("all designs", "actively protected")
BAND_SEED = 42                # the thesis seed; the first THESIS_PERMS shuffles are the thesis's own
THESIS_PERMS = 1000
PERMS = 10_000                # per band (author's decision of 2026-11-13; the thesis uses 1 000)
N_DRAWS = 1000
SAVE_EVERY = 50
SIGMA_LEVEL = 0.354           # test 2: log-normal factor, 95 % between x0.5 and x2
TEST_SEEDS = {"test2": 42, "test3a": 42, "test3b": 42}     # one seed everywhere (author, 2026-11-16); each draw has its own stream [seed, draw number]
THESIS_TARGET = {"dQ": -0.028, "band edge": -0.020}     # what the baseline check must give on the thesis data (3 decimals)

SYSTEMS = ("G1 architecture", "M1 structure", "M2 aerodynamics", "M3 propulsion")
#: (system, dimension, baseline share inside the system, rank inside the system; equal rank = tied in Table A.11)
TABLE_A11 = [
    ("G1 architecture", "Architecture", 1.0, 1),
    ("M1 structure", "Fuselage Shape", 0.50, 1),
    ("M1 structure", "Boom count", 0.30, 2),
    ("M1 structure", "Fuselage Kinematics", 0.20, 3),
    ("M2 aerodynamics", "Wing count", 0.30, 2),
    ("M2 aerodynamics", "Wing Architecture", 0.30, 2),
    ("M2 aerodynamics", "Vertical Position", 1 / 45, 3),
    ("M2 aerodynamics", "Longitudinal Position", 1 / 45, 3),
    ("M2 aerodynamics", "Planform", 1 / 45, 3),
    ("M2 aerodynamics", "Empennage Type", 1 / 3, 1),
    ("M3 propulsion", "Propulsor band", 0.35, 1),
    ("M3 propulsion", "Tilt share", 0.30, 2),
    ("M3 propulsion", "Propulsor Enclosure", 0.15, 3),
    ("M3 propulsion", "Tractor/Pusher Arrangement", 0.10, 4),
    ("M3 propulsion", "Mount locations", 0.10, 4),
]
DIMS = [d for _, d, _, _ in TABLE_A11]
SYS_OF = {d: s for s, d, _, _ in TABLE_A11}
SHARE0 = {d: sh for _, d, sh, _ in TABLE_A11}
RANK = {d: r for _, d, _, r in TABLE_A11}
LEVEL0 = {s: 1.0 for s in SYSTEMS}
#: candidates of the scope check (Section 4) and the system each would enter
CANDIDATES = {"Boom attachment": "M1 structure", "Boom retraction": "M1 structure",
              "Second-wing role": "M2 aerodynamics", "Tip-joined wings": "M2 aerodynamics"}
SCREEN_MIN_ANSWERED = 0.50    # "most designs answer it"
SCREEN_MAX_TOP = 0.80         # "no single option holds more than 80 %"


# ------------------------------------------------------------------------------------------------ weights
def weights(level=None, shares=None, dims=None) -> np.ndarray:
    """Dimension weights = system weight x share inside the system, in the order of ``dims`` (default the 15)."""
    level = {**LEVEL0, **(level or {})}
    shares = {**SHARE0, **(shares or {})}
    dims = DIMS if dims is None else dims
    return np.array([level[SYS_OF.get(d) or CANDIDATES[d]] * shares[d] for d in dims], dtype=float)


def dims_of(system: str) -> list:
    return [d for d in DIMS if SYS_OF[d] == system]


def draw_test2(rng) -> np.ndarray:
    """Each of the four level weights x exp(N(0, 0.354^2)), independent; shares at baseline."""
    f = np.exp(rng.normal(0.0, SIGMA_LEVEL, size=len(SYSTEMS)))
    return weights(level={s: float(x) for s, x in zip(SYSTEMS, f)})


def _ranked_shares(system: str, drawn: np.ndarray) -> dict:
    """Largest drawn share to the top-ranked dimension, and so on; tied dimensions take the mean of their drawn shares."""
    ds = sorted(dims_of(system), key=lambda d: RANK[d])          # stable: ties keep the table order
    srt = np.sort(drawn)[::-1]
    out = dict(zip(ds, srt))
    for r in {RANK[d] for d in ds}:
        tied = [d for d in ds if RANK[d] == r]
        m = float(np.mean([out[d] for d in tied]))
        for d in tied:
            out[d] = m
    return out


def draw_test3(rng, keep_order: bool) -> np.ndarray:
    """Per system, shares from Dirichlet(1,...,1) (uniform on the simplex). 3a: sorted into the order of Table A.11, ties
    averaged. 3b: as drawn. Level weights at 1. The systems are drawn in the order of SYSTEMS (architecture has one dimension)."""
    shares = {}
    for s in SYSTEMS:
        ds = dims_of(s)
        x = rng.dirichlet(np.ones(len(ds)))
        shares.update(_ranked_shares(s, x) if keep_order else dict(zip(ds, x)))
    return weights(shares=shares)


DRAWERS = {"test2": draw_test2, "test3a": lambda rng: draw_test3(rng, True), "test3b": lambda rng: draw_test3(rng, False)}


def draw_weights(test: str, i: int) -> np.ndarray:
    """Weights of draw ``i`` of a random test. One independent stream per draw, derived from the test seed, so the result of a
    draw does not depend on the number of workers nor on where a restart happened."""
    return DRAWERS[test](np.random.default_rng([TEST_SEEDS[test], i]))


def fixed_runs() -> list:
    """The 7 fixed runs of tests 1 to 3, after the baseline: (run id, test, description, weights of the 15)."""
    runs = [("baseline", "baseline", "Table A.11", weights())]
    for a in (0.0, 0.5, 2.0):
        runs.append((f"T1 architecture x{a:g}", "test1", f"architecture weight {a:g}", weights(level={"G1 architecture": a})))
    for s in SYSTEMS[1:]:
        runs.append((f"T2 without {s}", "test2", f"{s} weight 0", weights(level={s: 0.0})))
    eq = {d: 1.0 / len(dims_of(SYS_OF[d])) for d in DIMS}
    runs.append(("T3b equal shares", "test3b", "equal shares inside each system", weights(shares=eq)))
    return runs


def drop_one_runs() -> list:
    """Scope check: each dimension dropped in turn; the other shares of its system rescaled to sum to 1 (author's decision
    of 2026-11-13). Dropping Architecture leaves its system empty: the same weights as 'T1 architecture x0'."""
    runs = []
    for d in DIMS:
        rest = [x for x in dims_of(SYS_OF[d]) if x != d]
        tot = sum(SHARE0[x] for x in rest)
        sh = {d: 0.0, **{x: SHARE0[x] / tot for x in rest}}
        runs.append((f"drop {d}", "scope", f"{d} out, {SYS_OF[d]} rescaled", weights(shares=sh)))
    return runs


def extra_run(admitted: list):
    """Scope check, the extra run: each admitted candidate enters its system at the mean share of that system; shares rescaled
    to sum to 1. Returns (dimension list, weights)."""
    dims = DIMS + list(admitted)
    shares = dict(SHARE0)
    for s in SYSTEMS:
        new = [c for c in admitted if CANDIDATES[c] == s]
        if not new:
            continue
        old = dims_of(s)
        mean = 1.0 / len(old)
        tot = 1.0 + mean * len(new)
        for d in old:
            shares[d] = SHARE0[d] / tot
        for c in new:
            shares[c] = mean / tot
    return dims, weights(shares=shares, dims=dims)


# ------------------------------------------------------------------------------------------------ inputs (thesis code, once)
def _candidate_columns(v: pd.DataFrame, ovs: pd.Series) -> pd.DataFrame:
    """One value per aircraft for the four candidates (author's rule of 2026-11-13). Boom attachment and retraction read the boom
    set with the most booms (first listed on a tie), as the thesis does for the propulsor enclosure; 'none' when the design has
    no booms. Second-wing role reads wing 2; 'none' with fewer than two wings. Tip-joined is yes when any wing is ticked, no when
    one is recorded and none ticked; 'none' with no wing. Blank (not answered, or hidden by an M1 / M2 override) stays blank."""
    s = lambda x: "" if x is None or (isinstance(x, float) and np.isnan(x)) or pd.isna(x) else str(x).strip()      # noqa: E731
    num = lambda x: float(pd.to_numeric(x, errors="coerce")) if s(x) else 0.0                                          # noqa: E731
    rows = []
    for (_, r), ov in zip(v.iterrows(), ovs):
        g = lambda c: r[c] if c in r.index else None                                                                   # noqa: E731
        att = ret = role = tip = np.nan
        if "M1" not in ov:
            if s(g("boomsPresent")) != "True":
                att = ret = "none"
            else:
                sets_ = [(k, num(g(f"boom{k}_count"))) for k in range(1, 7) if s(g(f"boom{k}_attach")) or num(g(f"boom{k}_count")) > 0]
                if sets_:
                    k = max(sets_, key=lambda t: t[1])[0]            # max keeps the first on a tie
                    att = s(g(f"boom{k}_attach")) or np.nan
                    ret = {"True": "retracts", "False": "fixed"}.get(s(g(f"boom{k}_retracts")), np.nan)
        if "M2" not in ov:
            wc = num(g("wCount"))
            role = "none" if wc < 2 else (s(g("wing2_role")) or np.nan)
            if wc < 1:
                tip = "none"
            else:
                ticks = [s(g(f"wing{k}_tipJoin")) for k in range(1, 5)]
                tip = "yes" if "True" in ticks else "no" if "False" in ticks else np.nan
        rows.append({"Boom attachment": att, "Boom retraction": ret, "Second-wing role": role, "Tip-joined wings": tip})
    return pd.DataFrame(rows, index=v.index, dtype=object)


LEVEL_LABEL = {"A0": "A", "A1t": "A·W·T", "A0c": "A·U"}          # thesis code ids -> the labels of form_ap_vs_all


def build_inputs(dataset: str, verbose: bool = True, level: str = "A0", only: str | None = None, cohort: str = COHORT,
                 root: Path | None = None) -> Path:
    """Read one dataset with the thesis code and store everything the tests need. Returns the folder of this dataset version
    (``results/<dataset>_<n>designs_<hash>``); the same data give the same folder, changed data a new one. A folder whose
    inputs are unchanged is not written again.

    Options (added 2026-11-18 for the P1 tests; the default folder is RESULTS):
    level  = the level of description whose designs enter ("A0" = A, "A1t" = A·W·T, "A0c" = A·U); Q does not depend on the
             level, the level only decides which designs have a key (frames.archetype_key);
    only   = "F" keeps the designs of family F only (frames.dd_level_keys, family_b == FAMILY_LABEL);
    cohort = the cohort whose dQ is read (the Engine reads it from inputs.json);
    root   = folder the version folder is written in (default RESULTS)."""
    import warnings
    warnings.filterwarnings("ignore")
    import matplotlib
    matplotlib.use("Agg")
    sys.path.insert(0, str(THESIS_CODE))
    from lib import distance as _dist, dominant_design as dd          # noqa: E402
    from viz import analysis_iii, config, frames, thesis, thesis_q7      # noqa: E402

    cfg = config.load(DATASETS[dataset]["yaml"])
    ctx = thesis.context(cfg)
    frames.set_window_bounds(cfg)
    assert ctx.SEED == BAND_SEED and thesis_q7.PERMS == THESIS_PERMS
    fi = frames.gower_inputs(ctx.ds)
    assert fi.fields == DIMS, "the thesis code lists other dimensions than Table A.11 here"
    w_code = np.array([fi.weights[d] for d in DIMS])
    assert np.allclose(w_code, weights()), "the weights in the thesis code differ from Table A.11 as written here"
    D_ref = _dist.gower_distance(fi.frame, fi.fields, fi.numeric, fi.weights, ranges=fi.ranges, sets=fi.sets)

    # the designs and their order, exactly as dd_form_table / form_ap_vs_all take them (level A)
    v = ctx.v
    at = {a: i for i, a in enumerate(fi.frame["aircraft_id"].to_numpy())}
    sub = v[frames.archetype_key(v, level).notna()].dropna(subset=["window"]).copy()
    if only == "F":
        sub = sub[frames.dd_level_keys(ctx.ds, v)["family_b"].loc[sub.index].eq(frames.FAMILY_LABEL)]
    elif only is not None:
        raise ValueError(f"unknown subset {only!r}")
    sub["row"] = sub["aircraft_id"].map(at)
    sub = sub[sub["row"].notna()]
    rows = sub["row"].astype(int).to_numpy()
    live = v["aircraft_id"].map(frames.patent_state(ctx.ds, v)["in_force"]).astype(bool)[sub.index].to_numpy()

    def per_dim(frame, field):
        d = _dist.gower_distance(frame, [field], fi.numeric, {field: 1.0}, ranges=fi.ranges, sets=fi.sets)[np.ix_(rows, rows)]
        both = ~np.isnan(d)
        return np.where(both, d, 0.0), both

    d0, dl = zip(*(per_dim(fi.frame, d) for d in DIMS))
    vv = ctx.ds.variants
    vv = vv[vv["topType"].notna()]
    assert (vv.index == fi.frame.index).all()
    cand = _candidate_columns(vv, frames.override_sets(vv))
    c0, cl = zip(*(per_dim(cand, c) for c in CANDIDATES))

    # the thesis's own numbers on this dataset (1 000 shuffles, seed 42), for the baseline check
    tb = dd.cohesion_band(D_ref, rows, sub["window"].to_numpy(), ctx.WIN_NAMES, perms=THESIS_PERMS, seed=ctx.SEED)
    r_all = tb[tb["window"].eq(cohort)].iloc[0]
    ref = {"all designs": {"designs": int(r_all["aircraft"]), "dQ": float(r_all["ΔQ"]), "band edge": float(r_all["ΔQ permutation low"])}}
    if only is None:                                  # the actively protected base exists in the thesis code for the levels, not for F alone
        ap = analysis_iii.form_ap_vs_all(ctx, cohort)
        r_ap = ap[ap["level"].eq(LEVEL_LABEL[level])].iloc[0]
        ref["actively protected"] = {"designs": int(r_ap["actively protected designs"]), "dQ": float(r_ap["ΔQ"]), "band edge": float(r_ap["band low"])}

    arr = dict(d0=np.stack(d0), dl=np.stack(dl), c0=np.stack(c0), cl=np.stack(cl), D_ref=D_ref[np.ix_(rows, rows)],
               window=sub["window"].to_numpy().astype(str), ap=live, aircraft_id=sub["aircraft_id"].to_numpy().astype(str),
               win_names=np.array(ctx.WIN_NAMES))
    h = hashlib.sha256()
    for k in ("d0", "dl", "c0", "cl", "window", "ap", "aircraft_id"):
        h.update(np.ascontiguousarray(arr[k]).tobytes())
    h.update(json.dumps([PERMS, BAND_SEED, N_DRAWS, TEST_SEEDS, [list(map(str, t)) for t in TABLE_A11]]).encode())
    default = level == "A0" and only is None and cohort == COHORT
    tag = "" if default else (f"F_{cohort}_" if only == "F" else f"{LEVEL_LABEL[level].replace('·', '')}_{cohort}_")
    if not default:
        h.update(tag.encode())
    root = Path(root) if root is not None else RESULTS
    out = root / f"{dataset}_{tag}{len(rows)}designs_{h.hexdigest()[:8]}"
    latest_file = root / f"LATEST_{dataset}{'' if default else '_' + tag.rstrip('_')}.txt"
    if (out / "inputs.json").exists() and json.loads((out / "inputs.json").read_text(encoding="utf-8")).get("fingerprint") == h.hexdigest():
        latest_file.write_text(out.name, encoding="utf-8")
        if verbose:
            print(f"[{dataset}] {len(rows)} designs -> {out.name} (unchanged, nothing rewritten)")
        return out
    out.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out / "inputs.npz", **arr)
    frame = fi.frame.set_index("aircraft_id").loc[arr["aircraft_id"]].join(cand.set_index(vv["aircraft_id"]))
    frame.insert(0, "cohort", arr["window"])
    frame.insert(1, "actively protected", live)
    frame.to_csv(out / "design_frame.csv")
    meta = {"dataset": dataset, "words": DATASETS[dataset]["words"], "yaml": str(DATASETS[dataset]["yaml"]), "designs": int(len(rows)),
            "built": time.strftime("%Y-%m-%d %H:%M:%S"), "fingerprint": h.hexdigest(), "thesis_code_reference": ref,
            "settings": {"PERMS": PERMS, "THESIS_PERMS": THESIS_PERMS, "BAND_SEED": BAND_SEED, "N_DRAWS": N_DRAWS,
                         "SIGMA_LEVEL": SIGMA_LEVEL, "TEST_SEEDS": TEST_SEEDS, "COHORT": COHORT}}
    if not default:
        meta.update({"level": level, "only": only, "cohort": cohort})
    (out / "inputs.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
    latest_file.write_text(out.name, encoding="utf-8")
    if verbose:
        print(f"[{dataset}] {len(rows)} designs -> {out.name}")
    return out


def latest(dataset: str) -> Path:
    """Folder of the last built version of a dataset."""
    return RESULTS / (RESULTS / f"LATEST_{dataset}.txt").read_text(encoding="utf-8").strip()


# ------------------------------------------------------------------------------------------------ the engine
class Engine:
    """One dataset version in memory: the per-dimension matrices and the shuffles. ``run(W)`` evaluates weight sets."""

    def __init__(self, folder: Path, perms: int = PERMS, backend: str = "cpu", extras: tuple = ()):
        z = np.load(folder / "inputs.npz", allow_pickle=False)
        self.folder, self.perms, self.backend = Path(folder), perms, backend
        self.window, self.ap, self.win_names = z["window"], z["ap"], [str(w) for w in z["win_names"]]
        self.D_ref = z["D_ref"]
        d0, dl = z["d0"], z["dl"].astype(float)
        if extras:
            idx = [list(CANDIDATES).index(c) for c in extras]
            d0 = np.concatenate([d0, z["c0"][idx]])
            dl = np.concatenate([dl, z["cl"][idx].astype(float)])
        self.n = n = len(self.window)
        self.K = len(d0)
        sizes = [int((self.window == w).sum()) for w in self.win_names]
        cuts = np.cumsum([0] + sizes)
        meta = json.loads((Path(folder) / "inputs.json").read_text(encoding="utf-8"))
        self.cohort = cohort = meta.get("cohort", COHORT)             # P1 test 2 reads 2016-19 too (2026-11-18)
        k0, k1, kt = (self.win_names.index(w) for w in (*BASE_COHORTS, cohort))
        self.obs = {"b0": np.flatnonzero(self.window == BASE_COHORTS[0]), "b1": np.flatnonzero(self.window == BASE_COHORTS[1]),
                    "all designs": np.flatnonzero(self.window == cohort),
                    "actively protected": np.flatnonzero((self.window == cohort) & self.ap)}
        n_ap = len(self.obs["actively protected"])
        # the shuffles: one generator seeded as the thesis seeds its own, one permutation of the designs per shuffle
        rng = np.random.default_rng(BAND_SEED)
        base = np.arange(n)
        P = np.stack([rng.permutation(base) for _ in range(perms)])
        blocks = {"b0": P[:, cuts[k0]:cuts[k0 + 1]], "b1": P[:, cuts[k1]:cuts[k1 + 1]],
                  "all designs": P[:, cuts[kt]:cuts[kt + 1]], "actively protected": P[:, cuts[kt]:cuts[kt] + n_ap]}
        self.Z = {}
        for name, idx in blocks.items():
            Z = np.zeros((perms, n))
            np.put_along_axis(Z, idx, 1.0, axis=1)
            self.Z[name] = Z
        self.d0, self.dl = d0, dl
        if backend == "gpu":
            import torch
            self.t = torch
            dev = torch.device("cuda:0")
            self.d0_t = torch.as_tensor(d0, device=dev, dtype=torch.float64)
            self.dl_t = torch.as_tensor(dl, device=dev, dtype=torch.float64)
            self.Z_t = {k: torch.as_tensor(Z, device=dev, dtype=torch.float64) for k, Z in self.Z.items()}

    # ---- distance and Q
    def distance(self, w: np.ndarray):
        """(D with 0 where no dimension is shared, validity mask or None when every pair is valid)."""
        num = np.tensordot(w, self.d0, axes=1)
        den = np.tensordot(w, self.dl, axes=1)
        valid = den > 0
        if valid.all():
            return num / den, None
        return np.where(valid, num / np.where(valid, den, 1.0), 0.0), valid.astype(float)

    @staticmethod
    def _q_obs(D, V, idx):
        blk = D[np.ix_(idx, idx)]
        return float(blk.mean()) if V is None else float(blk.sum() / V[np.ix_(idx, idx)].sum())

    def _q_perm(self, D, V, Z):
        s = ((Z @ D) * Z).sum(axis=1)
        return s / (Z.sum(axis=1)[0] ** 2 if V is None else ((Z @ V) * Z).sum(axis=1))

    def one(self, w: np.ndarray, perms: int | None = None) -> dict:
        """One run: {base: (dQ, band edge, margin, holds)} for one weight vector. ``perms`` < self.perms reads the first shuffles."""
        if self.backend == "gpu":
            return self._one_gpu(w, perms)
        D, V = self.distance(np.asarray(w, dtype=float))
        sl = slice(0, perms or self.perms)
        ref = (self._q_obs(D, V, self.obs["b0"]) + self._q_obs(D, V, self.obs["b1"])) / 2
        ref_p = (self._q_perm(D, V, self.Z["b0"][sl]) + self._q_perm(D, V, self.Z["b1"][sl])) / 2
        out = {}
        for b in BASES:
            dq = self._q_obs(D, V, self.obs[b]) - ref
            edge = float(np.percentile(self._q_perm(D, V, self.Z[b][sl]) - ref_p, 2.5))
            out[b] = (dq, edge, edge - dq, bool(edge - dq > 0))
        return out

    def _one_gpu(self, w, perms=None):
        t = self.t
        wt = t.as_tensor(np.asarray(w, dtype=float), device=self.d0_t.device)
        num = t.tensordot(wt, self.d0_t, dims=1)
        den = t.tensordot(wt, self.dl_t, dims=1)
        valid = den > 0
        V = None if bool(valid.all()) else valid.to(t.float64)
        D = t.where(valid, num / t.where(valid, den, t.ones_like(den)), t.zeros_like(num))
        sl = slice(0, perms or self.perms)

        def q_obs(idx):
            i = t.as_tensor(idx, device=D.device)
            blk = D[i][:, i]
            return float(blk.mean()) if V is None else float(blk.sum() / V[i][:, i].sum())

        def q_perm(Z):
            s = ((Z @ D) * Z).sum(dim=1)
            return s / (Z.sum(dim=1)[0] ** 2 if V is None else ((Z @ V) * Z).sum(dim=1))

        ref = (q_obs(self.obs["b0"]) + q_obs(self.obs["b1"])) / 2
        ref_p = (q_perm(self.Z_t["b0"][sl]) + q_perm(self.Z_t["b1"][sl])) / 2
        out = {}
        for b in BASES:
            dq = q_obs(self.obs[b]) - ref
            edge = float(np.percentile((q_perm(self.Z_t[b][sl]) - ref_p).cpu().numpy(), 2.5))
            out[b] = (dq, edge, edge - dq, bool(edge - dq > 0))
        return out


_ENGINES: dict = {}


def engine(folder, perms: int = PERMS, backend: str = "cpu", extras: tuple = ()) -> Engine:
    """The engine of a dataset version, built once per process (each worker of the pool keeps its own)."""
    key = (str(folder), perms, backend, tuple(extras))
    if key not in _ENGINES:
        _ENGINES[key] = Engine(Path(folder), perms, backend, tuple(extras))
    return _ENGINES[key]


def _rows(run_id, test, draw, w, res, dims) -> list:
    return [{"test": test, "run": run_id, "draw": draw, "base": b, "dQ": res[b][0], "band edge": res[b][1], "margin": res[b][2],
             "holds": res[b][3], **{f"w: {d}": float(x) for d, x in zip(dims, w)}} for b in BASES]


_WFILES: dict = {}


def file_weights(folder, test: str):
    """The weights of every draw of ``test`` when the folder holds ``weights_<test>.csv`` (one row per draw, one column per
    dimension of DIMS; added 2026-11-18: the P1 tests read their draws from one saved file). None when there is no such file."""
    p = Path(folder) / f"weights_{test}.csv"
    if not p.exists():
        return None
    if str(p) not in _WFILES:
        _WFILES[str(p)] = pd.read_csv(p, index_col="draw").sort_index()[DIMS].to_numpy(dtype=float)
    return _WFILES[str(p)]


def _chunk(folder, test, draws, backend="cpu"):
    """Worker: a block of draws of one random test (weights from ``weights_<test>.csv`` when the folder has it)."""
    eng = engine(folder, PERMS, backend)
    W = file_weights(folder, test)
    out = []
    for i in draws:
        w = W[int(i)] if W is not None else draw_weights(test, int(i))
        out += _rows(f"{test} draw {i}", test, int(i), w, eng.one(w), DIMS)
    return out


# ------------------------------------------------------------------------------------------------ hardware and timing
def hardware() -> dict:
    hw = {"cores": os.cpu_count(), "RAM GB": None, "GPU": None}
    try:
        import psutil
        hw["RAM GB"] = round(psutil.virtual_memory().total / 2 ** 30, 1)
    except Exception:
        pass
    try:
        import torch
        if torch.cuda.is_available():
            hw["GPU"] = f"{torch.cuda.device_count()} x {torch.cuda.get_device_name(0)}, {round(torch.cuda.get_device_properties(0).total_memory / 2 ** 30, 1)} GB (torch {torch.__version__})"
    except Exception:
        pass
    return hw


def benchmark(folder, n: int = 20) -> dict:
    """Time ``n`` draws on the parallel CPU version and on the GPU (if any); pick the faster. Start-up (loading the matrices,
    drawing the shuffles) is left out of both: it is paid once per worker, not per draw."""
    from joblib import Parallel, delayed
    cores = os.cpu_count()
    hw = hardware()
    blocks = [list(range(i, n, cores)) for i in range(min(cores, n))]
    with Parallel(n_jobs=cores) as par:
        par(delayed(_chunk)(folder, "test3b", [0]) for _ in range(cores))             # warm-up: every worker builds its engine
        t = time.perf_counter()
        par(delayed(_chunk)(folder, "test3b", b) for b in blocks)
        cpu = (time.perf_counter() - t) / n
    out = {**hw, "draws timed": n, "CPU parallel, s per draw": round(cpu, 4), "GPU, s per draw": None, "backend": "cpu"}
    if hw["GPU"]:
        try:
            import torch
            eng = engine(folder, PERMS, "gpu")
            eng.one(draw_weights("test3b", 0))
            torch.cuda.synchronize()
            t = time.perf_counter()
            for i in range(n):
                eng.one(draw_weights("test3b", i))
            torch.cuda.synchronize()
            gpu = (time.perf_counter() - t) / n
            out["GPU, s per draw"] = round(gpu, 4)
            if gpu < cpu:
                out["backend"] = "gpu"
        except Exception as e:                                     # a busy or missing GPU must not stop the run
            out["GPU, s per draw"] = f"failed: {type(e).__name__}"
    p = Path(folder) / "benchmark.json"
    if not p.exists():                                             # the first timing of a folder is kept (2026-11-18)
        p.write_text(json.dumps(out, indent=1), encoding="utf-8")
    return out


def estimate(bench: dict, n_fixed: int = 24, n_random: int = 3 * N_DRAWS) -> dict:
    per = bench["GPU, s per draw"] if bench["backend"] == "gpu" else bench["CPU parallel, s per draw"]
    total = per * (n_fixed + n_random)
    ten = per * (n_fixed + 3 * 10_000)
    return {"backend": bench["backend"], "s per run": per, "runs": n_fixed + n_random, "estimated total, minutes": round(total / 60, 1),
            "with 10 000 draws per random test, hours": round(ten / 3600, 2), "10 000 draws fit in 48 h": bool(ten < 48 * 3600)}


# ------------------------------------------------------------------------------------------------ running, saving, resuming
def baseline_check(folder) -> pd.DataFrame:
    """The baseline weights, three ways: the thesis code itself (stored when the inputs were built), this code on the thesis's
    1 000 shuffles, and this code on the PERMS shuffles used by the tests. Raises if this code does not reproduce the thesis code."""
    folder = Path(folder)
    meta = json.loads((folder / "inputs.json").read_text(encoding="utf-8"))
    eng = engine(folder)
    D, V = eng.distance(weights())
    gap = float(np.nanmax(np.abs(D - eng.D_ref)))
    r1, rN = eng.one(weights(), THESIS_PERMS), eng.one(weights())
    rows = []
    col = f"designs in {eng.cohort}"
    for b in meta["thesis_code_reference"]:              # F alone has the all-designs base only
        t = meta["thesis_code_reference"][b]
        rows.append({"base": b, col: t["designs"], "computed by": f"thesis code, {THESIS_PERMS} shuffles, seed {BAND_SEED}",
                     "dQ": t["dQ"], "band edge": t["band edge"], "margin": round(t["band edge"] - t["dQ"], 4)})
        rows.append({"base": b, col: len(eng.obs[b]), "computed by": f"this code, the same {THESIS_PERMS} shuffles",
                     "dQ": r1[b][0], "band edge": r1[b][1], "margin": r1[b][2]})
        rows.append({"base": b, col: len(eng.obs[b]), "computed by": f"this code, {PERMS} shuffles (used by every test)",
                     "dQ": rN[b][0], "band edge": rN[b][1], "margin": rN[b][2]})
        ok = round(r1[b][0], 4) == t["dQ"] and round(r1[b][1], 4) == t["band edge"]
        if not ok or gap > 1e-12:
            raise SystemExit(f"STOP: the baseline does not reproduce on {meta['dataset']} ({b}): thesis code {t}, this code {r1[b][:2]}, "
                             f"largest gap between the two distance matrices {gap:.2e}")
    t = pd.DataFrame(rows)
    if meta["dataset"] == "thesis" and "cohort" not in meta:      # the thesis target holds for level A, all designs, 2020-23
        got = meta["thesis_code_reference"]["all designs"]
        if round(got["dQ"], 3) != THESIS_TARGET["dQ"] or round(got["band edge"], 3) != THESIS_TARGET["band edge"]:
            raise SystemExit(f"STOP: the thesis data give dQ {got['dQ']} and band edge {got['band edge']}, not {THESIS_TARGET}")
    if not (folder / "baseline_check.csv").exists():             # written once per folder (2026-11-18)
        t.to_csv(folder / "baseline_check.csv", index=False)
    return t


def _append(path: Path, rows: list) -> None:
    pd.DataFrame(rows).to_csv(path, mode="a", header=not path.exists(), index=False)


def run_fixed(folder, runs: list, name: str = "results_fixed.csv", extras: tuple = (), dims=None, verbose: bool = True) -> pd.DataFrame:
    """Fixed runs, one row per run and base, appended to ``results_fixed.csv``; a run already in the file is not repeated."""
    path = Path(folder) / name
    done = set(pd.read_csv(path)["run"]) if path.exists() else set()
    eng = engine(folder, PERMS, "cpu", extras)
    for run_id, test, words, w in runs:
        if run_id in done:
            continue
        res = eng.one(w)
        rows = _rows(run_id, test, -1, w, res, dims or DIMS)
        for r in rows:
            r["description"] = words
        _append(path, [{k: r.get(k) for k in ["test", "run", "description", "base", "dQ", "band edge", "margin", "holds"]} |
                       {f"w: {d}": r.get(f"w: {d}", 0.0) for d in DIMS + list(CANDIDATES)} for r in rows])   # candidates: 0 unless admitted
        if verbose:
            print(f"  {run_id:<44}" + "   ".join(f"{b}: margin {res[b][2]:+.4f} holds {res[b][3]}" for b in BASES), flush=True)
    t = pd.read_csv(path)
    return t[t["run"].isin([r[0] for r in runs])].reset_index(drop=True)


def run_random(folder, test: str, n_draws: int = N_DRAWS, backend: str = "cpu", verbose: bool = True) -> pd.DataFrame:
    """A random test: ``n_draws`` draws, saved every SAVE_EVERY draws to ``results_random_<test>.csv``; a restart reads the file
    and continues with the draws not yet in it. Prints progress and the running share of draws in which the condition holds."""
    from joblib import Parallel, delayed
    folder = Path(folder)
    path = folder / f"results_random_{test}.csv"
    have = pd.read_csv(path) if path.exists() else None
    done = set() if have is None else set(have.groupby("draw")["base"].nunique().loc[lambda s: s == len(BASES)].index)
    todo = [i for i in range(n_draws) if i not in done]
    if verbose and done:
        print(f"  {test}: {len(done)} draws already on disk, {len(todo)} to go", flush=True)
    blocks = [todo[i:i + SAVE_EVERY] for i in range(0, len(todo), SAVE_EVERY)]
    holds = {b: 0 for b in BASES}
    seen = 0
    if have is not None and len(done):
        h = have[have["draw"].isin(done)]
        holds = {b: int(h.loc[h["base"].eq(b), "holds"].sum()) for b in BASES}
        seen = len(done)
    t0 = time.perf_counter()

    def note(rows):
        nonlocal seen
        _append(path, rows)
        seen += len(rows) // len(BASES)
        for r in rows:
            holds[r["base"]] += int(r["holds"])
        if verbose:
            print(f"  {test}: {seen:>5} / {n_draws} draws   holds: " + "   ".join(f"{b} {100 * holds[b] / seen:5.1f} %" for b in BASES)
                  + f"   ({time.perf_counter() - t0:.0f} s)", flush=True)

    if backend == "gpu":
        for b in blocks:
            note(_chunk(folder, test, b, "gpu"))
    elif blocks:
        cores = os.cpu_count()
        small = [blk[i::cores] for blk in blocks for i in range(cores) if blk[i::cores]]      # each saved block spread over the cores
        per_block = [sum(1 for i in range(cores) if blk[i::cores]) for blk in blocks]
        gen = Parallel(n_jobs=cores, return_as="generator")(delayed(_chunk)(folder, test, s) for s in small)
        for k in per_block:
            rows = [r for _ in range(k) for r in next(gen)]
            note(sorted(rows, key=lambda r: (r["draw"], BASES.index(r["base"]))))
    t = pd.read_csv(path)
    return t[t["draw"] < n_draws].drop_duplicates(["draw", "base"]).sort_values(["draw", "base"]).reset_index(drop=True)


# ------------------------------------------------------------------------------------------------ summaries
def wilson(k: int, n: int, z: float = 1.959964) -> tuple:
    """Wilson 95 % interval of a share k / n."""
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (c - h, c + h)


def summary_random(t: pd.DataFrame) -> pd.DataFrame:
    """Per random test and base: draws, share that holds with its Wilson 95 % interval, median margin, 5th and 95th percentile."""
    rows = []
    for (test, base), g in t.groupby(["test", "base"], sort=False):
        k, n = int(g["holds"].sum()), len(g)
        lo, hi = wilson(k, n)
        rows.append({"test": test, "base": base, "draws": n, "share that holds": k / n, "Wilson 95 % low": lo, "Wilson 95 % high": hi,
                     "median margin": g["margin"].median(), "margin 5th percentile": g["margin"].quantile(0.05),
                     "margin 95th percentile": g["margin"].quantile(0.95)})
    return pd.DataFrame(rows)


def screen_candidates(folder) -> pd.DataFrame:
    """Scope check, the screen: answer rate and top-option share of the four candidates ('none' counts as an answer and as an
    option). Admitted = answered by more than SCREEN_MIN_ANSWERED of the designs and no option above SCREEN_MAX_TOP."""
    f = pd.read_csv(Path(folder) / "design_frame.csv", keep_default_na=True, na_values=[""])
    rows = []
    for c, s in CANDIDATES.items():
        x = f[c]
        vc = x.dropna().astype(str).value_counts()
        ans, top = x.notna().mean(), vc.iloc[0] / vc.sum()
        rows.append({"candidate": c, "system": s, "designs": len(x), "answered": ans, "applies (not 'none')": (x.notna() & x.astype(str).ne("none")).mean(),
                     "top option": vc.index[0], "top-option share": top, "options": "; ".join(f"{k} {n}" for k, n in vc.items()),
                     "admitted": bool(ans > SCREEN_MIN_ANSWERED and top <= SCREEN_MAX_TOP)})
    t = pd.DataFrame(rows)
    t.to_csv(Path(folder) / "scope_candidates_screen.csv", index=False)
    return t


def collect(folder) -> dict:
    """Read what is on disk and write the combined ``results_random.csv`` and ``summary_random.csv``."""
    folder = Path(folder)
    parts = [pd.read_csv(folder / f"results_random_{t}.csv").drop_duplicates(["draw", "base"]).sort_values(["draw", "base"])
             for t in TEST_SEEDS if (folder / f"results_random_{t}.csv").exists()]
    out = {"fixed": pd.read_csv(folder / "results_fixed.csv") if (folder / "results_fixed.csv").exists() else None}
    if parts:
        rnd = pd.concat(parts, ignore_index=True)
        rnd.to_csv(folder / "results_random.csv", index=False)
        out["random"] = rnd
        out["summary"] = summary_random(rnd)
        out["summary"].to_csv(folder / "summary_random.csv", index=False)
    return out
