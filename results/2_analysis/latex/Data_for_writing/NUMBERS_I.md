# NUMBERS_I — Analysis I (evidence base)

Generated 2026-11-25 by notebook 21_evidence_base (`viz/latex_text.py:write_numbers_I`) from the current inputs (external inputs: `script`), 621 designs, snapshot 2026-06-08. Every value is computed when this file is written; the source column names the CSV or the code that holds it. A value marked **new** is a number the earlier text did not quote.

## 1. Growth

### Doubling times, 2005-2023 (years, 95 % interval)

| number | value | source |
|---|---|---|
| eVTOL architecture patent families | 3.5 (3.0 to 4.3) | csv/q1_growth_rates.csv; csv/numbers_I_growth.csv; q1.numbers()['dbl_fam'] |
| eVTOL unique designs | 3.5 (2.8 to 4.5) | csv/numbers_I_growth.csv; q1.numbers()['dbl_ac'] |
| aeronautics (CPC B64) | 4.7 (4.1 to 5.6) | csv/numbers_I_growth.csv; q1.numbers()['dbl_b64'] |
| transport and operations (CPC section B) | 6.4 (5.4 to 7.9) | csv/numbers_I_growth.csv; q1.numbers()['dbl_secb'] |
| all patenting | 10.7 (9.6 to 12.2) | csv/numbers_I_growth.csv; q1.numbers()['dbl_all'] |
| growth per year, eVTOL architecture patent families | 22 % | csv/numbers_I_growth.csv |

### Growth-rate ratio of eVTOL architecture patent families (times as fast, 95 % interval)

| number | value | source |
|---|---|---|
| against aeronautics (CPC B64) | 1.34 (1.23 to 1.47) | csv/numbers_I_growth.csv; q1.numbers()['gr_fam_b64'], ['gr_fam_b64_ci'] |
| against transport and operations | 1.82 (1.63 to 1.98) | csv/numbers_I_growth.csv; q1.numbers()['gr_fam_secb'] |
| against all patents | 3.05 (2.74 to 3.38) | csv/numbers_I_growth.csv; q1.numbers()['gr_fam_all'] |
| against aeronautics with the fit ended at 2019 (sensitivity) | 1.28 (1.10 to 1.42) | q1.numbers()['gr_fam_b64_19'], ['gr_fam_b64_19_ci'] |

### Turning point (two-segment log fit, residual bootstrap, 5 000 draws as set in lib/growth.py)

| number | value | source |
|---|---|---|
| representative patents | 2016 (jump x3.45; chosen by 91 % of the resampled fits; 95 % range of the resampled year 2015 to 2018) | csv/numbers_I_turning_points.csv; lib/growth.py:turning_point |
| unique aircraft | 2017 (jump x1.83; chosen by 23 % of the resampled fits; 95 % range of the resampled year 2010 to 2020) | csv/numbers_I_turning_points.csv; lib/growth.py:turning_point |
| aircraft per 1 000 B64 | 2013 (jump x0.49; chosen by 18 % of the resampled fits; 95 % range of the resampled year 2009 to 2020) | csv/numbers_I_turning_points.csv; lib/growth.py:turning_point |

## 2. Active protection (every priority year; actively protected = any patent that shows the design is in force at the snapshot)

### The 604 designs of the nine architectures of ten designs or more (the designs plotted in `q1_in_force_status`)

| number | value | source |
|---|---|---|
| designs plotted | 598 | csv/q1_in_force_status.csv (sum of n) |
| not actively protected, all 604 | 180 of 598 = 30.1 % | csv/q1_in_force_status.csv; csv/numbers_I_active_protection_by_architecture.csv |
| US office: designs, share not actively protected | 352 designs, 81 = 23.0 % | csv/q1_in_force_status.csv |
| other offices: designs, share not actively protected | 246 designs, 99 = 40.2 % | csv/q1_in_force_status.csv |
| test of the architecture (nine architectures x not actively protected) | chi-square 12.38, df 8, p 0.135 | lib/association.chi2_test on the 604 designs; q1.numbers()['fa_p'] |
| test of the office (US against other offices x not actively protected), on the 604 | chi-square 19.63, df 1 (Yates correction, 2 x 2), p 9.4e-06 | lib/association.chi2_test on the 604 designs; **new** |
| the same office test on all 625 designs with an architecture (the earlier text) | chi-square 22.54, df 1, p 2.1e-06; US 22.9 % of 363, other offices 41.0 % of 256 | q1.numbers()['fo_us'], ['fo_else'], ['fo_n_us'], ['fo_n_else'], ['fo_p'] |

Share not actively protected per architecture (the nine plotted):

| architecture | code | designs | not actively protected | share |
|---|---|---|---|---|
| Lift + Cruise | SLC | 160 | 49 | 31 % |
| Tilt Propulsor | TP | 152 | 40 | 26 % |
| Combined Vectored Thrust | CVT | 106 | 31 | 29 % |
| Tilt Wing | TW | 54 | 17 | 31 % |
| Multicopter | MR | 47 | 16 | 34 % |
| Pitch-to-Cruise | PTC | 25 | 3 | 12 % |
| Tilt Frame | TF | 25 | 13 | 52 % |
| Hoverbike | HB | 19 | 8 | 42 % |
| Personal Flying Vehicle | PFV | 10 | 3 | 30 % |

### Designs not plotted in `q1_in_force_status`

| number | value | source |
|---|---|---|
| DS (Deflected Slipstream) | 4 designs, 25 % not actively protected | csv/numbers_I_active_protection_by_architecture.csv |
| RC (Rotorcraft) | 9 designs, 44 % not actively protected | csv/numbers_I_active_protection_by_architecture.csv |
| SRW (Stopped/Slowed Rotor Wing) | 8 designs, 38 % not actively protected | csv/numbers_I_active_protection_by_architecture.csv |
| no architecture read | 2 designs (read for legal status, see the all-designs table below) | viz/frames.py:force_frame drops a design without an architecture |
| designs not plotted, total | 23 of 621 (604 plotted) |  |

### The share if every design is read

| number | value | source |
|---|---|---|
| designs with a legal status read | 621 | frames.aircraft_patents, every design has at least one patent with a status |
| not actively protected | 190 of 621 = 30.6 % | **new** |
| (for comparison) the 625 designs with an architecture | 188 of 619 = 30.4 % | q1.numbers()['fa_share'], ['fa_n'] |

Share not actively protected per priority-year cohort (the age effect):

| cohort | designs (625 read) | share not actively protected (625) | designs (604 plotted) | share not actively protected (604) |
|---|---|---|---|---|
| <= 2011 | 59 | 69.5 % | 57 | 70.2 % |
| 2012-15 | 57 | 43.9 % | 56 | 42.9 % |
| 2016-19 | 211 | 34.6 % | 203 | 34.5 % |
| 2020-23 | 237 | 19.0 % | 230 | 18.3 % |
| 2024-26 (partial) | 55 | 7.3 % | 52 | 7.7 % |

### Age at lapse and share not actively protected per priority year (follow-up 2026-10-24)

Source: `viz/followup_lapse_age.py`; CSV `q1_age_at_lapse.csv`, `q1_age_at_lapse_patents.csv`, `q1_not_protected_by_priority_year.csv`. Designs: the 598 of `q1_in_force_status`. Patents: every patent linked to those designs (own primary patent plus D1/D2 duplicates, `frames.aircraft_patents`) whose PatSeer legal status is INACTIVE. Age at lapse = lapse date minus priority date (`Priority Date (Record)`), in years of 365.25 days. **Lapse date = PatSeer `Estimated Expiry Date`** of an INACTIVE record: the export has no separate lapse-date column; for these records the field holds the date of the last status event (it equals `Register Legal Status Date` for 79 % of the 230 records that have one). Office = the patent's own publication office (US against all others, WO included), not the design's. Snapshot 2026-06-08. 'Lapsed' here is every INACTIVE status: nonpayment, expired, withdrawn / abandoned, rejected. 216 inactive patents; left out: 2 with a date after the snapshot, 0 without a usable date.

| group              |   lapsed patents |   median (years) |   10th percentile (years) |   90th percentile (years) |
|:-------------------|-----------------:|-----------------:|--------------------------:|--------------------------:|
| all lapsed patents |              214 |             3.81 |                      2.25 |                      9.95 |
| US office          |              104 |             4.68 |                      2.75 |                     12.94 |
| other offices      |              110 |             3.5  |                      1.6  |                      6.52 |

By legal status (median age at lapse):

| legal status                              |   lapsed patents |   median (years) |
|:------------------------------------------|-----------------:|-----------------:|
| INACTIVE - EXPIRED                        |               40 |             3.5  |
| INACTIVE - NONPAYMENT                     |               46 |             6.8  |
| INACTIVE - REJECTED / REFUSED / SUSPENDED |               24 |             2.92 |
| INACTIVE - WITHDRAWN / SURRENDERED        |              104 |             3.73 |

Designs not actively protected, per priority year (no linked patent in force):

|   priority year |   designs |   not actively protected | share   |
|----------------:|----------:|-------------------------:|:--------|
|            1999 |         1 |                        1 | 100.0 % |
|            2001 |         5 |                        1 | 20.0 %  |
|            2002 |         1 |                        1 | 100.0 % |
|            2003 |         4 |                        4 | 100.0 % |
|            2004 |         5 |                        5 | 100.0 % |
|            2005 |         3 |                        3 | 100.0 % |
|            2006 |         5 |                        5 | 100.0 % |
|            2008 |         6 |                        3 | 50.0 %  |
|            2009 |         7 |                        4 | 57.1 %  |
|            2010 |         6 |                        3 | 50.0 %  |
|            2011 |        14 |                       10 | 71.4 %  |
|            2012 |        13 |                        4 | 30.8 %  |
|            2013 |        11 |                        7 | 63.6 %  |
|            2014 |        11 |                        6 | 54.5 %  |
|            2015 |        21 |                        7 | 33.3 %  |
|            2016 |        32 |                       10 | 31.2 %  |
|            2017 |        50 |                       18 | 36.0 %  |
|            2018 |        62 |                       27 | 43.5 %  |
|            2019 |        59 |                       15 | 25.4 %  |
|            2020 |        69 |                       15 | 21.7 %  |
|            2021 |        71 |                       12 | 16.9 %  |
|            2022 |        46 |                       13 | 28.3 %  |
|            2023 |        44 |                        2 | 4.5 %   |
|            2024 |        36 |                        1 | 2.8 %   |
|            2025 |        14 |                        3 | 21.4 %  |
|            2026 |         2 |                        0 | 0.0 %   |

