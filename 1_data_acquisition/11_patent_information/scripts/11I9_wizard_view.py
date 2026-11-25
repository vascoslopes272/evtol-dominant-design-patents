"""wizard_view.py — what the labelling wizard SHOWS for a record, replayed from the record alone.

The wizard (notebooks/UI_for_taxonomy_caracterization_15_4.html) locks some fields once the
architecture is known: it draws the locked value as a disabled chip whatever is stored. A stored
value that differs from the lock is therefore invisible on screen but lands in the export — the
screen says one thing, the Excel another. This module replays every lock on the long-form record
and lists each place where the two differ, so notebook 04 can check them and
scripts/apply_wizard_locks.py can write the locked value into the record.

Every rule below mirrors a named function in the wizard; keep them in sync:

  acState (per approved figure)  pageT2 "Aircraft State in this View" + isConvertibleArch() +
                                 archConfigChanges(): a fixed architecture whose record moves
                                 nothing is locked to Invariant (stored id 'HoverCruise')
  <card>_propKin, <card>_tN_propKin  propKinLock(): TW/DS/SLC/SRW/MR/TB/PTC/RC -> Fixed — on the card AND
                                 on every propeller type (m3TypeAttrs draws the lock per type; the
                                 wizard exports it per type since v15.11)
  fusKin                         applyFusKinLock() / pageM1: PTC, RC -> BodyPitch; TB -> never Fixed
  wingN_tilt                     g1-subbtn handler + pageM2: TB, PTC -> Fixed; TW -> wing1 Tilt
  wCount / wingConf / wingN_*    RC, MR are wingless: count 0, no wing architecture, no wing rows
                                 (G1 lock + v15.11 export)
  <card>_orient (M3)             SLC, SRW: 'Mixed' is not offered (m3OrientationOptions) — shown blank
  <card>_zone/zoneChord/zoneSpan m3Card: card-level mounting positions are drawn only on a single-type card with
                                 propulsors (count > 0); on a count-0 card or a multi-type card (positions live per
                                 type) they are hidden — v15.12 export writes them only when drawn
  hasLegends / isMain (figure)   pageT2: an unticked pill reads "No" — v15.12 export writes False, not blank

One deliberate difference: the wizard evaluates archConfigChanges() on the architecture that is
active while T2 is drawn (always arch 1), so on a multi-aircraft patent the figures of arch 2+
are judged by arch 1's morphology. Here each figure is judged by its OWN architecture, which is
what the lock means.

    from src.wizard_view import replay, INVARIANT_ID
    diffs = replay(long_df)            # columns: see DIFF_COLS
"""
from __future__ import annotations

import re

import pandas as pd

SEP = " — "
INVARIANT_ID = "HoverCruise"          # the wizard's id for the option it displays as "Invariant"
INVARIANT_NAME = "Invariant"
CONVERTIBLE = {"TW", "TP", "DS", "CVT", "SRW"}   # v16.0 codes (TR -> TP)                       # isConvertibleArch()
PROPKIN_FIXED = {"TW", "DS", "SLC", "SRW", "TF", "PTC", "RC"}   # v16.0 codes (TB -> TF)        # propKinLock() — MR unlocked 2026-09-19
BODYPITCH = {"PTC", "RC"}                                            # BODYPITCH_ARCHS
WINGLESS = {"RC", "MR"}
RETIRED_AC = {"Ground", "Unclear", "NonApplicable"}
PROPKIN_CARD_RE = re.compile(r"^(core_layout|hull_array|fuselage|emp|boom|wing\d)(_t\d+)?_propKin$")
DIFF_COLS = ["patent_id", "arch", "scope", "figure", "field", "topType", "stored", "wizard_shows", "rule"]


def strip_label(v) -> str:
    s = "" if v is None or (isinstance(v, float) and pd.isna(v)) else str(v)
    s = s.split(SEP, 1)[0].strip() if SEP in s else s.strip()
    return "" if s in ("nan", "None", "NaT") else s


def _long(L: pd.DataFrame) -> pd.DataFrame:
    L = L[["Patent_ID", "Section", "Sub_Dimension", "Field", "Value"]].copy()
    L["Patent_ID"] = L.Patent_ID.astype(str)
    L["v"] = L.Value.map(strip_label)
    L["base"] = L.Patent_ID.str.replace(r"_arch\d+$", "", regex=True)
    L["arch"] = pd.to_numeric(L.Patent_ID.str.extract(r"_arch(\d+)$")[0], errors="coerce").fillna(1).astype(int)
    return L


