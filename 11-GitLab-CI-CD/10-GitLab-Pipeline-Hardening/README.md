# GitLab Pipeline Hardening

A practical learning module for securing GitLab CI/CD pipelines against credential theft, untrusted code execution, supply-chain compromise, unauthorized deployment, and tampering.

## Learning objectives

By the end of this module, you should be able to:

- Explain the threat model of a CI/CD pipeline and identify high-value assets.
- Protect CI/CD variables and use an external secrets manager where appropriate.
- Separate untrusted merge-request workloads from protected deployment workloads.
- Apply least privilege to `CI_JOB_TOKEN`, deploy credentials, and runner access.
- Pin container images, dependencies, and included pipeline configuration.
- Protect `.gitlab-ci.yml` and shared pipeline components through review.
- Harden logs, artifacts, caches, and network communication.
- Add security checks and controlled deployment gates.
- Validate hardening controls with safe negative tests.

## 1. Pipeline threat model

A GitLab job executes repository-controlled commands. Treat every job as code execution with the permissions of its runner, token, network path, and injected variables.

| Asset | Example threat | Primary control |
|---|---|---|
| Secrets | Token printed or exfiltrated | External secret manager, masked/hidden/protected variables |
| Runner host | Malicious job compromises shared host | Ephemeral, isolated, scoped runners |
| Build artifact | Artifact replaced or poisoned | Provenance, immutable promotion, checksums |
| Pipeline definition | Attacker changes `.gitlab-ci.yml` | CODEOWNERS, protected branches, approvals |
| Production | Unauthorized deployment | Protected environment and approval rules |
| Dependencies | Mutable tag or compromised package | Lockfiles, hashes, pinned digests |
| Logs/cache | Sensitive data retained or exposed | Redaction, restricted access, cache separation |

## 2. Secure pipeline design

### 2.1 Trust boundaries

Use separate execution paths for:
- Untrusted merge requests and fork contributions.
- Trusted branch builds after review.
- Release/signing jobs.
- Production deployment jobs.

Do not expose production secrets or privileged runners to unreviewed code. Runner tags alone are not an authorization boundary; configure runner protection, project/group scope, executor isolation, and network controls.

### 2.2 Secrets

Prefer an external secrets manager for high-value credentials. If CI/CD variables are necessary:
- Mark secrets **masked** and **hidden** where supported.
- Mark them **protected** so they are available only to protected refs.
- Scope them to the smallest practical environment.
- Use short-lived credentials and rotate them.
- Never echo secrets, enable shell tracing around them, or place them in artifacts.
- Remember masking is not a guarantee against malicious code that can read a secret.

Example variable names (configure values in GitLab settings; never commit real values):
- `STAGING_DEPLOY_TOKEN`
- `PRODUCTION_DEPLOY_TOKEN`
- `CLOUD_ROLE_ARN`

### 2.3 Token and permission minimization

- Restrict `CI_JOB_TOKEN` inbound access to only required projects.
- Use the narrowest job-token allowlist and API scopes available.
- Avoid personal access tokens for automation when a job token or workload identity works.
- Give each job only the permissions it needs.
- Do not pass a powerful token to build, test, lint, or untrusted jobs.

### 2.4 Runner isolation

- Use ephemeral runners for untrusted workloads where possible.
- Separate runners by trust level and workload.
- Avoid privileged Docker mode unless there is a documented, reviewed requirement.
- Do not share persistent workspaces between mutually untrusted projects.
- Patch runner hosts and executors; restrict outbound network access.
- Keep runner registration and authentication tokens confidential.

## 3. Supply-chain integrity

### Pin images by digest

Prefer:
```yaml
image: python:3.12.7@sha256:<VERIFIED_DIGEST>
```
The digest above is a placeholder. Obtain the real digest from a trusted registry and verify it. Do not copy a fabricated digest.

Avoid mutable references such as `latest` for production pipelines.

### Lock dependencies

- Node.js: `npm ci` with a committed lockfile.
- Python: pinned requirements and hashes (`pip install --require-hashes`).
- Go: commit `go.sum` and run `go mod verify`.
- Use trusted registries and verify downloaded tool checksums.

### Pin included CI configuration

Use a reviewed commit SHA or protected version tag for remote project includes and components. Avoid unpinned remote includes in security-critical pipelines.

## 4. Example hardened `.gitlab-ci.yml`

