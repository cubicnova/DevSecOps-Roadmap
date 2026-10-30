# DAST in CI/CD - Examples

> Use only on an application you own or are explicitly authorized to test. The examples use local test targets and placeholders. Review action/image versions and pin immutable references before production use.

## 1. Local Docker Compose target
Example `compose.test.yml`:
```yaml
services:
  app:
    image: ghcr.io/juice-shop/juice-shop:latest
    ports:
      - "127.0.0.1:3000:3000"
    healthcheck:
      test: ["CMD", "node", "-e", "fetch('http://127.0.0.1:3000').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"]
      interval: 5s
      timeout: 3s
      retries: 20
```
For repeatable CI, prefer a reviewed immutable image digest instead of `latest`. Confirm the healthcheck command works with the selected image.

## 2. Readiness loop
```bash
#!/usr/bin/env bash
set -euo pipefail

url="${APP_HEALTH_URL:-http://127.0.0.1:3000}"
attempts=30

for ((i=1; i<=attempts; i++)); do
  if curl --fail --silent --show-error "$url" >/dev/null; then
    echo "Application is ready."
    exit 0
  fi
  sleep 2
done

echo "Application did not become ready." >&2
exit 1
```
Use a health endpoint that checks application readiness, not just process existence.

## 3. Run ZAP baseline with Docker
```bash
mkdir -p reports

docker run --rm \
  --network host \
  -v "$PWD/reports:/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
    -t http://127.0.0.1:3000 \
    -r baseline.html \
    -J baseline.json
```
This host-network example is Linux-specific and is not portable to all CI runners. Prefer a dedicated shared container network with service DNS where possible. Pin the image to a reviewed digest in production.

## 4. GitHub Actions baseline workflow
See `workflows/dast-github-actions.yml`. The workflow is a starter example; verify the current ZAP action release, inputs, and immutable commit SHA before using it.

## 5. GitLab CI baseline job
See `workflows/dast-gitlab-ci.yml`. The target URL must be reachable from the scanner job container. Use a runner and network model appropriate for your GitLab deployment.

## 6. Example finding gate policy
```yaml
gate:
  fail_on:
    - validated-critical
    - validated-high
  warn_on:
    - medium
    - low
  require_manual_review:
    - uncertain-confidence
  exceptions:
    require_owner: true
    require_expiry: true
    require_ticket: true
```
This is a conceptual policy file, not a built-in ZAP schema. Implement the evaluation in your pipeline and ensure it uses validated finding data.

## 7. Preserve scan failure
```bash
set -euo pipefail
docker run --rm ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t "$DAST_TARGET" -J reports/baseline.json
```
Do not append `|| true` just to make the pipeline green. If you intentionally collect findings without blocking, capture the exit status, publish the report, and make the policy decision explicit.

## 8. Report artifact hygiene
- Store reports in restricted pipeline artifacts.
- Set a reasonable retention period.
- Avoid including credentials, cookies, or personal data.
- Separate public build logs from restricted security artifacts.
- Record scanner and image versions with each report.
