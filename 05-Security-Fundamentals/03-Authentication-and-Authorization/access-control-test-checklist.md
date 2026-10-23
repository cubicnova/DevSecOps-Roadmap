# Authentication and Authorization Test Checklist

Use this checklist for an application you own or are explicitly authorized to assess.

## Authentication
- [ ] Passwords are stored using a dedicated password-hashing algorithm with suitable parameters.
- [ ] Login endpoints have proportionate rate limiting and abuse monitoring.
- [ ] MFA is available or required according to risk.
- [ ] Recovery and factor reset flows verify identity appropriately.
- [ ] Authentication errors do not unnecessarily reveal account existence.
- [ ] Password reset tokens expire and cannot be reused.

## Sessions and tokens
- [ ] Session IDs rotate after login and privilege changes.
- [ ] Logout invalidates the session.
- [ ] Cookie attributes are appropriate (`Secure`, `HttpOnly`, `SameSite`).
- [ ] Session expiry and revocation behavior are documented.
- [ ] Tokens are not exposed in URLs, logs, or client-side repositories unnecessarily.
- [ ] JWT signature, issuer, audience, expiry, and intended use are validated.

## Authorization
- [ ] Server-side authorization runs for every sensitive request.
- [ ] Object-level access is checked for read, create, update, delete, and export operations.
- [ ] Function-level permissions prevent low-privilege users from invoking admin features.
- [ ] Tenant and ownership boundaries are tested.
- [ ] Default behavior is deny unless explicitly permitted.
- [ ] Permissions are re-evaluated after role or membership changes.
- [ ] Background jobs and alternate API routes enforce equivalent rules.

## Audit and validation
- [ ] Sensitive permission changes are logged.
- [ ] Logs exclude passwords, session cookies, bearer tokens, and recovery secrets.
- [ ] Tests use authorized test accounts and synthetic data.
- [ ] Negative test cases have documented expected outcomes.
- [ ] Findings include evidence, impact, remediation, and retest criteria.
