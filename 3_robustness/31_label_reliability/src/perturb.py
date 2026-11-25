"""Coding-error replicas of the design table (Stage 2 of the coding-error check for P1).

    import core, perturb
    base = core.load()
    P = perturb.Perturber(base)
    replica, log = P.replica(seed=20261118, index=0)      # a perturbed copy of base.master
    core.evaluate(base, replica)

ERROR MODEL (rules marked PROVISIONAL wait for the author's ruling; each is one switch below)
- The designs perturbed are the analysis designs (the primary representative aircraft, ``Dataset.variants``). Other rows of the
  table are not read by the results and stay as they are.
- Every value coded from the drawings, architecture and morphology (wizard stages G1, M1, M2, M3), has a probability R of being
  replaced, independently of every other value.
    * an option field (``kind = id`` in the data dictionary) takes another option of its dimension, uniformly; the options are
      those of the data dictionary, legacy options left out;
    * a tick (``kind = bool``) takes the other answer;
    * PROVISIONAL (COUNTS): a count (wing count, boom-group count, propulsors per station or type) that is positive takes
      another positive count observed for that dimension in the analysis designs, uniformly. A count of 0 means the part is
      absent and is treated as blank. When the wing count falls, the wings above it and their propulsor cards are blanked;
      when it rises, the new wing has blank codes.
- A value is perturbed only where the wizard asks for it: a blank stays blank; a value an override hides, a boom group that
  does not exist, a wing above the wing count, a propulsor type above the station's type count are not answers and are left
  alone (PROVISIONAL: APPLICABLE_ONLY).
- Not perturbed: priority year, legal status, region, assignee (none is a wizard code), the T1/T2 fields (approval,
  duplicate, figure), the gate tags, the overrides and uncertainty flags, the number of propulsor types per station
  (structure of the record), free-text notes.
- Locks: a design whose perturbed codes break a lock of thesis Table A.5 that its original codes do not break (as the dataset
  applies them: articulation Other suspends L4, L5 and L8, DECISIONS 16; L8 exempts control-only propulsors; the boom tick
  'on the fixed part of the wing' is read, DECISIONS 17) is redrawn, up to MAX_REDRAWS times; then it keeps its original codes
  and is counted.
- The four propulsion columns notebook 04 derives from the codes (propulsor count, boom thrust state, wing thrust carrier,
  wing-borne count, with their notes) are recomputed from the perturbed codes with notebook 04's own rules
  (_build/nb04_v16/11I_master_labels.ipynb, cell 25, copied in :func:`derive`). The thesis code reads these columns.

RANDOM NUMBERS: replica i uses numpy default_rng([seed, i]); a replica does not depend on the others nor on the workers.
"""
from __future__ import annotations

import re
from collections import Counter

import numpy as np
import pandas as pd

R = 0.15
MAX_REDRAWS = 20
COUNTS = True             # PROVISIONAL: perturb positive counts (False = counts are never perturbed)
APPLICABLE_ONLY = True    # PROVISIONAL: perturb only values the wizard asks for (see the module text)
CODE_IN = {"TP": "TR", "TF": "TB"}         # dataset code -> the thesis code's (the master is read through the compat mirror)

STATIONS = ["fuselage", "wing1", "wing2", "wing3", "emp", "boom", "core_layout", "hull_array"]
TYPE_CAT = ["bmech", "chord", "orient", "propKin", "rmech"]          # per propulsor set
TYPE_ZONE = ["zone", "zoneChord", "zoneSpan"]                          # mount zone: on the card, or per type when types differ
M1_CAT = ["fusShape", "fusKin", "gearArch"]
M1_BOOL = ["latSym"]
BOOM_CAT = ["attach", "long", "orient", "span", "wingIdx", "wingRel"]
BOOM_BOOL = ["circSym", "hasProps", "retracts", "sym", "tilts", "onFixedPart"]
M2_CAT = ["wingConf", "empType"]
M2_BOOL = ["empTilts"]
WING_CAT = ["plan", "posL", "posV", "role", "tilt"]
WING_BOOL = ["tipJoin"]


# ------------------------------------------------------------------------------------------------------------- small readers
def _s(v):
    if v is None or v is pd.NA or (isinstance(v, float) and np.isnan(v)):
        return ""
    s = str(v).strip()
    return "" if s in ("nan", "None", "NaT", "<NA>") else s


