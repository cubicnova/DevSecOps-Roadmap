# OWASP ZAP (Zed Attack Proxy)

## Learning objectives

By completing this module, you should be able to:

- Explain the role of OWASP ZAP in Dynamic Application Security Testing (DAST).
- Configure ZAP as an intercepting proxy and inspect HTTP requests and responses.
- Understand sites, contexts, scope, sessions, spiders, passive scanning, and active scanning.
- Run baseline, full, and API scans with Docker.
- Configure repeatable scans with the ZAP Automation Framework.
- Test authenticated applications and APIs safely.
- Interpret alerts, manage false positives, and generate reports.
- Integrate ZAP into GitHub Actions and other CI/CD pipelines.

> **Authorization requirement:** Only scan applications you own or have explicit written permission to test. Active scanning sends attack-like requests and may change data, trigger alerts, or affect service availability. Use a local training application for labs.

## 1. Introduction to DAST

Dynamic Application Security Testing evaluates a running application from the outside. A DAST tool sends HTTP requests, observes responses, and identifies indicators of security weaknesses.

Unlike SAST, which analyzes source code, DAST tests the behavior of a deployed application. It can identify issues that depend on runtime configuration, routing, headers, server behavior, and application responses. DAST does not prove that an application is free of vulnerabilities; findings require validation.

## 2. What is OWASP ZAP?

OWASP ZAP (Zed Attack Proxy) is a free, open-source web application security testing tool. It can act as an intercepting proxy between a browser and a target application. ZAP provides:

- Manual request and response inspection.
- Traditional and AJAX crawling.
- Passive scanning of observed traffic.
- Active scanning with configurable rules and policies.
- Contexts, authentication, users, and session handling.
- API testing using OpenAPI, SOAP, and GraphQL support through add-ons.
- Automation Framework, Docker packaged scans, and REST API.
- HTML, JSON, and other report formats through report add-ons.

## 3. Installation and first launch

Download ZAP from the official website and select the package appropriate for your operating system:

