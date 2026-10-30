# CI/CD Concepts — Practical Exercises

Complete these exercises in a personal learning repository. Do not connect the practice workflow to production systems or use real secrets.

## Lab setup

Requirements: Git, Python 3.10+, and a GitHub account for the optional hosted workflow.

```bash
mkdir ci-cd-concepts-lab
cd ci-cd-concepts-lab
git init
```

Add the `app.py` and `test_app.py` examples from `examples.md`.

## Exercises

### Exercise 1 — Explain the terminology
Define CI, Continuous Delivery, and Continuous Deployment in your own words. Give one example of what happens after a successful test run in each model.

**Deliverable:** A short comparison table.

### Exercise 2 — Draw a pipeline
Design a pipeline for a small Python web API with stages for source validation, testing, packaging, staging, and production.

**Deliverable:** A diagram or numbered sequence showing stage order and failure paths.

### Exercise 3 — Run tests locally
Run the sample application and unit tests. Record the commands and results.

```bash
python app.py
python -m unittest -v
```

**Deliverable:** A short test report.

### Exercise 4 — Create a workflow
Create `.github/workflows/ci.yml` using the example in `examples.md`. Push it to a test GitHub repository.

**Deliverable:** A successful workflow run.

### Exercise 5 — Observe a failed quality gate
In a separate branch, change one expected test value so the test fails. Push the branch and observe the workflow.

**Deliverable:** Explain how the failure appears in the Actions tab and why a failed required check should block merging.

### Exercise 6 — Add a linting stage
Add Ruff or another appropriate linter to the pipeline. Pin the tool version in project configuration for repeatability.

**Deliverable:** A workflow with both tests and linting.

### Exercise 7 — Use job dependencies
Create separate `test` and `package` jobs. Configure packaging to depend on successful tests with `needs`.

**Deliverable:** A workflow where packaging does not run if tests fail.

### Exercise 8 — Artifact traceability
Explain how you would associate a package with the exact source revision that produced it.

**Deliverable:** List at least three metadata fields, such as commit SHA, build run ID, version, and image digest.

### Exercise 9 — Secrets handling review
Review a hypothetical workflow that contains `API_KEY = "abc123"` in its YAML file.

**Deliverable:** Explain why this is unsafe and describe how to rotate and store the credential safely. Do not create or use a real credential for this exercise.

### Exercise 10 — Least privilege
Inspect workflow permissions. Set minimum permissions for a workflow that only checks out source and runs tests.

**Deliverable:** Explain why read-only repository contents permission is generally sufficient for this example.

### Exercise 11 — Pull request threat model
A workflow runs code from external pull requests on a self-hosted runner that can access deployment credentials.

**Deliverable:** Identify at least three risks and propose controls.

### Exercise 12 — Release and rollback plan
Design a Continuous Delivery process that deploys to staging, runs smoke tests, requires approval, and then deploys to production.

**Deliverable:** Describe artifact promotion, approval, health checks, and rollback to a known-good release.

## Stretch challenges

- Add a test matrix for two supported Python versions.
- Add dependency vulnerability scanning using a suitable tool.
- Add a workflow concurrency group to cancel obsolete runs for the same branch.
- Add a manual trigger with `workflow_dispatch`.
- Document which jobs need write permissions and remove unnecessary access.

## Submission checklist

- [ ] `app.py` and `test_app.py` run locally.
- [ ] Workflow YAML is stored under `.github/workflows/`.
- [ ] Workflow passes for valid code.
- [ ] A deliberately failing test makes the workflow fail.
- [ ] No credentials are committed.
- [ ] Workflow permissions are minimal.
- [ ] The release plan includes artifact traceability and rollback.
