# Security Architecture Review — Examples

These examples are illustrative. Adapt findings and control choices to the real architecture, risk appetite, and applicable requirements.

## Example 1 — Three-tier web application

### Proposed architecture

```text
[Browser]
    |
    | HTTPS
    v
[Public Load Balancer / WAF]
    |
    v
[Web/API Service] -----> [Identity Provider]
    |
    | private network, service identity required
    v
[Database]
    |
    v
[Encrypted Backup Store]

[CI/CD Pipeline] ---- deployment identity ----> [Runtime Environment]
```

### Review questions

- Is the database unreachable from the public internet?
- Does the API authorize access to each record, not just authenticate the user?
- Are service identities and database credentials narrowly scoped?
- Can the deployment pipeline change production without appropriate review?
- Are backups encrypted, access-controlled, and restoration-tested?
- Are logs useful for investigations without recording credentials or sensitive payloads?

### Example findings

| ID | Finding | Risk rationale | Recommendation |
|---|---|---|---|
| AR-01 | Database network exposure is not documented | High uncertainty around a critical data store | Document and enforce private ingress from approved workloads only |
| AR-02 | API design checks login but not record ownership | Could allow cross-account access | Define server-side object-level authorization and negative tests |
| AR-03 | CI/CD deploy identity has broad administrator permissions | Pipeline compromise could affect the entire environment | Scope permissions to required deployment operations and isolate environments |
| AR-04 | Backup restoration is not tested | Recovery capability is uncertain | Establish restoration tests and protect backup access |

## Example 2 — Microservices and service-to-service trust

A system contains an API gateway, order service, payment service, message broker, and reporting service.

Review:
- Does each service authenticate callers, or does the design assume that internal network traffic is trusted?
- Can the reporting service access payment data it does not need?
- Are broker publish/consume permissions separated by topic or queue?
- Are messages validated and protected against unauthorized publication?
- Are retries safe and are duplicate events handled?
- Are trace IDs and security events available across asynchronous flows?

**Potential finding:** All services use a shared credential with broad access.

**Risk:** Compromise of one service could permit impersonation of others and increase blast radius.

**Recommendation:** Use distinct workload identities, narrowly scoped permissions, managed credential rotation, and explicit authorization for sensitive service calls.

**Acceptance criteria:** A service identity can perform only its documented actions; a test identity for one service is denied access to another service's restricted endpoint or message topic.

## Example 3 — SaaS integration review

A customer-support platform integrates with a third-party CRM using an API token.

| Review area | Weak design signal | Better design direction |
|---|---|---|
| Data sharing | All customer fields are copied by default | Share only required fields and document purpose |
| Credentials | One long-lived admin token is hard-coded | Use managed secret storage and a narrowly scoped integration identity |
| Network/API | Callback trusts source IP alone | Authenticate callbacks cryptographically or through an appropriate trusted mechanism |
| Authorization | All support agents can export all records | Enforce role- and record-level permissions |
| Lifecycle | No process to revoke access when integration is removed | Define ownership, rotation, revocation, and offboarding |
| Logging | Full tokens and customer payloads are recorded | Redact secrets and minimize sensitive event data |

Do not assume the vendor is secure simply because it is reputable. Review the data and access that the integration actually receives.

## Example 4 — Architecture decision record (ADR)

**Title:** Store uploaded documents in private object storage

**Context:** Users upload documents that may contain confidential information. The application needs scalable storage and controlled downloads.

**Decision:** Store objects in a private bucket/container. The API checks the authenticated user's permissions before issuing a short-lived download mechanism or streaming the file.

**Security considerations:**
- Storage is not publicly readable by default.
- Application and workload identities have least privilege.
- Object ownership and sharing permissions are stored and enforced server-side.
- Links, if used, have scoped access and a defined expiry/revocation strategy.
- Sensitive tokens are not written to logs.
- Uploads are scanned and served with safe content-handling controls.

**Alternatives considered:** Public object URLs; storing all files in the relational database; direct client access to storage.

**Trade-offs:** Short-lived links may be forwarded during their lifetime; direct API streaming can increase application load. These risks are documented and addressed in the threat model.

**Validation:** Cross-user access tests, private-storage policy checks, link-expiry tests, and log inspection.

## Example 5 — Finding record

```text
ID: AR-005
Title: No documented revocation behavior for service credentials
Domain: Identity and secrets
Status: Needs evidence
Evidence: Architecture notes do not define how credentials are revoked after compromise or service retirement
Threat scenario: A leaked credential remains usable after it should no longer be trusted
Impact: Unauthorized service access and potential data exposure
Likelihood rationale: Unknown until credential lifetime and access paths are confirmed
Recommendation: Define ownership, scope, rotation, emergency revocation, and monitoring
Acceptance criteria: A test or runbook demonstrates credential revocation and confirms the old credential is denied
Owner: Platform team
Due date: Set by project owner
Residual risk: Reassess after evidence is reviewed
```

Use “Needs evidence” when the control might exist but cannot be confirmed from available design material.

## Example 6 — Risk-based escalation

A team proposes a new public webhook endpoint that processes order events.

Escalate the review depth because it introduces a public entry point, third-party trust, and potentially consequential state changes.

Questions:
- How are event senders authenticated?
- Are signatures verified and replay handled?
- Are schemas and sizes bounded?
- Can repeated events create duplicate orders?
- Are retries, timeouts, and queue backlogs safe?
- What data is logged and who can inspect it?
- What happens when the upstream provider or message broker is unavailable?

Possible outputs: updated data-flow diagram, threat model, prioritized findings, specific security requirements, and tests for invalid signatures, replay, schema errors, duplicate events, and rate limits.

## Example 7 — Decision and exception record

**Gap:** A legacy integration cannot yet support the desired service identity.

A responsible exception should document:
- The exact control gap and affected data/operations
- Why the preferred control cannot currently be implemented
- Compensating controls and their limitations
- A named risk owner and required approval
- A time-bound remediation plan and review date
- Monitoring and conditions that trigger earlier reassessment

An exception is not a permanent substitute for a risk decision. Follow the organization's governance process.
