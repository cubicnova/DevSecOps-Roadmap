# Solutions — Security Scanning Pipeline

Use these as model answers and adapt them to your repository, scanners, and risk policy. Scanner flags and exit codes must be verified against the installed version.

## Solution 1: Example scan mapping

| Scan | Stage | Input | Output | Example gate |
|---|---|---|---|---|
| Secret scanning | Early validation | Git working tree | JSON report | Block confirmed live secrets |
| SAST | Before merge/release | Source code | JSON/SARIF | Block selected high-confidence critical issues |
| SCA | Before build/release | Lockfiles/manifests | JSON/SARIF | Block policy-defined vulnerable dependencies |
| IaC | Before deployment | Terraform/Kubernetes files | JSON report | Block critical insecure configurations |
| Container | After image build | Image tag/digest | JSON report | Block image release per risk policy |
| DAST | Test deployment | Authorized test URL | HTML/JSON report | Block selected exploitable findings |

## Solution 2: Secret scan response
- Save the report as a restricted build artifact.
- Verify a finding without copying the secret into logs or tickets.
- Revoke or rotate the credential immediately if it is genuine.
- Identify its owner and scope; inspect relevant access logs if exposure may have occurred.
- Remove the secret from source and, where necessary, history using an approved process.
- Add prevention such as pre-commit checks, least-privilege credentials, and secret scanning in CI.

Removing a secret from a file alone does not invalidate the credential and does not guarantee it is removed from repository history or forks.

## Solution 3: Example multi-stage pipeline
```groovy
pipeline {
    agent { label 'security-scanner' }
    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Secrets') {
            steps {
                sh 'gitleaks detect --source . --report-format json --report-path gitleaks.json'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'gitleaks.json', allowEmptyArchive: true
                }
            }
        }
        stage('SAST') {
            steps {
                sh 'semgrep scan --config auto --json --output semgrep.json .'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'semgrep.json', allowEmptyArchive: true
                }
            }
        }
        stage('SCA') {
            steps {
                sh 'trivy fs --scanners vuln --format json --output trivy.json .'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy.json', allowEmptyArchive: true
                }
            }
        }
    }
}
```

This is a starting point, not a universal release gate. If a scan exits non-zero, Jenkins may skip later stages while still running stage-level `post` actions. Test that behavior in your installed Jenkins version and pipeline configuration. Add a separate, tested policy-evaluation step if findings must be parsed independently from scanner execution status.

## Solution 4: Quality gate example

| Severity / case | Suggested action |
|---|---|
| Confirmed exposed credential | Fail and initiate credential rotation |
| Critical, high-confidence exploitable issue | Block release unless an approved exception applies |
| Medium finding | Track with remediation owner and deadline |
| Low finding | Record and prioritize according to context |
| Scanner unavailable or report malformed | Mark as scan failure; do not silently treat as clean |
| False positive | Require evidence, reviewer, scope, and expiry |

Severity labels are not identical across scanners. Combine severity with confidence, exploitability, asset criticality, exposure, and business requirements.

## Solution 5: Safe credential binding
- Create the token in **Manage Jenkins → Credentials** with the narrowest available scope.
- Reference its credential ID, not its value, in the Jenkinsfile.
- Bind it only around the command that requires it.
- Disable shell tracing before commands that might expose variables.
- Avoid command-line token arguments if the scanner supports environment-based authentication.
- Restrict job configuration and build-log access.
- Rotate the token if it is accidentally exposed.

Masking is a safeguard, not a guarantee. Avoid commands that print the environment or token.

## Solution 6: Failure test matrix

| Test | Expected behavior |
|---|---|
| Clean sample | Scan completes, report is present, gate passes |
| Known test finding | Report identifies finding and gate follows policy |
| Scanner executable missing | Scan stage fails as an execution error |
| Invalid report path | Scan fails or report-presence check catches missing output |
| Malformed report | Parser fails closed; build is not marked clean |
| Scanner timeout | Stage times out and produces a diagnosable failure |

Record actual results because tool versions and options change behavior.

## Solution 7: Missing report troubleshooting
1. Read the console log for the first relevant error.
2. Confirm the command ran on the expected agent and in the correct workspace.
3. Verify the scanner exists and is executable.
4. Check output-path permissions and whether the report flag is valid.
5. Check whether the scanner failed before report generation.
6. Confirm the archive glob matches the report location.
7. Correct the root cause and rerun; do not merely enable `allowEmptyArchive` to hide a missing report.

## Solution 8: Container scan controls
- Build from an approved base image and keep it updated.
- Scan the exact image intended for release.
- Record both human-readable tag and immutable digest.
- Archive the report with commit SHA, scanner version, and timestamp.
- Define vulnerability thresholds and exception handling.
- Restrict registry credentials and avoid publishing sensitive images.

## Solution 9: Pipeline threat model — sample findings

| Risk | Mitigation |
|---|---|
| Forked pull request can access release token | Do not bind release credentials to untrusted jobs |
| Shared agent reused between trusted and untrusted builds | Use isolated ephemeral agents or clean workspaces and identities |
| Scanner report publicly accessible | Restrict job/artifact access and retention |
| Scanner version floats without control | Pin and update through a tested process |
| Build ignores scanner findings | Add tested policy parsing and fail-closed behavior |
| Exception never expires | Require owner, rationale, approver, and expiry |
| Pipeline can reach unnecessary internal services | Limit agent network access |

## Final acceptance criteria
A strong solution demonstrates scan coverage, reproducible reports, explicit policy gates, safe credential handling, clear error behavior, and isolation between untrusted code and privileged stages.
