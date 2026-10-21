#!/usr/bin/env bash
set -Eeuo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 SOURCE_DIRECTORY BACKUP_DIRECTORY" >&2
  exit 2
fi

source_dir=$1
backup_dir=$2

if [[ ! -d "$source_dir" ]]; then
  printf 'Error: source directory does not exist: %s\n' "$source_dir" >&2
  exit 1
fi

source_dir=$(cd -- "$source_dir" && pwd -P)
mkdir -p -- "$backup_dir"
backup_dir=$(cd -- "$backup_dir" && pwd -P)

if [[ "$backup_dir" == "$source_dir" || "$backup_dir" == "$source_dir/"* ]]; then
  echo "Error: backup destination must not be inside the source directory." >&2
  exit 1
fi

stamp=$(date '+%Y%m%d_%H%M%S')
base=$(basename -- "$source_dir")
archive="$backup_dir/${base}_${stamp}.tar.gz"

tar -czf "$archive" -C "$(dirname -- "$source_dir")" -- "$base"
printf 'Backup created: %s\n' "$archive"
sha256sum -- "$archive"
