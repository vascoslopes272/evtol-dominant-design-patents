# NUMBERS_II — Analysis II (design space)

Written by notebook 50 (`viz/thesis_latex_part2.py`); every value is recomputed when the notebook runs. CSVs are in `Data_for_writing/csv/`. Levels are A (architecture), A·W·T (architecture, wings, tilt), A·U (architecture, propulsor units); the propulsor bands are 1–3, 4, 5–6, 7–8 and 9+. The one design recorded with 0 propulsors (GB202302720D0_ad1, its count never entered under an M2 override) is left out of U (rerun of 2026-10-15).

## Configurations that hold half of each cohort's designs, at A·U (`q6_half_of_cohort`, which leaves the text)

Source: `q6_half_of_cohort.csv`. The figure ranks the configurations by size within the cohort (first column); the old heatmap used the overall-size order (second), which gives 10 for 2016–19 where the text says 10. 2024–26 is incomplete and not read.

| cohort               |   designs |   designs in the 32 A·U configurations of five or more |   configurations that hold half (ranked by size within the cohort) |   same, columns in overall-size order (the old heatmap) |
|:---------------------|----------:|-------------------------------------------------------:|-------------------------------------------------------------------:|--------------------------------------------------------:|
| ≤2011                |        59 |                                                     57 |                                                                  5 |                                                       8 |
| 2012–15              |        57 |                                                     56 |                                                                  5 |                                                       7 |
| 2016–19              |       213 |                                                    200 |                                                                  9 |                                                       9 |
| 2020–23              |       237 |                                                    224 |                                                                  7 |                                                       7 |
| 2024–26 (incomplete) |        55 |                                                     53 |                                                                  6 |                                                      10 |

## Table: dimensions that vary

Source: `q6_selected_fields.csv` (notebook 50, group II1).

Change of 2026-10-16: three dimensions added (Table 4.3 of the dissertation): booms present (`boomsPresent`, all 627 designs), propulsor enclosure (any ducted: `any_ducted` of `frames.propulsion_states`, on the designs with a propulsor-unit answer, so the 0-propulsor design and HB / PFV are left out as in the two propulsor rows: 595, not the 596 of ANSWERS_II1.md) and fuselage shape (`fusShape`, codebook base names; the table prints the four most common options, the fifth is Other: 11). The three enter `q6_fixed_by_architecture` in the table's order, before number of wings, so the permutation p of number of wings (0.003 → 0.001) and wing configuration (0.006 → 0.004) moved with the shuffle stream; every V and every other p is unchanged.

| dimension                                  |   designs answering |   options | top share   | most common options                                                          |
|:-------------------------------------------|--------------------:|----------:|:------------|:-----------------------------------------------------------------------------|
| propulsor units per design (band)          |                 589 |         5 | 23 %        | 1–3: 135 · 4: 124 · 5–6: 116 · 9+: 113 · 7–8: 101                            |
| tail type                                  |                 594 |        13 | 29 %        | Tailless: 174 · Conventional: 72 · V-tail: 69 · Single fin: 59               |
| places carrying propulsor units per design |                 589 |         4 | 48 %        | 2: 284 · 1: 244 · 3: 58 · 4 or more: 3                                       |
| booms present                              |                 621 |         2 | 54 %        | No booms: 333 · Booms: 288                                                   |
| propulsor enclosure (any ducted)           |                 589 |         2 | 63 %        | None ducted: 374 · Any ducted: 215                                           |
| fuselage shape                             |                 597 |         5 | 64 %        | Oval: 385 · Circular: 114 · Rectangular: 52 · Blended: 36                    |
| number of wings (winged designs)           |                 542 |         3 | 65 %        | 1: 354 · 2: 172 · 3: 16                                                      |
| landing-gear type                          |                 596 |         3 | 68 %        | Unknown: 405 · Wheeled: 101 · Skids: 90                                      |
| fuselage motion hover to cruise            |                 596 |         4 | 85 %        | Fixed: 504 · Whole-body pitch: 62 · Tail-sitter: 17 · Variable incidence: 13 |
| wing configuration                         |                 537 |         6 | 87 %        | Standard: 468 · Other: 48 · Blended wing body: 15 · Lifting body: 4          |

## Which dimensions the architecture fixes (`q6_fixed_by_architecture`)