def _t(v):
    return _s(v) == "True"


def _n(v):
    s = _s(v)
    if s in ("", "False"):
        return 0
    if s == "True":
        return 1
    try:
        return int(float(s))
    except ValueError:
        return 0


def _blank(v):
    return _s(v) == ""


# ------------------------------------------------------------------------------------------- notebook 04, cell 25 (copied)
NO_UNITS_TYPES = {"HB", "PFV"}
WING_CARDS = ["wing1", "wing2", "wing3"]
WING_ATTACH = ("Wings", "Both")
DERIVED = ["propulsor_units", "propulsor_units_note", "boom_thrust_state", "wing_thrust_carrier", "wing_borne_units",
           "wing_borne_units_note", "wing_boom_candidate"]


def _station_units(r, st):
    if _t(r.get(f"{st}_quickOverride")):
        q = _s(r.get(f"{st}_quickCount"))
        if not q:
            return None, [], f"M3:{st} override without a quick count"
        n = _n(q)
        return n, ([dict(count=n, propKin="", zoneChord="")] if n > 0 else []), ""
    nt = _n(r.get(f"{st}_ntypes")) or 1
    tys = []
    for pre in ([f"{st}_t{k}_" for k in range(1, nt + 1)] if nt > 1 else [f"{st}_"]):
        c = _n(r.get(pre + "count"))
        if c > 0 and not _t(r.get(pre + "ctrlOnly")):
            tys.append(dict(count=c, propKin=_s(r.get(pre + "propKin")), zoneChord=_s(r.get(pre + "zoneChord"))))
    return sum(t["count"] for t in tys), tys, ""


def _boom_groups(r):
    out = []
    for k in range(1, 7):
        att, cnt = _s(r.get(f"boom{k}_attach")), _n(r.get(f"boom{k}_count"))
        if (not att and cnt == 0) or _s(r.get(f"boom{k}_hasProps")) == "False":
            continue
        out.append(dict(k=k, attach=att, wingIdx=_s(r.get(f"boom{k}_wingIdx")), wingRel=_s(r.get(f"boom{k}_wingRel")),
                        orient=_s(r.get(f"boom{k}_orient")), tilts=_t(r.get(f"boom{k}_tilts")), on_fixed=_t(r.get(f"boom{k}_onFixedPart"))))
    return out


def _rides_tilting_wing(g, tw):
    if g["attach"] not in WING_ATTACH or not tw or g["on_fixed"]:
        return False
    if g["wingIdx"] in ("", "Multi"):
        return True
    m = re.fullmatch(r"W(\d)", g["wingIdx"])
    return bool(m) and int(m.group(1)) in tw


