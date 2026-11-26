# Why the paper's numbers differ from the files: disagreements 2 to 6 of `docs/request_trace.md` section 3

Written 2026-11-26. Result in one line each: 2 explained (older dataset), 3 explained (older dataset, reproduced to the second decimal, with one consequence for the verdict), 4 explained (older dataset, plus a unit word), 5 explained for 68 %, 72 % not traceable to a sample but matched by the new census within 0.3, 6 small (definition of the reference set; no dataset effect).

## How the paper values were read and how they were reproduced

- The paper text is not in the files I could search. The paper values were read from the submitted thesis, `/tmp/claude-1006/-home-vasco-Vasco-Workspace-Tese-Vasco-Lnx/1cab545d-9418-4438-a882-6ebafb03763e/scratchpad/thesis.txt` (lines 3361-3373 Table 4.7 and text, 3445-3448 and 3483 last 100 designs, 2743 and 4665 step-up, 2540-2570 Table 4.1, 2700-2706 lag). Every paper value of items 2 to 6 is in that text, with the same number. If the paper (P1) differs from the thesis text, the comparison below is with the thesis.
- The thesis dataset is the frozen snapshot `/mnt/storage_11tb/Drive_files_to_syncronize/eVTOL_dataset_v1_WORK/_frozen_thesis_submitted/` (git tag `thesis-submitted`, 627 designs; its README lists the two later corrections: 2026-11-09 one Sikorsky helicopter removed, 627 to 626; 2026-11-11 one ground-truth change). `scratchpad/a627_old.csv` is the 626-design version of the same table.
- Method: the thesis functions of the repository, unchanged (`3_robustness/31_label_reliability/src/core.py` builds the context from a design table; `frames.archetype_levels_table`, `frames.discovery_inputs`, `diversity.discovery_tail_band`, `thesis_q1._calc`, `thesis_q1.growth_models`), fed with the frozen 627 tables, seed 42, one process under `nice -n 19`. The backup code of 2026-10-16 (`scratchpad/backup_2_analysis/21_thesis_analysis/src/lib/diversity.py, concentration.py, growth.py, viz/thesis_q6.py`) is identical to the current code (diff empty), so the code version is not a cause for these items. The scripts are in `numbers/discrepancy_scripts/` (copies of the scratchpad `dc/` folder): `run627_frozen.py` (items 2, 3), `q1_627g.py` (item 4), `vis627.py` (item 6), `cfgdiff.py` (which configuration changed).
- Command pattern: `EVTOL_DATASET=/mnt/storage_11tb/Drive_files_to_syncronize/eVTOL_dataset nice -n 19 python3 <script> old` (`old` = frozen 627 table, `new` = the 621 dataset).

## 2. Configurations 12, 39, 43 and effective numbers 7.3, 16.4, 29.3

| | paper (Table 4.7) | file, 621 designs | reproduced on the 627 table |
|---|---|---|---|
| configurations A / A.W.T / A.U | 12 / 39 / 43 | 12 / 39 / 44 | 12 / 39 / 43 |
| singletons | 0 / 10 / 3 | 0 / 10 / 4 | 0 / 10 / 3 |
| effective number, 1D | 7.3 / 16.4 / 29.3 | 7.3 / 16.5 / 29.6 | 7.3 / 16.4 / 29.3 |
| designs at the level | (623 at A.W.T) | 619 / 617 / 618 | 625 / 623 / 624 |
| largest share | 26 / 17 / 10 % | 26 / 16 / 10 % | 26 / 17 / 10 % |

- Cause: older dataset (627 against 621 designs, plus the relabelling of the review of 2026-11-21). Reproduced exactly with `run627_frozen.py old` (the 627 table gives all values of the paper, the 623 designs at A.W.T included).
- The earlier note of the request trace ("43 is A.U on complete years") is wrong: on the 627 table the whole corpus has 43 A.U configurations. On complete years it is 42.
- Which configuration moved: `cfgdiff.py`. A.U has one configuration in the 621 dataset that the 627 table lacks, "TB 9+" (Tilt Frame with nine or more propulsor units), because a few designs changed band between the two tables (SLC 9+ minus 4, TW 9+ minus 2, SLC 7-8 plus 1, TB 9+ plus 1, TR 9+ plus 1). A.W.T has the same 39 configurations (only the label format differs, "1.0" against "1").
- The paper's column is the 1D effective number (Table 4.7 header "1D", thesis text "effective number"). The statement of the request trace that the paper calls it 2D is not supported by the thesis text; the 2D values (5.7, 11.3, 22.5 on the 627 table; 5.72, 11.32, 22.78 on 621) are another column and are not the paper's.
- Size of the difference: one configuration (43 against 44, 2 %), 0.1 and 0.3 in the effective number (0.6 % and 1 %), one singleton. Verdict: explained (small).

