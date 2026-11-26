# Pending numbers of paper P1

Dataset `eVTOL_dataset` (621 designs), thesis seed 42. Every value has its script and file in the part where it appears. Nothing is interpreted. The status of every request and the places where the files disagree with the paper are in the first section.

## 0. Status of every request

# Request trace: every request for numbers of paper P1, where it is answered, and how far it can be trusted

Dataset `eVTOL_dataset` (621 designs, 619 with an architecture), thesis seed 42. Written 2026-11-26. Paths are relative to the repository unless they start with `eVTOL_dataset/`. Scripts are in `2_analysis/scripts/`; the notebook `2_analysis/notebooks/31_pending_numbers.ipynb` runs them in order. The assembled text is `results/2_analysis/pending_numbers/pending_numbers.md`; the same files are in `paper_figures_for_other_pc/numbers/`.

**Status words.** `done`: computed from the dataset by a script in the repository, file given. `done, differs from the paper`: computed, and the value is not the one the paper quotes (listed in the last section). `waits for the run`: needs the coding-noise runs, which were still running when this was written. `not possible`: the information is not in the files; the reason is given.

**How far each kind of number can be trusted.**
- Numbers that come straight from a table or from a thesis function called unchanged (counts, shares, Wilson intervals, band edges, percentiles) were recomputed, and several were checked a second time by hand (configurations 12, 39, 44; effective numbers 5.72, 11.32, 22.78; Gower worked example against the library to 1e-17).
- Numbers produced by a subagent were not all rechecked line by line. Items whose value disagrees with the paper (section 3 below) are the ones to read before they are used.
- The coding-noise numbers (items 1 to 4) are not final until the three runs listed in section 2 have finished.

## 1. The twenty items (prompt of 2026-11-26)

| # | request | status | where |
|---|---|---|---|
| 1 | replica count at 10 000 permutations; 1 000 replicas | waits for the run. 1 000 replicas at 10 000 permutations do not exist (about 42 h); the 1 000-replica run at 1 000 permutations is repeated with the new rule as the labelled reference | `pending_part_A.md` A1, `pending_csv/A1_replica_counts.csv`, `40_pending_block_A.py` |
| 2 | Table S7: every result, original, share kept under weights and under coding | waits for the run | `pending_csv/A2_S7_every_result.csv` |
| 3 | numbers of S5 and 4.4 (dQ below band, F three conditions, F fails share, medians, standard wings, TP decline) | waits for the run | `A3a_*.csv`, `A3b_*.csv` |
| 4 | verdict for F under replicas, both bases | waits for the run | `A4_F_verdict_*.csv` |
| 5 | rarefaction 30, 40, 50, all levels and bases; which verdicts change | done, differs from the paper (two cells change, not one) | `pending_part_B_C.md` item 5, `39_rarefaction_verdict_table.py` |
| 6 | variety threshold 70, 80, 90 % | done | item 6, `43_variety_window_tables.py` |
| 7 | share condition with 2, 3, 4 consecutive years, every level and base | done | item 7, `38_parameter_sweep.py --part window` |
| 8 | configurations at A, A·W·T, A·U and effective numbers | done, differs from the paper | item 8, `41_levels_and_last100.py` |
| 9 | new configurations in the 100 most recent designs | done, differs from the paper (4.1 against 1.6, p 0.058 not reproduced) | item 9, `41_levels_and_last100.py` |
| 10 | trends for family F alone | done, agrees with the paper | item 10, `42_family_F_trends.py` |
| 11 | Asia-Pacific 18 %; patents by priority year; the 90 % of 2023 | done; the "90 %" has two possible meanings in the code | `pending_part_D.md` item 11, `45_pending_D_items_11_12.py` |
| 12 | the 3.4 step-up of 2016 against 2.1 | done, differs from the paper (no "3.4 per cent" exists; factors from two procedures) | item 12 |
| 13 | Table S1 | done; reasons for exclusion are not written in the code | `46_pending_D_item_13_table_S1.py` |
| 14 | Table S2 | done | `47_pending_D_item_14_table_S2.py` |
| 15 | list of coding locks | done (12 locks; `05a_audit_lock_tests.py` named in a docstring is not in the repository) | `pending_part_D2.md` item 15, `55_pending_part_D2.py` |
| 16 | PatSeer queries, date, funnel | done; the count before family grouping is not stored; the search date comes from the export file | item 16 |
| 17 | how the 68 % and 72 % were drawn, with intervals | done, differs from the paper (no sample exists, both are counts over full sets) | item 17 |
| 18 | architecture mix against the VFS directory; ten mismatches | done | item 18 |
| 19 | Gower worked example | done | item 19 |
| 20 | Spearman and Holm list | done; driver and regional rows are read from the freeze files, not recomputed | `48_pending_D_item_20_spearman_holm.py` |

## 2. Coding-noise runs (new rule: list the values that break no lock, draw one at random; empty list keeps the original value)

| run | replicas | permutations | tag in `results/31_label_reliability/` | expected end (2026-11-26) |
|---|---|---|---|---|
| 15 % per value | 120 | 10 000 | `allowed_r15_p10000` | about 06:30 |
| 15 % per value, reference | 1 000 | 1 000 | `allowed_r15_p1000_n1000` | about 09:00 |
| 20 % per value | 120 | 10 000 | `allowed_r20_p10000` | about 14:00 |
| first version (redraw whole design up to 20 times), kept for the record | 120 | 10 000 | `r15_p10000` | done 2026-11-26 00:26 |

The first version is not the rule the Methods describe; its numbers are labelled as such wherever they appear. The new rule raises the share of architecture labels that change from 7.3 % to about 14 % (two test replicas, 87 of 621 designs each).

## 3. Where the files disagree with the paper (the author decides)

1. Rarefaction: balance verdicts change in two cells, not one: A·W·T all designs 2020-23 (percentile 2.7, 2.8, 2.5 at n = 30, 40, 50; below band only at 50) and A·U protected 2020-23 (3.0, 2.3, 2.6; below band only at 40).
2. Configurations: 12, 39, 44 on the whole corpus; the paper's 43 is A·U on complete years (to 2023). The effective numbers 7.3, 16.4, 29.3 are not the 2D (5.72, 11.32, 22.78); 7.3 is the 1D value at A, 16.5 and 29.6 the 1D values at the other levels.
3. The 100 most recent designs: 4.18 new configurations at A·W·T against 1.44 at random (p 0.007 or 0.0375 by the two estimators); at A·U 1.06 against 0.79. The paper's 4.1, 1.6, p 0.058 has no source in the files.
4. "3.4 per cent": the files hold factors, 3.45 for families (turning-point procedure) and 2.10 for aeronautics (level step of model a). Like-for-like: 3.30 against 2.10 (fit to 2022), 3.52 against 2.11 (fit to 2023).
5. 68 % and 72 %: no random sample is documented. 68 % is 1 108 of 1 639 families approved (Wilson 65.3 to 69.8); the completeness census gives 33 of 46 aircraft (71.7 %) and 31 of 43 programmes (72.1 %).
6. "90 % for 2023": either the p90 of the publication lag (3 years, a typed constant) or the share of 2023 designs already published (89.7 %).
7. Architecture-label change: 7.5 % in the text; 7.3 % under the first version, about 14 % under the rule of the paper.
8. Coding-noise values quoted in the text (13 to 18 %, 0.9 %, 99.7 to 100 %, 0.87 to 0.74, 73 %) come from the first run (1 000 replicas, 1 000 permutations, redraw rule) and are replaced by the new runs.



# A. Coding-noise run and weight draws (items 1-4)

# Pending numbers, block A (coding-noise run and weight draws)

Paper P1, dataset eVTOL_dataset (621 designs, 619 with an architecture), seed 42. Script `2_analysis/scripts/40_pending_block_A.py`; replica files as listed in the script docstring. Nothing is interpreted.

## A1. Replica counts

1 000 replicas at 10 000 permutations do not exist: a replica takes about 38 minutes on one core; 1 000 of them need about 42 hours on 15 workers. The 1 000-replica run at 1 000 permutations is reported next to the 10 000-permutation runs and is labelled.

| run                                                     |   replicas finished | file                                                                                                               |   permutations per band |   replica seed |   designs changed in architecture label, mean share |   min changed |   max changed |
|:--------------------------------------------------------|--------------------:|:-------------------------------------------------------------------------------------------------------------------|------------------------:|---------------:|----------------------------------------------------:|--------------:|--------------:|
| first version (redraw whole design), 15 %, 10 000 perms |                 120 | results/31_label_reliability/r15_p10000/replicas.jsonl                                                             |                   10000 |       20261118 |                                           0.0738728 |            31 |            61 |
| first version, 15 %, 1 000 perms (reference)            |                1000 | /mnt/storage_11tb/Drive_files_to_syncronize/eVTOL_dataset/07_results/71_label_reliability/reliability_replicas.csv |                    1000 |       20261118 |                                         nan         |           nan |           nan |

## A2. Table S7: every tested result, original value, share kept under weight draws and under coding replicas

Rows are the boolean results of `31B_run_replicas.py` (keys as in the replica file: 1 = variety of dimensions, 3/4 = conditions at A, A·W·T, A·U and F, 5 = trends of architecture shares, 6 = trends inside architectures, 7 = entrants, 8 = regions). `share kept` = share of replicas whose value equals the original. Weight draws change only the distance (condition 3); for the other results the weights column says 'not affected'.

