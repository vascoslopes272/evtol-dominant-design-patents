# evtol-dominant-design-patents

Code behind a study of dominant designs in electric vertical take-off and landing (eVTOL) aircraft, built from patents. It covers the whole chain, from the patent query and the labelling of the designs to the robustness tests and the figures of the paper. The data are in a separate Zenodo record (**eVTOL Aircraft Designs from Patents: a labelled dataset**, DOI 10.5281/zenodo.24590068). This repository holds only code, notebooks and the results they produce.

## How the repository is organised

Folders are numbered in the order the work was done. The first digit is the part, the two digits are the step inside it. Each step has the usual layout of a code repository (`notebooks/`, `src/`, `scripts/`) when it needs it, and its own README.

| Folder | What it does | Reads | Writes |
|---|---|---|---|
| `1_data_acquisition/11_patent_information` | Everything that comes out of the patents: the query and the gold standard, the download, the figures, the reading of the text, the labelling tool and the tables of labels | PatSeer, patent records | `eVTOL_dataset/01_query` to `05_images` |
| `1_data_acquisition/12_other_sources` | The rules that read the evtol.news pages and the AAM Reality Index (domain, year, readiness level, company map) | public web pages | `eVTOL_dataset/06_external` |
| `2_analysis` | The nine notebooks that draw every figure and table of the analysis, with the statistics in `src/lib` | the dataset | `results/2_analysis` |
| `3_robustness/31_label_reliability` | Replaces a share of the labels by random errors and recomputes every result (1 000 replicas) | the dataset | `eVTOL_dataset/07_results/71_label_reliability` |
| `3_robustness/32_weight_sensitivity` | Sensitivity of the dominant-design test to the weights of its third condition | the dataset | `eVTOL_dataset/07_results/72_weight_sensitivity` |
| `3_robustness/33_query_completeness` | Where the completeness of the query is measured (it uses the code of step 11) | files 21 to 29 | |
| `results/` | The figures and CSV files of the analysis, as the notebooks write them | | |
| `release/` | `make_release.sh` builds the two archives of the dataset (`eVTOL_dataset.zip` and `eVTOL_dataset_images.zip`) | | |
| `docs/` | A page that shows the whole dataset tree, file by file | | |

## To run the analysis

1. Create the environment: `conda env create -f environment.yml`.
2. Download the dataset from Zenodo and unzip both archives into one folder called `eVTOL_dataset`, next to this repository. If it is elsewhere, set the variable `EVTOL_DATASET` to its path.
3. Run `2_analysis/20_run_all.sh`. It runs the nine notebooks in order and writes the results to `results/2_analysis`.

The first part (`1_data_acquisition`) is the record of how the dataset was made. Some of its steps need PatSeer, a browser, or a GPU, and are not meant to be re-run end to end. The labels themselves were given by the author in the wizard and are in the dataset.

## What is not in this repository

- The weights of the models used to prepare the material (SigLIP, SBERT, DocLayout, Qwen). Each step README says which model it uses and where to get it.
- The embedding analysis of the patent figures (DINOv2), which is a separate piece of work.

## Where the data come from

How each part of the dataset was made, and what was reviewed by the author, is written in the README of the dataset. Read it before using the readings of the evtol.news pages, the SBERT outputs or the web evidence of file 44.

## Licence

Code: MIT. Data: CC BY 4.0 (see the dataset record).

## Licence

The code in this repository is released under the MIT licence (file `LICENSE`). The data have their own licence, stated in the Zenodo record.
