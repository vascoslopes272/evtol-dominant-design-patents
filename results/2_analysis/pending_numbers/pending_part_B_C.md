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
