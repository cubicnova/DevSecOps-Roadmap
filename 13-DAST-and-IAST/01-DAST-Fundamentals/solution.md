# DAST Fundamentals - Solutions and Guidance

These are model answers. Actual findings depend on the lab application, scanner version, configuration, and environment.

## Exercise 1 - Prepare the lab
A suitable answer identifies a deliberately vulnerable training application, records its version and local URL, confirms it responds, and demonstrates that the scanner can reach it. The target should not be exposed publicly. Use synthetic data and isolate the environment.

## Exercise 2 - Define scope
A good scope names the exact host, protocol, port, paths, test accounts/roles, scan window, request limits, and exclusions. Exclude state-changing endpoints such as account deletion, logout, payment, email dispatch, and administrative actions unless a specific test requires them and safeguards are in place.

## Exercise 3 - Baseline response review
Example command:
```bash
curl -sS -D headers.txt -o body.html http://127.0.0.1:3000/
```
Review headers such as `Content-Security-Policy`, `X-Content-Type-Options`, `Strict-Transport-Security` (for HTTPS deployments), and cookie attributes such as `Secure`, `HttpOnly`, and `SameSite`. Do not assume every header is appropriate in every application; document context and verify behavior.

## Exercise 4 - Passive baseline
A correct workflow records scanner version, target, start/end time, discovered URLs, warnings, and report filenames. Passive checks inspect observed traffic; they do not intentionally inject attack payloads. A passive scan can still create load and reports may contain sensitive URLs or response data, so protect the artifacts.

## Exercise 5 - Explore the application
Common crawler gaps include JavaScript-only routes, pages behind login, links requiring a particular state, routes loaded only after user interaction, and endpoints not linked from the UI. Record manual routes and explain which discovery method could improve coverage.

## Exercise 6 - Authentication coverage
Use a dedicated test account with only the permissions needed. Configure a supported ZAP authentication method and session verification mechanism. Confirm a protected endpoint returns authenticated content during the scan. Never commit credentials, cookies, or bearer tokens to source control.

## Exercise 7 - API discovery
Importing an OpenAPI definition can reveal routes and methods that a crawler cannot discover from links. Compare the endpoint list, identify protected operations, and note that a schema does not guarantee every request is valid or every business rule is tested.

## Exercise 8 - Alert triage
For each alert:
1. Confirm the affected asset and request.
2. Reproduce in the authorized lab.
3. Determine whether the evidence demonstrates the reported weakness.
4. Evaluate impact in the application context.
5. Record a reasoned disposition.

Do not dismiss an alert only because the scanner labels it low confidence. Equally, do not report it as confirmed solely because it appears in a report.

## Exercise 9 - Remediation and retest
Keep the original request and evidence. Apply the fix, repeat the same request under the same role and state, and verify the unsafe behavior is gone. Add regression tests where possible. A clean scan alone is not sufficient if the relevant endpoint was no longer reached.

## Exercise 10 - Scan policy
A strong policy defines:
- Exact allowlisted hosts and paths.
- Explicit exclusions for destructive or external integrations.
- Passive-first operation.
- Approval and isolation requirements for active tests.
- Dedicated test identities and least privilege.
- Rate limits, timeouts, and maintenance window.
- Report access control, retention, and cleanup.
- Escalation and stop conditions.

## Exercise 11 - CI/CD design
A robust pipeline should:
1. Build and deploy an ephemeral application instance.
2. Wait for a real health check, not an arbitrary fixed delay.
3. Run a pinned scanner image/action and a bounded passive scan.
4. Store reports as access-controlled artifacts.
5. Apply a reviewed policy to new or selected findings.
6. Preserve scan failure as failure (do not treat timeout as success).
7. Tear down the environment in an unconditional cleanup step.

## Exercise 12 - DAST limitations
Examples:
- A transfer workflow that requires a sequence of valid state transitions.
- A route accessible only to a second role.
- An endpoint not linked in the UI.
- A race condition requiring concurrent requests.
- A flaw whose impact is visible only through a second tenant or external system.

Manual testing and targeted test scripts complement automated scanning.

## Exercise 13 - Final report checklist
A complete report makes clear what was tested and what was not. It includes evidence, severity rationale, confidence, business impact, remediation, owner, and retest result. It avoids exposing passwords, session tokens, personal data, or unnecessary production details.

## Sample short report summary
> A passive DAST baseline was performed against the authorized local training application. The scan discovered the public routes reachable during the test and generated a report for manual triage. Authentication coverage was limited to the configured test role. Findings were reviewed against their request/response evidence; scanner severity was treated as an initial signal rather than a confirmed risk rating. Active scanning and destructive workflows were excluded. Additional authenticated and API testing is recommended before claiming full coverage.
