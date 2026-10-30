# 09 — Security Scanning Pipeline

## Overview
A security scanning pipeline integrates automated security checks into CI/CD so that issues can be identified before code or artifacts are released. This module shows how to design a Jenkins pipeline that runs multiple scanners, preserves reports, and applies clear quality gates.

The examples use common open-source tools and CLI patterns. Tool versions, output formats, flags, and exit codes can vary; verify commands against the version installed in your lab.

## Learning objectives
By the end of this module, you should be able to:
- Explain where SAST, SCA, secret, IaC, container, and DAST checks fit into a delivery pipeline.
- Build a declarative Jenkinsfile with separate scanning stages.
- Keep scanner credentials out of source code and logs.
- Archive machine-readable reports and make scan results reviewable.
- Define fail/pass policies and exceptions for security findings.
- Diagnose missing tools, malformed reports, timeouts, and false positives.
- Apply least privilege and isolate untrusted pull-request builds from sensitive credentials.

## Security scanning types
| Type | What it checks | Example tools |
|---|---|---|
| SAST | Source code patterns and insecure coding | Semgrep, CodeQL |
| SCA | Third-party libraries and known vulnerabilities | OWASP Dependency-Check, Trivy, Snyk |
| Secret scanning | Accidentally committed tokens or passwords | Gitleaks |
| IaC scanning | Terraform, Kubernetes, and deployment configuration | Checkov, Trivy |
| Container scanning | OS packages and application dependencies in images | Trivy |
| DAST | A running application from an external perspective | OWASP ZAP baseline scan |

Tool selection should reflect language, architecture, licensing, policy, and operational capacity. Running every scanner in every stage is not always necessary; prioritize coverage and actionable results.

## Pipeline design principles
1. **Fast feedback first:** run inexpensive checks early; place heavier scans where they fit.
2. **Separate stages:** make each scan independently visible and diagnosable.
3. **Reports as build artifacts:** retain machine-readable output and limit access to sensitive reports.
4. **Explicit quality gates:** define which findings fail a build, which create warnings, and who can approve exceptions.
5. **No secrets in code:** store scanner tokens in Jenkins Credentials and bind them only to the stages that need them.
6. **Safe testing:** scan only code, images, and test systems you are authorized to assess.
7. **Untrusted code isolation:** do not expose production credentials to forked pull requests or other untrusted build inputs.
8. **Reproducibility:** pin or control scanner versions and document configuration changes.

## Example workflow
1. Checkout source.
2. Run unit tests and basic validation.
3. Run secret scanning.
4. Run SAST and IaC checks.
5. Run SCA against dependency manifests or lockfiles.
6. Build an image and scan it before release.
7. Optionally deploy to an isolated test environment and run DAST.
8. Archive reports, evaluate policy, and publish an auditable result.

## Sample Jenkinsfile
The following illustrative pipeline assumes the agent already has the named scanner CLIs installed. Adjust commands and versions to match your tools. It deliberately uses `returnStatus` to collect results and then fails the pipeline when a configured blocking check fails.

```groovy
pipeline {
    agent { label 'security-scanner' }

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Secret Scan') {
            steps {
                script {
                    int rc = sh(
                        script: 'gitleaks detect --source . --report-format json --report-path gitleaks-report.json',
                        returnStatus: true
                    )
                    if (rc != 0) {
                        error("Secret scanning returned exit code ${rc}; review the report and scanner output.")
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'gitleaks-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('SAST') {
            steps {
                sh 'semgrep scan --config auto --json --output semgrep-report.json .'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'semgrep-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('Dependency Scan') {
            steps {
                sh 'trivy fs --scanners vuln --format json --output trivy-fs-report.json .'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-fs-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('IaC Scan') {
            steps {
                sh 'checkov -d . -o json > checkov-report.json'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'checkov-report.json', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            echo 'Security scanning stages finished. Review archived reports and stage status.'
        }
    }
}
```

**Important:** Scanner exit codes are not standardized. Some tools return non-zero for findings; others return non-zero for execution errors. Confirm each CLI's behavior and implement policy-aware parsing. Do not assume a successful command means no vulnerabilities were found.

## Reports and retention
- Archive JSON, SARIF, XML, or other supported output appropriate to the scanner.
- Avoid publishing full reports to a public job or repository if they reveal source paths, vulnerable components, or secret locations.
- Define retention based on audit and incident-response needs.
- Preserve scanner version, configuration, commit SHA, and timestamp for reproducibility.

## Quality gate model
A useful starting policy is:
- Block confirmed exposed secrets immediately.
- Block critical/high findings only when confidence, exploitability, and business policy support the decision.
- Track medium/low findings with owners and deadlines.
- Allow exceptions only with documented rationale, approver, compensating controls, and expiry date.
- Never suppress a finding simply to make the pipeline green.

## Troubleshooting
- **Scanner not found:** confirm tool installation and `PATH` on the actual Jenkins agent.
- **No report:** check working directory, output flags, permissions, and whether the scanner exited before writing the file.
- **Build always fails:** separate scanner execution errors from policy failures; inspect exit codes and logs.
- **Build always passes:** verify findings are actually parsed and the policy gate is connected to the scanner output.
- **Slow builds:** cache dependencies safely, parallelize independent scans, and use timeouts.
- **False positives:** document evidence and suppression expiry; keep suppression files reviewed.

## Further reading
- [Jenkins Pipeline Steps Reference](https://www.jenkins.io/doc/pipeline/steps/)
- [Jenkins Security Scan guidance](https://www.jenkins.io/doc/developer/security/scan/)
- [OWASP ZAP Automation Framework](https://www.zaproxy.org/docs/automate/)
- [Gitleaks](https://github.com/gitleaks/gitleaks)
- [Semgrep CLI](https://semgrep.dev/docs/cli-reference/)
- [Trivy](https://trivy.dev/latest/docs/)
- [Checkov](https://www.checkov.io/1.Welcome/Quick%20Start.html)
