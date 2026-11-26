#!/usr/bin/env bash
# Builds the two Zenodo archives from the dataset folder and writes their checksums.
# Four files result (README.md, two zip archives, SHA256SUMS), well inside the Zenodo limits of 100 files and 50 GB per record.
# usage: make_release.sh /path/to/eVTOL_dataset [output folder]   (the dataset folder must hold 05_images/)
set -euo pipefail
SRC="$(realpath "$1")"; OUT="$(realpath -m "${2:-.}")"; mkdir -p "$OUT"   # absolute paths: the script changes folder below
cd "$(dirname "$SRC")"; N="$(basename "$SRC")"
zip -r -X "$OUT/eVTOL_dataset.zip" "$N" -x "$N/05_images/*"
zip -r -X -0 "$OUT/eVTOL_dataset_images.zip" "$N/05_images"   # images are already compressed
cd "$OUT"; cp "$SRC/README.md" README.md
sha256sum README.md eVTOL_dataset.zip eVTOL_dataset_images.zip | tee SHA256SUMS
