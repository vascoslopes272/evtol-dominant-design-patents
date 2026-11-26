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
