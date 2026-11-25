# NUMBERS_IV — Analysis IV (evolution of the design space)

Written by notebook 51 (`viz/thesis_latex_part4.py`); every value is recomputed when the notebook runs. CSVs are in `Data_for_writing/csv/`.

## IV.1 Layout shares per cohort (share of the architecture's designs; count/architecture total)

Source: `q6_leading_layout_by_architecture.csv`. The first two cohorts hold few designs.

| architecture             | layout                                      | <= 2011        | 2012-15        | 2016-19        | 2020-23        |
|:-------------------------|:--------------------------------------------|:---------------|:---------------|:---------------|:---------------|
| Lift + Cruise            | on booms                                    | 61.5 % (8/13)  | 55.6 % (5/9)   | 43.8 % (21/48) | 48.0 % (36/75) |
| Lift + Cruise            | on the body                                 | 23.1 % (3/13)  | 11.1 % (1/9)   | 20.8 % (10/48) | 20.0 % (15/75) |
| Lift + Cruise            | on the body, stowed in cruise               | 0.0 % (0/13)   | 11.1 % (1/9)   | 2.1 % (1/48)   | 1.3 % (1/75)   |
| Lift + Cruise            | on the wing                                 | 15.4 % (2/13)  | 22.2 % (2/9)   | 22.9 % (11/48) | 25.3 % (19/75) |
| Lift + Cruise            | on booms, stowed in cruise                  | 0.0 % (0/13)   | 0.0 % (0/9)    | 6.2 % (3/48)   | 4.0 % (3/75)   |
| Lift + Cruise            | on the wing, stowed in cruise               | 0.0 % (0/13)   | 0.0 % (0/9)    | 4.2 % (2/48)   | 1.3 % (1/75)   |
| Tilt Propulsor           | one tilting set                             | 75.0 % (15/20) | 50.0 % (10/20) | 33.3 % (17/51) | 30.6 % (15/49) |
| Tilt Propulsor           | 2+ tilting sets, in one place               | 5.0 % (1/20)   | 20.0 % (4/20)  | 35.3 % (18/51) | 28.6 % (14/49) |
| Tilt Propulsor           | 2+ tilting sets, in 2+ places               | 20.0 % (4/20)  | 30.0 % (6/20)  | 31.4 % (16/51) | 38.8 % (19/49) |
| Tilt Propulsor           | no tilting set recorded                     | 0.0 % (0/20)   | 0.0 % (0/20)   | 0.0 % (0/51)   | 2.0 % (1/49)   |
| Combined Vectored Thrust | a wing tilts · fixed elsewhere              | 0.0 % (0/5)    | 30.0 % (3/10)  | 3.6 % (1/28)   | 7.5 % (4/53)   |
| Combined Vectored Thrust | a wing tilts · fixed on booms               | 0.0 % (0/5)    | 10.0 % (1/10)  | 0.0 % (0/28)   | 3.8 % (2/53)   |
| Combined Vectored Thrust | propulsors and a wing tilt · no fixed unit  | 0.0 % (0/5)    | 10.0 % (1/10)  | 3.6 % (1/28)   | 3.8 % (2/53)   |
| Combined Vectored Thrust | propulsors tilt · fixed elsewhere           | 80.0 % (4/5)   | 50.0 % (5/10)  | 46.4 % (13/28) | 28.3 % (15/53) |
| Combined Vectored Thrust | propulsors tilt · fixed on booms            | 20.0 % (1/5)   | 0.0 % (0/10)   | 39.3 % (11/28) | 52.8 % (28/53) |
| Combined Vectored Thrust | tilt not recorded · fixed elsewhere         | 0.0 % (0/5)    | 0.0 % (0/10)   | 7.1 % (2/28)   | 0.0 % (0/53)   |
| Combined Vectored Thrust | propulsors and a wing tilt · fixed on booms | 0.0 % (0/5)    | 0.0 % (0/10)   | 0.0 % (0/28)   | 1.9 % (1/53)   |
| Combined Vectored Thrust | propulsors tilt · no fixed unit             | 0.0 % (0/5)    | 0.0 % (0/10)   | 0.0 % (0/28)   | 1.9 % (1/53)   |

## IV.1 and IV.2 Traces per architecture and cohort

Source: `q6_architecture_traces_by_cohort.csv` (frame `dw` of `viz/thesis_q6.py`).