| key                                                                    | original   |   share kept, weight draws | weights: how read                                                                           |   share kept, coding first version (redraw whole design), 15 %, 10 000 perms (n=120) |   Wilson low first version (redraw whole design), 15 %, 10 000 perms |   Wilson high first version (redraw whole design), 15 %, 10 000 perms |   share kept, coding first version, 15 %, 1 000 perms (reference), n=1000 |
|:-----------------------------------------------------------------------|:-----------|---------------------------:|:--------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------:|---------------------------------------------------------------------:|----------------------------------------------------------------------:|--------------------------------------------------------------------------:|
| 1 | varies (under 80 %) | number of wings (winged designs)             | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 1 | varies (under 80 %) | tail type                                    | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 1 | varies (under 80 %) | fuselage motion hover to cruise              | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.000 |                                                                0.000 |                                                                 0.031 |                                                                     0.000 |
| 1 | varies (under 80 %) | wing configuration                           | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.000 |                                                                0.000 |                                                                 0.031 |                                                                     0.000 |
| 1 | varies (under 80 %) | landing-gear type                            | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 1 | varies (under 80 %) | left-right symmetry                          | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.908 |                                                                0.843 |                                                                 0.948 |                                                                     0.936 |
| 1 | varies (under 80 %) | fuselage shape                               | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 1 | varies (under 80 %) | booms present                                | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 1 | varies (under 80 %) | propulsor units per aircraft (band)          | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 1 | varies (under 80 %) | places carrying propulsor units per aircraft | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 1 | varies (under 80 %) | propulsor enclosure (any ducted)             | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 3 | all designs | 1 share | A                                          | False      |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 3 | all designs | 1 share | A·W·T                                      | False      |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 3 | all designs | 1 share | A·U                                        | False      |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 4 | all designs | 1 share | F                                          | False      |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                0.992 |                                                                0.954 |                                                                 0.999 |                                                                     0.997 |
| 3 | all designs | 2 balance | A                                        | True       |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                0.792 |                                                                0.711 |                                                                 0.855 |                                                                     0.797 |
| 3 | all designs | 2 balance | A·W·T                                    | False      |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                0.892 |                                                                0.823 |                                                                 0.936 |                                                                     0.854 |
| 3 | all designs | 2 balance | A·U                                      | False      |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                0.975 |                                                                0.929 |                                                                 0.991 |                                                                     0.980 |
| 4 | all designs | 2 balance | F                                        | True       |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                0.967 |                                                                0.917 |                                                                 0.987 |                                                                     0.979 |
| 3 | all designs | 3 disparity | A                                      | True       |                      0.693 | disparity: draws with dQ below band (test1_summary.csv)                                     |                                                                                0.150 |                                                                0.097 |                                                                 0.225 |                                                                     0.143 |
| 3 | all designs | 3 disparity | A·W·T                                  | True       |                      0.780 | disparity: draws with dQ below band (test1_summary.csv)                                     |                                                                                0.108 |                                                                0.064 |                                                                 0.177 |                                                                     0.136 |
| 3 | all designs | 3 disparity | A·U                                    | True       |                      0.790 | disparity: draws with dQ below band (test1_summary.csv)                                     |                                                                                0.108 |                                                                0.064 |                                                                 0.177 |                                                                     0.129 |
| 4 | all designs | 3 disparity | F                                      | True       |                      0.693 | disparity: draws with dQ below band (test1_summary.csv, F read on level L1)                 |                                                                                0.150 |                                                                0.097 |                                                                 0.225 |                                                                     0.143 |
| 3 | all designs | all three | A                                        | False      |                    nan     | not computed (weights change dQ only; combination of conditions not recomputed under draws) |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 3 | all designs | all three | A·W·T                                    | False      |                    nan     | not computed (weights change dQ only; combination of conditions not recomputed under draws) |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 3 | all designs | all three | A·U                                      | False      |                    nan     | not computed (weights change dQ only; combination of conditions not recomputed under draws) |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 4 | all designs | all three | F                                        | False      |                    nan     | not computed (weights change dQ only; combination of conditions not recomputed under draws) |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     0.999 |
| 3 | actively protected | 1 share | A                                   | False      |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 3 | actively protected | 1 share | A·W·T                               | False      |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 3 | actively protected | 1 share | A·U                                 | False      |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 4 | actively protected | 1 share | F                                   | True       |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                0.033 |                                                                0.013 |                                                                 0.083 |                                                                     0.035 |
| 3 | actively protected | 2 balance | A                                 | True       |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                0.767 |                                                                0.683 |                                                                 0.833 |                                                                     0.778 |
| 3 | actively protected | 2 balance | A·W·T                             | True       |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                0.200 |                                                                0.138 |                                                                 0.280 |                                                                     0.193 |
| 3 | actively protected | 2 balance | A·U                               | True       |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                0.125 |                                                                0.077 |                                                                 0.196 |                                                                     0.174 |
| 4 | actively protected | 2 balance | F                                 | True       |                      1.000 | not affected: the condition does not use the distance                                       |                                                                                0.983 |                                                                0.941 |                                                                 0.995 |                                                                     0.964 |
| 3 | actively protected | 3 disparity | A                               | True       |                      0.739 | disparity: draws with dQ below band (test1_summary.csv)                                     |                                                                                0.225 |                                                                0.159 |                                                                 0.308 |                                                                     0.180 |
| 3 | actively protected | 3 disparity | A·W·T                           | True       |                      0.829 | disparity: draws with dQ below band (test1_summary.csv)                                     |                                                                                0.175 |                                                                0.117 |                                                                 0.253 |                                                                     0.184 |
| 3 | actively protected | 3 disparity | A·U                             | True       |                      0.841 | disparity: draws with dQ below band (test1_summary.csv)                                     |                                                                                0.167 |                                                                0.111 |                                                                 0.243 |                                                                     0.177 |
| 4 | actively protected | 3 disparity | F                               | True       |                      0.739 | disparity: draws with dQ below band (test1_summary.csv, F read on level L1)                 |                                                                                0.225 |                                                                0.159 |                                                                 0.308 |                                                                     0.180 |
| 3 | actively protected | all three | A                                 | False      |                    nan     | not computed (weights change dQ only; combination of conditions not recomputed under draws) |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 3 | actively protected | all three | A·W·T                             | False      |                    nan     | not computed (weights change dQ only; combination of conditions not recomputed under draws) |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 3 | actively protected | all three | A·U                               | False      |                    nan     | not computed (weights change dQ only; combination of conditions not recomputed under draws) |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 4 | actively protected | all three | F                                 | True       |                    nan     | not computed (weights change dQ only; combination of conditions not recomputed under draws) |                                                                                0.000 |                                                                0.000 |                                                                 0.031 |                                                                     0.009 |
| 4 | all designs | F above 50 % in 2020                                 | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.992 |                                                                0.954 |                                                                 0.999 |                                                                     0.996 |
| 4 | all designs | F above 50 % in 2021                                 | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.383 |                                                                0.301 |                                                                 0.473 |                                                                     0.375 |
| 4 | actively protected | F above 50 % in 2020                          | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.050 |                                                                0.023 |                                                                 0.105 |                                                                     0.046 |
| 4 | actively protected | F above 50 % in 2021                          | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.667 |                                                                0.578 |                                                                 0.745 |                                                                     0.693 |
| 8 | regions differ 2020-23 (p < 0.05) | all assignees                  | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.992 |                                                                0.954 |                                                                 0.999 |                                                                     0.984 |
| 8 | regions differ 2020-23 (p < 0.05) | without the largest assignee   | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     0.994 |
| 5 | rises (rho > 0, Holm p < 0.05) | SLC                               | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 5 | falls (rho < 0, Holm p < 0.05) | SLC                               | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 5 | rises (rho > 0, Holm p < 0.05) | TP                                | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 5 | falls (rho < 0, Holm p < 0.05) | TP                                | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.742 |                                                                0.657 |                                                                 0.812 |                                                                     0.732 |
| 5 | rises (rho > 0, Holm p < 0.05) | CVT                               | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 5 | falls (rho < 0, Holm p < 0.05) | CVT                               | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 5 | rises (rho > 0, Holm p < 0.05) | TW                                | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 5 | falls (rho < 0, Holm p < 0.05) | TW                                | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 5 | rises (rho > 0, Holm p < 0.05) | MR                                | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.992 |                                                                0.954 |                                                                 0.999 |                                                                     0.991 |
| 5 | falls (rho < 0, Holm p < 0.05) | MR                                | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 5 | rises (rho > 0, Holm p < 0.05) | TF                                | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.917 |                                                                0.853 |                                                                 0.954 |                                                                     1.000 |
| 5 | falls (rho < 0, Holm p < 0.05) | TF                                | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.917 |                                                                0.853 |                                                                 0.954 |                                                                     1.000 |
| 5 | rises (rho > 0, Holm p < 0.05) | PTC                               | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.750 |                                                                0.666 |                                                                 0.819 |                                                                     0.995 |
| 5 | falls (rho < 0, Holm p < 0.05) | PTC                               | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.758 |                                                                0.674 |                                                                 0.826 |                                                                     1.000 |
| 6 | significant (Holm p < 0.05) | propulsors on booms in CVT           | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.808 |                                                                0.729 |                                                                 0.869 |                                                                     0.798 |
| 6 | significant (Holm p < 0.05) | ducted in CVT                        | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.958 |                                                                0.906 |                                                                 0.982 |                                                                     0.958 |
| 6 | significant (Holm p < 0.05) | propulsors in TP                     | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.983 |                                                                0.941 |                                                                 0.995 |                                                                     0.990 |
| 6 | significant (Holm p < 0.05) | propulsors in CVT                    | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.467 |                                                                0.380 |                                                                 0.556 |                                                                     0.406 |
| 7 | differ (p < 0.05) | 2016-19                                        | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.925 |                                                                0.864 |                                                                 0.960 |                                                                     0.908 |
| 7 | differ without the largest (p < 0.05) | 2016-19                    | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                1.000 |                                                                0.969 |                                                                 1.000 |                                                                     1.000 |
| 7 | differ (p < 0.05) | 2020-23                                        | True       |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.900 |                                                                0.833 |                                                                 0.942 |                                                                     0.899 |
| 7 | differ without the largest (p < 0.05) | 2020-23                    | False      |                      1.000 | not affected: the result does not use the distance                                          |                                                                                0.958 |                                                                0.906 |                                                                 0.982 |                                                                     0.967 |

## A3. Numbers for S5 and 4.4, coding noise first version (redraw whole design), 15 %, 10 000 perms, 120 replicas

Disparity (condition 3) per level and base:

| base               | level   |   share of replicas with dQ below band in 2020-23 |   median dQ under noise |   original dQ |   median band low edge under noise |   original band low edge |   replicas |
|:-------------------|:--------|--------------------------------------------------:|------------------------:|--------------:|-----------------------------------:|-------------------------:|-----------:|
| all designs        | A       |                                            0.1500 |                 -0.0096 |       -0.0257 |                            -0.0176 |                  -0.0218 |        120 |
| all designs        | A·W·T   |                                            0.1083 |                 -0.0082 |       -0.0277 |                            -0.0174 |                  -0.0213 |        120 |
| all designs        | A·U     |                                            0.1083 |                 -0.0082 |       -0.0277 |                            -0.0173 |                  -0.0212 |        120 |
| all designs        | F       |                                            0.1500 |                 -0.0096 |       -0.0257 |                            -0.0176 |                  -0.0218 |        120 |
| actively protected | A       |                                            0.2250 |                 -0.0118 |       -0.0287 |                            -0.0192 |                  -0.0234 |        120 |
| actively protected | A·W·T   |                                            0.1750 |                 -0.0113 |       -0.0313 |                            -0.0190 |                  -0.0230 |        120 |
| actively protected | A·U     |                                            0.1667 |                 -0.0113 |       -0.0313 |                            -0.0190 |                  -0.0230 |        120 |
| actively protected | F       |                                            0.2250 |                 -0.0118 |       -0.0287 |                            -0.0192 |                  -0.0234 |        120 |

| quantity                                                                               | value              | replica-file key                                 |   replicas |
|:---------------------------------------------------------------------------------------|:-------------------|:-------------------------------------------------|-----------:|
| F meets all three conditions, protected designs: share of replicas                     | 0.0                | 4 | actively protected | all three | F           |        120 |
| F fails the share condition, all designs: share of replicas                            | 0.9916666666666667 | 4 | all designs | 1 share | F                    |        120 |
| F share in 2020, protected designs: median over replicas                               | 0.444              | 4 | actively protected | F share 2020            |        120 |
| F share above 50 % in 2020, protected designs: share of replicas                       | 0.05               | 4 | actively protected | F above 50 % in 2020    |        120 |
| Tilt Propulsor share falls with Holm p < 0.05: share of replicas                       | 0.7416666666666667 | 5 | falls (rho < 0, Holm p < 0.05) | TP          |        120 |
| Tilt Propulsor share falls: original value                                             | True               | 5 | falls (rho < 0, Holm p < 0.05) | TP          |        120 |
| standard wings (wing configuration), leading share: original                           | 0.87               | 1 | top share | wing configuration               |        120 |
| standard wings (wing configuration), leading share: median under noise                 | 0.75               | 1 | top share | wing configuration               |        120 |
| standard wings (wing configuration), leading share: 5th to 95th percentile under noise | 0.72 to 0.77       | 1 | top share | wing configuration               |        120 |
| hover-to-cruise motion, leading share: original                                        | 0.85               | 1 | top share | fuselage motion hover to cruise  |        120 |
| hover-to-cruise motion, leading share: median under noise                              | 0.72               | 1 | top share | fuselage motion hover to cruise  |        120 |
| hover-to-cruise motion, leading share: 5th to 95th percentile under noise              | 0.70 to 0.74       | 1 | top share | fuselage motion hover to cruise  |        120 |
| ducted, leading share: original                                                        | 0.63               | 1 | top share | propulsor enclosure (any ducted) |        120 |
| ducted, leading share: median under noise                                              | 0.53               | 1 | top share | propulsor enclosure (any ducted) |        120 |
| ducted, leading share: 5th to 95th percentile under noise                              | 0.51 to 0.55       | 1 | top share | propulsor enclosure (any ducted) |        120 |

