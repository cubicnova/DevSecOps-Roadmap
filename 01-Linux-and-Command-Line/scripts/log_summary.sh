#!/usr/bin/env bash
set -Eeuo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 LOG_FILE" >&2
  exit 2
fi

log_file=$1
if [[ ! -r "$log_file" || ! -f "$log_file" ]]; then
  printf 'Error: file is not readable or is not a regular file: %s\n' "$log_file" >&2
  exit 1
fi

printf 'Log summary for: %s\n' "$log_file"
printf 'Total lines: '
wc -l < "$log_file"
printf 'ERROR matches: '
grep -Eic 'error|fatal|critical' "$log_file" || true
printf 'WARNING matches: '
grep -Eic 'warn(ing)?' "$log_file" || true
printf 'INFO matches: '
grep -Eic 'info' "$log_file" || true

printf '\nRecent matching problem lines (up to 10):\n'
grep -Ein 'error|fatal|critical|warn(ing)?' "$log_file" | tail -n 10 || true
