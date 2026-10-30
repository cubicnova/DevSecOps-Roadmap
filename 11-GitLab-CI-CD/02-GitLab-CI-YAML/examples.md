# GitLab CI/CD YAML — Examples

Each example is a `.gitlab-ci.yml` fragment. Combine compatible examples carefully; avoid defining the same top-level key multiple times without understanding YAML merge behavior.

## 1. Minimal pipeline

```yaml
stages:
  - test

hello:
  stage: test
  script:
    - echo "Hello from GitLab CI"
    - echo "Project: $CI_PROJECT_PATH"
```

## 2. Build, test, and deploy stages

```yaml
stages: [build, test, deploy]

build_app:
  stage: build
  image: alpine:3.20
  script:
    - mkdir -p dist
    - echo "sample build output" > dist/app.txt
  artifacts:
    paths: [dist/]
    expire_in: 1 week

test_app:
  stage: test
  image: alpine:3.20
  script:
    - test -s dist/app.txt

deploy_demo:
  stage: deploy
  image: alpine:3.20
  script:
    - echo "Replace with a real deployment command"
  environment:
    name: staging
```

## 3. Global and job variables

```yaml
variables:
  APP_NAME: "demo"
  LOG_LEVEL: "info"

build:
  stage: build
  variables:
    BUILD_TARGET: "linux"
  script:
    - echo "$APP_NAME"
    - echo "$LOG_LEVEL"
    - echo "$BUILD_TARGET"
```

Do not place passwords, access tokens, or private keys in this file.

## 4. Default image and setup

```yaml
default:
  image: python:3.12
  before_script:
    - python --version
    - pip --version

stages: [test]

python_checks:
  stage: test
  script:
    - python -m compileall .
```

## 5. Rules for merge requests and default branch

```yaml
unit_tests:
  stage: test
  script:
    - echo "Run unit tests"
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

## 6. Workflow rules

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
    - echo "Pipeline created for an allowed event"
```

## 7. Artifacts

```yaml
stages: [build, test]

build:
  stage: build
  script:
    - mkdir -p output
    - echo "compiled output" > output/app.txt
  artifacts:
    name: "build-$CI_COMMIT_REF_SLUG"
    paths:
      - output/
    expire_in: 3 days

verify:
  stage: test
  script:
    - test -f output/app.txt
    - cat output/app.txt
```

## 8. Cache dependencies

```yaml
python_tests:
  image: python:3.12
  stage: test
  cache:
    key: "pip-$CI_COMMIT_REF_SLUG"
    paths:
      - .cache/pip/
  variables:
    PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  script:
    - pip install -r requirements.txt
    - pytest
```

Cache is an optimization, not a guaranteed artifact transfer mechanism.

## 9. DAG with needs

```yaml
stages: [build, test, package]

build_linux:
  stage: build
  script:
    - mkdir -p dist
    - echo "linux binary" > dist/linux.txt
  artifacts:
    paths: [dist/]

build_docs:
  stage: build
  script:
    - mkdir -p docs-output
    - echo "docs" > docs-output/index.txt
  artifacts:
    paths: [docs-output/]

test_linux:
  stage: test
  needs:
    - job: build_linux
      artifacts: true
  script:
    - test -f dist/linux.txt

package_docs:
  stage: package
  needs:
    - job: build_docs
      artifacts: true
  script:
    - test -f docs-output/index.txt
```

## 10. Allow failure for a non-blocking check

```yaml
security_advisory_check:
  stage: test
  allow_failure: true
  script:
    - echo "Illustrative non-blocking check"
    - exit 1
```

Use `allow_failure` deliberately. Do not make critical security controls non-blocking without documented risk acceptance.

## 11. Manual deployment

```yaml
deploy_production:
  stage: deploy
  script:
    - echo "Run protected production deployment command"
  environment:
    name: production
  when: manual
  allow_failure: false
```

Configure protected environments and protected variables in GitLab settings. A manual job alone is not a complete authorization policy.

## 12. Reuse with extends

```yaml
.base_job:
  image: alpine:3.20
  before_script:
    - echo "Shared setup"

lint:
  extends: .base_job
  stage: test
  script:
    - echo "Lint source"
```

## 13. Include local configuration

```yaml
include:
  - local: '/ci/test-jobs.yml'

stages: [test]
```

Example `ci/test-jobs.yml`:

```yaml
unit_tests:
  stage: test
  script:
    - echo "Tests from included file"
```

## 14. Runner tags

```yaml
deploy:
  stage: deploy
  tags:
    - trusted-deploy-runner
  script:
    - echo "Runs only on a runner with the matching tag"
```

The runner must be available to the project and configured with the matching tag.

## 15. Validate YAML syntax locally

```bash
# Check indentation and basic YAML parsing (requires Ruby and a YAML parser).
ruby -e 'require "yaml"; YAML.load_file(".gitlab-ci.yml"); puts "YAML parsed"'

# Then use GitLab CI Lint to validate GitLab-specific keywords,
# expressions, includes, and merged configuration.
```

A generic YAML parser cannot validate all GitLab CI semantics.
