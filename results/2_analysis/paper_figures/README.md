# Paper P1 figure panels

One vector PDF per panel, 85 x 65 mm (one column), made by `2_analysis/scripts/33_paper_figures.py` from the tables of notebooks 21-29 and
`results/2_analysis/family_F/percentiles_*.csv` (script `31_family_F_numbers.py`). Same axes rectangle, Liberation Sans 7 pt, no title,
panel letter or in-image legend, white background, left and bottom spines only. Each PDF has a CSV of the plotted values next to it.

| file | content |
|---|---|
| fig4_architecture_shares.pdf | share of designs per architecture and cohort; first two cohorts and 2024-26* hollow (not tested); direct labels are architecture codes |
| fig5a/5b/5c_balance_L1/L2/L3.pdf | 2D of A, A-W-T, A-U: all designs (solid, grey band) and protected designs (dashed, hollow, own band as a thin outline) |
| fig5d_disparity.pdf | ΔQ: same two series, each with its own baseline and band |
| fig6a/6b/6c_modal_SLC/TP/CVT.pdf | layouts inside the three largest architectures (5 cohorts, 2024-26* faded) |
| fig6_legend_SLC/TP/CVT.pdf | one legend strip per panel (85 x 10.8 mm): the categories differ between the three architectures |
| fig7a_F_share.pdf, fig7b_F_balance.pdf | family F share per priority year, and 2D of F; same convention as Fig 5; panel c (disparity) removed |
| fig7c_F_disparity_within.pdf | optional: ΔQ inside F with architecture weight 0, per dimension (`test2_explore_per_dimension.csv`) |

`comparison_with_notebooks.csv` compares every all-designs value and band with the notebooks' tables; `log.txt` lists what did not fit.
The permutation count behind the bands is written in `log.txt` (the figures are redrawn with `python 33_paper_figures.py` after
`31_family_F_numbers.py --perms 10000` has finished).
