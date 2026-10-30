# Scan Configuration - Examples

> Use these examples only with a local disposable application or an explicitly authorized target. Confirm the syntax against the installed ZAP version.

## 1. Scope regex test
Example local-lab include pattern:
```regex
^http://127\.0\.0\.1:8080/.*$
```
This matches URLs on the local lab host and port. It does not match another hostname or port. ZAP Context patterns are matched against the whole URL, so test expected matches and non-matches.

## 2. Scope planning file
```yaml
assessment:
  name: local-training-app
  target: "http://127.0.0.1:8080"
  included_paths:
    - "/"
    - "/login"
    - "/catalog/.*"
  excluded_paths:
    - "/logout"
    - "/account/delete"
    - "/admin/delete/.*"
  environment: "disposable-local-lab"
  scan_profile: "passive-baseline"
```
This is a human-readable planning example, not a native ZAP configuration schema.

## 3. Passive-first Automation Framework plan
```yaml
env:
  contexts:
    - name: training
      urls:
        - http://127.0.0.1:8080
      includePaths:
        - "http://127\\.0\\.0\\.1:8080/.*"
      excludePaths:
        - "http://127\\.0\\.0\\.1:8080/logout.*"

jobs:
  - type: spider
    parameters:
      context: training
      maxDuration: 2

  - type: passiveScan-wait
    parameters:
      maxDuration: 2

  - type: report
    parameters:
      template: traditional-html
      reportDir: /zap/wrk
      reportFile: baseline.html
```
Automation Framework schemas and report templates can change; validate against the current documentation and installed add-ons.

## 4. Run a baseline scan with Docker
```bash
docker run --rm -t \
  -v "$PWD:/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://host.docker.internal:8080 \
  -r baseline.html
```
The target must be reachable from inside the container. On Linux, configure the host gateway or use a shared isolated Docker network if `host.docker.internal` is unavailable. Review the ZAP Docker documentation for current image tags and command options.

## 5. Example policy decision record
```text
Policy: training-medium
Target: disposable local application
Scope: one approved host
Passive checks: enabled
Active checks: approval required; not run by default
Threshold: Medium (illustrative)
Strength: Low for initial validation
Concurrency: conservative
Maximum duration: 15 minutes
Excluded: logout, delete, payment, external integrations
Rationale: establish safe baseline before targeted active tests
```
Threshold and strength labels are policy choices; configure them in ZAP rather than assuming this text applies them.

## 6. Compare scan summaries
```python
# examples/compare_alert_counts.py
import json
import sys
from collections import Counter

def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)

def summarize(report):
    counts = Counter()
    # ZAP JSON report layouts can differ by report template/version.
    # Adapt this extraction to the exact report schema you export.
    for site in report.get("site", []):
        for alert in site.get("alerts", []):
            counts[alert.get("riskdesc", "Unknown")] += 1
    return counts

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python compare_alert_counts.py old.json new.json")
    old, new = map(load, sys.argv[1:])
    print("Previous:", dict(summarize(old)))
    print("Current: ", dict(summarize(new)))
```
This is an educational starting point. Confirm the report JSON structure before relying on the output. Counts are not a substitute for alert-instance triage.

## 7. Illustrative CI profile separation
```yaml
name: DAST baseline
on:
  pull_request:

jobs:
  baseline:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy isolated preview app
        run: docker compose -f compose.test.yml up -d

      - name: Run passive baseline
        run: |
          # Invoke a pinned ZAP image/action and the reviewed baseline profile.
          # Publish the report as a restricted artifact.

      - name: Cleanup
        if: always()
        run: docker compose -f compose.test.yml down -v
```
This is pseudocode. Implement health checks, scanner invocation, report handling, and failure propagation before use.
