# GitLab CI/CD — Security Scanning

## Overview
Security scanning integrates automated security checks into the software delivery pipeline. GitLab provides scanners and CI/CD templates for source code, dependencies, secrets, infrastructure definitions, container images, and running applications.

Security scanning helps identify issues early, but it does not replace secure design, code review, manual testing, or a complete penetration test.

## Learning objectives
- Explain the purpose of security scanning in CI/CD.
- Differentiate SAST, DAST, dependency scanning, secret detection, IaC scanning, and container scanning.
- Enable GitLab security scanners with CI/CD templates.
- Understand security report artifacts and pipeline results.
- Configure scan stages and rules.
- Interpret findings and prioritize remediation.
- Apply safe testing practices and protect credentials.
- Troubleshoot scanners that do not run or produce reports.

## Security scanning types

| Scan type | What it examines | Typical finding |
|---|---|---|
| SAST | Source code without running the application | Injection risks, insecure functions, weak validation |
| DAST | A running application from the outside | Reflected XSS, insecure headers, exposed endpoints |
| Dependency scanning | Third-party libraries and packages | Vulnerable package versions |
| Secret detection | Repository content and commits | API keys, tokens, passwords, private keys |
| IaC scanning | Infrastructure configuration files | Public storage, overly permissive IAM, insecure container settings |
| Container scanning | Container image packages and OS libraries | Known vulnerable packages in an image |
| API security testing | Running API endpoints | API-specific weaknesses and unexpected behavior |
| Fuzz testing | Inputs and application behavior | Crashes, unexpected responses, input-handling bugs |

## How GitLab security scanning works
1. Add individual scanner templates to `.gitlab-ci.yml`, enable Auto DevOps where appropriate, or enforce scans with security policies.
2. GitLab evaluates the included jobs and their rules.
3. Eligible jobs run on configured GitLab Runners.
4. Scanner jobs produce security reports as job artifacts.
5. GitLab processes supported reports and presents findings in the pipeline, merge request, and security views where supported by the product tier and configuration.
6. The team triages findings, fixes vulnerabilities, and verifies remediation with another scan.

A scanner might not run if the project has no supported files, the job's rules do not match, or the required environment is missing. A successful scanner job does not necessarily mean the application has no vulnerabilities.

## Enable selected scanners

A starting point for a project using current GitLab security job templates:

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

Check each scanner's current documentation, availability, and prerequisites before using it. Some scanners or report features depend on GitLab tier, runner configuration, language, and project setup.

For a custom security stage, add the stage to `stages:` and override the scanner job stage as documented. Adding a stage alone does not move template jobs into it.

## Scanner templates and common prerequisites

### SAST
- Analyzes supported source code.
- Uses GitLab's SAST template and analyzer jobs.
- Results are provided in a SAST security report.
- Only supported languages and file types are analyzed.

### Secret detection
- Looks for secrets in repository content and commits according to the scanner's coverage rules.
- A historic scan may be needed to inspect earlier repository history.
- Revoke and rotate any exposed credential immediately; deleting it from the current file is not enough.

### Dependency scanning
- Analyzes supported dependency manifests and lockfiles.
- Identifies packages with known vulnerabilities.
- Findings depend on supported ecosystems and available advisory data.
- GitLab's newer dependency scanning v2 uses SBOM-based dependency resolution workflows.

### Container scanning
- Scans a container image for known vulnerabilities.
- Usually requires an image to be available in a registry or an archive passed from an earlier job.
- Self-managed runner requirements and supported architectures should be checked in the current documentation.

### DAST
- Tests a running application.
- Requires a reachable test target and should be restricted to systems you own or are explicitly authorized to test.
- Use a non-production environment and test accounts with limited permissions.

### IaC scanning
- Checks supported infrastructure-as-code files for insecure configurations.
- Add it to the pipeline with the current GitLab IaC scanning template and review the supported file types.

## Security reports
GitLab scanner jobs upload structured reports through `artifacts:reports`. Examples of report types include `sast`, `secret_detection`, `dependency_scanning`, `container_scanning`, and `dast`.

For a custom scanner integration, the report must follow GitLab's required schema and be declared under the correct `artifacts:reports` key. Merely naming a JSON file `gl-sast-report.json` does not make it a valid SAST report.

## Understanding findings
Prioritize findings using:
- Severity and confidence.
- Exploitability and exposure.
- Whether the affected component is reachable or used.
- Internet exposure and privilege level.
- Availability of a fix or upgrade.
- Business impact and compensating controls.

A vulnerability's severity is one input to triage, not the whole decision. Avoid automatically suppressing findings without documented justification and ownership.

## Safe pipeline design
- Run scans in merge request and default-branch workflows as appropriate.
- Protect credentials with masked/protected CI/CD variables or a secrets manager.
- Never print tokens or full environment variables in logs.
- Use isolated runners for untrusted merge-request code.
- Pin and review scanner images and templates according to organizational policy.
- Restrict DAST to authorized test targets.
- Use test data and non-production accounts.
- Retain reports according to organizational requirements.
- Treat scanner output as sensitive because it can contain source paths, code context, package names, and infrastructure details.

## Troubleshooting
- **No scanner job appears:** check template inclusion, `workflow: rules`, job rules, supported files, and project feature availability.
- **Pipeline says stage does not exist:** add the required stage or override the scanner job's stage.
- **Container scan cannot find image:** verify image build/push, registry authentication, and `CS_IMAGE` or image variables.
- **DAST cannot connect:** verify target URL, DNS, network access, TLS, and application readiness.
- **Secret scan misses older leaked credentials:** run the supported historic scan workflow.
- **Report is not displayed:** inspect job artifacts, report schema, and supported report type.
- **Job fails due to runner:** verify executor, architecture, network, disk space, and image-pull permissions.

## Suggested lab sequence
1. Enable SAST and inspect the generated job.
2. Add a deliberately insecure example in a local training repository and observe the finding.
3. Enable secret detection using a fake, nonfunctional training token.
4. Add a dependency manifest with an intentionally outdated lab dependency.
5. Build and scan a test container image.
6. Run DAST against a deliberately vulnerable local application only.
7. Triage findings and document fixes.

## References
- [GitLab security scanning overview](https://docs.gitlab.com/user/application_security/detect/)
- [Security configuration](https://docs.gitlab.com/user/application_security/detect/security_configuration/)
- [Pipeline secret detection](https://docs.gitlab.com/user/application_security/secret_detection/pipeline/)
- [Container scanning](https://docs.gitlab.com/user/application_security/container_scanning/)
- [Scan execution policies](https://docs.gitlab.com/user/application_security/policies/scan_execution_policies/)
