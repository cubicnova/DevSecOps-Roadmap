# 06 — Session Management

Session management maintains authenticated state across requests. A secure login is not enough if session identifiers can be stolen, fixed, guessed, replayed, or left valid after logout.

## Learning objectives
By completing this module, you should be able to:
- Explain session identifiers, cookies, server-side sessions, and token-based sessions.
- Review session creation, rotation, expiration, logout, and revocation.
- Configure cookie attributes and transport protections.
- Identify session fixation, hijacking, replay, CSRF, and insecure token-storage risks.
- Design safe behavior for password changes, privilege changes, and account recovery.
- Build a repeatable session-security test plan.

## Core concepts
- **Session identifier:** an opaque value that references session state or grants access to a session.
- **Session fixation:** an attacker causes a victim to use a session identifier known to the attacker.
- **Session hijacking:** an attacker obtains and reuses a valid session identifier or token.
- **Rotation:** issuing a new identifier after authentication or a security-relevant state change.
- **Revocation:** invalidating a session so it can no longer be used.
- **Idle timeout:** expiration after a period without activity.
- **Absolute timeout:** maximum lifetime regardless of activity.
- **CSRF:** causing a browser to send an authenticated request the user did not intend.

## Suggested learning sequence
1. Read this overview and `examples.md`.
2. Draw the session lifecycle from anonymous browsing to login, privilege change, logout, and expiry.
3. Complete the local labs in `practical.md`.
4. Compare findings with `solutions.md`.
5. Use `session-management-checklist.md` in code reviews.
6. Track outcomes in `session-test-matrix.csv`.

## Secure session design
- Use the framework's maintained session implementation unless there is a compelling, reviewed reason not to.
- Generate session identifiers with a cryptographically secure random source; use identifiers that are unpredictable and contain no user data or secrets in encoded form.
- Rotate identifiers after login and privilege changes, and after other security-sensitive transitions as appropriate.
- Invalidate server-side session state on logout. Do not rely only on deleting a browser cookie.
- Set cookies with `Secure`, `HttpOnly`, and an appropriate `SameSite` policy. Consider the `__Host-` prefix where compatible.
- Use HTTPS throughout and configure HSTS where appropriate.
- Set idle and absolute expiration based on the sensitivity of the application; enforce expiration server-side.
- Avoid storing session IDs or bearer tokens in URLs, logs, analytics, browser history, or error reports.
- Apply CSRF protections to state-changing requests when browser credentials are sent automatically.
- Validate authorization on every protected request; possession of a session does not imply permission to access every object or action.
- Decide how password changes, account recovery, suspected compromise, role changes, and MFA changes affect active sessions.
- For sensitive actions, require recent authentication or step-up verification.
- Monitor suspicious session behavior and provide users a way to review and revoke active sessions when feasible.
- Never log raw session IDs, cookies, access tokens, or refresh tokens.

## Common threats and controls

| Threat | Example control |
|---|---|
| Session fixation | Rotate session identifier after authentication |
| Session theft | HTTPS, secure cookies, XSS defenses, token redaction |
| Replay of revoked session | Server-side revocation and regression tests |
| Long-lived stolen session | Idle and absolute expiration; risk-based reauthentication |
| CSRF | Anti-CSRF tokens and/or suitable SameSite controls plus origin checks |
| Insecure cookie scope | Host-only cookies; narrow path and domain scope |
| Authorization confusion | Check permission and object ownership on every request |
| Token leakage in logs or URLs | Redaction and avoid URL-based credentials |

## Cookie attributes at a glance
- `Secure`: browser sends the cookie only over secure transport.
- `HttpOnly`: JavaScript cannot read the cookie through `document.cookie`.
- `SameSite`: controls cross-site cookie sending behavior; choose `Lax`, `Strict`, or `None` based on the app's flows. `None` requires `Secure` in modern browsers.
- `Path` and `Domain`: influence where the cookie is sent. Avoid broad `Domain` scope unless required.
- `__Host-` prefix: browsers require `Secure`, `Path=/`, and no `Domain` attribute for cookies using this prefix.

Cookie attributes are not a substitute for authorization checks, XSS prevention, or CSRF analysis.

## References
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- OWASP Cross-Site Request Forgery Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
- OWASP WSTG — Testing for Session Management: https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/
- MDN — Set-Cookie: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie
