# Practical Exercises — Matrix Strategies

## Lab prerequisites
- A GitHub repository where you can run Actions.
- A small project with tests, or a workflow that prints runtime information.
- No production secrets are required for these exercises.

## Exercise 1: Build a basic matrix
Create a workflow that tests two runtime versions on Ubuntu. Use `matrix` values in the setup action and print the active version.

**Deliverable:** Workflow YAML and a successful run with two matrix jobs.

## Exercise 2: Cross-platform testing
Expand the matrix to run on Ubuntu and Windows with two runtime versions.

**Task:** Calculate the expected number of jobs before running it.

**Deliverable:** Workflow, calculation, and actual job count.

## Exercise 3: Exclude unsupported combinations
Add a third runtime version and exclude one OS/runtime pair.

**Task:** Calculate the job count before and after the exclusion.

**Deliverable:** Updated YAML and explanation of why the combination is unsupported.

## Exercise 4: Use include to add metadata
Add a `coverage` or `experimental` value to selected combinations. Print the value from a step using an environment variable.

**Deliverable:** Matrix configuration and run log demonstrating the metadata.

## Exercise 5: Compare fail-fast behavior
Run a small matrix with `fail-fast: true`, then with `fail-fast: false`. Introduce a controlled, harmless failure in one configuration.

**Deliverable:** A comparison of which jobs complete or are cancelled. Restore the workflow after testing.

## Exercise 6: Test an experimental version
Add an experimental runtime using `include` and allow only that combination to fail without failing the entire workflow.

**Deliverable:** Workflow and explanation of how `continue-on-error` differs from `fail-fast`.

## Exercise 7: Limit concurrency
Configure at least six combinations and set `max-parallel: 2`.

**Deliverable:** YAML and evidence or explanation showing that no more than two matrix jobs run concurrently.

## Exercise 8: Avoid artifact collisions
Make every matrix job create a small report and upload it. Include OS and runtime in the artifact name.

**Deliverable:** Workflow and artifact list showing unique names.

## Exercise 9: Create a dynamic matrix
Create one job that writes a small JSON matrix to `$GITHUB_OUTPUT`. Use `fromJSON` in a dependent job.

**Deliverable:** Both jobs, the JSON output, and a note describing how you would validate external input.

## Exercise 10: Optimize a large matrix
Design a matrix with three dimensions. Calculate its size, identify combinations that do not need to run, and propose exclusions or separate workflows. Keep the final matrix within GitHub's documented limit.

**Deliverable:** Before-and-after job counts and rationale.

## Completion checklist
- [ ] Job counts are calculated correctly.
- [ ] `matrix` values are used in steps or runner selection.
- [ ] `include` and `exclude` behavior is understood.
- [ ] `fail-fast` and `continue-on-error` are distinguished.
- [ ] `max-parallel` is configured when useful.
- [ ] Artifacts have unique names.
- [ ] Dynamic matrix values are trusted, validated, and bounded.
