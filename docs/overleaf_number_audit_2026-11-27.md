# Number audit of Overleaf project "P1 - Dominant design in eVTOL" against eVTOL_dataset (621 designs)

Overleaf was NOT edited. Sources read from the downloaded zip (`P1___Dominant_design_in_eVTOL.zip`, 2026-11-27 00:58). Line numbers are those of the file in the zip. Already fixed today and not re-reported: 213 / 211, 3.3-fold, boom count 619 / 5 / 54 %, 39 % protected best yearly share, Table 5 share column.

Status: OK, ROUNDING, WRONG (correct value given), STALE (value from the old 627-design table or from an older coding run), NOT FOUND (no source in the results).

Sources (short names): **nb22 c16** = notebook 22_design_space cell 16 (`q7_levels_of_description`); **nb23 c14 / c16 / c20** = notebook 23 cells (`q7_condition1_family`, `q7_condition2_balance`, `q7_family_conditions`); **nb24 c7 / c14 / c20** = notebook 24 cells (`q6_leading_layout_by_architecture`, `q6_cvt_units_on_booms`, `q6_cvt_ducted_by_boom_layout`); **s31** = `scripts/31_family_F_numbers.py` -> `results/2_analysis/family_F/percentiles_*.csv` (10,000 permutations); **s56** = `scripts/56_request_2026-11-27_numbers.py`; **PN-A / PN-D** = `results/2_analysis/pending_numbers/pending_part_A.md`, `pending_part_D.md` and their CSVs; **DC** = `pending_numbers/discrepancy_causes.md`; **NV** = `freeze/NUMBERS_V.md`; **W1/W2** = `eVTOL_dataset/07_results/72_weight_sensitivity/test1_summary.csv`, `test2_*.csv`; **CA** = `07_results/73_coding_agreement/coding_agreement.csv`.

Check made by machine: every number of S4 Tables S-all and S-prot (288 values: n, share, ²D, band, percentile, ΔQ, band, percentile) was parsed from the .tex and compared with `percentiles_balance.csv` / `percentiles_disparity.csv`: 0 mismatches. Table S-protall also matches `percentiles_disparity_protected_vs_all.csv`.

## Table, sorted by file and line

