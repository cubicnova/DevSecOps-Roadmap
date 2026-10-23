# Authorization and Access Control — Suggested Solutions

These are reference answers. Real policies depend on the application's business rules; document assumptions and test them explicitly.

## Solution 1: Authentication vs. authorization

1. The API authenticates the session or establishes the caller's identity.
2. It has not established whether that caller may read the particular order.
3. Check ownership, an explicit sharing relationship, tenant membership, or a narrowly defined privileged permission for the requested order. Perform the check on every request.

## Solution 2: Example permission matrix

One possible policy, assuming viewers can read documents they have been granted access to, editors can edit but not delete/share, owners control their own documents, and administrators manage platform users:

| Role | View | Edit | Delete | Share | Manage users |
|---|---:|---:|---:|---:|---:|
| Viewer | Yes, permitted docs | No | No | No | No |
| Editor | Yes, permitted docs | Yes, permitted docs | No | No | No |
| Owner | Yes, owned/shared docs | Yes, owned docs | Yes, owned docs | Yes, owned docs | No |
| Administrator | Per approved admin policy | Per approved admin policy | Per approved admin policy | Per approved admin policy | Yes |

This matrix is only a starting point. Define whether administrators can access all content, whether sensitive documents need extra restrictions, and how tenant boundaries apply. Unlisted actions should be denied.

## Solution 3: IDOR

The original code does not verify the caller's identity, permission to the specific report, tenant membership, or safe handling of missing reports.

Example design:

```python
def download_report(request, report_id):
    user = require_authenticated_user(request)
    report = reports.find_accessible_by_user(
        report_id=report_id,
        user_id=user.id,
        tenant_id=user.tenant_id,
    )
    if report is None:
        raise NotFound()
    authorize(user, "report:download", report)
    audit_denial_or_success_as_appropriate(user, report)
    return send_file(report.path)
```

The repository method and `authorize` function are illustrative. Ensure the path cannot be manipulated to read arbitrary files. UUIDs can make enumeration harder, but they do not prove permission; the server still needs object-level authorization.

## Solution 4: Tenant isolation

Derive the authenticated user's tenant or memberships from validated server-side identity data. Query only projects in a tenant the user is allowed to access, and check project membership or another explicit policy.

```python
def get_project_for_caller(user, project_id, db):
    if user is None:
        raise PermissionError("Authentication required")

    project = db.projects.find_one(
        id=project_id,
        tenant_id=user.tenant_id,
    )
    if project is None:
        raise LookupError("Project not found")

    if not user_can_access_project(user, project):
        raise PermissionError("Forbidden")

    return project
```

Do not trust a request's `tenant_id` merely because it is syntactically valid. If users can switch among multiple tenants, validate the selected tenant against the user's current memberships before using it.

## Solution 5: Field-level authorization

The endpoint risks mass assignment and privilege escalation. The display-name endpoint should accept only `display_name`; ignore or reject unexpected privileged fields according to the API's documented validation policy.

```python
def update_display_name(user_record, payload):
    if "display_name" not in payload:
        raise ValueError("display_name is required")
    if set(payload) - {"display_name"}:
        raise ValueError("Unsupported field")
    user_record.display_name = validate_display_name(payload["display_name"])
```

Role, tenant membership, and account activation changes should use separate, tightly authorized administrative workflows with audit logging and tests.

## Solution 6: ABAC policy

```python
def can_access_case(user, case, now):
    return bool(
        user
        and case
        and user.is_active
        and user.department == case.department
        and user.clearance_level >= case.classification
        and now <= case.access_deadline
    )
```

Example tests:

1. Active user, same department, sufficient clearance, before deadline → allow.
2. Inactive user → deny.
3. Different department → deny.
4. Insufficient clearance → deny.
5. Deadline passed → deny.
6. Missing user → deny.
7. Missing case → deny.
8. Boundary time at the deadline → verify the intended `<=` or `<` rule.

Use a controlled clock in tests instead of depending on the actual current time.

## Solution 7: Fail closed

An authorization timeout means the application cannot establish that access is allowed. It should deny the protected operation or return a controlled temporary error without disclosing protected data. Log a policy-evaluation failure with a correlation ID and enough metadata for investigation, but do not log credentials, tokens, or sensitive payloads. Alert on repeated failures if appropriate.

## Solution 8: Test matrix

A reasonable starting point:

| Caller | GET | PATCH | DELETE |
|---|---|---|---|
| Owner | Allow | Allow permitted fields | Allow if business policy permits |
| Other user, same tenant | Deny unless shared | Deny unless explicitly editable | Deny |
| Other tenant | Deny | Deny | Deny |
| Administrator | Only as explicitly defined | Only as explicitly defined | Only as explicitly defined |
| Unauthenticated | Reject authentication | Reject authentication | Reject authentication |

Run each test against the actual API, not just the front-end. Include object IDs belonging to other users and tenants, plus attempts to alter owner, role, or tenant fields.

## Solution 9: Function-level authorization

A user can call the route directly even when the UI hides the button. The backend route must require an explicit permission such as `users:manage`, validate it on every request, deny by default, and have tests proving ordinary users are denied. UI visibility may improve usability but must not decide access.

## Solution 10: Authorization logging

Example event fields:

```json
{
  "event_type": "authorization_denied",
  "actor_id": "user-42",
  "action": "document:delete",
  "resource_type": "document",
  "resource_id": "doc-123",
  "outcome": "denied",
  "reason_code": "not_owner",
  "timestamp": "2026-01-01T12:00:00Z",
  "correlation_id": "req-example-001"
}
```

Use real timestamps and IDs from the application. Restrict access to logs, define retention, and avoid logging session cookies, bearer tokens, passwords, or full sensitive document contents.

## Solution 11: Threat-model review

Example resources: documents, sharing grants, project membership. Actions: read, edit, delete, share. Relationships: document owner, project member, explicitly invited collaborator.

Potential bypasses:

- Changing a document ID to access another user's file: scope lookups to authorized relationships and test cross-user reads/updates/deletes.
- Changing a sharing-grant ID or recipient: authorize the grant operation and validate both the grant owner and target recipient.
- Calling an administrative route directly: require a server-side administrative permission and test with a standard account.

Include tenant boundaries and file-storage paths in the review; authorization at the API layer must not be bypassed by direct object-storage access.

## Solution 12: Mini-project checklist

A solution meets the acceptance criteria when:

- Every protected route and operation calls a common authorization policy.
- Policy evaluation uses trusted identity and resource attributes.
- Data access is scoped to the user's allowed objects and tenant.
- Request schemas permit only expected writable fields.
- New roles, resources, and actions are denied until a policy allows them.
- Unit and integration tests cover success and denial paths.
- Authorization failures are logged safely.
- UI controls are treated as presentation only.
- Policy-service or configuration failures do not grant access.

## Further reading

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP IDOR Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html)
- [OWASP Top 10:2025 — Broken Access Control](https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/)
