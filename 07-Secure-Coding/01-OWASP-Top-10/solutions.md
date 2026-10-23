# OWASP Top 10:2025 — Sample Solutions

These are example answers. Multiple approaches may be valid if they address the underlying risk and can be verified.

## Exercise 1: Category mapping

1. **A01 — Broken Access Control:** missing resource-level authorization or tenant isolation.
2. **A02 — Security Misconfiguration:** unsafe production debug/error configuration.
3. **A03 — Software Supply Chain Failures:** untrusted dependency source and excessive CI release privileges.
4. **A04 — Cryptographic Failures:** exposed key material undermines data protection.
5. **A05 — Injection:** untrusted input is interpreted as SQL syntax.
6. **A06 — Insecure Design:** workflow lacks abuse controls and security requirements.
7. **A07 — Authentication Failures:** session lifecycle does not correctly maintain identity assurance. Depending on the exact failure, authorization or design issues may also be relevant.
8. **A08 — Software or Data Integrity Failures:** artifact integrity is not verified across the release boundary.
9. **A09 — Security Logging and Alerting Failures:** important security events and actionable alerts are missing.
10. **A10 — Mishandling of Exceptional Conditions:** dependency failure results in fail-open behavior.

A real issue may span multiple categories. Select the category that best captures the root cause and explain any overlap.

## Exercise 2: Access-control tests

| Test | Expected result | Evidence |
|---|---|---|
| Owner reads own project | Allowed | Test response and audit record |
| User from another tenant reads project | Denied | Test result and denial event |
| User from another tenant updates project | Denied; no data changes | Response and database assertion |
| Read-only user deletes project | Denied | Authorization test result |
| Direct API call bypasses UI restrictions | Same server-side policy applies | HTTP test and logs |
| Expired or invalid token | Rejected | Authentication event |
| Authorization service unavailable | Protected action denied | Correlated error and alert |

Use synthetic accounts and records. Confirm denied write requests do not produce partial changes.

## Exercise 3: Fix injection

The query concatenates untrusted input into SQL, allowing input to change query structure.

Example using a driver that supports `?` placeholders:

```python
email = request.args.get("email", "")
db.execute(
    "SELECT id, email FROM users WHERE email = ?",
    (email,)
)
```

Placeholder syntax varies by driver. Additional controls include least-privilege database credentials, input schema/length validation, generic error handling, and static analysis. A regression test should verify ordinary values work and crafted input is treated as a literal value, using a disposable test database and no production data.

## Exercise 4: Secure configuration review

| Item | Verification |
|---|---|
| Debug disabled | Deployment policy check and controlled error-response test |
| Defaults and sample endpoints removed | Endpoint inventory and automated configuration scan |
| TLS and headers | TLS configuration scan and HTTP response assertions |
| CORS | Review allowed origins and credential behavior; test untrusted origins |
| Cloud storage | Automated IAM/bucket policy review and anonymous-access test |
| Secrets | Secret scanning and runtime secret-access policy checks |
| Management ports | Network scan within authorized scope and firewall review |
| Dependencies | Lockfile review, software composition analysis, patch-status tracking |

Record exceptions, owners, and expiration dates. Automated checks should fail builds or deployments for defined critical violations.

## Exercise 5: Supply-chain threat model

**Assets:** source code, dependency artifacts, build credentials, signing keys, container image, registry, and production deployment identity.

**Trust boundaries:** contributor to repository, repository to CI runner, runner to package registry, build to artifact registry, and registry to deployment platform.

**Controls**
1. Protected branches and reviewed changes.
2. Dependency pinning, trusted registries, lockfiles, and dependency scanning.
3. Least-privilege short-lived CI credentials.
4. Isolated or ephemeral runners with restricted network access.
5. Secret scanning and immediate credential revocation procedures.
6. Immutable artifact storage and integrity/provenance verification.
7. Separate build, publish, and deploy permissions where practical.
8. Auditable approvals and monitoring for unusual publishing activity.

**Tests:** attempt an unapproved branch release, use a deliberately unauthorized token in a test pipeline, verify tampered artifact rejection, and confirm a dependency finding triggers the defined workflow. Owners can include application engineering, platform engineering, and security engineering.

## Exercise 6: Cryptography and data protection

- Collect only fields required for the stated purpose and define deletion/retention rules.
- Use correctly configured TLS for network traffic.
- Store passwords with a maintained password-hashing function such as Argon2id, scrypt, or bcrypt, configured to current platform guidance.
- Use an approved key-management service and restrict key access by workload.
- Store API credentials in a secrets manager; rotate and revoke them according to risk.
- Redact credentials and sensitive data from logs and error responses.
- Encrypt and restrict access to backups; test restore and key-recovery procedures.

Encryption protects confidentiality in specific contexts but does not decide whether an authenticated user is allowed to access a record. Authorization, key access control, and auditability remain necessary.

