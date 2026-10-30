# DAST Fundamentals - Practical Exercises

## Lab rules
- Use a local, disposable vulnerable application such as OWASP Juice Shop or WebGoat.
- Keep the target bound to localhost or an isolated lab network.
- Use synthetic accounts and data.
- Obtain explicit authorization before testing any non-local target.
- Start with passive scanning. Do not run active scans on production or public targets.

## Exercise 1 - Prepare the lab
1. Deploy a deliberately vulnerable training application locally.
2. Record its URL, port, version, and startup method.
3. Confirm reachability with `curl -i`.
4. Capture a screenshot or terminal output as evidence.

**Deliverable:** Lab setup notes and target ownership/authorization statement.

## Exercise 2 - Define scope
1. List the in-scope host and paths.
2. Identify logout, delete, payment, email, and other state-changing routes to exclude.
3. Document the allowed scan window and rate limits.
4. Explain how the scope prevents accidental testing of unrelated systems.

**Deliverable:** Completed `templates/scope-record.md`.

## Exercise 3 - Baseline response review
1. Fetch the home page with `curl -i`.
2. Save headers and body.
3. Identify server disclosure, cookies, cache directives, and security headers.
4. Explain which observations require further investigation.

**Deliverable:** Header review table.

## Exercise 4 - Run a passive baseline
1. Start ZAP.
2. Use its baseline scan against the local lab.
3. Export HTML and JSON reports.
4. Record scan duration, discovered URLs, warnings, and errors.

**Deliverable:** Reports plus a short scan summary.

## Exercise 5 - Explore the application
1. Browse the lab manually through common workflows.
2. Compare manually visited pages with crawler-discovered URLs.
3. Identify routes that the crawler missed.
4. Explain whether JavaScript routing or authentication contributed to the gap.

**Deliverable:** Coverage-gap list.

## Exercise 6 - Authentication coverage
1. Create a dedicated low-privilege test account.
2. Configure the scanner context using current ZAP documentation.
3. Verify the scanner can reach one protected page.
4. Check whether session expiry or logout affects the scan.

**Deliverable:** Authentication test notes. Do not include passwords or tokens.

## Exercise 7 - API discovery
1. Locate the lab's OpenAPI/Swagger definition if available.
2. Import it using the scanner's supported API import feature.
3. Compare imported endpoints with crawler-discovered endpoints.
4. Note endpoints requiring authentication or specific request bodies.

**Deliverable:** API coverage comparison.

## Exercise 8 - Alert triage
1. Select three alerts from the passive report.
2. Read each alert's description, evidence, URL, and request/response.
3. Decide whether each is confirmed, likely, false positive, or needs more testing.
4. Explain the evidence for each decision.

**Deliverable:** Three completed triage records.

## Exercise 9 - Retest a remediation
1. Choose a safe, reproducible finding in the lab.
2. Apply a documented configuration or code fix.
3. Repeat the same request and scan.
4. Compare the evidence before and after the change.

**Deliverable:** Before/after retest record.

## Exercise 10 - Scan policy design
Create a policy for a disposable test environment:
- Included hosts and paths.
- Excluded destructive endpoints.
- Passive checks enabled.
- Active checks requiring approval.
- Request rate and time limit.
- Authentication roles.
- Report handling and cleanup.

**Deliverable:** A one-page scan policy.

## Exercise 11 - CI/CD design
Draw a pipeline that deploys a disposable preview environment, waits for health, runs a passive baseline scan, stores a restricted report, evaluates policy, and always tears down the environment.

**Deliverable:** Pipeline diagram or YAML pseudocode.

## Exercise 12 - DAST limitations
For a sample web application, list five scenarios that automated crawling may miss, including one business-logic issue, one role-specific route, and one multi-step workflow.

**Deliverable:** Coverage and residual-risk statement.

## Exercise 13 - Final mini assessment
Prepare a short report containing:
1. Scope and authorization.
2. Environment and test accounts.
3. Scanner/version and configuration.
4. URLs and roles covered.
5. Findings and evidence.
6. False-positive decisions.
7. Limitations and excluded tests.
8. Remediation recommendations.
9. Retest status.

**Evaluation rubric (100 points)**
| Area | Points |
|---|---:|
| Safe lab setup and authorization | 15 |
| Scope and exclusions | 15 |
| Correct passive scan execution | 15 |
| Coverage and authentication analysis | 15 |
| Alert validation and evidence | 20 |
| Remediation and retest | 10 |
| Clear reporting | 10 |
