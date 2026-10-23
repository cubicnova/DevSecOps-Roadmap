# 10 - Security Standards

This module introduces widely used cybersecurity standards, frameworks, and control catalogs, and explains how to select and apply them in a DevSecOps environment.

## Learning objectives

By the end of this module, you should be able to:

- Explain the difference between a standard, framework, control catalog, regulation, and certification.
- Describe the purpose of ISO/IEC 27001, NIST Cybersecurity Framework (CSF), CIS Critical Security Controls, PCI DSS, and SOC 2.
- Map a business risk to a security control and collect evidence that the control operates.
- Understand scope, applicability, risk treatment, control ownership, and continuous improvement.
- Avoid claiming compliance or certification without appropriate evidence and independent assessment where required.

## 1. Standards, frameworks, regulations, and attestations

| Term | What it means | Example |
|---|---|---|
| Standard | A published set of requirements or guidance. | ISO/IEC 27001 |
| Framework | A structured way to organize outcomes and risk-management activities. | NIST CSF 2.0 |
| Control catalog | A prioritized set of safeguards or controls. | CIS Critical Security Controls |
| Regulation or contractual requirement | A binding obligation for organizations within its scope. | Applicable privacy law or payment-card obligations |
| Certification | Formal confirmation by an authorized certification body that defined requirements are met within a stated scope. | ISO/IEC 27001 certification |
| Attestation/report | An independent examination and report against defined criteria. | SOC 2 examination report |

These terms are related but not interchangeable. The right choice depends on customer expectations, laws, sector, risk, geography, and business goals.

## 2. Common cybersecurity standards and frameworks

### ISO/IEC 27001

ISO/IEC 27001 specifies requirements for establishing, implementing, maintaining, and continually improving an Information Security Management System (ISMS). It emphasizes risk assessment and treatment, leadership, defined responsibilities, documented processes, and continual improvement.

Useful when an organization needs a formal, risk-based ISMS and may seek independent certification. Certification applies to a defined scope; it does not mean every system is perfectly secure.

