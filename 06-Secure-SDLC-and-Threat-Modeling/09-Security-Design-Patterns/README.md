# 09 — Security Design Patterns

Reusable design patterns help teams build security into applications consistently instead of inventing security controls from scratch. A pattern describes a recurring problem, its context, a recommended approach, and the trade-offs to consider.

This module focuses on **application and architecture security patterns** for the DevSecOps lifecycle. Patterns are not drop-in guarantees: select them based on threat models, system constraints, and verified framework guidance.

## Learning objectives

By the end of this module, you should be able to:

- Explain the purpose and limits of security design patterns.
- Apply least privilege, defense in depth, deny-by-default, and complete mediation.
- Choose appropriate authentication, authorization, secrets, and secure-communication patterns.
- Design safe input handling, error handling, audit logging, and rate limiting.
- Recognize common anti-patterns and document design decisions.
- Convert pattern choices into testable security requirements.

## Core principles

| Principle | Meaning | Example |
|---|---|---|
| Least privilege | Grant only the access needed, for the shortest practical duration | A report service can read reports but cannot administer users |
| Defense in depth | Use multiple independent controls | Authentication, authorization, validation, monitoring, and rate limits |
| Secure defaults | Begin in the safest practical configuration | Admin routes disabled unless explicitly configured |
| Fail securely | Failure must not grant access or reveal secrets | Authorization-service timeout results in denial for protected actions |
| Minimize attack surface | Reduce exposed components and capabilities | Remove unused routes, ports, packages, and accounts |
| Complete mediation | Check authorization for each protected action | Verify object ownership on every API request |
| Separation of duties | Split high-risk authority | One person requests a production release; another approves it |
| Privacy by design | Minimize collection, exposure, and retention of personal data | Store only required fields and define retention rules |

## Patterns to know

### 1. Centralized identity and authentication

Use a trusted identity provider and well-maintained authentication libraries instead of creating a custom password or token protocol.

**Use when:** multiple applications or services need consistent identity, MFA, session management, or single sign-on.

**Design checks:**
- Validate issuer, audience, signature, expiry, and intended token use.
- Use short-lived access tokens and safe refresh-token handling.
- Require stronger authentication for privileged actions.
- Do not accept tokens from untrusted issuers or algorithm choices.
- Keep identity authentication separate from application authorization.

### 2. Server-side authorization and policy enforcement

Authentication answers “who is calling?” Authorization answers “may this caller perform this action on this resource?”

**Recommended pattern:** enforce authorization at a trusted server-side boundary and check resource-level permissions on every operation. Gateways can provide a common first layer, but services must not blindly trust client-supplied roles or object IDs.

Example requirement: “A user can read a report only when they belong to the report’s tenant and have the `report:read` permission.”

### 3. Least privilege and capability-based access

Give each user, workload, service account, and CI/CD job the minimum permissions it needs. Prefer scoped, short-lived credentials over shared long-lived secrets.

**Avoid:** one administrator credential shared by every service, wildcard cloud permissions, and production credentials available to every pipeline job.

### 4. Defense in depth

Combine controls that address different failure modes. For a web application, layers might include a hardened edge, TLS, authentication, authorization, input validation, parameterized database queries, output encoding, rate limiting, safe logging, and alerting.

A WAF is an additional layer—not a substitute for secure application logic.

### 5. Secure gateway / API façade

Place a managed API gateway or façade at the public boundary for consistent routing, TLS policy, request-size limits, authentication integration, throttling, and observability.

**Important:** downstream services still need explicit authorization and safe input handling. Avoid exposing internal services directly or allowing the gateway to become a single overprivileged trust point.

### 6. Input validation and context-aware output encoding

Validate input against an expected schema and business rules on the server. Prefer allowlists, type constraints, length limits, and parameterized queries. Encode output for the context in which it is rendered.

- Validation reduces unexpected input.
- Parameterized queries separate data from SQL syntax.
- Output encoding helps prevent injection into HTML, JavaScript, attributes, or URLs.
- These controls are related but are not interchangeable.

### 7. Secrets management and key rotation

Store credentials and cryptographic keys in an approved secrets manager or key-management service. Limit access, audit retrieval, rotate where appropriate, and prevent secrets from entering source control, logs, images, or build artifacts.

Do not invent your own cryptographic algorithms. Use established libraries and vetted key-management practices.

### 8. Secure communication and service identity

Protect data in transit with correctly configured TLS. In service-to-service environments, use authenticated service identity and consider mutual TLS (mTLS) when it fits the architecture. Verify certificates and identities; encryption without peer validation is insufficient.

### 9. Fail-secure error handling

Return a safe, predictable response to users while recording useful diagnostic details in restricted server-side logs. Never reveal stack traces, secrets, access tokens, database connection strings, or sensitive personal data to clients.

For protected operations, dependency failures should not silently bypass authorization. Define explicit behavior for timeouts, retries, and partial failures.

