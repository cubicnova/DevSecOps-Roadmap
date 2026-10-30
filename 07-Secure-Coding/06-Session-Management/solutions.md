# Session Management — Suggested Solutions

Use these notes to compare your lab observations. Adapt controls to the application architecture and threat model.

## Lab 1 — Lifecycle
A useful diagram includes anonymous session creation, authentication, session rotation, optional MFA/step-up, normal use, privilege change, idle/absolute expiry, logout, and administrative revocation. Each state-changing transition should have explicit expected behavior and tests.

## Lab 2 — Cookies
For session cookies, use HTTPS and typically `Secure`, `HttpOnly`, and an appropriate `SameSite` value. Prefer host-only scope and avoid unnecessarily broad `Domain` values. The `__Host-` prefix can help enforce host-only cookie requirements where compatible. Confirm framework defaults rather than assuming them.

## Lab 3 — Rotation
A new session identifier should be issued after authentication and relevant privilege changes. The pre-authentication identifier must not grant access to the authenticated session. Use the framework's session rotation API and test old-ID rejection.

## Lab 4 — Logout and revocation
Logout should invalidate the server-side session or mark it revoked, and clear the browser cookie. A replayed old cookie must fail. For distributed applications, ensure revocation reaches all relevant session stores and services. Redact all session values in evidence.

## Lab 5 — Expiration
Enforce idle and absolute timeouts on the server, not only in browser code. The absolute timeout should not be reset merely because the user is active. Choose values based on risk and document exceptions for long-running workflows.

## Lab 6 — CSRF
Use framework-provided CSRF defenses for cookie-authenticated state-changing requests. Validate tokens server-side and consider origin checks as an additional control. Do not use `GET` for state-changing operations. `SameSite` is defense-in-depth and must be evaluated against actual flows.

## Lab 7 — Leakage
Redact session IDs and tokens from application, proxy, and telemetry logs. Avoid putting them in URLs. Restrict access to logs and define retention policies. Where third-party resources are used on sensitive pages, assess referrer leakage and apply an appropriate `Referrer-Policy`.

## Sample finding
**Title:** Authenticated session remains usable after logout  
**Severity:** Risk-dependent; consider session lifetime, application sensitivity, and exploitability.  
**Impact:** A copied session cookie can continue to access the account after the user believes they have logged out.  
**Root cause:** The application deletes the client cookie but does not invalidate server-side session state.  
**Remediation:** Revoke the server-side session on logout, clear the cookie, and ensure every protected request checks session validity.  
**Regression test:** After logout, replay the former cookie in a local test environment. The server must reject it.

## Review quality
Distinguish confirmed observations from assumptions, redact secrets, avoid testing other users' sessions, and include a concrete fix plus a regression test.
