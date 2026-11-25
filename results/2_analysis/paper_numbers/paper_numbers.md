# Numbers for paper item 4

Dataset: eVTOL_dataset (621 designs, 619 with an architecture), thesis seed 42.

## 1. Three largest architectures per cohort

Architecture codes as the dataset names them (TR = TP, TB = TF in the compat layer).

| cohort            |   designs | largest three                  | sum of the three   |
|:------------------|----------:|:-------------------------------|:-------------------|
| <= 2011           |        59 | TR 33.9%, SLC 22.0%, MR 15.2%  | 71.2%              |
| 2012-15           |        57 | TR 35.1%, CVT 17.5%, SLC 15.8% | 68.4%              |
| 2016-19           |       213 | TR 23.9%, SLC 22.5%, CVT 13.2% | 59.6%              |
| 2020-23           |       237 | SLC 31.6%, CVT 22.4%, TR 20.7% | 74.7%              |
| 2024-26 (partial) |        55 | SLC 27.3%, TR 21.8%, CVT 18.2% | 67.3%              |

## 2. Largest architecture share per priority year (all designs)

Maximum over the years read: 36.2%.

|   priority year |   aircraft |   its share | read   |
|----------------:|-----------:|------------:|:-------|
|            2008 |          6 |      0.6667 | False  |
|            2009 |          7 |      0.2857 | False  |
|            2010 |          6 |      0.5    | False  |
|            2011 |         14 |      0.5    | False  |
|            2012 |         14 |      0.5    | False  |
|            2013 |         11 |      0.3636 | False  |
|            2014 |         11 |      0.3636 | False  |
|            2015 |         21 |      0.3333 | True   |
|            2016 |         34 |      0.3235 | True   |
|            2017 |         52 |      0.3077 | True   |
|            2018 |         66 |      0.3182 | True   |
|            2019 |         59 |      0.2373 | True   |
|            2020 |         69 |      0.3623 | True   |
|            2021 |         72 |      0.3333 | True   |
|            2022 |         48 |      0.2917 | True   |
|            2023 |         48 |      0.3125 | True   |

## 3a. Balance (2D) per cohort and level



| level   | cohort            |   aircraft |    D2 |   D2 permutation low |   D2 permutation high | below band   |
|:--------|:------------------|-----------:|------:|---------------------:|----------------------:|:-------------|
| A       | <= 2011           |         59 |  4.8  |                 4.11 |                  6.54 | False        |
| A       | 2012-15           |         57 |  4.9  |                 4.1  |                  6.55 | False        |
| A       | 2016-19           |        211 |  5.93 |                 4.75 |                  5.85 | False        |
| A       | 2020-23           |        237 |  4.55 |                 4.75 |                  5.8  | True         |
| A       | 2024-26 (partial) |         55 |  5.65 |                 4.12 |                  6.52 | False        |
| A·W·T   | <= 2011           |         59 |  8.17 |                 7.02 |                 12    | False        |
| A·W·T   | 2012-15           |         57 |  7.98 |                 7.11 |                 11.94 | False        |
| A·W·T   | 2016-19           |        211 | 10.55 |                 8.29 |                 10.49 | False        |
| A·W·T   | 2020-23           |        236 |  8.36 |                 8.31 |                 10.5  | False        |
| A·W·T   | 2024-26 (partial) |         54 |  9.58 |                 6.93 |                 12.18 | False        |
| A·U     | <= 2011           |         59 | 11.17 |                12.01 |                 19.17 | True         |
| A·U     | 2012-15           |         57 |  9.91 |                11.91 |                 19.22 | True         |
| A·U     | 2016-19           |        211 | 16.26 |                13.91 |                 16.88 | False        |
| A·U     | 2020-23           |        236 | 14.49 |                13.95 |                 16.75 | False        |
| A·U     | 2024-26 (partial) |         55 | 15.74 |                11.71 |                 19.21 | False        |

## 3b. dQ and band edges, 2020-23, three levels and F



