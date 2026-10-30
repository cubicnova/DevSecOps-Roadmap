# Jenkins RBAC and Authorization

Authorization determines what an authenticated Jenkins user or group is allowed to do. Jenkins separates **authentication** (who you are) from **authorization** (what you may access or change). The authorization strategy evaluates permissions at relevant scopes such as the controller, folder, job, build, or agent.

## Learning objectives
- Distinguish authentication, authorization, users, groups, roles, and permissions.
- Apply least privilege to Jenkins access.
- Compare Matrix-based Security and Role-based Authorization Strategy.
- Design global, item, and agent roles.
- Test access with separate test accounts and verify inheritance.
- Avoid common privilege-escalation and lockout mistakes.

## Key concepts

| Concept | Meaning |
|---|---|
| Authentication | Establishes user identity, often through Jenkins accounts, LDAP, or Active Directory |
| Authorization | Determines whether an identity may perform an action |
| Permission | A specific capability, such as reading a job or configuring an agent |
| Role | A named collection of permissions assigned to users or groups |
| Global role | Applies broadly across Jenkins |
| Item role | Applies to jobs/folders matching a configured pattern |
| Agent role | Applies to selected build agents |
| Inheritance | Determines whether permissions flow from parent/global scopes |

## Common approaches

### Matrix-based security
Matrix authorization assigns individual permissions to users and groups. Project-based matrix authorization can add item- or agent-specific permissions. It is flexible, but permission matrices can become difficult to maintain as the number of users and jobs grows.

### Role-based Authorization Strategy
The Role Strategy plugin supports global, item, and agent roles. It can make team responsibilities easier to express and review. Item roles commonly use regular-expression patterns, so patterns should be carefully tested and reviewed.

Both approaches require deliberate configuration and a safe recovery plan. Plugin availability and features depend on the installed Jenkins and plugin versions.

## Example role design

| Role | Typical permissions | Scope |
|---|---|---|
| Jenkins Admin | Full administrative permissions | Controller |
| Developer | Read jobs, view builds, trigger approved jobs | Relevant team folders |
| Release Manager | Read jobs, trigger release job, approve deployment where configured | Release jobs/folders |
| Auditor | Read-only access to selected jobs and build records | Selected folders |
| Agent Operator | View/manage approved agents as required | Selected agents |
| Anonymous | No access, or only explicitly approved public read access | Global |

This is a starting point, not a universal permission recipe. Grant only the specific permissions required by each workflow. Avoid giving `Overall/Administer` to users who only need to run builds.

## Safe implementation workflow

1. Confirm a working administrator account and a recovery path before changing authorization.
2. Identify the authentication source and group names.
3. Inventory jobs, folders, agents, and sensitive operations.
4. Select Matrix-based Security or Role-based Authorization Strategy based on requirements.
5. Create small, clearly named roles.
6. Grant the minimum permissions at the narrowest practical scope.
7. Test with separate non-admin accounts in a test instance or maintenance window.
8. Verify both allowed and denied actions, including inherited access.
9. Document role owners and review assignments periodically.

## Security considerations

- Do not use “Logged-in users can do anything” for production.
- Do not grant `Overall/Administer` or script-console capabilities for routine development.
- Treat job configuration permission as powerful: a user who can modify a pipeline may be able to run code on its agent or access credentials available to that job.
- Restrict who can configure credentials, agents, plugins, and security settings.
- Review permissions inherited from global and parent-folder scopes.
- Be cautious with item-role regular expressions; test exact job names and edge cases.
- Keep an administrator session open while testing changes, but do not rely on that alone as a recovery plan.
- Use separate test users and verify that unauthorized users receive access-denied responses.
- Review plugin security advisories and maintain supported versions.
- Re-audit permissions after team, folder, plugin, or pipeline changes.

## Official documentation
- [Jenkins Access Control](https://www.jenkins.io/doc/book/security/access-control/)
- [Managing Security](https://www.jenkins.io/doc/book/security/managing-security/)
- [Role-based Authorization Strategy plugin](https://plugins.jenkins.io/role-strategy/)
- [Matrix Authorization Strategy plugin](https://plugins.jenkins.io/matrix-auth/)
