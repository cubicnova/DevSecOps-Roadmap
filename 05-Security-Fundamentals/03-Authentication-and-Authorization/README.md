# 03 — Authentication and Authorization

Authentication verifies **who or what** is making a request. Authorization determines **what that identity is allowed to do**. Both are essential to securing applications, APIs, infrastructure, and data.

## Learning objectives
- Explain identification, authentication, authorization, and auditing.
- Compare passwords, MFA, passkeys, sessions, API keys, and tokens.
- Apply least privilege and deny-by-default authorization.
- Understand RBAC, ABAC, and relationship-based access control.
- Recognize IDOR/BOLA and broken function-level authorization.
- Design and test secure login, session, and access-control flows.

## Core concepts

| Concept | Purpose | Example |
|---|---|---|
| Identification | Claims an identity | Entering a username |
| Authentication | Verifies the identity or credential | Password plus MFA |
| Authorization | Determines allowed actions and resources | User can view only their own invoices |
| Auditing | Records relevant activity | Log an administrator changing permissions |
| Session management | Maintains authenticated state | Secure session cookie |
| Least privilege | Grants only necessary access | Read-only access for a reporting service |

**Authentication is not authorization.** A successfully authenticated user may still be forbidden from reading a particular record or invoking an administrative action. See the [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).

## Authentication factors
- **Something you know:** password or PIN.
- **Something you have:** security key, authenticator device, or registered device.
- **Something you are:** a biometric characteristic.

Two different factors are stronger than two instances of the same factor. MFA reduces risk but does not make phishing, account recovery, or session theft impossible.

## Common authentication mechanisms

### Passwords
- Store passwords using a dedicated password-hashing algorithm such as Argon2id, scrypt, or appropriately configured bcrypt.
- Use unique salts and current, defensible work factors.
- Never store plaintext passwords or reversible password encryption for ordinary login systems.
- Apply rate limiting and monitor suspicious login activity.
- Support password managers and long passphrases.

### Multi-factor authentication
Offer phishing-resistant options such as FIDO2/WebAuthn passkeys or security keys where feasible. Protect enrollment, recovery, device replacement, and factor removal as carefully as login itself.

### Sessions and cookies
For browser applications:
- Use HTTPS throughout authenticated flows.
- Set cookies with `Secure`, `HttpOnly`, and an appropriate `SameSite` policy.
- Rotate the session identifier after login and privilege changes.
- Expire sessions according to risk and business needs.
- Invalidate sessions on logout and relevant account-security events.
- Protect state-changing requests against CSRF when the architecture requires it.

### API keys and bearer tokens
- Treat API keys and bearer tokens as secrets.
- Scope them narrowly, rotate and revoke them, and avoid putting them in URLs.
- Validate token issuer, audience, expiry, signature, and intended use where applicable.
- Do not assume a decoded JWT is trustworthy; validate it cryptographically and enforce authorization separately.
- Use OAuth 2.0 / OpenID Connect correctly when delegated authorization or federated login is needed; do not invent a custom protocol.

## Authorization models

| Model | How it works | Example |
|---|---|---|
| RBAC | Permissions assigned to roles | `billing-admin` can manage invoices |
| ABAC | Decisions use subject, resource, action, and environment attributes | Allow download only for an assigned case |
| ReBAC | Decisions use relationships between identities and objects | Project member can edit that project |
| ACL | Permissions are listed on an object | Specific users can read a file |

A robust implementation checks authorization on the server for every sensitive operation. Hiding a button in the UI is not an access-control boundary.

## Secure authorization checklist
1. Deny by default.
2. Check authorization on every request and every relevant object.
3. Validate both function-level permission and object-level access.
4. Enforce tenant and ownership boundaries on the server.
5. Avoid relying on user-controlled IDs, role names, or client-side flags.
6. Use least privilege and separate administrative duties.
7. Re-check permissions after role, ownership, or membership changes.
8. Log sensitive authorization failures and permission changes without exposing secrets.
9. Test direct API requests, not just UI behavior.
10. Review recovery, support, background jobs, and alternate API routes for equivalent controls.

## Common vulnerabilities
- **Broken authentication:** weak or flawed identity verification and recovery.
- **Broken access control:** requests perform actions the caller should not be allowed to do.
- **IDOR / BOLA:** changing an object identifier exposes another user's object because ownership or policy is not checked.
- **Broken function-level authorization:** a regular user can invoke an administrative endpoint.
- **Session fixation or theft:** an attacker reuses or controls an authenticated session identifier.
- **Credential stuffing:** reused leaked credentials are tried against another service.
- **JWT validation errors:** the application accepts tokens without proper signature, issuer, audience, or expiry validation.
- **Privilege escalation:** a user gains permissions beyond their intended role.

## Safe testing examples
For an application you own or are explicitly authorized to test:
- Sign in as two separate test users and confirm each can access only their own records.
- Attempt a direct request to a protected endpoint using a low-privilege test account.
- Verify that changing a record ID does not reveal another tenant's data.
- Confirm that unauthenticated requests receive the intended response.
- Test expired sessions, logout, password reset, MFA recovery, and role changes.
- Verify server-side checks remain in place even when UI controls are altered.

Do not test accounts, data, or systems without authorization.

## Exercises
1. Explain authentication versus authorization with an example.
2. Design an RBAC policy for a small e-commerce application.
3. Describe defenses against IDOR/BOLA.
4. List secure cookie settings and explain their purpose.
5. Explain why JWT decoding alone is not validation.
6. Write test cases for tenant isolation and administrative functions.

## References
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-4/)