- [ZAP downloads](https://www.zaproxy.org/download/)
- [ZAP documentation](https://www.zaproxy.org/docs/)

On Linux, launch the installed package using its provided launcher, commonly `zap.sh`. On Windows, use the installer or provided executable. Keep ZAP and its add-ons updated in accordance with your organization's change-management process.

For a Docker-based environment:

```bash
docker pull ghcr.io/zaproxy/zaproxy:stable
docker run --rm ghcr.io/zaproxy/zaproxy:stable zap.sh -version
```

Use a pinned image version or digest in repeatable production pipelines rather than relying indefinitely on a moving tag.

## 4. ZAP as an intercepting proxy

A proxy receives browser requests and forwards them to the target. ZAP can inspect and modify requests and responses while testing.

Typical workflow:

1. Start ZAP.
2. Use the browser configured by ZAP or configure a dedicated test browser to use ZAP's proxy listener.
3. Browse only the authorized target.
4. Inspect requests, responses, cookies, headers, and parameters.
5. Send selected requests to manual testing tools.
6. Review alerts and validate findings.

Do not expose the ZAP proxy or API listener to untrusted networks. Use a dedicated testing profile and avoid browsing personal accounts through an interception proxy.

## 5. Sites, contexts, and scope

The Sites tree organizes hosts and paths observed by ZAP. A Context groups URLs and can hold authentication, session, and technology settings. Scope controls which URLs are considered in-scope for a particular test.

Before scanning:

- Define the exact scheme, host, and permitted paths.
- Exclude logout, destructive, payment, email, and other sensitive operations unless explicitly approved.
- Identify test accounts and test data.
- Confirm that redirects do not take the scan outside the authorized scope.
- Set request-rate and time limits appropriate to the environment.

## 6. Spidering and crawling

The traditional Spider discovers links and resources by parsing application responses. The AJAX Spider uses a browser to explore JavaScript-heavy applications. Newer client-side crawling capabilities may also be available depending on installed add-ons and ZAP version.

Crawling helps discover the application's attack surface; it is not itself proof that discovered endpoints are vulnerable.

Consider:
- Whether the application requires authentication.
- Whether important pages are reachable only through workflows.
- Whether client-side routing is used.
- Whether robots, rate limits, and test-data constraints apply.
- Whether the scan is accidentally discovering external hosts.

## 7. Passive and active scanning

### Passive scanning

Passive rules inspect requests and responses that ZAP has already observed. They do not intentionally modify requests to exploit a suspected issue. Examples include checking for missing security headers, cookie attributes, and information disclosure patterns.

### Active scanning

Active rules send additional crafted requests to test for weaknesses such as injection and path traversal. Active scanning can be intrusive. Run it only against explicitly authorized targets, preferably in a staging environment with backups and test data.

A useful progression is:

1. Baseline passive scan.
2. Review crawl coverage and passive alerts.
3. Configure authentication and scan scope.
4. Run a controlled active scan with an appropriate policy.
5. Manually validate important findings.

## 8. Docker packaged scans

ZAP's Docker images include packaged scan scripts.

### Baseline scan

A time-limited spider followed by passive analysis. It is a useful starting point for CI and is less intrusive than a full active scan.

```bash
mkdir -p reports
docker run --rm -t \
  -v "$(pwd)/reports:/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://host.docker.internal:3000 \
  -r zap-baseline.html
```

Container-to-host addressing differs by operating system and Docker configuration. On Linux, you may need an explicit host-gateway mapping or a shared Docker network. Never assume `host.docker.internal` is available in every environment.

### Full scan

The full scan includes crawling and active scanning. It can take longer and may affect the target.

```bash
docker run --rm -t \
  -v "$(pwd)/reports:/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-full-scan.py -t http://host.docker.internal:3000 \
  -r zap-full.html
```

### API scan

Use the API scan for an authorized API described by OpenAPI/Swagger or supported GraphQL input:

```bash
docker run --rm -t \
  -v "$(pwd)/reports:/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t http://host.docker.internal:3000/openapi.json \
  -f openapi -r zap-api.html
```

Confirm the input format and script options against the installed image's documentation. The exact API definition URL must be reachable from inside the container.

## 9. Automation Framework

The Automation Framework controls ZAP using a YAML plan. It is suitable for repeatable scans and can define environments, contexts, authentication, spiders, passive-scan waits, active scans, tests, and reports.

Example starter plan:

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

Run the plan:

```bash
docker run --rm -t \
  -v "$(pwd):/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap.sh -cmd -autorun /zap/wrk/zap.yaml
```

Validate job names and parameters against the current Automation Framework documentation and installed add-ons. The framework's exit status can represent plan errors or warnings; configure explicit tests and exit-status behavior for your pipeline policy.

## 10. Authentication testing

Many important application areas are available only after login. ZAP supports contexts and several authentication approaches, including form-based, script-based, HTTP, and browser-based methods depending on configuration and add-ons.

A reliable authenticated scan requires:

- A dedicated least-privilege test account.
- A defined login flow.
- Session management configuration.
- A verification mechanism that detects when the user is logged out.
- A safe logout strategy and test-data reset.
- Confirmation that scan requests are actually authenticated.

Never commit usernames, passwords, API keys, cookies, or bearer tokens to a repository. Inject secrets using the CI platform's secret store and avoid printing them in logs.

## 11. API testing

ZAP can import API definitions and scan discovered operations. For OpenAPI:

1. Obtain an approved OpenAPI document.
2. Confirm its server URLs point to the test environment.
3. Import the definition into ZAP.
4. Review the discovered endpoints and methods.
5. Configure authentication and headers.
6. Run passive analysis and a controlled active scan.
7. Validate authorization behavior separately, especially object-level access control.

An API definition helps discover endpoints but does not guarantee complete coverage or correct authorization testing.

## 12. Alerts, risk, and false positives

A ZAP alert commonly contains:

- Alert name and risk.
- Confidence.
- URL and method.
- Parameter or evidence.
- Description and solution.
- Reference links and tags.
- Instances and request/response evidence.

Risk is not the same as confidence. A high-risk alert with low confidence still needs investigation. Validate the affected endpoint, reproduce safely, identify business impact, and record evidence without exposing sensitive data.

For false positives:
1. Reproduce the behavior.
2. Review the rule and evidence.
3. Determine whether the issue is absent, mitigated, or out of scope.
4. Use a documented alert filter or suppression mechanism.
5. Record the rationale, owner, and review date.
6. Reassess exclusions when the application changes.

Do not suppress an alert merely to make a pipeline green.

## 13. CI/CD integration

A practical DAST pipeline can run a baseline scan against a deployed test environment, retain reports, and apply a documented policy. Example GitHub Actions outline:

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

      # Deploy or start the application in a controlled test environment here.

      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.14.0
        with:
          target: "http://127.0.0.1:3000"
          artifact_name: "zap-baseline-report"
```

This is an illustrative workflow: verify the maintained action version, inputs, target reachability, and report behavior before use. Pin actions to reviewed full commit SHAs in production. Do not run active scans against production by default.

## 14. Troubleshooting

| Symptom | Possible cause | Check |
|---|---|---|
| ZAP cannot reach target | Wrong URL, DNS, TLS, or container networking | Test connectivity from the ZAP container |
| No endpoints discovered | Login required, JS-heavy app, or crawl limits | Configure context/authentication and AJAX crawling |
| Alerts are missing | Traffic not proxied or passive queue incomplete | Verify proxy traffic and wait for passive scan |
| Active scan is disruptive | Aggressive policy or unsafe target | Stop scan; use staging and tune policy |
| Authenticated pages appear logged out | Session expiry or incorrect verification | Review authentication and session management |
| API scan finds no endpoints | Invalid or inaccessible API definition | Validate OpenAPI document and server URL |
| CI report missing | Wrong path or scan terminated early | Inspect action logs and mounted report directory |
| API listener is exposed | Unsafe bind/network configuration | Restrict listener and require an API key |

## 15. Knowledge check

1. What is the difference between SAST and DAST?
2. How does ZAP act as an intercepting proxy?
3. What is the difference between passive and active scanning?
4. Why should active scans be run in a controlled environment?
5. What are ZAP contexts used for?
6. Why is authenticated scanning important?
7. What does a baseline scan do?
8. What is the purpose of the Automation Framework?
9. How do risk and confidence differ?
10. Why should false-positive suppressions be documented?

## References

- [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)
- [ZAP Getting Started](https://www.zaproxy.org/getting-started/)
- [ZAP Docker Documentation](https://www.zaproxy.org/docs/docker/)
- [ZAP Automation Framework](https://www.zaproxy.org/docs/automate/automation-framework/)
- [ZAP API Documentation](https://www.zaproxy.org/docs/api/)
- [OWASP DevSecOps Guideline — DAST](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-4-Test/2-4-2-Dynamic-Application-Security-Testing/)
