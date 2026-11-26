# Paper P1: verdicts, robustness and the supplementary text

Draft for the supervisors, 25 November 2026. Numbers come from the public dataset (621 designs, 619 with an architecture) and from the runs in `results/` and `eVTOL_dataset/07_results`. Two runs are still going (see section 5). Nothing below depends on them, except where it says so.

## 0. How to read the robustness work (plain version)

Each result of the paper is a statement that is either true or false on the original table (for example "no architecture holds a majority"). A robustness test asks: if the input were slightly different, would the statement still be true? There are two kinds of "slightly different".

- **Different weights** (S1). The designs stay as coded, and the distance between designs is computed with 1,000 other sets of weights. If the statement stays true in most sets, it does not depend on the weights that were chosen.
- **Different coding** (S2). The weights stay as chosen, and 15 % of the coded values are replaced by random ones, 1,000 times. If the statement stays true in most replicas, it does not depend on a few coding mistakes.

The number reported for each statement is the share of the 1,000 repetitions in which it stays true. The rule for reading it is:

| Share that stays true | Reading | What the paper may say |
|---|---|---|
| 95 % or more | robust | State it plainly. |
| 70 to 95 % | mostly robust | State it, and give the share. |
| 30 to 70 % | sensitive | State it as an observation of this table, and give the share. |
| under 30 % | not robust | Do not rest an argument on it. Report it as exploratory. |

**Direction and significance are two different statements.** A result can stay in the same direction in almost every repetition and still fall inside the chance band in many of them. The table therefore reports both, and the paper should too.

| Result | Direction stays the same | Significance stays | Reading |
|---|---|---|---|
| Disparity, ΔQ in 2020-23 below 0 (A, all designs) | 99.0 % of weight draws, 87.8 % of coding replicas (85 to 88 % at A·W·T and A·U; 91 to 93 % on the protected base) | 69 % of weight draws, 14 % of coding replicas | The 2020-23 designs are closer together than the earliest cohorts in nearly every repetition. Whether the size of the change exceeds chance depends on weights and coding. |
| Propulsors rise in Tilt Propulsor (ρ > 0) | 100 % of replicas | 99 % | Robust. |
| Propulsors rise in CVT (ρ > 0) | 100 % of replicas | 41 % | The rise is always there. Its Holm-significance is not. |
| Propulsors on booms in CVT (ρ > 0) | 100 % of replicas | not significant on the original table either (Holm p 0.099) | Descriptive. |

Noise adds the same random variation to every cohort, so it pulls ΔQ toward 0 (from −0.026 to a median of −0.009) and moves it into the band. A shrunken ΔQ that keeps its sign is what dilution does to a real difference, and it is not what chance does. The band still has to be read as the test of size: inside the band, the data do not exclude that a change of this size arises from shuffling. The honest sentence is: "ΔQ is negative in 88 % of coding replicas and 99 % of weight draws, and below the chance band in 14 % and 69 %".

The cut points are a convention for reading the table and not a statistical threshold. The test is a stress test: the noise is larger than the audited disagreement for most values, so a statement that fails it is not shown to be wrong, only to need a coding better than the test assumes.

## 1. What the robustness work says, in one paragraph

The negative finding of the paper, that no architecture, wing or propulsor option holds a dominant share, survives every check: it survives 1,000 random weightings of the distance and 1,000 coding-noise replicas. The positive findings are weaker. The convergence of designs in 2020-23 (condition 3, disparity) holds in about 70 to 85 % of the weight draws, but only in 13 to 18 % of the coding-noise replicas. The family F verdict on the protected base, which meets all three conditions on the original table, meets them in 0.9 % of the replicas. These three results should be written as conditional on the coding being as accurate as the audit indicates, and should not be written as established.

## 2. Suggested wording of the verdicts

