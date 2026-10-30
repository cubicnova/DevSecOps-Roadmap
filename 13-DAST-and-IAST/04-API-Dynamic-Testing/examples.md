# API Dynamic Testing — Examples

> These examples are for a local mock API or an explicitly authorized test environment. Use synthetic accounts and data. Do not paste real credentials into source files or terminal history.

## 1. Define a local API target

Example base URL:

```bash
export API_BASE="http://127.0.0.1:8000"
```

Use a local service you control. Confirm the API is listening before testing:

```bash
curl -i "$API_BASE/health"
```

## 2. Inspect an OpenAPI document

Common locations include `/openapi.json`, `/swagger.json`, or `/api-docs`, depending on the framework.

```bash
curl -sS "$API_BASE/openapi.json" -o openapi.json
python -m json.tool openapi.json > /dev/null
```

List paths and methods with Python:

```python
import json
from pathlib import Path

spec = json.loads(Path("openapi.json").read_text(encoding="utf-8"))

for path, operations in spec.get("paths", {}).items():
    for method, operation in operations.items():
        if method.lower() in {
            "get", "post", "put", "patch", "delete",
            "options", "head", "trace"
        }:
            print(method.upper(), path, operation.get("summary", ""))
```

## 3. Baseline request and response

```bash
curl -i "$API_BASE/api/v1/profile"
```

Record the status, response content type, security headers, and response fields. If authentication is required, an unauthenticated response should follow the API's documented denial behavior.

## 4. Authenticated request using an environment variable

```bash
export API_TOKEN="replace-with-a-short-lived-lab-token"

curl -i \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Accept: application/json" \
  "$API_BASE/api/v1/profile"
```

Do not commit `API_TOKEN`. In CI, inject it from the platform's secret store. Avoid `set -x` or shell tracing while secrets are present.

## 5. Negative input tests

Missing required field:

```bash
curl -i -X POST "$API_BASE/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Wrong JSON type:

```bash
curl -i -X POST "$API_BASE/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{"age":"not-a-number"}'
```

Malformed JSON:

```bash
curl -i -X POST "$API_BASE/api/v1/users" \
  -H "Content-Type: application/json" \
  --data-binary '{"name":'
```

Expected behavior: controlled client errors with no stack trace, secrets, or internal implementation details. Use the contract's documented status codes.

## 6. BOLA test with two identities

Prepare two test users and an object owned by User A. Use a dedicated test environment.

```bash
export USER_A_TOKEN="short-lived-token-for-user-a"
export USER_B_TOKEN="short-lived-token-for-user-b"
export OBJECT_ID="test-object-created-by-user-a"

# Owner request: should be allowed.
curl -i \
  -H "Authorization: Bearer $USER_A_TOKEN" \
  "$API_BASE/api/v1/orders/$OBJECT_ID"

# Cross-user request: should not disclose User A's order.
curl -i \
  -H "Authorization: Bearer $USER_B_TOKEN" \
  "$API_BASE/api/v1/orders/$OBJECT_ID"
```

The second request should be denied according to the API's policy. A `403` or privacy-preserving `404` may be appropriate. Inspect the response body too; a denial status with leaked data is still a failure.

## 7. BFLA role test

Use a documented admin-only route in a lab API:

```bash
export BASIC_TOKEN="short-lived-basic-user-token"

curl -i \
  -H "Authorization: Bearer $BASIC_TOKEN" \
  "$API_BASE/api/v1/admin/audit"
```

Repeat with a dedicated admin test identity and compare the result. Do not use a real administrator account.

## 8. BOPLA / mass-assignment test

For a lab user-update endpoint, compare a normal update with an attempt to set a privileged property:

```bash
curl -i -X PATCH "$API_BASE/api/v1/profile" \
  -H "Authorization: Bearer $USER_A_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"displayName":"Lab User"}'
```

Then, only in a disposable lab, test whether a client-controlled privileged property is accepted:

```bash
curl -i -X PATCH "$API_BASE/api/v1/profile" \
  -H "Authorization: Bearer $USER_A_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"displayName":"Lab User","isAdmin":true}'
```

Verify persisted state through an authorized test method. A response that echoes an input field does not alone prove that the field was applied.

## 9. Rate-limit behavior (conservative)

Agree a low request budget with the application owner. This simple loop sends at most five requests with a pause:

```bash
for i in 1 2 3 4 5; do
  curl -sS -o /dev/null -w "%{http_code}\n" \
    "$API_BASE/api/v1/search?q=training"
  sleep 2
done
```

Record status codes and any `Retry-After` header. Do not increase request volume to cause service degradation.

## 10. ZAP API scan using OpenAPI

If the API definition is available to the container:

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

The target and API definition must be reachable from inside the container. Check Docker networking for your OS. Confirm scan scope and use only a lab target.

## 11. Schemathesis schema-driven test

Install Schemathesis in an isolated Python environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install schemathesis
```

Run against the local API schema:

```bash
schemathesis run http://127.0.0.1:8000/openapi.json
```

For authenticated testing, consult the installed Schemathesis CLI help and pass a short-lived lab credential using its supported header configuration. Do not put a live token in a committed command or workflow file.

## 12. Postman/Newman collection in CI

Install Newman:

```bash
npm install --save-dev newman
```

Run a checked-in collection with a local environment file:

```bash
npx newman run tests/api-security.postman_collection.json \
  -e tests/local.postman_environment.json
```

Do not commit real secrets in environment exports. Use CI variables or a secure secret store for credentials.

## 13. Python response checks

```python
import os
import requests

base = os.environ.get("API_BASE", "http://127.0.0.1:8000")
token = os.environ.get("API_TOKEN")

headers = {"Accept": "application/json"}
if token:
    headers["Authorization"] = f"Bearer {token}"

response = requests.get(
    f"{base}/api/v1/profile",
    headers=headers,
    timeout=10,
)

print("Status:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
print("Cache-Control:", response.headers.get("Cache-Control"))
print("Body preview:", response.text[:300])
```

Do not print full responses if they may contain personal or confidential information.

## 14. CI pipeline outline

```yaml
name: API Dynamic Tests

on:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  api-dast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Start test API
        run: |
          docker compose up -d api
          # Add a bounded health-check loop here.

      - name: Run schema-driven tests
        run: |
          python -m pip install schemathesis
          schemathesis run http://127.0.0.1:8000/openapi.json

      - name: Run ZAP API scan
        run: |
          mkdir -p reports
          docker run --rm -t \
            -v "$PWD/reports:/zap/wrk/:rw" \
            ghcr.io/zaproxy/zaproxy:stable \
            zap-api-scan.py \
            -t http://host.docker.internal:8000/openapi.json \
            -f openapi \
            -r api-dast-report.html

      - name: Upload reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: api-dast-reports
          path: reports/
          if-no-files-found: warn

      - name: Stop test API
        if: always()
        run: docker compose down
```

This is a structural example, not a drop-in workflow: configure runner/container networking, ensure the API is reachable from the ZAP container, add bounded health checks, pin actions to reviewed full commit SHAs, and define scan exit/quality-gate behavior.

## 15. Evidence template

For each confirmed issue, capture:

```text
Finding:
Endpoint and method:
Environment:
Test identity/role:
Preconditions:
Sanitized request:
Sanitized response:
Expected behavior:
Observed behavior:
Impact:
Reproduction steps:
Remediation:
Retest result:
```

Remove tokens, cookies, personal data, and unrelated customer records before sharing evidence.
