# Security Architecture Review

Learn how to review application and infrastructure architecture for security weaknesses before implementation, during significant changes, and as part of ongoing assurance.

## Learning objectives

By completing this module, you should be able to:

- Explain the purpose and scope of a security architecture review.
- Gather architecture diagrams, data flows, threat models, security requirements, and design decisions.
- Review trust boundaries, identity, authorization, data protection, secrets, dependencies, deployment, resilience, and monitoring.
- Identify architecture-level anti-patterns and record evidence-based findings.
- Rate findings by risk and distinguish design gaps from implementation defects.
- Recommend practical mitigations and define validation criteria.
- Produce a review report with decisions, owners, due dates, and residual-risk acceptance.
- Decide when a change needs a deeper threat model or specialist review.

## What is a security architecture review?

A security architecture review evaluates whether a system's design, components, integrations, and operating model meet security objectives and address relevant threats. It should occur early enough for design changes to remain practical and should be revisited when important features, dependencies, trust boundaries, or deployment patterns change.

A review is not simply a vulnerability scan, code review, compliance checklist, or penetration test. Those activities can provide useful evidence, but architecture review asks whether the system has been designed with appropriate security properties and whether its controls fit together.

## Inputs to collect

- System purpose, business context, data classification, and security requirements
- Current and proposed architecture diagrams
- Data-flow diagrams and trust boundaries
- Threat model, abuse cases, and risk register
- Identity, authentication, authorization, and session design
- API contracts and third-party integration inventory
- Network zones, ingress/egress paths, and deployment topology
- Data storage, encryption, retention, deletion, and key-management design
- CI/CD pipeline, infrastructure-as-code, secret-management, and software supply-chain design
- Logging, alerting, incident response, backup, recovery, and availability plans
- Relevant standards, policies, and regulatory obligations

If key evidence is missing, record it as an assumption or evidence gap rather than silently treating the control as implemented.

## Review workflow

1. **Set scope:** agree on systems, environments, data, interfaces, reviewers, and out-of-scope areas.
2. **Understand the design:** identify components, data stores, actors, flows, trust boundaries, and external dependencies.
3. **Confirm security objectives:** identify confidentiality, integrity, availability, privacy, accountability, and business requirements.
4. **Review design domains:** assess identity, authorization, data, network boundaries, dependencies, resilience, monitoring, and operational controls.
5. **Use threat-driven analysis:** compare the architecture with threat models and abuse cases; ask what happens when a component or credential is compromised.
6. **Record findings:** state evidence, threat scenario, impact, likelihood rationale, and affected requirements.
7. **Recommend mitigations:** prefer specific design changes with clear acceptance criteria.
8. **Agree on decisions:** assign owners, due dates, and treatment of residual risk.
9. **Validate:** identify architecture tests, configuration checks, negative tests, or operational evidence.
10. **Revisit:** review significant changes and verify that accepted mitigations were completed.

## Core architecture principles

| Principle | Review question |
|---|---|
| Least privilege | Does each user, service, workload, and pipeline have only the permissions it needs? |
| Defense in depth | Would one control failure immediately expose a critical asset? |
| Secure defaults | Are new deployments private and hardened by default? |
| Explicit trust boundaries | Are external, internal, administrative, and third-party boundaries visible and enforced? |
| Fail securely | Does a failed authentication, authorization, or dependency check fail in a safe way? |
| Minimize attack surface | Are unnecessary endpoints, ports, services, permissions, and data flows removed? |
| Separation of duties | Are sensitive actions protected against unilateral misuse where required? |
| Data minimization | Is only necessary data collected, shared, and retained? |
| Observability | Can security-relevant actions and failures be investigated without logging secrets? |
| Resilience | Are timeouts, quotas, safe retries, recovery, and degraded modes designed? |

## Architecture review checklist

Use this as a starter checklist. Mark each item **Pass**, **Gap**, **Not applicable**, or **Needs evidence** and record the rationale. Tailor it to the system and organizational baseline.

### 1. Scope and boundaries
- [ ] System context, components, and owners are documented.
- [ ] Data flows and trust boundaries are accurate.
- [ ] Public endpoints and administrative interfaces are identified.
- [ ] Third-party services and data-sharing relationships are inventoried.
- [ ] Threat model and abuse cases reflect the proposed design.

### 2. Identity and access control
- [ ] Authentication requirements and identity sources are explicit.
- [ ] Authorization is enforced server-side for every operation and resource.
- [ ] Privileged actions use appropriate MFA or step-up verification.
- [ ] Service-to-service identities are distinct and verifiable.
- [ ] Permissions follow least privilege and have an ownership/review process.
- [ ] Session, token expiry, revocation, and recovery behavior are defined.

