# Solutions and Guidance: Jenkins RBAC and Authorization

These are reference answers. Available permissions and configuration screens depend on Jenkins core, the selected authorization plugin, and other installed plugins.

## Lab 1: Authentication vs authorization
Authentication establishes identity (for example, a user signs in through LDAP). Authorization decides whether that identity can read a job, trigger a build, configure an item, manage an agent, or administer Jenkins. They are separate settings and both must be configured.

## Lab 2: Inventory
Record at minimum:
- User and group sources
- Global settings and plugins
- Folders and jobs
- Production/release jobs
- Credentials and which jobs can use them
- Agents and labels
- Users with configure, credential, script-console, or administrator access

Prioritize resources that can execute code, access secrets, publish artifacts, or deploy to production.

## Lab 3: Role design

| Role | Example allowed actions | Exclude by default |
|---|---|---|
| Administrator | Configure controller and security | Shared everyday use |
| Developer | Read/build approved team jobs | Controller admin, credential management |
| Release manager | Run approved release jobs | Plugin install, security changes |
| Auditor | Read selected jobs/builds | Build, configure, delete |
| Agent operator | Manage assigned agents | Broad credential and job access |

These are starting points. Add permissions only where a documented workflow requires them.

## Lab 4: Permission matrix
Build the matrix from actual required tasks rather than copying a universal template. Check permission implications and inheritance. In particular, controller administration is highly privileged; job configuration can also be dangerous when a job can access secrets or privileged agents.

## Lab 5: Matrix-based Security
Use the test instance to grant a developer read/build access to one test job, then verify that configure/delete/controller settings are denied. Test with a separate account and verify that global grants or parent-folder grants do not provide unexpected access.

## Lab 6: Role Strategy
Create narrowly scoped global roles for broad access and item roles for team folders or selected jobs. Assign roles to groups where possible. Verify the plugin version and exact permission names in the installed interface. Item roles use patterns, so test their match behavior carefully.

## Lab 7: Regular expressions
For example, `^team-a/.*$` is intended to match item names under `team-a/` if that is the full-name format used by your Jenkins setup. Confirm actual full item names and test similarly named folders. Use anchored patterns and avoid broad patterns that can match production jobs unintentionally.

## Lab 8: Inheritance
Matrix authorization permissions can be additive, and Role Strategy has its own global/item role semantics. A global grant may permit access even when an item-level role is more restrictive. Read the documentation for the installed strategy and verify with a test account; do not assume a local rule cancels a broader grant.

## Lab 9: Least privilege
Test every identity independently:
- Developer: assigned job read/build allowed; controller security changes denied.
- Release manager: approved release job allowed; unrelated jobs denied.
- Auditor: selected read access allowed; build/configure/delete denied.
- Anonymous: private resources denied unless explicitly intended.

Record actual results rather than relying on role names alone.

## Lab 10: Privilege escalation
A user who can modify a pipeline may alter its commands to use credentials already available to the job or run code on its agent. Mitigations include:
- Restrict job configuration to trusted maintainers.
- Narrow credential scope and use least-privileged tokens.
- Separate untrusted validation from privileged deployment.
- Protect release branches and deployment jobs.
- Isolate agents and avoid sharing privileged environments with untrusted builds.
- Review changes and audit credential use.

## Lab 11: Change and recovery plan
1. Confirm an administrator account and documented recovery method.
2. Export or record current roles and grants using an approved method.
3. Make the smallest possible change in a maintenance window or test instance.
4. Test with non-admin identities.
5. Confirm allowed and denied actions.
6. Roll back if administrators lose access or an unintended grant appears.
7. Record approver, change, test results, and follow-up actions.

Do not rely only on a browser session that might become inaccessible after the change.

## Lab 12: Final mini-project
The deliverable should include:
- A role/permission matrix tied to documented responsibilities
- A record of the selected authorization strategy and plugin version
- Tests for allowed and denied actions
- Pattern tests for item roles, where applicable
- A recovery plan
- Residual risks and review date

## Security checklist
- [ ] No unrestricted access for all logged-in users
- [ ] Administrative permissions restricted to a small trusted group
- [ ] Job configuration permissions are carefully controlled
- [ ] Credentials and agents are treated as privileged resources
- [ ] Global and inherited permissions are reviewed
- [ ] Item-role patterns are tested against unintended matches
- [ ] Allowed and denied actions are verified with test identities
- [ ] Changes have a recovery plan and approver
- [ ] Authorization and plugin versions are periodically reviewed

## Official references
- [Jenkins Access Control](https://www.jenkins.io/doc/book/security/access-control/)
- [Managing Security](https://www.jenkins.io/doc/book/security/managing-security/)
- [Role-based Authorization Strategy plugin](https://plugins.jenkins.io/role-strategy/)
- [Matrix Authorization Strategy plugin](https://plugins.jenkins.io/matrix-auth/)
