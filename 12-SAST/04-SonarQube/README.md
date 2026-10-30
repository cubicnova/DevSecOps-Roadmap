# SonarQube — Static Code Analysis, Quality, and Security

SonarQube is a platform for continuous inspection of source code. It helps teams identify bugs, vulnerabilities, security hotspots, and maintainability issues through static analysis integrated into developer workflows and CI/CD pipelines.

This module introduces SonarQube architecture, project onboarding, scanner configuration, quality profiles, quality gates, security findings, test coverage, and GitLab CI integration.

## Learning objectives

By completing this module, you should be able to:

- Explain SonarQube components and the static-analysis workflow.
- Install or access a suitable SonarQube deployment and create a project.
- Configure project analysis with `sonar-project.properties`.
- Run analysis using SonarScanner CLI and build-tool scanners.
- Configure source, test, binary, and coverage report paths.
- Understand rules, quality profiles, issues, and security hotspots.
- Configure and interpret quality gates and new-code definitions.
- Integrate analysis with GitLab CI/CD using protected tokens.
- Triage findings and manage exclusions responsibly.
- Troubleshoot common scanner and pipeline failures.

## 1. SonarQube concepts

| Concept | Purpose |
|---|---|
| Project | A codebase or repository analyzed by SonarQube |
| Scanner | Tool that collects source and analysis data and submits it to the server |
| Rule | A code pattern or analysis condition that can raise an issue |
| Quality Profile | Set of active rules for a language |
| Issue | A detected bug, vulnerability, or maintainability problem |
| Security Hotspot | Security-sensitive code requiring human review to determine whether it is risky |
| Quality Gate | Pass/fail policy applied to analysis metrics |
| New Code | Code added or changed within the configured baseline |
| Measures | Metrics such as coverage, duplication, and issue counts |

A Quality Profile determines what rules are evaluated. A Quality Gate determines whether the analysis meets the project's acceptance criteria. They serve different purposes.

## 2. Architecture and analysis flow

Typical flow:

```text
Developer / CI pipeline
        |
        v
SonarScanner (CLI, Maven, Gradle, etc.)
        |
        | source files, metadata, test/coverage reports
        v
SonarQube Server or SonarQube Cloud
        |
        v
Analysis results, issues, measures, Quality Gate
        |
        v
Developer feedback / CI pipeline decision
```

The scanner performs analysis and submits a report. The server processes the report and calculates the final project measures and Quality Gate status.

## 3. Deployment options

Common choices include:
- **SonarQube Community Build:** self-managed community distribution.
- **SonarQube Server:** self-managed product with capabilities depending on edition.
- **SonarQube Cloud:** hosted service.

Feature availability differs by product, edition, version, and language. Confirm branch analysis, pull/merge request analysis, security analysis, and report features in the documentation for the deployment you use.

For a lab, use an approved local or hosted instance and follow the current system requirements. Do not expose an unauthenticated SonarQube server to the public internet.

## 4. Create a project and token

1. Sign in to the SonarQube instance.
2. Create a project or onboard a repository.
3. Record the project key and server URL.
4. Generate a project-scoped analysis token where supported.
5. Store the token as a secret in the CI platform.
6. Grant only the permissions required to submit analysis.

Never commit tokens to source control or include them in logs. Rotate tokens if they are exposed.

Example environment variables:
```bash
export SONAR_HOST_URL="https://sonarqube.example.com"
export SONAR_TOKEN="<STORE_IN_SECRET_MANAGER>"
```

Use a placeholder in documentation; never use a real token in a committed file.

## 5. SonarScanner CLI installation

Install the scanner using the current official installation instructions for your operating system and SonarQube version.

Verify:
```bash
sonar-scanner --version
```

Run analysis from the project root:
```bash
sonar-scanner \
  -Dsonar.projectKey=my-training-project \
  -Dsonar.sources=src \
  -Dsonar.host.url="$SONAR_HOST_URL" \
  -Dsonar.token="$SONAR_TOKEN"
```

Scanner command-line options can override project properties. Prefer environment variables or a secret manager for credentials.

## 6. Project configuration

Create `sonar-project.properties`:

```properties
sonar.projectKey=cubicnova-training-app
sonar.projectName=CubicNova Training App
sonar.projectVersion=1.0

sonar.sources=src
sonar.tests=tests
sonar.sourceEncoding=UTF-8

# Example coverage report path; generate the report before analysis.
sonar.python.coverage.reportPaths=coverage.xml
```

Notes:
- `sonar.projectKey` must be unique in the SonarQube instance.
- `sonar.sources` identifies production source files.
- `sonar.tests` identifies test files.
- Coverage report paths must match files generated by the test tool.
- Language-specific properties vary; consult the analyzer documentation.
- Avoid putting credentials in this file.

