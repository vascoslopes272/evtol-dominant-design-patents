# Request trace: every request for numbers of paper P1, where it is answered, and how far it can be trusted

Dataset `eVTOL_dataset` (621 designs, 619 with an architecture), thesis seed 42. Written 2026-11-26. Paths are relative to the repository unless they start with `eVTOL_dataset/`. Scripts are in `2_analysis/scripts/`; the notebook `2_analysis/notebooks/31_pending_numbers.ipynb` runs them in order. The assembled text is `results/2_analysis/pending_numbers/pending_numbers.md`; the same files are in `paper_figures_for_other_pc/numbers/`.

**Status words.** `done`: computed from the dataset by a script in the repository, file given. `done, differs from the paper`: computed, and the value is not the one the paper quotes (listed in the last section). `done (all runs finished 2026-11-26)`: needs the coding-noise runs, which were still running when this was written. `not possible`: the information is not in the files; the reason is given.

**How far each kind of number can be trusted.**
- Numbers that come straight from a table or from a thesis function called unchanged (counts, shares, Wilson intervals, band edges, percentiles) were recomputed, and several were checked a second time by hand (configurations 12, 39, 44; effective numbers 5.72, 11.32, 22.78; Gower worked example against the library to 1e-17).
- Numbers produced by a subagent were not all rechecked line by line. Items whose value disagrees with the paper (section 3 below) are the ones to read before they are used.
- The coding-noise numbers (items 1 to 4) are not final until the three runs listed in section 2 have finished.

## 1. The twenty items (prompt of 2026-11-26)

| # | request | status | where |
|---|---|---|---|
| 1 | replica count at 10 000 permutations; 1 000 replicas | done (all runs finished 2026-11-26). 1 000 replicas at 10 000 permutations do not exist (about 42 h); the 1 000-replica run at 1 000 permutations is repeated with the new rule as the labelled reference | `pending_part_A.md` A1, `pending_csv/A1_replica_counts.csv`, `40_pending_block_A.py` |
| 2 | Table S7: every result, original, share kept under weights and under coding | done (all runs finished 2026-11-26) | `pending_csv/A2_S7_every_result.csv` |
| 3 | numbers of S5 and 4.4 (dQ below band, F three conditions, F fails share, medians, standard wings, TP decline) | done (all runs finished 2026-11-26) | `A3a_*.csv`, `A3b_*.csv` |
| 4 | verdict for F under replicas, both bases | done (all runs finished 2026-11-26) | `A4_F_verdict_*.csv` |
| 5 | rarefaction 30, 40, 50, all levels and bases; which verdicts change | done, differs from the paper (two cells change, not one) | `pending_part_B_C.md` item 5, `39_rarefaction_verdict_table.py` |
| 6 | variety threshold 70, 80, 90 % | done | item 6, `43_variety_window_tables.py` |
| 7 | share condition with 2, 3, 4 consecutive years, every level and base | done | item 7, `38_parameter_sweep.py --part window` |
| 8 | configurations at A, A·W·T, A·U and effective numbers | done, explained (627 against 621 designs; 1D values) | item 8, `41_levels_and_last100.py` |
| 9 | new configurations in the 100 most recent designs | done, explained (reproduced on the 627 table; p becomes 0.0375 on 621) | item 9, `41_levels_and_last100.py` |
| 10 | trends for family F alone | done, agrees with the paper | item 10, `42_family_F_trends.py` |
| 11 | Asia-Pacific 18 %; patents by priority year; the 90 % of 2023 | done; the "90 %" has two possible meanings in the code | `pending_part_D.md` item 11, `45_pending_D_items_11_12.py` |
| 12 | the 3.4 step-up of 2016 against 2.1 | done, explained (a factor, 3.4 times; not per cent) | item 12 |
| 13 | Table S1 | done; reasons for exclusion are not written in the code | `46_pending_D_item_13_table_S1.py` |
| 14 | Table S2 | done | `47_pending_D_item_14_table_S2.py` |
| 15 | list of coding locks | done (12 locks; `05a_audit_lock_tests.py` named in a docstring is not in the repository) | `pending_part_D2.md` item 15, `55_pending_part_D2.py` |
| 16 | PatSeer queries, date, funnel | done; the count before family grouping is not stored; the search date comes from the export file | item 16 |
| 17 | how the 68 % and 72 % were drawn, with intervals | done; 68 % explained (thesis sample of 100 families), 72 % open | item 17 |
| 18 | architecture mix against the VFS directory; ten mismatches | done | item 18 |
| 19 | Gower worked example | done | item 19 |
| 20 | Spearman and Holm list | done; driver and regional rows are read from the freeze files, not recomputed | `48_pending_D_item_20_spearman_holm.py` |

## 2. Coding-noise runs (new rule: list the values that break no lock, draw one at random; empty list keeps the original value)

