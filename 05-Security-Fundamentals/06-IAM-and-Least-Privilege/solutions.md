# IAM and Least Privilege - Suggested Solutions

Answers are examples. The exact implementation depends on the IAM platform, business requirements, and risk assessment.

## Part A: Knowledge Check

1. **Identification** names the claimed identity; **authentication** verifies it; **authorization** decides what it may do; **auditing** records activity for accountability and investigation.
2. Least privilege grants an identity only the minimum access necessary for its assigned task.
3. Workload identities can be compromised or misused too. Excessive permissions allow a compromised pipeline or service to affect more resources than required.
4. **RBAC** bases access on assigned roles. **ABAC** evaluates attributes and context. Both can be combined.
5. Examples include separate administrative accounts, MFA or phishing-resistant authentication, just-in-time elevation, short-lived credentials, approval workflows, and logging of privileged actions.
6. Reassess the person's permissions, remove obsolete access, grant the new role's required permissions, and record the review.
7. Temporary credentials reduce the period during which a stolen credential can be reused and can simplify revocation. They still require secure issuance and use.
8. Wildcards may grant access to unrelated resources or powerful actions. Narrow scope to required actions and resources, and document justified exceptions.

## Part B: Scenario Analysis

1. **Problem:** Broad standing privileges. **Fix:** Define task-based roles, limit administrator access, require approval for elevated actions, and review usage. **Verify:** Test representative developer tasks and confirm administrative actions are denied.
2. **Problem:** The pipeline can destroy resources unrelated to its task. **Fix:** Grant artifact-upload permissions only for the intended artifact destination; remove database-deletion permissions. **Verify:** Run a staging deployment test and negative tests against unrelated resources.
3. **Problem:** Offboarding was incomplete. **Fix:** Disable the account, revoke sessions and credentials, review tokens and owned resources, and inspect relevant logs. **Verify:** Confirm sign-in and token use are blocked.
4. **Problem:** The analyst has more data access than needed. **Fix:** Provide ticket-scoped read permissions and remove bulk export unless formally required. **Verify:** Test ticket viewing and ensure export endpoints or actions are denied.
5. **Problem:** Daily activity occurs under a privileged identity. **Fix:** Use a standard account for routine work and a separate, controlled privileged identity for administrative tasks. **Verify:** Confirm routine services work with the standard account and admin functions require elevation.
6. **Problem:** Users may manipulate attributes that determine access. **Fix:** Protect authoritative attributes, restrict who can modify tags, and validate policy conditions. **Verify:** Test attempts to alter tags and access resources across environments.
7. **Problem:** Emergency access may bypass normal controls. **Fix:** Use a documented break-glass process with strong authentication, limited authorized custodians, alerts, logging, post-use review, and credential rotation where appropriate.

## Part C: Practical Labs

### Lab 1: Example Role-Permission Matrix

| Action | Viewer | Developer | SecurityReviewer | PlatformAdmin |
|---|---|---|---|---|
| View application logs | Allow | Allow | Allow | Allow |
| Edit source code | Deny | Allow | Deny | Approval required |
| Deploy to development | Deny | Allow | Deny | Allow |
| Deploy to production | Deny | Approval required | Approval required | Allow under change control |
| Change IAM policies | Deny | Deny | Review only | Allow with audit |
| Review audit logs | Deny | Limited | Allow | Allow |

This is an illustrative starting point, not a universal access policy. Refine it to match actual job responsibilities and separation-of-duties requirements.

### Lab 2: Review an Over-Privileged Policy

Risks include access to unrelated resources, ability to perform destructive actions, and excessive impact if the pipeline is compromised. Replace broad permissions with only the required artifact and staging-deployment actions, scoped to the relevant resources. Do not grant production database deletion or IAM administration unless a separate, explicitly approved workflow requires it. Test the expected deployment and attempt representative unauthorized actions in a controlled environment.

### Lab 3: Joiner-Mover-Leaver Checklist

- **Joiner:** confirm identity and manager approval; create a unique account; require MFA; assign role-based permissions; document owner and approval.
- **Mover:** review old access; remove obsolete group memberships and roles; grant new required permissions; confirm ownership and record the review.
- **Leaver:** disable account; revoke sessions, tokens, keys, and application access; transfer ownership; remove unnecessary automation access; preserve required audit evidence; confirm completion.

Automate reliable steps where appropriate, but retain validation and exception handling.

### Lab 4: Example Access Review

| Identity | Access | Last used | Recommended action |
|---|---|---|---|
| dev-01 | Development deploy | Yesterday | Retain and review quarterly |
| dev-02 | Cloud administrator | 90 days ago | Remove standing admin; investigate need |
| contractor-01 | Production logs | 120 days ago | Confirm engagement; disable if ended |
| pipeline-staging | Deploy to staging and delete all databases | Today | Remove database deletion and narrow resources |
| auditor-01 | Read audit logs | 7 days ago | Retain if still required |

Dates are illustrative. A real review should use trusted usage records and an accountable business owner.

### Lab 5: IAM for CI/CD

Use a dedicated workload identity with separate permissions for source retrieval, build, artifact publication, and staging deployment. Prefer short-lived credentials or workload identity federation where supported. Avoid exposing secrets to untrusted pull-request code; keep deployment credentials in protected workflows and environments. Use separate, explicitly approved production deployment permissions, and log artifact identity, target environment, approver, and result.

## Part D: Sample Policy Outline

A suitable policy should require unique accounts and MFA for privileged access; manager and resource-owner approval for access; task-scoped roles; time-limited elevation; protected workload identities; recurring access reviews; timely offboarding; audit logging for privileged actions; and documented, time-limited exceptions with an owner and review date.

## Assessment Rubric

| Criterion | Strong response |
|---|---|
| Least privilege | Permissions are limited to required actions and resources |
| Identity lifecycle | Joiner, mover, and leaver steps are complete |
| Privileged access | Elevation is controlled, logged, and reviewed |
| DevSecOps | CI/CD identities are isolated and narrowly scoped |
| Verification | Includes positive and negative access tests |
| Governance | Includes ownership, approvals, reviews, and exceptions |

## References

- [NIST: Least Privilege Glossary](https://csrc.nist.gov/glossary/term/least_privilege)
- [NIST SP 800-171 Rev. 3](https://csrc.nist.gov/pubs/sp/800/171/r3/final)
- [AWS: Prepare for Least-Privilege Permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started-reduce-permissions.html)
- [AWS: Security Best Practices for IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