| base               | level   |   ²D <= 2011 |   ²D lower band edge <= 2011 |   ²D 2012-15 |   ²D lower band edge 2012-15 |   ²D 2016-19 |   ²D lower band edge 2016-19 |   ²D 2020-23 |   ²D lower band edge 2020-23 |   ΔQ 2020-23 |   ΔQ lower band edge 2020-23 |   ΔQ 2020-23, own baseline |   ΔQ lower band edge 2020-23, own baseline |
|:-------------------|:--------|-------------:|-----------------------------:|-------------:|-----------------------------:|-------------:|-----------------------------:|-------------:|-----------------------------:|-------------:|-----------------------------:|---------------------------:|-------------------------------------------:|
| all designs        | A       |         4.8  |                         4.11 |         4.9  |                         4.1  |         5.93 |                         4.75 |         4.55 |                         4.75 |      -0.0257 |                      -0.0223 |                    -0.0257 |                                    -0.0223 |
| all designs        | A·W·T   |         8.17 |                         7.02 |         7.98 |                         7.11 |        10.55 |                         8.29 |         8.36 |                         8.31 |      -0.0277 |                      -0.0209 |                    -0.0277 |                                    -0.0209 |
| all designs        | A·U     |        11.17 |                        12.01 |         9.91 |                        11.91 |        16.26 |                        13.91 |        14.49 |                        13.95 |      -0.0277 |                      -0.0218 |                    -0.0277 |                                    -0.0218 |
| all designs        | F       |         4.07 |                         3.06 |         4.73 |                         3.01 |         4.82 |                         3.6  |         3.25 |                         3.66 |      -0.0257 |                      -0.0223 |                    -0.0257 |                                    -0.0223 |
| actively protected | A       |         3    |                         2.95 |         3.85 |                         3.53 |         6.02 |                         4.48 |         4.4  |                         4.6  |      -0.0287 |                      -0.0231 |                     0.0112 |                                    -0.0225 |
| actively protected | A·W·T   |         4.15 |                         4.76 |         6.4  |                         6.17 |        11.37 |                         8.28 |         8.27 |                         8.48 |      -0.0313 |                      -0.022  |                     0.0086 |                                    -0.0212 |
| actively protected | A·U     |         5.59 |                         7.04 |         7.31 |                         9.85 |        16.42 |                        13.43 |        13.84 |                        13.82 |      -0.0313 |                      -0.0234 |                     0.0086 |                                    -0.0234 |
| actively protected | F       |         2.84 |                         2.28 |         3.76 |                         2.68 |         5.12 |                         3.4  |         3.14 |                         3.49 |      -0.0287 |                      -0.0231 |                     0.0112 |                                    -0.0225 |

## 4a. Share trends by architecture (Spearman, Holm)



| architecture code   | architecture             |   designs |   years |    rho |     p |   p (Holm) |   rho, 2016-23 |   p, 2016-23 |   p, 2016-23 (Holm) |
|:--------------------|:-------------------------|----------:|--------:|-------:|------:|-----------:|---------------:|-------------:|--------------------:|
| SLC                 | Lift + Cruise            |       142 |      16 |  0.443 | 0.09  |      0.43  |          0.515 |         0.19 |                   1 |
| TP                  | Tilt Propulsor           |       133 |      16 | -0.685 | 0.003 |      0.024 |         -0.452 |         0.26 |                   1 |
| CVT                 | Combined Vectored Thrust |        93 |      16 |  0.256 | 0.34  |      1     |          0.548 |         0.16 |                   1 |
| TW                  | Tilt Wing                |        49 |      16 | -0.144 | 0.59  |      1     |         -0.357 |         0.39 |                   1 |
| MR                  | Multicopter              |        36 |      16 |  0.155 | 0.57  |      1     |         -0.476 |         0.23 |                   1 |
| TF                  | Tilt Frame               |        23 |      16 |  0.001 | 1     |      1     |         -0.405 |         0.32 |                   1 |
| PTC                 | Pitch-to-Cruise          |        22 |      16 |  0.474 | 0.06  |      0.38  |          0.204 |         0.63 |                   1 |

