# Security Scanning - Practical Exercises

Perform these labs only in repositories and applications you own or are explicitly authorized to test. Use synthetic secrets and disposable environments.

## Lab 1: Configure CodeQL

1. Create a test repository with a small application.
2. Add a CodeQL workflow under `.github/workflows/`.
3. Configure the correct language and build steps if required.
4. Trigger a scan using a push or pull request.
5. Review the Code Scanning results and document one finding or why none were produced.

**Deliverable:** Workflow YAML, run evidence, and a finding summary.

## Lab 2: Dependency scanning

1. Use a sample Node.js project with a lockfile.
2. Add `npm ci` and `npm audit` to a workflow.
3. Set a documented severity threshold.
4. Review an advisory and its dependency path.
5. Update a vulnerable dependency in a test branch and rerun the scan.
6. Record whether the issue was resolved.

## Lab 3: Secret scanning

1. Add Gitleaks to a workflow.
2. Add a synthetic credential-like string in a disposable branch.
3. Run the scanner and observe its finding.
4. Remove the synthetic string and rerun.
5. Explain why a real leaked credential must be revoked or rotated even after its text is removed.

Never use a real token or password for this lab.

## Lab 4: Container scanning

1. Create a small Dockerfile for a sample application.
2. Build the image in GitHub Actions.
3. Run Trivy against the image.
4. Review package, installed version, fixed version, and severity.
5. Update the base image or package and rebuild.
6. Compare scan results.

## Lab 5: SARIF integration

1. Generate or use a sample SARIF report.
2. Validate that it uses SARIF 2.1.0.
3. Add `security-events: write` to workflow permissions.
4. Upload with `github/codeql-action/upload-sarif`.
5. Inspect Code Scanning if the repository has the required feature access.
6. Explain why categories distinguish multiple analyses.

## Lab 6: Design a security quality gate

Define policy for critical/high, medium/low, false positives, accepted risks, exception owners, and merge/deployment blocking. Implement one simple gate in a test workflow. Do not suppress mandatory scanner failures with `|| true`.

## Lab 7: DAST in a disposable environment

1. Launch a deliberately vulnerable application locally or in an isolated lab.
2. Define the exact authorized target URL.
3. Run a passive scan first.
4. Review alerts and evidence.
5. Use active scanning only with authorization and a disposable target.
6. Stop and clean up the environment even if scanning fails.

Do not scan public targets or production systems without written authorization and agreed scope.

## Lab 8: End-to-end pipeline review

Build separate jobs for SAST, dependency scanning, secret scanning, and (if relevant) container scanning. Review permissions, triggers, action references, logs, artifacts, and failure behavior.

## Completion checklist

- [ ] Distinguish SAST, SCA, secret scanning, container scanning, and DAST.
- [ ] Configure CodeQL.
- [ ] Run dependency and secret scans.
- [ ] Scan a container image.
- [ ] Understand SARIF and upload permissions.
- [ ] Define a security quality gate.
- [ ] Explain safe DAST scope and authorization.
