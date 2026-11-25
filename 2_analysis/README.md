# 2_analysis

The analysis of the dataset. It reads the public dataset and writes every figure and table of the analysis to `results/2_analysis`.

Run `20_run_all.sh` to run the nine notebooks in order (the dataset is expected in `eVTOL_dataset`, next to this repository, or at the path in the variable `EVTOL_DATASET`).

| Notebook | What it produces |
|---|---|
| `21_evidence_base` | Part I, the evidence base: patenting rate, protection, the establishment of the sector |
| `22_design_space` | Part II, the design space |
| `23_dominant_design` | Part III, the dominant design |
| `24_evolution_of_the_design_space` | Part IV, the evolution of the design space |
| `25_assignees_and_regions` | Part V, assignees and regions |
| `26_results_freeze` | The last steps: the numbers that the text quotes and the check of the results. It copies what the other notebooks wrote, so it runs last |
| `27_form_families` | Families of designs defined by form (exploratory) |
| `28_multiple_comparisons` | The register of multiple comparisons (Holm) and the sensitivity to the thresholds |
| `29_dominant_design_without_one_assignee` | The dominant-design test without two assignees |

Folders and files:

- `20_config.yaml` lists every path and constant. `PYTHONPATH=src python -m viz.config` checks that every input exists.
- `20_run_all.sh` runs the notebooks and then publishes the ids of the results.
- `notebooks/` holds the nine notebooks and `thesis_style.py`, the style they all use.
- `src/viz` builds the tables and figures. `src/viz/dataset_public.py` reads the public dataset and gives the code the tables it expects. `src/lib` holds the statistics (association, concentration, distance, diversity, dominant design, growth, intervals, multiple comparisons, regional).
- `review/` holds the rule scripts for domain, year, readiness level and company map, with the author's overrides. The rule outputs are in `review/script_outputs`.
- `assets/` holds the drawings of the codebook and the dimension register.
- `tests/reference/` holds the numbers the results are checked against.
