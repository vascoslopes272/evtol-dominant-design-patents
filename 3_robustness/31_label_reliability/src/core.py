"""Coding-error check for P1: the eight results of the paper as functions of one design table.

The design table is the aircraft table of eVTOL_dataset_v1 as the thesis code loads it (``Dataset.master``: one row per patent
and aircraft, every wizard field). :func:`evaluate` takes such a table (the original or a perturbed copy), rebuilds the
thesis ``Dataset`` and context from it, and recomputes every result: the gate, the analysis views, F membership, the levels,
both permutation bands, the Holm corrections. Nothing is carried over from the original except the inputs that are not
coded from the drawings (figures, patent identity, data dictionary, TRL).

The measures are NOT rewritten. Every number comes from the thesis code of eVTOL-Visual-Evaluation/labeling_evaluation, which
is imported, never edited:

  1  design space          frames.selected_fields; thesis_q6.fixed_by_architecture (80 %, architectures with 20+ designs)
  2  levels A, A.W.T, A.U  frames.archetype_levels_table (via thesis_q7._data)
  3  Table 4.9             analysis_iii.verdict_two_bases
  4  family F              frames.family_flags / family_mask (inside the above); F columns of the verdict and its detail
  5  architecture trends   analysis_iii.rho_table
  6  trajectories          lib.drivers.trace_trends + thesis_q6._with_holm, the lines of thesis_q6._data that build them
  7  entrants              frames.named_entries + frames.entry_split_test
  8  regions               frames.regional_frame -> region_lean, region_tests (via thesis_q7._data)

The 80 % rule (thesis Section 3.4.2) is the only cut used for result 1: a dimension varies when its leading option holds
under 80 % of the designs that answer it. The yaml constant ``field_drop_top_share`` (88 %) only chooses the rows the thesis
table prints; result 1 reads every dimension of ``frames.selected_fields``.

Usage:
    import core
    base = core.load()                       # once: config, original table, fixed inputs
    res = core.evaluate(base, base.master)   # dict result id -> value (flat)
"""
from __future__ import annotations

import os
import sys
import time
import warnings
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[3]                      # the root of this repository
ANALYSIS = REPO / "2_analysis"
THESIS_CODE = Path(os.environ.get("THESIS_CODE", ANALYSIS / "src"))   # the packages viz and lib of the analysis
YAML = ANALYSIS / "20_config.yaml"
OUT = REPO / "results" / "31_label_reliability"

SHARE_RULE = 0.80                 # thesis 3.4.2: a dimension varies when its leading option holds under 80 %
MIN_ARCH_DESIGNS = 20             # thesis: the per-architecture check reads architectures with 20 designs or more
COHORT = "2020-23"
LEVELS = {"A0": "A", "A1t": "A·W·T", "A0c": "A·U", "family_b": "F"}
BASES = ("all designs", "actively protected")
WINGED = ("SLC", "TR", "CVT", "TW", "TB", "PTC", "SRW", "DS")
TRAJ = [("propulsors on booms", "units carried on booms", "CVT"), ("ducted", "a ducted unit", "CVT"),
        ("propulsors", "propulsive units", "TR"), ("propulsors", "propulsive units", "CVT")]
CODE_OUT = {"TR": "TP", "TB": "TF"}          # the thesis code's names -> the dataset's


def _imports():
    warnings.filterwarnings("ignore")
    import matplotlib
    matplotlib.use("Agg")
    if str(THESIS_CODE) not in sys.path:
        sys.path.insert(0, str(THESIS_CODE))
    from viz import analysis_iii, config, data, frames, thesis, thesis_q1, thesis_q3, thesis_q6, thesis_q7   # noqa: F401
    from lib import drivers                                                                             # noqa: F401
    return SimpleNamespace(analysis_iii=analysis_iii, config=config, data=data, frames=frames, thesis=thesis, q1=thesis_q1,
                           q3=thesis_q3, q6=thesis_q6, q7=thesis_q7, drivers=drivers)


