# 06 - IAM and Least Privilege

Identity and Access Management (IAM) defines how identities are created, authenticated, authorized, reviewed, and removed. The **principle of least privilege** means granting each user, service, or process only the access required to perform its assigned tasks. This limits the impact of mistakes, compromised accounts, and malicious activity. [NIST defines least privilege](https://csrc.nist.gov/glossary/term/least_privilege) as restricting access privileges to the minimum necessary for assigned tasks.

## Learning Objectives

- Distinguish identification, authentication, authorization, and accounting/auditing.
- Explain IAM identities, groups, roles, permissions, and policies.
- Apply least privilege to human users, service accounts, and automation.
- Compare role-based access control (RBAC) and attribute-based access control (ABAC).
- Understand MFA, privileged access, access reviews, and joiner-mover-leaver processes.
- Review access policies and identify excessive permissions.

## 1. IAM Fundamentals

| Concept | Meaning | Example |
|---|---|---|
| Identity | A person, service, device, or workload represented in a system | Developer account or CI/CD workload |
| Authentication | Establishes that an identity is who or what it claims to be | Password plus MFA |
| Authorization | Determines which actions an authenticated identity may perform | Read a repository but cannot change settings |
| Accounting/auditing | Records actions for accountability and investigation | Audit log of role changes |
| Permission | An allowed or denied action on a resource | Read an object in a storage bucket |
| Policy | Rules defining access | Permit deployment only to a staging environment |
| Role | A named set of permissions assigned or assumed for a task | Read-only auditor |
| Privileged account | An identity with elevated or security-sensitive permissions | Domain administrator |

Authentication does not automatically mean a user should have broad access. Authentication verifies identity; authorization controls what that identity can do.

## 2. Principle of Least Privilege

Grant the minimum permissions needed, for the minimum time needed, to the correct identity and resources.

Practical rules:
- Prefer narrowly scoped permissions over broad administrator access.
- Limit permissions by action, resource, and relevant conditions.
- Use separate standard and administrative accounts where appropriate.
- Use temporary credentials and just-in-time elevation when supported.
- Review access regularly and remove permissions that are no longer needed.
- Apply least privilege to workloads and automation, not just employees.
- Monitor use of privileged functions and keep audit logs protected.

Least privilege is a continuous process: review granted permissions against actual business needs and adjust them as systems and responsibilities change. [AWS least-privilege guidance](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started-reduce-permissions.html) recommends granting only the permissions required for a task.

## 3. Access Control Models

### Role-Based Access Control (RBAC)
Permissions are associated with job or function roles, and identities are assigned to those roles.

**Example:** A `Developer` role can deploy to a test environment but cannot manage production identity policies.

**Benefits:** Easier administration and consistent role definitions.

**Risk:** Roles can accumulate too many permissions or become too broad.

### Attribute-Based Access Control (ABAC)
Access decisions use attributes such as department, resource tags, environment, device state, or request context.

**Example:** A deployment identity may modify resources only when the resource's environment tag matches the approved deployment environment.

**Benefits:** Flexible, scalable policies for dynamic environments.

**Risk:** Incorrect or untrusted attributes can produce unintended access.

## 4. Authentication and MFA

Multi-factor authentication (MFA) requires evidence from more than one factor category, such as something you know, have, or are. Prefer phishing-resistant methods where available for high-value accounts.

IAM hygiene includes:
- Unique accounts rather than shared human accounts.
- Strong authentication and MFA for privileged access.
- Secure recovery and account-recovery processes.
- Protected service credentials and tokens.
- Prompt removal of access when it is no longer required.

## 5. Privileged Access Management

Privileged access can change systems, users, security controls, or sensitive data. Reduce its risk by:
- Restricting privileged roles to authorized personnel.
- Using separate administrative identities where appropriate.
- Requiring approval or just-in-time elevation for sensitive tasks.
- Using short-lived credentials where possible.
- Logging and reviewing privileged actions.
- Maintaining tested emergency-access procedures with strong safeguards.

## 6. Identity Lifecycle

Use a consistent joiner-mover-leaver process:

1. **Joiner:** verify approval, create the identity, and assign access based on the person's role.
2. **Mover:** review existing permissions when responsibilities change; remove obsolete access before or as new access is granted.
3. **Leaver:** disable or remove accounts, revoke sessions and credentials, transfer ownership, and review automation or shared resources.
4. **Periodic review:** have owners validate that access remains necessary and remove unjustified permissions.

## 7. IAM in DevSecOps

IAM applies to developers, source control, CI/CD pipelines, cloud resources, containers, and production services.

- Give CI/CD jobs only the permissions required for that job.
- Prefer workload identity federation or short-lived credentials over long-lived static keys where supported.
- Separate build, test, and production permissions.
- Do not expose secrets to untrusted pull-request code.
- Scope deployment identities to specific environments and resources.
- Audit role changes, policy updates, secret access, and production deployments.
- Avoid using an administrator identity for routine tasks.

## Module Files

- [`examples.md`](examples.md) — worked IAM scenarios and sample policy-review patterns.
- [`exercises.md`](exercises.md) — IAM knowledge checks and practical labs.
- [`solutions.md`](solutions.md) — suggested answers and evaluation criteria.

## Knowledge Checklist

- [ ] I can distinguish authentication from authorization.
- [ ] I can explain least privilege and why it must be reviewed continuously.
- [ ] I can compare RBAC and ABAC.
- [ ] I can describe MFA and privileged-access controls.
- [ ] I can outline joiner-mover-leaver procedures.
- [ ] I can identify excessive permissions in a DevSecOps workflow.

## Further Reading

- [NIST: Least Privilege Glossary](https://csrc.nist.gov/glossary/term/least_privilege)
- [NIST SP 800-171 Rev. 3: Least Privilege](https://csrc.nist.gov/pubs/sp/800/171/r3/final)
- [AWS: Prepare for Least-Privilege Permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started-reduce-permissions.html)
- [AWS: Security Best Practices for IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
