# Pending numbers, part D2 (items 15 to 19)

Script for items 16 to 19: `2_analysis/scripts/55_pending_part_D2.py` (REPO = evtol-design-space-analysis-tools), run on `eVTOL_dataset` (621 designs, 619 with an architecture), seed 42 (no random draw), nothing interpreted. CSVs in `numbers/pending_csv/` (names `D2_*`). Item 15 is read from files, no script.

## 15. Coding locks (12 locks)

Rule source: `eVTOL_dataset/03_patents/34_codebook.md` section 7, lines 213-230 (one row per lock, lines 219-230). Where a broken lock is detected in the robustness run: `REPO/3_robustness/31_label_reliability/src/perturb.py`, function `locks(r)`, lines 200-304 (one `out.add("Ln")` per lock, line given below). Use: `perturb.py:455` (`if locks(r) <= self.orig_locks[i]`) accepts a perturbed design only if it breaks no lock its original codes do not break; otherwise it is redrawn up to `MAX_REDRAWS = 20` (`perturb.py:46`), then keeps its original codes (docstring `perturb.py:27-30`). Wizard: `REPO/1_data_acquisition/11_patent_information/wizard/11H_master_wizard.html` (lines given). The codebook says the wizard blocks a locked combination and the export check reports it as an error; identifiers L9, L11, L13 are not used.

| lock | rule in words | applies at | codebook line | perturb.py line | wizard line |
|---|---|---|---|---|---|
| L1 | SLC: no propulsor tilts | M3 | 219 | 263 | 2263 (propKinLock) |
| L2 | TW, SLC, SRW, TF, PTC, RC: propulsor articulation Fixed on every propulsor set (TP, CVT, MR free; DS has L7) | M3 | 220 | 265 | 2263-2268 |
| L3 | MR and RC: zero wings, no wing configuration recorded | M2 | 221 | 271 | 4730-4735 (wCount = 0) |
| L4 | CVT: at least two of tilting rotor, fixed rotor, tilting wing; suspended when articulation is Other or an override is used | M3, after all wings declared | 222 | 287 | 2156 |
| L5 | TW: every wing that carries propulsors is Tiltable; a thrust source that does not tilt with a wing makes it CVT; a control-only propulsor is not a thrust source; suspended by Other | M2 and M3, after all wings declared | 223 | 292 | 2188, 2491-2511 |
| L6 | TF: fuselage kinematics is Tail-sitter or Variable Incidence (the code in perturb.py accepts TiltBody, Variable Incidence, LevelCabin) | M1 | 224 | 294 | 2289-2305 |
| L7 | DS: all propulsors Fixed | M3 | 225 | 267 | 2263-2268 |
| L8 | TP: only tilting rotors; every wing Fixed and every rotor tilts on its own mount or on a tilting boom; control-only exempt; suspended by Other or an override | M2 and M3 | 226 | 297 | 2188 |
| L10 | RC and PTC: fuselage kinematics Whole-Body Pitch | M1 | 227 | 299 | 979, 2289-2306 |
| L12 | A propulsor on a tilting wing, a boom on a tilting wing, a tilting boom set or a tilting empennage has articulation Fixed (tested group by group when boom groups and boom propulsor types are equal in number); a boom ticked as on the fixed part of the wing does not tilt | M3 | 228 | 301 | 2173 |
| L14 | SLC and SRW: thrust kinematics Horizontal or Vertical, never Mixed | M3 | 229 | 303 | 2455-2465, 5006, 5017 |
| L15 | Code not TW, TP, DS, CVT or SRW and the record moves nothing: every approved figure's aircraft state is Invariant | T2 | 230 | not tested (T1/T2 fields are not perturbed, `perturb.py:24-26`) | 1794-1800, 3901-3916 |

CSV: `pending_csv/D2_15_locks.csv`. Not found: the script `05a_audit_lock_tests.py` named in the docstring of `locks()` (`perturb.py:201`) is not in REPO (find returned nothing outside results).