| architecture             | cohort   |   aircraft |   tilting sets (mean) |   propulsive units (median) |   share with units on booms |   share with a ducted unit |   ducted share, units on booms |   ducted share, no units on booms |
|:-------------------------|:---------|-----------:|----------------------:|----------------------------:|----------------------------:|---------------------------:|-------------------------------:|----------------------------------:|
| Lift + Cruise            | <= 2011  |         13 |                 0     |                         7   |                       0.615 |                      0.385 |                        nan     |                           nan     |
| Lift + Cruise            | 2012-15  |          9 |                 0     |                         5   |                       0.667 |                      0.222 |                        nan     |                           nan     |
| Lift + Cruise            | 2016-19  |         48 |                 0     |                         7   |                       0.521 |                      0.292 |                        nan     |                           nan     |
| Lift + Cruise            | 2020-23  |         75 |                 0     |                         7   |                       0.56  |                      0.48  |                        nan     |                           nan     |
| Tilt Propulsor           | <= 2011  |         20 |                 1.35  |                         2   |                       0.2   |                      0.15  |                        nan     |                           nan     |
| Tilt Propulsor           | 2012-15  |         20 |                 1.65  |                         2   |                       0.3   |                      0.45  |                        nan     |                           nan     |
| Tilt Propulsor           | 2016-19  |         51 |                 1.804 |                         4   |                       0.392 |                      0.431 |                        nan     |                           nan     |
| Tilt Propulsor           | 2020-23  |         49 |                 1.755 |                         4   |                       0.388 |                      0.306 |                        nan     |                           nan     |
| Combined Vectored Thrust | <= 2011  |          5 |                 1     |                         4   |                       0.2   |                      0.8   |                        nan     |                           nan     |
| Combined Vectored Thrust | 2012-15  |         10 |                 1.1   |                         4   |                       0.2   |                      0.4   |                        nan     |                             0.5   |
| Combined Vectored Thrust | 2016-19  |         28 |                 1.357 |                         5   |                       0.607 |                      0.464 |                          0.353 |                             0.636 |
| Combined Vectored Thrust | 2020-23  |         53 |                 1.434 |                         6   |                       0.623 |                      0.321 |                          0.061 |                             0.75  |
| Tilt Wing                | <= 2011  |          4 |               nan     |                       nan   |                     nan     |                    nan     |                        nan     |                           nan     |
| Tilt Wing                | 2012-15  |          6 |                 1.333 |                         4   |                       0     |                      0     |                        nan     |                           nan     |
| Tilt Wing                | 2016-19  |         21 |                 1.667 |                         6   |                       0.286 |                      0.333 |                        nan     |                           nan     |
| Tilt Wing                | 2020-23  |         19 |                 1.421 |                         4   |                       0.263 |                      0.158 |                        nan     |                           nan     |
| Multirotor               | <= 2011  |          9 |                 0.222 |                         4   |                       0.111 |                      0.778 |                        nan     |                           nan     |
| Multirotor               | 2012-15  |          3 |               nan     |                       nan   |                     nan     |                    nan     |                        nan     |                           nan     |
| Multirotor               | 2016-19  |         16 |                 0.688 |                         5.5 |                       0.812 |                      0.438 |                        nan     |                           nan     |
| Multirotor               | 2020-23  |         15 |                 0.4   |                         6   |                       0.6   |                      0.733 |                        nan     |                           nan     |

## IV.2 Median propulsor units per architecture and cohort

Source: `q6_propulsor_units_median_by_cohort.csv` (the aircraft of the architecture with a unit count above zero, as the traces frame; 2024–26 is incomplete and not read). The median of Tilt Propulsor goes 2, 2, 4, 4: 2 to 4 is right. The 6 is the median of one layout inside Tilt Propulsor (tilting sets in 2+ places), see below.

| architecture             | <= 2011   | 2012-15   | 2016-19   | 2020-23   | 2024-26 (incomplete)   |
|:-------------------------|:----------|:----------|:----------|:----------|:-----------------------|
| Tilt Propulsor           | 2 (n 20)  | 2 (n 20)  | 4 (n 51)  | 4 (n 49)  | 7 (n 12)               |
| Combined Vectored Thrust | 4 (n 5)   | 4 (n 10)  | 5 (n 28)  | 6 (n 53)  | 6 (n 10)               |
| Lift + Cruise            | 7 (n 13)  | 5 (n 9)   | 7 (n 48)  | 7 (n 75)  | 7 (n 15)               |

Median propulsor units of the leading layouts, per cohort:

| architecture             | cohort   | leading layout                  |   designs |   median propulsor units |
|:-------------------------|:---------|:--------------------------------|----------:|-------------------------:|
| Lift + Cruise            | <= 2011  | lift units on booms             |         8 |                      8.5 |
| Lift + Cruise            | 2020-23  | lift units on booms             |        36 |                      8   |
| Tilt Propulsor           | <= 2011  | one tilting set                 |        15 |                      2   |
| Tilt Propulsor           | 2020-23  | tilting sets in 2+ places       |        19 |                      6   |
| Combined Vectored Thrust | <= 2011  | tilting rotors, fixed elsewhere |         4 |                      3.5 |
| Combined Vectored Thrust | 2020-23  | tilting rotors, fixed on booms  |        28 |                      6   |

## IV.2 Spearman rho and p of every trace (every year to 2023; too thin / constant where not tested)

Source: `q6_driver_trends.csv`.

