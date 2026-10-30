# 03 — Build and Test Stages

This module explains how build and test stages fit into a CI/CD pipeline, how to make them repeatable, and how to use test results as quality gates.

## Learning objectives

By the end of this module, you should be able to:

- Explain the difference between building software and testing it.
- Identify compile, package, unit, integration, system, smoke, and regression tests.
- Design a pipeline where test failures block later stages.
- Produce and preserve build artifacts and test reports.
- Explain dependency caching versus artifact storage.
- Apply basic DevSecOps practices to build and test workflows.

## Prerequisites

- Basic Git and GitHub knowledge.
- Basic Python or another programming language.
- Familiarity with CI/CD concepts from the previous module.

## 1. What is a build stage?

A build stage transforms source code and its dependencies into an output that can be tested or deployed. Depending on the project, a build may compile source code, resolve dependencies, bundle frontend assets, create a package, or build a container image.

A reliable build should be repeatable, use known dependency versions, and produce traceable outputs.

## 2. What is a test stage?

A test stage checks whether the application behaves as expected and meets defined requirements. Tests should run automatically and return a non-zero exit code when a required check fails.

## 3. Common test levels

| Test type | Purpose | Example |
|---|---|---|
| Unit | Verify a small function or component in isolation | Test a Python calculation function |
| Integration | Check interaction between components | API + database test |
| System/end-to-end | Validate a complete user workflow | Sign in and submit a form |
| Smoke | Quickly check that a deployed build basically works | Health endpoint returns HTTP 200 |
| Regression | Ensure existing behavior still works after changes | Re-run a suite for previously fixed defects |
| Performance | Measure response time, throughput, or resource usage | Load test an API in an approved environment |
| Security | Identify security weaknesses | SAST, dependency, secret, or container scanning |

Choose tests based on the application and risk. Not every pipeline needs every test type on every commit.

## 4. Typical build-and-test flow

```text
Commit / Pull Request
        |
        v
Checkout Source
        |
        v
Install Locked Dependencies
        |
        v
Lint / Static Checks
        |
        v
Build / Package
        |
        v
Unit Tests
        |
        v
Integration Tests (if configured)
        |
        v
Security and Quality Gates
        |
        v
Publish Artifact + Test Reports
        |
        v
Eligible for a later deployment stage
```

Teams may run independent checks in parallel. A job that packages or deploys a release should depend on the required checks passing.

## 5. Build outputs, artifacts, and caches

- **Build output:** files produced by the build, such as a wheel, binary, static bundle, or container image.
- **Artifact:** a saved output or report that can be downloaded or passed to another job.
- **Dependency cache:** reusable downloaded dependencies that speed up future builds. A cache is an optimization, not the authoritative release artifact.
- **Test report:** a record of test results, failures, and sometimes coverage data.

Use a lockfile and deterministic build configuration where possible. Record the source commit and version for each release artifact.

## 6. Quality gates

A quality gate is a required condition before the pipeline can proceed. Examples include:

- All required unit tests pass.
- Linting or type checks pass.
- Minimum test coverage is met, where a meaningful threshold is defined.
- No prohibited dependency or secret-scanning findings remain.
- The build artifact is created successfully.

Avoid making a pipeline green by ignoring failures with `continue-on-error` for required tests. If a check is intentionally advisory, document that decision.

## 7. DevSecOps practices for build and test

- Use least-privilege workflow permissions.
- Never commit credentials or print secrets in logs.
- Pin dependencies and review dependency changes.
- Use isolated, preferably ephemeral runners for untrusted code.
- Avoid executing external pull-request code on privileged self-hosted runners.
- Run security checks appropriate to the project, including dependency and secret scanning.
- Keep test data synthetic or appropriately sanitized.
- Do not put production credentials into test jobs.
- Preserve logs and reports without including sensitive data.
- Keep build artifacts traceable to the source revision.

## 8. Hands-on lab

The `examples.md` file contains a small Python calculator, unit tests, and a GitHub Actions workflow that tests the code and uploads a test report. It also demonstrates a build job that runs only after tests pass.

The workflow file must be placed under `.github/workflows/` at the repository root. Official documentation: [GitHub Actions workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows), [workflow artifacts](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts), and [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

## Module files

- `README.md` — concepts, stages, and security practices.
- `examples.md` — Python code, tests, and GitHub Actions workflow.
- `practical.md` — hands-on exercises.
- `solution.md` — suggested answers and verification guidance.

## Completion checklist

- [ ] I can explain build stages and test stages.
- [ ] I can distinguish unit, integration, smoke, regression, and end-to-end tests.
- [ ] I can run a test suite locally.
- [ ] I can configure a workflow to fail when required tests fail.
- [ ] I can upload a test report or build artifact.
- [ ] I understand the difference between a cache and an artifact.
- [ ] I can identify basic security risks in build and test pipelines.
