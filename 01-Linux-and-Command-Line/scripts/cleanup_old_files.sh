#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  echo "Usage: $0 DIRECTORY DAYS [--delete]"
  echo "Default behavior is preview-only. --delete removes regular files older than DAYS."
}

if [[ $# -lt 2 || $# -gt 3 ]]; then
  usage >&2
  exit 2
fi

target=$1
days=$2
mode="${3:---dry-run}"

if [[ ! -d "$target" ]]; then
  printf 'Error: directory does not exist: %s\n' "$target" >&2
  exit 1
fi
if [[ ! "$days" =~ ^[0-9]+$ ]]; then
  echo "Error: DAYS must be a non-negative integer." >&2
  exit 2
fi
if [[ "$mode" != "--dry-run" && "$mode" != "--delete" ]]; then
  usage >&2
  exit 2
fi

target=$(cd -- "$target" && pwd -P)
echo "Target: $target"
echo "Age threshold: $days day(s)"
if [[ "$mode" == "--delete" ]]; then
  echo "Mode: DELETE (review the target and matches carefully)"
else
  echo "Mode: PREVIEW ONLY (no files will be deleted)"
fi

# -xdev prevents crossing into other mounted filesystems.
if [[ "$mode" == "--delete" ]]; then
  find "$target" -xdev -type f -mtime "+$days" -print -delete
else
  find "$target" -xdev -type f -mtime "+$days" -print
fi
