# Security Requirements Review Checklist

## Scope and traceability
- [ ] System boundaries, actors, assets, and sensitive data are identified.
- [ ] Requirements link to threats, risks, policies, or business needs.
- [ ] Requirement IDs are unique, stable, and version-controlled.
- [ ] Dependencies and assumptions are documented.
- [ ] Requirements are mapped to design components and tests.

## Requirement quality
- [ ] Each requirement has clear scope and one primary obligation.
- [ ] Wording is specific and testable.
- [ ] Thresholds, timeouts, limits, and retention periods are explicit or assigned for resolution.
- [ ] Positive and negative behaviors are defined.
- [ ] Acceptance criteria provide objective pass/fail evidence.
- [ ] Rationale is separate from the mandatory requirement statement.

## Security coverage
- [ ] Authentication, account recovery, and session lifecycle are addressed.
- [ ] Authorization and least privilege are addressed.
- [ ] Data classification, minimization, protection, retention, and deletion are addressed.
- [ ] Input handling and output encoding are addressed.
- [ ] API abuse prevention and availability requirements are addressed.
- [ ] Security logging, monitoring, and auditability are addressed.
- [ ] Secrets, cryptographic keys, and dependencies are addressed.
- [ ] Backup, recovery, secure configuration, and patching are addressed.
- [ ] Privacy and regulatory obligations have been reviewed by appropriate stakeholders.

## Verification and ownership
- [ ] Each requirement has an accountable owner.
- [ ] Verification method and evidence location are specified.
- [ ] Test cases include abuse cases and negative cases where relevant.
- [ ] Mandatory release gates are explicit.
- [ ] Residual risks and exceptions are documented.

## Change management
- [ ] Requirements are reviewed when architecture or threats change.
- [ ] Exceptions have authorized approval, scope, expiry, and mitigation.
- [ ] Requirement changes are versioned and impact-assessed.
- [ ] Verification is repeated after relevant implementation changes.
