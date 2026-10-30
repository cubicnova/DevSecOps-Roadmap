# SAST CI/CD Integration

This module explains how to integrate Static Application Security Testing (SAST) into Continuous Integration and Continuous Delivery (CI/CD) workflows. The goal is to make security analysis repeatable, visible, and actionable without exposing credentials or slowing delivery unnecessarily.

The examples focus on GitLab CI/CD and common SAST tools such as Semgrep, SonarQube, and CodeQL. Tool capabilities, report formats, licensing, and merge-request features vary by product and version; verify the current documentation before production use.

## Learning objectives

By completing this module, you should be able to:

- Explain where SAST fits in a CI/CD pipeline.
- Design a pipeline with validation, tests, SAST, reporting, and deployment stages.
- Integrate Semgrep, SonarQube, and CodeQL in CI.
- Handle tokens and credentials securely.
- Run scans on merge requests and protected branches with appropriate trust boundaries.
- Publish reports in machine-readable formats such as SARIF or GitLab security reports.
- Configure quality gates and severity-based pipeline policies.
- Manage scan exclusions, performance, caching, and analyzer versions.
- Triage findings and create a remediation workflow.
- Monitor scan coverage and continuously improve the integration.

## 1. Where SAST fits in CI/CD

A secure delivery workflow can include:

```text
Developer commit / merge request
              |
              v
        Validate pipeline
              |
              v
       Build and unit tests
              |
              v
       SAST / code analysis
              |
              v
    Parse and publish findings
              |
              v
       Review / quality gate
              |
       +------+------+
       |             |
      Pass          Fail
       |             |
       v             v
  Package/release  Remediate
       |
       v
  Deploy with approval
```

SAST should run early enough to give developers useful feedback, and its findings should be routed to people who can fix them. A scan that runs but is never reviewed is not an effective security control.

## 2. Integration design decisions

Before adding a scanner, decide:

1. **Trigger:** push, merge request, default branch, scheduled pipeline, or release.
2. **Scope:** all source files, changed files, or selected languages.
3. **Tool:** GitLab-managed SAST, Semgrep, SonarQube, CodeQL, or another approved scanner.
4. **Output:** console logs, JSON, SARIF, or GitLab security report format.
5. **Policy:** informational, warning, or blocking.
6. **Credentials:** which jobs need tokens and under what trust conditions.
7. **Ownership:** who triages findings and tracks remediation.
8. **Performance:** time limits, caching, parallelization, and runner resources.

Avoid running overlapping scanners without a reason. Duplicate findings can increase noise and reduce developer trust.

## 3. GitLab-managed SAST template

The simplest GitLab SAST integration uses the maintained template:

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml
```

The template adds analyzer jobs based on supported languages and configuration. Review the generated pipeline and the GitLab version/tier requirements. GitLab documents default branch-pipeline behavior and additional configuration for merge-request pipelines.

If you define custom stages, ensure the stages required by the included template exist. Validate template changes in a merge request before merging them into the default branch.

## 4. Standalone Semgrep integration

A simple CLI job:

```yaml
stages:
  - test
  - security

semgrep:
  stage: security
  image: semgrep/semgrep
  script:
    - semgrep scan --config auto --json --output semgrep.json .
  artifacts:
    when: always
    paths:
      - semgrep.json
    expire_in: 7 days
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH'
```

This example saves JSON as an artifact; it does not automatically make the JSON appear as a GitLab SAST security report. GitLab's security report ingestion expects the documented report schema. Use a supported integration or convert results with a validated converter.

To make findings fail the job, Semgrep supports options such as `--error`; define a policy and test it before enabling blocking behavior.

## 5. SonarQube integration

Example SonarScanner CLI job:

```yaml
stages:
  - test
  - quality

variables:
  GIT_DEPTH: "0"

sonarqube:
  stage: quality
  image: sonarsource/sonar-scanner-cli:latest
  script:
    - sonar-scanner
      -Dsonar.projectKey="$SONAR_PROJECT_KEY"
      -Dsonar.host.url="$SONAR_HOST_URL"
      -Dsonar.qualitygate.wait=true
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

Configure `SONAR_PROJECT_KEY`, `SONAR_HOST_URL`, and `SONAR_TOKEN` in GitLab CI/CD settings. Use masked/hidden and protected settings appropriate to the project trust model. SonarScanner supports token authentication through its documented configuration; do not print or commit the token.

Pin a reviewed scanner image version or digest in production. Merge-request and branch analysis support depends on SonarQube product, edition, and integration setup.

## 6. CodeQL integration concepts

CodeQL analysis typically involves:
1. Installing or invoking the CodeQL CLI or supported CI action.
2. Creating a CodeQL database for the target language.
3. Running approved query suites.
4. Producing SARIF output.
5. Uploading SARIF to a supported code-scanning platform.

