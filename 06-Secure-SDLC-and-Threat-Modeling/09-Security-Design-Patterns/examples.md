# Security Design Patterns — Examples

These examples are illustrative design exercises. Adapt them to your application's threat model and platform.

## Example 1: Tenant-aware authorization

**Problem:** A user changes `/documents/100` to `/documents/101` and attempts to access another tenant's document.

**Weak design:** The API checks that the user is logged in but loads any document ID supplied by the client.

**Safer pattern:**
1. Authenticate the caller.
2. Load the document using a tenant-aware query or verify ownership after loading.
3. Check the required permission for the specific action.
4. Deny by default if the resource, tenant, or policy check fails.
5. Record a security event without logging the document's sensitive contents.

**Test ideas:**
- A user reads their own document.
- A user attempts to read another tenant's document.
- A user with read-only permission attempts deletion.
- The authorization service is unavailable.
- A resource identifier is malformed or does not exist.

## Example 2: Defense in depth for a public API

| Layer | Control | Failure addressed |
|---|---|---|
| Edge | TLS, request-size limit, basic abuse filtering | Cleartext traffic and oversized requests |
| Identity | Token validation | Unauthenticated requests |
| Application | Resource-level authorization | Cross-user or cross-tenant access |
| Data access | Parameterized queries | SQL injection risk |
| Response | Context-aware encoding and data minimization | Injection and excessive data exposure |
| Operations | Structured audit logs and alerts | Delayed detection of abuse |

**Lesson:** each layer has a distinct job. Passing one layer does not imply the request is safe.

## Example 3: Secrets management

**Weak design:** A database password is committed to a repository and copied into container images.

**Safer design:**
- Store the credential in an approved secrets manager.
- Give only the workload identity permission to retrieve it.
- Inject it at runtime through the platform's supported mechanism.
- Rotate credentials according to risk and capability.
- Audit access and prevent secret values from appearing in logs.
- Revoke and rotate the exposed credential if a leak occurs.

**Verification:** scan repository history and build artifacts, test access policies, and confirm logs redact secrets.

## Example 4: Fail-secure authorization

**Scenario:** The policy service times out during a request to export customer records.

**Unsafe behavior:** The application proceeds because it cannot confirm a denial.

**Safer behavior:** Deny the protected export, return a generic error, log the dependency failure with a correlation ID, and alert if failures cross a threshold. Define retries and recovery so a temporary outage does not create an authorization bypass.

**Trade-off:** fail-closed behavior may reduce availability. Document the risk and define safe recovery; do not silently grant access.

## Example 5: API gateway with service-level checks

```text
Client
  |
  v
API Gateway -- TLS, request limits, token validation, routing
  |
  v
Document Service -- resource authorization, business rules
  |
  v
Document Store -- scoped service identity, parameterized access
```

The gateway provides common edge controls. The document service remains responsible for checking whether the caller can access the specific document. The data store is not directly exposed to the internet.

## Example 6: Rate limiting for authentication

**Requirement:** Limit repeated login and OTP attempts using appropriate account, client, and risk signals.

**Design considerations:**
- Use consistent responses that do not reveal whether an account exists.
- Avoid a single simplistic IP-only rule that can be bypassed or harm shared networks.
- Consider progressive delays, temporary throttling, risk-based challenges, and alerts.
- Ensure limits cannot be reset by changing an untrusted client-supplied identifier.
- Test concurrency and distributed deployments.

Exact thresholds should be set from threat analysis, user impact, and operational evidence—not copied blindly from a sample.

## Example 7: Separation of duties for production release

**Risk:** One compromised developer account can modify code and deploy it to production without review.

**Pattern:**
- Require peer review for protected branches.
- Run automated security and quality checks.
- Require an independent approval for sensitive production releases.
- Use short-lived, scoped deployment identity.
- Keep an auditable record of the actor, artifact, approvals, and result.

## Example 8: Idempotent sensitive operation

**Scenario:** A client retries a payment-like request after a network timeout and accidentally triggers duplicate processing.

**Pattern outline:**
- Client supplies a unique idempotency key for the intended operation.
- Server binds the key to the authenticated principal and request context.
- Server stores the processing state and final outcome safely.
- Concurrent duplicate requests cannot execute the business operation twice.
- Reusing a key with a materially different request is rejected.

Idempotency is not a substitute for authentication, authorization, or transaction integrity.

## Example 9: Architecture Decision Record (ADR)

```markdown
# ADR-004: Centralize workforce authentication

## Status
Accepted

## Context
Several internal applications need consistent MFA and account lifecycle controls.

## Decision
Use the organization's approved identity provider with OIDC.
Applications validate tokens using a maintained library and enforce
their own resource-level authorization policies.

## Alternatives considered
- Build a custom authentication service.
- Use separate local accounts in each application.

## Security consequences
- Centralizes identity lifecycle and MFA.
- Requires resilient identity-provider integration and safe failure behavior.
- Does not remove the need for application authorization.
- Token validation, issuer configuration, and key rotation must be tested.
```

## Example 10: Turn a principle into a testable requirement

**Vague:** “The application should use least privilege.”

**Testable:** “The report worker can read report records and write report status, but cannot change user roles, read payment credentials, or administer cloud resources. Automated tests and cloud policy checks verify these boundaries.”

A useful requirement states the actor, resource, allowed action, denied action, failure behavior, and verification evidence.
