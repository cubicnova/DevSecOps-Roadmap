#!/usr/bin/env bash
set -Eeuo pipefail

name="${1:-Learner}"
printf 'Hello, %s!\n' "$name"
printf 'Current user: %s\n' "$(id -un)"
printf 'Current directory: %s\n' "$PWD"
