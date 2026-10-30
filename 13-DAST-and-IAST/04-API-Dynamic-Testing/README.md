# API Dynamic Testing

## Learning objectives

By completing this module, you will be able to:

- Explain API DAST and how it differs from web-application DAST, SAST, and API contract testing.
- Build an API inventory from OpenAPI documents, traffic, and application behavior.
- Test REST and JSON APIs using positive, negative, boundary, and stateful test cases.
- Assess authentication, authorization, object/property access, rate limits, and business workflows.
- Use tools such as OWASP ZAP, Postman/Newman, Schemathesis, curl, and Python.
- Automate safe API security checks in CI/CD.
- Document evidence, triage findings, and define meaningful security gates.

> **Authorization and safety:** Run tests only against APIs you own or are explicitly authorized to assess. Use staging or a disposable lab, test accounts, and synthetic data. Avoid destructive operations, denial-of-service testing, credential attacks, and third-party systems unless the engagement explicitly authorizes them and defines safe limits.

## 1. What is API Dynamic Testing?

API Dynamic Application Security Testing (API DAST) evaluates a running API by sending requests and analyzing responses. It focuses on runtime behavior: authentication, authorization, input validation, data exposure, error handling, configuration, and business workflows.

API DAST can be black-box (little prior knowledge), grey-box (specification and test identities supplied), or integrated with development artifacts. An OpenAPI definition improves endpoint discovery and request generation, but it does not prove the implementation is secure or that the specification is complete.

## 2. API DAST vs. related testing

| Approach | Main focus | Typical inputs |
|---|---|---|
| SAST | Source-code weaknesses | Source code and build metadata |
| Web DAST | Running web application | URLs, browser traffic, forms |
| API DAST | Running API behavior | API endpoints, requests, tokens, schemas |
| Contract testing | Implementation vs. API contract | OpenAPI/JSON Schema and test cases |
| IAST | Runtime observations with instrumentation | Running app plus agent/sensor |

Use these methods together. A DAST scan cannot reliably infer all business rules, valid object relationships, or role permissions.

## 3. API security assessment workflow

A repeatable assessment can follow this sequence:

1. Confirm written authorization, target environment, test window, and rate limits.
2. Collect API inventory, OpenAPI files, Postman collections, authentication details, and test identities.
3. Identify hosts, versions, endpoints, methods, parameters, request bodies, and data sensitivity.
4. Establish a baseline using valid requests.
5. Run schema and input-validation tests.
6. Test authentication and token lifecycle.
7. Test authorization using multiple roles and identities.
8. Test resource consumption and abuse controls within approved limits.
9. Test security configuration, error handling, and external integrations.
10. Review undocumented, deprecated, and shadow endpoints.
11. Validate findings manually and record reproducible evidence.
12. Retest fixes and report residual risk.

## 4. API inventory and attack surface

An API inventory should capture:

- Base URL, environment, version, and owner.
- Endpoint path and HTTP method.
- Authentication scheme and required scopes.
- Role/permission requirements.
- Request and response content types.
- Parameters, schemas, and sensitive fields.
- Rate limits and expected request volume.
- Deprecation status and external dependencies.

Useful sources include OpenAPI/Swagger, source repositories, gateway configuration, Postman/Bruno collections, logs, browser/mobile traffic, and service catalogs. Compare the specification with observed traffic to identify undocumented endpoints and stale versions.

## 5. OpenAPI and schema-driven testing

OpenAPI describes paths, operations, parameters, request bodies, responses, schemas, and security requirements. Use it to generate valid and invalid requests, then compare actual behavior with the contract.

Test categories:

- Positive: valid requests produce expected responses.
- Negative: missing fields, invalid types, malformed JSON, and unsupported values are rejected safely.
- Boundary: minimum/maximum lengths, numeric limits, empty values, and array sizes.
- Unknown properties: determine whether extra fields are intentionally supported or improperly accepted.
- Response validation: check status codes, content types, schema, and sensitive-field exposure.

Do not treat every undocumented field as a vulnerability. Compare behavior with the intended contract and authorization model.

## 6. Authentication testing

Assess how the API identifies callers:

- Missing, malformed, expired, revoked, or invalid tokens.
- JWT signature verification and validation of `iss`, `aud`, `exp`, and `nbf`.
- OAuth 2.0/OIDC flow configuration, redirect URI validation, PKCE where applicable, and scope enforcement.
- API key handling, rotation, and leakage through URLs or logs.
- Session/token invalidation after logout, password change, or account disablement.
- Consistent authentication requirements across all versions and routes.

Use test credentials. Never place live tokens in source control, screenshots, reports, or command history.

## 7. Authorization testing

Authentication answers “who are you?” Authorization answers “what may you do?”

### BOLA / IDOR

Create two test identities, User A and User B. Have User A create a test object, then attempt to read or modify that object while authenticated as User B. The API should deny access without disclosing protected data.

### BFLA

Test whether a lower-privilege role can invoke administrative or privileged functions. Compare behavior across roles and HTTP methods.

### BOPLA / excessive data exposure

Compare fields returned to different roles and test whether callers can read or modify properties they should not control, such as `isAdmin`, `accountBalance`, or ownership fields.

