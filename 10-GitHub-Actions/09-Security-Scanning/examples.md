# Security Scanning - Examples

These are learning examples. Review tool versions, permissions, and project-specific configuration before production use.

## 1. CodeQL

```yaml
name: CodeQL
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
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
      - uses: github/codeql-action/analyze@v3
```

Select languages supported by your project; compiled languages may require a build step.

## 2. Node.js dependency audit

```yaml
name: NPM Dependency Audit
on:
  pull_request:
  push:
    branches: [main]
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

Requires `package.json` and `package-lock.json`.

## 3. Gitleaks

```yaml
name: Gitleaks Scan
on:
  push:
    branches: [main]
  pull_request:
permissions:
  contents: read
jobs:
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Use synthetic patterns only in a lab. Follow the current action documentation.

## 4. Trivy filesystem scan

```yaml
name: Filesystem Vulnerability Scan
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aquasecurity/trivy-action@0.28.0
        with:
          scan-type: fs
          scan-ref: .
          format: table
          severity: HIGH,CRITICAL
          exit-code: "1"
```

Tune exclusions and thresholds based on a documented policy. Review the action version before use.

## 5. Container image scan

```yaml
steps:
  - uses: actions/checkout@v4
  - run: docker build -t sample-app:local .
  - uses: aquasecurity/trivy-action@0.28.0
    with:
      image-ref: sample-app:local
      severity: HIGH,CRITICAL
      exit-code: "1"
```

Requires a Dockerfile in the workspace.

## 6. SARIF upload example

```yaml
name: Third-party SARIF Upload
on:
  workflow_dispatch:
permissions:
  contents: read
  security-events: write
jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate training SARIF
        run: |
          cat > results.sarif <<'SARIF'
          {
            "version": "2.1.0",
            "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
            "runs": [{
              "tool": {"driver": {"name": "TrainingScanner", "rules": []}},
              "results": []
            }]
          }
          SARIF
      - uses: github/codeql-action/upload-sarif@v4
        with:
          sarif_file: results.sarif
          category: training-scanner
```

This is an empty training report, not an actual security scan. Repository Code Scanning availability and permissions apply.

## 7. Security checks as separate jobs

```yaml
name: Security Checks
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  dependency-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: npm
      - run: npm ci
      - run: npm audit --audit-level=high

  source-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Replace with the project's SAST command"
```

Add actual tools and only the permissions they require.

## 8. DAST in a disposable environment (outline)

```yaml
name: DAST Training Outline
on:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  dast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Start test app
        run: docker compose up -d
      - name: Run approved scanner
        run: echo "Configure scanner for the local test URL"
      - name: Stop test app
        if: always()
        run: docker compose down
```

Define a health check, exact local target, and bounded scan profile before adding an active scanner.
