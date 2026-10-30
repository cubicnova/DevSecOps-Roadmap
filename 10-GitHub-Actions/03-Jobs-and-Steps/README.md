# 03 - Jobs and Steps

Understand how GitHub Actions organizes automation into jobs and steps, how jobs run on runners, and how to control ordering, conditions, outputs, and failure behavior.

## Learning objectives

By completing this module, you should be able to:

- Define jobs and steps in a workflow.
- Configure a runner using `runs-on`.
- Explain sequential steps versus parallel jobs.
- Add dependencies with `needs`.
- Use `if`, `id`, `env`, and step outputs.
- Set timeouts and understand failure handling.
- Apply least-privilege permissions and avoid exposing secrets.

## Jobs versus steps

| Feature | Job | Step |
|---|---|---|
| Purpose | Groups related tasks | Performs one task within a job |
| Execution environment | Runs on a selected runner | Runs within its job's runner |
| Ordering | Jobs run in parallel by default | Steps run in order by default |
| Dependencies | `needs` | Order in the `steps` list |
| Data sharing | Use outputs/artifacts for cross-job data | Share workspace; pass outputs via `$GITHUB_OUTPUT` |
| Failure impact | Dependent jobs are normally skipped | Later steps are normally skipped after failure |

Each job runs in its own runner environment. Do not assume that files or shell state created in one job automatically exist in another job.

## Basic structure

```yaml
name: Jobs and Steps Demo

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  validate:
    name: Validate repository
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Print start message
        run: echo "Starting validation"

      - name: Show runner OS
        run: echo "Runner OS: $RUNNER_OS"

      - name: Finish
        run: echo "Validation finished"
```

## Step types

A step normally uses one of these fields:

- `run`: executes shell commands.
- `uses`: invokes an action.
- `with`: supplies inputs to an action.
- `id`: gives a step an identifier for referencing its outputs.
- `if`: controls whether the step runs.
- `env`: sets environment variables for that step.
- `working-directory`: selects a directory for shell commands.
- `timeout-minutes`: limits the step's runtime.

A step should normally use `run` or `uses`, not both.

## Job dependencies

Jobs without dependencies may run in parallel. Use `needs` when one job must wait for another:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Build"

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Test after build"
```

A job that depends on a failed or skipped job is skipped by default. Use status-check functions such as `always()` or `failure()` only when their behavior is intentional.

## Step outputs

Use a step `id` and write output values to `$GITHUB_OUTPUT`:

```yaml
- name: Create build label
  id: metadata
  run: echo "label=dev-build" >> "$GITHUB_OUTPUT"

- name: Read build label
  env:
    BUILD_LABEL: ${{ steps.metadata.outputs.label }}
  run: echo "Build label: $BUILD_LABEL"
```

For cross-job outputs, declare the output under the producing job and access it with `needs.<job_id>.outputs.<name>`. Use artifacts for files that must be transferred between jobs.

## Conditions and environment

```yaml
- name: Run only on main
  if: ${{ github.ref == 'refs/heads/main' }}
  run: echo "Main branch"

- name: Show configured environment variable
  env:
    GREETING: Hello
  run: echo "$GREETING"
```

Prefer passing context values through `env` when appropriate, especially when values may contain special characters. Treat user-controlled event data as untrusted input and avoid inserting it directly into shell commands.

## Failure handling

- By default, a failing `run` command fails the step and usually prevents subsequent steps from running.
- `continue-on-error: true` can allow the workflow to continue, but the failure should still be visible and handled deliberately.
- `if: ${{ failure() }}` can run a diagnostic step after a failure.
- `timeout-minutes` helps prevent hung jobs or steps from running indefinitely.

## Good practices

1. Give jobs and steps descriptive names.
2. Keep each step focused on one task.
3. Set least-privilege workflow or job permissions.
4. Use explicit job dependencies rather than relying on timing.
5. Transfer data across jobs using outputs or artifacts.
6. Set sensible timeouts.
7. Never print secrets or place them in workflow logs.
8. Review third-party actions and pin them to full commit SHAs where supply-chain assurance requires it.

## Further reading

- [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Contexts reference](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts)
- [Secure use reference](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