| File:line | As written | In the results (source) | Status |
|---|---|---|---|
| 00_frontmatter:3 | 621 designs; 1,639 patent families | 621 (`len(ctx.v)`); 1,639 (`numbers_I_funnel.csv`) | OK |
| 00_frontmatter:3 | F holds 49 % and 57 % of new designs in 2020 and 2021 | 49.3 %, 56.9 % (nb23 c14; PN-D) | OK |
| 00_frontmatter:3 | "over a thousand concepts" | external (VFS); not in results | NOT FOUND |
| 01_introduction:2 | over 1,100 concepts; USD 1.5 trillion; a few dozen programmes; about half a dozen programmes in 2016 | external citations (vfs2025, morganstanley2019, smg2026) | NOT FOUND (external) |
| 01_introduction:10 | 621 designs from 876 patents, 1,639 families | 621; 876 representative patents; 1,639 (funnel) | OK |
| 03_methods:17 | patent families rise 3.3-fold against 2.1-fold | 3.30 (2.12 to 4.89) vs 2.10 (1.77 to 2.57), fit 2005-2022, break 2016 (PN-D item 12) | OK (no interval quoted) |
| 03_methods:17 | roughly 90 % of 2023 patents published | 89.7 % (three regions, n 345) or 88.9 % (all designs 2016-21, n 354) (D11c) | ROUNDING; S2:110 says 89 % |
| 03_methods:76 | query run 8 June 2026; 1,639 families | funnel: snapshot 2026-06-08 | OK |
| 03_methods:76 | completeness 72 % | thesis gold standard of 56 gives 60.7 % (34/56) or 82.1 % (46/56); census gives 71.7 % (33/46 aircraft) or 72.1 % (31/43 programmes); no file says which (DC item 5) | NOT FOUND |
| 03_methods:76 | relevance 68 % | 68 of 100 sampled (thesis sample, file not in repo); full count 1,108/1,639 = 67.6 % | ROUNDING |
| 03_methods:76 | patent precedes first flight by a median of 3 years | 3.0 years (index assignees, n 12; 13 with planned years) (`q4_publication_lead_summary.csv`) | OK |
| 03_methods:81 | 876 representative patents; 97 matched, 87 agree, kappa 0.87; two of ten mismatches from drawings | 876; CA: 87/97, kappa 0.87; of the ten, **one** is a drawing misread (e-Starling, drawing SLC, text CVT) and **nine** are patents that differ from the aircraft built (R59_D2_ten_disagreements.csv; the Supernal S-A1 ruling moved one from 2 to 8) | 876, 87, 0.87 OK; "two" and "eight" STALE (1 and 9) |
| 03_methods:85 | "Nine dimensions pass the first filter" (at least 500 answers) | all 11 dimensions of the design-space table answer >= 500 (537 to 621) and all 15 of the distance (`paper_numbers.md` 7a/7b). Nine are the ones listed in Table S1 after dropping landing gear (68 % Unknown) and left-right symmetry (top share 95 %, rule `field_drop_top_share` 0.88) | WRONG as a description of the filter |
| 03_methods:87 | each cohort compared at a fixed size of 40 | `rarefy_n: 40` | OK |
| 03_methods:107 | draws of 30 and 50 designs "yield identical verdicts" | two cells change: A.W.T all designs 2020-23 (percentiles 2.7, 2.8, 2.5; below band only at n = 50) and A.U protected 2020-23 (3.0, 2.3, 2.6; below band only at n = 40) (PN-B item 5, `5_rarefaction_verdict_changes.csv`) | WRONG (and contradicts 04:160) |
| 03_methods:111 | filings rose from about 60 designs per cohort to 213 | 59 and 57; 213 | OK |
| 03_methods:113 | cohort labels permuted 10,000 times, seed 42 | `run_note.txt`: 10,000, seed 42 (notebooks 21-29 run 1,000; the figures and S4 use 10,000) | OK |
| 03_methods:122 | balance on ²D rarefied to 40 | as above | OK |
| 03_methods:158 | entrant = first time with a design, in whichever cohort | `frames.filers_by_window`, `analysis_v.py` L234: cohort of the first design, not first patent; individual inventors not entrants | OK |
| 03_methods:160 | weights drawn 1,000 times; coding changed with probability 0.15 in 1,000 replicas | weights: 1,000 draws OK. Coding: 1,000 replicas exist only at 1,000 permutations; the 10,000-permutation runs have 120 replicas (PN-A A1) | WRONG if the text means 10,000 permutations (S5:11 says so) |
| 04_results:12 | fuselage fixed in 85 % of designs; 87 % of winged aircraft standard wing | 84.6 %; 87.2 % (PN-D 13a) | OK |
| 04_results:12 | oval 64 % of designs, 19 % circular | 64.49 % of 597 (13a, unrounded 0.6449) ; circular 114/596 = 19.1 % | OK |
| 04_results:12 | largest propulsor interval 23 %; tailless 29 % | 22.9 %; 29.3 % | OK |
| 04_results:14 | 12 to 39 and 43 configurations | 12 / 39 / **44** (nb22 c16) | STALE |
| 04_results:14 | effective numbers (²D) rise from 7.3 to 16.4 and 29.3 | these are ¹D values of the 627 table. 621 dataset: ¹D 7.3 / 16.5 / 29.6; **²D 5.7 / 11.3 / 22.8** (`levels` table, `thesis_q7._data`) | WRONG (symbol and value) |
| 04_results:14 | largest configuration 26 %, 17 %, 10 % | 25.8 / **16.2** / 9.9 % (nb22 c16) | STALE (A.W.T) |
| 04_results:14 | last 100 designs: 4.1 against 1.6, p = 0.058 | 4.18 against 1.44, **p = 0.0375** (whole-counts estimator; 0.007 by the other estimator); A.U 1.06 against 0.79, p 0.544 (`q6_discovery_last100_band.csv`, DC item 3). The verdict "not detected" at A.W.T flips at 5 % | STALE |
| 04_results:16 | ²D = 29.3 at A.U | ¹D 29.6; ²D 22.8 | WRONG |
| 04_results:21, 80 | at most 36 % (all) and 39 % (protected) | 36.2 % SLC 2020; 39.0 % CVT 2021 | OK (already fixed) |
| 04_results:30 | three largest hold 13-24 % in 2016-19 and 21-32 % in 2020-23; together 60 % and 75 % | 13.2-23.9; 20.7-31.6; 59.6; 74.7 | OK |
| 04_results:30 | largest configuration 19 % and 11 % in 2020-23 | 19.1 %, 10.6 % (all designs). Protected: 18.8 %, 10.5 % | OK |
| 04_results:40-46 | Table 5 ticks | S4 tables: all designs A met/met, A.W.T not/met, A.U not/met; protected balance met at three levels, disparity met | OK |
| 04_results:51 | 4.8, 4.9, 5.9, 4.55 (percentile 0.2); A.W.T percentile 2.8; A.U 9.5; protected 0.2, 0.8, 2.3 | 4.80, 4.90, 5.93, 4.55 (0.2); 2.8; 9.5; 0.2, 0.8, 2.3 (s31) | OK |
| 04_results:76 | all designs dQ -0.026, edge -0.022, 1.2 %; protected earliest -0.034, -0.046; percentiles 0.6 to 0.9 | -0.0257, -0.0218, 1.2; -0.0335, -0.0464; 0.9, 0.6, 0.7 | OK |
| 04_results:92 | SLC 48 %; TP single tilting set 75 % to 31 %; CVT boom units 20 % to 62 %, Holm n.s. | 48.0 %; 75.0 % (<=2011) to 30.6 % (2020-23) (nb24 c7); 0.20 to 0.62, Holm 0.099 (nb24 c14) | OK |
| 04_results:92 | median propulsors 2 to 4 (TP), 4 to 6 (CVT); tilting sets rho 0.22 / 0.25, Holm 0.020; propulsive units TP rho 0.41, Holm <0.001; CVT 0.31, 0.004 | same (`q6_driver_trends.csv`, `q6_architecture_traces_by_cohort.csv`) | OK |
| 04_results:115 | ducts fall 35 % to 6 % | 0.353 to 0.061 (nb24 c20) | OK |
| 04_results:117 | F 49.3 %, 56.9 %; protected 51.8 %, 59.3 % | same (nb23 c14, c20) | OK |
| 04_results:133 | 198 companies and universities; 130 filed one design | 198 named assignees; 130 of 198 (NV) | OK |
| 04_results:133 | no assignee above 24 % of an architecture with 20+ designs; removing Bell moves a share by 2.6 points | 24 % (Tilt Frame, Bell, 25 designs); `lev1_pp` 2.6 (NV) | OK |
| 04_results:133 | individual inventors 68 % (40/59) to 24 % (56/237); new companies 14, 19 to 58, 81; entrants file 63 % and 65 % | 40/59; 56/237; 14, 19, 58, 81; `first_share` 63 %, 65 % (NV) | OK |
| 04_results:135 | North America tilting 67 %, 60 % without Bell; F 48, 57, 46 %; Asia-Pacific 18 % to 39 % | 66.8, 60.3; 48.05, 57.14, 45.65; 17.8, 38.8 | OK |
| 04_results:147 | margin 0.004; sign negative 99.0 % and 99.3 %; below band 69 % and 74 % | 0.0039; 0.990, 0.993; 0.693, 0.739 (W1, `test1_draws.csv`) | OK |
| 04_results:149 | negative verdicts hold in 99.7 to 100 % of replicas | rule of the Methods (120 replicas, 10,000 perms): 100 % on all share rows; first version 99.2 %; 1,000-replica reference 97.5 to 100 % | NOT FOUND (exact 99.7) |
| 04_results:149 | decline of Tilt Propulsor holds in 73 % | **55 %** (rule of the Methods, 120 replicas); 57.7 % (1,000 replicas, 1,000 perms); 74 % is the first version | STALE |
| 04_results:149 | standard wing 0.87 to 0.74 | 0.87 to **0.75** (0.72-0.77) | STALE |
| 04_results:149 | disparity met in 13 to 18 % of replicas | **14 to 23 %** (rule of the Methods); first version 11 to 23 % | STALE |
| 04_results:149 | F meets three conditions on protected designs in 0.9 % | **0.8 %** (1/120); first version 0.0 %; 1,000-replica run 0.2 % | STALE |
| 04_results:149 | 10 % architecture disagreement vs built aircraft | 10/97 (CA) | OK |
| 04_results:151 | F alone: dQ +0.045 and +0.010; no draw below band; -0.035 against -0.039, 0.004 short, 33 % of draws | 0.0453, 0.0098; 0 of 1,000; -0.0354, -0.0392, 0.0037; 0.329 (W2) | OK |
| 04_results:151 | architecture kept: +0.038, +0.019 against earliest, -0.019 against 2016-19, edge -0.038; CVT* share 31 % to 36 % | -0.0191, -0.0376 (W2 since-peak); 31.4 % to 35.9 %. +0.038/+0.019 are not stored; they are consistent with Q 0.4058/0.3867 and a baseline 0.3678 | OK (+0.038, +0.019 derived, not stored) |
| 04_results:151 | wing configuration below band; tractor/pusher "just reaches"; propulsor interval "close"; no dimension below band against the earliest | margins +0.034, +0.003, -0.007; none (fig 8 data) | OK (tractor/pusher listed, see below) |
| 04_results:160 | rarefying to 30 or 50 changes only A.W.T 2020-23 | two cells (see 03_methods:107) | WRONG |
| 04_results:72, 129, 156 | captions: protected designs are "dashed lines with hollow markers" | the regenerated figures draw protected designs as solid blue lines with filled markers; dashed grey hollow = untested 2024-26. Fig 8 has circles (2016-19) and squares (2020-23) with band-edge ticks, no all/protected lines | WRONG (caption vs figure) |
| 06_conclusions:9 | entrants "with no aircraft patents before their first eVTOL filing" | the code counts the first design in the dataset, not any earlier patent (`analysis_v.py` L234) | WRONG (definition) |
| S1:59-67 Table S1 | answering 595, 600, 595, 603, 547, 602, 541 | 589 (units), 594 (tail), 589 (mount), 597 (shape), 542 (wings), 596 (kinematics), 537 (wing conf.) (PN-D 13a) | STALE (the file's own todo says 627) |
| S1:62 | boom count 619, 5 options, 54 % | 619, 5, 53.8 % | OK (already fixed) |
| S1:63 | enclosure 63 % | 63.50 % printed, unrounded 0.63498 | OK |
| S1:64 | fuselage shape 64 % | unrounded 0.6449 | OK |
| S1:65 | number of wings 66 % | **65.3 %** | STALE |
| S1:61 | mount locations 4 options | 4 stations (D13a) | OK |
| S1:67 | wing configuration 5 options | 6 options (W, Oth, BWB, LB, FW, Unknown) (D13a) | WRONG (6) |
| S1:59-60, 66 | 23 %, 29 %, 85 %, 87 %; options 5, 13, 4 | 22.9, 29.3, 84.6, 87.2; 5, 13, 4 | OK |
| S1:72 | wing positions 514 (61 %), 514 (68 %), 532 (62 %); tilt share 588 (42 %); tractor/pusher 522 (95 %) | 514/60.7, 514/68.1, 532/61.8, 588/42.5, 522/95.4 | OK; tilt share ROUNDING (43 %); tractor/pusher: known wrong |
| S1:72 | landing gear 68 % Unknown | `core.py` note, thesis II.1 | OK |
| S1:86-88 Table S1 levels | configurations 12, 39, 43 | 12, 39, **44** | STALE |
| S1:86-88 | singletons 0, 10, 3 | 0, 10, **4** | STALE |
| S1:86-88 | effective number 7.3, 16.4, 29.3 | ¹D 7.3, 16.5, 29.6 (²D 5.7, 11.3, 22.8); header "Effective number" does not say which order | STALE |
| S1:86-88 | largest 26 %, 17 %, 10 % | 26, **16**, 10 % (TP 1-3 units 9.9 %) | STALE |
| S1:106-117 | twelve locks | `D2_15_locks.csv`: 12 | OK |
| S2:5 | 1,639 families, 8 June 2026 | funnel | OK |
| S2:45 | script flagged 522 of 1,639; coder corrected 322; thresholds 0.05 and 0.45 | thesis text (Methods 3.3, 1,639 families): 522 flagged, flags of 322 corrected, thresholds 0.05 and 0.45. Not recomputed for the 621 dataset | OK (thesis) |
| S2:48 | 68 % relevance, 72 % completeness | see 03_methods:76 | NOT FOUND (72) |
| S2:50 | 68 of 100 (68.0 %, +-8.9); 1,109 of 1,639 (67.7 %); 879 of 1,639 (53.6 %) | 68 of 100 (thesis); **1,108** (67.6 %); **876** (53.4 %) in the 621 dataset | STALE |
| S2:52 | reference set of 56 patents | thesis gold standard v1 has 56 (34 same number, ...). The 72 % does not come from it (see above) | NOT FOUND (72) |
| S2:59 | chi-square p < 0.001; adjusted residuals -10.7 and +9.9 | -10.7 (wingless) and **+10.1** (vectored thrust) (`q4_dataset_vs_directory_classes.csv`) | STALE (+9.9) |
| S2:59 | multicopters 8 % against 30 % | 7.6 %; 30.4 % (265/871) | OK |
| S2:59 | 5 % (3 of 56) in the reference set | 3 of 56 not stored | NOT FOUND |
| S2:59 | 83 of the 94 directory aircraft, p = 0.571 | thesis: of the 97 named designs, 94 are in the VFS directory and 83 are inside the domain rules of the directory (p 0.571 on the 627 table). 621 dataset: 83 linked, chi-square 3.2, **p = 0.527** | 94 and 83 OK; p STALE (0.527) |
| S2:76 | 97 matched, 87 agree, kappa 0.87; coder consulted drawings for 11 of 97 | CA: 87/97, 0.87. Thesis: in 11 of the 97 the text did not state the architecture and the coder used the drawing | OK |
| S2:86 | drawing vs aircraft 87, 0.90, 0.83-0.94, 0.87 | same (CA) | OK |
| S2:87 | text vs aircraft 89, 0.92, 0.85-0.96, 0.90 | **88**, 0.91, 0.84-0.95, **0.89** (CA) | STALE |
| S2:88 | drawing vs text 93, 0.96, 0.91-0.98, 0.95 | **94**, 0.97, 0.92-0.99, **0.96** (CA) | STALE |
| S2:101-102 | 2 and 8 | 1 and 9 (R59_D2_ten_disagreements.csv) | STALE |
| S2:110 | 90 % of 2023 published; 98 % of 2022; 89 % of 2023; 90 % within three years | 89.7 % (or 88.9 %); 98.5 %; 89.7 %; p90 3 years | ROUNDING (90 vs 89 inside the same paragraph) |
| S3:9 | 40 designs, 1,000 subsamples, 40 subsamples per permutation, cohorts under 10 excluded | `balance_band(n=40, obs_draws=1000, perm_draws=40, min_aircraft=10)` | OK |
| S3:29-33 | worked example 0.047 | 0.1000 + 0.0875 = 0.1875 / 4.000 = 0.0469 | OK |
| S3:44-56 Table S3 weights | 1.000, 0.500, 0.300, 0.200, 0.300, 0.300, 0.333, 0.022, 0.350, 0.300, 0.150, 0.100, 0.100 | `D13b_table_S1_distance_dimensions.csv` | OK (tractor/pusher listed below) |
| S3:62 | 10,000 shuffles, seed 42 | `run_note.txt` | OK |
| S3:75 | propulsors per design TP +0.41 (<0.001), CVT +0.31 (0.004) | 0.41 (0.000002), 0.31 (0.004) | OK |
| S3:76 | tilting sets TP +0.22 (0.020), CVT +0.25 (0.020) | 0.22 (0.0198), 0.25 (0.0198) | OK |
| S3:77 | tilting sets per propulsor TP -0.32 | rho -0.32, raw p 0.0001 on the 621 dataset (`thesis_q6._data(ctx)["spu"]`; means 0.50, 0.59, 0.46, 0.39) | OK (Holm < 0.001) |
| S3:78 | propulsors on booms SLC +0.10, TP +0.11, CVT +0.22 | SLC **0.05**, TP 0.11, CVT 0.22 (`units carried on booms`) | WRONG (SLC) |
| S4:8-89 Tables S-all, S-prot, S-protall | 288 values + 4 rows | all match (machine check) | OK |
| S4:4, 91, 93 | 18 and 32 designs; percentiles 0.2, 2.8, 9.5; 0.2, 0.8, 2.3; 0.9 and 0.1 | match | OK |
| S4:4, 91, 93 | stray "[cite: 5, 6, 7]" tokens in the text | | WRONG (leftover markup) |
| S5:1 | line starts with a stray "5" before `\section` | | WRONG (typo) |
| S5:6 | factor exp(e), e ~ N(0, 0.35^2); 90 % between 0.56 and 1.78; 1,000 draws; 10,000 perms | exp(+-1.645 x 0.35) = 0.56 to 1.78 | OK |
| S5:8 | 99.0 %, 69 %; 78 %, 79 %; 74, 83, 84 %; margins 0.0035 to 0.0079; 5th percentile negative | 0.990, 0.693; 0.780, 0.790; 0.739, 0.829, 0.841; 0.00351 to 0.00788; all negative | OK |
| S5:8 | equal weights margin -0.008 to -0.014 | margins -0.0070 to -0.0081; -0.0114 to -0.0143 are the dQ values, not the margins | WRONG |
| S5:8 | upper Wilson bound 0.4 % | 0.0038 | OK |
| S5:11 | all analyses on 1,000 replicas, 10,000 permutations | 120 replicas at 10,000; 1,000 replicas at 1,000 (PN-A A1) | WRONG |
| S5:11 | redrawn up to 20 times if a lock is violated; label shifts for 7.3 % (100 replicas) | that is the first version (7.4 %, 120 replicas). Rule of the Methods (allowed values): **14.9 %** (71-121 of 621), 120 replicas | STALE |
| S5:11 | "double-coding audit" of 97 aircraft, kappa 0.87 to 0.96, 3 to 10 % | it is the comparison of drawing, text and built aircraft (CA: kappa 0.87, 0.89, 0.96; disagreement 3 % to 10 %); 04:162 says a second independent coding is still to be done | WRONG (label) |
| S5:13 | 0.87 to 0.74; dQ median -0.009; below band 14 %; F median 46.3 %; 0.9 %; fails share 99.7 % | 0.75; **-0.011** (A, all); **19 %** (A), 14 % (A.U); **42.6 %**; **0.8 %**; **100 %** (first version 99.2 %) | STALE |
| S5:24-33 Table S5 | 36 % at most / 100 % | 36.2 %; 100 % | OK |
| S5:25, 27, 31 | coding cells `\todo{--}` | A2: balance A 57.5 %; disparity below band A 19.2 %; F three conditions (protected) 0.8 % | NOT FILLED |
| S5:26 | dQ < 0, A: 99.0 % weights, 88 % coding | 99.0 % OK; coding: 89 % (120 replicas, 10,000 perms), 88 % (1,000 replicas, 1,000 perms) (`replicas.jsonl`) | OK |
| S5:28 | TP share falls: rho -0.69, 73 % | rho -0.685 OK; 55 % (73 % is first version 74 %) | STALE |
| S5:29-30 | propulsors rise TP 100 and 99 %; CVT 100 and 41 % | TP Holm 98 %; CVT Holm **38 %** (34 % at 1,000 replicas) | STALE |
| S5:31 | F meets three conditions, protected: weights 74 % | 74 % is the share of draws where **disparity** is below the band; the three conditions are "not computed" under weight draws (PN-A A2) | WRONG (label) |
| S5:32 | regions 98 to 99 % | 100 % (120) and 97.5-98.3 % (1,000) | OK |
| S5:33 | entrants differ, 90 to 91 % | **68 to 69 %** (first version 90 to 92.5 %) | STALE |
| S5:39 | rarefaction, variety threshold, window results | `\todo`: no content; cited from 04:107, 04:160, 03:107 | NOT FILLED |

## Extra checks

**1. Same number in several places.** Differences found: 2023 publication share 90 % (03:17, S2:110) against 89 % (S2:110). Effective numbers 7.3 / 16.4 / 29.3 appear in 04:14, 04:16 and S1:88 (all stale, all labelled ²D or "effective number"). The 1,000 replicas appear in 03:160, 04:149, S5:11 (see above). Rarefaction "identical verdicts" in 03:107 against "unchanged but A.W.T" in 04:160. All other repeated numbers (36 and 39 %, 49.3 / 56.9 / 51.8 / 59.3, 4.55, 0.2 / 0.8 / 2.3, -0.026 / -0.022, 18 / 32, 213, 621, 876, 1,639) are identical everywhere.

**2. References.** Every "Supplementary Material, Section Sx" exists. Content checks: S1 table exists (03:85) but its answer counts are stale; 03:87 sends the reader to S1 for "the full test" of levels, and the row "Finer levels set aside" is `\todo`; 03:107 and 04:160 send the reader to S5 for rarefaction, variety and window results and S5:39 is `\todo`. Table 5 caption (04:33) says values and percentiles are in S4: true (all in Tables S-all, S-prot, S-protall). S0 section map matches.

**3. Protected numbers.** All protected values in the text and S4 are protected-design results (own n, own D2, own band; checked against the protected base of `percentiles_balance.csv`, e.g. 18 / 32 / 138 / 192 / 51 and F 51.8 % / 59.3 %). None is a copy of the all-designs value. Disparity for the protected base is read against the all-designs baseline and band, as the text says (S4 Table S-protall). Exception: S5:31 attributes the 74 % weight-draw share to "F meets the three conditions".

**4. No source found.** 522 / 322 triage counts and thresholds (S2:45); 72 % completeness and the sampled reference set (03:76, S2:48-52); 3 of 56 multicopters; "94 directory aircraft"; drawings consulted for 11 of 97 (S2:76); mount-locations and wing-configuration option counts in Table S1; tilting sets per propulsor -0.32 (S3:77); coding-replica 88 % (S5:26); the introduction's market figures (external citations).

## Where tractor/pusher (95 %) is used

- S1:72, "tractor/pusher arrangement for 522 (95 %)".
- S3:55, Table S3 weights, "Tractor / pusher arrangement ... 0.100".
- 03_methods:109, one of the "five further dimensions" (no value).
- 04_results:151, "the tractor or pusher arrangement just reaches it" (fig 8 reading; data: margin +0.0032, first-column of `test2_explore_since_peak.csv`).
- Fig 8 label "Tractor/pusher arrangement" (`fig7c_F_disparity_within.pdf`).
