#!/usr/bin/env bash
set -Eeuo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 DIRECTORY OUTPUT_FILE" >&2
  exit 2
fi

target=$1
output=$2
if [[ ! -d "$target" ]]; then
  printf 'Error: directory does not exist: %s\n' "$target" >&2
  exit 1
fi

target=$(cd -- "$target" && pwd -P)
# Resolve the output's parent so the manifest is not accidentally included
# when it lives inside the target directory.
out_parent=$(dirname -- "$output")
mkdir -p -- "$out_parent"
out_parent=$(cd -- "$out_parent" && pwd -P)
out_file="$out_parent/$(basename -- "$output")"

tmp_file=$(mktemp)
trap 'rm -f -- "$tmp_file"' EXIT

while IFS= read -r -d '' file; do
  [[ "$file" == "$out_file" ]] && continue
  sha256sum -- "$file"
done < <(find "$target" -type f -print0 | sort -z) > "$tmp_file"

mv -- "$tmp_file" "$out_file"
trap - EXIT
printf 'SHA-256 manifest written to: %s\n' "$out_file"
