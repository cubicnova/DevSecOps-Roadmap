# Remediation and Verification — Examples

All examples are educational. Use synthetic data and authorized lab systems only.

## 1. Parameterized SQL

```python
def find_user(cursor, email):
    cursor.execute(
        "SELECT id, email FROM users WHERE email = %s",
        (email,)
    )
    return cursor.fetchone()
```

The value is bound separately from SQL syntax. Confirm placeholder syntax for the database driver. Test normal input, quote characters, and benign injection-like strings.

## 2. Safe DOM text insertion

```html
<div id="output"></div>
<script>
  const userInput = "Example text";
  document.querySelector("#output").textContent = userInput;
</script>
```

For plain text, `textContent` avoids interpreting the value as HTML. Verify every rendering context where the same value is used.

## 3. Tenant-scoped object access

```python
def get_invoice(current_user, invoice_id, repository):
    invoice = repository.find_for_tenant(
        invoice_id=invoice_id,
        tenant_id=current_user.tenant_id,
    )
    if invoice is None:
        raise NotFound()
    return invoice
```

The lookup is scoped to the authenticated tenant. Apply equivalent authorization to update, delete, export, and nested-resource operations.

## 4. Canonical path containment

```python
from pathlib import Path

BASE = Path("/srv/app/approved-files").resolve()

def resolve_download(filename):
    candidate = (BASE / filename).resolve()
    if candidate == BASE or BASE not in candidate.parents:
        raise ValueError("Invalid file path")
    if not candidate.is_file():
        raise FileNotFoundError()
    return candidate
```

Prefer server-controlled file IDs over arbitrary path input. Consider symlinks, race conditions, and platform-specific path behavior.

## 5. Authorization regression test

```python
def test_user_cannot_read_other_tenant_invoice(client, user_a, invoice_b):
    response = client.get(
        f"/api/invoices/{invoice_b.id}",
        headers=user_a.auth_headers,
    )
    assert response.status_code in (403, 404)
    assert "sensitive_invoice_field" not in response.text
```

Adapt fixtures and response policy to the application. Test that same-tenant access still succeeds.

## 6. Retest record JSON

```json
{
  "finding_id": "DAST-2026-014",
  "build": "release-2.8.1+build.412",
  "environment": "staging",
  "original_test_replayed": true,
  "variant_tests": ["cross-tenant GET", "cross-tenant PATCH"],
  "regression_tests_passed": true,
  "result": "fixed",
  "evidence": ["request-redacted.txt", "test-results.xml"]
}
```

Do not include real tokens, cookies, passwords, or customer records.

## 7. Remediation age calculation

```python
from datetime import date

findings = [
    {"id": "F-101", "opened": date(2026, 10, 1),
     "closed": date(2026, 10, 3)},
    {"id": "F-102", "opened": date(2026, 10, 2),
     "closed": None},
]

today = date.today()
for item in findings:
    end = item["closed"] or today
    print(item["id"], (end - item["opened"]).days, "days")
```

This calculates age only. Define severity-specific SLA thresholds separately and document paused tickets and accepted risks.

## 8. GitHub Actions regression job

```yaml
name: Security regression
on:
  pull_request:
  workflow_dispatch:
permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install -r requirements.txt
      - run: pytest -q
```

Pin actions to reviewed commit SHAs for production. Do not expose deployment credentials to untrusted pull requests.

## 9. Example closure note

> Retest completed against the recorded staging build. The original request and cross-tenant update variant no longer expose or modify another tenant's invoice. Same-tenant retrieval and update regression tests passed. Sanitized request/response evidence and automated test output are attached. Status: Fixed.

## 10. Example partial-fix note

> The main server-rendered response now encodes the reflected value, but a secondary client-side rendering path still inserts it into an unsafe HTML sink. Keep the finding open, document the remaining path, and add a regression test for that rendering flow.
