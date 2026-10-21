# Repository Permissions — Examples

These examples describe access-planning scenarios. They do not change permissions in a live repository.

## 1. Choose the lowest appropriate role

| Scenario | Suggested role | Reason |
|---|---|---|
| Product stakeholder reads code and docs | Read | No code contribution required |
| Community coordinator labels issues and manages PR workflow | Triage | Needs issue/PR management without pushing code |
| Developer submits code changes | Write | Needs contribution capability |
| Project lead manages routine repository tasks | Maintain | Needs maintenance without full admin privileges |
| Trusted repository owner manages settings and access | Admin | Needs administrative control |

Confirm the exact capabilities for the repository and GitHub plan before applying a role.

## 2. Access review inventory template

```markdown
| Person/team | Access path | Current role | Required task | Proposed role | Owner | Review date |
|---|---|---|---|---|---|---|
| frontend-team | Team | Write | Submit frontend changes | Write | Engineering lead | YYYY-MM-DD |
| release-coordinator | Direct | Admin | Manage releases only | Review for lower role | Repository owner | YYYY-MM-DD |
```

Use real identities only in an appropriately protected internal document. Do not commit private access inventories to a public repository.

## 3. Least-privilege decision tree

```text
Does the person need repository access?
  No  -> Do not grant access.
  Yes -> Do they only need to read?
           Yes -> Read
           No  -> Do they manage issues and PRs without pushing code?
                    Yes -> Triage
                    No  -> Do they contribute code?
                             Yes -> Write
                             No  -> Do they manage routine repository tasks?
                                      Yes -> Maintain
                                      No  -> Admin only if full administration is required
```

## 4. Review access in the GitHub UI

For an organization-owned repository, a user with suitable permissions can open repository **Settings** and review access under the repository's access-management area. Review both direct collaborators and teams, including inherited team access. The exact labels may change over time.

## 5. Example GitHub Actions permission minimization

A workflow that only checks out code and runs tests may not need broad write access. Consider explicitly limiting token permissions:

```yaml
permissions:
  contents: read
```

Add permissions only when the workflow genuinely needs them. For example, a workflow that publishes a release may require additional write permissions, but should use the smallest scope and trusted triggers necessary. Validate permissions against the specific actions and workflow tasks.

## 6. Example offboarding checklist

```markdown
- [ ] Remove repository collaborator access.
- [ ] Remove or adjust organization and team membership as appropriate.
- [ ] Review inherited team permissions.
- [ ] Revoke or rotate personal access tokens and deploy keys where applicable.
- [ ] Review secrets or credentials the person could access.
- [ ] Transfer ownership of needed issues, PRs, and automation.
- [ ] Record who approved the access removal and when.
```

## 7. Risk review example

**Scenario:** Every contributor is an administrator.

**Risks:** Accidental repository deletion, uncontrolled access changes, broad security-setting changes, and weakened review controls.

**Improvement:** Keep a small set of trusted administrators, give developers Write, use Triage for issue coordination, and enforce branch rules and required reviews.
