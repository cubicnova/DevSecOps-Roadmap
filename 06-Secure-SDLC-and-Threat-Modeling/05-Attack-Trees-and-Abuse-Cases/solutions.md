# Attack Trees and Abuse Cases — Sample Solutions

These are sample solutions. Other answers are valid when assumptions, logic, risk reasoning, and testability are clear.

## Exercise 1 — Draw an attack tree

**Root goal:** Access another user's private document.

```text
Access another user's private document
OR
+-- Abuse the download API
|   AND
|   +-- Have a valid low-privilege session
|   +-- Submit another user's document identifier
|   +-- Authorization check is missing or incorrect
|
+-- Abuse a sharing link
|   AND
|   +-- Obtain a link
|   +-- Link is too broad, expired but still accepted, or not revoked
|
+-- Reuse an authorized session
    AND
    +-- Obtain a session token through a separate compromise
    +-- Token remains valid and can access the document
```

**Assets:** document contents, ownership metadata, session credentials.
**Trust boundaries:** browser-to-API, API-to-storage, and any external sharing or identity service.

**Possible mitigations**
- Enforce object-level authorization on every document operation.
- Scope, expire, and revoke sharing links; enforce revocation at the download service.
- Protect sessions and support appropriate expiry and revocation.

**Validation:** Cross-account access tests, share-link scope/expiry/revocation tests, and revoked-session tests. These tests should use test accounts and test documents.

## Exercise 2 — Write an abuse case

**Legitimate use case:** A user requests a reset link and changes their password using a valid token.

**Abuse case A:** Repeated reset requests flood a user's inbox or SMS channel.
- Preconditions: Public reset endpoint.
- Impact: User disruption, service load, support burden.
- Controls: Rate limiting, abuse monitoring, appropriate request aggregation and notifications.
- Tests: Controlled repeated requests; verify documented limits and alerting.

**Abuse case B:** Responses reveal whether an account exists.
- Preconditions: Public endpoint with distinguishable responses.
- Impact: Account enumeration and targeted attacks.
- Controls: Consistent response content and timing where practical; rate limiting.
- Tests: Compare responses for existing and nonexistent test accounts.

**Additional negative tests**
- Expired tokens are rejected.
- Used tokens cannot be replayed.
- Tokens cannot be used to change a different account's password.
- Tokens do not appear in logs or analytics.
- Required session-revocation behavior occurs after a successful reset.

## Exercise 3 — Find missing logic

The original tree lists three items without showing whether they are alternatives or sequential requirements.

One clearer model:

```text
Perform an unauthorized admin action
OR
+-- Abuse a privileged session
|   AND
|   +-- Obtain a privileged session
|   +-- Session remains usable despite required revocation
|
+-- Abuse authorization
    AND
    +-- Authenticate as a normal user
    +-- Reach an admin endpoint
    +-- Server fails to enforce the user's permissions
```

**Mitigations and tests**
- Privileged-session path: revoke sessions when policy requires and enforce session validation on protected requests. Test that a revoked session is denied.
- Authorization path: check permissions server-side on each privileged operation. Test every admin endpoint as a normal user and expect denial.

## Exercise 4 — Prioritize attack paths

| Path | Calculation | Score | Training band |
|---|---:|---:|---|
| A | 4 × 5 | 20 | High |
| B | 3 × 2 | 6 | Medium |
| C | 2 × 5 | 10 | Medium |
| D | 4 × 2 | 8 | Medium |

A reasonable starting order is A first because it combines high likelihood and direct financial impact, followed by C because a revocation control is failing and confidentiality impact is high. B and D should be ranked using context, exposure, and business requirements rather than the score alone.

Evidence to collect:
- Whether the affected endpoint is public or restricted
- Reproducible behavior in a test environment
- Scope of affected users, orders, or documents
- Existing compensating controls
- Confidence in likelihood and impact estimates
- Business, privacy, and contractual consequences
- Remediation effort and dependency constraints

## Exercise 5 — Turn vague controls into acceptance criteria

**Secure the admin API**
- Requirement: Every privileged endpoint checks the authenticated identity's server-side permissions for the requested action.
- Positive test: An authorized administrator performs an allowed action.
- Negative test: A normal user calls the same endpoint and is denied, even if request fields claim an admin role.

**Prevent account enumeration**
- Requirement: Account-recovery responses do not unnecessarily reveal whether an account exists.
- Positive test: A valid reset request follows the documented workflow.
- Negative test: Compare responses for existing and nonexistent test accounts and verify no sensitive difference is exposed.

**Make share links safe**
- Requirement: Links have documented scope, expiry, and revocation behavior, enforced on every access.
- Positive test: An authorized recipient accesses an active link within scope.
- Negative test: Expired, revoked, or out-of-scope access is denied.

**Stop duplicate orders**
- Requirement: Repeated submission of the same checkout operation cannot create duplicate order or payment actions.
- Positive test: A valid checkout creates one order.
- Negative test: Replaying the same idempotent request does not create another order.

**Improve audit logging**
- Requirement: Sensitive actions record actor, target, timestamp, outcome, and correlation ID in access-controlled logs without secrets or sensitive payloads.
- Positive test: A successful privileged action produces a complete event.
- Negative test: A denied action is logged, while tokens and passwords remain absent from the logs.

## Exercise 6 — Abuse-case review: document sharing

Possible abuse cases:
1. Link is forwarded to an unintended recipient.
2. Link leaks into browser history, logs, analytics, or referrer headers.
3. A link continues to work after the owner revokes it.
4. A link grants access to more documents than intended.
5. Automated requests enumerate or abuse public links.
6. A recipient retains access longer than the business purpose requires.

Questions to confirm:
- Is public anonymous sharing actually required?
- What data classifications can be shared?
- Who may create links?
- Can owners set expiry and revoke access?
- How is access audited and rate-limited?
- What is the expected behavior for cached or downloaded copies?

Safer controls include private-by-default behavior, scoped high-entropy tokens, expiry and revocation, access logging, appropriate rate limits, safe handling of tokens in URLs, and clear owner controls. Test active, expired, revoked, and out-of-scope links with test documents. Product, security, privacy, and the designated risk owner should review any residual risk.

## Exercise 7 — AND/OR practice

**Goal: Create a duplicate order**
- OR path 1: retry a checkout request AND idempotency is absent or incorrectly implemented.
- OR path 2: concurrent requests AND order creation is not transaction-safe.
- Controls: idempotency, atomic state transitions, concurrency tests.

**Goal: Read a confidential report**
- OR path 1: authenticated account AND object-level authorization is missing.
- OR path 2: obtain a share link AND link scope or revocation is insufficient.
- Controls: per-object authorization, scoped links, expiry, revocation, access logging.

**Goal: Act after administrator access is revoked**
- OR path 1: use an existing session AND revocation is not enforced.
- OR path 2: use a cached authorization decision AND the cache is not invalidated within the required policy.
- Controls: enforce revocation at protected operations, bounded cache lifetime, invalidation, and tests after role removal.

## Exercise 8 — Complete a mini deliverable

A strong submission clearly links:
1. A scoped root goal to the assets at risk.
2. Each path to its prerequisites and logic.
3. Each abuse case to an unintended outcome.
4. Each risk rating to a rationale.
5. Each mitigation to a specific path.
6. Each requirement to a positive or negative validation test.
7. Residual risk to a named owner and review trigger.

Use the model to guide engineering decisions, not as a checklist exercise. Revisit it when new features, dependencies, trust boundaries, or incidents change the assumptions.

## Further reading

- [OWASP Abuse Case Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet.html)
- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
