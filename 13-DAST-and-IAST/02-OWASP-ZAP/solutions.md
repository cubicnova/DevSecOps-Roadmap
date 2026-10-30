# OWASP ZAP — Lab Solutions and Reference Answers

These are reference approaches. ZAP add-ons, UI labels, command options, and GitHub Action inputs can change. Confirm them against the documentation for the version installed in your lab.

## Solution 1 — Install and launch

Use the official ZAP download page or official Docker image:

```bash
docker pull ghcr.io/zaproxy/zaproxy:stable
docker run --rm ghcr.io/zaproxy/zaproxy:stable zap.sh -version
```

Record the exact version and image digest used. A moving `stable` tag is convenient for learning but a pinned version/digest is more reproducible in CI.

## Solution 2 — Browser proxy

A typical local ZAP proxy listener uses `127.0.0.1` and a configured port (often `8080`, depending on installation). Configure only a dedicated testing browser profile.

Verify:
- Browser requests appear in ZAP History.
- The target host appears in the Sites tree.
- Request and response details are visible.
- HTTPS interception is configured only for the test profile and lab.

Never export or submit raw authenticated requests containing cookies or bearer tokens.

## Solution 3 — Context and scope

A good Context should include only the authorized application origin and permitted paths. For example, a local lab might include:

```text
http://127.0.0.1:3000.*
```

The exact regex must match the intended host and path set. Exclude destructive or out-of-scope routes, and verify redirects do not send the scan to a third-party domain.

## Solution 4 — Baseline scan

```bash
mkdir -p reports

docker run --rm -t \
  -v "$(pwd)/reports:/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
  -t http://host.docker.internal:3000 \
  -r zap-baseline.html
```

The baseline scan crawls the target and reports passive scan alerts. It is useful for repeatable low-impact checks, but it does not replace an active scan or manual penetration test. Confirm container-to-host networking for your OS.

## Solution 5 — Spider comparison

The traditional Spider discovers links from responses and markup. The AJAX Spider uses a browser to interact with JavaScript-heavy pages. Compare the URL lists and note routes that require authentication, user interaction, or specific application state.

A crawler's discovered URL count is not a reliable measure of complete security coverage.

## Solution 6 — Passive and active scanning

| Passive scan | Active scan |
|---|---|
| Analyzes observed requests/responses | Sends additional crafted requests |
| Generally lower impact | Can be intrusive |
| Useful for headers, cookies, and disclosure clues | Tests suspected weaknesses with attack-like input |
| Does not prove exploitability | May change data or affect availability |

Use a disposable environment and narrow policy for active testing.

## Solution 7 — Authenticated scanning

Reference sequence:

1. Create a dedicated low-privilege test account.
2. Define a Context containing only the lab.
3. Configure the correct authentication method.
4. Configure session management.
5. Define a logged-in verification check.
6. Configure a Context user.
7. Run the Spider using that user.
8. Inspect the Sites tree and verify protected pages were discovered.

If the scan is unauthenticated, review login URL, credentials injection, CSRF requirements, session cookies, and logged-in verification. Avoid hardcoding secrets in `zap.yaml`.

## Solution 8 — API scan

For an OpenAPI document:

```bash
docker run --rm -t \
  -v "$(pwd)/reports:/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py \
  -t http://host.docker.internal:3000/openapi.json \
  -f openapi \
  -r zap-api.html
```

Check that:
- The document is valid and reachable from the container.
- Server URLs resolve to the authorized lab.
- Authentication is configured where required.
- Destructive methods are safe for the test data.
- API authorization is separately tested, including object-level access control.

## Solution 9 — Automation Framework

Example plan:

```yaml
env:
  contexts:
    - name: training
      urls:
        - http://host.docker.internal:3000
      includePaths:
        - "http://host.docker.internal:3000.*"

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
      reportDir: /zap/wrk/reports
      reportFile: zap-report.html
```

Run:

```bash
mkdir -p reports
docker run --rm -t \
  -v "$(pwd):/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap.sh -cmd -autorun /zap/wrk/zap.yaml
```

If the plan fails, inspect the ZAP log, validate YAML indentation, confirm job names and parameters, and check that required add-ons are installed.

## Solution 10 — CI/CD integration

A workflow outline:

```yaml
name: ZAP Baseline DAST
on:
  workflow_dispatch:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  dast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Start or deploy the authorized test app here.

      - name: ZAP baseline
        uses: zaproxy/action-baseline@v0.14.0
        with:
          target: "http://127.0.0.1:3000"
```

The workflow must start the application or deploy it before the scan. Confirm that the target is reachable from the runner and that the action's current inputs and report artifact behavior match your version. Pin actions to full commit SHAs in production.

## Solution 11 — Triage example

| Field | Example entry |
|---|---|
| Alert | Missing anti-clickjacking header |
| Risk | Medium (example only; use actual ZAP output) |
| Confidence | Medium |
| Affected endpoint | `/account/profile` |
| Evidence | Response lacks the expected framing protection |
| Validation | Confirm response headers and whether framing is possible |
| Remediation | Configure CSP `frame-ancestors` and/or appropriate frame protection |
| Status | Needs validation |
| Owner | Application team |
| Review date | Record actual date |

A false positive should have reproducible reasoning, a reviewer, and a review date. Use the alert filter mechanism supported by your ZAP version rather than deleting evidence from the original report.

## Solution 12 — Capstone architecture

```text
Pull request / approved trigger
             |
             v
      Build test application
             |
             v
      Deploy isolated target
             |
             v
      Validate target scope
             |
             v
      ZAP baseline scan
             |
             +------> Save report artifact
             |
             v
      Parse and triage findings
             |
             v
      Apply documented quality gate
             |
             v
      Clean up test environment
```

For a scheduled or manually approved deeper test, add a controlled active scan and API scan. Keep the scanner's execution status separate from the findings policy: a failed scanner must not be interpreted as a clean application.

## Suggested quality-gate policy

An example policy for a training repository:

- Fail if the scanner cannot start, the target is unreachable, or the report is missing.
- Fail if a validated high-risk finding is present.
- Require manual review for medium-risk findings.
- Track low-risk and informational findings.
- Permit suppression only with documented rationale, owner, scope, and expiry/review date.
- Re-run the scan after remediation.

The thresholds are an example; select risk tolerances with the application owner and security team.

## Further reading

- [ZAP Docker scans](https://www.zaproxy.org/docs/docker/)
- [ZAP Automation Framework](https://www.zaproxy.org/docs/automate/automation-framework/)
- [ZAP API](https://www.zaproxy.org/docs/api/)
- [OWASP DevSecOps Guideline — DAST](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-4-Test/2-4-2-Dynamic-Application-Security-Testing/)
