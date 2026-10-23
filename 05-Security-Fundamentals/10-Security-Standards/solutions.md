# Security Standards — Suggested Solutions

These are model answers. Other answers are valid when they are reasoned, scoped, evidence-based, and consistent with the selected source.

## Exercise 1: Distinguish the terms

1. **Standard:** Published requirements or guidance, such as ISO/IEC 27001.
2. **Framework:** A structure for organizing risk-management outcomes, such as NIST CSF 2.0.
3. **Control catalog:** A collection of safeguards, such as CIS Critical Security Controls.
4. **Regulation or contractual requirement:** An obligation that applies based on jurisdiction, sector, contract, or scope.
5. **Certification:** Formal confirmation from an authorized certification body that a defined scope meets a specified standard.
6. **Attestation report:** A report from an independent examination against defined criteria, such as a SOC 2 report.

## Exercise 2: Match the use case

- **A:** NIST CSF 2.0 — organizes cybersecurity outcomes and risk communication.
- **B:** CIS Controls — provides prioritized, practical safeguards.
- **C:** ISO/IEC 27001 — specifies requirements for an ISMS.
- **D:** PCI DSS — addresses payment account data security for entities and systems within scope.
- **E:** OWASP ASVS — provides verifiable security requirements for applications.

An organization may use more than one source. The actual requirements, scope, and version must be checked.

## Exercise 3: Scope definition

A reasonable scope could cover the SaaS production environment, its CI/CD pipeline, product engineering, support operations that access customer data, and associated security processes. Clarify:
- Whether employee laptops and identity services are in scope or provide critical dependencies.
- The payment provider's responsibilities and the company's own payment-data handling.
- Whether the marketing website shares identity, infrastructure, or deployment processes with the product.
- Cloud-provider inherited controls versus customer responsibilities.
- Geographic, legal, contractual, and organizational boundaries.

## Exercise 4: Map risk to controls

Possible safeguards:
1. **MFA and strong account lifecycle controls** — owner: IAM team; evidence: identity configuration and access review.
2. **Least-privilege repository permissions** — owner: Engineering; evidence: repository roles and periodic review.
3. **Required peer review and protected branches** — owner: Engineering; evidence: branch settings and pull-request history.
4. **Protected CI/CD credentials** — owner: Platform Engineering; evidence: pipeline identity configuration and secret-scanning results.
5. **Deployment audit logging and alerting** — owner: Security Operations; evidence: logs and alert test results.
6. **Rollback and release verification** — owner: Release Engineering; evidence: release records and recovery exercise.

## Exercise 5: Review a claim

A policy is only one part of a security program. ISO/IEC 27001 requires an appropriately scoped ISMS and risk-management processes, among other requirements. NIST CSF describes outcomes but does not itself grant certification. A defensible assessment needs a defined scope, applicable requirements, risk assessment, implemented controls, assigned owners, evidence of operation, gap treatment, and review. Any claim of certification must be supported by a valid certificate from the appropriate certification process and must describe its scope accurately.

## Exercise 6: Create a gap register

Illustrative rows:

| Objective | Current state / gap | Risk | Owner | Next action | Evidence |
|---|---|---|---|---|---|
| Review privileged access | No review record located | Excess access may persist | IAM Lead | Define review cadence and complete first review | Approved review and remediation tickets |
| Track vulnerabilities | Scans run but findings have no owners | Critical issues may remain unresolved | AppSec Lead | Assign owners, risk-based due dates, and escalation rules | Tickets linked to scan findings |
| Validate recovery | Backups exist but no restore evidence | Recovery may fail when needed | Operations Lead | Run a controlled restore test | Test record, timing, outcome, corrective actions |

Set due dates based on risk and organizational policy.

## Exercise 7: Evidence quality

- **Interview statement:** useful context, but subjective and difficult to verify alone.
- **Policy:** proves the expected rule is documented, not that it is followed.
- **Branch-protection screenshot:** shows configuration at a point in time; confirm scope and current state.
- **Pull-request samples:** demonstrate review activity for sampled changes; sample selection and completeness matter.
- **Direct-push test:** provides evidence that a specific technical safeguard works under tested conditions.

The strongest evidence set combines policy, configuration, operating samples, and a test. No single item proves every aspect of control effectiveness.

## Exercise 8: Exception management

A good record includes the control, affected scope, business reason, residual risk, accountable risk owner, approval, temporary safeguards, monitoring, review cadence, exact expiry date, permanent remediation plan, and closure criteria. The exception should be re-evaluated if the threat or exposure changes.

## Exercise 9: DevSecOps mapping

Examples:
- **Source control:** protected branches and peer review; evidence: settings and pull-request records.
- **Build/dependencies:** dependency scanning; evidence: build report and remediation tickets.
- **Infrastructure as Code:** scan Terraform plans or configuration; evidence: pipeline results and approved exceptions.
- **Containers:** scan images and use trusted base images; evidence: image scan and registry metadata.
- **Deployment:** restrict deployment identity and require appropriate approvals; evidence: IAM policy and release logs.
- **Production monitoring:** collect security events and test alerts; evidence: log coverage and alert test records.

## Exercise 10: Standards implementation plan

- **Days 1–5:** Confirm business drivers, stakeholders, scope, and assets.
- **Days 6–10:** Assess key risks and select a primary framework or standard.
- **Days 11–15:** Choose relevant controls, assign owners, and define evidence.
- **Days 16–20:** Perform a gap review and prioritize high-risk gaps.
- **Days 21–25:** Implement a small set of high-value improvements and track actions.
- **Days 26–30:** Collect evidence, review exceptions, report progress, and agree the next cycle.

This is a starter plan, not a guarantee of certification or compliance in 30 days.

## Exercise 11: Short reflection

A strong answer explains that a framework organizes outcomes and a standard may define requirements, but selecting either does not automatically implement controls. Security depends on scope, risk, architecture, people, operational processes, evidence, and continuous improvement. A control can be documented but not followed, implemented but ineffective, or applied to only part of the environment. Organizations must validate implementation, address gaps, review changes, and ensure evidence matches the claim being made. Certification and independent reports follow their own defined assessment processes and apply only to their stated scope. Therefore, framework adoption is a starting point for structured improvement—not proof that an organization is invulnerable, compliant with every obligation, or certified.
