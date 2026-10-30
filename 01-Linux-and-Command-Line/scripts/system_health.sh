#!/usr/bin/env bash
set -Eeuo pipefail

echo "=== System Health Snapshot ==="
printf 'Host: %s\n' "$(hostname)"
printf 'Time: %s\n' "$(date --iso-8601=seconds 2>/dev/null || date)"
printf 'Uptime: '
uptime
printf '\nMemory:\n'
if command -v free >/dev/null 2>&1; then
  free -h
else
  echo "The 'free' utility is not installed."
fi
printf '\nRoot filesystem:\n'
df -h /
printf '\nTop CPU processes (snapshot):\n'
ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -n 6