## 4b. Driver trends inside architectures (Spearman, Holm)



| trace                                    | architecture                    | code   |   aircraft | first cohort   |   first value |   2020-23 value |    rho |             p |      p_holm | movement   |
|:-----------------------------------------|:--------------------------------|:-------|-----------:|:---------------|--------------:|----------------:|-------:|--------------:|------------:|:-----------|
| tilting joint groups                     | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0    |            0    | nan    | nan           | nan         | constant   |
| tilting joint groups                     | Tilt Propulsor                  | TR     |        140 | <= 2011        |          1    |            2    |   0.22 |   0.00990773  |   0.0198155 | rises      |
| tilting joint groups                     | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          1    |            1    |   0.25 |   0.0134655   |   0.0198155 | rises      |
| tilting joint groups                     | Tilt Wing                       | TW     |         50 | 2012-15        |          1    |            1    |  -0.12 |   0.412058    | nan         | flat       |
| tilting joint groups                     | Multirotor                      | MR     |         43 | <= 2011        |          0    |            0    |   0.1  |   0.527669    | nan         | flat       |
| tilting joint groups                     | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          1    |            1    |  -0.01 |   0.891507    | nan         | flat       |
| tilting joint groups                     | all classed aircraft            | ALL    |        536 | <= 2011        |          1    |            1    |  -0.01 |   0.76624     | nan         | flat       |
| a propulsor retracts or folds its blades | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0    |            0.07 |  -0.03 |   0.740757    |   0.740757  | flat       |
| a propulsor retracts or folds its blades | Tilt Propulsor                  | TR     |        140 | <= 2011        |          0    |            0    |  -0.08 |   0.360257    |   0.720514  | flat       |
| a propulsor retracts or folds its blades | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          0.2  |            0.13 |  -0.15 |   0.155901    |   0.467702  | flat       |
| a propulsor retracts or folds its blades | Tilt Wing                       | TW     |         50 | 2012-15        |          0    |            0.05 |   0.2  |   0.155031    | nan         | flat       |
| a propulsor retracts or folds its blades | Multirotor                      | MR     |         43 | <= 2011        |          0    |            0.13 |   0.22 |   0.164247    | nan         | flat       |
| a propulsor retracts or folds its blades | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          0.02 |            0.07 |   0.01 |   0.855815    | nan         | flat       |
| a propulsor retracts or folds its blades | all classed aircraft            | ALL    |        536 | <= 2011        |          0.02 |            0.06 |   0    |   0.933134    | nan         | flat       |
| booms stow                               | Lift + Cruise                   | SLC    |         81 | <= 2011        |          0    |            0.05 |   0.04 |   0.745846    |   1         | flat       |
| booms stow                               | Tilt Propulsor                  | TR     |         52 | 2012-15        |          0    |            0    | nan    | nan           | nan         | constant   |
| booms stow                               | Combined Vectored Thrust        | CVT    |         55 | 2016-19        |          0.06 |            0.06 |  -0.08 |   0.580149    |   1         | flat       |
| booms stow                               | Tilt Wing                       | TW     |         14 | 2016-19        |          0    |            0    | nan    | nan           | nan         | too thin   |
| booms stow                               | Multirotor                      | MR     |         25 | 2016-19        |          0    |            0.11 |   0.2  |   0.332409    | nan         | flat       |
| booms stow                               | five drawn architectures pooled | ALL5   |        227 | <= 2011        |          0    |            0.05 |   0.03 |   0.684236    | nan         | flat       |
| booms stow                               | all classed aircraft            | ALL    |        257 | <= 2011        |          0    |            0.04 |   0.04 |   0.547882    | nan         | flat       |
| units carried on booms                   | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0.62 |            0.56 |   0.05 |   0.545261    |   0.545261  | flat       |
| units carried on booms                   | Tilt Propulsor                  | TR     |        140 | <= 2011        |          0.2  |            0.39 |   0.11 |   0.201741    |   0.403482  | flat       |
| units carried on booms                   | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          0.2  |            0.62 |   0.22 |   0.0329559   |   0.0988678 | rises      |
| units carried on booms                   | Tilt Wing                       | TW     |         50 | 2012-15        |          0    |            0.26 |   0.28 |   0.0453358   | nan         | rises      |
| units carried on booms                   | Multirotor                      | MR     |         43 | <= 2011        |          0.11 |            0.6  |   0.26 |   0.0882352   | nan         | flat       |
| units carried on booms                   | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          0.27 |            0.51 |   0.16 |   0.000579916 | nan         | rises      |
| units carried on booms                   | all classed aircraft            | ALL    |        536 | <= 2011        |          0.27 |            0.49 |   0.14 |   0.00159009  | nan         | rises      |
| booms present                            | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0.62 |            0.56 |   0.05 |   0.545261    |   0.545261  | flat       |
| booms present                            | Tilt Propulsor                  | TR     |        140 | <= 2011        |          0.2  |            0.41 |   0.12 |   0.149308    |   0.298616  | flat       |
| booms present                            | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          0.4  |            0.62 |   0.18 |   0.0842121   |   0.252636  | flat       |
| booms present                            | Tilt Wing                       | TW     |         50 | 2012-15        |          0.17 |            0.26 |   0.12 |   0.414471    | nan         | flat       |
| booms present                            | Multirotor                      | MR     |         43 | <= 2011        |          0.11 |            0.6  |   0.26 |   0.0882352   | nan         | flat       |
| booms present                            | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          0.31 |            0.52 |   0.14 |   0.00231008  | nan         | rises      |
| booms present                            | all classed aircraft            | ALL    |        564 | <= 2011        |          0.31 |            0.49 |   0.12 |   0.00615385  | nan         | rises      |
| a ducted unit                            | Lift + Cruise                   | SLC    |        145 | <= 2011        |          0.38 |            0.48 |   0.11 |   0.179996    |   0.359991  | flat       |
| a ducted unit                            | Tilt Propulsor                  | TR     |        140 | <= 2011        |          0.15 |            0.31 |   0.04 |   0.626798    |   0.626798  | flat       |
| a ducted unit                            | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          0.8  |            0.32 |  -0.2  |   0.0519001   |   0.1557    | flat       |
| a ducted unit                            | Tilt Wing                       | TW     |         50 | 2012-15        |          0    |            0.16 |  -0.02 |   0.916865    | nan         | flat       |
| a ducted unit                            | Multirotor                      | MR     |         43 | <= 2011        |          0.78 |            0.73 |   0.06 |   0.698686    | nan         | flat       |
| a ducted unit                            | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          0.39 |            0.39 |  -0    |   0.930542    | nan         | flat       |
| a ducted unit                            | all classed aircraft            | ALL    |        536 | <= 2011        |          0.36 |            0.37 |  -0.01 |   0.792409    | nan         | flat       |
| propulsor types                          | Lift + Cruise                   | SLC    |        145 | <= 2011        |          3    |            3    |  -0.05 |   0.578272    |   0.578272  | flat       |
| propulsor types                          | Tilt Propulsor                  | TR     |        140 | <= 2011        |          1    |            2    |   0.23 |   0.00579278  |   0.0173784 | rises      |
| propulsor types                          | Combined Vectored Thrust        | CVT    |         96 | <= 2011        |          2    |            3    |   0.14 |   0.165697    |   0.331395  | flat       |
| propulsor types                          | Tilt Wing                       | TW     |         50 | 2012-15        |          1.5  |            1    |  -0.05 |   0.715321    | nan         | flat       |
| propulsor types                          | Multirotor                      | MR     |         43 | <= 2011        |          2    |            2    |   0.09 |   0.572457    | nan         | flat       |
| propulsor types                          | five drawn architectures pooled | ALL5   |        474 | <= 2011        |          2    |            2    |   0.18 |   5.32632e-05 | nan         | rises      |
| propulsor types                          | all classed aircraft            | ALL    |        536 | <= 2011        |          2    |            2    |   0.18 |   2.21183e-05 | nan         | rises      |