| trace                                     | driver kind   | architecture                    | code   |   aircraft | first cohort   |   first value |   2020-23 value |   first mean |   2020-23 mean |    rho |             p |        p_holm | movement   |
|:------------------------------------------|:--------------|:--------------------------------|:-------|-----------:|:---------------|--------------:|----------------:|-------------:|---------------:|-------:|--------------:|--------------:|:-----------|
| tilting joint groups                      | A1            | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0    |            0    |         0    |           0    | nan    | nan           | nan           | constant   |
| tilting joint groups                      | A1            | Tilt Propulsor                  | TR     |        140 | <= 2011        |          1    |            2    |         1.35 |           1.76 |   0.22 |   0.00990773  |   0.0198155   | rises      |
| tilting joint groups                      | A1            | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          1    |            1    |         1    |           1.43 |   0.25 |   0.0134655   |   0.0198155   | rises      |
| tilting joint groups                      | A1            | Tilt Wing                       | TW     |         50 | 2012-15        |          1    |            1    |         1.33 |           1.42 |  -0.12 |   0.412058    | nan           | flat       |
| tilting joint groups                      | A1            | Multirotor                      | MR     |         43 | <= 2011        |          0    |            0    |         0.22 |           0.4  |   0.1  |   0.527669    | nan           | flat       |
| tilting joint groups                      | A1            | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          1    |            1    |         0.78 |           0.92 |  -0.01 |   0.891507    | nan           | flat       |
| tilting joint groups                      | A1            | all classed aircraft            | ALL    |        536 | <= 2011        |          1    |            1    |         0.75 |           0.84 |  -0.01 |   0.76624     | nan           | flat       |
| fuselage kinematics not fixed             | A1            | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0    |            0    |       nan    |         nan    |  -0.09 |   0.258495    |   0.258495    | flat       |
| fuselage kinematics not fixed             | A1            | Tilt Propulsor                  | TR     |        140 | <= 2011        |          0    |            0    |       nan    |         nan    | nan    | nan           | nan           | constant   |
| fuselage kinematics not fixed             | A1            | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          0    |            0    |       nan    |         nan    | nan    | nan           | nan           | constant   |
| fuselage kinematics not fixed             | A1            | Tilt Wing                       | TW     |         50 | 2012-15        |          0    |            0    |       nan    |         nan    |  -0.22 |   0.117774    | nan           | flat       |
| fuselage kinematics not fixed             | A1            | Multirotor                      | MR     |         43 | <= 2011        |          0.67 |            0.33 |       nan    |         nan    |  -0.41 |   0.00684722  | nan           | falls      |
| fuselage kinematics not fixed             | A1            | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          0.14 |            0.02 |       nan    |         nan    |  -0.16 |   0.000518073 | nan           | falls      |
| fuselage kinematics not fixed             | A1            | all classed aircraft            | ALL    |        542 | <= 2011        |          0.2  |            0.09 |       nan    |         nan    |  -0.11 |   0.00998288  | nan           | falls      |
| a propulsor retracts or folds its blades  | A2            | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0    |            0.07 |       nan    |         nan    |  -0.03 |   0.740757    |   0.740757    | flat       |
| a propulsor retracts or folds its blades  | A2            | Tilt Propulsor                  | TR     |        140 | <= 2011        |          0    |            0    |       nan    |         nan    |  -0.08 |   0.360257    |   0.720514    | flat       |
| a propulsor retracts or folds its blades  | A2            | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          0.2  |            0.13 |       nan    |         nan    |  -0.15 |   0.155901    |   0.467702    | flat       |
| a propulsor retracts or folds its blades  | A2            | Tilt Wing                       | TW     |         50 | 2012-15        |          0    |            0.05 |       nan    |         nan    |   0.2  |   0.155031    | nan           | flat       |
| a propulsor retracts or folds its blades  | A2            | Multirotor                      | MR     |         43 | <= 2011        |          0    |            0.13 |       nan    |         nan    |   0.22 |   0.164247    | nan           | flat       |
| a propulsor retracts or folds its blades  | A2            | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          0.02 |            0.07 |       nan    |         nan    |   0.01 |   0.855815    | nan           | flat       |
| a propulsor retracts or folds its blades  | A2            | all classed aircraft            | ALL    |        536 | <= 2011        |          0.02 |            0.06 |       nan    |         nan    |   0    |   0.933134    | nan           | flat       |
| booms stow                                | B             | Lift + Cruise                   | SLC    |         81 | <= 2011        |          0    |            0.05 |       nan    |         nan    |   0.04 |   0.745846    |   1           | flat       |
| booms stow                                | B             | Tilt Propulsor                  | TR     |         52 | 2012-15        |          0    |            0    |       nan    |         nan    | nan    | nan           | nan           | constant   |
| booms stow                                | B             | Combined Vectored Thrust        | CVT    |         55 | 2016-19        |          0.06 |            0.06 |       nan    |         nan    |  -0.08 |   0.580149    |   1           | flat       |
| booms stow                                | B             | Tilt Wing                       | TW     |         14 | 2016-19        |          0    |            0    |       nan    |         nan    | nan    | nan           | nan           | too thin   |
| booms stow                                | B             | Multirotor                      | MR     |         25 | 2016-19        |          0    |            0.11 |       nan    |         nan    |   0.2  |   0.332409    | nan           | flat       |
| booms stow                                | B             | five drawn architectures pooled | ALL5   |        227 | <= 2011        |          0    |            0.05 |       nan    |         nan    |   0.03 |   0.684236    | nan           | flat       |
| booms stow                                | B             | all classed aircraft            | ALL    |        257 | <= 2011        |          0    |            0.04 |       nan    |         nan    |   0.04 |   0.547882    | nan           | flat       |
| propulsive units                          | A1            | Lift + Cruise                   | SLC    |        145 | <= 2011        |          7    |            7    |       nan    |         nan    |   0.06 |   0.448104    |   0.448104    | flat       |
| propulsive units                          | A1            | Tilt Propulsor                  | TR     |        140 | <= 2011        |          2    |            4    |       nan    |         nan    |   0.41 |   6.06342e-07 |   1.81903e-06 | rises      |
| propulsive units                          | A1            | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          4    |            6    |       nan    |         nan    |   0.31 |   0.00211034  |   0.00422068  | rises      |
| propulsive units                          | A1            | Tilt Wing                       | TW     |         50 | 2012-15        |          4    |            4    |       nan    |         nan    |   0.11 |   0.466831    | nan           | flat       |
| propulsive units                          | A1            | Multirotor                      | MR     |         43 | <= 2011        |          4    |            6    |       nan    |         nan    |   0.26 |   0.0922254   | nan           | flat       |
| propulsive units                          | A1            | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          4    |            6    |       nan    |         nan    |   0.28 |   6.64616e-10 | nan           | rises      |
| propulsive units                          | A1            | all classed aircraft            | ALL    |        536 | <= 2011        |          4    |            6    |       nan    |         nan    |   0.28 |   4.9922e-11  | nan           | rises      |
| units carried on booms                    | A1            | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0.62 |            0.56 |       nan    |         nan    |   0.05 |   0.545261    |   0.545261    | flat       |
| units carried on booms                    | A1            | Tilt Propulsor                  | TR     |        140 | <= 2011        |          0.2  |            0.39 |       nan    |         nan    |   0.11 |   0.201741    |   0.403482    | flat       |
| units carried on booms                    | A1            | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          0.2  |            0.62 |       nan    |         nan    |   0.22 |   0.0329559   |   0.0988678   | rises      |
| units carried on booms                    | A1            | Tilt Wing                       | TW     |         50 | 2012-15        |          0    |            0.26 |       nan    |         nan    |   0.28 |   0.0453358   | nan           | rises      |
| units carried on booms                    | A1            | Multirotor                      | MR     |         43 | <= 2011        |          0.11 |            0.6  |       nan    |         nan    |   0.26 |   0.0882352   | nan           | flat       |
| units carried on booms                    | A1            | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          0.27 |            0.51 |       nan    |         nan    |   0.16 |   0.000579916 | nan           | rises      |
| units carried on booms                    | A1            | all classed aircraft            | ALL    |        536 | <= 2011        |          0.27 |            0.49 |       nan    |         nan    |   0.14 |   0.00159009  | nan           | rises      |
| stations carrying units                   | A1            | Lift + Cruise                   | SLC    |        145 | <= 2011        |          2    |            2    |         1.85 |           2.01 |   0.04 |   0.633378    |   1           | flat       |
| stations carrying units                   | A1            | Tilt Propulsor                  | TR     |        140 | <= 2011        |          1    |            1    |         1.3  |           1.45 |   0.19 |   0.0258674   |   0.0776021   | rises      |
| stations carrying units                   | A1            | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          2    |            2    |         1.8  |           1.91 |  -0.03 |   0.774039    |   1           | flat       |
| stations carrying units                   | A1            | Tilt Wing                       | TW     |         50 | 2012-15        |          1    |            1    |         1.33 |           1.47 |  -0    |   0.976836    | nan           | flat       |
| stations carrying units                   | A1            | Multirotor                      | MR     |         43 | <= 2011        |          1    |            1    |         1    |           1.13 |   0.25 |   0.113206    | nan           | flat       |
| stations carrying units                   | A1            | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          1    |            2    |         1.43 |           1.74 |   0.16 |   0.000338121 | nan           | rises      |
| stations carrying units                   | A1            | all classed aircraft            | ALL    |        536 | <= 2011        |          1    |            2    |         1.4  |           1.72 |   0.15 |   0.000573279 | nan           | rises      |
| booms present                             | A2            | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0.62 |            0.56 |       nan    |         nan    |   0.05 |   0.545261    |   0.545261    | flat       |
| booms present                             | A2            | Tilt Propulsor                  | TR     |        140 | <= 2011        |          0.2  |            0.41 |       nan    |         nan    |   0.12 |   0.149308    |   0.298616    | flat       |
| booms present                             | A2            | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          0.4  |            0.62 |       nan    |         nan    |   0.18 |   0.0842121   |   0.252636    | flat       |
| booms present                             | A2            | Tilt Wing                       | TW     |         50 | 2012-15        |          0.17 |            0.26 |       nan    |         nan    |   0.12 |   0.414471    | nan           | flat       |
| booms present                             | A2            | Multirotor                      | MR     |         43 | <= 2011        |          0.11 |            0.6  |       nan    |         nan    |   0.26 |   0.0882352   | nan           | flat       |
| booms present                             | A2            | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          0.31 |            0.52 |       nan    |         nan    |   0.14 |   0.00231008  | nan           | rises      |
| booms present                             | A2            | all classed aircraft            | ALL    |        564 | <= 2011        |          0.31 |            0.49 |       nan    |         nan    |   0.12 |   0.00615385  | nan           | rises      |
| wing units at the leading edge            | A2            | Lift + Cruise                   | SLC    |         67 | <= 2011        |          0    |            0.46 |       nan    |         nan    |   0.11 |   0.382067    |   0.805924    | flat       |
| wing units at the leading edge            | A2            | Tilt Propulsor                  | TR     |         83 | <= 2011        |          1    |            0.82 |       nan    |         nan    |  -0.12 |   0.268641    |   0.805924    | flat       |
| wing units at the leading edge            | A2            | Combined Vectored Thrust        | CVT    |         65 | 2012-15        |          0.88 |            0.73 |       nan    |         nan    |   0.03 |   0.783067    |   0.805924    | flat       |
| wing units at the leading edge            | A2            | Tilt Wing                       | TW     |         44 | 2012-15        |          1    |            0.87 |       nan    |         nan    |  -0.29 |   0.060584    | nan           | flat       |
| wing units at the leading edge            | A2            | Multirotor                      | MR     |          0 |                |        nan    |          nan    |       nan    |         nan    | nan    | nan           | nan           | too thin   |
| wing units at the leading edge            | A2            | five drawn architectures pooled | ALL5   |        259 | <= 2011        |          0.73 |            0.69 |       nan    |         nan    |  -0.08 |   0.192267    | nan           | flat       |
| wing units at the leading edge            | A2            | all classed aircraft            | ALL    |        288 | <= 2011        |          0.7  |            0.71 |       nan    |         nan    |  -0.06 |   0.34772     | nan           | flat       |
| a pusher unit                             | A2            | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0.54 |            0.49 |       nan    |         nan    |   0.04 |   0.603519    |   0.603519    | flat       |
| a pusher unit                             | A2            | Tilt Propulsor                  | TR     |        140 | <= 2011        |          0    |            0.12 |       nan    |         nan    |   0.14 |   0.0954347   |   0.286304    | flat       |
| a pusher unit                             | A2            | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          0.2  |            0.11 |       nan    |         nan    |  -0.12 |   0.257299    |   0.514598    | flat       |
| a pusher unit                             | A2            | Tilt Wing                       | TW     |         50 | 2012-15        |          0    |            0.05 |       nan    |         nan    |  -0.08 |   0.589063    | nan           | flat       |
| a pusher unit                             | A2            | Multirotor                      | MR     |         43 | <= 2011        |          0    |            0.07 |       nan    |         nan    |   0.23 |   0.144461    | nan           | flat       |
| a pusher unit                             | A2            | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          0.18 |            0.24 |       nan    |         nan    |   0.1  |   0.0350409   | nan           | rises      |
| a pusher unit                             | A2            | all classed aircraft            | ALL    |        536 | <= 2011        |          0.16 |            0.23 |       nan    |         nan    |   0.1  |   0.0232383   | nan           | rises      |
| two or more wing panels                   | A2            | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0.46 |            0.37 |       nan    |         nan    |   0.1  |   0.247133    |   0.494266    | flat       |
| two or more wing panels                   | A2            | Tilt Propulsor                  | TR     |        140 | <= 2011        |          0.2  |            0.35 |       nan    |         nan    |   0.13 |   0.132743    |   0.398229    | flat       |
| two or more wing panels                   | A2            | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          0.2  |            0.36 |       nan    |         nan    |   0.11 |   0.27168     |   0.494266    | flat       |
| two or more wing panels                   | A2            | Tilt Wing                       | TW     |         50 | 2012-15        |          0.33 |            0.37 |       nan    |         nan    |  -0.16 |   0.275365    | nan           | flat       |
| two or more wing panels                   | A2            | Multirotor                      | MR     |         43 | <= 2011        |          0    |            0    |       nan    |         nan    | nan    | nan           | nan           | constant   |
| two or more wing panels                   | A2            | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          0.25 |            0.34 |       nan    |         nan    |   0.09 |   0.0421158   | nan           | rises      |
| two or more wing panels                   | A2            | all classed aircraft            | ALL    |        563 | <= 2011        |          0.24 |            0.34 |       nan    |         nan    |   0.09 |   0.0302934   | nan           | rises      |
| swept or delta main wing                  | B             | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0.77 |            0.43 |       nan    |         nan    |  -0.1  |   0.245583    |   0.736748    | flat       |
| swept or delta main wing                  | B             | Tilt Propulsor                  | TR     |        140 | <= 2011        |          0.15 |            0.31 |       nan    |         nan    |   0.05 |   0.551639    |   1           | flat       |
| swept or delta main wing                  | B             | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          0.2  |            0.26 |       nan    |         nan    |  -0.03 |   0.757834    |   1           | flat       |
| swept or delta main wing                  | B             | Tilt Wing                       | TW     |         50 | 2012-15        |          0.17 |            0    |       nan    |         nan    |  -0.19 |   0.176622    | nan           | flat       |
| swept or delta main wing                  | B             | Multirotor                      | MR     |          0 |                |        nan    |          nan    |       nan    |         nan    | nan    | nan           | nan           | too thin   |
| swept or delta main wing                  | B             | five drawn architectures pooled | ALL5   |        431 | <= 2011        |          0.33 |            0.31 |       nan    |         nan    |  -0.01 |   0.914216    | nan           | flat       |
| swept or delta main wing                  | B             | all classed aircraft            | ALL    |        485 | <= 2011        |          0.36 |            0.31 |       nan    |         nan    |   0    |   0.98235     | nan           | flat       |
| no tail surface                           | A2            | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0.62 |            0.23 |       nan    |         nan    |  -0.11 |   0.190034    |   0.30326     | flat       |
| no tail surface                           | A2            | Tilt Propulsor                  | TR     |        140 | <= 2011        |          0.05 |            0.27 |       nan    |         nan    |   0.12 |   0.15163     |   0.30326     | flat       |
| no tail surface                           | A2            | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          0.4  |            0.08 |       nan    |         nan    |  -0.3  |   0.00303835  |   0.00911504  | falls      |
| no tail surface                           | A2            | Tilt Wing                       | TW     |         50 | 2012-15        |          0.33 |            0.32 |       nan    |         nan    |  -0    |   0.975351    | nan           | flat       |
| no tail surface                           | A2            | Multirotor                      | MR     |         43 | <= 2011        |          0.44 |            0.87 |       nan    |         nan    |   0.31 |   0.0412337   | nan           | rises      |
| no tail surface                           | A2            | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          0.31 |            0.25 |       nan    |         nan    |  -0.06 |   0.177615    | nan           | flat       |
| no tail surface                           | A2            | all classed aircraft            | ALL    |        540 | <= 2011        |          0.33 |            0.27 |       nan    |         nan    |  -0.04 |   0.305553    | nan           | flat       |
| a ducted unit                             | B             | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0.38 |            0.48 |       nan    |         nan    |   0.11 |   0.179996    |   0.359991    | flat       |
| a ducted unit                             | B             | Tilt Propulsor                  | TR     |        140 | <= 2011        |          0.15 |            0.31 |       nan    |         nan    |   0.04 |   0.626798    |   0.626798    | flat       |
| a ducted unit                             | B             | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          0.8  |            0.32 |       nan    |         nan    |  -0.2  |   0.0519001   |   0.1557      | flat       |
| a ducted unit                             | B             | Tilt Wing                       | TW     |         50 | 2012-15        |          0    |            0.16 |       nan    |         nan    |  -0.02 |   0.916865    | nan           | flat       |
| a ducted unit                             | B             | Multirotor                      | MR     |         43 | <= 2011        |          0.78 |            0.73 |       nan    |         nan    |   0.06 |   0.698686    | nan           | flat       |
| a ducted unit                             | B             | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          0.39 |            0.39 |       nan    |         nan    |  -0    |   0.930542    | nan           | flat       |
| a ducted unit                             | B             | all classed aircraft            | ALL    |        536 | <= 2011        |          0.36 |            0.37 |       nan    |         nan    |  -0.01 |   0.792409    | nan           | flat       |
| ground contact drawn                      | B             | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0    |            0.27 |       nan    |         nan    |   0.09 |   0.278433    |   0.556867    | flat       |
| ground contact drawn                      | B             | Tilt Propulsor                  | TR     |        140 | <= 2011        |          0.35 |            0.39 |       nan    |         nan    |   0.09 |   0.297276    |   0.556867    | flat       |
| ground contact drawn                      | B             | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          0    |            0.32 |       nan    |         nan    |   0.18 |   0.0742997   |   0.222899    | flat       |
| ground contact drawn                      | B             | Tilt Wing                       | TW     |         50 | 2012-15        |          0    |            0.21 |       nan    |         nan    |   0.01 |   0.935294    | nan           | flat       |
| ground contact drawn                      | B             | Multirotor                      | MR     |         43 | <= 2011        |          0.11 |            0.6  |       nan    |         nan    |   0.37 |   0.0135551   | nan           | rises      |
| ground contact drawn                      | B             | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          0.18 |            0.33 |       nan    |         nan    |   0.1  |   0.0258919   | nan           | rises      |
| ground contact drawn                      | B             | all classed aircraft            | ALL    |        542 | <= 2011        |          0.22 |            0.35 |       nan    |         nan    |   0.08 |   0.0496843   | nan           | rises      |
| wheeled gear, of the ground contact drawn | B             | Lift + Cruise                   | SLC    |         37 | 2016-19        |          0.53 |            0.55 |       nan    |         nan    |   0.04 |   0.796529    |   0.974166    | flat       |
| wheeled gear, of the ground contact drawn | B             | Tilt Propulsor                  | TR     |         46 | <= 2011        |          0.71 |            0.53 |       nan    |         nan    |  -0.17 |   0.245932    |   0.737795    | flat       |
| wheeled gear, of the ground contact drawn | B             | Combined Vectored Thrust        | CVT    |         21 | 2020-23        |          0.71 |            0.71 |       nan    |         nan    |   0.16 |   0.487083    |   0.974166    | flat       |
| wheeled gear, of the ground contact drawn | B             | Tilt Wing                       | TW     |         11 | 2016-19        |          0.17 |          nan    |       nan    |         nan    | nan    | nan           | nan           | too thin   |
| wheeled gear, of the ground contact drawn | B             | Multirotor                      | MR     |         15 | 2020-23        |          0.22 |            0.22 |       nan    |         nan    | nan    | nan           | nan           | too thin   |
| wheeled gear, of the ground contact drawn | B             | five drawn architectures pooled | ALL5   |        130 | <= 2011        |          0.78 |            0.52 |       nan    |         nan    |  -0.07 |   0.446783    | nan           | flat       |
| wheeled gear, of the ground contact drawn | B             | all classed aircraft            | ALL    |        170 | <= 2011        |          0.75 |            0.49 |       nan    |         nan    |  -0.08 |   0.294571    | nan           | flat       |
| propulsor types                           | C             | Lift + Cruise                   | SLC    |        145 | <= 2011        |          3    |            3    |         2.62 |           2.71 |  -0.05 |   0.578272    |   0.578272    | flat       |
| propulsor types                           | C             | Tilt Propulsor                  | TR     |        140 | <= 2011        |          1    |            2    |         1.35 |           1.8  |   0.23 |   0.00579278  |   0.0173784   | rises      |
| propulsor types                           | C             | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          2    |            3    |         2.4  |           2.75 |   0.14 |   0.165697    |   0.331395    | flat       |
| propulsor types                           | C             | Tilt Wing                       | TW     |         50 | 2012-15        |          1.5  |            1    |         1.5  |           1.58 |  -0.05 |   0.715321    | nan           | flat       |
| propulsor types                           | C             | Multirotor                      | MR     |         43 | <= 2011        |          2    |            2    |         1.89 |           1.8  |   0.09 |   0.572457    | nan           | flat       |
| propulsor types                           | C             | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          2    |            2    |         1.86 |           2.34 |   0.18 |   5.32632e-05 | nan           | rises      |
| propulsor types                           | C             | all classed aircraft            | ALL    |        536 | <= 2011        |          2    |            2    |         1.8  |           2.31 |   0.18 |   2.21183e-05 | nan           | rises      |

