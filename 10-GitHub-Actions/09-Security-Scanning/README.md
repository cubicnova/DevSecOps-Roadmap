# 09 - Security Scanning

Security scanning integrates automated security checks into CI/CD workflows. This module covers SAST, SCA, secret scanning, container scanning, DAST, SARIF reporting, and secure pipeline design.

## Learning objectives

- Distinguish SAST, SCA, secret scanning, container scanning, IaC scanning, and DAST.
- Configure CodeQL in GitHub Actions.
- Run dependency and container vulnerability checks.
- Detect exposed credentials.
- Upload third-party SARIF results to GitHub Code Scanning.
- Define security quality gates and handle findings responsibly.

## Scanning categories

| Category | Purpose | Example tools |
|---|---|---|
| SAST | Find insecure source-code patterns | CodeQL, Semgrep |
| SCA | Find vulnerable dependencies | Dependabot, npm audit, OSV-Scanner |
| Secret scanning | Detect exposed credentials | GitHub secret scanning, Gitleaks |
| Container scanning | Find image/package vulnerabilities | Trivy |
| IaC scanning | Detect risky infrastructure configuration | Checkov, Trivy |
| DAST | Test a running application | OWASP ZAP |

## 1. CodeQL (SAST)

CodeQL analyzes source code for security vulnerabilities.

```yaml
name: CodeQL Security Analysis

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "23 3 * * 1"

permissions:
  contents: read
  security-events: write
  actions: read

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: javascript
      - name: Build (if required)
        run: echo "Add the project's build command here"
      - uses: github/codeql-action/analyze@v3
```

Choose languages and build steps for your project. Review current CodeQL documentation for supported languages and setup. Pin actions to reviewed full commit SHAs when stronger supply-chain assurance is required.

## 2. Dependency scanning (SCA)

For Node.js projects with a committed lockfile:

```yaml
name: Dependency Audit

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: npm
      - run: npm ci
      - run: npm audit --audit-level=high
```

Investigate affected dependency paths, available fixes, compatibility, and exploitability before accepting a risk exception.

## 3. Secret detection

Gitleaks can detect credential-like patterns in repository content and history:

```yaml
name: Secret Scan

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Review the action's current configuration and authentication requirements. Never commit a real secret for testing. If a real credential is exposed, revoke or rotate it immediately; removing it from the latest commit is not sufficient.

## 4. Container scanning

Trivy can scan a locally built container image:

```yaml
name: Container Security Scan

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t sample-app:local .
      - uses: aquasecurity/trivy-action@0.28.0
        with:
          image-ref: sample-app:local
          format: table
          severity: HIGH,CRITICAL
          exit-code: "1"
```

This expects a Dockerfile in the repository root. Review and update action versions deliberately; pin full commit SHAs for stronger integrity.

## 5. SARIF reporting

SARIF (Static Analysis Results Interchange Format) is a standard format for static analysis findings. A SARIF-compatible scanner can generate a report that GitHub Code Scanning can ingest:

```yaml
permissions:
  contents: read
  security-events: write

steps:
  - uses: actions/checkout@v4
  - name: Run scanner
    run: ./scanner --format sarif --output results.sarif
  - name: Upload SARIF
    if: always()
    uses: github/codeql-action/upload-sarif@v4
    with:
      sarif_file: results.sarif
      category: third-party-scanner
```

The scanner command is a placeholder. Replace it with a real SARIF-producing tool. Upload requires `security-events: write`; Code Scanning availability depends on repository type and enabled features. Use a distinct category for separate analyses of the same commit.

## 6. DAST

Dynamic testing requires a running application. Use a disposable test environment, define the exact authorized target, run a bounded scan, save results, and stop the environment even if scanning fails. Never run active DAST against production or third-party systems without explicit authorization and agreed scope.

## Quality gates and triage

- Define severity thresholds and exception ownership.
- Avoid `|| true` or `continue-on-error` on mandatory checks.
- Assign findings, assess reachability and exploitability, remediate, then rescan.
- Document accepted risks with owner, rationale, compensating controls, and expiry.
- Preserve reports carefully; do not publish secrets or sensitive data.

## Secure the scanning workflow

1. Grant only required token permissions.
2. Do not expose secrets to untrusted pull-request code.
3. Review third-party Actions and pin full commit SHAs where appropriate.
4. Use trusted runners and isolate privileged deployment jobs.
5. Treat scanner output and pull-request content as untrusted input.
6. Keep tools and rulesets updated.
7. Protect default branches and require review for workflow changes.

## Further reading

- [GitHub CodeQL](https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql)
- [Upload SARIF results](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/integrate-with-existing-tools/upload-sarif-file)
- [GitHub Actions security hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
- [Gitleaks](https://github.com/gitleaks/gitleaks)
- [Trivy](https://trivy.dev/)
- [OWASP ZAP](https://www.zaproxy.org/)