## 4c. Share of CVT designs with propulsors on booms



| window               |   aircraft |   aircraft, units on booms |   share with units on booms |
|:---------------------|-----------:|---------------------------:|----------------------------:|
| <= 2011              |          5 |                          1 |                       0.2   |
| 2012-15              |         10 |                          2 |                       0.2   |
| 2016-19              |         28 |                         17 |                       0.607 |
| 2020-23              |         53 |                         33 |                       0.623 |
| 2024-26 (incomplete) |         10 |                          6 |                       0.6   |

## 4d. Median propulsor units by cohort



| architecture             | <= 2011   | 2012-15   | 2016-19   | 2020-23   | 2024-26 (incomplete)   |
|:-------------------------|:----------|:----------|:----------|:----------|:-----------------------|
| Tilt Propulsor           | 2 (n 20)  | 2 (n 20)  | 4 (n 51)  | 4 (n 49)  | 7 (n 12)               |
| Combined Vectored Thrust | 4 (n 5)   | 4 (n 10)  | 5 (n 28)  | 6 (n 53)  | 6 (n 10)               |
| Lift + Cruise            | 7 (n 13)  | 5 (n 9)   | 7 (n 48)  | 7 (n 75)  | 7 (n 15)               |

## 5. Assignees

From the design table (aircraft_id, assignee as recorded). The patent-level view is in q2_largest_filers_share.csv.

