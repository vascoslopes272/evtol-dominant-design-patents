# 1_data_acquisition

How the dataset was made. It has two parts, one for what comes from the patents and one for what comes from other sources. In each, notebooks and scripts are named with the step number and a letter, in the order of the work. A script that belongs to a notebook takes its letter and a number (`11B1`, `11B2`, ...).

| Folder | What it covers |
|---|---|
| `11_patent_information` | Everything that comes out of the patents: the query and the gold standard that checks it, the download of pages and figures, the figure crops, the reading of the text, the labelling tool and the tables of labels |
| `12_other_sources` | The evtol.news directory and the AAM Reality Index: the rules that read each aircraft page (domain, year, readiness level) and match the companies |

Every folder has the usual layout: `notebooks/`, `scripts/` and, when the code is imported, `src/`. Paths in the scripts are read from environment variables or from the config file of the folder, so edit those before running.
