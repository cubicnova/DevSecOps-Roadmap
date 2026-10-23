# Authorization and Access Control — Exercises

Complete these exercises in a local demo project or a code review of an application you own or are authorized to assess.

## Exercise 1: Authentication vs. authorization

An API validates a user's session and then returns any order whose ID appears in `/api/orders/{id}`.

1. Which security decision is already being made?
2. Which decision is missing?
3. What must the server check before returning an order?

## Exercise 2: Build a permission matrix

For a simple document application, define permissions for these roles:

- Viewer
- Editor
- Owner
- Administrator

Actions: view, edit, delete, share, manage users.

Write down any assumptions, such as whether an editor may edit only documents they belong to. Use deny-by-default for any unspecified combination.

## Exercise 3: Find the IDOR

Review this pseudocode:

```python
def download_report(request, report_id):
    report = reports.get(report_id)
    return send_file(report.path)
```

1. Identify the missing security checks.
2. Rewrite the logic so the report is retrieved only if the current user is authorized.
3. Explain why changing integer IDs to UUIDs is not a complete fix.

## Exercise 4: Tenant isolation

A SaaS API accepts `tenant_id` and `project_id` from the request. A user belongs to tenant `acme`, but requests a project belonging to tenant `globex`.

Design the validation and lookup logic. Explain which values should come from trusted server-side identity/membership state.

## Exercise 5: Field-level authorization

An endpoint accepts this payload:

```json
{
  "display_name": "Sam",
  "role": "admin",
  "tenant_id": "other-tenant",
  "is_active": true
}
```

The endpoint is intended only to update a user's display name.

1. Explain the risk.
2. Define an allow-list of writable fields.
3. Describe how role, tenant, and account-status changes should be handled.

## Exercise 6: ABAC policy

A case-management system should allow access only when all these conditions hold:

- User is active.
- User and case belong to the same department.
- User clearance is at least the case classification.
- The case has not passed its access deadline.

Write a policy function and list at least five positive and negative tests.

## Exercise 7: Fail closed

The authorization service times out. The application currently treats the timeout as “allow.”

1. Why is this unsafe?
2. What should the application do?
3. What should be logged, and what should not be exposed to the client?

## Exercise 8: Test coverage

Create a test matrix for `GET`, `PATCH`, and `DELETE` on `/api/documents/{id}` for:

- Owner
- Another user in the same tenant
- User in another tenant
- Administrator
- Unauthenticated caller

Include expected outcomes and explain any intentional exceptions.

## Exercise 9: Function-level authorization

A hidden “Admin” button is not shown to ordinary users, but the backend route `/api/admin/users` does not check permissions.

Explain why the UI is not a security control and outline a server-side fix.

## Exercise 10: Authorization logging

Design an audit event for a denied request. Include useful fields such as actor identifier, action, resource type, outcome, timestamp, and correlation ID. Avoid storing credentials, access tokens, or unnecessary sensitive resource data.

## Exercise 11: Threat-model review

For a file-sharing service, identify:

- Three protected resources
- Four actions
- At least three subject/resource relationships
- Two likely authorization bypasses
- Preventive controls and negative tests for each bypass

## Exercise 12: Mini-project

Build a small API with users, projects, and documents. Implement:

- RBAC for administrative functions
- Object-level access for project members
- Tenant isolation
- Field allow-lists
- Deny-by-default behavior
- Automated tests for allowed and denied operations
- Safe audit logging

**Acceptance criteria:** no endpoint relies on UI visibility; each protected operation checks authorization; cross-user and cross-tenant tests fail safely; missing policy data does not grant access.