## IV.2 The driver table

Source: `q6_driver_verdicts.csv`.

| trace                                        | where it moved (every year to 2023)                                                          | goes with (driver: what it predicts)                                                                  | goes against (driver: what it predicts)                              | what it means                                                                                                  |
|:---------------------------------------------|:---------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------|
| ● tilting sets per aircraft                  | rises in Tilt Propulsor (ρ +0.22, p 0.010); rises in CVT (ρ +0.25, p 0.01); pooled: flat     | regime transition (more)                                                                              | development and certification cost (fewer); maintenance cost (fewer) | drivers disagree; it moved with those under 'goes with'; per propulsor unit it falls                           |
| a body that tilts or rotates                 | falls in Multirotor (ρ -0.41, p 0.007); pooled: falls                                        | occupant presence (fewer)                                                                             | regime transition (more)                                             | drivers disagree; it moved with those under 'goes with'                                                        |
| ● propulsor units per aircraft               | rises in Tilt Propulsor (ρ +0.41, p < 0.001); rises in CVT (ρ +0.31, p 0.002); pooled: rises | distributed propulsion and propulsor control (more); failure tolerance (more); community noise (more) | —                                                                    | 3 drivers predict it; the labelled dataset cannot say which acts                                               |
| ● propulsor units carried on booms           | rises in CVT (ρ +0.22, p 0.03); rises in Tilt Wing (ρ +0.28, p 0.05); pooled: rises          | distributed propulsion and propulsor control (more)                                                   | —                                                                    | one driver predicts it, and it moved that way                                                                  |
| places carrying propulsor units per aircraft | rises in Tilt Propulsor (ρ +0.19, p 0.03); pooled: rises                                     | distributed propulsion and propulsor control (more)                                                   | —                                                                    | one driver predicts it, and it moved that way                                                                  |
| booms present                                | no trend detected in any architecture; pooled: rises                                         | —                                                                                                     | —                                                                    | no driver predicts a direction; only physical limits bear on it (hover load path, flow interference and drag)  |
| a pusher unit                                | no trend detected in any architecture; pooled: rises                                         | —                                                                                                     | —                                                                    | no driver predicts a direction; only physical limits bear on it (flow interference and drag)                   |
| two or more wing panels                      | no trend detected in any architecture; pooled: rises                                         | mission range and speed (either way)                                                                  | —                                                                    | one driver predicts it, and it moved that way                                                                  |
| no tail surface                              | falls in CVT (ρ -0.30, p 0.003); rises in Multirotor (ρ +0.31, p 0.04); pooled: flat         | —                                                                                                     | —                                                                    | architectures move in opposite directions; no driver reading                                                   |
| landing gear drawn                           | rises in Multirotor (ρ +0.37, p 0.01); pooled: rises                                         | payload (either way); operating environment (either way); maintenance cost (either way)               | —                                                                    | 3 drivers predict it; the labelled dataset cannot say which acts                                               |
| ● propulsor types per aircraft               | rises in Tilt Propulsor (ρ +0.23, p 0.006); pooled: rises                                    | —                                                                                                     | development and certification cost (fewer); production cost (fewer)  | moved against the only direction any driver predicts; in Tilt Propulsor the added type is a second tilting set |

