# Security Review Checklists

## Overview
Security review checklists help reviewers consistently inspect design, code changes, configurations, dependencies, and release readiness. They support—not replace—threat modeling, security testing, and informed engineering judgment.

Use a risk-based approach: apply deeper review to authentication, authorization, sensitive data, cryptography, public interfaces, infrastructure-as-code, CI/CD, and trust-boundary changes.

## Learning objectives
- Prepare and scope a security review.
- Review application code and business logic for common security weaknesses.
- Assess APIs, identity, data handling, dependencies, cloud configuration, and CI/CD changes.
- Record evidence, findings, owners, severity, and retest results.
- Decide when a change needs security escalation before merge or release.

## Recommended review workflow
1. **Understand the change:** read the issue, acceptance criteria, diff, architecture, and relevant threat model.
2. **Identify risk areas:** new entry points, trust boundaries, sensitive data, privileged operations, dependencies, and deployment changes.
3. **Use relevant checklists:** select only the checklists that apply to the feature and technology.
4. **Trace data flows:** follow untrusted input through validation and processing to sensitive sinks.
5. **Verify controls:** inspect implementation and tests; do not treat comments or intended behavior as evidence.
6. **Record findings:** include affected component, evidence, impact, reproduction or validation steps, and remediation guidance.
7. **Agree on disposition:** fix, defer with authorized risk acceptance, or block merge/release according to policy.
8. **Retest and close:** confirm the fix and check for regressions.
9. **Improve the checklist:** add lessons from incidents and recurring findings.

## Checklist status labels
Use a consistent status for each item:
- `PASS` — verified with evidence.
- `FAIL` — a weakness or missing control was confirmed.
- `N/A` — not applicable; record a brief reason for important exclusions.
- `NEEDS-REVIEW` — insufficient evidence or follow-up required.

Avoid marking an item PASS merely because a scanner did not report an issue.

## Review areas
This module includes checklists for:
- Review preparation and architecture
- Input validation and injection
- Authentication and session management
- Authorization and object-level access
- API and business logic
- Sensitive data and cryptography
- Errors, logging, and monitoring
- Dependencies and software supply chain
- Cloud, containers, and infrastructure as code
- CI/CD and release security
- Final release readiness

## High-priority review triggers
Escalate for deeper security review when a change:
- Adds or changes authentication, session, authorization, or privilege logic.
- Exposes a new public endpoint or changes network exposure.
- Introduces a new external integration or data store.
- Handles payment data, credentials, tokens, health data, or other sensitive information.
- Changes cryptographic code, deserialization, file uploads, or URL fetching.
- Modifies build pipelines, deployment credentials, container images, or infrastructure permissions.
- Changes a security control, threat-model assumption, or a previously vulnerable component.

## Finding template
A useful finding includes:
- ID and title
- Affected component/file/endpoint
- Severity and rationale
- Preconditions and impact
- Evidence or safe reproduction steps
- Recommended remediation
- Owner and due date
- Retest result and closure evidence

## References
- OWASP Secure Code Review Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html
- OWASP DevSecOps Guideline — Secure Code Review: https://owasp.github.io/DevSecOpsGuideline/2-Process/2-2-Develop/2-2-3-Secure-Code-Review/
- OWASP Application Security Verification Standard (ASVS): https://asvs.owasp.org/
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
