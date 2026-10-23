# 01 - Secure Software Development Life Cycle (Secure SDLC)

Secure SDLC integrates security activities into every phase of software development so risks are identified and addressed early, rather than left until release or incident response.

**Repository path:** `06-Secure-SDLC-and-Threat-Modeling/01-Secure-SDLC/`

## Learning objectives

By completing this module, you should be able to:

- Describe the phases of an SDLC and where security fits into each phase.
- Define security requirements and acceptance criteria before implementation.
- Apply threat modeling and risk-based design review.
- Integrate code review, SAST, SCA, secret scanning, DAST, and infrastructure scanning into delivery workflows.
- Establish release gates, vulnerability handling, and security verification.
- Collect evidence and improve the development process over time.

## 1. What is Secure SDLC?

A Software Development Life Cycle (SDLC) defines how software is planned, designed, built, tested, released, operated, and retired. A **Secure SDLC** adds security requirements, risk analysis, verification, and feedback to those activities.

Security is a shared responsibility among product owners, developers, architects, security teams, QA, platform engineers, and operations. The exact activities vary by risk, system type, regulatory needs, and delivery model.

### Why shift security left?

Finding design flaws early is often less expensive than fixing them after deployment. However, security does not end at release: monitoring, patching, incident learning, and retirement remain important.

## 2. SDLC phases and security activities

| Phase | Security activities | Example evidence |
|---|---|---|
| Planning and requirements | Identify data, users, trust boundaries, abuse cases, legal obligations, and security objectives | Security requirements, risk register, acceptance criteria |
| Architecture and design | Threat modeling, trust-boundary review, secure design patterns, authentication/authorization design | Architecture diagram, threat model, design review |
| Development | Secure coding, peer review, secrets handling, dependency hygiene | Pull requests, coding checklist, secret-scan results |
| Build and integration | SAST, SCA, secret scanning, IaC checks, build provenance and artifact controls | Pipeline results, dependency inventory, build logs |
| Verification and testing | Security test cases, DAST, API tests, configuration review, penetration testing where appropriate | Test report, defect tickets, retest evidence |
| Release and deployment | Approval gates, least-privilege deployment identity, secure configuration, rollback plan | Release approval, deployment logs, configuration checks |
| Operations and maintenance | Monitoring, patching, vulnerability triage, access review, incident response, backup/recovery testing | Alerts, remediation records, incident exercises |
| Retirement | Revoke credentials, remove endpoints, archive or dispose of data securely, decommission assets | Decommission checklist, access revocation evidence |

## 3. Security requirements

Security requirements should be specific, testable, and linked to business risks.

Examples:
- Authentication: “Administrative access must require MFA.”
- Authorization: “A user may access only records permitted by their role and ownership.”
- Session security: “Session identifiers must be rotated after authentication and invalidated on logout.”
- Data protection: “Sensitive data must use approved encryption in transit and at rest.”
- Logging: “Authentication failures and privileged actions must be logged without storing passwords or access tokens.”
- Resilience: “The service must enforce rate limits on sensitive authentication and recovery endpoints.”
- Supply chain: “Dependencies must be inventoried and reviewed for known vulnerabilities.”
- Recovery: “Backups and restoration procedures must be tested at a defined cadence.”

Pair each requirement with an acceptance test, an owner, and the evidence needed to demonstrate it works.

## 4. Secure design and threat modeling

Before implementation:
1. Identify assets and sensitive data.
2. Draw the system's components, data flows, external dependencies, and trust boundaries.
3. Identify entry points and privileged operations.
4. Consider threats such as spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privilege (STRIDE is one useful model).
5. Estimate likelihood and impact.
6. Choose mitigations and assign owners.
7. Verify that mitigations appear in requirements, design, and tests.

Threat modeling is not a one-time form. Revisit it when architecture, data sensitivity, identity, dependencies, or exposure changes.

## 5. Secure coding and review

Useful practices include:
- Validate inputs with context-appropriate rules and encode outputs appropriately.
- Use parameterized database queries rather than string concatenation.
- Enforce authorization on the server for every sensitive action and object.
- Use established cryptographic libraries and secure random-number generators.
- Avoid hard-coded credentials and never commit secrets.
- Handle errors without exposing internal details or sensitive data.
- Keep dependencies and runtimes supported and patched.
- Review security-sensitive changes with a checklist and tests.
- Use safe defaults and fail securely.

Automated tools assist developers but do not replace design review, manual reasoning, or runtime testing.

## 6. Security testing in CI/CD

