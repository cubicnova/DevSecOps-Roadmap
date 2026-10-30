#!/usr/bin/env bash
set -Eeuo pipefail

username="${1:-}"
if [[ -z "$username" ]]; then
  echo "Usage: $0 USERNAME" >&2
  exit 2
fi

# Example policy: 3–32 characters; starts with a letter or underscore;
# remaining characters may be letters, digits, underscores, or hyphens.
if [[ "$username" =~ ^[a-zA-Z_][a-zA-Z0-9_-]{2,31}$ ]]; then
  printf 'Username format accepted: %s\n' "$username"
else
  echo "Invalid username format." >&2
  echo "Use 3–32 characters, start with a letter or underscore, and use only letters, digits, _ or -." >&2
  exit 1
fi
