# Jobs and Steps - Examples

Each example is a standalone workflow fragment. For a runnable example, save the complete YAML under `.github/workflows/`.

## 1. Multiple sequential steps

```yaml
name: Sequential Steps

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  demo:
    runs-on: ubuntu-latest
    steps:
      - name: Step one
        run: echo "One"

      - name: Step two
        run: echo "Two"

      - name: Step three
        run: echo "Three"
```

Steps run in the order listed. If a step fails, later steps are generally skipped unless their conditions say otherwise.

## 2. Parallel jobs and a dependent job

```yaml
name: Job Graph

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Lint complete"

  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Unit tests complete"

  package:
    needs: [lint, unit-tests]
    runs-on: ubuntu-latest
    steps:
      - run: echo "Package after both checks pass"
```

`lint` and `unit-tests` can run concurrently. `package` waits for both.

## 3. Step outputs

```yaml
name: Step Outputs

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  output-demo:
    runs-on: ubuntu-latest
    steps:
      - name: Create value
        id: build_info
        run: echo "version=1.2.3" >> "$GITHUB_OUTPUT"

      - name: Use value
        env:
          VERSION: ${{ steps.build_info.outputs.version }}
        run: echo "Building version $VERSION"
```

## 4. Pass an output between jobs

```yaml
name: Job Outputs

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  prepare:
    runs-on: ubuntu-latest
    outputs:
      release_label: ${{ steps.label.outputs.value }}
    steps:
      - id: label
        run: echo "value=learning-release" >> "$GITHUB_OUTPUT"

  publish-message:
    needs: prepare
    runs-on: ubuntu-latest
    steps:
      - name: Read job output
        env:
          LABEL: ${{ needs.prepare.outputs.release_label }}
        run: echo "Prepared label: $LABEL"
```

## 5. Conditional step and diagnostic

```yaml
name: Conditional and Failure Steps

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  demo:
    runs-on: ubuntu-latest
    steps:
      - name: Conditional message
        if: ${{ github.event_name == 'workflow_dispatch' }}
        run: echo "Started manually"

      - name: Intentional failure
        id: fail_demo
        continue-on-error: true
        run: exit 1

      - name: Report failure outcome
        if: ${{ steps.fail_demo.outcome == 'failure' }}
        run: echo "The previous step failed, but the job continued"
```

This example intentionally fails one step. `continue-on-error` lets the job proceed; use it for real tasks only when failure is expected and appropriately reported.

## 6. Working directory and timeout

```yaml
name: Working Directory

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  inspect:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    defaults:
      run:
        shell: bash
    steps:
      - uses: actions/checkout@v4
      - name: List root files
        run: pwd && ls -la
      - name: Inspect a directory
        working-directory: .github
        run: ls -la
```

The working directory must exist before the step starts.

## 7. Run a diagnostic step after failure

```yaml
name: Failure Diagnostics

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  demo:
    runs-on: ubuntu-latest
    steps:
      - name: Simulate a failure
        run: |
          echo "Simulating failure"
          exit 1

      - name: Diagnostic step
        if: ${{ failure() }}
        run: echo "A previous step failed"
```

## 8. Use an environment variable safely

```yaml
name: Environment Variables

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  demo:
    runs-on: ubuntu-latest
    env:
      APP_ENV: learning
    steps:
      - name: Print configured environment
        env:
          MESSAGE: "Hello from workflow"
        run: |
          echo "$MESSAGE"
          echo "Environment: $APP_ENV"
```

Do not use `echo` to print secret values.
