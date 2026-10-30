# Solutions — Workflow Permissions

These model answers illustrate secure configuration patterns. Confirm each scope with the current GitHub documentation for the exact operation and event.

## Solution 1: Read-only CI
```yaml
name: CI

on: [push, pull_request]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - run: echo "Run tests here"
```
Why: the job reads repository content and runs tests; it does not need to push commits, publish packages, or modify issues.

## Solution 2: Default-deny baseline
```yaml
permissions: {}

jobs:
  test:
    permissions:
      contents: read
```
When explicit permission scopes are specified, omitted scopes become `none`. A job can receive a different scope set from the workflow-level baseline.

## Solution 3: Issue labeling
```yaml
on:
  issues:
    types: [opened]

permissions: {}

jobs:
  label:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ISSUE_NUMBER: ${{ github.event.issue.number }}
        run: gh issue edit "$ISSUE_NUMBER" --add-label "triage"
```
Expected: the job can update issue labels, but does not receive repository-content write permission. Verify the label exists and the event/job can access the API.

## Solution 4: Diagnose a 403
1. Identify the failing API endpoint or action.
2. Check the top-level and job-level permission declarations.
3. Consult the API/action documentation for its required scope.
4. Check fork, Dependabot, organization, repository, and environment restrictions.
5. Add only the documented missing scope.
6. Rerun and verify that unrelated permissions remain absent.

Do not respond to every 403 by switching to `write-all` or granting a broad personal access token.

## Solution 5: Separate build and publish
```yaml
jobs:
  test:
    permissions:
      contents: read

  publish:
    needs: test
    permissions:
      contents: read
      packages: write
```
The test job does not need package publishing rights. Restricting `packages: write` to the publish job reduces impact if test code or an action is compromised.

## Solution 6: Fork pull requests
Fork pull-request workflows generally receive read-only `GITHUB_TOKEN` permissions and do not receive repository secrets. Repository settings and event type matter. Keep untrusted validation separate from privileged release or deployment jobs.

## Solution 7: `pull_request_target` threat model
**Risk:** The workflow executes in the base repository context and may have access to privileged permissions or secrets. Executing attacker-controlled code from a pull request could let that code misuse the workflow's access.

**Mitigations:**
- Prefer `pull_request` for ordinary build/test validation.
- Never check out and execute untrusted pull-request code in a privileged `pull_request_target` job.
- Use minimal permissions and avoid secrets unless essential.
- Separate trusted automation from untrusted artifacts and scripts.
- Validate event data and require approval for sensitive actions.

## Solution 8: OIDC
```yaml
permissions:
  contents: read
  id-token: write
```
`id-token: write` permits requesting an OIDC token. It does not automatically grant permissions in AWS, Azure, GCP, or another provider. The provider must trust the correct issuer, audience, repository, branch, and/or protected environment claims. Use short-lived credentials and restrict the resulting cloud role.

## Solution 9: Permission review checklist
- Is the permission explicitly declared?
- Can the job work with fewer scopes?
- Are write scopes limited to the jobs that need them?
- Are third-party actions trusted and reviewed?
- Is checkout credential persistence disabled for read-only jobs where appropriate?
- Can fork or Dependabot events reach secrets or privileged steps?
- Are untrusted values and artifacts handled safely?
- Are environment approvals and deployment protections configured?
- Are tokens kept out of logs and artifacts?
- Is there a documented owner for exceptions?

## Key rules
- Start with minimum access; add only demonstrated requirements.
- Workflow-level permissions establish a baseline; job-level permissions can further scope access.
- A job may be unable to write even if a different job can.
- Fork and Dependabot workflows have special restrictions.
- OIDC token permission is separate from the cloud role's authorization.
