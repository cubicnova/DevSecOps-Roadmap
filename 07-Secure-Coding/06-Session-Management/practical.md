# Session Management — Practical Labs

Only test your own application, a local lab, or systems for which you have explicit permission.

## Lab 1 — Map the lifecycle
Document these states: anonymous, authenticated, elevated/step-up authenticated, expired, logged out, and revoked. For each transition, note which component changes the session state and what the client receives.

**Deliverable:** a session lifecycle diagram and list of transition tests.

## Lab 2 — Review cookie configuration
1. Sign in to a test account and inspect response headers in browser developer tools.
2. Record cookie name, `Secure`, `HttpOnly`, `SameSite`, `Path`, and `Domain`.
3. Confirm the authenticated cookie is not set over plain HTTP.
4. Check that no session ID appears in the URL.
5. Compare actual behavior with the app's documented cookie policy.

**Deliverable:** cookie configuration review.

## Lab 3 — Test session rotation
1. In a local test environment, record the anonymous session identifier.
2. Authenticate using a test account.
3. Check whether the identifier changes.
4. Verify the pre-authentication identifier cannot be used to access the authenticated session.
5. Repeat after a role or privilege change if applicable.

**Deliverable:** before/after observations and regression tests.

## Lab 4 — Test logout and revocation
1. Sign in and capture the session cookie locally.
2. Log out normally.
3. Replay the old cookie only against your local test application.
4. Confirm the server rejects the revoked session.
5. Repeat after password reset or an administrator-triggered revocation if supported.

**Deliverable:** evidence that server-side invalidation works. Redact session values from all evidence.

## Lab 5 — Validate expiration
1. Use a test configuration with short idle and absolute timeouts.
2. Confirm inactivity causes server-side expiration.
3. Confirm activity does not extend the absolute lifetime beyond policy.
4. Verify expired sessions redirect or return a controlled unauthorized response.
5. Check that stale browser cookies do not restore an expired session.

**Deliverable:** timeout test table.

## Lab 6 — Review CSRF controls
1. Identify state-changing endpoints that rely on browser cookies.
2. Verify the framework's CSRF protection is enabled.
3. In a controlled test, submit a state-changing request without a valid anti-CSRF token.
4. Verify the request is rejected.
5. Confirm read-only requests do not accidentally change application state.

**Deliverable:** endpoint-by-endpoint CSRF review.

## Lab 7 — Check session leakage and logging
1. Search local test logs, analytics events, and error reports for session identifiers or bearer tokens.
2. Check links and redirects for session values in query strings.
3. Review referrer policy and third-party resources on sensitive pages.
4. Confirm audit logs record session creation, revocation, and suspicious activity without raw secrets.

**Deliverable:** leakage review and redaction recommendations.

## Lab 8 — Write a finding
For one confirmed issue, document title, severity rationale, affected endpoint, preconditions, reproducible steps, redacted evidence, impact, root cause, remediation, and regression test.

## Completion criteria
- Session ID rotates after login and privilege changes.
- Logout and revocation invalidate server-side state.
- Cookie attributes and HTTPS are appropriate.
- Idle and absolute timeouts are enforced server-side.
- CSRF controls are tested for cookie-authenticated state changes.
- Session identifiers and tokens do not appear in URLs or logs.
- Authorization is checked independently on every protected request.