## 3. The 100 most recent designs: 4.1 against 1.6, p 0.058; at A.U 1.1 against 0.6, p 0.44

| | paper | file, 621 designs | reproduced on the 627 table |
|---|---|---|---|
| A.W.T new in last 100 | 4.1 | 4.18 | 4.14 |
| A.W.T random order | 1.6 | 1.44 | 1.61 |
| A.W.T p | 0.058 | 0.0375 (whole counts) / 0.007 (share >= date mean) | 0.0579 (whole counts) / 0.0126 |
| A.U new in last 100 | 1.1 | 1.06 | 1.09 |
| A.U random order | 0.6 | 0.79 | 0.60 |
| A.U p | 0.44 | 0.544 (whole counts) / 0.170 | 0.4447 (whole counts) / 0.1058 |

- Cause: older dataset, and the estimator is the "whole counts, averaged over the date orderings" p, not the "share of shuffles >= date mean". Reproduced to the second decimal with `run627_frozen.py old` (frozen 627 table, complete years up to 2023, 568 designs at A.W.T and A.U, tail 100, 1 000 date orderings, 10 000 shuffles, seed 42): 4.14 against 1.61, p 0.0579 (paper 0.058); A.U 1.09 against 0.60, p 0.4447 (paper 0.44). The earlier statement "source not found" is replaced by this.
- The 626-design table (`a627_old.csv`) gives 4.14 against 1.61, p 0.0516, and A.U p 0.4499; the p moves by about 0.005 between the two tables and by about 0.004 with the seed (seeds 1 to 3 on the 626 table: 0.053 to 0.056), so the paper's 0.058 needs the 627 table; that is within Monte Carlo noise.
- Size of the difference: the random mean moves from 1.61 to 1.44 at A.W.T (0.17, 11 %) and from 0.60 to 0.79 at A.U, because the tail and the configurations of the 563 complete-year designs changed with the relabelling (singletons 8 to 7 at A.W.T complete years, 37 to 36 configurations).
- A consequence the author must see: the verdict flips at A.W.T under the whole-counts p. The paper says "not detected (p 0.058)"; on the 621 dataset the same estimator gives 0.0375 (below 0.05) and the other estimator 0.007. Both 621 values say "detected at 5 %". At A.U nothing changes (not detected). The paper sentence "the difference is not detected" for A.W.T therefore does not hold for the 621 dataset at the 5 % level and has to be rewritten with the new value, or the choice of estimator stated.
- Verdict: explained (older dataset and estimator), with the verdict change at A.W.T noted above. Not small in its consequence.

## 4. "3.4 per cent" step-up in 2016 against 2.1 for aeronautics

- The thesis does not say per cent. It says "steps up by 3.4 times (interval 2.1 to 5.1) against 2.1 times for aeronautics (1.8 to 2.6)" (thesis.txt lines 2743-2744 and 4665-4666). These are factors, so the unit "per cent" is a wording error in whatever text says it; 3.4 times is a rise of 240 %.
- Definition: the level step of model (a), two lines with a free level step, break 2016, fit 2005-2022, 95 % residual-bootstrap interval (`lib/growth_models.py`, `thesis_q1.growth_models`). The turning-point jump (3.45 on 621, 3.38 on 627) is the other procedure; both round to 3.4.
- Reproduced on the 627 table with `q1_627g.py old` (frozen aircraft table, identity and figure table): eVTOL level step 3.35 (2.12 to 5.05) which prints as 3.4 (2.1 to 5.1); aeronautics 2.10 (1.77 to 2.57) which prints as 2.1 (1.8 to 2.6). Both match the paper exactly, intervals included.
- On the 621 dataset: 3.30 (2.12 to 4.89) and 2.10 (1.77 to 2.57) (`numbers_I_growth_breakpoints.csv`). The aeronautics value does not change (it does not depend on the designs). The eVTOL step moves by 0.05 (1.5 %), the upper end of the interval by 0.16, so the paper's "3.4 (2.1 to 5.1)" becomes "3.3 (2.1 to 4.9)".
- The earlier note "3.45 for families and 2.10 for aeronautics, two procedures" is not the paper's pair: the paper's pair is the level step 3.35 against 2.10, a like-for-like pair, and now 3.30 against 2.10.
- Note for the reader of the code: running `thesis_q1._calc` on the 627 table with the patent table of the 621 dataset (the table `aircraft_627.csv` alone, without the 1 750-row aircraft table) gives a break at 2017 and 1.8; that is an artefact of the missing patents, not a result (see `q1_627f.py` run in the scratchpad `dc/`).
- Verdict: explained (older dataset), small (0.05 in the factor), plus a unit wording error to correct.

