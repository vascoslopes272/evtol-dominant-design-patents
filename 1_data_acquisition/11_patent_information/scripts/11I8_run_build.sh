#!/usr/bin/env bash
# Rebuilds the tables of eVTOL_dataset_v1 from its wizard record (build A of 2026-11-21).
# Notebook 04 of Patent-Labelling-Tools is run in a STAGING folder: the old working inputs are COPIED (read only at the
# source), the dataset's own record, review decisions and identity are laid over them, and the output goes to staging.
# Then _build/scripts/11I4_install_build.py writes the tables into the dataset, 11I5_rename_ids.py renames the
# aircraft ids to <patent>_ad<N> (tables and image folders), and 11I6_images.py brings the image folders in line. What 06f takes out of the dataset goes to <staging>/work.
# Usage: bash _build/nb04_v16/11I8_run_build.sh <staging dir>
set -euo pipefail
ST="$1"
D="$(cd "$(dirname "$0")/../.." && pwd)"                                   # the dataset root
PLT="${PLT:-..}"     # pipeline code (read only)
AN="${AN:-../../../2_analysis}"   # analysis loader (read only)
IN="${IN:-data/labelled/inputs}"
ENV_PY="$HOME/anaconda3/envs/nb_01_review/bin/python"                       # kernel of notebook 04
rm -rf "$ST"; mkdir -p "$ST/inputs" "$ST/code/notebooks" "$ST/kernels/nb_01_review"
for x in "$IN"/*; do n=$(basename "$x"); if [ "$n" = images ]; then ln -s "$x" "$ST/inputs/images"; else cp -r "$x" "$ST/inputs/"; fi; done
cp "$D/02_patents/wizard_record_Batch_ALL.xlsx" "$ST/inputs/record/reviewed_patents_Batch_ALL.xlsx"
cp "$D"/02_patents/review_decisions/*.csv "$ST/inputs/review_decisions/"
cp "$D/02_patents/aircraft_identity_ALL.xlsx" "$ST/inputs/identity/aircraft_identity_ALL.xlsx"
# correction of 2026-11-11 (DECISIONS item 15), absent from the old text-architecture table
python3 - "$ST/inputs/text_architecture/architecture_text_final_variants.csv" <<'EOF'
import csv, sys
p = sys.argv[1]; R = list(csv.reader(open(p, newline='', encoding='utf-8'))); i = {c: j for j, c in enumerate(R[0])}
for r in R[1:]:
    if r[i['variant_id']] == 'US2024253779A1': r[i['arch_final']] = 'SLC'; r[i['provenance']] = 'adjudicated_other'; r[i['visible_in_figures']] = 'yes'
csv.writer(open(p, 'w', newline='', encoding='utf-8')).writerows(R)
EOF
cp -r "$PLT/src" "$PLT/scripts" "$ST/code/"
cp "$D/_build/nb04_v16/11I_master_labels.ipynb" "$ST/code/notebooks/04_master_labels.ipynb"
cp "$PLT/notebooks/04_other_note_tags.csv" "$ST/code/notebooks/"
cp "$D/_build/nb04_v16/11I9_wizard_view.py" "$ST/code/src/wizard_view.py"
python3 - "$PLT/config.yaml" "$ST" "$D" > "$ST/code/config.yaml" <<'EOF'
import re, sys
s = open(sys.argv[1]).read(); st, d = sys.argv[2], sys.argv[3]
s = re.sub(r'(\n  labelled_root:\s+)"[^"]*"', rf'\1"{st}"', s)
s = re.sub(r'(\n  labelled:\s+)"[^"]*"', rf'\1"{st}/inputs"', s)
s = re.sub(r'(\n  labelled_outputs:\s+)"[^"]*"', rf'\1"{st}/out"', s)
s = re.sub(r'(\n  html_template:\s+)"[^"]*"', rf'\1"{d}/02_patents/wizard/UI_for_taxonomy_caracterization_16_0.html"', s)
print(s, end='')
EOF
printf '{"argv": ["%s", "-m", "ipykernel_launcher", "-f", "{connection_file}"], "display_name": "nb_01_review", "language": "python"}\n' "$ENV_PY" > "$ST/kernels/nb_01_review/kernel.json"
mkdir -p "$ST/runs/v16"
( cd "$ST/code/notebooks" && JUPYTER_PATH="$ST" NB04_OUT_DIR="$ST/runs/v16/out" NB04_COPY_IMAGES=0 \
  jupyter nbconvert --to notebook --execute 04_master_labels.ipynb --output "$ST/runs/v16/04_executed.ipynb" --ExecutePreprocessor.timeout=2800 )
( cd "$D" && python3 _build/scripts/11I4_install_build.py "$ST/runs/v16/out" "$AN" \
           && python3 _build/scripts/11I5_rename_ids.py \
           && python3 _build/scripts/11I6_images.py "$ST/work" )
