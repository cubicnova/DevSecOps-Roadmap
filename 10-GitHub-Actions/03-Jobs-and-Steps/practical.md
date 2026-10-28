# Jobs and Steps - Practical Exercises

Perform these labs in a test repository. Use non-sensitive sample data only.

## Lab 1: Create a multi-step job

1. Create `.github/workflows/multi-step.yml`.
2. Add a manually triggered workflow.
3. Create one job with at least four named steps.
4. Print a message and runner information.
5. Run the workflow and verify the order in the logs.

**Deliverable:** YAML file and a brief note explaining step order.

## Lab 2: Compare parallel and sequential jobs

1. Create `lint` and `test` jobs with no dependencies.
2. Observe the job graph in the Actions run.
3. Add a `package` job with `needs: [lint, test]`.
4. Confirm that packaging waits for both checks.
5. Intentionally fail one prerequisite in a test branch and record what happens to `package`.

## Lab 3: Generate and consume a step output

1. Create a step with `id: metadata`.
2. Write a value such as `build_name=practice-build` to `$GITHUB_OUTPUT`.
3. Read it in the next step using `steps.metadata.outputs.build_name`.
4. Pass the value through an environment variable before using it in a shell command.
5. Verify the output in the logs.

## Lab 4: Share output across jobs

1. Create a `prepare` job that defines a step output.
2. Expose it using `jobs.prepare.outputs`.
3. Create a second job with `needs: prepare`.
4. Read the value with `needs.prepare.outputs.<name>`.
5. Explain why the jobs do not share the same filesystem automatically.

## Lab 5: Add conditions

1. Add a step that runs only on `main`.
2. Add another step that runs only if a previous step fails.
3. Test the workflow on a feature branch and on `main` if available.
4. Explain the difference between a condition on a job and a condition on a step.

## Lab 6: Configure timeouts and working directories

1. Set `timeout-minutes` on a job.
2. Set a job-level default shell.
3. Set a step's `working-directory`.
4. Verify that the directory exists before using it.
5. Explain when a timeout is useful.

## Lab 7: Handle a non-critical failure

1. Create a step that exits with a non-zero code.
2. Add `continue-on-error: true`.
3. Add a following step that checks `steps.<id>.outcome`.
4. Record the difference between `outcome` and `conclusion`.
5. Explain why continuing after a failure should be intentional.

## Lab 8: Security review

Review your workflow and check:

- [ ] `GITHUB_TOKEN` permissions are minimal.
- [ ] No secrets are printed or committed.
- [ ] User-controlled values are not interpolated directly into shell scripts.
- [ ] Job dependencies are explicit.
- [ ] Timeouts are reasonable.
- [ ] External actions are reviewed and versioned.
- [ ] Cross-job files use artifacts or another explicit transfer mechanism.

## Completion checklist

- [ ] Can explain jobs versus steps.
- [ ] Can configure `needs` dependencies.
- [ ] Can use step and job outputs.
- [ ] Can use `if` and failure status functions.
- [ ] Can configure a working directory and timeout.
- [ ] Can explain basic workflow security concerns.
