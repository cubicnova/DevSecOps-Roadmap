# IAM and Least Privilege - Examples

These examples illustrate IAM decisions. Policy syntax and available controls differ across platforms; validate configuration in a test environment before applying it to production.

## Example 1: Developer Access

**Scenario:** A developer needs to read application logs and deploy to a development environment but must not change production IAM policies.

**Poor design:** Give the developer global administrator access because it is easier to configure.

**Least-privilege design:**
- Assign a developer role with repository and development-environment permissions.
- Allow read-only access to the required log resources.
- Restrict production access and identity-policy administration.
- Require a separate approval process for production changes.
- Audit role assignments and deployment actions.

**Lesson:** Permissions should match the task, not the person's general technical ability.

## Example 2: RBAC vs. ABAC

**RBAC approach:** Assign users to roles such as `Developer`, `SecurityReviewer`, and `PlatformAdmin`. Each role has a reviewed set of permissions.

**ABAC approach:** Permit a deployment job to update a resource only when its environment attribute matches the job's approved environment and other required conditions are satisfied.

| Question | RBAC | ABAC |
|---|---|---|
| Main decision input | Assigned role | Attributes and context |
| Useful when | Job functions are relatively stable | Policies depend on tags or context |
| Common risk | Roles become overly broad | Attributes are incorrect or can be manipulated |

Many systems combine these models.

## Example 3: Access Review

A quarterly review finds:
- An employee still has access to a previous team's database.
- A former contractor's account remains active.
- A CI/CD identity can delete all cloud resources even though it only deploys one service.

Suggested actions:
1. Confirm business owners and current requirements.
2. Remove the former contractor's access through the established offboarding process.
3. Remove obsolete team permissions.
4. restrict the CI/CD identity to required actions and resources.
5. Review audit logs for potentially inappropriate use and document the changes.

## Example 4: Just-in-Time Privilege

**Scenario:** An engineer occasionally needs production administrator permissions for approved maintenance.

A safer workflow grants a short-lived elevated role after approval, records the reason and approver, logs privileged activity, and automatically expires the access. Emergency access should be available only through a controlled, monitored process.

## Example 5: IAM Policy Review Pattern

When reviewing any policy, ask:
- Are actions limited to what the task requires?
- Are resources scoped as narrowly as practical?
- Are conditions available to restrict environment, identity, or request context?
- Does the policy allow privilege escalation or changing access controls?
- Are broad wildcard permissions justified and documented?
- Is the identity human, service, or automation—and does the policy fit that identity?
- Are logs and periodic reviews in place?

**Illustrative pseudo-policy — not directly deployable syntax:**

```text
ALLOW:
  action: read application logs
  resource: logs for the development service
  condition: identity is assigned the Developer role

DENY / NOT GRANTED:
  action: modify IAM policies
  resource: production account
```

The exact syntax and evaluation rules depend on the platform. Test both allowed and denied cases.

## Example 6: Secure CI/CD Identity

**Scenario:** A pipeline builds an application and deploys it to staging.

Recommended controls:
- Use a dedicated workload identity rather than a developer's personal credentials.
- Prefer short-lived credentials or workload identity federation where supported.
- Grant only required build and staging-deployment actions.
- Do not expose secrets to untrusted pull-request workflows.
- Separate production deployment permissions from routine build permissions.
- Record deployment identity, artifact, environment, and outcome in audit logs.

## Example 7: Joiner-Mover-Leaver

| Event | IAM action |
|---|---|
| New employee joins | Create a unique account after approval and assign role-based access |
| Employee changes teams | Reassess access, remove old permissions, then grant new required access |
| Contractor engagement ends | Disable account and revoke sessions, tokens, and credentials |
| Service is retired | Remove workload identity, associated policies, and unused secrets after dependency checks |

The goal is to prevent access from accumulating after it is no longer needed.
