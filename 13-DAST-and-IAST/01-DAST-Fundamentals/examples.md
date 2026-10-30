# DAST Fundamentals - Examples

> Run these examples only against a local lab or another target for which you have explicit authorization.

## 1. Check that a lab target is reachable
```bash
curl -i http://127.0.0.1:3000/
```
Review the status code, response headers, and body. A successful HTTP response does not mean the application is secure.

## 2. Capture response headers
```bash
curl -sS -D response-headers.txt -o response-body.html \
  http://127.0.0.1:3000/
```
Inspect `response-headers.txt` for headers such as Content-Security-Policy, Strict-Transport-Security (when HTTPS is used), X-Content-Type-Options, and frame-related protections. Header requirements depend on application behavior and deployment architecture.

## 3. Passive baseline scan with ZAP
```bash
zap-baseline.py -t http://127.0.0.1:3000 -r zap-baseline.html
```
The baseline workflow is designed for passive scanning. Review the generated report and verify findings. Consult the current ZAP documentation for installation-specific command names and options.

## 4. Docker invocation pattern
```bash
docker run --rm -t \
  -v "$PWD:/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://host.docker.internal:3000 \
  -J zap-report.json -r zap-report.html
```
The target address must be reachable from inside the scanner container. On Linux, `host.docker.internal` may need explicit host-gateway configuration. An isolated shared Docker network is often more predictable.

## 5. Compare two responses
```bash
curl -sS -D before.headers -o before.body \
  http://127.0.0.1:3000/profile

# After applying a fix:
curl -sS -D after.headers -o after.body \
  http://127.0.0.1:3000/profile

diff -u before.headers after.headers
```
Use a controlled test account and avoid saving real personal information in response files.

## 6. Simple Python response-header review
```python
# examples/header_review.py
from urllib.request import Request, urlopen

TARGET = "http://127.0.0.1:3000/"  # Authorized local lab only

request = Request(TARGET, headers={"User-Agent": "DAST-Learning-Lab/1.0"})
with urlopen(request, timeout=5) as response:
    print("Status:", response.status)
    for name, value in response.headers.items():
        print(f"{name}: {value}")
```
This is a small inspection helper, not a DAST scanner. It does not crawl, authenticate, inject payloads, or validate vulnerabilities.

## 7. Example triage record
```text
Finding: Missing security header
Asset: http://127.0.0.1:3000/
Evidence: Response does not include the expected header
Scanner severity: Informational (example only)
Validation: Confirmed on the tested response
Impact: Depends on application features and threat model
Recommendation: Define and test an appropriate header policy
Status: Open - owner assigned
```

## 8. Example scope definition
```yaml
assessment:
  name: local-training-app
  target: "http://127.0.0.1:3000"
  allowed_hosts:
    - "127.0.0.1"
  included_paths:
    - "/"
    - "/login"
    - "/products"
  excluded_paths:
    - "/logout"
    - "/admin/delete"
  environment: "disposable-local-lab"
  scan_mode: "passive-first"
```
This is an illustrative planning file, not a ZAP configuration schema. Translate scope and exclusions into the scanner's supported context/configuration format.

## 9. Example CI stage (conceptual)
```yaml
name: DAST baseline
on:
  pull_request:

jobs:
  dast:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy isolated test application
        run: |
          docker compose -f compose.test.yml up -d
          # Replace fixed sleep with a health-check loop in real pipelines.

      - name: Run passive DAST
        run: |
          # Invoke a pinned, reviewed ZAP container/action here.
          # Store reports as restricted build artifacts.

      - name: Tear down
        if: always()
        run: docker compose -f compose.test.yml down -v
```
Do not copy a placeholder pipeline into production without implementing deployment readiness, scanner invocation, report retention, and failure handling.
