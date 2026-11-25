# Results text, Q7 (Analysis III, dominant design)

Generated from `viz/thesis_text_q7.py` with `viz.thesis_q7.numbers(ctx)`.

## Method

- **Objective:** Whether a dominant design exists, one layout most new designs copy after competing alternatives (Abernathy and Utterback, 1978).
- **Data and unit:** Unique designs by priority year or four-year cohort, in four configuration sets, A, A·W·T, A·U and F. The main base is all designs; the actively protected designs are a sensitivity base, read alone and never mixed with the main one.
- **Procedure:** Three conditions asked in the same period on one base, the largest configuration's share, the balance ²D and the form ΔQ. ΔQ uses one declared weighting (w15): 15 dimensions of the codebook, each of its four systems weighing 1 (the table of method III.2).
- **Test:** Share above half in two consecutive read years; ²D and ΔQ below their 1000-permutation bands.
- **Limit:** Patent records have no sales, so renewal fees stand in; the latest years are still filling.

## A. Defining the candidates

[tab:q7_archetype_sets] gives the four configuration sets the test is run in. At A the same designs are 12 architectures that behave like 7.3 equally common ones. A·W·T and A·U cut them finer, into 39 and 44 configurations. The largest single design in any set is F, with 39 % of the whole corpus against 26 % for Lift + Cruise alone. At A·U the largest configuration holds 10 %.

The configuration set, not the corpus, sets how many designs there are, so every claim below names its set. F was defined after the architecture and configuration readings had been seen, and no result on it is a pre-registered test.

## B. The test

On all designs, the main base, F meets two of the three conditions in 2020-23 and misses the third by one design. [fig:q7_condition2_balance] shows the balance condition met, F's ²D 3.25 against a band edge of 3.66. [fig:q7_condition3_cohesion] shows the form condition met, ΔQ −0.026 against a band edge of −0.022. [fig:q7_condition1_family] shows the counts condition missed: F holds 56.9 % of the designs of 2021 but 49.3 % of 2020 (34 of 69), 1 design short of half, so no two consecutive years are above half.

The form condition uses one weighting only, w15: 15 dimensions of the codebook with each of its four systems weighing 1 (the table of method III.2). For A, A·U and F, which read the same designs, ΔQ is −0.026 against a band edge of −0.022.

No set meets the three conditions in the same period on all designs ([tab:q7_verdict_table]). A, A·W·T and A·U fail the counts condition, their largest configuration reaching at most 36.2 % of a year's designs.

## C. Robustness

Read alone on the actively protected designs, the sensitivity base, the result moves rather than holds. F meets the counts condition there, 51.8 % and 59.3 % in 2020 and 2021 (28 of 54 and 35 of 59), and the balance condition, ²D 3.14 against 3.49. It misses the form condition, ΔQ −0.029 against a band edge of −0.023. The two bases are never combined, so neither gives F the three conditions in one period.

On granted and live patents alone F holds 53 % and 59 % of the same two years. Only 80 % and 34 % of the actively protected designs of the two last years hold a granted patent, so whether the family held after them cannot be said. What holds on every base is a shared morphology, a fixed wing carrying many propulsors, and not a shared functional allocation.

## D. By region

[fig:q7_region_family_share] shows the three regions reaching F in like measure. In 2020-23 F holds 48 % of North America's aircraft. Europe holds 57 % and Asia-Pacific 46 %. No regional difference in F is detected in any window from 2012, the smallest p being 0.13. North America is the one region whose F share rises detectably, ρ +0.20 with p 0.004.

The tilting lean is North America's and not only its largest assignee's. Without Bell / Textron 60 % of North America's aircraft still tilt (p 0.027), more than in Europe or Asia-Pacific ([fig:q7_region_lean_without_largest_filer]). Two assignees of one region are no more alike than two of different regions, 0.48 against 0.52 ([fig:q7_region_firm_proximity]).

Among the index assignees that disclose funding, 67 % of the aircraft sit in F when each assignee is weighted by its funding, against 39 % of the whole corpus. With 10 assignees behind it this is an indication only.

## Answer

The sector shows a shared morphology that cuts across two architectures, Lift + Cruise together with the CVT designs that tilt a propulsor set on a fixed wing, in simple words a fixed wing carrying many propulsors. On all designs that family F meets balance and form in 2020-23 and misses the counts condition by one design (2020: 34 of 69, 49.3 %). On the actively protected designs, read alone, it meets counts and balance and misses form (ΔQ −0.029 against −0.023). No single architecture or configuration comes close, the largest reaching 36.2 % of a year's designs. The members of F part on the functional allocation of thrust, so a dominant design in the full sense is not found. The three regions hold F in like measure by 2020-23.

## Appendix captions

- `q7_verdict_table`: On all designs no set meets the three conditions in one period: F meets balance and form in 2020-23 and misses counts by one design; on the actively protected designs, read alone, F meets counts and balance and misses form. At A·W·T the three largest configurations hold 47 % of 2020-23, an era of ferment.
- `q7_region_lean_without_largest_filer`: North America's tilting lean outlives Bell / Textron, with 60 % of its aircraft still tilting without the assignee (p 0.027).
- `q7_region_firm_proximity`: Two assignees of one region are no more alike than two of different regions, 0.48 against 0.52. Europe's assignees are the least alike.
- `q7_cannot_answer`: [hl]The labelled dataset answers eight stakeholder questions only in part or not at all. Mission, size, certification and claim scope are not labels, so they need another study.[/hl]
