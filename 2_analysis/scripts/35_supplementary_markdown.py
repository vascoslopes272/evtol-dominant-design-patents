"""Assembles numbers/supplementary_numbers.md from the CSVs of 34_supplementary_numbers.py, 36_robustness_numbers.py and
37_entrants_in_replicas_check.py, plus the code reading of section A (line numbers checked against the files on 2026-11-25).

    python 2_analysis/scripts/35_supplementary_markdown.py
"""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

NUM = Path(os.environ.get("SUPP_OUT", "/mnt/storage_11tb/Drive_files_to_syncronize/paper_figures_for_other_pc/numbers"))
C = NUM / "supplementary_csv"
REPO = Path(__file__).resolve().parents[2]
S34, S36, S37 = "2_analysis/scripts/34_supplementary_numbers.py", "2_analysis/scripts/36_robustness_numbers.py", "2_analysis/scripts/37_entrants_in_replicas_check.py"


def rd(n):
    return pd.read_csv(C / n)


def md(df, floatfmt=None):
    return df.to_markdown(index=False, floatfmt=floatfmt) if floatfmt else df.to_markdown(index=False)


def pct(x, d=1):
    return f"{100 * x:.{d}f} %"


def main():
    V = pd.concat([rd("_values.csv"), rd("_robustness_values.csv")], ignore_index=True).set_index("id")["value"]
    ag, nc = rd("B5_agreement_kappa.csv"), rd("B4_named_and_compared.csv")
    co, lvs = rd("B6a_designs_per_cohort_and_base.csv"), rd("B6c_configurations_per_level.csv")
    b7a, b7b = rd("B7a_design_space_table_dimensions_answered.csv"), rd("B7b_distance_dimensions_answered.csv")
    fun, dup, reas = rd("C8a_funnel.csv"), rd("C8d_aircraft_rows_duplicates.csv"), rd("C8b_disapproval_reasons.csv")
    e15, e16, e16d, e16g = rd("E15_entrant_design_shares.csv"), rd("E16a_firm_leverage_ranking.csv"), rd("E16d_numerators_denominators.csv"), rd("E16e_first_firm_grid_cohort_architecture.csv")
    e17 = rd("E17b_region_denominators_2020_23.csv")
    vt10, vt1 = rd("E11_verdict_table_10000perms.csv"), rd("E11_verdict_table_1000reps_1000perms.csv")
    bd10, bd1 = rd("E11b_band_dependent_numbers_10000perms.csv"), rd("E11b_band_dependent_numbers_1000reps_1000perms.csv")
    lc, e14 = rd("E12_label_change_per_replica.csv"), rd("E14_entrant_flags_original_vs_replicas.csv")
    n10 = int(V["E11.n_replicas_10000perms"])
    long = rd("D9_long_all_levels_all_bases.csv")
    L = []
    w = L.append

    w("# Supplementary numbers, paper P1 (dominant design in eVTOL, TFSC)\n")
    w("Recomputed on the public dataset folder `eVTOL_dataset` (621 designs, 619 with an architecture, 540 primary patents, 1 639 patent families), thesis seed 42, 10 000 permutations per band wherever a permutation band appears. "
      "Written 2026-11-25. Nothing is interpreted; no value is rounded beyond what the column says (the CSVs hold the unrounded values). "
      "Every value below has a value, the script and file it came from, and a one-line definition. Paths are relative to `evtol-design-space-analysis-tools/` unless they start with `/mnt/`. "
      "One CSV per table is in `numbers/supplementary_csv/`; the register of every single value is `numbers/supplementary_csv/_values.csv` and `_robustness_values.csv`.\n")
    w("**Scripts written for this file** (new, in `2_analysis/scripts/`): `34_supplementary_numbers.py` (sections B, C, D, E15-E17), `36_robustness_numbers.py` (E11-E13), `37_entrants_in_replicas_check.py` (E14), `35_supplementary_markdown.py` (this file). "
      "Existing scripts they rely on, unchanged: `31_family_F_numbers.py --perms 10000` (the percentile and band tables of section D, run 2026-11-25 20:30), `3_robustness/31_label_reliability/src/{core,perturb,31B_run_replicas}.py`, `viz/thesis_q2.py`, `viz/thesis_q4.py`, `viz/frames.py`, `lib/dominant_design.py`, `lib/diversity.py`.\n")
    w("**Status of the runs this file depends on.** The coding-noise run at 15 % and 10 000 permutations (`results/31_label_reliability/r15_p10000/replicas.jsonl`, started 19:05 by another process, asked for 120 replicas, about 38 minutes per replica) "
      f"held **{n10} finished replicas** when section E was computed. 1 000 replicas at 10 000 permutations do not exist and cannot be produced in this session (about 1 000 x 38 min / 15 workers, roughly 42 hours on this machine). "
      "The only 1 000-replica run is the earlier one at 1 000 permutations (`/mnt/storage_11tb/Drive_files_to_syncronize/eVTOL_dataset/07_results/71_label_reliability/`); it is given next to the 10 000-permutation numbers and labelled. "
      "`python 2_analysis/scripts/36_robustness_numbers.py` followed by `35_supplementary_markdown.py` re-reads the file and updates every E11-E13 value when the run finishes.\n")

    # ------------------------------------------------------------------ A
    w("---\n\n## A. Supplementary S3 (statistics)\n")
    w("### A1. How the rarefied 2D is obtained\n")
    w("**Observed value: the mean over 1 000 random subsamples, not one draw.** For each cohort with at least 10 designs, `hill_numbers(keys, n=40, draws=1000)` draws 1 000 subsamples of 40 designs without replacement (`rng.choice(x, size=min(n, len(x)), replace=False)`), computes 2D = 1 / sum(p_i^2) on each, and reports the arithmetic mean (rounded to 2 decimals) with the 2.5th and 97.5th percentiles of the draws (the 'D2 low / high' columns, which are not the permutation band). "
      "A fresh `np.random.default_rng(42)` is created inside every call, so the 1 000 draws of a cohort are the same in every run.\n")
    w("| value | script and line | definition |\n|---|---|---|")
    w("| N = 1 000 draws (observed) | `2_analysis/src/lib/dominant_design.py:111` (`obs_draws: int = 1000`), used at `:139` (`hill_numbers(sub[\"key\"], n=n, draws=obs_draws)`) | subsamples averaged for the observed rarefied 2D of a cohort |")
    w("| draw loop and mean | `2_analysis/src/lib/diversity.py:52-62` (`rng.choice(... size=min(n, len(x)) ...)` at `:53`; `a.mean()` at `:62`) | one subsample of min(40, cohort size) designs per draw; the 2D reported is the mean over draws |")
    w("| N = 40 draws (each shuffle of the permutation band) | `lib/dominant_design.py:111` (`perm_draws: int = 40`), used at `:151` with `seed=int(rng.integers(1e9))` | in every permutation the shuffled keys of a cohort are rarefied with 40 draws (mean of the 40), not 1 000; the band is built from these 10 000 values of the mean |")
    w("| band | `lib/dominant_design.py:156-157` | 2.5th and 97.5th percentile of the 10 000 permuted 2D values per cohort, rounded to 2 decimals |")
    w("| percentile of the observed 2D | `2_analysis/scripts/31_family_F_numbers.py` (one line added to `balance_band`: `np.mean(b <= r[\"D2\"]) * 100`) | share of the shuffles at or below the observed 2D |\n")
    w("Note: the observed value is a mean of 1 000 draws and each permuted value a mean of 40 draws. This is how the thesis code is written; it is stated here and not judged.\n")
    w("### A2. Cohorts with fewer than 40 designs\n")
    w("**Rule in the code: rarefied to their own size; skipped only under 10 designs; not flagged.** `size=min(n, len(x))` (`lib/diversity.py:53`) makes every draw take all designs of the cohort when it holds fewer than 40, so all 1 000 draws are identical and the observed 2D is the plain 1 / sum(p_i^2) of the cohort (the 'D2 low' and 'D2 high' equal it). "
      "In the permutation, the shuffled cohort has the same size, so it is rarefied to the same own size and its band is built at that size. A cohort under `min_aircraft = 10` is skipped (`lib/dominant_design.py:137`, `if len(sub) < min_aircraft: continue`), and there is no column that flags a cohort below 40. "
      "On this dataset no cohort falls under 10, so none is skipped. Cohorts under 40 are the two earliest protected cohorts (<= 2011: 18, 2012-15: 32); all-designs cohorts are 59, 57, 213 (211 with an architecture), 237 and 55.\n")
    w("### A3. Confirmations in code\n")
    w("| item asked | holds? | where in the code | what it does exactly |\n|---|---|---|---|")
    w("| share threshold above 50 % in two consecutive priority years | yes | `lib/dominant_design.py:46` (`k1 / n > 0.5`, strictly above), `:70-77` (`b == a + 1`), `viz/frames.py:1822-1823` (years 2008-2023; `DD_YEAR_MIN = 20`) | a year counts only if it holds at least 20 designs (`read`); condition 1 is met in the years that belong to a pair of consecutive read years both above 50 %. Years under 20 designs (2008-2014 on the all-designs base, more on the protected base) are never read. |")
    w("| band = 2.5th and 97.5th percentiles | yes | `lib/dominant_design.py:156-157` (2D) and `:220` (dQ) | `np.percentile(..., 2.5)` and `(..., 97.5)` of the permutation values; 'below band' = observed < low edge |")
    w("| cohort labels shuffled | yes, in an equivalent form | `lib/dominant_design.py:148` (condition 2: `rng.permutation(pool)` of the archetype keys, cohort sizes kept) and `:206-210` (condition 3: `rng.permutation(rows)` of the designs, cut into blocks of the cohort sizes) | shuffling the keys (or the designs) over a fixed list of cohort slots is the same as shuffling the cohort labels. The pool contains the designs of all five cohorts, the partial one included. |")
    w("| windows <= 2011, 2012-15, 2016-19, 2020-23, 2024-26 partial (not tested) | yes, with one point to read | `2_analysis/20_config.yaml:72-77`; `viz/frames.py:2396` (`complete = [w ... if \"partial\" not in w]`) | the verdict table reads only the four complete windows. The 2024-26 window is still computed in the band tables (rows with `partial = True`) and its designs are part of the shuffled pool of both bands. |")
    w("| Q0 = the two earliest cohorts pooled | **no: the code averages the two cohort values** | `lib/dominant_design.py:199-200` (`ref = float(np.mean([obs[w] for w in base_windows ...]))`) and `:212` (`r0` in each shuffle) | Q0 = (Q(<= 2011) + Q(2012-15)) / 2, the unweighted mean of two cohort Q values; it is not the Q of the pooled 116 designs. dQ = Q(cohort) - Q0. The same mean is taken inside every shuffle. Column 'Q of the earliest windows' in the CSVs is this value. |")
    w("| Rao's Q on the weighted Gower distance over 15 dimensions | yes | `viz/frames.py:2042-2085` (`FORM15`, `form_weights(None, \"w15\")`), `:2309-2325` (`gower_inputs`, `form_distance`), `lib/distance.py` (`gower_distance`), `lib/dominant_design.py:165-174` (`mean_pairwise_distance`) | d(i,j) = sum_k w_k delta_ijk (1 - s_ijk) / sum_k w_k delta_ijk over the 15 dimensions, blanks left out of the pair; each of the four systems weighs 1 (4 in all). Q of a cohort = `np.nanmean(D[idx, idx])`, the mean over all ordered pairs **with the diagonal (zeros) included**, which lowers Q by about 1/n. The 34-dimension weighting `w34` is also computed, for the record only. |\n")
    w("Also read from the code: condition 3 of family F is the row of level A (`viz/frames.py:2375`, `f = q[q[\"level\"].eq(\"A0\")].assign(level=\"family_b\")`): Q uses no archetype, so dQ, its band and its percentile for F are those of A. The F rows of the tables in section D repeat A's dQ for that reason.\n")

    # ------------------------------------------------------------------ B
    w("---\n\n## B. Supplementary S2 (corpus and coding)\n")
    w("### B4. Designs matched by name to a public aircraft, and the agreement check\n")
    w(md(nc))
    w("")
    w(f"- **Matched by name and compared: {V['B4.compared']}** (`{S34}` via `viz/thesis_q4.public_frame` -> `viz/frames.public_arch_frame`; definition: designs whose patent aircraft is matched to an evtol.news aircraft, every one of which enters the agreement table). Designs carrying a real product name: {V['B4.named']}; linked to an evtol.news page: {V['B4.linked_to_page']}. File: `numbers/supplementary_csv/B4_named_and_compared.csv`.")
    w(f"- **How many of the 97 were used for the agreement check: all {V['B4.compared']}.** The check has no subset. The number 87 of the paper is not a subset size: it is the number of those 97 designs on which the drawing label agrees with the public aircraft (87 of 97, `agree` / `of` in `viz/thesis_q4.py:100`). The two other comparisons give 88 of 97 and 94 of 97 (the last is over the designs that have a patent-text architecture; here also 97).\n")
    w("### B5. Cohen's kappa and raw agreement\n")
    w(md(ag, ".6f"))
    w("")
    w(f"File `numbers/supplementary_csv/B5_agreement_kappa.csv`; script `{S34}` calling `viz/thesis_q4.pairwise` and `public_labels`, `lib/association.cohen_kappa` and `raw_agreement`. Definition: kappa = (p_o - p_e) / (1 - p_e) on the architecture label of the same designs; raw agreement = agree / compared. "
      "**Per dimension: cannot be computed.** The check compares only the architecture label (G1). No source of public labels exists for any other dimension, and the match record (`match` column of `public_arch_frame`) is at architecture level. "
      "Note on the labels: the public aircraft's label is rebuilt from the existing match record (`viz/thesis_q4.py:74-89`, no new reading), so the two public pairs share the 'taxonomy' rule described there. Values of the match column: see `B5b_public_match_values.csv`.\n")
    w("### B6. Designs per cohort, base, architecture and level\n")
    w(md(co))
    w("")
    w(f"`{S34}`; files `B6a_designs_per_cohort_and_base.csv`, `B6b_designs_per_configuration_level_base_cohort.csv` (every configuration at every level, all designs and protected, per cohort), `B6c_configurations_per_level.csv`. Definition: protected = at least one linked patent whose PatSeer status is known and not inactive (`viz/frames.patent_state`, `in_force`); a design without a key at a level (no architecture, or a missing dimension at A.W.T and A.U) is not counted at that level.\n")
    w(md(lvs))
    w("")
    w("Level naming used in this file: L1 = A (architecture), L2 = A.W.T, L3 = A.U (`3_robustness/32_weight_sensitivity/src/p1_tests.py:35`); F is the yes/no family and is given on its own. Counts per architecture are the rows of L1 in `B6b`.\n")
    w("### B7. Dimensions answered for at least 500 designs\n")
    w(f"- Design-space table (11 dimensions, `viz/frames.selected_fields`): **{V['B7.design_space_table']}** answered for at least 500 designs. File `B7a_design_space_table_dimensions_answered.csv`.")
    w(f"- 15-dimension distance (`viz/frames.form_frame15`): **{V['B7.distance']}** answered for at least 500 designs (non-null cells; a pair of designs is compared only on the dimensions both answer). File `B7b_distance_dimensions_answered.csv`.\n")
    w("Lowest counts: design-space table " + ", ".join(f"{r['dimension']} {r['answered']}" for _, r in b7a.sort_values("answered").head(3).iterrows())
      + "; distance " + ", ".join(f"{r['dimension']} {r['answered']}" for _, r in b7b.sort_values("answered").head(3).iterrows()) + ".\n")

    # ------------------------------------------------------------------ C
    w("---\n\n## C. Supplementary S1 and corpus counts\n")
    w("### C8. Funnel and counts\n")
    w(md(fun))
    w("")
    w(f"`{S34}`; file `C8a_funnel.csv`. Sources: the PatSeer export `01_query/patseer_1639_2026-06-08.xlsx`, `03_patents/33_patents.csv`, `04_aircraft/42_aircraft.csv`, `45_designs.csv` (all in `/mnt/storage_11tb/Drive_files_to_syncronize/eVTOL_dataset/`) and the counts of `viz/data.py` (`ds.counts`).\n")
    w("Chain to the 621: 1 639 families -> 531 disapproved at T1 -> 1 108 approved -> 1 219 aircraft rows on them -> 422 non-primary rows removed as duplicates (D1 41 + D2 381) -> 797 primary rows -> 176 set aside by the gate -> **621 designs** on 540 primary patents. "
      "(The other chain in `viz/data.py`: 1 108 - 232 gated = 876 representative patents; 1 219 - 262 gated rows = 957 aircraft observations, of which 621 are primary.) Reasons for disapproval: " + ", ".join(f"{r['reason']} {r['patents']}" for _, r in reas.iterrows()) + ".\n")
    w(md(dup.rename(columns={"step": "aircraft-row step"})))
    w("")
    w("**Cannot be computed from the dataset:** (i) the number of records retrieved *before* family grouping and any filter on the PatSeer side: the export holds one row per family (1 639 rows, 1 639 distinct Simple Family IDs); the sum of the `No. of Simple Family Members` column is 6 884 family members, which is the closest record count the export holds, but the Get Count of the query before export is not stored; (ii) an inventor count free of name variants: the export lists inventors as `NAME (CC)`; the counts above split on `;`, lower-case and collapse spaces, so one person with two spellings or two country codes counts twice. "
      "'Assignees' in the paper (198, 130 with one design) are organisations (companies and universities, `ctx.v.firm`); the raw assignee strings number 368 and are not the paper's count.\n")

    # ------------------------------------------------------------------ D
    w("---\n\n## D. Supplementary S4 (full tables)\n")
    w("### D9. Leading share, 2D, percentile, band edges, dQ, for each level, base and cohort\n")
    w("Source: `2_analysis/scripts/31_family_F_numbers.py --perms 10000` (run note: " + V["D9.run_note"].strip() + "), output files `results/2_analysis/family_F/percentiles_balance.csv`, `percentiles_disparity.csv`, `percentiles_disparity_protected_vs_all.csv`, restructured by "
      f"`{S34}`. Definitions: *share* = share of the leading configuration in the cohort; *2D* = Hill 2D rarefied to 40 (raw, mean of 1 000 draws, see A1); *percentile* = share of the 10 000 shuffles at or below the observed value (the tests read the low tail); *band* = 2.5th and 97.5th percentile of the shuffles; "
      "*dQ* = Q(cohort) - Q0 with the weighting `w15`; *protected* = designs with an active patent (the protected base has its own shuffles, built on the protected designs only). Cohort 2024-26 is partial and is listed, not tested. "
      "Files, one per level and base, long format: `D9_L1_all.csv`, `D9_L1_protected.csv`, `D9_L2_all.csv`, `D9_L2_protected.csv`, `D9_L3_all.csv`, `D9_L3_protected.csv`, `D9_F_all.csv`, `D9_F_protected.csv`; all together `D9_long_all_levels_all_bases.csv`; wide table `D9_wide.csv`; LaTeX `D9_wide_latex.tex` (a `tabular` with one row per level, base and cohort). "
      "Also: `D9_protected_2020_23_against_all_designs_baseline.csv` (protected designs of 2020-23 against the baseline and band of all designs, the reading of Table 4 in the thesis) and `D9_dq_weighting_w34_for_the_record.csv`.\n")
    w("Points the reader needs: (1) for F, dQ, its band and its percentile are those of A (A2, last paragraph); (2) the F level keeps every design's architecture except that the designs of the family share one archetype, 'Lift + Cruise + CVT* family' (`viz/frames.py:1856-1866`), so F has 12 classes and its leading configuration is the family from 2016-19 on; (3) the 'protected' band of dQ is the band of the protected designs shuffled among themselves in `frames.dd_form_table`, whereas the weight test (`ws_core.py`) and `D9_protected_2020_23_against_all_designs_baseline.csv` use the all-designs baseline and band for the protected designs of 2020-23.\n")
    sub = long[long["window"].eq("2020-23")][["L", "base", "aircraft", "share of the leading configuration", "Hill 2D rarefied to 40 (raw, mean of 1000 draws)", "percentile of the observed 2D in its permutation distribution", "2D band low (2.5th pct)", "2D band high (97.5th pct)", "dQ", "percentile of the observed dQ", "dQ band low (2.5th pct)", "dQ band high (97.5th pct)"]]
    w("Extract (cohort 2020-23, all levels and bases; the full tables are in the CSVs):\n")
    w(md(sub))
    w("")
    w("### D10. Figures of `paper_figures_for_other_pc` beyond the main ones\n")
    w("`paper_figures_for_other_pc` holds 15 PDFs (each with a CSV of the plotted values in `results/2_analysis/paper_figures/`), made by `2_analysis/scripts/33_paper_figures.py` on 2026-11-25 20:30. Which figures are the main ones of the paper is not recorded anywhere I could read; I take Figures 4, 5 (combined), 6 and 7 of the folder's README as main. The README's panel list gives:\n")
    w("| file | content | in the folder as main or extra |\n|---|---|---|")
    for f, t, k in [("fig4_architecture_shares.pdf", "share of designs per architecture and cohort", "main (Fig 4)"),
                    ("fig5abc_balance_three_levels.pdf", "2D at A, A-W-T, A-U on one sheet, all and protected designs", "main (Fig 5)"),
                    ("fig5a_balance_L1.pdf, fig5b_balance_L2.pdf, fig5c_balance_L3.pdf", "the three panels of the sheet one by one, per level", "extra, per level, could go in S4"),
                    ("fig5d_disparity.pdf", "dQ with its band, all designs and the protected designs of 2020-23", "main (Fig 5d)"),
                    ("fig6a_modal_SLC.pdf, fig6b_modal_TP.pdf, fig6c_modal_CVT.pdf", "layouts inside the three largest architectures, five cohorts", "main (Fig 6)"),
                    ("fig6_legend_SLC.pdf, fig6_legend_TP.pdf, fig6_legend_CVT.pdf", "legend strips of Fig 6", "support files"),
                    ("fig7a_F_share.pdf, fig7b_F_balance.pdf", "F share per priority year; 2D of F", "main (Fig 7)"),
                    ("fig7c_exploratory_check_dQ_inside_F.pdf", "exploratory check of dQ inside F with architecture weight 0 (no convergence inside F)", "extra, sensitivity, could go in S4")]:
        w(f"| {f} | {t} | {k} |")
    w("")
    w("**Per-region and sensitivity figures are not in `paper_figures_for_other_pc`.** Candidates that exist elsewhere, as produced by the notebooks (names only, not checked for style): "
      "per region, in `results/2_analysis/figures/Part_V_assignees_and_regions/`: `V3_regions_what_and_when/main/q3_region_design_all_years.pdf`, `.../main/q3_region_entry_lag.pdf`, `.../appendix/q3_region_countries.pdf`, `q3_region_mix_by_window_class.pdf`, `q3_region_mix_by_window_tilting.pdf`, `q3_region_mix_by_window_units.pdf`, "
      "`V4_regions_and_family_F/main/q7_region_family_share.pdf`, `.../appendix/q7_region_lean_without_largest_filer.pdf` (and `q7_region_firm_proximity.pdf` in `freeze/Figures/...`); "
      "entrants: `V2_new_and_returning_assignees/appendix/q2_first_vs_returning_filers.pdf`, `q2_entrant_class_mix.pdf`, `q2_tilt_wing_entrants.pdf`; "
      "dominant design: `Part_III_dominant_design/III2_III3_dominant_design/main/q7_condition1_family.pdf`, `q7_condition2_balance.pdf`, `q7_condition3_cohesion.pdf`, `q7_family_conditions.pdf`; "
      "sensitivity to the weights: `/mnt/storage_11tb/Drive_files_to_syncronize/eVTOL_dataset/07_results/72_weight_sensitivity/test1_figure.pdf` (and `.png`). No figure of the coding-noise run exists. "
      "Note: the notebook figures of Part III use 1 000 permutations (`viz/thesis_q7.py:26`), not the 10 000 of the paper figures.\n")

    # ------------------------------------------------------------------ E
    w("---\n\n## E. Pending numbers for the main text\n")
    w("### E11. Coding-noise robustness (15 % per value, locks), every result of the verdict table\n")
    w(f"Two runs, side by side. **10 000 permutations: {n10} replicas (of the 120 asked; not 1 000).** **1 000 permutations: 1 000 replicas (reference run, 2026-11-22/23).** "
      "Both: error rate 0.15 per coded value, locks redrawn up to 20 times, replica i uses `default_rng([20261118, i])`. The data and the original verdicts are the same in both runs; the only differences on the original table are the band edges (1 000 against 10 000 shuffles) and one verdict, "
      "**balance at A.U on the protected base: met with 10 000 shuffles, not met with 1 000** (the observed 2D sits next to the band edge, 13.88 against 13.82 and 13.95-13.99 for the other edges). "
      "Because of that flip the share 'keeping the original value' for that row is not comparable between the two runs (14.6 % against 82.6 %): the shares where the statement is *true* are 14.6 % and 17.4 %.\n")
    keep = ["base", "condition", "level", "original", "replicas", "share keeping the original value", "Wilson 95 % low", "Wilson 95 % high", "share where it is true"]
    m = vt10[keep].merge(vt1[["base", "condition", "level", "original", "replicas", "share keeping the original value", "share where it is true"]], on=["base", "condition", "level"], suffixes=(" (10 000 perms)", " (1 000 perms, 1 000 reps)"))
    w(md(m, ".3f"))
    w("")
    w(f"Files: `E11_verdict_table_10000perms.csv`, `E11_verdict_table_1000reps_1000perms.csv`; script `{S36}` reading `results/31_label_reliability/r15_p10000/replicas.jsonl` and `eVTOL_dataset/07_results/71_label_reliability/reliability_replicas.csv`; keys are those of `3_robustness/31_label_reliability/src/core.py` (`r3_r4_r8`). "
      "Definition: 'keeping the original value' = share of replicas in which the yes/no cell has the value it has on the original table (a cell that is False on the original table is kept when it stays False); Wilson 95 % interval on that share; condition names as in the verdict table (1 share, 2 balance, 3 disparity, all three). Levels A, A.W.T, A.U, F.\n")
    w("**Band-dependent values included** (the 2D and dQ of 2020-23 and their own lower band edges in each replica, 10 000 permutations):\n")
    w(md(bd10[["base", "level", "replicas", "2D original", "2D median", "2D band low original", "2D band low median", "share with 2D below its own band low", "dQ original", "dQ median", "dQ p5", "dQ p95", "dQ band low original", "dQ band low median", "share with dQ below 0", "share with dQ below its own band low"]], ".4f"))
    w("")
    w("Files `E11b_band_dependent_numbers_10000perms.csv` and `E11b_band_dependent_numbers_1000reps_1000perms.csv`. Definition: 'below its own band low' = in that replica, observed value < the 2.5th percentile of that replica's own permutation distribution; 'dQ below 0' = direction only. The trend results (architecture shares, trajectories) and the regional and entrant tests are in `E11c_trend_keys.csv` and in the full per-key summary of the run (`results/31_label_reliability/r15_p10000/` when `31B_run_replicas.py --summary-only` is run on the finished job).\n")
    w("### E12. Share of label changes\n")
    w(f"**Mean {pct(float(V['E12.mean_share_621']), 2)} of the 621 designs ({pct(float(V['E12.mean_share_619']), 2)} of the 619 with an architecture) change architecture label per replica, over 100 replicas (0-99).** Median {V['E12.median_changed']} labels, range {V['E12.min_max_changed']}. The paper's 7.5 % is not reproduced exactly; the mean is 7.3 %. "
      f"Definition (`3_robustness/31_label_reliability/src/31B_run_replicas.py:_one`, lines `a0 = ... topType`, `a1 = ...`): number of analysis designs whose architecture code `topType` differs between the original and the perturbed table, divided by the number of designs perturbed (621). The change is the net result after the locks: a perturbed architecture that breaks a lock is redrawn up to 20 times (`perturb.MAX_REDRAWS`), so less than 15 % of the labels change. "
      f"Computed by `{S36}` by running only the perturbation (no permutations are needed, so it does not depend on the permutation count); check against the {n10} finished 10 000-permutation replicas: {V['E12.crosscheck_with_jsonl']}. File `E12_label_change_per_replica.csv`.\n")
    w("### E13. Verdict for family F under the coding replicas\n")
    f10 = vt10[vt10["level"].eq("F")][["base", "condition", "original", "replicas", "share keeping the original value", "Wilson 95 % low", "Wilson 95 % high", "share where it is true"]]
    f1 = vt1[vt1["level"].eq("F")][["base", "condition", "share keeping the original value", "share where it is true"]]
    w(md(f10.merge(f1, on=["base", "condition"], suffixes=(" (10 000 perms)", " (1 000 perms, 1 000 reps)")), ".3f"))
    w("")
    w("Files `E13_family_F_verdict_10000perms.csv` and `E13_family_F_verdict_1000reps_1000perms.csv`; same script and definitions as E11. The conditions 'F above 50 % in 2020 / 2021' are the F-share cells of condition 1.\n")
    w("### E14. Entrants inside the replicas\n")
    w("**Confirmed: the replicas use definition (b), first appearance with a design in any cohort.** `core.r7_entrants` (`3_robustness/31_label_reliability/src/core.py:226-241`) calls `viz/frames.named_entries` (`frames.py:2969-2978`): for each organisation, `first` = its earliest cohort that holds a design of it (any of the five cohorts, the partial one included); a design is 'first-time' when its cohort equals that cohort. Definition (a) (first family in the corpus, `2_analysis/scripts/30_entrants_two_definitions.py`) is not used in the replicas. "
      "The perturbation does not touch organisation, priority year or cohort (`perturb.py` module text), so the entrant flags are identical in every replica; checked on replicas 0-4 against the original table (0 differences in flag, cohort and organisation, while 29-42 architecture labels differ in each):\n")
    w(md(e14))
    w(f"\nFile `E14_entrant_flags_original_vs_replicas.csv`, script `{S37}`. What changes in the replicas is only the architecture mix that the chi-square compares (result 7 of `core.py`).\n")
    w("### E15. Entrant shares of company and university designs\n")
    w(md(e15, ".6f"))
    w("")
    w(f"**2016-19: {V['E15.2016-19']}; 2020-23: {V['E15.2020-23']}.** The paper's 63 % and 65 % are reproduced (63.46 % and 64.64 %). Numerator = designs of named organisations (companies and universities; `v.named`: 397 company + 43 university designs, 440 in all cohorts) whose organisation's earliest cohort with a design is this cohort; denominator = all designs of named organisations in the cohort. Individual inventors and unnamed assignees are not in the denominator. "
      f"Script `{S34}` via `viz/frames.named_entries` (`frames.py:2969`); the text values come from `viz/thesis_q2.py:398-401` (`first_1619` 99, `named_1619` 156, `first_2023` 117, `named_2023` 181, in `results/2_analysis/freeze/NUMBERS_V.md:152-159`). File `E15_entrant_design_shares.csv`. "
      "Counted by organisations instead of designs, definition (b) gives 89.2 % (58 of 65) and 81.0 % (81 of 100) (`results/2_analysis/entrants/entrants_two_definitions.csv`, script `30_entrants_two_definitions.py`, copy in `E15b_...csv`); do not mix the two units.\n")
    w("### E16. Dropping the largest assignee (Bell / Textron)\n")
    w(md(e16d, ".6f"))
    w("")
    w(f"**{V['E16.first']}** and **{V['E16.second']}.** The figure 2.6 is Bell / Textron and Lift + Cruise (SLC); the figure 1.1 is **not Bell / Textron: it is Airbus**, the second firm of the ranking, also on Lift + Cruise (SLC). Both are all-cohort shifts over the 619 designs with an architecture (all cohorts together, not one cohort): "
      "the SLC share is 160 of 619 = 25.85 % with the firm and 159 of 559 = 28.44 % without Bell / Textron (60 designs), and 148 of 598 = 24.75 % without Airbus (21 designs). "
      f"Script `{S34}` via `viz/frames.firm_leverage_table` (`frames.py:2858`) and `firm_leverage_classes` (`:2882`), the functions behind `lev1_pp` and `lev2_pp` of `viz/thesis_q2.py:389-390`. Definition: the largest change in a class share, in points, when one firm with 3 or more designs is dropped (all years). Files `E16a_firm_leverage_ranking.csv`, `E16b_share_shift_when_firm_dropped.csv`, `E16c_first_firm_all_classes.csv`, `E16d_numerators_denominators.csv`. "
      "In case the paper meant a per-cohort change instead, `E16e_first_firm_grid_cohort_architecture.csv` gives the change of every architecture share in every cohort when Bell / Textron is dropped (no value of 2.6 or 1.1 appears there for SLC in a cohort: the largest per-cohort Tilt Propulsor change is 5.0 points in 2016-19, `q7_iii1_without_bell.csv` of `results/2_analysis/freeze/csv`). The without-Bell / Textron dominant-design test is a different computation (notebook 29, `freeze/csv/q7_iii1_without_bell.csv`).\n")
    w("### E17. Region check\n")
    w(md(e17, ".6f"))
    w("")
    w(f"**Asia-Pacific: {V['E17.asia_pacific']} designs of 2020-23 (92 / 237 = 38.8 % of the cohort).** The three regions together hold **{V['E17.three_regions']}** of the 237 designs of 2020-23 (North America 77, Europe 63, Asia-Pacific 92); 5 designs are outside the three regions or have no region. "
      "So 92 and 232 are not both over 237: 92 is Asia-Pacific's count in the cohort (also its F base, because F is defined for every one of them), and 232 is the base of the regional F test (F aircraft 37 + 36 + 42 = 115 of 232). "
      f"Script `{S34}` via `viz/frames.regional_frame` and `region_lean` (`frames.py:3270`); file `E17b_region_denominators_2020_23.csv`, `E17a_region_F_share.csv`; check against `results/2_analysis/freeze/csv/q7_region_family_share.csv` (77, 63, 92).\n")

    # ------------------------------------------------------------------ S5 sweep
    w("### S5. Parameter sweep (rarefaction size, variety threshold, share window)\n")
    w("Script `2_analysis/scripts/38_parameter_sweep.py` (thesis functions unchanged, seed 42, 10 000 permutations for the rarefaction part). Files `S5_*.csv`. Default values for comparison: rarefaction 40, threshold 80 %, two consecutive years.\n")
    for n_ in (30, 50):
        f = C / f"S5_rarefaction_{n_}.csv"
        if f.exists():
            r = pd.read_csv(f)
            r = r[r["window"].isin(["<= 2011", "2012-15", "2016-19", "2020-23"])]
            w(f"**Rarefied to {n_} designs: balance (condition 2) per level, base and cohort.** 2D = mean of 1 000 draws; percentile and band as in D9; 'below band' = 2D under the 2.5th percentile of the shuffles.\n")
            w(md(r[["L", "base", "window", "aircraft", "D2", "percentile of the observed D2 (share of shuffles at or below)", "D2 permutation low", "D2 permutation high", "below band"]].rename(columns={"percentile of the observed D2 (share of shuffles at or below)": "percentile"}), ".2f"))
            w("")
        else:
            w(f"Rarefaction {n_}: not finished when this file was written.\n")
    f = C / "S5_variety_threshold.csv"
    if f.exists():
        w("**Variety threshold** (a dimension varies when its leading option holds under the threshold; wing configuration is fixed in a winged architecture with 20+ designs when its leading share is at or above it):\n")
        w(md(pd.read_csv(f).drop(columns=["varying dimensions"])))
        w("\nThe interpretation of 'variety threshold' as this 80 % rule (thesis 3.4.2, `core.py` result 1) is mine; the names of the varying dimensions at each threshold are in the CSV.\n")
    f = C / "S5_share_window.csv"
    if f.exists():
        w("**Share window** (condition 1: k consecutive read years, each with >= 20 designs, above 50 %). k = 2 is the default; 3 and 4 are added because the request says '2 and 4 years' and the code's default is two:\n")
        r = pd.read_csv(f).fillna("")
        w(md(r[r["condition 1 met"] | r["level"].isin(["L1", "F"])]))
        w("")
    w("Early-cohort note: at A.U on all designs the two earliest cohorts sit below their own bands (percentiles 0.9 and 0.1); on the protected base A.U is below band in both and A.W.T in <= 2011 (percentile 0.7). `D9_L3_all.csv`, `D9_L2_protected.csv`, `D9_L3_protected.csv`.\n")

    # ------------------------------------------------------------------ F
    w("---\n\n## F. Robustness methods, in prose (for your review)\n")
    import json
    kept = sum(json.loads(x)["log"]["designs kept after 20 redraws"] for x in (REPO / "results" / "31_label_reliability" / "r15_p10000" / "replicas.jsonl").read_text().splitlines())
    w(PROSE.replace("KEPT design(s)", f"{kept}"))

    # ------------------------------------------------------------------ differences
    w("\n---\n\n## What differs from the numbers already in the paper (old value, new value)\n")
    w(DIFFS(vt10, vt1, bd10, bd1, lc, n10))
    w("\n---\n\n## What could not be done\n")
    w("- 1 000 coding-noise replicas at 10 000 permutations (E11, E13): not available. " + f"{n10} of 120 exist at 10 000 permutations (the job is still running); the 1 000-replica run is at 1 000 permutations. Cost of 1 000 at 10 000: about 38 minutes per replica per core, roughly 42 hours on 15 workers.")
    w("- Per-dimension kappa (B5): no public label exists below the architecture level.")
    w("- Records retrieved before family grouping and a person-level inventor count (C8): not stored in the dataset.")
    w("- Which figures are 'main' (D10): not recorded; per-region and sensitivity figures are not in `paper_figures_for_other_pc`.")
    return "\n".join(L)