## 7. Example Python workflow

Install test and coverage tools:
```bash
python -m pip install pytest coverage
```

Run tests and create a coverage XML report:
```bash
coverage run -m pytest
coverage xml -o coverage.xml
```

Then run:
```bash
sonar-scanner
```

Example project layout:
```text
my-app/
├── src/
│   └── app.py
├── tests/
│   └── test_app.py
├── coverage.xml
└── sonar-project.properties
```

Coverage is imported from a report generated by the test tool; SonarQube does not generate unit-test coverage itself.

## 8. Quality Profiles

A Quality Profile is a language-specific collection of active rules. It controls which rules are applied during analysis.

Good practices:
- Start with the recommended built-in profile.
- Add custom rules only when they address a clear organizational requirement.
- Review rule changes with developers and security engineers.
- Avoid disabling rules simply to reduce issue counts.
- Test profile changes on representative projects before broad rollout.

## 9. Issues and Security Hotspots

Common issue categories:
- **Bugs:** code likely to behave incorrectly.
- **Vulnerabilities:** code with a potential security weakness.
- **Code Smells:** maintainability problems.
- **Security Hotspots:** security-sensitive code that requires review and a decision.

A hotspot is not automatically a confirmed vulnerability. Review the context, data flow, reachable paths, and mitigations. Record the review outcome and remediation when needed.

## 10. Quality Gates

A Quality Gate evaluates analysis metrics and returns a pass/fail status. It can be reported to CI and used to prevent unacceptable code from progressing.

The built-in **Sonar way** gate is a recommended baseline. Its conditions and availability can vary with product and version. Review the actual gate configured on your instance rather than assuming a fixed set of thresholds.

A practical rollout:
1. Start with the default gate on new code.
2. Establish a baseline for the main branch.
3. Agree on coverage, duplication, and issue thresholds.
4. Apply gates to merge requests or branches where supported.
5. Make remediation ownership clear.
6. Review exceptions periodically.

Focus on new code first instead of trying to remediate every legacy issue at once.

## 11. GitLab CI integration

Example `.gitlab-ci.yml` for a generic scanner image:

```yaml
stages:
  - test
  - quality

variables:
  GIT_DEPTH: "0"

sonarqube-check:
  stage: quality
  image: sonarsource/sonar-scanner-cli:latest
  script:
    - sonar-scanner
      -Dsonar.projectKey="$SONAR_PROJECT_KEY"
      -Dsonar.host.url="$SONAR_HOST_URL"
      -Dsonar.qualitygate.wait=true
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

Configure these as GitLab CI/CD variables:
- `SONAR_HOST_URL`
- `SONAR_TOKEN` (secret; masked/hidden and protected as appropriate)
- `SONAR_PROJECT_KEY`

The scanner uses the token from its supported environment/configuration mechanism; do not place the token in the command line or echo it. Confirm the scanner image tag exists and pin a reviewed version or digest in production instead of using `latest`.

Branch and merge-request analysis support depends on your SonarQube product/edition and GitLab integration configuration. Check the current documentation before relying on it.

## 12. Exclusions and scope

Use exclusions only for content that should genuinely not be analyzed, such as generated code or vendored dependencies.

Example:
```properties
sonar.exclusions=**/generated/**,**/vendor/**
sonar.coverage.exclusions=**/tests/**,**/migrations/**
```

Do not exclude security-sensitive source directories merely to make a Quality Gate pass. Keep exclusions documented and reviewed.

## 13. Troubleshooting

| Symptom | Checks |
|---|---|
| Authentication failed | Token value, token permissions, variable availability |
| Project not found | Exact project key and server URL |
| Scanner cannot connect | DNS, TLS certificate, proxy, firewall |
| No source files analyzed | `sonar.sources`, working directory, exclusions |
| Coverage shows 0% | Report generated, path correct, format supported |
| Quality Gate not awaited | `sonar.qualitygate.wait=true` and server processing |
| Shallow clone warning | Fetch full history or configure appropriate Git depth |
| Unsupported Java/runtime | Scanner and server compatibility requirements |

Read the complete scanner log, but redact tokens, internal endpoints, and sensitive file contents before sharing it.

## 14. Further reading

- [SonarQube documentation](https://docs.sonarsource.com/sonarqube-server/)
- [SonarScanner CLI](https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/sonarscanner/)
- [Analysis parameters](https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/analysis-parameters/)
- [Quality profiles](https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-quality-profiles/)
- [Quality gates](https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-quality-gates/)
- [GitLab CI/CD integration](https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/gitlab-integration/)

Use the platform only on repositories you own or are authorized to assess.
