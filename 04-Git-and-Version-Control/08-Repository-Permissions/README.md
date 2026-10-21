# Repository Permissions

Repository permissions control who can view, contribute to, manage, or administer a code repository. Good access control helps protect source code, secrets, release workflows, and project settings.

This module focuses on GitHub repository access, with practical examples of least privilege, team-based access, collaborator reviews, and access audits.

## Learning objectives

- Distinguish repository permissions from organization roles.
- Understand the common GitHub repository roles.
- Select appropriate access for contributors, reviewers, maintainers, and administrators.
- Apply least privilege and use teams for repeatable access management.
- Audit current access and remove access that is no longer required.
- Recognize risks involving deploy keys, automation tokens, and repository secrets.

## Why permissions matter

Excessive repository access can allow accidental or malicious changes, exposure of private code, workflow tampering, or deletion of important resources. Grant each person or automation identity only the permissions needed for its task, then review access regularly.

## GitHub repository roles

For repositories owned by an organization, the standard repository roles, from least to most privileged, are:

| Role | Typical use | General capability |
|---|---|---|
| Read | Viewers and non-code contributors | Read repository content and participate in permitted discussions |
| Triage | Issue and pull request coordinators | Manage issues and pull requests without write access to code |
| Write | Active contributors | Push to branches where repository rules permit |
| Maintain | Project maintainers | Manage many repository tasks without the full destructive/admin capability set |
| Admin | Repository administrators | Manage access and sensitive repository settings |

Exact capabilities can vary by repository type, product plan, and policy. See [GitHub's official repository roles documentation](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization).

For a repository under a personal account, access is generally managed through the owner and collaborators rather than the full organization role model.

## Least-privilege examples

- A person who only reads documentation usually needs **Read**, not Write.
- Someone triaging issues may need **Triage**, not permission to push code.
- A developer contributing code usually needs **Write**, subject to branch protection and review rules.
- A project coordinator may need **Maintain** for repository operations but not full administration.
- Keep **Admin** access limited to trusted people who manage repository settings, access, or sensitive operations.
- Use dedicated, narrowly scoped identities for automation where supported; avoid sharing a human's personal token.

## Managing access in GitHub

For an organization repository, a user with sufficient administrative permissions can generally:

1. Open the repository on GitHub.
2. Open **Settings**.
3. Find the access-management section, often labelled **Collaborators and teams** or similar.
4. Review direct collaborators and team access.
5. Add a person or team with the minimum required role, or adjust/remove access when it is no longer needed.
6. Check organization base permissions and team inheritance where applicable.

GitHub's interface can change. Use the official documentation for current UI details:
- [Managing repository roles](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles)
- [Managing team access](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/managing-team-access-to-an-organization-repository)

## Teams versus direct collaborators

Teams are useful for organization-owned repositories because access can be managed consistently for a group. Direct collaborator access can be appropriate for a specific external contributor, but should be documented and reviewed.

Check for inherited access from parent teams. Removing a child team's direct access may not remove permissions inherited from a parent team.

## Permission review checklist

- [ ] Every user and team has a clear business or project need.
- [ ] The assigned role is the lowest level that supports the task.
- [ ] Admin access is limited and has an owner.
- [ ] Former employees, contractors, and inactive collaborators are removed promptly.
- [ ] Team inheritance and organization base permissions are understood.
- [ ] Branch protection or rulesets protect important branches.
- [ ] Actions/workflow permissions and secrets are restricted appropriately.
- [ ] Deploy keys and access tokens are inventoried and rotated when needed.
- [ ] Access is reviewed after role changes and on a recurring schedule.

## Important security considerations

### Repository access is not the same as branch protection

A role can grant the ability to write to a repository, while branch protection or rulesets determine whether specific changes can be pushed or merged directly. Use both access control and review/check requirements.

### Secrets and automation

- Do not store credentials in source code.
- Scope tokens to the minimum repositories and permissions required.
- Review GitHub Actions workflow permissions, especially `GITHUB_TOKEN` permissions.
- Do not expose privileged secrets to untrusted pull request code.
- Remove unused deploy keys and rotate credentials if they may have been exposed.

### Access removal and offboarding

When access is no longer needed, remove direct collaborator access, review team memberships and inherited permissions, and revoke related tokens or keys where appropriate. Removing a user from a repository does not automatically invalidate every credential they may previously have created.

## Exercises

1. Map five example team members to the least-privileged role that meets their responsibilities.
2. Compare Read, Triage, Write, Maintain, and Admin.
3. Draft a repository access-review checklist for a small engineering team.
4. Explain the difference between repository roles and branch protection.
5. Review a hypothetical team tree and identify inherited access.
6. Create an offboarding checklist for a contractor.
7. Identify risks in a workflow that has broad write permissions.
8. Propose a least-privilege access model for a public open-source project and a private internal project.

## References

- [GitHub: Access permissions](https://docs.github.com/en/get-started/learning-about-github/access-permissions-on-github)
- [GitHub: Repository roles for an organization](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization)
- [GitHub: Managing repository roles](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles)
- [GitHub: Managing team access](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/managing-team-access-to-an-organization-repository)
