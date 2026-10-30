# Examples: Writing Security Requirements

These are adaptable examples, not universal compliance statements. Tailor them to the system, threat model, risk appetite, and applicable policies.

## 1. Authentication

**Vague:** The system must have secure login.

**Testable requirement:** The application shall authenticate users through the approved identity service and shall not issue an authenticated session until all required authentication checks have succeeded.

**Acceptance criteria**
- Invalid credentials do not establish an authenticated session.
- Authentication errors do not reveal whether a username exists.
- Automated tests verify success, failure, lockout/rate-limit behavior, and session creation.
- Authentication events are logged without recording passwords, one-time codes, or tokens.

## 2. Authorization and object-level access

**Requirement:** For every request that reads or changes a protected object, the API shall verify that the authenticated principal is authorized for that specific object and action.

**Acceptance criteria**
- Tests use at least two users with separate test-owned records.
- User A cannot read, update, or delete User B's protected record by changing an identifier.
- Negative tests confirm that unauthorized responses do not disclose protected fields.
- Authorization is enforced server-side, not only by hiding UI controls.

## 3. Data in transit

**Requirement:** External connections carrying credentials, session material, or sensitive application data shall use approved TLS configurations and reject invalid certificates.

**Acceptance criteria**
- Automated configuration tests validate the supported TLS policy.
- Invalid, expired, or untrusted certificates are not silently accepted.
- Secrets are not sent in URLs or written to connection-debug logs.
- Exceptions are documented and approved through the designated process.

## 4. Data at rest and key management

**Requirement:** Sensitive data stored by the system shall be protected using organization-approved encryption or equivalent controls, with keys managed separately from the protected data.

**Acceptance criteria**
- Data inventory identifies which stores contain sensitive data.
- Storage configuration and key-management permissions are reviewed.
- Tests or configuration evidence demonstrate the approved protection is enabled.
- Key access and rotation responsibilities are documented.

Avoid prescribing a cryptographic algorithm without considering the organization's approved cryptographic baseline and platform capabilities.

## 5. Session management

**Requirement:** The application shall invalidate a session on logout and enforce configured idle and absolute session timeouts.

**Acceptance criteria**
- A logged-out session cannot be reused.
- Expired sessions cannot access protected endpoints.
- Session identifiers are not placed in URLs or logs.
- Timeout values are specified by policy and tested in the relevant user flows.

## 6. Audit logging

**Requirement:** The system shall record security-relevant authentication, authorization, privilege-change, and administrative events with a UTC timestamp, event type, outcome, actor/context where available, and correlation ID.

**Acceptance criteria**
- Tests verify that the required events are emitted.
- Logs contain no passwords, bearer tokens, session cookies, or private keys.
- Access to logs is restricted and audited.
- Collection failures trigger a defined operational response.

## 7. Input handling

**Requirement:** Data received from untrusted sources shall be validated against an explicit schema and contextually encoded or parameterized before use in interpreters, queries, or rendered output.

**Acceptance criteria**
- Negative tests cover malformed, unexpected, oversized, and boundary values.
- Database operations use parameterized queries or safe ORM operations.
- HTML output is contextually encoded.
- Validation errors do not disclose stack traces or sensitive implementation details.

## 8. API abuse protection

**Requirement:** Sensitive or resource-intensive API operations shall enforce documented request limits and return a consistent response when limits are exceeded.

**Acceptance criteria**
- Limits are specified per user, token, IP, or other suitable identity/context.
- Tests demonstrate that the limit is enforced under the defined conditions.
- Limit events are observable and do not expose secrets.
- Limits are reviewed against legitimate traffic and abuse scenarios.

## 9. Dependency and build integrity

**Requirement:** Production builds shall use approved dependency sources and shall evaluate dependency vulnerabilities against the organization's severity and remediation policy before release.

**Acceptance criteria**
- Dependency inventory or lockfile is generated and reviewed.
- Automated scanning runs in the build pipeline.
- Policy violations fail the release or require an approved, time-bound exception.
- Build artifacts and deployment provenance are retained as required.

## 10. Backup and recovery

**Requirement:** Critical application data shall be backed up according to the approved recovery objectives, and restoration shall be tested at a defined interval.

**Acceptance criteria**
- Recovery point objective (RPO) and recovery time objective (RTO) are documented.
- Backup access is restricted and backup data is protected.
- A restoration exercise records duration, data integrity, and issues.
- Recovery failures have an assigned owner and remediation plan.

## 11. Requirement traceability example

| Requirement ID | Threat/risk | Requirement | Verification |
|---|---|---|---|
| SEC-AUTH-01 | Credential stuffing | Authentication endpoints shall enforce approved rate limits and risk-based controls. | Automated load/limit tests and configuration review |
| SEC-ACC-02 | IDOR/BOLA | Every object access shall enforce server-side object-level authorization. | Two-user negative authorization tests |
| SEC-LOG-03 | Weak investigation trail | Security events shall include UTC timestamp, event, outcome, and correlation ID. | Integration tests and sample-log review |
| SEC-DEP-04 | Vulnerable dependency | CI shall scan production dependencies and enforce the approved policy. | Pipeline test with a known test fixture |

## Writing tips

- Use “shall” for mandatory requirements if that matches your organization's convention.
- Keep one main obligation per requirement where possible.
- Separate the requirement from its rationale and its verification procedure.
- Avoid prescribing an implementation unless it is necessary or mandated.
- Define thresholds and timeouts explicitly rather than saying “fast,” “strong,” or “regular.”
- Mark assumptions and dependencies; do not invent legal or compliance obligations.
