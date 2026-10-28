# Examples — GitHub Actions Events and Triggers

The following examples are educational templates. Test them in a non-production repository and adjust permissions and action versions to your project.

## Example 1: Run on push and pull request
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Basic validation
        run: |
          echo "Event: $GITHUB_EVENT_NAME"
          echo "Ref: $GITHUB_REF"
```

## Example 2: Trigger only for selected paths
```yaml
name: Docs and application changes

on:
  push:
    branches: [main]
    paths:
      - 'app/**'
      - 'tests/**'
      - '!app/docs/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Relevant paths changed"
```

Remember that path filters are evaluated with GitHub's documented path-diff rules and limits. Test the exact patterns with representative changes.

## Example 3: Trigger on issue activity
```yaml
name: Label new issues

on:
  issues:
    types: [opened]

permissions:
  issues: write

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Add triage label
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ISSUE_NUMBER: ${{ github.event.issue.number }}
        run: gh issue edit "$ISSUE_NUMBER" --add-label "triage"
```

The `triage` label must already exist or be created through a controlled process. The job needs `issues: write`; avoid granting broader permissions than necessary.

## Example 4: Manual workflow with validated input
```yaml
name: Manual environment check

on:
  workflow_dispatch:
    inputs:
      environment:
        description: Environment to inspect
        type: choice
        options: [dev, staging]
        required: true

permissions:
  contents: read

jobs:
  inspect:
    runs-on: ubuntu-latest
    steps:
      - name: Print selection safely
        env:
          TARGET_ENV: ${{ inputs.environment }}
        run: |
          case "$TARGET_ENV" in
            dev|staging) echo "Inspecting $TARGET_ENV" ;;
            *) echo "Invalid environment" >&2; exit 1 ;;
          esac
```

The example deliberately excludes production. Add production only with explicit environment protection and approval requirements.

## Example 5: Scheduled maintenance check
```yaml
name: Weekly dependency review

on:
  schedule:
    - cron: '23 3 * * 1'
  workflow_dispatch:

permissions:
  contents: read

jobs:
  reminder:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Run the approved dependency review process"
```

Cron uses UTC by default. Choose a minute other than the top of the hour when practical to reduce contention during peak scheduling periods.

## Example 6: Tag-based release workflow
```yaml
name: Release validation

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: read

jobs:
  release-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Validate release tag $GITHUB_REF_NAME"
```

This validates a tag event; it does not publish a release or prove that the tag is trustworthy. Protect release permissions and validate the source commit before deployment.

## Example 7: Trigger after another workflow completes
```yaml
name: Follow-up after CI

on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]

permissions:
  contents: read

jobs:
  report:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest
    steps:
      - run: echo "The CI workflow completed successfully"
```

Use `workflow_run` carefully. Do not download or execute untrusted artifacts from a less-trusted workflow in a privileged follow-up workflow.

## Example 8: Event payload inspection
```yaml
name: Inspect event metadata

on:
  pull_request:
    types: [opened, reopened]

permissions:
  contents: read

jobs:
  inspect:
    runs-on: ubuntu-latest
    steps:
      - name: Print selected fields
        env:
          EVENT_NAME: ${{ github.event_name }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
          BASE_BRANCH: ${{ github.event.pull_request.base.ref }}
        run: |
          echo "Event: $EVENT_NAME"
          echo "PR number: $PR_NUMBER"
          echo "Base branch: $BASE_BRANCH"
```

Avoid printing the entire event payload if it may contain private repository metadata. Never embed untrusted event values directly into a generated shell script.
