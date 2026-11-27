# NUMBERS_III — Analysis III (dominant design)

Written by notebook 23_dominant_design (`viz/thesis_latex_part3.py`); every value is recomputed when the notebook runs. Dataset: the public eVTOL_dataset, 621 designs (619 with an architecture). CSVs are in `Data_for_writing/csv/`.

## (a) III.1, cohort shares of Tilt Propulsor and Lift + Cruise

Source: `q6_architecture_shares_by_cohort.csv` (share of the cohort's designs).

| cohort   |   designs | Tilt Propulsor   | Lift + Cruise   |
|:---------|----------:|:-----------------|:----------------|
| <= 2011  |        59 | 33.9 %           | 22.0 %          |
| 2012-15  |        57 | 35.1 %           | 15.8 %          |
| 2016-19  |       213 | 23.9 %           | 22.5 %          |
| 2020-23  |       237 | 20.7 %           | 31.6 %          |
| 2024–26* |        55 | 21.8 %           | 27.3 %          |

## III.1, Spearman rho of share on priority year (2008–2023)

Source: `q6_share_trend_spearman.csv`.

| architecture code   | architecture             |   designs |   years |    rho |     p |   p (Holm) |   rho, 2016-23 |   p, 2016-23 |   p, 2016-23 (Holm) |
|:--------------------|:-------------------------|----------:|--------:|-------:|------:|-----------:|---------------:|-------------:|--------------------:|
| SLC                 | Lift + Cruise            |       142 |      16 |  0.443 | 0.09  |      0.43  |          0.515 |         0.19 |                   1 |
| TP                  | Tilt Propulsor           |       133 |      16 | -0.685 | 0.003 |      0.024 |         -0.452 |         0.26 |                   1 |
| CVT                 | Combined Vectored Thrust |        93 |      16 |  0.256 | 0.34  |      1     |          0.548 |         0.16 |                   1 |
| TW                  | Tilt Wing                |        49 |      16 | -0.144 | 0.59  |      1     |         -0.357 |         0.39 |                   1 |
| MR                  | Multicopter              |        36 |      16 |  0.155 | 0.57  |      1     |         -0.476 |         0.23 |                   1 |
| TF                  | Tilt Frame               |        23 |      16 |  0.001 | 1     |      1     |         -0.405 |         0.32 |                   1 |
| PTC                 | Pitch-to-Cruise          |        22 |      16 |  0.474 | 0.06  |      0.38  |          0.204 |         0.63 |                   1 |

## (b) III.4, VT on the five directory categories, actively protected designs

Source: `q7_iii4_directory_categories.csv` (balance), notebook 23_dominant_design §III4. VT is the largest category in every year and cohort. Fold: `q7_iii4_directory_fold.csv`.

VT share per cohort:

| cohort   |   actively protected designs |   VT designs | VT share   |
|:---------|-----------------------------:|-------------:|:-----------|
| <= 2011  |                           18 |           10 | 55.6 %     |
| 2012-15  |                           32 |           24 | 75.0 %     |
| 2016-19  |                          138 |           83 | 60.1 %     |
| 2020-23  |                          192 |          114 | 59.4 %     |
| 2024–26* |                           51 |           30 | 58.8 %     |

VT share per priority year (read years, 20 designs or more, 2016–2023); condition 1 met in 2016, 2017, 2018, 2019, 2021, 2022, 2023 (all designs: 2016, 2017, 2021, 2022, 2023):

|   priority year |   aircraft |   its aircraft | share   | above 50 %   |
|----------------:|-----------:|---------------:|:--------|:-------------|
|            2016 |         24 |             13 | 54.2 %  | True         |
|            2017 |         33 |             24 | 72.7 %  | True         |
|            2018 |         37 |             20 | 54.0 %  | True         |
|            2019 |         44 |             26 | 59.1 %  | True         |
|            2020 |         54 |             25 | 46.3 %  | False        |
|            2021 |         59 |             40 | 67.8 %  | True         |
|            2022 |         35 |             23 | 65.7 %  | True         |
|            2023 |         44 |             26 | 59.1 %  | True         |

Balance (²D rarefied to 40, all designs, 1000 permutations) with the band, per cohort; 2024–26* is incomplete and not read:

| cohort            |   aircraft |   D2 |   D2 permutation low |   D2 permutation high | below band   |
|:------------------|-----------:|-----:|---------------------:|----------------------:|:-------------|
| <= 2011           |         59 | 2.81 |                 1.77 |                  2.83 | False        |
| 2012-15           |         57 | 1.92 |                 1.81 |                  2.82 | False        |
| 2016-19           |        211 | 2.34 |                 2.05 |                  2.54 | False        |
| 2020-23           |        237 | 2.18 |                 2.08 |                  2.51 | False        |
| 2024-26 (partial) |         55 | 2.37 |                 1.83 |                  2.87 | False        |

## Verdict table (each base read alone: all designs is the main reading, actively protected the sensitivity; condition 3 under the w15 weighting, on the actively protected base against the all-designs baseline and band)

Source: `q7_verdict_table.csv`.

| base               | condition                                                                             | A                                | A·W·T                            | A·U                              | F                                       |
|:-------------------|:--------------------------------------------------------------------------------------|:---------------------------------|:---------------------------------|:---------------------------------|:----------------------------------------|
| all designs        | 1, counts: one architecture above 50 % of the designs, two consecutive priority years | ✗ not met, at most 36.2 % (2020) | ✗ not met, at most 27.3 % (2018) | ✗ not met, at most 19.4 % (2021) | ✗ not met, at most 56.9 % (2021)        |
| all designs        | 2, balance: ²D below the permutation band                                             | ✓ met in 2020-23                 | ✗ not met                        | ✓ met in <= 2011, 2012-15        | ✓ met in 2020-23                        |
| all designs        | 3, form: Q below the two earliest cohorts by more than the band                       | ✓ met in 2020-23                 | ✓ met in 2020-23                 | ✓ met in 2020-23                 | ✓ met in 2020-23                        |
| all designs        | all three in the same period                                                          | ✗ not met                        | ✗ not met                        | ✗ not met                        | ✗ not met                               |
| actively protected | 1, counts: one architecture above 50 % of the designs, two consecutive priority years | ✗ not met, at most 39.0 % (2021) | ✗ not met, at most 27.1 % (2021) | ✗ not met, at most 23.7 % (2021) | ✓ met in 2020 and 2021 (51.8 %, 59.3 %) |
| actively protected | 2, balance: ²D below the permutation band                                             | ✓ met in 2020-23                 | ✓ met in <= 2011, 2020-23        | ✓ met in <= 2011, 2012-15        | ✓ met in 2020-23                        |
| actively protected | 3, form: Q below the two earliest cohorts by more than the band                       | ✓ met in 2020-23                 | ✓ met in 2020-23                 | ✓ met in 2020-23                 | ✓ met in 2020-23                        |
| actively protected | all three in the same period                                                          | ✗ not met                        | ✗ not met                        | ✗ not met                        | ✓ met in 2020-23                        |

## The numbers behind the verdict

Source: `q7_verdict_detail.csv`. Condition 1: the largest share of a read year (20 designs or more) and the years met; condition 2: ²D rarefied to 40 and the lower edge of its band; condition 3: ΔQ 2020-23 of the form distance under w15 (15 dimensions, each of the four systems weighing 1) and the lower edge of its band (1000 permutations, seed 42); on the actively protected base against the all-designs baseline and band (§3.4.4, table 'Condition 3, actively protected against the all-designs baseline'), its own-baseline values in the last two columns.

| base               | level   | condition 1: largest share   |   condition 1: its year | condition 1: years met   | condition 1: share 2020 (n of N)   | condition 1: share 2021 (n of N)   |   ²D <= 2011 |   ²D lower band edge <= 2011 |   ²D 2012-15 |   ²D lower band edge 2012-15 |   ²D 2016-19 |   ²D lower band edge 2016-19 |   ²D 2020-23 |   ²D lower band edge 2020-23 |   ΔQ 2020-23 |   ΔQ lower band edge 2020-23 | condition 3 baseline   |   ΔQ 2020-23, own baseline |   ΔQ lower band edge 2020-23, own baseline |
|:-------------------|:--------|:-----------------------------|------------------------:|:-------------------------|:-----------------------------------|:-----------------------------------|-------------:|-----------------------------:|-------------:|-----------------------------:|-------------:|-----------------------------:|-------------:|-----------------------------:|-------------:|-----------------------------:|:-----------------------|---------------------------:|-------------------------------------------:|
| all designs        | A       | 36.2 %                       |                    2020 | none                     | 36.2 % (25 of 69)                  | 33.3 % (24 of 72)                  |         4.8  |                         4.11 |         4.9  |                         4.1  |         5.93 |                         4.75 |         4.55 |                         4.75 |      -0.0257 |                      -0.0223 | all designs            |                    -0.0257 |                                    -0.0223 |
| all designs        | A·W·T   | 27.3 %                       |                    2018 | none                     | 24.6 % (17 of 69)                  | 23.6 % (17 of 72)                  |         8.17 |                         7.02 |         7.98 |                         7.11 |        10.55 |                         8.29 |         8.36 |                         8.31 |      -0.0277 |                      -0.0209 | all designs            |                    -0.0277 |                                    -0.0209 |
| all designs        | A·U     | 19.4 %                       |                    2021 | none                     | 14.5 % (10 of 69)                  | 19.4 % (14 of 72)                  |        11.17 |                        12.01 |         9.91 |                        11.91 |        16.26 |                        13.91 |        14.49 |                        13.95 |      -0.0277 |                      -0.0218 | all designs            |                    -0.0277 |                                    -0.0218 |
| all designs        | F       | 56.9 %                       |                    2021 | none                     | 49.3 % (34 of 69)                  | 56.9 % (41 of 72)                  |         4.07 |                         3.06 |         4.73 |                         3.01 |         4.82 |                         3.6  |         3.25 |                         3.66 |      -0.0257 |                      -0.0223 | all designs            |                    -0.0257 |                                    -0.0223 |
| actively protected | A       | 39.0 %                       |                    2021 | none                     | 38.9 % (21 of 54)                  | 39.0 % (23 of 59)                  |         3    |                         2.95 |         3.85 |                         3.53 |         6.02 |                         4.48 |         4.4  |                         4.6  |      -0.0287 |                      -0.0231 | all designs            |                     0.0112 |                                    -0.0225 |
| actively protected | A·W·T   | 27.1 %                       |                    2021 | none                     | 24.1 % (13 of 54)                  | 27.1 % (16 of 59)                  |         4.15 |                         4.76 |         6.4  |                         6.17 |        11.37 |                         8.28 |         8.27 |                         8.48 |      -0.0313 |                      -0.022  | all designs            |                     0.0086 |                                    -0.0212 |
| actively protected | A·U     | 23.7 %                       |                    2021 | none                     | 16.7 % (9 of 54)                   | 23.7 % (14 of 59)                  |         5.59 |                         7.04 |         7.31 |                         9.85 |        16.42 |                        13.43 |        13.84 |                        13.82 |      -0.0313 |                      -0.0234 | all designs            |                     0.0086 |                                    -0.0234 |
| actively protected | F       | 59.3 %                       |                    2021 | 2020, 2021               | 51.8 % (28 of 54)                  | 59.3 % (35 of 59)                  |         2.84 |                         2.28 |         3.76 |                         2.68 |         5.12 |                         3.4  |         3.14 |                         3.49 |      -0.0287 |                      -0.0231 | all designs            |                     0.0112 |                                    -0.0225 |

## Weights table (condition 3, the reported weighting w15: 15 dimensions of the codebook, each of the four systems weighing 1, 4 in all)

Source: `q7_condition3_weights.csv`; 15 dimensions, 619 designs (2 without an architecture recorded are left out). Eleven dimensions are compared as options (0 same, 1 different); three are ordered and compared by rank difference over a fixed range: boom count (0 when no boom, 1, 2, 3 to 4, 5 or more; / 4), wing count (0 when no wing, 1, 2, 3; / 3) and the band of propulsors (1 to 3, 4, 5 to 6, 7 to 8, 9 or more; / 4, the bands of A·U); the tilt share is the share 0 to 1 of the design's propulsors whose thrust turns between hover and cruise (a propulsor that pivots on its mount, sits on a tilting wing, a tilting empennage or a tilting boom, or a Tilt Body design, which turns whole), compared by absolute difference; the mount locations are the set of stations carrying propulsors among fuselage, wing, boom and empennage, compared by Jaccard distance (the share of the stations used by either design that only one of them uses). The three wing dimensions read wing 1 (the primary wing of codebook R5-03, which is wing 1 in every design: the author checked the designs whose role reading pointed to wing 2); enclosure and tractor/pusher arrangement read the set with the most propulsors (first listed on a tie); a dimension that does not apply or that an override hides is blank and left out of the pair's average, and the propulsion dimensions are blank for designs with no propulsor card (Hoverbike, Personal Flying Vehicle).

| system          | dimension                  | codebook field                                                           | compared as                                                                                     |   weight |
|:----------------|:---------------------------|:-------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------|---------:|
| G1 architecture | Architecture               | topType                                                                  | 0 same option, 1 different                                                                      |    1     |
| M1 structure    | Fuselage Shape             | fusShape                                                                 | 0 same option, 1 different                                                                      |    0.5   |
| M1 structure    | Boom count                 | boomsPresent, boom1..6_count                                             | ordered 0, 1, 2, 3 to 4, 5 or more; rank difference / 4                                         |    0.3   |
| M1 structure    | Fuselage Kinematics        | fusKin                                                                   | 0 same option, 1 different                                                                      |    0.2   |
| M2 aerodynamics | Wing count                 | wCount                                                                   | ordered 0, 1, 2, 3; difference / 3                                                              |    0.3   |
| M2 aerodynamics | Wing Architecture          | wingConf                                                                 | 0 same option, 1 different                                                                      |    0.3   |
| M2 aerodynamics | Vertical Position          | wing1_posV                                                               | 0 same option, 1 different                                                                      |    0.022 |
| M2 aerodynamics | Longitudinal Position      | wing1_posL                                                               | 0 same option, 1 different                                                                      |    0.022 |
| M2 aerodynamics | Planform                   | wing1_plan                                                               | 0 same option, 1 different                                                                      |    0.022 |
| M2 aerodynamics | Empennage Type             | empType                                                                  | 0 same option, 1 different                                                                      |    0.333 |
| M3 propulsion   | Propulsor band             | propulsor_units                                                          | ordered 1 to 3, 4, 5 to 6, 7 to 8, 9 or more; rank difference / 4                               |    0.35  |
| M3 propulsion   | Tilt share                 | <station>_count, propKin, wing tilt, empTilts, boom_thrust_state, fusKin | share 0 to 1 of the propulsors whose thrust turns between hover and cruise; absolute difference |    0.3   |
| M3 propulsion   | Propulsor Enclosure        | <set>_bmech                                                              | 0 same option, 1 different (the set with the most propulsors)                                   |    0.15  |
| M3 propulsion   | Tractor/Pusher Arrangement | <set>_chord                                                              | 0 same option, 1 different (the set with the most propulsors)                                   |    0.1   |
| M3 propulsion   | Mount locations            | <station>_count                                                          | stations carrying propulsors among fuselage, wing, boom, empennage; Jaccard distance            |    0.1   |
| total           | 15 dimensions              |                                                                          |                                                                                                 |    4     |

## Condition 3 on F (the same w15 weights; Q on the designs of F's base, per cohort)

Source: `q7_condition3_family.csv`. Q uses no architecture, so F on all designs is the same set as A.

| base               | cohort            |   designs |      Q |   Q of the earliest cohorts |      ΔQ |   ΔQ permutation low |   ΔQ permutation high | below band   | partial   |
|:-------------------|:------------------|----------:|-------:|----------------------------:|--------:|---------------------:|----------------------:|:-------------|:----------|
| actively protected | <= 2011           |        18 | 0.5107 |                      0.5043 |  0.0064 |              -0.0478 |                0.0336 | False        | False     |
| actively protected | 2012-15           |        32 | 0.4978 |                      0.5043 | -0.0064 |              -0.0336 |                0.0478 | False        | False     |
| actively protected | 2016-19           |       138 | 0.5731 |                      0.5043 |  0.0688 |              -0.0238 |                0.0661 | False        | False     |
| actively protected | 2020-23           |       192 | 0.5154 |                      0.5043 |  0.0112 |              -0.0225 |                0.0695 | False        | False     |
| actively protected | 2024-26 (partial) |        51 | 0.5399 |                      0.5043 |  0.0357 |              -0.0401 |                0.0688 | False        | True      |
| all designs        | <= 2011           |        59 | 0.5547 |                      0.5442 |  0.0105 |              -0.0242 |                0.0238 | False        | False     |
| all designs        | 2012-15           |        57 | 0.5336 |                      0.5442 | -0.0105 |              -0.0238 |                0.0242 | False        | False     |
| all designs        | 2016-19           |       211 | 0.5682 |                      0.5442 |  0.024  |              -0.0225 |                0.0373 | False        | False     |
| all designs        | 2020-23           |       237 | 0.5185 |                      0.5442 | -0.0257 |              -0.0223 |                0.0361 | True         | False     |
| all designs        | 2024-26 (partial) |        55 | 0.548  |                      0.5442 |  0.0038 |              -0.0426 |                0.0406 | False        | True      |
| granted and live   | <= 2011           |        18 | 0.5107 |                      0.5051 |  0.0056 |              -0.0447 |                0.0318 | False        | False     |
| granted and live   | 2012-15           |        31 | 0.4994 |                      0.5051 | -0.0056 |              -0.0318 |                0.0447 | False        | False     |
| granted and live   | 2016-19           |       135 | 0.5751 |                      0.5051 |  0.07   |              -0.024  |                0.0677 | False        | False     |
| granted and live   | 2020-23           |       148 | 0.5046 |                      0.5051 | -0.0005 |              -0.0249 |                0.0699 | False        | False     |
| granted and live   | 2024-26 (partial) |        10 | 0.5488 |                      0.5051 |  0.0438 |              -0.1269 |                0.0563 | False        | True      |

## Condition 3, actively protected against the all-designs baseline

Source: `viz/analysis_iii.py` form_ap_vs_all (dissertation §3.4.4, III.2). Q of the actively protected designs of 2020-23; baseline = pooled Q of the two earliest cohorts of all designs; band: all designs shuffled 1000 times (seed 42), cohort sizes of all designs kept except 2020-23, which takes the size of its actively protected cohort; w15.

| level   | cohort   |   actively protected designs |      Q |   baseline (all designs, two earliest cohorts) |      ΔQ |   band low |   band high | below band   |
|:--------|:---------|-----------------------------:|-------:|-----------------------------------------------:|--------:|-----------:|------------:|:-------------|
| A       | 2020-23  |                          192 | 0.5154 |                                         0.5442 | -0.0287 |    -0.0231 |      0.036  | True         |
| A·W·T   | 2020-23  |                          191 | 0.5128 |                                         0.5442 | -0.0313 |    -0.022  |      0.0356 | True         |
| A·U     | 2020-23  |                          191 | 0.5128 |                                         0.5442 | -0.0313 |    -0.0234 |      0.0366 | True         |
| F       | 2020-23  |                          192 | 0.5154 |                                         0.5442 | -0.0287 |    -0.0231 |      0.036  | True         |

## Three-year check (condition 1, three consecutive years, actively protected designs)

Source: `q7_three_year_check.csv`.

| level   | years above 50 % in three consecutive years, actively protected designs   |
|:--------|:--------------------------------------------------------------------------|
| A       | none                                                                      |
| A·W·T   | none                                                                      |
| A·U     | none                                                                      |
| F       | none                                                                      |

## F on granted and live patents alone

Source: `q7_granted_live_condition1.csv`, `q7_granted_live_condition2.csv`.

|   priority year |   designs |   F designs |   share of F | read (20 designs or more)   |
|----------------:|----------:|------------:|-------------:|:----------------------------|
|            2016 |        24 |           6 |       0.25   | True                        |
|            2017 |        32 |           5 |       0.1562 | True                        |
|            2018 |        35 |          11 |       0.3143 | True                        |
|            2019 |        44 |          16 |       0.3636 | True                        |
|            2020 |        51 |          27 |       0.5294 | True                        |
|            2021 |        54 |          32 |       0.5926 | True                        |
|            2022 |        28 |          11 |       0.3929 | True                        |
|            2023 |        15 |           9 |       0.6    | False                       |

| cohort            |   designs |   ²D |   band, lower edge |   band, upper edge | below band   |
|:------------------|----------:|-----:|-------------------:|-------------------:|:-------------|
| <= 2011           |        18 | 2.84 |               2.19 |               6    | False        |
| 2012-15           |        31 | 3.92 |               2.65 |               5.69 | False        |
| 2016-19           |       135 | 5.1  |               3.46 |               4.68 | False        |
| 2020-23           |       148 | 2.98 |               3.51 |               4.65 | True         |
| 2024-26 (partial) |        10 | 3.33 |               1.85 |               5.56 | False        |

## III.4, which VT share the figure draws

`q7_iii4_directory_categories` draws VT's share per priority YEAR (left panel, condition 1: all designs solid, actively protected dashed, years under 20 designs hollow grey; the met years of each base as red bars), and ²D per COHORT against its band (right panel, condition 2, all designs). The per-cohort VT share above is not drawn; it is listed here for the text. Per-year values: the table 'VT share per priority year' above, also written to `Data_for_writing/csv/q7_iii4_vt_share_per_year.csv`. The same table on all designs (2008–2023): `Data_for_writing/csv/q7_iii4_vt_share_per_year_all.csv`.

## Designs per cohort: III.1 against the form distance of condition 3

Source: `q6_architecture_shares_by_cohort.csv` (`designs`), `q7_condition3_cohesion.csv` (`aircraft`, w15 weighting).

| cohort   |   designs in III.1 (denominator of the shares) |   designs in the form distance, A and F |   designs in the form distance, A·U |   designs in the form distance, A·W·T |   difference to A |
|:---------|-----------------------------------------------:|----------------------------------------:|------------------------------------:|--------------------------------------:|------------------:|
| <= 2011  |                                             59 |                                      59 |                                  59 |                                    59 |                 0 |
| 2012-15  |                                             57 |                                      57 |                                  57 |                                    57 |                 0 |
| 2016-19  |                                            213 |                                     211 |                                 211 |                                   211 |                 2 |
| 2020-23  |                                            237 |                                     237 |                                 236 |                                   236 |                 0 |
| 2024–26* |                                             55 |                                      55 |                                  55 |                                    54 |                 0 |

Why they differ: the shares of III.1 divide by every design of the cohort, including the designs with no architecture recorded (a bar segment 'no architecture recorded'), while the form distance needs an architecture to place a design in a level, so those designs are left out. The two designs without an architecture (`CN109263914A_ad1`, `CN109263949A_ad1`) have priority year 2018, so only 2016–19 differs (213 against 211). A·W·T drops further designs whose wings or tilt are not recorded.

## Numbers quoted by the Results text, III.1 (sub-question B)

Source: `viz/thesis_q6.py` numbers(ctx), notebook cell of the III1 group.

- `cvt_w4` = 22 %
- `lc_w1` = 22 %
- `lc_w4` = 32 %
- `three_w4` = 75 %
- `tp_w1` = 34 %
- `tp_w3` = 24 %
- `tp_w4` = 21 %
- `w1_n` = 59
- `w3` = 2016-19
- `w4_n` = 237

## Numbers quoted by the Results text, III.2 to III.4 (Q7, regions and external comparison left out)

Source: `viz/thesis_q7.py` numbers(ctx), notebook cells of the III2_III3 group.

- `w_last` = 2020-23
- `w_early` = 2012-15
- `w_mid` = 2016-19
- `w_first` = 2012
- `met_years` = 2020 and 2021
- `met_span` = 2020-21
- `met_first` = 2020
- `met_last` = 2021
- `t7_c_arch` = 12
- `t7_cwt_arch` = 39
- `t7_cu_arch` = 44
- `t7_f_arch` = 12
- `t7_c_d1` = 7.3
- `t7_cwt_d1` = 16.5
- `t7_cu_d1` = 29.6
- `t7_f_d1` = 6.3
- `t7_f_share` = 39 %
- `t7_slc_share` = 26 %
- `t7_cu_share` = 10 %
- `t7_cwt_share` = 16 %
- `t7_f_n` = 241
- `t7_cwt_largest` = Lift + Cruise · one wing · no tilting propulsor
- `t7_cu_largest` = Tilt Propulsor · 1-3 propulsor units
- `dd_year_min` = 20
- `dd_read_years` = eight
- `dd_first_read` = 2016
- `dd_first_read_all` = 2015
- `dd_last_year` = 2023
- `dd_first_year` = 2008
- `f_in_2020` = 51.8 %
- `f_in_2021` = 59.3 %
- `f_in_2022` = 42.9 %
- `f_in_2023` = 43.2 %
- `f_all_2020` = 49.3 %
- `f_all_2021` = 56.9 %
- `f_all_2022` = 47.9 %
- `f_in_2020_k` = 28 of 54
- `f_in_2021_k` = 35 of 59
- `f_all_2020_k` = 34 of 69
- `gl_2020` = 94 %
- `gl_2021` = 92 %
- `gl_2022` = 80 %
- `gl_2023` = 34 %
- `f_gl_2020` = 53 %
- `f_gl_2021` = 59 %
- `lapse_2022` = 23.8 %
- `lapse_2023` = 56.5 %
- `max_rest` = 39.0 %
- `max_c` = 39.0 %
- `max_cwt` = 27.1 %
- `max_cu` = 23.7 %
- `max_c_year` = 2021
- `max_c_arch` = Combined Vectored Thrust
- `f_d2_last` = 3.25
- `f_d2_edge` = 3.66
- `c_d2_last` = 4.55
- `c_d2_edge` = 4.75
- `cu_d2_w1` = 11.17
- `cu_d2_w1_edge` = 12.01
- `cu_d2_w2` = 9.91
- `cu_d2_w2_edge` = 11.91
- `dq_main` = −0.026
- `dq_main_edge` = −0.022
- `top3_cwt` = 47 %
- `top3_cu` = 26 %
- `rarefy_n` = 40
- `perms` = 1000
- `seed` = 42
- `f_ap_d2` = 3.14
- `f_ap_d2_edge` = 3.49
- `dq_ap` = −0.029
- `dq_ap_edge` = −0.023
- `f_all_short` = 1
- `max_c_all` = 36.2 %
- `dq_f_all` = −0.026
- `dq_f_all_edge` = −0.022

## III.1 without Bell / Textron

Written by notebook 29_dominant_design_without_one_assignee (`viz/followup_iii1.py`). The III.1 frames and rules unchanged (`viz/analysis_iii.rho_table`, `frames.class_counts_by_window`): cohort shares over every design of the cohort; Spearman rho of each architecture's yearly share on the priority year over 2008-2023 (16 years) and 2016-2023 (8 years); the same 7 architectures (20 designs or more, all assignees) and the same Holm family per span as III.1. Every design whose assignee is Bell / Textron leaves numerator and denominator. Spearman draws nothing at random, so the seed plays no part. No figure is changed. Table: `csv/q7_iii1_without_bell.csv`.

### 1. Bell / Textron's designs per cohort and architecture

60 designs, 27 of them Tilt Propulsor. In 2016-19, 17 of the cohort's 51 Tilt Propulsor designs (33.3 %) are Bell / Textron's.

| cohort            | Combined Vectored Thrust   | Hoverbike   | Multicopter   | Lift + Cruise   | Tilt Frame   | Tilt Propulsor   | Tilt Wing   | all architectures   |
|:------------------|:---------------------------|:------------|:--------------|:----------------|:-------------|:-----------------|:------------|:--------------------|
| <= 2011           | 0                          | 0           | 0             | 0               | 0            | 2                | 0           | 2                   |
| 2012-15           | 0                          | 0           | 0             | 0               | 0            | 2                | 0           | 2                   |
| 2016-19           | 6                          | 1           | 1             | 0               | 5            | 17               | 3           | 33                  |
| 2020-23           | 11                         | 0           | 0             | 1               | 1            | 5                | 4           | 22                  |
| 2024-26 (partial) | 0                          | 0           | 0             | 0               | 0            | 1                | 0           | 1                   |
| all cohorts       | 17                         | 1           | 1             | 1               | 6            | 27               | 7           | 60                  |

### 2. Tilt Propulsor share per cohort (share of every design of the cohort)

2024-26 is a partial cohort and is not read.

| cohort            | all assignees      | without Bell / Textron   |
|:------------------|:-------------------|:-------------------------|
| <= 2011           | 20 of 59 (33.9 %)  | 18 of 57 (31.6 %)        |
| 2012-15           | 20 of 57 (35.1 %)  | 18 of 55 (32.7 %)        |
| 2016-19           | 51 of 213 (23.9 %) | 34 of 180 (18.9 %)       |
| 2020-23           | 49 of 237 (20.7 %) | 44 of 215 (20.5 %)       |
| 2024-26 (partial) | 12 of 55 (21.8 %)  | 11 of 54 (20.4 %)        |

### 3. Tilt Propulsor, Spearman rho of share on priority year

All-assignees row, as in III.1 (2016-2023: rho -0.452, p 0.26).

| assignees              | designs 2008-2023   | rho 2008-2023   | p 2008-2023   | p 2008-2023 (Holm)   | rho 2016-2023   | p 2016-2023   | p 2016-2023 (Holm)   |
|:-----------------------|:--------------------|:----------------|:--------------|:---------------------|:----------------|:--------------|:---------------------|
| all assignees          | 133                 | -0.685          | 0.003         | 0.024                | -0.452          | 0.260         | 1.000                |
| without Bell / Textron | 107                 | -0.538          | 0.032         | 0.221                | -0.048          | 0.911         | 1.000                |

### 4. The other architectures, without Bell / Textron

`designs 2008-2023` counts the designs left; Holm over the 7 architectures of III.1 in each span. Tilt Frame falls under 20 designs without Bell / Textron (17); it stays in the family as in III.1.

| architecture             | designs 2008-2023   | rho 2008-2023   | p 2008-2023   | p 2008-2023 (Holm)   | rho 2016-2023   | p 2016-2023   | p 2016-2023 (Holm)   |
|:-------------------------|:--------------------|:----------------|:--------------|:---------------------|:----------------|:--------------|:---------------------|
| Lift + Cruise            | 141                 | 0.390           | 0.135         | 0.752                | 0.548           | 0.160         | 0.960                |
| Combined Vectored Thrust | 76                  | 0.102           | 0.708         | 1.000                | 0.452           | 0.260         | 1.000                |
| Tilt Wing                | 42                  | -0.267          | 0.318         | 1.000                | -0.595          | 0.120         | 0.837                |
| Multicopter              | 35                  | 0.138           | 0.611         | 1.000                | -0.524          | 0.183         | 0.960                |
| Pitch-to-Cruise          | 22                  | 0.399           | 0.125         | 0.752                | -0.359          | 0.382         | 1.000                |
| Tilt Frame               | 17                  | -0.032          | 0.907         | 1.000                | 0.132           | 0.756         | 1.000                |

With all assignees, for comparison:

| architecture             | designs 2008-2023   | rho 2008-2023   | p 2008-2023   | p 2008-2023 (Holm)   | rho 2016-2023   | p 2016-2023   | p 2016-2023 (Holm)   |
|:-------------------------|:--------------------|:----------------|:--------------|:---------------------|:----------------|:--------------|:---------------------|
| Lift + Cruise            | 142                 | 0.443           | 0.085         | 0.427                | 0.515           | 0.192         | 1.000                |
| Combined Vectored Thrust | 93                  | 0.256           | 0.338         | 1.000                | 0.548           | 0.160         | 1.000                |
| Tilt Wing                | 49                  | -0.144          | 0.594         | 1.000                | -0.357          | 0.385         | 1.000                |
| Multicopter              | 36                  | 0.155           | 0.566         | 1.000                | -0.476          | 0.233         | 1.000                |
| Tilt Frame               | 23                  | 0.001           | 0.996         | 1.000                | -0.405          | 0.320         | 1.000                |
| Pitch-to-Cruise          | 22                  | 0.474           | 0.064         | 0.383                | 0.204           | 0.629         | 1.000                |

### 5. Answer

The decrease of Tilt Propulsor from the 2016-19 cohort to 2020-23 does not hold without Bell / Textron: its share goes up by 1.6 points (18.9 % to 20.5 %), against a decrease of 3.2 points with all assignees. Its trend over 2008-2023 is no longer detected (rho -0.538, Holm p 0.221) and over 2016-2023 not detected (rho -0.048, Holm p 1.000); no other architecture's trend is detected after the removal, over either span.