## A4. Verdict for family F under coding replicas (first version (redraw whole design), 15 %, 10 000 perms, 120 replicas)

| base               | condition   | original   |   share of replicas where it is met |   share keeping the original |   Wilson low |   Wilson high |   replicas |
|:-------------------|:------------|:-----------|------------------------------------:|-----------------------------:|-------------:|--------------:|-----------:|
| all designs        | 1 share     | False      |                               0.008 |                        0.992 |        0.954 |         0.999 |        120 |
| all designs        | 2 balance   | True       |                               0.967 |                        0.967 |        0.917 |         0.987 |        120 |
| all designs        | 3 disparity | True       |                               0.150 |                        0.150 |        0.097 |         0.225 |        120 |
| all designs        | all three   | False      |                               0.000 |                        1.000 |        0.969 |         1.000 |        120 |
| actively protected | 1 share     | True       |                               0.033 |                        0.033 |        0.013 |         0.083 |        120 |
| actively protected | 2 balance   | True       |                               0.983 |                        0.983 |        0.941 |         0.995 |        120 |
| actively protected | 3 disparity | True       |                               0.225 |                        0.225 |        0.159 |         0.308 |        120 |
| actively protected | all three   | True       |                               0.000 |                        0.000 |        0.000 |         0.031 |        120 |



# B and C. Parameter sweeps and numbers quoted in the article (items 5-10)

# Pending numbers, part B and C (items 5 to 10)

Scripts in `REPO/2_analysis/scripts` (REPO = evtol-design-space-analysis-tools), run with `EVTOL_DATASET=/mnt/storage_11tb/Drive_files_to_syncronize/eVTOL_dataset PYTHONPATH=REPO/2_analysis/src python3 <script>` from REPO. Seed 42; thesis functions unchanged. CSV files in `numbers/pending_csv/`. Values only, no interpretation.

## 5. Rarefaction at 30, 40, 50

Runs: `S5_rarefaction_30.csv` and `S5_rarefaction_50.csv` (supplementary_csv) are complete: 40 rows each (4 levels x 5 cohorts x 2 bases), 10 000 permutations, no empty percentile; produced by `38_parameter_sweep.py --part rare --n 30|50` (not rerun). The 40 values are `results/2_analysis/family_F/percentiles_balance.csv` (10 000 permutations, seed 42, 40 rows). Table built by `39_rarefaction_verdict_table.py` -> `pending_csv/5_rarefaction_verdict_30_40_50.csv` (with D2 and band edges at each n), `5_rarefaction_verdict_changes.csv`. Definition: below = observed rarefied D2 under the 2.5th percentile of the permutation band; pct = share of shuffles at or below the observed D2. Protected cohorts <= 2011 (18 designs) and 2012-15 (32) are rarefied to their own size at n = 40 and 50 (and the 18-design one at 30).

| level   | base               | cohort            |   pct 30 | below 30   |   pct 40 | below 40   |   pct 50 | below 50   |
|:--------|:-------------------|:------------------|---------:|:-----------|---------:|:-----------|---------:|:-----------|
| A       | all designs        | <= 2011           |     24   | False      |     24   | False      |     24.2 | False      |
| A       | all designs        | 2012-15           |     32.5 | False      |     29.7 | False      |     29.2 | False      |
| A       | all designs        | 2016-19           |     98.5 | False      |     98.9 | False      |     99   | False      |
| A       | all designs        | 2020-23           |      0.5 | True       |      0.2 | True       |      0.2 | True       |
| A       | all designs        | 2024-26 (partial) |     71.9 | False      |     73.2 | False      |     73.1 | False      |
| A.W.T   | all designs        | <= 2011           |     15.6 | False      |     16.7 | False      |     15.7 | False      |
| A.W.T   | all designs        | 2012-15           |     13.9 | False      |     13.3 | False      |     12.9 | False      |
| A.W.T   | all designs        | 2016-19           |     97.6 | False      |     97.4 | False      |     98.3 | False      |
| A.W.T   | all designs        | 2020-23           |      2.7 | False      |      2.8 | False      |      2.5 | True       |
| A.W.T   | all designs        | 2024-26 (partial) |     54.7 | False      |     57.8 | False      |     55.9 | False      |
| A.U     | all designs        | <= 2011           |      1   | True       |      0.9 | True       |      0.8 | True       |
| A.U     | all designs        | 2012-15           |      0.1 | True       |      0.1 | True       |      0.1 | True       |
| A.U     | all designs        | 2016-19           |     85.5 | False      |     84.4 | False      |     86.4 | False      |
| A.U     | all designs        | 2020-23           |      8.8 | False      |      9.5 | False      |     11.5 | False      |
| A.U     | all designs        | 2024-26 (partial) |     55.6 | False      |     56.6 | False      |     57.4 | False      |
| F       | all designs        | <= 2011           |     48.5 | False      |     49.7 | False      |     50.6 | False      |
| F       | all designs        | 2012-15           |     85.3 | False      |     84.1 | False      |     84.4 | False      |
| F       | all designs        | 2016-19           |     98.8 | False      |     98.9 | False      |     99.3 | False      |
| F       | all designs        | 2020-23           |      0   | True       |      0   | True       |      0   | True       |
| F       | all designs        | 2024-26 (partial) |     51.2 | False      |     51.5 | False      |     50.6 | False      |
| A       | actively protected | <= 2011           |      2.8 | False      |      2.8 | False      |      2.8 | False      |
| A       | actively protected | 2012-15           |      6.5 | False      |      6.7 | False      |      6.7 | False      |
| A       | actively protected | 2016-19           |     99.6 | False      |     99.7 | False      |     99.8 | False      |
| A       | actively protected | 2020-23           |      0.3 | True       |      0.2 | True       |      0.2 | True       |
| A       | actively protected | 2024-26 (partial) |     76.7 | False      |     76.8 | False      |     76.1 | False      |
| A.W.T   | actively protected | <= 2011           |      0.7 | True       |      0.7 | True       |      0.7 | True       |
| A.W.T   | actively protected | 2012-15           |      3.5 | False      |      3.7 | False      |      3.7 | False      |
| A.W.T   | actively protected | 2016-19           |     99.4 | False      |     99.6 | False      |     99.6 | False      |
| A.W.T   | actively protected | 2020-23           |      0.7 | True       |      0.8 | True       |      0.6 | True       |
| A.W.T   | actively protected | 2024-26 (partial) |     48.5 | False      |     51.4 | False      |     51.4 | False      |
| A.U     | actively protected | <= 2011           |      0.3 | True       |      0.3 | True       |      0.3 | True       |
| A.U     | actively protected | 2012-15           |      0   | True       |      0   | True       |      0   | True       |
| A.U     | actively protected | 2016-19           |     82.8 | False      |     86.6 | False      |     86.6 | False      |
| A.U     | actively protected | 2020-23           |      3   | False      |      2.3 | True       |      2.6 | False      |
| A.U     | actively protected | 2024-26 (partial) |     61.4 | False      |     62.2 | False      |     61.3 | False      |
| F       | actively protected | <= 2011           |     16   | False      |     16   | False      |     16   | False      |
| F       | actively protected | 2012-15           |     42.4 | False      |     43.4 | False      |     43.4 | False      |
| F       | actively protected | 2016-19           |     99.9 | False      |     99.9 | False      |    100   | False      |
| F       | actively protected | 2020-23           |      0   | True       |      0   | True       |      0   | True       |
| F       | actively protected | 2024-26 (partial) |     53.7 | False      |     52   | False      |     49.8 | False      |

Verdicts that change among 30, 40, 50 (2 of 40 cells):

| level | base | cohort | pct 30 / 40 / 50 | below 30 / 40 / 50 |
|---|---|---|---|---|
| A.W.T | all designs | 2020-23 | 2.7 / 2.8 / 2.5 | False / False / True |
| A.U | actively protected | 2020-23 | 3.0 / 2.3 / 2.6 | False / True / False |

Check of the paper claim ("only balance of A.W.T in 2020-23 moves"): A.W.T, all designs, 2020-23 does move (below band only at 50; percentiles 2.7, 2.8, 2.5, edge cases around 2.5). It is NOT the only one: A.U, actively protected, 2020-23 is below band at 40 (percentile 2.3) but not at 30 (3.0) or 50 (2.6). Against the default 40, the change at 30 is A.U protected 2020-23 (below -> not below); at 50 it is A.W.T all 2020-23 (not below -> below) and A.U protected 2020-23 (below -> not below). All other 38 cells have the same verdict at 30, 40 and 50. DISAGREEMENT with the paper claim: a second cell moves.

## 6. Variety threshold 70 / 80 / 90 %

`38_parameter_sweep.py --part variety` (S5_variety_threshold.csv, S5_variety_top_shares.csv); names split by `43_variety_window_tables.py` -> `pending_csv/6_variety_settled_vs_varying.csv`. Definition: a dimension of the 11 of `frames.selected_fields` varies when its leading option holds under the threshold of the designs that answer it; settled otherwise. Counts: varying 8 / 8 / 10 at 70 / 80 / 90 %.

| dimension                                    | 0.7     | 0.8     | 0.9     |   answered |   leading_share |
|:---------------------------------------------|:--------|:--------|:--------|-----------:|----------------:|
| booms present                                | varies  | varies  | varies  |        621 |            0.54 |
| fuselage motion hover to cruise              | settled | settled | varies  |        596 |            0.85 |
| fuselage shape                               | varies  | varies  | varies  |        597 |            0.64 |
| landing-gear type                            | varies  | varies  | varies  |        596 |            0.68 |
| left-right symmetry                          | settled | settled | settled |        621 |            0.95 |
| number of wings (winged designs)             | varies  | varies  | varies  |        542 |            0.65 |
| places carrying propulsor units per aircraft | varies  | varies  | varies  |        589 |            0.48 |
| propulsor enclosure (any ducted)             | varies  | varies  | varies  |        589 |            0.63 |
| propulsor units per aircraft (band)          | varies  | varies  | varies  |        589 |            0.23 |
| tail type                                    | varies  | varies  | varies  |        594 |            0.29 |
| wing configuration                           | settled | settled | varies  |        537 |            0.87 |

Settled, 70 % and 80 %: fuselage motion hover to cruise (85 %), wing configuration (87 %), left-right symmetry (95 %). Settled at 90 %: left-right symmetry only. Varying at 70 and 80 %: number of wings (winged designs), tail type, landing-gear type, fuselage shape, booms present, propulsor units per aircraft (band), places carrying propulsor units per aircraft, propulsor enclosure (any ducted). At 90 % the same eight vary plus fuselage motion hover to cruise and wing configuration. (Leading share of landing-gear type 68 %: under 70 % too.)

## 7. Condition 1 (share above 50 %) with 2, 3, 4 consecutive years, every level and base

The existing `S5_share_window.csv` already holds all four levels (L1 = A, L2 = A.W.T, L3 = A.U, F), both bases, k = 2, 3, 4 (24 rows), from `38_parameter_sweep.py --part window`; it was not limited to L1 and F. Relabelled copy `pending_csv/7_share_window_all_levels.csv` (`43_variety_window_tables.py`). Definition: years read = priority years with 20 or more designs (9 all designs, 8 protected); condition 1 met when k consecutive read years are each above 50 % for the leading configuration.

