# Security Architecture Review — Exercises

Use fictional systems or architecture documents you are authorized to assess. Record unknowns as evidence gaps instead of assuming a control exists or is absent.

## Exercise 1 — Prepare for a review

A team is building a web application with a public API, identity provider, relational database, object storage, third-party email service, and CI/CD pipeline.

Tasks:
1. List at least eight artifacts or pieces of evidence to request.
2. Identify the system's likely high-value assets.
3. Draw or describe the main data flows and trust boundaries.
4. List five questions that must be answered before sign-off.
5. Identify two changes that should trigger a deeper review.

## Exercise 2 — Review identity and authorization

The design says: “Users log in through the identity provider. The API receives `user_id` and `role` fields in the request and uses them to decide what records the user can access.”

Tasks:
1. Identify architecture-level concerns.
2. Describe at least three threat scenarios.
3. Recommend design changes.
4. Write three acceptance criteria.
5. Propose positive and negative tests.

## Exercise 3 — Assess data protection

An application stores personal data and uploaded documents. The diagram shows object storage and a database, but does not specify encryption, retention, deletion, backup access, or logging.

Tasks:
1. Separate confirmed facts from missing evidence.
2. List questions about data classification and ownership.
3. Recommend controls for transit, storage, keys, logs, retention, and backups.
4. Define validation evidence for each recommendation.
5. Explain how you would record residual uncertainty.

## Exercise 4 — Review a microservices design

A system uses five services. All services share one API token and can read from every message queue. Internal traffic is unencrypted because “it stays inside the VPC.”

Tasks:
1. Identify the principal architecture weaknesses.
2. Explain the likely blast radius of a compromised service.
3. Recommend identity, authorization, communication, and segmentation controls.
4. Define four validation tests.
5. Prioritize the findings with a rationale.

## Exercise 5 — Review a CI/CD architecture

The deployment pipeline can read all production secrets, modify cloud IAM policies, and deploy directly to production. The same credential is used in development and production.

Tasks:
1. Identify threats and trust boundaries.
2. Recommend least-privilege and environment-separation changes.
3. Explain where approval or separation of duties may be appropriate.
4. Define artifact-integrity and deployment validation checks.
5. Draft a concise finding with acceptance criteria.

## Exercise 6 — Rate findings

Use your organization's severity model if available. Otherwise, use a documented qualitative rationale.

| Finding | Context |
|---|---|
| A | Public API does not document object-level authorization |
| B | Audit events omit correlation IDs |
| C | Production secret is accessible to every CI job |
| D | Backup restoration has never been tested |

Tasks:
1. Give each finding a provisional severity.
2. Explain impact, exposure, and uncertainty.
3. Identify which findings require immediate escalation.
4. State what evidence could change your assessment.
5. Avoid treating provisional severity as proof of exploitability.

## Exercise 7 — Produce an architecture review report

Choose a fictional system: online checkout, document-sharing service, SaaS integration, or internal admin portal.

Your report must include:
- Scope and review date
- Architecture summary and trust boundaries
- Key assets and security objectives
- Threat model and assumptions
- Checklist results with evidence
- At least five findings
- Risk rationale and specific recommendations
- Acceptance criteria, owners, and target dates
- Exceptions and residual-risk decisions
- Required validation and follow-up review triggers

## Exercise 8 — Review a proposed architecture change

A service that previously accepted requests only from a private network will expose a public API and integrate with a new vendor.

Tasks:
1. Identify changed trust boundaries and entry points.
2. Review authentication, authorization, data minimization, and vendor access.
3. Identify required updates to the threat model and data-flow diagram.
4. Propose tests for abuse, failure, and recovery conditions.
5. Decide what must be completed before production release.

## Self-review checklist

- [ ] Scope and system boundaries are explicit.
- [ ] Findings distinguish evidence from assumptions.
- [ ] Threat scenarios explain how a design gap could cause harm.
- [ ] Recommendations are actionable and proportionate.
- [ ] Acceptance criteria can be tested or evidenced.
- [ ] Owners and due dates are assigned.
- [ ] High-risk exceptions are approved and time-bound.
- [ ] Review triggers and follow-up responsibilities are documented.
