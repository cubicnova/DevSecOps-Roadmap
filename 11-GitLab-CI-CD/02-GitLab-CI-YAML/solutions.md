# GitLab CI/CD YAML — Solutions and Explanations

## Solution 1: Minimal pipeline

```yaml
stages:
  - test

hello:
  stage: test
  script:
    - echo "Hello from GitLab CI"
```

Commit this file as `.gitlab-ci.yml`. A compatible runner must be available for the job.

## Solution 2: Multiple stages

```yaml
stages: [build, test, deploy]

build:
  stage: build
  script:
    - echo "Build step"

test:
  stage: test
  script:
    - echo "Test step"

deploy:
  stage: deploy
  script:
    - echo "Deployment placeholder"
```

GitLab executes stages in declared order. Jobs in the same stage can run in parallel when runner capacity allows.

## Solution 3: Image and tags

```yaml
lint:
  stage: test
  image: alpine:3.20
  tags:
    - docker
  script:
    - echo "Running on a Docker-tagged runner"
```

A tag does not install a runner. It selects a runner that is already configured with the matching tag and is allowed to run the project job.

## Solution 4: Variables

```yaml
variables:
  APP_NAME: "sample"

build:
  stage: build
  variables:
    BUILD_MODE: "debug"
  script:
    - echo "$APP_NAME"
    - echo "$BUILD_MODE"
```

Store credentials in GitLab CI/CD settings. Mark sensitive variables masked and protected when appropriate, and do not echo them. Protected variables are only exposed in eligible protected-ref contexts according to project settings.

## Solution 5: Artifacts

```yaml
stages: [build, test]

build:
  stage: build
  script:
    - mkdir -p dist
    - echo "build output" > dist/app.txt
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

verify:
  stage: test
  script:
    - test -f dist/app.txt
    - cat dist/app.txt
```

Artifacts persist job output. By default, later-stage jobs download artifacts from earlier stages; control this behavior with `dependencies` or `needs:artifacts`.

## Solution 6: Cache

```yaml
python_tests:
  image: python:3.12
  stage: test
  variables:
    PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  cache:
    key: "pip-$CI_COMMIT_REF_SLUG"
    paths:
      - .cache/pip/
  script:
    - pip install -r requirements.txt
    - pytest
```

Cache is best-effort optimization. Use artifacts for required outputs that must be passed to later jobs.

## Solution 7: Rules

```yaml
tests:
  stage: test
  script:
    - echo "Run tests"
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

Rules are evaluated in order. The first matching rule determines whether and how the job is added.

## Solution 8: Workflow rules

```yaml
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
    - when: never

stages: [test]

check:
  stage: test
  script:
    - echo "Allowed pipeline"
```

`workflow:rules` decides whether a pipeline is created. Job-level `rules` decide whether an individual job is added to a created pipeline.

## Solution 9: DAG with needs

```yaml
stages: [build, test]

build_app:
  stage: build
  script:
    - mkdir -p dist
    - echo "app" > dist/app.txt
  artifacts:
    paths: [dist/]

build_docs:
  stage: build
  script:
    - mkdir -p docs
    - echo "docs" > docs/index.txt
  artifacts:
    paths: [docs/]

test_app:
  stage: test
  needs:
    - job: build_app
      artifacts: true
  script:
    - test -f dist/app.txt
```

The test job depends on `build_app`, not `build_docs`. `needs` can allow DAG execution and limits artifact downloads to declared dependencies by default.

## Solution 10: Reuse with extends and include

`.gitlab-ci.yml`:

```yaml
include:
  - local: '/ci/security-jobs.yml'

.base:
  image: alpine:3.20
  before_script:
    - echo "Common preparation"

lint:
  extends: .base
  stage: test
  script:
    - echo "Lint source"
```

`ci/security-jobs.yml`:

```yaml
dependency_audit:
  stage: test
  script:
    - echo "Replace with a dependency audit command"
  allow_failure: true
```

The included file is merged with the main configuration. Review included content as code because it can define jobs and global behavior.

## Solution 11: Manual deployment

```yaml
stages: [deploy]

deploy_staging:
  stage: deploy
  script:
    - echo "Replace with deployment command"
  environment:
    name: staging
  when: manual
  allow_failure: false
```

A manual job requires a user to start it, but production authorization should also consider protected environments, protected refs, protected variables, runner trust, and deployment permissions.

## Solution 12: CI Lint
Use GitLab's CI Lint / Pipeline Editor validation. It checks GitLab-specific configuration semantics that a generic YAML parser cannot understand. For runtime failures, inspect the job log and verify runner tags, executor, image availability, network access, and shell commands.

## Common errors and fixes

| Error or symptom | Likely cause | Fix |
|---|---|---|
| Pipeline not created | `workflow:rules` excludes the event | Review pipeline source and rule order |
| Job stuck pending | No eligible runner | Check runner status, tags, and project access |
| Unknown stage | Job stage is not declared | Add the stage or correct the spelling |
| Script key missing | Job has no valid execution definition | Add `script`, `run`, or a valid trigger configuration |
| Artifact missing | Wrong path or job did not produce file | Use paths relative to `$CI_PROJECT_DIR` and inspect build logs |
| Cache not restored | Cache key/path mismatch or runner cache setup | Verify key, path, and runner cache configuration |
| Variable is empty | Variable scope/protection/type mismatch | Check project/group settings and protected-ref eligibility |
| Include not found | Incorrect local path or inaccessible remote/project file | Verify path, permissions, and include source |
| Job never appears | `rules` conditions do not match | Inspect predefined variables and rule order |

## Security review checklist
- Keep credentials out of YAML and logs.
- Use protected variables for protected deployment refs.
- Avoid privileged secrets in untrusted merge-request pipelines.
- Review and pin external CI includes where possible.
- Use dedicated trusted runners for deployment.
- Avoid storing secrets in artifacts or caches.
- Limit artifact retention and access.
- Use least-privilege job-token permissions.

## Official documentation
- [CI/CD YAML syntax reference](https://docs.gitlab.com/ci/yaml/)
- [GitLab CI/CD documentation](https://docs.gitlab.com/ci/)
- [CI/CD variables](https://docs.gitlab.com/ci/variables/)
