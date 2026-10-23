# API Security — Suggested Solutions

Use this answer key to compare your lab observations. Final controls depend on the API's architecture, data, and risk.

## Lab 1 — Inventory
Include route, HTTP method, API version, owner, purpose, data classification, authentication scheme, required scopes/roles, object-level policy, rate limits, dependencies, and retirement status. Include internal and partner APIs, not only public routes.

## Lab 2 — Object-level authorization
Every request that references an object must verify the caller is allowed to perform the requested action on that exact object. Do not rely on unguessable IDs or frontend filtering. Test read, update, delete, export, nested resources, and bulk operations. Deny by default.

## Lab 3 — Property-level authorization
Use explicit request DTOs/schemas and response serializers. Allow only fields intended for that endpoint and caller. Never blindly bind request JSON to database models. Protect privileged fields and avoid exposing internal or sensitive properties in responses.

## Lab 4 — Token validation
Use a maintained library and fixed validation policy. Validate signature, issuer, audience, expiry, not-before, and required claims/scopes. Do not treat a valid signature as proof of authorization. Reject tokens with unexpected algorithms, missing required claims, or invalid key sources. Define key rotation and revocation behavior.

## Lab 5 — Resource limits
Set maximum request body and upload size, pagination bounds, query complexity, execution timeout, concurrency, and per-identity/tenant quotas. Return controlled errors and monitor repeated abuse. Tune limits to legitimate workload; avoid unplanned load testing.

## Lab 6 — CORS and errors
Allow only required origins and methods. Be especially careful when credentials are allowed; do not use wildcard origins with credentialed access. CORS does not replace authentication or authorization. Return stable, minimal error bodies and place detailed diagnostics in access-controlled, sanitized logs.

## Lab 7 — SSRF
Prefer destination allowlists. Validate URL scheme and hostname, resolve and check addresses, account for redirects and DNS rebinding, and enforce outbound network restrictions. Block internal and metadata ranges unless explicitly required. Use a dedicated egress policy and do not rely solely on regular expressions.

## Lab 8 — Business-flow abuse
Model expected state transitions and enforce them server-side. Use idempotency keys where appropriate, verify eligibility at the time of action, enforce per-user/tenant quotas, and make state changes atomic. Treat client-side sequencing as advisory only.

## Sample finding
**Title:** API permits cross-tenant access to an object  
**Severity:** Depends on data sensitivity, exposed operations, and exploitability.  
**Impact:** An authenticated user may view or modify records belonging to another tenant.  
**Root cause:** The endpoint loads a record by client-supplied ID but does not enforce tenant/object authorization.  
**Remediation:** Apply server-side object-level authorization for each operation, scope data access to the authorized tenant, and add regression tests for read/update/delete/export paths.  
**Regression test:** Authenticate as tenant A and request tenant B's test object. The request must be denied without disclosing its contents.

## Reporting quality
Keep evidence minimal and redacted, distinguish confirmed behavior from assumptions, and propose a fix that can be verified by automated tests.
