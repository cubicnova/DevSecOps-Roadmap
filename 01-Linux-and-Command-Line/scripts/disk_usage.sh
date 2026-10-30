#!/usr/bin/env bash
set -Eeuo pipefail

target="${1:-.}"
if [[ ! -e "$target" ]]; then
  printf 'Error: path does not exist: %s\n' "$target" >&2
  exit 1
fi

printf 'Disk space for filesystem containing %s:\n' "$target"
df -h -- "$target"
printf '\nSize of target:\n'
du -sh -- "$target"
