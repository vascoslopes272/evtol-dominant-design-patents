#!/usr/bin/env bash
# Runs the nine analysis notebooks in order and then publishes the results folder.
# Needs the public dataset: unzip it next to the repository (folder eVTOL_dataset) or set EVTOL_DATASET=/path/to/eVTOL_dataset
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGS="${LOGS:-$HERE/../results/2_analysis/_logs}"; mkdir -p "$LOGS"
export PYTHONPATH="$HERE/src"
cd "$HERE/notebooks"
for n in ${NOTEBOOKS:-21_evidence_base 22_design_space 23_dominant_design 24_evolution_of_the_design_space 25_assignees_and_regions 27_form_families 28_multiple_comparisons 29_dominant_design_without_one_assignee 26_results_freeze}; do
  s=$(date +%s)
  jupyter nbconvert --to notebook --execute "$n.ipynb" --output "$LOGS/$n.executed.ipynb" --ExecutePreprocessor.timeout=3600 --ExecutePreprocessor.kernel_name=python3 > "$LOGS/$n.log" 2>&1
  echo "$n exit $? $(( $(date +%s) - s ))s" >> "$LOGS/STATUS.txt"
done
cd "$HERE/src" && python3 -m viz.dataset_ids "$HERE/../results/2_analysis" >> "$LOGS/STATUS.txt" 2>&1
echo DONE >> "$LOGS/STATUS.txt"
