# Security Design Patterns — Sample Solutions

These are model answers, not the only acceptable designs. A production solution should be adapted to the application's threat model, regulatory obligations, platform, and operational requirements.

## Exercise 1: Identify the pattern

1. **Administrator service account:** least privilege; workload identity; scoped permissions. Reduce permissions and separate unrelated duties.
2. **Authorization timeout grants access:** fail-secure behavior. Deny the protected operation when authorization cannot be confirmed; log and monitor the failure.
3. **Cross-tenant object access:** complete mediation and resource-level authorization. Check tenant ownership and permission for each request.
4. **Credential committed to Git:** secrets management. Revoke and rotate the credential, remove exposure from artifacts/history where appropriate, and prevent recurrence with secret scanning.
5. **Unlimited OTP attempts:** rate limiting and abuse monitoring. Add risk-aware throttling and alerting while considering shared-IP and account-lockout abuse.
6. **One person controls all release stages:** separation of duties. Add protected branches, independent approval, scoped deploy identities, and audit trails.
7. **Unlimited request body:** resource controls. Enforce size and time limits at the edge and application layer; monitor rejection rates.
8. **Stack traces and connection strings exposed:** fail-secure error handling and data minimization. Return generic errors and restrict diagnostic details to protected logs.

## Exercise 2: Secure document API requirements

Example requirements:

1. All interactive users authenticate through an approved identity provider; privileged tenant-administration actions require MFA.
2. Every document read, update, and delete checks the authenticated principal's tenant and permission on the server.
3. Missing, invalid, or unavailable authorization decisions deny the protected action.
4. The report worker uses a dedicated workload identity with read access to required document metadata and write access only to its report status.
5. All external and service-to-service traffic uses appropriately validated TLS; stored confidential documents use approved encryption and key-management controls.
6. Secrets are retrieved at runtime from an approved secrets manager and are never committed to source control or written to application logs.
7. Login, password reset, document export, and expensive search operations have abuse controls with monitored rejection and failure rates.
8. Audit events record actor, action, target identifier, outcome, timestamp, and correlation ID without recording document contents, tokens, or credentials.
9. User-facing errors do not expose stack traces or infrastructure details; diagnostic logs have restricted access and defined retention.
10. Automated tests verify cross-tenant denial, expired-token rejection, role restrictions, and safe behavior when identity or policy dependencies fail.

Each requirement can be mapped to a test, configuration check, log event, or review artifact.

## Exercise 3: Gateway-only authorization

**Weaknesses**
- A private network is treated as proof of caller identity.
- A client-influenced or improperly protected role header may be spoofed.
- Services may have no object-level or tenant-level authorization.
- A future route or network change could bypass the gateway.
- A compromised internal service may impersonate another user.

**Safer model**
- Authenticate callers at the gateway and establish a verifiable identity context.
- Strip untrusted identity headers at the edge and create trusted metadata only through a protected mechanism.
- Authenticate service-to-service calls and restrict network paths.
- Each service validates the identity context and enforces its own resource-level authorization.
- Use policy libraries or a policy service consistently, with explicit failure behavior.

**Gateway responsibilities:** TLS termination policy, token validation where appropriate, request limits, routing, coarse-grained access controls, and observability.

**Service responsibilities:** business rules, resource ownership, tenant boundaries, action-level authorization, and safe data access.

**Negative tests**
1. A caller submits a forged `X-User-Role: admin` header; the service must not grant elevated access.
2. A valid user token attempts to access another tenant's document; the service denies access.
3. The policy dependency times out; the protected action is denied and an event is recorded.

## Exercise 4: Pattern trade-offs

- **Central identity provider:** improves consistency and lifecycle management. It introduces a dependency that needs resilience planning. A custom solution is rarely justified unless there is a compelling, reviewed requirement.
- **Fail-closed authorization:** protects confidentiality and integrity during dependency failure but may reduce availability. Define timeouts, safe retries, alerting, and recovery; do not silently allow protected actions.
- **API gateway:** centralizes edge policy and visibility but adds operational complexity and can become a bottleneck or concentration of risk. Keep downstream services protected and independently authorized.
- **Synchronous policy lookup:** can provide fresh decisions but adds latency and dependency risk. Caching may improve availability, but stale decisions can preserve revoked access; define cache lifetime and invalidation requirements.
- **Static secret versus workload identity:** short-lived identity reduces secret distribution and rotation burden when supported. Static credentials may remain necessary for some integrations, but must be scoped, protected, audited, and rotated.

Choices should be based on risk, platform capability, latency, availability, and evidence—not convenience alone.

## Exercise 5: Sample ADR

