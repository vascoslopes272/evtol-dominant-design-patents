# 12_other_sources

The evtol.news directory and the AAM Reality Index. The rules read the public page of each aircraft and the index, and write the lists the analysis uses.

| Step | What it does |
|---|---|
| `notebooks/12A_directory_page_rules` | Applies the rules to every page and writes four lists: domain, year, readiness level, company map (`2_analysis/review/script_outputs`) |
| `scripts/12A1_page_trl.py` | The readiness level of every page, with the rule of the analysis, applied to all pages |
| `scripts/12A2_page_trl_level7.py` | A rule for readiness level 7 or higher, written for the census of the gold standard |
| `scripts/yearscript/` | The rules themselves: `year_rule`, `trl_rule`, `trl_page_rule`, `ari_rule` and `split_sentences` |

The rules are keywords with no model. The author checked a sample and then took the rest as reliable. The accuracy found is in `eVTOL_dataset/06_external/61_evtol_news_directory/directory_accuracy.csv`.

The rules were developed on pages the author did not review, with the agreement of two earlier readings of the same pages as a stand-in target. Those readings are not part of the dataset, and the author's own review sample was used to score the rules once.
