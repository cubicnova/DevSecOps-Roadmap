# Authorization and Access Control — Examples

These examples are educational patterns. Adapt them to your framework and policy requirements, and test both allowed and denied cases.

## 1. RBAC: require a permission

A role name is useful for grouping permissions, but the application should make a server-side decision for each protected operation.

```python
def has_permission(user, required_permission):
    if user is None or not user.is_active:
        return False

    return required_permission in user.permissions


def publish_article(user, article):
    if not has_permission(user, "article:publish"):
        raise PermissionError("Forbidden")

    article.status = "published"
```

Avoid trusting a role or permission supplied by the browser. Load authorization attributes from trusted server-side state.

## 2. Object-level authorization: avoid IDOR/BOLA

**Unsafe pattern:**

```python
# The ID comes from the request, but no ownership check is made.
invoice = db.invoices.get(request.path_params["invoice_id"])
return serialize(invoice)
```

**Safer pattern: scope the lookup to the caller:**

```python
def get_invoice_for_user(db, user, invoice_id):
    if user is None:
        raise PermissionError("Authentication required")

    # The query itself limits results to invoices the user may access.
    invoice = db.invoices.find_one(
        id=invoice_id,
        owner_id=user.id,
    )

    if invoice is None:
        # Many applications return 404 here to avoid disclosing existence.
        raise LookupError("Invoice not found")

    return invoice
```

If shared access is supported, include the explicit membership/relationship policy in the query or a subsequent authorization decision. A random UUID does not replace authorization.

## 3. Tenant isolation

```python
def get_project(db, user, project_id):
    if user is None:
        raise PermissionError("Forbidden")

    project = db.projects.find_one(
        id=project_id,
        tenant_id=user.tenant_id,
    )
    if project is None:
        raise LookupError("Project not found")

    return project
```

For multi-tenant applications, derive the tenant from trusted identity or membership context. Do not let an arbitrary request parameter choose the security boundary without validation.

## 4. ABAC: policy uses attributes

```python
def can_view_case(user, case, now):
    if not user or not case:
        return False

    return (
        user.is_active
        and user.department == case.department
        and user.clearance_level >= case.required_clearance
        and now < case.retention_deadline
    )
```

Real ABAC policies may include the requested action, device posture, network, time, resource classification, and other approved attributes. Keep policy rules understandable and testable.

## 5. Field-level authorization and mass assignment

**Risky:** copying every client field into a privileged model.

```python
# Do not do this with untrusted request data.
for key, value in request.json.items():
    setattr(user_record, key, value)
```

**Safer:** explicitly select fields that this endpoint permits.

```python
ALLOWED_PROFILE_FIELDS = {"display_name", "timezone"}

def update_profile(user_record, payload):
    for field in ALLOWED_PROFILE_FIELDS:
        if field in payload:
            setattr(user_record, field, payload[field])
```

Use a separate privileged workflow for sensitive changes such as role, tenant, account status, or billing permissions. Validate values and apply authorization to that workflow too.

## 6. Deny by default

```python
POLICIES = {
    ("reader", "document:read"): True,
    ("editor", "document:read"): True,
    ("editor", "document:update"): True,
    ("admin", "document:read"): True,
    ("admin", "document:update"): True,
    ("admin", "user:manage"): True,
}

def is_allowed(role, action):
    return POLICIES.get((role, action), False)
```

The default is `False`. In production, avoid a simplistic global role table if authorization depends on object ownership, tenant, relationships, or other attributes.

## 7. Unit tests for authorization

```python
def test_owner_can_read_invoice():
    owner = User(id=10, permissions=set(), is_active=True)
    invoice = Invoice(id=50, owner_id=10)
    assert can_read_invoice(owner, invoice) is True


def test_other_user_cannot_read_invoice():
    stranger = User(id=11, permissions=set(), is_active=True)
    invoice = Invoice(id=50, owner_id=10)
    assert can_read_invoice(stranger, invoice) is False


def test_missing_user_is_denied():
    invoice = Invoice(id=50, owner_id=10)
    assert can_read_invoice(None, invoice) is False
```

These snippets assume simple illustrative classes and a policy function defined in the application. Add tests for inactive users, administrators, shared resources, cross-tenant access, update/delete operations, and policy-service failures.

## 8. HTTP behavior

Common response choices include:

- `401 Unauthorized`: authentication is missing or invalid.
- `403 Forbidden`: the caller is authenticated but lacks permission.
- `404 Not Found`: sometimes used to avoid revealing whether a protected object exists.

Choose a consistent policy. Do not include private object contents or stack traces in error responses.

## Review questions

- Is the policy enforced on the server for every request?
- Is the object lookup scoped to the user's allowed resources?
- Can client input change role, owner, tenant, or privilege fields?
- Does the system deny access if authorization data is unavailable?
- Are denied access attempts observable without leaking secrets?