## Exercise 7: Authentication and session review

Priority fixes:
1. Add rate limits and abuse detection for login and recovery.
2. Rotate the session identifier after login and relevant privilege changes.
3. Set appropriate cookie attributes such as `Secure`, `HttpOnly`, and a context-appropriate `SameSite` value.
4. Use unpredictable, short-lived, single-use reset tokens.
5. Use consistent reset responses that do not reveal account existence.

Tests should verify throttling under controlled repeated attempts, session ID rotation, cookie attributes over HTTPS, reset-token expiry and reuse rejection, and consistent response behavior. Avoid locking users out in a way attackers can easily abuse.

## Exercise 8: Logging and alerting

**Useful event fields:** timestamp, event type, actor or workload identifier, action, target identifier where appropriate, outcome, source/context, and correlation ID.

**Example alert ideas**
- Repeated authentication failures over a defined window.
- A high rate of denied access across many object IDs or tenants.
- Privilege changes outside approved workflows.
- Unusual sensitive exports.
- Unexpected release or deployment identity.
- Repeated authorization dependency failures.

Assign an on-call owner, severity, response runbook, and escalation path. Never log passwords, session cookies, bearer tokens, private keys, or unnecessary sensitive payloads. Test by generating synthetic events and verifying both log ingestion and alert delivery.

## Exercise 9: Exceptional conditions

| Failure | Safe behavior | Verification |
|---|---|---|
| Authorization timeout | Deny protected export | Fault-injection test and denial event |
| Database timeout before transaction | Return safe error; do not claim success | Integration test and no partial state |
| File service failure after work begins | Use transaction/state machine or cleanup/retry strategy | Recovery and consistency test |
| Client retries request | Prevent duplicate business operation where required | Idempotency test |
| Repeated dependency failures | Bounded retries, timeout budget, alerting | Metrics and alert test |

Do not retry indefinitely or treat an unknown authorization result as approval. Define idempotency keys and operation states for actions where duplicates have material impact.

## Exercise 10: DevSecOps mapping

| Category | Preventive control | Pipeline/deployment check | Runtime signal |
|---|---|---|---|
| A01 Access control | Server-side resource authorization | Authorization regression tests | Repeated denials or cross-tenant probes |
| A02 Misconfiguration | Hardened baseline | IaC/configuration checks | Unexpected exposure or configuration drift |
| A03 Supply chain | Trusted, scoped dependencies and CI | SCA, secret scanning, artifact verification | Unexpected package or release changes |
| A04 Cryptographic failures | Approved cryptography and key management | Secret scans and TLS/config checks | Key-access anomalies |
| A05 Injection | Parameterized queries and safe APIs | SAST and focused tests | Repeated input rejection or suspicious errors |
| A06 Insecure design | Threat modeling and abuse-case requirements | Security acceptance tests | Abuse patterns against workflows |
| A07 Authentication | Maintained identity/session controls | Auth-flow and session tests | Credential attacks and anomalous login activity |
| A08 Integrity failures | Verified artifacts and trusted data boundaries | Signature/provenance checks | Unexpected artifact or integrity mismatch |
| A09 Logging/alerting | Structured security events | Logging/alert integration tests | Missing telemetry or security alerts |
| A10 Exceptional conditions | Explicit safe failure behavior | Timeout, retry, and fault tests | Error spikes and dependency failures |

## Exercise 11: Sample finding

```markdown
### Title
Cross-tenant access to project records

### Category
OWASP Top 10:2025 A01 — Broken Access Control

### Scope
GET /projects/{id} in the authorized test environment.

### Impact
An authenticated user may access project data belonging to a different tenant,
potentially exposing confidential business information.

### Evidence
Using synthetic Tenant A and Tenant B accounts, a request by Tenant A for
a Tenant B project returned the test record instead of denying access.

### Recommendation
Enforce server-side tenant and resource-level authorization for every read
and write operation. Deny by default and add regression tests.

### Retest
Verify same-tenant access succeeds, cross-tenant read and write requests fail,
and denial events are logged without sensitive payloads.
```

## Exercise 12: Mini project sample

For a local application, choose three areas:

1. **A01:** add a resource ownership check and a test that cross-tenant access is denied.
2. **A05:** replace string-built SQL with parameterized queries and add a regression test.
3. **A10:** make authorization dependency failure deny protected actions and add a timeout test.

For each, save the original test result, remediation commit, passing regression result, and remaining-risk note. Run scans only against the local project and its dependencies.

## Final rubric

A strong submission:
- Uses the correct OWASP Top 10:2025 category names.
- Explains root cause rather than only naming a symptom.
- Provides preventive controls and testable acceptance criteria.
- Includes negative and abnormal-condition tests.
- Maps security checks into CI/CD and runtime operations.
- Protects real credentials and personal data in evidence.
