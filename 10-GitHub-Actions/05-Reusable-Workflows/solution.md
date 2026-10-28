# Reusable Workflows - Solutions and Explanations

Use these reference solutions to check your exercises. Adjust file names to match your repository.

## Lab 1: Minimal reusable workflow

Reusable file: `.github/workflows/reusable-hello.yml`

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
        run: echo "Hello from the reusable workflow"
```

Caller file: `.github/workflows/call-hello.yml`

```yaml
name: Call Reusable Hello

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  hello:
    uses: ./.github/workflows/reusable-hello.yml
```

The reusable workflow must be directly under `.github/workflows/`. The caller invokes it at the job level, not inside a step.

## Lab 2: Typed inputs

Reusable workflow:

```yaml
name: Reusable Project Check

on:
  workflow_call:
    inputs:
      project_name:
        required: true
        type: string
      run_extra:
        required: false
        type: boolean
        default: false

permissions:
  contents: read

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - name: Show project
        env:
          PROJECT_NAME: ${{ inputs.project_name }}
        run: echo "Project: $PROJECT_NAME"

      - name: Optional check
        if: ${{ inputs.run_extra }}
        run: echo "Extra check enabled"
```

Caller job:

```yaml
jobs:
  check:
    uses: ./.github/workflows/reusable-project-check.yml
    with:
      project_name: "sample-app"
      run_extra: true
```

Input values must match the declared `string`, `number`, or `boolean` type.

## Lab 3: Named secret

Reusable workflow:

```yaml
on:
  workflow_call:
    secrets:
      demo_token:
        required: true

permissions:
  contents: read

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - name: Verify token exists
        env:
          DEMO_TOKEN: ${{ secrets.demo_token }}
        run: |
          if [ -z "$DEMO_TOKEN" ]; then
            echo "Token is missing"
            exit 1
          fi
          echo "Token is configured"
```

Caller:

```yaml
jobs:
  check:
    uses: ./.github/workflows/reusable-secret-check.yml
    secrets:
      demo_token: ${{ secrets.DEMO_TOKEN }}
```

The caller maps its `DEMO_TOKEN` secret to the name expected by the reusable workflow. The token is never printed.

## Lab 4: Workflow output

Reusable workflow:

```yaml
name: Reusable Output

on:
  workflow_call:
    outputs:
      result_label:
        description: Result label
        value: ${{ jobs.prepare.outputs.result_label }}

permissions:
  contents: read

jobs:
  prepare:
    runs-on: ubuntu-latest
    outputs:
      result_label: ${{ steps.make.outputs.value }}
    steps:
      - id: make
        run: echo "value=check-passed" >> "$GITHUB_OUTPUT"
```

Caller:

```yaml
jobs:
  prepare:
    uses: ./.github/workflows/reusable-output.yml

  report:
    needs: prepare
    runs-on: ubuntu-latest
    steps:
      - env:
          RESULT_LABEL: ${{ needs.prepare.outputs.result_label }}
        run: echo "Result: $RESULT_LABEL"
```

The output is mapped from step to job to reusable workflow, then read from the caller's `needs` context.

## Lab 5: Matrix

Reusable workflow must define the `target` input:

```yaml
on:
  workflow_call:
    inputs:
      target:
        required: true
        type: string

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - env:
          TARGET: ${{ inputs.target }}
        run: echo "Validating target $TARGET"
```

Caller:

```yaml
jobs:
  validate:
    strategy:
      matrix:
        target: [dev, staging, test]
    uses: ./.github/workflows/reusable-target-check.yml
    with:
      target: ${{ matrix.target }}
```

The matrix creates a job invocation for each target value.

## Lab 6: Cross-repository calls

The caller's `uses` value generally follows this structure:

```yaml
jobs:
  shared:
    uses: OWNER/REPOSITORY/.github/workflows/FILE.yml@REF
```

Replace each placeholder with a real repository, workflow filename, and ref. Ensure repository access policies allow the caller. For stronger stability and integrity, use a reviewed full commit SHA instead of a moving branch reference.

## Lab 7: Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Workflow cannot be called | Missing `workflow_call` trigger | Add `on.workflow_call` |
| Workflow file not found | File is not directly under `.github/workflows/` or path is wrong | Correct location and reference |
| Invalid input | Missing required input, wrong name, or wrong type | Match the declared input contract |
| Secret error | Secret name mismatch or required secret not passed | Align the caller mapping and reusable declaration |
| Cross-repository access error | Repository policy or reference prevents access | Check workflow access settings and ref |
| Permission validation failure | Called workflow attempts to elevate permissions | Reduce required permissions or grant needed permissions to the caller, if appropriate |

## Lab 8: Security answer guide

Prefer explicit secret mapping over broad inheritance when practical. Never log secrets. Validate user-controlled inputs before passing them to shell commands. Use minimal token permissions, review shared workflows as supply-chain dependencies, and pin cross-repository references to reviewed commit SHAs for high-assurance use. Permissions in a nested reusable workflow chain can be maintained or reduced, not elevated.

## Suggested grading rubric

| Area | Points |
|---|---:|
| Reusable workflow definition and caller | 20 |
| Typed inputs | 15 |
| Secret handling | 15 |
| Workflow outputs | 15 |
| Matrix usage | 10 |
| Cross-repository reuse | 10 |
| Troubleshooting and security review | 15 |
| **Total** | **100** |
