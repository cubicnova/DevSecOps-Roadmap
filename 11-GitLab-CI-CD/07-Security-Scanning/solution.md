# GitLab Security Scanning — Solutions and Explanations

> These are reference solutions for a controlled lab. Scanner templates, supported languages, variables, and report formats change over time. Confirm the current GitLab documentation before adopting examples in production.

## 1. Enable SAST

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml
```

Push a branch containing supported source files. Inspect the generated SAST job and its artifacts.

**Explanation:** SAST analyzes supported source code without executing the application. A job may not run if the repository has no supported files or its rules do not match.

## 2. Safe SAST exercise

Use a deliberately vulnerable training sample, such as an unsafe SQL query in a local-only demo application. Run SAST and record the reported location, severity, and remediation guidance. Replace the unsafe query with parameterized queries and rescan.

**Explanation:** The goal is to understand the finding lifecycle, not to exploit a live system. Analyzer coverage and finding details depend on the language and scanner version.

## 3. Secret detection

```yaml
include:
  - template: Jobs/Secret-Detection.gitlab-ci.yml
```

Use only a fake marker string in a disposable repository. Review the scanner report and coverage mode.

**Explanation:** Secret detection coverage depends on pipeline type and analyzer behavior. If a real credential is exposed, revoke and rotate it immediately, assess access logs, and follow incident response. Removing the text from the latest version does not invalidate an exposed credential.

## 4. Historic secret detection
Pipeline secret detection commonly focuses on current repository state and commits in the relevant pipeline range. To identify older leaks, consult and run GitLab's supported historic scan workflow.

**Explanation:** A normal pipeline scan should not be assumed to audit every commit in the repository's full history. Check current version-specific documentation and record the scanned range.

## 5. Dependency scanning

```yaml
include:
  - template: Jobs/Dependency-Scanning.v2.gitlab-ci.yml
```

Add a supported manifest and lockfile, run the pipeline, and inspect package/version/advisory/fixed-version data where available. Upgrade the test dependency to a fixed release and rerun.

**Explanation:** Dependency scanning identifies known vulnerabilities in supported package ecosystems. Results depend on supported files, dependency resolution, advisory data, and scanner version.

## 6. Container scanning

```yaml
include:
  - template: Jobs/Container-Scanning.gitlab-ci.yml

container_scanning:
  variables:
    CS_IMAGE: "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"
```

Ensure the image has already been built and is accessible to the scanner job. For private registries, configure supported authentication variables securely.

**Explanation:** Container scanning analyzes the image's packages and operating-system components. A missing image, inaccessible registry, unsupported architecture, or missing runner prerequisites can prevent the scan.

## 7. DAST

```yaml
include:
  - template: Jobs/DAST.gitlab-ci.yml

variables:
  DAST_WEBSITE: "https://staging.example.test"
```

Replace the example URL with a target you own or are explicitly authorized to test. Confirm the runner can resolve and reach the target.

**Explanation:** DAST requires a running application. A syntactically valid URL is not enough if the service is unavailable, blocked by network policy, or requires additional authentication configuration.

## 8. IaC scanning

Use the current GitLab IaC scanning template documented for your GitLab version. Add supported Terraform, Kubernetes, or other infrastructure configuration files and scan them in a non-deployable lab repository.

**Explanation:** IaC scanning identifies risky configuration patterns before infrastructure is deployed. Template names and supported file types should be checked against current docs.

## 9. Security reports

A custom job can preserve arbitrary output:

```yaml
custom_output:
  image: alpine:3.20
  script:
    - mkdir -p reports
    - echo '{"training":true}' > reports/output.json
  artifacts:
    paths:
      - reports/
```

This is a generic artifact, not a GitLab security report. A custom scanner integration must generate the exact supported schema and declare it with the matching `artifacts:reports` type.

**Explanation:** GitLab uses the report declaration and schema to process findings. A filename alone does not establish report type or validity.

## 10. Custom security stage

```yaml
stages:
  - build
  - security
  - deploy

include:
  - template: Jobs/SAST.gitlab-ci.yml
  - template: Jobs/Secret-Detection.gitlab-ci.yml

sast:
  stage: security

secret_detection:
  stage: security
```

For dependency scanning v2, use its documented `stage` input and account for its resolution jobs' stage behavior. Validate the complete merged configuration using GitLab CI Lint.

**Explanation:** Defining a `security` stage does not automatically move included scanner jobs into it. Each included job must be configured as documented.

## 11. Triage example

| Field | Example action |
|---|---|
| Finding | Vulnerable dependency in a service |
| Severity | Record scanner severity and validate context |
| Exposure | Determine whether the vulnerable component is deployed and reachable |
| Fix | Upgrade to a fixed compatible version |
| Owner | Assign to the component maintainer |
| Verification | Run dependency scanning again and confirm the finding is resolved |
| Risk acceptance | Document rationale, compensating controls, owner, and review date |

**Explanation:** Prioritize using severity, exploitability, reachability, exposure, business impact, and fix availability. Do not suppress a finding merely to make the pipeline green.

## 12. Troubleshooting

| Symptom | Likely cause | Recommended action |
|---|---|---|
| Scanner job missing | Template omitted, rules exclude job, unsupported files, workflow rules, or feature availability | Inspect merged CI config, job rules, supported files, and project configuration |
| Missing stage error | Scanner job uses a stage not declared in `stages` | Add the stage or override the scanner job's stage |
| Container image pull fails | Wrong image reference, registry credentials, or network issue | Verify image tag/digest, registry permissions, and runner connectivity |
| DAST cannot reach target | Target down, DNS/TLS issue, firewall, or runner network isolation | Check reachability from runner and target readiness |
| Older secret not found | Historic repository history was not scanned | Use the documented historic scan workflow |
| No findings | No issue detected, unsupported file, scan not executed, or coverage limitation | Verify job logs, supported inputs, and report artifact before concluding |
| Report not displayed | Wrong schema/type, missing `artifacts:reports`, or unsupported UI feature | Validate report format and declaration; check GitLab version/tier |

## Key concepts — viva answers
1. **Security scanning:** Automated analysis to identify vulnerabilities and misconfigurations during software delivery.
2. **SAST vs DAST:** SAST analyzes source code; DAST tests a running application from the outside.
3. **Dependency scanning:** Identifies known vulnerabilities in third-party packages.
4. **Secret detection:** Finds exposed credentials that could enable unauthorized access.
5. **IaC scanning:** Reviews infrastructure configuration for insecure settings.
6. **Container scanning:** Identifies known vulnerabilities in image packages and OS components.
7. **Security report artifact:** A structured report in a supported schema, declared with `artifacts:reports`.
8. **Missing scanner job:** Template, rules, workflow, supported file, feature, or stage configuration issue.
9. **Authorized DAST target:** Prevents unauthorized testing and unintended impact on third-party or production services.
10. **Real leaked secret:** Revoke/rotate it immediately, investigate possible use, and follow incident response.
11. **Successful scan:** Does not prove the application is secure; scanners have coverage and detection limitations.
12. **Prioritization:** Consider severity, exploitability, exposure, reachability, business impact, and remediation availability.

## Further reading
- [GitLab security scanning overview](https://docs.gitlab.com/user/application_security/detect/)
- [Security configuration](https://docs.gitlab.com/user/application_security/detect/security_configuration/)
- [Pipeline secret detection](https://docs.gitlab.com/user/application_security/secret_detection/pipeline/)
- [Container scanning](https://docs.gitlab.com/user/application_security/container_scanning/)
