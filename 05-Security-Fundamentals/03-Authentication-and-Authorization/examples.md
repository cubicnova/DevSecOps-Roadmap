# Authentication and Authorization — Examples

Examples are educational patterns. Adapt them to your framework, threat model, and current security guidance.

## 1. Authentication versus authorization
A user signs in successfully, so the application knows the user's identity. The user requests `/api/invoices/9002`. The server must still determine whether this user is allowed to access invoice `9002`. Authentication alone does not grant access to every invoice.

## 2. RBAC policy example

| Role | View own profile | View own orders | Manage all orders | Manage users |
|---|---:|---:|---:|---:|
| Customer | Yes | Yes | No | No |
| Support agent | Limited | Policy-based | Limited, audited | No |
| Order manager | Yes | As authorized | Yes | No |
| Administrator | Yes | Yes | Yes | Yes, audited |

Use least privilege. Support access to customer data should be limited to legitimate support needs and audited.

## 3. Server-side object authorization (pseudocode)

```python
def get_invoice(current_user, invoice_id):
    invoice = db.get_invoice(invoice_id)
    if invoice is None:
        return not_found()

    if invoice.owner_id != current_user.id:
        return forbidden_or_not_found()

    return success(invoice)
```

The important idea is the server-side ownership check. In multi-tenant systems, validate tenant membership and applicable policy too. Choose `403` versus `404` consistently with the application's information-disclosure policy.

## 4. Cookie configuration concept

```http
Set-Cookie: session=REDACTED; Secure; HttpOnly; SameSite=Lax; Path=/
```

This is a conceptual example. Choose cookie domain, path, lifetime, and `SameSite` behavior based on the application. Never expose actual session values in logs, screenshots, or examples.

## 5. Authorization test cases

| Test | Expected result |
|---|---|
| Anonymous user requests protected profile | Redirect to login or return documented `401` response |
| User A requests User B's private record | Denied without disclosing protected data |
| Customer calls admin endpoint | Denied |
| User with expired session makes a protected request | Reauthentication required |
| User removed from a project accesses project data | Access denied after policy changes take effect |
| Authorized administrator changes a role | Allowed only under policy and logged |

## 6. Token validation checklist
For a signed token such as a JWT, validate the signature using a trusted algorithm/key configuration, issuer, audience, expiry and not-before claims where relevant, and token purpose. Reject malformed, expired, wrongly scoped, or otherwise invalid tokens. Apply authorization checks after token validation.

Never trust a token merely because it can be decoded.
