# 01 — CI/CD Concepts

Learn the principles, architecture, and security practices behind Continuous Integration (CI), Continuous Delivery (CD), and Continuous Deployment.

## Learning objectives

- Explain CI, Continuous Delivery, and Continuous Deployment.
- Describe a pipeline from source commit to production.
- Identify pipeline stages, triggers, artifacts, environments, and quality gates.
- Explain repeatable builds, automated tests, and artifact traceability.
- Recognize common CI/CD security risks and apply basic mitigations.
- Read and adapt a simple GitHub Actions workflow.

## Prerequisites

Basic Git/GitHub knowledge, familiarity with a programming language, and basic software testing concepts.

## Core concepts

### Continuous Integration (CI)
Developers frequently merge small changes into a shared branch. Each change triggers automated checks such as dependency installation, linting, unit tests, and build validation. The goal is to detect integration problems early.

### Continuous Delivery
Every change that passes the pipeline is kept in a deployable state. Production deployment is possible at any time, but a person or release process may approve the production deployment.

### Continuous Deployment
Every change that passes all required automated checks is deployed to production automatically. This requires reliable tests, monitoring, rollback capability, and strong release controls.

| Practice | What is automated? | Production release |
|---|---|---|
| CI | Integrate, build, test, validate | Not implied |
| Continuous Delivery | CI plus prepare a release-ready artifact | Usually requires approval or a release decision |
| Continuous Deployment | CI/CD through production | Automatic after required checks pass |

## Typical pipeline lifecycle

1. **Source** — commit or pull request.
2. **Checkout** — runner obtains the source revision.
3. **Install** — install dependencies, preferably from a lockfile.
4. **Validate** — linting, formatting, type checks, and policy checks.
5. **Test** — unit and integration tests.
6. **Build/package** — create a deployable artifact or container image.
7. **Security and quality gates** — run applicable SAST, dependency, secret, IaC, or container checks.
8. **Publish** — store the artifact in a registry or artifact repository.
9. **Deploy** — release to test, staging, or production.
10. **Verify and recover** — smoke tests, monitoring, and rollback if needed.

## Important building blocks

- **Trigger/event:** push, pull request, release, schedule, or manual dispatch.
- **Workflow/pipeline:** the overall automated process.
- **Job/stage:** a logical unit of work; jobs may run sequentially or in parallel.
- **Step/task:** a command or reusable action within a job.
- **Runner/agent:** the machine that executes jobs.
- **Artifact:** a versioned build output, package, or image.
- **Environment:** a deployment target such as development, staging, or production.
- **Quality gate:** a condition that must pass before a later stage can proceed.
- **Secret:** a credential provided securely to a workflow.
- **Rollback:** return to a previously known-good release.

## Pipeline overview

```text
Commit / Pull Request
        |
        v
Checkout -> Install -> Lint -> Test -> Build
                                  |
                                  v
                         Security / Quality Gates
                                  |
                                  v
                         Publish Immutable Artifact
                                  |
                                  v
                      Deploy to Staging -> Smoke Tests
                                  |
                         Approval (if required)
                                  |
                                  v
                            Production
                                  |
                         Monitor / Roll Back
```

## CI/CD security principles

- Give each workflow only the permissions it needs.
- Never hard-code passwords, API keys, or cloud credentials in source files.
- Use approved secret stores and prefer short-lived identity federation where supported.
- Pin third-party actions to reviewed immutable commit SHAs in production workflows.
- Treat pull-request code as untrusted, especially when it comes from forks.
- Avoid running untrusted code on privileged self-hosted runners.
- Protect production environments with required reviewers and branch rules.
- Scan source, dependencies, infrastructure definitions, and container images as appropriate.
- Keep artifacts traceable to a commit; promote the same immutable artifact between environments.
- Keep logs useful but never print secrets or sensitive data.
- Define monitoring, rollback, and incident-response procedures.

## Hands-on example

`examples.md` includes a small Python project and a GitHub Actions workflow that runs checks on pushes and pull requests. The example is educational and does not deploy to production.

GitHub Actions workflow files belong in `.github/workflows/` at the repository root. See the official [GitHub Actions concepts guide](https://docs.github.com/en/actions/get-started/understand-github-actions) and [workflow syntax reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

## Suggested learning sequence

1. Learn the terminology and compare CI, delivery, and deployment.
2. Draw a pipeline for a small application.
3. Run the Python example locally.
4. Add the workflow to a test repository and inspect the Actions tab.
5. Complete the exercises in `practical.md`.
6. Check your reasoning against `solution.md`.

## Module files

- `README.md` — concepts and learning objectives.
- `examples.md` — sample project, workflow, and common patterns.
- `practical.md` — hands-on exercises.
- `solution.md` — suggested answers and verification steps.

## Completion checklist

- [ ] I can explain the difference between CI, Continuous Delivery, and Continuous Deployment.
- [ ] I can identify triggers, jobs, steps, runners, artifacts, and gates.
- [ ] I can read a basic GitHub Actions workflow.
- [ ] I can explain how secrets, permissions, and untrusted pull requests affect pipeline security.
- [ ] I can propose a safe deployment and rollback strategy.