## 16. PatSeer query, date, funnel

- **Query string** (value: one line, as PatSeer accepts it): file `eVTOL_dataset/01_query/query_thesis.txt` (also `01_query/README.md`: "returns the 1 639 patent families"):

```
((CPC:(B64C29*) AND TACD:((aircraft OR evtol OR rotorcraft OR vtol OR vehicle) W5 (architecture OR configuration OR topology OR airframe OR fuselage OR layout OR frame OR structur* OR body OR wing* OR boom OR tilt* OR canard)) AND (CPC:(B64D27/30 OR B64D27/31 OR B64D27/32 OR B64D27/33 OR B64D27/34) OR TACD:((electri* W3 (motor* OR propuls* OR drive*)) OR eVTOL OR ("distributed" W2 "propulsion")) OR T:(tiltrotor OR "tilt rotor" OR "tilting rotor*" OR "tilting propeller*" OR (vtol AND (wing* OR fuselage OR airframe OR rotor* OR boom OR canard OR frame)))) AND PBY:[2005 TO 2026])) NOT (CPC:(B64B* OR B64G* OR B64F* OR F28* OR B64D11/06* OR B64D43* OR B64D45* OR B60F5*) OR TA:((("gasoline" OR "petrol" OR "jet" OR "turbine") W "engine") OR diesel OR "internal combustion" OR "jet propulsion" OR "gas turbine" OR "fuel cell" OR "hydrogen") OR TA:(UAV OR unmanned OR drone) OR T:("battery" OR "charging system*" OR "power management" OR cooling OR wiring OR seat* OR display* OR simulator* OR GYROSCOPIC* OR gearbox OR Circuits OR Method))
```
  Priority-year window in the query: `PBY:[2005 TO 2026]`.
- **Search date: 2026-06-08.** Source: the export file name `patseer_1639_2026-06-08.xlsx`; the file's modification time is 2026-06-08 18:54:58 (+0100). The xlsx has no search-date field of its own (workbook properties show 2026-11-26, not the search date). No other date is stored; the PatSeer Get Count is not stored.
- **Funnel** (script 55 recomputed from files 33, 42, 45; identical to `supplementary_csv/C8a_funnel.csv`, which holds more rows):

| step | families / rows | source |
|---|---|---|
| families in the export = rows of file 33 | 1 639 | `03_patents/33_patents.csv` (1 639 distinct Simple Family IDs, C8a) |
| disapproved at T1 | 531 | `is_approved == False` |
| approved at T1 | 1 108 | `is_approved == True` |
| aircraft rows on approved patents | 1 219 | `04_aircraft/42_aircraft.csv` |
| non-primary rows (duplicates D1 41 + D2 381) | 422 | `is_primary == False` |
| primary rows | 797 | `is_primary == True` |
| primary rows set aside by the gate ('but similar') | 176 | C8a |
| designs | 621 | `is_design == True`, file 45 |
| designs with an architecture (analysis frame) | 619 | `topType` not blank |
| primary patents behind the designs | 540 | C8a |

  Disapproval reasons of the 531 (file 33 `reason`): No Aircraft Image 173, Pure UAV 161, Out of Domain 158, Other 22, No Content 12, Not VTOL 5. Not computable: records retrieved before family grouping and the Get Count (not stored; C8 note).
- CSVs: `D2_16_funnel_recomputed.csv`, `D2_16_disapproval_reasons.csv`.

## 17. Relevance (68 %) and completeness (72 %), Wilson 95 % intervals

**Finding about the procedure: the files document no random sample for either figure.** Both are counts over a full set.