def derive(r: dict) -> dict:
    """The derived propulsion columns of one primary approved aircraft, as notebook 04 computes them (its loop body, rules 1-3;
    the override list is read, not rebuilt: overrides are not perturbed)."""
    out = {c: None for c in DERIVED}
    tt = _s(r.get("topType"))
    ov = [o for o in _s(r.get("overrides")).split("|") if o]
    su = {st: _station_units(r, st) for st in STATIONS}
    why = ([f"{tt}: the codebook excludes hoverbikes and PFVs from propulsor counts"] if tt in NO_UNITS_TYPES else []) \
        + (["G1 override: the aircraft has no type"] if "G1" in ov else []) + [su[st][2] for st in STATIONS if su[st][0] is None]
    if why:
        out["propulsor_units_note"] = "; ".join(why)
    else:
        out["propulsor_units"] = int(sum(su[st][0] for st in STATIONS))
    gs = _boom_groups(r)
    tw = {k for k in range(1, 5) if _s(r.get(f"wing{k}_tilt")) == "Tilt"}
    bu, btys, _ = su["boom"]
    m1_ovr, boom_ovr = "M1" in ov, "M3:boom" in ov
    if m1_ovr or boom_ovr:
        state = None
    elif not btys:
        state = "none"
    else:
        cats = set()
        for t in btys:
            for g in (gs or [None]):
                if g is not None and _rides_tilting_wing(g, tw):
                    cats.add("on_tilting_wing")
                elif (g is not None and g["tilts"]) or t["propKin"] == "Tilt":
                    cats.add("tilting")
                else:
                    cats.add("fixed")
        state = cats.pop() if len(cats) == 1 else "mixed"
    out["boom_thrust_state"] = state
    if "M2" in ov:
        wwhy = ["M2 override: the wings are not determinable"]
    elif _n(r.get("wCount")) <= 0:
        wwhy = ["wingless"]
    else:
        wwhy = (["M1 override: the boom groups are not determinable"] if m1_ovr else []) + [su[st][2] for st in WING_CARDS + ["boom"] if su[st][0] is None]
    if wwhy:
        out["wing_borne_units_note"] = "; ".join(wwhy)
        return out
    wty = [t for st in WING_CARDS for t in su[st][1]]
    wgs = [g for g in gs if g["attach"] in WING_ATTACH]
    ogs = [g for g in gs if g["attach"] not in WING_ATTACH]
    on_wing_boom = bool(btys) and bool(wgs)
    out["wing_thrust_carrier"] = "both" if (wty and on_wing_boom) else "wing_boom" if on_wing_boom else "wing" if wty else "none"
    rel = {g["wingRel"] for g in wgs}
    out["wing_boom_candidate"] = bool((on_wing_boom and (rel in ({"Fore"}, {"Aft"}) or any(g["orient"] == "Vert" and g["wingRel"] == "Straddle" for g in wgs)))
                                      or any(t["zoneChord"] in ("Above", "Below") for t in wty))
    uwhy = ([f"{tt}: the codebook excludes hoverbikes and PFVs from propulsor counts"] if tt in NO_UNITS_TYPES else []) \
        + (["G1 override: the aircraft has no type"] if "G1" in ov else [])
    if bu > 0 and not gs:
        uwhy.append("the boom card's rotors have no propeller-carrying boom group")
    elif bu > 0 and wgs and ogs:
        uwhy.append("the boom card's rotors cannot be apportioned: boom groups mix wing (Wings/Both) and other attachment")
    if uwhy:
        out["wing_borne_units_note"] = "; ".join(uwhy)
    else:
        out["wing_borne_units"] = int(sum(su[st][0] for st in WING_CARDS) + (bu if wgs else 0))
    return out