PROSE = (
    "The robustness work asks whether each yes/no statement of the paper stays true when the input is changed, by two different kinds of change, and it never changes the thesis code: every measure is imported and called as it is.\n\n"
    "The first kind changes the weights of the distance behind the disparity condition and leaves the designs as coded. The distance is a Gower distance over 15 dimensions, with the 15 weights of Table A.11 held as one flat list. One thousand weight vectors are drawn once, with numpy's default generator seeded 42 (`default_rng(42).normal(0, 0.35, (1000, 15))`, then the exponential), so that each of the 15 weights is multiplied by its own independent factor exp(N(0, 0.35^2)); nine times in ten a factor lies between about 0.56 and 1.78. The draws are saved to a file and every test reads that file. "
    "For each draw, Rao's Q is recomputed for the cohort 2020-23 and for the two earliest cohorts, dQ is the difference between Q of 2020-23 and the mean of the two earliest cohorts' Q, and the lower band edge is the 2.5th percentile of dQ over 10 000 shuffles of the designs across cohorts with the cohort sizes kept. The shuffles are drawn once, with the generator seeded 42, and reused in every draw, so that two draws differ only by their weights. "
    "The condition holds in a draw when dQ lies below the lower band edge, and the margin is the band edge minus dQ. This is done at the three levels (A, A.W.T, A.U), on all designs and on the actively protected designs (for the protected designs the Q of 2020-23 is compared with the all-designs baseline and band, with the 2020-23 block cut at the protected size). A second, exploratory test applies the same draws to family F alone with the weight of the architecture set to 0.\n\n"
    "The second kind changes the coding and leaves the weights as chosen. Every value that the wizard asks for in the architecture and morphology stages (architecture, fuselage, boom, wing and propulsor fields, for the 621 analysis designs) is replaced independently with probability 0.15. An option field takes another option of the same dimension, drawn uniformly among the options of the data dictionary; a tick takes the other answer; a positive count takes another positive count observed for that dimension in the analysis designs. Blanks, values that the wizard hides by an override, boom groups or wings that do not exist, and the priority year, legal status, region, assignee, approval and duplicate fields are not changed. "
    "A design whose changed codes break one of the twelve locks of the codebook (Table A.5), when its original codes do not break it, is redrawn up to 20 times, after which it keeps its original codes (in the finished replicas of the 10 000-permutation run, KEPT design(s) were kept after 20 redraws in all). The four propulsion columns that the dataset derives from the codes are recomputed from the perturbed codes with the rules of the dataset build. Replica i uses numpy's default generator seeded with the pair (20261118, i), so a replica does not depend on the others or on the number of workers. "
    "On each replica the gate, the levels, family F, both permutation bands, the Holm corrections and the regional and entrant tests are recomputed from the thesis code. The permutation bands inside the replicas use the seed 42 and either 1 000 shuffles (the run of 1 000 replicas) or 10 000 shuffles (the run of 120 replicas at 15 % and 120 at 20 %, of which the first is partly finished). "
    "The share of architecture labels that change is measured on the perturbation alone; after the locks it is about 7.3 % at the 15 % rate, over 100 replicas. For each yes/no result the table gives the share of replicas in which the original verdict is kept, with its Wilson 95 % interval, and for numbers the median and the 5th and 95th percentile.\n\n"
    "The reading convention is applied by hand to the share of replicas or draws in which a statement stays true, and it is not written in any code: 95 % or more is read as robust, 70 to under 95 % as mostly robust, 30 to under 70 % as sensitive, and under 30 % as not robust. The cut points are a convention for reading the tables and not a statistical threshold. Direction (the sign of dQ, the sign of a trend) and significance (dQ below its band, a Holm p-value under 0.05) are reported as two separate statements. "
    "All permutation bands use the thesis seed 42, and the thesis value of 1 000 permutations is kept only where a result is compared with the thesis; the paper's own bands, the weight test and the 10 000-permutation coding runs use 10 000.\n")


