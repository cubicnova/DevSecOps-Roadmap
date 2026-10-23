# Security Standards — Examples

These examples demonstrate how to interpret frameworks and build evidence. They are learning examples, not a statement that an organization is compliant or certified.

## Example 1: Select a reference

**Scenario:** A small SaaS provider wants to improve its security program and respond to customer security questionnaires.

A reasonable starting approach:
1. Use **NIST CSF 2.0** to organize cybersecurity outcomes and discuss maturity.
2. Use **CIS Controls** to prioritize practical safeguards.
3. Consider **ISO/IEC 27001** if customers or business strategy call for a formal ISMS and possible certification.
4. Assess whether any contractual, legal, privacy, or sector-specific requirements apply.
5. Define scope before promising a certification or report.

The best selection depends on actual customer requirements and business context; the frameworks do not automatically replace one another.

## Example 2: Map a risk to safeguards

**Risk:** A compromised CI/CD token could publish an unapproved release.

| Risk treatment | Example implementation | Example evidence |
|---|---|---|
| Reduce credential lifetime | Use workload identity or short-lived credentials where supported | Pipeline identity configuration |
| Restrict permissions | Scope deployment role to required resources/actions | IAM role policy and review |
| Protect source changes | Require review and protect release branches | Repository settings and pull-request history |
| Detect misuse | Log deployment activity and alert on unusual changes | Audit events and alert test |
| Recover | Maintain known-good artifacts and a rollback procedure | Release and recovery test records |

The mapping should reference the chosen framework's actual requirement or safeguard and edition. Do not invent a formal control number.

## Example 3: Draft a gap register

| ID | Control objective | Current state | Gap | Owner | Next step |
|---|---|---|---|---|---|
| GAP-01 | Review privileged access | No review record found | Access may remain broader than needed | Platform Lead | Establish quarterly review and evidence retention |
| GAP-02 | Track dependency vulnerabilities | Scans run but tickets lack owners | Findings may remain unresolved | AppSec Lead | Define triage rules, ticket fields, and due dates |
| GAP-03 | Test recovery | Backups exist but restore test is undocumented | Recovery capability is unverified | Operations Lead | Perform a controlled restore test and record results |

Use real evidence to determine whether a gap exists. “No evidence found” may mean a control is absent or that evidence is stored elsewhere; investigate before final classification.

## Example 4: Evidence collection

For a control requiring code review, possible evidence includes:
- Repository branch-protection settings
- A sample of pull requests with reviewer approval
- Documented exceptions and their approvals
- A periodic test confirming direct pushes are blocked where required

A policy that says “all code must be reviewed” is useful, but it does not alone prove the policy is consistently followed.

## Example 5: Framework mapping without overclaiming

A team maps its vulnerability-management process to a framework objective. Its evidence includes scan coverage, a risk register, remediation tickets, and retest results.

A defensible statement is: “The team has implemented the listed practices within the defined scope and retains the evidence shown.”

Avoid saying: “We are fully compliant with every security standard.” A mapping is not an audit opinion or certification, and each source has its own scope and requirements.

## Example 6: Scope statement

**Illustrative scope:** “The ISMS assessment covers the SaaS product engineering team, its production cloud environment, CI/CD platform, and supporting security operations. Corporate HR systems and unrelated subsidiaries are excluded from this exercise, with the exclusions and their rationale documented.”

A real scope must reflect organizational context and interested-party requirements. Do not exclude critical dependencies simply to make an assessment easier.

## Example 7: Exception record

- **Control:** Privileged access review
- **Reason:** Identity platform migration in progress
- **Risk owner:** Named business owner
- **Temporary safeguards:** Review high-privilege changes weekly; alert on role changes; restrict administrative roles
- **Expiry:** A specific date
- **Review cadence:** Weekly until closed
- **Closure criteria:** New review process is operational and evidence is retained
- **Approval:** Security and accountable risk owner according to policy

An exception should not silently become permanent. Expired exceptions must be reviewed and escalated.

## Example 8: Continuous improvement

After a cloud architecture change:
1. Reassess scope and dependencies.
2. Review affected risks and control mappings.
3. Update policies, diagrams, and ownership records.
4. Re-test controls affected by the change.
5. Collect new evidence and resolve gaps.
6. Update the risk register and track improvement actions.