### 3. Data protection
- [ ] Data is classified and has an accountable owner.
- [ ] Encryption in transit and at rest is designed for applicable data.
- [ ] Key generation, storage, access, rotation, and recovery are defined.
- [ ] Secrets are stored in an appropriate secret manager, not code or logs.
- [ ] Retention, deletion, backup, and data residency requirements are addressed.
- [ ] Sensitive fields are minimized or redacted in logs, analytics, and errors.

### 4. Network and service boundaries
- [ ] Network exposure and ingress/egress paths are justified.
- [ ] Internal services authenticate and authorize callers.
- [ ] Cross-zone traffic uses governed paths and required encryption.
- [ ] Administrative access is restricted and auditable.
- [ ] Segmentation limits lateral movement and blast radius.

### 5. APIs and integrations
- [ ] API contracts, authentication, authorization, and versioning are defined.
- [ ] Input and output schemas are validated at trust boundaries.
- [ ] Rate limits, quotas, timeouts, and pagination limits are considered.
- [ ] Third-party credentials and permissions are narrowly scoped.
- [ ] Webhooks, callbacks, and asynchronous messages are authenticated and validated.
- [ ] Duplicate requests and retries cannot create unsafe state changes.

### 6. Dependencies and delivery pipeline
- [ ] Dependencies have a documented purpose and maintenance strategy.
- [ ] Build and deployment identities have least privilege.
- [ ] Secrets are not exposed in CI logs or artifacts.
- [ ] Infrastructure-as-code and deployment configuration are reviewed.
- [ ] Artifact provenance, integrity, and release permissions are addressed.
- [ ] Security checks cover relevant source, dependency, container, and configuration risks.

### 7. Resilience and operations
- [ ] Timeouts, retry policies, circuit breakers, and resource limits are defined.
- [ ] Backups are protected and restoration is tested.
- [ ] Security logging and actionable alerting are designed.
- [ ] Incident response roles, evidence handling, and escalation paths are documented.
- [ ] Recovery objectives and critical dependency failures are considered.
- [ ] Security-relevant configuration drift can be detected.

### 8. Assurance and governance
- [ ] Security requirements are traceable to controls and tests.
- [ ] Findings have owners, due dates, and risk treatment.
- [ ] High-risk exceptions have explicit approval and expiry/review dates.
- [ ] Architecture decisions and their trade-offs are documented.
- [ ] Review triggers and maintenance ownership are defined.

## Finding severity and report quality

Use the organization's risk method if available. A training report can use Critical, High, Medium, Low, and Informational, but must define what those labels mean locally.

A finding should include:
- **Title and ID**
- **Evidence:** diagram, design statement, configuration, or unanswered question
- **Threat scenario:** what could happen and under what conditions
- **Impact:** affected asset and business consequence
- **Likelihood rationale:** exposure, prerequisites, existing controls, and uncertainty
- **Recommendation:** specific design change or decision
- **Acceptance criteria:** how reviewers can verify the fix
- **Owner and due date**
- **Residual risk and approval**, if applicable

Avoid claiming a vulnerability is confirmed when the review only identifies a design risk or missing evidence.

## Example finding

**Finding:** Internal service trusts caller-supplied user identity.

**Evidence:** The design shows the API forwarding a `user_id` from the request body to the document service, with no documented authorization check.

**Threat scenario:** A valid low-privilege user changes the identifier and requests another user's document.

**Impact:** Unauthorized disclosure of confidential documents.

**Recommendation:** Derive identity from a validated authentication context and enforce object-level authorization in the service that owns the resource.

**Acceptance criteria:** Automated tests show that an authenticated user can access permitted documents but cannot read or modify documents outside their permissions.

**Status:** Open until the design change and validation evidence are reviewed.

## Useful references

- [OWASP Secure by Design Framework](https://owasp.org/projects/secure-by-design-framework)
- [OWASP Developer Guide — Design](https://devguide.owasp.org/en/04-design/)
- [OWASP SAMM — Secure Architecture](https://owaspsamm.org/model/design/secure-architecture/)
- [OWASP SAMM — Architecture Assessment](https://owaspsamm.org/model/verification/architecture-assessment/)
- [Microsoft Azure Well-Architected Framework — Security checklist](https://learn.microsoft.com/en-us/azure/well-architected/security/checklist)

## Responsible practice

Architecture review is a defensive design activity. Use authorized diagrams, configurations, and test environments. Protect architecture artifacts because they may contain sensitive system details, trust boundaries, and dependency information.
