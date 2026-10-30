# SAST CI/CD Integration — Solutions and Explanations

These are reference solutions. Scanner behavior, GitLab report ingestion, merge-request support, and available features vary by product, edition, version, and configuration.

## Solution 1 — Pipeline placement

A practical order is:
```text
validate → build/test → SAST → report/quality gate → package → approved deploy
```

Some scanners can run in parallel with unit tests when they do not depend on compiled output or coverage artifacts. Compiled-language analyzers may need a build job first. Choose stage placement based on scanner requirements.

## Solution 2 — GitLab-managed SAST

Add:
```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml
```

Validate the pipeline and inspect the jobs created. GitLab selects analyzers according to the template, language support, and repository contents. Merge-request scanning may require additional configuration. Review the current GitLab SAST documentation for the instance version and tier.

## Solution 3 — Semgrep integration

Example:
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

This creates a generic artifact. It does not automatically publish a native GitLab SAST report. For native ingestion, use the required GitLab security report schema and artifact declaration, or use GitLab's supported SAST integration.

To enforce findings, consider Semgrep's `--error` option after the ruleset and severity policy have been tested.

## Solution 4 — SonarQube integration

Example:
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

Configure:
- `SONAR_PROJECT_KEY`
- `SONAR_HOST_URL`
- `SONAR_TOKEN`

Keep the token in a protected, masked/hidden CI/CD variable as appropriate. Do not print it or commit it. Pin the scanner image to a reviewed version or digest.

## Solution 5 — Coverage integration

Generate coverage before the scanner runs:
```bash
coverage run -m pytest
coverage xml -o coverage.xml
```

Publish the file as an artifact if the scanner runs in a separate job. Configure the appropriate language-specific report path. Verify the scanner job downloads the artifact and that the path is correct.

## Solution 6 — CodeQL output

A typical process is:
1. Create a CodeQL database for the target language.
2. Run a supported query suite.
3. Produce SARIF output.
4. Upload SARIF using the supported platform integration.

Example analysis command:
```bash
codeql database analyze codeql-db <QUERY_SUITE> \
  --format=sarif-latest \
  --output=codeql-results.sarif
```

The query-suite placeholder must be replaced with a valid suite. Build requirements vary by language. A SARIF artifact stored in GitLab is not necessarily ingested into GitLab's security dashboard.

## Solution 7 — Merge-request trust boundaries

- Run scanners without secrets whenever possible.
- Do not expose production deployment credentials to untrusted code.
- Use protected variables only in jobs on appropriately protected refs.
- Use isolated runners for untrusted merge requests.
- Restrict job-token permissions.
- Keep deployment jobs separate and protected.

A masked variable is not a substitute for a trust boundary: malicious job code may still read and transmit a value available to that job.

## Solution 8 — Quality gate rollout

Recommended rollout:
1. Advisory scans.
2. Baseline existing findings.
3. Fix high-confidence critical issues.
4. Define blocking rules for new findings.
5. Assign remediation owners and due dates.
6. Test both pass and fail behavior.
7. Review exceptions and update rulesets regularly.

Do not block every pipeline on low-confidence findings without first understanding the noise and impact.

## Solution 9 — Report handling

| Format | Typical use |
|---|---|
| Text | Developer-readable console output |
| JSON | Custom automation and processing |
| SARIF | Standard static-analysis interchange |
| GitLab security report | Native GitLab security report ingestion |

A generic artifact path makes a report downloadable. Native dashboard ingestion requires the platform's supported schema and CI artifact declaration. Validate the resulting UI, not just the existence of a file.

## Solution 10 — Scanner versions and exclusions

- Pin versions or image digests for repeatability.
- Review scanner updates regularly.
- Use narrow exclusions for generated or irrelevant content.
- Document every exclusion and its owner.
- Confirm that sensitive source directories remain scanned.

GitLab SAST variables and exclusion behavior can vary by analyzer. Check the analyzer-specific documentation.

## Solution 11 — Performance

Good optimization steps:
- Use appropriate runner resources.
- Cache dependency downloads, not untrusted scan findings.
- Reuse build artifacts where required.
- Avoid duplicate scans unless they provide distinct coverage.
- Run independent scanners in parallel only if resources permit.
- Set realistic timeouts.
- Measure both duration and failure rate.

Do not reduce scan depth or exclude important directories solely to improve pipeline speed.

## Solution 12 — Final review checklist

- [ ] SAST runs on the intended branch and merge-request events.
- [ ] Scanner supports the repository's languages.
- [ ] Secrets are not exposed to untrusted jobs.
- [ ] Runner isolation matches the trust level.
- [ ] Scanner versions are reviewed and pinned appropriately.
- [ ] Reports are stored securely and ingested correctly.
- [ ] Quality-gate policy is documented.
- [ ] New findings have owners and remediation targets.
- [ ] Exclusions are narrow and reviewed.
- [ ] Scan duration and reliability are monitored.
- [ ] Exceptions have rationale and expiry.
- [ ] Pipeline configuration changes require review.

## Example remediation plan

| Priority | Finding | Action | Owner |
|---|---|---|---|
| P0 | Production token available to untrusted MR | Remove access; rotate token; isolate deploy job | Platform |
| P1 | SAST runs only on default branch | Add supported MR scan workflow | DevSecOps |
| P1 | Reports stored but not ingested | Use supported security report schema | CI owner |
| P1 | Floating scanner image tag | Pin reviewed version/digest | Platform |
| P2 | Excessive exclusions | Review and narrow patterns | AppSec |
| P2 | Findings have no owners | Define triage and remediation workflow | Engineering |

## Evaluation rubric

| Area | Marks |
|---|---:|
| Pipeline architecture and triggers | 10 |
| GitLab-managed SAST setup | 10 |
| Semgrep/SonarQube/CodeQL integration | 20 |
| Secrets and runner trust boundaries | 15 |
| Report formats and artifact handling | 15 |
| Quality gates and finding triage | 15 |
| Performance and scanner maintenance | 5 |
| Evidence and documentation | 10 |
| **Total** | **100** |

A strong submission demonstrates a working scan, safe credential handling, clear report handling, a documented policy, and evidence of both successful and failing test runs.
