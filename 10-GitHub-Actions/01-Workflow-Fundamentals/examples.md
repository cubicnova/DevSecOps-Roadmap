# Workflow Fundamentals - Examples

Examples are intended for a learning repository. Add each YAML example as a separate file under `.github/workflows/` to run it.

## 1. Minimal workflow

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
      - name: Display greeting
        run: echo "Hello, GitHub Actions!"
```

Run manually from **Actions → Hello Workflow → Run workflow**.

## 2. Run on pushes and pull requests

```yaml
name: Basic CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  inspect:
    runs-on: ubuntu-latest
    steps:
      - name: Show repository and commit
        run: |
          echo "Repository: $GITHUB_REPOSITORY"
          echo "Commit: $GITHUB_SHA"
          echo "Ref: $GITHUB_REF"
```

## 3. Checkout and inspect files

```yaml
name: Repository Inspection

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  inspect:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout source
        uses: actions/checkout@v4

      - name: List tracked workspace files
        run: |
          pwd
          ls -la
          git status --short
```

## 4. Multiple steps in one job

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
        run: echo "First step"

      - name: Step two
        run: echo "Second step runs after step one"

      - name: Verify shell
        run: |
          echo "Runner OS: $RUNNER_OS"
          bash --version | head -n 1
```

Each `run` step starts a separate process. Environment changes made inside one step do not automatically persist to the next step.

## 5. Two jobs with a dependency

```yaml
name: Job Dependency Demo

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Build completed"

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Tests run after build succeeds"
```

## 6. Conditional step

```yaml
name: Conditional Step

on:
  workflow_dispatch:
    inputs:
      run_extra:
        description: Run the optional step
        type: boolean
        default: false
        required: true

permissions:
  contents: read

jobs:
  demo:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Always runs"

      - name: Optional step
        if: ${{ inputs.run_extra }}
        run: echo "The optional step was requested"
```

## 7. Least-privilege token permissions

```yaml
name: Read-only Workflow

on:
  pull_request:

permissions:
  contents: read

jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Add non-destructive validation here"
```

If a workflow must publish a release or write to the repository, grant only the additional permissions it needs at the narrowest appropriate scope.