|   assignees (designs) |   with one design | largest assignee                 |   its designs |   its share of designs |   designs |
|----------------------:|------------------:|:---------------------------------|--------------:|-----------------------:|----------:|
|                   368 |               277 | BELL HELICOPTER TEXTRON INC (US) |            23 |                  0.037 |       621 |

## 5b. Without Bell / Textron



| table                                      | cohort            |   Tilt Propulsor | assignees              |   designs |   share % | reading            | architecture             |   designs 2008-2023 |   rho 2008-2023 |   p 2008-2023 |   p 2008-2023 (Holm) |   rho 2016-2023 |   p 2016-2023 |   p 2016-2023 (Holm) |
|:-------------------------------------------|:------------------|-----------------:|:-----------------------|----------:|----------:|:-------------------|:-------------------------|--------------------:|----------------:|--------------:|---------------------:|----------------:|--------------:|---------------------:|
| 2 Tilt Propulsor share per cohort          | <= 2011           |               20 | all assignees          |        59 |      33.9 | 20 of 59 (33.9 %)  | nan                      |                 nan |         nan     |       nan     |              nan     |         nan     |       nan     |              nan     |
| 2 Tilt Propulsor share per cohort          | 2012-15           |               20 | all assignees          |        57 |      35.1 | 20 of 57 (35.1 %)  | nan                      |                 nan |         nan     |       nan     |              nan     |         nan     |       nan     |              nan     |
| 2 Tilt Propulsor share per cohort          | 2016-19           |               51 | all assignees          |       213 |      23.9 | 51 of 213 (23.9 %) | nan                      |                 nan |         nan     |       nan     |              nan     |         nan     |       nan     |              nan     |
| 2 Tilt Propulsor share per cohort          | 2020-23           |               49 | all assignees          |       237 |      20.7 | 49 of 237 (20.7 %) | nan                      |                 nan |         nan     |       nan     |              nan     |         nan     |       nan     |              nan     |
| 2 Tilt Propulsor share per cohort          | 2024-26 (partial) |               12 | all assignees          |        55 |      21.8 | 12 of 55 (21.8 %)  | nan                      |                 nan |         nan     |       nan     |              nan     |         nan     |       nan     |              nan     |
| 2 Tilt Propulsor share per cohort          | <= 2011           |               18 | without Bell / Textron |        57 |      31.6 | 18 of 57 (31.6 %)  | nan                      |                 nan |         nan     |       nan     |              nan     |         nan     |       nan     |              nan     |
| 2 Tilt Propulsor share per cohort          | 2012-15           |               18 | without Bell / Textron |        55 |      32.7 | 18 of 55 (32.7 %)  | nan                      |                 nan |         nan     |       nan     |              nan     |         nan     |       nan     |              nan     |
| 2 Tilt Propulsor share per cohort          | 2016-19           |               34 | without Bell / Textron |       180 |      18.9 | 34 of 180 (18.9 %) | nan                      |                 nan |         nan     |       nan     |              nan     |         nan     |       nan     |              nan     |
| 2 Tilt Propulsor share per cohort          | 2020-23           |               44 | without Bell / Textron |       215 |      20.5 | 44 of 215 (20.5 %) | nan                      |                 nan |         nan     |       nan     |              nan     |         nan     |       nan     |              nan     |
| 2 Tilt Propulsor share per cohort          | 2024-26 (partial) |               11 | without Bell / Textron |        54 |      20.4 | 11 of 54 (20.4 %)  | nan                      |                 nan |         nan     |       nan     |              nan     |         nan     |       nan     |              nan     |
| 3-4 Spearman rho of share on priority year | nan               |              nan | all assignees          |       nan |     nan   | nan                | Lift + Cruise            |                 142 |           0.443 |         0.085 |                0.427 |           0.515 |         0.192 |                1     |
| 3-4 Spearman rho of share on priority year | nan               |              nan | all assignees          |       nan |     nan   | nan                | Tilt Propulsor           |                 133 |          -0.685 |         0.003 |                0.024 |          -0.452 |         0.26  |                1     |
| 3-4 Spearman rho of share on priority year | nan               |              nan | all assignees          |       nan |     nan   | nan                | Combined Vectored Thrust |                  93 |           0.256 |         0.338 |                1     |           0.548 |         0.16  |                1     |
| 3-4 Spearman rho of share on priority year | nan               |              nan | all assignees          |       nan |     nan   | nan                | Tilt Wing                |                  49 |          -0.144 |         0.594 |                1     |          -0.357 |         0.385 |                1     |
| 3-4 Spearman rho of share on priority year | nan               |              nan | all assignees          |       nan |     nan   | nan                | Multicopter              |                  36 |           0.155 |         0.566 |                1     |          -0.476 |         0.233 |                1     |
| 3-4 Spearman rho of share on priority year | nan               |              nan | all assignees          |       nan |     nan   | nan                | Tilt Frame               |                  23 |           0.001 |         0.996 |                1     |          -0.405 |         0.32  |                1     |
| 3-4 Spearman rho of share on priority year | nan               |              nan | all assignees          |       nan |     nan   | nan                | Pitch-to-Cruise          |                  22 |           0.474 |         0.064 |                0.383 |           0.204 |         0.629 |                1     |
| 3-4 Spearman rho of share on priority year | nan               |              nan | without Bell / Textron |       nan |     nan   | nan                | Lift + Cruise            |                 141 |           0.39  |         0.135 |                0.752 |           0.548 |         0.16  |                0.96  |
| 3-4 Spearman rho of share on priority year | nan               |              nan | without Bell / Textron |       nan |     nan   | nan                | Tilt Propulsor           |                 107 |          -0.538 |         0.032 |                0.221 |          -0.048 |         0.911 |                1     |
| 3-4 Spearman rho of share on priority year | nan               |              nan | without Bell / Textron |       nan |     nan   | nan                | Combined Vectored Thrust |                  76 |           0.102 |         0.708 |                1     |           0.452 |         0.26  |                1     |
| 3-4 Spearman rho of share on priority year | nan               |              nan | without Bell / Textron |       nan |     nan   | nan                | Tilt Wing                |                  42 |          -0.267 |         0.318 |                1     |          -0.595 |         0.12  |                0.837 |
| 3-4 Spearman rho of share on priority year | nan               |              nan | without Bell / Textron |       nan |     nan   | nan                | Multicopter              |                  35 |           0.138 |         0.611 |                1     |          -0.524 |         0.183 |                0.96  |
| 3-4 Spearman rho of share on priority year | nan               |              nan | without Bell / Textron |       nan |     nan   | nan                | Pitch-to-Cruise          |                  22 |           0.399 |         0.125 |                0.752 |          -0.359 |         0.382 |                1     |
| 3-4 Spearman rho of share on priority year | nan               |              nan | without Bell / Textron |       nan |     nan   | nan                | Tilt Frame               |                  17 |          -0.032 |         0.907 |                1     |           0.132 |         0.756 |                1     |

