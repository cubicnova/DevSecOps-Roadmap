# 05 - Reusable Workflows

Reusable workflows let you define a workflow once and call it from other workflows. They help teams standardize CI checks, testing, security scans, and deployments without copying the same YAML into every repository.

## Learning objectives

By completing this module, you should be able to:

- Explain reusable workflows and when to use them.
- Define a callable workflow with `on: workflow_call`.
- Call a workflow from a job using `jobs.<job_id>.uses`.
- Declare and pass typed inputs and named secrets.
- Expose outputs from a reusable workflow.
- Use reusable workflows with `needs` and matrix strategies.
- Apply access control, version pinning, and least-privilege permissions.

## Reusable workflow vs action

| Reusable workflow | Action |
|---|---|
| Reuses one or more jobs and their steps | Reuses a step-level unit of work |
| Called from a job using `jobs.<job_id>.uses` | Used within a step using `steps[*].uses` |
| Can define jobs, dependencies, runners, and permissions | Usually performs a focused operation inside a job |

## Where reusable workflows live

Reusable workflow files must be stored directly in `.github/workflows/`; nested directories inside that folder are not supported.

A reusable workflow must declare the `workflow_call` event:

```yaml
name: Reusable Validation

on:
  workflow_call:

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Validate
        run: echo "Reusable validation ran"
```

## Calling a workflow in the same repository

A caller invokes a reusable workflow at the job level:

```yaml
name: Call Shared Validation

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  validation:
    uses: ./.github/workflows/reusable-validation.yml
```

A caller job that uses a reusable workflow does not define `runs-on` or `steps` itself; those are defined by the called workflow.

## Inputs

Declare inputs under `on.workflow_call.inputs`. Each input needs a type: `string`, `number`, or `boolean`.

```yaml
on:
  workflow_call:
    inputs:
      environment_name:
        description: Environment label
        required: true
        type: string
```

Read an input in the called workflow with `${{ inputs.environment_name }}` and pass it from the caller with `with:`. The supplied value must match the declared type.

## Secrets

Declare expected secrets under `on.workflow_call.secrets` and pass them by name from the caller. Do not hard-code credentials or print secret values.

```yaml
on:
  workflow_call:
    secrets:
      deploy_token:
        description: Token required by the deployment job
        required: true
```

Caller:

```yaml
jobs:
  deploy:
    uses: ./.github/workflows/deploy.yml
    secrets:
      deploy_token: ${{ secrets.DEPLOY_TOKEN }}
```

`secrets: inherit` can pass all secrets available to the caller in supported repository/organization contexts. Prefer explicitly named secrets when possible because it makes the workflow's dependencies clearer and limits accidental exposure.

## Outputs

A reusable workflow can expose a job output through `on.workflow_call.outputs`, mapping it to a job output in the called workflow. The caller can then read it from `needs.<job_id>.outputs.<output_name>`.

## Dependencies and matrix strategies

A caller can use `needs`, `if`, `strategy`, `with`, `secrets`, and `permissions` on the job that invokes a reusable workflow, subject to GitHub's supported syntax. Matrix strategies can call the same reusable workflow with different inputs.

## Security and maintainability

1. Keep reusable workflows in a trusted repository with controlled write access.
2. Pin cross-repository workflow references to a full commit SHA for stronger integrity.
3. Use a tag or branch only when you have an intentional versioning and update process.
4. Grant the minimum `GITHUB_TOKEN` permissions required.
5. Do not pass secrets unless the called workflow needs them.
6. Remember that nested workflows cannot elevate token permissions beyond those available to the caller.
7. Review caller-controlled inputs and avoid treating them as trusted shell code.
8. Keep workflow names, input names, and output names descriptive.
9. Test changes in a sandbox repository before adopting them across many projects.

## Common mistakes

- Missing `workflow_call`.
- Placing a reusable workflow in a subdirectory under `.github/workflows/`.
- Calling the reusable workflow from a step instead of a job.
- Defining an input without a type.
- Passing an input with the wrong type or name.
- Passing a secret name that is not declared in the called workflow.
- Referencing a file that is not accessible to the caller.
- Assuming the called workflow can increase token permissions.

## Further reading

- [Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
- [Reusable workflow configuration reference](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations)
- [Workflow syntax reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
