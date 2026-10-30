# Security Architecture Review — Sample Solutions

These are example answers, not a substitute for examining the actual design. A finding's severity depends on evidence, system context, exposure, and existing controls.

## Exercise 1 — Prepare for a review

**Useful evidence**
1. System-context and component diagrams
2. Data-flow diagram with trust boundaries
3. Data classification and retention requirements
4. Threat model and abuse cases
5. Identity and authorization design
6. API contracts and integration inventory
7. Network and deployment topology
8. Secrets and key-management design
9. CI/CD permissions and release workflow
10. Logging, alerting, backup, and incident-response plans

**Likely assets:** personal data, uploaded documents, account credentials, session tokens, API secrets, order or business records, audit logs, and service availability.

**Questions before sign-off**
- Are all public endpoints and third-party data flows identified?
- Is authorization enforced for each object and operation?
- Are storage resources private by default?
- Can the CI/CD pipeline access only the resources required for its job?
- Can the team detect, investigate, and recover from a security incident?

A public API, new vendor, new sensitive data type, or changed trust boundary can justify a deeper threat model and specialist review.

## Exercise 2 — Review identity and authorization

**Concerns**
- Request-body `user_id` and `role` are untrusted inputs.
- The design does not establish a trusted link between the authenticated principal and requested resource.
- Authorization rules and denial behavior are unspecified.

**Threat scenarios**
1. A user changes `user_id` and accesses another user's record.
2. A user sets `role` to `admin` to invoke a privileged function.
3. A stale or revoked identity context remains accepted.

**Design changes**
- Validate authentication at the API boundary.
- Derive the caller's identity from the validated authentication context.
- Enforce object- and function-level authorization server-side.
- Define role/permission sources, token lifetime, revocation, and privileged-action controls.

**Acceptance criteria**
- Client-supplied identity or role fields cannot elevate permissions.
- Each protected request checks permissions for the requested object and action.
- Unauthenticated and unauthorized requests are denied consistently and logged appropriately.

**Tests:** An authorized user can access permitted data; a different test user is denied; a normal user cannot call an admin endpoint by altering JSON fields; revoked sessions are denied according to policy.

## Exercise 3 — Assess data protection

**Confirmed facts:** The architecture includes a database and object storage and handles personal data and uploaded documents.

**Not confirmed:** Encryption configuration, key ownership, retention, deletion, backup access, logging behavior, and restoration capability. Missing documentation is an evidence gap, not conclusive proof that controls are absent.

**Recommendations and evidence**
- **Classification:** Document data types, owners, purpose, and required protection.
- **Transit:** Define TLS requirements and verify endpoint configuration.
- **At rest:** Document storage encryption and key access; inspect configuration or provider evidence.
- **Key management:** Define key ownership, access, rotation, recovery, and emergency revocation.
- **Logging:** Redact credentials and sensitive payloads; inspect representative events.
- **Retention/deletion:** Define lifecycle rules and test deletion behavior across active storage and applicable copies.
- **Backups:** Restrict access, protect backup data, and run restoration tests.

Record unknowns with an owner, requested evidence, target date, and interim risk decision. Do not mark a control “Pass” without supporting evidence.

## Exercise 4 — Review a microservices design

**Principal weaknesses**
- Shared identity makes attribution and revocation difficult.
- Broad queue access violates least privilege.
- Unencrypted internal traffic increases exposure if a network segment or workload is compromised.
- Network location is treated as the only trust signal.

**Potential blast radius:** A compromised service may impersonate other services, read unrelated messages, and move laterally across the application.

**Recommendations**
- Use distinct workload identities and scoped permissions.
- Authenticate and authorize service-to-service calls.
- Encrypt traffic according to the system's threat model, including mTLS where appropriate.
- Separate network zones and restrict service-to-service paths.
- Give each service only the message topics and operations it needs.
- Monitor privileged access and identity use.

**Validation tests**
1. Service A is denied access to Service B's restricted API.
2. Service A cannot consume Service B's restricted queue.
3. Connections that violate required transport-security policy are rejected.
4. Revoking a workload identity prevents subsequent protected operations within the documented policy.

