# GitLab Pipeline Fundamentals

## Overview
GitLab CI/CD automates building, testing, packaging, and deploying software. A pipeline is defined in a YAML file named `.gitlab-ci.yml` at the repository root by default. GitLab evaluates this configuration and schedules jobs on available GitLab Runners.

## Learning objectives
By the end of this module, you should be able to:
- Explain continuous integration, continuous delivery, and continuous deployment.
- Describe the relationship between pipelines, stages, jobs, and runners.
- Create and run a basic `.gitlab-ci.yml` pipeline.
- Understand sequential stages and parallel jobs within a stage.
- Use common YAML keywords such as `image`, `before_script`, `script`, `after_script`, `variables`, `rules`, `artifacts`, and `cache`.
- Inspect pipeline and job status, logs, and artifacts.
- Apply basic security and troubleshooting practices.

## Core concepts

| Concept | Meaning |
|---|---|
| Pipeline | A collection of jobs created from a CI/CD configuration for a commit, merge request, schedule, or manual run. |
| Stage | A named phase that groups jobs and establishes their default execution order. |
| Job | A unit of work, such as linting, testing, building, or deploying. |
| Runner | An agent that picks up and executes eligible jobs. |
| Executor | The environment used by a runner, such as Docker, Shell, or Kubernetes. |
| Artifact | Output saved by a job and made available for download or to later jobs. |
| Cache | Reusable files intended to speed up later job runs, commonly dependencies. |

Stages run in the order listed in `stages`. Jobs in the same stage can run concurrently when sufficient runners are available. The next stage normally starts after the current stage succeeds. A job without an explicit `stage` uses the default `test` stage.

## Pipeline lifecycle
1. A configured event occurs, such as a push or merge request.
2. GitLab reads and validates `.gitlab-ci.yml`.
3. GitLab creates the pipeline and its jobs.
4. Eligible runners pick up jobs.
5. Runners execute job scripts and upload artifacts/reports.
6. GitLab records status, logs, and results.

## First pipeline

Create `.gitlab-ci.yml` in the root of a test repository:

```yaml
stages:
  - build
  - test
  - package

variables:
  APP_NAME: "demo-app"

build_app:
  stage: build
  image: alpine:3.20
  script:
    - echo "Building ${APP_NAME}"
    - mkdir -p output
    - echo "Build completed" > output/build.txt
  artifacts:
    paths:
      - output/
    expire_in: 1 week

unit_tests:
  stage: test
  image: alpine:3.20
  script:
    - echo "Running unit tests"
    - test -f output/build.txt

package_app:
  stage: package
  image: alpine:3.20
  script:
    - echo "Packaging ${APP_NAME}"
```

The test job receives artifacts from earlier stages by default, unless artifact download behavior is changed. This deliberately small example demonstrates the pipeline structure; it is not a production build.

## Common keywords

- `stages`: declares stage order.
- `stage`: assigns a job to a stage.
- `image`: selects a container image when using a compatible executor.
- `script`: commands executed by the job.
- `before_script` / `after_script`: commands run before/after the main script.
- `variables`: defines non-sensitive configuration values.
- `rules`: controls whether a job is added and how it runs.
- `artifacts`: preserves job output.
- `cache`: reuses files to reduce repeated work.
- `tags`: selects runners with matching tags.
- `needs`: expresses job dependencies and can enable DAG-style execution.

## How to run it
1. Create a GitLab project and ensure an eligible runner is available.
2. Add `.gitlab-ci.yml` at the repository root.
3. Commit and push the file.
4. Open **Build > Pipelines** and select the new pipeline.
5. Open each job to inspect its log and status.
6. If a job fails, identify the first failing command and correct the configuration or environment.

## Basic security guidance
- Do not commit passwords, private keys, or access tokens in YAML or source code.
- Store sensitive values in GitLab CI/CD variables or an approved secret manager; mask and protect variables where appropriate.
- Restrict protected variables and deployment runners to trusted protected refs.
- Pin important images and dependencies to controlled versions or digests.
- Use least-privilege project and runner permissions.
- Treat merge-request code from untrusted contributors as untrusted input.
- Prefer isolated, short-lived runners for workloads that execute untrusted code.
- Review job logs before printing environment values; never dump all variables.

## Troubleshooting checklist
- Is `.gitlab-ci.yml` in the expected path and valid YAML?
- Does the pipeline configuration pass CI Lint?
- Is a runner online, enabled for the project, and eligible for the job tags?
- Does the selected image exist and support the commands used?
- Are commands valid for the runner's shell/OS?
- Are required files present in the job workspace?
- Are artifact paths relative to `$CI_PROJECT_DIR`?
- Do `rules` unintentionally exclude the job?

## Suggested learning sequence
1. Read the concepts and lifecycle.
2. Run the first pipeline.
3. Modify stage names and add a parallel test job.
4. Add an artifact and inspect it in the UI.
5. Experiment with variables and `rules`.
6. Break a job intentionally, read its log, and fix it.

## References
- [GitLab CI/CD pipelines](https://docs.gitlab.com/ci/pipelines/)
- [Create and run your first pipeline](https://docs.gitlab.com/ci/quick_start/)
- [CI/CD YAML syntax reference](https://docs.gitlab.com/ci/yaml/)
- [GitLab CI/CD jobs](https://docs.gitlab.com/ci/jobs/)
