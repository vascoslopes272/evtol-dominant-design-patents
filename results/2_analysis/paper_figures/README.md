# Paper P1 figure panels

One vector PDF per panel, 85 x 65 mm (one column), made by `2_analysis/scripts/33_paper_figures.py` from the tables of notebooks 21-29 and
`results/2_analysis/family_F/percentiles_*.csv` (script `31_family_F_numbers.py`). Same axes rectangle, Liberation Sans 7 pt, no title,
panel letter or in-image legend, white background, left and bottom spines only. Each PDF has a CSV of the plotted values next to it.

| file | content |
|---|---|
| fig4_architecture_shares.pdf | share of designs per architecture and cohort; first two cohorts and 2024-26* hollow (not tested); direct labels are architecture codes |
| fig5a/5b/5c_balance_L1/L2/L3.pdf | 2D of A, A-W-T, A-U: all designs (black, solid, grey band) and protected designs (blue, solid, filled; own band as a dark thick dotted outline); same cohort position; untested 2024-26* grey, dashed, hollow; red ring = below band; legend in 5a only; 5a and 5b y axis tight (bands whole, whiskers cut at the axis limits) |
| fig5d_disparity.pdf | ΔQ in the reading of the thesis (Table 4): all designs and protected designs, all five protected points against the baseline (all designs, two earliest cohorts) and the band of all designs; 2024-26* untested |
| fig6a/6b/6c_modal_SLC/TP/CVT.pdf | layouts inside the three largest architectures (5 cohorts, 2024-26* faded) |
| fig6_legend_SLC/TP/CVT.pdf | one legend strip per panel (85 x 10.8 mm): the categories differ between the three architectures |
| fig7a_F_share.pdf, fig7b_F_balance.pdf | family F share per priority year (legend in the panel), and 2D of F (full legend); same symbols as Fig 5 |
| fig7c_exploratory_check_dQ_inside_F.pdf | EXPLORATORY check of ΔQ inside F (architecture weight 0), 120 x 170 mm: per cohort and per dimension against the lower band edge; no convergence inside F |

`comparison_with_notebooks.csv` compares every all-designs value and band with the notebooks' tables; `log.txt` lists what did not fit.
The permutation count behind the bands is written in `log.txt` (the figures are redrawn with `python 33_paper_figures.py` after
`31_family_F_numbers.py --perms 10000` has finished).