## IV.2 Links: Tilt Propulsor units by tilting sets, CVT ducting by boom layout

Source: frame `links` of `viz/thesis_q6.py`.

| link                                         | group             |   aircraft |   median |   mean |    rho |           p |      p_holm | movement   |
|:---------------------------------------------|:------------------|-----------:|---------:|-------:|-------:|------------:|------------:|:-----------|
| Tilt Rotor: propulsive units by tilting sets | 1                 |         57 |        2 |  3.42  | nan    | nan         | nan         |            |
| Tilt Rotor: propulsive units by tilting sets | 2                 |         74 |        4 |  7.41  | nan    | nan         | nan         |            |
| Tilt Rotor: propulsive units by tilting sets | 3 or more         |         20 |        6 |  7     | nan    | nan         | nan         |            |
| CVT: ducted share by boom layout             | units on booms    |         53 |      nan |  0.186 |  -0.31 |   0.0249761 |   0.0499522 | falls      |
| CVT: ducted share by boom layout             | no units on booms |         43 |      nan |  0.638 |   0.12 |   0.455621  |   0.455621  | flat       |
| CVT: ducted share by boom layout             | all CVT           |         96 |      nan |  0.387 |  -0.2  |   0.0519001 | nan         | flat       |

## IV.2 Tilt mechanisms per propulsor unit, per architecture and cohort