Source: `q6_fixed_by_architecture.csv` and `q6_fixed_by_architecture_detail.csv` (notebook 50, group II1, appendix; `viz/thesis_q6.py` fixed_by_architecture).

For each dimension of the table above, on the designs that answer it and have an architecture, the bias-corrected Cramér's V (Bergsma 2013) of dimension × architecture is read with a permutation p (1000 shuffles of the architecture column, one generator seeded 42, dimensions in the table's order; p = share of shuffles at or above the observed V). Per architecture the leading option of the dimension and its share of that architecture's answering designs are read (the detail csv); an architecture with fewer than 10 answering designs is too few to read, and the dimension is fixed in an architecture when the leading option holds 80 % or more of them.

| dimension                                  |   designs answering |   Cramér's V | p       | p (Holm)   | architectures at 80 % or more   | architectures too few to read                                                                                |
|:-------------------------------------------|--------------------:|-------------:|:--------|:-----------|:--------------------------------|:-------------------------------------------------------------------------------------------------------------|
| propulsor units per design (band)          |                 589 |         0.23 | < 0.001 | < 0.001    | 0 of 7 read                     | Rotorcraft, Stopped/Slowed Rotor Wing, Deflected Slipstream, Hoverbike, Personal Flying Vehicle              |
| tail type                                  |                 593 |         0.11 | 0.028   | 0.028      | 0 of 7 read                     | Rotorcraft, Stopped/Slowed Rotor Wing, Deflected Slipstream, Hoverbike, Personal Flying Vehicle              |
| places carrying propulsor units per design |                 589 |         0.26 | < 0.001 | < 0.001    | 1 of 7 read                     | Rotorcraft, Stopped/Slowed Rotor Wing, Deflected Slipstream, Hoverbike, Personal Flying Vehicle              |
| booms present                              |                 619 |         0.29 | < 0.001 | < 0.001    | 2 of 9 read                     | Rotorcraft, Stopped/Slowed Rotor Wing, Deflected Slipstream                                                  |
| propulsor enclosure (any ducted)           |                 589 |         0.18 | 0.001   | 0.004      | 1 of 7 read                     | Rotorcraft, Stopped/Slowed Rotor Wing, Deflected Slipstream, Hoverbike, Personal Flying Vehicle              |
| fuselage shape                             |                 596 |         0.19 | < 0.001 | < 0.001    | 1 of 7 read                     | Rotorcraft, Stopped/Slowed Rotor Wing, Deflected Slipstream, Hoverbike, Personal Flying Vehicle              |
| number of wings (winged designs)           |                 540 |         0.17 | 0.003   | 0.009      | 1 of 7 read                     | Multicopter, Rotorcraft, Stopped/Slowed Rotor Wing, Deflected Slipstream, Personal Flying Vehicle            |
| landing-gear type                          |                 595 |         0.24 | < 0.001 | < 0.001    | 0 of 7 read                     | Rotorcraft, Stopped/Slowed Rotor Wing, Deflected Slipstream, Hoverbike, Personal Flying Vehicle              |
| fuselage motion hover to cruise            |                 595 |         0.72 | < 0.001 | < 0.001    | 5 of 7 read                     | Rotorcraft, Stopped/Slowed Rotor Wing, Deflected Slipstream, Hoverbike, Personal Flying Vehicle              |
| wing configuration                         |                 536 |         0.32 | 0.003   | 0.009      | 5 of 6 read                     | Multicopter, Rotorcraft, Stopped/Slowed Rotor Wing, Deflected Slipstream, Hoverbike, Personal Flying Vehicle |

## Table: levels of description

Source: `q7_levels_of_description.csv` (notebook 50, group II2). The family F row is in Analysis III.

| level   |   configurations |   singletons |   ¹D | largest configuration                 | its share   |
|:--------|-----------------:|-------------:|-----:|:--------------------------------------|:------------|
| A       |               12 |            0 |  7.3 | SLC                                   | 26 %        |
| A·W·T   |               39 |           10 | 16.5 | SLC · one wing · no tilting propulsor | 16 %        |
| A·U     |               44 |            4 | 29.6 | TP · 1–3 propulsor units              | 10 %        |

## Table: Hill numbers of each level

Source: `q7_hill_numbers_by_level.csv`; all years, 627 designs less those the level cannot name.