### 10. Rate limiting and resource controls

Apply limits at relevant boundaries based on account, token, IP, tenant, or operation. Use stricter limits for login, password reset, OTP verification, expensive searches, and sensitive business actions.

Return consistent responses and avoid exposing whether an account exists. Rate limiting should be paired with monitoring and abuse-response procedures.

### 11. Audit logging and security observability

Record security-relevant events such as authentication failures, privilege changes, access denials, key administrative actions, and sensitive exports. Use structured logs, timestamps, correlation IDs, access controls, and a defined retention policy.

Do not log passwords, session tokens, full payment data, or secrets. Logs should be protected against unauthorized modification and access.

### 12. Secure-by-default configuration

Use hardened templates and configuration-as-code so new environments inherit safe settings. Fail deployment checks when critical configuration is missing; keep development convenience settings out of production.

### 13. Separation of duties and approval gates

Require independent approval for high-risk operations such as production deployment, privilege elevation, and key rotation. Use auditable approvals and narrowly scoped break-glass access.

### 14. Idempotency for sensitive operations

For payment-like or other high-impact operations, use an idempotency key or equivalent deduplication mechanism so retries do not unintentionally repeat a business action. Bind keys to the caller and operation, define expiry, and handle concurrent requests safely.

## Pattern selection workflow

1. **Understand the context:** assets, actors, trust boundaries, data sensitivity, and business rules.
2. **Identify threats and abuse cases:** include authorization bypass, replay, abuse, data leakage, and dependency failure.
3. **Select a pattern:** use vetted platform capabilities and established libraries where possible.
4. **Record trade-offs:** latency, availability, complexity, operational ownership, and failure modes.
5. **Write testable requirements:** state the expected behavior, not just “use security.”
6. **Verify:** design review, code review, automated tests, configuration checks, and operational monitoring.
7. **Revisit after change:** new endpoints, data types, integrations, or trust boundaries can invalidate the original choice.

## Example requirement format

> **Requirement:** Every request to read or modify a tenant-owned object must verify that the authenticated principal has the required permission and belongs to the object’s tenant. A failed or unavailable authorization check must deny the operation. Tests must cover cross-tenant access attempts.

## Design review checklist

- [ ] Authentication uses a trusted, maintained implementation.
- [ ] Authorization is enforced server-side for every protected action and resource.
- [ ] Roles and permissions are not trusted merely because the client supplied them.
- [ ] Privileges and service credentials are scoped to the minimum necessary.
- [ ] Trust boundaries and service identities are explicit.
- [ ] TLS and certificate validation are configured correctly.
- [ ] Inputs have schema and business-rule validation; database operations use parameterization.
- [ ] Output is encoded for the correct context.
- [ ] Secrets are kept out of source control, logs, and build artifacts.
- [ ] Error paths fail safely and do not disclose internals.
- [ ] Rate limits protect authentication and expensive operations.
- [ ] Security events are logged without exposing sensitive values.
- [ ] High-risk actions have appropriate approval and audit trails.
- [ ] Security controls have negative tests and operational owners.

## Common anti-patterns

- **Security by obscurity:** hiding a URL is treated as authorization.
- **Gateway-only authorization:** internal services trust every request from the gateway without validating the required identity and permissions.
- **Client-side enforcement:** the browser hides a button, but the API accepts the operation.
- **Fail-open authorization:** a timeout or exception grants access.
- **Custom cryptography:** bespoke algorithms or token formats replace standard, reviewed libraries.
- **Overly broad service accounts:** one compromised component can access unrelated systems.
- **Logging everything:** credentials and sensitive payloads are copied into searchable logs.
- **One control solves all:** a WAF or encryption is assumed to replace authorization and safe application logic.

## Suggested hands-on lab

Design a multi-tenant document API with `GET /documents/{id}`, `POST /documents`, and `DELETE /documents/{id}`.

1. Identify the trust boundaries and sensitive assets.
2. Define roles and resource-level authorization rules.
3. Choose patterns for authentication, secrets, transport security, validation, rate limiting, and logging.
4. Write at least eight testable security requirements.
5. Create negative test cases for cross-tenant access, expired tokens, oversized input, and dependency failure.
6. Document one decision and one rejected alternative in an Architecture Decision Record (ADR).

Use a local toy application or a system you are authorized to test. Do not test these ideas against systems without permission.

## Further reading

- [OWASP Secure Design and Requirements](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-1-Design/2-1-2-Secure-design-and-requirements/)
- [OWASP Developer Guide — Design](https://devguide.owasp.org/en/04-design/)
- [OWASP Secure by Design Framework](https://owasp.org/projects/secure-by-design-framework)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)

## Completion criteria

You can explain the purpose and limitations of at least six patterns, select suitable patterns for a documented threat model, translate choices into verifiable requirements, and describe how the controls will be tested and monitored.
