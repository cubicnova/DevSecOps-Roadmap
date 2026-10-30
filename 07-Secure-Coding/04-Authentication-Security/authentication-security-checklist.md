# Authentication Security Review Checklist

Use `- [ ]` to track each item during design review, code review, or testing.

## Passwords
- [ ] Passwords are hashed with a maintained password-hashing algorithm and library.
- [ ] Passwords are never stored in plaintext or reversibly encrypted.
- [ ] Hash parameters can be upgraded and legacy hashes migrated safely.
- [ ] Password policy supports long passphrases and avoids arbitrary composition rules.
- [ ] Common or known-compromised passwords are blocked where practical.
- [ ] Passwords and hashes are excluded from application logs and analytics.

## Login and account enumeration
- [ ] Login failures use generic messages.
- [ ] Registration and recovery responses do not reveal account existence.
- [ ] Login and verification endpoints have layered abuse controls.
- [ ] Rate limits account for source and account context without creating easy denial of service.
- [ ] MFA is required for privileged and other high-risk accounts according to policy.
- [ ] Automated tests cover valid, invalid, throttled, and edge-case flows.

## Password reset and recovery
- [ ] Reset tokens use cryptographically secure randomness.
- [ ] Tokens are time-limited, single-use, account-bound, and purpose-bound.
- [ ] Tokens are stored safely and never logged.
- [ ] Reset responses are generic and delivery uses a verified channel.
- [ ] Expired, used, malformed, and wrong-purpose tokens are rejected.
- [ ] Successful reset triggers appropriate notification and session revocation policy.

## MFA
- [ ] Enrollment, removal, and recovery require appropriate authentication and recent reauthentication.
- [ ] New factors are verified before activation.
- [ ] One-time codes expire and cannot be replayed.
- [ ] Verification endpoints are rate-limited.
- [ ] Recovery codes are single-use and protected.
- [ ] Users are notified about factor and recovery changes.
- [ ] Phishing-resistant authentication is considered for high-risk use cases.

## Sessions and cookies
- [ ] Session identifiers rotate after login and privilege changes.
- [ ] Cookies use `Secure`, `HttpOnly`, and appropriate `SameSite` attributes.
- [ ] HTTPS is enforced throughout the session.
- [ ] Logout invalidates the session server-side.
- [ ] Idle and absolute session lifetimes fit the risk.
- [ ] Password changes and account recovery have a documented session-revocation policy.
- [ ] CSRF protections are applied where cookie-based authentication requires them.

## Monitoring and operations
- [ ] Authentication events are logged with useful, sanitized context.
- [ ] Passwords, OTPs, reset tokens, session IDs, and bearer tokens are never logged.
- [ ] Alerts cover unusual failure rates, recovery abuse, and sensitive factor changes.
- [ ] Clock, token-expiry, and concurrent-use behavior are tested.
- [ ] Authentication dependencies are maintained and security updates are applied.
- [ ] Security tests run in CI and include regression cases for known findings.