## 3. The acquisition funnel of section 4.1

| step | count | source |
|---|---|---|
| patent query hits (PatSeer, snapshot 2026-06-08) | 1639 | ds.counts['patents_acquired'] |
| disapproved at labelling (no usable image, pure UAV, out of the domain, other) | 531 | difference |
| after the patent triage T1: patents approved at labelling | 1108 | ds.counts['patents_wizard_approved'] |
| approved patents whose every aircraft is 'but similar' (UAV or not electric), set aside | 232 | ds.counts['patents_gated_out'] |
| representative patents (patent families) | 876 | ds.counts['patents_approved'] |
| aircraft observations (a patent can show several aircraft) | 957 | ds.counts['approved_variants'] |
| all designs (unique aircraft), on primary patents | 621 | len(ctx.v); primary patents 540 |
| after the image triage T2: whole-aircraft figures approved | 1530 | ds.counts['approved_figures']; on 575 patents |

*Mapping of T1 and T2:* the repository names the stages above; **T1 = the patent triage at labelling (1 109 approved, then the domain gate to 879)** and **T2 = the figure approval (1 538 whole-aircraft figures on 578 patents)** is my reading of your two names. The 627 designs sit between them (a design needs approved figures). Tell me if your T1 or T2 is another step.

### The VFS eVTOL directory and the company map

