#!/usr/bin/env bash
set -Eeuo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 FILE" >&2
  exit 2
fi

file=$1
if [[ ! -f "$file" ]]; then
  printf 'Error: not a regular file: %s\n' "$file" >&2
  exit 1
fi

printf 'Path: %s\n' "$(realpath -- "$file" 2>/dev/null || printf '%s' "$file")"
printf 'Size: %s bytes\n' "$(wc -c < "$file" | tr -d '[:space:]')"
printf 'Lines: %s\n' "$(wc -l < "$file" | tr -d '[:space:]')"
printf 'Permissions: %s\n' "$(stat -c '%A (%a)' -- "$file" 2>/dev/null || stat -f '%Sp' -- "$file")"