def load(yaml: Path = YAML) -> SimpleNamespace:
    """Config, the original design table and the inputs that are not perturbed."""
    m = _imports()
    cfg = m.config.load(yaml)
    m.thesis.context(cfg)                              # style.apply once, as the notebooks do
    ds = m.data.load_dataset(cfg)
    # the master BEFORE Dataset.__post_init__ touched it is what a replica perturbs: re-read it the way load_dataset does
    dd = m.data.read(cfg, "label_dictionary", required=False)
    master = m.data._apply_kinds(m.data.read(cfg, "aircraft_labels"), dd)
    return SimpleNamespace(m=m, cfg=cfg, yaml=str(yaml), master=master, figures=ds.figures, identity=ds.identity,
                           dd=ds.data_dictionary, trl=ds.trl)


def context(base, master: pd.DataFrame) -> SimpleNamespace:
    """The thesis context (viz.thesis.context) built from ``master``: a new Dataset, a new design frame, empty caches."""
    m, cfg = base.m, base.cfg
    for mod in (m.q1, m.q3, m.q7):                    # module caches keyed by id(ctx): an id can be reused
        mod._CACHE.clear()
    ds = m.data.Dataset(root=cfg.roots["labelled"], master=master.copy(), figures=base.figures, identity=base.identity,
                        data_dictionary=base.dd, trl=base.trl)
    v = m.frames.base(ds, cfg)
    win_names = list(cfg.analysis["windows"])
    ctx = SimpleNamespace(cfg=cfg, ds=ds, v=v, WIN=m.frames.windows_from_config(cfg), WIN_NAMES=win_names,
                          COMPLETE=[w for w in win_names if "partial" not in w], W=6.3, HALF=3.1,
                          WSHORT={"<= 2011": "≤2011", "2012-15": "12–15", "2016-19": "16–19", "2020-23": "20–23",
                                  "2024-26 (partial)": "24–26*"},
                          SEED=cfg.analysis["random_seed"], thin=lambda n: f"{int(n):,}".replace(",", " "),
                          pct=lambda x: f"{x:.0%}".replace("%", " %"), pval=lambda p: "< 0.001" if p < 0.001 else f"{p:.3f}", np=np)
    m.frames.set_window_bounds(cfg)
    return ctx


# ------------------------------------------------------------------------------------------------------------------ results
def r1_design_space(base, ctx) -> dict:
    """Top-option share of every dimension of frames.selected_fields; varies = share < 80 %; per architecture, the 80 % rule on the
    designs of the architectures with 20 or more: the winged architectures where the wing configuration is fixed."""
    m = base.m
    t6 = m.frames.selected_fields(ctx.ds)
    out = {}
    for _, r in t6.iterrows():
        out[f"1 | top share | {r['name']}"] = float(r["top_share"])
        out[f"1 | varies (under 80 %) | {r['name']}"] = bool(r["top_share"] < SHARE_RULE)
    out["1 | dimensions that vary (count)"] = int((t6["top_share"] < SHARE_RULE).sum())
    out["1 | dimensions read (count)"] = int(len(t6))
    # the thesis count ("seven of the nine dimensions") leaves the landing gear out: 68 % of its answers are Unknown (thesis II.1)
    keep = ~t6["name"].astype(str).str.contains("landing-gear", case=False)
    out["1 | dimensions that vary, landing gear left out (count)"] = int((t6.loc[keep, "top_share"] < SHARE_RULE).sum())
    out["1 | dimensions read, landing gear left out (count)"] = int(keep.sum())
    # fixed_by_architecture reads only t6 and the cut from thesis_q6._data: give it those two, so the discovery curve and the rest
    # of _data are not computed (the function itself is unchanged); the cut there only chooses the printed dimensions
    ctx._q6 = {"t6": t6, "cut": base.cfg.analysis["field_drop_top_share"]}
    summary, detail = m.q6.fixed_by_architecture(ctx, share=SHARE_RULE, min_designs=MIN_ARCH_DESIGNS)
    ctx._q6 = None
    wc = detail[detail["dimension"].astype(str).str.contains("wing configuration", case=False)]
    read = wc[wc["code"].isin(WINGED) & wc["read"].astype(bool)]
    out["1 | wing configuration fixed at 80 % (winged architectures)"] = int((read["share"] >= SHARE_RULE).sum())
    out["1 | wing configuration, winged architectures read"] = int(len(read))
    return out


