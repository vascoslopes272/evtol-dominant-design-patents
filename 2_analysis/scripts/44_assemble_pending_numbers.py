"""Assembles pending_numbers.md from the parts written by scripts 36-55 and copies parts and CSVs into the repository.

    python 2_analysis/scripts/44_assemble_pending_numbers.py

Reads numbers/pending_part_A.md (40_pending_block_A.py), pending_part_B_C.md (39, 41, 42, 43), pending_part_D.md (45-48), pending_part_D2.md (55)
and docs/request_trace.md (the status of every request). Writes numbers/pending_numbers.md and copies it, the parts and numbers/pending_csv to
results/2_analysis/pending_numbers/. Run it after the scripts, and again when the coding-noise runs have finished.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
NUM = Path(os.environ.get("SUPP_OUT", "/mnt/storage_11tb/Drive_files_to_syncronize/paper_figures_for_other_pc/numbers"))
OUT = REPO / "results" / "2_analysis" / "pending_numbers"
PARTS = [("A. Coding-noise run and weight draws (items 1-4)", "pending_part_A.md"),
         ("B and C. Parameter sweeps and numbers quoted in the article (items 5-10)", "pending_part_B_C.md"),
         ("D. Quoted numbers and supplement tables (items 11-14, 20)", "pending_part_D.md"),
         ("D2. Locks, query, samples, mismatches, Gower example (items 15-19)", "pending_part_D2.md")]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    text = ["# Pending numbers of paper P1", "", "Dataset `eVTOL_dataset` (621 designs), thesis seed 42. Every value has its script and file in the part where it appears. "
            "Nothing is interpreted. The status of every request and the places where the files disagree with the paper are in the first section.", "",
            "## 0. Status of every request", "", (REPO / "docs" / "request_trace.md").read_text(encoding="utf-8"), ""]
    for title, f in PARTS:
        p = NUM / f
        text += ["", f"# {title}", "", p.read_text(encoding="utf-8") if p.exists() else f"*{f} does not exist yet.*", ""]
    s = "\n".join(text)
    (NUM / "pending_numbers.md").write_text(s, encoding="utf-8")
    (OUT / "pending_numbers.md").write_text(s, encoding="utf-8")
    for _, f in PARTS:
        if (NUM / f).exists():
            shutil.copy2(NUM / f, OUT / f)
    if (NUM / "pending_csv").exists():
        shutil.copytree(NUM / "pending_csv", OUT / "pending_csv", dirs_exist_ok=True)
    print(len(s), "characters;", len(list((OUT / "pending_csv").glob("*.csv"))), "CSV files in", OUT)


if __name__ == "__main__":
    main()
