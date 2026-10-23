# Authentication Security — Suggested Solutions

Use this answer key to compare your lab findings. Real applications may require additional controls based on architecture and risk.

## Lab 1 — Endpoint inventory
Include every identity lifecycle endpoint, not only login. For each endpoint document:
- Authentication requirement and authorization checks
- Rate limits and anti-automation controls
- Input validation and response behavior
- Token/session state transitions
- Notifications and audit events
- Failure handling and recovery options

Prioritize password reset, MFA recovery, factor changes, and session revocation because they can undermine otherwise strong login controls.

## Lab 2 — Password storage
Use a maintained password-hashing implementation such as Argon2id, scrypt, or bcrypt, with parameters appropriate to the deployment. Let the library manage salts. Never use plaintext, reversible encryption, or a single fast hash such as SHA-256. Limit access to password-hash records and plan rehashing when parameters change.

## Lab 3 — Login abuse controls
Use layered controls such as per-account and per-source throttling, progressive delays, bot/risk signals, MFA, and monitoring. Do not rely only on source IP, and avoid permanent account lockouts that attackers can trigger against victims. Keep error messages generic and make processing behavior reasonably consistent.

## Lab 4 — Password reset
Generate tokens using a cryptographically secure random generator. Bind each token to an account and reset purpose; store a verifier/digest where practical; expire it; and consume it atomically once. Return generic request responses, deliver links only through verified channels, redact tokens from logs, and prevent referrer leakage. After successful reset, invalidate the token and consider revoking existing sessions. Notify the user of the change.

## Lab 5 — Sessions
Rotate the session identifier after login and privilege changes to reduce fixation risk. Use HTTPS and secure cookie attributes (`Secure`, `HttpOnly`, appropriate `SameSite`). Invalidate server-side session state on logout and apply idle and absolute expiration based on risk. Decide how password changes, account recovery, and suspected compromise affect active sessions.

## Lab 6 — MFA
Require a valid authenticated context and recent reauthentication for factor changes. Verify a newly enrolled factor before activation. Use phishing-resistant factors when feasible. Expire one-time codes, prevent replay, rate-limit verification, protect recovery codes, and notify users of changes. Recovery should not be materially weaker than the primary authentication path.

## Sample finding
**Title:** Password reset token remains valid after use  
**Severity:** Risk-dependent; assess token exposure, account impact, and exploitability.  
**Impact:** A captured token could be replayed to reset the same account again if the token remains accepted.  
**Remediation:** Enforce single-use token consumption atomically; invalidate all related reset tokens after a successful reset; test concurrent requests and replay attempts.  
**Regression test:** Submit the same token twice. The first valid request succeeds; all later requests fail without changing credentials.

## Report quality
Separate observed facts from assumptions. Redact credentials and tokens from screenshots and logs. Include a clear reproduction path and a specific fix that developers can verify.
