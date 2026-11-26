# 32_weight_sensitivity

Sensitivity of the dominant-design test to the weights of its third condition. `notebooks/32A_test1_main.ipynb` is the main test (15 weights drawn at random, 1 000 draws, three levels). `notebooks/32B_test2_family_F.ipynb` is exploratory (family F, architecture weight 0). The code is in `src/ws_core.py` and `src/p1_tests.py`; it calls the analysis code in `2_analysis/src` and reads the public dataset through `2_analysis/20_config.yaml`.

The dataset is expected in `eVTOL_dataset`, next to this repository, or at the path in the variable `EVTOL_DATASET`. The results are in `eVTOL_dataset/07_results/72_weight_sensitivity` (override with `WS_RESULTS`).
