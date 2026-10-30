# GitLab Pipeline Fundamentals — Examples

These examples are learning snippets. Add them to a `.gitlab-ci.yml` file in a test project and confirm that a compatible runner is available.

## 1. Minimal pipeline

```yaml
hello:
  script:
    - echo "Hello from GitLab CI"
```

When `stages` and `stage` are omitted, the job uses the default `test` stage.

## 2. Multiple stages and parallel jobs

```yaml
stages:
  - build
  - test
  - deploy

compile:
  stage: build
  image: alpine:3.20
  script:
    - mkdir -p dist
    - echo "compiled" > dist/app.txt
  artifacts:
    paths:
      - dist/

test_unit:
  stage: test
  image: alpine:3.20
  script:
    - echo "Unit tests passed"

test_style:
  stage: test
  image: alpine:3.20
  script:
    - echo "Style checks passed"

deploy_demo:
  stage: deploy
  image: alpine:3.20
  script:
    - echo "Deploy step placeholder"
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual
```

The two test jobs can run in parallel. The deploy job is offered manually only on the default branch. It does not perform a real deployment.

## 3. Reusable defaults and variables

```yaml
default:
  image: alpine:3.20
  before_script:
    - echo "Preparing job"

variables:
  APP_ENV: "test"

show_environment:
  script:
    - echo "Environment: ${APP_ENV}"
  after_script:
    - echo "Job cleanup"
```

Use YAML variables for ordinary configuration, not secrets.

## 4. Rules for branch and merge-request pipelines

```yaml
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH'

lint:
  image: alpine:3.20
  script:
    - echo "Linting source"
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

`workflow: rules` controls whether the pipeline is created. Job-level `rules` controls whether an individual job is included.

## 5. Cache dependencies (illustrative Python example)

```yaml
python_tests:
  image: python:3.12
  cache:
    key: "pip-${CI_COMMIT_REF_SLUG}"
    paths:
      - .cache/pip/
  variables:
    PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  script:
    - python --version
    - pip install -r requirements.txt
    - python -m pytest
```

This assumes `requirements.txt` and a pytest test suite exist. A cache is an optimization, not a reliable way to pass build outputs between jobs.

## 6. Artifacts and reports

```yaml
test_report:
  image: alpine:3.20
  script:
    - mkdir -p reports
    - echo "sample test result" > reports/result.txt
  artifacts:
    when: always
    paths:
      - reports/
    expire_in: 7 days
```

Artifacts preserve job outputs. Use report-specific artifact types when publishing supported test, coverage, or security reports.

## 7. Runner tags

```yaml
shell_job:
  tags:
    - linux
    - shell
  script:
    - echo "This job requires a runner with both tags"
```

The job remains pending if no eligible online runner has the required tags.

## 8. Inspect predefined variables safely

```yaml
inspect_context:
  image: alpine:3.20
  script:
    - echo "Project: ${CI_PROJECT_PATH}"
    - echo "Branch: ${CI_COMMIT_REF_NAME}"
    - echo "Commit: ${CI_COMMIT_SHORT_SHA}"
```

Print only the specific non-sensitive predefined values needed for debugging. Do not print secrets or the complete environment.

## 9. Validate locally with a YAML parser

```python
# validate_yaml.py
from pathlib import Path
import yaml

config = yaml.safe_load(Path(".gitlab-ci.yml").read_text())
if not isinstance(config, dict):
    raise SystemExit("Pipeline configuration must be a YAML mapping")

print("YAML parsed successfully")
```

Install PyYAML with `python -m pip install pyyaml`. A generic YAML parser checks YAML syntax only; it does not validate GitLab-specific keywords or semantics. Use GitLab CI Lint for that.
