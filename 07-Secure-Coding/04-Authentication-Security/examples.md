# Authentication Security — Examples

Examples are illustrative. Use maintained libraries and your framework's official security guidance in production.

## 1. Avoid account enumeration

**Risky response design**
- Existing account: `Email exists; password incorrect`
- Unknown account: `No account found`

These messages disclose account status.

**Safer response design**
- Return a generic message such as: `Sign-in failed. Check your details and try again.`
- Keep status codes and response structure consistent where practical.
- Avoid large timing differences that reveal account existence.

## 2. Password storage

**Never do this**
```python
# INSECURE: never store plaintext passwords
database.save(email=email, password=password)
```

**Use a dedicated password-hashing library**
```python
# Pseudocode: use your framework's maintained password hasher.
password_hash = password_hasher.hash(password)
database.save(email=email, password_hash=password_hash)

# At sign-in:
if password_hasher.verify(stored_hash, submitted_password):
    create_authenticated_session()
else:
    return_generic_sign_in_failure()
```

Use a password-hashing algorithm designed for passwords (for example Argon2id, scrypt, or bcrypt), with unique salts and parameters selected using current library recommendations. A fast general-purpose hash such as plain SHA-256 is not a password-storage scheme.

## 3. Generate a reset token safely

```python
import secrets

# Generate a high-entropy token; store a hash of it where practical.
raw_token = secrets.token_urlsafe(32)
token_digest = secure_digest(raw_token)

store_reset_token(
    account_id=account.id,
    token_digest=token_digest,
    expires_at=short_expiry(),
    used=False,
    purpose="password-reset",
)
send_reset_link_to_verified_address(account.email, raw_token)
```

`secure_digest`, persistence, expiry, and delivery are pseudocode placeholders; implement them with vetted application components. Do not log the raw token. On use, verify the digest, purpose, expiry, and unused state, then atomically mark it used and invalidate it after success.

## 4. Cookie configuration

Example configuration concept; exact syntax varies by framework:
```text
Set-Cookie: __Host-session=<opaque-id>; Path=/; Secure; HttpOnly; SameSite=Lax
```

The `__Host-` prefix has browser-enforced requirements: use `Secure`, set `Path=/`, and omit `Domain`. Choose `SameSite` according to the application's flow and threat model. Cookies do not replace CSRF protections for state-changing requests.

## 5. MFA enrollment and recovery
- Require an authenticated session and recent reauthentication before enrolling or removing an MFA factor.
- Confirm possession of the new factor before activation.
- Notify the account owner when factors or recovery methods change.
- Protect recovery codes as secrets; display them once and store only a verifier/hash if the design supports it.
- Avoid treating knowledge-based questions as strong authentication.

## 6. Safe login endpoint flow

```text
Receive request
  -> enforce request-size and input limits
  -> apply IP/account/device-aware abuse controls
  -> look up account without exposing its existence
  -> verify password using the password-hashing library
  -> require MFA when policy demands it
  -> rotate session identifier
  -> set secure cookie
  -> record sanitized security event
  -> return generic success/failure response
```

## 7. Authentication event logging

Good event fields: event type, timestamp, outcome, coarse source context, correlation ID, and internal account reference where justified.

Do not log: passwords, raw OTPs, recovery codes, reset tokens, session cookies, or bearer tokens.
