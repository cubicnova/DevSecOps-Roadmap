# GitLab CI/CD YAML — Practical Exercises

## Prerequisites
- A GitLab project where you can commit `.gitlab-ci.yml`.
- A GitLab Runner available to the project, or access to GitLab-hosted runners.
- Basic Git and YAML knowledge.
- A sample project with no production credentials.

## Lab 1: Create your first pipeline
1. Add `.gitlab-ci.yml` at the repository root.
2. Define one `test` stage and one job with a simple `echo` command.
3. Commit and push the file.
4. Open **Build → Pipelines** and inspect the run.

**Expected result:** A pipeline is created and the job succeeds.

## Lab 2: Define multiple stages
1. Add `build`, `test`, and `deploy` stages.
2. Create one job in each stage.
3. Commit the changes.
4. Observe the stage order and job execution.

**Expected result:** Stages run in order; jobs within a stage can run concurrently if runners are available.

## Lab 3: Configure an image and runner tags
1. Set a container `image` for a job.
2. Add a runner `tag` that matches a runner available to your project.
3. Run the pipeline.
4. Compare the job result with and without a matching runner tag.

**Expected result:** The job uses the configured execution environment and is scheduled only on a compatible runner.

## Lab 4: Use global and job variables
1. Define `APP_NAME` globally.
2. Define `BUILD_MODE` at job level.
3. Print non-sensitive values in the job log.
4. Move a dummy token into GitLab CI/CD settings rather than YAML.
5. Confirm the token is used without printing its value.

**Expected result:** Variable precedence and safe secret handling are understood.

## Lab 5: Generate and pass artifacts
1. Create a build job that writes a file into `dist/`.
2. Configure `artifacts:paths`.
3. Add a later-stage job that reads the file.
4. Set an artifact expiration.
5. Download the artifact from the GitLab UI.

**Expected result:** Build output is persisted and available to the downstream job.

## Lab 6: Configure cache
1. Create a Python sample project with `requirements.txt`.
2. Set `PIP_CACHE_DIR` inside the project directory.
3. Cache `.cache/pip/` using a branch-specific cache key.
4. Run the pipeline more than once.
5. Compare logs and runtime; do not assume a cache hit is guaranteed.

**Expected result:** You can distinguish dependency caching from artifact transfer.

## Lab 7: Add rules
1. Configure a job to run for merge request pipelines.
2. Add another rule for the default branch.
3. Test a feature branch and the default branch.
4. Inspect which jobs are created.

**Expected result:** Job creation follows the configured conditions.

## Lab 8: Configure workflow rules
1. Add `workflow:rules` to control pipeline creation.
2. Allow merge request pipelines and default-branch pushes.
3. Add a final `when: never` rule.
4. Test a disallowed event.

**Expected result:** Disallowed events do not create a pipeline.

## Lab 9: Use needs for a DAG
1. Create two independent build jobs.
2. Create a test job that needs only the first build.
3. Use `needs:artifacts` to specify whether files should be downloaded.
4. Compare the pipeline graph and execution timing.

**Expected result:** Jobs can start based on explicit dependencies rather than waiting for every job in the previous stage.

## Lab 10: Reuse configuration
1. Create a hidden base job.
2. Use `extends` from two visible jobs.
3. Add a local include file under `ci/`.
4. Validate the merged configuration.
5. Document which settings are inherited and which are overridden.

**Expected result:** Shared configuration reduces duplication while keeping job behavior understandable.

## Lab 11: Manual deployment gate
1. Create a `deploy` stage and a manual job.
2. Associate it with a `staging` environment.
3. Configure protected environment/variables if your project tier supports them.
4. Run the pipeline and trigger the manual job.
5. Explain why `when: manual` is not equivalent to a full authorization policy.

**Expected result:** You can manually control a deployment job and understand the additional controls required for production.

## Lab 12: CI Lint and troubleshooting
1. Introduce a safe YAML indentation error in a branch.
2. Run CI Lint and record the error.
3. Correct it.
4. Introduce an invalid stage name or missing required command.
5. Inspect the validation result and job logs.

**Expected result:** You can distinguish configuration errors from runner and script failures.

## Lab deliverables
- `.gitlab-ci.yml` and any included YAML files.
- Screenshots of successful pipeline stages and DAG.
- Artifact and cache test observations.
- CI Lint validation result.
- A short security review of variables, runners, includes, and artifacts.