| quantity | k / n | share | Wilson 95 % | file |
|---|---|---|---|---|
| relevance: families approved at T1 of all 1 639 | 1 108 / 1 639 | 67.60 % | 65.30 to 69.82 % | `03_patents/33_patents.csv` (`is_approved`) |
| completeness, aircraft with a patent found: captured / (captured + outside the query) | 33 / 46 | 71.74 % | 57.45 to 82.68 % | `02_gold_standard/29_gold_standard.csv` (`aircraft_outcome`) |
| completeness, programmes with a patent found: same, one row per programme | 31 / 43 | 72.09 % | 57.31 to 83.25 % | same (`programme_outcome`) |
| completeness, all 69 census aircraft (incl. no patent found 21, search pending 2) | 33 / 69 | 47.83 % | 36.47 to 59.41 % | same |
| completeness, all 63 programmes | 31 / 63 | 49.21 % | 37.27 to 61.24 % | same |

Definition of Wilson: `lib.intervals.wilson_interval(k, n)` (95 %, no finite-population correction). Which of the completeness rows is the "72 %" is not stated in any file I found: 71.74 % (aircraft) and 72.09 % (programmes) both round to 72 %; the 68 % matches the relevance row (67.60 %). Gold-standard counts: aircraft captured 33, outside with patent 13, no patent found 21, search pending 2; programmes captured 31, outside 12, no patent 20 (`D2_17_gold_standard_counts.csv`, also split by `entered_by` and `tier`).

How the files document the procedure:
- **Relevance (judging).** `03_patents/34_codebook.md` section 3 and 4 (lines 50-64, 92-101): T1 is one answer per patent (Approve or Disapprove, with a reason); a patent is kept when it holds an aircraft inside the technological domain and at least one figure that can establish the architecture; patents were labelled in assignee order, then priority-date order, by one coder. `eVTOL_dataset/README.md` ("How the data were made"): every label in file 32 was given by the author, one patent, figure and aircraft at a time, in the wizard. So the 1 639 families were all judged; there is no drawn sample.
- **Completeness reference set (construction).** `02_gold_standard/README.md` and `22_searches_described.md`: the gold standard (file 29) is a census of mature eVTOL programmes, one row per census aircraft, built from `21_census_candidates.csv` (candidates from the evtol.news directory and the AAM index, with the reason each entered or not), searched with ten PatSeer searches (`22_searches_described.md`, `23_search_query.txt`: pool, census, enhanced, enhanced2, avic_beta, widen_winged, lift_cruise_no_patent and others, joined with OR), hits per aircraft in file 25, author answers in file 27 (`27_author_answers.csv`, in order of step). The result per aircraft is `captured`, `outside, patent found` or `no patent found`. The entry criteria in file 29 (`criterion`): VFS TRL 7, AAM index, AAM index (history), VFS TRL 6 winged, VFS TRL 6 wingless; tier TRL 7 or higher 45 aircraft, TRL 6 24 aircraft. The README states "The review pages had no button to confirm a proposal, so only changes were recorded: an empty decision means the author accepted the proposal as shown." REPO `3_robustness/33_query_completeness/README.md` has no code of its own and points to `1_data_acquisition/11_patent_information` (the account script `scripts/11A10_full_account.py`, section 4.1b, computes completeness by programme and architecture; it is an older account whose totals (43 programmes at its date) differ from the current file 29).
- **Sample-based accuracy that does exist (hand-reviewed samples, not the 68 % or 72 %):** `06_external/61_evtol_news_directory/directory_accuracy.csv` (copied to `D2_17_directory_accuracy_copy.csv`): domain flag kept pages 77 of 88 (87.5 %, 79.0-92.9), excluded pages 59 of 68 (86.8 %, 76.7-92.9); development year exact 49 of 81 (60.5 %); TRL exact 23 of 46 (50.0 %), within one level 35 of 46 (76.1 %).
- Not documented anywhere I looked: any random draw (seed, sampling frame, sample size) for a "relevance sample", and an independent judge. If the paper text says "sample", it does not match the files.

## 18. Architecture mix, dataset against the VFS directory; ten mismatches