| level   | base               |   consecutive years required |   years read | years above 50 %   | years in which condition 1 is met   | condition 1 met   |
|:--------|:-------------------|-----------------------------:|-------------:|:-------------------|:------------------------------------|:------------------|
| A       | all designs        |                            2 |            9 |                    |                                     | False             |
| A       | all designs        |                            3 |            9 |                    |                                     | False             |
| A       | all designs        |                            4 |            9 |                    |                                     | False             |
| A       | actively protected |                            2 |            8 |                    |                                     | False             |
| A       | actively protected |                            3 |            8 |                    |                                     | False             |
| A       | actively protected |                            4 |            8 |                    |                                     | False             |
| A.U     | all designs        |                            2 |            9 |                    |                                     | False             |
| A.U     | all designs        |                            3 |            9 |                    |                                     | False             |
| A.U     | all designs        |                            4 |            9 |                    |                                     | False             |
| A.U     | actively protected |                            2 |            8 |                    |                                     | False             |
| A.U     | actively protected |                            3 |            8 |                    |                                     | False             |
| A.U     | actively protected |                            4 |            8 |                    |                                     | False             |
| A.W.T   | all designs        |                            2 |            9 |                    |                                     | False             |
| A.W.T   | all designs        |                            3 |            9 |                    |                                     | False             |
| A.W.T   | all designs        |                            4 |            9 |                    |                                     | False             |
| A.W.T   | actively protected |                            2 |            8 |                    |                                     | False             |
| A.W.T   | actively protected |                            3 |            8 |                    |                                     | False             |
| A.W.T   | actively protected |                            4 |            8 |                    |                                     | False             |
| F       | all designs        |                            2 |            9 | 2021               |                                     | False             |
| F       | all designs        |                            3 |            9 | 2021               |                                     | False             |
| F       | all designs        |                            4 |            9 | 2021               |                                     | False             |
| F       | actively protected |                            2 |            8 | 2020, 2021         | 2020, 2021                          | True              |
| F       | actively protected |                            3 |            8 | 2020, 2021         |                                     | False             |
| F       | actively protected |                            4 |            8 | 2020, 2021         |                                     | False             |

At A, A.W.T and A.U no read year is above 50 % on either base (empty list), so the verdict is False for every k. F: 2021 alone (all designs); 2020 and 2021 (protected); met only at k = 2 and only on the protected base.

## 8. Configurations and effective number at A, A.W.T, A.U

Script `41_levels_and_last100.py` -> `pending_csv/8_levels_configurations_2D.csv`, `8b_configurations_complete_years.csv`. Function `frames.archetype_levels_table` (whole corpus, all years); the discovery set uses `frames.discovery_inputs` (priority year up to 2023).

Whole corpus (621 designs; a design without a key at a level is left out):

| level   |   aircraft |   left out |   archetypes |   singletons |   effective number ¹D |   effective number ²D |   largest share |
|:--------|-----------:|-----------:|-------------:|-------------:|----------------------:|----------------------:|----------------:|
| A       |        619 |          0 |           12 |            0 |                   7.3 |                   5.7 |           0.258 |
| A.U     |        618 |          1 |           44 |            4 |                  29.6 |                  22.8 |           0.099 |
| A.W.T   |        617 |          2 |           39 |           10 |                  16.5 |                  11.3 |           0.162 |

Complete years only (priority year <= 2023; the set of the discovery test):

| level   | base                                   |   designs |   configurations |   singletons |    1D |    2D |
|:--------|:---------------------------------------|----------:|-----------------:|-------------:|------:|------:|
| A       | complete years (priority year <= 2023) |       564 |               12 |            0 |  7.27 |  5.71 |
| A.U     | complete years (priority year <= 2023) |       563 |               43 |            4 | 29.01 | 21.98 |
| A.W.T   | complete years (priority year <= 2023) |       563 |               36 |            7 | 16.32 | 11.28 |

Which count is right: whole corpus = 12, 39, 44 (`B6c_configurations_per_level.csv`, the thesis table `q7_levels_of_description.csv` and this run agree). The article's 12, 39, 43 mixes two sets: 43 is the A.U count on the complete years (<= 2023, 563 designs; A.W.T is 36 there), and 39 is the A.W.T whole-corpus count (and also the Chao1 estimate on complete years, 39.0). So "44" is the whole-corpus A.U count and "43" the complete-years count; they differ by one configuration present only in 2024-26. Singletons: A.W.T 10, A.U 4 (whole corpus); missing key: 2 designs at A.W.T, 1 at A.U, 2 at A (no architecture) -> 617, 618, 619 designs.

Effective numbers: article "7.3, 16.4, 29.3" called 2D. Computed ²D (1 / sum p^2) is 5.7, 11.3, 22.8 (whole corpus) and 5.71, 11.28, 21.98 (complete years). The effective number ¹D is 7.3, 16.5, 29.6 (whole corpus; also in the thesis table `q7_levels_of_description.csv`) and 7.27, 16.32, 29.01 (complete years). DISAGREEMENT: only 7.3 reproduces (as ¹D); 16.4 and 29.3 match neither set (nearest 16.5 / 29.6, or 16.32 / 29.01), and ²D is a different quantity.

## 9. New configurations in the last 100 designs against random order

Code: `lib/diversity.py` `discovery_tail_band`, `viz/frames.py` `discovery_inputs` and `discovery_estimators`, called as in `thesis_q6._data` and `thesis_latex_part2.tab_discovery_last100_band`: complete years (priority year <= 2023), 1 000 date orderings (ties shuffled), 10 000 random orders, tail 100, seed 42. Script `41_levels_and_last100.py` -> `9_last100_estimators.csv`, `9_last100_band.csv`.

| level   |   aircraft |   archetypes observed |   seen once (f1) |   Chao1 |   new in the last 100 aircraft |   new in the last 100, random order |   date order vs random, last tail |
|:--------|-----------:|----------------------:|-----------------:|--------:|-------------------------------:|------------------------------------:|----------------------------------:|
| A       |        564 |                    12 |                0 |      12 |                           0    |                                0    |                              0    |
| A.U     |        563 |                    43 |                4 |      45 |                           1.06 |                                0.79 |                              0.27 |
| A.W.T   |        563 |                    36 |                7 |      39 |                           4.18 |                                1.44 |                              2.74 |

| level   |   designs |   date mean |   date 2.5 % |   date 97.5 % |   random mean (exact) |   random mean (shuffles) |   random 95th |   random 99th |   random max |   p (share >= date mean) |   p (whole counts) |
|:--------|----------:|------------:|-------------:|--------------:|----------------------:|-------------------------:|--------------:|--------------:|-------------:|-------------------------:|-------------------:|
| A       |       564 |       0     |            0 |             0 |           0.000968325 |                   0.0006 |             0 |             0 |            1 |                   1      |          1         |
| A.U     |       563 |       1.064 |            1 |             2 |           0.787246    |                   0.7679 |             2 |             3 |            5 |                   0.1701 |          0.543938  |
| A.W.T   |       563 |       4.182 |            4 |             5 |           1.44493     |                   1.4508 |             3 |             4 |            6 |                   0.007  |          0.0374605 |

Article: 4.1 against 1.6, p = 0.058 at A.W.T. DISAGREEMENT: the thesis code at seed 42 gives 4.18 against 1.44 (exact random expectation; shuffle mean 1.45), p = 0.007 (share of shuffles >= date mean) or 0.0375 (whole counts averaged over the date orderings). No p of 0.058 and no random mean of 1.6 appears. A.U: 1.06 against 0.79, p = 0.170 / 0.544. These values equal the older thesis file `q6_discovery_last100_band.csv` (same numbers), so the article values do not come from this code on this set. Diagnostic (no year cut, 617 / 618 designs, `9b_last100_band_all_years_diagnostic.csv`): A.W.T 4.96 against 1.79, p 0.022 / 0.0245; A.U 1.00 against 0.74, p 0.548; also not 4.1 / 1.6 / 0.058. Source of 4.1 / 1.6 / 0.058: not found.

## 10. Trends inside family F alone

F = `frames.family_flags` + `family_mask` (Lift + Cruise, or CVT with a tilting propulsor set and no tilting wing panel): 241 designs (<= 2011: 18, 2012-15: 13, 2016-19: 70, 2020-23: 117, 2024-26: 23).

The article's dQ values are NOT Spearman trends: they come from `3_robustness/32_weight_sensitivity/src/p1_tests.py` (test 2: designs = F only, shuffles move the cohort labels among the F designs, 10 000 shuffles, seed 42, w15 weights with architecture weight 0), results in `eVTOL_dataset/07_results/72_weight_sensitivity/test2_*.csv` (written 22 Nov 2026 with `ws.PERMS = 10000`; F counts 70 and 117 match the present dataset). Not rerun (it would overwrite those dataset files); copied to `pending_csv/10c_*.csv` by `42_family_F_trends.py`.

dQ inside F, baseline (architecture weight 0), reference = the two earliest cohorts (31 F designs):

| cohort | F designs | dQ | band lower edge (10 000) | margin | below band |
|---|---|---|---|---|---|
| 2016-19 | 70 | +0.0453 | -0.0345 | -0.0798 | False |
| 2020-23 | 117 | +0.0098 | -0.0272 | -0.0371 | False |
| 2020-23 against 2016-19 (since the peak) | 70 and 117 | -0.0354 | -0.0392 | -0.0037 | False |

Article: +0.045, +0.010, -0.035: AGREES (+0.0453, +0.0098, and -0.0354 as the since-peak dQ; -0.035 is also the 2016-19 band edge, -0.0345, so the third value is read as the since-peak dQ, edge -0.0392). Test 2's 1000 weight draws: share below band 0 of 1000 in both cohorts.

Share of CVT* inside F by cohort (`10b_F_cvt_share_by_cohort.csv`, also `test2_explore_slc_cvt.csv`): <= 2011 27.8 % (5 of 18), 2012-15 30.8 % (4 of 13), 2016-19 31.4 % (22 of 70), 2020-23 35.9 % (42 of 117), 2024-26 34.8 % (8 of 23). Article 31 % to 36 %: AGREES (31.4 % to 35.9 %). Spearman of the CVT* indicator inside F on priority year (`drivers.trend_test`, complete years, 218 designs): rho 0.06, p 0.396, flat.

Per-dimension dQ inside F, architecture weight 0 (`10c_dQ_inside_F_per_dimension.csv`, one dimension at weight, same band): no dimension below its band in 2016-19 or 2020-23.

| dimension                  |   2016-19: dQ |   2016-19: band edge | 2016-19: dQ below band   |   2020-23: dQ |   2020-23: band edge | 2020-23: dQ below band   |
|:---------------------------|--------------:|---------------------:|:-------------------------|--------------:|---------------------:|:-------------------------|
| Architecture               |        0.0174 |              -0.0923 | False                    |        0.0466 |              -0.0786 | False                    |
| Fuselage Shape             |       -0.1011 |              -0.1948 | False                    |       -0.0992 |              -0.1678 | False                    |
| Boom count                 |        0.0375 |              -0.0667 | False                    |        0.0168 |              -0.058  | False                    |
| Fuselage Kinematics        |        0.082  |              -0.0988 | False                    |        0      |              -0.1065 | False                    |
| Wing count                 |        0.0719 |              -0.0715 | False                    |        0.0304 |              -0.0661 | False                    |
| Wing Architecture          |        0.2365 |              -0.2095 | False                    |        0.0431 |              -0.1976 | False                    |
| Vertical Position          |       -0.0412 |              -0.1388 | False                    |       -0.0273 |              -0.122  | False                    |
| Longitudinal Position      |        0.0424 |              -0.1841 | False                    |        0.0321 |              -0.1617 | False                    |
| Planform                   |        0.0706 |              -0.0964 | False                    |        0.0483 |              -0.0796 | False                    |
| Empennage Type             |        0.1548 |              -0.0132 | False                    |        0.1635 |              -0.0024 | False                    |
| Propulsor band             |       -0.0068 |              -0.0676 | False                    |       -0.0584 |              -0.0602 | False                    |
| Tilt share                 |        0.0534 |              -0.1006 | False                    |        0.0938 |              -0.0936 | False                    |
| Propulsor Enclosure        |       -0.0675 |              -0.1217 | False                    |       -0.058  |              -0.0989 | False                    |
| Tractor/Pusher Arrangement |        0.1028 |              -0.1892 | False                    |       -0.0418 |              -0.1831 | False                    |
| Mount locations            |        0.0323 |              -0.0379 | False                    |        0.023  |              -0.0295 | False                    |

