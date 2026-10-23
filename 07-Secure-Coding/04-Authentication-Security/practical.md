# Authentication Security — Practical Labs

**Authorization boundary:** perform these exercises only against your own local application, an intentionally vulnerable training app, or a system for which you have explicit permission.

## Lab 1 — Build an authentication flow inventory
1. List login, logout, registration, password reset, email verification, MFA enrollment, MFA recovery, and session-revocation endpoints.
2. Record the accepted identity factors, state transitions, rate limits, and security events for each.
3. Identify endpoints that disclose account existence.
4. Document the expected result for valid, invalid, expired, and replayed credentials.

**Deliverable:** endpoint inventory plus a short list of highest-risk gaps.

## Lab 2 — Password storage review
1. Inspect the application's password creation and verification code.
2. Confirm that plaintext passwords are never persisted or logged.
3. Identify the password-hashing algorithm, library, configuration, and migration approach.
4. Verify that password hashes use per-password salts through the chosen library.
5. Document how parameters can be upgraded over time.

**Deliverable:** findings and a recommended remediation plan.

## Lab 3 — Login abuse controls
1. In a local test environment, make a small, controlled number of failed login attempts.
2. Verify rate limiting and response behavior without attempting a denial of service.
3. Compare responses for an existing test account and a nonexistent test account.
4. Check whether controls can be trivially bypassed by changing one request field.
5. Propose a layered strategy that does not permanently lock out a victim based on attacker-generated failures.

**Deliverable:** test table with observations and expected behavior.

## Lab 4 — Password reset lifecycle
1. Request a reset for a test account.
2. Confirm the response does not reveal whether an account exists.
3. Check token expiry, single-use behavior, account binding, and purpose binding.
4. Verify that a used or expired token is rejected.
5. Verify that the application does not expose the token in logs, analytics, referrers, or error reports.
6. Confirm that password reset triggers appropriate notifications and session handling.

**Deliverable:** reset-token lifecycle diagram and test results.

## Lab 5 — Session security
1. Record the session cookie before and after login.
2. Verify that the session identifier rotates after authentication and privilege changes.
3. Review `Secure`, `HttpOnly`, and `SameSite` cookie attributes.
4. Test logout and server-side invalidation.
5. Check session expiration and behavior after password change or account recovery.

**Deliverable:** session security review.

## Lab 6 — MFA workflow
1. Review MFA enrollment, verification, removal, and recovery.
2. Confirm recent reauthentication is required for sensitive factor changes.
3. Test expired and reused one-time codes in a test environment.
4. Confirm recovery codes are single-use and protected.
5. Verify that high-risk events trigger notifications and logs.

**Deliverable:** MFA threat model and remediation list.

## Lab 7 — Security test report
Choose three findings from the labs. For each, write:
- Title and severity with rationale
- Affected component
- Preconditions and reproducible steps
- Evidence with secrets redacted
- Impact and realistic abuse scenario
- Root cause
- Remediation and regression test

## Completion criteria
- No plaintext or reversible password storage.
- Generic authentication and recovery responses.
- Abuse controls for all sensitive authentication endpoints.
- Reset tokens are high entropy, expiring, single-use, and purpose-bound.
- Session rotation and secure cookie attributes are verified.
- MFA changes and recovery are protected.
- Logs contain useful security context without authentication secrets.