Official resource: [ISO/IEC 27001](https://www.iso.org/standard/27001)

### NIST Cybersecurity Framework (CSF) 2.0

NIST CSF 2.0 organizes cybersecurity outcomes into six functions:

- **Govern** — establish and monitor cybersecurity risk strategy, expectations, and policy.
- **Identify** — understand assets, context, and risks.
- **Protect** — implement safeguards.
- **Detect** — discover and analyze possible attacks or compromises.
- **Respond** — take action regarding detected incidents.
- **Recover** — restore capabilities and improve after incidents.

The CSF is outcome-oriented and does not prescribe one universal implementation. Organizations select and tailor practices to their risks.

Official resource: [NIST CSF](https://www.nist.gov/cyberframework)

### CIS Critical Security Controls

CIS Controls provide prioritized, practical safeguards to reduce common cyber risks. They can help teams turn broad security goals into operational actions such as maintaining asset inventories, managing software, protecting data, securely configuring systems, controlling access, and managing vulnerabilities.

Official resource: [CIS Critical Security Controls](https://www.cisecurity.org/controls)

### PCI DSS

The Payment Card Industry Data Security Standard applies to environments that store, process, transmit, or can affect the security of payment account data, according to its scope and applicability rules. Organizations should use current official PCI SSC materials and qualified professionals where appropriate. Do not assume that every business is in scope or that outsourcing automatically removes all responsibility.

Official resource: [PCI Security Standards Council](https://www.pcisecuritystandards.org/)

### SOC 2

SOC 2 is an examination and reporting framework for controls at a service organization against applicable Trust Services Criteria. It is not the same as ISO certification, and a SOC 2 report is not a generic certificate. Reports have a defined scope, period or point in time, system description, and auditor conclusions.

Official resource: [AICPA SOC resources](https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services)

### Other references

- **CIS Benchmarks:** secure configuration recommendations for specific technologies.
- **OWASP ASVS:** verifiable security requirements for web applications and services.
- **NIST SP 800-53:** a broad security and privacy control catalog, commonly used in U.S. federal and other risk-management contexts.
- **NIST SP 800-61:** incident response guidance.
- **ISO/IEC 27701:** privacy information management guidance/requirements within its applicable edition and context.

Always check the official publisher for the current edition, errata, scope, and licensing terms.

## 3. How to select a framework

1. Identify business goals, customer requirements, legal obligations, and industry constraints.
2. Define the organizational and technical scope.
3. Assess current risks, assets, processes, and existing controls.
4. Choose a framework or standard that fits the goal; multiple sources may be mapped together.
5. Perform a gap assessment and assign control owners.
6. Prioritize implementation based on risk and dependencies.
7. Collect evidence that controls are designed appropriately and operate in practice.
8. Review changes, incidents, exceptions, and control effectiveness regularly.
9. Prepare for an external assessment or certification only when the scope and evidence are ready.

## 4. Mapping a risk to a control

Example risk: A production deployment pipeline uses a long-lived credential with broad permissions.

| Element | Example |
|---|---|
| Risk | Credential theft could permit unauthorized deployment or access to production resources. |
| Desired outcome | Restrict deployment privileges and detect misuse. |
| Possible safeguards | Short-lived credentials, least privilege, secret storage, protected branches, approval gates, audit logs, credential rotation. |
| Evidence | Pipeline configuration, IAM policy review, secret-scanning results, access logs, approval records, periodic access-review record. |
| Owner | Platform Engineering, with Security oversight. |
| Review trigger | Pipeline changes, incident, new integration, or scheduled control review. |

A control mapping is not automatically proof of compliance. The organization must assess whether the selected control is appropriate, implemented, operating, and in scope.

## 5. DevSecOps implementation examples

- **Governance:** define security ownership, risk acceptance, policies, and exception expiry dates.
- **Source control:** require peer review, branch protection, and appropriate repository permissions.
- **CI/CD:** use short-lived credentials, protect secrets, limit runner permissions, and log deployments.
- **Dependencies:** inventory components, scan dependencies, and establish remediation workflows.
- **Infrastructure as Code:** scan Terraform and Kubernetes configuration before deployment.
- **Containers:** scan images, use trusted base images, minimize privileges, and rebuild patched images.
- **Production:** centralize logs, manage access, test backups, and rehearse incident response.
- **Evidence:** retain policy approvals, scan reports, change records, test results, access reviews, and incident exercises according to policy.

## 6. Example control register

| Control ID | Objective | Owner | Example evidence | Status |
|---|---|---|---|---|
| GOV-01 | Security policies are approved and reviewed | Security Lead | Approved policy and review history | In progress |
| IAM-01 | Access follows least privilege | Platform Team | Role policies and access-review records | Implemented |
| SDLC-01 | Code changes receive review | Engineering Lead | Branch protection and pull-request history | Implemented |
| VULN-01 | Vulnerabilities are tracked to verified closure | Security Operations | Scan results and remediation tickets | In progress |
| IR-01 | Incident response is exercised | Incident Response Lead | Exercise plan, results, and actions | Planned |

This is an illustrative register, not a prescribed control set. Use IDs and evidence requirements suited to your organization.

## 7. Gap assessment and evidence

For each applicable requirement or control, record:

- Requirement or control reference and source edition
- Applicability and scope rationale
- Current implementation and owner
- Evidence and date collected
- Gap or residual risk
- Remediation action, priority, and due date
- Exception or risk-treatment decision, if applicable
- Review date and status

Avoid marking a control “effective” based only on a policy document. Depending on the control, evidence may include configuration exports, samples, logs, tests, access reviews, change records, or interview notes.

## 8. Common mistakes

- Treating all frameworks as equivalent or interchangeable.
- Confusing a control being documented with it operating effectively.
- Using an old edition without checking whether it remains applicable.
- Copying controls without defining scope, ownership, or evidence.
- Claiming certification or compliance before a suitable assessment.
- Ignoring suppliers, cloud services, software dependencies, and inherited controls.
- Treating a gap assessment as a one-time task instead of a continuous process.

## 9. Practical lab

Use a fictional organization or an environment you are authorized to assess.

1. Choose one business service, such as a customer-facing web application.
2. Define the scope, key assets, data types, and stakeholders.
3. Select one framework or control catalog as the primary reference.
4. Write five security outcomes or controls relevant to the service.
5. Map each to an owner, implementation example, and evidence source.
6. Identify two gaps and prioritize them by risk.
7. Create a remediation plan with target dates and verification evidence.
8. Explain how you would review the controls after a major architecture change.

## 10. Checklist

- [ ] Business drivers and applicable obligations are documented.
- [ ] Scope and boundaries are clear.
- [ ] The selected source and edition are recorded.
- [ ] Controls have owners and evidence requirements.
- [ ] Gaps are prioritized by risk.
- [ ] Exceptions have approval, rationale, and expiry.
- [ ] Evidence is current and demonstrates operation where required.
- [ ] Reviews and improvement actions are scheduled.

## Further reading

- [ISO/IEC 27001](https://www.iso.org/standard/27001)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CIS Critical Security Controls](https://www.cisecurity.org/controls)
- [PCI Security Standards Council](https://www.pcisecuritystandards.org/)
- [AICPA SOC resources](https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services)
- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
- [NIST SP 800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)

---
**Repository path:** `05-Security-Fundamentals/10-Security-Standards/`
