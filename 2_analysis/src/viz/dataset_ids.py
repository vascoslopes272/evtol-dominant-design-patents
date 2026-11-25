"""Read eVTOL_dataset_v1 in its corrected form (2026-11-21) with the thesis code, unchanged inside.

Since the review of 2026-11, the dataset publishes aircraft ids as ``<patent>_ad<N>`` (aircraft design; column ``ad``,
``points_to_ad``) and the thesis architecture codes TP and TF. This code was written for ``<patent>_ua<N>`` and the
labelling tool's codes TR and TB, which it already prints as TP and TF (style.py, TS_CODE). Two boundaries keep both true:

- ``ensure_compat(root, output)``: on load, the data files the analysis reads (02_patents, 03_aircraft, 05_secondary,
  06_gold_standard; no images) are mirrored into ``<output>/_dataset_v1_compat/`` with the ids and codes this code reads.
  Rebuilt when any source file is newer than the mirror. Nothing else in the values changes.
- ``publish_ids(folder)``: after the analysis, the ids written in its text outputs (csv, md, json, txt) are renamed to
  ``_ad`` so the outputs match the dataset.

``viz.config.load`` calls ``ensure_compat`` by itself when the labelled root is eVTOL_dataset_v1 in the corrected form
(it holds ``_build/nb04_v16``). The thesis as delivered (``_ua`` ids, TR/TB) is read as before.
"""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

import pandas as pd

FOLDERS = ("02_patents", "03_aircraft", "05_secondary", "06_gold_standard")
EXT = (".csv", ".xlsx", ".json", ".jsonl", ".md", ".txt")
CODE_IN = {"TP": "TR", "TF": "TB"}                         # dataset code -> code of this analysis
CODE_COLUMNS = ("topType", "arch_gt", "image_label", "ml_topType")
AD = re.compile(r"(?<=[A-Z0-9])_ad(?=\d)")
UA = re.compile(r"(?<=[A-Z0-9])_ua(?=\d)")


def is_v1(root) -> bool:
    return root is not None and (Path(root) / "_build" / "nb04_v16").is_dir()


def _sources(root: Path):
    for top in FOLDERS:
        for d, _, fs in os.walk(root / top):
            for f in fs:
                if f.endswith(EXT):
                    yield Path(d) / f


def _renamed(dst: Path) -> bool:
    """True when the mirror's own id file was renamed to _ad (it must then be rebuilt)."""
    f = dst / "03_aircraft" / "aircraft_table.csv"
    return f.exists() and bool(AD.search(f.read_text(encoding="utf-8", errors="surrogateescape")[:200000]))


def ensure_compat(root, output) -> Path:
    """The mirror of ``root`` this code reads; rebuilt when the dataset changed."""
    root, dst = Path(root), Path(output) / "_dataset_v1_compat"
    src = list(_sources(root))
    stamp = dst / ".built"
    newest = max(p.stat().st_mtime for p in src)
    if stamp.exists() and stamp.stat().st_mtime >= newest and not _renamed(dst):
        return dst
    if dst.exists():
        shutil.rmtree(dst)
    for s in src:
        d = dst / s.relative_to(root)
        d.parent.mkdir(parents=True, exist_ok=True)
        if s.suffix == ".xlsx":
            shutil.copy2(s, d)
            continue
        t = AD.sub("_ua", s.read_text(encoding="utf-8", errors="surrogateescape"))
        if s.suffix == ".csv":
            head, nl, rest = t.partition("\n")
            head = ",".join("ua" if c == "ad" else "points_to_ua" if c == "points_to_ad" else c for c in head.split(","))
            t = head + nl + rest
        d.write_text(t, encoding="utf-8", errors="surrogateescape")
        if s.suffix == ".csv" and any(c in head.split(",") for c in CODE_COLUMNS + ("column",)):
            try:
                df = pd.read_csv(d, dtype=str, keep_default_na=False, low_memory=False)
            except Exception:
                continue
            n = 0
            for c in CODE_COLUMNS:
                if c in df.columns:
                    m = df[c].isin(CODE_IN)
                    n += int(m.sum())
                    df.loc[m, c] = df.loc[m, c].map(CODE_IN)
            if s.name == "data_dictionary.csv":
                m = df["column"].eq("topType")
                df.loc[m, "options"] = df.loc[m, "options"].str.replace(r"\bTP=", "TR=", regex=True).str.replace(r"\bTF=", "TB=", regex=True)
                n += int(m.sum())
            if n:
                df.to_csv(d, index=False)
    stamp.write_text(f"mirror of {root}\n")
    return dst


def publish_ids(folder) -> int:
    """Rename <patent>_ua<N> to <patent>_ad<N> in every text output under ``folder``; returns the files changed."""
    n = 0
    for d, ds, fs in os.walk(folder):
        ds[:] = [x for x in ds if not x.startswith("_dataset_")]      # the mirrors the code reads keep the code's ids
        for f in fs:
            if f.endswith((".csv", ".md", ".json", ".txt")):
                p = Path(d) / f
                s = p.read_text(encoding="utf-8", errors="surrogateescape")
                t = UA.sub("_ad", s)
                if t != s:
                    p.write_text(t, encoding="utf-8", errors="surrogateescape")
                    n += 1
    return n


if __name__ == "__main__":
    import sys
    print(publish_ids(sys.argv[1]), "files renamed to _ad ids under", sys.argv[1])
