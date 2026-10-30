# Authenticated Scanning - Solutions and Guidance

The exact settings depend on the target application, authentication protocol, ZAP release, and installed add-ons. Treat these as model answers rather than universal configuration values.

## Exercise 1 - Map the login flow
Record the login request method and path, required fields, redirects, cookies, and any CSRF or JavaScript requirements. Use ZAP's History tab to inspect requests and responses. Redact credentials, tokens, and session identifiers in screenshots and notes.

## Exercise 2 - Define a Context
A Context should represent the application under test. Include only the approved origin and paths. Exclude logout and state-changing operations that could terminate sessions or modify data. ZAP URL include/exclude regular expressions match the whole URL, so test them carefully.

## Exercise 3 - Configure session management
Choose cookie-based session management if the application uses session cookies, HTTP authentication session management if it uses the Authorization header, or an appropriate script-based method for custom behavior. Confirm a protected request includes the required session material. Do not copy live cookies into a report.

## Exercise 4 - Configure authentication
Select the authentication method that matches the actual login flow. A simple form may use form-based authentication; a JavaScript-heavy SPA may need browser-based authentication; a JSON login endpoint may need a JSON-based method. Configure a dedicated test user and verify login before scanning.

## Exercise 5 - Configure verification
Use a stable endpoint such as `/api/me` that returns a marker only when authenticated. A logged-in indicator could match a test username field; a logged-out indicator could match a login form marker. Test the indicators in both states. A generic `200 OK` is not enough because login pages often return 200.

## Exercise 6 - Authenticated spider
Choose the configured user for the spider. Confirm protected routes return application content rather than a login page. Compare crawler output with manually visited pages and document dynamic or multi-step routes that were not discovered.

## Exercise 7 - Session expiry
A good test demonstrates that the verification strategy recognizes expiry and ZAP re-authenticates. If the scanner continues sending requests anonymously, investigate the verification URL, indicator, session cookie handling, login flow, and any logout link encountered during crawling.

## Exercise 8 - Token-based API authentication
Store the token in a protected environment variable or secret store. Confirm the `/api/me` endpoint identifies the expected test identity. Ensure the token is scoped to the lab, has minimum permissions, and is revoked after the test. Never include it in the repository, command output, or report.

## Exercise 9 - Role-based scans
Run each role separately and compare endpoint coverage. A standard user should be denied access to admin-only routes unless the application intentionally grants that access. A 401 generally indicates missing or invalid authentication; a 403 generally indicates the request is understood but access is denied. Confirm the application's actual contract before interpreting a response.

## Exercise 10 - Troubleshooting guide

| Symptom | Likely causes | Diagnostic action |
|---|---|---|
| Login page repeatedly found | Login did not complete; context or credentials incorrect | Inspect login request/response and Context scope |
| 302 to login | Cookie absent, expired, or not replayed | Inspect session management and verification |
| 401 from API | Token missing, invalid, expired, wrong audience/scope | Verify token issuance and Authorization header |
| 403 from API | Authenticated identity lacks permission | Check role and endpoint authorization |
| SPA routes missing | Client-side routing or browser dependency | Use browser/AJAX spider and test workflows |
| Session expires during crawl | Expiry, rotation, CSRF, or logout route | Validate re-authentication and exclude logout |

## Exercise 11 - CI/CD design
A robust pipeline:
1. Deploys an ephemeral app and synthetic data.
2. Provisions a temporary least-privilege identity.
3. Injects secrets only at runtime.
4. Validates the identity using an authenticated-only endpoint.
5. Runs a bounded scan as the configured user.
6. Stores reports with access controls and retention limits.
7. Revokes the account/token and tears down the environment in an unconditional cleanup step.

Pin scanner images/actions and review upgrades. Do not run untrusted pull-request code with secrets.

## Exercise 12 - Final assessment checklist
The report should prove that authentication succeeded and remained valid during the scan. Include the verification mechanism, identity/role, authenticated endpoint evidence, URLs discovered, session-expiry behavior, and limitations. Do not include passwords, cookies, bearer tokens, or sensitive response bodies.

## Sample conclusion
> Authenticated DAST was performed against the authorized test environment using a dedicated low-privilege identity. The scanner's login flow and session handling were validated using an authenticated-only identity endpoint. Protected routes discovered by the crawler were compared with manually browsed routes. The assessment also documented session-expiry behavior and role-specific coverage. Results are limited to the configured identity, routes, and test data; privileged roles and untested workflows require separate coverage.
