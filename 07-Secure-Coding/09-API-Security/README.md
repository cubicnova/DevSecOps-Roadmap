# 09 — API Security

APIs expose application data and actions to clients, integrations, mobile apps, and services. Secure API design requires strong identity checks, object- and function-level authorization, careful input handling, safe data exposure, abuse controls, and reliable monitoring.

## Learning objectives
- Identify common API threat categories and map them to appropriate controls.
- Distinguish authentication from object-level, function-level, and property-level authorization.
- Apply safe validation, serialization, pagination, and error handling.
- Protect tokens, API keys, secrets, and sensitive data in transit and at rest.
- Test rate limits, workflow abuse, SSRF risks, and inventory/version exposure.
- Document reproducible findings and regression tests.

## API security review workflow
1. Inventory endpoints, methods, versions, authentication schemes, data classes, and owners.
2. Map actors and trust boundaries; identify sensitive objects and actions.
3. Review authentication, object-level authorization, function-level authorization, and property-level authorization.
4. Review input validation, output filtering, pagination, file handling, and error behavior.
5. Assess resource consumption, rate limiting, business workflows, and third-party integrations.
6. Review TLS, CORS, secrets management, logging, monitoring, and API version lifecycle.
7. Test negative and boundary cases in an authorized environment; record evidence and retest fixes.

## Core controls
- Enforce authorization server-side on every request and every object/action. Never trust IDs supplied by the client.
- Return only the properties a caller is allowed to see or modify; use explicit request and response schemas.
- Validate type, format, length, range, and business meaning. Reject unexpected fields where practical.
- Use standard, maintained authentication mechanisms such as OAuth 2.0/OIDC where suitable; validate token issuer, audience, signature, expiry, and required claims.
- Keep secrets out of source code, URLs, client-side bundles, and logs. Rotate exposed credentials and use a secrets manager where available.
- Apply rate limits and resource quotas by relevant dimensions (identity, tenant, endpoint, and source context).
- Protect sensitive business workflows from automation and out-of-order execution.
- Set request size, upload size, pagination, query complexity, and execution time limits.
- Use HTTPS; configure CORS narrowly for browser clients. CORS is not authentication or authorization.
- Treat external URLs and webhooks as untrusted input; use SSRF defenses and strict egress controls.
- Return safe error messages and stable error formats without stack traces, internal paths, or secrets.
- Log security events with correlation IDs while redacting tokens, credentials, and sensitive payloads.
- Inventory and retire obsolete API versions, test endpoints, and undocumented routes.

## OWASP API Security Top 10 themes
This learning module covers the major themes in the OWASP API Security Top 10, including:
- Broken Object Level Authorization (BOLA)
- Broken Authentication
- Broken Object Property Level Authorization
- Unrestricted Resource Consumption
- Broken Function Level Authorization
- Unrestricted Access to Sensitive Business Flows
- Server Side Request Forgery (SSRF)
- Security Misconfiguration
- Improper Inventory Management
- Unsafe Consumption of APIs

Consult the current OWASP project page for the precise edition and definitions used by your organization.

## Suggested folder contents
- `README.md` — concepts and review workflow
- `examples.md` — secure API patterns and anti-patterns
- `practical.md` — authorized hands-on exercises
- `solutions.md` — answer key and remediation guidance
- `api-security-checklist.md` — review checklist
- `api-test-matrix.csv` — reusable test matrix
- `api-inventory-template.csv` — endpoint inventory template

## References
- OWASP API Security Top 10: https://owasp.org/API-Security/
- OWASP REST Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html
- OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP SSRF Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