## 5. 68 % and 72 %

- 68 %: thesis Table 4.1, relevance "68 of 100 sampled" simple families, 68.0 % with margin 8.9 % (thesis.txt 2530-2538, 4626). So a random sample of 100 families was judged in the thesis; the request trace statement "no random sample is documented" refers to the repository and the public dataset, where the sample file is not present (I found no file of the 100 judgements in the dataset folders, the v1 folders or the scratchpad; `scope_sample_decisions.csv` is a different sample of 99). The thesis itself compares the 68.0 % with the full-set count of in-domain plus similar patents, 1 109 of 1 639, 67.7 %. On the 621 dataset the full-set count is 1 108 of 1 639, 67.6 % (Wilson 65.3 to 69.8). All three round to 68. Difference 0.1 to 0.4 points. Verdict: explained, small.
- 72 %: not in the thesis. The thesis completeness is 60.7 % (simple family, 34 of 56), 82.1 % (46 of 56 with same-design patents) on a gold standard of 56 patents of large companies (Table 4.1; the v1 table is `eVTOL_dataset_v1_WORK/06_gold_standard_v1/gold_standard_v1.csv`: 33 same number, 8 same design, 4 extended family, 1 simple family, 10 missed). No variant of that gold standard gives 72 %. The new census gold standard of the public dataset (`eVTOL_dataset/02_gold_standard/29_gold_standard.csv`) gives 33 of 46 aircraft (71.7 %, Wilson 57.5 to 82.7) and 31 of 43 programmes (72.1 %, 57.3 to 83.3). The paper's 72 % is therefore consistent with the census, to within 0.3 points, but I cannot tell which of the two (aircraft or programmes) is meant, and nothing in the files states it. If the paper meant the thesis gold standard, the value would be 82.1 % or 60.7 %, which is not close.
- Verdict: 68 % explained (small); 72 % matched by the census within 0.3 points but the choice between 71.7 and 72.1 and the way it was drawn is open, to be stated by the author. It is a census, not a random sample, so no sampling margin applies; the Wilson interval is of the census count.

## 6. "90 % for 2023"

- The thesis has both quantities: "89 % of the 2023 designs are already visible" (the share already published at the snapshot, thesis.txt 2698-2699) and "90 % of the patents take up to three years from priority to publication" (the 90th percentile of the publication lag, 3 years, thesis.txt 2703). The paper's "90 %" is one of them: the 89.7 % rounds to 90, the 89 % of the thesis does not.
- The share published: 88.9 % with all designs of 2016-21 as the reference set (n 354, "Other regions" included; `results/2_analysis/freeze/NUMBERS_I.md` line 304, `csv/q1_filings_per_year_lag_corrected.csv`), 89.7 % with the three regions only (n 345). Reproduced with `vis627.py`: the frozen 627 table gives 88.9 % (n 354) and 89.7 % (n 345); the 621 dataset gives exactly the same 88.9 % and 89.7 %. So the difference between 88.9 and 89.7 is the reference set (all designs or three regions), not the dataset: the lags of the designs of 2016-21 are identical in both tables (0: 42, 1: 140, 2: 107, 3: 47, 4: 9). This corrects the note of `pending_part_D.md` item 11 that put 88.9 on the 627 table and 89.7 on the 621 dataset.
- p90 of the lag: 3.0 years in both tables (`vis627.py`), and the config value `publication_lag_p90_years: 3`.
- Size: 0.8 points between the two definitions of the reference set; 0.3 to 1.1 points to the paper's 90. Verdict: small; cause is a definition (reference set) and rounding, not the dataset.

## What stays open

- 72 %: which census count (aircraft 33 of 46 or programmes 31 of 43) the paper means, and the description of how it was drawn.
- 3: nothing open in the number; the paper sentence on "not detected" at A.W.T needs the author's decision (see item 3).
- The paper draft itself was not available; if it quotes values different from the thesis text, those were not compared.
