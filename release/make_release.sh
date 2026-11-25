#!/usr/bin/env bash
# Builds the two Zenodo archives from the dataset folder and writes their checksums.
# usage: make_release.sh /path/to/eVTOL_dataset [output folder]   (the dataset folder must hold 05_images/)
set -euo pipefail
SRC="$1"; OUT="${2:-.}"; cd "$(dirname "$SRC")"; N="$(basename "$SRC")"
zip -r -X "$OUT/eVTOL_dataset.zip" "$N" -x "$N/05_images/*"
zip -r -X -0 "$OUT/eVTOL_dataset_images.zip" "$N/05_images"   # images are already compressed
cd "$OUT"; cp "$SRC/README.md" README.md
sha256sum README.md eVTOL_dataset.zip eVTOL_dataset_images.zip | tee SHA256SUMS