| # | Statement in the paper | Evidence | Survives | Suggested wording |
|---|---|---|---|---|
| 1 | No architecture reaches a majority (condition 1) at A, A·W·T, A·U | Largest share 36 % (A, all designs) | 100 % of replicas, all three levels | "No architecture holds a majority in any year. This holds under coding noise (1,000 replicas) and is not a product of the weighting." State without hedge. |
| 2 | All three conditions are not met at A, A·W·T, A·U | Verdict table | 100 % of replicas | "No level meets all three conditions." State without hedge. |
| 3 | Balance: the architecture mix is more concentrated than chance in 2020-23 (A, all designs) | ²D 4.55, band edge 4.75 | 80 % of replicas | "...in four of five replicas." Report the share. At A·W·T the verdict (not met) holds in 85 %, on the protected base it flips in 81 % of replicas: do not rest an argument on A·W·T. |
| 4 | Disparity: the 2020-23 designs are closer together than in the two earliest cohorts (condition 3) | ΔQ −0.026 against band edge −0.022 (A, all designs) | Weights: 69 to 84 % of draws. Coding noise: 13 to 18 % of replicas | "Designs of 2020-23 are closer together than in the earliest cohorts, by a margin that is small (0.004) and that depends on the weights and on the coding. It is not met under equal weights." Do not call it a finding of convergence. Call it a signal. |
| 5 | F meets the three conditions on the protected base | All met in 2020-23 | 0.9 % of replicas. F share above 50 % in 2020: 4.6 % | Present F as a hypothesis and not as a result: "F reaches a majority only on the protected base and not under coding noise." On the all-designs base, F fails condition 1 in 99.7 % of replicas. |
| 6 | Tilt Propulsor falls in share (ρ −0.69, Holm p 0.024) | Spearman, 16 years | 73 % of replicas | "The decline is consistent in about three quarters of the replicas." No other architecture trend is significant, in 97 to 100 % of replicas. |
| 7 | CVT propulsors rise over time, Holm-significant | Trace of propulsor count | 41 % | Do not make this a result. Write it as descriptive. Tilt Propulsor propulsors: 99 %. |
| 8 | Regions do not differ in F share in 2020-23 | χ², all assignees and without the largest | 98 to 99 % | State without hedge. |
| 9 | Entrants differ from returning assignees in architecture mix (chi-squared, first-time against returning assignees), 2016-19 and 2020-23 | p 0.015 (2016-19) and 0.010 (2020-23) | Test with p < 0.05 in 90 to 91 % of replicas | "First-time and returning assignees chose different architectures in 2016-19 and 2020-23 (p 0.015 and 0.010), in about nine of ten replicas. The difference is carried by one firm: without Bell / Textron it is not significant (p 0.59 and 0.17), in 97 to 100 % of replicas." Present it as a Bell / Textron effect and not as a general difference between entrants and incumbents. |

Leading shares fall under noise (for example standard wings 0.87 to 0.74, hover-to-cruise motion 0.85 to 0.72, ducted 0.63 to 0.53). Two dimensions that are fixed at 80 % in the original table (hover-to-cruise motion, wing configuration) are never fixed in the replicas. State the 80 % rule result for those two as "close to the threshold", with the replica value.

## 3. Draft of the supplementary material

**S1. Weights.** The distance behind the disparity condition is a Gower distance over 15 dimensions with the weights of Table A.11. To test whether the verdict depends on these weights, 1,000 weight vectors were drawn by multiplying each of the 15 weights by exp(N(0, 0.35²)), with a fixed seed (42). For each draw the disparity condition was recomputed at the three levels (A, A·W·T, A·U) on both bases (all designs, actively protected designs), with 10,000 permutations per band and the same shuffles in every draw. The condition holds when ΔQ in 2020-23 falls below the lower band edge. It holds in 69.3 % (A), 78.0 % (A·W·T) and 79.0 % (A·U) of the draws on all designs, and in 73.9 %, 82.9 % and 84.1 % on the protected designs. The median margin (band edge minus ΔQ) is 0.0035 to 0.0079, and the 5th percentile is negative at every level, that is, in the weakest 5 % of draws the condition fails. With equal weights the condition is not met at any level (margin −0.008 to −0.014). The draws change the weights only, not the data, and the band is recomputed from the same designs. The figures 74 % and 82.9 % quoted earlier belong to different levels (A and A·W·T, protected base) and are both current.

**S1b. F within itself.** With architecture weight 0, the designs of F in 2020-23 are not closer together than in the two earliest cohorts in any of the 1,000 draws (share of draws below the band 0, upper Wilson bound 0.4 %). The disparity measured on the whole cohort therefore does not come from inside F.

