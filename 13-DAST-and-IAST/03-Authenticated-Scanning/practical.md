# Authenticated Scanning - Practical Exercises

## Lab safety
- Use an owned local training application or a target covered by written authorization.
- Create dedicated synthetic accounts; never use personal or production accounts.
- Use low-privilege credentials first.
- Keep scan scope narrow and exclude destructive operations.
- Start with authentication validation and passive scanning.
- Never submit real passwords, cookies, or bearer tokens in reports or source control.

## Exercise 1 - Map the login flow
1. Browse the local application through ZAP.
2. Record login URL, method, form fields, redirects, and response cookies.
3. Identify whether the app uses cookie, HTTP, or token-based session management.
4. Identify any CSRF token or JavaScript dependency.

**Deliverable:** Authentication flow diagram and notes.

## Exercise 2 - Define an application Context
1. Create a ZAP Context for the lab.
2. Include only the target host and approved paths.
3. Exclude logout and destructive endpoints.
4. Confirm out-of-scope URLs are not included.

**Deliverable:** Context scope record.

## Exercise 3 - Configure session management
1. Determine whether the app uses cookies or an Authorization header.
2. Configure the matching session management method.
3. Authenticate manually through the proxied browser.
4. Inspect a protected request to verify the session material is present.

**Deliverable:** Session management evidence with secrets redacted.

## Exercise 4 - Configure authentication
1. Select a supported authentication method.
2. Configure the login URL and required parameters.
3. Create a dedicated test user in the Context.
4. Test the authentication process.
5. Confirm the app recognizes the test user.

**Deliverable:** Authentication configuration notes; do not include credentials.

## Exercise 5 - Configure verification
1. Find an endpoint that returns authenticated-only information.
2. Define a logged-in indicator or polling verification rule.
3. Identify a logged-out response.
4. Test both states by logging in and logging out.
5. Confirm the indicator does not match anonymous content.

**Deliverable:** Verification rule and test results.

## Exercise 6 - Run an authenticated spider
1. Select the configured test user.
2. Run the traditional spider or AJAX spider as appropriate.
3. Review discovered URLs.
4. Compare results with a manual browsing session.
5. Identify protected pages that were missed.

**Deliverable:** URL coverage comparison.

## Exercise 7 - Test session expiry
1. Use a short-lived lab session if available.
2. Allow the session to expire or invalidate it through the lab's supported mechanism.
3. Observe whether ZAP detects the unauthenticated state.
4. Verify whether it re-authenticates successfully.
5. Record any requests that were scanned anonymously.

**Deliverable:** Session expiry test report.

## Exercise 8 - Token-based API authentication
1. Create a dedicated short-lived lab token.
2. Store it in an environment variable.
3. Call the test `/api/me` endpoint.
4. Confirm the scanner can use the token through a supported secure mechanism.
5. Rotate or revoke the token after the exercise.

**Deliverable:** Token-auth test record. Do not submit the token.

## Exercise 9 - Role-based scans
1. Create standard-user and admin test identities.
2. Configure separate ZAP users.
3. Run discovery for each role separately.
4. Compare routes and actions.
5. Confirm a standard user cannot access admin-only functionality.

**Deliverable:** Role coverage matrix.

## Exercise 10 - Diagnose authentication failures
Simulate or inspect these symptoms:
- Login page repeatedly rediscovered.
- 302 redirect to login during scan.
- API returns 401.
- API returns 403.
- SPA route is not discovered.
- Session expires during crawling.

For each, state likely causes and the next diagnostic step.

**Deliverable:** Troubleshooting table.

## Exercise 11 - CI/CD authenticated scan design
Design a pipeline that:
1. Deploys an isolated preview app.
2. Creates a temporary low-privilege test account.
3. Injects credentials from protected CI secrets.
4. Verifies authentication before crawling.
5. Runs a bounded passive scan.
6. Stores a restricted report.
7. Revokes the test identity and tears down the environment even on failure.

**Deliverable:** Pipeline YAML pseudocode and security review.

## Exercise 12 - Final assessment
Prepare a report with:
- Scope and authorization.
- Login and session flow.
- Context and authentication method.
- Session management and verification.
- Test users and roles (no secrets).
- URLs discovered per role.
- Authentication health evidence.
- Findings, coverage gaps, and exclusions.
- Remediation and retest status.

### Evaluation rubric (100 points)
| Area | Points |
|---|---:|
| Login/session flow analysis | 10 |
| Context and scope configuration | 10 |
| Authentication method configuration | 15 |
| Session management configuration | 15 |
| Verification and expiry testing | 15 |
| Authenticated crawling and coverage | 15 |
| Secret hygiene and CI design | 10 |
| Reporting and evidence | 10 |