| level   |   designs |   ⁰D (configurations) |   ¹D |   ²D |
|:--------|----------:|----------------------:|-----:|-----:|
| A       |       619 |                    12 |  7.3 |  5.7 |
| A·W·T   |       617 |                    39 | 16.5 | 11.3 |
| A·U     |       618 |                    44 | 29.6 | 22.8 |

## Discovery (`q6_discovery_curve`): complete years (to 2023)

Source: `q6_discovery_estimators.csv`; the figure's last-100 window and these numbers are on the complete years.

| level   |   designs (complete years) |   configurations seen |   Chao1 |   new in the last 100 designs |   new in the last 100, random order |
|:--------|---------------------------:|----------------------:|--------:|------------------------------:|------------------------------------:|
| A       |                        564 |                    12 |      12 |                           0   |                                 0   |
| A·W·T   |                        563 |                    36 |      39 |                           4.2 |                                 1.4 |
| A·U     |                        563 |                    43 |      45 |                           1.1 |                                 0.8 |

### Band of the last 100 designs (`q6_discovery_last100_band.csv`, supervisor review 2)

Date order: the count of configurations first seen in the last 100 designs over the 1 000 tie orderings inside a priority year that draw the curve (same generator stream, seed 42); its mean is the value above. Random order: 10 000 full shuffles of the same designs (second generator, seed 42); the random mean is the exact expectation (the value above), the shuffle mean is the check (within 0.02). One-sided p: (a) share of shuffles with a count at or above the date-order mean; (b) for each date ordering the share of shuffles at or above its whole count, averaged over the orderings. The dissertation quotes (b).

| level   |   designs |   new in last 100 (date order, mean) |   date order 2.5 % |   date order 97.5 % |   random mean (exact expectation) |   random mean (10 000 shuffles, check) |   random 95th percentile (10 000 shuffles) |   random 99th percentile (10 000 shuffles) |   random max (10 000 shuffles) |   one-sided p (share >= date mean) |   one-sided p (whole counts, averaged over the date orderings) |   date orderings |   shuffles |   seed |
|:--------|----------:|-------------------------------------:|-------------------:|--------------------:|----------------------------------:|---------------------------------------:|-------------------------------------------:|-------------------------------------------:|-------------------------------:|-----------------------------------:|---------------------------------------------------------------:|-----------------:|-----------:|-------:|
| A       |       564 |                                 0    |                  0 |                   0 |                              0    |                                  0.001 |                                          0 |                                          0 |                              1 |                             1      |                                                         1      |             1000 |      10000 |     42 |
| A·W·T   |       563 |                                 4.18 |                  4 |                   5 |                              1.44 |                                  1.451 |                                          3 |                                          4 |                              6 |                             0.007  |                                                         0.0375 |             1000 |      10000 |     42 |
| A·U     |       563 |                                 1.06 |                  1 |                   2 |                              0.79 |                                  0.768 |                                          2 |                                          3 |                              5 |                             0.1701 |                                                         0.5439 |             1000 |      10000 |     42 |

## Core (`q6_configuration_core`)

Source: `q6_configuration_core.csv`. Core: the A·U configurations taken in order of their share of the 2016–23 designs until the cumulative share reaches 50 % (the one that crosses 50 % is included, and any tied with it, on the unrounded shares): 10 configurations holding 56.4 % of the 2016–23 designs; periphery: 16 configurations holding 22.2 %. 2024–26 is not drawn. Judgement call on labels: the figure names the core and the 3 largest non-core configurations by their 2016–23 share (unrounded; ties kept); every other point is grey and unnamed.

## Numbers quoted by the Results text, Analysis II (sub-question A)

Source: `viz/thesis_q6.py` numbers(ctx), notebook cells of groups II1–II3.

- `core_n` = 10
- `core_share` = 56 %
- `cu_top_w4` = 11 %
- `cwt_chao` = 39.0
- `cwt_exp` = 1.4
- `cwt_found` = 92 %
- `cwt_new` = 4.2
- `disc_after_last_class` = 362
- `half_w3` = 9
- `half_w4` = 7
- `span_recent` = 2016-23
- `tail_top` = 29 %
- `units_median` = 5
- `units_top` = 23 %
- `w3` = 2016-19