Spearman trace trends inside F (`10a_F_trace_trends.csv`): thesis `drivers.trace_drift` / `trace_trends` called unchanged on the trace frame of the 241 F designs (topType relabelled "F"); Spearman on priority year, complete years, scipy two-sided p (the thesis uses no permutation for these); Holm over the 17 traces computed in the script (not `q6._with_holm`).

| trace                                     |   aircraft | first window   |   first value |   2020-23 value |   rho |      p |   p_holm | movement   |
|:------------------------------------------|-----------:|:---------------|--------------:|----------------:|------:|-------:|---------:|:-----------|
| tilting joint groups                      |        218 | <= 2011        |          0    |            0    |  0.09 | 0.1695 |   1      | flat       |
| fuselage kinematics not fixed             |        218 | <= 2011        |          0    |            0    | -0.09 | 0.2106 |   1      | flat       |
| a propulsor retracts or folds its blades  |        218 | <= 2011        |          0.06 |            0.09 | -0.08 | 0.2211 |   1      | flat       |
| booms stow                                |        126 | <= 2011        |          0    |            0.04 |  0.02 | 0.8364 |   1      | flat       |
| propulsive units                          |        218 | <= 2011        |          5.5  |            7    |  0.13 | 0.0581 |   0.9296 | flat       |
| units carried on booms                    |        218 | <= 2011        |          0.5  |            0.6  |  0.11 | 0.1166 |   1      | flat       |
| stations carrying units                   |        218 | <= 2011        |          2    |            2    |  0.03 | 0.6374 |   1      | flat       |
| booms present                             |        218 | <= 2011        |          0.56 |            0.6  |  0.09 | 0.1769 |   1      | flat       |
| wing units at the leading edge            |        113 | <= 2011        |          0.22 |            0.56 |  0.12 | 0.2137 |   1      | flat       |
| a pusher unit                             |        218 | <= 2011        |          0.44 |            0.36 |  0    | 1      |   1      | flat       |
| two or more wing panels                   |        218 | <= 2011        |          0.39 |            0.33 |  0.06 | 0.3427 |   1      | flat       |
| swept or delta main wing                  |        218 | <= 2011        |          0.61 |            0.38 | -0.11 | 0.1082 |   1      | flat       |
| no tail surface                           |        218 | <= 2011        |          0.56 |            0.17 | -0.17 | 0.0096 |   0.1637 | falls      |
| a ducted unit                             |        218 | <= 2011        |          0.5  |            0.42 | -0.03 | 0.6372 |   1      | flat       |
| ground contact drawn                      |        218 | <= 2011        |          0    |            0.28 |  0.12 | 0.088  |   1      | flat       |
| wheeled gear, of the ground contact drawn |         52 | 2016-19        |          0.53 |            0.61 |  0.1  | 0.4941 |   1      | flat       |
| propulsor types                           |        218 | <= 2011        |          2    |            3    |  0.04 | 0.5945 |   1      | flat       |

Only 'no tail surface' has p < 0.05 unadjusted (rho -0.17, p 0.0096); after Holm 0.164. The article has no Spearman trend for F alone to compare with; the permutation count of 10 000 applies to the dQ bands, not to these Spearman p values.



# D. Quoted numbers and supplement tables (items 11-14, 20)

# Pending numbers, part D (items 11, 12, 13, 14, 20), paper P1

Recomputed on the public dataset folder `eVTOL_dataset` (621 designs, 619 with an architecture, 540 primary patents), seed 42, thesis functions unchanged, run 2026-11-26, one process at a time (`nice 19`). Paths are relative to `evtol-design-space-analysis-tools/` unless they start with `/mnt/`. CSVs are in `numbers/pending_csv/`. Values only, nothing interpreted. New scripts in `2_analysis/scripts/`: `45_pending_D_items_11_12.py`, `46_pending_D_item_13_table_S1.py`, `47_pending_D_item_14_table_S2.py`, `48_pending_D_item_20_spearman_holm.py`; each needs `EVTOL_DATASET=/mnt/storage_11tb/Drive_files_to_syncronize/eVTOL_dataset PYTHONPATH=2_analysis/src`, python3 without -I.

---

## 11. Asia-Pacific share of 2016-19; patents by priority year; the 90 % of 2023

### 11a. Asia-Pacific share of the designs of 2016-19

| value | number | script, file | definition |
|---|---|---|---|
| Asia-Pacific designs, cohort 2016-19 | 38 | `2_analysis/scripts/45_pending_D_items_11_12.py`, `D11a_region_share_per_cohort.csv` | designs with priority year 2016-2019 whose applicant region (`region3`, `frames.base`) is Asia-Pacific |
| designs in the cohort (denominator) | 213 | same | all designs with priority year 2016-2019 (the 213 of B6) |
| **share** | **17.84 % (38 / 213)** | same | 38 / 213; confirms 18 % |
| same share on the three named regions only | 38 / 206 = 18.45 % | same | denominator leaves out the 7 designs of 'Other regions' |
| same, designs with an architecture | 36 / 211 | same | for the record |

Asia-Pacific share per cohort (`D11a_region_share_per_cohort.csv`): <= 2011 11/59 = 18.64 %; 2012-15 6/57 = 10.53 %; 2016-19 38/213 = 17.84 %; 2020-23 92/237 = 38.82 %; 2024-26 39/55 = 70.91 %. Regions of 2016-19: North America 104, Europe 64, Asia-Pacific 38, Other 7.

### 11b. Patents by priority year (share of all years)

File `D11b_patents_by_priority_year.csv` (designs, patent families acquired, representative patents, primary patents behind the designs, each with its share of the all-years total; `complete` flag; years since year end). Source `2_analysis/scripts/45_pending_D_items_11_12.py` via `frames.filings_per_year` (`la_tables.filings_per_year`) and the design table.

| priority year | designs | patents acquired (families) | representative patents | primary patents behind the designs | complete |
|---|---|---|---|---|---|
| 2012 | 14 (2.3%) | 21 (1.3%) | 11 (1.3%) | 11 (2.0%) | True |
| 2013 | 11 (1.8%) | 43 (2.6%) | 13 (1.5%) | 11 (2.0%) | True |
| 2014 | 11 (1.8%) | 47 (2.9%) | 16 (1.8%) | 11 (2.0%) | True |
| 2015 | 21 (3.4%) | 60 (3.7%) | 21 (2.4%) | 18 (3.3%) | True |
| 2016 | 34 (5.5%) | 118 (7.2%) | 58 (6.6%) | 30 (5.6%) | True |
| 2017 | 52 (8.4%) | 144 (8.8%) | 73 (8.3%) | 45 (8.3%) | True |
| 2018 | 68 (11.0%) | 193 (11.8%) | 98 (11.2%) | 60 (11.1%) | True |
| 2019 | 59 (9.5%) | 150 (9.2%) | 82 (9.4%) | 53 (9.8%) | True |
| 2020 | 69 (11.1%) | 152 (9.3%) | 86 (9.8%) | 55 (10.2%) | True |
| 2021 | 72 (11.6%) | 140 (8.5%) | 98 (11.2%) | 56 (10.4%) | True |
| 2022 | 48 (7.7%) | 125 (7.6%) | 88 (10.0%) | 45 (8.3%) | True |
| 2023 | 48 (7.7%) | 115 (7.0%) | 72 (8.2%) | 43 (8.0%) | False |
| 2024 | 37 (6.0%) | 119 (7.3%) | 69 (7.9%) | 36 (6.7%) | False |
| 2025 | 16 (2.6%) | 39 (2.4%) | 22 (2.5%) | 16 (3.0%) | False |
| 2026 | 2 (0.3%) | 3 (0.2%) | 2 (0.2%) | 2 (0.4%) | False |

Column sums over all years: designs 621, patents acquired 1638, representative patents 876, primary patents behind the designs 540. Years 1999 to 2011 are in the CSV.

### 11c. What 'the article says 90 % for 2023' means, and where it is computed

Two different quantities carry '90' in the code:

1. **Publication lag, 90th percentile = 3 years** (`publication_lag_p90_years: 3` in `2_analysis/20_config.yaml`, line 71). Computed by `viz/frames.py:publication_lag` (years from priority to publication of each of the 540 representative primary patents) and `lib/growth.py:lag_quantile` (0.9 quantile). Recomputed here: **3.0 years** (unrounded), equal to the yaml value; by region (rounded 90th percentile, patents): North America 3 (212), Asia-Pacific 3 (164), Europe 3 (151), South America 3 (6), Middle East 4 (4). Rule that uses it: a priority year is complete when (snapshot 2026-06-08 minus 31 Dec of the year) / 365.25 >= 3 (`lib/growth.py:year_is_complete`, `complete` column of `D11b`): 2022 is complete (3.4 years), 2023 is not (2.4 years). Used in `frames.filings_per_year` and the evidence-base notebook `21_evidence_base.ipynb`.
2. **Share of 2023 already published at the snapshot** (the likely '90 %'): `lib/growth.py:visible_share` = P(lag <= k-1) + f * P(lag = k), k = 2026 - priority year, f = 159/365 = 0.436, lag distribution of the designs of priority years 2016-21 (n = 345; lag 0: 42, 1: 140, 2: 107, 3: 47, 4: 9). Applied in `frames.region_years` (per region) and `viz/followup_part1.py` (total). Recomputed here (`D11c_visible_share_by_priority_year.csv`):

| priority year | all three regions | North America | Europe | Asia-Pacific |
|---|---|---|---|---|
| 2022 | 98.5% | 98.2% | 98.3% | 99.4% |
| **2023** | **89.7%** | 91.7% | 87.3% | 89.0% |
| 2024 | 66.3% | 65.5% | 62.7% | 71.4% |

The stored freeze files (`results/2_analysis/freeze/NUMBERS_I.md`, `csv/q1_filings_per_year_lag_corrected.csv`) give 88.9 % for 2023 overall (reference n = 354, an earlier 627-design table); on the 621 designs it is 89.7% (reference n = 345). Which of the two quantities the article means is not stated in the code; the 90 % matches item 2 (89.7 %, regions 87.3 to 91.7 %); item 1 gives 3 years.

---

## 12. The 3.4 step-up in patent families in 2016 against 2.1 for aeronautics

Searched: `2_analysis/src`, `2_analysis/notebooks`, `results/2_analysis/freeze` and the dataset folder `06_external` (the dataset stores no step or jump value; `06_external/63_context_series` holds only counts). **No value is written as '3.4 per cent'. The values are multiplicative factors (x), not per cent.** Two procedures give a 2016 jump for the patent-family series:

| value | number | script, file | definition |
|---|---|---|---|
| jump factor at the turning point 2016, representative patent families | **3.4463** (printed 'x3.4' by `viz/thesis_q1.py:numbers`, key `turn_pat_x`, format .1f; stored rounded 3.45) | `2_analysis/scripts/45_pending_D_items_11_12.py` -> `viz/thesis_q1.py:_calc` -> `lib/growth.py:turning_point`; `D12b_turning_point_jump.csv`; freeze `csv/numbers_I_turning_points.csv` | exp(c2) of the two-segment log fit at the SSE-minimising break; break 2016 chosen by 91.4 % of 1 000 resampled fits, 95 % range 2015 to 2018 |
| level step, eVTOL architecture patent families, model (a), fit 2005-2022 | 3.30 (2.12 to 4.89) | `2_analysis/scripts/45_pending_D_items_11_12.py`, `D12a_level_step_model_a.csv`; freeze `csv/numbers_I_growth_breakpoints.csv` | exp(c2) of 'two lines with a free level step' (`lib/growth_models.py`), break 2016, 95 % residual-bootstrap interval |
| same, fit 2005-2023 | 3.52 (2.39 to 5.26) | same | same, one year more |
| level step, aeronautics (CPC B64), fit 2005-2022 | **2.10** (1.77 to 2.57) | same | same model on the B64 PatSeer series, break 2016 (range 2016 to 2016) |
| same, fit 2005-2023 | 2.11 (1.76 to 2.50) | same | same |
| level step, transport and operations (CPC section B), 2005-2022 / 2005-2023 | 2.05 / 2.07 | same | for the record |
| level step, all patents, 2005-2022 / 2005-2023 | 1.20 / 1.21 | same | for the record |