## 6a. F share by priority year, all and protected



|   priority year |   aircraft |   F aircraft |   F share |   aircraft in force |   F aircraft in force |   F share in force |
|----------------:|-----------:|-------------:|----------:|--------------------:|----------------------:|-------------------:|
|            2019 |         59 |           24 |    0.4068 |                  44 |                    16 |             0.3636 |
|            2020 |         69 |           34 |    0.4928 |                  54 |                    28 |             0.5185 |
|            2021 |         72 |           41 |    0.5694 |                  59 |                    35 |             0.5932 |
|            2022 |         48 |           23 |    0.4792 |                  35 |                    15 |             0.4286 |
|            2023 |         48 |           19 |    0.3958 |                  44 |                    19 |             0.4318 |

## 6b. F share by region



| region        |   F aircraft 2012-15 |   F base 2012-15 |   F share 2012-15 |   F aircraft 2016-19 |   F base 2016-19 |   F share 2016-19 |   F aircraft 2020-23 |   F base 2020-23 |   F share 2020-23 |
|:--------------|---------------------:|-----------------:|------------------:|---------------------:|-----------------:|------------------:|---------------------:|-----------------:|------------------:|
| North America |                    8 |               28 |            0.2857 |                   28 |              104 |            0.2692 |                   37 |               77 |            0.4805 |
| Europe        |                    5 |               23 |            0.2174 |                   23 |               64 |            0.3594 |                   36 |               63 |            0.5714 |
| Asia-Pacific  |                    0 |                6 |            0      |                   16 |               36 |            0.4444 |                   42 |               92 |            0.4565 |