def locked_view(d: dict) -> dict:
    """The architecture's fields as the wizard exports them: card-level propKin and fusKin under their locks."""
    tt, v = d.get("topType", ""), dict(d)
    if tt in PROPKIN_FIXED:
        for k in v:
            if PROPKIN_CARD_RE.match(k) and v[k]: v[k] = "Fixed"
    if tt in BODYPITCH: v["fusKin"] = "BodyPitch"
    return v


def moves(d: dict) -> list[str]:
    """morphConfigChanges() on the exported morphology: something changes shape between hover and cruise."""
    why = []
    for k, x in locked_view(d).items():
        if re.fullmatch(r"boom\d+_(tilts|retracts)", k) and x == "True": why.append(k)
        elif re.fullmatch(r"wing\d+_tilt", k) and x == "Tilt": why.append(f"{k}=Tilt")
        elif k == "fusKin" and x == "LevelCabin": why.append("fusKin=LevelCabin")
        elif k == "empTilts" and x == "True": why.append("empTilts")
        elif k.endswith("_propKin") and x in ("Tilt", "Vectored"): why.append(f"{k}={x}")
        elif k.endswith("_rmech") and x in ("Retracting", "Retractable", "BladeFold"): why.append(f"{k}={x}")
    return sorted(why)


def architectures(L: pd.DataFrame) -> dict[tuple[str, int], dict]:
    """(patent, arch) -> {Field: id} for G1–M3 of every architecture that carries a topType."""
    L = _long(L)
    m = L[L.Section.isin(["G1", "M1", "M2", "M3"])]
    out = {}
    for k, g in m.groupby(["base", "arch"]):
        d = dict(zip(g.Field.astype(str), g.v))
        if d.get("topType"): out[k] = d
    return out


def figures(L: pd.DataFrame) -> pd.DataFrame:
    """One row per T2 figure block (placeholders '(fig N)' excluded): base, figure, arch, status, acState."""
    L = _long(L)
    t2 = L[(L.Section == "T2") & ~L.Sub_Dimension.astype(str).str.contains(r"\(fig", regex=True)]
    t2 = t2[t2.Field.isin(["arch", "status", "acState", "hasLegends", "isMain"])]
    F = t2.pivot_table(index=["base", "Sub_Dimension"], columns="Field", values="v", aggfunc="last").reset_index()
    for c in ("arch", "status", "acState", "hasLegends", "isMain"):
        if c not in F.columns: F[c] = ""
    F["arch"] = pd.to_numeric(F.arch.replace("", "1"), errors="coerce").fillna(1).astype(int)
    return F.rename(columns={"Sub_Dimension": "figure"}).fillna("")


def _count(x) -> int:
    """xlCount(): a count of 1 is stored as True."""
    x = str(x)
    if x == "True": return 1
    if x in ("", "False", "nan", "None"): return 0
    try: return int(float(x))
    except ValueError: return 0


