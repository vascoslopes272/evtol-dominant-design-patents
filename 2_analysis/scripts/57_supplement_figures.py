"""Supplement figures S2 and S3 with the names of the paper (the two builders of the thesis figures, one label each changed).

    EVTOL_DATASET=<path to eVTOL_dataset> python 57_supplement_figures.py
Writes results/2_analysis/supplement_figures/S_class_mix_vs_directory.pdf (Fig S2, builder figures_part1.fig_class_mix_ts) and
S_directory_categories.pdf (Fig S3, builder figures_part3.fig_directory_categories), with the .png and the csv of each.
Changes against the thesis versions: panel names of S2 (Separate Lift + Cruise, Vectored thrust, Multicopter, Rotorcraft, Hoverbike / Personal Flying Vehicle);
y label of S3 panel (b): "Effective number of configurations, ²D". Everything else (style, data, colours) is the builder's.
"""
import re
import sys
import inspect
import textwrap
from pathlib import Path

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "2_analysis" / "src"))
sys.path.insert(0, str(REPO / "2_analysis" / "notebooks"))
OUT = REPO / "results" / "2_analysis" / "supplement_figures"

from viz import config, thesis
from viz import figures_part1 as p1
from viz import figures_part3 as p3

cfg = config.load()
ctx = thesis.context(cfg)
import thesis_style as ts
ts.use()

# S2: panel names
p1.VFS_TITLE = {"LC": "Separate\nLift + Cruise", "VT": "Vectored\nthrust", "WM": "Multicopter", "ER": "Rotorcraft",
                "HB": "Hoverbike /\nPersonal Flying\nVehicle"}
# S3: the y label of panel (b): the builder is used as it is with that one line changed
src = textwrap.dedent(inspect.getsource(p3.fig_directory_categories))
old = 'a2.set_ylabel("²D of all designs with a\\ndirectory category: large\\ndesigns in play")'
assert old in src
src = src.replace(old, 'a2.set_ylabel("Effective number of\\nconfigurations, ²D")')
ns = dict(p3.__dict__)
exec(src, ns)
fig_dir = ns["fig_directory_categories"]

OUT.mkdir(parents=True, exist_ok=True)
for builder, name in ((p1.fig_class_mix_ts, "S_class_mix_vs_directory"), (fig_dir, "S_directory_categories")):
    fig, data = builder(ctx)
    ts.save(fig, name, OUT)
    if data is not None:
        data.to_csv(OUT / f"{name}.csv", index=False)
    plt.close(fig)
    print("written", OUT / f"{name}.pdf")
