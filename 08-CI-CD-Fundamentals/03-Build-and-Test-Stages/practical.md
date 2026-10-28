# Build and Test Stages — Practical Exercises

Complete the exercises in a personal practice repository. Use synthetic data and do not connect labs to production systems.

## Lab setup

Requirements: Git, Python 3.10+, and GitHub for the optional hosted workflow.

```bash
mkdir build-test-lab
cd build-test-lab
git init
```

Create `calculator.py` and `test_calculator.py` using `examples.md`.

## Exercises

### Exercise 1 — Identify the stages
Describe what happens during checkout, dependency installation, linting, building, unit testing, integration testing, packaging, and artifact upload.

**Deliverable:** A table with stage, purpose, and typical failure.

### Exercise 2 — Run the unit tests
Run:

```bash
python -m unittest -v
```

**Deliverable:** Record the number of tests passed and explain what a non-zero exit code means.

### Exercise 3 — Add test cases
Add tests for adding zero, negative values, decimal values, and division by zero.

**Deliverable:** A test suite that covers normal cases and at least one error case.

### Exercise 4 — Run a build validation
Run:

```bash
python -m compileall -q .
```

**Deliverable:** Explain why successful compilation does not prove that the program is correct.

### Exercise 5 — Create a GitHub Actions workflow
Add the workflow from `examples.md` under `.github/workflows/build-test.yml` and push it to a test repository.

**Deliverable:** A successful workflow run.

### Exercise 6 — Make a test fail intentionally
Change an expected result so it no longer matches the function's output.

**Deliverable:** Show the failing local test and failed CI job. Restore the assertion afterwards.

### Exercise 7 — Add a quality gate
Configure the pipeline so a packaging job depends on a successful test job using `needs`.

**Deliverable:** Demonstrate that packaging is skipped when tests fail and runs when tests pass.

### Exercise 8 — Preserve test reports
Upload the test report as a workflow artifact. Inspect the artifact from the Actions run.

**Deliverable:** Explain when a report should still be uploaded after a test failure and how `if: always()` helps.

### Exercise 9 — Build a test matrix
If your project supports multiple Python versions, configure a matrix for two supported versions.

**Deliverable:** Explain why a matrix may uncover compatibility issues and why unsupported versions should not be included.

### Exercise 10 — Cache versus artifact
Describe when you would cache downloaded dependencies and when you would upload a compiled package or test report.

**Deliverable:** Give two examples of each and explain why a cache is not a release artifact.

### Exercise 11 — Add a security check
Choose an appropriate static-analysis or dependency-checking tool for the project. Add it to a separate step and document how findings should affect the build.

**Deliverable:** Tool name, purpose, output, and failure policy. Do not add real secrets.

### Exercise 12 — Build-stage threat review
A pipeline downloads dependencies, builds a package, runs tests, and publishes artifacts.

**Deliverable:** Identify at least four risks, such as dependency compromise, leaked secrets, untrusted runner access, artifact tampering, or sensitive test output. Suggest one mitigation for each.

### Exercise 13 — Trace the artifact
Explain how to associate a build artifact with the source revision that produced it.

**Deliverable:** Document the commit SHA, workflow run ID, artifact name/version, and checksum or image digest where applicable.

## Stretch challenges

- Add coverage measurement and choose a meaningful minimum threshold.
- Add a test that validates input errors.
- Separate lint, test, and package into distinct jobs.
- Add concurrency control for repeated pushes to the same branch.
- Store build metadata alongside the package.
- Add a dependency lockfile and explain how it improves repeatability.

## Submission checklist

- [ ] Tests pass locally.
- [ ] Build validation runs.
- [ ] CI workflow is stored in `.github/workflows/`.
- [ ] A deliberate test failure causes CI to fail.
- [ ] Packaging depends on successful tests.
- [ ] Test reports or build outputs are uploaded as artifacts.
- [ ] No secrets are committed.
- [ ] Artifact traceability and dependency security are documented.