Source: `q6_tilt_mechanisms_per_propulsor.csv` (tilting sets / propulsor units, mean per cohort, cohorts of 5 designs or more).

| architecture             | cohort   |   aircraft |   mean_per_unit |   rho |      p |   aircraft_in_test |
|:-------------------------|:---------|-----------:|----------------:|------:|-------:|-------------------:|
| Tilt Propulsor           | <= 2011  |         20 |          0.5042 | -0.32 | 0.0001 |                140 |
| Tilt Propulsor           | 2012-15  |         20 |          0.5925 | -0.32 | 0.0001 |                140 |
| Tilt Propulsor           | 2016-19  |         51 |          0.46   | -0.32 | 0.0001 |                140 |
| Tilt Propulsor           | 2020-23  |         49 |          0.3886 | -0.32 | 0.0001 |                140 |
| Combined Vectored Thrust | <= 2011  |          5 |          0.2258 | -0.09 | 0.4063 |                 96 |
| Combined Vectored Thrust | 2012-15  |         10 |          0.2479 | -0.09 | 0.4063 |                 96 |
| Combined Vectored Thrust | 2016-19  |         28 |          0.2453 | -0.09 | 0.4063 |                 96 |
| Combined Vectored Thrust | 2020-23  |         53 |          0.2247 | -0.09 | 0.4063 |                 96 |
| Tilt Wing                | <= 2011  |          4 |        nan      | -0.21 | 0.1381 |                 50 |
| Tilt Wing                | 2012-15  |          6 |          0.4167 | -0.21 | 0.1381 |                 50 |
| Tilt Wing                | 2016-19  |         21 |          0.2837 | -0.21 | 0.1381 |                 50 |
| Tilt Wing                | 2020-23  |         19 |          0.3202 | -0.21 | 0.1381 |                 50 |

