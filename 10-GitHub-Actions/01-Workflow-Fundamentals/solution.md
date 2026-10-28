# Workflow Fundamentals - Solutions and Explanations

Use these solutions to verify your work. Adapt branch names and repository details to your environment.

## Lab 1: First workflow

Create `.github/workflows/hello.yml`:

```yaml
name: Hello Workflow

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - name: Print greeting
        run: echo "Hello from my first GitHub Actions workflow!"
```

Commit and push the file. Open **Actions**, select **Hello Workflow**, and choose **Run workflow**.

## Lab 2: Event triggers

```yaml
name: Trigger Demo

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Triggered by $GITHUB_EVENT_NAME"
```

- `push` runs for commits pushed to a matching branch.
- `pull_request` runs for matching pull-request activity and target branches.
- A branch filter limits which branch names qualify. Check the event payload and target branch if no run starts.

## Lab 3: Runner inspection

```yaml
name: Runner Inspection

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  inspect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Print runner details
        run: |
          echo "OS: $RUNNER_OS"
          echo "Repository: $GITHUB_REPOSITORY"
          echo "Commit: $GITHUB_SHA"
          ls -la
```

Checkout makes the repository's source available in the runner workspace. Without it, the workspace generally does not contain the repository files.

## Lab 4: Job ordering

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
      - run: echo "Test"
```

Jobs without dependencies can run in parallel. With `needs: build`, `test` waits for `build`; if `build` fails or is skipped, `test` is skipped by default unless a suitable condition changes that behavior.

## Lab 5: Conditional step

```yaml
name: Conditional Demo

on:
  workflow_dispatch:
    inputs:
      run_extra:
        type: boolean
        description: Run the optional step
        default: false
        required: true

permissions:
  contents: read

jobs:
  demo:
    runs-on: ubuntu-latest
    steps:
      - run: echo "This always runs"
      - name: Optional step
        if: ${{ inputs.run_extra }}
        run: echo "This runs only when run_extra is true"
```

When the input is false, the optional step is skipped. When true, it runs.

## Lab 6: Permissions

A reasonable starting point for a read-only validation workflow is:

```yaml
permissions:
  contents: read
```

If all permissions are set explicitly, unspecified permissions are set to `none`. Add a narrowly scoped permission only when a documented workflow operation requires it. For example, creating an issue may require `issues: write`; do not grant it to unrelated jobs.

## Lab 7: Troubleshooting guide

| Problem | Check / fix |
|---|---|
| YAML parse error | Correct indentation and key placement |
| Workflow does not appear | Confirm file is committed under `.github/workflows/` on the relevant ref |
| No run on push | Check event type and branch filters |
| Job does not start | Check `needs`, `if`, and upstream job status |
| Step fails | Open the step log and inspect command exit status |
| Permission denied | Identify the API or operation and grant only the required token permission |

## Lab 8: Security review answer guide

A sound baseline uses minimal token permissions, reviewed and versioned action references, no hard-coded secrets, and no privileged secrets in jobs that execute untrusted code. Treat third-party actions as code dependencies and review their source and maintenance status. Avoid running pull-request-controlled scripts in privileged `pull_request_target` workflows.

## Suggested grading rubric

| Area | Points |
|---|---:|
| Workflow structure and YAML correctness | 20 |
| Correct trigger behavior | 15 |
| Jobs, runners, and steps explained | 15 |
| Job dependencies and conditions | 15 |
| Least-privilege permissions | 15 |
| Troubleshooting evidence | 10 |
| Security review | 10 |
| **Total** | **100** |