def r3_r4_r8(base, ctx) -> dict:
    """Table 4.9 on both bases (result 3), the F cells and numbers (4), the levels (2) and the regions (8): one call of
    analysis_iii.verdict_two_bases, whose thesis_q7._data also holds the levels table and the regional frames."""
    m = base.m
    verdict, det = m.analysis_iii.verdict_two_bases(ctx)
    d = m.q7._data(ctx)
    out = {}
    # 2. levels
    lv = d["levels"].set_index("level")
    b7 = d["brief7"].set_index("level id")
    for lid in ("A0", "A1t", "A0c"):
        out[f"2 | configurations | {LEVELS[lid]}"] = int(b7.loc[lid, "archetypes"])
        out[f"2 | effective number 1D | {LEVELS[lid]}"] = float(b7.loc[lid, "effective number ¹D"])
        out[f"2 | effective number 2D | {LEVELS[lid]}"] = float(lv.loc[lid, "effective number ²D"])
        out[f"2 | largest share | {LEVELS[lid]}"] = float(b7.loc[lid, "its share"])
    # 3 and 4. the cells of Table 4.9, true/false (1: met in some pair of years; 2, 3: met in 2020-23; all three: met somewhere)
    for _, r in verdict.iterrows():
        cond = r["condition"].split(",")[0].split(":")[0].strip()
        cond = {"1": "1 share", "2": "2 balance", "3": "3 disparity"}.get(cond, "all three")
        for lvl in LEVELS.values():
            cell = str(r[lvl])
            met = cell.startswith("✓") and (COHORT in cell if cond in ("2 balance", "3 disparity") else True)
            k = "4" if lvl == "F" else "3"
            out[f"{k} | {r['base']} | {cond} | {lvl}"] = bool(met)
    for _, r in det.iterrows():
        lvl, bs = r["level"], r["base"]
        k = "4" if lvl == "F" else "3"
        if lvl == "F":
            for y in (2020, 2021):
                s = str(r[f"condition 1: share {y} (n of N)"])
                out[f"4 | {bs} | F share {y}"] = float(s.split(" %")[0]) / 100 if "%" in s else np.nan
                out[f"4 | {bs} | F above 50 % in {y}"] = bool(out[f"4 | {bs} | F share {y}"] > 0.5)
        out[f"{k} | {bs} | largest share | {lvl}"] = float(str(r["condition 1: largest share"]).split(" %")[0]) / 100
        out[f"{k} | {bs} | 2D 2020-23 | {lvl}"] = float(r["²D 2020-23"])
        out[f"{k} | {bs} | 2D band low 2020-23 | {lvl}"] = float(r["²D lower band edge 2020-23"])
        out[f"{k} | {bs} | dQ 2020-23 | {lvl}"] = float(r["ΔQ 2020-23"])
        out[f"{k} | {bs} | dQ band low 2020-23 | {lvl}"] = float(r["ΔQ lower band edge 2020-23"])
    # 8. regions: F share per region in 2020-23, and the chi-square of region x F in 2020-23 (all assignees; without the largest)
    ln = d["ln"].set_index("region")
    for reg in ln.index:
        out[f"8 | F share 2020-23 | {reg}"] = float(ln.loc[reg, f"F share {COHORT}"])
    ts = d["ts"]
    left = ts.attrs.get("left_out", "largest")
    for who in ts["filers"].unique():
        row = ts[ts["measure"].eq("family F") & ts["period"].eq(COHORT) & ts["filers"].eq(who)].iloc[0]
        tag = "all assignees" if who == "all filers" else "without the largest assignee"
        out[f"8 | region x F 2020-23, p | {tag}"] = float(row["p (chi-square, region)"])
        out[f"8 | region x F 2020-23, p (Holm) | {tag}"] = float(row["p (Holm)"])
        out[f"8 | regions differ 2020-23 (p < 0.05) | {tag}"] = bool(row["p (chi-square, region)"] < 0.05)
    out["8 | largest assignee left out"] = str(left)
    return out


