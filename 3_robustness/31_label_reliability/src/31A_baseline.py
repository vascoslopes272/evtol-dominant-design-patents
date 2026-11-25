"""Stage 1: every result of core.py on the original design table, written to results/31_label_reliability/baseline.csv.

    EVTOL_DATASET=/path/to/eVTOL_dataset python 31A_baseline.py
"""
import time

import core

if __name__ == "__main__":
    t0 = time.time()
    now = core.load()
    base = core.as_frame(core.evaluate(now, now.master))
    core.OUT.mkdir(parents=True, exist_ok=True)
    base.to_csv(core.OUT / "baseline.csv", index=False)
    print(f"baseline: {len(base)} values ({time.time() - t0:.0f} s)")
