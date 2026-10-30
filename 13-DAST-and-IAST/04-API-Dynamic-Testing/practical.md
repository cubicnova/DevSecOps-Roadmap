# API Dynamic Testing — Practical Labs

## Lab safety and prerequisites

Use a local intentionally vulnerable API or a dedicated staging API with written authorization. Good lab choices include OWASP crAPI, OWASP Juice Shop APIs, or a small API you create yourself. Use synthetic data and dedicated test accounts.

Suggested tools:
- curl and Python
- Postman/Newman
- OWASP ZAP
- Schemathesis
- Docker
- OpenAPI document for the target

Do not conduct destructive tests, high-volume load tests, or credential attacks unless explicitly included in the approved test plan.

## Lab 1 — API discovery and inventory

**Tasks**

1. Identify the API base URL and environment.
2. Locate the OpenAPI/Swagger definition.
3. Extract all paths and HTTP methods.
4. Identify versioned and deprecated routes.
5. Compare documented routes with observed traffic or gateway logs.
6. Record owner, authentication, role, and data sensitivity for each route.

**Deliverable:** `api-inventory.xlsx` or `api-inventory.md`.

## Lab 2 — Establish a baseline

**Tasks**

1. Select five read-only endpoints.
2. Send valid requests with the correct test identity.
3. Record status, headers, content type, response schema, and timing.
4. Repeat without authentication where appropriate.
5. Compare actual behavior with the API contract.

**Deliverable:** baseline request/response matrix with secrets removed.

## Lab 3 — Schema and input validation

**Tasks**

For selected endpoints, test:
- Missing required fields.
- Incorrect JSON types.
- Empty strings and null values.
- Values just below and above documented limits.
- Unexpected fields.
- Malformed JSON and unsupported content types.

Check that the API returns controlled errors and does not leak stack traces or internal data.

**Deliverable:** validation test cases and results.

## Lab 4 — Authentication and token lifecycle

**Tasks**

1. Use a dedicated lab account.
2. Test missing, malformed, expired, and revoked credentials.
3. Review JWT validation behavior where JWTs are used.
4. Test token invalidation after logout or password change, if supported.
5. Check that API keys and tokens are not exposed in URLs or error messages.

**Deliverable:** authentication test matrix. Do not submit raw tokens.

## Lab 5 — BOLA / IDOR

**Tasks**

1. Create User A and User B in the lab.
2. Have User A create a test object.
3. Record the object identifier.
4. Request the object as User A.
5. Request the same object as User B.
6. Try a safe read-only variant and, only if approved, a reversible update on disposable data.
7. Verify that User B cannot read or modify User A's object.

**Deliverable:** sanitized evidence and access-control matrix.

## Lab 6 — BFLA / role authorization

**Tasks**

1. Identify an administrative endpoint.
2. Create basic-user and administrator test identities.
3. Invoke the endpoint with each identity.
4. Compare status, response content, and side effects.
5. Check alternate HTTP methods if they are part of the API contract.
6. Record whether role enforcement is consistent across versions.

**Deliverable:** role-versus-operation matrix.

## Lab 7 — BOPLA and excessive data exposure

**Tasks**

1. Identify sensitive object properties in the API schema.
2. Compare responses for different roles.
3. Test whether a user can read fields outside their permission.
4. In a disposable lab, submit a privileged property in an update request.
5. Verify persisted state rather than relying only on the response body.

**Deliverable:** property-level access matrix and remediation notes.

## Lab 8 — Injection and parser robustness

**Tasks**

1. Identify parameters that reach database queries, URL fetchers, file paths, or interpreters.
2. Use harmless, non-destructive test values.
3. Test type confusion, duplicate parameters, malformed JSON, and boundary values.
4. Review response differences, error messages, and server logs if authorized.
5. Stop if the API shows instability or unexpected side effects.

**Deliverable:** input-validation test record. Do not attempt destructive payloads.

## Lab 9 — Resource consumption controls

**Tasks**

1. Agree a conservative request budget with the API owner.
2. Identify expensive search, export, pagination, and upload operations.
3. Send a small number of requests with controlled delays.
4. Observe rate-limit headers and `429` behavior.
5. Verify maximum page size and body-size enforcement.
6. Stop immediately if latency or error rates exceed the agreed threshold.

**Deliverable:** rate-limit observation report.

## Lab 10 — Business logic and workflow

**Tasks**

1. Map a multi-step workflow using test accounts and synthetic data.
2. Record allowed state transitions.
3. Try a safe out-of-order request.
4. Check whether a one-time action can be replayed in the lab.
5. Verify server-side validation of price, quantity, ownership, and approval state.
6. Use sandbox integrations rather than real payment or messaging services.

**Deliverable:** workflow diagram and test-case table.

## Lab 11 — ZAP and Schemathesis automation

**Tasks**

1. Import the OpenAPI definition into ZAP.
2. Run an API scan against the lab.
3. Save an HTML report.
4. Run Schemathesis against the same schema.
5. Compare discovered operations and findings.
6. Investigate differences and document coverage gaps.

**Deliverable:** ZAP report, Schemathesis output, and comparison notes.

## Lab 12 — CI/CD security gate

**Tasks**

1. Deploy the API in an ephemeral or dedicated test environment.
2. Wait for a bounded health check.
3. Run schema-driven tests.
4. Run a controlled API DAST scan.
5. Run explicit two-user authorization tests.
6. Save reports as CI artifacts.
7. Fail the pipeline on scanner errors or confirmed policy violations.
8. Clean up containers and test data even when a step fails.

**Deliverable:** pipeline YAML, test logs, and gate policy.

## Lab 13 — API inventory drift

**Tasks**

1. Extract paths and methods from the OpenAPI document.
2. Compare them with the endpoint inventory or approved traffic sample.
3. Identify undocumented, deprecated, and unexpected endpoints.
4. Verify each discrepancy with the API owner.
5. Record whether it is an approved exception, shadow API, or stale route.

**Deliverable:** API inventory drift report.

## Lab 14 — Capstone: API security assessment

Assess a dedicated API with at least two test roles.

Required coverage:
- Inventory and OpenAPI review.
- Positive, negative, and boundary tests.
- Authentication and token lifecycle.
- BOLA, BFLA, and BOPLA.
- Input validation and safe injection checks.
- Rate limiting within an approved request budget.
- Business workflow validation.
- ZAP or equivalent API DAST scan.
- CI/CD automation and report retention.
- Finding triage, remediation, and retesting.

**Deliverables:**
- Scope and rules of engagement.
- API inventory.
- Test matrix and sanitized evidence.
- Automated scan reports.
- Confirmed findings and risk ratings.
- Remediation recommendations.
- Retest summary.

## Submission checklist

- [ ] Written authorization and target scope recorded.
- [ ] API inventory prepared.
- [ ] OpenAPI definition reviewed.
- [ ] Baseline requests captured.
- [ ] Negative and boundary cases tested.
- [ ] Authentication and token lifecycle tested.
- [ ] Two-identity BOLA tests performed.
- [ ] Role and property-level authorization tested.
- [ ] Resource-consumption checks stayed within limits.
- [ ] Business workflows tested with synthetic data.
- [ ] DAST and schema-driven tools executed.
- [ ] CI reports retained securely.
- [ ] Secrets and personal data removed from evidence.
- [ ] Findings manually validated and retested.
