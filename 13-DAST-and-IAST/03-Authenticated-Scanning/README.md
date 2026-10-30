# 03 - Authenticated Scanning

## Learning objectives
After completing this module, learners should be able to:
- Explain why authenticated DAST is necessary for applications with protected functionality.
- Distinguish authentication, session management, and authentication verification.
- Configure an authorized ZAP context, test user, and login/session strategy.
- Validate that crawlers and scanners remain authenticated throughout a scan.
- Handle cookie, HTTP Basic/Bearer token, form, browser-based, and API authentication patterns.
- Protect credentials, tokens, reports, and test identities in local and CI environments.
- Assess role-based coverage and identify authentication-related scan gaps.

## 1. What is authenticated scanning?
Authenticated scanning runs DAST from the perspective of one or more valid application users. It helps discover pages, APIs, and behaviors that are inaccessible to anonymous visitors.

A scan is not genuinely authenticated merely because credentials were supplied. The scanner must:
1. Authenticate successfully.
2. Maintain the application's session.
3. Detect when the session expires or becomes invalid.
4. Re-authenticate when required.
5. Confirm that requests reach protected functionality as the intended user.

A scanner that silently receives login redirects or public pages may produce a misleadingly clean report.

## 2. Three essential concepts

| Concept | Purpose | Examples |
|---|---|---|
| Authentication method | Establish identity | Form login, JSON login, browser login, HTTP auth, API token |
| Session management | Keep identity attached to later requests | Cookies, Authorization header, custom script |
| Authentication verification | Determine whether the session is still valid | Logged-in/out regex, polling a `/api/me` endpoint |

ZAP associates these settings with a Context. Users hold the credentials used by the configured authentication method.

## 3. Common authentication patterns

### Cookie-based form login
The scanner submits a login form and receives a session cookie. The cookie must be preserved on later requests. CSRF tokens, redirects, MFA, and JavaScript flows may require additional configuration or browser-based authentication.

### HTTP Basic authentication
The client sends an `Authorization: Basic ...` header. Use only over HTTPS outside an isolated local lab. Do not paste encoded credentials into source control; Base64 is not encryption.

### Bearer token / API key
The scanner sends a token in an HTTP header, commonly `Authorization: Bearer ...` or a documented API-key header. Use a dedicated test token with least privilege and short lifetime where possible.

### Browser-based / SPA login
A real browser performs the login flow, useful when JavaScript, redirects, or client-side behavior is required. Browser automation may need a supported browser and add-ons.

### OAuth / OIDC
A scanner may need a test client, dedicated test identity, token acquisition flow, and refresh strategy. Avoid reusing personal accounts or production client secrets.

## 4. ZAP configuration workflow
The exact labels may vary by ZAP version and installed add-ons. Consult the current ZAP documentation.

1. Start ZAP and browse the authorized test application through its proxy.
2. Create a Context for the application and include only approved URLs.
3. Configure the application's session management method.
4. Configure the authentication method and required parameters.
5. Define logged-in and logged-out indicators, or a supported verification strategy.
6. Create a dedicated test User in the Context.
7. Test authentication and verify the user can access a protected page.
8. Run the spider/AJAX spider as the configured user.
9. Inspect requests and responses to confirm the session is still valid.
10. Run passive checks first; request approval and isolate the environment before active scanning.

### Verification is mandatory
Choose an endpoint that reliably returns authenticated-only content, such as `/api/me`, and a response marker that cannot appear in the anonymous response. Do not use a generic HTTP 200 as proof of authentication.

## 5. Example ZAP Automation Framework plan
The following is an illustrative starting point for a local training application. Authentication method parameters, job names, and schema can change across ZAP releases and add-ons. Validate the plan against the current Automation Framework documentation before use.

