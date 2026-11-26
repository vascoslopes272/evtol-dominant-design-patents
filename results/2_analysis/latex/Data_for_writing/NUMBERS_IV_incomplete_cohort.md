# NUMBERS_IV, the incomplete 2024-26 cohort (drawn, never tested)

Written by notebook 24_evolution_of_the_design_space (`viz/thesis_latex_part4.py`, refresh of 2026-10-16). The 2024-26 cohort is the fifth column or point of the Analysis IV figures; it enters no test, no disparity and no number of `NUMBERS_IV.md`, which stays on the four complete cohorts. Designs with a priority year of 2024 or later.

## Layout shares, 2024-26 (share of the architecture's designs)

Source: `q6_leading_layout_by_architecture.csv`, rows `2024-26 (incomplete)`.

| architecture                   | layout                                     |   designs |   of | share   |
|:-------------------------------|:-------------------------------------------|----------:|-----:|:--------|
| Combined Vectored Thrust (CVT) | a wing tilts · fixed elsewhere             |         1 |   10 | 10.0 %  |
| Combined Vectored Thrust (CVT) | propulsors and a wing tilt · no fixed unit |         2 |   10 | 20.0 %  |
| Combined Vectored Thrust (CVT) | propulsors tilt · fixed elsewhere          |         4 |   10 | 40.0 %  |
| Combined Vectored Thrust (CVT) | propulsors tilt · fixed on booms           |         3 |   10 | 30.0 %  |
| Separate Lift + Cruise (SLC)   | on booms                                   |        10 |   15 | 66.7 %  |
| Separate Lift + Cruise (SLC)   | on booms, stowed in cruise                 |         1 |   15 | 6.7 %   |
| Separate Lift + Cruise (SLC)   | on the body, stowed in cruise              |         1 |   15 | 6.7 %   |
| Separate Lift + Cruise (SLC)   | on the wing                                |         3 |   15 | 20.0 %  |
| Tilt Propulsor (TP)            | 2+ tilting sets, in one place              |         2 |   12 | 16.7 %  |
| Tilt Propulsor (TP)            | 2+ tilting sets, in 2+ places              |        10 |   12 | 83.3 %  |

## Traces, 2024-26 (per architecture)

Source: `q6_architecture_centres_tilting_units.csv`, `q6_boom_share_by_architecture.csv`, `q6_cvt_units_on_booms.csv`, `q6_ducted_share_by_architecture.csv`, `q6_cvt_ducted_by_boom_layout.csv`, rows `2024-26 (incomplete)`. A cell is blank under 5 designs (the same rule as every other cohort).

| class                          |   aircraft |   tilting sets (mean) |   propulsive units (median) |   share with units on booms |   share with a ducted unit |   aircraft, units on booms |   ducted share, units on booms |   aircraft, no units on booms |   ducted share, no units on booms |
|:-------------------------------|-----------:|----------------------:|----------------------------:|----------------------------:|---------------------------:|---------------------------:|-------------------------------:|------------------------------:|----------------------------------:|
| Separate Lift + Cruise (SLC)   |         15 |                 0     |                           7 |                       0.733 |                      0.267 |                         11 |                        nan     |                             4 |                               nan |
| Tilt Propulsor (TP)            |         12 |                 2.583 |                           7 |                       0.5   |                      0.333 |                          6 |                        nan     |                             6 |                               nan |
| Combined Vectored Thrust (CVT) |         10 |                 1.9   |                           6 |                       0.6   |                      0.3   |                          6 |                          0.333 |                             4 |                               nan |
