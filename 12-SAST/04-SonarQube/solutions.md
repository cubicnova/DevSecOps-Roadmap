# SonarQube — Solutions and Explanations

These are reference solutions. UI labels and feature availability can differ by SonarQube product, edition, and version.

## Solution 1 — Environment setup

Use an approved local or hosted deployment and follow the official requirements for the chosen release. For a disposable local lab, a container can be convenient, but production requires supported persistence, database configuration, backups, resource planning, access controls, and TLS.

Do not expose a default lab instance to the internet.

## Solution 2 — Project and token

1. Create a project in the SonarQube UI or onboard the repository.
2. Copy the exact project key.
3. Generate a token with only the required analysis permissions.
4. Store it in an environment variable or CI secret store.
5. Never commit it to Git.

Example local environment:
```bash
export SONAR_HOST_URL="https://sonarqube.example.com"
export SONAR_TOKEN="<SECRET_FROM_SECRET_STORE>"
```

The placeholder is not a usable token.

## Solution 3 — First analysis

Example `sonar-project.properties`:
```properties
sonar.projectKey=training-app
sonar.projectName=Training App
sonar.sources=src
sonar.tests=tests
sonar.sourceEncoding=UTF-8
```

Run:
```bash
sonar-scanner \
  -Dsonar.host.url="$SONAR_HOST_URL" \
  -Dsonar.token="$SONAR_TOKEN"
```

Confirm that the scanner completed submission and the server processed the analysis. A successful scanner upload does not necessarily mean the Quality Gate passed.

## Solution 4 — Coverage import

Python:
```bash
python -m pip install pytest coverage
coverage run -m pytest
coverage xml -o coverage.xml
```

Properties:
```properties
sonar.sources=src
sonar.tests=tests
sonar.python.coverage.reportPaths=coverage.xml
```

Run the scanner after generating the report. If coverage is missing, verify the report path relative to the scanner's working directory, the report format, and whether the report was generated before analysis.

## Solution 5 — Quality Profiles

A Quality Profile defines which language rules are active. Start with the built-in recommended profile, inspect rule descriptions, and test any customizations on representative code.

Avoid disabling rules simply to make the dashboard appear cleaner. Track the owner and reason for any exception.

## Solution 6 — Issues and Security Hotspots

For each finding:
- Read the rule description.
- Inspect the highlighted code and surrounding context.
- Determine whether the input is attacker-controlled.
- Identify the sensitive operation or sink.
- Check validation and mitigations.
- Reproduce safely if necessary.
- Fix confirmed issues and add regression tests.

A Security Hotspot requires review; it is not automatically a confirmed vulnerability.

## Solution 7 — Quality Gate

A Quality Gate consists of conditions on metrics and produces a pass/fail status. Start with the default Sonar way gate and inspect its actual conditions in your instance.

Example policy ideas for new code:
- No new high-severity issues according to the team's risk policy.
- Review all new Security Hotspots.
- Meet an agreed coverage threshold.
- Keep duplication below an agreed threshold.

Avoid copying thresholds without considering language, project size, test maturity, and the product's new-code definition.

## Solution 8 — GitLab CI integration

Example:
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
```

Configure `SONAR_TOKEN` as a protected secret variable. The scanner recognizes its supported token environment configuration. Do not echo it or add it to the command line. Pin the scanner image to a reviewed version or digest in production.

Ensure that untrusted pipelines cannot access protected credentials. Configure merge-request analysis only when supported by the SonarQube product/edition and your GitLab trust model.

## Solution 9 — Failing gate

A controlled failure can be demonstrated by introducing a known training issue or adjusting a test fixture so coverage drops below the lab threshold. Run analysis, record the Quality Gate status, remediate the change, and rerun.

Do not use real secrets or intentionally vulnerable production code. Ensure the gate is actually awaited by the scanner or reported to the CI system.

## Solution 10 — Analysis scope

Example:
```properties
sonar.sources=src
sonar.tests=tests
sonar.exclusions=**/generated/**,**/vendor/**
sonar.coverage.exclusions=**/tests/**
```

Source exclusions and coverage exclusions have different effects. Review the analyzed file list and ensure security-sensitive source code remains in scope.

## Solution 11 — Troubleshooting

| Problem | Likely cause | Resolution |
|---|---|---|
| Authentication error | Missing/invalid token | Check secret variable and token permission |
| Project key error | Wrong key or project absent | Confirm project key in UI |
| Server unreachable | DNS, firewall, proxy, TLS | Test network path and certificate |
| No files analyzed | Incorrect source path or exclusions | Verify working directory and paths |
| Coverage missing | Report absent or incorrect path | Generate report before scanner run |
| Git blame warning | Shallow clone | Fetch full history or configure Git depth |
| Gate not returned to CI | Wait/report integration not configured | Enable Quality Gate wait or CI integration |

Use debug logs only when needed and redact secrets and internal details before sharing.

## Solution 12 — Final workflow checklist

- [ ] SonarQube instance is supported and secured.
- [ ] Project key and scanner configuration are correct.
- [ ] Token is stored securely and least-privileged.
- [ ] Source and test paths are correct.
- [ ] Coverage reports are generated before analysis.
- [ ] Quality Profile is reviewed.
- [ ] Quality Gate policy is documented.
- [ ] New-code definition is understood.
- [ ] Security Hotspots are reviewed by a person.
- [ ] GitLab CI waits for or receives the Quality Gate result.
- [ ] Untrusted pipelines cannot access protected tokens.
- [ ] Exclusions are narrow and documented.
- [ ] Findings have owners and remediation plans.

## Example remediation report

| Finding | Risk | Action | Validation |
|---|---|---|---|
| Dynamic SQL construction | Injection risk | Use parameterized queries | Unit test and rescan |
| Missing test coverage | Reduced regression confidence | Add unit tests | Coverage report imported |
| New critical issue | Potential high impact | Fix code path | Gate passes after rescan |
| Unreviewed security hotspot | Unknown security impact | Review context and document decision | Hotspot status updated |
| Scanner token in repository | Credential exposure | Revoke and rotate token; move to CI secret | Search history and verify logs |

## Evaluation rubric

| Area | Marks |
|---|---:|
| Setup and project onboarding | 10 |
| Scanner configuration and analysis | 15 |
| Coverage integration | 10 |
| Quality Profiles and rules | 15 |
| Issues and Security Hotspots triage | 15 |
| Quality Gate configuration | 15 |
| GitLab CI integration and secret handling | 15 |
| Documentation and evidence | 5 |
| **Total** | **100** |

A strong submission demonstrates a repeatable scan, imported coverage, documented gate policy, secure CI token handling, and a controlled pass/fail pipeline result.
