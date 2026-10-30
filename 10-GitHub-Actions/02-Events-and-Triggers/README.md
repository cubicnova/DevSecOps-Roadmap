# 02 — Events and Triggers

## Overview
GitHub Actions workflows run when a configured event occurs, at a scheduled time, or when someone manually starts the workflow. The `on` key in a workflow YAML file defines these triggers. Activity types and filters help limit when a workflow runs.

This module covers practical event selection, branch and path filters, manual and scheduled workflows, event payloads, and secure trigger design.

## Learning objectives
By the end of this module, you should be able to:
- Explain the difference between an event, an activity type, and a filter.
- Configure `push`, `pull_request`, `issues`, `release`, `workflow_dispatch`, `schedule`, and `workflow_run` triggers.
- Filter events by branch, tag, path, and activity type.
- Read useful values from the `github` context and event payload.
- Understand how `GITHUB_TOKEN`-generated events can affect workflow chaining.
- Avoid unsafe use of `pull_request_target` and untrusted event data.
- Troubleshoot workflows that do not run as expected.

## Core terminology

- **Event:** A repository or platform activity, such as a push or pull request.
- **Activity type:** A particular action associated with an event, such as an issue being opened or labeled.
- **Filter:** A condition limiting the branches, tags, or paths that cause a workflow to run.
- **Manual trigger:** `workflow_dispatch`, which enables a user to start a workflow and optionally supply inputs.
- **Scheduled trigger:** `schedule`, which uses POSIX cron syntax and runs on GitHub's scheduling service.
- **Event payload:** Structured information about the activity, exposed through contexts such as `github.event`.

## Common trigger patterns

### Push to selected branches
```yaml
name: Build on main and release branches

on:
  push:
    branches:
      - main
      - 'releases/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Build for $GITHUB_REF"
```

### Pull request validation
```yaml
name: Pull request checks

on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Validate pull request"
```

The branch filter on `pull_request` refers to the **target/base branch**. Use `github.event.pull_request.head.ref` if you need the source branch name.

### Path filters
```yaml
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'tests/**'
      - '!docs/**'
```

When both branch and path filters are configured, both must match. Path filters have event-specific limits and pattern behavior; check the official documentation for edge cases. A skipped required workflow can leave a required check pending, so design required checks carefully.

### Manual workflow with inputs
```yaml
name: Manual maintenance task

on:
  workflow_dispatch:
    inputs:
      environment:
        description: Target environment
        required: true
        type: choice
        options: [staging, production]
      dry_run:
        description: Show intended changes only
        required: true
        type: boolean
        default: true

permissions:
  contents: read

jobs:
  inspect:
    runs-on: ubuntu-latest
    steps:
      - name: Show selected options
        env:
          TARGET_ENV: ${{ inputs.environment }}
          DRY_RUN: ${{ inputs.dry_run }}
        run: |
          echo "Target environment: $TARGET_ENV"
          echo "Dry run: $DRY_RUN"
```

A manual input is not a substitute for authorization. Protect production environments and use narrowly scoped permissions.

### Scheduled workflow
```yaml
name: Scheduled repository check

on:
  schedule:
    - cron: '17 4 * * 1'
  workflow_dispatch:

permissions:
  contents: read

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Weekly check at 04:17 UTC on Monday"
```

Scheduled workflows use UTC unless a supported timezone is explicitly configured. Scheduling can be delayed during high load; do not use it for exact-time guarantees. The workflow file must be on the default branch for scheduled runs.

## Security notes
- Prefer `pull_request` for ordinary validation of contributions.
- Be cautious with `pull_request_target`: it runs in the base repository context and may have access to privileged tokens or secrets. Never check out and execute untrusted pull-request code in a privileged context.
- Set minimal `permissions` for `GITHUB_TOKEN`.
- Do not interpolate untrusted event fields directly into shell scripts. Pass values through environment variables and quote them appropriately.
- Treat manual inputs as untrusted values; validate against an allowlist before using them in commands.
- Events caused by a workflow's `GITHUB_TOKEN` generally do not start new workflow runs, with documented exceptions such as `workflow_dispatch`, `repository_dispatch`, and certain pull-request events. Consider this when chaining automation.

## Troubleshooting checklist
1. Confirm the workflow file is under `.github/workflows/`.
2. Validate YAML indentation and the exact `on` event names.
3. Check that branch, tag, path, and activity-type filters match the event.
4. Verify the workflow exists on the branch or default branch as required by that event.
5. Check whether the workflow is disabled or awaiting approval.
6. Review permissions and event payload assumptions.
7. Remember that GitHub Actions workflows triggered by `GITHUB_TOKEN` may not recursively trigger another workflow.
8. Inspect the Actions tab and workflow run logs.

## Further reading
- [Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- [Triggering a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
- [Workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)
- [Contexts reference](https://docs.github.com/en/actions/learn-github-actions/contexts)