| Activity | Typical purpose | Important limitation |
|---|---|---|
| SAST | Finds patterns of potential flaws in source code | May lack runtime context and can produce false positives |
| SCA | Identifies known issues and licenses in third-party components | Package presence alone may not prove exploitability |
| Secret scanning | Detects possible credentials in code and history | A clean scan does not prove secrets were never exposed |
| DAST | Tests a running application from the outside | Coverage depends on reachable routes, roles, and test data |
| IaC scanning | Flags risky infrastructure configuration | Must be interpreted with deployment context |
| Container scanning | Detects vulnerable packages and configuration in images | Results depend on image, package metadata, and runtime context |
| Manual security review | Assesses logic, authorization, architecture, and context | Requires skilled reviewers and a defined scope |

### Example pipeline sequence

1. Pull request opened.
2. Formatting, unit tests, and code review checks run.
3. SAST, SCA, secret scanning, and IaC checks run.
4. Findings are deduplicated, validated, and prioritized.
5. Policy-defined release gates block unacceptable risk; approved exceptions are documented and time-bound.
6. Build artifact is produced and stored with traceable provenance.
7. Staging security tests run.
8. Release is approved, deployed, monitored, and verified.

A gate should define its scope and thresholds clearly. Avoid a blanket “fail on every scanner warning” policy without triage, but do not silently ignore high-risk findings.

## 7. Vulnerability handling

For each finding, capture:
- Affected component, version, and environment
- Detection source and evidence
- Severity and contextual risk rationale
- Exploitability, exposure, and asset criticality
- Responsible owner and target date
- Remediation or mitigation plan
- Exception approval and expiry if remediation is delayed
- Verification evidence and closure date

Define a process for security issues discovered after release, including triage, patch delivery, customer communication where required, and lessons learned.

## 8. Example security acceptance criteria

**Feature:** User profile API

- A user can retrieve or update only their own profile unless explicitly authorized.
- Unauthorized requests do not reveal another user's data.
- Input validation rejects invalid fields without leaking stack traces.
- Sensitive actions are logged with a request/correlation ID, without logging secrets.
- Automated tests cover allowed and denied access cases.
- Dependency and secret scans run in the pull-request pipeline.
- Security findings above the release threshold are resolved or have an approved, expiring exception.

These criteria are examples. Adapt them to the product's actual architecture and risk.

## 9. Roles and responsibilities

- **Product owner:** clarifies business impact, scope, and risk decisions.
- **Architect:** designs security boundaries and evaluates design trade-offs.
- **Developer:** implements secure code and fixes defects.
- **Security/AppSec:** advises on threat modeling, standards, tests, and risk triage.
- **QA/test engineering:** validates functional and security acceptance criteria.
- **Platform/DevOps:** secures build, deployment, runtime configuration, and credentials.
- **Operations/SRE:** monitors production, responds to incidents, and supports recovery.
- **Risk owner:** formally accepts residual risk within delegated authority.

In small teams, one person may perform multiple roles, but responsibilities should still be explicit.

## 10. Practical lab

Use a demo app, toy project, or repository you own or are authorized to assess.

1. Write five testable security requirements for the application.
2. Draw a basic data-flow diagram and mark trust boundaries.
3. Create a small threat model with at least five threats and mitigations.
4. Add code review and dependency scanning to a development workflow.
5. Add secret scanning and infrastructure checks where applicable.
6. Define release-gate thresholds and an exception process.
7. Create a security defect ticket with owner, severity, target date, and verification plan.
8. Fix one issue in a test branch and capture before/after evidence.
9. Document what would be monitored after deployment.

Do not scan or test systems without permission. Use test credentials and non-production data.

## 11. Metrics and continuous improvement

Potential measures:
- Percentage of repositories using required security checks
- Percentage of high-risk findings fixed within the target window
- Time from discovery to verified remediation
- Threat models completed for in-scope high-risk changes
- Recurrence rate for previously fixed vulnerability classes
- Rate of security exceptions past expiry
- Percentage of releases with traceable build and approval evidence

Metrics need context. A low finding count can mean strong security, poor coverage, or weak detection; interpret results alongside coverage and quality.

## 12. Checklist

- [ ] Security requirements are defined and testable.
- [ ] High-risk designs receive threat modeling.
- [ ] Secure coding and peer-review practices are documented.
- [ ] CI/CD includes appropriate security checks.
- [ ] Release gates and exceptions are risk-based and explicit.
- [ ] Findings have owners, due dates, and verification steps.
- [ ] Production monitoring and incident response are planned.
- [ ] Security is revisited after significant changes and at end of life.

## Further reading

- [NIST Secure Software Development Framework (SSDF), SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final)
- [OWASP Software Assurance Maturity Model (SAMM)](https://owaspsamm.org/)
- [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CISA Secure by Design](https://www.cisa.gov/securebydesign)

---
**Next module:** Continue with the threat-modeling materials in this roadmap section.