Pooled over Tilt Propulsor, CVT and Tilt Wing (mean per cohort): <= 2011 0.467, 2012-15 0.467, 2016-19 0.363, 2020-23 0.306

## Future work: distance of each cohort from the first, and Rao's Q (`q6_centroid_dispersion`; leaves the dissertation)

Source: `q6_centroid_dispersion.csv`. Gower distance over 15 dimensions (four systems, each weighing 1), 619 designs; 1000 permutations, seed 42, cohort sizes kept; band = 2.5th to 97.5th percentile. Distance of a cohort = mean Gower distance between its designs and those of ≤2011 minus the mean of the two Rao's Q.

| cohort   |   aircraft |   d_between |   d_between_low |   d_between_high |      Q |   Q of the earliest cohorts |      ΔQ |   ΔQ permutation low |   ΔQ permutation high | below band   |
|:---------|-----------:|------------:|----------------:|-----------------:|-------:|----------------------------:|--------:|---------------------:|----------------------:|:-------------|
| <= 2011  |         59 |      0      |          0      |           0      | 0.5547 |                      0.5442 |  0.0105 |              -0.0242 |                0.0238 | False        |
| 2012-15  |         57 |      0.0133 |          0.0046 |           0.0181 | 0.5336 |                      0.5442 | -0.0105 |              -0.0238 |                0.0242 | False        |
| 2016-19  |        211 |      0.0102 |          0.0029 |           0.0118 | 0.5682 |                      0.5442 |  0.024  |              -0.0225 |                0.0373 | False        |
| 2020-23  |        237 |      0.0215 |          0.003  |           0.0108 | 0.5185 |                      0.5442 | -0.0257 |              -0.0223 |                0.0361 | True         |

