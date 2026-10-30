# Authenticated Scanning - Examples

> All examples are for an owned local lab or an explicitly authorized test environment. Use synthetic identities and never paste production secrets into examples or source control.

## 1. Verify an authenticated session manually
```bash
curl -i \
  -b "$COOKIE_JAR" \
  http://127.0.0.1:8080/api/me
```
The response should identify the expected test account. A `200 OK` alone is insufficient; inspect the response body for a stable authenticated-only marker.

## 2. Save cookies without printing them
```bash
umask 077
curl -sS -c "$COOKIE_JAR" \
  -d "username=$DAST_USER&password=$DAST_PASSWORD" \
  -o /dev/null \
  http://127.0.0.1:8080/login
```
This form is illustrative. Real applications may require CSRF tokens, JSON bodies, redirects, MFA, or browser interaction. Protect and delete the cookie jar after use.

## 3. Reuse a cookie jar for a protected endpoint
```bash
curl -i -b "$COOKIE_JAR" http://127.0.0.1:8080/account
```
Compare with an unauthenticated request. Confirm that the authenticated response contains protected content and the anonymous response does not.

## 4. Bearer token request
```bash
curl -i \
  -H "Authorization: Bearer ${DAST_TEST_TOKEN}" \
  http://127.0.0.1:8080/api/me
```
Keep the token in an environment variable injected by a secret manager. Do not enable shell tracing or print the variable.

## 5. ZAP Automation Framework plan (illustrative)
```yaml
env:
  contexts:
    - name: local-app
      urls:
        - http://127.0.0.1:8080
      authentication:
        method: browser
        parameters:
          loginPageUrl: http://127.0.0.1:8080/login
        verification:
          method: poll
          parameters:
            pollUrl: http://127.0.0.1:8080/api/me
            pollFrequency: 60
            pollUnits: requests
            loggedInRegex: '"username"'
      sessionManagement:
        method: cookie
      users:
        - name: test-reader
          credentials:
            username: "${ZAP_USER}"
            password: "${ZAP_PASSWORD}"
```
Validate the exact schema and method parameters against the installed ZAP version and required add-ons. The regex must match content present only in an authenticated response.

## 6. Basic auth header
```bash
curl -i -u "$DAST_USER:$DAST_PASSWORD" \
  http://127.0.0.1:8080/private/
```
Use only for an isolated lab over HTTP. For non-local environments, use HTTPS and a secret-safe mechanism. Do not use `-v` because verbose output can expose sensitive headers.

## 7. Python authentication-state check
```python
# examples/auth_state_check.py
import os
import requests

BASE_URL = os.getenv("DAST_BASE_URL", "http://127.0.0.1:8080")
TOKEN = os.getenv("DAST_TEST_TOKEN")

if not TOKEN:
    raise SystemExit("Set DAST_TEST_TOKEN in your environment.")

response = requests.get(
    f"{BASE_URL}/api/me",
    headers={"Authorization": f"Bearer {TOKEN}"},
    timeout=10,
)
print("HTTP status:", response.status_code)

if response.status_code == 200:
    data = response.json()
    # Print only a non-sensitive test identity marker.
    print("Authenticated identity marker present:", bool(data.get("username")))
elif response.status_code == 401:
    print("Not authenticated: token missing, invalid, or expired.")
elif response.status_code == 403:
    print("Authenticated or recognized, but not authorized for this resource.")
else:
    print("Unexpected response; inspect securely in the authorized lab.")
```
Install dependency with `python -m pip install requests`. Avoid logging the token or full response body.

## 8. Multi-role coverage matrix
| Role | Test identity | Protected route | Expected result |
|---|---|---|---|
| Anonymous | None | `/api/me` | 401 or login redirect |
| Standard | `dast-reader` | `/api/me` | 200, reader identity |
| Standard | `dast-reader` | `/admin` | 403 or safe denial |
| Admin | `dast-admin` | `/admin` | 200, admin-only page |

Adjust expected responses to the application's documented behavior. The purpose is to verify both authentication and authorization boundaries.

## 9. CI secret injection (conceptual)
```yaml
steps:
  - name: Run authenticated DAST
    env:
      ZAP_USER: ${{ secrets.DAST_TEST_USER }}
      ZAP_PASSWORD: ${{ secrets.DAST_TEST_PASSWORD }}
    run: |
      # Invoke a pinned ZAP Automation Framework container/action.
      # Do not print environment variables or enable shell tracing.
      ./run-zap-authenticated-scan.sh
```
The script and scanner configuration must be implemented for the chosen ZAP release. Restrict the job to trusted branches/environments and ensure the test app is isolated.
