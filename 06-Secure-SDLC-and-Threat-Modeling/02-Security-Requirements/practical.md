# Practical Labs: Security Requirements

Use a fictional application or an authorized development environment. Do not test against systems without permission.

## Lab 1 — Rewrite vague requirements

Rewrite each statement into a specific, testable requirement with acceptance criteria:
1. The application must be secure.
2. Passwords must be strong.
3. Logs should be good.
4. The API should be protected from abuse.
5. Data must be encrypted.

For each, state scope, rationale, owner, and verification method.

## Lab 2 — Requirements from a threat model

Scenario: A customer portal lets users sign in, view invoices, update contact details, and download PDF statements. Support staff can access customer records through a separate admin interface.

Identify assets, trust boundaries, abuse cases, and at least eight security requirements. Include object-level authorization, session security, audit logging, data protection, rate limits, and support-staff least privilege.

## Lab 3 — Write acceptance criteria

For the requirement below, write at least five pass/fail criteria:

> The API shall enforce object-level authorization for all customer invoice operations.

Include read, update, delete/download if applicable, cross-account access, and error-data leakage.

## Lab 4 — Build a traceability matrix

Create a matrix connecting each requirement to:
- Requirement ID and version.
- Threat/risk or policy source.
- Design component.
- Implementation owner.
- Verification method and test ID.
- Evidence location.
- Status and release gate.

Populate at least five fictional requirements.

## Lab 5 — Prioritize requirements

Rank your requirements using impact, likelihood, exposure, and implementation dependencies. Define your ranking method and explain why the ranking is appropriate. Avoid relying on CVSS alone for system-level business priorities.

## Lab 6 — Review requirement quality

Review the examples in `examples.md`. For each, identify missing assumptions or decisions that a real team must settle, such as timeout values, TLS baseline, retention period, rate-limit thresholds, RPO/RTO, or exception authority.

## Lab 7 — Change control and exceptions

A team wants to defer an authentication requirement until after launch. Draft a change request that includes rationale, affected threats, temporary mitigations, test evidence, accountable risk owner, expiration date, monitoring, and remediation milestone.

## Lab 8 — Verification planning

Choose five requirements and specify whether each should be verified by unit test, integration test, dynamic test, configuration review, threat-model review, penetration test, or operational exercise. Explain why the method produces suitable evidence.

## Deliverables
- `security-requirements.md`
- `traceability-matrix.csv`
- `verification-plan.md`
- One documented exception/change request, if relevant.

## Completion checklist
- [ ] Requirements are specific, scoped, testable, and traceable.
- [ ] Acceptance criteria clearly define pass/fail.
- [ ] Threats and assets are linked to requirements.
- [ ] Verification evidence and owners are assigned.
- [ ] Exceptions have an accountable approver and expiry.
