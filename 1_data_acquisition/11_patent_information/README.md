# 11_patent_information

Everything that comes out of the patents, in the order of the work. The files of the dataset that each step writes are in brackets.

| Step | Notebook or file | What it does |
|---|---|---|
| A | `11A_gold_standard`, `11A_pool_triage`, `11A_family_F_level`, scripts `11A1` to `11A20` | The gold standard that checks the query is complete (files 21 to 29). Scripts `11A1` to `11A16` build the census of mature programmes, look for their families in the search export and write the review pages on which the author answered. `11A17` and `11A18` say which clause of the query leaves a family out. `11A19` is the keyword and SBERT triage of the search results, and `11A20` with `11A_family_F_level` reads the Lift + Cruise and CVT families |
| B | `11B_patseer_download` | Downloads the images and descriptions of each family from PatSeer |
| C | `11C_triage_filter` | SigLIP separates drawings from tables in the page images |
| D | `11D_grouping` | Groups the families by company into batches. The batches were reorganised by hand afterwards, so do not run the grouping cells again without checking |
| E | `11E_figure_crop` | Cuts the figures out of the page images (DocLayout, EasyOCR, Qwen) and matches each to its description (`05_images`, `index.csv`) |
| F | `11F_wizard_feed` | Writes the suggestions the wizard shows and finds duplicates (file 30) |
| G | `11G_aircraft_identity` | Reads the text of each family: inside the domain or not, aircraft name, powertrain, take-off (file 31). Scripts `11G1` and `11G2` write the corpus-wide table |
| H | `wizard/11H_master_wizard.html` | The labelling tool. It takes a batch of suggestions (file 30) and an earlier export to resume from (file 32). The rules are in `eVTOL_dataset/03_patents/34_codebook.md` |
| I | `11I_master_labels` | Turns the export of the wizard into the tables of the dataset (files 33, 41, 42, 43). Scripts `11I1` to `11I9` do the steps, `11I8_run_build.sh` runs them |

- **The gold standard.** The census and the searches were done in several rounds. The scripts and notebooks of step A are the ones that did it. Some of their text is still in Portuguese and their paths point to working folders, so they need adapting to the files of the dataset before they run. The same holds for the scripts and the notebook of step I: they rebuild the tables from the wizard export in a working folder, not from the folders of the published dataset.
- `src/` holds the code the notebooks import (download, grouping, cropping, text reading, the wizard feed). `config.yaml` has its paths.
- The model weights (SigLIP, SBERT, DocLayout, Qwen) are not in the repository.
- `src/identity_llm.py` can build a prompt for a language model and read its answer. No value of file 31 comes from it, as the `*_source` columns of the file show.