def r5_trends(base, ctx) -> dict:
    """Spearman trend of each architecture's yearly share (20 designs or more), raw and Holm-corrected (analysis_iii.rho_table)."""
    t = base.m.analysis_iii.rho_table(ctx)
    out = {}
    for _, r in t.iterrows():
        c = CODE_OUT.get(r["code"], r["code"])
        out[f"5 | rho | {c}"] = float(r["rho"])
        out[f"5 | p (Holm) | {c}"] = float(r["p (Holm)"])
        out[f"5 | rises (rho > 0, Holm p < 0.05) | {c}"] = bool(r["rho"] > 0 and r["p (Holm)"] < 0.05)
        out[f"5 | falls (rho < 0, Holm p < 0.05) | {c}"] = bool(r["rho"] < 0 and r["p (Holm)"] < 0.05)
        out[f"5 | rho 2016-23 | {c}"] = float(r["rho, 2016-23"])
        out[f"5 | p 2016-23 (Holm) | {c}"] = float(r["p, 2016-23 (Holm)"])
    out["5 | architectures tested"] = ",".join(CODE_OUT.get(c, c) for c in t["code"])
    return out


def r6_trajectories(base, ctx) -> dict:
    """Trace trends inside each architecture with Holm per trace: the lines of thesis_q6._data that build d['trends'] and
    d['links'], called unchanged, then thesis_q6._with_holm."""
    m = base.m
    ds, v = ctx.ds, ctx.v
    cn = {c: m.q6.style.cls(c).name for c in m.q6.style.CLASS_ORDER}
    cf = m.frames.config_frame(ds, v)
    tf = m.frames.trace_frame(ds, v)
    classes = m.drivers.class_selection(v)
    drift = m.drivers.trace_drift(tf, classes, class_names=cn)
    trends = m.drivers.trace_trends(tf, drift, classes, class_names=cn)
    links = m.drivers.driver_links(cf)
    trends, links = m.q6._with_holm(trends, links)
    out = {}
    for name, trace, code in TRAJ:
        r = trends[trends["trace"].eq(trace) & trends["code"].eq(code)]
        c = CODE_OUT.get(code, code)
        if len(r):
            r = r.iloc[0]
            out[f"6 | rho | {name} in {c}"] = float(r["rho"])
            out[f"6 | p (Holm) | {name} in {c}"] = float(r["p_holm"])
            out[f"6 | significant (Holm p < 0.05) | {name} in {c}"] = bool(r["p_holm"] < 0.05)
            out[f"6 | sign | {name} in {c}"] = int(np.sign(r["rho"]))
    return out


def r7_entrants(base, ctx) -> dict:
    """Chi-square of the architecture mix, entrants against incumbents, per tested cohort, with and without the largest
    returning assignee (frames.entry_split_test)."""
    m = base.m
    ent = m.frames.named_entries(ctx.v, ctx.WIN_NAMES)
    et = m.frames.entry_split_test(ent, ctx.COMPLETE)
    out = {}
    for _, r in et[et["p"].notna()].iterrows():
        w = r["window"]
        out[f"7 | p | {w}"] = float(r["p"])
        out[f"7 | p without the largest assignee | {w}"] = float(r["p without it"])
        out[f"7 | differ (p < 0.05) | {w}"] = bool(r["p"] < 0.05)
        out[f"7 | differ without the largest (p < 0.05) | {w}"] = bool(r["p without it"] < 0.05)
        out[f"7 | largest returning assignee | {w}"] = str(r["largest returning firm"])
    return out


RESULTS = [r1_design_space, r3_r4_r8, r5_trends, r6_trajectories, r7_entrants]


def evaluate(base, master: pd.DataFrame, timings: dict | None = None) -> dict:
    """Every result on ``master``: one flat dict, key 'result | ... ' -> value."""
    ctx = context(base, master)
    out = {"designs analysed": int(ctx.v["topType"].notna().sum())}
    for f in RESULTS:
        t0 = time.time()
        out.update(f(base, ctx))
        if timings is not None:
            timings[f.__name__] = round(time.time() - t0, 1)
    return out


def as_frame(res: dict) -> pd.DataFrame:
    rows = []
    for k, v in res.items():
        p = [x.strip() for x in k.split("|")]
        rows.append({"result": p[0] if p[0][:1].isdigit() else "0", "key": k, "value": v})
    return pd.DataFrame(rows)
