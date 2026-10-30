# GitLab Security Scanning — Examples

> Use these examples in a test project. Scanner templates and variables evolve; verify current documentation before using them in production.

## 1. Include selected GitLab scanner templates

```yaml
stages:
  - build
  - test
  - deploy

include:
  - template: Jobs/SAST.gitlab-ci.yml
  - template: Jobs/Secret-Detection.gitlab-ci.yml
  - template: Jobs/Dependency-Scanning.v2.gitlab-ci.yml
  - template: Jobs/Container-Scanning.gitlab-ci.yml
```

This enables selected repository and image scanners when their job rules and prerequisites are satisfied. It does not configure DAST because DAST needs a running target application.

## 2. Use a dedicated security stage

```yaml
stages:
  - build
  - security
  - deploy

include:
  - template: Jobs/SAST.gitlab-ci.yml
  - template: Jobs/Secret-Detection.gitlab-ci.yml
  - template: Jobs/Container-Scanning.gitlab-ci.yml

sast:
  stage: security

secret_detection:
  stage: security

container_scanning:
  stage: security
```

If using dependency scanning v2, configure its template stage input according to the current template documentation. Its resolution jobs may use a separate earlier stage.

## 3. SAST for supported source code

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml

sast:
  variables:
    SECURE_LOG_LEVEL: "info"
```

SAST analyzer jobs are selected according to supported languages, files, and template rules. A repository without supported source files may not produce a scan.

## 4. Secret detection

```yaml
include:
  - template: Jobs/Secret-Detection.gitlab-ci.yml
```

For a safe classroom demonstration, use an obviously fake string such as:

```text
TRAINING_TOKEN_NOT_REAL_1234567890
```

Do not create, commit, or share a real cloud key, password, personal access token, or private key. If a real secret is exposed, revoke and rotate it immediately.

## 5. Dependency scanning v2

```yaml
include:
  - template: Jobs/Dependency-Scanning.v2.gitlab-ci.yml
```

Add supported dependency manifests and lockfiles to the repository, such as a Python requirements file or supported package-manager lockfile. The scanner's supported ecosystems and behavior can change; consult the current GitLab documentation.

## 6. Container scanning

```yaml
include:
  - template: Jobs/Container-Scanning.gitlab-ci.yml

build_image:
  stage: build
  image: docker:27
  services:
    - name: docker:27-dind
      alias: docker
  variables:
    DOCKER_HOST: tcp://docker:2375
    DOCKER_TLS_CERTDIR: ""
  script:
    - docker build -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA" .
    - docker push "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"

container_scanning:
  variables:
    CS_IMAGE: "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"
  needs:
    - job: build_image
```

This is an illustrative pattern only. Docker-in-Docker configuration can require privileged runner settings and additional TLS/security controls. Prefer your organization's approved image build method. Confirm that the scanner job receives the image and registry credentials correctly.

## 7. DAST against a test target

```yaml
include:
  - template: Jobs/DAST.gitlab-ci.yml

variables:
  DAST_WEBSITE: "https://staging.example.test"
```

Replace the example URL with an application you own or are explicitly authorized to test. The target must be reachable from the runner. Use a dedicated staging environment, not a third-party or production system without explicit approval.

## 8. IaC scanning

```yaml
include:
  - template: Jobs/SAST-IaC.gitlab-ci.yml
```

Add supported Terraform, Kubernetes, or other infrastructure configuration files to the test repository. Review the current GitLab template name and supported file types before running.

## 9. Custom security report artifact

```yaml
custom_scan:
  image: alpine:3.20
  script:
    - mkdir -p reports
    - |
      cat > reports/example-report.json <<'JSON'
      {
        "training": true,
        "message": "Illustrative output only; not a GitLab security report schema"
      }
      JSON
  artifacts:
    paths:
      - reports/
```

This stores a generic artifact. It will not appear as a GitLab security finding because it is not a valid scanner report. A real integration must produce the required GitLab report schema and declare the correct `artifacts:reports` type.

## 10. Inspect scan artifacts

```yaml
inspect_artifact:
  image: alpine:3.20
  script:
    - echo "Open this job in GitLab and inspect its artifacts"
    - ls -la
```

For actual scanner jobs, open the job page and review its artifacts and report sections. Avoid copying sensitive source snippets or secrets into public issue trackers.

## 11. Custom security gate (illustrative policy logic)

```yaml
security_review:
  stage: test
  image: alpine:3.20
  script:
    - echo "Review scanner findings and documented risk acceptance"
    - echo "This placeholder does not parse or enforce a security report"
  allow_failure: false
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

A real security gate must parse validated reports or use supported GitLab approval/policy features. Do not claim that this placeholder blocks vulnerabilities.

## 12. Run scans only on relevant pipeline types

```yaml
security_inventory:
  image: alpine:3.20
  stage: test
  script:
    - echo "Security checks for branch or merge request"
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

This is a custom example job, not a replacement for the rules inside GitLab's scanner templates. Confirm scanner support for merge request pipelines and avoid unintentionally excluding required scans.
