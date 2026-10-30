# Repository Permissions — Suggested Solutions

The following are sample answers. Real assignments should be based on actual responsibilities, repository settings, and organization policy.

## Exercise 1 — Map roles to responsibilities

1. Documentation reader: **Read**.
2. Community manager handling issues and PRs: **Triage**.
3. Developer pushing feature branches: **Write**.
4. Project maintainer managing routine tasks: **Maintain**.
5. Trusted person managing access and sensitive settings: **Admin**.

Use the lowest role that meets the person's needs. Some capabilities depend on the repository type and product plan.

## Exercise 2 — Access inventory

Example fictional inventory:

| Person/team | Access path | Current role | Required task | Proposed role |
|---|---|---|---|---|
| docs-readers | Team | Read | Read documentation | Read |
| issue-triage | Team | Write | Manage issues and PRs | Triage |
| app-devs | Team | Write | Submit code | Write |
| project-lead | Direct | Admin | Routine maintenance | Review for Maintain |
| repo-owners | Team | Admin | Manage access and settings | Admin |

Review each row with the resource owner before changing access.

## Exercise 3 — Role comparison

- **Read:** view repository content and participate in permitted discussions.
- **Triage:** manage issues and pull requests without code-write access.
- **Write:** contribute code where branch rules permit.
- **Maintain:** manage routine repository tasks without the full set of sensitive admin actions.
- **Admin:** manage access and sensitive repository settings.

The exact permissions are documented by GitHub and can vary by repository context.

## Exercise 4 — Direct versus inherited access

Permissions can come from multiple paths. Removing direct access may leave team-based access intact. Inspect parent-team membership and inherited repository access before concluding that access has been removed.

## Exercise 5 — Offboarding

A useful checklist includes:
- remove direct repository access;
- remove team or organization access as appropriate;
- review inherited permissions;
- revoke or rotate related tokens and deploy keys when needed;
- review secrets and systems the person could access;
- transfer ownership of open issues, PRs, and automation;
- record approval and completion.

Do not assume removing repository access revokes all credentials previously created by the person.

## Exercise 6 — Branch protection

Repository roles control broad capabilities, while branch protection or rulesets can add requirements for protected branches. For example, a developer may push a feature branch but still need a pull request, required reviews, and successful status checks before merging into `main`.

## Exercise 7 — GitHub Actions permissions

`write-all` grants broad token permissions. A test-only workflow can often start with:

```yaml
permissions:
  contents: read
```

Add permissions only for tasks that require them, and review which events can trigger the workflow. Avoid exposing privileged secrets to untrusted pull request code.

## Exercise 8 — Quarterly access audit

- Export or review the current collaborator and team list.
- Confirm direct and inherited access.
- Check whether Admin access is limited to trusted owners.
- Verify organization base permissions.
- Inventory deploy keys and automation tokens.
- Review Actions token permissions and secret exposure paths.
- Remove access that is no longer required.
- Record the reviewer, date, exceptions, and follow-up owner.

## Mini-project — Sample least-privilege plan

| Identity | Suggested access | Additional controls |
|---|---|---|
| Maintainers | Maintain | Required reviews and status checks |
| Developers | Write | Feature branches and protected default branch |
| Issue triagers | Triage | No code-write permission needed |
| External reviewers | Read or Triage, as needed | Time-bound access where practical |
| CI automation | Narrow token permissions | Trusted triggers and protected secrets |

Document role owners, review access periodically, and remove credentials and memberships promptly when responsibilities change.
