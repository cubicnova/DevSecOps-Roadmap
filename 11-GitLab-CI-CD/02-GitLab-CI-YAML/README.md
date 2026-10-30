# GitLab CI/CD YAML

## Overview
GitLab CI/CD pipelines are configured primarily in a `.gitlab-ci.yml` file at the root of a repository. The file describes jobs, stages, execution conditions, dependencies, artifacts, caches, variables, and deployment behavior. GitLab parses the YAML configuration when creating a pipeline, then schedules eligible jobs on compatible GitLab Runners.

## Learning objectives
- Understand the structure of `.gitlab-ci.yml`.
- Define stages and jobs using `script`.
- Configure images, tags, variables, and defaults.
- Control pipeline and job creation with `workflow:rules` and `rules`.
- Pass files between jobs with artifacts and improve performance with cache.
- Use `needs` to build dependency graphs.
- Reuse configuration with anchors, `extends`, and `include`.
- Validate YAML and troubleshoot common pipeline errors.

## 1. Basic pipeline structure

Create `.gitlab-ci.yml` in the repository root:

```yaml
stages:
  - build
  - test
  - deploy

build_app:
  stage: build
  image: alpine:3.20
  script:
    - echo "Building application"

test_app:
  stage: test
  image: alpine:3.20
  script:
    - echo "Running tests"

deploy_app:
  stage: deploy
  image: alpine:3.20
  script:
    - echo "Deploying application"
```

Stages run in the order declared. Jobs in the same stage can run in parallel when runners are available. A later stage normally starts after earlier-stage jobs succeed. If a job omits `stage`, it uses the default `test` stage.

## 2. Job keywords

| Keyword | Purpose |
|---|---|
| `stage` | Assigns a job to a stage |
| `script` | Commands executed by the runner |
| `image` | Container image used by a Docker executor |
| `tags` | Selects runners with matching tags |
| `before_script` | Commands run before `script` |
| `after_script` | Commands run after the main script |
| `variables` | Defines job-level variables |
| `artifacts` | Stores output files for later jobs/download |
| `cache` | Reuses dependencies or generated files |
| `rules` | Controls whether and how a job is added |
| `needs` | Defines job dependencies and DAG execution |
| `when` | Controls job execution timing |
| `allow_failure` | Allows a job failure without failing the pipeline |
| `environment` | Associates a job with a deployment environment |
| `retry` | Retries a job under configured conditions |
| `timeout` | Sets a job timeout |

## 3. Stages and jobs

```yaml
stages: [lint, test, package]

lint:
  stage: lint
  script:
    - echo "Linting"

unit_tests:
  stage: test
  script:
    - echo "Unit tests"

package:
  stage: package
  script:
    - mkdir -p dist
    - echo "package" > dist/build.txt
  artifacts:
    paths:
      - dist/
    expire_in: 1 week
```

Artifacts are pipeline outputs, such as test reports or compiled files. By default, later-stage jobs download artifacts from earlier stages. Use `dependencies` or `needs:artifacts` to control which artifacts are downloaded.

## 4. Variables

Variables can be declared globally, at job level, or in GitLab project/group settings.

```yaml
variables:
  APP_NAME: "sample-app"
  BUILD_MODE: "release"

build:
  script:
    - echo "Building $APP_NAME in $BUILD_MODE mode"
```

Use GitLab's CI/CD settings for sensitive values. Mark secrets as masked and protected when appropriate, scope them to environments where possible, and never echo secret values. Do not assume masking makes arbitrary secret handling safe.

## 5. Defaults and shared commands

```yaml
default:
  image: alpine:3.20
  before_script:
    - echo "Preparing job"

stages: [test]

unit_tests:
  stage: test
  script:
    - echo "Run tests"
```

`default` supplies default job configuration. A job-level keyword can override the default. Default configuration is not a general deep merge of every nested job keyword.

## 6. Rules and workflow rules

Use `rules` to decide whether a job is added to a pipeline and to set attributes when a rule matches.

```yaml
test:
  script: echo "Run tests"
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

Use `workflow:rules` to control whether the pipeline itself is created:

```yaml
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH'
```

Rules are evaluated in order; the first matching rule determines the result. Avoid mixing `only/except` with `rules` in the same configuration because their behavior can be confusing and those older keywords are not recommended for new pipelines.

## 7. Artifacts versus cache

- **Artifacts** preserve outputs produced by a job and make them available to later jobs or users.
- **Cache** speeds up subsequent jobs by reusing dependencies or generated data. A cache is an optimization and should not be the only copy of an essential build output.

```yaml
test:
  script:
    - mkdir -p reports
    - echo "passed" > reports/result.txt
  artifacts:
    paths:
      - reports/
    expire_in: 7 days
```

```yaml
dependencies:
  cache:
    key: "$CI_COMMIT_REF_SLUG"
    paths:
      - .cache/pip/
```

Use stable, appropriately scoped cache keys. Avoid caching secrets or untrusted executable content across trust boundaries.

## 8. Job dependencies with needs

`needs` creates a directed acyclic graph (DAG) and can let a job start before all jobs in earlier stages finish.

```yaml
build:
  stage: build
  script: echo "build"

test:
  stage: test
  needs: [build]
  script: echo "test"
```

With `needs`, artifact downloads are limited to the listed jobs by default. Use `artifacts: false` when a dependency is needed for ordering but its artifacts are not required. Do not combine `needs` and `dependencies` in the same job.

## 9. Reuse configuration

YAML anchors can reuse snippets within one file:

```yaml
.python_job: &python_job
  image: python:3.12
  before_script:
    - python --version

unit_tests:
  <<: *python_job
  script:
    - python -m compileall .
```

`extends` reuses hidden job configuration:

```yaml
.base:
  image: alpine:3.20
  before_script:
    - echo "Setup"

lint:
  extends: .base
  script:
    - echo "Lint"
```

`include` imports configuration from local files, other projects, remote URLs, or templates. Treat external CI configuration as a dependency: review its source, pin trusted revisions where possible, and consider integrity verification for remote includes.

## 10. Validate and debug
- Use **Build → Pipeline editor → Validate** or the CI Lint tool.
- Inspect the merged configuration when includes and inheritance are involved.
- Check that every job has a valid `script`, `run`, or `trigger` configuration as required.
- Confirm runner availability, tags, executor, and image compatibility.
- Check variable names and quoting.
- Inspect job logs and artifact availability.

## Security checklist
- [ ] Use least-privilege job tokens and credentials.
- [ ] Store secrets in GitLab CI/CD settings, not YAML.
- [ ] Protect sensitive variables and protected branches/tags.
- [ ] Review external includes and pin trusted revisions.
- [ ] Avoid running untrusted merge-request code with privileged secrets.
- [ ] Use trusted runner pools for sensitive deployment jobs.
- [ ] Limit artifact retention and avoid storing secrets in artifacts.
- [ ] Separate cache keys and trust boundaries appropriately.
- [ ] Validate changes with CI Lint before merging.

## Official documentation
- [CI/CD YAML syntax reference](https://docs.gitlab.com/ci/yaml/)
- [Get started with GitLab CI/CD](https://docs.gitlab.com/ci/)
- [CI/CD variables](https://docs.gitlab.com/ci/variables/)
- [CI/CD pipelines](https://docs.gitlab.com/ci/pipelines/)
