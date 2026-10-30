# GitLab Stages and Jobs — Practical Exercises

## Lab requirements
- GitLab project with an available runner.
- Permission to commit `.gitlab-ci.yml`.
- Git and a text editor.
- Use a test project; do not connect exercises to production deployment credentials.

## Exercise 1: Create a multi-stage pipeline
Create the stages `validate`, `build`, `test`, and `deploy`. Add one job to each stage using harmless `echo` commands.

**Tasks**
1. Commit and push the YAML file.
2. Open the pipeline graph.
3. Record the stage order and job statuses.

**Expected result:** Four stages execute in the configured order.

## Exercise 2: Create parallel jobs
Add three jobs to the `test` stage: `unit_tests`, `lint_checks`, and `security_checks`. Add a short `sleep` command to each job.

**Tasks**
- Observe whether the jobs overlap.
- Repeat with runner concurrency limited to one if you administer a disposable runner.
- Explain why same-stage jobs may still execute sequentially.

## Exercise 3: Use job lifecycle commands
Create a job with `before_script`, `script`, and `after_script`.

**Tasks**
- Add an `echo` command to each section.
- Review the job log.
- Intentionally fail one command in `script` and observe the result.
- Explain whether `after_script` runs after the main script fails.

## Exercise 4: Configure runner tags
Inspect the tags of a runner available to your project. Add those tags to a job.

**Tasks**
1. Run the job with matching tags.
2. Change one tag to a nonexistent tag.
3. Observe the job's pending state.
4. Restore the valid tag.

Do not change shared runner settings without administrator approval.

## Exercise 5: Pass artifacts between stages
Create a build job that writes `output/app.txt` and saves `output/` as an artifact. Create a test job in a later stage that reads the file.

**Expected result:** The test job can read the artifact downloaded from the build job.

## Exercise 6: Restrict artifact downloads
Create two build jobs, each producing a different artifact directory. Add a test job with `dependencies` referencing only one build job.

**Tasks**
- Confirm that only the selected artifact is downloaded.
- Explain why `dependencies` does not replace stage ordering.

## Exercise 7: Configure a non-blocking job
Create a quality-check job that exits with status `1` and set `allow_failure: true`.

**Tasks**
- Run the pipeline.
- Inspect the job and pipeline status.
- Explain when a non-blocking failure is appropriate and when it is dangerous.

## Exercise 8: Build a DAG with needs
Create two independent build jobs and two test jobs. Make each test job depend only on its matching build job using `needs`.

**Tasks**
- Observe the dependency graph.
- Compare the execution with a pipeline that uses stage ordering only.
- Explain how `needs` can reduce waiting time.

## Exercise 9: Immediate lint job
Create a lint job in the `test` stage with `needs: []`. Keep a build job in the `build` stage.

**Expected result:** The lint job can start as soon as the pipeline is created, without waiting for the build job.

## Exercise 10: Optional dependency with rules
Create an optional test job controlled by a variable or branch rule. Make a later job depend on it with `optional: true`.

**Tasks**
- Run with the optional job included.
- Run with it excluded.
- Confirm that the pipeline can be created in both cases.

## Exercise 11: Parallel matrix
Create a matrix job for two application components and two target labels. Confirm that GitLab creates four job instances.

## Exercise 12: Troubleshooting challenge
Diagnose each condition in a test pipeline:
- A job remains pending.
- A job is skipped unexpectedly.
- A downstream job cannot find an artifact.
- Pipeline creation fails because a `needs` target does not exist.
- A test job starts later than expected.

Record the cause, evidence from the UI/logs, and correction.

## Submission checklist
- [ ] Multi-stage pipeline committed.
- [ ] Three jobs in one stage demonstrated.
- [ ] `before_script`, `script`, and `after_script` tested.
- [ ] Runner tags tested.
- [ ] Artifact created and consumed by a later job.
- [ ] `dependencies` behavior demonstrated.
- [ ] `allow_failure` behavior demonstrated.
- [ ] DAG pipeline using `needs` demonstrated.
- [ ] Immediate job using `needs: []` demonstrated.
- [ ] Optional dependency tested with and without its target job.
- [ ] Matrix creates four jobs.
- [ ] Troubleshooting notes submitted.

## Viva questions
1. Differentiate a stage and a job.
2. What is the default stage when `stage` is omitted?
3. Can jobs in the same stage run in parallel?
4. What controls runner job concurrency?
5. What happens when a job fails?
6. What is the purpose of `allow_failure`?
7. Differentiate `dependencies` and `needs`.
8. What is a DAG pipeline?
9. What does `needs: []` do?
10. Why might a job remain pending?
11. How are artifacts passed between stages?
12. What is the purpose of `parallel:matrix`?