```yaml
env:
  contexts:
    - name: training-app
      urls:
        - http://127.0.0.1:8080
      includePaths:
        - "http://127\\.0\\.0\\.1:8080/.*"
      authentication:
        method: browser
        parameters:
          loginPageUrl: "http://127.0.0.1:8080/login"
        verification:
          method: poll
          parameters:
            pollUrl: "http://127.0.0.1:8080/api/me"
            pollFrequency: 60
            pollUnits: requests
            loggedInRegex: '"username"'
      sessionManagement:
        method: cookie
      users:
        - name: dast-reader
          credentials:
            username: "${ZAP_USER}"
            password: "${ZAP_PASSWORD}"
```

The snippet illustrates the concepts and may need adjustment for the target app, ZAP version, and authentication add-ons. Never put real credentials directly in this file.

## 6. Token-based scanning
For a simple local lab API, an Authorization header can be supplied through an environment variable or secret store. Example request:

```bash
curl -i \
  -H "Authorization: Bearer $DAST_TEST_TOKEN" \
  http://127.0.0.1:8080/api/me
```

Confirm the token is accepted and the endpoint returns the expected test identity. Do not echo the token, enable shell tracing (`set -x`), or include it in command-line arguments that may be exposed in process listings or CI logs. Prefer the scanner's supported secret/environment-variable mechanism.

## 7. Multi-role authenticated scanning
Test separate identities for materially different authorization levels:
- Anonymous visitor.
- Standard user.
- Privileged user / administrator.
- Tenant A and Tenant B test users where multi-tenancy exists.

Do not assume a successful scan as an administrator covers standard-user access control. Compare the endpoints and actions reachable by each role. Use synthetic data and ensure the test users cannot affect real customers or shared production resources.

## 8. Common failure modes

| Symptom | Likely cause | What to check |
|---|---|---|
| Only login page is scanned | Login failed or context scope is wrong | Authentication test, URL include rules |
| Scanner gets 302 to login | Cookie/token missing or expired | Session management and verification |
| Scan starts authenticated then becomes anonymous | Expiry, logout route, CSRF/session rotation | Re-authentication and logout exclusions |
| SPA pages are missed | JavaScript routes not discovered | AJAX/browser spider and workflows |
| API returns 401 | Wrong token, audience, scope, or header | Token claims and API auth contract |
| API returns 403 | Identity authenticated but not authorized | Role/permission configuration |
| One role's routes are missing | Only one user was scanned | Separate role-specific users and runs |

## 9. Credential and report hygiene
- Use dedicated, low-privilege test identities.
- Use short-lived test tokens and rotate/revoke them after the assessment.
- Store secrets in the CI secret manager; never commit `.env` files with real values.
- Avoid printing request headers, cookies, tokens, or login bodies.
- Restrict report access and retention; reports can contain sensitive data.
- Ensure test identities have synthetic data and safe permissions.
- Clean up temporary accounts, tokens, sessions, and environments.

## 10. CI/CD integration principles
- Deploy an isolated ephemeral environment for each pipeline run.
- Provision test identities and seed synthetic data.
- Inject secrets only at runtime using protected CI secrets.
- Pin scanner images/actions to reviewed versions or immutable digests/SHAs.
- Run authenticated passive discovery first.
- Verify login success before treating scan results as meaningful.
- Separate role-specific scans and report coverage by role.
- Tear down the environment and revoke temporary credentials even if a scan fails.

## Knowledge check
1. Why are authentication, session management, and verification separate settings?
2. Why is HTTP 200 not a reliable logged-in indicator?
3. What is the difference between HTTP 401 and 403?
4. Why should a standard user and an administrator be scanned separately?
5. Why should credentials not be placed directly in a YAML plan?
6. What evidence proves the scanner remained authenticated?

## Further reading
- ZAP Authentication: https://www.zaproxy.org/docs/desktop/start/features/authentication/
- ZAP Authentication Concepts: https://www.zaproxy.org/docs/getting-further/authentication/concepts/
- ZAP Session Handling: https://www.zaproxy.org/docs/getting-further/authentication/session-handling/
- ZAP Users: https://www.zaproxy.org/docs/desktop/start/features/users/
- OWASP DevSecOps DAST Guideline: https://owasp.github.io/DevSecOpsGuideline/2-Process/2-4-Test/2-4-2-Dynamic-Application-Security-Testing/