**S2. Coding noise.** Every value that the wizard asks for in the architecture and morphology stages (architecture, fuselage, wings, booms, propulsors) was replaced, independently, with probability 15 %: an option by another option of the same dimension, drawn uniformly, a tick by the other answer, a positive count by another observed count. Values that the wizard does not ask for, blanks, the priority year, the legal status, the region and the assignee were not changed. A design whose changed codes break a lock of the codebook (Table A.5) that its original codes do not break was redrawn, up to 20 times. All results of the paper were recomputed on each of 1,000 replicas (seed 20261118), including the gate, the levels, F, both bands (1,000 permutations), Holm corrections and the regional tests. For each yes/no result the table reports the share of replicas with the original verdict and its Wilson 95 % interval. Because the locks reject most changes of architecture, 15 % per value moves the architecture label of about 7.5 % of the designs, which sits between the disagreements found in the audit of 97 designs (3 % to 10 %, Cohen's κ 0.87 to 0.96).

**S2b. How to read it.** The noise is uniform, so it dilutes structure: leading shares fall, effective numbers rise, ΔQ moves toward 0. A result that depends on a small margin therefore fails more easily than it would under real errors, which are concentrated on a few confusions (for example tilt wing against tilt propulsor). The noise test is a stress test, and not an estimate of the error. The audit agreement is the estimate. A result that survives the stress test is robust. A result that fails it is conditional on the coding being better than the stress assumes.

## 4. Is the run valid or too strong?

- **Weights run: valid.** It tests one thing, the weights, and the margin it reports is the one the paper needs. Nothing to change.
- **Coding run at 15 %: valid as a stress test, too strong as an estimate.** The per-value rate was not measured. The only measured disagreement is at the architecture label, and 15 % per value gives 7.5 % there, which is inside the measured range. For the 14 morphological values nothing was audited. The run therefore overstates the noise if errors are rarer in the morphology than in the architecture, which is plausible, and understates it if errors are correlated.
- **Condition 3 under noise (13 to 18 %) is mostly a statement about its small margin.** The margin is 0.004 on a band of width 0.02. Any dilution moves ΔQ across the edge. This is a property of the condition and not of the dataset, and the paper should say so.
- **Changes I suggest, none blocking:**
  1. Keep 15 % and 20 % at 10,000 permutations as running (120 replicas each). They replace the 1,000-permutation run in the paper. The 1,000-permutation result stays in the supplement as the 1,000-replica reference.
  2. Add a 10 % run if the supervisors want a rate closer to the audit (optional, about the same cost as one of the two).
  3. Do not change the error model to confusion-structured errors. It needs an audit of the morphology that does not exist.

## 5. Still running or not yet computed

- Coding noise, 15 % then 20 %, 120 replicas each, 10,000 permutations: running. Gives the share of replicas that change the architecture label (the 7.5 % claim) from at least 100 replicas.
- Family F percentiles of the observed balance and disparity in their own permutation distributions, 10,000 permutations: running.
- Family F, top-option shares inside and outside F in 2020-23: done (`results/2_analysis/family_F/F_vs_rest_2020_23.csv`). Booms differ (60 % against 38 % with booms, Fisher p 0.001). Number of wings, wing configuration and tractor/pusher do not differ (p 0.26 to 0.61). Propulsor band: different leading option (9+ against 4), p 0.10.
- Item 4 numbers: collected in `results/2_analysis/paper_numbers/paper_numbers.md`.
- Entrants under both definitions: `results/2_analysis/entrants/entrants_two_definitions.csv`.

## 6. What the two tests claim, and the rules for changing the weights

**The weights of the paper are a decision, and the test does not question it.** The weights of Table A.11 follow a stated principle (each of the four systems of the aircraft carries the same total weight, and the dimensions of a system share it), and the paper reports them as the author's choice. The weight test asks a different question: how far from these weights can the distance be moved before the disparity verdict changes. It reports a margin and not a verdict on the weights. Reading it as "the weights are wrong in 20 % of cases" misreads it.

**What the current draws do.** Each of the 15 weights is multiplied by exp(N(0, 0.35²)), independently. Five times in six a factor lies between 0.56 and 1.78, so two weights can end up with a ratio of three or more, and the system totals are not kept. The draws therefore include weightings that break the principle behind Table A.11. This is a strong perturbation, and the shares that hold (69 to 84 %) are a lower bound on what a rule-bound perturbation would give.

**A rule for changing the weights, if the supervisors want one.** Two variants follow the principle of the paper and can be run with the same code and the same 10,000 permutations:

1. *Within systems.* Keep the total of each system fixed and redraw only the split among its dimensions (same σ). This tests the part of the weighting that the paper does not argue for, and leaves the part that it does.
2. *Dose and response.* Repeat the current draws at σ = 0.10, 0.20 and 0.35. The share that holds as a function of σ shows where the verdict breaks, and the reader can judge which σ is plausible. At σ = 0.10 a factor lies between 0.85 and 1.18.

I would run these only if a reviewer asks. The paper can say now that the draws are a deliberately wide stress test, that equal weights do not meet the condition (a margin of −0.008 at A), and that the margin of the chosen weights (+0.004) is small. Both variants would take hours, not minutes (not measured).

**The 0.9 % of the family F verdict comes from the coding test, and not from the weights.** Conditions 1 and 2 do not use the weights. Condition 3 on F is the disparity of the whole cohort, and under the weight draws it holds in 73.9 % (A, protected base). The F verdict under the weights is therefore the 74 % figure, provided that conditions 1 and 2 hold on the original table, which they do.

**Why the coding test lowers F so much.** On the protected base, F reaches a majority in 2020 with 51.8 % of the designs, 1.8 points above the threshold, and in 2021 with 59.3 %. Under noise the median share falls to 46.3 % and 52.5 %. F is defined by a conjunction of codes (Lift + Cruise, or a CVT with a tilting propulsor set and no tilting wing panel), and a random error leaves the class more often than it joins it, so the noise lowers F systematically and not only at random. The 0.9 % is a stress result for a class with a knife-edge majority, and is not an estimate of how often the verdict is wrong. Report it as: "F passes condition 1 by 1.8 points in 2020, a margin that coding errors of the size tested remove."

**Coding test: kept as it is.** It is a stress test with a stated rate, 15 % per value, and its architecture-label change (about 7.5 %) lies inside the audited disagreement. State that the noise is uniform, that it dilutes structure and that classes defined by a conjunction lose members faster than they gain them. With these three sentences the test does not need to be rerun.

**What would justify rerunning.** Only a request for rule-bound weights (section 6, variants 1 and 2). The coding runs in progress (15 % and 20 %, 10,000 permutations) stay as planned.
