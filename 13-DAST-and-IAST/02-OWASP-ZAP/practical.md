# OWASP ZAP — Practical Labs

## Lab safety rules

- Use OWASP Juice Shop, DVWA, WebGoat, or another intentionally vulnerable local lab.
- Do not scan public websites, school/company systems, or cloud assets without explicit authorization.
- Start with passive/baseline scans. Active scans can alter data and affect availability.
- Use dedicated test credentials and non-production data.
- Keep ZAP's proxy and API bound to localhost or an isolated lab network.

## Lab 1 — Install and launch ZAP

**Tasks**

1. Download and install ZAP using the official download page, or pull the official Docker image.
2. Record the ZAP version.
3. Open the desktop application.
4. Review the Quick Start, Sites, History, and Alerts panels.
5. Record the proxy address and port configured by your installation.

**Deliverables:** version output and a short installation note.

## Lab 2 — Configure browser proxy

**Tasks**

1. Start ZAP.
2. Use the ZAP-launched browser or configure a dedicated test browser to use ZAP's local proxy.
3. Browse your local training application.
4. Locate the HTTP request and response in the History tab.
5. Identify the method, URL, status code, request headers, response headers, and cookies.

**Deliverables:** sanitized request/response notes. Do not include session secrets.

## Lab 3 — Explore the Sites tree and define scope

**Tasks**

1. Browse several pages of the lab application.
2. Inspect the Sites tree.
3. Create a Context for the lab host.
4. Include only the intended host and paths.
5. Identify logout and destructive endpoints that should be excluded from automated crawling or active scanning.
6. Confirm no unrelated host is in scope.

**Deliverables:** context/scope description and an exclusion list.

## Lab 4 — Run a baseline scan

**Tasks**

1. Start the lab application.
2. Run the Docker baseline scan against the local target.
3. Save an HTML report.
4. Record the number of alerts by risk.
5. Pick three alerts and inspect the evidence.
6. Explain why a baseline scan is not a full active penetration test.

**Deliverables:** report and alert-review notes.

## Lab 5 — Traditional Spider and AJAX Spider

**Tasks**

1. Run the traditional Spider against the lab.
2. Record discovered URLs.
3. If the application uses JavaScript-heavy navigation, run the AJAX Spider if available.
4. Compare the discovered endpoints.
5. Identify important routes that were not discovered automatically.
6. Explain how login and client-side routing affect crawl coverage.

**Deliverables:** URL inventory and comparison.

## Lab 6 — Passive versus active scanning

**Tasks**

1. Run passive scanning on observed traffic.
2. Record passive alerts.
3. In a disposable lab only, configure a narrow active scan policy.
4. Run the active scan against the explicitly scoped lab host.
5. Compare alert types and scan duration.
6. Record any operational impact.

**Deliverables:** comparison table and scan-safety notes.

## Lab 7 — Authenticated scanning

**Tasks**

1. Create a dedicated test user in the lab application.
2. Configure a ZAP Context and authentication method.
3. Configure session management.
4. Define a logged-in verification condition.
5. Run the spider as the test user.
6. Verify that protected pages appear in the Sites tree.
7. Confirm that the scan does not log out or modify user data unexpectedly.

**Deliverables:** sanitized authentication configuration and evidence of authenticated coverage. Never submit passwords or session tokens.

## Lab 8 — API scanning

**Tasks**

1. Obtain the OpenAPI definition for a local API.
2. Validate that its server URL points to the lab.
3. Import the definition into ZAP or run the Docker API scan.
4. Review discovered endpoints and methods.
5. Configure a test authentication header if needed.
6. Run a controlled scan and inspect findings.
7. Identify API authorization cases that require manual tests, such as object-level access checks.

**Deliverables:** API endpoint inventory and scan report.

## Lab 9 — Automation Framework

**Tasks**

1. Create a `zap.yaml` plan.
2. Define a Context and include paths.
3. Add a Spider job.
4. Add a passive-scan wait job.
5. Add report generation.
6. Run the plan in the official ZAP Docker image.
7. Review the log and generated report.
8. Intentionally introduce an invalid job parameter and observe the failure.

**Deliverables:** `zap.yaml`, report, and execution notes.

## Lab 10 — CI/CD integration

**Tasks**

1. Create a GitHub Actions workflow for a local test deployment or dedicated staging environment.
2. Start/deploy the application in the workflow.
3. Run a ZAP baseline scan.
4. Retain the generated report as a workflow artifact.
5. Review action logs and exit behavior.
6. Pin third-party actions to reviewed commit SHAs before production use.
7. Document the conditions under which a pipeline should fail.

**Deliverables:** workflow YAML, artifact, and gate policy.

## Lab 11 — Alert triage and false-positive handling

For at least five alerts, document:

- Alert name, risk, and confidence.
- Affected URL and method.
- Evidence and reproduction steps.
- Whether the finding is confirmed, false positive, accepted risk, or needs more investigation.
- Recommended remediation.
- Reviewer and date.

Use an alert filter only after documenting the reason and scope. Do not suppress alerts simply to hide failures.

**Deliverables:** `zap-triage.csv` or a Markdown triage table.

## Lab 12 — Capstone: DAST pipeline

Build an end-to-end DAST workflow for an intentionally vulnerable local application.

Required capabilities:

1. Start the application in a disposable environment.
2. Define the target scope.
3. Run a baseline scan on each pull request or selected branch.
4. Run a controlled active scan on a scheduled or manually approved workflow.
5. Run an API scan if an API definition exists.
6. Preserve HTML/JSON reports as artifacts.
7. Triage findings with risk and confidence.
8. Apply a documented quality gate.
9. Keep credentials in CI secrets.
10. Prevent scanning of out-of-scope hosts.
11. Preserve scanner execution failures separately from vulnerability findings.
12. Clean up containers and test data.

**Deliverables:** workflow, ZAP plan, scan reports, triage records, and a short final assessment.

## Submission checklist

- [ ] ZAP installed and version recorded.
- [ ] Browser traffic successfully proxied.
- [ ] Scope and Context configured.
- [ ] Baseline report generated.
- [ ] Passive and active scanning differences explained.
- [ ] Authentication coverage validated.
- [ ] API definition imported and reviewed.
- [ ] Automation Framework plan executed.
- [ ] CI workflow retains reports.
- [ ] Findings triaged and false positives documented.
- [ ] No credentials or sensitive evidence committed.
- [ ] Only authorized targets were scanned.
