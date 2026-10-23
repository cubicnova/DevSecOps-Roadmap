# OWASP Top 10:2025 — Practical Examples

Examples below are deliberately small and educational. Use only local labs or systems you are authorized to test.

## A01 — Broken Access Control: object ownership

**Weak behavior:** The API checks that the user is logged in, then returns the record matching a client-supplied ID without checking ownership.

**Safer pseudocode:**

```python
def get_invoice(current_user, invoice_id):
    invoice = load_invoice(invoice_id)
    if invoice is None:
        return not_found()

    if invoice.tenant_id != current_user.tenant_id:
        return not_found()  # or a consistent authorization response

    if not policy.allows(current_user, "invoice:read", invoice):
        return forbidden()

    return invoice
```

The policy and data-loading details depend on the framework. The important rule is server-side authorization on the specific resource, not merely authentication.

**Tests:** own invoice allowed; another tenant's invoice denied; read-only user cannot delete; missing policy service does not grant access.

## A02 — Security Misconfiguration: debug settings

**Risk:** Production exceptions expose framework details, filesystem paths, internal hostnames, or secrets.

**Safer approach:**
- Disable debug mode in production.
- Use environment-specific configuration with safe defaults.
- Validate required settings during deployment.
- Return a generic error and keep restricted diagnostics in server-side logs.

**Verification:** cause a controlled application error in a test environment and confirm the response contains no stack trace or secret.

## A03 — Software Supply Chain Failures: dependency controls

**Illustrative pipeline:**

```text
Pull request
   |
   +--> Unit tests and code review
   |
   +--> Secret scanning
   |
   +--> Dependency/SCA scan + lockfile review
   |
   +--> Build in restricted runner
   |
   +--> Artifact integrity/provenance verification
   |
   +--> Approved release and deployment
```

A scan is not sufficient by itself. Protect the runner, CI tokens, package sources, branch rules, release permissions, and artifact storage. Define how teams triage findings and exceptions.

## A04 — Cryptographic Failures: password storage

**Unsafe pattern:** Store a password as plaintext or use a fast general-purpose hash such as plain SHA-256 as the password-storage mechanism.

**Safer pattern:** Use a maintained password-hashing library configured for a suitable password-hashing algorithm such as Argon2id, scrypt, or bcrypt according to the platform's guidance. Use unique salts managed by the library and keep any optional pepper separate in a secrets manager.

Do not design a custom password-hashing scheme. Verify the library's configuration and migration strategy.

## A05 — Injection: SQL query construction

**Unsafe Python example:**

```python
# Do not use this pattern with untrusted input.
query = "SELECT * FROM users WHERE email = '" + email + "'"
```

**Safer example using parameterization:**

```python
cursor.execute(
    "SELECT id, email FROM users WHERE email = ?",
    (email,)
)
```

Placeholder syntax varies by database driver. The key is that the driver sends the value as data rather than concatenating it into SQL syntax. Use least-privilege database accounts and avoid returning detailed database errors to clients.

## A06 — Insecure Design: password reset

**Weak design:** A reset token never expires, can be reused, and is not rate-limited.

**Safer requirements:**
- Reset tokens are unpredictable, short-lived, and single-use.
- The server stores or validates them safely and invalidates them after successful use.
- The workflow has rate limits and abuse monitoring.
- Responses do not unnecessarily reveal whether an account exists.
- Successful recovery triggers appropriate session/token invalidation and user notification.

Test expiration, reuse, concurrent requests, and account-enumeration behavior.

## A07 — Authentication Failures: session cookie

**Example secure cookie settings (framework support required):**

```http
Set-Cookie: session=...; Secure; HttpOnly; SameSite=Lax; Path=/
```

Choose `SameSite` according to the application's legitimate cross-site flow. Rotate session identifiers after login and privilege changes, expire sessions appropriately, and implement CSRF defenses where required. Cookie flags do not replace authorization.

## A08 — Software or Data Integrity Failures: trusted release

**Risk:** A production environment deploys an artifact that was not the artifact tested and approved.

**Safer controls:**
- Build once and promote the same immutable artifact.
- Verify artifact digest and signature/provenance according to the platform.
- Restrict who can publish or deploy artifacts.
- Require appropriate review and approval for sensitive releases.
- Audit deployment identity, artifact version, and approval evidence.

**Test:** alter an artifact or its metadata in a controlled pipeline test and verify that integrity checks reject it.

## A09 — Security Logging and Alerting Failures: event design

Example structured event:

```json
{
  "event_type": "authorization_denied",
  "actor_id": "user-123",
  "resource_type": "invoice",
  "resource_id": "invoice-456",
  "action": "read",
  "outcome": "denied",
  "correlation_id": "req-789",
  "timestamp": "2026-01-01T10:15:00Z"
}
```

Use synthetic identifiers in examples. Do not include passwords, bearer tokens, secret values, or sensitive record contents. Ensure the event is access-controlled, retained according to policy, and connected to an actionable alert when risk thresholds are met.

## A10 — Mishandling of Exceptional Conditions: fail-secure behavior

**Scenario:** The policy service times out during a protected export.

**Unsafe behavior:** The application treats the missing decision as approval.

**Safer behavior:**
1. Deny the protected operation when authorization cannot be confirmed.
2. Return a safe, consistent error response.
3. Log a correlation ID and dependency failure without exposing sensitive data.
4. Alert on sustained or unusual failure rates.
5. Define bounded retries, timeout budgets, and recovery behavior.

Availability trade-offs should be documented. Do not silently bypass a security decision.

## Cross-category example: multi-tenant document API

| Concern | Relevant category | Example control |
|---|---|---|
| Read another tenant's document | A01 | Resource-level authorization |
| Public admin console | A02 | Hardened configuration and restricted network access |
| Compromised build dependency | A03 | Dependency controls and protected pipeline |
| Exposed encryption key | A04 | Key management and access control |
| SQL injection | A05 | Parameterized queries |
| Abuse-prone recovery workflow | A06 | Threat modeling and rate limits |
| Weak session handling | A07 | Secure session lifecycle |
| Unverified release artifact | A08 | Integrity and provenance verification |
| Missing privilege-change events | A09 | Audit logging and alerting |
| Timeout grants unauthorized access | A10 | Explicit fail-secure behavior |

## Example finding format

```markdown
### Finding: Missing tenant authorization on document retrieval

**Category:** OWASP Top 10:2025 A01 — Broken Access Control

**Affected component:** GET /documents/{id}

**Impact:** An authenticated user may retrieve a document belonging to another tenant.

**Evidence:** In the authorized test environment, a test user from Tenant A
was able to request a synthetic document owned by Tenant B.

**Recommendation:** Enforce server-side tenant and resource permissions
on every read and write operation. Deny by default.

**Retest:** Verify same-tenant access succeeds and cross-tenant access fails.
```
