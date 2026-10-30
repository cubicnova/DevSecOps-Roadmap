# GitLab Stages and Jobs — Examples

Each example is a focused `.gitlab-ci.yml` pattern. Test in a non-production project with an available runner.

## 1. Custom stages

```yaml
stages:
  - validate
  - build
  - test
  - release

validate_config:
  stage: validate
  image: alpine:3.20
  script:
    - echo "Configuration validated"

build_app:
  stage: build
  image: alpine:3.20
  script:
    - echo "Build completed"

test_app:
  stage: test
  image: alpine:3.20
  script:
    - echo "Tests passed"

release_app:
  stage: release
  image: alpine:3.20
  script:
    - echo "Release placeholder"
```

## 2. Multiple jobs in one stage

```yaml
stages: [test]

unit_tests:
  stage: test
  image: alpine:3.20
  script:
    - echo "Unit tests"

lint_checks:
  stage: test
  image: alpine:3.20
  script:
    - echo "Lint checks"

security_checks:
  stage: test
  image: alpine:3.20
  script:
    - echo "Security checks"
```

These jobs can run concurrently when runner capacity is available.

## 3. before_script and after_script

```yaml
stages: [test]

test_job:
  image: alpine:3.20
  before_script:
    - echo "Preparing test environment"
  script:
    - echo "Executing tests"
  after_script:
    - echo "Running cleanup commands"
```

`after_script` runs in a separate shell context in many executor configurations. Do not rely on shell variables exported in `script` being available there.

## 4. Job-level variables

```yaml
stages: [build]

build_development:
  stage: build
  image: alpine:3.20
  variables:
    BUILD_MODE: "development"
  script:
    - echo "Build mode: ${BUILD_MODE}"
```

Use GitLab CI/CD variables or an external secret manager for sensitive values; never commit secrets in the YAML file.

## 5. Runner tags

```yaml
linux_build:
  stage: build
  tags:
    - linux
    - docker
  image: alpine:3.20
  script:
    - echo "This job requires a runner matching its tags"
```

The runner must be online, enabled for the project, and eligible for all tags required by the job.

## 6. Allow a non-critical job to fail

```yaml
optional_quality_check:
  stage: test
  image: alpine:3.20
  script:
    - echo "Non-blocking check"
    - exit 1
  allow_failure: true
```

Use `allow_failure` only for checks whose failure is intentionally non-blocking.

## 7. Artifacts between stages

```yaml
stages: [build, test]

create_build:
  stage: build
  image: alpine:3.20
  script:
    - mkdir -p output
    - echo "build-output" > output/app.txt
  artifacts:
    paths:
      - output/
    expire_in: 1 week

verify_build:
  stage: test
  image: alpine:3.20
  script:
    - test -s output/app.txt
    - cat output/app.txt
```

The later-stage job downloads earlier-stage artifacts by default.

## 8. Restrict artifacts with dependencies

```yaml
stages: [build, test]

build_frontend:
  stage: build
  script:
    - mkdir -p frontend
    - echo "frontend" > frontend/app.txt
  artifacts:
    paths: [frontend/]

build_backend:
  stage: build
  script:
    - mkdir -p backend
    - echo "backend" > backend/app.txt
  artifacts:
    paths: [backend/]

test_frontend:
  stage: test
  dependencies:
    - build_frontend
  script:
    - test -s frontend/app.txt
```

`dependencies` controls which artifacts from previous stages are downloaded. It does not define an execution dependency beyond the normal stage order.

## 9. DAG pipeline using needs

```yaml
stages: [build, test, deploy]

build_api:
  stage: build
  script:
    - echo "API build complete"

build_ui:
  stage: build
  script:
    - echo "UI build complete"

test_api:
  stage: test
  needs: ["build_api"]
  script:
    - echo "API tests complete"

test_ui:
  stage: test
  needs: ["build_ui"]
  script:
    - echo "UI tests complete"

deploy_api:
  stage: deploy
  needs: ["test_api"]
  script:
    - echo "API deploy placeholder"
```

`test_api` can start when `build_api` completes; it does not have to wait for `build_ui`.

## 10. Immediate job with needs: []

```yaml
stages: [build, test]

build_app:
  stage: build
  script:
    - echo "Build"

early_lint:
  stage: test
  needs: []
  script:
    - echo "Lint can start immediately"
```

The lint job starts when the pipeline is created, without waiting for the build stage.

## 11. Optional dependency

```yaml
stages: [build, test, deploy]

build:
  stage: build
  script:
    - echo "Build"

optional_test:
  stage: test
  rules:
    - if: '$RUN_EXTRA_TESTS == "true"'
  script:
    - echo "Optional test"

deploy:
  stage: deploy
  needs:
    - job: build
    - job: optional_test
      optional: true
  script:
    - echo "Deploy placeholder"
```

When `optional_test` is not added to the pipeline, `deploy` can proceed after `build`. When it is present, `deploy` waits for it.

## 12. Parallel matrix jobs

```yaml
test_matrix:
  stage: test
  image: alpine:3.20
  parallel:
    matrix:
      - TARGET: ["api", "web"]
        OS_NAME: ["linux", "alpine"]
  script:
    - echo "Testing ${TARGET} on ${OS_NAME}"
```

GitLab creates a job for each matrix combination. Matrix variables help reuse one job definition for multiple targets.
