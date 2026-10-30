# Reusable Workflows - Practical Exercises

Complete the exercises in a test repository. Use harmless sample values and do not place real credentials in source files.

## Lab 1: Build a minimal reusable workflow

1. Create `.github/workflows/reusable-hello.yml`.
2. Add `on: workflow_call`.
3. Add one job and one named step.
4. Create a separate caller workflow triggered by `workflow_dispatch`.
5. Call the reusable workflow from a job using `uses`.
6. Run the caller and inspect the run details.

**Deliverable:** Both YAML files and a screenshot or notes from a successful run.

## Lab 2: Add typed inputs

1. Add a required string input named `project_name`.
2. Add an optional boolean input named `run_extra` with a default.
3. Use both inputs in the called workflow.
4. Pass values through the caller's `with` block.
5. Test the optional step with both `true` and `false`.
6. Try passing a value of the wrong type and note the validation result.

## Lab 3: Pass a named secret safely

1. Declare an optional or required secret in `workflow_call`.
2. Add a repository Actions secret in GitHub settings.
3. Pass the secret from the caller by name.
4. Check whether the value is present without printing it.
5. Explain why printing or committing a secret is unsafe.

Do not use a real production credential in this exercise.

## Lab 4: Return a workflow output

1. Create a step output using `$GITHUB_OUTPUT`.
2. Map it to a job output.
3. Expose it under `on.workflow_call.outputs`.
4. Call the workflow from a caller job.
5. Add a dependent job using `needs.<job_id>.outputs.<name>`.

## Lab 5: Use a matrix

1. Create a reusable workflow with a required string input called `target`.
2. Call it using a matrix with `dev`, `staging`, and `test`.
3. Display the target from the called workflow.
4. Verify that separate matrix combinations are represented in the run.

## Lab 6: Reuse a workflow across repositories

1. Create a reusable workflow in a dedicated test repository.
2. Configure access so the caller can use it.
3. Reference it from another test repository with `owner/repo/.github/workflows/file.yml@ref`.
4. Confirm the referenced ref exists and the file is accessible.
5. For a high-assurance setup, use a reviewed full commit SHA.

## Lab 7: Debug common failures

Cause and fix one issue at a time:

- Remove `workflow_call`.
- Move the reusable workflow into a nested directory under `.github/workflows/`.
- Omit a required input.
- Pass a secret under the wrong name.
- Reference a missing file or inaccessible repository.
- Ask the called workflow for broader token permissions than the caller allows.

Record the error or behavior and the fix for each.

## Lab 8: Security review

Review your caller and reusable workflows:

- [ ] Only necessary secrets are passed.
- [ ] Secrets are never printed.
- [ ] Inputs are validated before being used in commands.
- [ ] Token permissions are minimal.
- [ ] Cross-repository workflow references are pinned or versioned deliberately.
- [ ] Called workflows are reviewed and accessible only as intended.
- [ ] Nested workflows do not rely on permission escalation.
- [ ] Deployment workflows have appropriate approval and environment controls.

## Completion checklist

- [ ] Can define and call a reusable workflow.
- [ ] Can pass typed inputs and named secrets.
- [ ] Can expose and consume outputs.
- [ ] Can call a workflow using a matrix.
- [ ] Can explain cross-repository access and versioning.
- [ ] Can troubleshoot common configuration errors.
