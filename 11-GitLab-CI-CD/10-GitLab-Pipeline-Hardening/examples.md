# GitLab Pipeline Hardening — Examples

Examples are educational templates. Replace placeholders, verify image digests, and configure GitLab project settings before using in production.

## 1. Safe defaults and workflow rules

```yaml
default:
  interruptible: true
  retry:
    max: 1
    when: runner_system_failure

workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH'
```

Avoid broad rules that unintentionally run deployment jobs for untrusted refs.

## 2. Protected production deployment

```yaml
deploy_production:
  stage: deploy
  image: alpine:3.20
  environment:
    name: production
  resource_group: production
  script:
    - test -n "$PRODUCTION_DEPLOY_TOKEN"
    - ./scripts/deploy.sh
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual
```

Configure `production` as a protected environment, restrict who can deploy, and require approvals where supported. Store the token as a protected, masked/hidden, environment-scoped variable or use an external secrets manager.

## 3. Do not expose secrets in logs

Unsafe:
```yaml
debug:
  script:
    - env
    - echo "$DEPLOY_TOKEN"
    - set -x
```

Safer:
```yaml
deploy:
  script:
    - test -n "$DEPLOY_TOKEN"
    - ./deploy-client --token-stdin < <(printf '%s' "$DEPLOY_TOKEN")
```

The exact secure input mechanism depends on the deployment client. Avoid putting credentials in command-line arguments because process listings and logs may expose them.

## 4. Locked Python dependencies

```yaml
python_tests:
  image: python:3.12.7
  script:
    - python -m pip install --require-hashes -r requirements.txt
    - python -m pytest -q
```

The requirements file must pin versions and include hashes for all packages and platform variants used.

## 5. Locked Node.js dependencies

```yaml
node_tests:
  image: node:22.11.0
  script:
    - npm ci
    - npm test
```

Commit `package-lock.json`; `npm ci` fails when the lockfile and package manifest are inconsistent.

## 6. Pin a shared pipeline include

```yaml
include:
  - project: "platform/ci-templates"
    ref: "0123456789abcdef0123456789abcdef01234567"
    file: "/templates/security.yml"
```

The SHA is illustrative. Replace it with the reviewed commit SHA from the trusted template repository.

## 7. Narrow job-token access

Configure the CI job token allowlist in project settings so only explicitly approved projects can access the target project. Do not assume a YAML setting alone enforces every inbound access policy.

A useful review record:
```text
Consumer project: group/application
Target project: group/deployment-config
Required operation: read one repository
Reason: deployment configuration retrieval
Review date: YYYY-MM-DD
Owner: platform team
```

## 8. Separate untrusted and protected workloads

```yaml
untrusted_validation:
  stage: test
  tags:
    - isolated-untrusted
  script:
    - ./scripts/test.sh
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'

trusted_release:
  stage: deploy
  tags:
    - protected-release
  environment:
    name: production
  script:
    - ./scripts/release.sh
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual
```

Runner tags are selectors, not sufficient security by themselves. Mark the release runner protected, restrict its project scope, isolate its executor, and protect the environment and branch.

## 9. Create a checksum for an artifact

```yaml
package:
  stage: package
  image: alpine:3.20
  script:
    - tar -czf application.tar.gz app/
    - sha256sum application.tar.gz > SHA256SUMS
  artifacts:
    paths:
      - application.tar.gz
      - SHA256SUMS
    expire_in: 7 days
```

A checksum detects accidental corruption when compared with a trusted checksum; it does not establish authenticity if an attacker can replace both files.

## 10. Security scan placeholder

```yaml
security_review:
  stage: security
  script:
    - echo "Run approved SAST, dependency, container, and secret scanning tools."
  allow_failure: false
```

Replace the placeholder with scanners supported by your GitLab tier and organization. Define severity thresholds, exception approval, and remediation ownership.

## 11. CODEOWNERS example

```text
/.gitlab-ci.yml       @platform-security
/ci/                  @platform-security
/deploy/              @release-engineering
```

Enable the corresponding approval rules and ensure the named owners are valid project members.

## 12. Secret-safe diagnostic output

```yaml
diagnostics:
  script:
    - echo "Job: $CI_JOB_NAME"
    - echo "Commit: $CI_COMMIT_SHA"
    - echo "Environment: ${CI_ENVIRONMENT_NAME:-not-set}"
    - test -n "$DEPLOY_TOKEN" && echo "Deployment credential is configured"
```

Do not print `env`, `printenv`, secret values, full HTTP headers, or shell traces in jobs that receive credentials.
