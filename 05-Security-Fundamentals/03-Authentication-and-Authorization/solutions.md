# Solutions — Authentication and Authorization

Sample answers for the exercises and lab. The correct implementation depends on application architecture and policy.

## Exercise 1 — Authentication versus authorization
Authentication verifies the identity or credential presented by a caller. Authorization decides whether that identity may perform a particular action on a particular resource. A customer may authenticate successfully but still be denied access to another customer's order.

## Exercise 2 — Example RBAC policy
- **Customer:** View and update permitted profile fields; view own orders.
- **Support agent:** Access only records required for assigned support tasks; sensitive actions are limited and audited.
- **Order manager:** Manage orders within the assigned business scope.
- **Administrator:** Manage users and system configuration with strong authentication, least privilege, and audit logging.

Roles should be reviewed regularly. Avoid broad, permanent admin access for routine work.

## Exercise 3 — Defenses against IDOR/BOLA
- Enforce server-side object ownership or relationship checks for every operation.
- Validate tenant boundaries and authorization policy.
- Do not rely on unguessable IDs as the only protection.
- Test read, update, delete, export, and nested-object endpoints.
- Add regression tests using separate test identities.
- Log relevant denied access attempts without exposing sensitive data.

## Exercise 4 — Secure cookie attributes
- `Secure`: Send the cookie only over HTTPS.
- `HttpOnly`: Prevent ordinary client-side scripts from reading the cookie.
- `SameSite`: Reduce some cross-site request risks; choose a value compatible with the application's flows.
- `Path` and `Domain`: Limit where the browser sends the cookie.
- Expiration: Bound session lifetime as required by risk and policy.

Cookie attributes complement, but do not replace, secure session management and CSRF defenses.

## Exercise 5 — JWT decoding versus validation
Decoding parses the token's contents; it does not prove the token was issued by a trusted party or remains valid. Verify the signature and expected algorithm, issuer, audience, expiry, and intended token use. Then enforce authorization separately.

## Exercise 6 — Sample test plan

| Case | Expected result |
|---|---|
| Anonymous request to private endpoint | Authentication required |
| User A reads User B's record | Denied |
| Customer invokes admin function | Denied |
| Expired session used | Rejected |
| Revoked project membership used | Denied |
| Valid authorized request | Allowed and audited where required |

## Common mistakes to avoid
- Checking permissions only in the frontend.
- Assuming authentication grants broad access.
- Trusting user-supplied role or owner IDs.
- Storing plaintext passwords.
- Logging passwords, session cookies, access tokens, or reset tokens.
- Using JWTs without proper validation.
- Leaving recovery and support workflows less protected than normal login.

## Evaluation rubric
- 2 points: explains identity verification versus permission checks.
- 2 points: creates a least-privilege role matrix.
- 2 points: tests object-level and function-level authorization.
- 2 points: covers sessions, cookies, and recovery.
- 2 points: records evidence and actionable remediation.

Total: 10 points.
