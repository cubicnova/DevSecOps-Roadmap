# Solutions — Events and Triggers

These are model solutions. Verify event-specific details against the current GitHub documentation and your repository's configuration.

## Solution 1: Push trigger
```yaml
name: Push validation

on:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Validated commit $GITHUB_SHA"
```
Expected result: a run starts when a commit is pushed to `main`, assuming the workflow exists and is enabled.

## Solution 2: Pull request trigger
```yaml
on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]
```
- `opened`: a pull request is opened.
- `synchronize`: the source branch receives new commits.
- `reopened`: a previously closed pull request is reopened.

Here, `branches: [main]` filters by the target/base branch, not the source branch.

## Solution 3: Branch and path filters
```yaml
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'tests/**'
```
Expected: changes matching the included patterns can trigger the workflow; documentation-only changes should not. When branch and path filters are both present, both conditions must be satisfied. Confirm behavior for mixed commits and the repository's required status checks.

## Solution 4: Manual input validation
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [dev, staging]
        required: true
      dry_run:
        type: boolean
        default: true
        required: true
```
Use the input as data, not as executable shell text. Validate again in the job if the value affects an operation. Use protected environments and approvals for sensitive deployments.

## Solution 5: Schedule
Example:
```yaml
on:
  schedule:
    - cron: '23 3 * * 1'
  workflow_dispatch:
```
Interpretation: minute 23, hour 3, every day of the month, every month, Monday, in UTC by default. Scheduled runs may be delayed; manual dispatch is useful for testing.

## Solution 6: Issue labeling
```yaml
on:
  issues:
    types: [opened]

permissions:
  issues: write
```
Use `github.event.issue.number` to identify the issue. Store it in an environment variable and quote it in the shell command. Confirm the label exists and the workflow's token has only the permissions needed.

## Solution 7: Tag event
```yaml
on:
  push:
    tags:
      - 'v*'
```
Create and push a test tag. The workflow validates that tag event, but release deployment should also verify trusted source, approvals, environment protections, and artifact provenance.

## Solution 8: Trigger troubleshooting sequence
1. Confirm the YAML file is under `.github/workflows/`.
2. Check indentation and the `on` key.
3. Verify the event happened and the configured activity type includes it.
4. Check branch, tag, and path patterns.
5. Check whether that event requires the workflow file on the default branch.
6. Check whether the workflow is disabled or needs approval.
7. Check whether a prior workflow used `GITHUB_TOKEN` to create the event.
8. Inspect Actions logs and repository settings.

Do not assume an absent run means GitHub is broken; filters and token behavior commonly explain it.

## Solution 9: Safe event value handling
**Safer pattern:**
```yaml
- name: Use pull request metadata
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: |
    printf 'Pull request title: %s\n' "$PR_TITLE"
```
**Riskier pattern:**
```yaml
- run: echo "${{ github.event.pull_request.title }}"
```
Directly inserting untrusted data into a shell script can change the script's syntax. Environment-variable passing and correct quoting reduce this risk, but values should still be validated before being used as arguments or paths.

## Solution 10: `pull_request_target` threat model
**Risk:** The workflow runs in the base repository context and may have access to secrets or write permissions. If it checks out and executes attacker-controlled pull-request code, that code may use the workflow's privileges.

**Mitigations:**
- Prefer `pull_request` for ordinary untrusted code validation.
- Never execute untrusted PR code in a privileged `pull_request_target` job.
- Keep permissions minimal and do not expose secrets unnecessarily.
- Separate trusted automation from untrusted build/test execution.
- Validate and sanitize event data.
- Review downloaded artifacts and external inputs before use.

## Important `GITHUB_TOKEN` behavior
Events generated using the repository's `GITHUB_TOKEN` generally do not trigger new workflow runs, to prevent recursion. Documented exceptions include `workflow_dispatch`, `repository_dispatch`, and certain pull-request activity cases. If one workflow must intentionally trigger another, choose a supported event and authentication approach with the least privilege necessary.

## Final review
A correct trigger configuration combines the right event, activity type, filters, permissions, and trust boundary. Always test both expected-trigger and expected-no-trigger cases.
