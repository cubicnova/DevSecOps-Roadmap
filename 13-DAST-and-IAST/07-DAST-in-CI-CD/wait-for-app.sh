#!/usr/bin/env bash
set -euo pipefail

url="${APP_HEALTH_URL:-http://127.0.0.1:3000/}"
attempts="${APP_HEALTH_ATTEMPTS:-30}"
delay="${APP_HEALTH_DELAY_SECONDS:-2}"

for ((i = 1; i <= attempts; i++)); do
  if curl --fail --silent --show-error "$url" >/dev/null; then
    echo "Application is ready at $url"
    exit 0
  fi
  echo "Waiting for application ($i/$attempts)..."
  sleep "$delay"
done

echo "Application did not become ready: $url" >&2
exit 1