## Numbers quoted by the Results text, IV.1 (sub-question C)

Source: `viz/thesis_q6.py` numbers(ctx).

- `cvt_rb_w4` = 53 %
- `cvt_re_w3` = 46 %
- `slc_lead_w4` = 48 %
- `slc_poss` = 6
- `tr_one_w1` = 75 %
- `tr_one_w4` = 31 %
- `tr_twost_w4` = 39 %
- `w3` = 2016-19

## Numbers quoted by the Results text, IV.2 (sub-question D)

Source: `viz/thesis_q6.py` numbers(ctx).

- `cvt_duct_booms_w3` = 35 %
- `cvt_duct_booms_w4` = 6.1 %
- `cvt_onb_w1` = 20 %
- `cvt_onb_w4` = 62 %
- `slc_onb_w4` = 56 %
- `tr_units_w1` = 2
- `tr_units_w4` = 4
- `traces_moving` = 8

## IV.2 Representative aircraft (`q6_iv2_representative_aircraft`)

Source: `q6_iv2_representative_aircraft.csv`; shares are those of the layout figure.

| architecture             | cohort   | layout                          |   share of the architecture |   designs in the layout |   designs in the architecture | patent number   | design identifier   |   propulsor units |   median units of the layout in the cohort | view            | figure key   |
|:-------------------------|:---------|:--------------------------------|----------------------------:|------------------------:|------------------------------:|:----------------|:--------------------|------------------:|-------------------------------------------:|:----------------|:-------------|
| Lift + Cruise            | <= 2011  | lift units on booms             |                      0.6154 |                       8 |                            13 | US2013020429A1  | US2013020429A1_ad1  |                10 |                                        8.5 | Top             | 1            |
| Lift + Cruise            | 2020-23  | lift units on booms             |                      0.48   |                      36 |                            75 | US2022281593A1  | US2022281593A1_ad1  |                 8 |                                        8   | Top             | 1            |
| Tilt Propulsor           | <= 2011  | one tilting set                 |                      0.75   |                      15 |                            20 | US2013026303A1  | US2013026303A1_ad1  |                 2 |                                        2   | Top             | 13           |
| Tilt Propulsor           | 2020-23  | tilting sets in 2+ places       |                      0.3878 |                      19 |                            49 | US2023331379A1  | US2023331379A1_ad1  |                 4 |                                        6   | Top             | 5            |
| Combined Vectored Thrust | <= 2011  | tilting rotors, fixed elsewhere |                      0.8    |                       4 |                             5 | US2012091257A1  | US2012091257A1_ad1  |                 3 |                                        3.5 | Top             | 3            |
| Combined Vectored Thrust | 2020-23  | tilting rotors, fixed on booms  |                      0.5283 |                      28 |                            53 | US2022306292A1  | US2022306292A1_ad1  |                 6 |                                        6   | Front-Isometric | Fu_D00000    |

## IV.2 Representative aircraft, alternatives (`q6_iv2_representative_aircraft_alt`)

Source: `q6_iv2_representative_aircraft_alt.csv`; shares are those of the layout figure.

| architecture             | cohort   | layout                          |   share of the architecture |   designs in the layout |   designs in the architecture | patent number   | design identifier   |   propulsor units |   median units of the layout in the cohort | view   |   figure key |
|:-------------------------|:---------|:--------------------------------|----------------------------:|------------------------:|------------------------------:|:----------------|:--------------------|------------------:|-------------------------------------------:|:-------|-------------:|
| Lift + Cruise            | <= 2011  | lift units on booms             |                      0.6154 |                       8 |                            13 | US2013020429A1  | US2013020429A1_ad1  |                10 |                                        8.5 | Top    |            1 |
| Lift + Cruise            | 2020-23  | lift units on booms             |                      0.48   |                      36 |                            75 | US2022281593A1  | US2022281593A1_ad1  |                 8 |                                        8   | Top    |            1 |
| Tilt Propulsor           | <= 2011  | one tilting set                 |                      0.75   |                      15 |                            20 | US2013026303A1  | US2013026303A1_ad1  |                 2 |                                        2   | Top    |           13 |
| Tilt Propulsor           | 2020-23  | tilting sets in 2+ places       |                      0.3878 |                      19 |                            49 | US2021229802A1  | US2021229802A1_ad2  |                 4 |                                        6   | Top    |           18 |
| Combined Vectored Thrust | <= 2011  | tilting rotors, fixed elsewhere |                      0.8    |                       4 |                             5 | US2012091257A1  | US2012091257A1_ad1  |                 3 |                                        3.5 | Top    |            3 |
| Combined Vectored Thrust | 2020-23  | tilting rotors, fixed on booms  |                      0.5283 |                      28 |                            53 | US2022388648A1  | US2022388648A1_ad1  |                 6 |                                        6   | Top    |            3 |