def replay(L: pd.DataFrame) -> pd.DataFrame:
    """Every place where the record stores something other than what the wizard shows."""
    A = architectures(L)
    rows = []
    def diff(pid, arch, scope, fig, field, tt, stored, shows, rule):
        rows.append(dict(patent_id=pid, arch=arch, scope=scope, figure=fig, field=field, topType=tt,
                         stored=stored, wizard_shows=shows, rule=rule))

    for (pid, arch), d in A.items():
        tt = d["topType"]
        if tt in PROPKIN_FIXED:
            for f, x in d.items():
                if PROPKIN_CARD_RE.match(f) and x and x != "Fixed":
                    diff(pid, arch, "aircraft", "", f, tt, x, "Fixed", f"propKinLock: {tt} propulsors never articulate")
            # an EMPTY articulation on a propulsor group with units is drawn as the locked Fixed chip too (m3TypeAttrs)
            for card in ("wing1", "wing2", "wing3", "wing4", "fuselage", "emp", "boom", "hull_array", "core_layout"):
                nt = _count(d.get(f"{card}_ntypes", "")) or 1
                for pre in ([f"{card}_t{t}_" for t in range(1, nt + 1)] if nt > 1 else [f"{card}_"]):
                    if _count(d.get(pre + "count", "")) > 0 and not d.get(pre + "propKin", ""):
                        diff(pid, arch, "aircraft", "", pre + "propKin", tt, "", "Fixed", f"propKinLock: {tt} propulsors never articulate (empty = shown Fixed)")
        fk = d.get("fusKin", "")
        if tt in BODYPITCH and fk != "BodyPitch":
            diff(pid, arch, "aircraft", "", "fusKin", tt, fk, "BodyPitch", f"applyFusKinLock: {tt} pitches as one body")
        if tt == "TF" and fk == "Fixed":
            diff(pid, arch, "aircraft", "", "fusKin", tt, fk, "", "applyFusKinLock: a TF body cannot be Fixed (pick TiltBody or LevelCabin)")
        for f, x in d.items():
            if not re.fullmatch(r"wing\d+_tilt", f) or not x: continue
            if tt in ("TF", "PTC") and x != "Fixed":
                diff(pid, arch, "aircraft", "", f, tt, x, "Fixed", f"wing-tilt lock: a {tt} wing is rigid to the airframe")
            elif tt in WINGLESS:
                pass                                        # reported with the rest of the wing rows below
        if tt in WINGLESS:
            if d.get("wCount", "") not in ("", "0", "False"):
                diff(pid, arch, "aircraft", "", "wCount", tt, d["wCount"], "False", f"{tt} is wingless: wing count 0")
            for f, x in sorted(d.items()):
                if x and (f == "wingConf" or re.match(r"wing\d+_", f)) and not f.endswith(("_count", "_sym", "_ntypes", "_quickOverride", "_quickCount", "_zone", "_zoneChord", "_zoneSpan", "_chord", "_orient", "_bmech", "_rmech", "_propKin", "_propKinOth", "_ctrlOnly", "_notes", "_symLong", "_symCirc")):
                    diff(pid, arch, "aircraft", "", f, tt, x, "", f"{tt} is wingless: no wing architecture")
        if tt in ("SLC", "SRW"):                        # m3OrientationOptions(): independent thrust never tilts — no 'Mixed'
            for f, x in d.items():
                if f.endswith("_orient") and not re.match(r"boom\d+_orient$", f) and x == "Mixed":
                    diff(pid, arch, "aircraft", "", f, tt, x, "", f"{tt}: thrust direction 'Mixed' is not offered (the wizard shows it blank) — pick Vertical or Horizontal")
        if tt == "TW" and d.get("wing1_tilt", "") not in ("", "Tilt"):
            diff(pid, arch, "aircraft", "", "wing1_tilt", tt, d["wing1_tilt"], "Tilt", "wing-tilt lock: the TW primary wing tilts")

        # card-level mounting positions hidden by m3Card (count 0, or a multi-type card; RC hubs excepted)
        for card in ("wing1", "wing2", "wing3", "wing4", "fuselage", "emp", "boom", "hull_array", "core_layout"):
            vals = {f: d.get(f"{card}_{f}", "") for f in ("zone", "zoneChord", "zoneSpan")}
            if not any(vals.values()) or d.get(f"{card}_quickOverride") == "True": continue
            nt = _count(d.get(f"{card}_ntypes", "")) or 1
            hidden = (_count(d.get(f"{card}_count", "")) == 0) if nt <= 1 else (tt != "RC")
            if hidden:
                for f, x in vals.items():
                    if x: diff(pid, arch, "aircraft", "", f"{card}_{f}", tt, x, "", "hidden mounting position (m3Card draws none here)")

    for r in figures(L).itertuples():
        if r.status != "approved": continue
        for f in ("hasLegends", "isMain"):
            if getattr(r, f) == "":
                diff(r.base, r.arch, "figure", r.figure, f, "", "", "False", "an unticked pill reads No (v15.12 export writes False)")
        d = A.get((r.base, r.arch))
        if not d: continue                                   # no topType (D1/D2, unclassifiable): nothing is locked
        tt = d["topType"]
        if tt in CONVERTIBLE or moves(d): continue           # unlocked: the reviewer's pick is what is shown
        if r.acState != INVARIANT_ID:
            diff(r.base, r.arch, "figure", r.figure, "acState", tt, r.acState, INVARIANT_ID,
                 f"acState lock: a {tt} whose record moves nothing shows Invariant on every figure")
    return pd.DataFrame(rows, columns=DIFF_COLS)


def unlocked_fixed(L: pd.DataFrame) -> pd.DataFrame:
    """Fixed-architecture records the wizard UNLOCKS because something moves (v15.8), with the reason."""
    rows = [dict(patent_id=p, arch=a, topType=d["topType"], moves="; ".join(moves(d)))
            for (p, a), d in architectures(L).items() if d["topType"] not in CONVERTIBLE and moves(d)]
    return pd.DataFrame(rows, columns=["patent_id", "arch", "topType", "moves"])
