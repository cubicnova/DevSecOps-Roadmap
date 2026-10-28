# Reusable Workflows - Examples

Save reusable workflow definitions directly under `.github/workflows/`. Caller workflows can be stored there too. These examples use the same repository unless a cross-repository example is explicitly shown.

## 1. Minimal reusable workflow

File: `.github/workflows/reusable-hello.yml`

```yaml
name: Reusable Hello

on:
  workflow_call:

permissions:
  contents: read

jobs:
  hello:
    runs-on: ubuntu-latest
    steps:
      - name: Greeting
        run: echo "Hello from a reusable workflow"
```

Caller file: `.github/workflows/call-hello.yml`

```yaml
name: Call Reusable Hello

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  call-hello:
    uses: ./.github/workflows/reusable-hello.yml
```

## 2. Reusable workflow with typed inputs

File: `.github/workflows/reusable-check.yml`

```yaml
name: Reusable Check

on:
  workflow_call:
    inputs:
      project_name:
        description: Name shown in the log
        required: true
        type: string
      run_extra:
        description: Whether to run the optional check
        required: false
        default: false
        type: boolean

permissions:
  contents: read

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - name: Print project name
        env:
          PROJECT_NAME: ${{ inputs.project_name }}
        run: echo "Checking $PROJECT_NAME"

      - name: Optional check
        if: ${{ inputs.run_extra }}
        run: echo "Optional check enabled"
```

Caller:

```yaml
name: Call Reusable Check

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  check:
    uses: ./.github/workflows/reusable-check.yml
    with:
      project_name: "sample-app"
      run_extra: true
```

## 3. Pass a named secret

Reusable file: `.github/workflows/reusable-deploy.yml`

```yaml
name: Reusable Deployment Example

on:
  workflow_call:
    secrets:
      deployment_token:
        description: Token needed by a deployment command
        required: true

permissions:
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Confirm token was provided without printing it
        env:
          DEPLOYMENT_TOKEN: ${{ secrets.deployment_token }}
        run: |
          if [ -z "$DEPLOYMENT_TOKEN" ]; then
            echo "Deployment token is missing"
            exit 1
          fi
          echo "Deployment token is available"
```

Caller:

```yaml
name: Call Reusable Deployment

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  deploy:
    uses: ./.github/workflows/reusable-deploy.yml
    secrets:
      deployment_token: ${{ secrets.DEPLOYMENT_TOKEN }}
```

Create `DEPLOYMENT_TOKEN` in repository Actions secrets before running the caller. The sample only checks that a value exists; it does not deploy anything.

## 4. Expose an output

Reusable file: `.github/workflows/reusable-metadata.yml`

```yaml
name: Reusable Metadata

on:
  workflow_call:
    outputs:
      build_label:
        description: Label produced by the workflow
        value: ${{ jobs.prepare.outputs.build_label }}

permissions:
  contents: read

jobs:
  prepare:
    runs-on: ubuntu-latest
    outputs:
      build_label: ${{ steps.label.outputs.value }}
    steps:
      - id: label
        run: echo "value=sample-build" >> "$GITHUB_OUTPUT"
```

Caller:

```yaml
name: Consume Reusable Output

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  prepare:
    uses: ./.github/workflows/reusable-metadata.yml

  report:
    needs: prepare
    runs-on: ubuntu-latest
    steps:
      - name: Print output
        env:
          BUILD_LABEL: ${{ needs.prepare.outputs.build_label }}
        run: echo "Build label: $BUILD_LABEL"
```

## 5. Matrix calling a reusable workflow

```yaml
name: Reusable Workflow Matrix

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  validate:
    strategy:
      matrix:
        target: [dev, staging]
    uses: ./.github/workflows/reusable-target-check.yml
    with:
      target: ${{ matrix.target }}
```

The called workflow must declare a string input named `target` under `workflow_call`.

## 6. Call a reusable workflow from another repository

```yaml
jobs:
  shared-check:
    uses: cubicnova/DevSecOps-Roadmap/.github/workflows/reusable-check.yml@<FULL_COMMIT_SHA>
    with:
      project_name: "sample-app"
    permissions:
      contents: read
```

Replace `<FULL_COMMIT_SHA>` with an actual reviewed commit SHA and ensure the target file exists at that path and is accessible to the caller. The referenced workflow must declare the inputs shown. Avoid using a made-up SHA.

## 7. Explicit secrets vs inherited secrets

Explicit passing:

```yaml
jobs:
  call-workflow:
    uses: ./.github/workflows/reusable-deploy.yml
    secrets:
      deployment_token: ${{ secrets.DEPLOYMENT_TOKEN }}
```

In supported contexts, inheritance can be used:

```yaml
jobs:
  call-workflow:
    uses: ./.github/workflows/reusable-workflow.yml
    secrets: inherit
```

Inheritance passes all secrets available to the caller, so use it only when that broader access is appropriate.