# --------------------------------------------------------------------------------- locks of thesis Table A.5 (from 05a)
def locks(r: dict) -> set:
    """The locks one aircraft breaks, as the dataset applies them (05a_audit_lock_tests.py on one record, with the rulings of
    DECISIONS 16 and 17: articulation Other suspends L4, L5, L8; L8 exempts control-only propulsors; the fixed-part boom tick)."""
    arch = {"TR": "TP", "TB": "TF"}.get(_s(r.get("topType")), _s(r.get("topType")))
    if not arch:
        return set()
    g = lambda c: (None if _blank(r.get(c)) else r.get(c))                     # noqa: E731
    sets = []
    for k in ["fuselage", "wing1", "wing2", "wing3", "emp", "boom", "hull_array", "core_layout"]:
        if _t(g(k + "_quickOverride")):
            sets.append(dict(card=k, override=True))
            continue
        nt = _n(g(k + "_ntypes")) or 1
        if nt <= 1:
            if _n(g(k + "_count")) > 0:
                sets.append(dict(card=k, t=0, pk=_s(g(k + "_propKin")) or None, orient=_s(g(k + "_orient")) or None,
                                 ctrl=_t(g(k + "_ctrlOnly")), override=False))
        else:
            for t in range(1, nt + 1):
                p = f"{k}_t{t}_"
                if _n(g(p + "count")) > 0:
                    sets.append(dict(card=k, t=t, pk=_s(g(p + "propKin")) or None, orient=_s(g(p + "orient")) or None,
                                     ctrl=_t(g(p + "ctrlOnly")), override=False))
    B = []
    if _t(g("boomsPresent")):
        for i in range(1, 7):
            if g(f"boom{i}_count") is None and g(f"boom{i}_attach") is None:
                continue
            B.append(dict(attach=_s(g(f"boom{i}_attach")), wingIdx=g(f"boom{i}_wingIdx"), tilts=_t(g(f"boom{i}_tilts")),
                          hasProps=(None if g(f"boom{i}_hasProps") is None else _t(g(f"boom{i}_hasProps"))), onFixed=_t(g(f"boom{i}_onFixedPart"))))
    act = [s for s in sets if not s["override"]]
    Bp = [b for b in B if b["hasProps"] is not False]
    wc = _n(g("wCount"))
    tw = {i for i in range(1, wc + 1) if _s(g(f"wing{i}_tilt")) == "Tilt"}
    m1o, m2o = _t(g("m1_quickOverride")), _t(g("m2_quickOverride"))
    fk, empT = _s(g("fusKin")), _t(g("empTilts"))

    def on_tw(b):
        if b["attach"] not in ("Wings", "Both") or not tw or b["onFixed"]:
            return False
        w = _s(b["wingIdx"])
        return w in ("", "Multi") or (w.replace("W", "").isdigit() and int(w.replace("W", "")) in tw)
    bt = [s for s in act if s["card"] == "boom"]
    mapped = len(bt) == len(Bp) and all(s["t"] > 0 for s in bt)

    def support(s):
        m = re.fullmatch(r"wing(\d)", s["card"])
        if m and int(m.group(1)) in tw:
            return "tilting wing"
        if s["card"] == "emp" and empT:
            return "tilting empennage"
        if s["card"] == "boom":
            G = [Bp[s["t"] - 1]] if mapped else Bp
            if G and all(on_tw(b) for b in G):
                return "boom on tilting wing"
            if G and all(b["tilts"] for b in G):
                return "tilting boom"
            if any(on_tw(b) or b["tilts"] for b in G):
                return "boom, part tilts"
        return "fixed support"
    out = set()
    nonF = [s for s in act if s["pk"] not in (None, "Fixed")]
    if arch == "SLC" and any(s["pk"] == "Tilt" for s in nonF):
        out.add("L1")
    if arch in ("TW", "SLC", "SRW", "TF", "PTC", "RC") and nonF:
        out.add("L2")
    if arch == "DS" and nonF:
        out.add("L7")
    if arch in ("MR", "RC") and not m2o:
        if any(_s(g(c)) not in ("", "0", "False") for c in ["wingConf", "wing1_tilt", "wing1_plan", "wing1_posV"]) or wc > 0 \
                or any(s["card"].startswith("wing") for s in act):
            out.add("L3")
    thrust = [s for s in act if not s["ctrl"]]
    other = any(s["pk"] == "Other" for s in thrust)
    anyov = any(s["override"] for s in sets)
    kinds = set()
    for s in thrust:
        sp = support(s)
        if sp in ("tilting wing", "tilting empennage", "boom on tilting wing"):
            kinds.add("tilting wing")
        elif sp == "tilting boom" or s["pk"] == "Tilt":
            kinds.add("tilting rotor")
        elif sp == "boom, part tilts":
            kinds |= {"tilting rotor", "fixed rotor"}
        elif s["pk"] == "Fixed":
            kinds.add("fixed rotor")
    if arch == "CVT" and not anyov and not other and len(kinds) < 2:
        out.add("L4")
    if arch == "TW" and not m2o and not other:
        bad = not tw or any(i not in tw and any(s["card"] == f"wing{i}" for s in thrust) for i in range(1, wc + 1)) \
            or any(support(s) not in ("tilting wing", "tilting empennage", "boom on tilting wing") and not s["card"].startswith("wing") for s in thrust)
        if bad:
            out.add("L5")
    if arch == "TF" and not m1o and fk not in ("TiltBody", "Variable Incidence", "LevelCabin"):
        out.add("L6")
    if arch == "TP" and not anyov and not other:
        if (tw and not m2o) or not thrust or any(not (s["pk"] == "Tilt" or support(s) == "tilting boom") for s in thrust):
            out.add("L8")
    if arch in ("RC", "PTC") and not m1o and fk != "BodyPitch":
        out.add("L10")
    if any(s["pk"] == "Tilt" and support(s) in ("tilting wing", "tilting empennage", "boom on tilting wing", "tilting boom") for s in act):
        out.add("L12")
    if arch in ("SLC", "SRW") and any(s["orient"] == "Mixed" for s in act):
        out.add("L14")
    return out


# ----------------------------------------------------------------------------------------------------------- the perturber
def _options(dd: pd.DataFrame) -> dict:
    """column -> valid option ids (data dictionary, legacy options left out; architecture codes in the thesis code's form)."""
    out = {}
    for _, r in dd[dd["kind"].eq("id") & dd["options"].notna()].iterrows():
        ids = []
        for part in str(r["options"]).split(" | "):
            k, _, lab = part.partition("=")
            if "legacy" in lab.lower():
                continue
            ids.append(CODE_IN.get(k.strip(), k.strip()))
        out[r["column"]] = ids
    return out


