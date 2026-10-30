# Jobs and Steps - Solutions and Explanations

These are reference solutions. Run them in a disposable repository and compare your observations with the expected behavior.

## Lab 1: Multi-step job

```yaml
name: Multi-step Demo

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  demo:
    runs-on: ubuntu-latest
    steps:
      - name: Start
        run: echo "Starting"
      - name: Runner details
        run: echo "OS=$RUNNER_OS"
      - name: Current directory
        run: pwd
      - name: Finish
        run: echo "Finished"
```

Expected: steps appear in the listed order. Each `run` step executes in its own process, so a shell variable created in one step does not automatically persist to another.

## Lab 2: Parallel and sequential jobs

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Lint"

  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Test"

  package:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - run: echo "Package"
```

`lint` and `test` can run in parallel. `package` waits for both to finish successfully. If either dependency fails, `package` is skipped by default.

## Lab 3: Step output

```yaml
- name: Create metadata
  id: metadata
  run: echo "build_name=practice-build" >> "$GITHUB_OUTPUT"

- name: Use metadata
  env:
    BUILD_NAME: ${{ steps.metadata.outputs.build_name }}
  run: echo "Build name: $BUILD_NAME"
```

The `id` gives the step a stable identifier. `$GITHUB_OUTPUT` is the supported file for setting step outputs. The later step reads the value from the `steps` context.

## Lab 4: Cross-job output

```yaml
jobs:
  prepare:
    runs-on: ubuntu-latest
    outputs:
      build_name: ${{ steps.meta.outputs.build_name }}
    steps:
      - id: meta
        run: echo "build_name=practice-build" >> "$GITHUB_OUTPUT"

  consume:
    needs: prepare
    runs-on: ubuntu-latest
    steps:
      - env:
          BUILD_NAME: ${{ needs.prepare.outputs.build_name }}
        run: echo "Build name: $BUILD_NAME"
```

The `outputs` mapping exposes a step output at job level. `needs: prepare` establishes the dependency and makes that job's outputs available. Files do not automatically move between separate jobs; use artifacts when you need to transfer files.

## Lab 5: Conditions

```yaml
- name: Main branch only
  if: ${{ github.ref == 'refs/heads/main' }}
  run: echo "This is main"

- name: Report previous failure
  if: ${{ failure() }}
  run: echo "A prior step failed"
```

A job-level `if` determines whether the whole job is eligible to run. A step-level `if` determines whether that step runs inside an otherwise running job.

## Lab 6: Timeouts and working directory

```yaml
jobs:
  inspect:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    defaults:
      run:
        shell: bash
    steps:
      - uses: actions/checkout@v4
      - name: Inspect configuration
        working-directory: .github
        timeout-minutes: 1
        run: ls -la
```

The `.github` directory must exist in the checked-out repository. A job timeout bounds the total job runtime; a step timeout bounds an individual step.

## Lab 7: Continue after an expected failure

```yaml
- name: Optional check
  id: optional_check
  continue-on-error: true
  run: exit 1

- name: Report result
  if: ${{ steps.optional_check.outcome == 'failure' }}
  run: echo "Optional check failed; review the result"
```

- `outcome` reports the step result before `continue-on-error` is applied.
- `conclusion` reports the result after that behavior is applied; it can be `success` when a failed step was allowed to continue.

Do not hide failures in mandatory security or quality checks.

## Common troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| Dependent job is skipped | An upstream dependency failed or was skipped | Inspect the `needs` job results |
| Output is empty | Missing or incorrect `id`, output name, or `$GITHUB_OUTPUT` syntax | Compare names and check the producing step's log |
| Variable missing in next step | Shell state does not persist across steps | Use `$GITHUB_OUTPUT`, `$GITHUB_ENV`, or workflow-level `env` appropriately |
| Working directory error | Directory does not exist in the workspace | Check out the repository and verify the path |
| Later steps skipped | Earlier step failed | Fix the cause or use a deliberate condition |
| Workflow runs too long | No timeout or a command is waiting indefinitely | Set a sensible timeout and diagnose the command |

## Security answer guide

Use minimal token permissions, avoid printing secrets, and treat event-derived values as untrusted. Pass values through environment variables where appropriate rather than constructing shell code from untrusted strings. Review external actions and avoid granting secrets or write permissions to jobs that execute untrusted code.

## Suggested grading rubric

| Area | Points |
|---|---:|
| Job and step structure | 15 |
| Parallelism and `needs` | 15 |
| Step outputs | 15 |
| Cross-job outputs | 15 |
| Conditions and failure behavior | 15 |
| Timeouts and working directories | 10 |
| Security review | 15 |
| **Total** | **100** |