```markdown
# ADR-007: Use an approved secrets manager

## Status
Accepted

## Context
Several services need database and third-party API credentials. Storing
secrets in source control or container images increases exposure risk.

## Decision
Use the approved secrets manager with workload-specific access policies.
Services retrieve only the credentials they require at runtime.

## Alternatives considered
- Environment-specific files distributed manually.
- Encrypted values committed to source control.
- A shared secret copied to all workloads.

## Security consequences
- Reduces secret sprawl and enables access auditing.
- Does not prevent exposure if a workload with access is compromised.
- Access policies, rotation, and log redaction remain necessary.

## Operational consequences
- Runtime dependency and access-policy management are required.
- Availability and recovery procedures must be documented.

## Validation plan
- Verify each workload can retrieve only its intended secret.
- Confirm unauthorized identities are denied.
- Scan source, images, and logs for exposed values.
- Test rotation and recovery procedures.
```

## Exercise 6: Security test plan

| Test | Expected result | Evidence |
|---|---|---|
| Same-tenant authorized read | Allowed | Test response and audit event |
| Cross-tenant read/write | Denied | Denial result and security event |
| Expired or invalid token | Rejected | Authentication failure log |
| Read-only user deletes document | Denied | Authorization test result |
| Policy service times out | Protected action denied | Correlated error and alert |
| Oversized request | Rejected within defined limits | Response and metrics |
| Rate limit exceeded | Throttled according to policy | Counter, response, alert if applicable |
| Bearer token in logs | No token value appears | Log inspection / automated assertion |
| Duplicate sensitive request | Business operation occurs at most once for the same idempotency key | Stored state and transaction/test evidence |

Use non-production test data and avoid placing actual secrets in test fixtures.

## Exercise 7: Prioritized remediation

**Immediate containment**
1. Restrict public database access to approved network paths.
2. Revoke and rotate the hardcoded API key.
3. Disable production debug output.
4. Prevent further token logging and restrict access to existing logs; handle retained sensitive data under incident procedures.

**Architecture changes**
5. Introduce server-side resource authorization and tenant isolation.
6. Replace the broad shared account with workload-specific identities and minimal permissions.
7. Store secrets in an approved manager and establish rotation and access auditing.
8. Apply TLS, network segmentation, request limits, and safe error handling as appropriate.

**Verification and operations**
9. Add tests for authorization denials, secret exposure, and configuration drift.
10. Scan repository history, images, artifacts, and logs for exposure.
11. Assign owners, deadlines, and residual-risk acceptance; monitor for misuse of the exposed credential.

Priorities can change if evidence shows active exploitation or specific business-critical exposure.

## Exercise 8: Pattern limitations

Examples:

- **API gateway:** centralizes edge controls, but cannot reliably decide every object-level business permission by itself. A bypass route or overtrusted internal service can defeat the design. Test direct service access and cross-tenant operations.
- **Secrets manager:** reduces secret sprawl but cannot protect a secret from a workload that is legitimately authorized and compromised. Test access boundaries, rotation, and secret redaction.
- **Rate limiting:** slows automated abuse but does not prove a request is legitimate; distributed traffic and shared IPs complicate enforcement. Monitor limit hits, account recovery failures, and false-positive impact.

## Exercise 9: Password-reset abuse

**Assets:** account identifiers, reset tokens, email delivery capacity, support resources, and user privacy.

**Threats:** account enumeration, automated reset floods, token guessing/replay, and denial of service.

**Controls:** consistent user-facing responses, cryptographically random short-lived single-use reset tokens, rate limiting, monitoring, safe token storage, and minimal exposure of identity data. Avoid revealing account existence in response content or timing where practical.

**Trade-offs:** aggressive throttling can affect users behind shared networks or allow attackers to lock out victims. Prefer layered, risk-aware limits and avoid destructive account lockout behavior.

**Tests:** compare responses for existing and nonexistent accounts; test token expiry and reuse; simulate bursts; verify tokens are absent from logs; confirm alerts fire for unusual patterns.

## Exercise 10: Mini design review

A reasonable design includes:
- Browser-to-application traffic protected by TLS.
- An approved identity provider for authentication.
- API authorization for each operation and resource.
- Database reachable only from the application and using scoped credentials.
- Background worker with a separate workload identity and narrow permissions.
- Secrets manager for credentials and key access.
- Structured security logs with sensitive-field redaction.
- Rate limits for authentication and expensive endpoints.
- Explicit behavior for identity, policy, and database failures.
- Negative tests for cross-user access and privilege escalation.

For each control, name an owner (for example, application team, platform team, or security engineering) and define evidence such as automated test output, policy configuration, or monitored security events.

## Final review rubric

A strong submission:
- Distinguishes identity verification from authorization.
- Identifies trust boundaries and realistic abuse cases.
- Chooses patterns that address the stated risks.
- Documents failure modes and operational trade-offs.
- Provides testable requirements and negative tests.
- Avoids claiming that a single product or pattern guarantees security.