class Perturber:
    def __init__(self, base, r: float = R):
        self.r = r
        self.master = base.master
        dd = pd.read_csv(base.cfg.inputs["label_dictionary"]) if hasattr(base.cfg, "inputs") else base.dd
        self.opts = _options(dd if "options" in dd.columns else base.dd)
        ctx = base.m.data.Dataset(root=base.cfg.roots["labelled"], master=base.master.copy(), figures=base.figures,
                                  identity=base.identity, data_dictionary=base.dd, trl=base.trl)
        self.rows = list(ctx.variants.index)                    # the analysis designs (master index)
        self.orig = {i: base.master.loc[i].to_dict() for i in self.rows}
        self.orig_locks = {i: locks(self.orig[i]) for i in self.rows}
        # observed positive counts per count dimension (pooled over the copies of one dimension: wing1..3, type 1..7)
        # (PROVISIONAL) drawn with the frequency each count has in the analysis designs, so a 4 becomes a 6 more often than a 136
        pool = {}
        for i in self.rows:
            r = self.orig[i]
            for c, kind in self.slots(r):
                if kind == "count":
                    pool.setdefault(self._count_dim(c), Counter())[_n(r[c])] += 1
        self.count_pool = {d: dict(sorted(v.items())) for d, v in pool.items()}

    @staticmethod
    def _count_dim(c: str):
        if c == "wCount":
            return "wCount"
        if re.fullmatch(r"boom\d_count", c):
            return "boom group count"
        m = re.fullmatch(r"(fuselage|wing\d|emp|boom|core_layout|hull_array)(_t\d)?_count", c)
        if m:
            return re.sub(r"\d", "N", m.group(1)) + (" type" if m.group(2) else "") + " count"
        return None

    # the values the wizard asks for on one record: (column, kind) with kind 'cat', 'bool' or 'count'
    def slots(self, r: dict) -> list:
        out = []
        ov = set(o for o in _s(r.get("overrides")).split("|") if o)
        add = lambda c, k: out.append((c, k)) if not _blank(r.get(c)) else None      # noqa: E731
        if "G1" not in ov:
            add("topType", "cat")
        if "M1" not in ov:
            for c in M1_CAT:
                add(c, "cat")
            for c in M1_BOOL:
                add(c, "bool")
            if _t(r.get("boomsPresent")):
                for k in range(1, 7):
                    if _n(r.get(f"boom{k}_count")) <= 0 and _blank(r.get(f"boom{k}_attach")):
                        continue
                    for f in BOOM_CAT:
                        add(f"boom{k}_{f}", "cat")
                    for f in BOOM_BOOL:
                        add(f"boom{k}_{f}", "bool")
                    if _n(r.get(f"boom{k}_count")) > 0:
                        add(f"boom{k}_count", "count")
        wc = _n(r.get("wCount"))
        if "M2" not in ov:
            for c in M2_CAT:
                add(c, "cat")
            for c in M2_BOOL:
                add(c, "bool")
            if wc > 0:
                add("wCount", "count")
            for k in range(1, min(wc, 3) + 1):
                for f in WING_CAT:
                    if not (k == 1 and f == "role"):                 # wing 1 has no role (thesis Table A.3: wing 2 and beyond)
                        add(f"wing{k}_{f}", "cat")
                for f in WING_BOOL:
                    add(f"wing{k}_{f}", "bool")
        for st in STATIONS:
            if f"M3:{st}" in ov or _n(r.get(f"{st}_count")) <= 0:
                continue
            if st.startswith("wing") and int(st[-1]) > wc:
                continue
            nt = _n(r.get(f"{st}_ntypes")) or 1
            for f in TYPE_ZONE:
                add(f"{st}_{f}", "cat")
            add(f"{st}_sym", "bool")
            pres = [f"{st}_"] if nt <= 1 else [f"{st}_t{k}_" for k in range(1, nt + 1) if _n(r.get(f"{st}_t{k}_count")) > 0]
            for p in pres:
                for f in TYPE_CAT + ([] if nt <= 1 else TYPE_ZONE):
                    add(p + f, "cat")
                add(p + "ctrlOnly", "bool")
                add(p + "count", "count")
        return [(c, k) for c, k in out if k != "count" or COUNTS]

    def _new_value(self, rng, c, kind, v):
        if kind == "bool":
            return not _t(v)
        if kind == "count":
            pool = {x: w for x, w in self.count_pool.get(self._count_dim(c), {}).items() if x != _n(v)}
            if not pool:
                return v
            xs, ws = list(pool), np.array(list(pool.values()), dtype=float)
            return int(rng.choice(xs, p=ws / ws.sum()))
        opts = [o for o in self.opts.get(re.sub(r"^(boom)\d_", r"boom1_", re.sub(r"^wing\d_", "wing1_", re.sub(r"_t\d_", "_t1_", c))),
                                         self.opts.get(c, [])) if o != _s(v)]
        if not opts:
            opts = [o for o in self.opts.get(c, []) if o != _s(v)]
        return rng.choice(opts) if opts else v

    def _apply_structure(self, r: dict, c: str):
        """After a count changed: keep the record consistent (station total = sum of its types; wings above the wing count blank)."""
        m = re.fullmatch(r"(\w+?)_t\d_count", c)
        if m:
            st = m.group(1)
            nt = _n(r.get(f"{st}_ntypes")) or 1
            r[f"{st}_count"] = sum(_n(r.get(f"{st}_t{k}_count")) for k in range(1, nt + 1))
        if c == "wCount":
            wc = _n(r["wCount"])
            for k in range(1, 4):
                if k > wc:
                    for f in WING_CAT + WING_BOOL + ["plan_otherNote", "role_otherNote"]:
                        r[f"wing{k}_{f}"] = None
                    for key in [x for x in r if x.startswith(f"wing{k}_") and x not in (f"wing{k}_ntypes",)]:
                        if key.split("_", 1)[1] in TYPE_CAT + TYPE_ZONE + ["ctrlOnly", "sym", "quickOverride", "quickCount"] or \
                                re.fullmatch(rf"wing{k}_t\d_\w+", key):
                            r[key] = None
                    r[f"wing{k}_count"] = 0

    def design(self, rng, i):
        """One perturbed design: (record, values changed, redraws used, kept original)."""
        o = self.orig[i]
        for attempt in range(MAX_REDRAWS + 1):
            r = dict(o)
            changed = 0
            for c, kind in self.slots(o):
                if rng.random() < self.r:
                    nv = self._new_value(rng, c, kind, r.get(c))
                    if _s(nv) != _s(r.get(c)):
                        r[c] = nv
                        changed += 1
                        if kind == "count":
                            self._apply_structure(r, c)
            if locks(r) <= self.orig_locks[i]:
                return r, changed, attempt, False
        return dict(o), 0, MAX_REDRAWS, True

    def replica(self, seed: int, index: int, write_all: bool = False):
        """The perturbed design table of replica ``index`` and its log. ``write_all`` (a test) rewrites every analysis design
        through the same path, changed or not."""
        rng = np.random.default_rng([seed, index])
        m = self.master.copy()
        n_changed = redraws = kept = 0
        redrawn = Counter()
        recs = {}
        for i in self.rows:
            r, ch, att, keep = self.design(rng, i)
            n_changed += ch
            redraws += att
            kept += int(keep)
            if att:
                redrawn["designs redrawn at least once"] += 1
            if ch or write_all:
                d = derive(r)
                r.update(d)
                recs[i] = r
        if recs:
            upd = pd.DataFrame.from_dict(recs, orient="index")
            cols = [c for c in upd.columns if c in m.columns
                    and any(_s(recs[i].get(c)) != _s(self.orig[i].get(c)) for i in recs)]      # only the columns that changed
            for c in cols:                                   # write, then give each column back the dtype the loader gave it
                dt = str(self.master[c].dtype)
                col = m[c].astype(object)
                col.loc[upd.index] = upd[c].to_numpy(dtype=object)
                if dt == "Int64":
                    col = pd.to_numeric(col.map(lambda x: None if _blank(x) else x), errors="coerce").astype("Int64")
                elif dt == "boolean":
                    col = col.map(lambda x: pd.NA if _blank(x) else _t(x) if not isinstance(x, (bool, np.bool_)) else bool(x)).astype("boolean")
                elif dt == "bool":
                    col = col.astype(bool)
                m[c] = col
        log = {"replica": index, "codes changed": n_changed, "designs changed": len(recs), "redraws": redraws,
               "designs redrawn": redrawn["designs redrawn at least once"], "designs kept after 20 redraws": kept}
        return m, log
