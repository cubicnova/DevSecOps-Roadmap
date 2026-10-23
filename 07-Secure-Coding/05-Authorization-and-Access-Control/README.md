# Authorization and Access Control

Learn how applications decide **who can do what, to which resource, and under which conditions**. This module focuses on secure, server-side authorization for web applications, APIs, and multi-tenant systems.

## Learning objectives

By the end of this module, you should be able to:

- Explain authentication versus authorization.
- Compare role-based access control (RBAC), attribute-based access control (ABAC), and relationship-based access control (ReBAC).
- Apply least privilege, deny-by-default, and server-side enforcement.
- Prevent broken function-level authorization, IDOR/BOLA, and property-level authorization issues.
- Design authorization checks for read, create, update, delete, export, and administrative actions.
- Write tests for both permitted and denied access.

## Core concepts

### Authentication vs. authorization

- **Authentication** establishes the identity of a user or service.
- **Authorization** determines whether that identity may perform a specific action on a particular resource.
- A valid login or token does not imply permission to access every resource.

### Common access-control models

| Model | Decision based on | Example |
|---|---|---|
| RBAC | Assigned role and permissions | `editor` can publish articles |
| ABAC | Subject, resource, action, and environment attributes | A staff member can access a record only in their department |
| ReBAC | Relationship between subject and resource | A project member can view that project |
| ACL | Explicit permissions attached to an object | A document grants read access to two users |

Models can be combined. Keep policy decisions centralized and enforce them close to the protected operation.

## Security principles

1. **Deny by default:** only explicitly permitted actions succeed.
2. **Least privilege:** grant only the permissions needed.
3. **Check every request:** include API calls, background jobs, exports, file downloads, and alternate HTTP methods.
4. **Enforce on the server:** UI hiding is not a security boundary.
5. **Scope access to the object:** a user who can read one invoice cannot automatically read every invoice.
6. **Fail closed:** if policy evaluation or required security configuration fails, do not grant access.
7. **Test negative cases:** verify that unauthorized access is denied.
8. **Log meaningful failures:** avoid logging secrets or unnecessary sensitive data.

## A practical authorization checklist

- [ ] Identify subjects, resources, actions, and trust boundaries.
- [ ] Document permission rules and business ownership requirements.
- [ ] Use a shared authorization service or policy layer.
- [ ] Derive identity from trusted server-side session/token validation.
- [ ] Query objects within the caller's permitted scope.
- [ ] Allow-list writable fields; prevent mass assignment.
- [ ] Check permissions on every relevant operation and API endpoint.
- [ ] Return safe errors without leaking resource details.
- [ ] Log denied attempts and alert on suspicious patterns.
- [ ] Test user-to-user, role-to-role, tenant-to-tenant, and field-level boundaries.
- [ ] Review permissions periodically and remove stale privileges.

## Common failure patterns

| Weakness | Typical symptom | Defensive approach |
|---|---|---|
| Broken function-level authorization | A regular user invokes an admin endpoint | Check required permission on the server |
| IDOR / BOLA | Changing an object ID exposes another user's record | Enforce object ownership/relationship on every access |
| Broken property-level authorization | API returns or accepts fields the caller should not access | Use response DTOs and explicit writable-field allow-lists |
| Privilege escalation | User changes a role or privileged field | Never trust client-supplied privilege attributes |
| Inconsistent checks | One route or HTTP method skips authorization | Centralize checks and test route/method combinations |
| Fail-open behavior | Policy service error leads to access being allowed | Deny on uncertainty and handle errors safely |

## Example: resource-level policy

A user may read an invoice if they own it or have a specifically authorized finance role. The client-provided invoice ID is only a lookup value; it is not proof of permission.

```python
def can_read_invoice(user, invoice):
    if user is None or invoice is None:
        return False

    if "finance_admin" in user.permissions:
        return True

    return invoice.owner_id == user.id
```

This is an illustrative policy function. In a real application, obtain `user` from validated server-side authentication, load the invoice through an authorized data-access layer where possible, and apply the policy to every relevant operation.

## Suggested learning path

1. Read this overview and compare access-control models.
2. Work through [`examples.md`](examples.md).
3. Complete [`exercises.md`](exercises.md) without looking at the solutions.
4. Check your reasoning in [`solutions.md`](solutions.md).
5. Apply the checklist to a small demo application you own or are authorized to test.

## Safe lab boundaries

Use a local intentionally vulnerable application or a system for which you have explicit authorization. Do not test access-control bypasses against real users, production systems, or third-party services without written permission.

## References

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP Insecure Direct Object Reference Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html)
- [OWASP Top 10:2025 — A01 Broken Access Control](https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/)
- [OWASP Proactive Controls — C1 Implement Access Control](https://top10proactive.owasp.org/the-top-10/c1-accesscontrol/)
