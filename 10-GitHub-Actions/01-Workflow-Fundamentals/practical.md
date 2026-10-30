# Workflow Fundamentals - Practical Exercises

Complete these exercises in a test repository. Do not add production credentials or sensitive data.

## Lab 1: Create your first workflow

**Goal:** Create a manually triggered workflow.

1. Create `.github/workflows/hello.yml`.
2. Add a workflow named `Hello Workflow`.
3. Add a `workflow_dispatch` trigger.
4. Create a job named `greet` on `ubuntu-latest`.
5. Add a step that prints your preferred greeting.
6. Commit and push the file, then run it from the Actions tab.

**Evidence:** Workflow YAML and a successful run.

## Lab 2: Add event triggers

1. Configure a workflow to run on pushes to `main`.
2. Add a `pull_request` trigger targeting `main`.
3. Make a small change on a feature branch and open a pull request.
4. Confirm which event started each run.

**Questions:** What is the difference between `push` and `pull_request`? Why might a branch filter prevent a run?

## Lab 3: Inspect the runner

1. Check out the repository using `actions/checkout`.
2. Print `$RUNNER_OS`, `$GITHUB_REPOSITORY`, and `$GITHUB_SHA`.
3. List the files in the workspace.
4. Explain why a checkout step is needed before reading repository files.

## Lab 4: Understand job ordering

1. Create `build` and `test` jobs.
2. Run them without a dependency and observe their execution.
3. Add `needs: build` to the `test` job.
4. Observe the updated order.
5. Explain what happens to `test` if `build` fails.

## Lab 5: Use a condition

1. Add a boolean `workflow_dispatch` input named `run_extra`.
2. Add a step that runs only when the input is `true`.
3. Run the workflow once with `false` and once with `true`.
4. Record the result of each run.

## Lab 6: Review permissions

1. Set workflow-level `permissions: contents: read`.
2. Identify which steps need repository access.
3. Explain why broad write permissions are not a good default.
4. If a task requires writes, document the exact permission needed before adding it.

## Lab 7: Troubleshoot intentionally broken YAML

In a disposable branch, introduce one issue at a time:

- Incorrect indentation under `jobs`.
- A workflow file outside `.github/workflows/`.
- A branch filter that does not match your branch.
- A step with neither `run` nor `uses`.

For each issue, note the symptom, inspect the Actions run or workflow validation feedback, fix it, and rerun.

## Lab 8: Workflow security review

Review a sample workflow and answer:

- Does it request more `GITHUB_TOKEN` permissions than necessary?
- Are actions referenced with a reviewed version or SHA?
- Could an untrusted pull request access secrets?
- Are secrets printed or copied into artifacts?
- Is `pull_request_target` used? If yes, is untrusted code executed with privileged access?

## Completion checklist

- [ ] Workflow is in `.github/workflows/`.
- [ ] Triggers behave as expected.
- [ ] Job and step ordering is understood.
- [ ] Permissions follow least privilege.
- [ ] No credentials are committed.
- [ ] At least one successful run is documented.
