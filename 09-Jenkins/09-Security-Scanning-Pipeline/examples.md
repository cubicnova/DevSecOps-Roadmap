# Examples — Security Scanning Pipeline

> Run these examples only in a repository, image registry, or test environment you are authorized to assess. Scanner commands and exit-code behavior can differ by version.

## Example 1: Secret scanning with Gitleaks

```bash
gitleaks detect \
  --source . \
  --report-format json \
  --report-path gitleaks-report.json
```

Review the report securely. If a real credential was committed, revoke or rotate it; deleting it from the latest commit does not guarantee it is gone from Git history.

## Example 2: SAST with Semgrep

```bash
semgrep scan --config auto --json --output semgrep-report.json .
```

For repeatable production use, review the selected rules and pin a tested ruleset or configuration. Auto-selected rules may change as tool behavior evolves.

## Example 3: Dependency and filesystem scan with Trivy

```bash
trivy fs \
  --scanners vuln \
  --format json \
  --output trivy-fs-report.json \
  .
```

Review whether the project contains lockfiles or manifests that the scanner recognizes. Keep the scanner database updated through an approved network path.

## Example 4: Infrastructure-as-Code scan with Checkov

```bash
checkov -d . -o json > checkov-report.json
```

Use the appropriate Checkov options for your chosen output and configuration. Redirecting standard output does not necessarily capture diagnostics printed to standard error.

## Example 5: Container image scan

```bash
trivy image \
  --format json \
  --output trivy-image-report.json \
  my-app:ci
```

Build and tag the image in the pipeline before this step. Use immutable digests for release verification when possible, and do not publish images containing secrets.

## Example 6: Declarative Jenkins pipeline with independent stages

```groovy
pipeline {
    agent { label 'security-scanner' }

    options {
        timestamps()
        timeout(time: 25, unit: 'MINUTES')
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Secret scan') {
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
                sh 'trivy fs --scanners vuln --format json --output trivy-fs.json .'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-fs.json', allowEmptyArchive: true
                }
            }
        }
    }
    post {
        always {
            echo 'Review stage results and archived reports.'
        }
    }
}
```

This basic example uses each scanner's default exit behavior. Before using it as a release gate, verify exit codes, define severity thresholds, and test both clean and intentionally vulnerable sample inputs.

## Example 7: Bind a scanner token from Jenkins Credentials

```groovy
withCredentials([string(credentialsId: 'scanner-api-token', variable: 'SCANNER_TOKEN')]) {
    sh '''
        set +x
        scanner-cli scan --token-env SCANNER_TOKEN
    '''
}
```

The `scanner-cli` command is a placeholder; replace it with the vendor's documented command and token mechanism. Do not put the token value in the Jenkinsfile, command-line arguments, artifacts, or console output. Limit the credential's scope and the users/jobs allowed to use it.

## Example 8: Simple report-presence check

```bash
test -s gitleaks-report.json
test -s semgrep-report.json
test -s trivy-fs-report.json
```

This verifies that report files exist and are non-empty; it does **not** validate report schema or determine whether findings violate policy. Use each tool's documented JSON/SARIF schema for automated parsing.