**One sentence.** In the dataset, 366 of 619 designs with an architecture (59.1 %) are vectored thrust, 168 (27.1 %) lift plus cruise, 47 (7.6 %) wingless multicopter, 9 (1.5 %) electric rotorcraft and 29 (4.7 %) hoverbike or personal flying device, against 286 (32.8 %), 153 (17.6 %), 265 (30.4 %), 57 (6.5 %) and 110 (12.6 %) of the 871 in-domain pages of the VFS (evtol.news) directory (chi-square 208.29, 4 degrees of freedom, p = 6.2e-44; adjusted residuals +10.08, +4.43, -10.67, -4.71, -5.20).

Source: `viz/thesis_q4.py:215` `directory_mix(ctx)` (the call behind notebook `2_analysis/notebooks/21_evidence_base.ipynb`, item `q4_dataset_vs_directory_classes`, `viz/figures_part1.py:509`); directory = `06_external/61_evtol_news_directory/directory_aircraft.csv` pages with `domain_in_domain` true (871 of 1 229); the figure csv `results/2_analysis/figures/Part_I_evidence_base/I4_external_validity/appendix/q4_dataset_vs_directory_classes.csv` holds the same counts. Classes: VT = TR, CVT, TW, TB, PTC, DS (vectored thrust), LC = SLC, WM = MR, ER = RC, HB = HB/PFV (the eight SRW designs sit in none of the five, per the account script); 366+168+47+9+29 = 619. Table: `D2_18_dataset_vs_directory.csv`.

**Ten drawing-against-public-aircraft mismatches** (97 designs carry a public aircraft name; drawing label agrees on 87, so 10 do not; sources `viz/frames.py:985` `public_arch_frame`, `07_results/73_coding_agreement/coding_agreement.csv`, `supplementary_csv/B4_named_and_compared.csv`, `B5_agreement_kappa.csv`, `B5b_public_match_values.csv`: yes 81, taxonomy 6, no 9, image 1). In 9 ("no") the drawing label and the patent-text label agree with each other and not with the public aircraft; in 1 ("image") the drawing label differs from the text, which matches the public aircraft.

| design | aircraft name | label from the drawing | label from the text | public aircraft (directory `public_arch`) | match type |
|---|---|---|---|---|---|
| US2018290736A1_ad1 | S4 v1 | SLC | SLC | Vectored thrust (S4, tilt rotor) | no |
| US9975631B1_ad1 | Cora v1 | TW | TW | Lift + cruise (Cora) | no |
| US2018086448A1_ad1 | Wisk Aero | TW | TW | Conventional take-off (Z-P1) | no |
| DE102023108565B3_ad1 | Porsche-Boeing concept | SLC | SLC | Vectored thrust (concept) | no |
| US2021371117A1_ad1 | Porsche-Boeing concept v1 | SLC | SLC | Vectored thrust (concept) | no |
| DE102023133781B3_ad1 | Porsche-Boeing concept v2 | SLC | SLC | Vectored thrust (concept) | no |
| US2024253779A1_ad1 | S-A1 | SLC | SLC | Vectored thrust (S-A1 mock-up) | no |
| WO2024151705A1_ad1 | S-A1 v1 | SLC | SLC | Vectored thrust (S-A1 mock-up) | no |
| CN119262274A_ad1 | AE200 | SLC | SLC | Vectored thrust (AE200, tilt rotor) | no |
| GB201801766D0_ad1 | e-Starling | SLC | CVT | Vectored thrust (e-Starling) | image |

CSV: `D2_18_ten_mismatches.csv`. Agreement values (B5): drawing against public 87/97, kappa 0.8727, Wilson-FPC 0.83-0.94; text against public 88/97, kappa 0.8866; drawing against text 94/97, kappa 0.9613.

## 19. Worked example, Gower distance (w15)

