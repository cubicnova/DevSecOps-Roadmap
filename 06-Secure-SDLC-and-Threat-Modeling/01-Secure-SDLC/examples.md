# Secure SDLC — Examples

Use these examples as starting points for your own project. Adapt them to the architecture and risk; do not treat them as a substitute for review.

## Example 1: Turn a business need into a security requirement

**Business need:** Users can view their account details.

Weak requirement: “The API must be secure.”

Testable requirements:
- The API must authenticate requests before returning account data.
- The server must verify that the authenticated user is authorized to access the requested account.
- Requests for another user's account must not return that user's data.
- Authorization failures must be logged without logging credentials or sensitive response content.
- Automated tests must cover both permitted and denied access cases.

## Example 2: Threat-model a simple application

**System:** Browser → Web API → Database. The API also calls an email provider.

| Asset / boundary | Threat | Possible mitigation | Verification |
|---|---|---|---|
| Login endpoint | Credential stuffing | Rate limiting, MFA options, monitoring | Automated rate-limit tests and alert review |
| API-to-database | SQL injection | Parameterized queries and restricted database role | Code review and security tests |
| User profile endpoint | Broken object-level authorization | Server-side object ownership checks | Tests with two distinct user accounts |
| API-to-email provider | Credential leakage | Secret manager, scoped credentials, rotation | Secret scan and access review |
| Database | Unauthorized access | Network restrictions, least privilege, encryption where appropriate | Configuration review and access test |

A threat model should also capture assumptions, trust boundaries, residual risks, and an owner for each mitigation.

## Example 3: Pull-request security checklist

Before merging a sensitive change, review:
- [ ] Authorization is enforced server-side for each sensitive action.
- [ ] Database queries use safe parameterization or a suitable ORM.
- [ ] Input validation and output encoding match the context.
- [ ] Secrets are not hard-coded or included in logs.
- [ ] Errors do not disclose sensitive internals.
- [ ] Dependencies and configuration are reviewed.
- [ ] Tests include denied-access and misuse cases.
- [ ] Security checks ran and findings were triaged.
- [ ] Any exception is approved, justified, and time-bound.

## Example 4: CI workflow design

A generic secure workflow might contain:
1. Checkout a trusted commit.
2. Install dependencies from lockfiles using approved sources.
3. Run unit and integration tests.
4. Run SAST, SCA, and secret scanning.
5. Scan IaC and container images when present.
6. Enforce the organization's documented risk gate.
7. Build and identify the artifact.
8. Deploy to a controlled test environment.
9. Run relevant dynamic and integration security tests.
10. Require deployment authorization and monitor the release.

Use maintained actions and pin third-party workflow dependencies according to your organization's supply-chain policy. Do not expose production secrets to untrusted pull-request code.

## Example 5: Security finding lifecycle

**Finding:** A dependency scanner reports a vulnerable package.

- **Validate:** Confirm package name, version, lockfile, and affected range.
- **Assess:** Review the advisory, exploitability, reachability, exposure, and asset criticality.
- **Assign:** Create a ticket with a clear owner and target date.
- **Fix:** Upgrade to a supported fixed release after compatibility tests.
- **Verify:** Re-run the audit and application tests.
- **Close:** Attach results and record the deployed version.
- **Learn:** Consider automated dependency updates or policy improvements to prevent recurrence.

## Example 6: Release gate

Illustrative policy:
- Block release for a confirmed critical issue that meets the organization's release-blocking criteria.
- Require security-owner review for high-risk findings.
- Allow exceptions only through documented risk acceptance with compensating controls and an expiry date.
- Reopen a finding if verification shows the fix did not reach all intended environments.

The actual thresholds should be defined by the organization and reflect risk, not copied blindly from this example.

## Example 7: Evidence for a secure release

A release evidence bundle may include:
- Commit and pull-request identifiers
- Code-review approval
- CI test and security-scan summaries
- Dependency and artifact identifiers
- Exception approvals, if any
- Deployment approval and change record
- Post-deployment health and security checks

Avoid storing raw secrets, personal data, or unnecessarily sensitive scan details in broadly accessible evidence stores.
