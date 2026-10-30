# Remediation and Verification — Practical Exercises

## Lab safety
Use a deliberately vulnerable application or local project that you own. Do not test public or production systems without explicit authorization.

Suggested tools: OWASP ZAP or Burp Suite for authorized request replay, browser developer tools, pytest or the application's test framework, Git, and a ticket tracker.

## Exercise 1 — Create a remediation ticket
Finding: `GET /api/orders/{orderId}` allows one authenticated test user to retrieve another test account's order.

Create a ticket with summary, impact, preconditions, reproduction steps, root-cause hypothesis, fix recommendation, acceptance criteria, regression tests, owner, and due date.

**Deliverable:** `remediation-ticket.md`

## Exercise 2 — Fix SQL injection
In a local toy application:
1. Locate string concatenation used to build SQL.
2. Replace it with parameter binding.
3. Add tests for normal input and quote-containing input.
4. Add a benign injection regression test.
5. Confirm query structure and expected behavior remain unchanged.

**Deliverable:** code diff and test output.

## Exercise 3 — Verify object-level authorization
1. Create two test users in separate tenants and one record per tenant.
2. Confirm each user can access their own record.
3. Attempt cross-tenant read and update.
4. Implement tenant-scoped server-side authorization.
5. Add allowed and denied automated tests.
6. Confirm sensitive fields are not returned on denial.

**Deliverable:** authorization tests and sanitized evidence.

## Exercise 4 — Remediate XSS
1. Identify the output context: HTML text, attribute, URL, JavaScript, or CSS.
2. Replace unsafe DOM insertion with safe APIs or context-aware encoding.
3. Test harmless markup-like text.
4. Check reflected, stored, and DOM-based paths where relevant.
5. Confirm legitimate content still renders correctly.

**Deliverable:** code diff and test output.

## Exercise 5 — Verify path traversal protection
Use harmless files created for the lab.
1. Trace how the requested filename becomes a filesystem path.
2. Prefer an opaque ID-to-file mapping or implement canonical containment.
3. Test a valid file.
4. Test traversal-like path variants locally.
5. Confirm access stays inside the approved directory.
6. Consider symlink and platform-specific behavior.

**Deliverable:** test matrix.

## Exercise 6 — Design SSRF remediation
For a feature that fetches a URL:
1. Document the business requirement and allowed destinations.
2. Prefer an allowlist or server-side destination identifier.
3. Define scheme, host, port, DNS, redirect, and IP-range checks.
4. Propose network egress restrictions.
5. Verify using local mock services only.

Do not probe cloud metadata endpoints or third-party systems.

**Deliverable:** control design and test matrix.

## Exercise 7 — Retest the original DAST finding
1. Record build and environment.
2. Replay the original sanitized request.
3. Test relevant parameter and encoding variations.
4. Confirm the endpoint was reached and the intended control executed.
5. Capture sanitized evidence.
6. Classify as Fixed, Partially Fixed, Not Fixed, or Unable to Verify.

**Deliverable:** retest report.

## Exercise 8 — Add regression tests
For one fixed weakness:
1. Write a test for secure behavior.
2. Write a negative test for the formerly vulnerable behavior.
3. Include a valid business-flow test.
4. Confirm tests fail against the vulnerable version and pass against the fixed version.

**Deliverable:** test file and run output.

## Exercise 9 — Build an evidence package
Include finding summary, original and post-fix sanitized requests, response excerpts, build identifier, regression output, and retest conclusion. Remove credentials, cookies, API keys, and personal/customer data.

**Deliverable:** evidence folder and explanatory README.

## Exercise 10 — Integrate checks into CI
Create a pipeline stage that installs dependencies, runs unit and integration/security regression tests, publishes results, and fails when required tests fail. Use a dedicated test target for DAST; do not expose production secrets to untrusted pull-request workflows.

**Deliverable:** CI YAML and sample run.

## Exercise 11 — Define a closure policy
Specify who can mark findings ready for retest, who verifies, required evidence, when independent retesting is required, how partial fixes are tracked, how risk acceptance is approved/reviewed, and how reopened findings are handled.

**Deliverable:** `closure-policy.md`

## Exercise 12 — Calculate remediation metrics
Use at least ten fictional findings. Calculate remediation time, open-finding age, SLA compliance, retest pass rate, and reopen rate. Explain severity differences, paused tickets, and scope changes.

**Deliverable:** CSV or Markdown report and interpretation.

## Exercise 13 — Test related attack surfaces
For a shared authorization helper:
1. Inventory all routes that use it.
2. Test read, create, update, delete, and export operations where applicable.
3. Include different roles and tenant boundaries.
4. Record endpoints that could not be verified.

**Deliverable:** endpoint coverage matrix.

## Exercise 14 — Final verification report
Present the original behavior and impact, root cause, code/configuration change, automated tests, original DAST retest, variant tests, evidence, final status, and residual risks.

**Deliverable:** remediation verification report.

## Test matrix template

| Test ID | Scenario | Expected result | Actual result | Evidence | Status |
|---|---|---|---|---|---|
| V-01 | Original reproduction | Attack no longer succeeds | | | |
| V-02 | Alternate input variant | Control remains effective | | | |
| V-03 | Authorized workflow | Valid use still works | | | |
| V-04 | Unauthorized workflow | Access is denied | | | |
| V-05 | Related endpoint | Same control is enforced | | | |

A lab is complete only when the fix is implemented, the original issue and relevant variants are retested, regression tests pass, and evidence supports the recorded status.
