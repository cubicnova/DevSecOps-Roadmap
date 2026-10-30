# Security Scanning - Solutions and Explanations

Use these reference solutions to validate your exercises. Review official documentation for current tool versions and supported features.

## Lab 1: CodeQL

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

For compiled languages, configure the required build process. CodeQL setup differs by language and repository. Review alerts in the Code Scanning interface when available.

## Lab 2: Dependency scanning

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: "22"
    cache: npm
- run: npm ci
- run: npm audit --audit-level=high
```

`npm ci` installs the lockfile-defined dependency tree. `npm audit` checks it against known advisories. Investigate direct and transitive paths, available fixes, compatibility, and exploitability.

## Lab 3: Secret scanning

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0
- uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

A full-history checkout can help inspect earlier commits. If a real credential is found, revoke or rotate it immediately and investigate its use. Removing the text from the current branch does not invalidate the credential.

## Lab 4: Container scan

```yaml
- name: Build image
  run: docker build -t sample-app:local .

- name: Scan image
  uses: aquasecurity/trivy-action@0.28.0
  with:
    image-ref: sample-app:local
    severity: HIGH,CRITICAL
    exit-code: "1"
```

Review package, installed version, fixed version, severity, and reachability. Update the base image or package and rebuild. Pin and maintain the action reference deliberately.

## Lab 5: SARIF upload

```yaml
permissions:
  contents: read
  security-events: write

steps:
  - uses: actions/checkout@v4
  - name: Run SARIF-producing scanner
    run: ./scanner --format sarif --output results.sarif
  - name: Upload findings
    if: always()
    uses: github/codeql-action/upload-sarif@v4
    with:
      sarif_file: results.sarif
      category: training-scanner
```

The scanner command is a placeholder. The report must be compatible with GitHub's supported SARIF format. `security-events: write` permits upload. A distinct category differentiates multiple analyses for one commit. Repository type and enabled features determine Code Scanning availability.

## Lab 6: Example quality-gate policy

| Finding | Suggested response |
|---|---|
| Critical | Block merge/deployment until fixed or formally accepted |
| High | Block according to policy; require security review |
| Medium | Track remediation with a due date |
| Low | Prioritize in routine maintenance |
| False positive | Document evidence and use a narrow reviewed suppression |
| Accepted risk | Record owner, reason, controls, and expiry |

A gate should be documented and consistent. Tune scanners before making every warning a hard failure.

## Lab 7: DAST safety

Target only an application instance created for the lab. Use an isolated environment, known local URL, bounded scan profile, and always stop the environment. Active scanning can alter data or affect availability; do not scan systems outside written authorization and scope.

## Lab 8: Pipeline design

A basic design uses independent jobs for SAST, dependency checks, and secret scanning. Add container scanning if the project builds images. Give each job minimal permissions and make deployment depend on the required checks. Do not expose deployment secrets to untrusted pull-request jobs.

## Common troubleshooting

| Symptom | Likely cause | Resolution |
|---|---|---|
| CodeQL unsupported language | Wrong language identifier or unsupported setup | Check CodeQL language support |
| CodeQL build fails | Missing dependencies/build steps | Add documented build commands and inspect logs |
| `npm ci` fails | Missing or inconsistent lockfile | Commit the correct lockfile |
| Secret scanner finds nothing | Shallow history, unsupported pattern, or config | Check scan scope with synthetic data |
| Trivy cannot find image | Image not built or tag mismatch | Verify build and `image-ref` |
| SARIF upload denied | Missing `security-events: write` or feature unavailable | Check permissions and repository Code Scanning access |
| SARIF rejected | Invalid schema or unsupported content | Validate SARIF 2.1.0 and inspect upload errors |
| Scan does not block merge | Check not required by branch protection or job is non-blocking | Configure required checks and propagate failures |

## Security answer guide

Use complementary scanners and define a policy for their results. Secure the pipeline with least-privilege permissions, reviewed action references, no secrets in untrusted jobs, safe log handling, and protected deployment environments. Scanning reduces risk; it does not prove software is vulnerability-free.

## Suggested grading rubric

| Area | Points |
|---|---:|
| CodeQL setup | 15 |
| Dependency scanning | 15 |
| Secret detection | 15 |
| Container scanning | 15 |
| SARIF integration | 15 |
| Quality-gate design | 10 |
| DAST scope and safety | 5 |
| Pipeline security review | 10 |
| **Total** | **100** |
