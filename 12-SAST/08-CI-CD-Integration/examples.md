# SAST CI/CD Integration — Examples

These are teaching templates. Verify tool versions, supported report formats, runner requirements, and licensing before production use.

## 1. GitLab-managed SAST

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml
```

GitLab selects applicable analyzers based on supported languages and template rules. Review the generated jobs and configure merge-request scanning where supported and required.

## 2. Semgrep scan with JSON artifact

```yaml
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
```

This publishes a generic job artifact. It is not automatically a GitLab SAST report unless converted to the required schema and declared using the supported report artifact type.

## 3. Semgrep blocking mode

```yaml
semgrep:
  stage: security
  image: semgrep/semgrep
  script:
    - semgrep scan --config auto --error .
```

`--error` can make findings fail the job. Test the behavior and ruleset first. A staged policy may be better than blocking on every informational or low-confidence result.

## 4. SonarQube scanner job

```yaml
sonarqube:
  stage: quality
  image: sonarsource/sonar-scanner-cli
  variables:
    GIT_DEPTH: "0"
  script:
    - sonar-scanner
      -Dsonar.projectKey="$SONAR_PROJECT_KEY"
      -Dsonar.host.url="$SONAR_HOST_URL"
      -Dsonar.qualitygate.wait=true
```

Configure `SONAR_PROJECT_KEY`, `SONAR_HOST_URL`, and `SONAR_TOKEN` securely in CI/CD settings. Do not echo secrets or place them in committed files. Pin a reviewed scanner image version or digest.

## 5. Python test and coverage before analysis

```yaml
python_tests:
  stage: test
  image: python:3.12
  script:
    - python -m pip install pytest coverage
    - coverage run -m pytest
    - coverage xml -o coverage.xml
  artifacts:
    when: always
    paths:
      - coverage.xml
    expire_in: 7 days
```

A later SonarQube job can import the report if configured with the correct language-specific coverage property and if the report is available in that job.

## 6. CodeQL workflow concept

A CodeQL workflow generally:
- Initializes CodeQL for one or more supported languages.
- Builds or autobuilds the application where required.
- Runs a query suite.
- Produces SARIF.
- Uploads results to a supported code-scanning platform.

Example command concepts:
```bash
codeql database create codeql-db --language=python
codeql database analyze codeql-db <QUERY_SUITE> \
  --format=sarif-latest \
  --output=codeql-results.sarif
```

`<QUERY_SUITE>` is a placeholder; use a valid query suite for the CodeQL version and language. Database creation options depend on the language and build mode. Do not assume GitLab will ingest the SARIF file automatically.

## 7. Run on merge requests and branches

```yaml
semgrep:
  stage: security
  image: semgrep/semgrep
  script:
    - semgrep scan --config auto .
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH'
```

Check whether the rules create duplicate pipelines for your project. Configure merge-request pipeline behavior deliberately.

## 8. Keep production credentials out of untrusted scans

```yaml
untrusted_sast:
  stage: security
  image: semgrep/semgrep
  script:
    - semgrep scan --config auto .
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

This job does not need a production credential. If a scanner requires an API token, use a separate trusted job or a narrowly scoped token with an explicit trust model.

## 9. Pin a scanner image

Illustrative:
```yaml
semgrep:
  image: semgrep/semgrep:<REVIEWED_VERSION>
  script:
    - semgrep scan --config auto .
```

Replace the placeholder with a verified version or digest. Avoid using floating tags such as `latest` for repeatable production scans.

## 10. Narrow scan exclusions

```yaml
variables:
  SAST_EXCLUDED_PATHS: "spec,tests,tmp,generated"
```

Exclusion behavior varies by analyzer. Keep exclusions narrow, review them, and confirm that security-sensitive application code remains in scope.

## 11. Conditional scan by source files

```yaml
semgrep:
  stage: security
  image: semgrep/semgrep
  script:
    - semgrep scan --config auto .
  rules:
    - exists:
        - "**/*.py"
        - "**/*.js"
        - "**/*.ts"
```

Ensure the file patterns cover the languages and extensions in the repository. The scanner itself may have additional language and file-size limits.

## 12. Publish SARIF as a generic artifact

```yaml
codeql-report:
  stage: security
  script:
    - codeql database analyze codeql-db <QUERY_SUITE> --format=sarif-latest --output=codeql-results.sarif
  artifacts:
    when: always
    paths:
      - codeql-results.sarif
    expire_in: 7 days
```

A generic artifact makes the file downloadable. It does not by itself upload the findings into a platform's security dashboard.

## 13. Use `allow_failure` deliberately

```yaml
semgrep_advisory:
  stage: security
  image: semgrep/semgrep
  script:
    - semgrep scan --config auto .
  allow_failure: true
```

This is appropriate only during an explicitly time-bounded advisory rollout. Document the owner and date to move to enforcement. Do not leave security checks advisory indefinitely.

## 14. Simple finding triage record

```text
Finding ID:
Scanner / rule:
File and line:
Source:
Sink:
Severity and confidence:
Reachability:
Existing mitigation:
Decision: Fix / False positive / Accepted risk
Remediation owner:
Due date:
Validation evidence:
```
