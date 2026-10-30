# API Security — Examples

The snippets are illustrative. Use your framework's maintained libraries and validate all controls server-side.

## 1. Object-level authorization (BOLA)

**Risky pattern**
```python
# INSECURE: trusting a client-supplied object ID alone
record = database.get_record(request.path_params["record_id"])
return record
```

**Safer pattern**
```python
record_id = request.path_params["record_id"]
record = database.get_record(record_id)

if record is None or not policy.can_read(current_user, record):
    return generic_not_found()

return serialize_record_for(current_user, record)
```

The policy check must be enforced server-side. Returning a generic not-found response can reduce object enumeration, but does not replace authorization.

## 2. Property-level authorization and mass assignment

**Risky pattern**
```python
# INSECURE: blindly applying every client-supplied field
user.update(request.json)
```

**Safer pattern**
```python
payload = validate_schema(request.json, allowed_fields={"display_name", "timezone"})
user.display_name = payload["display_name"]
user.timezone = payload["timezone"]
save(user)
```

Do not allow clients to set privileged properties such as `role`, `tenant_id`, `is_admin`, account balance, or approval status unless a specific authorized workflow permits it.

## 3. Validate tokens correctly

For JWTs or other signed tokens, use a maintained library and explicitly validate:
- Signature using the expected algorithm and trusted key source
- Issuer (`iss`) and audience (`aud`)
- Expiration (`exp`) and not-before (`nbf`) where present
- Required scopes/claims and the caller's authorization
- Key rotation and token revocation strategy where applicable

Do not merely decode a JWT and trust its contents. Never accept an algorithm or key source chosen without policy by the untrusted token.

## 4. Request and response schemas

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["display_name"],
  "properties": {
    "display_name": {"type": "string", "minLength": 1, "maxLength": 80},
    "timezone": {"type": "string", "maxLength": 64}
  }
}
```

This illustrative JSON Schema rejects undeclared fields and sets bounds. Add application-specific format and business validation, and keep response schemas separate from request schemas.

## 5. Rate limiting and resource bounds

Example policy (adapt to workload and risk):
```text
POST /auth/login       -> per-account and source-aware throttling
POST /reports/export   -> per-user quota, concurrency cap, job timeout
GET  /items            -> maximum page size, bounded filters
POST /uploads          -> body-size cap, type validation, malware scanning where appropriate
```

Use consistent error semantics, such as `429 Too Many Requests` with an appropriate retry policy. Avoid relying on a single IP-only limit for authenticated multi-tenant APIs.

## 6. Safe errors

**Avoid:** stack traces, SQL errors, internal hostnames, secret values, and raw request dumps.

**Prefer:** a stable error code, a safe message, and a correlation ID. Keep detailed diagnostics in access-controlled logs with sensitive fields redacted.

## 7. CORS is not access control

CORS controls which browser origins may read certain cross-origin responses. Non-browser clients can call an API regardless of browser CORS policy. Every request still needs authentication and authorization.

## 8. SSRF-aware URL fetching
If an API fetches a URL provided by a caller, prefer strict allowlists of trusted destinations. Validate the scheme and hostname, resolve and validate addresses, defend against redirects and DNS rebinding, block loopback/private/link-local and metadata destinations as appropriate, and enforce network egress controls. Do not rely on a single string check.