Automated scanners often cannot determine valid object IDs, ownership, or business roles. Build explicit authorization test cases from the application's data model.

## 8. Input validation and injection

Test inputs at API boundaries:

- SQL/NoSQL injection indicators.
- OS command injection indicators.
- Server-side request forgery in URL-fetching features.
- Path traversal and file handling.
- XML external entity handling where XML is accepted.
- Template injection and unsafe deserialization where relevant.
- Header and content-type confusion.
- Duplicate parameters and JSON type confusion.

Use non-destructive test payloads and stop if the target behaves unexpectedly. A response difference is an indicator, not proof; confirm with controlled reproduction and application-owner review.

## 9. Rate limiting and resource consumption

Assess controls against excessive resource consumption without creating service disruption:

- Per-user and per-token limits.
- Per-IP and global limits.
- Pagination maximums and response-size limits.
- Request-body and upload-size limits.
- Expensive search/report/export operations.
- GraphQL depth, complexity, and batching limits.
- Predictable retry behavior and `429 Too Many Requests` responses.

Agree a conservative request rate and stop threshold in advance. Do not perform uncontrolled load or denial-of-service testing.

## 10. Business logic and workflow testing

Some API weaknesses are specific to application workflows and are difficult to detect with generic scanners. Examples include:

- Reusing a one-time coupon or reset token.
- Skipping an approval step.
- Changing the price or quantity after validation.
- Replaying a payment or transfer request.
- Performing actions out of sequence.
- Accessing another tenant's data.
- Automating a sensitive flow beyond intended limits.

Use test accounts and mock payment or sandbox services. Document expected state transitions and compare them with observed behavior.

## 11. Common tools

### OWASP ZAP

Import OpenAPI definitions, explore endpoints, run passive checks, and perform controlled active scanning. See the [ZAP API scan documentation](https://www.zaproxy.org/docs/docker/api-scan/).

### Postman and Newman

Use collections and environments for repeatable functional/security checks. Keep secrets in environment variables or a CI secret store. Newman can run collections in CI.

### Schemathesis

Generate property-based tests from OpenAPI or GraphQL schemas. It is useful for positive, negative, and edge-case contract testing. It does not replace business-logic or authorization testing.

### curl and Python

Use curl for precise request construction and Python for custom checks, test orchestration, and result summaries.

## 12. Example test matrix

| Area | Test | Expected secure behavior |
|---|---|---|
| Authentication | No token | 401 or documented denial |
| Authentication | Expired token | Rejected |
| Authorization | User B requests User A object | 403/404 without data disclosure |
| Authorization | Basic role calls admin endpoint | Denied |
| Property access | Client sets privileged field | Field rejected or ignored according to policy |
| Validation | Wrong JSON type | Controlled 4xx response |
| Validation | Oversized input | Rejected within defined limits |
| Rate limiting | Approved test burst reaches threshold | 429 or documented throttling |
| Error handling | Invalid identifier | No stack trace or secret leakage |
| Inventory | Deprecated route | Removed or explicitly governed |

Status codes depend on the API contract. A `404` can be used to avoid revealing object existence; do not assume one status code is universally required.

## 13. CI/CD integration

A practical pipeline can:

1. Deploy the API to an ephemeral or staging environment.
2. Obtain the matching OpenAPI definition.
3. Run schema-based tests.
4. Run ZAP API scan or another approved API DAST tool.
5. Execute authenticated tests using CI-managed secrets.
6. Run explicit cross-user and role-based authorization tests.
7. Save machine-readable and human-readable reports.
8. Apply a documented quality gate.
9. Clean up the test environment.

Keep scanner failures separate from vulnerability findings. A missing report, unreachable target, or failed authentication setup must not be treated as a clean security result.

## 14. Reporting and triage

A useful finding contains:

- Title and affected API operation.
- OWASP API risk category where applicable.
- Severity and confidence with rationale.
- Preconditions and test identity/role.
- Sanitized request and response evidence.
- Reproduction steps.
- Security and business impact.
- Recommended remediation.
- Owner, status, and retest result.

Remove tokens, passwords, personal data, and unrelated customer records from evidence. Store reports with appropriate access controls and retention.

## 15. Knowledge check

1. What does API DAST test that SAST does not?
2. Why is an OpenAPI document useful but insufficient?
3. Explain BOLA, BFLA, and BOPLA.
4. Why are two test identities valuable?
5. What JWT claims should be validated?
6. How can excessive data exposure be tested?
7. Why should rate-limit testing use an agreed request budget?
8. What is the difference between contract testing and security testing?
9. Why are business-logic tests difficult to automate generically?
10. How should scanner execution failure be handled in CI?

## References

- [OWASP API Security Project](https://api-security.owasp.org/)
- [OWASP API Security Top 10 — 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [OWASP API Security Testing Guideline](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/12-API_Testing/)
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [OWASP DevSecOps Guideline — API Security](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-4-Test/2-4-4-API-Security/)
- [ZAP API Scan](https://www.zaproxy.org/docs/docker/api-scan/)
- [Schemathesis Documentation](https://schemathesis.readthedocs.io/)
