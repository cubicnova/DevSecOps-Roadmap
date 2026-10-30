# API Security — Practical Labs

Run these exercises only against a local lab, your own application, or a system you are explicitly authorized to test. Use synthetic accounts and data.

## Lab 1 — Build an API inventory
1. List routes, methods, versions, authentication requirements, owner, and data sensitivity.
2. Mark public, user, tenant-admin, and service-only operations.
3. Identify deprecated routes, debug endpoints, and undocumented versions.
4. Add an owner and retirement date for every version.

**Deliverable:** completed `api-inventory-template.csv`.

## Lab 2 — Test object-level authorization
1. Create two test users, A and B, with separate records.
2. Authenticate as A and access A's record.
3. Change only the record identifier to B's record in the controlled lab.
4. Verify the API denies access and does not expose B's data.
5. Repeat for read, update, delete, export, and nested-resource endpoints where applicable.

**Deliverable:** endpoint-by-endpoint authorization results.

## Lab 3 — Test property-level authorization
1. Inspect request schemas for profile, order, and administrative endpoints.
2. Submit an unexpected field such as `role` or `owner_id` using a test account.
3. Confirm the server rejects or safely ignores unauthorized fields.
4. Check that responses do not disclose internal fields such as password hashes, secrets, or internal flags.

**Deliverable:** allowlisted field map and regression tests.

## Lab 4 — Authentication and token validation
1. Review how the API obtains and validates identity tokens.
2. In a test environment, test expired, malformed, wrong-audience, and wrong-issuer tokens.
3. Verify unsigned or incorrectly signed tokens are rejected.
4. Confirm scope/role checks are separate from token signature validation.
5. Ensure credentials do not appear in URLs or logs.

**Deliverable:** token-validation test results.

## Lab 5 — Resource consumption
1. Review pagination, query filters, uploads, exports, and expensive endpoints.
2. Test reasonable boundary values in a local environment.
3. Verify oversized bodies, excessive page sizes, and invalid ranges are rejected.
4. Confirm rate limits and quotas return controlled responses.
5. Avoid stress tests or high-volume traffic unless explicitly planned and authorized.

**Deliverable:** resource-limit matrix.

## Lab 6 — CORS and error handling
1. Review allowed origins, methods, and headers.
2. Verify untrusted origins are not granted credentialed access.
3. Trigger controlled validation and authorization errors.
4. Confirm responses omit stack traces, database details, and secrets.
5. Check correlation IDs link the response to sanitized server-side logs.

**Deliverable:** CORS and error review.

## Lab 7 — SSRF and outbound requests
1. Identify endpoints that accept URLs, webhook targets, image URLs, or import sources.
2. Review destination allowlisting, DNS/IP validation, redirect behavior, and egress controls.
3. In a local mock environment, verify private, loopback, link-local, and disallowed destinations are blocked.
4. Confirm errors do not expose internal network topology.

**Deliverable:** outbound-request threat model.

## Lab 8 — Business-flow abuse
1. Map a sensitive workflow such as coupon redemption, booking, checkout, or account recovery.
2. Identify required state transitions and server-side invariants.
3. Test duplicate submissions, out-of-order steps, and replayed idempotency keys using test data.
4. Confirm quotas and eligibility checks are enforced server-side.

**Deliverable:** abuse-case list and mitigations.

## Lab 9 — Write a finding
Document a confirmed issue with title, severity rationale, endpoint, role/preconditions, reproducible steps, redacted evidence, impact, root cause, remediation, and regression test.

## Completion criteria
- Every endpoint is inventoried and has an owner.
- Object-, function-, and property-level authorization are tested.
- Tokens are validated with explicit issuer, audience, expiry, signature, and claim rules.
- Input, output, pagination, uploads, and expensive operations are bounded.
- CORS, errors, secrets, logs, SSRF, and business workflows are reviewed.
