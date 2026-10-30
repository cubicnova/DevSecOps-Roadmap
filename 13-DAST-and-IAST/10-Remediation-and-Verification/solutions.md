# Remediation and Verification — Solutions and Guidance

These are reference approaches. Adapt them to your language, framework, database, and authorization model.

## Exercise 1 — Ticket
**Title:** Enforce tenant-level authorization on order retrieval.  
**Root cause:** The endpoint looks up an order by client-supplied ID without scoping it to the authenticated user's tenant.  
**Fix:** Query through the user's tenant scope and enforce authorization on every action.  
**Acceptance criteria:** Same-tenant access succeeds; cross-tenant access is denied; sensitive data is not disclosed; read/update/delete/export paths have tests.

## Exercise 2 — SQL injection
Use parameter binding:

```python
def find_account(cursor, account_id):
    cursor.execute(
        "SELECT id, status FROM accounts WHERE id = %s",
        (account_id,)
    )
    return cursor.fetchone()
```

Test normal and quote-containing values. A strong regression test verifies that input is treated as data and cannot alter query structure.

## Exercise 3 — Object-level authorization
Scope the query to the authenticated tenant:

```python
def get_order_for_user(user, order_id, repository):
    order = repository.find_by_id_and_tenant(
        order_id=order_id,
        tenant_id=user.tenant_id,
    )
    if order is None:
        raise NotFound()
    return order
```

Test cross-tenant denial and same-tenant success. Use a consistent `403` or `404` policy and ensure unauthorized data is not disclosed.

## Exercise 4 — XSS
For plain text:

```javascript
document.querySelector("#output").textContent = userInput;
```

For server templates, use contextual auto-escaping. If rich HTML is required, use a maintained sanitizer with a strict allowlist. Do not disable escaping globally. Test every rendering path that consumes the value.

## Exercise 5 — Path traversal
Prefer opaque identifiers mapped to server-controlled paths:

```python
FILES = {
    "guide": "/srv/app/approved-files/guide.pdf",
    "policy": "/srv/app/approved-files/policy.pdf",
}

def get_file(file_id):
    path = FILES.get(file_id)
    if path is None:
        raise FileNotFoundError()
    return path
```

If arbitrary paths are unavoidable, canonicalize and verify containment. Consider symlinks, race conditions, and OS-specific semantics.

## Exercise 6 — SSRF
Prefer a destination key mapped to a configured endpoint rather than accepting arbitrary URLs. If URL fetching is necessary:
- Permit only required schemes.
- Enforce host and port allowlists.
- Resolve DNS and reject prohibited address ranges.
- Revalidate redirect destinations.
- Apply network egress controls.
- Set connection timeouts and response-size limits.
- Log decisions without secrets.

Use local mock destinations for tests.

## Exercise 7 — Retest result
A meaningful retest records finding ID, original request/preconditions, build/environment, date/tester, original test result, variants, regression tests, evidence, and conclusion.

- **Fixed:** Original path and relevant variants fail for the intended security reason; valid use succeeds.
- **Partially fixed:** A related path remains vulnerable.
- **Not fixed:** Original weakness still reproduces.
- **Unable to verify:** Target/build/authentication/test setup prevented a meaningful test.

Scanner silence alone is not proof of a fix.

## Exercise 8 — Regression tests
Pair a negative security test with a positive business-flow test. For authorization, assert cross-tenant denial and same-tenant success. For input handling, assert untrusted structure is not interpreted while valid input remains accepted.

## Exercise 9 — Evidence package

```text
evidence/
├── README.md
├── finding-summary.md
├── original-request-redacted.txt
├── retest-request-redacted.txt
├── response-summary.txt
├── regression-test-results.txt
└── build-info.txt
```

Explain each artifact and how to reproduce the test. Store evidence in an access-controlled location with an appropriate retention period.

## Exercise 10 — CI example

```yaml
name: Security regression
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

For production, pin actions to reviewed commit SHAs, use least privilege, protect secrets, and scan only an isolated authorized test deployment.

## Exercise 11 — Closure policy
Only an authorized verifier should close a finding. Require replay of the original scenario, relevant variants, regression evidence, and sanitized records. High-risk findings should receive independent verification where practical. Risk acceptance needs an approver, rationale, compensating controls, owner, and expiry/review date. Reopened findings retain their history.

## Exercise 12 — Metrics

```text
Remediation time = verified closure date - opened date

SLA compliance (%) =
  findings closed within applicable SLA
  / findings due and closed in the measurement period
  * 100

Retest pass rate (%) =
  findings passing retest / findings retested * 100

Reopen rate (%) =
  findings reopened after closure / findings previously closed * 100
```

Report by severity and asset tier. Explain treatment of paused tickets, accepted risks, and findings awaiting retest.

## Exercise 13 — Coverage matrix

| Component | Operation | Role | Expected control |
|---|---|---|---|
| Orders API | Read | Tenant member | Own tenant only |
| Orders API | Update | Tenant member | Own tenant and valid state |
| Orders API | Delete | Tenant admin | Own tenant and admin permission |
| Export API | Export | Tenant member | Own tenant only |
| Nested items API | Read/update | Tenant member | Parent authorization enforced |

Assess every relevant route and operation that uses the shared helper.

## Exercise 14 — Report outline

```markdown
# Remediation Verification Report

## Finding
- ID:
- Title:
- Severity:
- Affected asset:
- Original build:

## Root Cause
Describe the underlying design or implementation weakness.

## Remediation
Describe the code/configuration change and commit.

## Verification
- Original reproduction:
- Variant tests:
- Regression tests:
- Environment and build:
- Tester and date:

## Evidence
List sanitized evidence references.

## Result
Fixed / Partially Fixed / Not Fixed / Unable to Verify

## Residual Risk
Document remaining exposure and follow-up actions.
```

## Reviewer checklist
- [ ] Root cause addressed, not merely hidden.
- [ ] Fix is in the exact build under test.
- [ ] Original reproduction repeated.
- [ ] Variants and related endpoints assessed.
- [ ] Positive and negative regression tests pass.
- [ ] Evidence is sanitized and reproducible.
- [ ] Closure status matches the evidence.
- [ ] Residual risks and exceptions documented.
