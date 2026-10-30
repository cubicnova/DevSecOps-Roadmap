# GitLab Pipeline Fundamentals — Practical Exercises

## Lab setup
- A GitLab account and a test project.
- An available GitLab Runner (GitLab-hosted runners may be available depending on project settings and plan).
- Git installed locally.
- A text editor.
- No production credentials or production deployment target are required.

## Exercise 1: Create your first pipeline
**Goal:** Create and execute a minimal pipeline.

1. Create a project named `gitlab-ci-fundamentals-lab`.
2. Add `.gitlab-ci.yml` at the repository root.
3. Add a job named `hello` with a `script` that prints a greeting.
4. Commit and push the file.
5. Open **Build > Pipelines**.
6. Record the pipeline status and job duration.

**Expected result:** One successful pipeline containing one successful job.

## Exercise 2: Define stages
**Goal:** Understand stage sequencing.

Create three stages: `build`, `test`, and `deploy`. Add one job to each stage. Use harmless `echo` commands. Push the changes and observe the order in the pipeline graph.

**Questions**
- Which stage starts first?
- Does the deploy stage start if the test job fails?
- What happens when a job has no `stage` key?

## Exercise 3: Observe parallel execution
**Goal:** Compare jobs in the same stage.

Add two jobs to the `test` stage. Give each a short `sleep` command followed by an `echo`. Observe whether they overlap.

**Questions**
- Why might jobs appear sequential even when they share a stage?
- How do runner concurrency and available runners affect this?

## Exercise 4: Save and inspect an artifact
**Goal:** Preserve job output.

1. Create a `build_output` directory in a job.
2. Write a text file into it.
3. Configure `artifacts: paths` to include the directory.
4. Run the pipeline.
5. Download and inspect the artifact from the job page.

**Expected result:** The output directory is available as a downloadable artifact.

## Exercise 5: Use variables
**Goal:** Configure a job without hard-coding repeated values.

1. Define a non-sensitive variable such as `APP_ENV: "lab"`.
2. Print the variable from a job.
3. Override it at job level.
4. Compare the output.
5. Do not place passwords or tokens in the YAML file.

## Exercise 6: Add conditional execution
**Goal:** Use `rules`.

Create a job that runs on the default branch and a separate job that runs for merge-request pipelines. Create a branch and merge request to test the behavior.

**Expected result:** Jobs are included only when their rules match.

## Exercise 7: Test runner tags
**Goal:** Understand runner selection.

1. Inspect the tags on an available runner.
2. Add a matching tag to a test job.
3. Run the pipeline.
4. Change the job to a tag that no runner has.
5. Observe the pending state, then restore a valid tag.

Do not modify shared or production runner configuration without administrator approval.

## Exercise 8: Troubleshoot a failing job
**Goal:** Read logs and diagnose failure.

1. Add a command that intentionally exits with a non-zero status, such as `exit 1`.
2. Run the pipeline.
3. Open the failed job log.
4. Identify the failing command and exit code.
5. Correct the command and rerun.

## Exercise 9: Validate the configuration
**Goal:** Use GitLab CI Lint.

1. Open the project's CI/CD pipeline editor or CI Lint tool.
2. Paste or select your `.gitlab-ci.yml`.
3. Validate it.
4. Introduce a YAML indentation error and validate again.
5. Fix the error and confirm validation succeeds.

## Submission checklist
- [ ] `.gitlab-ci.yml` committed at the repository root.
- [ ] Pipeline contains build, test, and deploy stages.
- [ ] Two test jobs demonstrate same-stage concurrency.
- [ ] At least one artifact is downloadable.
- [ ] A non-sensitive variable is used.
- [ ] A `rules` condition is demonstrated.
- [ ] Runner tag behavior is documented.
- [ ] One intentional failure was diagnosed and fixed.
- [ ] CI Lint validation succeeded.

## Viva questions
1. What is GitLab CI/CD?
2. What is the purpose of `.gitlab-ci.yml`?
3. Differentiate a pipeline, stage, job, and runner.
4. How are jobs in the same stage scheduled?
5. What happens when a job fails?
6. What is the difference between cache and artifacts?
7. Why are runner tags used?
8. What is the purpose of `rules`?
9. What are predefined CI/CD variables?
10. Why should secrets not be hard-coded in YAML?