The 2.1 for aeronautics is the model-(a) level step (2.10 / 2.11). The turning-point routine of `lib/growth.py` is run on representative patents, unique aircraft and aircraft per 1 000 B64, not on B64 itself, so no 3.4-type jump exists for aeronautics: the 3.4 (3.4463) and the 2.1 come from two procedures. The like-for-like pairs in the code are 3.30 against 2.10 (fit to 2022) and 3.52 against 2.11 (fit to 2023). Figure: `viz/figures_part1.py:fig_growth_rates_ts` (Fig 4.2), notebook `21_evidence_base.ipynb`.

---

## 13. Table S1: the dimensions of the taxonomy

80 % rule: a dimension varies when its leading option holds under 80 % of the answering designs (`3_robustness/31_label_reliability/src/core.py`, `SHARE_RULE = 0.80`; thesis 3.4.2). Answer rate = designs answering / 621 designs (the 619-base rate is in the CSV; two designs without an architecture still answer `left-right symmetry` and `booms present`, so a 619 base gives 100.3 % for those two). Script `2_analysis/scripts/46_pending_D_item_13_table_S1.py`; functions `frames.selected_fields`, `frames.selected_field_series`, `frames.form_frame15`; CSVs `D13a_table_S1_design_space_table_dimensions.csv`, `D13b_table_S1_distance_dimensions.csv`, `D13c_w34_dimensions_not_in_w15.csv`.

### 13a. The 11 dimensions of the design-space table

| dimension | designs answering | answer rate | share of the most common option | varies (< 80 %) | enters the 15-dimension distance |
|---|---|---|---|---|---|
| number of wings (winged designs) | 542 | 87.3% | 65.3% | yes | yes, as Wing count |
| tail type | 594 | 95.7% | 29.3% | yes | yes, as Empennage Type |
| fuselage motion hover to cruise | 596 | 96.0% | 84.6% | no | yes, as Fuselage Kinematics |
| wing configuration | 537 | 86.5% | 87.2% | no | yes, as Wing Architecture |
| landing-gear type | 596 | 96.0% | 68.0% | yes | no |
| left-right symmetry | 621 | 100.0% | 95.3% | no | no |
| fuselage shape | 597 | 96.1% | 64.5% | yes | yes, as Fuselage Shape |
| booms present | 621 | 100.0% | 53.6% | yes | yes, as Boom count |
| propulsor units per aircraft (band) | 589 | 94.8% | 22.9% | yes | yes, as Propulsor band |
| places carrying propulsor units per aircraft | 589 | 94.8% | 48.2% | yes | yes, as Mount locations |
| propulsor enclosure (any ducted) | 589 | 94.8% | 63.5% | yes | yes, as Propulsor Enclosure |

How the table rows enter the distance (`frames.FORM15`, `frames.form_frame15`): tail type, fuselage motion, wing configuration, number of wings, fuselage shape and propulsor units (band) enter through the dimension of the same field (Empennage Type, Fuselage Kinematics, Wing Architecture, Wing count, Fuselage Shape, Propulsor band). 'Booms present' enters only through Boom count (rank 0 when `boomsPresent` is not True). 'Propulsor enclosure (any ducted)' and 'places carrying propulsor units' are not the distance's variables: the distance reads the enclosure of the set with the most propulsors (Propulsor Enclosure) and the set of stations carrying propulsors by Jaccard distance (Mount locations).

Reasons for exclusion from the distance (read in `frames.py`, `core.py`, `20_config.yaml`, `docs/`):

