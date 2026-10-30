# 10 — Remediation and Verification

## Overview
This module covers how to turn a validated DAST/IAST finding into a secure code or configuration change, then prove that the weakness is fixed. A finding is not closed merely because a commit exists or a scanner stops reporting it. Verification must show that the original attack path no longer succeeds, relevant variants are addressed, and normal functionality still works.

**Safety:** Use only systems you own or are explicitly authorized to test. Prefer isolated test environments and synthetic data.

## Learning objectives
- Explain the remediation lifecycle and finding states.
- Write developer-ready remediation tickets with root cause and acceptance criteria.
- Select secure fixes for common web/API weaknesses.
- Retest the original request and relevant variations.
- Add unit, integration, and security regression tests.
- Collect sanitized, reproducible evidence.
- Integrate verification into CI/CD and measure remediation quality.

## 1. Remediation lifecycle
1. **Validate:** Reproduce the finding and confirm scope, preconditions, and impact.
2. **Analyze:** Identify the vulnerable component and underlying root cause.
3. **Prioritize:** Consider severity, exploitability, exposure, business impact, and asset criticality.
4. **Plan:** Assign an owner, target release, due date, and remediation approach.
5. **Implement:** Correct the root cause, not just the visible symptom.
6. **Review:** Perform code review and targeted tests.
7. **Verify:** Replay the original test and test reasonable variants.
8. **Regress:** Confirm valid workflows and adjacent controls still work.
9. **Close or reopen:** Record evidence and an accurate status.

### Suggested finding states

| State | Meaning | Evidence |
|---|---|---|
| New | Report received | Scanner/report reference |
| Validated | Reproduced and confirmed | Sanitized request/response or trace |
| In progress | Fix being implemented | Owner and target date |
| Ready for retest | Fix deployed to test environment | Build/commit identifier |
| Fixed | Weakness no longer reproduces | Retest and regression evidence |
| Partially fixed | Risk reduced but an exploitable path remains | Remaining path and follow-up ticket |
| Not fixed | Original issue still reproduces | Reproduction evidence |
| Accepted risk | Authorized deferral | Approver, rationale, expiry/review date |
| Unable to verify | Test could not be completed | Blocker and next step |

A timeout, unavailable endpoint, failed login, or incorrect build is **Unable to verify**, not Fixed.

## 2. Remediation ticket template
Include:
- Finding ID, title, severity, and affected application.
- Environment, endpoint, method, parameter, and affected component.
- Preconditions, required role, and safe reproduction steps.
- Sanitized request/response or IAST trace.
- Root cause and likely code/configuration location.
- Business and technical impact.
- Recommended secure design or coding pattern.
- Acceptance criteria and regression tests.
- Owner, due date, target release, and retest contact.

### Example: broken object-level authorization
**Title:** Enforce tenant authorization on invoice retrieval  
**Route:** `GET /api/invoices/{invoiceId}`  
**Root cause:** Authentication is checked, but the invoice lookup is not scoped to the caller's tenant.  
**Impact:** A user may retrieve another tenant's invoice by changing the identifier.  
**Remediation:** Query through the authenticated user's authorized tenant scope and enforce authorization server-side for every relevant action.  
**Acceptance criteria:** Same-tenant retrieval works; cross-tenant access is denied; sensitive fields are not disclosed; read/update/delete/export paths have regression tests.

## 3. Common remediation patterns

### SQL injection
Cause: untrusted input is concatenated into SQL syntax. Use parameterized queries or a safely used ORM.

```python
# Unsafe
query = "SELECT * FROM users WHERE email = '" + email + "'"

# Safer (placeholder syntax depends on the database driver)
cursor.execute("SELECT id, email FROM users WHERE email = %s", (email,))
```

Verify normal input, quote-containing input, and benign injection-like test strings in a controlled lab. Confirm input remains data and query structure is unchanged.

### Cross-site scripting
Cause: untrusted data is interpreted in an executable browser context. Prefer framework auto-escaping, context-aware output encoding, and safe DOM APIs.

```javascript
// Unsafe
element.innerHTML = userInput;

// Safer when plain text is intended
element.textContent = userInput;
```

Verify reflected, stored, and DOM-based rendering paths as applicable. Confirm payload-like text is inert and valid formatting still works.