Prioritize shared credentials and broad cross-service access because they can amplify compromise across multiple components. Confirm exposure and existing compensating controls before assigning final severity.

## Exercise 5 — Review a CI/CD architecture

**Threats and boundaries**
- A compromised build job could read production secrets.
- A pipeline compromise could alter cloud permissions and take control of the environment.
- Shared credentials weaken environment isolation and complicate attribution.
- Direct production deployment may bypass required independent checks.

**Recommendations**
- Use separate identities and permissions for development and production.
- Scope each job to the resources and actions it needs.
- Avoid exposing production secrets to untrusted pull requests or unrelated build jobs.
- Require protected deployment environments and independent approval for high-impact changes where appropriate.
- Protect artifacts, pin or verify dependencies where feasible, and preserve deployment provenance.
- Audit and rotate pipeline credentials.

**Sample finding**

**Title:** CI/CD deployment identity has excessive production privileges.

**Evidence:** Pipeline identity can read all production secrets and modify IAM policies; the same credential is used in development and production.

**Threat scenario:** A compromised repository or build job can obtain production secrets and modify permissions, enabling a broader compromise.

**Recommendation:** Separate environments, use narrowly scoped deployment identities, and restrict IAM changes to an approved workflow.

**Acceptance criteria:** Development jobs cannot access production secrets; deployment identity can perform only documented release actions; privileged IAM changes require the approved workflow; automated tests or configuration evidence demonstrate the restrictions.

## Exercise 6 — Rate findings

Provisional ratings depend on system context. A possible qualitative assessment:

| Finding | Example provisional rating | Rationale |
|---|---|---|
| A: Object-level authorization undocumented | High / Needs evidence | Potential cross-user data exposure; confirm the actual enforcement and sensitivity of data |
| B: Missing correlation IDs | Low–Medium | May reduce investigation quality, but impact depends on logging architecture and criticality |
| C: Production secret accessible to every CI job | High | Broad access can turn a lower-trust job compromise into production compromise |
| D: Backup restoration never tested | Medium–High | Recovery is uncertain; severity depends on business criticality and recovery objectives |

Findings A and C deserve prompt escalation for evidence and mitigation planning. D may also be urgent for a critical service. B should be assessed against investigation and audit requirements.

Evidence that could change ratings includes actual policy/configuration, data sensitivity, network exposure, compensating controls, reproducible tests, blast radius, and business recovery objectives.

## Exercise 7 — Produce an architecture review report

A complete report should let another reviewer understand:
- What was reviewed and what was out of scope
- Which architecture artifacts and evidence were examined
- What assumptions and gaps remain
- How a design gap could create a concrete threat scenario
- Why each finding received its severity
- What action will resolve or reduce the risk
- How the team will prove the action is effective
- Who owns the decision and when it must be revisited

Avoid findings that only say “use best practices.” Tie each recommendation to the system's architecture and a measurable outcome.

## Exercise 8 — Review a proposed architecture change

**Changed boundaries:** private network to public API, plus a new third-party trust relationship.

**Review topics**
- Authentication for external callers and service identity for vendor callbacks
- Server-side authorization and permission scope
- API schemas, input limits, rate limits, quotas, and safe error handling
- Data minimization and vendor data-use constraints
- Credential storage, rotation, and revocation
- Logging, alerting, and incident response for the integration
- Failure behavior, retries, duplicate requests, and service availability

**Required updates:** system diagram, data-flow diagram, threat model, integration inventory, security requirements, and operational runbooks.

**Tests:** unauthenticated requests, invalid credentials, insufficient permissions, malformed payloads, rate limits, replay/duplicate events, dependency failure, secret rotation, and monitoring alerts.

Before production release, resolve or formally approve material findings, assign owners and due dates for remaining work, and verify critical controls with evidence.

## Further reading

- [OWASP Secure by Design Framework](https://owasp.org/projects/secure-by-design-framework)
- [OWASP SAMM — Secure Architecture](https://owaspsamm.org/model/design/secure-architecture/)
- [OWASP SAMM — Architecture Assessment](https://owaspsamm.org/model/verification/architecture-assessment/)
- [Microsoft Azure Well-Architected Framework — Security checklist](https://learn.microsoft.com/en-us/azure/well-architected/security/checklist)