## 7a. Distance dimensions (the 15 used for disparity) and designs answering

Dimensions answered for at least 500 designs: 15 of 15.

| dimension                  |   answered |
|:---------------------------|-----------:|
| Architecture               |        619 |
| Fuselage Shape             |        596 |
| Boom count                 |        619 |
| Fuselage Kinematics        |        595 |
| Wing count                 |        618 |
| Wing Architecture          |        536 |
| Vertical Position          |        514 |
| Longitudinal Position      |        514 |
| Planform                   |        532 |
| Empennage Type             |        593 |
| Propulsor band             |        589 |
| Tilt share                 |        588 |
| Propulsor Enclosure        |        588 |
| Tractor/Pusher Arrangement |        522 |
| Mount locations            |        588 |

## 7b. Dimensions of the design-space table and designs answering

Answered for at least 500 designs: 11 of 11.

| dimension                                    |   answered |
|:---------------------------------------------|-----------:|
| number of wings (winged designs)             |        542 |
| tail type                                    |        594 |
| fuselage motion hover to cruise              |        596 |
| wing configuration                           |        537 |
| landing-gear type                            |        596 |
| left-right symmetry                          |        621 |
| fuselage shape                               |        597 |
| booms present                                |        621 |
| propulsor units per aircraft (band)          |        589 |
| places carrying propulsor units per aircraft |        589 |
| propulsor enclosure (any ducted)             |        589 |