def DIFFS(vt10, vt1, bd10, bd1, lc, n10):
    rows = []
    rows.append(("Architecture-label change per replica", "7.5 % (paper text, S2)", f"{100 * lc['share of 621 designs'].mean():.2f} % of 621 (100 replicas, seed 20261118)"))
    rows.append(("Drawing against patent text, agreement (Table 2)", "93 of 97, kappa 0.95 (thesis as delivered)", f"{int(rd('B5_agreement_kappa.csv').iloc[2]['designs that agree'])} of 97, kappa {rd('B5_agreement_kappa.csv').iloc[2]['Cohen' + chr(39) + 's kappa (unrounded)']:.2f}"))
    rows.append(("Patent text against public aircraft, agreement (Table 2)", "89 of 97, kappa 0.90 (thesis as delivered)", f"{int(rd('B5_agreement_kappa.csv').iloc[1]['designs that agree'])} of 97, kappa {rd('B5_agreement_kappa.csv').iloc[1]['Cohen' + chr(39) + 's kappa (unrounded)']:.2f}"))
    rows.append(("Spread of the weight factors (draft text of the robustness note)", "five times in six between 0.56 and 1.78", "exp(N(0, 0.35^2)): 0.56 to 1.78 is the central 90 % (nine in ten); five in six lies between 0.62 and 1.62"))
    rows.append(("Q0 (two earliest cohorts)", "'pooled' (as the request describes it)", "mean of the two cohort Q values (`dominant_design.py:200`)"))
    rows.append(("Rarefied 2D, observed", "'one draw or a mean?' (open in the request)", "mean of 1 000 draws; permutations use the mean of 40 draws"))
    rows.append(("'Used for the agreement check' (97 and 87)", "97 matched, 87 used", "97 matched and all 97 used; 87 = agreements of drawing against public aircraft"))
    rows.append(("Second leverage figure (1.1 points)", "attributed to Bell / Textron in the request", "Airbus, Lift + Cruise; Bell / Textron is 2.6 points"))
    # shares: draft robustness document (1 000 reps) vs now
    doc = [("Balance met at A, all designs: share keeping it", "80 %", "3 | all designs | 2 balance | A"),
           ("Balance at A.W.T, all designs: share keeping 'not met'", "85 %", "3 | all designs | 2 balance | A.W.T"),
           ("Disparity at A, all designs: share where dQ below band", "14 %", "3 | all designs | 3 disparity | A"),
           ("F meets all three, protected: share of replicas", "0.9 %", "4 | actively protected | all three | F"),
           ("F share above 50 % in 2020, protected: share of replicas", "4.6 %", "4 | actively protected | F above 50 % in 2020")]
    for name, old, key in doc:
        p = key.split(" | ")
        k = key.replace("A.W.T", "A·W·T")
        r = vt10[vt10["key"].eq(k)]
        if len(r):
            r = r.iloc[0]
            val = r["share where it is true"] if "below band" in name or "meets" in name or "above 50" in name else r["share keeping the original value"]
            rows.append((name, f"{old} (1 000 replicas, 1 000 perms, draft of 25 Nov)", f"{100 * val:.1f} % ({n10} replicas, 10 000 perms; not final)"))
    rows.append(("Balance at A.U, protected base, original verdict", "not met (run with 1 000 shuffles)", "met (10 000 shuffles): 2D sits next to the band edge"))
    # band edges
    refsum = pd.read_csv("/mnt/storage_11tb/Drive_files_to_syncronize/eVTOL_dataset/07_results/71_label_reliability/reliability_summary.csv")
    import json
    jl = (REPO / "results" / "31_label_reliability" / "r15_p10000" / "replicas.jsonl").read_text().splitlines()
    base = next(json.loads(x)["results"] for x in jl if json.loads(x)["log"]["replica"] == -1)
    old = dict(zip(refsum["key"], refsum["original value"]))
    for k in base:
        if "band low" in k and str(base[k]) != str(old.get(k)):
            rows.append((f"Lower band edge: {k}".replace(" | ", " / "), f"{old.get(k)} (1 000 shuffles)", f"{base[k]} (10 000 shuffles)"))
    t = pd.DataFrame(rows, columns=["quantity", "old value", "new value"])
    t.to_csv(C / "differences_old_new.csv", index=False)
    return "Old values are those stated in the request, in the thesis as delivered, or in the draft `docs/robustness_verdicts_for_supervisors.md` (which used the 1 000-permutation run). New values are from this file. Items that agree with the paper (97 and 87; 198 and 130; 63 % and 65 %; 2.6; 92 of 237 and 232) are not listed. File `differences_old_new.csv`.\n\n" + t.to_markdown(index=False)


if __name__ == "__main__":
    text = main()
    (NUM / "supplementary_numbers.md").write_text(text + "\n", encoding="utf-8")
    print(len(text))