### IDOR / BOLA / broken access control
Cause: a user-controlled object ID is trusted without checking ownership or policy. Scope data access to the authenticated principal/tenant and enforce authorization on the server for every action. Hidden UI controls and unpredictable identifiers are not authorization controls.

Verify with two test users and two test tenants across read, update, delete, and export operations.

### SSRF
Cause: the server fetches arbitrary user-controlled destinations. Prefer an allowlist or server-side destination identifiers. Validate scheme, host, port, resolved IP, and redirect targets. Block prohibited address ranges and apply network egress controls.

Verify approved destinations and denied destinations using local mocks. Do not probe third-party systems or cloud metadata endpoints.

### Path traversal
Cause: user-controlled path segments influence filesystem access. Prefer opaque file IDs mapped to server-controlled paths. If paths must be accepted, canonicalize and enforce containment inside an approved base directory, considering symlinks and race conditions.

### Security headers and configuration
Set security headers centrally where possible. Define and test CSP, use HSTS only after HTTPS readiness, remove debug disclosures, and verify success, error, redirect, and authenticated responses.

## 4. Verification method
### A. Preserve the original conditions
Record the URL, method, parameter, relevant headers, body/content type, authentication role, tenant context, payload, expected vulnerable behavior, and observed result.

### B. Replay after the fix
Replay the original test against the exact build intended for release. Then test appropriate variations: alternate encodings, parameter locations, HTTP methods, roles, ownership contexts, boundary values, redirects, API versions, and related routes.

### C. Run regression tests
Confirm valid business workflows still work; authorized users retain required access; unauthorized users remain denied; errors do not disclose secrets; logging/monitoring still work; and related endpoints use the corrected control.

### D. Independent confirmation
For high-risk findings, use a verifier other than the implementer where practical.

## 5. Evidence and closure
A verification record should include finding ID, build, environment, date, tester, original test result, variant tests, regression results, sanitized evidence references, final status, and rationale.

Never store raw passwords, session cookies, API keys, or unnecessary personal/customer data in tickets. Evidence should be reproducible, access-controlled, time-stamped, and retained according to policy.

## 6. CI/CD integration
A pipeline can combine:
- Unit tests for the vulnerable control.
- Integration tests for authorization and data boundaries.
- SAST checks to detect recurrence.
- DAST smoke tests against an isolated authorized test deployment.
- Dependency and configuration checks.
- Quality gates and documented exception approvals.

Illustrative GitHub Actions workflow:

```yaml
name: Remediation verification
on:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  regression:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install -r requirements.txt
      - run: pytest -q
```

For production workflows, pin third-party actions to reviewed immutable references, use least privilege, and do not expose privileged credentials to untrusted pull-request code. Run DAST only against a dedicated authorized target.

## 7. Metrics
Useful measures include:
- Mean time to remediate (MTTR), segmented by severity.
- Percentage closed within the organization's SLA.
- Retest pass rate and reopen rate.
- Recurrence rate by root cause.
- Age of overdue findings.
- Percentage of findings with complete evidence.

Avoid optimizing only for ticket closure counts. SLA thresholds should follow organizational policy and risk context.

## 8. Common mistakes
- Closing based only on a commit or developer statement.
- Testing only one exact payload.
- Treating scanner silence as proof when the endpoint was not reached.
- Fixing the UI while leaving server-side authorization broken.
- Relying only on a WAF rule for an application defect.
- Retesting a different build without recording it.
- Skipping positive regression tests.
- Saving credentials or customer data in evidence.
- Accepting risk without an approver and review date.
- Ignoring related endpoints that share the vulnerable component.

## 9. Closure checklist
- [ ] Finding reproduced and validated.
- [ ] Root cause documented.
- [ ] Owner and due date assigned.
- [ ] Secure fix implemented and reviewed.
- [ ] Unit/integration tests added.
- [ ] Original reproduction repeated against the correct build.
- [ ] Relevant variants and related endpoints tested.
- [ ] Regression tests passed.
- [ ] Evidence sanitized and attached.
- [ ] Status and residual risk recorded.

## References
- [OWASP Web Security Testing Guide](https://owasp.org/projects/web-security-testing-guide)
- [OWASP WSTG stable guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/)
- [OWASP Developer Guide — Verification](https://devguide.owasp.org/en/06-verification/)
- [OWASP DevSecOps Guideline](https://github.com/OWASP/DevSecOpsGuideline)