| number | value | source |
|---|---|---|
| directory aircraft pages | 1229 | frames.directory_frame; csv/numbers_I_funnel.csv |
| kept by the corrected domain rules | 871 | frames.directory_frame()['in_domain'] (rules of Section 3.1.1 and the author's single-page rulings) |
| matched to a design (pages linked to a patent design, use = yes) | 97 pages, 99 designs | evtolnews_patent_links.csv, use = yes |
| of those pages, kept in the domain | 83 | frames.directory_frame() |
| index companies read in full (AAM Reality Index company map rows) | 43 | ari_firm_map / review/script_outputs/COMPANY_MAP.csv |
| companies the script matches to a company of the dataset (non-blank match) | 18 | notebooks/_build/yearscript/ari_rule.py |
| companies where the script's match equals the author's name | 35 of 43 | notebook 60, review/script_outputs/COMPANY_MAP.csv |
| index companies that file in the dataset | 22 | frames.ari_firms; csv/numbers_I_funnel.csv |
| of them, in the current index release with a first flight and entry date (the clock figure) | 14 | frames.ari_timeline; csv/q4_patent_vs_market_clock.csv |

*If any count differs from the ones you listed:* one reading differs. The directory's 1 229 pages, the 871 kept, the 97 matched pages, the 43 companies read and the 22 that file all match. The **35** is the number of the 43 companies on which the script's answer equals the author's, counting the companies both leave blank; the script returns a non-blank match for **18** of them. Say which of the two the text should print.

### The funnel family: six tests, Holm-corrected (supervisor review 2)

Pearson chi-square of each group against the rest of the 627 designs (`frames.representativeness`); the Holm correction runs once over the six raw p (`lib.multiple.holm`). Source: `viz/thesis_q4.py:funnel_family`; CSV: `numbers_I_funnel_family_holm.csv`.

| key | groups | attribute | p raw | p Holm |
|---|---|---|---|---|
| `flown_cohort_p_holm` | flown designs (TRL 5 or more) (68) vs the rest (553) | priority-year cohort | 0.0372 | 0.180 |
| `flown_class_p_holm` | flown designs (TRL 5 or more) (68) vs the rest (553) | architecture (five directory categories) | 0.1594 | 0.478 |
| `flown_region_p_holm` | flown designs (TRL 5 or more) (68) vs the rest (553) | applicant region | 0.3341 | 0.478 |
| `fari_cohort_p_holm` | designs of the flown index assignees (42) vs the rest (579) | priority-year cohort | 0.2021 | 0.478 |
| `fari_class_p_holm` | designs of the flown index assignees (42) vs the rest (579) | architecture (five directory categories) | 0.0360 | 0.180 |
| `fari_region_p_holm` | designs of the flown index assignees (42) vs the rest (579) | applicant region | 0.0014 | 0.008 |

### I.3, propulsors of the flown designs (Mann-Whitney)

Source: `viz/flown_propulsors.py` (follow-up 2026-10-27; no figure, table or other number changed). Flown = TRL 5 or more (`viz/thesis_q4.py:representativeness`); the rest = the other designs of the 627. Propulsor count = `units` of the analysis set, designs with a count above zero, as in `frames.representativeness`. Mann-Whitney U, two-sided (`scipy.stats.mannwhitneyu`; U of the flown designs). Holm: one correction over the six funnel tests above plus this one (seven raw p); the six Holm p above do not change with the seventh test. CSV: `numbers_I_flown_propulsors_mw.csv`.

| group                         |   designs |   with a propulsor count |   median propulsors |
|:------------------------------|----------:|-------------------------:|--------------------:|
| flown designs (TRL 5 or more) |        68 |                       68 |                   8 |
| the other designs             |       553 |                      521 |                   5 |

- median difference: +3 propulsors (flown minus the rest)
- U = 24814
- p = 5.7e-08 (raw 5.747e-08)
- p Holm (funnel family, seven tests) = 4.0e-07 (raw 4.023e-07)

## 4. Checks requested on 2026-10-12 (no figure or text changed by them)

### Flown designs (TRL 5 or more)

- **Definition in the code** (`viz/thesis_q4.py:representativeness`): flown = `trl >= 5`, where `trl` is `frames.trl_frame(ds)`: the NASA TRL of each design from `0_labelling/inputs/trl/aircraft_trl.csv`, overridden, design by design, by the TRL of the rule-based scripts (the author's own reading where he reviewed the design) when `analysis.external_inputs` is `script` (`viz/script_inputs.py`, `review/script_outputs/TRL.csv`). A design without a TRL is TRL 2. TRL 3-4 (ground and wind-tunnel tests) is not flown; no design of the 627 sits at TRL 3 or 4 under the script inputs.
- **Sizes:** the earlier group (TRL above 2 on the earlier inputs) has 63 designs, of which 1 sit at TRL 3 or 4 and 62 at TRL 5 or more. The new group (TRL 5 or more on the script inputs) has 68 designs, none at TRL 3 or 4.
- **Why 68 against 63:** the TRL values differ between the two input sets, and the definition moves the TRL 3-4 design out. 10 designs are in the new group and were not in the old one, 5 were in the old one and are not in the new (63 + 10 - 5 = 68). A design moves from the old group to the rest when the script finds no flight sentence on its linked directory pages where the earlier reading had found one (and the reverse). They are listed below and in `csv/numbers_I_flown_group_difference.csv`.

| aircraft_id | company | architecture | TRL, earlier inputs | TRL, script inputs | in the old group (TRL above 2, earlier inputs) | in the new group (TRL 5 or more, script inputs) |
|---|---|---|---|---|---|---|
| US2018208305A1_ad1 | Bell / Textron | TR | 2 | 6 | False | True |
| US2020239134A1_ad1 | Bell / Textron | CVT | 2 | 6 | False | True |
| US2020391879A1_ad1 | Bell / Textron | TR | 2 | 6 | False | True |
| US2023118750A1_ad1 | Bell / Textron | TR | 2 | 6 | False | True |
| US2014158816A1_ad1 | DeLorean Aerospace | TR | 3 | 2 | True | False |
| US2020354048A1_ad1 | Embraer / Eve | SLC | 6 | 2 | True | False |
| US2021354816A1_ad1 | Embraer / Eve | TR | 2 | 6 | False | True |
| KR20230089903A_ad1 | KARI | CVT | 7 | 2 | True | False |
| US2025304249A1_ad1 | Leonardo | CVT | 2 | 6 | False | True |
| US2019135413A1_ad1 | Uber Elevate | CVT | 2 | 6 | False | True |
| GB201801766D0_ad1 | Samad Aerospace | SLC | 5 | 2 | True | False |
| US2011042510A1_ad1 | None | TW | 2 | 6 | False | True |
| CN117985223A_ad1 | Changsha Huayu Xianxiang Aviation Technology | TR | 6 | 2 | True | False |
| US2024051687A1_ad1 | Katla Aero | SLC | 2 | 6 | False | True |
| WO2025109312A1_ad1 | Sora Aviation | TR | 2 | 6 | False | True |

### Flown index-firm group

- **Definition:** the designs of the index firms of the current AAM Reality Index release whose first flight, as the index prints it, is a year before 2026 (the index prints years only; a 2026 year is read as a plan, as in the clock figure). The other index firms, and the 22 - 14 firms with no row in the current release, go to the rest. The group has 42 designs of 12 firms.

Architecture groups behind "LC +21.5 pp, p 0.047" (flown index-firm designs against the rest, the five directory categories):

| directory category | flown index-firm designs | % of the flown index-firm designs | the rest | % of the rest | gap pp |
|---|---|---|---|---|---|
| VT | 17 | 40.5 | 349 | 60.3 | -19.8 |
| LC | 20 | 47.6 | 148 | 25.6 | 22.1 |
| WM | 3 | 7.1 | 44 | 7.6 | -0.5 |
| HB | 2 | 4.8 | 27 | 4.7 | 0.1 |
| ER | 0 | 0.0 | 9 | 1.6 | -1.6 |

chi-square on this 2 x 5 table: p 0.036. The two designs without an architecture group are in the rest of the other attributes but not in this table (the five rows add to 42 and 577, not 42 and 579).

Index firms and whether their first flight counts as flown:

| company | designs | first flight in the index (earliest year) | counts as flown before the snapshot | reason if not |
|---|---|---|---|---|
| Joby Aviation | 8 | 2018 | True |  |
| Guangzhou Ehang Intelligent Technology | 1 | 2018 | True |  |
| Embraer / Eve | 4 | 2025 | True |  |
| Honda | 9 | 2024 | True |  |
| AutoFlight | 2 | 2022 | True |  |
| Volocopter | 4 | 2021 | True |  |
| Wisk Aero | 4 | 2025 | True |  |
| Archer Aviation | 4 | 2023 | True |  |
| Beta Technologies | 1 | 2020 | True |  |
| Wollant Aviation | 2 | 2023 | True |  |
| Supernal | 4 |  | False | no first flight in the index |
| Ascendance Flight Technologies | 1 | 2027 | False | a planned first flight (after the index release of 2026) |
| Vertical Aerospace | 1 | 2023 | True |  |
| Wofei / Geely Aviation | 2 | 2023 | True |  |

### I.1 turning points and the lead from the first patent to the first flight

| series | turning point | 95 % range of the resampled year | share of the fits choosing it | jump factor |
|---|---|---|---|---|
| representative patents | 2016 | 2015 to 2018 | 91 % | x3.45 |
| unique aircraft | 2017 | 2010 to 2020 | 23 % | x1.83 |
| aircraft per 1 000 B64 | 2013 | 2009 to 2020 | 18 % | x0.49 |

(`unique aircraft` = the designs series; `representative patents` = the patent-families series.)

| company | first patent | first flight | years from the first patent to the first flight |
|---|---|---|---|
| Joby Aviation | 2013 | 2018 | 5 |
| Guangzhou Ehang Intelligent Technology | 2015 | 2018 | 3 |
| Embraer / Eve | 2018 | 2025 | 7 |
| Honda | 2018 | 2024 | 6 |
| AutoFlight | 2019 | 2022 | 3 |
| Volocopter | 2019 | 2021 | 2 |
| Wisk Aero | 2020 | 2025 | 5 |
| Archer Aviation | 2020 | 2023 | 3 |
| Beta Technologies | 2021 | 2020 | -1 |
| Wollant Aviation | 2022 | 2023 | 1 |
| Vertical Aerospace | 2024 | 2023 | -1 |
| Wofei / Geely Aviation | 2024 | 2023 | -1 |

- firms with a first flight on record (year 2026 or before): n = 12; with the first patent before the flight: n = 9; median lead among those 3 years (range 1 to 7); median over all 12: 3.0 years.
- 90th-percentile publication lag: 3 years (the largest of the three regions, `frames.publication_lag`). Median lead minus that lag: 0 years (`q5.numbers()['ff_visible']`), the "about 1 year" figure, on the same n = 9 firms. The lag is subtracted as one number, from the median, not firm by firm.

- Publication lag, 90th percentile in years (`frames.publication_lag`, 540 representative primary patents, snapshot 2026-06-08). It takes ALL priority years (1999-2026), with no filter for years complete at the snapshot; `frames.filings_per_year` feeds the same all-years lag to `lag_quantile`. (b) is the same on priority years 2016-2021 only. Both give 3 years in every region, so the choice of years does not change the figure.

| key | all priority years | 2016-2021 only |
|---|---|---|
| `pub_lag_na_allyears` / `pub_lag_na_1621` (North America) | 3.0 | 3.0 |
| `pub_lag_eu_allyears` / `pub_lag_eu_1621` (Europe) | 3.0 | 3.0 |
| `pub_lag_ap_allyears` / `pub_lag_ap_1621` (Asia-Pacific) | 3.0 | 3.0 |
| `pub_lag_all_allyears` / `pub_lag_all_1621` (overall, all regions) | 3.0 | 3.0 |

- Share of the aircraft already published at the snapshot (`lib.growth.visible_share`, lags of the designs of priority years 2016-21 per region, as `frames.region_years`; overall = all 354 designs, other regions included, as the lag-corrected total below):

| key | 2022 | 2023 |
|---|---|---|
| `visible_{2022,2023}_na` (North America, n ref = 155) | 98.2 % | 91.7 % |
| `visible_{2022,2023}_eu` (Europe, n ref = 99) | 98.3 % | 87.3 % |
| `visible_{2022,2023}_ap` (Asia-Pacific, n ref = 91) | 99.4 % | 89.0 % |
| `visible_{2022,2023}_all` (overall, n ref = 354) | 98.2 % | 88.9 % |

## 5. What each figure plots

| figure | what is plotted |
|---|---|
| q1_filings_per_year | 627 designs over the priority years 2005 (pooled with the earlier ones) to 2026; 625 have an architecture, 2 do not (grey segment); 876 patent families; cohort 2024-26 faded |
| q1_growth_rates | eVTOL architecture patent families, aeronautics, transport and operations, all patents; 2005-2023 fitted, 2024-26 shown and never fitted |
| q4_patent_vs_market_clock | 14 index firms with a first patent here; first flight 13 firms, entry into service 10 firms |
| q1_in_force_status | 598 designs of the nine architectures, by office; 23 not plotted (see section 2) |
| q4_class_mix | patent dataset: <= 2011 59, 2012-15 57, 2016-19 211, 2020-23 237, 2024-26 (partial) 55; directory: <= 2011 45, 2012-15 90, 2016-19 307, 2020-23 271, 2024-26 (partial) 69 |
| q5_funding_vs_aircraft | 10 firms with a disclosed amount; Spearman rho +0.58, p 0.08 (not printed in the figure) |

## 6. Every number the Results text of Analysis I quotes

Placeholders of `viz/thesis_text_q1.py`, `thesis_text_q4.py` and `thesis_text_q5.py` (results, answer and appendix lines) with the value they take now. A value that differs from the old Results text is marked (was X); section 7 lists them one line each.

### Q1 growth and active protection

| key | value now | where used | sentence | source |
|---|---|---|---|---|
| `ac_2015` | 21 | results A (Growth of the field) | In 2015 the dataset gains {ac_2015} unique aircraft. | viz/thesis_q1.py:numbers() |
| `ac_2018` | 68 | results A (Growth of the field) | In 2018 it gains {ac_2018}, and the count holds near that level to the last complete year. | viz/thesis_q1.py:numbers() |
| `ap_2526` | 18 | results B (Entry by region) | Lag explains only the two latest years, whose {ap_2526} aircraft are all Asia-Pacific's. | viz/thesis_q1.py:numbers() |
| `ap_delay_cvt` | −1 | results B (Entry by region) | On Combined Vectored Thrust (CVT) no delay is detected, {ap_delay_cvt} years with an interval of {ap_delay_cvt_ci} that takes in zero, because North A… | viz/thesis_q1.py:numbers() |
| `ap_delay_cvt_ci` | −3 to +1 | results B (Entry by region) | On Combined Vectored Thrust (CVT) no delay is detected, {ap_delay_cvt} years with an interval of {ap_delay_cvt_ci} that takes in zero, because North A… | viz/thesis_q1.py:numbers() |
| `ap_delay_range` | 2 to 4 | results B (Entry by region) | Asia-Pacific files Lift + Cruise, Tilt Propulsor and Tilt Wing {ap_delay_range} years after North America. | viz/thesis_q1.py:numbers() |
| `dbl_ac` | 3.5 (was 3.7) | appendix q1_growth_rates_table | Against all patenting they grow {gr_fam_all} times as fast, and the unique aircraft double every {dbl_ac} years. | viz/thesis_q1.py:numbers() |
| `dbl_all` | 10.7 | results A (Growth of the field) | Transport doubles every {dbl_secb} years and all patenting every {dbl_all} (). | viz/thesis_q1.py:numbers() |
| `dbl_b64` | 4.7 | results A (Growth of the field) | eVTOL is the fastest-growing series (), its architecture patents doubling every {dbl_fam} years against {dbl_b64} for aeronautics. | viz/thesis_q1.py:numbers() |
| `dbl_fam` | 3.5 (was 3.6) | results A (Growth of the field) | eVTOL is the fastest-growing series (), its architecture patents doubling every {dbl_fam} years against {dbl_b64} for aeronautics. | viz/thesis_q1.py:numbers() |
| `dbl_secb` | 6.4 | results A (Growth of the field) | Transport doubles every {dbl_secb} years and all patenting every {dbl_all} (). | viz/thesis_q1.py:numbers() |
| `fa_c_2023` | 19 % | results B (Entry by region) | It is {fa_c_2023} in the youngest complete cohort. | viz/thesis_q1.py:numbers() |
| `fa_c_le2011` | 69 % | results B (Entry by region) | It is {fa_c_le2011} in the oldest. | viz/thesis_q1.py:numbers() |
| `fa_cvt` | 29 % (was 53 %) | results B (Entry by region) | By architecture it runs from {fa_mr} for Multicopter to {fa_cvt} for CVT. | viz/thesis_q1.py:numbers() |
| `fa_mr` | 34 % (was 31 %) | results B (Entry by region) | By architecture it runs from {fa_mr} for Multicopter to {fa_cvt} for CVT. | viz/thesis_q1.py:numbers() |
| `fa_n` | 619 (was 332) | results B (Entry by region) | Of the {fa_n} designs, {fa_share} are not actively protected at the snapshot (). | viz/thesis_q1.py:numbers() |
| `fa_p` | 0.135 (was 0.043) | results B (Entry by region) | The architectures differ with p {fa_p}. | viz/thesis_q1.py:numbers() |
| `fa_share` | 30 % (was 43 %) | results B (Entry by region) | Of the {fa_n} designs, {fa_share} are not actively protected at the snapshot (). | viz/thesis_q1.py:numbers() |
| `fo_else` | 41 % (was 69 %) | results B (Entry by region) | At the other offices it is {fo_else}, over {fo_n_else} designs. | viz/thesis_q1.py:numbers() |
| `fo_n_else` | 256 | results B (Entry by region) | At the other offices it is {fo_else}, over {fo_n_else} designs. | viz/thesis_q1.py:numbers() |
| `fo_n_us` | 363 (was 209) | results B (Entry by region) | At the US office the share is {fo_us}, over {fo_n_us} designs. | viz/thesis_q1.py:numbers() |
| `fo_p` | < 0.001 | results B (Entry by region) | The two differ with p {fo_p}. | viz/thesis_q1.py:numbers() |
| `fo_us` | 23 % (was 31 %) | results B (Entry by region) | At the US office the share is {fo_us}, over {fo_n_us} designs. | viz/thesis_q1.py:numbers() |
| `gr_fam_all` | 3.05 (was 3.00) | appendix q1_growth_rates_table | Against all patenting they grow {gr_fam_all} times as fast, and the unique aircraft double every {dbl_ac} years. | viz/thesis_q1.py:numbers() |
| `gr_fam_b64` | 1.34 (was 1.32) | results A (Growth of the field) | Counted in families, eVTOL grows {gr_fam_b64} times as fast as aeronautics ({gr_fam_b64_ci}). | viz/thesis_q1.py:numbers() |
| `gr_fam_b64_19` | 1.28 (was 1.26) | results A (Growth of the field) | The lead rests partly on the latest years, and with the fit ended at 2019 the ratio falls to {gr_fam_b64_19}. | viz/thesis_q1.py:numbers() |
| `gr_fam_b64_19_ci` | 1.10 to 1.42 (was 1.07 to 1.41) | results A (Growth of the field) | Its interval, {gr_fam_b64_19_ci}, still leaves eVTOL the faster series. | viz/thesis_q1.py:numbers() |
| `gr_fam_b64_ci` | 1.23 to 1.47 (was 1.20 to 1.46) | results A (Growth of the field) | Counted in families, eVTOL grows {gr_fam_b64} times as fast as aeronautics ({gr_fam_b64_ci}). | viz/thesis_q1.py:numbers() |
| `na_2021` | 32 | results B (Entry by region) | North America's count falls from {na_2021} to {na_2023} aircraft over the same two years. | viz/thesis_q1.py:numbers() |
| `na_2023` | 10 | results B (Entry by region) | North America's count falls from {na_2021} to {na_2023} aircraft over the same two years. | viz/thesis_q1.py:numbers() |
| `na_share_2021` | 44 % | results B (Entry by region) | Its share falls from {na_share_2021} to {na_share_2023} over those two years (). | viz/thesis_q1.py:numbers() |
| `na_share_2023` | 22 % | results B (Entry by region) | Its share falls from {na_share_2021} to {na_share_2023} over those two years (). | viz/thesis_q1.py:numbers() |
| `na_share_2023_corr` | 22 % | results B (Entry by region) | Corrected for lag, the share of 2023 stays at {na_share_2023_corr}. | viz/thesis_q1.py:numbers() |
| `turn_ac_hi` | 2020 | results A (Growth of the field) | The resamples place that year anywhere from {turn_ac_lo} to {turn_ac_hi}. | viz/thesis_q1.py:numbers() |
| `turn_ac_lo` | 2010 | results A (Growth of the field) | The resamples place that year anywhere from {turn_ac_lo} to {turn_ac_hi}. | viz/thesis_q1.py:numbers() |
| `turn_ac_year` | 2017 | results A (Growth of the field) | The unique aircraft turn in {turn_ac_year}. | viz/thesis_q1.py:numbers() |
| `turn_pat_boot` | 91 % (was 90 %) | results A (Growth of the field) | Filing takes off in {turn_pat_year}, the year chosen by {turn_pat_boot} of the resampled fits (). | viz/thesis_q1.py:numbers() |
| `turn_pat_year` | 2016 | results A (Growth of the field) | Filing takes off in {turn_pat_year}, the year chosen by {turn_pat_boot} of the resampled fits (). | viz/thesis_q1.py:numbers() |
| `vis_2023_hi` | 92 % | results B (Entry by region) | The snapshot already sees {vis_2023_lo} to {vis_2023_hi} of every region's aircraft of that year. | viz/thesis_q1.py:numbers() |
| `vis_2023_lo` | 87 % | results B (Entry by region) | The snapshot already sees {vis_2023_lo} to {vis_2023_hi} of every region's aircraft of that year. | viz/thesis_q1.py:numbers() |

### Q4 representativeness and the market clock

| key | value now | where used | sentence | source |
|---|---|---|---|---|
| `ari_n` | 152 (was 147) | answer | The aircraft public sources cover, the {trl_n} that got built and the {ari_n} of the index firms, are company-backed and carry more propulsor units, s… | viz/thesis_q4.py:numbers() |
| `closest_p` | 0.527 (was 0.208) | results B (Is the mix representative) | Only the directory pages linked to a patent of this dataset match the dataset's mix (p {closest_p}, ). | viz/thesis_q4.py:numbers() |
| `eis_lead` | 7 | results B (Is the mix representative) | The lead is a median of {ff_lead} years, and planned entry into service sits a median of {eis_lead} years after the first patent. | viz/thesis_q4.py:numbers() |
| `fari_class_p` | 0.036 | results B (Is the mix representative) | By architecture group the flown designs give p {flown_class_p}, the flown index-firm designs p {fari_class_p}. | viz/thesis_q4.py:numbers() |
| `fari_differs` | 5 | results B (Is the mix representative) | The {fari_n} designs of the index firms that have flown differ on {fari_differs} of the six (). | viz/thesis_q4.py:numbers() |
| `fari_n` | 42 | results B (Is the mix representative) | The {fari_n} designs of the index firms that have flown differ on {fari_differs} of the six (). | viz/thesis_q4.py:numbers() |
| `ff_before` | 9 (was 8) | results B (Is the mix representative) | {ff_before} of the {ff_flown} firms with a first flight on record filed their first patent in this corpus before flying. | viz/thesis_q4.py:numbers() |
| `ff_flown` | 12 (was 11) | results B (Is the mix representative) | {ff_before} of the {ff_flown} firms with a first flight on record filed their first patent in this corpus before flying. | viz/thesis_q4.py:numbers() |
| `ff_lead` | 3 (was 4) | results B (Is the mix representative) | The lead is a median of {ff_lead} years, and planned entry into service sits a median of {eis_lead} years after the first patent. | viz/thesis_q4.py:numbers() |
| `flown_class_p` | 0.16 | results B (Is the mix representative) | By architecture group the flown designs give p {flown_class_p}, the flown index-firm designs p {fari_class_p}. | viz/thesis_q4.py:numbers() |
| `flown_differs` | 3 | results B (Is the mix representative) | They differ from the rest on {flown_differs} of the six attributes (). | viz/thesis_q4.py:numbers() |
| `flown_n` | 68 | results B (Is the mix representative) | Of the {unique} designs, {flown_n} have flown. | viz/thesis_q4.py:numbers() |
| `lc_dir_first` | 4 % (was 13 %) | results B (Is the mix representative) | In the directory it goes from {lc_dir_first} to {lc_dir_last}. | viz/thesis_q4.py:numbers() |
| `lc_dir_last` | 20 % | results B (Is the mix representative) | In the directory it goes from {lc_dir_first} to {lc_dir_last}. | viz/thesis_q4.py:numbers() |
| `lc_ds_first` | 22 % (was 27 %) | results B (Is the mix representative) | Lift + Cruise rises in both, from {lc_ds_first} to {lc_ds_last} of the dataset's aircraft. | viz/thesis_q4.py:numbers() |
| `lc_ds_last` | 33 % | results B (Is the mix representative) | Lift + Cruise rises in both, from {lc_ds_first} to {lc_ds_last} of the dataset's aircraft. | viz/thesis_q4.py:numbers() |
| `mix_p` | < 0.001 | appendix q4_dataset_vs_directory_classes | All years together the two mixes differ (chi-square p {mix_p}), and Wingless carries the gap with an adjusted residual of {resid_low}. | viz/thesis_q4.py:numbers() |
| `nc_gen` | 524 (was 530) | appendix q4_name_coverage | {nc_named} aircraft carry a real product name and {nc_gen} a generated identifier; none of the generated ones could be matched to a public aircraft. | viz/thesis_q4.py:numbers() |
| `nc_named` | 97 | results A (Is the coding right) | Only a named aircraft can be checked at all, {nc_named} of {unique}, so these shares speak for the company-backed part of the dataset. | viz/thesis_q4.py:numbers() |
| `pw_ci` | 0.83–0.94 | results A (Is the coding right) | That share, {pw_share}, has an interval of {pw_ci}. | viz/thesis_q4.py:numbers() |
| `pw_img_pub` | 87 | results A (Is the coding right) | The drawing label gives the built aircraft's architecture class for {pw_img_pub} of the {pw_n} matched aircraft (). | viz/thesis_q4.py:numbers() |
| `pw_img_txt` | 94 (was 93) | results A (Is the coding right) | The patent text agrees with the public aircraft on {pw_txt_pub} of them, and the drawing agrees with the text on {pw_img_txt}. | viz/thesis_q4.py:numbers() |
| `pw_n` | 97 | results A (Is the coding right) | The drawing label gives the built aircraft's architecture class for {pw_img_pub} of the {pw_n} matched aircraft (). | viz/thesis_q4.py:numbers() |
| `pw_share` | 90 % | results A (Is the coding right) | That share, {pw_share}, has an interval of {pw_ci}. | viz/thesis_q4.py:numbers() |
| `pw_txt_pub` | 88 (was 89) | results A (Is the coding right) | The patent text agrees with the public aircraft on {pw_txt_pub} of them, and the drawing agrees with the text on {pw_img_txt}. | viz/thesis_q4.py:numbers() |
| `resid_low` | −10.7 (was −10.8) | results B (Is the mix representative) | All years together Wingless carries the gap between the two mixes (adjusted residual {resid_low}, ). | viz/thesis_q4.py:numbers() |
| `trl_n` | 68 (was 63) | answer | The aircraft public sources cover, the {trl_n} that got built and the {ari_n} of the index firms, are company-backed and carry more propulsor units, s… | viz/thesis_q4.py:numbers() |
| `trl_share` | 11 % (was 10 %) | appendix q4_trl_by_class | Only {trl_share} of the aircraft, {trl_n}, got past the paper stage of NASA TRL, and they come from the classes patented most, Lift + Cruise and Tilt … | viz/thesis_q4.py:numbers() |
| `unique` | 621 (was 627) | results A (Is the coding right) | Only a named aircraft can be checked at all, {nc_named} of {unique}, so these shares speak for the company-backed part of the dataset. | viz/thesis_q4.py:numbers() |
| `wm_domain` | 30 % | results B (Is the mix representative) | Restricting the directory to electric crewed pages leaves Wingless at {wm_domain}, so the domain gate does not explain the gap. | viz/thesis_q4.py:numbers() |

### Q5 funding and investment

| key | value now | where used | sentence | source |
|---|---|---|---|---|
| `ari_timeline_n` | 14 (was 13) | results A (Timing) | Of the {ari_timeline_n} index firms that file here, {ff_record_n} have a first flight on record up to the release year. | viz/thesis_q5.py:numbers() |
| `best_air` | 8 | results B (Funding vs filing and output) | {best_firm}, the best funded, holds {best_air} aircraft. | viz/thesis_q5.py:numbers() |
| `best_firm` | Joby Aviation | results B (Funding vs filing and output) | {best_firm}, the best funded, holds {best_air} aircraft. | viz/thesis_q5.py:numbers() |
| `eis_lead` | 7 | results A (Timing) | Planned entry into service sits a median of {eis_lead} years after the first patent on the {eis_n} firms that state one, firm by firm in . | viz/thesis_q5.py:numbers() |
| `eis_n` | 10 (was 9) | results A (Timing) | Planned entry into service sits a median of {eis_lead} years after the first patent on the {eis_n} firms that state one, firm by firm in . | viz/thesis_q5.py:numbers() |
| `ff_before_n` | 9 (was 8) | results A (Timing) | Of those, {ff_before_n} filed their first patent in this corpus before flying, a median of {ff_lead} years earlier. | viz/thesis_q5.py:numbers() |
| `ff_lead` | 3 (was 4) | results A (Timing) | Of those, {ff_before_n} filed their first patent in this corpus before flying, a median of {ff_lead} years earlier. | viz/thesis_q5.py:numbers() |
| `ff_record_n` | 12 (was 11) | results A (Timing) | Of the {ari_timeline_n} index firms that file here, {ff_record_n} have a first flight on record up to the release year. | viz/thesis_q5.py:numbers() |
| `ff_visible` | 0 (was 1) | results A (Timing) | Once that lag is paid, about {ff_visible} year of the median lead is left. | viz/thesis_q5.py:numbers() |
| `lag_p90` | 3 | results A (Timing) | The lead a reader of published patents can use is shorter, because a patent is published up to {lag_p90} years after its priority date and a priority … | viz/thesis_q5.py:numbers() |
| `p_air` | 0.08 (was 0.11) | results B (Funding vs filing and output) | sets the disclosed funding of the firms with an amount against their unique aircraft in the corpus, ρ {rho_air} with p {p_air}, no relation detected. | viz/thesis_q5.py:numbers() |
| `p_fp` | 0.13 (was 0.031) | results B (Funding vs filing and output) | Money does go with filing early, ρ {rho_fp} against the priority year of the first patent with p {p_fp}, and the best-funded firm filed first. | viz/thesis_q5.py:numbers() |
| `p_lead` | 0.29 (was 0.23) | results B (Funding vs filing and output) | The lead from first patent to first flight does not shorten with money either, ρ {rho_lead} with p {p_lead} on the firms whose first flight has happen… | viz/thesis_q5.py:numbers() |
| `rho_air` | +0.58 (was +0.56) | results B (Funding vs filing and output) | sets the disclosed funding of the firms with an amount against their unique aircraft in the corpus, ρ {rho_air} with p {p_air}, no relation detected. | viz/thesis_q5.py:numbers() |
| `rho_fp` | −0.51 (was −0.71) | results B (Funding vs filing and output) | Money does go with filing early, ρ {rho_fp} against the priority year of the first patent with p {p_fp}, and the best-funded firm filed first. | viz/thesis_q5.py:numbers() |
| `rho_lead` | +0.40 (was +0.48) | results B (Funding vs filing and output) | The lead from first patent to first flight does not shorten with money either, ρ {rho_lead} with p {p_lead} on the firms whose first flight has happen… | viz/thesis_q5.py:numbers() |
| `top1` | Joby Aviation | results C (Concentration of funding) | The money is concentrated in {top1} and {top2}, where the patents are not. | viz/thesis_q5.py:numbers() |
| `top2` | Beta Technologies | results C (Concentration of funding) | The money is concentrated in {top1} and {top2}, where the patents are not. | viz/thesis_q5.py:numbers() |
| `top2_airshare` | 1.4 % | results C (Concentration of funding) | These two firms hold {top2_fundshare} of the funding the index firms disclose and {top2_airshare} of the aircraft of this labelled dataset. | viz/thesis_q5.py:numbers() |
| `top2_fundshare` | 56 % (was 57 %) | results C (Concentration of funding) | These two firms hold {top2_fundshare} of the funding the index firms disclose and {top2_airshare} of the aircraft of this labelled dataset. | viz/thesis_q5.py:numbers() |

`thesis_figures/Q1_growth/numbers.json`, `Q4_representativeness/numbers.json` and `Q5_money/numbers.json` were rewritten on 2026-10-13 from the current inputs (the corrected company map with EHang, the script TRL, the script years); the previous Q4 and Q5 files are kept beside them as `numbers.PRE_20261013.json`, and the values of the old Results text are in `review/numbers_old/`.

## 7. What changed since the old Results text (old -> new)

Old = the values the old Results text printed (the `numbers.json` files before the changes of 2026-10-12: the all-years protection method, the flown definition, the script inputs and the corrected company map with EHang). New = the values now. A key that the new text no longer quotes reads "(no longer quoted)".

### The statistics you listed, one line each

- **Index firms that file here** (rows of the clock figure, the firms of the current index release with a first patent in the dataset): 13 -> 14 (Q5 `ari_timeline_n`)
- **Index companies that file in the dataset** (whole company map): 18 -> 22 (Q4 `ari_firms_n`); their designs 147 -> 152 (Q4 `ari_n`)
- **Firms with a first flight on record** (year 2026 or before): 11 -> 12 (Q5 `ff_record_n`; Q4 `ff_flown` 11 -> 12)
- **Firms that filed their first patent before flying**: 8 -> 9 (Q5 `ff_before_n`; Q4 `ff_before` 8 -> 9); firms with a first flight at or before the first patent: 3 -> 3 (`ff_after_n`)
- **Median lead from the first patent to the first flight**, years: 4 -> 3 (Q5 `ff_lead`; Q4 4 -> 3), on the 9 firms with the patent before the flight (was 8); range 1 to 7 -> 1 to 7
- **The lead left after the 90th-percentile publication lag** (3 years, unchanged): 1 -> 0 years (Q5 `ff_visible`)
- **Median years from the first patent to the planned entry into service**: 7 -> 7 (Q5 `eis_lead`), on 9 -> 10 firms that state one (`eis_n`)
- **Firms behind each statistic (now)**: first flights 12; the lead median 9; planned entry into service 10; clock rows 14; funding tests 10 firms with a disclosed amount, 10 for the first-patent year, 9 for the lead (before 9, 9, 8)
- **Size of the flown group**: 63 (designs above TRL 2, earlier inputs) -> 68 (designs at TRL 5 or more, script inputs); the rest 564 -> 553 (Q4 `trl_n` -> `flown_n`); 10 designs entered and 5 left (section 4)
- **Turning point, patent families**: 2016 -> 2016 (unchanged), chosen by 90 % -> 91 % of the resampled fits, 95 % range of the resampled year 2015 to 2018 (not quoted before)
- **Turning point, designs**: 2017 -> 2017 (unchanged), chosen by 23 % of the resampled fits (not quoted before), 95 % range 2010 to 2020 -> 2010 to 2020 (unchanged)

None of the turning-point numbers depends on the company map, the TRL or the years of the directory: they come from the patent counts per priority year.

### Every number the old Results text quoted that changed

- Q1 `dbl_ac`: 3.7 -> 3.5   (Against all patenting they grow {gr_fam_all} times as fast, and the unique aircraft double every {dbl_ac} year…)
- Q1 `dbl_fam`: 3.6 -> 3.5   (eVTOL is the fastest-growing series (), its architecture patents doubling every {dbl_fam} years against {dbl_b…)
- Q1 `fa_cvt`: 53 % -> 29 %   (The classes appear to differ, CVT and Lift + Cruise at {fa_cvt} against Multirotor at {fa_mr}, but the differe…)
- Q1 `fa_mr`: 31 % -> 34 %   (The classes appear to differ, CVT and Lift + Cruise at {fa_cvt} against Multirotor at {fa_mr}, but the differe…)
- Q1 `fa_mr_first`: 41 % -> (no longer quoted)   (Counting a patent that names several aircraft for its first aircraft only, Multirotor rises to {fa_mr_first} a…)
- Q1 `fa_p`: 0.043 -> 0.135   (The class difference (p {fa_p}) does not survive the filing office.)
- Q1 `fa_p_first`: 0.079 -> (no longer quoted)   (Counting a patent that names several aircraft for its first aircraft only, Multirotor rises to {fa_mr_first} a…)
- Q1 `fa_share`: 43 % -> 30 %   (Of the aircraft with a priority year of 2019 or earlier, {fa_share} have no patent left in force ().)
- Q1 `fo_else`: 69 % -> 41 %   (Aircraft filed at the US office are out of force {fo_us} of the time, against {fo_else} elsewhere.)
- Q1 `fo_n_us`: 209 -> 363   (Within the US office no class difference is detected (p {fo_p_us}, {fo_n_us} aircraft).)
- Q1 `fo_p_us`: 0.43 -> (no longer quoted)   (Within the US office no class difference is detected (p {fo_p_us}, {fo_n_us} aircraft).)
- Q1 `fo_us`: 31 % -> 23 %   (Aircraft filed at the US office are out of force {fo_us} of the time, against {fo_else} elsewhere.)
- Q1 `gr_fam_all`: 3.00 -> 3.05   (Against all patenting they grow {gr_fam_all} times as fast, and the unique aircraft double every {dbl_ac} year…)
- Q1 `gr_fam_b64`: 1.32 -> 1.34   (Counted in families, eVTOL grows {gr_fam_b64} times as fast as aeronautics ({gr_fam_b64_ci}).)
- Q1 `gr_fam_b64_19`: 1.26 -> 1.28   (The lead rests partly on the latest years, and with the fit ended at 2019 the ratio falls to {gr_fam_b64_19}.)
- Q1 `gr_fam_b64_19_ci`: 1.07 to 1.41 -> 1.10 to 1.42   (Its interval, {gr_fam_b64_19_ci}, still leaves eVTOL the faster series.)
- Q1 `gr_fam_b64_ci`: 1.20 to 1.46 -> 1.23 to 1.47   (Counted in families, eVTOL grows {gr_fam_b64} times as fast as aeronautics ({gr_fam_b64_ci}).)
- Q1 `turn_pat_boot`: 90 % -> 91 %   (Filing takes off in {turn_pat_year}, the year chosen by {turn_pat_boot} of the resampled fits ().)
- Q4 `ari_class_p`: 0.15 -> (no longer quoted)   (Neither group differs detectably in architecture class (p {trl_class_p} and {ari_class_p}).)
- Q4 `ari_n`: 147 -> 152   (The {ari_n} aircraft of the index firms differ on four of the six attributes (): region, priority window, file…)
- Q4 `closest_p`: 0.208 -> 0.527   (Only the directory pages linked to a patent of this dataset match the dataset's mix (p {closest_p}, ).)
- Q4 `ff_before`: 8 -> 9   ({ff_before} of the {ff_flown} firms with a first flight on record filed their first patent in this corpus befo…)
- Q4 `ff_flown`: 11 -> 12   ({ff_before} of the {ff_flown} firms with a first flight on record filed their first patent in this corpus befo…)
- Q4 `ff_lead`: 4 -> 3   (The lead is a median of {ff_lead} years, and planned entry into service sits a median of {eis_lead} years afte…)
- Q4 `lc_dir_first`: 13 % -> 4 %   (In the directory it goes from {lc_dir_first} to {lc_dir_last}.)
- Q4 `lc_ds_first`: 27 % -> 22 %   (Lift + Cruise rises in both, from {lc_ds_first} to {lc_ds_last} of the dataset's aircraft.)
- Q4 `nc_gen`: 530 -> 524   ({nc_named} aircraft carry a real product name and {nc_gen} a generated identifier; none of the generated ones …)
- Q4 `pw_img_txt`: 93 -> 94   (The patent text agrees with the public aircraft on {pw_txt_pub} of them, and the drawing agrees with the text …)
- Q4 `pw_txt_pub`: 89 -> 88   (The patent text agrees with the public aircraft on {pw_txt_pub} of them, and the drawing agrees with the text …)
- Q4 `resid_low`: −10.8 -> −10.7   (All years together Wingless carries the gap between the two mixes (adjusted residual {resid_low}, ).)
- Q4 `trl_class_p`: 0.11 -> (no longer quoted)   (Neither group differs detectably in architecture class (p {trl_class_p} and {ari_class_p}).)
- Q4 `trl_n`: 63 -> 68   (The aircraft that got built, {trl_n} of {unique}, differ from the rest on filer type and propulsor units and o…)
- Q4 `trl_share`: 10 % -> 11 %   (Only {trl_share} of the aircraft, {trl_n}, got past the paper stage of NASA TRL, and they come from the classe…)
- Q4 `unique`: 627 -> 621   (Only a named aircraft can be checked at all, {nc_named} of {unique}, so these shares speak for the company-bac…)
- Q5 `ari_timeline_n`: 13 -> 14   (Of the {ari_timeline_n} index firms that file here, {ff_record_n} have a first flight on record up to the rele…)
- Q5 `eis_n`: 9 -> 10   (Planned entry into service sits a median of {eis_lead} years after the first patent on the {eis_n} firms that …)
- Q5 `ff_before_n`: 8 -> 9   (Of those, {ff_before_n} filed their first patent in this corpus before flying, a median of {ff_lead} years ear…)
- Q5 `ff_lead`: 4 -> 3   (Of those, {ff_before_n} filed their first patent in this corpus before flying, a median of {ff_lead} years ear…)
- Q5 `ff_record_n`: 11 -> 12   (Of the {ari_timeline_n} index firms that file here, {ff_record_n} have a first flight on record up to the rele…)
- Q5 `ff_visible`: 1 -> 0   (Once that lag is paid, about {ff_visible} year of the median lead is left.)
- Q5 `p_air`: 0.11 -> 0.08   (sets the disclosed funding of the firms with an amount against their unique aircraft in the corpus, ρ {rho_air…)
- Q5 `p_fp`: 0.031 -> 0.13   (Money does go with filing early, ρ {rho_fp} against the priority year of the first patent with p {p_fp}, and t…)
- Q5 `p_lead`: 0.23 -> 0.29   (The lead from first patent to first flight does not shorten with money either, ρ {rho_lead} with p {p_lead} on…)
- Q5 `rho_air`: +0.56 -> +0.58   (sets the disclosed funding of the firms with an amount against their unique aircraft in the corpus, ρ {rho_air…)
- Q5 `rho_fp`: −0.71 -> −0.51   (Money does go with filing early, ρ {rho_fp} against the priority year of the first patent with p {p_fp}, and t…)
- Q5 `rho_lead`: +0.48 -> +0.40   (The lead from first patent to first flight does not shorten with money either, ρ {rho_lead} with p {p_lead} on…)
- Q5 `top2_fundshare`: 57 % -> 56 %   (These two firms hold {top2_fundshare} of the funding the index firms disclose and {top2_airshare} of the aircr…)

### Numbers that did NOT change (37)

| question | key | value (old = new) | used in the sentence |
|---|---|---|---|
| Q1 | `ac_2015` | 21 | In 2015 the dataset gains {ac_2015} unique aircraft. |
| Q1 | `ac_2018` | 68 | In 2018 it gains {ac_2018}, and the count holds near that level to the last complete year. |
| Q1 | `ap_2526` | 18 | Lag explains only the two latest years, whose {ap_2526} aircraft are all Asia-Pacific's. |
| Q1 | `ap_delay_cvt` | −1 | On Combined Vectored Thrust (CVT) no delay is detected, {ap_delay_cvt} years with an interval of {ap_delay_cvt… |
| Q1 | `ap_delay_cvt_ci` | −3 to +1 | On Combined Vectored Thrust (CVT) no delay is detected, {ap_delay_cvt} years with an interval of {ap_delay_cvt… |
| Q1 | `ap_delay_range` | 2 to 4 | Asia-Pacific files Lift + Cruise, Tilt Propulsor and Tilt Wing {ap_delay_range} years after North America. |
| Q1 | `dbl_all` | 10.7 | Transport doubles every {dbl_secb} years and all patenting every {dbl_all} (). |
| Q1 | `dbl_b64` | 4.7 | eVTOL is the fastest-growing series (), its architecture patents doubling every {dbl_fam} years against {dbl_b… |
| Q1 | `dbl_secb` | 6.4 | Transport doubles every {dbl_secb} years and all patenting every {dbl_all} (). |
| Q1 | `na_2021` | 32 | North America's count falls from {na_2021} to {na_2023} aircraft over the same two years. |
| Q1 | `na_2023` | 10 | North America's count falls from {na_2021} to {na_2023} aircraft over the same two years. |
| Q1 | `na_share_2021` | 44 % | Its share falls from {na_share_2021} to {na_share_2023} over those two years (). |
| Q1 | `na_share_2023` | 22 % | Its share falls from {na_share_2021} to {na_share_2023} over those two years (). |
| Q1 | `na_share_2023_corr` | 22 % | Corrected for lag, the share of 2023 stays at {na_share_2023_corr}. |
| Q1 | `turn_ac_hi` | 2020 | The resamples place that year anywhere from {turn_ac_lo} to {turn_ac_hi}. |
| Q1 | `turn_ac_lo` | 2010 | The resamples place that year anywhere from {turn_ac_lo} to {turn_ac_hi}. |
| Q1 | `turn_ac_year` | 2017 | The unique aircraft turn in {turn_ac_year}. |
| Q1 | `turn_pat_year` | 2016 | Filing takes off in {turn_pat_year}, the year chosen by {turn_pat_boot} of the resampled fits (). |
| Q1 | `vis_2023_hi` | 92 % | The snapshot already sees {vis_2023_lo} to {vis_2023_hi} of every region's aircraft of that year. |
| Q1 | `vis_2023_lo` | 87 % | The snapshot already sees {vis_2023_lo} to {vis_2023_hi} of every region's aircraft of that year. |
| Q4 | `eis_lead` | 7 | The lead is a median of {ff_lead} years, and planned entry into service sits a median of {eis_lead} years afte… |
| Q4 | `lc_dir_last` | 20 % | In the directory it goes from {lc_dir_first} to {lc_dir_last}. |
| Q4 | `lc_ds_last` | 33 % | Lift + Cruise rises in both, from {lc_ds_first} to {lc_ds_last} of the dataset's aircraft. |
| Q4 | `mix_p` | < 0.001 | All years together the two mixes differ (chi-square p {mix_p}), and Wingless carries the gap with an adjusted … |
| Q4 | `nc_named` | 97 | Only a named aircraft can be checked at all, {nc_named} of {unique}, so these shares speak for the company-bac… |
| Q4 | `pw_ci` | 0.83–0.94 | That share, {pw_share}, has an interval of {pw_ci}. |
| Q4 | `pw_img_pub` | 87 | The drawing label gives the built aircraft's architecture class for {pw_img_pub} of the {pw_n} matched aircraf… |
| Q4 | `pw_n` | 97 | The drawing label gives the built aircraft's architecture class for {pw_img_pub} of the {pw_n} matched aircraf… |
| Q4 | `pw_share` | 90 % | That share, {pw_share}, has an interval of {pw_ci}. |
| Q4 | `wm_domain` | 30 % | Restricting the directory to electric crewed pages leaves Wingless at {wm_domain}, so the domain gate does not… |
| Q5 | `best_air` | 8 | {best_firm}, the best funded, holds {best_air} aircraft. |
| Q5 | `best_firm` | Joby Aviation | {best_firm}, the best funded, holds {best_air} aircraft. |
| Q5 | `eis_lead` | 7 | Planned entry into service sits a median of {eis_lead} years after the first patent on the {eis_n} firms that … |
| Q5 | `lag_p90` | 3 | The lead a reader of published patents can use is shorter, because a patent is published up to {lag_p90} years… |
| Q5 | `top1` | Joby Aviation | The money is concentrated in {top1} and {top2}, where the patents are not. |
| Q5 | `top2` | Beta Technologies | The money is concentrated in {top1} and {top2}, where the patents are not. |
| Q5 | `top2_airshare` | 1.4 % | These two firms hold {top2_fundshare} of the funding the index firms disclose and {top2_airshare} of the aircr… |

## I.1 growth models (supervisor review 2, 2026-10)

Figure `q1_growth_rates` (and `q1_growth_rates_baselines`). ln count on priority year, least squares, each series alone: (a) two lines with a free level step at the break, (b) two lines meeting at the break, (c) logistic S-curve. The break is each series' own, searched over every year leaving 3 years or more on each side; the break and the error variance count as parameters (k = 6, 5, 4). Winner: lowest AIC and BIC; 'wins clearly' = lowest on both by 10 or more. Intervals: residual bootstrap, 1000 resamples per series and model, break searched again each time, seeds [42, series, model]. Main fit 2005-2022 (2023 still filling up); 2005-2023 as the check. Source: `lib/growth_models.py`, `viz/thesis_q1.py:growth_models`; `csv/numbers_I_growth_models.csv`, `csv/numbers_I_growth_breakpoints.csv`.

| series | years | model | parameters k | SSE (log scale) | AIC | BIC | AICc | ΔAIC | ΔBIC | wins clearly |
|---|---|---|---|---|---|---|---|---|---|---|
| eVTOL architecture patents | 2005–2022 | (a) two lines, free level step | 6 | 0.8209 | -43.58 | -38.24 | -35.94 | 0.0 | 0.0 | True |
| eVTOL architecture patents | 2005–2022 | (b) two lines meeting at the break (slope change only) | 5 | 1.964 | -29.88 | -25.43 | -24.88 | 13.7 | 12.81 | False |
| eVTOL architecture patents | 2005–2022 | (c) logistic S-curve | 4 | 2.4389 | -27.98 | -24.42 | -24.9 | 15.6 | 13.82 | False |
| aeronautics (CPC B64) | 2005–2022 | (a) two lines, free level step | 6 | 0.1838 | -70.52 | -65.17 | -62.88 | 0.0 | 0.0 | True |
| aeronautics (CPC B64) | 2005–2022 | (b) two lines meeting at the break (slope change only) | 5 | 0.6144 | -50.79 | -46.34 | -45.79 | 19.72 | 18.83 | False |
| aeronautics (CPC B64) | 2005–2022 | (c) logistic S-curve | 4 | 0.8881 | -46.16 | -42.6 | -43.09 | 24.35 | 22.57 | False |
| transport and operations (CPC section B) | 2005–2022 | (a) two lines, free level step | 6 | 0.2135 | -67.82 | -62.48 | -60.18 | 0.0 | 0.0 | True |
| transport and operations (CPC section B) | 2005–2022 | (b) two lines meeting at the break (slope change only) | 5 | 0.5084 | -54.2 | -49.75 | -49.2 | 13.62 | 12.73 | False |
| transport and operations (CPC section B) | 2005–2022 | (c) logistic S-curve | 4 | 0.7977 | -48.1 | -44.53 | -45.02 | 19.72 | 17.94 | False |
| all patents | 2005–2022 | (a) two lines, free level step | 6 | 0.0545 | -92.39 | -87.04 | -84.75 | 0.0 | 0.0 | False |
| all patents | 2005–2022 | (b) two lines meeting at the break (slope change only) | 5 | 0.0772 | -88.13 | -83.67 | -83.13 | 4.26 | 3.37 | False |
| all patents | 2005–2022 | (c) logistic S-curve | 4 | 0.1059 | -84.44 | -80.88 | -81.36 | 7.95 | 6.16 | False |
| eVTOL architecture patents | 2005–2023 | (a) two lines, free level step | 6 | 0.9034 | -45.88 | -40.21 | -38.88 | 0.0 | 0.0 | True |
| eVTOL architecture patents | 2005–2023 | (b) two lines meeting at the break (slope change only) | 5 | 2.2686 | -30.38 | -25.66 | -25.76 | 15.5 | 14.55 | False |
| eVTOL architecture patents | 2005–2023 | (c) logistic S-curve | 4 | 2.7914 | -28.44 | -24.66 | -25.58 | 17.43 | 15.55 | False |
| aeronautics (CPC B64) | 2005–2023 | (a) two lines, free level step | 6 | 0.1841 | -76.1 | -70.43 | -69.1 | 0.0 | 0.0 | True |
| aeronautics (CPC B64) | 2005–2023 | (b) two lines meeting at the break (slope change only) | 5 | 0.618 | -55.09 | -50.37 | -50.47 | 21.01 | 20.06 | False |
| aeronautics (CPC B64) | 2005–2023 | (c) logistic S-curve | 4 | 0.9642 | -48.64 | -44.86 | -45.78 | 27.46 | 25.57 | False |
| transport and operations (CPC section B) | 2005–2023 | (a) two lines, free level step | 6 | 0.2161 | -73.05 | -67.39 | -66.05 | 0.0 | 0.0 | True |
| transport and operations (CPC section B) | 2005–2023 | (b) two lines meeting at the break (slope change only) | 5 | 0.6554 | -53.97 | -49.25 | -49.36 | 19.08 | 18.14 | False |
| transport and operations (CPC section B) | 2005–2023 | (c) logistic S-curve | 4 | 0.8692 | -50.61 | -46.83 | -47.75 | 22.45 | 20.56 | False |
| all patents | 2005–2023 | (a) two lines, free level step | 6 | 0.0546 | -99.2 | -93.54 | -92.2 | 0.0 | 0.0 | False |
| all patents | 2005–2023 | (b) two lines meeting at the break (slope change only) | 5 | 0.0772 | -94.6 | -89.88 | -89.98 | 4.6 | 3.66 | False |
| all patents | 2005–2023 | (c) logistic S-curve | 4 | 0.1142 | -89.17 | -85.39 | -86.31 | 10.04 | 8.15 | False |

Breaks, slopes (per year, log scale) and the level step of model (a), with 95 % bootstrap intervals:

| series | years | model | break year | break low | break high | share of draws at the break | pre slope | pre slope low | pre slope high | pre doubling (years) | post slope | post slope low | post slope high | level step (factor) | step low | step high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eVTOL architecture patents | 2005–2022 | (a) two lines, free level step | 2016.0 | 2016.0 | 2017.0 | 0.97 | 0.136 | 0.092 | 0.183 | 5.1 | 0.061 | -0.025 | 0.139 | 3.3 | 2.12 | 4.89 |
| aeronautics (CPC B64) | 2005–2022 | (a) two lines, free level step | 2016.0 | 2016.0 | 2016.0 | 1.0 | 0.13 | 0.111 | 0.148 | 5.3 | 0.013 | -0.026 | 0.054 | 2.1 | 1.77 | 2.57 |
| transport and operations (CPC section B) | 2005–2022 | (a) two lines, free level step | 2016.0 | 2016.0 | 2016.0 | 1.0 | 0.069 | 0.049 | 0.088 | 10.1 | 0.025 | -0.012 | 0.066 | 2.05 | 1.67 | 2.48 |
| all patents | 2005–2022 | (a) two lines, free level step | 2016.0 | 2015.0 | 2019.0 | 0.852 | 0.062 | 0.051 | 0.074 | 11.1 | 0.027 | 0.001 | 0.053 | 1.2 | 1.06 | 1.33 |
| eVTOL architecture patents | 2005–2023 | (a) two lines, free level step | 2016.0 | 2016.0 | 2016.0 | 0.979 | 0.136 | 0.097 | 0.182 | 5.1 | 0.03 | -0.037 | 0.091 | 3.52 | 2.39 | 5.26 |
| aeronautics (CPC B64) | 2005–2023 | (a) two lines, free level step | 2016.0 | 2016.0 | 2016.0 | 1.0 | 0.13 | 0.112 | 0.148 | 5.3 | 0.011 | -0.016 | 0.036 | 2.11 | 1.76 | 2.5 |
| transport and operations (CPC section B) | 2005–2023 | (a) two lines, free level step | 2016.0 | 2016.0 | 2016.0 | 0.999 | 0.069 | 0.048 | 0.089 | 10.1 | 0.02 | -0.013 | 0.051 | 2.07 | 1.73 | 2.49 |
| all patents | 2005–2023 | (a) two lines, free level step | 2016.0 | 2015.0 | 2020.0 | 0.872 | 0.062 | 0.051 | 0.074 | 11.1 | 0.027 | 0.007 | 0.049 | 1.21 | 0.98 | 1.32 |

## I.1 segment slopes (added 2026-10-14; kept for the record: Figure 4.2 no longer draws the 2016 split, see the growth models above)

Figure `q1_growth_rates`. Turning point = break year of the two-segment fit of ln count on year over 2006–2023 (`lib/growth.py:turning_point`, breaks 2009–2020, 2000 residual-bootstrap draws, generator seeded as for the eVTOL turning point of section 1); the B64 series is run alone with the same settings. The break year opens the second segment. Slope b of ln c_t = a + b t, t-interval with n − 2 df; doubling time = ln 2 / b. Source: `viz/latex_text.py:_segment_slopes`, `csv/numbers_I_segment_slopes.csv`; turning points in `viz/thesis_q1.py:_calc` (`seg`).

| series | turning point (year) | share of resampled fits choosing it | 95 % range of resampled turning points |
|---|---|---|---|
| eVTOL architecture patent families | 2016 | 91.4% | 2015 to 2018 |
| aeronautics (CPC B64) | 2016 | 99.8% | 2016 to 2016 |

| series | years fitted | n years | b | b, 95 % low | b, 95 % high | doubling time (years) | doubling, low end (from b high) | doubling, high end (from b low) |
|---|---|---|---|---|---|---|---|---|
| eVTOL architecture patent families | 2005–2023 | 19 | 0.197 | 0.16 | 0.233 | 3.5 | 3.0 | 4.3 |
| eVTOL architecture patent families | 2005–2015 | 11 | 0.136 | 0.075 | 0.197 | 5.1 | 3.5 | 9.2 |
| eVTOL architecture patent families | 2016–2023 | 8 | 0.03 | -0.036 | 0.096 | 23.3 | 7.3 | no doubling |
| aeronautics (CPC B64) | 2005–2023 | 19 | 0.146 | 0.124 | 0.169 | 4.7 | 4.1 | 5.6 |
| aeronautics (CPC B64) | 2005–2015 | 11 | 0.13 | 0.102 | 0.157 | 5.3 | 4.4 | 6.8 |
| aeronautics (CPC B64) | 2016–2023 | 8 | 0.011 | -0.02 | 0.042 | 63.8 | 16.4 | no doubling |

## I.2 on the in-domain directory (2026-10-15)

The directory side of `q4_class_mix`, `q4_dataset_vs_directory_classes` and `q4_dataset_vs_directory_subsets` is now the 871 pages of `frames.directory_frame()['in_domain']` (electric and crewed, rules of Section 3.1.1 and the author's single-page rulings); before, all 1 229 pages. The patent dataset is unchanged. Source: `viz/latex_text.py:_in_domain_directory`, `viz/thesis_q4.py` (`class_mix`, `directory_mix`, `directory_keys`); tables in `csv/numbers_I_in_domain_directory.csv` and `csv/numbers_I_in_domain_directory_parts.csv`.

**Which pages enter `q4_class_mix`.** Of the 871 in-domain pages, 782 have a development year and are placed in a cohort (the figure prints each cohort's page count under its bar); 89 are left out of the figure because they have no year: 81 where the year rule found none and the author did not read the page, 8 that the author read and left without a year; 86 of the 89 have no dated statement on the page at all. The 89 stay in the all-years comparison (chi-square, `q4_dataset_vs_directory_classes`, the parts), which does not need a year. The year file is `review/script_outputs/YEAR.csv`.

| number | old: all pages | new: in-domain pages |
|---|---|---|
| directory pages used (all years, chi-square and parts) | 1 229 | 871 |
| directory pages with a development year, entering q4_class_mix | 1093 | 782 |
| directory pages in <= 2011 | 70 | 45 |
| directory pages in 2012-15 | 126 | 90 |
| directory pages in 2016-19 | 393 | 307 |
| directory pages in 2020-23 | 387 | 271 |
| directory pages in 2024-26 (partial) | 117 | 69 |
| chi-square of the two mixes, all years (4 df) | 203.0 | 208.3 |
| `mix_p` | < 0.001 | < 0.001 |
| adjusted residual, Vectored Thrust | +10.0 | +10.1 |
| adjusted residual, Lift + Cruise | +4.4 | +4.4 |
| adjusted residual, Wingless | −10.8 | −10.7 |
| adjusted residual, Electric Rotorcraft | −5.1 | −4.7 |
| adjusted residual, Hoverbike / Personal Flying Device | −4.1 | −5.2 |
| `resid_low` (category carrying it) | −10.8 (Wingless) | −10.7 (Wingless) |
| `resid_high` (category carrying it) | +10.0 (Vectored Thrust) | +10.1 (Vectored Thrust) |
| `closest_subset` | (d) linked to a patent of this dataset | (d) linked to a patent of this dataset |
| `closest_chi2` | 6.1 | 3.2 |
| `closest_p` | 0.194 | 0.527 |
| `closest_n` | 97 | 83 |
| `wm_dir` (Wingless share of the directory) | 30 % | 30 % |
| `wm_domain` (Wingless share of the in-domain pages) | 30 % | 30 % |
| `wm_flying` | 36 % | 41 % |
| `wm_linked` | 10 % | 11 % |
| Lift + Cruise share of the directory, <= 2011 | 8.6% | 4.4% |
| Lift + Cruise share of the directory, 2012-15 | 10.3% | 10.0% |
| Lift + Cruise share of the directory, 2016-19 | 17.0% | 16.0% |
| Lift + Cruise share of the directory, 2020-23 | 19.9% | 19.6% |
| Lift + Cruise share of the directory, 2024-26 (partial) | 32.5% | 33.3% |
| Vectored Thrust share of the directory, <= 2011 | 30.0% | 26.7% |
| Vectored Thrust share of the directory, 2012-15 | 42.1% | 35.6% |
| Vectored Thrust share of the directory, 2016-19 | 31.0% | 31.6% |
| Vectored Thrust share of the directory, 2020-23 | 37.7% | 35.4% |
| Vectored Thrust share of the directory, 2024-26 (partial) | 27.4% | 23.2% |
| largest directory category, <= 2011 | Vectored Thrust | Wingless |
| largest directory category, 2012-15 | Vectored Thrust | Vectored Thrust |
| largest directory category, 2016-19 | Vectored Thrust | Vectored Thrust |
| largest directory category, 2020-23 | Vectored Thrust | Vectored Thrust |
| largest directory category, 2024-26 (partial) | Lift + Cruise | Lift + Cruise (tie) |

**Parts of the directory against the dataset** (chi-square of the dataset's mix against the part's mix, 4 df; the in-domain part of the old figure is now the directory itself, and the parts are subsets of the in-domain pages):

| source | n old | chi-square vs dataset old | p vs dataset old | p vs dataset (Holm) old | n new | chi-square vs dataset new | p vs dataset new | p vs dataset (Holm) new |
|---|---|---|---|---|---|---|---|---|
| directory: in-domain pages | - | - | - | - | 871 | 208.3 | < 0.001 | < 0.001 |
| (b) concept designs | 420.0 | 103.3 | < 0.001 | < 0.001 | 274 | 92.4 | < 0.001 | < 0.001 |
| (b) flying hardware | 247.0 | 158.4 | < 0.001 | < 0.001 | 155 | 146.9 | < 0.001 | < 0.001 |
| (d) linked to a patent of this dataset | 97.0 | 6.1 | 0.194 | 0.194 | 83 | 3.2 | 0.527 | 0.527 |
| (d) not linked to a patent | 1132.0 | 225.7 | < 0.001 | < 0.001 | 788 | 236.9 | < 0.001 | < 0.001 |

Vectored Thrust is the largest directory category in every complete cohort (≤2011 to 2020–23): old yes, new no; in every cohort including 2024–26: old no, new no.

**Analysis III.4** (`q7_iii4_directory_categories`, `q7_iii4_directory_fold`) does not use directory pages: it folds the patent dataset's own architectures to the five directory categories (`analysis_iii.directory`, `analysis.class_fold`), so its share and ²D values do not change and it was not rerun.

## 7b. Not actively protected by filing office and priority-year cohort (added 2026-10-14)

The 598 designs of `q1_in_force_status` (the nine architectures of ten designs or more). Not actively protected = no patent that shows the design is in force at the snapshot. The four cohorts are the complete ones; the fifth, 2024-26, is partial and has only 2 US-office designs, so it is shown to reconcile the 598 but left out of the test (sensitivity with it below). Source: `viz/latex_text.py:_office_by_cohort`, table in `csv/numbers_I_office_by_cohort.csv`.

| priority-year cohort | designs | US office: designs | US office: not actively protected | other offices: designs | other offices: not actively protected |
|---|---|---|---|---|---|
| <= 2011 | 57 | 45 | 62.2% | 12 | 100.0% |
| 2012-15 | 56 | 36 | 41.7% | 20 | 45.0% |
| 2016-19 | 203 | 138 | 18.8% | 65 | 67.7% |
| 2020-23 | 230 | 131 | 9.2% | 99 | 30.3% |
| 2024-26 (partial) (not in the test) | 52 | 2 | 0.0% | 50 | 8.0% |
| all | 598 | 352 | 23.0% | 246 | 40.2% |

**Cochran-Mantel-Haenszel**, office (other offices against US office) x not actively protected, stratified by the four cohorts (546 designs; no continuity correction):

- CMH statistic = 59.36, 1 df, p = 1.3e-14
- common odds ratio (Mantel-Haenszel) = 5.06, 95 % CI 3.26 to 7.85 (other offices against US office; above 1 = other offices more often not actively protected)
- odds ratio in each cohort: <= 2011 undefined (a zero cell), 2012-15 1.15, 2016-19 9.03, 2020-23 4.31
- Breslow-Day test that the odds ratio is the same in the four cohorts: statistic 11.84, p = 0.0079
- sensitivity, all five cohorts (598 designs): CMH = 59.50, p = 1.2e-14; common odds ratio 5.08, 95 % CI 3.27 to 7.88

**Plain chi-square**, same four cohorts pooled, ignoring cohort (546 designs): chi-square (Yates) = 35.74, p = 2.3e-09; odds ratio = 3.12, 95 % CI 2.15 to 4.54 (Wald).

## 8. The funnel of section 4.1 in one table

| step | count |
|---|---|
| patent query hits (PatSeer, snapshot 2026-06-08) | 1 639 |
| T1: patents approved at labelling (patent triage) | 1 108 (879 after the domain gate) |
| T2: whole-aircraft figures approved (image triage), and the patents they sit on | 1 530 figures on 575 patents |
| designs characterised | 621 (on 540 primary patents) |
| directory pages (VFS eVTOL directory) | 1 229 |
| kept by the corrected domain rules | 871 |
| pages matched to a design (and the designs they give) | 97 pages, 99 designs |
| companies read in full (index company map) | 43 |
| companies where the script and the author agree (counting the companies both leave blank) | 35 of 43 |
| companies where the script returns a match | 18 |
| index companies that file in the dataset | 22 |

## Follow-up 2026-10-24, lag-corrected total

Source: `viz/followup_part1.py` (`frames.with_publication`, `lib.growth.visible_share`; no figure changed). Professor comments 35 and 71.

Method: the correction of V.3 (`frames.region_years`, behind na_share_2023_corr) applied to the total instead of per region. Reference = the 354 designs of priority years 2016-21, whole years from priority to publication (0 y: 42, 1 y: 143, 2 y: 108, 3 y: 50, 4 y: 11). Snapshot 2026-06-08. Part visible for priority year y, with k = 2026 - y and f = day of year / 365: P(lag <= k - 1) + f * P(lag = k). Designs expected = designs counted / part visible. The check column sums the same correction run region by region on each region's own lags. CSV: `q1_filings_per_year_lag_corrected.csv`.

|   priority year |   designs counted (raw) |   visible at the snapshot (%) |   estimated not yet published |   designs expected after correction |   check: sum of per-region corrections |
|----------------:|------------------------:|------------------------------:|------------------------------:|------------------------------------:|---------------------------------------:|
|            2016 |                      34 |                         100   |                           0   |                                34   |                                   34   |
|            2017 |                      52 |                         100   |                           0   |                                52   |                                   52   |
|            2018 |                      68 |                         100   |                           0   |                                68   |                                   68   |
|            2019 |                      59 |                         100   |                           0   |                                59   |                                   59   |
|            2020 |                      69 |                         100   |                           0   |                                69   |                                   69   |
|            2021 |                      72 |                         100   |                           0   |                                72   |                                   72   |
|            2022 |                      48 |                          98.2 |                           0.9 |                                48.9 |                                   48.7 |
|            2023 |                      48 |                          88.9 |                           6   |                                54   |                                   55.6 |

Reading: the decrease from 72 (2021) to 48 (2022 and 2023), 33 % raw, survives the correction: 72.0 to 48.9 (2022) and 54.0 (2023), a decrease of 32 % and 25 %; the correction adds 0.9 designs to 2022 and 6.0 to 2023, against the 24 needed to close the gap.
