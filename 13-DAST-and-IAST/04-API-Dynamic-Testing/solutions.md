# API Dynamic Testing — Solutions and Reference Answers

These are reference approaches. Adapt endpoint names, authentication methods, expected status codes, and test limits to the API contract and rules of engagement.

## Solution 1 — API inventory

Extract OpenAPI paths and methods:

```python
import json
from pathlib import Path

spec = json.loads(Path("openapi.json").read_text(encoding="utf-8"))
methods = {
    "get", "post", "put", "patch", "delete",
    "options", "head", "trace"
}

for path, operations in spec.get("paths", {}).items():
    for method, operation in operations.items():
        if method.lower() in methods:
            security = operation.get("security", spec.get("security", []))
            print(
                method.upper(),
                path,
                operation.get("operationId", ""),
                "security=", bool(security)
            )
```

This is a first-pass inventory. Resolve `$ref` values and inspect components, callbacks, webhooks, server URLs, and external references when needed.

## Solution 2 — Baseline testing

For each endpoint, record:
- Request method and path.
- Test identity and role.
- Status code and response content type.
- Required headers and authentication.
- Response schema and sensitive fields.
- Expected behavior from the contract.

Compare authenticated and unauthenticated responses without exposing real tokens or personal data.

## Solution 3 — Input validation

Expected secure behavior:
- Missing required fields and malformed JSON are rejected with controlled client errors.
- Wrong types do not trigger unhandled exceptions.
- Boundary values follow documented constraints.
- Error responses do not expose stack traces, SQL details, secrets, or internal hostnames.
- Unknown properties follow the documented schema and server-side policy.

A `400`, `415`, or `422` may be appropriate depending on the contract; status codes should be consistent and documented.

## Solution 4 — Authentication

Expected checks:
- Missing or invalid credentials are rejected.
- Expired and revoked tokens are not accepted.
- JWT signature is verified with an approved algorithm.
- `iss`, `aud`, and time claims are validated where applicable.
- OAuth scopes and redirect URIs are constrained.
- API keys are not placed in URLs or exposed in logs.
- Logout and credential changes invalidate sessions/tokens according to policy.

Do not assume decoding a JWT proves it is valid; signature and claim validation are required.

## Solution 5 — BOLA / IDOR

Reference procedure:

1. User A creates object `object-A`.
2. User A reads the object successfully.
3. User B requests `object-A`.
4. User B must not receive the protected object or be able to modify it.
5. Repeat for each object type and relevant operation.

A denial may use `403` or a privacy-preserving `404`, depending on policy. Verify response bodies and side effects; a denial status alone is not enough.

## Solution 6 — BFLA

Build a role-operation matrix:

| Operation | Anonymous | Basic user | Admin |
|---|---:|---:|---:|
| Read own profile | Deny | Allow | Allow |
| Read another user's profile | Deny | Deny | Policy-dependent |
| Read admin audit data | Deny | Deny | Allow |
| Change global settings | Deny | Deny | Allow |

The exact expected permissions must come from the application's authorization design. Check every method and API version that exposes the function.

## Solution 7 — BOPLA and excessive data exposure

Reference approach:
- Identify sensitive properties in the data model.
- Compare response fields for each role.
- Check whether update endpoints accept client-controlled ownership or privilege properties.
- Verify persisted state through a separate authorized read.
- Confirm that server-side allowlists govern writable fields.

A response echoing a submitted property is not proof that the property was persisted or used.

## Solution 8 — Injection and parser robustness

Test only approved input surfaces with non-destructive values. Record:
- Input and endpoint.
- Expected schema behavior.
- Actual response and status.
- Any unexpected error or timing difference.
- Whether the result is reproducible.
- Relevant server-side evidence if access is authorized.

A generic error or changed response is not automatically proof of injection. Confirm with a controlled test and application-owner review.

## Solution 9 — Resource consumption

A safe assessment:
1. Agree a request rate, total request budget, and stop threshold.
2. Test with a small request count and pauses.
3. Observe `429`, `Retry-After`, and rate-limit headers.
4. Review page-size, body-size, and concurrency constraints.
5. Stop if latency or errors exceed the agreed threshold.

Do not run uncontrolled stress or denial-of-service tests as part of routine API DAST.

## Solution 10 — Business logic

Document the workflow's valid state transitions. Test a limited set of safe deviations, such as repeating a one-time action in a disposable environment or attempting a step out of order. Verify that the server, not just the client, enforces state, ownership, price, quantity, and approval rules.

## Solution 11 — ZAP and Schemathesis

ZAP API scan example:

```bash
mkdir -p reports

docker run --rm -t \
  -v "$(pwd)/reports:/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py \
  -t http://host.docker.internal:8000/openapi.json \
  -f openapi \
  -r api-dast-report.html
```

Schemathesis example:

```bash
python -m pip install schemathesis
schemathesis run http://127.0.0.1:8000/openapi.json
```

ZAP can identify runtime issues based on its rules and observed API surface. Schemathesis generates tests from the schema and checks behavior against contract expectations. Neither automatically proves BOLA/BFLA or business-logic correctness; add explicit tests using multiple identities and known object relationships.

## Solution 12 — CI/CD gate

A robust pipeline separates these outcomes:

| Pipeline outcome | Meaning |
|---|---|
| Target startup failed | Environment problem; do not call it a clean scan |
| Scanner failed | Tool/execution problem; fail or mark inconclusive |
| Schema validation failed | Contract or validation issue |
| Confirmed policy violation | Security gate failure |
| Scan completed with no blocking findings | Pass under the defined policy |
| Report upload failed | Evidence-retention problem; handle according to policy |

Use `if: always()` for artifact upload and cleanup where appropriate, but do not mask the original scan exit status.

## Solution 13 — Inventory drift

Compare:
- OpenAPI paths/methods.
- Gateway route configuration.
- Observed requests from an approved test dataset.
- Deprecated API versions and ownership records.

Investigate discrepancies with service owners. A route absent from the specification may be an undocumented endpoint, a legitimate internal route, or an inventory error; validate before classifying.

## Solution 14 — Capstone report structure

Suggested final report:

```text
1. Executive summary
2. Scope and authorization
3. Test environment and identities
4. API inventory and specification review
5. Methodology and tools
6. Authentication findings
7. Authorization findings (BOLA/BFLA/BOPLA)
8. Input validation and injection findings
9. Resource-consumption observations
10. Business-logic findings
11. Automated DAST and schema-test results
12. Risk-ranked findings with sanitized evidence
13. Remediation recommendations
14. Retest results
15. Limitations and residual risk
```

## Example finding: Broken Object Level Authorization

**Title:** User can access another user's order

**Category:** OWASP API1:2023 — Broken Object Level Authorization

**Precondition:** Two test accounts and an order created by User A.

**Test:** Authenticate as User B and request the order identifier owned by User A.

**Expected:** The API denies access and does not disclose object data.

**Observed:** Record the actual status and sanitized response only if the issue is reproduced.

**Impact:** Unauthorized access to another user's data or actions, depending on exposed operations.

**Remediation:** Enforce object ownership/tenant authorization on the server for every object operation. Do not rely on client-supplied identifiers or hidden UI controls.

**Retest:** Repeat the same test using a separate identity after the fix.

## Further reading

- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [OWASP API Security Testing](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/12-API_Testing/)
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [OWASP DevSecOps API Security](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-4-Test/2-4-4-API-Security/)
- [ZAP API Scan](https://www.zaproxy.org/docs/docker/api-scan/)
- [Schemathesis](https://schemathesis.readthedocs.io/)
