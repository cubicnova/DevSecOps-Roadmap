# Security Requirements

Learn how to define, document, validate, and maintain clear, testable security requirements throughout the software development lifecycle (SDLC).

## Learning objectives

- Distinguish functional, non-functional, security, privacy, and compliance requirements.
- Write security requirements that are specific, measurable, testable, and traceable.
- Derive requirements from assets, threats, abuse cases, data sensitivity, and business obligations.
- Define acceptance criteria and verification methods for each requirement.
- Connect requirements to design decisions, tests, risks, and release gates.
- Manage exceptions, requirement changes, and residual risk.

## Contents

- `examples.md` — sample requirements and acceptance criteria.
- `practical.md` — guided exercises for web apps, APIs, and deployment pipelines.
- `solutions.md` — example answers and requirement-writing patterns.
- `security-requirements-template.csv` — reusable requirements register.
- `requirements-review-checklist.md` — review checklist for requirements and traceability.

## What makes a good security requirement?

A useful requirement is:
- **Specific:** describes the expected behavior or control.
- **Testable:** a reviewer can determine pass/fail with evidence.
- **Traceable:** linked to a threat, risk, policy, or business need.
- **Scoped:** identifies the relevant component, data, user, or workflow.
- **Owned:** has an accountable role and an agreed verification method.
- **Maintainable:** versioned and revisited when the system or threat model changes.

Avoid vague statements such as “the application must be secure” or “use strong encryption.” Prefer requirements that specify protected data, required behavior, measurable conditions, and how compliance will be demonstrated.

## Common categories

- Authentication and identity lifecycle.
- Authorization and least privilege.
- Data classification, minimization, and protection.
- Session management and account recovery.
- Input validation and output encoding.
- API protection, rate limiting, and abuse prevention.
- Audit logging, monitoring, and alerting.
- Cryptographic key and secret management.
- Secure configuration, dependency management, and patching.
- Availability, resilience, backup, and recovery.
- Privacy, retention, deletion, and consent where applicable.
- Secure development, code review, testing, and release controls.

## Suggested workflow

1. Identify assets, users, data flows, trust boundaries, and business goals.
2. Review the threat model, abuse cases, policies, and applicable obligations.
3. Draft requirements using clear, testable language.
4. Define measurable acceptance criteria and verification evidence.
5. Assign owners, priority, and implementation/verification milestones.
6. Link requirements to design components, tests, and identified risks.
7. Review exceptions and residual risk with the authorized risk owner.
8. Revisit requirements when architecture, data, dependencies, or threats change.

## Requirement pattern

> The [system/component] shall [required behavior] for [scope/condition] within [measurable constraint], and compliance shall be verified by [test/evidence].

Example:

> The API shall deny requests for resources outside the authenticated user's authorized scope. Verification shall include automated negative tests using two separate test accounts and shall confirm that unauthorized requests return no protected resource data.

Use organization-approved policies and standards where applicable. A requirement should not claim regulatory compliance merely because one control has been implemented.

## References

- OWASP Application Security Verification Standard (ASVS): https://owasp.org/www-project-application-security-verification-standard/
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- NIST Secure Software Development Framework (SSDF), SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final
- NIST SP 800-160 Vol. 1, Systems Security Engineering: https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final