| run | replicas | permutations | tag in `results/31_label_reliability/` | expected end (2026-11-26) |
|---|---|---|---|---|
| 15 % per value | 120 | 10 000 | `allowed_r15_p10000` | done 2026-11-26 06:34 |
| 15 % per value, reference | 1 000 | 1 000 | `allowed_r15_p1000_n1000` | done 2026-11-26 10:46 |
| 20 % per value | 120 | 10 000 | `allowed_r20_p10000` | done 2026-11-26 15:52 |
| first version (redraw whole design up to 20 times), kept for the record | 120 | 10 000 | `r15_p10000` | done 2026-11-26 00:26 |

The first version is not the rule the Methods describe; its numbers are labelled as such wherever they appear. The new rule raises the share of architecture labels that change from 7.3 % to about 14 % (two test replicas, 87 of 621 designs each).

## 3. Where the files disagree with the paper, and the cause found (see `results/2_analysis/pending_numbers/discrepancy_causes.md`)

Reproduced by running the thesis functions unchanged on the frozen 627-design thesis table (`eVTOL_dataset_v1_WORK/_frozen_thesis_submitted/03_aircraft/`), seed 42. The paper values were taken from the submitted thesis text (the P1 text itself was not found); if the paper differs from the thesis, that comparison is not made.

1. Rarefaction: balance verdicts change in two cells, not one: A·W·T all designs 2020-23 (percentile 2.7, 2.8, 2.5 at n = 30, 40, 50; below band only at 50) and A·U protected 2020-23 (3.0, 2.3, 2.6; below band only at 40). Open for the author: correct the sentence in the paper.
2. Configurations 12, 39, 43 and effective numbers 7.3, 16.4, 29.3: **explained, small.** The 627 table gives exactly these values. The effective numbers are the 1D values, not 2D. The 621 dataset has 44 A·U configurations because a recoded design created "TB 9+" (one configuration; 0.1 to 0.3 in the effective numbers). Use 12, 39, 44 and 7.3, 16.5, 29.6, or keep the thesis values and say so.
3. The 100 most recent designs, 4.1 against 1.6, p 0.058: **explained, reproduced.** The 627 table gives 4.14 against 1.61, p 0.0579 at A·W·T (A·U 1.09 against 0.60, p 0.4447). On the 621 dataset the same estimator gives 4.18 against 1.44, p 0.0375, so "not detected" at A·W·T becomes "detected" at the 5 % level. Open for the author: how to word it.
4. "3.4 per cent": **explained, small, plus a unit error.** It is a factor (3.4 times, interval 2.1 to 5.1). The 627 table gives 3.35 (2.12 to 5.05) against 2.10 (1.77 to 2.57) for aeronautics; the 621 dataset gives 3.30 (2.12 to 4.89). Write "times", not "per cent".
5. 68 %: **explained**, it is the thesis sample of 68 of 100 families (about 8.9 points either way); the full count is 67.6 %. 72 %: **open.** The thesis completeness values are 82.1 % and 60.7 %. The census gives 71.7 % (33 of 46 aircraft) or 72.1 % (31 of 43 programmes), but no file says which one is meant or how it was drawn.
6. "90 % for 2023": **small.** The thesis has both readings; the share of 2023 designs already published is 89.7 % (88.9 % with the reference set of all designs); the p90 of the publication lag is 3 years. The difference between the two published shares is a definition, not a dataset effect.
7. Architecture-label change: 7.5 % in the text; 7.3 % under the first version; **14.9 % under the rule of the paper** (allowed-values rule, 15 %, 120 replicas, 71 to 121 of 621 designs per replica). The text value is replaced.
8. Coding-noise values under the rule of the paper (15 %, 120 replicas, 10 000 permutations, finished 2026-11-26 06:34). Small shifts from the first-run values quoted in the text: share of replicas with dQ below band 14 to 23 % (text 13 to 18 %); F meets all three conditions, protected designs 0.8 % (first version 0.0 %); F fails the share condition, all designs 100 %; F above 50 % in 2020, protected 2.5 % (first version 3.4 %); leading share of standard wings 0.87 to 0.75 (text 0.87 to 0.74); hover-to-cruise 0.85 to 0.72; ducted 0.63 to 0.53; Tilt Propulsor share falls with Holm p < 0.05 in 55 % of replicas (text 73 %, first run). No change of robustness category except the Tilt Propulsor decline (to be read against the reading rule: 30 to 70 % is sensitive). At 20 % (120 replicas, about 20 % of labels change): balance kept 85 % (all designs) and 78 % (protected), disparity met 8 % and 9 %, F meets all three conditions 0 % (protected), F above 50 % in 2020 0 %, Tilt Propulsor falls in 57 % of replicas, standard wings 0.87 to 0.71, hover-to-cruise 0.85 to 0.68, ducted 0.63 to 0.57. The 1 000-replica reference (1 000 permutations) has finished and is in the tables; it did not store the label-change count.
