# 06 — Workflow Permissions

## Overview
GitHub Actions workflows use the automatically created `GITHUB_TOKEN` to authenticate with GitHub APIs and perform repository operations. The workflow `permissions` key controls the token's access. Secure workflows grant only the permissions needed for each task and avoid exposing write-capable tokens to untrusted code.

This module covers workflow-level and job-level permissions, common scopes, least privilege, fork pull requests, third-party actions, and troubleshooting permission errors.

## Learning objectives
By the end of this module, you should be able to:
- Explain what `GITHUB_TOKEN` is and why it is created per job.
- Configure workflow-level and job-level `permissions`.
- Apply least privilege by setting unused scopes to `none`.
- Identify common permission scopes for checkout, pull requests, issues, packages, and security reports.
- Separate read-only CI from jobs that need write access.
- Recognize risks from untrusted pull requests and privileged events.
- Troubleshoot HTTP 403 errors and missing permissions safely.

## 1. What is `GITHUB_TOKEN`?
GitHub creates a short-lived repository-scoped token for each job. Actions can access it through supported contexts even if it is not explicitly passed to an action. Therefore, a workflow should define permissions intentionally rather than assuming that an action cannot access the token.

## 2. Workflow-level permissions
Top-level permissions establish a baseline for jobs in the workflow.

```yaml
name: Read-only CI

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

If you specify individual permission keys, all omitted permission scopes are set to `none`. `write` access includes `read` access for that scope. `permissions: {}` disables all `GITHUB_TOKEN` permissions unless a job explicitly grants the scopes it needs.

## 3. Job-level permissions
Different jobs may need different access. Grant write access only to the job that requires it.

```yaml
name: Validate and label

on:
  issues:
    types: [opened]

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - run: echo "Validation requires no write access"

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

The `triage` label must exist. The example illustrates scoping; in a real workflow, verify each job's actual requirements and use the narrowest possible permissions.

## 4. Common permission scopes
Names and availability are maintained in the official workflow syntax reference. Common scopes include:

| Scope | Typical purpose |
|---|---|
| `contents: read` | Checkout or read repository content |
| `contents: write` | Push commits or create/update repository content |
| `pull-requests: read` | Read pull-request metadata |
| `pull-requests: write` | Modify pull requests or comments through supported APIs |
| `issues: write` | Create or update issues and labels |
| `packages: write` | Publish packages to GitHub Packages |
| `security-events: write` | Upload supported code-scanning results |
| `id-token: write` | Request an OIDC token for a configured identity provider |
| `actions: read` | Read workflow/action-related information |
| `deployments: write` | Create or update deployment records |

Grant only the scopes needed for the operation. A particular API or action may require additional permissions; check its current documentation rather than guessing.

## 5. Read-only CI versus write operations
Most build-and-test workflows need only `contents: read`. Operations such as publishing a package, creating a release, opening a pull request, or uploading security results may need additional scopes. Separate build and publish jobs where practical so a test step does not inherit publish permissions.

## 6. Forked pull requests and privileged triggers
- For pull requests from forks, write permissions are generally downgraded to read-only unless repository settings explicitly allow write tokens.
- Secrets are generally not available to ordinary fork pull-request workflows.
- `pull_request_target` runs in the base repository context and can have elevated token permissions. Never check out and execute untrusted pull-request code in a privileged `pull_request_target` workflow.
- Dependabot-triggered workflows have special restrictions and generally use read-only token permissions.
- Avoid using a privileged workflow to run scripts or artifacts produced by an untrusted workflow.

## 7. Secure action and checkout practices
- Pin third-party actions to reviewed immutable commit SHAs when your supply-chain policy requires it; use trusted maintainers and review changes.
- Do not pass `GITHUB_TOKEN` to an action that does not need it.
- For read-only checkout jobs, consider `persist-credentials: false` to avoid leaving the token in local Git configuration.
- Keep long-lived personal access tokens out of workflows when `GITHUB_TOKEN` or a narrowly scoped GitHub App installation token is sufficient.
- Never print tokens or dump all environment variables into logs.

## 8. Troubleshooting
**HTTP 403 / Resource not accessible by integration**
1. Identify the exact API or action that failed.
2. Check the workflow's top-level `permissions`.
3. Check the specific job's `permissions`; it can narrow or override the workflow-level configuration.
4. Check repository/organization settings and fork/Dependabot restrictions.
5. Confirm the operation's documented required permission scope.
6. Add only the missing scope, rerun, and verify no broader permission is needed.

**Workflow works in one event but fails in another**
- The token may be read-only for a fork pull request.
- A secret may not be available to that event.
- The event may use a different security context.
- An environment protection rule or organization policy may block access.

## Further reading
- [Workflow syntax: permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions)
- [GITHUB_TOKEN concept](https://docs.github.com/en/actions/concepts/security/github_token)
- [Authenticate with GITHUB_TOKEN](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