Frame: `viz/frames.py:2242` `form_frame15(ds)` (via `gower_inputs(ds, "w15")`, 619 rows, 15 dimensions); weights `form_weights(None, "w15")` (`frames.py:2074`, from `FORM15`, `frames.py:2046`); distance `lib/distance.py` `gower_distance` with the fixed ranges of `FORM15_RANGES`: d_ij = sum_k w_k delta_ijk / sum_k w_k present_ijk, with delta = 0 if the categories match, 1 if not; for an ordered dimension |rank difference| / range (Boom count 4, Wing count 3, Propulsor band 4); Tilt share |difference|; Mount locations the Jaccard distance. Search: all pairs of the 619 whose other 13 dimensions are identical (blank counted as equal) and whose wing count and propulsor band both differ: 3 pairs (`D2_19_candidate_pairs.csv`). The pair with no blank cell and the smallest rank differences is shown (the first of the 3).

Design i = **EP4748710A1_ad1** (Leonardo, priority year 2024, cohort 2024-26 partial); design j = **DE102019001834A1_ad1** (no assignee in the table, priority year 2019, cohort 2016-19). Both architecture CVT. Propulsor band ranks: 0 = "1-3" units, 1 = "4", 2 = "5-6", 3 = "7-8", 4 = "9+" (`frames.py:34`).

| dimension | design i | design j | weight | both present | delta | w x delta |
|---|---|---|---|---|---|---|
| Architecture | CVT | CVT | 1 | 1 | 0 | 0 |
| Fuselage Shape | Oval | Oval | 0.5 | 1 | 0 | 0 |
| Boom count (rank) | 0 | 0 | 0.3 | 1 | 0 | 0 |
| Fuselage Kinematics | Fixed | Fixed | 0.2 | 1 | 0 | 0 |
| **Wing count** | 2 | 1 | 0.3 | 1 | 1/3 = 0.333333 | 0.1 |
| Wing Architecture | W | W | 0.3 | 1 | 0 | 0 |
| Vertical Position | High | High | 1/45 = 0.022222 | 1 | 0 | 0 |
| Longitudinal Position | Cent | Cent | 1/45 | 1 | 0 | 0 |
| Planform | Str | Str | 1/45 | 1 | 0 | 0 |
| Empennage Type | Conventional | Conventional | 1/3 = 0.333333 | 1 | 0 | 0 |
| **Propulsor band (rank)** | 2 (5-6) | 0 (1-3) | 0.35 | 1 | 2/4 = 0.5 | 0.175 |
| Tilt share | 0.666667 | 0.666667 | 0.3 | 1 | 0 | 0 |
| Propulsor Enclosure | Open | Open | 0.15 | 1 | 0 | 0 |
| Tractor/Pusher Arrangement | Front | Front | 0.1 | 1 | 0 | 0 |
| Mount locations | {empennage, wing} | {empennage, wing} | 0.1 | 1 | 0 (Jaccard) | 0 |
| **sum** | | | 4.0 (all 15 present) | | | **0.275** |

d_ij = 0.275 / 4.0 = **0.06875**. Check: `lib.distance.gower_distance` on the two-row frame = 0.06875; on the full 619 x 619 frame, entry (i, j) = 0.06875; absolute difference to the hand value 1.4e-17 (`D2_19_check.csv`). Per-dimension table with the sum row: `D2_19_worked_gower_example.csv`. Note the number of wings is the wing count column (2 against 1) and the band ranks differ by 2 (5-6 against 1-3 units); the other two candidate pairs differ by 1 wing and 2 ranks (US2022388647A1_ad1 against WO2012047337A1_ad1) and 1 wing and 4 ranks (EP3998191A1_ad1 against UA124132C2_ad1).

## Not possible or not found

- Item 15: script `05a_audit_lock_tests.py` is not in REPO; line references use the codebook, `perturb.py` and the wizard.
- Item 16: records before family grouping and PatSeer Get Count are not stored; the search date comes from the file name and file time only.
- Item 17: no drawing or judging procedure of a random "relevance sample" and no random draw for the completeness set are documented; figures given are full-set counts with Wilson intervals as above.