This is a teaching template. Replace placeholder image digests and deployment commands with verified organization-specific values. Configure protected variables, runners, branches, and environments in GitLab settings as well.

```yaml
stages:
  - validate
  - test
  - security
  - package
  - deploy

default:
  interruptible: true
  retry:
    max: 1
    when:
      - runner_system_failure

workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH'

validate:
  stage: validate
  image: python:3.12.7
  script:
    - python --version
    - python -m compileall -q .
  rules:
    - if: '$CI_PIPELINE_SOURCE'

unit_tests:
  stage: test
  image: python:3.12.7
  script:
    - python -m pip install --requirement requirements.txt
    - python -m pytest -q
  rules:
    - if: '$CI_PIPELINE_SOURCE'

secret_detection_review:
  stage: security
  image: alpine:3.20
  script:
    - echo "Run an approved secret scanner here; do not print secret values."
  rules:
    - if: '$CI_PIPELINE_SOURCE'

package:
  stage: package
  image: alpine:3.20
  script:
    - mkdir -p dist
    - tar -czf "dist/source-${CI_COMMIT_SHA}.tar.gz" .
    - sha256sum "dist/source-${CI_COMMIT_SHA}.tar.gz" > dist/SHA256SUMS
  artifacts:
    paths:
      - dist/
    expire_in: 7 days
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

deploy_production:
  stage: deploy
  image: alpine:3.20
  environment:
    name: production
  resource_group: production
  script:
    - test -n "$PRODUCTION_DEPLOY_TOKEN"
    - echo "Invoke your approved deployment client without printing credentials."
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual
```

**Important:** This YAML alone does not secure the project. The production variable must be protected and environment-scoped; the default branch must be protected; production must be a protected environment; and deployment must run on an appropriately isolated protected runner. Replace floating image tags with verified digest-pinned references for production use.

## 5. Pipeline definition and repository controls

- Protect the default and release branches.
- Require merge-request review and successful required pipelines.
- Add `CODEOWNERS` rules for `.gitlab-ci.yml`, `ci/`, deployment manifests, and reusable pipeline templates.
- Require appropriate approval for changes to pipeline/security configuration.
- Protect release tags and container registry tags.
- Restrict who can change CI/CD settings, variables, runners, and protected environments.
- Audit changes to pipeline configuration and access permissions.

Example `CODEOWNERS`:
```text
/.gitlab-ci.yml       @platform-security
/ci/                  @platform-security
/deploy/              @release-engineering
```
Replace team handles with real GitLab groups/users in your project.

## 6. Logs, artifacts, caches, and network

- Do not print environment variables or enable `set -x` in secret-bearing jobs.
- Ensure logs do not contain credentials, authorization headers, private keys, or sensitive command arguments.
- Restrict artifact access and set short retention for sensitive outputs.
- Never store secrets in caches or artifacts.
- Separate caches for protected and unprotected refs; use trusted cache writers.
- Use TLS 1.2 or newer for external communication and validate certificates.
- Apply outbound network allowlists where practical.
- Keep audit logs and review unusual pipeline, runner, and token activity.

## 7. Security validation checklist

- [ ] Protected branches and tags are configured.
- [ ] Pipeline configuration changes require review.
- [ ] Production variables are protected, hidden/masked, and environment-scoped.
- [ ] High-value secrets are retrieved from a secrets manager where feasible.
- [ ] Untrusted merge requests cannot access production secrets or privileged runners.
- [ ] Runners are isolated, patched, and scoped.
- [ ] Job-token access is allowlisted narrowly.
- [ ] Images and included configurations are pinned to immutable references.
- [ ] Dependencies are locked and integrity-checked.
- [ ] Production is a protected environment with approval controls.
- [ ] Artifacts and caches have appropriate access and retention.
- [ ] Logs are checked for accidental secret disclosure.
- [ ] Security scans run and findings have an owner and remediation path.

## 8. Further reading

- [GitLab Pipeline security](https://docs.gitlab.com/ci/pipeline_security/)
- [GitLab CI/CD hardening recommendations](https://docs.gitlab.com/security/hardening_cicd_recommendations/)
- [GitLab runner security](https://docs.gitlab.com/runner/security/)
- [GitLab hardening recommendations](https://docs.gitlab.com/security/hardening/)
- [OWASP CI/CD Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html)

## Lab safety

Perform exercises only in a project and runner environment you own or are authorized to administer. Use dummy credentials and harmless test jobs. Never attempt to exfiltrate real secrets or compromise shared runners.
