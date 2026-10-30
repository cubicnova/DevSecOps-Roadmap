# Secure SDLC — Suggested Solutions

These are sample answers. Other solutions are acceptable if they are technically sound, testable, and appropriate to the stated system.

## Exercise 1: SDLC mapping

| Phase | Security activities | Example evidence |
|---|---|---|
| Requirements | Identify sensitive data; define access and logging requirements | Security requirements and acceptance tests |
| Design | Threat model; review trust boundaries | Data-flow diagram and threat register |
| Development | Secure coding; peer review | Pull requests and review checklist |
| Build | SAST/SCA/secret scanning; protect build identity | Pipeline reports and workflow configuration |
| Testing | DAST/API authorization tests; configuration checks | Test reports and defect tickets |
| Release | Approval gate; least-privilege deployment | Release record and deployment logs |
| Operations | Monitor alerts; patch vulnerabilities | Incident records and remediation tickets |
| Retirement | Revoke credentials; remove data and endpoints securely | Decommission checklist |

## Exercise 2: Improve vague requirements

Examples:
1. **Requirement:** “All unauthenticated requests to protected account endpoints must be rejected.” **Verification:** Integration tests call the endpoints without a valid session and assert an appropriate denial.
2. **Requirement:** “A user can retrieve only records they own or are explicitly authorized to access.” **Verification:** Tests use two accounts and attempt cross-account access.
3. **Requirement:** “Production credentials must be stored in the approved secret manager and must not appear in source control or application logs.” **Verification:** Review configuration and scan repository/log test output.
4. **Requirement:** “Confirmed high-risk vulnerabilities must be assigned an owner and target date under the approved remediation policy.” **Verification:** Sample tickets and report overdue findings.

## Exercise 3: Threat modeling

Assets may include user credentials, profile data, database records, API credentials, email content, and audit logs. Trust boundaries include browser-to-API and API-to-database or third-party provider.

Example threats:
- Credential stuffing → rate limiting, MFA options, anomaly detection → test controls and alerting.
- SQL injection → parameterized queries and restricted DB permissions → code review and security tests.
- Cross-user data access → server-side ownership checks → tests with separate users.
- Email-provider key theft → secret manager and scoped/rotatable credentials → configuration review and secret scan.
- Database exposure → network restrictions, least privilege, encryption where appropriate → configuration and access tests.

## Exercise 4: Choose security checks

- **Python API:** SAST, SCA or `pip-audit`, secret scanning, unit/API authorization tests, DAST in a controlled environment. SAST may miss runtime logic; SCA may identify packages whose vulnerable code path is not reachable.
- **Terraform:** IaC scanning, policy checks, peer review, plan review. Static checks may not reflect every deployed cloud control or inherited permission.
- **Container app:** image scanning, base-image review, secret scanning, runtime configuration checks, DAST. Image scans can miss application behavior and do not prove that a deployed workload is configured securely.

## Exercise 5: Design a release gate

A sound policy names the blocking criteria, defines who can make risk decisions, requires documented evidence, and prevents exceptions from becoming indefinite. A high-risk exception should identify residual risk, an accountable approver, compensating controls, a clear expiry, and a remediation plan. Post-deployment verification should confirm the fix is present in all intended environments.

## Exercise 6: Vulnerability ticket

Include:
- Finding and affected package/version
- Vendor advisory and scanner evidence
- Contextual risk, exposure, and asset criticality
- Named owner and policy-based target date
- Fixed version and upgrade plan
- Compatibility tests and rollback steps
- Re-scan and functional-test requirements
- Deployment evidence and final package version
- Approved exception process if the fix is blocked

## Exercise 7: Secrets handling

1. Revoke or disable the exposed key immediately, then issue a replacement through the approved secret manager.
2. Identify permissions and resources the key could access; review provider audit logs for misuse.
3. Remove the secret from the current source and assess repository history, forks, caches, build logs, artifacts, and copies.
4. Coordinate any history rewrite carefully; rewriting history does not make a leaked credential safe again.
5. Update consumers, test the replacement, and monitor for suspicious activity.
6. Add secret scanning, least-privilege credentials, short-lived tokens where possible, and developer guidance.

## Exercise 8: Review a pipeline

Risks include vulnerable dependencies, accidentally committed secrets, insecure infrastructure configuration, weak deployment permissions, lack of traceability, and missing security gates. Add appropriate SCA, secret scanning, IaC scanning, protected branches, least-privilege build identities, and controlled release approvals. Do not pass production secrets to untrusted pull-request jobs; use isolated test credentials and separate trusted deployment workflows.

## Exercise 9: Metrics

Examples:
- **Security-check coverage:** share of in-scope repositories with required checks; misleading if the repository inventory is incomplete.
- **Time to remediate:** time from discovery to verified closure; misleading if teams close tickets without verification.
- **High-risk findings past due:** indicates backlog against policy; needs exposure and asset context.
- **Threat-model coverage:** share of qualifying changes with a reviewed threat model; does not alone prove the model is accurate or mitigations work.
- **Exception expiry compliance:** shows whether risk acceptances are reviewed; does not prove compensating controls are effective.

## Exercise 10: Practical mini-project

A successful submission contains five measurable requirements, a data-flow diagram and threat list, a code-review checklist, three appropriate automated checks, documented release criteria and exception handling, a complete example ticket, and a post-release verification plan. Evidence should be reproducible and should not contain real secrets or sensitive production data.

## Exercise 11: Reflection

A strong response notes that automated tools scale checks across many changes and help identify patterns such as known vulnerable dependencies, secret-like strings, risky infrastructure settings, and suspicious code constructs. But tools can produce false positives, miss business-logic flaws, lack runtime context, and fail to test authorization across realistic roles. A scanner also cannot by itself decide the business impact of a finding, ensure the right owner fixes it, or prove that a patch reached every environment. A Secure SDLC combines automation with secure requirements, threat modeling, code review, contextual triage, manual testing where needed, release governance, monitoring, and verified remediation. Tool output must be interpreted and tracked through closure.
