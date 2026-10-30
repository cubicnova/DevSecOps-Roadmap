# OWASP ZAP — Practical Examples

> Run these examples only against a local lab or an application for which you have explicit authorization. Use a staging environment for active scans.

## 1. Check Docker and ZAP image

```bash
docker --version
docker pull ghcr.io/zaproxy/zaproxy:stable
docker run --rm ghcr.io/zaproxy/zaproxy:stable zap.sh -version
```

## 2. Run a baseline scan

Start a local training application on port 3000, then run:

```bash
mkdir -p reports

docker run --rm -t \
  -v "$(pwd)/reports:/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
  -t http://host.docker.internal:3000 \
  -m 2 \
  -r zap-baseline.html
```

The baseline scan is designed for passive findings after crawling; it is not equivalent to a full active penetration test.

## 3. Run a full scan in a disposable lab

```bash
docker run --rm -t \
  -v "$(pwd)/reports:/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-full-scan.py \
  -t http://host.docker.internal:3000 \
  -m 5 \
  -r zap-full.html
```

Use a disposable target with resettable data. Review the scan options before using this command; full scans can send intrusive requests.

## 4. Scan an OpenAPI definition

```bash
docker run --rm -t \
  -v "$(pwd)/reports:/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py \
  -t http://host.docker.internal:3000/openapi.json \
  -f openapi \
  -r zap-api.html
```

The API definition must be reachable from inside the container. Confirm that its server URL points only to the authorized test environment.

## 5. Start ZAP in daemon mode

For a local isolated lab:

```bash
docker run --rm -d \
  --name zap-lab \
  -p 127.0.0.1:8080:8080 \
  ghcr.io/zaproxy/zaproxy:stable \
  zap.sh -daemon \
  -host 0.0.0.0 \
  -port 8080 \
  -config api.key=change-this-lab-key
```

The port is bound to loopback on the host. Do not expose an unauthenticated ZAP API to a shared or untrusted network.

Check that the API responds:

```bash
curl "http://127.0.0.1:8080/JSON/core/view/version/?apikey=change-this-lab-key"
```

Stop the container:

```bash
docker stop zap-lab
```

## 6. Example API calls

Replace the API key and target with lab values. URL-encode parameters when they contain special characters.

Check version:

```bash
curl "http://127.0.0.1:8080/JSON/core/view/version/?apikey=change-this-lab-key"
```

Access the Sites tree:

```bash
curl "http://127.0.0.1:8080/JSON/core/view/sites/?apikey=change-this-lab-key"
```

Start a spider scan against a lab target:

```bash
curl "http://127.0.0.1:8080/JSON/spider/action/scan/?url=http%3A%2F%2Fhost.docker.internal%3A3000&apikey=change-this-lab-key"
```

Check spider status using the scan ID returned by the previous request:

```bash
curl "http://127.0.0.1:8080/JSON/spider/view/status/?scanId=0&apikey=change-this-lab-key"
```

Do not start an active scan until the target scope, impact, and authorization have been confirmed.

## 7. Starter Automation Framework plan

Save as `zap.yaml`:

```yaml
env:
  contexts:
    - name: local-training
      urls:
        - http://host.docker.internal:3000
      includePaths:
        - "http://host.docker.internal:3000.*"

jobs:
  - type: spider
    parameters:
      context: local-training
      maxDuration: 2

  - type: passiveScan-wait
    parameters:
      maxDuration: 2

  - type: report
    parameters:
      template: traditional-html
      reportDir: /zap/wrk/reports
      reportFile: zap-automation.html
```

Run it:

```bash
mkdir -p reports

docker run --rm -t \
  -v "$(pwd):/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap.sh -cmd -autorun /zap/wrk/zap.yaml
```

The report template and required add-ons can vary. If the plan fails, inspect the Automation Framework log and installed add-ons.

## 8. GitHub Actions baseline workflow

Save as `.github/workflows/zap-baseline.yml`:

```yaml
name: OWASP ZAP Baseline

on:
  workflow_dispatch:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  zap:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Start/deploy your authorized test application before this step.
      - name: Run ZAP baseline
        uses: zaproxy/action-baseline@v0.14.0
        with:
          target: "http://127.0.0.1:3000"
```

This example assumes the target is already running and reachable from the runner. Add the application startup/deployment steps required by your project. Verify current action inputs and pin the action to a reviewed full commit SHA for production.

## 9. Basic alert review checklist

For each alert, record:

- Alert name and risk.
- Confidence.
- URL, HTTP method, and parameter.
- Evidence and request/response context.
- Reproduction steps in the test environment.
- Business impact.
- Remediation recommendation.
- False-positive decision and reviewer.

Do not copy session cookies, access tokens, passwords, or personal data into a public issue.

## 10. Example Python report inventory

If you export a JSON report from ZAP, this script prints a concise alert inventory. Export format fields can vary by report template and ZAP version; inspect your actual JSON structure first.

```python
import json
from collections import Counter
from pathlib import Path

report = json.loads(Path("zap-report.json").read_text(encoding="utf-8"))
alerts = report.get("site", [])
risk_counts = Counter()

for site in alerts:
    for alert in site.get("alerts", []):
        risk = alert.get("riskdesc", "Unknown")
        risk_counts[risk] += 1
        print(
            risk,
            alert.get("alert", "Unnamed alert"),
            alert.get("url", "No URL")
        )

print("\nSummary")
for risk, count in sorted(risk_counts.items()):
    print(f"{risk}: {count}")
```

## 11. Clean up

```bash
docker ps -a
docker stop zap-lab 2>/dev/null || true
docker rm zap-lab 2>/dev/null || true
```

Remove test accounts and reset the training application's database as required.
