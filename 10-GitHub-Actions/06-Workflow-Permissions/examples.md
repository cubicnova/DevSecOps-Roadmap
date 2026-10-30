# Examples — GitHub Actions Workflow Permissions

These examples are templates. Test in a non-production repository and confirm required scopes against the current GitHub API and action documentation.

## Example 1: Minimal read-only CI
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
      - run: echo "Run build and tests"
```

## Example 2: Disable all token permissions by default
```yaml
name: Default-deny permissions

on:
  workflow_dispatch:

permissions: {}

jobs:
  inspect:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - run: echo "Repository content is readable"
```

The job explicitly grants only `contents: read`; other scopes remain unavailable to `GITHUB_TOKEN`.

## Example 3: Job-level permissions for issue labeling
```yaml
name: Triage issues

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
      - name: Add triage label
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ISSUE_NUMBER: ${{ github.event.issue.number }}
        run: gh issue edit "$ISSUE_NUMBER" --add-label "triage"
```

Ensure the label exists and the job only handles trusted issue metadata. Do not grant `contents: write` if the job does not change repository content.

## Example 4: Create a release with content write access
```yaml
name: Release task

on:
  workflow_dispatch:

permissions: {}

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - name: Show release permissions
        run: echo "This job can update repository content"
```

This example demonstrates permission scope only; it does not create a release. Add release steps only after reviewing the required permissions and protecting the workflow with approvals and trusted inputs.

## Example 5: Publish a package
```yaml
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - run: echo "Build and publish using the package registry's documented flow"
```

Use the exact permissions required by the registry and publishing action. Keep publishing credentials isolated from untrusted pull-request builds.

## Example 6: Upload supported code-scanning results
```yaml
permissions:
  contents: read
  security-events: write
```

Use `security-events: write` only when the workflow uploads supported security results and the feature/repository configuration permits it. The scanner or upload action may require additional setup.

## Example 7: OIDC permissions
```yaml
permissions:
  contents: read
  id-token: write
```

`id-token: write` allows a job to request an OIDC token; it does not itself grant cloud access. Configure trust conditions at the cloud identity provider, restrict repository/branch/environment claims, and request only the cloud role required.

## Example 8: Read-only API call
```yaml
permissions:
  contents: read

jobs:
  metadata:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Read repository metadata
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          REPOSITORY: ${{ github.repository }}
        run: gh api "repos/$REPOSITORY" --jq '.full_name'
```

The exact endpoint and permission requirements can vary. Do not print the token or include it directly in the URL.

## Example 9: Separate build from publish
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - run: echo "Build and test"

  publish:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - run: echo "Publish only after trusted-branch checks"
```

Add the real build/publish commands and suitable environment protection. A branch condition alone may not be sufficient for high-impact deployments.
