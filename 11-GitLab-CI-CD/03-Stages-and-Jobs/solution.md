# GitLab Stages and Jobs — Solutions

These are reference implementations. Run them in a test project with a compatible runner.

## 1. Multi-stage pipeline

```yaml
stages:
  - validate
  - build
  - test
  - deploy

validate_job:
  stage: validate
  image: alpine:3.20
  script:
    - echo "Validation complete"

build_job:
  stage: build
  image: alpine:3.20
  script:
    - echo "Build complete"

test_job:
  stage: test
  image: alpine:3.20
  script:
    - echo "Tests complete"

deploy_job:
  stage: deploy
  image: alpine:3.20
  script:
    - echo "Deployment placeholder"
```

**Explanation:** Stages execute in the order declared. Each later stage normally waits for the previous stage to complete successfully.

## 2. Parallel jobs

```yaml
stages: [test]

unit_tests:
  stage: test
  image: alpine:3.20
  script:
    - sleep 5
    - echo "Unit tests complete"

lint_checks:
  stage: test
  image: alpine:3.20
  script:
    - sleep 5
    - echo "Lint complete"

security_checks:
  stage: test
  image: alpine:3.20
  script:
    - sleep 5
    - echo "Security check complete"
```

**Explanation:** GitLab can schedule same-stage jobs concurrently. Actual overlap depends on available eligible runners and runner concurrency.

## 3. Job lifecycle

```yaml
lifecycle_demo:
  image: alpine:3.20
  before_script:
    - echo "Prepare"
  script:
    - echo "Run task"
    - exit 1
  after_script:
    - echo "Cleanup"
```

**Explanation:** `before_script` runs before `script`; `after_script` runs after the main script. The job is still failed because the main script returned a non-zero status. `after_script` uses a separate shell context, so do not rely on shell state created in `script`.

## 4. Runner tags

```yaml
tagged_job:
  tags:
    - linux
  script:
    - echo "Runner tag matched"
```

**Explanation:** Replace `linux` with a tag actually configured on an eligible runner. If no online runner matches all required tags and access rules, the job can remain pending.

## 5. Artifacts

```yaml
stages: [build, test]

build_output:
  stage: build
  image: alpine:3.20
  script:
    - mkdir -p output
    - echo "CI artifact content" > output/app.txt
  artifacts:
    paths:
      - output/
    expire_in: 1 week

test_output:
  stage: test
  image: alpine:3.20
  script:
    - test -s output/app.txt
    - cat output/app.txt
```

**Explanation:** Later-stage jobs download artifacts from earlier stages by default. Artifact paths are relative to the project working directory.

## 6. Restrict artifact downloads

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
    - test ! -e backend/app.txt
```

**Explanation:** `dependencies` limits artifact downloads from earlier stages. It does not create an independent scheduling graph; stage ordering still applies.

## 7. Non-blocking failure

```yaml
optional_check:
  image: alpine:3.20
  script:
    - echo "Demonstrating a non-blocking check"
    - exit 1
  allow_failure: true
```

**Explanation:** The job is allowed to fail without making the pipeline fail. Avoid this for mandatory security, compliance, or release gates.

## 8. DAG using needs

```yaml
stages: [build, test, deploy]

build_api:
  stage: build
  script:
    - echo "API built"

build_web:
  stage: build
  script:
    - echo "Web built"

test_api:
  stage: test
  needs: ["build_api"]
  script:
    - echo "API tested"

test_web:
  stage: test
  needs: ["build_web"]
  script:
    - echo "Web tested"

deploy_api:
  stage: deploy
  needs: ["test_api"]
  script:
    - echo "API deployment placeholder"
```

**Explanation:** Each test job can start when its own build dependency finishes, without waiting for unrelated build jobs. This is a DAG (directed acyclic graph) dependency model.

## 9. Immediate job

```yaml
stages: [build, test]

build_app:
  stage: build
  script:
    - echo "Build"

lint:
  stage: test
  needs: []
  script:
    - echo "Lint starts immediately"
```

**Explanation:** An empty `needs` list means the job has no job dependencies and can start as soon as the pipeline is created.

## 10. Optional dependency

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
    - echo "Deployment placeholder"
```

**Explanation:** If the optional job exists, the downstream job waits for it. If rules exclude it, the optional dependency is ignored. Without `optional: true`, a reference to a missing job can prevent pipeline creation.

## 11. Parallel matrix

```yaml
matrix_tests:
  stage: test
  image: alpine:3.20
  parallel:
    matrix:
      - COMPONENT: ["api", "web"]
        TARGET: ["linux", "alpine"]
  script:
    - echo "Testing ${COMPONENT} for ${TARGET}"
```

**Explanation:** Two values for each of two matrix variables create four job instances.

## 12. Troubleshooting guide

| Symptom | Likely cause | Action |
|---|---|---|
| Job pending | No eligible runner, tags mismatch, runner paused, or concurrency limit | Check runner status, tags, access, and capacity |
| Job skipped | `rules`, `when`, or workflow conditions excluded it | Inspect evaluated pipeline configuration and rules |
| Artifact missing | Wrong path, expired artifact, or artifact not downloaded | Check producer logs, artifact paths, expiry, and `dependencies`/`needs` |
| `needs` target missing | Target job was excluded by rules or not defined | Align rules or use `optional: true` if genuinely optional |
| Job starts late | Stage barrier, unmet `needs`, or runner queue | Inspect stage/dependency graph and runner availability |

## Key answers
1. A **stage** groups jobs into a phase; a **job** performs a task.
2. The default stage is `test`.
3. Yes, if runner capacity and configuration allow it.
4. Runner concurrency settings and available eligible runners determine how many jobs can execute at once.
5. A failed job normally fails the pipeline and blocks later stages, unless failure is allowed or other control flow applies.
6. `allow_failure` makes a job's failure non-blocking.
7. `dependencies` selects artifacts from earlier stages; `needs` defines execution dependencies and can allow jobs to start earlier.
8. A DAG is a directed acyclic graph of job dependencies.
9. `needs: []` allows the job to start immediately when the pipeline is created.
10. Common causes include no eligible runner, mismatched tags, runner pause, or exhausted concurrency.
11. A producer job declares `artifacts`; later jobs download them according to default stage behavior or explicit configuration.
12. `parallel:matrix` creates multiple job instances from combinations of variable values.

## Further reading
- [GitLab YAML reference](https://docs.gitlab.com/ci/yaml/)
- [The `needs` keyword](https://docs.gitlab.com/ci/yaml/needs/)
- [Job artifacts](https://docs.gitlab.com/ci/jobs/job_artifacts/)