- **landing-gear type** (`gearArch`): not in `FORM15`; present in the older 34-dimension weighting w34 as 'Ground Contact Interface'. The reason for leaving it out of w15 is **not stated in the code**. Separate note in `core.py:r1_design_space`: the thesis count of varying dimensions leaves it out because 68 % of its answers are 'Unknown' (thesis II.1); that is a reason for the varying count, not written as the reason for the distance.
- **left-right symmetry** (`latSym`): not in `FORM15`; in w34 as 'Airframe Lateral Symmetry'. Reason: **not stated in the code**.
- The only written rule for the 15 is the `FORM15` comment in `frames.py`: 'the dissertation's declaration, 2026-10-15: 15 dimensions, each of the four systems weighing 1'. No per-dimension reason is given.
- Another cut: `field_drop_top_share: 0.88` in `20_config.yaml` (Table 6 leaves out a field whose top answer holds 88 % or more); it governs the printed table, not the distance. Options dropped from the table: wCount = 0 and places = 0 (`frames.D3_DROP_OPTIONS`, author's ruling of 2026-10-15).

### 13b. The 15 dimensions of the distance

All 15 enter the distance (definition of `FORM15`); system, weight and way of comparing are in the CSV. Answer rate = non-null cells of `form_frame15` (619 designs with an architecture) over 621 designs; for ordered or set dimensions the share is of the most common value.

| dimension | system | weight | designs answering | answer rate | share of the most common value | varies (< 80 %) |
|---|---|---|---|---|---|---|
| Architecture | G1 architecture | 1.0000 | 619 | 99.7% | 25.8% (SLC) | yes |
| Fuselage Shape | M1 structure | 0.5000 | 596 | 96.0% | 64.6% (Oval) | yes |
| Boom count | M1 structure | 0.3000 | 619 | 99.7% | 53.8% (0.0) | yes |
| Fuselage Kinematics | M1 structure | 0.2000 | 595 | 95.8% | 84.5% (Fixed) | no |
| Wing count | M2 aerodynamics | 0.3000 | 618 | 99.5% | 57.0% (1.0) | yes |
| Wing Architecture | M2 aerodynamics | 0.3000 | 536 | 86.3% | 87.1% (W) | no |
| Vertical Position | M2 aerodynamics | 0.0222 | 514 | 82.8% | 60.7% (High) | yes |
| Longitudinal Position | M2 aerodynamics | 0.0222 | 514 | 82.8% | 68.1% (Cent) | yes |
| Planform | M2 aerodynamics | 0.0222 | 532 | 85.7% | 61.8% (Str) | yes |
| Empennage Type | M2 aerodynamics | 0.3333 | 593 | 95.5% | 29.3% (Tailless) | yes |
| Propulsor band | M3 propulsion | 0.3500 | 589 | 94.8% | 22.9% (0.0) | yes |
| Tilt share | M3 propulsion | 0.3000 | 588 | 94.7% | 42.5% (1.0) | yes |
| Propulsor Enclosure | M3 propulsion | 0.1500 | 588 | 94.7% | 69.0% (Open) | yes |
| Tractor/Pusher Arrangement | M3 propulsion | 0.1000 | 522 | 84.1% | 95.4% (Front) | no |
| Mount locations | M3 propulsion | 0.1000 | 588 | 94.7% | 24.1% (frozenset({'wing'})) | yes |

Do not vary under the 80 % rule: distance dimensions Fuselage Kinematics (84.5 %), Wing Architecture (87.1 %), Tractor/Pusher Arrangement (95.4 %); table dimensions fuselage motion (84.6 %), wing configuration (87.2 %), left-right symmetry (95.3 %). Wing count in the distance keeps 0 wings (table row drops it), hence 56.96 % for 1 wing in the distance against 65.31 % in the table.

The 22 dimensions of the 34-dimension weighting (w34, kept for the record in `frames.FORM_GROUPS`) that are not among the 15 are listed in `D13c_w34_dimensions_not_in_w15.csv`. Reason for each: **not stated in the code**.

---

## 14. Table S2: levels of description

Script `2_analysis/scripts/47_pending_D_item_14_table_S2.py`; functions `frames.archetype_levels_table` (key `frames.level_key`), `frames.archetype_screens`, `lib.concentration.inverse_hhi` (order-2 Hill number, 1 / sum p_i^2), `frames.dd_level_keys` (F); CSVs `D14a_table_S2_levels.csv`, `D14b_table_S2_screens.csv`, `D14c_table_S2_three_levels_archetype_key_basis.csv`. `frames.ARCHETYPE_SETS` holds nine sets: the three of the paper and six others, all computed in the thesis 'nine sets' table and screened by the four rules of `20_config.yaml: archetype_screens` (at least twice as many configurations as classes, at most 5 % of designs alone, at least 90 % in configurations of 5 or more, at least 3 configurations of 5 % or more). The dataset folder holds no other level and no finer coding (grep of `A0c`, `A1tc`, `A2c` over its csv and md files: no hit). Letters: A or C architecture class, W number of wings, T any tilting propulsor, U propulsor-unit band, B booms present, B# booms binned (none, 1-2, 3, 4+), E tail type. L1 = A0, L2 = A1t, L3 = A0c.

| level | thesis code | designs keyed | configurations | singletons | effective number, order 2 | share of the largest configuration | largest configuration | screens passed |
|---|---|---|---|---|---|---|---|---|
| L1 (A) | C | 619 | 12 | 0 | 5.72 | 25.8% | SLC | 3 of 4 |
| L2 (A.W.T) | C·W·T | 617 | 39 | 10 | 11.32 | 16.2% | SLC · 1 · False | 4 of 4 |
| L3 (A.U) | C·U | 618 | 44 | 4 | 22.78 | 9.9% | TR · 1-3 | 4 of 4 |
| A.W.B | C·W·B | 618 | 57 | 17 | 20.49 | 9.2% | TR · 1 · False | 4 of 4 |
| A.W.B# (booms binned) | C·W·B# | 618 | 76 | 23 | 26.67 | 9.4% | TR · 1 · none | 3 of 4 |
| A.W.T.U | C·W·T·U | 617 | 108 | 38 | 40.68 | 8.1% | TR · 1 · True · 1-3 | 1 of 4 |
| A.W.B.U | C·W·B·U | 618 | 151 | 62 | 58.52 | 6.8% | TR · 1 · False · 1-3 | 1 of 4 |
| A.W.B.E | C·W·B·E | 618 | 191 | 83 | 85.83 | 3.4% | MR · 0 · True · Tailless | 1 of 4 |
| A.W.B.E.U | C·W·B·E·U | 618 | 347 | 226 | 181.87 | 2.6% | HB · 1 · False · blank · n/a (no M3 card) | 1 of 4 |
| F (family as one archetype) | F | 619 | 12 | 0 | 4.31 | 38.9% | Lift + Cruise + CVT* family | not computed (not in ARCHETYPE_SETS) |

Notes. (1) L1 to L3 use `frames.level_key`; `frames.archetype_key` (used by `dd_level_keys` and B6c) gives the same configurations, singletons and shares (order 2: 5.72, 11.32, 22.78; `D14c`). (2) Order 1 (exp Shannon), singleton share and designs left out are in `D14a`. (3) The stored `freeze/csv/q7_levels_of_description.csv` and `q7_hill_numbers_by_level.csv` hold L1 to L3 (12/39/44 configurations, 0/10/4 singletons, order 2 = 5.7/11.3/22.8, largest share 26/16/10 %) and agree. (4) F is the family reading of the architecture (Lift + Cruise + CVT* family as one option): 12 configurations, 0 singletons, order 2 = 4.31, largest 38.9 % (the family itself); it is not in `ARCHETYPE_SETS`, so no screens are computed for it. (5) A.W.B# is set `A1b`.

---

## 20. Quantities tested with Spearman and Holm (S3.4)

Script `2_analysis/scripts/48_pending_D_item_20_spearman_holm.py`; output `D20_spearman_holm_tests.csv` (165 rows: 14 + 109 + 42; one row per test with rho, raw p, Holm p, family, comparisons in the family, source file). Sources are the stored freeze files of 2026-11-25 (`results/2_analysis/freeze/csv/q6_share_trend_spearman.csv`, `q6_driver_trends.csv`, `q3_region_mix_change.csv`; `holm_register.csv` agrees). Block A was recomputed with `viz/analysis_iii.rho_table` and matches the stored values (`D20_check_rho_table_recomputed.csv`); blocks B and C are read from the freeze files, not recomputed. Holm function: `lib/multiple.py:holm` (statsmodels `multipletests`, method holm; a NaN p is outside the family). Notebook `28_multiple_comparisons.ipynb` step 2 describes the families as: III.1 the architectures, one family per span; V the regional trends, one family; the driver families are `thesis_q6.HOLM_ARCH` (`_with_holm`).

| block | quantity tested | family of the Holm correction | comparisons in the family |
|---|---|---|---|
| A. III.1 | share of each architecture in the year's designs against priority year, 2008-2023, the 7 architectures with 20 or more designs | the 7 architectures of that span | 7 |
| A. III.1 | same, 2016-2023 | the 7 architectures of that span | 7 |
| B. IV | trend of each of 17 traces inside an architecture over the cohorts (rows SLC, TR, CVT) | one family per trace over SLC, TR, CVT; a constant or too-thin architecture leaves the family | 3 for 14 traces; 2 for 'booms stow' and 'tilting joint groups'; 1 for 'fuselage kinematics not fixed' |
| B. IV | same traces for Tilt Wing, Multirotor and the pooled rows (ALL5, ALL) | none: raw p only | not applicable (62 of the 109 rows carry no Holm p) |
| C. V | trend 2012-2023 of a regional answer (3 regions x class, propulsive units, tilting unit, family F) | every trend test of the table, one family | 42 |

**A. Share trends (all 14 tests).**

| quantity | rho | raw p | Holm p | comparisons |
|---|---|---|---|---|
| Lift + Cruise (SLC), 2008-2023 | 0.443 | 0.09 | 0.43 | 7 |
| Tilt Propulsor (TP), 2008-2023 | -0.685 | 0.003 | 0.024 | 7 |
| Combined Vectored Thrust (CVT), 2008-2023 | 0.256 | 0.34 | 1 | 7 |
| Tilt Wing (TW), 2008-2023 | -0.144 | 0.59 | 1 | 7 |
| Multicopter (MR), 2008-2023 | 0.155 | 0.57 | 1 | 7 |
| Tilt Frame (TF), 2008-2023 | 0.001 | 1 | 1 | 7 |
| Pitch-to-Cruise (PTC), 2008-2023 | 0.474 | 0.06 | 0.38 | 7 |
| Lift + Cruise (SLC), 2016-2023 | 0.515 | 0.19 | 1 | 7 |
| Tilt Propulsor (TP), 2016-2023 | -0.452 | 0.26 | 1 | 7 |
| Combined Vectored Thrust (CVT), 2016-2023 | 0.548 | 0.16 | 1 | 7 |
| Tilt Wing (TW), 2016-2023 | -0.357 | 0.39 | 1 | 7 |
| Multicopter (MR), 2016-2023 | -0.476 | 0.23 | 1 | 7 |
| Tilt Frame (TF), 2016-2023 | -0.405 | 0.32 | 1 | 7 |
| Pitch-to-Cruise (PTC), 2016-2023 | 0.204 | 0.63 | 1 | 7 |

Blocks B (109 tests) and C (42 tests) are listed row by row in `D20_spearman_holm_tests.csv`. Codes are those of the source files (`TP` and `TF` in the share file; `TR` in the driver and regional files for the same architectures).

---

## What could not be done

- Item 11: which of the two '90' quantities the article means is not stated in the code (both given).
- Item 12: no source or script writes '3.4 per cent'; the closest stored values and their procedures are given.
- Item 13: reasons for leaving landing-gear type, left-right symmetry and the other w34 dimensions out of the 15 are not written in the code, config or docs read.
- Item 14: nothing missing; no finer coding than the nine sets exists in the thesis code or the dataset.
- Item 20: driver rows (block B) and regional rows (block C) are read from the freeze file, not recomputed.



# D2. Locks, query, samples, mismatches, Gower example (items 15-19)

# Pending numbers, part D2 (items 15 to 19)

Script for items 16 to 19: `2_analysis/scripts/55_pending_part_D2.py` (REPO = evtol-design-space-analysis-tools), run on `eVTOL_dataset` (621 designs, 619 with an architecture), seed 42 (no random draw), nothing interpreted. CSVs in `numbers/pending_csv/` (names `D2_*`). Item 15 is read from files, no script.

## 15. Coding locks (12 locks)

Rule source: `eVTOL_dataset/03_patents/34_codebook.md` section 7, lines 213-230 (one row per lock, lines 219-230). Where a broken lock is detected in the robustness run: `REPO/3_robustness/31_label_reliability/src/perturb.py`, function `locks(r)`, lines 200-304 (one `out.add("Ln")` per lock, line given below). Use: `perturb.py:455` (`if locks(r) <= self.orig_locks[i]`) accepts a perturbed design only if it breaks no lock its original codes do not break; otherwise it is redrawn up to `MAX_REDRAWS = 20` (`perturb.py:46`), then keeps its original codes (docstring `perturb.py:27-30`). Wizard: `REPO/1_data_acquisition/11_patent_information/wizard/11H_master_wizard.html` (lines given). The codebook says the wizard blocks a locked combination and the export check reports it as an error; identifiers L9, L11, L13 are not used.

| lock | rule in words | applies at | codebook line | perturb.py line | wizard line |
|---|---|---|---|---|---|
| L1 | SLC: no propulsor tilts | M3 | 219 | 263 | 2263 (propKinLock) |
| L2 | TW, SLC, SRW, TF, PTC, RC: propulsor articulation Fixed on every propulsor set (TP, CVT, MR free; DS has L7) | M3 | 220 | 265 | 2263-2268 |
| L3 | MR and RC: zero wings, no wing configuration recorded | M2 | 221 | 271 | 4730-4735 (wCount = 0) |
| L4 | CVT: at least two of tilting rotor, fixed rotor, tilting wing; suspended when articulation is Other or an override is used | M3, after all wings declared | 222 | 287 | 2156 |
| L5 | TW: every wing that carries propulsors is Tiltable; a thrust source that does not tilt with a wing makes it CVT; a control-only propulsor is not a thrust source; suspended by Other | M2 and M3, after all wings declared | 223 | 292 | 2188, 2491-2511 |
| L6 | TF: fuselage kinematics is Tail-sitter or Variable Incidence (the code in perturb.py accepts TiltBody, Variable Incidence, LevelCabin) | M1 | 224 | 294 | 2289-2305 |
| L7 | DS: all propulsors Fixed | M3 | 225 | 267 | 2263-2268 |
| L8 | TP: only tilting rotors; every wing Fixed and every rotor tilts on its own mount or on a tilting boom; control-only exempt; suspended by Other or an override | M2 and M3 | 226 | 297 | 2188 |
| L10 | RC and PTC: fuselage kinematics Whole-Body Pitch | M1 | 227 | 299 | 979, 2289-2306 |
| L12 | A propulsor on a tilting wing, a boom on a tilting wing, a tilting boom set or a tilting empennage has articulation Fixed (tested group by group when boom groups and boom propulsor types are equal in number); a boom ticked as on the fixed part of the wing does not tilt | M3 | 228 | 301 | 2173 |
| L14 | SLC and SRW: thrust kinematics Horizontal or Vertical, never Mixed | M3 | 229 | 303 | 2455-2465, 5006, 5017 |
| L15 | Code not TW, TP, DS, CVT or SRW and the record moves nothing: every approved figure's aircraft state is Invariant | T2 | 230 | not tested (T1/T2 fields are not perturbed, `perturb.py:24-26`) | 1794-1800, 3901-3916 |

CSV: `pending_csv/D2_15_locks.csv`. Not found: the script `05a_audit_lock_tests.py` named in the docstring of `locks()` (`perturb.py:201`) is not in REPO (find returned nothing outside results).

## 16. PatSeer query, date, funnel

- **Query string** (value: one line, as PatSeer accepts it): file `eVTOL_dataset/01_query/query_thesis.txt` (also `01_query/README.md`: "returns the 1 639 patent families"):

```
((CPC:(B64C29*) AND TACD:((aircraft OR evtol OR rotorcraft OR vtol OR vehicle) W5 (architecture OR configuration OR topology OR airframe OR fuselage OR layout OR frame OR structur* OR body OR wing* OR boom OR tilt* OR canard)) AND (CPC:(B64D27/30 OR B64D27/31 OR B64D27/32 OR B64D27/33 OR B64D27/34) OR TACD:((electri* W3 (motor* OR propuls* OR drive*)) OR eVTOL OR ("distributed" W2 "propulsion")) OR T:(tiltrotor OR "tilt rotor" OR "tilting rotor*" OR "tilting propeller*" OR (vtol AND (wing* OR fuselage OR airframe OR rotor* OR boom OR canard OR frame)))) AND PBY:[2005 TO 2026])) NOT (CPC:(B64B* OR B64G* OR B64F* OR F28* OR B64D11/06* OR B64D43* OR B64D45* OR B60F5*) OR TA:((("gasoline" OR "petrol" OR "jet" OR "turbine") W "engine") OR diesel OR "internal combustion" OR "jet propulsion" OR "gas turbine" OR "fuel cell" OR "hydrogen") OR TA:(UAV OR unmanned OR drone) OR T:("battery" OR "charging system*" OR "power management" OR cooling OR wiring OR seat* OR display* OR simulator* OR GYROSCOPIC* OR gearbox OR Circuits OR Method))
```
  Priority-year window in the query: `PBY:[2005 TO 2026]`.
- **Search date: 2026-06-08.** Source: the export file name `patseer_1639_2026-06-08.xlsx`; the file's modification time is 2026-06-08 18:54:58 (+0100). The xlsx has no search-date field of its own (workbook properties show 2026-11-26, not the search date). No other date is stored; the PatSeer Get Count is not stored.
- **Funnel** (script 55 recomputed from files 33, 42, 45; identical to `supplementary_csv/C8a_funnel.csv`, which holds more rows):

| step | families / rows | source |
|---|---|---|
| families in the export = rows of file 33 | 1 639 | `03_patents/33_patents.csv` (1 639 distinct Simple Family IDs, C8a) |
| disapproved at T1 | 531 | `is_approved == False` |
| approved at T1 | 1 108 | `is_approved == True` |
| aircraft rows on approved patents | 1 219 | `04_aircraft/42_aircraft.csv` |
| non-primary rows (duplicates D1 41 + D2 381) | 422 | `is_primary == False` |
| primary rows | 797 | `is_primary == True` |
| primary rows set aside by the gate ('but similar') | 176 | C8a |
| designs | 621 | `is_design == True`, file 45 |
| designs with an architecture (analysis frame) | 619 | `topType` not blank |
| primary patents behind the designs | 540 | C8a |

  Disapproval reasons of the 531 (file 33 `reason`): No Aircraft Image 173, Pure UAV 161, Out of Domain 158, Other 22, No Content 12, Not VTOL 5. Not computable: records retrieved before family grouping and the Get Count (not stored; C8 note).
- CSVs: `D2_16_funnel_recomputed.csv`, `D2_16_disapproval_reasons.csv`.

## 17. Relevance (68 %) and completeness (72 %), Wilson 95 % intervals

**Finding about the procedure: the files document no random sample for either figure.** Both are counts over a full set.

| quantity | k / n | share | Wilson 95 % | file |
|---|---|---|---|---|
| relevance: families approved at T1 of all 1 639 | 1 108 / 1 639 | 67.60 % | 65.30 to 69.82 % | `03_patents/33_patents.csv` (`is_approved`) |
| completeness, aircraft with a patent found: captured / (captured + outside the query) | 33 / 46 | 71.74 % | 57.45 to 82.68 % | `02_gold_standard/29_gold_standard.csv` (`aircraft_outcome`) |
| completeness, programmes with a patent found: same, one row per programme | 31 / 43 | 72.09 % | 57.31 to 83.25 % | same (`programme_outcome`) |
| completeness, all 69 census aircraft (incl. no patent found 21, search pending 2) | 33 / 69 | 47.83 % | 36.47 to 59.41 % | same |
| completeness, all 63 programmes | 31 / 63 | 49.21 % | 37.27 to 61.24 % | same |

Definition of Wilson: `lib.intervals.wilson_interval(k, n)` (95 %, no finite-population correction). Which of the completeness rows is the "72 %" is not stated in any file I found: 71.74 % (aircraft) and 72.09 % (programmes) both round to 72 %; the 68 % matches the relevance row (67.60 %). Gold-standard counts: aircraft captured 33, outside with patent 13, no patent found 21, search pending 2; programmes captured 31, outside 12, no patent 20 (`D2_17_gold_standard_counts.csv`, also split by `entered_by` and `tier`).

How the files document the procedure:
- **Relevance (judging).** `03_patents/34_codebook.md` section 3 and 4 (lines 50-64, 92-101): T1 is one answer per patent (Approve or Disapprove, with a reason); a patent is kept when it holds an aircraft inside the technological domain and at least one figure that can establish the architecture; patents were labelled in assignee order, then priority-date order, by one coder. `eVTOL_dataset/README.md` ("How the data were made"): every label in file 32 was given by the author, one patent, figure and aircraft at a time, in the wizard. So the 1 639 families were all judged; there is no drawn sample.
- **Completeness reference set (construction).** `02_gold_standard/README.md` and `22_searches_described.md`: the gold standard (file 29) is a census of mature eVTOL programmes, one row per census aircraft, built from `21_census_candidates.csv` (candidates from the evtol.news directory and the AAM index, with the reason each entered or not), searched with ten PatSeer searches (`22_searches_described.md`, `23_search_query.txt`: pool, census, enhanced, enhanced2, avic_beta, widen_winged, lift_cruise_no_patent and others, joined with OR), hits per aircraft in file 25, author answers in file 27 (`27_author_answers.csv`, in order of step). The result per aircraft is `captured`, `outside, patent found` or `no patent found`. The entry criteria in file 29 (`criterion`): VFS TRL 7, AAM index, AAM index (history), VFS TRL 6 winged, VFS TRL 6 wingless; tier TRL 7 or higher 45 aircraft, TRL 6 24 aircraft. The README states "The review pages had no button to confirm a proposal, so only changes were recorded: an empty decision means the author accepted the proposal as shown." REPO `3_robustness/33_query_completeness/README.md` has no code of its own and points to `1_data_acquisition/11_patent_information` (the account script `scripts/11A10_full_account.py`, section 4.1b, computes completeness by programme and architecture; it is an older account whose totals (43 programmes at its date) differ from the current file 29).
- **Sample-based accuracy that does exist (hand-reviewed samples, not the 68 % or 72 %):** `06_external/61_evtol_news_directory/directory_accuracy.csv` (copied to `D2_17_directory_accuracy_copy.csv`): domain flag kept pages 77 of 88 (87.5 %, 79.0-92.9), excluded pages 59 of 68 (86.8 %, 76.7-92.9); development year exact 49 of 81 (60.5 %); TRL exact 23 of 46 (50.0 %), within one level 35 of 46 (76.1 %).
- Not documented anywhere I looked: any random draw (seed, sampling frame, sample size) for a "relevance sample", and an independent judge. If the paper text says "sample", it does not match the files.

## 18. Architecture mix, dataset against the VFS directory; ten mismatches

**One sentence.** In the dataset, 366 of 619 designs with an architecture (59.1 %) are vectored thrust, 168 (27.1 %) lift plus cruise, 47 (7.6 %) wingless multicopter, 9 (1.5 %) electric rotorcraft and 29 (4.7 %) hoverbike or personal flying device, against 286 (32.8 %), 153 (17.6 %), 265 (30.4 %), 57 (6.5 %) and 110 (12.6 %) of the 871 in-domain pages of the VFS (evtol.news) directory (chi-square 208.29, 4 degrees of freedom, p = 6.2e-44; adjusted residuals +10.08, +4.43, -10.67, -4.71, -5.20).

Source: `viz/thesis_q4.py:215` `directory_mix(ctx)` (the call behind notebook `2_analysis/notebooks/21_evidence_base.ipynb`, item `q4_dataset_vs_directory_classes`, `viz/figures_part1.py:509`); directory = `06_external/61_evtol_news_directory/directory_aircraft.csv` pages with `domain_in_domain` true (871 of 1 229); the figure csv `results/2_analysis/figures/Part_I_evidence_base/I4_external_validity/appendix/q4_dataset_vs_directory_classes.csv` holds the same counts. Classes: VT = TR, CVT, TW, TB, PTC, DS (vectored thrust), LC = SLC, WM = MR, ER = RC, HB = HB/PFV (the eight SRW designs sit in none of the five, per the account script); 366+168+47+9+29 = 619. Table: `D2_18_dataset_vs_directory.csv`.

**Ten drawing-against-public-aircraft mismatches** (97 designs carry a public aircraft name; drawing label agrees on 87, so 10 do not; sources `viz/frames.py:985` `public_arch_frame`, `07_results/73_coding_agreement/coding_agreement.csv`, `supplementary_csv/B4_named_and_compared.csv`, `B5_agreement_kappa.csv`, `B5b_public_match_values.csv`: yes 81, taxonomy 6, no 9, image 1). In 9 ("no") the drawing label and the patent-text label agree with each other and not with the public aircraft; in 1 ("image") the drawing label differs from the text, which matches the public aircraft.

| design | aircraft name | label from the drawing | label from the text | public aircraft (directory `public_arch`) | match type |
|---|---|---|---|---|---|
| US2018290736A1_ua1 | S4 v1 | SLC | SLC | Vectored thrust (S4, tilt rotor) | no |
| US9975631B1_ua1 | Cora v1 | TW | TW | Lift + cruise (Cora) | no |
| US2018086448A1_ua1 | Wisk Aero | TW | TW | Conventional take-off (Z-P1) | no |
| DE102023108565B3_ua1 | Porsche-Boeing concept | SLC | SLC | Vectored thrust (concept) | no |
| US2021371117A1_ua1 | Porsche-Boeing concept v1 | SLC | SLC | Vectored thrust (concept) | no |
| DE102023133781B3_ua1 | Porsche-Boeing concept v2 | SLC | SLC | Vectored thrust (concept) | no |
| US2024253779A1_ua1 | S-A1 | SLC | SLC | Vectored thrust (S-A1 mock-up) | no |
| WO2024151705A1_ua1 | S-A1 v1 | SLC | SLC | Vectored thrust (S-A1 mock-up) | no |
| CN119262274A_ua1 | AE200 | SLC | SLC | Vectored thrust (AE200, tilt rotor) | no |
| GB201801766D0_ua1 | e-Starling | SLC | CVT | Vectored thrust (e-Starling) | image |

CSV: `D2_18_ten_mismatches.csv`. Agreement values (B5): drawing against public 87/97, kappa 0.8727, Wilson-FPC 0.83-0.94; text against public 88/97, kappa 0.8866; drawing against text 94/97, kappa 0.9613.

## 19. Worked example, Gower distance (w15)

Frame: `viz/frames.py:2242` `form_frame15(ds)` (via `gower_inputs(ds, "w15")`, 619 rows, 15 dimensions); weights `form_weights(None, "w15")` (`frames.py:2074`, from `FORM15`, `frames.py:2046`); distance `lib/distance.py` `gower_distance` with the fixed ranges of `FORM15_RANGES`: d_ij = sum_k w_k delta_ijk / sum_k w_k present_ijk, with delta = 0 if the categories match, 1 if not; for an ordered dimension |rank difference| / range (Boom count 4, Wing count 3, Propulsor band 4); Tilt share |difference|; Mount locations the Jaccard distance. Search: all pairs of the 619 whose other 13 dimensions are identical (blank counted as equal) and whose wing count and propulsor band both differ: 3 pairs (`D2_19_candidate_pairs.csv`). The pair with no blank cell and the smallest rank differences is shown (the first of the 3).

Design i = **EP4748710A1_ua1** (Leonardo, priority year 2024, cohort 2024-26 partial); design j = **DE102019001834A1_ua1** (no assignee in the table, priority year 2019, cohort 2016-19). Both architecture CVT. Propulsor band ranks: 0 = "1-3" units, 1 = "4", 2 = "5-6", 3 = "7-8", 4 = "9+" (`frames.py:34`).

| dimension | design i | design j | weight | both present | delta | w x delta |
|---|---|---|---|---|---|---|
| Architecture | CVT | CVT | 1 | 1 | 0 | 0 |
| Fuselage Shape | Oval | Oval | 0.5 | 1 | 0 | 0 |
| Boom count (rank) | 0 | 0 | 0.3 | 1 | 0 | 0 |
| Fuselage Kinematics | Fixed | Fixed | 0.2 | 1 | 0 | 0 |
| **Wing count** | 2 | 1 | 0.3 | 1 | 1/3 = 0.333333 | 0.1 |
| Wing Architecture | W | W | 0.3 | 1 | 0 | 0 |
| Vertical Position | High | High | 1/45 = 0.022222 | 1 | 0 | 0 |
| Longitudinal Position | Cent | Cent | 1/45 | 1 | 0 | 0 |
| Planform | Str | Str | 1/45 | 1 | 0 | 0 |
| Empennage Type | Conventional | Conventional | 1/3 = 0.333333 | 1 | 0 | 0 |
| **Propulsor band (rank)** | 2 (5-6) | 0 (1-3) | 0.35 | 1 | 2/4 = 0.5 | 0.175 |
| Tilt share | 0.666667 | 0.666667 | 0.3 | 1 | 0 | 0 |
| Propulsor Enclosure | Open | Open | 0.15 | 1 | 0 | 0 |
| Tractor/Pusher Arrangement | Front | Front | 0.1 | 1 | 0 | 0 |
| Mount locations | {empennage, wing} | {empennage, wing} | 0.1 | 1 | 0 (Jaccard) | 0 |
| **sum** | | | 4.0 (all 15 present) | | | **0.275** |

d_ij = 0.275 / 4.0 = **0.06875**. Check: `lib.distance.gower_distance` on the two-row frame = 0.06875; on the full 619 x 619 frame, entry (i, j) = 0.06875; absolute difference to the hand value 1.4e-17 (`D2_19_check.csv`). Per-dimension table with the sum row: `D2_19_worked_gower_example.csv`. Note the number of wings is the wing count column (2 against 1) and the band ranks differ by 2 (5-6 against 1-3 units); the other two candidate pairs differ by 1 wing and 2 ranks (US2022388647A1_ua1 against WO2012047337A1_ua1) and 1 wing and 4 ranks (EP3998191A1_ua1 against UA124132C2_ua1).

## Not possible or not found

- Item 15: script `05a_audit_lock_tests.py` is not in REPO; line references use the codebook, `perturb.py` and the wizard.
- Item 16: records before family grouping and PatSeer Get Count are not stored; the search date comes from the file name and file time only.
- Item 17: no drawing or judging procedure of a random "relevance sample" and no random draw for the completeness set are documented; figures given are full-set counts with Wilson intervals as above.

