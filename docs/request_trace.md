# Request trace: every request for numbers of paper P1, where it is answered, and how far it can be trusted

Dataset `eVTOL_dataset` (621 designs, 619 with an architecture), thesis seed 42. Written 2026-11-26. Paths are relative to the repository unless they start with `eVTOL_dataset/`. Scripts are in `2_analysis/scripts/`; the notebook `2_analysis/notebooks/31_pending_numbers.ipynb` runs them in order. The assembled text is `results/2_analysis/pending_numbers/pending_numbers.md`; the same files are in `paper_figures_for_other_pc/numbers/`.

**Status words.** `done`: computed from the dataset by a script in the repository, file given. `done, differs from the paper`: computed, and the value is not the one the paper quotes (listed in the last section). `waits for the run`: needs the coding-noise runs, which were still running when this was written. `not possible`: the information is not in the files; the reason is given.

**How far each kind of number can be trusted.**
- Numbers that come straight from a table or from a thesis function called unchanged (counts, shares, Wilson intervals, band edges, percentiles) were recomputed, and several were checked a second time by hand (configurations 12, 39, 44; effective numbers 5.72, 11.32, 22.78; Gower worked example against the library to 1e-17).
- Numbers produced by a subagent were not all rechecked line by line. Items whose value disagrees with the paper (section 3 below) are the ones to read before they are used.
- The coding-noise numbers (items 1 to 4) are not final until the three runs listed in section 2 have finished.

## 1. The twenty items (prompt of 2026-11-26)

| # | request | status | where |
|---|---|---|---|
| 1 | replica count at 10 000 permutations; 1 000 replicas | waits for the run. 1 000 replicas at 10 000 permutations do not exist (about 42 h); the 1 000-replica run at 1 000 permutations is repeated with the new rule as the labelled reference | `pending_part_A.md` A1, `pending_csv/A1_replica_counts.csv`, `40_pending_block_A.py` |
| 2 | Table S7: every result, original, share kept under weights and under coding | waits for the run | `pending_csv/A2_S7_every_result.csv` |
| 3 | numbers of S5 and 4.4 (dQ below band, F three conditions, F fails share, medians, standard wings, TP decline) | waits for the run | `A3a_*.csv`, `A3b_*.csv` |
| 4 | verdict for F under replicas, both bases | waits for the run | `A4_F_verdict_*.csv` |
| 5 | rarefaction 30, 40, 50, all levels and bases; which verdicts change | done, differs from the paper (two cells change, not one) | `pending_part_B_C.md` item 5, `39_rarefaction_verdict_table.py` |
| 6 | variety threshold 70, 80, 90 % | done | item 6, `43_variety_window_tables.py` |
| 7 | share condition with 2, 3, 4 consecutive years, every level and base | done | item 7, `38_parameter_sweep.py --part window` |
| 8 | configurations at A, A·W·T, A·U and effective numbers | done, differs from the paper | item 8, `41_levels_and_last100.py` |
| 9 | new configurations in the 100 most recent designs | done, differs from the paper (4.1 against 1.6, p 0.058 not reproduced) | item 9, `41_levels_and_last100.py` |
| 10 | trends for family F alone | done, agrees with the paper | item 10, `42_family_F_trends.py` |
| 11 | Asia-Pacific 18 %; patents by priority year; the 90 % of 2023 | done; the "90 %" has two possible meanings in the code | `pending_part_D.md` item 11, `45_pending_D_items_11_12.py` |
| 12 | the 3.4 step-up of 2016 against 2.1 | done, differs from the paper (no "3.4 per cent" exists; factors from two procedures) | item 12 |
| 13 | Table S1 | done; reasons for exclusion are not written in the code | `46_pending_D_item_13_table_S1.py` |
| 14 | Table S2 | done | `47_pending_D_item_14_table_S2.py` |
| 15 | list of coding locks | done (12 locks; `05a_audit_lock_tests.py` named in a docstring is not in the repository) | `pending_part_D2.md` item 15, `55_pending_part_D2.py` |
| 16 | PatSeer queries, date, funnel | done; the count before family grouping is not stored; the search date comes from the export file | item 16 |
| 17 | how the 68 % and 72 % were drawn, with intervals | done, differs from the paper (no sample exists, both are counts over full sets) | item 17 |
| 18 | architecture mix against the VFS directory; ten mismatches | done | item 18 |
| 19 | Gower worked example | done | item 19 |
| 20 | Spearman and Holm list | done; driver and regional rows are read from the freeze files, not recomputed | `48_pending_D_item_20_spearman_holm.py` |

## 2. Coding-noise runs (new rule: list the values that break no lock, draw one at random; empty list keeps the original value)

| run | replicas | permutations | tag in `results/31_label_reliability/` | expected end (2026-11-26) |
|---|---|---|---|---|
| 15 % per value | 120 | 10 000 | `allowed_r15_p10000` | about 06:30 |
| 15 % per value, reference | 1 000 | 1 000 | `allowed_r15_p1000_n1000` | about 09:00 |
| 20 % per value | 120 | 10 000 | `allowed_r20_p10000` | about 14:00 |
| first version (redraw whole design up to 20 times), kept for the record | 120 | 10 000 | `r15_p10000` | done 2026-11-26 00:26 |

The first version is not the rule the Methods describe; its numbers are labelled as such wherever they appear. The new rule raises the share of architecture labels that change from 7.3 % to about 14 % (two test replicas, 87 of 621 designs each).

## 3. Where the files disagree with the paper (the author decides)

1. Rarefaction: balance verdicts change in two cells, not one: A·W·T all designs 2020-23 (percentile 2.7, 2.8, 2.5 at n = 30, 40, 50; below band only at 50) and A·U protected 2020-23 (3.0, 2.3, 2.6; below band only at 40).
2. Configurations: 12, 39, 44 on the whole corpus; the paper's 43 is A·U on complete years (to 2023). The effective numbers 7.3, 16.4, 29.3 are not the 2D (5.72, 11.32, 22.78); 7.3 is the 1D value at A, 16.5 and 29.6 the 1D values at the other levels.
3. The 100 most recent designs: 4.18 new configurations at A·W·T against 1.44 at random (p 0.007 or 0.0375 by the two estimators); at A·U 1.06 against 0.79. The paper's 4.1, 1.6, p 0.058 has no source in the files.
4. "3.4 per cent": the files hold factors, 3.45 for families (turning-point procedure) and 2.10 for aeronautics (level step of model a). Like-for-like: 3.30 against 2.10 (fit to 2022), 3.52 against 2.11 (fit to 2023).
5. 68 % and 72 %: no random sample is documented. 68 % is 1 108 of 1 639 families approved (Wilson 65.3 to 69.8); the completeness census gives 33 of 46 aircraft (71.7 %) and 31 of 43 programmes (72.1 %).
6. "90 % for 2023": either the p90 of the publication lag (3 years, a typed constant) or the share of 2023 designs already published (89.7 %).
7. Architecture-label change: 7.5 % in the text; 7.3 % under the first version, about 14 % under the rule of the paper.
8. Coding-noise values quoted in the text (13 to 18 %, 0.9 %, 99.7 to 100 %, 0.87 to 0.74, 73 %) come from the first run (1 000 replicas, 1 000 permutations, redraw rule) and are replaced by the new runs.