CodeQL workflows and upload capabilities depend on the hosting platform and repository configuration. Do not assume that a SARIF artifact is automatically ingested by GitLab. Confirm supported upload paths and permissions for your platform.

## 7. Secure merge-request pipelines

Merge-request pipelines may execute code contributed by users who should not receive protected credentials.

Controls:
- Do not expose production secrets to untrusted merge requests or forks.
- Use protected variables only on appropriately protected refs and jobs.
- Separate untrusted validation jobs from trusted release jobs.
- Avoid privileged runners for untrusted code.
- Limit job-token permissions and project access.
- Review pipeline configuration changes.
- Use short-lived tokens and external secret managers where practical.

A scanner that needs no credential should generally run without one. If a token is required, give it only to the job and pipeline contexts that need it.

## 8. Reports and artifacts

Common output types:
- **Text:** convenient for local debugging.
- **JSON:** useful for custom processing.
- **SARIF:** standardized static-analysis interchange format.
- **GitLab security report:** GitLab-specific schema used by supported security report features.

Keep these distinctions clear. Saving a JSON or SARIF file as a generic artifact is not the same as publishing a GitLab SAST report.

Example artifact retention:
```yaml
artifacts:
  when: always
  paths:
    - semgrep.json
  expire_in: 7 days
```

Reports may contain source paths and code excerpts. Restrict artifact access and retention based on the sensitivity of your repository.

## 9. Quality gates and blocking policy

A staged rollout is often safer than immediately failing every pipeline:
1. Run scans in report-only mode.
2. Establish a baseline and identify noisy rules.
3. Fix high-confidence critical issues.
4. Define which new findings block a merge.
5. Assign owners and remediation SLAs.
6. Review exceptions and suppressions periodically.
7. Expand policy after measuring impact.

Prefer gating on new findings rather than requiring a large legacy codebase to become clean in one change. Do not silently suppress findings to achieve green pipelines.

## 10. Performance and reliability

- Use appropriate runner CPU and memory.
- Cache dependencies, not untrusted generated scan results.
- Avoid sharing sensitive caches across trust boundaries.
- Limit scans to supported source code, but keep exclusions narrow.
- Pin scanner images for repeatability; update them through a reviewed process.
- Use full Git history when a scanner or analysis mode needs blame/diff data.
- Set realistic job timeouts.
- Run analyzers in parallel only when runner capacity permits.
- Retain reports long enough for review, but not indefinitely.

## 11. Example combined pipeline

This is a teaching template. In a real project, choose a single primary SAST integration or intentionally manage overlap. Pin all images to reviewed versions/digests.

```yaml
stages:
  - validate
  - test
  - security
  - quality

validate:
  stage: validate
  image: alpine:3.20
  script:
    - test -f .gitlab-ci.yml

unit_tests:
  stage: test
  image: python:3.12
  script:
    - python -m pip install -r requirements.txt
    - python -m pytest -q

semgrep:
  stage: security
  image: semgrep/semgrep
  script:
    - semgrep scan --config auto --json --output semgrep.json .
  artifacts:
    when: always
    paths:
      - semgrep.json
    expire_in: 7 days
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH'

sonarqube:
  stage: quality
  image: sonarsource/sonar-scanner-cli
  script:
    - sonar-scanner
      -Dsonar.projectKey="$SONAR_PROJECT_KEY"
      -Dsonar.host.url="$SONAR_HOST_URL"
      -Dsonar.qualitygate.wait=true
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

This template assumes the variables are configured securely and that the selected scanner versions and image tags are valid. Do not copy it into production without reviewing trust boundaries, tool overlap, and report handling.

## 12. Metrics for an effective SAST program

Useful measures include:
- Percentage of repositories with SAST enabled.
- Percentage of active branches or merge requests scanned.
- Scan success rate and median scan duration.
- New findings by severity and confidence.
- Mean time to triage and remediate.
- Reopened findings and recurrence rate.
- False-positive and accepted-risk rates.
- Percentage of findings with assigned owners.

Avoid using raw finding counts as the only measure of security performance.

## 13. Further reading

- [GitLab SAST documentation](https://docs.gitlab.com/user/application_security/sast/)
- [GitLab security scanning detection](https://docs.gitlab.com/user/application_security/detect/)
- [GitLab security scanner integration](https://docs.gitlab.com/development/integrations/secure/)
- [Semgrep CI documentation](https://semgrep.dev/docs/semgrep-ci/overview/)
- [SonarQube GitLab integration](https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/gitlab-integration/)
- [CodeQL documentation](https://codeql.github.com/docs/)
- [SARIF specification](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html)

Perform all exercises in repositories and CI environments you own or are authorized to test.
