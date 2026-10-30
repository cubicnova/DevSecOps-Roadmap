# 04 — Authentication Security

Learn how to design, implement, test, and review secure authentication flows in web applications and APIs.

## Learning objectives
By completing this module, you should be able to:
- Distinguish authentication, authorization, and session management.
- Apply secure password storage and account-recovery practices.
- Design MFA, login throttling, and safe error messages.
- Protect sessions, cookies, tokens, and authentication endpoints.
- Test common authentication weaknesses using a controlled lab.
- Document findings with evidence, impact, and remediation guidance.

## Core concepts
- **Authentication:** verifies an identity.
- **Authorization:** determines what an authenticated identity may do.
- **Session management:** maintains authenticated state across requests.
- **MFA:** combines independent factors, such as a password and a security key.
- **Reauthentication:** asks a user to prove their identity again for sensitive actions.

## Recommended learning sequence
1. Read the authentication principles below.
2. Review the examples and identify the security property each one protects.
3. Complete the practical exercises only in a local lab or systems you are authorized to test.
4. Compare your results with `solutions.md`.
5. Use `authentication-security-checklist.md` during code review.
6. Record test outcomes using `authentication-test-matrix.csv`.

## Secure design principles
- Prefer established framework authentication libraries over custom cryptography or home-grown protocols.
- Store passwords with a dedicated password-hashing algorithm such as Argon2id, scrypt, or bcrypt, using current library guidance and appropriate parameters. Do not store plaintext or reversibly encrypted passwords.
- Use MFA for privileged and high-risk accounts; prefer phishing-resistant methods such as WebAuthn/passkeys or security keys where feasible.
- Apply rate limits and progressive abuse controls to login, recovery, OTP verification, and MFA enrollment endpoints.
- Avoid revealing whether an account exists through login, registration, and recovery responses.
- Use cryptographically secure randomness for reset tokens and session identifiers.
- Make reset tokens single-use, time-limited, and bound to the intended account and purpose.
- Use HTTPS throughout. Protect session cookies with `Secure`, `HttpOnly`, and an appropriate `SameSite` value.
- Rotate the session identifier after login and privilege changes; invalidate sessions on logout and account recovery where appropriate.
- Require reauthentication or step-up verification for sensitive actions such as changing MFA, changing a recovery email, or adding a payment method.
- Log security-relevant events without recording passwords, raw reset tokens, OTPs, session IDs, or access tokens.
- Monitor authentication failures and unusual activity while avoiding account-lockout designs that let attackers deny service to victims.

## Threats to assess
| Threat | Example control |
|---|---|
| Password guessing / credential stuffing | Rate limiting, breached-password checks, MFA, anomaly detection |
| Password database exposure | Slow password hashing, unique salts, restricted access |
| Account enumeration | Consistent responses and comparable processing behavior |
| Reset-token theft or replay | High-entropy, expiring, single-use tokens; secure delivery |
| Session fixation or theft | Session rotation, HTTPS, secure cookie attributes |
| MFA bypass or fatigue | Phishing-resistant MFA, transaction context, abuse limits |
| Weak recovery process | Strong identity proofing, notifications, limited recovery paths |
| Secret leakage in logs | Structured redaction and log review |

## Suggested folder contents
- `README.md` — concepts and learning path
- `examples.md` — secure and insecure design examples
- `practical.md` — hands-on exercises
- `solutions.md` — answer key and remediation notes
- `authentication-security-checklist.md` — review checklist
- `authentication-test-matrix.csv` — reusable test cases

## References
- OWASP Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- OWASP Forgot Password Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- NIST SP 800-63B, Digital Identity Guidelines: https://pages.nist.gov/800-63-4/sp800-63b.html
