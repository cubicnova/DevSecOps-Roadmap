# GitLab CI/CD — Stages and Jobs

## Overview
Stages and jobs define how work is organized and executed in a GitLab CI/CD pipeline. A **stage** is a phase in the pipeline, while a **job** is an individual task assigned to a stage. By default, stages execute sequentially and jobs in the same stage can run concurrently when runner capacity allows.

This module introduces stage ordering, job configuration, runner scheduling, job dependencies, DAG pipelines with `needs`, and artifact flow.

## Learning objectives
- Define stages and jobs in `.gitlab-ci.yml`.
- Explain the default stage order and the default `test` stage.
- Configure multiple jobs in one stage.
- Use `before_script`, `script`, `after_script`, `image`, `tags`, and `variables`.
- Understand how job failures affect later stages.
- Use `needs` to create directed acyclic graph (DAG) execution.
- Pass build output between jobs with artifacts.
- Troubleshoot pending, skipped, and failed jobs.

## Stage vs job

| Item | Stage | Job |
|---|---|---|
| Purpose | Groups work into a pipeline phase | Performs a specific task |
| Defined by | `stages` at top level | A named job entry |
| Assignment | Referenced by a job's `stage` | Assigned to one stage |
| Execution | Stage order is sequential by default | Same-stage jobs may run concurrently |
| Example | `build`, `test`, `deploy` | `compile_app`, `unit_tests`, `deploy_staging` |

## Default stages
GitLab provides default stages in this order:
1. `.pre`
2. `build`
3. `test`
4. `deploy`
5. `.post`

You can define your own stage list. If a job does not specify `stage`, it uses `test`. The special `.pre` and `.post` stages do not need to be listed in the `stages` array. A pipeline containing only `.pre` or `.post` jobs does not run; include at least one job in another stage.

## Basic stage and job configuration

```yaml
stages:
  - build
  - test
  - package
  - deploy

compile_app:
  stage: build
  image: alpine:3.20
  script:
    - mkdir -p dist
    - echo "compiled application" > dist/app.txt
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

unit_tests:
  stage: test
  image: alpine:3.20
  script:
    - test -s dist/app.txt
    - echo "Unit tests passed"

package_app:
  stage: package
  image: alpine:3.20
  script:
    - mkdir -p package
    - cp dist/app.txt package/
  artifacts:
    paths:
      - package/

deploy_demo:
  stage: deploy
  image: alpine:3.20
  script:
    - echo "Deployment placeholder"
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual
```

This is a demonstration pipeline, not a real application build or deployment. Artifacts from earlier stages are downloaded by later-stage jobs by default.

## How stage scheduling works
- GitLab normally waits for all jobs in a stage to finish successfully before starting the next stage.
- Jobs in the same stage can run at the same time if eligible runners are available.
- A single runner can execute jobs concurrently only when its concurrency configuration permits it.
- A failed job normally causes the pipeline to fail and prevents later stages from running.
- `allow_failure: true` can make a job failure non-blocking; use it only when that behavior is intentional.

## Important job keywords

| Keyword | Purpose |
|---|---|
| `stage` | Assigns a job to a stage |
| `script` | Commands executed by the job |
| `before_script` | Commands run before the main script |
| `after_script` | Commands run after the main script |
| `image` | Container image used by compatible executors |
| `tags` | Selects eligible runners |
| `variables` | Defines job-level or pipeline-level variables |
| `artifacts` | Saves job outputs for download or later jobs |
| `dependencies` | Selects artifacts from earlier-stage jobs |
| `needs` | Defines job dependencies and can bypass stage barriers |
| `when` | Controls when a job is run |
| `allow_failure` | Allows a job to fail without failing the whole pipeline |

## Job dependencies with `needs`
Without `needs`, the stage barrier applies. With `needs`, a job can start as soon as its listed dependencies finish, even if other jobs in earlier stages are still running.

```yaml
stages: [build, test, deploy]

build_api:
  stage: build
  script: echo "Build API"

build_web:
  stage: build
  script: echo "Build web"

test_api:
  stage: test
  needs: ["build_api"]
  script: echo "Test API"

test_web:
  stage: test
  needs: ["build_web"]
  script: echo "Test web"

deploy_api:
  stage: deploy
  needs: ["test_api"]
  script: echo "Deploy API"
```

`needs: []` allows a job to start immediately when the pipeline is created. If a needed job may be omitted by `rules`, consider `optional: true` for that dependency.

## Artifacts and dependencies
Artifacts preserve files produced by a job. By default, jobs in later stages download artifacts from all jobs in earlier stages. Use `dependencies` to restrict which earlier-stage artifacts are downloaded. With `needs`, artifacts are downloaded only from the jobs listed in `needs` unless configured otherwise.

Do not confuse:
- **Artifacts:** pipeline outputs that should be preserved or passed to downstream jobs.
- **Cache:** reusable files intended to speed up later jobs; cache contents should be safe to recreate.

Avoid combining `dependencies` and `needs` in the same job. Use `needs:artifacts` to control artifact downloads for jobs using `needs`.

## Troubleshooting
- **Job pending:** check runner availability, runner tags, project access, and concurrency.
- **Later stage not starting:** inspect earlier stage failures and manual jobs.
- **Job skipped:** review `rules`, `only/except` legacy configuration, and `when`.
- **Artifact missing:** check artifact paths, job success, expiry, and dependency configuration.
- **`needs` job not found:** ensure the needed job is added under the same pipeline conditions, or use `optional: true` when appropriate.
- **Unexpected serial execution:** inspect runner concurrency and available runner capacity.

## Recommended practice
1. Keep jobs small and focused.
2. Give jobs descriptive names.
3. Separate build, test, security checks, package, and deployment responsibilities.
4. Use `needs` only where the dependency graph is clear.
5. Pass outputs with artifacts rather than assuming one job's filesystem is shared with another.
6. Do not print secrets in job logs.
7. Use protected environments and restricted runners for deployments.
8. Validate YAML and GitLab semantics with CI Lint.

## References
- [CI/CD YAML syntax reference](https://docs.gitlab.com/ci/yaml/)
- [Make jobs start earlier with `needs`](https://docs.gitlab.com/ci/yaml/needs/)
- [Job artifacts](https://docs.gitlab.com/ci/jobs/job_artifacts/)
- [CI/CD pipelines](https://docs.gitlab.com/ci/pipelines/)
